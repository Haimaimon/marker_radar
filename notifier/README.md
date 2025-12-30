# Market Radar - Notifier Module

## Overview

The Notifier module provides a flexible, modular notification system for Market Radar. It supports multiple notification channels with a clean, protocol-based interface.

## Architecture

```
notifier/
├── base.py           # Protocol definition (Notifier interface)
├── console.py        # Console/terminal output
├── telegram.py       # Telegram bot integration ⭐
├── __init__.py       # Module exports
├── README.md         # This file
└── TELEGRAM_SETUP.md # Detailed Telegram guide
```

## Supported Channels

### 1. Console Notifier ✅
**Status:** Fully implemented

Simple console output for development and debugging.

```python
from notifier import ConsoleNotifier

notifier = ConsoleNotifier()
notifier.notify(news_item)
```

### 2. Telegram Notifier ⭐
**Status:** Fully implemented with advanced features

Professional Telegram integration with:
- ✅ Rich HTML formatting
- ✅ Automatic retry with exponential backoff
- ✅ Error handling and logging
- ✅ Batch notifications
- ✅ Interactive buttons
- ✅ System alerts
- ✅ Summary messages
- ✅ Silent mode
- ✅ Thread/topic support
- ✅ Message length validation

```python
from notifier import TelegramNotifier

notifier = TelegramNotifier(
    bot_token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID",
    silent=False,
    thread_id=None,
    retry_attempts=3,
    retry_delay=2,
)
notifier.notify(news_item)
```

## Protocol Interface

All notifiers implement the `Notifier` protocol:

```python
from typing import Protocol
from core.models import NewsItem

class Notifier(Protocol):
    def notify(self, item: NewsItem) -> None:
        """Send notification for a news item"""
        ...
```

This allows for:
- ✅ Type safety
- ✅ Easy testing with mocks
- ✅ Simple addition of new notifiers
- ✅ Flexible notification strategies

## Adding New Notifiers

To add a new notification channel:

1. Create a new file in `notifier/` (e.g., `slack.py`)
2. Implement the `Notifier` protocol:

```python
from core.models import NewsItem

class SlackNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def notify(self, item: NewsItem) -> None:
        # Your implementation here
        pass
```

3. Add to `__init__.py`:

```python
from .slack import SlackNotifier

__all__ = [
    "Notifier",
    "ConsoleNotifier",
    "TelegramNotifier",
    "SlackNotifier",  # Add your notifier
]
```

4. Update `app.py` to use it:

```python
def build_notifier():
    notifiers = [ConsoleNotifier()]
    
    if settings.enable_slack:
        notifiers.append(SlackNotifier(settings.slack_webhook))
    
    return notifiers
```

## Telegram Features

### Basic Notification

```python
notifier.notify(news_item)
```

Sends a rich formatted message with:
- Ticker and impact score
- Title and source
- Market data (gap %, volume)
- Validation status
- Direct link

### Batch Notifications

```python
notifier.notify_batch([item1, item2, item3])
```

Sends multiple events in a single summarized message.

### Interactive Buttons

```python
notifier.send_message_with_buttons(
    "Check out this stock!",
    [
        ("View Chart", "https://example.com/chart"),
        ("Read News", "https://example.com/news"),
    ]
)
```

### Summary Messages

```python
notifier.send_summary(
    total_events=156,
    validated_events=23,
    top_ticker="NVDA"
)
```

### System Alerts

```python
notifier.send_alert(
    title="High Activity",
    message="Unusual market activity detected",
    level="warning"  # info, warning, error, critical
)
```

## Configuration

### Environment Variables

```bash
# Telegram
ENABLE_TELEGRAM=true
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
TELEGRAM_SILENT=false
TELEGRAM_THREAD_ID=
TELEGRAM_RETRY_ATTEMPTS=3
TELEGRAM_RETRY_DELAY=2
```

### Programmatic Configuration

```python
from config import settings
from notifier import TelegramNotifier

notifier = TelegramNotifier(
    bot_token=settings.telegram_bot_token,
    chat_id=settings.telegram_chat_id,
    silent=settings.telegram_silent,
    thread_id=settings.telegram_thread_id or None,
    retry_attempts=settings.telegram_retry_attempts,
    retry_delay=settings.telegram_retry_delay,
)
```

## Testing

### Test Telegram Configuration

```bash
python test_telegram.py
```

This will:
1. ✅ Verify environment variables
2. ✅ Test API connection
3. ✅ Send sample notification

### Manual Testing

```python
from notifier import TelegramNotifier

notifier = TelegramNotifier(bot_token="...", chat_id="...")

# Test connection
notifier.send_test_message()

# Test notification
notifier.notify(sample_news_item)
```

## Error Handling

The Telegram notifier includes comprehensive error handling:

### Automatic Retry

Network errors and timeouts trigger automatic retry with exponential backoff:
- Attempt 1: Immediate
- Attempt 2: 1s delay
- Attempt 3: 2s delay
- Attempt 4: 4s delay
- Attempt 5: 8s delay

### Logging

All errors are logged with context:

```
ERROR - Failed to send notification for AAPL: Connection timeout
INFO - Retrying in 2 seconds... (attempt 2/3)
INFO - Notification sent successfully for AAPL
```

### Graceful Degradation

If Telegram is unavailable, the app continues running with console notifications only.

## Performance

- **Message size:** Automatic truncation if > 4096 chars
- **Rate limiting:** Respects Telegram's 30 msg/second limit
- **Retry logic:** Exponential backoff prevents API flooding
- **Async-ready:** Can be easily adapted for async/await

## Security

- ✅ Credentials stored in `.env` (not in code)
- ✅ `.env` added to `.gitignore`
- ✅ HTML escaping prevents injection
- ✅ HTTPS for all API calls
- ✅ Token rotation supported

## Future Enhancements

Potential additions:

- [ ] Discord notifier
- [ ] Slack notifier
- [ ] Email notifier
- [ ] SMS notifier (Twilio)
- [ ] Webhook notifier (generic)
- [ ] Database logger
- [ ] Notification rate limiting
- [ ] User preferences (filter by ticker, score, etc.)
- [ ] Message templates
- [ ] Multi-language support

## Examples

See `examples/telegram_advanced.py` for:
- Basic notifications
- Batch processing
- Silent mode
- Interactive buttons
- Summaries
- Alerts
- Retry handling

## Resources

- [Telegram Setup Guide](./TELEGRAM_SETUP.md) - Detailed configuration
- [Quick Start](../TELEGRAM_QUICKSTART.md) - 3-step setup
- [Telegram Bot API](https://core.telegram.org/bots/api) - Official docs
- [Example Config](../env.example.txt) - Environment template

## Support

For issues or questions:
1. Check logs in console
2. Verify `.env` configuration
3. Test with `python test_telegram.py`
4. Review setup guide

---

**Built with ❤️ for traders**

