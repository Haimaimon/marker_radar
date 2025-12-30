#!/usr/bin/env python3
"""
Test date filtering functionality
"""

from utils.date_utils import is_today, parse_date, get_today, get_age_in_days
from datetime import datetime, timedelta

def test_date_parsing():
    """Test various date formats"""
    print("=" * 80)
    print("Date Parsing Tests")
    print("=" * 80)
    
    test_cases = [
        # Today's date in various formats
        datetime.now().strftime("%Y-%m-%d"),
        datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "Today",
        "2 hours ago",
        
        # Yesterday
        (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "Yesterday",
        
        # Other formats
        "Dec 29, 2025",
        "12/29/2025",
        "20251229T123000",
    ]
    
    print(f"\nToday is: {get_today()}\n")
    
    for date_str in test_cases:
        parsed = parse_date(date_str)
        today = is_today(date_str)
        age = get_age_in_days(date_str)
        
        status = "✅ TODAY" if today else "❌ OLD"
        print(f"{status} | {date_str:30} → {parsed} (age: {age} days)")


def test_filtering_logic():
    """Test filtering logic"""
    print("\n" + "=" * 80)
    print("Filtering Logic Test")
    print("=" * 80)
    
    # Simulate news items with different dates
    test_items = [
        ("Today's breaking news", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("Yesterday's news", (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")),
        ("Last week's news", (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")),
        ("No date provided", ""),
    ]
    
    print("\nWith ONLY_TODAY_NEWS=true:\n")
    
    for title, date_str in test_items:
        should_show = is_today(date_str) if date_str else True
        age = get_age_in_days(date_str) if date_str else None
        
        if should_show:
            print(f"✅ SHOW: {title:30} (date: {date_str or 'N/A'}, age: {age})")
        else:
            print(f"❌ SKIP: {title:30} (date: {date_str}, age: {age} days)")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Date Filtering System Test" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    test_date_parsing()
    test_filtering_logic()
    
    print("\n" + "=" * 80)
    print("Configuration Recommendations:")
    print("=" * 80)
    print()
    print("For DAILY NEWS ONLY (recommended):")
    print("  ONLY_TODAY_NEWS=true")
    print("  AUTO_CLEANUP_OLD_NEWS=true")
    print()
    print("For ALL NEWS (not recommended):")
    print("  ONLY_TODAY_NEWS=false")
    print("  AUTO_CLEANUP_OLD_NEWS=false")
    print()
    print("=" * 80)
    print("✅ Test complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()

