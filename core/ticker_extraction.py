from __future__ import annotations
import re
from typing import Optional
from .company_tickers import (
    COMPANY_TO_TICKER,
    ALIASES,
    BLACKLIST,
    normalize_company_name,
    get_all_tickers,
)

# Patterns for explicit ticker mentions
EXCHANGE_TICKER = re.compile(r"\b(?:NASDAQ|NYSE|AMEX|OTC):\s*([A-Z]{1,5}(?:\-[A-Z])?)\b")
PAREN_TICKER = re.compile(r"\(([A-Z]{1,5}(?:\-[A-Z])?)\)")
DOLLAR_TICKER = re.compile(r"\$([A-Z]{1,5}(?:\-[A-Z])?)\b")  # Twitter-style $AAPL
ALLCAPS_TOKEN = re.compile(r"\b([A-Z]{2,5}(?:\-[A-Z])?)\b")

# Cache for known tickers (performance optimization)
_KNOWN_TICKERS = get_all_tickers()


def extract_ticker(title: str, summary: str) -> Optional[str]:
    """
    Extract ticker symbol from text using multiple strategies:
    
    1. Explicit formats: NASDAQ:AAPL, (AAPL), $AAPL
    2. Company name matching: "Apple" → AAPL
    3. Alias matching: "Meta Platforms" → META
    4. ALL-CAPS fallback: "NVDA beats earnings" → NVDA
    
    Returns the first match found, or None
    """
    text = f"{title} {summary}"
    
    # Strategy 1: Explicit exchange prefix (highest confidence)
    m = EXCHANGE_TICKER.search(text)
    if m:
        return m.group(1)
    
    # Strategy 2: Parentheses format (high confidence)
    m = PAREN_TICKER.search(text)
    if m:
        return m.group(1)
    
    # Strategy 3: Dollar sign format (social media style)
    m = DOLLAR_TICKER.search(text)
    if m:
        ticker = m.group(1)
        if ticker in _KNOWN_TICKERS and ticker not in BLACKLIST:
            return ticker
    
    # Strategy 4: Company name mapping (medium confidence)
    ticker = _match_company_name(text)
    if ticker:
        return ticker
    
    # Strategy 5: ALL-CAPS token fallback (lower confidence)
    m = ALLCAPS_TOKEN.search(text)
    if m:
        candidate = m.group(1)
        # Only return if it's a known ticker and not blacklisted
        if candidate in _KNOWN_TICKERS and candidate not in BLACKLIST:
            return candidate
    
    return None


def _match_company_name(text: str) -> Optional[str]:
    """
    Try to match company names in text
    Uses fuzzy matching and handles common variations
    """
    text_lower = text.lower()
    
    # Try exact company name matches first
    for company, ticker in COMPANY_TO_TICKER.items():
        # Simple word boundary check
        if f" {company} " in f" {text_lower} ":
            return ticker
        # Check at start of text
        if text_lower.startswith(f"{company} "):
            return ticker
        # Check at end of text
        if text_lower.endswith(f" {company}"):
            return ticker
    
    # Try aliases
    for alias, ticker in ALIASES.items():
        if f" {alias} " in f" {text_lower} ":
            return ticker
        if text_lower.startswith(f"{alias} "):
            return ticker
        if text_lower.endswith(f" {alias}"):
            return ticker
    
    # Try normalized matching (more fuzzy)
    normalized_text = normalize_company_name(text)
    for company, ticker in COMPANY_TO_TICKER.items():
        normalized_company = normalize_company_name(company)
        if normalized_company and normalized_company in normalized_text:
            # Extra validation: company name should be significant portion
            if len(normalized_company) >= 4:  # At least 4 chars
                return ticker
    
    return None


def extract_all_tickers(text: str) -> list[str]:
    """
    Extract ALL ticker mentions from text (for advanced use)
    Returns list of unique tickers found
    """
    tickers = []
    
    # Find all explicit mentions
    for pattern in [EXCHANGE_TICKER, PAREN_TICKER, DOLLAR_TICKER]:
        for match in pattern.finditer(text):
            ticker = match.group(1)
            if ticker not in tickers and ticker not in BLACKLIST:
                tickers.append(ticker)
    
    # Find company names
    ticker = _match_company_name(text)
    if ticker and ticker not in tickers:
        tickers.append(ticker)
    
    return tickers
