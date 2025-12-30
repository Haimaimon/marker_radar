# Market Radar 📈

> Real-time market monitoring system with intelligent event detection and notifications

## 🎯 Overview

Market Radar is an automated system that monitors financial news sources, scores market impact, validates with real market data, and sends intelligent notifications about significant market events.

### Key Features

- ⚡ **Real-time Monitoring** - RSS feeds from major news wires + SEC filings
- 🎯 **Smart Ticker Extraction** - Automatic extraction from news titles
- 📊 **Impact Scoring** - ML-powered relevance scoring
- ✅ **Market Validation** - Confirms with actual price/volume data
- 🔔 **Smart Notifications** - Console + **Telegram with rich formatting**
- 🗄️ **Deduplication** - SQLite-based event tracking
- 🔄 **Modular Architecture** - Easy to extend and customize

---

## 🚀 Quick Start

### 1. Install

```bash
git clone <your-repo>
cd market_radar
pip install -r requirements.txt
```

### 2. Configure

Copy and edit environment file:

```bash
cp env.example.txt .env
```

Edit `.env` with your settings (especially Telegram credentials).

### 3. Run

```bash
python app.py
```

---

## 📦 Installation

### Requirements

- Python 3.10+
- pip

### Dependencies

```bash
pip install -r requirements.txt
```

**Main packages:**
- `feedparser` - RSS feed parsing
- `pydantic` - Data validation
- `yfinance` - Market data
- `requests` - HTTP requests
- `python-telegram-bot` - Telegram integration
- `tenacity` - Retry logic

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file (see `env.example.txt`):

```bash
# General
POLL_SECONDS=30
MIN_IMPACT_SCORE=70

# Market Validation
MIN_GAP_PCT=4.0
MIN_VOL_SPIKE=1.8

# Telegram (🆕 Enhanced!)
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
TELEGRAM_SILENT=false
TELEGRAM_RETRY_ATTEMPTS=3
```

### Telegram Setup

See **[Quick Start Guide](TELEGRAM_QUICKSTART.md)** for 3-step setup!

Detailed guides:
- 📘 [Complete Integration Guide](TELEGRAM_INTEGRATION.md)
- 📗 [Setup Instructions](notifier/TELEGRAM_SETUP.md)

---

## 🏗️ Architecture

### Project Structure

```
market_radar/
├── collectors/          # Data collection modules
│   ├── base.py
│   ├── rss_collector.py
│   └── sec_collector.py
├── core/                # Core processing logic
│   ├── models.py        # Data models
│   ├── dedup.py         # Deduplication
│   ├── scoring.py       # Impact scoring
│   ├── ticker_extraction.py
│   └── validation.py    # Market validation
├── market_data/         # Market data providers
│   ├── base.py
│   └── yfinance_provider.py
├── notifier/            # Notification channels
│   ├── base.py
│   ├── console.py
│   └── telegram.py      # 🆕 Enhanced!
├── storage/             # Data persistence
│   └── sqlite_store.py
├── utils/               # Utilities
│   └── log.py
├── examples/            # 🆕 Usage examples
│   └── telegram_advanced.py
├── app.py               # Main application
├── config.py            # Configuration
└── test_telegram.py     # 🆕 Test script
```

### Data Flow

```
┌─────────────────┐
│  News Sources   │
│ (RSS, SEC, etc) │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Collectors    │
│  Fetch & Parse  │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Ticker Extract  │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Impact Scoring  │
└────────┬────────┘
         │
         v
┌─────────────────┐
│Market Validation│
│ (Gap, Volume)   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Notifiers     │
│ (Console, TG)   │
└─────────────────┘
```

---

## 🔔 Notifications

### Console (Default)

Always enabled. Shows all validated events in terminal.

### Telegram (🆕 Enhanced!)

**New features:**
- ✅ Rich HTML formatting with emojis
- ✅ Automatic retry with exponential backoff
- ✅ Batch notifications
- ✅ Interactive buttons
- ✅ System alerts
- ✅ Summary messages
- ✅ Silent mode
- ✅ Thread/topic support

**Example notification:**

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

**Setup:** See [TELEGRAM_QUICKSTART.md](TELEGRAM_QUICKSTART.md)

---

## 🧪 Testing

### Test Telegram Integration

```bash
python test_telegram.py
```

### Run Examples

```bash
python examples/telegram_advanced.py
```

**Available examples:**
1. Basic notification
2. Batch notification
3. Silent mode
4. Interactive buttons
5. Summary messages
6. System alerts
7. Retry logic

---

## 📊 Components

### Collectors

Fetch data from various sources:

- **RSSCollector** - GlobeNewswire, PR Newswire, etc.
- **SECRSSCollector** - SEC EDGAR filings

### Core Processing

- **Ticker Extraction** - Parse ticker from text
- **Impact Scoring** - ML-based relevance scoring
- **Validation** - Confirm with market data (gap %, volume)
- **Deduplication** - Avoid duplicate alerts

### Market Data

- **YFinanceProvider** - Current implementation
- *Future:* Finnhub, Polygon, Alpha Vantage

### Storage

- **SQLiteStore** - Persistent event tracking
- Deduplication
- Historical data

---

## 🚀 Future Enhancements

### Planned Improvements

Based on your requirements:

#### 1. 🎯 Smart Ticker Extraction
- [ ] NER (Named Entity Recognition)
- [ ] Company → Ticker mapping database
- [ ] Fuzzy matching for company names
- [ ] Handle variations and aliases

#### 2. 📊 Enhanced SEC Filtering
- [ ] Filter to 8-K / S-4 only
- [ ] Parse filing content
- [ ] Extract key events
- [ ] Categorize filing types

#### 3. 💹 Better Market Data
- [ ] Finnhub integration
- [ ] Polygon.io integration
- [ ] Real-time WebSocket feeds
- [ ] Multiple data sources with fallback

#### 4. 🖥️ Real-time UI
- [ ] Streamlit dashboard
- [ ] Top Events view
- [ ] Filters and search
- [ ] Live updates
- [ ] Charts and visualizations

#### 5. 🔔 More Notifiers
- [ ] Discord integration
- [ ] Slack integration
- [ ] Email notifications
- [ ] SMS (Twilio)
- [ ] Custom webhooks

---

## 📚 Documentation

### Getting Started
- 📄 [README](README.md) - This file
- 📄 [Telegram Quick Start](TELEGRAM_QUICKSTART.md) - 3-step setup

### Detailed Guides
- 📄 [Telegram Integration](TELEGRAM_INTEGRATION.md) - Complete guide
- 📄 [Telegram Setup](notifier/TELEGRAM_SETUP.md) - Detailed setup
- 📄 [Notifier Module](notifier/README.md) - Module documentation

### Reference
- 📄 [Upgrade Summary](UPGRADE_SUMMARY.md) - What's new
- 📄 [Config Template](env.example.txt) - Environment variables
- 📄 [Examples](examples/telegram_advanced.py) - Code examples

---

## 🛠️ Development

### Adding a Collector

```python
from collectors.base import Collector
from core.models import NewsItem

class MyCollector(Collector):
    def fetch(self) -> list[NewsItem]:
        # Your implementation
        return items
```

### Adding a Notifier

```python
from core.models import NewsItem

class MyNotifier:
    def notify(self, item: NewsItem) -> None:
        # Your implementation
        pass
```

### Adding a Market Data Provider

```python
from market_data.base import MarketDataProvider

class MyProvider(MarketDataProvider):
    def get_quote(self, ticker: str) -> dict:
        # Your implementation
        return quote_data
```

---

## 🤝 Contributing

Contributions welcome! Areas to improve:

1. **Ticker Extraction** - Better NER, company mapping
2. **SEC Filtering** - Form type filtering, content parsing
3. **Market Data** - New providers (Finnhub, Polygon)
4. **UI** - Streamlit dashboard
5. **Notifiers** - Discord, Slack, Email
6. **Testing** - Unit tests, integration tests

---

## 📝 Changelog

### v2.0 - Telegram Enhancement (Current)

**Added:**
- 🆕 Enhanced Telegram notifier with rich formatting
- 🆕 Automatic retry logic with exponential backoff
- 🆕 Batch notifications
- 🆕 Interactive buttons
- 🆕 System alerts and summaries
- 🆕 Silent mode and thread support
- 🆕 Comprehensive documentation (10+ files)
- 🆕 Test scripts and examples
- 🆕 Configuration improvements

**Updated:**
- ⬆️ `notifier/telegram.py` - Complete rewrite
- ⬆️ `config.py` - New Telegram settings
- ⬆️ `app.py` - Startup test integration
- ⬆️ `requirements.txt` - New dependencies

**Fixed:**
- ✅ Error handling in notifications
- ✅ Message formatting and truncation
- ✅ Network resilience

### v1.0 - Initial Release

**Core Features:**
- RSS and SEC collectors
- Impact scoring
- Market validation
- Basic Telegram notifications
- SQLite storage

---

## 🔐 Security

- ✅ Credentials in `.env` (never committed)
- ✅ `.env` in `.gitignore`
- ✅ HTML escaping in messages
- ✅ HTTPS for all API calls
- ✅ Token rotation supported

---

## 📄 License

[Your License Here]

---

## 🙏 Acknowledgments

Built with:
- [yfinance](https://github.com/ranaroussi/yfinance) - Market data
- [feedparser](https://github.com/kurtmckee/feedparser) - RSS parsing
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram API
- [pydantic](https://github.com/pydantic/pydantic) - Data validation
- [tenacity](https://github.com/jd/tenacity) - Retry logic

---

## 📞 Support

For help:
1. Check documentation files
2. Run test scripts
3. Review logs
4. Open an issue

---

**Happy Trading! 📈**

---

## Quick Links

- 🚀 [Quick Start](TELEGRAM_QUICKSTART.md)
- 📚 [Full Documentation](TELEGRAM_INTEGRATION.md)
- 🧪 [Test Script](test_telegram.py)
- 💡 [Examples](examples/telegram_advanced.py)
- 📝 [What's New](UPGRADE_SUMMARY.md)

