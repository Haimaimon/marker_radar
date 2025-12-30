#!/usr/bin/env python3
"""
Advanced Telegram usage examples for Market Radar

This file demonstrates various advanced features of the Telegram integration.
"""

from __future__ import annotations
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from notifier.telegram import TelegramNotifier
from core.models import NewsItem


def example_basic_notification():
    """Example: Send a basic notification"""
    print("Example 1: Basic Notification\n" + "=" * 50)
    
    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
    )
    
    item = NewsItem(
        source="Reuters",
        title="Tech Company Announces Breakthrough in Quantum Computing",
        link="https://example.com/news/quantum",
        ticker="QCOM",
        impact_score=88,
        impact_reason="Major technological breakthrough",
        validated=True,
        validation_reason="Strong market reaction with high volume",
        gap_pct=6.5,
        vol_spike=3.2,
    )
    
    notifier.notify(item)
    print("✅ Basic notification sent!\n")


def example_batch_notification():
    """Example: Send multiple events in a batch"""
    print("Example 2: Batch Notification\n" + "=" * 50)
    
    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
    )
    
    items = [
        NewsItem(
            source="Bloomberg",
            title="Banking Giant Reports Record Q4 Earnings",
            link="https://example.com/news/bank1",
            ticker="JPM",
            impact_score=82,
            impact_reason="Better than expected earnings",
            validated=True,
            validation_reason="Significant price movement",
        ),
        NewsItem(
            source="CNBC",
            title="Tech Startup Announces $500M Funding Round",
            link="https://example.com/news/startup1",
            ticker="TECH",
            impact_score=75,
            impact_reason="Large funding announcement",
            validated=True,
            validation_reason="Increased trading activity",
        ),
        NewsItem(
            source="WSJ",
            title="Pharma Company Gets FDA Approval for New Drug",
            link="https://example.com/news/pharma1",
            ticker="PFE",
            impact_score=91,
            impact_reason="FDA approval - major catalyst",
            validated=True,
            validation_reason="Strong volume spike",
        ),
    ]
    
    notifier.notify_batch(items)
    print("✅ Batch notification sent!\n")


def example_silent_notification():
    """Example: Send notification without sound"""
    print("Example 3: Silent Notification\n" + "=" * 50)
    
    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
        silent=True,  # No notification sound
    )
    
    item = NewsItem(
        source="MarketWatch",
        title="Low Impact Market Update",
        link="https://example.com/news/update",
        ticker="SPY",
        impact_score=65,
        impact_reason="Regular market update",
        validated=False,
        validation_reason="Below validation thresholds",
    )
    
    notifier.notify(item)
    print("✅ Silent notification sent (no sound)!\n")


def example_with_buttons():
    """Example: Send message with interactive buttons"""
    print("Example 4: Message with Buttons\n" + "=" * 50)
    
    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
    )
    
    message = (
        "🔥 <b>AAPL - Major Announcement</b>\n\n"
        "Apple announces new product line expected to drive significant revenue growth.\n\n"
        "Impact Score: 92\n"
        "Current Price: $175.25 (+5.3%)"
    )
    
    buttons = [
        ("📈 View Chart", "https://finance.yahoo.com/chart/AAPL"),
        ("📰 Read News", "https://example.com/news/aapl"),
        ("💹 Trading View", "https://tradingview.com/symbols/AAPL"),
    ]
    
    notifier.send_message_with_buttons(message, buttons)
    print("✅ Message with buttons sent!\n")


def example_summary():
    """Example: Send daily/hourly summary"""
    print("Example 5: Summary Message\n" + "=" * 50)
    
    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
    )
    
    notifier.send_summary(
        total_events=156,
        validated_events=23,
        top_ticker="NVDA",
    )
    print("✅ Summary sent!\n")


def example_alerts():
    """Example: Send system alerts"""
    print("Example 6: System Alerts\n" + "=" * 50)
    
    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
    )
    
    # Info alert
    notifier.send_alert(
        title="System Started",
        message="Market Radar monitoring system has been started successfully.",
        level="info",
    )
    
    # Warning alert
    notifier.send_alert(
        title="High Activity Detected",
        message="Unusual number of events detected in the last hour. System may be under heavy load.",
        level="warning",
    )
    
    # Error alert
    notifier.send_alert(
        title="Data Source Error",
        message="Failed to fetch data from SEC RSS feed. Will retry in 30 seconds.",
        level="error",
    )
    
    print("✅ Alerts sent!\n")


def example_retry_handling():
    """Example: Demonstrate retry logic"""
    print("Example 7: Retry Logic\n" + "=" * 50)
    
    notifier = TelegramNotifier(
        bot_token=settings.telegram_bot_token,
        chat_id=settings.telegram_chat_id,
        retry_attempts=5,  # More retries
        retry_delay=1,     # Faster retries
    )
    
    print("Notifier configured with 5 retry attempts and 1s initial delay")
    print("If a message fails, it will automatically retry with exponential backoff")
    print("Delays: 1s, 2s, 4s, 8s, 16s\n")
    
    # This will succeed (assuming valid config)
    notifier.send_test_message()
    print("✅ Retry example completed!\n")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Market Radar - Advanced Telegram Integration Examples")
    print("=" * 60 + "\n")
    
    if not settings.enable_telegram:
        print("❌ Telegram is not enabled in configuration")
        print("Set ENABLE_TELEGRAM=true in your .env file")
        return
    
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        print("❌ Telegram credentials not configured")
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your .env file")
        return
    
    print("Choose an example to run:")
    print("1. Basic Notification")
    print("2. Batch Notification (multiple events)")
    print("3. Silent Notification (no sound)")
    print("4. Message with Interactive Buttons")
    print("5. Summary Message")
    print("6. System Alerts (info/warning/error)")
    print("7. Retry Logic Demonstration")
    print("8. Run All Examples")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-8): ").strip()
    
    examples = {
        "1": example_basic_notification,
        "2": example_batch_notification,
        "3": example_silent_notification,
        "4": example_with_buttons,
        "5": example_summary,
        "6": example_alerts,
        "7": example_retry_handling,
    }
    
    if choice == "0":
        print("Goodbye!")
        return
    elif choice == "8":
        print("\n🚀 Running all examples...\n")
        for func in examples.values():
            func()
            input("Press Enter to continue to next example...")
    elif choice in examples:
        examples[choice]()
    else:
        print("❌ Invalid choice")
    
    print("\n" + "=" * 60)
    print("Examples completed! Check your Telegram for messages.")
    print("=" * 60)


if __name__ == "__main__":
    main()

