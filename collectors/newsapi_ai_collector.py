"""
NewsAPI.ai Collector

Fetches news articles with advanced analytics from NewsAPI.ai
Documentation: https://newsapi.ai/documentation
"""

from __future__ import annotations
from typing import List
import logging
import requests
from datetime import datetime
from core.models import NewsItem

logger = logging.getLogger("market_radar.newsapi_ai")


class NewsAPIaiCollector:
    """
    Collector for NewsAPI.ai (Event Registry)
    
    Features:
    - Advanced news analytics
    - Concept tagging
    - Entity extraction
    - Sentiment analysis
    - Global coverage
    
    Rate Limits:
    - Free: 2,000 tokens/day
    - 1 article query = ~10 tokens
    """
    
    BASE_URL = "https://newsapi.ai/api/v1/article/getArticles"
    
    def __init__(
        self,
        api_key: str,
        keywords: str = None,
        concept_uri: str = None,
        category_uri: str = "news/Business",
        limit: int = 50,
    ):
        """
        Initialize NewsAPI.ai collector
        
        Args:
            api_key: Your NewsAPI.ai API key
            keywords: Keywords to search for (optional)
            concept_uri: Concept URI to filter by (optional)
            category_uri: Category URI (news/Business, news/Technology, etc.)
            limit: Number of articles to fetch (max 100)
        """
        self.api_key = api_key
        self.keywords = keywords
        self.concept_uri = concept_uri
        self.category_uri = category_uri
        self.limit = limit
        self._last_fetch_time = None
    
    def fetch(self) -> List[NewsItem]:
        """
        Fetch latest news from NewsAPI.ai
        
        Returns:
            List of NewsItem objects
        """
        if not self.api_key:
            logger.warning("NewsAPI.ai API key not configured")
            return []
        
        try:
            # Build query
            query = {
                "$query": {
                    "$and": []
                }
            }
            
            # Add filters
            if self.keywords:
                query["$query"]["$and"].append({
                    "keyword": self.keywords
                })
            
            if self.category_uri:
                query["$query"]["$and"].append({
                    "categoryUri": self.category_uri
                })
            
            # If no filters, get latest business/tech news
            if not query["$query"]["$and"]:
                query["$query"] = {
                    "$or": [
                        {"categoryUri": "news/Business"},
                        {"categoryUri": "news/Technology"}
                    ]
                }
            
            payload = {
                "query": query,
                "resultType": "articles",
                "articlesSortBy": "date",
                "articlesCount": self.limit,
                "includeArticleTitle": True,
                "includeArticleBody": True,
                "includeArticleBasicInfo": True,
                "includeArticleConcepts": True,
                "includeArticleCategories": True,
                "apiKey": self.api_key,
            }
            
            logger.debug(f"Fetching from NewsAPI.ai: category={self.category_uri}, limit={self.limit}")
            
            response = requests.post(
                self.BASE_URL,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Check for errors
            if "error" in data:
                logger.error(f"NewsAPI.ai error: {data['error']}")
                return []
            
            # Parse articles
            articles = data.get("articles", {}).get("results", [])
            items = []
            
            for article in articles:
                try:
                    item = self._parse_article(article)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to parse article: {e}")
                    continue
            
            logger.info(f"📰 NewsAPI.ai: fetched {len(items)} news items")
            self._last_fetch_time = datetime.now()
            
            return items
            
        except requests.exceptions.RequestException as e:
            logger.error(f"NewsAPI.ai request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"NewsAPI.ai collector error: {e}", exc_info=True)
            return []
    
    def _parse_article(self, article: dict) -> NewsItem:
        """
        Parse NewsAPI.ai article into NewsItem
        
        Article structure:
        {
            "uri": "...",
            "title": "...",
            "body": "...",
            "url": "...",
            "dateTime": "2025-12-29T10:30:00Z",
            "source": {"uri": "...", "title": "..."},
            "sentiment": 0.123,
            "concepts": [...]
        }
        """
        # Parse timestamp
        date_time = article.get("dateTime", "")
        if date_time:
            try:
                dt = datetime.fromisoformat(date_time.replace("Z", "+00:00"))
                published = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                published = date_time
        else:
            published = ""
        
        # Get source name
        source_info = article.get("source", {})
        source_name = source_info.get("title", "Unknown")
        
        # Get sentiment
        sentiment = article.get("sentiment")
        summary = article.get("body", "")[:500]  # First 500 chars
        if sentiment is not None:
            summary = f"[Sentiment: {sentiment:.2f}] {summary}"
        
        # Extract concepts (entities)
        concepts = article.get("concepts", [])
        concept_labels = [c.get("label", {}).get("eng", "") for c in concepts[:3]]
        
        # Create NewsItem
        item = NewsItem(
            source=f"NewsAPI.ai ({source_name})",
            title=article.get("title", ""),
            link=article.get("url", ""),
            published=published,
            summary=summary,
            raw={
                "newsapi_ai": {
                    "uri": article.get("uri"),
                    "sentiment": sentiment,
                    "concepts": concept_labels,
                    "categories": article.get("categories", []),
                    "source_uri": source_info.get("uri"),
                }
            }
        )
        
        return item
    
    def get_usage_info(self) -> dict:
        """Get information about API usage"""
        return {
            "last_fetch": self._last_fetch_time,
            "api_key_set": bool(self.api_key),
            "rate_limit": "2,000 tokens/day (free tier)",
            "category": self.category_uri,
            "limit_per_request": self.limit,
        }

