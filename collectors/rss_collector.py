from __future__ import annotations
from typing import List, Tuple
import logging
import feedparser
from core.models import NewsItem

logger = logging.getLogger("market_radar.rss")

class RSSCollector:
    def __init__(self, sources: List[Tuple[str, str]]):
        self.sources = sources

    def fetch(self) -> List[NewsItem]:
        out: List[NewsItem] = []
        for name, url in self.sources:
            try:
                d = feedparser.parse(url)
                entries = getattr(d, "entries", [])
                count = len(entries)
                
                for e in entries:
                    title = getattr(e, "title", "").strip()
                    link = getattr(e, "link", "").strip()
                    published = getattr(e, "published", "") or getattr(e, "updated", "")
                    summary = getattr(e, "summary", "") or getattr(e, "description", "")
                    out.append(NewsItem(
                        source=name,
                        title=title,
                        link=link,
                        published=published,
                        summary=summary,
                        raw={"feed": url},
                    ))
                
                logger.debug(f"📰 {name}: fetched {count} items")
                
            except Exception as e:
                logger.error(f"❌ Error fetching from {name}: {e}")
                
        return out
