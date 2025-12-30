import time
import json
import hashlib
from pathlib import Path
from typing import List, Dict

import feedparser
import requests

# =========================
# CONFIG
# =========================

TELEGRAM_BOT_TOKEN = "8443425255:AAG7Kkzf60CjmXSAorFoBqNiZxo2sS1qET8"
TELEGRAM_CHAT_ID = "8075458483"

POLL_SECONDS = 30  # כל כמה שניות למשוך RSS

# RSS FEEDS (אפשר להחליף לקטגוריות אחרות)
RSS_FEEDS = [
    {
        "name": "GlobeNewswire",
        # דוגמה לפיד מרכזי/קטגוריה. אם יש לך פיד ספציפי יותר, שים אותו כאן.
        "url": "https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire%20-%20News%20Release"
    },
    {
        "name": "BusinessWire",
        # דוגמה לפיד מרכזי. אפשר להחליף לקטגוריות/תעשיות.
        "url": "https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeGVtUWA=="
    }
]

TRIGGER_KEYWORDS = [
    "business combination",
    "merger",
    "acquisition",
    "definitive agreement",
    "strategic",
    "partnership",
    "takeover",
    "purchase agreement",
    "all-cash",
    "tender offer",
]

# קובץ מקומי כדי לא לשלוח אותה כתבה פעמיים
SEEN_FILE = Path("seen_items.json")


# =========================
# HELPERS
# =========================

def load_seen() -> set:
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def save_seen(seen: set) -> None:
    SEEN_FILE.write_text(json.dumps(sorted(list(seen))), encoding="utf-8")


def norm_text(s: str) -> str:
    return (s or "").strip().lower()


def item_id(entry: Dict) -> str:
    """
    מייצר ID יציב לכתבה (כדי למנוע כפילויות) לפי link+title.
    """
    base = f"{entry.get('link','')}|{entry.get('title','')}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def matches_keywords(title: str, summary: str) -> List[str]:
    hay = f"{norm_text(title)} {norm_text(summary)}"
    hits = [kw for kw in TRIGGER_KEYWORDS if kw in hay]
    return hits


def send_telegram_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": False
    }
    r = requests.post(url, json=payload, timeout=15)
    r.raise_for_status()


def fetch_feed(feed_name: str, feed_url: str) -> List[Dict]:
    parsed = feedparser.parse(feed_url)
    entries = []
    for e in parsed.entries[:25]:  # לוקחים את האחרונים
        entries.append({
            "source": feed_name,
            "title": e.get("title", ""),
            "link": e.get("link", ""),
            "summary": e.get("summary", "") or e.get("description", ""),
            "published": e.get("published", "") or e.get("updated", "")
        })
    return entries


# =========================
# MAIN LOOP
# =========================

def main():
    seen = load_seen()
    print(f"[START] Loaded seen: {len(seen)} items")

    while True:
        try:
            for feed in RSS_FEEDS:
                items = fetch_feed(feed["name"], feed["url"])

                for it in items:
                    uid = item_id(it)
                    if uid in seen:
                        continue

                    hits = matches_keywords(it["title"], it["summary"])
                    if not hits:
                        continue

                    msg = (
                        f"🚨 {it['source']} | KEYWORDS: {', '.join(hits)}\n"
                        f"📰 {it['title']}\n"
                        f"🕒 {it['published']}\n"
                        f"🔗 {it['link']}"
                    )

                    # שליחה לטלגרם
                    send_telegram_message(msg)
                    print(f"[SENT] {it['source']} - {it['title']}")

                    # מסמנים כ"נראה"
                    seen.add(uid)

            save_seen(seen)

        except Exception as ex:
            print(f"[ERROR] {ex}")

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
