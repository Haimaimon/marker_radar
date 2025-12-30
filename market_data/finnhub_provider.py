"""
Finnhub Market Data Provider
=============================
Professional-grade real-time market data from Finnhub.io

Features:
- Real-time quotes (15-minute delayed for free tier)
- 60 API calls/minute (free tier)
- High reliability
- Additional data: market cap, PE ratio, etc.

API Docs: https://finnhub.io/docs/api

Author: Market Radar Team
"""

from __future__ import annotations
import logging
import time
from typing import Dict, Any, Optional
import requests
from market_data.base import MarketDataProvider, MarketSnapshot

logger = logging.getLogger(__name__)


class FinnhubProvider(MarketDataProvider):
    """
    Finnhub.io market data provider.
    
    Free Tier Limits:
    - 60 API calls/minute
    - 15-minute delayed quotes
    
    Paid Tiers:
    - Real-time quotes
    - Higher rate limits
    """
    
    BASE_URL = "https://finnhub.io/api/v1"
    
    def __init__(self, api_key: str, rate_limit_delay: float = 1.0):
        """
        Initialize Finnhub provider.
        
        Args:
            api_key: Finnhub API key
            rate_limit_delay: Seconds between requests (default: 1.0 for free tier)
        """
        self.api_key = api_key
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0.0
        self.session = requests.Session()
        self.session.headers.update({"X-Finnhub-Token": api_key})
        
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
            response = self.session.get(
                f"{self.BASE_URL}/quote",
                params={"symbol": ticker},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            # Finnhub returns empty dict or error field if ticker not found
            if not data or "error" in data:
                logger.debug(f"Finnhub: ticker {ticker} not found or error: {data}")
                return MarketSnapshot(
                    symbol=ticker,
                    price=None,
                    prev_close=None,
                    volume=None,
                    avg_volume_10d=None,
                )
            
            # Parse Finnhub response
            # Response format: {"c": 175.25, "d": 5.23, "dp": 3.08, "h": 176.00, ...}
            return MarketSnapshot(
                symbol=ticker,
                price=data.get("c"),  # Current price
                prev_close=data.get("pc"),  # Previous close
                volume=None,  # Finnhub quote doesn't include volume
                avg_volume_10d=None,  # Not available in quote endpoint
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Finnhub API error for {ticker}: {e}")
            return MarketSnapshot(
                symbol=ticker,
                price=None,
                prev_close=None,
                volume=None,
                avg_volume_10d=None,
            )
        except Exception as e:
            logger.exception(f"Unexpected error in Finnhub provider for {ticker}: {e}")
            return MarketSnapshot(
                symbol=ticker,
                price=None,
                prev_close=None,
                volume=None,
                avg_volume_10d=None,
            )
    
    def get_company_profile(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get company profile (market cap, industry, etc.)
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Company profile data or None
        """
        self._rate_limit()
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/stock/profile2",
                params={"symbol": ticker},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
            
            return {
                "ticker": ticker,
                "name": data.get("name", ""),
                "market_cap": data.get("marketCapitalization", 0),
                "industry": data.get("finnhubIndustry", ""),
                "exchange": data.get("exchange", ""),
                "currency": data.get("currency", "USD"),
                "ipo": data.get("ipo", ""),
                "provider": "finnhub",
            }
            
        except Exception as e:
            logger.debug(f"Finnhub profile error for {ticker}: {e}")
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
                f"Finnhub: {ticker} has {change_pct:.2f}% change (threshold: {min_gap_pct}%)"
            )
            return True
        
        logger.debug(
            f"Finnhub: {ticker} change {change_pct:.2f}% below threshold {min_gap_pct}%"
        )
        return False
    
    def _rate_limit(self):
        """Apply rate limiting (60 calls/minute = 1 call/second)."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()


def main():
    """Test Finnhub provider."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("FINNHUB_API_KEY")
    
    if not api_key:
        print("❌ FINNHUB_API_KEY not found in .env file")
        print("\n📝 Get your free API key at: https://finnhub.io/register")
        return
    
    print("🚀 Testing Finnhub Provider\n")
    print("=" * 80)
    
    provider = FinnhubProvider(api_key)
    
    # Test tickers
    tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "INVALID123"]
    
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
            
            # Validate impact
            has_impact = provider.validate_market_impact(ticker)
            print(f"   Impact: {'✅ YES' if has_impact else '❌ NO'}")
        else:
            print(f"   ❌ No data found")
        
        # Get profile
        profile = provider.get_company_profile(ticker)
        if profile:
            print(f"   Company: {profile['name']}")
            print(f"   Market Cap: ${profile['market_cap']:,.0f}M")
            print(f"   Industry: {profile['industry']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

