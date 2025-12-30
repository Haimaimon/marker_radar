"""
Date utilities for filtering and validating news by date
"""

from __future__ import annotations
from datetime import datetime, date, timedelta
from typing import Optional
import logging
import re

logger = logging.getLogger("market_radar.date_utils")


def get_today() -> date:
    """Get today's date"""
    return datetime.now().date()


def is_today(date_string: str) -> bool:
    """
    Check if a date string represents today
    
    Supports formats:
    - ISO: 2025-12-29, 2025-12-29T10:30:00
    - US: 12/29/2025
    - Descriptive: Dec 29, 2025
    - Relative: Today, yesterday
    
    Args:
        date_string: Date string to check
    
    Returns:
        True if the date is today, False otherwise
    """
    if not date_string:
        # No date = assume recent, allow through
        return True
    
    try:
        parsed_date = parse_date(date_string)
        if parsed_date:
            return parsed_date == get_today()
    except Exception as e:
        logger.debug(f"Could not parse date '{date_string}': {e}")
    
    # If can't parse, allow through (don't filter)
    return True


def parse_date(date_string: str) -> Optional[date]:
    """
    Parse various date formats into a date object
    
    Supports:
    - ISO: 2025-12-29, 2025-12-29T10:30:00Z
    - US: 12/29/2025
    - Timestamp: 20251229T123000
    - Relative: includes "ago", "yesterday", "today"
    
    Args:
        date_string: String containing a date
    
    Returns:
        date object or None if parsing fails
    """
    if not date_string or not isinstance(date_string, str):
        return None
    
    date_string = date_string.strip()
    
    # Check for relative dates
    if "today" in date_string.lower():
        return get_today()
    
    if "yesterday" in date_string.lower():
        return get_today() - timedelta(days=1)
    
    # Check for "X hours/minutes ago"
    if "ago" in date_string.lower():
        # Assume recent if mentioned as "ago"
        return get_today()
    
    # Try common formats
    formats = [
        "%Y-%m-%d",                    # 2025-12-29
        "%Y-%m-%dT%H:%M:%S",          # 2025-12-29T10:30:00
        "%Y-%m-%dT%H:%M:%SZ",         # 2025-12-29T10:30:00Z
        "%Y-%m-%dT%H:%M:%S.%f",       # 2025-12-29T10:30:00.123
        "%Y-%m-%dT%H:%M:%S.%fZ",      # 2025-12-29T10:30:00.123Z
        "%Y-%m-%d %H:%M:%S",          # 2025-12-29 10:30:00
        "%m/%d/%Y",                    # 12/29/2025
        "%d/%m/%Y",                    # 29/12/2025
        "%b %d, %Y",                   # Dec 29, 2025
        "%B %d, %Y",                   # December 29, 2025
        "%Y%m%dT%H%M%S",              # 20251229T123000 (Alpha Vantage)
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_string[:len(fmt)], fmt)
            return dt.date()
        except (ValueError, IndexError):
            continue
    
    # Try parsing ISO format with timezone
    try:
        if "T" in date_string:
            # Remove timezone info
            date_part = date_string.split("T")[0]
            return datetime.strptime(date_part, "%Y-%m-%d").date()
    except:
        pass
    
    # Try extracting date with regex
    # Pattern: YYYY-MM-DD or YYYY/MM/DD
    pattern = r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})"
    match = re.search(pattern, date_string)
    if match:
        try:
            year, month, day = match.groups()
            return date(int(year), int(month), int(day))
        except:
            pass
    
    return None


def get_date_range_today() -> tuple[datetime, datetime]:
    """
    Get datetime range for today (00:00 to 23:59)
    
    Returns:
        Tuple of (start_of_day, end_of_day)
    """
    today = get_today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    return start, end


def format_date_for_api(d: date) -> str:
    """Format date for API queries (YYYY-MM-DD)"""
    return d.strftime("%Y-%m-%d")


def get_age_in_days(date_string: str) -> Optional[int]:
    """
    Calculate how many days old a date string is
    
    Args:
        date_string: Date string to check
    
    Returns:
        Number of days old, or None if can't parse
    """
    parsed = parse_date(date_string)
    if parsed:
        return (get_today() - parsed).days
    return None


def is_within_hours(date_string: str, hours: int = 24) -> bool:
    """
    Check if date is within the last N hours
    
    Args:
        date_string: Date string to check
        hours: Number of hours to check within
    
    Returns:
        True if within the time window
    """
    age_days = get_age_in_days(date_string)
    if age_days is None:
        return True  # Can't determine, allow through
    
    return age_days * 24 <= hours


# For testing
if __name__ == "__main__":
    test_dates = [
        "2025-12-29",
        "2025-12-29T10:30:00",
        "2025-12-28",
        "Today",
        "Yesterday",
        "2 hours ago",
        "Dec 29, 2025",
        "20251229T123000",
        "12/29/2025",
    ]
    
    print(f"Today is: {get_today()}")
    print("\nTesting dates:")
    for test_date in test_dates:
        parsed = parse_date(test_date)
        is_today_result = is_today(test_date)
        age = get_age_in_days(test_date)
        print(f"  {test_date:30} → {parsed} | Today: {is_today_result} | Age: {age} days")

