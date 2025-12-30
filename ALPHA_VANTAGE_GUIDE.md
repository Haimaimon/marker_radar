# Alpha Vantage Integration Guide 📊

## Overview

Alpha Vantage מספק API איכותי לחדשות פיננסיות עם ניתוח רגשות (sentiment analysis) וזיהוי אוטומטי של טיקרים.

### למה Alpha Vantage? 🎯

✅ **חדשות איכותיות** - מקורות אמינים ומקצועיים  
✅ **טיקרים מזוהים** - לא צריך extraction  
✅ **Sentiment Analysis** - ניתוח חיובי/שלילי/ניטרלי  
✅ **Real-time** - עדכונים מהירים  
✅ **Topics מסוננים** - רק חדשות רלוונטיות  
✅ **Free tier** - 25 requests/day  

---

## Quick Start 🚀

### 1. הכנת API Key

✅ **יש לך כבר:** `XOOEO2RJ5Y3LO547`

או קבל חדש: https://www.alphavantage.co/support/#api-key

### 2. הגדרה ב-.env

```bash
# Enable Alpha Vantage
ENABLE_ALPHA_VANTAGE=true
ALPHA_VANTAGE_API_KEY=XOOEO2RJ5Y3LO547
```

### 3. בדיקה

```bash
python test_alpha_vantage.py
```

### 4. הרצה

```bash
python app.py
```

---

## Features מתקדמות 🔥

### 1. Sentiment Analysis

כל חדשה מגיעה עם ניתוח רגשות:

```json
{
  "sentiment_label": "Bullish",
  "sentiment_score": 0.432,
  "relevance_score": 0.9
}
```

**Labels:**
- `Bullish` - חיובי מאוד (0.35 עד 1.0)
- `Somewhat-Bullish` - חיובי (0.15 עד 0.35)
- `Neutral` - ניטרלי (-0.15 עד 0.15)
- `Somewhat-Bearish` - שלילי (-0.35 עד -0.15)
- `Bearish` - שלילי מאוד (-1.0 עד -0.35)

### 2. Ticker Sentiment

לכל חדשה - ניתוח רגשות **לכל מניה** שמוזכרת:

```json
{
  "ticker_sentiment": [
    {"ticker": "AAPL", "relevance_score": "0.9", "ticker_sentiment_score": "0.5"},
    {"ticker": "MSFT", "relevance_score": "0.3", "ticker_sentiment_score": "-0.2"}
  ]
}
```

### 3. Topics Filtering

סינון לפי נושאים:

```python
AlphaVantageCollector(
    api_key="...",
    topics="earnings,ipo,mergers_and_acquisitions",
    limit=50
)
```

**Available Topics:**
- `earnings` - דוחות רווח
- `ipo` - הנפקות
- `mergers_and_acquisitions` - מיזוגים ורכישות
- `financial_markets` - שווקים פיננסיים
- `economy_fiscal` - כלכלה
- `technology` - טכנולוגיה
- `life_sciences` - ביוטכנולוגיה
- `manufacturing` - תעשייה
- `real_estate` - נדל"ן
- `retail_wholesale` - קמעונאות

---

## Configuration ⚙️

### Basic Setup

```bash
# .env
ENABLE_ALPHA_VANTAGE=true
ALPHA_VANTAGE_API_KEY=XOOEO2RJ5Y3LO547
```

### Advanced Settings

בקובץ `app.py` תוכל לשנות:

```python
alpha_vantage_collector = AlphaVantageCollector(
    api_key=settings.alpha_vantage_api_key,
    topics="technology,earnings,ipo",  # ← נושאים
    limit=50,                            # ← מספר חדשות
)
```

---

## Rate Limits ⚠️

### Free Tier
- **25 requests per day**
- 1 request מחזיר עד 50 חדשות
- בסה"כ: **1,250 חדשות ליום!**

### Tips להימנעות מחריגה:
1. **הרץ כל 30 דקות** (לא כל 30 שניות)
2. **השתמש ב-time_from** למשיכת רק חדשות חדשות
3. **מערבב עם RSS** - תחסוך requests

### אם חרגת:
```json
{
  "Note": "Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day."
}
```

פתרון: חכה 24 שעות או שדרג לתכנית בתשלום.

---

## Data Structure 📋

### NewsItem מ-Alpha Vantage

```python
NewsItem(
    source="Alpha Vantage",
    title="Apple announces new iPhone",
    link="https://...",
    published="2025-12-29 12:30:00",
    summary="[Sentiment: Bullish] Apple unveiled...",
    ticker="AAPL",  # ← כבר מזוהה!
    raw={
        "alpha_vantage": {
            "sentiment_score": 0.432,
            "sentiment_label": "Bullish",
            "ticker_sentiments": [...],
            "source": "Bloomberg",
            "source_domain": "bloomberg.com"
        }
    }
)
```

---

## Usage Examples 💡

### דוגמה 1: רק Earnings

```python
# ב-app.py
alpha_vantage_collector = AlphaVantageCollector(
    api_key=settings.alpha_vantage_api_key,
    topics="earnings",  # רק דוחות רווח
    limit=50,
)
```

### דוגמה 2: עם Time Filter

```python
from datetime import datetime, timedelta

# רק חדשות מהשעה האחרונה
one_hour_ago = datetime.now() - timedelta(hours=1)
time_from = one_hour_ago.strftime("%Y%m%dT%H%M%S")

collector = AlphaVantageCollector(
    api_key="...",
    time_from=time_from,
)
```

### דוגמה 3: בדיקת Sentiment

```python
items = collector.fetch()

for item in items:
    if "alpha_vantage" in item.raw:
        av = item.raw["alpha_vantage"]
        sentiment = av["sentiment_label"]
        
        if sentiment in ["Bullish", "Somewhat-Bullish"]:
            print(f"📈 Positive: {item.title}")
        elif sentiment in ["Bearish", "Somewhat-Bearish"]:
            print(f"📉 Negative: {item.title}")
```

---

## Integration with Existing System 🔗

### Alpha Vantage + RSS + SEC

המערכת משלבת את כל המקורות:

```python
Poll #1:
  📰 PR Newswire: 20 items
  📰 Yahoo Finance: 50 items
  🏛️  SEC EDGAR: 100 items
  📊 Alpha Vantage: 50 items  ← חדש!
  
Total: 220 items
```

### יתרון: Diversity

- **RSS**: מהיר, הרבה נפח
- **SEC**: רשמי, אמין
- **Alpha Vantage**: איכותי, עם sentiment ✨

---

## Advanced: Using Sentiment in Scoring 🎯

### שילוב Sentiment ב-Impact Score

עתיד: ניתן להשתמש ב-sentiment לשיפור הסקורינג:

```python
# ב-scoring.py (עתידי)
def score(source, title, summary):
    base_score = calculate_base_score(title)
    
    # Boost if Alpha Vantage + positive sentiment
    if source == "Alpha Vantage":
        if "[Sentiment: Bullish]" in summary:
            base_score += 10
        elif "[Sentiment: Bearish]" in summary:
            base_score += 5  # Negative news = also important
    
    return base_score
```

---

## Troubleshooting 🔧

### Issue: "API key not configured"

**פתרון:**
```bash
# בדוק .env
cat .env | grep ALPHA_VANTAGE

# אמור להראות:
ENABLE_ALPHA_VANTAGE=true
ALPHA_VANTAGE_API_KEY=XOOEO2RJ5Y3LO547
```

### Issue: "No news items returned"

**אפשרויות:**
1. **Rate limit** - חכה 24 שעות
2. **Topics מוגבלים מדי** - הרחב
3. **time_from ישן מדי** - הסר או עדכן

### Issue: "Request timeout"

**פתרון:**
```python
# הגדל timeout ב-collector
response = requests.get(..., timeout=60)  # במקום 30
```

---

## Performance Tips ⚡

### 1. Cache Results

```python
# שמור תוצאות לפי זמן
last_fetch = None
cached_items = []

def fetch_with_cache():
    now = datetime.now()
    if last_fetch and (now - last_fetch).seconds < 1800:  # 30 min
        return cached_items
    
    cached_items = collector.fetch()
    last_fetch = now
    return cached_items
```

### 2. Batch Processing

```python
# במקום כל 30 שניות:
POLL_SECONDS=30  # RSS/SEC
ALPHA_VANTAGE_POLL=1800  # 30 דקות

if poll_count % (ALPHA_VANTAGE_POLL / POLL_SECONDS) == 0:
    items.extend(alpha_vantage_collector.fetch())
```

---

## Monitoring 📊

### Track Usage

```python
usage = collector.get_usage_info()
print(f"Last fetch: {usage['last_fetch']}")
print(f"Rate limit: {usage['rate_limit']}")
```

### Log Statistics

```python
av_items = [i for i in items if i.source == "Alpha Vantage"]
print(f"Alpha Vantage contributed: {len(av_items)} items")
```

---

## Cost Analysis 💰

### Free Tier
- **Cost:** $0
- **Limit:** 25 requests/day
- **Value:** ~1,250 news items/day
- **Best for:** Personal use, development

### Premium Tiers

| Tier | Cost/month | Requests/day | Requests/minute |
|------|------------|--------------|-----------------|
| Free | $0 | 25 | 5 |
| Basic | $50 | Unlimited | 5 |
| Standard | $150 | Unlimited | 15 |
| Premium | $300 | Unlimited | 120 |

**Recommendation:** Start with free, upgrade if needed.

---

## Comparison: Alpha Vantage vs RSS 🆚

| Feature | Alpha Vantage | RSS Feeds |
|---------|---------------|-----------|
| **Quality** | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐ Medium |
| **Tickers** | ✅ Pre-tagged | ❌ Need extraction |
| **Sentiment** | ✅ Included | ❌ None |
| **Speed** | ⚡ Real-time | ⚡ Real-time |
| **Volume** | 📊 50/request | 📊 20-50/source |
| **Cost** | 💰 Limited free | 💰 Free |
| **Reliability** | ✅ High | ⚠️ Variable |

**Best Strategy:** Use both! 🎯

---

## Future Enhancements 🚀

### Ideas:
1. **Sentiment-based filtering** - רק חדשות חיוביות/שליליות
2. **Ticker sentiment scoring** - שילוב ב-impact score
3. **Source tracking** - העדפה למקורות מסוימים
4. **Historical sentiment** - מעקב אחרי שינויים
5. **Multi-ticker analysis** - חדשות המשפיעות על כמה מניות

---

## Resources 📚

- [Official API Docs](https://www.alphavantage.co/documentation/#news-sentiment)
- [Support Forum](https://www.alphavantage.co/support/)
- [API Key Management](https://www.alphavantage.co/support/#api-key)

---

## Summary ✨

**Alpha Vantage מוסיף:**
- ✅ חדשות איכותיות
- ✅ טיקרים מזוהים
- ✅ ניתוח רגשות
- ✅ סינון נושאים
- ✅ מקורות אמינים

**Setup:**
```bash
# .env
ENABLE_ALPHA_VANTAGE=true
ALPHA_VANTAGE_API_KEY=XOOEO2RJ5Y3LO547

# Test
python test_alpha_vantage.py

# Run
python app.py
```

**תהנה מחדשות איכותיות! 📈**

