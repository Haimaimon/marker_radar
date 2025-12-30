# 🚀 פריסה מהירה - 5 דקות

## כן! אפשר להריץ את הבוט בענן **חינם** 24/7!

---

## 🎯 המלצה: Render.com (הכי קל)

### למה Render?
- ✅ **100% חינם** (750 שעות/חודש)
- ✅ **לא צריך כרטיס אשראי**
- ✅ **ממשק פשוט**
- ✅ **לוגים בזמן אמת**

---

## 📋 5 צעדים פשוטים:

### 1️⃣ העלה ל-GitHub (אם עדיין לא)

```bash
cd C:\Users\haima\Desktop\market_radar

git init
git add .
git commit -m "Initial commit"

# צור repository חדש ב-GitHub.com
# אז:
git remote add origin https://github.com/YOUR_USERNAME/market_radar.git
git push -u origin main
```

---

### 2️⃣ הירשם ל-Render.com

1. לך ל: **https://render.com**
2. לחץ **"Get Started"**
3. בחר **"Sign Up with GitHub"**
4. אשר את החיבור

---

### 3️⃣ צור Background Worker

1. בדף הבית, לחץ **"New +"** → **"Background Worker"**
2. בחר את ה-repository: **`market_radar`**
3. מלא:
   ```
   Name: market-radar-bot
   Region: Oregon (או Frankfurt)
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   Plan: Free
   ```

---

### 4️⃣ הוסף Environment Variables

לחץ **"Environment"** והוסף את המשתנים האלה:

#### חובה:
```
TELEGRAM_BOT_TOKEN = 8443425255:AAG7Kkzf60CjmXSAorFoBqNiZxo2sS1qET8
TELEGRAM_CHAT_ID = 8075458483
ENABLE_TELEGRAM = true

FINNHUB_API_KEY = d596r09r01...  (ה-key שלך)
ENABLE_FINNHUB = true
```

#### מומלץ (העתק-הדבק):
```
MIN_GAP_PCT = 0.5
MIN_VOL_SPIKE = 1.0
ENABLE_TICKER_FILTER = true
ENABLE_MARKET_VALIDATION = true
VERBOSE_LOGGING = true
ONLY_TODAY_NEWS = true
ENABLE_SEC_FILTERED = true
POLL_SECONDS = 30
MIN_IMPACT_SCORE = 70
```

---

### 5️⃣ Deploy!

1. לחץ **"Create Background Worker"**
2. המתן 2-3 דקות...
3. תראה **"Live"** ✅

---

## 📊 איך לבדוק שזה עובד?

### בדוק לוגים:
1. בדף הבוט, לחץ **"Logs"**
2. תראה:
   ```
   Starting Market Radar...
   🎯 Ticker filter enabled: 96 tickers
   📰 GlobeNewswire: fetched 50 items
   ✅ VALIDATED EVENT: AAPL (score=85)
   ```

### קבל התראה:
תוך כמה דקות תקבל התראה ראשונה ב-Telegram! 🎉

---

## 🎛️ ניהול מרחוק

### לעצור את הבוט:
1. לך לדף הבוט ב-Render
2. לחץ **"Suspend"**

### להפעיל שוב:
1. לך לדף הבוט
2. לחץ **"Resume"**

### לעדכן את הקוד:
1. עשה שינויים במחשב
2. `git push`
3. Render יעדכן אוטומטית!

---

## 🔧 Troubleshooting

### לא מקבל התראות?
1. בדוק לוגים - יש שגיאות?
2. ודא ש-`TELEGRAM_BOT_TOKEN` נכון
3. ודא ש-`TELEGRAM_CHAT_ID` נכון
4. ודא ש-`ENABLE_TELEGRAM=true`

### "Build failed"?
1. ודא ש-`requirements.txt` קיים
2. בדוק שאין שגיאות syntax בקוד

### הבוט עובד אבל אין כתבות?
1. בדוק ש-`MIN_IMPACT_SCORE` לא גבוה מדי
2. נסה `ENABLE_MARKET_VALIDATION=false`
3. בדוק לוגים - מה נסנן?

---

## 💰 כמה זה עולה?

**חינם לגמרי!**

- Render Free tier: 750 שעות/חודש
- הבוט צריך: 720 שעות/חודש (24/7)
- **יש לך 30 שעות עודפות!** ✅

---

## 🎉 זהו!

**הבוט שלך רץ בענן 24/7 בחינם!**

אתה יכול:
- ✅ לכבות את המחשב
- ✅ לקבל התראות בכל מקום
- ✅ לנהל מרחוק דרך Render.com

---

## 📚 רוצה עוד אפשרויות?

קרא את **DEPLOYMENT_GUIDE.md** למדריך מלא עם:
- Railway.app
- Fly.io
- Docker
- ועוד...

---

**זמן התקנה:** 5 דקות  
**עלות:** ₪0  
**קושי:** קל מאוד ⭐⭐⭐⭐⭐

