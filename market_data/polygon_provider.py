"""
Polygon.io Market Data Provider
================================
Professional real-time market data from Polygon.io

Features:
- Real-time quotes
- 5 API calls/minute (free tier)
- High accuracy
- Rich historical data

API Docs: https://polygon.io/docs

Author: Market Radar Team
"""

from __future__ import annotations
import logging
import time
from typing import Dict, Any, Optional
import requests
from market_data.base import MarketDataProvider, MarketSnapshot

logger = logging.getLogger(__name__)


class PolygonProvider(MarketDataProvider):
    """
    Polygon.io market data provider.
    
    Free Tier Limits:
    - 5 API calls/minute
    - Real-time data
    - US stocks only
    
    Paid Tiers:
    - Higher rate limits
    - More exchanges
    - Advanced features
    """
    
    BASE_URL = "https://api.polygon.io"
    
    def __init__(self, api_key: str, rate_limit_delay: float = 12.0):
        """
        Initialize Polygon provider.
        
        Args:
            api_key: Polygon API key
            rate_limit_delay: Seconds between requests (default: 12.0 for free tier = 5 calls/min)
        """
        self.api_key = api_key
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0.0
        self.session = requests.Session()
        
    def get_snapshot(self, ticker: str) -> MarketSnapshot:
        """
        Get real-time quote for a ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            
        Returns:
            MarketSnapshot object
        """
        self._rate_limit()
        
        try:
            # Get previous close for comparison
            prev_close_response = self.session.get(
                f"{self.BASE_URL}/v2/aggs/ticker/{ticker}/prev",
                params={"apiKey": self.api_key},
                timeout=5
            )
            prev_close_response.raise_for_status()
            prev_data = prev_close_response.json()
            
            if prev_data.get("status") != "OK" or not prev_data.get("results"):
                logger.debug(f"Polygon: ticker {ticker} not found or no data")
                return MarketSnapshot(
                    symbol=ticker,
                    price=None,
                    prev_close=None,
                    volume=None,
                    avg_volume_10d=None,
                )
            
            prev_close = prev_data["results"][0]["c"]
            prev_volume = prev_data["results"][0].get("v")
            
            # Get current snapshot
            self._rate_limit()
            snapshot_response = self.session.get(
                f"{self.BASE_URL}/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}",
                params={"apiKey": self.api_key},
                timeout=5
            )
            snapshot_response.raise_for_status()
            snapshot_data = snapshot_response.json()
            
            if snapshot_data.get("status") != "OK" or not snapshot_data.get("ticker"):
                logger.debug(f"Polygon: no snapshot for {ticker}")
                return MarketSnapshot(
                    symbol=ticker,
                    price=None,
                    prev_close=prev_close,
                    volume=None,
                    avg_volume_10d=None,
                )
            
            tick = snapshot_data["ticker"]
            
            # Parse Polygon response
            current_price = tick.get("day", {}).get("c", prev_close)
            volume = tick.get("day", {}).get("v")
            
            return MarketSnapshot(
                symbol=ticker,
                price=current_price,
                prev_close=prev_close,
                volume=volume,
                avg_volume_10d=prev_volume,  # Approximation: using prev day volume
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Polygon API error for {ticker}: {e}")
            return MarketSnapshot(
                symbol=ticker,
                price=None,
                prev_close=None,
                volume=None,
                avg_volume_10d=None,
            )
        except Exception as e:
            logger.exception(f"Unexpected error in Polygon provider for {ticker}: {e}")
            return MarketSnapshot(
                symbol=ticker,
                price=None,
                prev_close=None,
                volume=None,
                avg_volume_10d=None,
            )
    
    def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get company details.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Company details or None
        """
        self._rate_limit()
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/v3/reference/tickers/{ticker}",
                params={"apiKey": self.api_key},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK" or not data.get("results"):
                return None
            
            results = data["results"]
            
            return {
                "ticker": ticker,
                "name": results.get("name", ""),
                "market_cap": results.get("market_cap", 0),
                "industry": results.get("sic_description", ""),
                "exchange": results.get("primary_exchange", ""),
                "currency": results.get("currency_name", "USD"),
                "type": results.get("type", ""),
                "provider": "polygon",
            }
            
        except Exception as e:
            logger.debug(f"Polygon profile error for {ticker}: {e}")
            return None
    
    def validate_market_impact(
        self, 
        ticker: str, 
        min_gap_pct: float = 2.0,
        min_vol_spike: float = 1.3
    ) -> bool:
        """
        Validate if ticker has significant market movement.
        
        Args:
            ticker: Stock ticker symbol
            min_gap_pct: Minimum price change percentage (default: 2.0%)
            min_vol_spike: Minimum volume spike multiplier (default: 1.3x)
            
        Returns:
            True if significant movement detected
        """
        snap = self.get_snapshot(ticker)
        if not snap.price or not snap.prev_close or snap.prev_close == 0:
            return False
        
        # Check price change
        change_pct = abs((snap.price - snap.prev_close) / snap.prev_close * 100)
        if change_pct >= min_gap_pct:
            logger.debug(
                f"Polygon: {ticker} has {change_pct:.2f}% change (threshold: {min_gap_pct}%)"
            )
            return True
        
        logger.debug(
            f"Polygon: {ticker} change {change_pct:.2f}% below threshold {min_gap_pct}%"
        )
        return False
    
    def _rate_limit(self):
        """Apply rate limiting (5 calls/minute = 1 call every 12 seconds)."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()


def main():
    """Test Polygon provider."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("POLYGON_API_KEY")
    
    if not api_key:
        print("❌ POLYGON_API_KEY not found in .env file")
        print("\n📝 Get your free API key at: https://polygon.io/dashboard/signup")
        return
    
    print("🚀 Testing Polygon Provider\n")
    print("=" * 80)
    
    provider = PolygonProvider(api_key)
    
    # Test tickers
    tickers = ["AAPL", "MSFT", "TSLA", "NVDA"]
    
    for ticker in tickers:
        print(f"\n📊 Testing {ticker}:")
        print("-" * 80)
        
        # Get snapshot
        snap = provider.get_snapshot(ticker)
        if snap.price:
            print(f"   Price: ${snap.price:.2f}")
            if snap.prev_close:
                change = snap.price - snap.prev_close
                change_pct = (change / snap.prev_close) * 100
                print(f"   Change: {change:+.2f} ({change_pct:+.2f}%)")
            if snap.volume:
                print(f"   Volume: {snap.volume:,}")
            
            # Validate impact
            has_impact = provider.validate_market_impact(ticker)
            print(f"   Impact: {'✅ YES' if has_impact else '❌ NO'}")
        else:
            print(f"   ❌ No data found")
        
        print()
    
    print("=" * 80)
    print("\n⚠️  Note: Polygon free tier has 5 calls/minute limit.")
    print("   This test uses 2 calls per ticker (prev close + snapshot).")


if __name__ == "__main__":
    main()

