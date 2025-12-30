#!/usr/bin/env python3
"""
Test script for Telegram integration
Run this to verify your Telegram configuration before starting the main app
"""

from __future__ import annotations
import sys
import logging
from config import settings
from notifier.telegram import TelegramNotifier
from core.models import NewsItem

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("telegram_test")


def test_telegram_config():
    """Test Telegram configuration"""
    logger.info("Testing Telegram configuration...")
    
    if not settings.enable_telegram:
        logger.error("❌ ENABLE_TELEGRAM is not set to true")
        return False
    
    if not settings.telegram_bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN is not set")
        return False
    
    if not settings.telegram_chat_id:
        logger.error("❌ TELEGRAM_CHAT_ID is not set")
        return False
    
    logger.info("✅ Configuration looks good")
    return True


def test_connection():
    """Test connection to Telegram API"""
    logger.info("Testing Telegram API connection...")
    
    try:
        notifier = TelegramNotifier(
            bot_token=settings.telegram_bot_token,
            chat_id=settings.telegram_chat_id,
            silent=settings.telegram_silent,
            thread_id=settings.telegram_thread_id if settings.telegram_thread_id else None,
        )
        
        if notifier.send_test_message():
            logger.info("✅ Test message sent successfully!")
            return notifier
        else:
            logger.error("❌ Failed to send test message")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error creating notifier: {e}")
        return None


def test_notification():
    """Test sending a formatted notification"""
    logger.info("Testing notification with sample data...")
    
    notifier = test_connection()
    if not notifier:
        return False
    
    # Create a sample NewsItem
    sample_item = NewsItem(
        source="TEST",
        title="Sample Market Alert: Tech Giant Announces Major Acquisition",
        link="https://example.com/news/12345",
        published="2025-12-29 14:30:00",
        summary="Breaking: Major tech company announces acquisition of AI startup for $2B",
        ticker="AAPL",
        impact_score=85,
        impact_reason="Major acquisition announcement",
        gap_pct=5.23,
        vol_spike=2.45,
        validated=True,
        validation_reason="Strong market reaction detected",
        uid="test_notification_123"
    )
    
    try:
        notifier.notify(sample_item)
        logger.info("✅ Sample notification sent successfully!")
        logger.info("Check your Telegram to see the formatted message")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send notification: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Market Radar - Telegram Integration Test")
    logger.info("=" * 60)
    
    # Test 1: Configuration
    if not test_telegram_config():
        logger.error("\n❌ Configuration test failed")
        logger.info("\nPlease check your .env file and ensure:")
        logger.info("  - ENABLE_TELEGRAM=true")
        logger.info("  - TELEGRAM_BOT_TOKEN is set (from @BotFather)")
        logger.info("  - TELEGRAM_CHAT_ID is set (from @userinfobot)")
        logger.info("\nSee notifier/TELEGRAM_SETUP.md for detailed instructions")
        sys.exit(1)
    
    # Test 2: Connection
    logger.info("\n" + "=" * 60)
    if not test_connection():
        logger.error("\n❌ Connection test failed")
        logger.info("\nPossible issues:")
        logger.info("  - Bot token is incorrect")
        logger.info("  - Chat ID is incorrect")
        logger.info("  - Bot is blocked or not started")
        logger.info("  - Network connectivity issues")
        sys.exit(1)
    
    # Test 3: Formatted notification
    logger.info("\n" + "=" * 60)
    if not test_notification():
        logger.error("\n❌ Notification test failed")
        sys.exit(1)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ All tests passed successfully!")
    logger.info("=" * 60)
    logger.info("\nYour Telegram integration is ready to use.")
    logger.info("You can now run the main application with: python app.py")
    

if __name__ == "__main__":
    main()

