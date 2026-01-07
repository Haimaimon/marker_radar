# utils/date_utils.py
"""
Date/time utilities for Market Radar.

Key rule:
- Internally work with timezone-aware datetimes in UTC.
- Convert to local timezone (e.g., Asia/Jerusalem) only for display.

Fixes:
- Correct parsing of RSS RFC822 dates like: "Wed, 07 Jan 2026 07:45 GMT"
- Prevent losing time by returning date-only objects (used previously)
- Accurate "within hours" checks
"""

from __future__ import annotations

from datetime import datetime, date, timedelta, timezone
from typing import Optional
import logging
import re
from email.utils import parsedate_to_datetime

logger = logging.getLogger("market_radar.date_utils")

try:
    # Python 3.9+
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None


def now_utc() -> datetime:
    """Return current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


def parse_datetime_utc(date_string: str) -> Optional[datetime]:
    """
    Parse many date formats into an AWARE datetime in UTC.

    Supports:
    - RSS RFC822: 'Wed, 07 Jan 2026 07:45 GMT'
    - ISO8601: '2026-01-07T07:45:00Z' / '2026-01-07T07:45:00+00:00'
    - Common date/time strings you already used (AlphaVantage etc.)
    - Falls back to regex date parsing if needed

    Returns:
        datetime (tz-aware, UTC) or None if parsing fails
    """
    if not date_string or not isinstance(date_string, str):
        return None

    s = date_string.strip()
    low = s.lower()

    # Relative-ish strings (best effort)
    if "today" in low:
        return now_utc()
    if "yesterday" in low:
        return now_utc() - timedelta(days=1)
    if "ago" in low:
        # Can't know exact delta reliably without NLP.
        # Don't block item; treat as recent.
        return now_utc()

    # 1) RSS RFC822 / email-style timestamps (BEST for RSS feeds)
    try:
        dt = parsedate_to_datetime(s)
        if dt is not None:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # 2) ISO8601 (with Z or offset)
    try:
        iso = s
        if iso.endswith("Z"):
            iso = iso[:-1] + "+00:00"
        dt = datetime.fromisoformat(iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # 3) Older supported formats (keep compatibility)
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y%m%dT%H%M%S",  # Alpha Vantage
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%b %d, %Y",
        "%B %d, %Y",
    ]

    for fmt in formats:
        try:
            # Keep original behavior: if only a date exists, time becomes 00:00
            dt = datetime.strptime(s, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except Exception:
            continue

    # 4) Regex fallback for YYYY-MM-DD or YYYY/MM/DD embedded in text
    pattern = r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})"
    match = re.search(pattern, s)
    if match:
        try:
            y, m, d = map(int, match.groups())
            return datetime(y, m, d, tzinfo=timezone.utc)
        except Exception:
            pass

    logger.debug(f"Failed to parse date string: {date_string}")
    return None


def parse_date(date_string: str) -> Optional[date]:
    """
    Backward-compatible helper:
    returns ONLY date, based on parse_datetime_utc().

    Note:
    Prefer parse_datetime_utc() wherever you care about hours/minutes.
    """
    dt = parse_datetime_utc(date_string)
    return dt.date() if dt else None


def is_within_days(date_string: str, days: int = 7) -> bool:
    """
    Check if a date_string is within the last X days (UTC).

    This is safe for older use cases (days-based filters).
    """
    dt = parse_datetime_utc(date_string)
    if not dt:
        return True  # don't block if unknown
    age = now_utc() - dt
    return age <= timedelta(days=days)


def is_within_hours(date_string: str, hours: int = 24) -> bool:
    """
    FIXED:
    Check if a date_string is within the last X hours (UTC).
    """
    dt = parse_datetime_utc(date_string)
    if not dt:
        return True  # don't block if unknown
    age_seconds = (now_utc() - dt).total_seconds()
    return age_seconds <= (hours * 3600)


def format_dt_for_display(dt_utc: Optional[datetime], tz_name: str = "Asia/Jerusalem") -> str:
    """
    Convert a UTC datetime into a display string in the requested timezone.

    If ZoneInfo is unavailable, it returns UTC formatted string.
    """
    if not dt_utc:
        return ""

    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)

    if ZoneInfo:
        local_dt = dt_utc.astimezone(ZoneInfo(tz_name))
    else:
        local_dt = dt_utc  # fallback to UTC

    return local_dt.strftime("%a, %d %b %Y %H:%M:%S %Z")


def format_date(date_obj: Optional[date]) -> str:
    """Format date as a readable string (kept for compatibility)."""
    if not date_obj:
        return ""
    return date_obj.strftime("%Y-%m-%d")

def today_in_tz(tz_name: str = "Asia/Jerusalem") -> date:
    dt = now_utc()
    if ZoneInfo:
        return dt.astimezone(ZoneInfo(tz_name)).date()
    return dt.date()  # fallback UTC


def is_today(date_string: str, tz_name: str = "Asia/Jerusalem") -> bool:
    dt = parse_datetime_utc(date_string)
    if not dt:
        return True  # if unknown, don't block
    if ZoneInfo:
        local_dt = dt.astimezone(ZoneInfo(tz_name))
        return local_dt.date() == today_in_tz(tz_name)
    # fallback UTC
    return dt.date() == now_utc().date()


def get_age_in_days(date_string: str, tz_name: str = "Asia/Jerusalem") -> int:
    dt = parse_datetime_utc(date_string)
    if not dt:
        return 0
    if ZoneInfo:
        local_date = dt.astimezone(ZoneInfo(tz_name)).date()
        return (today_in_tz(tz_name) - local_date).days
    return (now_utc().date() - dt.date()).days


def get_today(tz_name: str = "Asia/Jerusalem") -> str:
    return str(today_in_tz(tz_name))
