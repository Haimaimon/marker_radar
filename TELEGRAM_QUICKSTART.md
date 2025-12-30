# Telegram Integration - Quick Start 🚀

## 3 Steps to Start

### 1️⃣ Get Your Bot Token

1. Open Telegram → Search `@BotFather`
2. Send `/newbot`
3. Copy the token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2️⃣ Get Your Chat ID

1. Open Telegram → Search `@userinfobot`
2. Send any message
3. Copy your user ID (e.g., `123456789`)

### 3️⃣ Configure & Test

Add to `.env`:

```bash
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE
```

Test it:

```bash
python test_telegram.py
```

If you see ✅ messages in both console and Telegram - you're ready!

## Run the App

```bash
python app.py
```

---

## What You'll Receive

Rich notifications with:
- 🚨 Ticker & Impact Score
- 📰 News Title & Source  
- 📈 Market Data (Gap %, Volume)
- ✅ Validation Status
- 🔗 Direct Link

---

## Need Help?

See detailed guide: `notifier/TELEGRAM_SETUP.md`

## Optional Settings

```bash
# Silent mode (no notification sound)
TELEGRAM_SILENT=true

# Custom retry settings
TELEGRAM_RETRY_ATTEMPTS=5
TELEGRAM_RETRY_DELAY=2
```

---

**That's it! Happy trading! 📈**

