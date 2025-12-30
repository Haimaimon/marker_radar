# 🚀 התחלה מהירה - איך לא לפספס כתבות

## ⚡ TL;DR - תקצר לי

**הבעיה:** כתבות עם ציון גבוה נחסמות באימות שוק ולא מתריעות

**הפתרון המהיר:**

### אופציה 1: בטל אימות לגמרי (המלצה למתחילים)

```bash
# ערוך את .env
nano .env
```

```env
# שנה את השורה הזו:
ENABLE_MARKET_VALIDATION=false
```

✅ **תוצאה:** כל כתבה עם ציון מעל 70 תתריע, גם בלי טיקר או תגובת שוק

---

### אופציה 2: הורד את הסף (מאוזן)

```env
MIN_GAP_PCT=2.0      # במקום 4.0
MIN_VOL_SPIKE=1.3    # במקום 1.8
```

✅ **תוצאה:** יותר כתבות יעברו אימות

---

## 🔍 בדוק מה פספסת

```bash
# הורד ותפעיל
python check_missed_articles.py
```

**פלט לדוגמה:**
```
⚠️  כתבות עם ציון גבוה שלא עברו אימות: 2

1. [70] N/A - Deutsche Bank Says 2026...
   ❌ לא עבר אימות: Market validation disabled or no ticker
```

---

## 📊 מצא את ההגדרות המושלמות

```bash
python analyze_validation_settings.py
```

**פלט לדוגמה:**
```
🔬 Simulation:
  MIN_GAP_PCT=2.0% → 35/50 כתבות (70%)
  MIN_GAP_PCT=4.0% → 15/50 כתבות (30%)  ← זה מה שיש לך עכשיו
```

---

## 📁 ייצא לסקירה ידנית

```bash
python export_high_score_articles.py
```

**יוצר:**
- `high_score_articles.csv` - Excel
- `high_score_articles.html` - דפדפן

---

## ⚙️ תרחישים נפוצים

### תרחיש 1: "אני רוצה **הכל** - אפילו שמועות"

```env
MIN_IMPACT_SCORE=50
ENABLE_MARKET_VALIDATION=false
```

---

### תרחיש 2: "אני רוצה רק אירועים שכבר **השפיעו**"

```env
MIN_IMPACT_SCORE=70
ENABLE_MARKET_VALIDATION=true
MIN_GAP_PCT=4.0
MIN_VOL_SPIKE=1.8
```

---

### תרחיש 3: "אני רוצה גם כתבות **בלי טיקר**"

```env
ENABLE_MARKET_VALIDATION=false
```

כי כתבות בלי טיקר עוברות אוטומטית רק אם אימות מבוטל.

---

## 🎯 המלצה שלי

**ליום הראשון:**
```env
# בטל אימות - תראה הכל
ENABLE_MARKET_VALIDATION=false
MIN_IMPACT_SCORE=70
VERBOSE_LOGGING=true
```

**אחרי יום-יומיים:**
```bash
# בדוק מה קיבלת
python check_missed_articles.py 2
python analyze_validation_settings.py 2
```

**אז תחליט:**
- אם יש יותר מדי רעש → הפעל חזרה אימות
- אם יש כתבות טובות → השאר מבוטל

---

## 📚 מסמכים מלאים

- **מדריך מפורט:** [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md)
- **README ראשי:** [README.md](README.md)

---

**זמן קריאה:** 2 דקות  
**זמן הגדרה:** 30 שניות

