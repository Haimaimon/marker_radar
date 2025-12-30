#!/usr/bin/env python3
"""
Test script for Alpha Vantage integration
"""

import sys
from config import settings
from collectors.alpha_vantage_collector import AlphaVantageCollector, test_connection

def main():
    print("=" * 80)
    print("Alpha Vantage API - Connection Test")
    print("=" * 80)
    
    # Check configuration
    if not settings.alpha_vantage_api_key:
        print("\n❌ Alpha Vantage API key not configured!")
        print("\nPlease add to .env:")
        print("  ALPHA_VANTAGE_API_KEY=YOUR_KEY_HERE")
        print("  ENABLE_ALPHA_VANTAGE=true")
        return 1
    
    print(f"\n✅ API Key configured: {settings.alpha_vantage_api_key[:10]}...")
    
    # Test connection
    print("\n🔌 Testing API connection...")
    
    if not test_connection(settings.alpha_vantage_api_key):
        print("❌ Connection test failed")
        return 1
    
    print("✅ Connection successful!")
    
    # Fetch sample news
    print("\n📰 Fetching sample news...")
    
    collector = AlphaVantageCollector(
        api_key=settings.alpha_vantage_api_key,
        topics="technology,earnings",
        limit=10,
    )
    
    items = collector.fetch()
    
    if not items:
        print("⚠️  No news items returned (might be rate limited)")
        return 0
    
    print(f"✅ Fetched {len(items)} news items")
    
    # Display sample
    print("\n" + "=" * 80)
    print("Sample News Items:")
    print("=" * 80)
    
    for i, item in enumerate(items[:5], 1):
        print(f"\n{i}. {item.title}")
        print(f"   Ticker: {item.ticker or 'N/A'}")
        print(f"   Published: {item.published}")
        print(f"   Link: {item.link[:60]}...")
        
        # Show sentiment if available
        if "alpha_vantage" in item.raw:
            av_data = item.raw["alpha_vantage"]
            print(f"   Sentiment: {av_data.get('sentiment_label')} ({av_data.get('sentiment_score', 0):.3f})")
    
    # Usage info
    print("\n" + "=" * 80)
    print("API Usage Information:")
    print("=" * 80)
    usage = collector.get_usage_info()
    for key, value in usage.items():
        print(f"  {key}: {value}")
    
    print("\n✅ All tests passed!")
    print("\nYou can now enable Alpha Vantage in your .env:")
    print("  ENABLE_ALPHA_VANTAGE=true")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

