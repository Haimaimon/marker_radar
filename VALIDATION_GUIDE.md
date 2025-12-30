# 🎯 מדריך אימות ומעקב אחר כתבות - Market Radar

## 📋 תוכן עניינים

1. [איך עובד האימות?](#איך-עובד-האימות)
2. [למה כתבות נחסמות?](#למה-כתבות-נחסמות)
3. [איך לא לפספס כתבות חשובות?](#איך-לא-לפספס-כתבות-חשובות)
4. [כלים לניתוח](#כלים-לניתוח)
5. [התאמת הגדרות](#התאמת-הגדרות)

---

## 🔍 איך עובד האימות?

המערכת מבצעת **3 שלבי סינון**:

### שלב 1: חילוץ טיקר
```
כותרת הכתבה → זיהוי טיקר (למשל: AAPL, TSLA, MSFT)
```
- אם אין טיקר, הכתבה תמשיך לשלב הבא (עם `ticker=N/A`)
- זה לא חוסם כתבות!

### שלב 2: ציון חשיבות (Impact Score)
```
תוכן + מקור → ציון 0-100
```

**דוגמאות:**
- "acquisition" = 35 נקודות
- "FDA approval" = 45 נקודות
- "bankruptcy" = 45 נקודות
- מקור SEC = בונוס של 25 נקודות

**סף ברירת מחדל: 70**

אם הציון נמוך מ-70, הכתבה **לא תמשיך הלאה**.

### שלב 3: אימות שוק (Market Validation)
```
טיקר → בדיקת מחיר + נפח → אישור/דחייה
```

**תנאים:**
- `MIN_GAP_PCT=4.0%` - שינוי מחיר של לפחות 4%
- `MIN_VOL_SPIKE=1.8x` - נפח מסחר גבוה פי 1.8 מהממוצע

**חשוב!** אם **אין טיקר** או **אימות מושבת**, הכתבה **עוברת אוטומטית**.

---

## ❓ למה כתבות נחסמות?

### סיבה 1: ציון נמוך מ-70
```
❌ LOW SCORE (55): ACME - New product launch... | Reason: no-keyword-hit
```

**פתרון:** הורד את `MIN_IMPACT_SCORE` ב-`.env`

```env
MIN_IMPACT_SCORE=50  # במקום 70
```

### סיבה 2: אין תגובת שוק משמעותית
```
⚠️ NOT VALIDATED: TSLA - Tesla announces... | Reason: weak reaction gap=1.2% vol_spike=1.1x
```

**המשמעות:**
- המחיר זז רק 1.2% (פחות מ-4%)
- הנפח עלה פי 1.1 (פחות מ-1.8)

**פתרון:** הורד את סף האימות:

```env
MIN_GAP_PCT=2.0     # במקום 4.0
MIN_VOL_SPIKE=1.3   # במקום 1.8
```

### סיבה 3: אין נתוני שוק זמינים
```
⚠️ NOT VALIDATED: XXXX - Breaking news... | Reason: no-price-or-prev-close
```

**סיבות אפשריות:**
- טיקר לא נכון/לא קיים
- API לא מצליח למצוא נתונים
- חברה לא נסחרת בבורסה (פרטית)

**פתרון:** בטל אימות לכתבות חשובות:

```env
ENABLE_MARKET_VALIDATION=false
```

---

## 🔐 איך לא לפספס כתבות חשובות?

### ✅ כל הכתבות נשמרות ב-DB!

**גם אם כתבה לא עברה אימות, היא שמורה כאן:**

```
market_radar.db
```

### 1️⃣ בדוק מה פספסת

```bash
python check_missed_articles.py
```

**דוגמת פלט:**
```
⚠️  כתבות עם ציון גבוה שלא עברו אימות: 2

1. [70] N/A - Deutsche Bank Says 2026 Promises to Be Anything But Dull
   💡 סיבת הציון: merger, acquisition
   ❌ לא עבר אימות: Market validation disabled or no ticker
   🕒 2025-12-30 17:40:12
   🔗 https://...
```

### 2️⃣ נתח את הגדרות האימות

```bash
python analyze_validation_settings.py
```

**דוגמת פלט:**
```
📈 Gap% Analysis
  MIN_GAP_PCT=4.0% → 15/50 כתבות (30%)
  MIN_GAP_PCT=2.0% → 35/50 כתבות (70%)

💡 המלצות:
  1. להוריד את הסף (יותר התראות)
     MIN_GAP_PCT=2.0
     MIN_VOL_SPIKE=1.3
```

### 3️⃣ ייצא ל-CSV/HTML לסקירה ידנית

```bash
python export_high_score_articles.py
```

**יוצר 2 קבצים:**
- `high_score_articles.csv` - לפתיחה ב-Excel
- `high_score_articles.html` - לפתיחה בדפדפן

---

## 🛠️ כלים לניתוח

### סקריפט 1: `check_missed_articles.py`

**שימוש:**
```bash
# בדוק יום אחרון (ברירת מחדל)
python check_missed_articles.py

# בדוק 7 ימים אחרונים
python check_missed_articles.py 7

# בדוק 3 ימים, ציון מינימלי 60
python check_missed_articles.py 3 60
```

**מה זה עושה?**
- מציג כתבות עם ציון גבוה שלא עברו אימות
- מראה את הסיבות לחסימה
- נותן סטטיסטיקה מפורטת

---

### סקריפט 2: `analyze_validation_settings.py`

**שימוש:**
```bash
# נתח 7 ימים אחרונים (ברירת מחדל)
python analyze_validation_settings.py

# נתח 30 ימים
python analyze_validation_settings.py 30
```

**מה זה עושה?**
- מראה התפלגות של Gap% ו-Volume Spike
- מציע ערכי סף אופטימליים
- סימולציה של סטינגים שונים

---

### סקריפט 3: `export_high_score_articles.py`

**שימוש:**
```bash
# ייצא יום אחרון
python export_high_score_articles.py

# ייצא 7 ימים, ציון מינימלי 60
python export_high_score_articles.py 7 60
```

**מה זה עושה?**
- מייצא ל-CSV לפתיחה ב-Excel
- מייצא ל-HTML מעוצב לפתיחה בדפדפן
- כולל את כל הנתונים: Gap%, Volume, סיבות

---

## ⚙️ התאמת הגדרות

### אופציה 1: אימות מחמיר (פחות התראות, יותר מדויקות)

```env
MIN_IMPACT_SCORE=80
ENABLE_MARKET_VALIDATION=true
MIN_GAP_PCT=5.0
MIN_VOL_SPIKE=2.0
```

✅ **טוב ל:** סוחרי יום, אירועים חזקים בלבד  
❌ **רע ל:** מי שלא רוצה לפספס אירועים

---

### אופציה 2: מאוזן (ברירת מחדל)

```env
MIN_IMPACT_SCORE=70
ENABLE_MARKET_VALIDATION=true
MIN_GAP_PCT=4.0
MIN_VOL_SPIKE=1.8
```

✅ **טוב ל:** רוב המשתמשים  
⚖️ **איזון:** בין רעש לכיסוי

---

### אופציה 3: מקלט (יותר התראות, יותר רעש)

```env
MIN_IMPACT_SCORE=60
ENABLE_MARKET_VALIDATION=true
MIN_GAP_PCT=2.0
MIN_VOL_SPIKE=1.3
```

✅ **טוב ל:** מי שלא רוצה לפספס שום דבר  
❌ **רע ל:** מי שלא אוהב התראות מיותרות

---

### אופציה 4: בלי אימות (כל כתבה עם ציון גבוה)

```env
MIN_IMPACT_SCORE=70
ENABLE_MARKET_VALIDATION=false
```

✅ **טוב ל:**  
- כתבות בלי טיקר (M&A כלליים, חדשות מאקרו)
- אירועים שטרם השפיעו על השוק
- מניות קטנות/OTC בלי נתוני שוק

❌ **רע ל:** מי שרוצה רק אירועים שכבר השפיעו

---

### אופציה 5: אימות חלקי (רק Gap או Volume)

ערוך את `core/validation.py`:

```python
# אימות רק לפי Gap (התעלם מ-Volume)
if gap_ok:
    return True, f"gap={gap_pct:.2f}% (vol ignored)"

# OR: אימות רק לפי Volume (התעלם מ-Gap)
if vol_ok:
    return True, f"vol_spike={vol_spike:.2f}x (gap ignored)"
```

---

## 📊 דוגמאות מהחיים

### דוגמה 1: כתבת M&A בלי טיקר

```
TITLE: Deutsche Bank Says 2026 Promises to Be Anything But Dull
TICKER: N/A
SCORE: 70 (merger, acquisition)
VALID: True (Market validation disabled or no ticker)
```

✅ **עברה!** כי אין טיקר, אז אימות מדולג

---

### דוגמה 2: כתבה עם תגובת שוק חלשה

```
TITLE: XYZ Corp Announces New Product
TICKER: XYZ
SCORE: 75 (acquisition)
GAP: 1.2%
VOL_SPIKE: 1.1x
VALID: False (weak reaction gap=1.2% vol_spike=1.1x)
```

❌ **נחסמה!** השוק לא הגיב מספיק

**פתרון:** הורד את `MIN_GAP_PCT` ל-1.0

---

### דוגמה 3: כתבה עם תגובת שוק חזקה

```
TITLE: ABC Inc FDA Approval for Cancer Drug
TICKER: ABC
SCORE: 90 (fda approval)
GAP: 15.3%
VOL_SPIKE: 5.2x
VALID: True (gap=15.3% vol_spike=5.2x)
```

✅ **עברה!** השוק הגיב חזק

---

## 🎓 שאלות נפוצות

### ש: למה יש לי 2 כתבות עם High Score אבל רק 1 עברה אימות?

**ת:** כנראה שלאחת מהן:
1. אין טיקר → צריך לבטל אימות
2. אין תגובת שוק → צריך להוריד סף
3. אין נתוני שוק → צריך לבדוק API

**בדוק עם:**
```bash
python check_missed_articles.py
```

---

### ש: איך אני יודע מה הסף האופטימלי עבורי?

**ת:** הרץ את הניתוח:
```bash
python analyze_validation_settings.py 7
```

והוא יראה לך כמה כתבות עוברות עם כל סף.

---

### ש: האם כדאי לבטל אימות לגמרי?

**ת:** תלוי במטרה שלך:

✅ **כן, אם:**
- אתה מחפש חדשות כלליות (לא רק מניות)
- אתה רוצה אירועים לפני שהשוק מגיב
- יש לך הרבה כתבות בלי טיקר

❌ **לא, אם:**
- אתה רוצה רק אירועים שכבר השפיעו
- אתה לא רוצה התראות מיותרות
- אתה סוחר יום שמחפש volatility

---

### ש: איך אני יכול לקבל התראה רק על כתבות ספציפיות?

**ת:** ערוך את `core/scoring.py` והוסף מילות מפתח:

```python
KEYWORDS = {
    # הוסף מילות מפתח משלך
    "my company name": 50,
    "my keyword": 30,
    # ...
}
```

---

## 🚀 זרימת עבודה מומלצת

### יום 1: התחלה
```bash
# 1. הרץ את המערכת עם הגדרות ברירת מחדל
python app.py

# 2. המתן יום אחד
```

### יום 2: ניתוח
```bash
# 3. בדוק מה פספסת
python check_missed_articles.py 1

# 4. נתח הגדרות
python analyze_validation_settings.py 1

# 5. ייצא לסקירה
python export_high_score_articles.py 1
```

### יום 3: אופטימיזציה
```bash
# 6. עדכן .env לפי המלצות
nano .env

# 7. הרץ שוב
python app.py
```

### שבוע 1: בדיקה חוזרת
```bash
# 8. נתח שבוע שלם
python analyze_validation_settings.py 7

# 9. עשה fine-tuning אחרון
```

---

## 📞 תמיכה

אם משהו לא ברור:
1. בדוק את `check_missed_articles.py` לסיבה מדויקת
2. בדוק את `VERBOSE_LOGGING=true` ב-`.env`
3. הרץ `python app.py` ובדוק את הלוגים

---

**עודכן לאחרונה:** דצמבר 2025  
**גרסה:** 2.0

