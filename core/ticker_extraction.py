from __future__ import annotations

import re
from typing import Optional

from .company_tickers import (
    get_company_to_ticker,
    get_aliases,
    BLACKLIST,
    normalize_company_name,
    get_all_tickers,
)

# Supports: BRK.B, BRK-B, BF.A, etc.
TICKER_RE = r"[A-Z]{1,6}(?:[.\-][A-Z]{1,2})?"

# ✅ Accept common exchange prefixes (case-insensitive) + variants
EXCHANGE_TICKER = re.compile(
    rf"\b(?:NASDAQ|NYSE|AMEX|OTC|NYSE\s+AMERICAN|NASDAQ\s+CM|NASDAQ\s+GM|NASDAQ\s+GS)\s*:\s*({TICKER_RE})\b",
    re.IGNORECASE,
)

# ✅ (RDNT) or ( RDNT )
PAREN_TICKER = re.compile(rf"\(\s*({TICKER_RE})\s*\)")

# ✅ $RDNT
DOLLAR_TICKER = re.compile(rf"\$\s*({TICKER_RE})\b")

# ✅ Delimited tokens like: "RadNet - RDNT" / "RadNet | RDNT" / "RadNet – RDNT"
DELIM_TICKER = re.compile(rf"(?:\s[-–|]\s)({TICKER_RE})\b")

# ✅ Any token fallback
ALLCAPS_TOKEN = re.compile(rf"\b({TICKER_RE})\b")


def extract_ticker(title: str, summary: str) -> Optional[str]:
    text = f"{title} {summary}"

    known_tickers = get_all_tickers()
    company_map = get_company_to_ticker()
    aliases = get_aliases()

    # Helper: validate candidate
    def _valid(cand: str) -> bool:
        if not cand:
            return False
        c = cand.upper().strip()
        if c.lower() in BLACKLIST:
            return False
        return c in known_tickers

    # 1) Explicit exchange (highest confidence)
    m = EXCHANGE_TICKER.search(text)
    if m:
        cand = m.group(1)
        if _valid(cand):
            return cand.upper()

    # 2) Parentheses (high confidence)
    m = PAREN_TICKER.search(text)
    if m:
        cand = m.group(1)
        if _valid(cand):
            return cand.upper()

    # 3) $TICKER
    m = DOLLAR_TICKER.search(text)
    if m:
        cand = m.group(1)
        if _valid(cand):
            return cand.upper()

    # 3.5) Delimiter patterns: " - RDNT" / " | RDNT"
    m = DELIM_TICKER.search(text)
    if m:
        cand = m.group(1)
        if _valid(cand):
            return cand.upper()

    # 4) Company-name / alias n-grams (best practical)
    ticker = _match_company_name_ngrams(text, company_map, aliases)
    if ticker:
        return ticker

    # 5) ALL-CAPS fallback (first valid)
    return _pick_best_allcaps(text, known_tickers)


def _match_company_name_ngrams(
    text: str,
    company_map: dict[str, str],
    aliases: dict[str, str],
) -> Optional[str]:
    """
    Tokenize normalized text and try n-grams (1..6 words).
    Prefer longest match.
    """
    norm = normalize_company_name(text)
    if not norm:
        return None

    tokens = norm.split()
    if not tokens:
        return None

    max_n = 6
    for n in range(min(max_n, len(tokens)), 0, -1):
        for i in range(0, len(tokens) - n + 1):
            phrase = " ".join(tokens[i : i + n])
            if phrase in company_map:
                return company_map[phrase]
            if phrase in aliases:
                return aliases[phrase]
    return None


def _pick_best_allcaps(text: str, known_tickers: set[str]) -> Optional[str]:
    """
    Scan tokens and return the first valid ticker that is not blacklisted.
    """
    for m in ALLCAPS_TOKEN.finditer(text):
        cand = m.group(1).upper().strip()
        if cand.lower() in BLACKLIST:
            continue
        if cand in known_tickers:
            return cand
    return None
