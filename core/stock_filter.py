"""
Stock Market Relevance Filter
==============================
Ensures articles are related to stock market and finance.
"""

from __future__ import annotations
from typing import Tuple

# Stock market indicators (if ANY of these appear, it's likely stock-related)
STOCK_MARKET_INDICATORS = {
    # Stock market terms
    "stock", "stocks", "share", "shares", "equity", "equities",
    "nasdaq", "nyse", "dow jones", "s&p 500", "s&p500", "russell",
    
    # Trading terms
    "ticker", "ipo", "listing", "delisting", "halt", "trading",
    "market cap", "valuation", "price target",
    
    # Financial instruments
    "securities", "adr", "etf", "index", "indices",
    
    # Company/market actions
    "earnings", "revenue", "profit", "loss", "eps", "guidance",
    "dividend", "buyback", "split", "reverse split",
    "merger", "acquisition", "m&a", "takeover", "tender offer",
    "ipo", "spac", "de-spac",
    
    # FDA/Clinical (biotech stocks)
    "fda", "phase 1", "phase 2", "phase 3", "phase i", "phase ii", "phase iii",
    "clinical trial", "nda", "bla", "pdufa", "approval",
    
    # Financial terms
    "sec", "10-k", "10-q", "8-k", "s-1", "s-4", "proxy",
    "quarterly", "annual report", "filing",
    
    # Analyst terms
    "analyst", "upgrade", "downgrade", "rating", "buy", "sell", "hold",
    "price target", "consensus",
    
    # Market movements
    "surge", "plunge", "rally", "crash", "volatility", "volume",
    "pre-market", "after-hours", "intraday",
    
    # Investment terms
    "investor", "shareholders", "institutional", "retail",
    "hedge fund", "mutual fund", "portfolio",
    
    # Specific financial terms
    "market", "wall street", "stock market", "equity market",
    "publicly traded", "public company", "listed company",
}

# Exclusion terms (if these appear WITHOUT stock indicators, probably not relevant)
EXCLUSION_TERMS = {
    # Non-stock content
    "recipe", "cooking", "fashion", "sports", "celebrity", "entertainment",
    "movie", "music", "game", "gaming", "esports",
    "weather", "traffic", "crime", "politics" "election",
    "real estate only", "cryptocurrency only", "nft",
}


def is_stock_market_related(title: str, summary: str) -> Tuple[bool, str]:
    """
    Check if article is related to stock market.
    
    Args:
        title: Article title
        summary: Article summary
        
    Returns:
        (is_relevant, reason)
    """
    text = f"{title} {summary}".lower()
    
    # Check for stock market indicators
    found_indicators = []
    for indicator in STOCK_MARKET_INDICATORS:
        # Use word boundaries to avoid false matches (e.g., "eps" in "recipe")
        import re
        pattern = r'\b' + re.escape(indicator) + r'\b'
        if re.search(pattern, text):
            found_indicators.append(indicator)
    
    # If we found stock market indicators, it's relevant
    if found_indicators:
        return True, f"Stock market indicators: {', '.join(found_indicators[:3])}"
    
    # Check if it has a ticker (even without other indicators)
    # Simple ticker pattern: $XXXX or (XXXX) or XXXX:
    import re
    ticker_pattern = r'\$[A-Z]{1,5}\b|\([A-Z]{1,5}\)|[A-Z]{2,5}:'
    if re.search(ticker_pattern, title + " " + summary):
        return True, "Contains ticker symbol"
    
    # Check for exclusion terms
    exclusion_found = []
    for term in EXCLUSION_TERMS:
        if term in text:
            exclusion_found.append(term)
    
    if exclusion_found and not found_indicators:
        return False, f"Not stock-related: {', '.join(exclusion_found[:2])}"
    
    # Default: reject if no stock market indicators found
    return False, "No stock market indicators found"

