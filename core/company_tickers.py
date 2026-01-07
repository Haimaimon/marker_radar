"""
Company Name to Ticker Symbol Mapping

Loads:
- Built-in seed mappings (small, curated)
- Optional large JSON mapping: data/company_to_ticker.json (generated automatically)

Provides:
- normalize_company_name()
- get_company_to_ticker()
- get_aliases()
- get_all_tickers()
- get_company_names()
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Set, Optional
import json
import re

# ============================================================
# 1) Small curated seed (manual overrides / critical companies)
# ============================================================
SEED_COMPANY_TO_TICKER: Dict[str, str] = {
    # Big Tech
    "apple": "AAPL",
    "amazon": "AMZN",
    "alphabet": "GOOGL",
    "google": "GOOGL",
    "microsoft": "MSFT",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "tesla": "TSLA",

    # Your real cases
    "radnet": "RDNT",
    "rad net": "RDNT",
    "radnet inc": "RDNT",

    "glaxosmithkline": "GSK",
    "glaxo smith kline": "GSK",
}

SEED_ALIASES: Dict[str, str] = {
    # Ticker aliases
    "aapl": "AAPL",
    "amzn": "AMZN",
    "googl": "GOOGL",
    "goog": "GOOGL",
    "msft": "MSFT",
    "fb": "META",
    "nvda": "NVDA",
    "tsla": "TSLA",
    "gsk": "GSK",
    "rdnt": "RDNT",
}

# ============================================================
# 2) Normalization rules
# ============================================================
STOP_WORDS: Set[str] = {
    "inc", "incorporated", "corp", "corporation", "ltd", "limited",
    "company", "co", "plc", "group", "holdings", "holding",
    "technologies", "technology", "tech", "systems", "solutions",
    "the", "a", "an", "and",
}

BLACKLIST: Set[str] = {
    # General noise
    "usa", "us", "ceo", "cfo", "cto", "cio",
    "ipo", "etf", "esg", "ai", "ml", "api",
    "sec", "fda", "fcc", "ftc", "doj",
    "nft", "nfts", "pr", "hr", "it", "rd",
    "q1", "q2", "q3", "q4", "fy",

    # Dates / time
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec",
    "monday", "tuesday", "wednesday", "thursday", "friday",

    # Exchanges
    "nyse", "nasdaq", "amex", "otc",
}

# ============================================================
# 3) Paths & caches
# ============================================================
DEFAULT_JSON_PATH = Path("data") / "company_to_ticker.json"

_COMPANY_TO_TICKER: Optional[Dict[str, str]] = None
_ALIASES: Optional[Dict[str, str]] = None

_PUNCT_RE = re.compile(r"[^\w\s]+", re.UNICODE)


# ============================================================
# 4) Core helpers
# ============================================================
def normalize_company_name(name: str) -> str:
    """
    Normalize company name for matching.

    - lowercase
    - remove punctuation
    - remove stop words
    - collapse spaces
    """
    if not name:
        return ""

    name = name.lower()
    name = _PUNCT_RE.sub(" ", name)

    words = []
    for w in name.split():
        if w in STOP_WORDS:
            continue
        if w in BLACKLIST:
            continue
        if len(w) <= 1:
            continue
        words.append(w)

    return " ".join(words)


def _load_json_mapping(path: Path) -> Dict[str, str]:
    """
    Load mapping from JSON file:
    expected format: { "Company Name": "TICKER", ... }
    """
    if not path.exists():
        return {}

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    out: Dict[str, str] = {}
    if not isinstance(raw, dict):
        return out

    for company, ticker in raw.items():
        if not company or not ticker:
            continue
        norm = normalize_company_name(company)
        if not norm:
            continue
        out[norm] = str(ticker).upper().strip()

    return out


# ============================================================
# 5) Public API
# ============================================================
def get_company_to_ticker(json_path: Path = DEFAULT_JSON_PATH) -> Dict[str, str]:
    """
    Return merged mapping:
    - seed (manual, overrides)
    - JSON mapping (NASDAQ + S&P500)
    """
    global _COMPANY_TO_TICKER
    if _COMPANY_TO_TICKER is not None:
        return _COMPANY_TO_TICKER

    merged: Dict[str, str] = {}

    # Seed first (highest priority)
    for k, v in SEED_COMPANY_TO_TICKER.items():
        merged[normalize_company_name(k)] = v.upper().strip()

    # Auto JSON (lower priority)
    merged.update(_load_json_mapping(json_path))

    _COMPANY_TO_TICKER = merged
    return _COMPANY_TO_TICKER


def get_aliases() -> Dict[str, str]:
    global _ALIASES
    if _ALIASES is not None:
        return _ALIASES

    _ALIASES = {
        normalize_company_name(k): v.upper().strip()
        for k, v in SEED_ALIASES.items()
    }
    return _ALIASES


def get_all_tickers(json_path: Path = DEFAULT_JSON_PATH) -> Set[str]:
    m = get_company_to_ticker(json_path)
    a = get_aliases()
    tickers = set(m.values())
    tickers.update(a.values())
    return tickers


def get_company_names(json_path: Path = DEFAULT_JSON_PATH) -> Set[str]:
    return set(get_company_to_ticker(json_path).keys())
