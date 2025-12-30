#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Ticker Filter - NASDAQ & S&P 500
======================================
Tests the ticker filtering system.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from core.ticker_filter import TickerFilter


def main():
    print("\n" + "="*80)
    print("🧪 Testing Ticker Filter (NASDAQ & S&P 500)")
    print("="*80 + "\n")
    
    # Initialize filter
    print("📥 Loading ticker filter...")
    filter = TickerFilter()
    
    # Show stats
    stats = filter.get_stats()
    print(f"\n📊 Filter Statistics:")
    print(f"   Total tickers: {stats['total_tickers']}")
    print(f"   Cache age: {stats['cache_age_hours']:.1f} hours")
    print(f"   Cache valid: {'✅' if stats['cache_valid'] else '❌'}")
    print(f"   Cache file: {stats['cache_file']}")
    
    # Test known tickers
    print("\n" + "="*80)
    print("🧪 Testing Known Tickers")
    print("="*80 + "\n")
    
    test_cases = [
        # Should PASS (major stocks)
        ("AAPL", True, "Apple - NASDAQ"),
        ("MSFT", True, "Microsoft - NASDAQ"),
        ("GOOGL", True, "Google - NASDAQ"),
        ("TSLA", True, "Tesla - NASDAQ"),
        ("AMZN", True, "Amazon - NASDAQ"),
        ("META", True, "Meta - NASDAQ"),
        ("NVDA", True, "NVIDIA - NASDAQ"),
        ("JPM", True, "JPMorgan - NYSE/S&P 500"),
        ("JNJ", True, "Johnson & Johnson - NYSE/S&P 500"),
        ("V", True, "Visa - NYSE/S&P 500"),
        
        # Should FAIL (not in major indices or invalid)
        ("XXXX", False, "Invalid ticker"),
        ("ABCD", False, "Likely penny stock"),
        ("TEST", False, "Test ticker"),
        ("N/A", False, "No ticker"),
        ("", False, "Empty"),
        (None, False, "None"),
    ]
    
    passed = 0
    failed = 0
    
    for ticker, expected, description in test_cases:
        result = filter.is_valid_ticker(ticker)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        ticker_display = ticker if ticker else "<empty>"
        print(f"{status} | {ticker_display:10} | Expected: {expected:5} | Got: {result:5} | {description}")
    
    # Summary
    print("\n" + "="*80)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("="*80)
    
    if failed == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed - check ticker lists")
    
    # Sample tickers from the list
    print("\n" + "="*80)
    print("📋 Sample Tickers in List (first 20):")
    print("="*80 + "\n")
    
    sample = sorted(list(filter.tickers))[:20]
    for i, ticker in enumerate(sample, 1):
        print(f"{i:2}. {ticker}")
    
    if len(filter.tickers) > 20:
        print(f"\n... and {len(filter.tickers) - 20} more")
    
    print("\n" + "="*80)
    print("✅ Test completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

