"""
Test Market Data Providers
===========================
Tests the new market data system with Finnhub, Polygon, and yfinance fallback.

Usage:
    python test_market_data.py
"""

import sys
import os
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()


def main():
    print("📊 Testing Market Data System")
    print("=" * 80)
    
    # Check which providers are configured
    has_finnhub = bool(os.getenv("FINNHUB_API_KEY"))
    has_polygon = bool(os.getenv("POLYGON_API_KEY"))
    
    print("\n🔧 Configuration:")
    print(f"   Finnhub: {'✅ API key found' if has_finnhub else '❌ No API key'}")
    print(f"   Polygon: {'✅ API key found' if has_polygon else '❌ No API key'}")
    print(f"   yfinance: ✅ Always enabled (fallback)")
    
    if not has_finnhub and not has_polygon:
        print("\n⚠️  No premium providers configured!")
        print("\n📝 To get API keys:")
        print("   • Finnhub: https://finnhub.io/register (60 calls/min)")
        print("   • Polygon: https://polygon.io/dashboard/signup (5 calls/min)")
        print("\n   Add to .env:")
        print("   FINNHUB_API_KEY=your_key_here")
        print("   POLYGON_API_KEY=your_key_here")
        print("\n   Then enable in .env:")
        print("   ENABLE_FINNHUB=true")
        print("   ENABLE_POLYGON=true")
        print("\n🔄 Falling back to yfinance for this test...")
    
    print("\n" + "=" * 80)
    print("\n🚀 Initializing Market Data Manager...\n")
    
    from market_data.market_data_manager import MarketDataManager, ProviderType
    
    manager = MarketDataManager()
    
    # Add Finnhub (if available)
    if has_finnhub:
        from market_data.finnhub_provider import FinnhubProvider
        finnhub = FinnhubProvider(os.getenv("FINNHUB_API_KEY"))
        manager.add_provider(ProviderType.FINNHUB, finnhub, priority=1)
    
    # Add Polygon (if available)
    if has_polygon:
        from market_data.polygon_provider import PolygonProvider
        polygon = PolygonProvider(os.getenv("POLYGON_API_KEY"))
        manager.add_provider(ProviderType.POLYGON, polygon, priority=2)
    
    # Add yfinance (always)
    from market_data.yfinance_provider import YFinanceProvider
    yfinance = YFinanceProvider()
    manager.add_provider(ProviderType.YFINANCE, yfinance, priority=99)
    
    print("\n" + "=" * 80)
    print("\n📊 Testing quotes with automatic fallback:\n")
    
    # Test tickers
    test_tickers = ["AAPL", "MSFT", "TSLA", "NVDA"]
    
    for ticker in test_tickers:
        print(f"\n🔍 {ticker}:")
        print("-" * 80)
        
        # Get snapshot (will try providers in priority order)
        snap = manager.get_snapshot(ticker)
        if snap and snap.price:
            print(f"   ✅ Ticker: {snap.symbol}")
            print(f"   💰 Price: ${snap.price:.2f}")
            if snap.prev_close:
                change = snap.price - snap.prev_close
                change_pct = (change / snap.prev_close) * 100
                print(f"   📈 Change: {change:+.2f} ({change_pct:+.2f}%)")
            
            # Validate impact
            has_impact = manager.validate_market_impact(ticker, min_gap_pct=2.0)
            impact_status = "🔥 YES" if has_impact else "❄️  NO"
            print(f"   📊 Impact: {impact_status} (threshold: 2.0%)")
        else:
            print(f"   ❌ Failed to get snapshot from all providers")
    
    print("\n" + "=" * 80)
    print("\n📊 Provider Statistics:\n")
    
    stats = manager.get_stats()
    for provider_name, provider_stats in stats.items():
        print(f"   {provider_name}:")
        print(f"      Requests: {provider_stats['requests']}")
        print(f"      Successes: {provider_stats['successes']}")
        print(f"      Failures: {provider_stats['failures']}")
        print(f"      Success Rate: {provider_stats['success_rate']}")
        print(f"      Priority: {provider_stats['priority']}")
        print()
    
    print("=" * 80)
    print("\n✅ Test complete!")
    print("\n💡 Key features:")
    print("   • Automatic fallback: If primary fails, tries next provider")
    print("   • Priority-based: Finnhub (1) → Polygon (2) → yfinance (99)")
    print("   • Rate limiting: Each provider respects its own limits")
    print("   • Statistics: Track success/failure rates per provider")


if __name__ == "__main__":
    main()

