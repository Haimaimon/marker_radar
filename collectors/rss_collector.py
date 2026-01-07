from __future__ import annotations
from typing import List, Tuple
import logging
import time

import feedparser
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.models import NewsItem

logger = logging.getLogger("market_radar.rss")


def _build_session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        backoff_factor=0.8,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


class RSSCollector:
    def __init__(self, sources: List[Tuple[str, str]]):
        self.sources = sources
        self.session = _build_session()

    def fetch(self) -> List[NewsItem]:
        out: List[NewsItem] = []

        for name, url in self.sources:
            try:
                headers = {
                    "User-Agent": "MarketRadar/1.0 (+https://example.com)",
                    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "close",
                }

                resp = self.session.get(url, headers=headers, timeout=25)
                if resp.status_code >= 400:
                    raise RuntimeError(f"HTTP {resp.status_code}")

                # Feedparser parses bytes/text better than it fetches sometimes
                d = feedparser.parse(resp.content)

                entries = getattr(d, "entries", []) or []
                for e in entries:
                    title = getattr(e, "title", "").strip()
                    link = getattr(e, "link", "").strip()
                    published = getattr(e, "published", "") or getattr(e, "updated", "")
                    summary = getattr(e, "summary", "") or getattr(e, "description", "")
                    out.append(
                        NewsItem(
                            source=name,
                            title=title,
                            link=link,
                            published=published,
                            summary=summary,
                            raw={"feed": url},
                        )
                    )

                logger.debug(f"📰 {name}: fetched {len(entries)} items")

                # tiny sleep to be nice to RSS servers (especially PRN)
                time.sleep(0.2)

            except Exception as e:
                logger.error(f"❌ Error fetching from {name}: {e}")

        return out
