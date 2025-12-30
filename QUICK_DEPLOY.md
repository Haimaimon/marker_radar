# ⚡ העלאה מהירה לשרת - 5 דקות

## 🎯 בחר שירות:

### אופציה 1: PythonAnywhere (חינמי לגמרי!) ⭐

```bash
# 1. הרשם ב: https://www.pythonanywhere.com (חינמי!)

# 2. פתח Bash Console והרץ:
git clone https://github.com/YOUR_USERNAME/market_radar.git
cd market_radar
pip3.10 install --user -r requirements.txt

# 3. צור .env (Files → market_radar → New File → .env)
# העתק את התוכן מהמחשב שלך

# 4. בדוק:
python3.10 app.py

# 5. הגדר Scheduled Task:
# Tasks → Add scheduled task → כל דקה:
# /home/YOUR_USERNAME/market_radar/run_once.py
```

**⏰ עדכון:** צריך לחדש את ה-web app כל 3 חודשים (קליק אחד)

---

### אופציה 2: Railway.app ($5/חודש, always-on) 🚂

```bash
# 1. העלה את הקוד ל-GitHub (אם עדיין לא)
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. לך ל: https://railway.app
# 3. "New Project" → "Deploy from GitHub"
# 4. בחר repo
# 5. הוסף Environment Variables:
#    - FINNHUB_API_KEY=xxx
#    - TELEGRAM_BOT_TOKEN=xxx
#    - TELEGRAM_CHAT_ID=xxx
#    - ENABLE_TICKER_FILTER=true
#    - וכו' (העתק מה-.env שלך)

# 6. Deploy!
```

**💰 עלות:** $5 קרדיט חינמי, אחר כך ~$5/חודש

---

### אופציה 3: Render.com (חינמי, אבל sleeps) 😴

```bash
# 1. העלה ל-GitHub (כמו Railway)

# 2. לך ל: https://render.com
# 3. "New" → "Background Worker"
# 4. חבר GitHub repo
# 5. הוסף Environment Variables
# 6. Deploy!
```

**⚠️ חשוב:** ב-tier החינמי, השירות נרדם אחרי 15 דקות ללא שימוש.

---

## 🔒 אבטחה - חובה!

### לפני העלאה ל-GitHub:

```bash
# ודא ש-.gitignore קיים:
cat .gitignore

# אם לא, צור אותו:
echo ".env
*.db
*.sqlite
ticker_cache.json
__pycache__/
*.pyc" > .gitignore

# ודא שלא עולה .env:
git status
# אסור לראות .env ברשימה!
```

---

## 🧪 בדיקה מהירה

### מקומית (לפני העלאה):

```bash
# בדוק תלויות
pip install -r requirements.txt

# בדוק שעובד
python app.py
# לחץ Ctrl+C אחרי 30 שניות
```

### בשרת:

**PythonAnywhere:**
```bash
cd ~/market_radar
python3.10 run_once.py
```

**Railway/Render:**
בדוק ב-Logs tab

---

## 💡 המלצה שלי

| אם אתה... | אז בחר... |
|-----------|----------|
| רוצה חינמי לגמרי | PythonAnywhere |
| מוכן לשלם $5 | Railway.app |
| רק לנסות | Render.com |

---

## 📞 עזרה?

קרא את `DEPLOY_GUIDE.md` למדריך מפורט.

