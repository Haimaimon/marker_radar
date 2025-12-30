# Market Radar - Logging & Monitoring Guide 📊

## סקירה כללית

המערכת כעת כולל מערכת logging מקיף שמאפשר לך לראות בדיוק מה קורה בכל poll!

## מצבי Logging 🔊

### 1. מצב רגיל (ברירת מחדל)

```bash
VERBOSE_LOGGING=false
```

**מה תראה:**
- ✅ סיכום כל poll
- ✅ אירועים שעברו validation
- ✅ סטטיסטיקות (כמה חדשות, כמה עברו, וכו')
- ❌ לא תראה פירוט על כל חדשה

**דוגמת פלט:**

```
2025-12-29 11:27:05,068 | INFO | market_radar | Poll #1 - Fetching news...
2025-12-29 11:27:07,123 | INFO | market_radar | 📥 Fetched 145 total items from all sources
2025-12-29 11:27:15,456 | INFO | market_radar | 🔥 VALIDATED EVENT: AAPL (score=85) - Apple Announces Revolutionary...
2025-12-29 11:27:15,789 | INFO | market_radar | 📊 Poll #1 Summary:
2025-12-29 11:27:15,790 | INFO | market_radar |    Fetched: 145 | New: 12 | Duplicates: 133
2025-12-29 11:27:15,791 | INFO | market_radar |    Low Score: 8 | High Score: 4
2025-12-29 11:27:15,792 | INFO | market_radar |    Not Validated: 3 | Validated: 1
2025-12-29 11:27:15,793 | INFO | market_radar |    🔔 Notified: 1
2025-12-29 11:27:15,794 | INFO | market_radar | Next poll in 30 seconds...
```

### 2. מצב Verbose (מפורט)

```bash
VERBOSE_LOGGING=true
```

**מה תראה:**
- ✅ כל מה שבמצב רגיל
- ✅ פירוט על כל חדשה שנמצאה
- ✅ הסיבה למה חדשות נפסלו
- ✅ ציונים של כל חדשה
- ✅ סיבות validation

**דוגמת פלט:**

```
2025-12-29 11:27:05,068 | INFO | market_radar | Poll #1 - Fetching news...
2025-12-29 11:27:07,123 | INFO | market_radar | 📥 Fetched 145 total items from all sources
2025-12-29 11:27:07,125 | DEBUG | market_radar | ⏭️  SKIP (duplicate): Apple Q4 Earnings Report Released...
2025-12-29 11:27:07,156 | DEBUG | market_radar | ⚠️  No ticker found: Market Commentary: Tech Sector Overview...
2025-12-29 11:27:07,234 | DEBUG | market_radar | ❌ LOW SCORE (45): MSFT - Microsoft Office Update... | Reason: Minor product update
2025-12-29 11:27:08,567 | DEBUG | market_radar | ✅ HIGH SCORE (75): TSLA - Tesla Opens New Facility... | Reason: Expansion announcement
2025-12-29 11:27:09,234 | DEBUG | market_radar | ⚠️  NOT VALIDATED: TSLA - Tesla Opens New Facility... | Reason: Gap below threshold (2.1% < 4.0%)
2025-12-29 11:27:10,456 | DEBUG | market_radar | ✅ HIGH SCORE (85): AAPL - Apple Announces Revolutionary... | Reason: Major product announcement
2025-12-29 11:27:11,234 | INFO | market_radar | 🔥 VALIDATED EVENT: AAPL (score=85) - Apple Announces Revolutionary...
2025-12-29 11:27:15,789 | INFO | market_radar | 📊 Poll #1 Summary:
2025-12-29 11:27:15,790 | INFO | market_radar |    Fetched: 145 | New: 12 | Duplicates: 133
2025-12-29 11:27:15,791 | INFO | market_radar |    No Ticker: 3
2025-12-29 11:27:15,792 | INFO | market_radar |    Low Score: 8 | High Score: 4
2025-12-29 11:27:15,793 | INFO | market_radar |    Not Validated: 3 | Validated: 1
2025-12-29 11:27:15,794 | INFO | market_radar |    🔔 Notified: 1
2025-12-29 11:27:15,795 | INFO | market_radar | Next poll in 30 seconds...
```

---

## הגדרות נוספות ⚙️

### להפחית רעש - הגדל סינון

```bash
MIN_IMPACT_SCORE=80      # הגבר מ-70 ל-80
MIN_GAP_PCT=5.0          # הגבר מ-4.0 ל-5.0
MIN_VOL_SPIKE=2.0        # הגבר מ-1.8 ל-2.0
```

### לראות יותר התראות - הנמך סינון

```bash
MIN_IMPACT_SCORE=60      # הנמך מ-70 ל-60
MIN_GAP_PCT=3.0          # הנמך מ-4.0 ל-3.0
MIN_VOL_SPIKE=1.5        # הנמך מ-1.8 ל-1.5
```

### לבדוק מהר יותר

```bash
POLL_SECONDS=15          # כל 15 שניות במקום 30
```

---

## סטטיסטיקות שתראה 📊

בכל poll תקבל סיכום:

| מדד | משמעות |
|-----|---------|
| **Fetched** | כמה חדשות נאספו מכל המקורות |
| **New** | כמה חדשות חדשות (לא duplicates) |
| **Duplicates** | כמה חדשות כבר ראינו קודם |
| **No Ticker** | כמה חדשות ללא ticker (verbose בלבד) |
| **Low Score** | כמה חדשות עם ציון נמוך (< MIN_IMPACT_SCORE) |
| **High Score** | כמה חדשות עם ציון גבוה |
| **Not Validated** | כמה לא עברו market validation |
| **Validated** | כמה עברו את הכל ✅ |
| **Notified** | כמה הודעות נשלחו (טלגרם + קונסול) |

---

## סיבות נפוצות לפסילה 🚫

### 1. Low Score (ציון נמוך)
```
❌ LOW SCORE (45): MSFT - Microsoft Office Update...
Reason: Minor product update
```

**פתרון:** הנמך `MIN_IMPACT_SCORE` או חכה לחדשות יותר משמעותיות

### 2. No Ticker (אין טיקר)
```
⚠️  No ticker found: Market Commentary: Tech Sector Overview...
```

**פתרון:** 
- הכתבה לא מזכירה מניה ספציפית
- העתיד: NER + Company mapping ישפר את זה

### 3. Not Validated (לא עבר market validation)
```
⚠️  NOT VALIDATED: TSLA - Tesla Opens New Facility...
Reason: Gap below threshold (2.1% < 4.0%)
```

**פתרון:** הנמך `MIN_GAP_PCT` או `MIN_VOL_SPIKE`

### 4. Duplicate (כפילות)
```
⏭️  SKIP (duplicate): Apple Q4 Earnings Report Released...
```

**זה בסדר!** - המערכת כבר ראתה את זה

---

## דוגמאות שימוש 🎯

### בדיקה מהירה - רוצה לראות שהמערכת עובדת

```bash
# הגדר ב-.env:
MIN_IMPACT_SCORE=50
MIN_GAP_PCT=2.0
MIN_VOL_SPIKE=1.3
VERBOSE_LOGGING=true
POLL_SECONDS=15

# הרץ:
python app.py
```

תראה הרבה יותר התראות!

### ייצור - רק אירועים חשובים באמת

```bash
# הגדר ב-.env:
MIN_IMPACT_SCORE=80
MIN_GAP_PCT=5.0
MIN_VOL_SPIKE=2.0
VERBOSE_LOGGING=false
POLL_SECONDS=30

# הרץ:
python app.py
```

תקבל רק את האירועים הכי משמעותיים.

---

## טיפים 💡

### 1. עקוב אחרי מניה ספציפית

הוסף logging לחיפוש ticker:

```python
# בקובץ app.py, אחרי שורה 79:
if item.ticker == "AAPL":
    logger.info(f"🍎 Found AAPL news: {item.title}")
```

### 2. שמור לוגים לקובץ

```python
# בקובץ utils/log.py:
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),  # קונסול
            logging.FileHandler("market_radar.log")  # קובץ
        ]
    )
```

### 3. ראה רק validated events

```bash
python app.py | grep "VALIDATED EVENT"
```

### 4. ספור התראות

```bash
python app.py | grep "Notified:" | wc -l
```

---

## מבנה הלוג 📋

כל poll עובר בשלבים:

```
1. 📥 Fetch from all sources
   ↓
2. ⏭️  Skip duplicates
   ↓
3. 🎯 Extract ticker
   ↓
4. 📊 Calculate impact score
   ├─ ❌ Low score → Skip
   └─ ✅ High score → Continue
       ↓
5. 💹 Market validation
   ├─ ⚠️  Not validated → Save & Skip
   └─ ✅ Validated → Notify!
       ↓
6. 🔔 Send notifications
   ├─ Console
   └─ Telegram
```

---

## שאלות נפוצות ❓

### Q: למה אני לא רואה שום התראות?

**A:** בדוק:
1. ✅ יש חדשות חדשות? (ראה "Fetched" בסיכום)
2. ✅ הן לא duplicates? (ראה "New" בסיכום)
3. ✅ הן עברו את impact score? (ראה "High Score")
4. ✅ הן עברו market validation? (ראה "Validated")

אם "New" = 0 → כל החדשות כפילות, חכה לחדשות חדשות.
אם "High Score" = 0 → הנמך `MIN_IMPACT_SCORE`
אם "Validated" = 0 → הנמך `MIN_GAP_PCT` או `MIN_VOL_SPIKE`

### Q: המערכת רצה אבל אין פלט?

**A:** הפעל `VERBOSE_LOGGING=true` כדי לראות הכל.

### Q: איך אני יודע שה-RSS feeds עובדים?

**A:** הפעל verbose logging ותראה:
```
DEBUG | market_radar.rss | 📰 GlobeNewswire: fetched 50 items
DEBUG | market_radar.rss | 📰 PR Newswire: fetched 95 items
DEBUG | market_radar.sec | 🏛️  SEC EDGAR: fetched 100 filings
```

### Q: יש לי יותר מדי התראות!

**A:** הגבר את הסינון:
```bash
MIN_IMPACT_SCORE=85
MIN_GAP_PCT=6.0
MIN_VOL_SPIKE=2.5
```

---

## מעקב ב-Real Time 🔴

### Linux/Mac:

```bash
# ראה רק סיכומים
python app.py | grep "Summary"

# ראה רק validated events
python app.py | grep "VALIDATED"

# ראה רק notifications
python app.py | grep "Notified"

# שמור הכל לקובץ
python app.py 2>&1 | tee market_radar_$(date +%Y%m%d).log
```

### Windows PowerShell:

```powershell
# ראה רק validated events
python app.py | Select-String "VALIDATED"

# שמור לקובץ
python app.py | Tee-Object -FilePath "market_radar.log"
```

---

## העתיד - שדרוגים מתוכננים 🚀

1. **Web Dashboard** - Streamlit UI בזמן אמת
2. **Database Analytics** - שאילתות היסטוריות
3. **Performance Metrics** - זמני תגובה, API calls
4. **Alert Rules** - פילטר מותאם אישית לכל משתמש

---

**כעת יש לך שקיפות מלאה! 🎉**

ראה בדיוק מה המערכת עושה, למה חדשות נפסלות, וכמה אירועים נמצאו.

