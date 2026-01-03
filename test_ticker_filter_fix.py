#!/usr/bin/env python3
"""
Test Ticker Filter - Check if downloads work now
=================================================
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from core.ticker_filter import TickerFilter

print("\n" + "="*80)
print("🧪 Testing Ticker Filter Downloads")
print("="*80)

# Delete cache first
from pathlib import Path
cache = Path("ticker_cache.json")
if cache.exists():
    cache.unlink()
    print("✅ Deleted old cache")

# Create new filter (will trigger download)
print("\n🔄 Creating new filter (will download fresh data)...\n")

try:
    ticker_filter = TickerFilter()
    
    stats = ticker_filter.get_stats()
    
    print("\n" + "="*80)
    print("📊 Results:")
    print("="*80)
    print(f"Total tickers: {stats['total_tickers']}")
    print(f"Cache valid: {stats['cache_valid']}")
    print(f"Cache age: {stats['cache_age_hours']:.1f} hours")
    
    if stats['total_tickers'] > 1000:
        print("\n✅ SUCCESS! Downloaded full ticker lists!")
        print(f"   {stats['total_tickers']} tickers available")
    elif stats['total_tickers'] > 96:
        print("\n⚠️  PARTIAL SUCCESS")
        print(f"   Got {stats['total_tickers']} tickers (better than 96!)")
    else:
        print("\n❌ FAILED - Still using fallback list")
        print("   Only 96 tickers available")
        print("\n💡 Solutions:")
        print("   1. Install pandas: pip install pandas lxml html5lib")
        print("   2. Or disable: ENABLE_TICKER_FILTER=false")
    
    # Test some common tickers
    print("\n🧪 Testing common tickers:")
    test_tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMD"]
    for ticker in test_tickers:
        valid = ticker_filter.is_valid_ticker(ticker)
        print(f"   {ticker}: {'✅' if valid else '❌'}")
    
    print("\n" + "="*80 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

