import requests
import feedparser

URLS = [
    # Wire Services (הודעות לעיתונות רשמיות)
    ("GlobeNewswire", "https://www.globenewswire.com/rss/news-releases"),
    ("PR Newswire", "https://www.prnewswire.com/rss/news-releases-list.rss"),
    ("Business Wire", "https://feeds.businesswire.com/businesswire/news/home"),
    
    # Financial News Sites (אתרי חדשות פיננסיות)
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("MarketWatch - Top Stories", "https://feeds.marketwatch.com/marketwatch/topstories/"),
    ("MarketWatch - Breaking News", "https://feeds.marketwatch.com/marketwatch/marketpulse/"),
    ("Reuters Business", "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"),
    ("CNBC Top News", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("CNBC Investing", "https://www.cnbc.com/id/15839135/device/rss/rss.html"),
    ("Barrons", "https://www.barrons.com/feed/barrons-voices/rss"),
    
    # Investment Analysis (אנליזות והמלצות)
    ("Seeking Alpha - Market News", "https://seekingalpha.com/market_currents.xml"),
    ("Seeking Alpha - Wall Street Breakfast", "https://seekingalpha.com/feed.xml"),
    ("The Motley Fool", "https://www.fool.com/feeds/"),
    ("Zacks", "https://www.zacks.com/rss/stock-news.xml"),
    
    # Tech & Startups (טכנולוגיה וסטארטאפים)
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("VentureBeat", "https://venturebeat.com/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    
    # Crypto & Fintech
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Decrypt", "https://decrypt.co/feed"),
    
    # SEC Filings (טפסים רשמיים)
    ("SEC - All Filings", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=100&output=atom"),
    ("SEC - 8K Only", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&count=100&output=atom"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MarketRadar/1.0",
    "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
}

for name, url in URLS:
    print("\n==============================")
    print(name, url)

    r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
    print("HTTP:", r.status_code)
    print("Content-Type:", r.headers.get("content-type"))
    print("First 200 chars:", r.text[:200].replace("\n", " "))

    feed = feedparser.parse(r.text)
    print("Entries:", len(feed.entries))
    if feed.entries:
        print("First title:", feed.entries[0].get("title"))
