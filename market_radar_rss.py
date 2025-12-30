# market_radar_rss.py
from __future__ import annotations

import time
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Tuple
import feedparser
import pandas as pd


# ============
# RSS SOURCES
# ============
RSS_SOURCES = [
    # GlobeNewswire categories list page exists; pick feeds you want from there.
    # Example: "Press Releases" feed (you can add more categories later)
    ("GlobeNewswire - Press Releases", "https://www.globenewswire.com/rss/news-releases"),
    # PR Newswire main feed / categories (PR has many category feeds)
    ("PR Newswire - Main", "https://www.prnewswire.com/rss/news-releases-list.rss"),
]

# =========================
# IMPACT KEYWORDS (RULES)
# =========================
KEYWORDS = {
    # M&A
    "merger": 35,
    "acquisition": 35,
    "acquire": 25,
    "definitive agreement": 35,
    "purchase agreement": 25,
    "tender offer": 35,
    "s-4": 35,

    # Clinical / biotech
    "phase 3": 35,
    "phase iii": 35,
    "phase 2": 25,
    "phase ii": 25,
    "phase 1": 15,
    "phase i": 15,
    "topline": 30,
    "primary endpoint": 35,
    "met its primary endpoint": 45,
    "statistically significant": 30,
    "fda approval": 45,
    "fda accepts": 35,
    "nda": 25,
    "bla": 25,
    "fast track": 20,
    "breakthrough therapy": 25,
    "clinical trial": 15,

    # Financial / material
    "bankruptcy": 45,
    "going concern": 30,
    "restatement": 30,
    "investigation": 25,
    "sec filing": 15,
    "8-k": 25,

    # Dilution (חשוב להתרעה, לרוב שלילי)
    "public offering": 30,
    "registered direct offering": 35,
    "atm offering": 25,
    "dilution": 25,
    "convertible notes": 25,
}

SOURCE_BONUS = {
    "GlobeNewswire - Press Releases": 10,
    "PR Newswire - Main": 10,
    "Business Wire": 10,
    "SEC": 20,
}


@dataclass
class NewsItem:
    source: str
    title: str
    link: str
    published: str
    summary: str
    impact_score: int
    reason: str
    uid: str


def make_uid(title: str, link: str) -> str:
    h = hashlib.sha1((title.strip() + "|" + link.strip()).encode("utf-8")).hexdigest()
    return h


def score_item(source: str, title: str, summary: str) -> Tuple[int, str]:
    text = f"{title} {summary}".lower()
    score = SOURCE_BONUS.get(source, 0)
    hits = []

    for k, w in KEYWORDS.items():
        if k in text:
            score += w
            hits.append(k)

    # cap score
    score = min(score, 100)

    reason = ", ".join(hits[:8]) if hits else "no-keyword-hit"
    return score, reason


def fetch_feed(source_name: str, url: str) -> List[NewsItem]:
    d = feedparser.parse(url)
    items: List[NewsItem] = []
    for e in d.entries:
        title = getattr(e, "title", "").strip()
        link = getattr(e, "link", "").strip()
        published = getattr(e, "published", "") or getattr(e, "updated", "")
        summary = getattr(e, "summary", "") or getattr(e, "description", "")
        uid = make_uid(title, link)

        score, reason = score_item(source_name, title, summary)
        items.append(NewsItem(
            source=source_name,
            title=title,
            link=link,
            published=published,
            summary=summary,
            impact_score=score,
            reason=reason,
            uid=uid,
        ))
    return items


def run_radar(poll_seconds: int = 30, min_score: int = 70, out_csv: str = "market_radar_events.csv"):
    seen: set[str] = set()
    rows: List[Dict] = []

    print(f"[RADAR] Starting... poll={poll_seconds}s min_score={min_score}")
    while True:
        try:
            for source_name, url in RSS_SOURCES:
                for item in fetch_feed(source_name, url):
                    if item.uid in seen:
                        continue
                    seen.add(item.uid)

                    if item.impact_score >= min_score:
                        print("\n" + "=" * 90)
                        print(f"[{item.source}] score={item.impact_score}  reason={item.reason}")
                        print(item.title)
                        print(item.published)
                        print(item.link)

                        rows.append({
                            "source": item.source,
                            "score": item.impact_score,
                            "reason": item.reason,
                            "published": item.published,
                            "title": item.title,
                            "link": item.link,
                        })

                        # save snapshot
                        pd.DataFrame(rows).to_csv(out_csv, index=False)

            time.sleep(poll_seconds)

        except KeyboardInterrupt:
            print("\n[RADAR] Stopped by user.")
            break
        except Exception as ex:
            print(f"[RADAR] Error: {ex}")
            time.sleep(poll_seconds)


if __name__ == "__main__":
    # Tune these:
    run_radar(poll_seconds=30, min_score=70, out_csv="market_radar_events.csv")
