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
EXCHANGE_TICKER = re.compile(r"\b(?:NASDAQ|NYSE|AMEX|OTC):\s*([A-Z]{1,5}(?:[.-][A-Z]{1,2})?)\b")
PAREN_TICKER = re.compile(r"\(([A-Z]{1,5}(?:[.-][A-Z]{1,2})?)\)")
DOLLAR_TICKER = re.compile(r"\$([A-Z]{1,5}(?:[.-][A-Z]{1,2})?)\b")
ALLCAPS_TOKEN = re.compile(r"\b([A-Z]{2,5}(?:[.-][A-Z]{1,2})?)\b")

# Cache for known tickers
_KNOWN_TICKERS = get_all_tickers()

# Pre-sorted keys (longest first = less false positives)
_COMPANY_KEYS = sorted(COMPANY_TO_TICKER.keys(), key=len, reverse=True)
_ALIAS_KEYS = sorted(ALIASES.keys(), key=len, reverse=True)

# Compile phrase regex cache for speed
_PHRASE_REGEX_CACHE: dict[str, re.Pattern] = {}

def _phrase_regex(phrase: str) -> re.Pattern:
    # word-boundary safe match for phrases, cached
    pat = _PHRASE_REGEX_CACHE.get(phrase)
    if pat:
        return pat
    pat = re.compile(r"\b" + re.escape(phrase) + r"\b", flags=re.IGNORECASE)
    _PHRASE_REGEX_CACHE[phrase] = pat
    return pat


def extract_ticker(title: str, summary: str) -> Optional[str]:
    """
    Extract ticker symbol from text using multiple strategies:

    1. Explicit formats: NASDAQ:AAPL, (AAPL), $AAPL
    2. Company name matching: "GlaxoSmithKline" → GSK
    3. Alias matching: "GSK plc" → GSK
    4. ALL-CAPS fallback: "NVDA beats earnings" → NVDA

    Returns the first match found, or None
    """
    text = f"{title} {summary}".strip()
    if not text:
        return None

    # Strategy 1: Explicit exchange prefix (highest confidence)
    m = EXCHANGE_TICKER.search(text)
    if m:
        return _validate_known_ticker(m.group(1))

    # Strategy 2: Parentheses format (high confidence)
    m = PAREN_TICKER.search(text)
    if m:
        return _validate_known_ticker(m.group(1))

    # Strategy 3: Dollar sign format
    m = DOLLAR_TICKER.search(text)
    if m:
        return _validate_known_ticker(m.group(1))

    # Strategy 4: Company name / alias mapping (medium confidence)
    ticker = _match_company_name(text)
    if ticker:
        return ticker

    # Strategy 5: ALL-CAPS token fallback (lower confidence)
    m = ALLCAPS_TOKEN.search(text)
    if m:
        return _validate_known_ticker(m.group(1))

    return None


def _validate_known_ticker(candidate: str) -> Optional[str]:
    if not candidate:
        return None
    t = candidate.strip().upper()
    if t in BLACKLIST:
        return None
    # only allow if we know it (prevents random ALLCAPS words)
    if t in _KNOWN_TICKERS:
        return t
    return None


def _match_company_name(text: str) -> Optional[str]:
    """
    Match company names in text efficiently.
    - Longest-first matching to avoid partial collisions
    - Word-boundary aware phrase matching
    - Normalized fallback as last resort
    """
    text_lower = text.lower()

    # Exact phrase match (best)
    for company in _COMPANY_KEYS:
        if company in BLACKLIST:
            continue
        if _phrase_regex(company).search(text_lower):
            return COMPANY_TO_TICKER[company]

    # Alias match
    for alias in _ALIAS_KEYS:
        if alias in BLACKLIST:
            continue
        if _phrase_regex(alias).search(text_lower):
            return ALIASES[alias]

    # Normalized fuzzy fallback
    normalized_text = normalize_company_name(text)
    if not normalized_text:
        return None

    for company in _COMPANY_KEYS:
        normalized_company = normalize_company_name(company)
        if len(normalized_company) >= 4 and normalized_company in normalized_text:
            return COMPANY_TO_TICKER[company]

    return None


def extract_all_tickers(text: str) -> list[str]:
    """
    Extract ALL ticker mentions from text (advanced use).
    Returns list of unique tickers found.
    """
    if not text:
        return []

    found: list[str] = []

    for pattern in (EXCHANGE_TICKER, PAREN_TICKER, DOLLAR_TICKER):
        for match in pattern.finditer(text):
            t = _validate_known_ticker(match.group(1))
            if t and t not in found:
                found.append(t)

    t2 = _match_company_name(text)
    if t2 and t2 not in found:
        found.append(t2)

    return found
