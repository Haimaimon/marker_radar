# 🚀 מדריך פריסה לענן - Market Radar

## 🎯 כן! אפשר להריץ את הבוט בענן בחינם 24/7!

יש **3 אפשרויות מעולות** לשרתים חינמיים:

---

## 🏆 אופציה 1: Render.com (הכי מומלץ למתחילים)

### ✅ יתרונות:
- ✅ **100% חינם** (750 שעות/חודש = מספיק ל-24/7)
- ✅ **הכי קל להתקנה** (ממשק גרפי פשוט)
- ✅ **אוטו-deploy** מ-GitHub
- ✅ **לוגים בזמן אמת**
- ✅ **לא צריך כרטיס אשראי**

### 📋 התקנה (5 דקות):

#### שלב 1: העלה ל-GitHub
```bash
# אם עדיין לא עשית:
cd C:\Users\haima\Desktop\market_radar
git init
git add .
git commit -m "Initial commit"

# צור repository חדש ב-GitHub (דרך האתר)
# אז:
git remote add origin https://github.com/YOUR_USERNAME/market_radar.git
git push -u origin main
```

#### שלב 2: הירשם ל-Render.com
1. לך ל: https://render.com
2. לחץ "Get Started" → "Sign Up with GitHub"
3. אשר את החיבור

#### שלב 3: צור Background Worker
1. לחץ "New +" → "Background Worker"
2. בחר את ה-repository שלך (`market_radar`)
3. הגדרות:
   - **Name:** `market-radar-bot`
   - **Region:** `Oregon` (או `Frankfurt` לאירופה)
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Plan:** `Free`

#### שלב 4: הוסף Environment Variables
בעמוד ההגדרות, לחץ "Environment" והוסף:

**חובה:**
```
TELEGRAM_BOT_TOKEN = 8443425255:AAG7Kkzf60CjmXSAorFoBqNiZxo2sS1qET8
TELEGRAM_CHAT_ID = 8075458483
ENABLE_TELEGRAM = true

FINNHUB_API_KEY = d596r09r01... (ה-key שלך)
ENABLE_FINNHUB = true
```

**מומלץ:**
```
MIN_GAP_PCT = 0.5
MIN_VOL_SPIKE = 1.0
ENABLE_TICKER_FILTER = true
VERBOSE_LOGGING = true
```

#### שלב 5: Deploy!
1. לחץ "Create Background Worker"
2. Render יבנה ויפעיל את הבוט אוטומטית
3. תראה לוגים בזמן אמת!

### 📊 מעקב:
- **לוגים:** לחץ על "Logs" בדף הבוט
- **Restart:** לחץ "Manual Deploy" → "Deploy latest commit"
- **Stop:** לחץ "Suspend"

---

## 🚂 אופציה 2: Railway.app (הכי מתקדם)

### ✅ יתרונות:
- ✅ **$5 חינם לחודש** (מספיק לבוט קטן)
- ✅ **ביצועים מעולים**
- ✅ **Database מובנה** (אם תצטרך בעתיד)
- ✅ **CLI מתקדם**
- ⚠️ **דורש כרטיס אשראי** (לא חייבים)

### 📋 התקנה:

#### שלב 1: הירשם ל-Railway
1. לך ל: https://railway.app
2. "Start a New Project" → "Deploy from GitHub repo"
3. בחר את ה-repository שלך

#### שלב 2: הגדרות
Railway יזהה אוטומטית את `railway.json` ו-`Dockerfile`!

#### שלב 3: Environment Variables
הוסף ב-"Variables":
```
TELEGRAM_BOT_TOKEN = ...
TELEGRAM_CHAT_ID = ...
FINNHUB_API_KEY = ...
ENABLE_TELEGRAM = true
ENABLE_FINNHUB = true
MIN_GAP_PCT = 0.5
MIN_VOL_SPIKE = 1.0
ENABLE_TICKER_FILTER = true
```

#### שלב 4: Deploy
לחץ "Deploy" והבוט יעלה!

---

## ✈️ אופציה 3: Fly.io (הכי גמיש)

### ✅ יתרונות:
- ✅ **חינם עד 3 VMs קטנים**
- ✅ **גיאוגרפיה גלובלית** (שרתים בכל העולם)
- ✅ **CLI מצוין**
- ⚠️ **דורש כרטיס אשראי**

### 📋 התקנה:

#### שלב 1: התקן Fly CLI
```bash
# Windows (PowerShell):
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# או הורד מ: https://fly.io/docs/hands-on/install-flyctl/
```

#### שלב 2: התחבר
```bash
fly auth signup  # או fly auth login
```

#### שלב 3: Deploy
```bash
cd C:\Users\haima\Desktop\market_radar

# צור אפליקציה (פעם אחת)
fly launch --no-deploy

# הוסף secrets
fly secrets set TELEGRAM_BOT_TOKEN="8443425255:AAG7Kkzf60CjmXSAorFoBqNiZxo2sS1qET8"
fly secrets set TELEGRAM_CHAT_ID="8075458483"
fly secrets set FINNHUB_API_KEY="d596r09r01..."
fly secrets set ENABLE_TELEGRAM="true"
fly secrets set ENABLE_FINNHUB="true"

# Deploy!
fly deploy
```

#### שלב 4: מעקב
```bash
# לוגים בזמן אמת
fly logs

# סטטוס
fly status

# עצור
fly scale count 0

# הפעל שוב
fly scale count 1
```

---

## 📊 השוואה מהירה

| תכונה | Render.com | Railway.app | Fly.io |
|-------|-----------|-------------|--------|
| **מחיר** | חינם לגמרי | $5/חודש חינם | חינם לגמרי |
| **כרטיס אשראי** | ❌ לא צריך | ⚠️ מומלץ | ✅ צריך |
| **קלות התקנה** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **ביצועים** | טוב | מצוין | מצוין |
| **לוגים** | ✅ UI מעולה | ✅ UI טוב | ✅ CLI |
| **Auto-deploy** | ✅ כן | ✅ כן | ⚠️ ידני |
| **מומלץ למתחילים** | ✅✅✅ | ✅✅ | ✅ |

---

## 🎯 המלצה שלי

### למתחילים:
**→ Render.com** - הכי קל, חינם, ללא כרטיס אשראי!

### למתקדמים:
**→ Railway.app** - ביצועים מעולים, CLI נוח

### למקצוענים:
**→ Fly.io** - שליטה מלאה, גיאוגרפיה גלובלית

---

## 🔧 Troubleshooting

### בעיה: "Build failed"
**פתרון:** ודא ש-`requirements.txt` קיים ותקין:
```bash
cat requirements.txt
```

### בעיה: "App crashes immediately"
**פתרון:** בדוק לוגים:
- **Render:** לחץ "Logs"
- **Railway:** לחץ "Deployments" → "View Logs"
- **Fly:** `fly logs`

סיבות נפוצות:
- חסר `TELEGRAM_BOT_TOKEN` או `TELEGRAM_CHAT_ID`
- שגיאה ב-`.env` variables

### בעיה: "No notifications"
**פתרון:** ודא:
1. `ENABLE_TELEGRAM=true` מוגדר
2. ה-Bot Token תקין
3. ה-Chat ID נכון
4. הבוט רץ (בדוק לוגים)

---

## 📱 איך לעצור/להפעיל מרחוק?

### Render.com:
1. לך לדף הבוט
2. לחץ "Suspend" (עצור) או "Resume" (הפעל)

### Railway.app:
1. לך לדף הפרויקט
2. לחץ על ה-service
3. "Settings" → "Sleep" או "Wake"

### Fly.io:
```bash
fly scale count 0  # עצור
fly scale count 1  # הפעל
```

---

## 🔐 אבטחה

### ⚠️ חשוב מאוד:

1. **אל תעלה את `.env` ל-GitHub!**
   ```bash
   # ודא שיש .gitignore עם:
   .env
   *.db
   ```

2. **השתמש ב-Environment Variables** בפלטפורמה
   - ✅ טוב: הגדר ב-Render/Railway/Fly
   - ❌ רע: שים ב-`.env` ותעלה ל-GitHub

3. **Secrets רגישים:**
   - `TELEGRAM_BOT_TOKEN`
   - `FINNHUB_API_KEY`
   - `TELEGRAM_CHAT_ID`

---

## 📊 ניטור מרחוק

### אופציה 1: לוגים בפלטפורמה
כל הפלטפורמות מציעות לוגים בזמן אמת.

### אופציה 2: Telegram Status Bot
הוסף לבוט הודעת "heartbeat" כל שעה:

```python
# בapp.py, בתוך הלולאה:
if poll_count % 120 == 0:  # כל שעה (אם POLL_SECONDS=30)
    notifier.notify_system_status(f"✅ Bot alive! Poll #{poll_count}")
```

### אופציה 3: UptimeRobot (חינם)
אם תוסיף endpoint לבדיקת health.

---

## 💰 עלויות

### Render.com:
- **Free tier:** 750 שעות/חודש
- **זה מספיק?** כן! 24/7 = 720 שעות/חודש
- **אחרי?** $7/חודש

### Railway.app:
- **Free tier:** $5 credit/חודש
- **זה מספיק?** כן לבוט קטן
- **אחרי?** Pay as you go

### Fly.io:
- **Free tier:** 3 shared-cpu VMs
- **זה מספיק?** כן!
- **אחרי?** $1.94/חודש

---

## 🎓 מדריך צעד-אחר-צעד מלא (Render.com)

### 1. הכן את הקוד
```bash
cd C:\Users\haima\Desktop\market_radar

# ודא שהקבצים האלה קיימים:
ls Dockerfile
ls requirements.txt
ls render.yaml
```

### 2. העלה ל-GitHub
```bash
# אם עדיין לא:
git init
git add .
git commit -m "Ready for deployment"

# צור repo ב-GitHub.com (דרך הדפדפן)
# אז:
git remote add origin https://github.com/YOUR_USERNAME/market_radar.git
git push -u origin main
```

### 3. צור חשבון ב-Render
- לך ל: https://render.com
- "Get Started" → "Sign Up with GitHub"
- אשר גישה ל-repository

### 4. צור Background Worker
- Dashboard → "New +" → "Background Worker"
- בחר `market_radar` repository
- הגדרות:
  ```
  Name: market-radar-bot
  Region: Oregon
  Branch: main
  Build Command: pip install -r requirements.txt
  Start Command: python app.py
  Instance Type: Free
  ```

### 5. הוסף Environment Variables
לחץ "Environment" והוסף **אחד-אחד**:

```
TELEGRAM_BOT_TOKEN = 8443425255:AAG7Kkzf60CjmXSAorFoBqNiZxo2sS1qET8
TELEGRAM_CHAT_ID = 8075458483
ENABLE_TELEGRAM = true

FINNHUB_API_KEY = d596r09r01...
ENABLE_FINNHUB = true

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

### 6. Deploy!
- לחץ "Create Background Worker"
- Render יתחיל לבנות...
- אחרי 2-3 דקות תראה: "Live"

### 7. בדוק לוגים
- לחץ "Logs"
- תראה:
  ```
  Starting Market Radar...
  🎯 Ticker filter enabled: 96 tickers
  📰 GlobeNewswire: fetched 50 items
  ✅ VALIDATED EVENT: AAPL...
  ```

### 8. קבל התראה ראשונה!
תוך כמה דקות תקבל התראה ראשונה ב-Telegram! 🎉

---

## ✅ סיכום

**כן, זה אפשרי וזה חינם!**

1. ✅ **Render.com** - הכי קל, חינם לגמרי, ללא כרטיס אשראי
2. ✅ **Railway.app** - מתקדם יותר, $5 חינם
3. ✅ **Fly.io** - גמיש מאוד, חינם

**המלצה:** תתחיל עם **Render.com** - זה לוקח 5 דקות!

---

## 📞 עזרה נוספת

אם משהו לא עובד:
1. בדוק לוגים בפלטפורמה
2. ודא ש-Environment Variables מוגדרים נכון
3. בדוק שה-Bot Token תקין
4. נסה להריץ מקומית קודם: `python app.py`

---

**יצר:** AI Assistant  
**עודכן:** דצמבר 2025  
**גרסה:** 1.0

