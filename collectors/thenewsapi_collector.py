"""
TheNewsAPI Collector

Fetches news articles from TheNewsAPI
Documentation: https://www.thenewsapi.com/documentation
"""

from __future__ import annotations
from typing import List
import logging
import requests
from datetime import datetime, timedelta
from core.models import NewsItem

logger = logging.getLogger("market_radar.thenewsapi")


class TheNewsAPICollector:
    """
    Collector for TheNewsAPI
    
    Features:
    - Global news coverage
    - Multiple categories
    - Language filtering
    - Source filtering
    
    Rate Limits:
    - Free: 100 requests/day
    - Results: up to 100 articles per request
    """
    
    BASE_URL = "https://api.thenewsapi.com/v1/news/all"
    
    def __init__(
        self,
        api_token: str,
        categories: str = "business,tech",
        language: str = "en",
        limit: int = 50,
    ):
        """
        Initialize TheNewsAPI collector
        
        Args:
            api_token: Your TheNewsAPI token
            categories: Comma-separated categories (business, tech, sports, etc.)
            language: Language code (en, es, fr, etc.)
            limit: Number of articles to fetch (max 100)
        """
        self.api_token = api_token
        self.categories = categories
        self.language = language
        self.limit = limit
        self._last_fetch_time = None
    
    def fetch(self) -> List[NewsItem]:
        """
        Fetch latest news from TheNewsAPI
        
        Returns:
            List of NewsItem objects
        """
        if not self.api_token:
            logger.warning("TheNewsAPI token not configured")
            return []
        
        try:
            # Get news from last 24 hours
            published_after = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d")
            
            params = {
                "api_token": self.api_token,
                "categories": self.categories,
                "language": self.language,
                "limit": self.limit,
                "published_after": published_after,
            }
            
            logger.debug(f"Fetching from TheNewsAPI: categories={self.categories}, limit={self.limit}")
            
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Check for errors
            if "error" in data:
                logger.error(f"TheNewsAPI error: {data['error']}")
                return []
            
            # Parse articles
            articles = data.get("data", [])
            items = []
            
            for article in articles:
                try:
                    item = self._parse_article(article)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to parse article: {e}")
                    continue
            
            logger.info(f"📰 TheNewsAPI: fetched {len(items)} news items")
            self._last_fetch_time = datetime.now()
            
            return items
            
        except requests.exceptions.RequestException as e:
            logger.error(f"TheNewsAPI request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"TheNewsAPI collector error: {e}", exc_info=True)
            return []
    
    def _parse_article(self, article: dict) -> NewsItem:
        """
        Parse TheNewsAPI article into NewsItem
        
        Article structure:
        {
            "uuid": "...",
            "title": "...",
            "description": "...",
            "url": "...",
            "published_at": "2025-12-29 10:30:00",
            "source": "...",
            "categories": ["business"]
        }
        """
        # Parse timestamp
        published = article.get("published_at", "")
        
        # Create NewsItem
        item = NewsItem(
            source=f"TheNewsAPI ({article.get('source', 'Unknown')})",
            title=article.get("title", ""),
            link=article.get("url", ""),
            published=published,
            summary=article.get("description", ""),
            raw={
                "thenewsapi": {
                    "uuid": article.get("uuid"),
                    "source": article.get("source"),
                    "categories": article.get("categories", []),
                    "image_url": article.get("image_url"),
                }
            }
        )
        
        return item
    
    def get_usage_info(self) -> dict:
        """Get information about API usage"""
        return {
            "last_fetch": self._last_fetch_time,
            "api_token_set": bool(self.api_token),
            "rate_limit": "100 requests/day (free tier)",
            "categories": self.categories,
            "limit_per_request": self.limit,
        }

