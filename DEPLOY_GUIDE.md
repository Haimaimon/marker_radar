# 🚀 מדריך העלאה לשרת - Market Radar

## 🌐 אפשרויות שרתים חינמיים

### 🥇 אופציה 1: PythonAnywhere (מומלץ!)

**יתרונות:**
- ✅ **חינמי לגמרי לתמיד**
- ✅ תומך ב-Python מהקופסה
- ✅ קל להתקנה (ממשק ווב)
- ✅ פועל 24/7
- ✅ 100 שניות CPU ליום (מספיק!)

**חסרונות:**
- ⚠️ צריך לעדכן את המערכת כל 3 חודשים (קליק אחד)

---

## 📋 הכנה לפני ההעלאה

### שלב 1: צור `requirements.txt`

הקובץ כבר קיים במערכת! בדוק:
```bash
cat requirements.txt
```

### שלב 2: בדוק שהכל עובד מקומית

```bash
# בדוק תלויות
pip install -r requirements.txt

# בדוק שהמערכת רצה
python app.py
```

### שלב 3: הכן את ה-`.env`

**חשוב מאוד!** 🔒

1. **אל תעלה את `.env` ל-Git!**
2. תצטרך להעתיק את ההגדרות ידנית לשרת

---

## 🚀 העלאה ל-PythonAnywhere (שלב אחר שלב)

### שלב 1: הרשמה

1. לך ל: https://www.pythonanywhere.com
2. לחץ "Pricing & signup"
3. בחר "Create a Beginner account" (חינמי!)
4. מלא פרטים והרשם

---

### שלב 2: העלה את הקוד

**אופציה A: דרך Git (מומלץ)**

1. העלה את הקוד ל-GitHub:
   ```bash
   # במחשב שלך
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/USERNAME/market_radar.git
   git push -u origin main
   ```

2. ב-PythonAnywhere, פתח **Bash Console**:
   ```bash
   git clone https://github.com/USERNAME/market_radar.git
   cd market_radar
   ```

**אופציה B: העלה ידנית (פשוט יותר)**

1. ב-PythonAnywhere, לך ל-**Files**
2. צור תיקייה חדשה: `market_radar`
3. העלה את כל הקבצים (ללא `.env`!)

---

### שלב 3: התקן תלויות

ב-**Bash Console** ב-PythonAnywhere:

```bash
cd ~/market_radar

# התקן pip packages
pip3.10 install --user -r requirements.txt

# בדוק שהתקנה הצליחה
python3.10 -c "import feedparser; import requests; print('OK')"
```

---

### שלב 4: הגדר `.env`

**⚠️ חשוב: אל תעתיק סיסמאות/tokens באופן גלוי!**

ב-PythonAnywhere, ב-**Files**:

1. נווט ל-`market_radar/`
2. צור קובץ חדש: `.env`
3. העתק את התוכן מהמחשב שלך (אבל **לא את ה-Telegram tokens** - ראה למטה)

**תוכן `.env` לשרת:**
```env
# General Settings
POLL_SECONDS=30
MIN_IMPACT_SCORE=70
VERBOSE_LOGGING=true
ONLY_TODAY_NEWS=true
AUTO_CLEANUP_OLD_NEWS=true

# Ticker Filtering
ENABLE_TICKER_FILTER=true

# Market Validation
ENABLE_MARKET_VALIDATION=true
MIN_GAP_PCT=0.5
MIN_VOL_SPIKE=1.0

# Finnhub (שים את ה-key שלך כאן)
ENABLE_FINNHUB=true
FINNHUB_API_KEY=YOUR_KEY_HERE

# SEC
ENABLE_SEC_FILTERED=true
ENABLE_SEC_LEGACY=false

# Telegram (שים את הפרטים שלך כאן)
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
TELEGRAM_SILENT=false
TELEGRAM_THREAD_ID=
TELEGRAM_RETRY_ATTEMPTS=3
TELEGRAM_RETRY_DELAY=2
```

**🔒 Security Tip:**
ודא שהקובץ `.env` לא public! ב-Git:
```bash
# ודא ש-.env בתוך .gitignore
echo ".env" >> .gitignore
```

---

### שלב 5: בדיקה ידנית

ב-**Bash Console**:

```bash
cd ~/market_radar
python3.10 app.py
```

אם הכל עובד, תראה:
```
Starting Market Radar...
🎯 Ticker filter enabled: 96 tickers
📰 GlobeNewswire: fetched 50 items
...
```

לחץ `Ctrl+C` לעצירה.

---

### שלב 6: הגדר הרצה אוטומטית (Always-On Task)

**חשוב:** ב-tier החינמי אין "Always-On Tasks".

**פתרונות:**

#### פתרון A: Scheduled Task (מומלץ לחינמי!)

1. לך ל-**Tasks** ב-PythonAnywhere
2. הוסף **Scheduled Task**
3. הגדר:
   - **Time:** כל יום בשעה 09:00 (או כל שעה אחרת)
   - **Command:** 
     ```bash
     cd /home/YOUR_USERNAME/market_radar && /usr/bin/python3.10 app.py
     ```
   - זה ירוץ פעם אחת ביום

**אבל זה רק פעם אחת ביום!**

#### פתרון B: שדרג ל-$5/חודש (Hacker plan)

אם אתה רוצה שזה ירוץ 24/7:
1. שדרג ל-"Hacker" plan ($5/חודש)
2. אז תוכל להשתמש ב-**Always-On Task**

---

### שלב 7: פתרון חכם - Cron-like Script

אם אתה רוצה לרוץ כל 30 שניות בחינם:

צור `run_once.py`:

```python
#!/usr/bin/env python3
"""
Run one poll cycle and exit.
Perfect for PythonAnywhere scheduled tasks.
"""
import os
from app import main_once  # We'll need to modify app.py

if __name__ == "__main__":
    main_once()
```

הוסף ל-`app.py` בסוף:

```python
def main_once():
    """Run one poll cycle and exit (for scheduled tasks)."""
    # ... copy the main loop content but run only once
    pass
```

אז הגדר Scheduled Task לרוץ כל דקה.

---

## 🎯 אופציה 2: Railway.app (אוטומטי יותר)

### יתרונות:
- ✅ $5 קרדיט חינמי לחודש
- ✅ הפעלה אוטומטית מ-Git
- ✅ Always-on by default

### חסרונות:
- ⚠️ קרדיט מסתיים אחרי חודש

---

### הכנה ל-Railway:

1. צור `Procfile`:
```bash
worker: python app.py
```

2. צור `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

3. העלה ל-GitHub

4. לך ל-Railway.app:
   - התחבר עם GitHub
   - "New Project" → "Deploy from GitHub repo"
   - בחר את ה-repo
   - הוסף **Environment Variables** (מתוך `.env`)
   
5. Deploy!

---

## 🎯 אופציה 3: Render.com

### שלבים:

1. צור `render.yaml`:
```yaml
services:
  - type: worker
    name: market-radar
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
```

2. העלה ל-GitHub
3. התחבר ל-Render.com
4. "New" → "Background Worker"
5. חבר ל-GitHub repo
6. הוסף Environment Variables
7. Deploy!

---

## 🔒 אבטחה - חובה לקרוא!

### ⚠️ אל תעלה ל-Git:

- ❌ `.env` (סיסמאות וtokens)
- ❌ `market_radar.db` (מידע אישי)
- ❌ `ticker_cache.json` (לא רגיש, אבל לא נחוץ)
- ❌ `*.pyc` / `__pycache__/` (קבצי cache)

### ✅ צור `.gitignore`:

```
# Environment
.env
*.env

# Database
*.db
*.sqlite
*.sqlite3

# Cache
ticker_cache.json
__pycache__/
*.pyc
*.pyo
*.pyd

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

### 🔒 הוסף environment variables דרך הממשק:

**PythonAnywhere:**
Files → .env → edit manually

**Railway/Render:**
Dashboard → Environment Variables → Add

---

## 🧪 בדיקת השרת

### בדיקה 1: האם הבוט רץ?

שלח לבוט הטלגרם שלך:
```
/start
```

או בדוק בלוגים:
- **PythonAnywhere:** Console logs
- **Railway:** Logs tab
- **Render:** Logs tab

### בדיקה 2: האם מקבל כתבות?

חכה 30 שניות ובדוק טלגרם.

---

## 📊 השוואת אפשרויות

| שירות | מחיר | Always-On | קל להתקנה | מגבלות |
|-------|------|-----------|-----------|---------|
| **PythonAnywhere Free** | ₪0 | ❌ (רק scheduled) | ⭐⭐⭐⭐⭐ | 100s CPU/יום |
| **PythonAnywhere Hacker** | $5/חודש | ✅ | ⭐⭐⭐⭐⭐ | ללא |
| **Railway** | $5 credit | ✅ | ⭐⭐⭐⭐ | $5/חודש |
| **Render Free** | ₪0 | ⚠️ (sleeps) | ⭐⭐⭐ | שינה אחרי 15 דקות |
| **Google Cloud Run** | $300 credit | ✅ | ⭐⭐ | מורכב |

---

## 💡 המלצה שלי

### אם אתה רוצה **חינמי לגמרי:**
👉 **PythonAnywhere Free** + Scheduled Task (כל דקה)

### אם אתה מוכן לשלם $5/חודש:
👉 **Railway.app** - הכי קל, always-on

### אם אתה רוצה לנסות בחינם ואז לשדרג:
👉 **PythonAnywhere Free** → שדרג ל-Hacker אם אתה אוהב

---

## 🚀 סקריפט התקנה מהיר (PythonAnywhere)

```bash
# 1. Clone/העלה קוד
git clone https://github.com/YOUR_USERNAME/market_radar.git
cd market_radar

# 2. התקן תלויות
pip3.10 install --user -r requirements.txt

# 3. צור .env (copy manually from your local .env)
nano .env
# paste your settings
# Ctrl+X, Y, Enter to save

# 4. בדוק שעובד
python3.10 app.py

# 5. הגדר Scheduled Task בממשק
# Tasks → Add scheduled task → כל דקה
```

---

## 📞 עזרה נוספת

**PythonAnywhere Help:**
https://help.pythonanywhere.com/

**Railway Docs:**
https://docs.railway.app/

**Render Docs:**
https://render.com/docs

---

**רוצה שאעזור לך להעלות? תגיד לי איזה שירות בחרת!** 🚀

