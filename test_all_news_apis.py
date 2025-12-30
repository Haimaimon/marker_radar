#!/usr/bin/env python3
"""
Test script for all News APIs
Tests Alpha Vantage, TheNewsAPI, and NewsAPI.ai
"""

import sys
from config import settings
from collectors.alpha_vantage_collector import AlphaVantageCollector
from collectors.thenewsapi_collector import TheNewsAPICollector
from collectors.newsapi_ai_collector import NewsAPIaiCollector

def test_alpha_vantage():
    """Test Alpha Vantage API"""
    print("\n" + "=" * 80)
    print("1. Alpha Vantage API Test")
    print("=" * 80)
    
    if not settings.alpha_vantage_api_key:
        print("❌ Not configured")
        return 0
    
    print(f"✅ API Key: {settings.alpha_vantage_api_key[:10]}...")
    
    try:
        collector = AlphaVantageCollector(
            api_key=settings.alpha_vantage_api_key,
            topics="technology,earnings",
            limit=10,
        )
        
        items = collector.fetch()
        print(f"✅ Fetched {len(items)} items")
        
        if items:
            print(f"\nSample: {items[0].title}")
            print(f"Ticker: {items[0].ticker or 'N/A'}")
        
        return len(items)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0


def test_thenewsapi():
    """Test TheNewsAPI"""
    print("\n" + "=" * 80)
    print("2. TheNewsAPI Test")
    print("=" * 80)
    
    if not settings.thenewsapi_token:
        print("❌ Not configured")
        return 0
    
    print(f"✅ Token: {settings.thenewsapi_token[:10]}...")
    
    try:
        collector = TheNewsAPICollector(
            api_token=settings.thenewsapi_token,
            categories="business,tech",
            limit=10,
        )
        
        items = collector.fetch()
        print(f"✅ Fetched {len(items)} items")
        
        if items:
            print(f"\nSample: {items[0].title}")
            print(f"Source: {items[0].source}")
        
        return len(items)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0


def test_newsapi_ai():
    """Test NewsAPI.ai"""
    print("\n" + "=" * 80)
    print("3. NewsAPI.ai Test")
    print("=" * 80)
    
    if not settings.newsapi_ai_key:
        print("❌ Not configured")
        return 0
    
    print(f"✅ API Key: {settings.newsapi_ai_key[:10]}...")
    
    try:
        collector = NewsAPIaiCollector(
            api_key=settings.newsapi_ai_key,
            category_uri="news/Business",
            limit=10,
        )
        
        items = collector.fetch()
        print(f"✅ Fetched {len(items)} items")
        
        if items:
            print(f"\nSample: {items[0].title}")
            print(f"Source: {items[0].source}")
        
        return len(items)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0


def main():
    """Run all tests"""
    print("=" * 80)
    print("News APIs - Comprehensive Test")
    print("=" * 80)
    
    total_items = 0
    
    # Test each API
    total_items += test_alpha_vantage()
    total_items += test_thenewsapi()
    total_items += test_newsapi_ai()
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Total items fetched: {total_items}")
    
    enabled_count = sum([
        settings.enable_alpha_vantage and bool(settings.alpha_vantage_api_key),
        settings.enable_thenewsapi and bool(settings.thenewsapi_token),
        settings.enable_newsapi_ai and bool(settings.newsapi_ai_key),
    ])
    
    print(f"APIs enabled: {enabled_count}/3")
    
    if total_items > 0:
        print("\n✅ All configured APIs working!")
        print("\nYou can now enable them in .env:")
        if settings.alpha_vantage_api_key:
            print("  ENABLE_ALPHA_VANTAGE=true")
        if settings.thenewsapi_token:
            print("  ENABLE_THENEWSAPI=true")
        if settings.newsapi_ai_key:
            print("  ENABLE_NEWSAPI_AI=true")
    else:
        print("\n⚠️  No APIs configured or all failed")
        print("\nPlease configure at least one API in .env")
    
    return 0 if total_items > 0 else 1


if __name__ == "__main__":
    sys.exit(main())

