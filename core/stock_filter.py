"""
Stock Market Relevance Filter
==============================
Ensures articles are related to stock market and finance.
"""

from __future__ import annotations
from typing import Tuple
import re

STOCK_MARKET_INDICATORS = {
    "stock", "stocks", "share", "shares", "equity", "equities",
    "nasdaq", "nyse", "dow jones", "s&p 500", "s&p500", "russell",

    "ticker", "ipo", "listing", "delisting", "halt", "trading",
    "market cap", "valuation", "price target",

    "securities", "adr", "etf", "index", "indices",

    "earnings", "revenue", "profit", "loss", "eps", "guidance",
    "dividend", "buyback", "split", "reverse split",
    "merger", "acquisition", "m&a", "takeover", "tender offer",
    "spac", "de-spac",

    # FDA/Clinical (biotech)
    "fda", "phase 1", "phase 2", "phase 3", "phase i", "phase ii", "phase iii",
    "clinical trial", "nda", "bla", "pdufa", "approval",

    "sec", "10-k", "10-q", "8-k", "s-1", "s-4", "proxy",
    "quarterly", "annual report", "filing",

    "analyst", "upgrade", "downgrade", "rating", "buy", "sell", "hold",
    "consensus",

    "surge", "plunge", "rally", "crash", "volatility", "volume",
    "pre-market", "after-hours", "intraday",

    "investor", "shareholders", "institutional", "retail",
    "hedge fund", "mutual fund", "portfolio",

    "market", "wall street", "stock market", "equity market",
    "publicly traded", "public company", "listed company",
}

EXCLUSION_TERMS = {
    "recipe", "cooking", "fashion", "sports", "celebrity", "entertainment",
    "movie", "music", "game", "gaming", "esports",
    "weather", "traffic", "crime",
    "real estate only", "cryptocurrency only", "nft",
}

# Ticker pattern in text (loose)
_TICKER_PATTERN = re.compile(r'\$[A-Z]{1,5}\b|\([A-Z]{1,5}\)|\b(?:NASDAQ|NYSE|AMEX|OTC):\s*[A-Z]{1,5}\b')


def _has_indicator(text: str, indicator: str) -> bool:
    """
    Better matching:
    - for multi-word indicators -> substring match (fast + reliable)
    - for single-word -> strict word boundary
    """
    if " " in indicator or "&" in indicator or "-" in indicator:
        return indicator in text
    return re.search(r"\b" + re.escape(indicator) + r"\b", text) is not None


def is_stock_market_related(title: str, summary: str) -> Tuple[bool, str]:
    text = f"{title} {summary}".lower().strip()
    if not text:
        return False, "Empty text"

    found = []
    for indicator in STOCK_MARKET_INDICATORS:
        if _has_indicator(text, indicator):
            found.append(indicator)

    if found:
        return True, f"Stock market indicators: {', '.join(found[:3])}"

    # If it contains a ticker-like mention, keep it
    if _TICKER_PATTERN.search(title + " " + summary):
        return True, "Contains ticker symbol"

    exclusion_found = [t for t in EXCLUSION_TERMS if t in text]
    if exclusion_found:
        return False, f"Not stock-related: {', '.join(exclusion_found[:2])}"

    return False, "No stock market indicators found"
