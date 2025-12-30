"""
Market Data Manager
===================
Unified manager for multiple market data providers with automatic fallback.

Features:
- Multi-provider support (Finnhub, Polygon, yfinance)
- Automatic fallback on failure
- Provider priority configuration
- Caching for performance
- Rate limit management

Author: Market Radar Team
"""

from __future__ import annotations
import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class ProviderType(Enum):
    """Available market data providers."""
    FINNHUB = "finnhub"
    POLYGON = "polygon"
    YFINANCE = "yfinance"


class MarketDataManager:
    """
    Manages multiple market data providers with automatic fallback.
    
    Usage:
        manager = MarketDataManager()
        manager.add_provider(ProviderType.FINNHUB, finnhub_instance, priority=1)
        manager.add_provider(ProviderType.POLYGON, polygon_instance, priority=2)
        
        quote = manager.get_quote("AAPL")
        has_impact = manager.validate_market_impact("AAPL")
    """
    
    def __init__(self):
        """Initialize the market data manager."""
        self.providers: Dict[ProviderType, Any] = {}
        self.provider_priority: List[ProviderType] = []
        self.provider_stats: Dict[ProviderType, Dict[str, int]] = {}
        
    def add_provider(
        self,
        provider_type: ProviderType,
        provider_instance: Any,
        priority: int = 100
    ):
        """
        Add a market data provider.
        
        Args:
            provider_type: Type of provider (FINNHUB, POLYGON, YFINANCE)
            provider_instance: Instance of the provider
            priority: Priority (lower = higher priority, default: 100)
        """
        self.providers[provider_type] = {
            "instance": provider_instance,
            "priority": priority,
        }
        
        # Rebuild priority list
        self.provider_priority = sorted(
            self.providers.keys(),
            key=lambda p: self.providers[p]["priority"]
        )
        
        # Initialize stats
        self.provider_stats[provider_type] = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
        }
        
        logger.info(
            f"✅ Added {provider_type.value} provider (priority: {priority})"
        )
    
    def get_snapshot(self, ticker: str) -> Optional[Any]:
        """
        Get market snapshot from the first available provider.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            MarketSnapshot or None if all providers fail
        """
        for provider_type in self.provider_priority:
            provider = self.providers[provider_type]["instance"]
            stats = self.provider_stats[provider_type]
            stats["requests"] += 1
            
            try:
                snap = provider.get_snapshot(ticker)
                if snap and snap.price is not None:
                    stats["successes"] += 1
                    logger.debug(f"✅ {provider_type.value}: Got snapshot for {ticker}")
                    return snap
                else:
                    stats["failures"] += 1
                    logger.debug(f"⚠️  {provider_type.value}: No snapshot for {ticker}, trying next provider...")
            except Exception as e:
                stats["failures"] += 1
                logger.warning(
                    f"❌ {provider_type.value}: Error for {ticker}: {e}, trying next provider..."
                )
                continue
        
        logger.warning(f"❌ All providers failed for {ticker}")
        return None
    
    def validate_market_impact(
        self,
        ticker: str,
        min_gap_pct: float = 2.0,
        min_vol_spike: float = 1.3
    ) -> bool:
        """
        Validate market impact using the first available provider.
        
        Args:
            ticker: Stock ticker symbol
            min_gap_pct: Minimum price change percentage
            min_vol_spike: Minimum volume spike multiplier
            
        Returns:
            True if significant movement detected
        """
        for provider_type in self.provider_priority:
            provider = self.providers[provider_type]["instance"]
            
            try:
                result = provider.validate_market_impact(
                    ticker,
                    min_gap_pct=min_gap_pct,
                    min_vol_spike=min_vol_spike
                )
                logger.debug(
                    f"✅ {provider_type.value}: Validated {ticker} = {result}"
                )
                return result
            except Exception as e:
                logger.warning(
                    f"❌ {provider_type.value}: Validation error for {ticker}: {e}, trying next provider..."
                )
                continue
        
        logger.warning(f"❌ All providers failed validation for {ticker}")
        return False
    
    def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get company profile from the first available provider.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Company profile or None
        """
        for provider_type in self.provider_priority:
            provider = self.providers[provider_type]["instance"]
            
            try:
                # Check if provider has get_company_profile method
                if hasattr(provider, "get_company_profile"):
                    profile = provider.get_company_profile(ticker)
                    if profile:
                        logger.debug(
                            f"✅ {provider_type.value}: Got profile for {ticker}"
                        )
                        return profile
            except Exception as e:
                logger.debug(
                    f"⚠️  {provider_type.value}: Profile error for {ticker}: {e}"
                )
                continue
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all providers.
        
        Returns:
            Dictionary with provider statistics
        """
        stats = {}
        for provider_type, provider_stats in self.provider_stats.items():
            total = provider_stats["requests"]
            success = provider_stats["successes"]
            failure = provider_stats["failures"]
            success_rate = (success / total * 100) if total > 0 else 0
            
            stats[provider_type.value] = {
                "requests": total,
                "successes": success,
                "failures": failure,
                "success_rate": f"{success_rate:.1f}%",
                "priority": self.providers[provider_type]["priority"],
            }
        
        return stats
    
    def log_stats(self):
        """Log provider statistics."""
        stats = self.get_stats()
        
        logger.info("📊 Market Data Provider Statistics:")
        for provider_name, provider_stats in stats.items():
            logger.info(
                f"   {provider_name}: {provider_stats['requests']} requests, "
                f"{provider_stats['successes']} success, "
                f"{provider_stats['failures']} failures "
                f"({provider_stats['success_rate']} success rate)"
            )


def main():
    """Test the Market Data Manager."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    print("🚀 Testing Market Data Manager\n")
    print("=" * 80)
    
    manager = MarketDataManager()
    
    # Try to add Finnhub
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    if finnhub_key:
        from market_data.finnhub_provider import FinnhubProvider
        finnhub = FinnhubProvider(finnhub_key)
        manager.add_provider(ProviderType.FINNHUB, finnhub, priority=1)
        print("✅ Added Finnhub provider (priority 1)")
    else:
        print("⚠️  FINNHUB_API_KEY not found, skipping Finnhub")
    
    # Try to add Polygon
    polygon_key = os.getenv("POLYGON_API_KEY")
    if polygon_key:
        from market_data.polygon_provider import PolygonProvider
        polygon = PolygonProvider(polygon_key)
        manager.add_provider(ProviderType.POLYGON, polygon, priority=2)
        print("✅ Added Polygon provider (priority 2)")
    else:
        print("⚠️  POLYGON_API_KEY not found, skipping Polygon")
    
    # Add yfinance as fallback
    from market_data.yfinance_provider import YFinanceProvider
    yfinance = YFinanceProvider()
    manager.add_provider(ProviderType.YFINANCE, yfinance, priority=99)
    print("✅ Added yfinance provider (priority 99 - fallback)")
    
    print("\n" + "=" * 80)
    print("\n📊 Testing quotes with automatic fallback:\n")
    
    # Test tickers
    test_tickers = ["AAPL", "MSFT", "TSLA"]
    
    for ticker in test_tickers:
        print(f"\n🔍 Testing {ticker}:")
        print("-" * 80)
        
        # Get snapshot (will try providers in priority order)
        snap = manager.get_snapshot(ticker)
        if snap and snap.price:
            print(f"   Ticker: {snap.symbol}")
            print(f"   Price: ${snap.price:.2f}")
            if snap.prev_close:
                change = snap.price - snap.prev_close
                change_pct = (change / snap.prev_close) * 100
                print(f"   Change: {change:+.2f} ({change_pct:+.2f}%)")
        else:
            print(f"   ❌ Failed to get snapshot from all providers")
        
        # Validate impact
        has_impact = manager.validate_market_impact(ticker)
        print(f"   Impact: {'✅ YES' if has_impact else '❌ NO'}")
    
    print("\n" + "=" * 80)
    print("\n📊 Provider Statistics:\n")
    manager.log_stats()
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

