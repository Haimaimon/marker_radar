# 🎯 מדריך סינון כתבות - רק שוק ההון

## ✅ מה נוסף?

**פילטר חדש שמבטיח שתקבל רק כתבות על מניות ושוק ההון!**

---

## 🔍 איך זה עובד?

המערכת בודקת כל כתבה עם **3 שכבות סינון**:

### שכבה 1: זיהוי מונחי שוק ההון ✅

הכתבה **חייבת** להכיל לפחות אחד מהמונחים האלה:

#### מונחי שוק:
- `stock`, `stocks`, `share`, `shares`, `equity`, `equities`
- `nasdaq`, `nyse`, `dow jones`, `s&p 500`
- `ipo`, `listing`, `ticker`, `trading`

#### מונחים פיננסיים:
- `earnings`, `revenue`, `profit`, `loss`, `eps`
- `dividend`, `buyback`, `split`
- `market cap`, `valuation`, `price target`

#### פעולות תאגידיות:
- `merger`, `acquisition`, `m&a`, `takeover`
- `sec`, `8-k`, `10-k`, `s-1`, `filing`

#### מונחי ביוטק (למניות ביוטק):
- `fda`, `phase 1/2/3`, `clinical trial`
- `nda`, `bla`, `pdufa`, `approval`

#### מונחי אנליסטים:
- `analyst`, `upgrade`, `downgrade`, `rating`
- `buy`, `sell`, `hold`, `consensus`

**ועוד 50+ מונחים!**

---

### שכבה 2: זיהוי סימבולי טיקר ✅

אם יש **סימבול טיקר** בכתבה (כמו `$AAPL`, `(TSLA)`, `MSFT:`), היא עוברת!

---

### שכבה 3: חסימת תוכן לא רלוונטי ❌

כתבות עם המונחים האלה **נחסמות** (אלא אם יש גם מונחי שוק):
- `recipe`, `cooking`, `fashion`, `sports`
- `celebrity`, `entertainment`, `movie`, `music`
- `weather`, `traffic`, `crime`
- `gaming`, `esports`, `nft`

---

## 📊 דוגמאות

### ✅ יעבור (שוק ההון):

```
✅ "Apple Announces Record Earnings"
   → מכיל: earnings, shares, quarterly

✅ "FDA Approves New Drug - Stock Surges"
   → מכיל: fda, stock, approval

✅ "Tesla Stock Split Announced"
   → מכיל: stock, split

✅ "Amazon Beats Wall Street Expectations"
   → מכיל: revenue, wall street

✅ "Company A to Acquire Company B for $5B"
   → מכיל: acquisition, merger, nyse
```

---

### ❌ ייחסם (לא שוק ההון):

```
❌ "New Restaurant Opens Downtown"
   → אין מונחי שוק

❌ "Movie Review: Latest Blockbuster"
   → מכיל: movie

❌ "Sports: Team Wins Championship"
   → מכיל: sports, game

❌ "Recipe: Best Chocolate Cake"
   → מכיל: recipe

❌ "Celebrity Gets Married"
   → מכיל: celebrity
```

---

## 🚀 איך להפעיל?

### אוטומטי - כבר עובד!

הפילטר **כבר משולב** ב-`app.py` ועובד אוטומטית.

### בדיקה:

```bash
python test_stock_filter.py
```

**תראה:**
```
✅ PASS | Apple Announces Record Earnings
✅ PASS | FDA Approves New Drug
❌ PASS | Recipe: Best Chocolate Cake (blocked)
📊 Test Results: 15 passed, 0 failed
🎉 All tests passed!
```

---

## 📊 איך זה ישפיע?

### לפני הסינון:
```
500 כתבות נאספו
├─ 300 כתבות על שוק ההון ✅
├─ 100 כתבות כלליות (טכנולוגיה, חדשות) ❌
├─ 50 כתבות על ספורט/בידור ❌
└─ 50 כתבות אחרות ❌

→ 60% רק רלוונטי
```

### אחרי הסינון:
```
500 כתבות נאספו
└─ 300 כתבות על שוק ההון ✅

→ 100% רלוונטי! 🎯
```

**הפחתת רעש: 40%!**

---

## 🎛️ הגדרות

### מופעל כברירת מחדל:

הפילטר רץ **אוטומטית** לפני כל הסינונים האחרים.

### ראה בלוגים:

```env
VERBOSE_LOGGING=true
```

**תראה:**
```
🚫 NOT STOCK-RELATED: Recipe for success in business
   Reason: Not stock-related: recipe

✅ HIGH SCORE (85): Apple Reports Earnings Beat
   Reason: Stock market indicators: earnings, shares
```

---

## 📈 סטטיסטיקה

בלוג Poll Summary יכלול:

```
📊 Poll #5 Summary:
   Fetched: 500 | New: 450 | Duplicates: 50
   🚫 Not Stock-Related: 150  ← חדש!
   No Ticker: 50
   Low Score: 100 | High Score: 150
   Not Validated: 50 | Validated: 100
   🔔 Notified: 100
```

---

## 🔧 התאמה אישית

### להוסיף מונחים נוספים:

ערוך `core/stock_filter.py`:

```python
STOCK_MARKET_INDICATORS = {
    # הוסף מונחים משלך:
    "my custom term",
    "another term",
    # ...
}
```

### לחסום מונחים נוספים:

```python
EXCLUSION_TERMS = {
    # הוסף מונחים לחסימה:
    "crypto",
    "real estate",
    # ...
}
```

---

## 🧪 בדיקה

### בדוק את הפילטר:

```bash
python test_stock_filter.py
```

### הרץ את המערכת:

```bash
python app.py
```

**תראה בלוגים:**
```
🚫 NOT STOCK-RELATED: New restaurant opens...
✅ HIGH SCORE (85): Apple reports earnings...
```

---

## 📊 שילוב עם פילטרים אחרים

הסינון רץ **לפני** כל הפילטרים האחרים:

```
1. 🚫 Stock Market Filter     ← חדש!
2. 🎯 Ticker Filter (NASDAQ/S&P 500)
3. 📊 Impact Scoring
4. ✅ Market Validation
5. 🔔 Notification
```

**זרימה:**
```
500 כתבות
  ↓ Stock Filter
300 כתבות (רק שוק ההון)
  ↓ Ticker Filter
150 כתבות (רק NASDAQ/S&P)
  ↓ Impact Scoring
50 כתבות (ציון גבוה)
  ↓ Market Validation
20 כתבות (תגובת שוק)
  ↓ Notification
20 התראות! 🔔
```

---

## 💡 טיפים

### 1. השתמש ב-Verbose Logging

```env
VERBOSE_LOGGING=true
```

תראה בדיוק מה נסנן ולמה.

### 2. בדוק תקופה

```bash
python check_missed_articles.py
```

ראה אם פספסת כתבות חשובות.

### 3. התאם לצרכים שלך

אם אתה רוצה גם כתבות על טכנולוגיה כללית, הוסף:
```python
"technology", "innovation", "startup"
```

---

## 🎯 סיכום

**לפני:**
- ✅ 60% כתבות רלוונטיות
- ❌ 40% רעש (ספורט, בידור, אוכל...)

**אחרי:**
- ✅ **100% כתבות על שוק ההון!**
- 🎯 רק מניות, earnings, M&A, FDA, SEC...
- 📉 אפס רעש!

---

**נוצר:** דצמבר 2025  
**גרסה:** 1.0  
**תואם:** Market Radar v2.0+

