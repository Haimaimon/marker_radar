# Telegram Integration Setup Guide

## Overview
The Market Radar Telegram integration provides real-time notifications with rich formatting, automatic retry logic, and advanced configuration options.

## Features ✨

- **Rich HTML Formatting**: Beautiful messages with emojis, bold text, and inline links
- **Automatic Retry**: Exponential backoff retry logic for reliability
- **Error Handling**: Comprehensive error logging and handling
- **Silent Mode**: Option to send notifications without sound
- **Topic Support**: Support for topic-enabled groups
- **Message Validation**: Automatic truncation of long messages
- **Test Messages**: Verification on startup

## Quick Setup 🚀

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to choose a name and username
4. **Save the bot token** - you'll need it for configuration

### 2. Get Your Chat ID

**Option A: Personal notifications**
1. Search for `@userinfobot` in Telegram
2. Send it any message
3. Copy your **user ID** (numeric)

**Option B: Channel notifications**
1. Create a new channel
2. Add your bot as an administrator
3. The chat ID will be the channel username (e.g., `@mychannel`) or numeric ID (e.g., `-1001234567890`)

**Option C: Group notifications**
1. Create a group and add your bot
2. Use a bot like `@RawDataBot` to get the group chat ID

### 3. Configure Environment Variables

Add to your `.env` file:

```bash
# Enable Telegram notifications
ENABLE_TELEGRAM=true

# Your bot token from @BotFather
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Your chat ID (user, channel, or group)
TELEGRAM_CHAT_ID=123456789

# Optional: Silent notifications (no sound)
TELEGRAM_SILENT=false

# Optional: Thread ID for topic-enabled groups
TELEGRAM_THREAD_ID=

# Optional: Retry configuration
TELEGRAM_RETRY_ATTEMPTS=3
TELEGRAM_RETRY_DELAY=2
```

## Message Format 📱

Messages include:

- **Emoji indicators** based on impact score:
  - 🚨 Critical (90+)
  - 🔥 High (80-89)
  - ⚡ Medium (70-79)
  - 📊 Low (<70)

- **Validation status**: ✅ Validated / ⚠️ Not Validated

- **Rich data**:
  - Ticker and impact score
  - Article title and source
  - Gap % and volume spike (if available)
  - Validation and impact reasons
  - Timestamp
  - Direct link to article

### Example Message

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

## Advanced Configuration ⚙️

### Silent Notifications

Disable notification sound (useful for high-frequency alerts):

```bash
TELEGRAM_SILENT=true
```

### Topic/Thread Support

For topic-enabled groups, specify the thread ID:

```bash
TELEGRAM_THREAD_ID=12345
```

### Retry Configuration

Customize retry behavior:

```bash
# Number of retry attempts
TELEGRAM_RETRY_ATTEMPTS=5

# Initial delay between retries (seconds)
# Uses exponential backoff: 2s, 4s, 8s, 16s...
TELEGRAM_RETRY_DELAY=2
```

## Testing 🧪

The system automatically sends a test message on startup when Telegram is enabled. Look for:

```
✅ Telegram notifier initialized successfully
```

If you see an error:
```
❌ Telegram test failed - notifier disabled
```

Check:
1. Bot token is correct
2. Chat ID is correct
3. Bot has permission to send messages to the chat
4. Internet connection is working

## Troubleshooting 🔧

### "Chat not found" error
- Ensure the chat ID is correct
- For channels/groups, make sure the bot is added as an administrator

### "Bot was blocked by the user"
- Unblock the bot in Telegram
- Start a conversation with the bot first

### "Unauthorized" error
- Check that the bot token is correct
- Generate a new token from @BotFather if needed

### Messages not received
- Verify ENABLE_TELEGRAM=true
- Check that MIN_IMPACT_SCORE threshold is not too high
- Review logs for error messages

### Rate limiting
- Telegram has a limit of ~30 messages/second
- The system includes automatic retry with backoff
- Consider batching notifications if hitting limits

## Security Notes 🔒

- **Never commit** your bot token or chat ID to version control
- Store credentials in `.env` file (add to `.gitignore`)
- Rotate bot token periodically via @BotFather
- Use channel/group IDs instead of personal IDs for shared deployments

## API Reference 📚

### TelegramNotifier Class

```python
from notifier.telegram import TelegramNotifier

notifier = TelegramNotifier(
    bot_token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID",
    silent=False,              # Optional
    thread_id=None,            # Optional
    retry_attempts=3,          # Optional
    retry_delay=2              # Optional
)

# Send notification
notifier.notify(news_item)

# Test connection
notifier.send_test_message()
```

## Resources 📖

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Python Telegram Bot Library](https://github.com/python-telegram-bot/python-telegram-bot)
- [BotFather Commands](https://core.telegram.org/bots#6-botfather)

## Support 💬

If you encounter issues:
1. Check the application logs
2. Verify environment variables
3. Test with a simple bot message manually
4. Review Telegram API status

---

**Happy Trading! 📈**

