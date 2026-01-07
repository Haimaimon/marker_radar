"""
Ticker Filter - NASDAQ & S&P 500
=================================
Filters tickers to only major US indices (NASDAQ & S&P 500) to reduce noise.
If NASDAQ is blocked, falls back to local data/company_to_ticker.json.
"""

from __future__ import annotations

import json
import logging
import re
import time
from io import StringIO
from pathlib import Path
from typing import Optional, Set

import requests

logger = logging.getLogger(__name__)

_VALID_TICKER_RE = re.compile(r"^[A-Z]{1,6}([.-][A-Z]{1,2})?$")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


class TickerFilter:
    PROJECT_ROOT = _project_root()

    CACHE_FILE = PROJECT_ROOT / "ticker_cache.json"
    CACHE_TTL_SECONDS = 86400  # 24 hours

    # ✅ Local DB from your script
    LOCAL_COMPANY_DB = PROJECT_ROOT / "data" / "company_to_ticker.json"

    # ✅ Always allow these (safety net)
    ALWAYS_ALLOW = {
        "RDNT",
        "BRK.B", "BRK-B",
        "BF.B", "BF-B",
    }

    FALLBACK_TICKERS = {
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA",
        "JPM", "JNJ", "V", "WMT", "PG", "MA", "HD", "MRK", "ABBV",
        "NFLX", "DIS", "CRM", "TMO", "ORCL", "QCOM",
        "BRK.B", "BF.B",
        "RDNT",
    }

    def __init__(self, cache_file: Optional[Path] = None):
        self.cache_file = cache_file or self.CACHE_FILE
        self.tickers: Set[str] = set()
        self.last_update: float = 0.0
        self._load_or_refresh()

    def _load_or_refresh(self) -> None:
        if self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text(encoding="utf-8"))
                self.tickers = set(data.get("tickers", []))
                self.last_update = float(data.get("timestamp", 0))

                age = time.time() - self.last_update
                if age < self.CACHE_TTL_SECONDS and len(self.tickers) > 0:
                    logger.info(f"✅ Loaded {len(self.tickers)} tickers from cache "
                                f"(age: {age/3600:.1f}h) -> {self.cache_file}")
                    return
                logger.info(f"⏰ Cache expired/empty, refreshing... (age: {age/3600:.1f}h)")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")

        self._refresh_tickers()

    def _refresh_tickers(self) -> None:
        logger.info("🔄 Refreshing ticker lists...")

        new_tickers: Set[str] = set()

        # 1) S&P 500
        sp500 = self._get_sp500_tickers()
        if sp500:
            new_tickers.update(sp500)
            logger.info(f"✅ Downloaded {len(sp500)} S&P 500 tickers")
        else:
            logger.warning("⚠️ Failed to download S&P 500 list")

        # 2) NASDAQ
        nasdaq = self._get_nasdaq_tickers()
        if nasdaq:
            new_tickers.update(nasdaq)
            logger.info(f"✅ Downloaded {len(nasdaq)} NASDAQ tickers")
        else:
            logger.warning("⚠️ NASDAQ download returned 0 tickers")

            # 3) Local DB fallback (your generated file)
            local = self._load_local_company_db_tickers()
            if local:
                new_tickers.update(local)
                logger.info(f"✅ Loaded {len(local)} tickers from local DB: {self.LOCAL_COMPANY_DB}")
            else:
                logger.warning("⚠️ Local company_to_ticker.json not available/empty")

        # 4) Final fallback if still empty
        if not new_tickers:
            logger.warning("⚠️ No tickers available -> using FALLBACK_TICKERS")
            new_tickers = set(self.FALLBACK_TICKERS)

        # 5) Clean + normalize + add dot/dash variants
        cleaned: Set[str] = set()
        for t in new_tickers:
            t2 = str(t).strip().upper().replace("/", "-")
            if _VALID_TICKER_RE.match(t2):
                cleaned.add(t2)

                # add paired versions
                if "." in t2:
                    cleaned.add(t2.replace(".", "-"))
                if "-" in t2:
                    cleaned.add(t2.replace("-", "."))

        # 6) Always allow safety net
        for t in self.ALWAYS_ALLOW:
            cleaned.add(t)
            if "." in t:
                cleaned.add(t.replace(".", "-"))
            if "-" in t:
                cleaned.add(t.replace("-", "."))

        self.tickers = cleaned
        self.last_update = time.time()

        try:
            cache_data = {
                "tickers": sorted(self.tickers),
                "timestamp": self.last_update,
                "count": len(self.tickers),
            }
            self.cache_file.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")
            logger.info(f"💾 Saved {len(self.tickers)} tickers to cache -> {self.cache_file}")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def _load_local_company_db_tickers(self) -> Set[str]:
        """
        Loads tickers from data/company_to_ticker.json (company -> ticker)
        """
        try:
            if not self.LOCAL_COMPANY_DB.exists():
                return set()
            data = json.loads(self.LOCAL_COMPANY_DB.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return set()

            out: Set[str] = set()
            for _, t in data.items():
                if not t:
                    continue
                sym = str(t).strip().upper().replace("/", "-")
                if _VALID_TICKER_RE.match(sym):
                    out.add(sym)
            return out
        except Exception:
            return set()

    def _get_sp500_tickers(self) -> Set[str]:
        try:
            import pandas as pd

            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()

            tables = pd.read_html(StringIO(r.text))
            df = tables[0]
            symbols = df["Symbol"].astype(str).str.strip().str.upper()
            return set(symbols.tolist())
        except Exception:
            return set()

    def _get_nasdaq_tickers(self) -> Set[str]:
        url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&exchange=nasdaq"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nasdaq.com/",
            "Origin": "https://www.nasdaq.com",
            "Connection": "keep-alive",
        }

        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            rows = r.json().get("data", {}).get("rows", []) or []

            tickers: Set[str] = set()
            for row in rows:
                sym = str(row.get("symbol", "")).strip().upper()
                if _VALID_TICKER_RE.match(sym):
                    tickers.add(sym)

            if len(tickers) == 0:
                raise RuntimeError("NASDAQ API returned 0 rows")

            return tickers
        except Exception:
            return self._get_nasdaq_alternative()

    def _get_nasdaq_alternative(self) -> Set[str]:
        try:
            url = "https://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()

            tickers = set()
            for line in r.text.splitlines()[1:]:
                parts = line.split("|")
                if not parts:
                    continue
                sym = parts[0].strip().upper()
                if _VALID_TICKER_RE.match(sym):
                    tickers.add(sym)
            return tickers
        except Exception:
            return set()

    def is_valid_ticker(self, ticker: Optional[str]) -> bool:
        if not ticker:
            return False
        t = ticker.strip().upper()
        return t in self.tickers

    def get_stats(self) -> dict:
        age_hours = (time.time() - self.last_update) / 3600 if self.last_update else 999999
        return {
            "total_tickers": len(self.tickers),
            "cache_age_hours": age_hours,
            "cache_valid": age_hours < (self.CACHE_TTL_SECONDS / 3600),
            "cache_file": str(self.cache_file),
            "local_company_db": str(self.LOCAL_COMPANY_DB),
        }


_global_filter: Optional[TickerFilter] = None


def get_ticker_filter() -> TickerFilter:
    global _global_filter
    if _global_filter is None:
        _global_filter = TickerFilter()
    return _global_filter


def is_major_ticker(ticker: Optional[str]) -> bool:
    return get_ticker_filter().is_valid_ticker(ticker)
