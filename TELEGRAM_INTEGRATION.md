# Telegram Integration - Complete Guide 🚀

## 📋 Table of Contents

- [Overview](#overview)
- [What's New](#whats-new)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Features](#features)
- [Testing](#testing)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The Telegram integration provides professional, real-time notifications for Market Radar with rich formatting, automatic error handling, and advanced features.

## ✨ What's New

### Enhanced Features

✅ **Rich HTML Formatting**
- Beautiful messages with emojis, bold text, links
- Score-based emoji indicators (🚨 🔥 ⚡ 📊)
- Clickable inline links

✅ **Automatic Retry Logic**
- Exponential backoff (1s → 2s → 4s → 8s...)
- Configurable retry attempts
- Network error resilience

✅ **Advanced Notifications**
- Batch notifications (multiple events)
- Interactive buttons (inline keyboard)
- System alerts (info/warning/error)
- Summary messages

✅ **Smart Configuration**
- Silent mode (no notification sound)
- Thread/topic support for groups
- Message length validation (auto-truncate)
- Startup test message

✅ **Professional Code**
- Full type hints
- Comprehensive error handling
- Detailed logging
- Modular architecture

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Telegram Credentials

**Get Bot Token:**
1. Open Telegram → Search `@BotFather`
2. Send `/newbot`
3. Follow instructions → Copy token

**Get Chat ID:**
1. Search `@userinfobot`
2. Send any message → Copy your ID

### 3. Configure

Create/edit `.env`:

```bash
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

### 4. Test

```bash
python test_telegram.py
```

### 5. Run

```bash
python app.py
```

---

## 📦 Installation

### Required Packages

```bash
# Basic packages (already in requirements.txt)
feedparser==6.0.11
pydantic==2.8.2
python-dotenv==1.0.1
requests==2.32.3
yfinance==0.2.52

# New packages for Telegram
python-telegram-bot==21.0.1
tenacity==8.2.3
```

### Install All

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENABLE_TELEGRAM` | Yes | `false` | Enable/disable Telegram |
| `TELEGRAM_BOT_TOKEN` | Yes | - | Bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Yes | - | Chat ID from @userinfobot |
| `TELEGRAM_SILENT` | No | `false` | Silent notifications (no sound) |
| `TELEGRAM_THREAD_ID` | No | - | Thread ID for topic groups |
| `TELEGRAM_RETRY_ATTEMPTS` | No | `3` | Number of retry attempts |
| `TELEGRAM_RETRY_DELAY` | No | `2` | Initial retry delay (seconds) |

### Example Configuration

```bash
# .env file
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
TELEGRAM_SILENT=false
TELEGRAM_RETRY_ATTEMPTS=5
TELEGRAM_RETRY_DELAY=2
```

### Configuration Files

- `env.example.txt` - Template with all options
- `config.py` - Settings loader (updated)
- `app.py` - Main app (updated to use new features)

---

## 🎨 Features

### 1. Rich Formatted Notifications

Messages include:
- **Ticker & Score** with emoji indicator
- **Title** (bold, HTML formatted)
- **Source** information
- **Market Data** (gap %, volume spike)
- **Validation Status** (✅/⚠️)
- **Impact Reason**
- **Timestamp**
- **Direct Link** (clickable)

**Example Message:**

```
🔥 AAPL | Score: 85

Apple Announces Revolutionary AI Chip

📰 Source: PR Newswire
📈 Gap: 5.23%
📊 Volume Spike: 2.45x

✅ Validation: Strong market reaction detected
💡 Impact: Major product announcement
🕒 2025-12-29 14:30:00

🔗 Read Full Article
```

### 2. Batch Notifications

Send multiple events in one message:

```python
notifier.notify_batch([item1, item2, item3])
```

### 3. Interactive Buttons

Add clickable buttons to messages:

```python
notifier.send_message_with_buttons(
    "Check out this stock!",
    [
        ("View Chart", "https://example.com/chart"),
        ("Read News", "https://example.com/news"),
    ]
)
```

### 4. System Alerts

Send system notifications with severity levels:

```python
notifier.send_alert(
    title="High Activity Detected",
    message="Unusual market activity in the last hour",
    level="warning"  # info, warning, error, critical
)
```

### 5. Summary Messages

Send periodic summaries:

```python
notifier.send_summary(
    total_events=156,
    validated_events=23,
    top_ticker="NVDA"
)
```

### 6. Silent Mode

Disable notification sound for non-urgent messages:

```bash
TELEGRAM_SILENT=true
```

### 7. Auto-Retry

Automatic retry with exponential backoff:
- Network errors → auto-retry
- Timeouts → auto-retry
- API errors → logged and reported

---

## 🧪 Testing

### Automated Test Script

```bash
python test_telegram.py
```

**Tests:**
1. ✅ Configuration validation
2. ✅ API connection test
3. ✅ Sample notification

### Manual Testing

```python
from notifier import TelegramNotifier

notifier = TelegramNotifier(
    bot_token="YOUR_TOKEN",
    chat_id="YOUR_CHAT_ID"
)

# Test connection
notifier.send_test_message()

# Test notification
notifier.notify(news_item)
```

### Run Examples

```bash
python examples/telegram_advanced.py
```

**Available Examples:**
1. Basic notification
2. Batch notification
3. Silent mode
4. Interactive buttons
5. Summary messages
6. System alerts
7. Retry logic

---

## 🔧 Advanced Usage

### Custom Notifier

```python
from notifier import TelegramNotifier
from config import settings

notifier = TelegramNotifier(
    bot_token=settings.telegram_bot_token,
    chat_id=settings.telegram_chat_id,
    silent=True,              # Silent mode
    thread_id="12345",        # Topic ID
    retry_attempts=5,         # More retries
    retry_delay=1,            # Faster retry
)
```

### Multiple Channels

```python
# Personal notifications
personal = TelegramNotifier(
    bot_token=TOKEN,
    chat_id=PERSONAL_CHAT_ID
)

# Channel broadcasts
channel = TelegramNotifier(
    bot_token=TOKEN,
    chat_id="@mychannel",
    silent=True
)

# Send to both
for notifier in [personal, channel]:
    notifier.notify(item)
```

### Filtering Notifications

```python
# Only high-impact to Telegram
if item.impact_score >= 80:
    telegram_notifier.notify(item)

# All events to console
console_notifier.notify(item)
```

---

## 🔍 Troubleshooting

### Common Issues

#### "Chat not found"
- ✅ Verify chat ID is correct
- ✅ Start conversation with bot first
- ✅ For channels: Add bot as admin

#### "Unauthorized"
- ✅ Check bot token is correct
- ✅ No extra spaces in token
- ✅ Generate new token if needed

#### "Bot was blocked"
- ✅ Unblock bot in Telegram
- ✅ Send `/start` to bot

#### Messages not received
- ✅ Check `ENABLE_TELEGRAM=true`
- ✅ Verify `MIN_IMPACT_SCORE` threshold
- ✅ Review logs for errors
- ✅ Test with `python test_telegram.py`

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

Look for these messages:

```
✅ INFO - Telegram notifier initialized successfully
✅ INFO - Notification sent successfully for AAPL
❌ ERROR - Failed to send notification: Connection timeout
```

---

## 📚 Documentation

- **Quick Start:** `TELEGRAM_QUICKSTART.md` (3 steps)
- **Detailed Setup:** `notifier/TELEGRAM_SETUP.md`
- **Module Docs:** `notifier/README.md`
- **Config Template:** `env.example.txt`
- **Examples:** `examples/telegram_advanced.py`

---

## 🏗️ Architecture

### File Structure

```
market_radar/
├── notifier/
│   ├── __init__.py           # Module exports
│   ├── base.py               # Protocol interface
│   ├── console.py            # Console notifier
│   ├── telegram.py           # Telegram notifier ⭐ UPGRADED
│   ├── README.md             # Module documentation
│   └── TELEGRAM_SETUP.md     # Setup guide
├── examples/
│   ├── __init__.py
│   └── telegram_advanced.py  # Usage examples ⭐ NEW
├── config.py                 # Settings ⭐ UPDATED
├── app.py                    # Main app ⭐ UPDATED
├── test_telegram.py          # Test script ⭐ NEW
├── requirements.txt          # Dependencies ⭐ UPDATED
├── env.example.txt           # Config template ⭐ NEW
├── TELEGRAM_QUICKSTART.md    # Quick guide ⭐ NEW
└── TELEGRAM_INTEGRATION.md   # This file ⭐ NEW
```

### Code Structure

```python
# Protocol-based design
class Notifier(Protocol):
    def notify(self, item: NewsItem) -> None: ...

# Multiple implementations
class ConsoleNotifier: ...
class TelegramNotifier: ...

# Easy to extend
class SlackNotifier: ...
class DiscordNotifier: ...
```

---

## 🔐 Security

✅ **Credentials Management**
- Store tokens in `.env` file
- Add `.env` to `.gitignore`
- Never commit credentials

✅ **API Security**
- HTTPS for all requests
- HTML escaping prevents injection
- Token rotation supported

✅ **Best Practices**
- Use channel IDs (not personal)
- Rotate tokens periodically
- Monitor unauthorized access

---

## 🎯 Next Steps

After setting up Telegram, consider these enhancements:

### Other Notifiers
- [ ] Discord integration
- [ ] Slack integration
- [ ] Email notifications
- [ ] SMS (Twilio)
- [ ] Webhooks

### Advanced Features
- [ ] User preferences (filter by ticker)
- [ ] Notification schedules
- [ ] Rate limiting
- [ ] Message templates
- [ ] Multi-language support

### Ticker Extraction Improvements
- [ ] NER (Named Entity Recognition)
- [ ] Company → Ticker mapping
- [ ] Fuzzy matching

### SEC Filtering
- [ ] Filter to 8-K / S-4 only
- [ ] Parse filing details
- [ ] Highlight key events

### Market Data Upgrades
- [ ] Finnhub integration
- [ ] Polygon.io integration
- [ ] Real-time WebSocket data

### UI Development
- [ ] Streamlit dashboard
- [ ] Top events view
- [ ] Filtering & search
- [ ] Real-time updates

---

## 📞 Support

For help:
1. Review documentation files
2. Run test script: `python test_telegram.py`
3. Check logs for errors
4. Verify configuration

---

## 📝 Changelog

### v2.0 - Telegram Integration Upgrade

**Added:**
- ✅ Rich HTML formatting
- ✅ Automatic retry with exponential backoff
- ✅ Batch notifications
- ✅ Interactive buttons
- ✅ System alerts
- ✅ Summary messages
- ✅ Silent mode
- ✅ Thread/topic support
- ✅ Comprehensive documentation
- ✅ Test scripts and examples

**Updated:**
- ✅ `notifier/telegram.py` - Complete rewrite
- ✅ `config.py` - Added new settings
- ✅ `app.py` - Startup test integration
- ✅ `requirements.txt` - New dependencies

**Fixed:**
- ✅ No error handling → Comprehensive error handling
- ✅ Basic text → Rich HTML formatting
- ✅ No retry → Automatic retry logic
- ✅ Single messages only → Batch support

---

**Built with ❤️ for traders | Happy Trading! 📈**

