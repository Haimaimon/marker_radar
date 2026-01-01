# 🚀 Trading Signals - QUICKSTART

## ⚡ התחלה מהירה (3 דקות!)

### 1️⃣ הגדרת `.env`

פתח את `.env` והוסף:

```env
# Trading Signals
ENABLE_TRADING_SIGNALS=true
SIGNALS_MIN_CONFIDENCE=70
SIGNALS_STYLE=rich
```

### 2️⃣ בדיקה

```bash
python test_trading_signals.py
```

אם רואה:
```
✅ PASS - Signal generated correctly
✅ Validation: ✅ Valid
🎉 All tests passed!
```

**→ אתה מוכן!**

### 3️⃣ הפעלה

```bash
python app.py
```

תראה:
```
📊 Trading Signals enabled (min_confidence=70%, style=rich)
🔥 VALIDATED EVENT: TICKER...
📊 Trading signal sent for TICKER
```

---

## 📱 איך זה נראה?

```
🎯 BUY SIGNAL

LCFY

💰 Price: $7.69 📈 +3.78%

🎯 Entry: $7.73
   Stop: $7.46
   Target: $8.27

⚡ R/R: 1:2.00 (Risk: 3.5%, Reward: 7.0%)
🚀 Volume: 7.4x
📰 Partnership Announcement
⚡ Confidence: 66%
```

---

## ⚙️ התאמה אישית

### רוצה יותר signals?
```env
SIGNALS_MIN_CONFIDENCE=65  # ירידה = יותר signals
```

### רוצה פחות signals?
```env
SIGNALS_MIN_CONFIDENCE=80  # עלייה = פחות signals
```

### רוצה פורמט קצר?
```env
SIGNALS_STYLE=compact
```

---

## 📊 מה זה בודק?

1. **News Impact** (עד 30 נקודות)
2. **Volume Spike** (עד 25 נקודות)
3. **Price Gap** (עד 20 נקודות)
4. **Float** (עד 15 נקודות)
5. **Price Action** (עד 10 נקודות)

**סך הכל: 0-100% confidence**

---

## 🎯 Entry/Stop/Target

**Entry:** מעט מעל המחיר (0.5%)

**Stop:** 2-4% תלוי באסטרטגיה

**Targets:**
- T1: Risk × 2 (2R)
- T2: Risk × 3 (3R)
- T3: Risk × 4 (4R)

---

## 🐛 בעיות?

### Signal לא נשלח?
- בדוק `SIGNALS_MIN_CONFIDENCE` (אולי גבוה מדי)
- בדוק `ENABLE_TRADING_SIGNALS=true`
- הרץ `python test_trading_signals.py`

### שגיאה בהפעלה?
```bash
pip install -r requirements.txt
```

---

## 📚 מסמכים מלאים

- **MISSION_COMPLETE.md** - סיכום מלא
- **TRADING_SIGNALS_GUIDE.md** - מדריך מפורט
- **signals/README.md** - API documentation

---

## 💡 טיפ!

רוצה לראות איך זה עובד?

```bash
python demo_signals.py
```

תראה 4 דוגמאות מפורטות! 🎨

---

**זהו! אתה מוכן! 🚀**

*Need help? Check MISSION_COMPLETE.md for full details*

