# RSS News Sources for Market Radar 📰

## מקורות RSS שעובדים (מאומתים)

### ✅ מקורות פעילים

#### 1. PR Newswire
```
URL: https://www.prnewswire.com/rss/news-releases-list.rss
Type: הודעות לעיתונות כלליות
Update: תדיר (כל כמה דקות)
Coverage: חברות פומביות, הכרזות גדולות
```

#### 2. SEC EDGAR
```
URL: https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&...
Type: טפסי SEC רשמיים
Update: Real-time
Coverage: כל החברות הפומביות בארה"ב
```

#### 3. Business Wire
```
URL: https://www.businesswire.com/portal/site/home/news/
Type: הודעות לעיתונות עסקיות
Update: תדיר
Coverage: חברות טכנולוגיה ופיננסים
```

---

## ❌ מקורות שכבר לא עובדים

### GlobeNewswire (לא פעיל)
```
Old URL: https://www.globenewswire.com/rss/news-releases
Status: 404 - Not Found (החל מדצמבר 2025)
Reason: אולי שינו את מבנה ה-RSS או ביטלו גישה חופשית
```

---

## 🆕 מקורות מומלצים להוסיף

### חדשות פיננסיות כלליות

```python
# Bloomberg (אם זמין)
("Bloomberg", "https://www.bloomberg.com/feed/...")

# Reuters Business
("Reuters", "https://www.reuters.com/rssFeed/businessNews")

# Yahoo Finance
("Yahoo Finance", "https://finance.yahoo.com/news/rssindex")

# MarketWatch
("MarketWatch", "https://feeds.marketwatch.com/marketwatch/topstories/")

# Seeking Alpha
("Seeking Alpha", "https://seekingalpha.com/feed.xml")
```

### SEC ממוקד (טפסים ספציפיים)

```python
# רק 8-K (major events)
("SEC 8-K", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&...")

# רק S-4 (M&A)
("SEC S-4", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=S-4&...")
```

### RSS לפי סקטור

```python
# Tech
("TechCrunch", "https://techcrunch.com/feed/")

# Biotech
("BioSpace", "https://www.biospace.com/rss")

# Energy
("Oil & Gas Journal", "...")
```

---

## 🔧 איך להוסיף מקור RSS חדש?

### 1. בדוק שה-URL עובד

פתח בדפדפן את ה-URL. אתה אמור לראות XML כזה:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>News Feed</title>
    <item>
      <title>Company Announces...</title>
      <link>https://...</link>
      <description>...</description>
    </item>
  </channel>
</rss>
```

אם אתה רואה 404 או שגיאה - ה-RSS לא עובד.

### 2. הוסף ל-app.py

```python
rss_sources = [
    ("שם המקור", "URL של ה-RSS"),
    ("PR Newswire", "https://www.prnewswire.com/rss/news-releases-list.rss"),
    # הוסף כאן עוד מקורות
]
```

### 3. הרץ ובדוק

```bash
# הפעל verbose logging
VERBOSE_LOGGING=true

python app.py
```

תראה בלוג:
```
DEBUG | market_radar.rss | 📰 שם המקור: fetched 50 items
```

אם רואה 0 items → בדוק את ה-URL שוב.

---

## 🎯 מקורות מומלצים לפי מטרה

### רוצה הכי הרבה כיסוי?
```python
rss_sources = [
    ("PR Newswire", "https://www.prnewswire.com/rss/news-releases-list.rss"),
    ("Business Wire", "https://www.businesswire.com/portal/site/home/news/"),
    ("MarketWatch", "https://feeds.marketwatch.com/marketwatch/topstories/"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
]
```

### רוצה רק אירועים משמעותיים?
```python
rss_sources = [
    # רק SEC 8-K (material events)
]
sec_collector = SECRSSCollector(form_types=["8-K", "S-4"])
```

### רוצה רק סקטור ספציפי?
```python
rss_sources = [
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
]
```

---

## 🧪 בדיקת RSS Feed

### שיטה 1: דפדפן

פתח את ה-URL בדפדפן:
- ✅ רואה XML → עובד
- ❌ רואה 404 / שגיאה → לא עובד

### שיטה 2: Python

```python
import feedparser

url = "https://www.prnewswire.com/rss/news-releases-list.rss"
d = feedparser.parse(url)

print(f"Found {len(d.entries)} items")
for entry in d.entries[:5]:
    print(f"- {entry.title}")
```

### שיטה 3: curl

```bash
curl "https://www.prnewswire.com/rss/news-releases-list.rss"
```

אמור להחזיר XML.

---

## ⚠️ שימו לב

### Rate Limits
חלק מהמקורות יש להם rate limiting:
- SEC: ~10 requests/second
- RSS רוב המקורות: בדרך כלל ללא הגבלה

### תדירות עדכון
- **Real-time**: SEC, Bloomberg Terminal
- **כל 5-15 דקות**: PR Newswire, Business Wire
- **כל שעה**: חלק מהאתרים הקטנים

### איכות המידע
- **הכי אמין**: SEC filings
- **מהיר**: Wire services (PR Newswire, Business Wire)
- **אנליזה**: Seeking Alpha, MarketWatch

---

## 🚀 שדרוג עתידי: API במקום RSS

במקום RSS, שקול:

### 1. News APIs (בתשלום, אבל יותר טוב)
- **Alpha Vantage** - $50/month
- **Polygon.io** - $29/month
- **Finnhub** - Free tier + paid
- **News API** - Free tier

### 2. יתרונות API על פני RSS
- ✅ Real-time יותר
- ✅ סינון לפי ticker
- ✅ Metadata עשיר יותר
- ✅ Rate limits ברורים
- ✅ אמינות גבוהה

---

## 📝 עדכון אחרון

**תאריך:** 29 דצמבר 2025
**סטטוס מקורות:**
- ✅ PR Newswire - עובד
- ✅ SEC EDGAR - עובד
- ✅ Business Wire - עובד
- ❌ GlobeNewswire RSS - לא עובד (404)

---

**זקוק לעזרה? פתח issue או עדכן קובץ זה!**

