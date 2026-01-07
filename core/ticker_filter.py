"""
Ticker Filter - NASDAQ & S&P 500
=================================
Filters tickers to only major US indices (NASDAQ & S&P 500) to reduce noise.
"""

from __future__ import annotations
import logging
import json
import time
import re
from pathlib import Path
from typing import Set, Optional
import requests

logger = logging.getLogger(__name__)

_VALID_TICKER_RE = re.compile(r"^[A-Z]{1,5}([.-][A-Z]{1,2})?$")  # ✅ allows BRK.B / BF.B / RDS-A


class TickerFilter:
    CACHE_FILE = Path("ticker_cache.json")
    CACHE_TTL_SECONDS = 86400  # 24 hours

    FALLBACK_TICKERS = {
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA", "AMD", "INTC",
        "JPM", "JNJ", "V", "WMT", "PG", "MA", "HD", "CVX", "MRK", "ABBV",
        "KO", "PEP", "COST", "AVGO", "CSCO", "ADBE", "ACN", "NFLX", "DIS", "CRM",
        "VZ", "TMO", "NKE", "CMCSA", "MCD", "ABT", "ORCL", "TXN", "DHR", "UNP",
        "NEE", "LIN", "QCOM", "PM", "HON", "UPS", "RTX", "IBM", "AMGN", "LOW",
        "SPGI", "INTU", "BA", "EL", "CAT", "GS", "NOW", "SBUX", "BLK", "AXP",
        "GILD", "REGN", "VRTX", "BIIB", "MRNA", "BNTX",
        "PYPL", "AMAT", "ADI", "ISRG", "MDLZ", "BKNG", "LRCX", "SYK", "TJX", "ADP",
        "CI", "MMC", "ZTS", "CB", "DUK", "SO", "CME", "USB", "PNC", "TFC",
        "SCHW", "MS", "COF", "BK", "TRV", "AON", "ICE", "MCO", "AFL", "MET",
        # ✅ include dotted tickers in fallback too
        "BRK.B", "BF.B",
    }

    def __init__(self, cache_file: Optional[Path] = None):
        self.cache_file = cache_file or self.CACHE_FILE
        self.tickers: Set[str] = set()
        self.last_update: float = 0
        self._load_or_refresh()

    def _load_or_refresh(self) -> None:
        if self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text(encoding="utf-8"))
                self.tickers = set(data.get("tickers", []))
                self.last_update = data.get("timestamp", 0)

                age = time.time() - self.last_update
                if age < self.CACHE_TTL_SECONDS:
                    logger.info(f"✅ Loaded {len(self.tickers)} tickers from cache (age: {age/3600:.1f}h)")
                    return
                logger.info(f"⏰ Cache expired (age: {age/3600:.1f}h), refreshing...")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")

        self._refresh_tickers()

    def _refresh_tickers(self) -> None:
        logger.info("🔄 Refreshing ticker lists...")

        new_tickers: Set[str] = set()

        # S&P 500
        try:
            sp500 = self._get_sp500_tickers()
            new_tickers.update(sp500)
            logger.info(f"✅ Downloaded {len(sp500)} S&P 500 tickers")
        except Exception as e:
            logger.warning(f"Failed to download S&P 500 list: {e}")

        # NASDAQ
        try:
            nasdaq = self._get_nasdaq_tickers()
            new_tickers.update(nasdaq)
            logger.info(f"✅ Downloaded {len(nasdaq)} NASDAQ tickers")
        except Exception as e:
            logger.warning(f"Failed to download NASDAQ list: {e}")

        if not new_tickers:
            logger.warning("⚠️  Failed to download ticker lists, using fallback list")
            new_tickers = set(self.FALLBACK_TICKERS)

        # ✅ normalize + validate
        cleaned: Set[str] = set()
        for t in new_tickers:
            t2 = t.strip().upper().replace("/", "-")
            if _VALID_TICKER_RE.match(t2):
                cleaned.add(t2)

        self.tickers = cleaned
        self.last_update = time.time()

        try:
            cache_data = {
                "tickers": sorted(list(self.tickers)),
                "timestamp": self.last_update,
                "count": len(self.tickers),
            }
            self.cache_file.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")
            logger.info(f"💾 Saved {len(self.tickers)} tickers to cache")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def _get_sp500_tickers(self) -> Set[str]:
        try:
            import pandas as pd
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            tables = pd.read_html(url, storage_options={'User-Agent': 'Mozilla/5.0'})
            df = tables[0]
            # Wikipedia uses '.' for some tickers -> convert to '-' or keep '.'?
            # For US tickers, BRK.B is common; keep '.' format:
            symbols = df["Symbol"].astype(str).str.strip().str.upper()
            return set(symbols.tolist())
        except Exception:
            return set()

    def _get_nasdaq_tickers(self) -> Set[str]:
        url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&exchange=nasdaq"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            rows = r.json().get("data", {}).get("rows", [])
            tickers = set()
            for row in rows:
                sym = str(row.get("symbol", "")).strip().upper()
                if _VALID_TICKER_RE.match(sym):
                    tickers.add(sym)
            return tickers
        except Exception:
            return self._get_nasdaq_alternative()

    def _get_nasdaq_alternative(self) -> Set[str]:
        try:
            url = "http://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
            r = requests.get(url, timeout=30)
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
        age_hours = (time.time() - self.last_update) / 3600
        return {
            "total_tickers": len(self.tickers),
            "cache_age_hours": age_hours,
            "cache_valid": age_hours < (self.CACHE_TTL_SECONDS / 3600),
            "cache_file": str(self.cache_file),
        }


_global_filter: Optional[TickerFilter] = None

def get_ticker_filter() -> TickerFilter:
    global _global_filter
    if _global_filter is None:
        _global_filter = TickerFilter()
    return _global_filter

def is_major_ticker(ticker: Optional[str]) -> bool:
    return get_ticker_filter().is_valid_ticker(ticker)
