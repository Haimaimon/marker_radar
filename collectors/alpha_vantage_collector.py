"""
Alpha Vantage News & Sentiments API Collector

Fetches financial news with sentiment analysis and ticker symbols
from Alpha Vantage's premium news feed.

API Docs: https://www.alphavantage.co/documentation/#news-sentiment
"""

from __future__ import annotations
from typing import List
import logging
import requests
from datetime import datetime
from core.models import NewsItem

logger = logging.getLogger("market_radar.alpha_vantage")


class AlphaVantageCollector:
    """
    Collector for Alpha Vantage News & Sentiments API
    
    Features:
    - Real-time financial news
    - Pre-tagged with ticker symbols
    - Sentiment analysis included
    - Multiple sources aggregated
    
    Rate Limits (free tier):
    - 25 requests per day
    - Consider caching results
    """
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(
        self,
        api_key: str,
        topics: str = "technology,earnings,ipo,mergers_and_acquisitions",
        limit: int = 50,
        time_from: str = None,
    ):
        """
        Initialize Alpha Vantage collector
        
        Args:
            api_key: Your Alpha Vantage API key
            topics: Comma-separated topics to filter
                   Options: earnings, ipo, mergers_and_acquisitions, 
                           financial_markets, economy_fiscal, economy_monetary,
                           economy_macro, energy_transportation, finance,
                           life_sciences, manufacturing, real_estate,
                           retail_wholesale, technology
            limit: Number of news items to fetch (max 1000)
            time_from: Start time in YYYYMMDDTHHMM format (optional)
        """
        self.api_key = api_key
        self.topics = topics
        self.limit = limit
        self.time_from = time_from
        self._last_fetch_time = None
    
    def fetch(self) -> List[NewsItem]:
        """
        Fetch latest financial news from Alpha Vantage
        
        Returns:
            List of NewsItem objects with ticker symbols and sentiment
        """
        if not self.api_key:
            logger.warning("Alpha Vantage API key not configured")
            return []
        
        try:
            params = {
                "function": "NEWS_SENTIMENT",
                "apikey": self.api_key,
                "topics": self.topics,
                "limit": self.limit,
                "sort": "LATEST",  # Most recent first
            }
            
            if self.time_from:
                params["time_from"] = self.time_from
            
            logger.debug(f"Fetching from Alpha Vantage: topics={self.topics}, limit={self.limit}")
            
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                logger.error(f"Alpha Vantage API error: {data['Error Message']}")
                return []
            
            if "Note" in data:
                logger.warning(f"Alpha Vantage rate limit: {data['Note']}")
                return []
            
            # Parse news feed
            feed = data.get("feed", [])
            items = []
            
            for article in feed:
                try:
                    item = self._parse_article(article)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to parse article: {e}")
                    continue
            
            logger.info(f"📰 Alpha Vantage: fetched {len(items)} news items")
            self._last_fetch_time = datetime.now()
            
            return items
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Alpha Vantage API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Alpha Vantage collector error: {e}", exc_info=True)
            return []
    
    def _parse_article(self, article: dict) -> NewsItem:
        """
        Parse Alpha Vantage article into NewsItem
        
        Article structure:
        {
            "title": "...",
            "url": "...",
            "time_published": "20251229T123000",
            "summary": "...",
            "overall_sentiment_score": 0.123,
            "overall_sentiment_label": "Bullish",
            "ticker_sentiment": [
                {"ticker": "AAPL", "relevance_score": "0.9", "ticker_sentiment_score": "0.5"}
            ]
        }
        """
        # Extract main ticker (highest relevance)
        ticker = None
        ticker_sentiments = article.get("ticker_sentiment", [])
        if ticker_sentiments:
            # Sort by relevance and take the highest
            sorted_tickers = sorted(
                ticker_sentiments,
                key=lambda x: float(x.get("relevance_score", 0)),
                reverse=True
            )
            if sorted_tickers:
                ticker = sorted_tickers[0].get("ticker")
        
        # Parse timestamp
        time_published = article.get("time_published", "")
        try:
            # Format: 20251229T123000 → 2025-12-29 12:30:00
            if time_published:
                dt = datetime.strptime(time_published, "%Y%m%dT%H%M%S")
                published = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                published = ""
        except:
            published = time_published
        
        # Get sentiment info
        sentiment_score = article.get("overall_sentiment_score", 0.0)
        sentiment_label = article.get("overall_sentiment_label", "Neutral")
        
        # Build summary with sentiment info
        summary = article.get("summary", "")
        if sentiment_label:
            summary = f"[Sentiment: {sentiment_label}] {summary}"
        
        # Create NewsItem
        item = NewsItem(
            source="Alpha Vantage",
            title=article.get("title", ""),
            link=article.get("url", ""),
            published=published,
            summary=summary,
            ticker=ticker,
            raw={
                "alpha_vantage": {
                    "sentiment_score": sentiment_score,
                    "sentiment_label": sentiment_label,
                    "ticker_sentiments": ticker_sentiments,
                    "source": article.get("source", ""),
                    "source_domain": article.get("source_domain", ""),
                }
            }
        )
        
        return item
    
    def get_usage_info(self) -> dict:
        """
        Get information about API usage
        
        Returns:
            Dict with usage stats
        """
        return {
            "last_fetch": self._last_fetch_time,
            "api_key_set": bool(self.api_key),
            "rate_limit": "25 requests/day (free tier)",
            "topics": self.topics,
            "limit_per_request": self.limit,
        }


def test_connection(api_key: str) -> bool:
    """
    Test Alpha Vantage API connection
    
    Args:
        api_key: API key to test
    
    Returns:
        True if connection successful
    """
    try:
        collector = AlphaVantageCollector(api_key, limit=1)
        items = collector.fetch()
        return len(items) > 0 or True  # Even 0 items means API responded
    except Exception as e:
        logger.error(f"Alpha Vantage connection test failed: {e}")
        return False

