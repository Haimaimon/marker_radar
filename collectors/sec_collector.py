from __future__ import annotations
from typing import List
import logging
import feedparser
from core.models import NewsItem

logger = logging.getLogger("market_radar.sec")

class SECRSSCollector:
    """
    SEC EDGAR RSS – can be tuned to specific forms later.
    We start with SEC 'Latest Filings' RSS.
    """
    SEC_LATEST_FILINGS_RSS = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=100&output=atom"

    def fetch(self) -> List[NewsItem]:
        try:
            d = feedparser.parse(self.SEC_LATEST_FILINGS_RSS)
            out: List[NewsItem] = []
            entries = getattr(d, "entries", [])
            count = len(entries)

            for e in entries:
                title = getattr(e, "title", "").strip()
                link = getattr(e, "link", "").strip()
                published = getattr(e, "published", "") or getattr(e, "updated", "")
                summary = getattr(e, "summary", "") or getattr(e, "description", "")
                out.append(NewsItem(
                    source="SEC EDGAR",
                    title=title,
                    link=link,
                    published=published,
                    summary=summary,
                    raw={"feed": "SEC_LATEST_FILINGS"},
                ))
            
            logger.debug(f"🏛️  SEC EDGAR: fetched {count} filings")
            return out
            
        except Exception as e:
            logger.error(f"❌ Error fetching from SEC: {e}")
            return []
