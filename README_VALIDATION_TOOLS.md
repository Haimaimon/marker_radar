# 🛠️ כלים לניתוח ואימות - Market Radar

## 📦 סקירת הכלים

אוסף סקריפטים לעזור לך להבין למה כתבות נחסמות ואיך לתקן את זה.

---

## 🔍 1. בדיקת כתבות שפספסת

### `check_missed_articles.py`

**מה זה עושה?**
- מציג כתבות עם ציון גבוה שלא עברו אימות
- מראה את הסיבות המדויקות לחסימה
- נותן סטטיסטיקה מפורטת

**איך להריץ?**
```bash
# בדוק יום אחרון
python check_missed_articles.py

# בדוק 7 ימים
python check_missed_articles.py 7

# בדוק 3 ימים, ציון מינימלי 60
python check_missed_articles.py 3 60
```

**דוגמת פלט:**
```
⚠️  כתבות עם ציון גבוה שלא עברו אימות: 5

1. [100] GM - Silver's big swing, another AI acquisition...
   💡 סיבת הציון: acquisition, bankruptcy
   ❌ לא עבר אימות: weak reaction gap=-0.16%
   📊 Gap: -0.16%
```

---

## 📊 2. ניתוח הגדרות האימות

### `analyze_validation_settings.py`

**מה זה עושה?**
- מנתח את התפלגות Gap% ו-Volume Spike
- מציע ערכי סף אופטימליים
- מריץ סימולציה של הגדרות שונות

**איך להריץ?**
```bash
# נתח 7 ימים אחרונים
python analyze_validation_settings.py

# נתח 30 ימים
python analyze_validation_settings.py 30
```

**דוגמת פלט:**
```
📈 Gap% Analysis
Min: 0.12%
Max: 15.30%
Average: 2.45%
Median: 1.20%

🔬 Simulation:
  MIN_GAP_PCT=1.0% → 45/50 כתבות (90%)
  MIN_GAP_PCT=2.0% → 35/50 כתבות (70%)
  MIN_GAP_PCT=4.0% → 15/50 כתבות (30%)  ← זה מה שיש לך עכשיו

💡 המלצות:
  להוריד את הסף ל-2.0% כדי לתפוס 70% מהכתבות
```

---

## 📤 3. ייצוא לסקירה ידנית

### `export_high_score_articles.py`

**מה זה עושה?**
- מייצא כתבות ל-CSV (Excel)
- מייצא ל-HTML מעוצב (דפדפן)
- כולל את כל הנתונים

**איך להריץ?**
```bash
# ייצא יום אחרון
python export_high_score_articles.py

# ייצא 7 ימים, ציון מינימלי 60
python export_high_score_articles.py 7 60
```

**מה זה יוצר?**
- `high_score_articles.csv` - פתח ב-Excel
- `high_score_articles.html` - פתח בדפדפן

---

## 🚀 זרימת עבודה מומלצת

### יום 1: איסוף נתונים
```bash
# הרץ את המערכת
python app.py
```

### יום 2: ניתוח
```bash
# בדוק מה פספסת
python check_missed_articles.py 1

# נתח הגדרות
python analyze_validation_settings.py 1

# ייצא לסקירה
python export_high_score_articles.py 1
```

### יום 3: אופטימיזציה
```bash
# עדכן .env לפי ההמלצות
notepad .env

# הרץ שוב
python app.py
```

### שבוע 1: בדיקה חוזרת
```bash
# נתח שבוע שלם
python analyze_validation_settings.py 7
python export_high_score_articles.py 7
```

---

## 📝 קבצי מדריך

| קובץ | תיאור | מתי להשתמש |
|------|--------|------------|
| `QUICK_START_VALIDATION.md` | התחלה מהירה | רוצה פתרון מהיר |
| `VALIDATION_GUIDE.md` | מדריך מלא | רוצה להבין לעומק |
| `RECOMMENDED_SETTINGS.txt` | הגדרות מומלצות | רוצה להעתיק-הדבק |

---

## 🎯 תרחישים נפוצים

### "פספסתי כתבה חשובה!"
```bash
# בדוק מה עוד פספסת
python check_missed_articles.py 7

# ראה את הסיבה המדויקת
# ערוך .env בהתאם
```

### "אני מקבל יותר מדי רעש"
```bash
# נתח את הנתונים
python analyze_validation_settings.py 7

# העלה את הסף ב-.env
```

### "רוצה לסקור הכל ידנית"
```bash
# ייצא ל-HTML
python export_high_score_articles.py 7

# פתח את high_score_articles.html בדפדפן
```

---

## 🐛 פתרון בעיות

### "אין DB" / "No database found"
```bash
# הרץ את המערכת לפחות פעם אחת
python app.py

# המתן למחזור אחד (30 שניות)
# לחץ Ctrl+C
# נסה שוב את הסקריפט
```

### "UnicodeEncodeError"
זה תוקן! אם עדיין קורה:
```bash
# הרץ עם PowerShell 7 או
chcp 65001
python check_missed_articles.py
```

### "אין נתונים"
```bash
# בדוק אם יש כתבות בכלל
python -c "import sqlite3; c=sqlite3.connect('market_radar.db'); print(c.execute('SELECT COUNT(*) FROM events').fetchone()[0])"
```

---

## 💡 טיפים

1. **הרץ ניתוח אחרי כל שינוי**
   ```bash
   python check_missed_articles.py 1
   ```

2. **השתמש ב-VERBOSE_LOGGING**
   ```env
   VERBOSE_LOGGING=true
   ```
   כדי לראות בדיוק מה נסנן

3. **ייצא לסקירה שבועית**
   ```bash
   python export_high_score_articles.py 7
   ```
   ותסקור את הכל בנוחות

4. **התחל עם אימות מבוטל**
   ```env
   ENABLE_MARKET_VALIDATION=false
   ```
   ואחר כך תחמיר

---

## 📚 למד עוד

- [README.md](README.md) - README ראשי
- [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md) - מדריך מלא
- [QUICK_START_VALIDATION.md](QUICK_START_VALIDATION.md) - התחלה מהירה

---

**יצר:** AI Assistant  
**עודכן:** דצמבר 2025  
**גרסה:** 1.0

