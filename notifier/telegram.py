from __future__ import annotations
import logging
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests
from requests.exceptions import RequestException, Timeout
from core.models import NewsItem


logger = logging.getLogger("market_radar.telegram")


class TelegramNotifier:
    """
    Enhanced Telegram notifier with:
    - HTML formatting for rich messages
    - Automatic retry logic with exponential backoff
    - Error handling and logging
    - Support for silent notifications
    - Support for topic/thread IDs
    - Message length validation
    """
    
    MAX_MESSAGE_LENGTH = 4096
    
    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        silent: bool = False,
        thread_id: Optional[str] = None,
        retry_attempts: int = 3,
        retry_delay: int = 2,
    ):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.silent = silent
        self.thread_id = thread_id
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        logger.info(
            f"TelegramNotifier initialized: chat_id={chat_id}, "
            f"silent={silent}, thread_id={thread_id or 'None'}"
        )
    
    def notify(self, item: NewsItem) -> None:
        """Send notification for a NewsItem"""
        try:
            text = self._format_message(item)
            self._send_message(text)
            logger.info(f"Notification sent successfully for {item.ticker or 'N/A'}: {item.title[:50]}...")
        except Exception as e:
            logger.error(f"Failed to send notification for {item.ticker or 'N/A'}: {e}", exc_info=True)
    
    def _format_message(self, item: NewsItem) -> str:
        """Format NewsItem as rich HTML message"""
        # Emoji based on score
        if item.impact_score >= 90:
            emoji = "🚨"  # Critical
        elif item.impact_score >= 80:
            emoji = "🔥"  # High
        elif item.impact_score >= 70:
            emoji = "⚡"  # Medium
        else:
            emoji = "📊"  # Low
        
        # Validation emoji
        validation_emoji = "✅" if item.validated else "⚠️"
        
        # Build message parts
        parts = [
            f"{emoji} <b>{self._escape_html(item.ticker or 'N/A')}</b> | Score: {item.impact_score}",
            "",
            f"<b>{self._escape_html(item.title)}</b>",
            "",
            f"📰 <b>Source:</b> {self._escape_html(item.source)}",
        ]
        
        # Add market data if available
        if item.gap_pct is not None:
            gap_emoji = "📈" if item.gap_pct > 0 else "📉"
            parts.append(f"{gap_emoji} <b>Gap:</b> {item.gap_pct:.2f}%")
        
        if item.vol_spike is not None:
            parts.append(f"📊 <b>Volume Spike:</b> {item.vol_spike:.2f}x")
        
        # Add validation info
        parts.append(f"\n{validation_emoji} <b>Validation:</b> {self._escape_html(item.validation_reason)}")
        
        # Add impact reason
        if item.impact_reason:
            parts.append(f"💡 <b>Impact:</b> {self._escape_html(item.impact_reason)}")
        
        # Add timestamp if available
        if item.published:
            parts.append(f"🕒 {self._escape_html(item.published)}")
        
        # Add link
        parts.append(f"\n🔗 <a href=\"{item.link}\">Read Full Article</a>")
        
        message = "\n".join(parts)
        
        # Truncate if too long
        if len(message) > self.MAX_MESSAGE_LENGTH:
            message = message[:self.MAX_MESSAGE_LENGTH - 100] + "\n\n... (truncated)"
            logger.warning(f"Message truncated for {item.ticker}")
        
        return message
    
    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters"""
        if not text:
            return ""
        return (
            text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((RequestException, Timeout)),
        reraise=True,
    )
    def _send_message(self, text: str) -> None:
        """
        Send message to Telegram with retry logic
        Uses exponential backoff: 1s, 2s, 4s, 8s...
        """
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
            "disable_notification": self.silent,
        }
        
        # Add thread ID if specified (for topic-enabled groups)
        if self.thread_id:
            payload["message_thread_id"] = self.thread_id
        
        response = requests.post(self.api_url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if not result.get("ok"):
            error_msg = result.get("description", "Unknown error")
            raise RuntimeError(f"Telegram API error: {error_msg}")
    
    def send_test_message(self) -> bool:
        """
        Send a test message to verify configuration
        Returns True if successful, False otherwise
        """
        try:
            test_text = (
                "🧪 <b>Market Radar Test Message</b>\n\n"
                "✅ Telegram integration is working correctly!\n"
                "You will receive notifications here when significant market events are detected."
            )
            self._send_message(test_text)
            logger.info("Test message sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send test message: {e}")
            return False
    
    def notify_batch(self, items: list[NewsItem]) -> None:
        """
        Send multiple notifications in batch
        Useful for summarizing multiple events
        """
        if not items:
            return
        
        try:
            # If only one item, use regular notify
            if len(items) == 1:
                self.notify(items[0])
                return
            
            # Create summary message
            text = self._format_batch_message(items)
            self._send_message(text)
            logger.info(f"Batch notification sent for {len(items)} items")
        except Exception as e:
            logger.error(f"Failed to send batch notification: {e}", exc_info=True)
    
    def _format_batch_message(self, items: list[NewsItem]) -> str:
        """Format multiple NewsItems as a summary message"""
        parts = [
            "📊 <b>Market Radar - Multiple Events Detected</b>",
            f"<b>{len(items)} events</b> in this batch\n",
        ]
        
        for i, item in enumerate(items[:10], 1):  # Limit to 10 to avoid message length
            emoji = "🔥" if item.impact_score >= 80 else "⚡"
            parts.append(
                f"{i}. {emoji} <b>{self._escape_html(item.ticker or 'N/A')}</b> "
                f"(Score: {item.impact_score})\n"
                f"   {self._escape_html(item.title[:80])}...\n"
                f"   <a href=\"{item.link}\">Read more</a>\n"
            )
        
        if len(items) > 10:
            parts.append(f"\n... and {len(items) - 10} more events")
        
        return "\n".join(parts)
    
    def send_summary(self, total_events: int, validated_events: int, top_ticker: str = None) -> None:
        """
        Send a summary message (useful for daily/hourly summaries)
        """
        try:
            parts = [
                "📈 <b>Market Radar Summary</b>\n",
                f"📊 Total events processed: {total_events}",
                f"✅ Validated events: {validated_events}",
            ]
            
            if top_ticker:
                parts.append(f"🔥 Most active ticker: <b>{self._escape_html(top_ticker)}</b>")
            
            text = "\n".join(parts)
            self._send_message(text)
            logger.info("Summary message sent")
        except Exception as e:
            logger.error(f"Failed to send summary: {e}", exc_info=True)
    
    def send_message_with_buttons(self, text: str, buttons: list[tuple[str, str]]) -> None:
        """
        Send a message with inline keyboard buttons
        
        Args:
            text: Message text (HTML formatted)
            buttons: List of (button_text, url) tuples
        
        Example:
            notifier.send_message_with_buttons(
                "Check out this stock!",
                [("View Chart", "https://example.com/chart"), ("Read News", "https://example.com/news")]
            )
        """
        try:
            # Create inline keyboard
            keyboard = {
                "inline_keyboard": [
                    [{"text": text, "url": url}] for text, url in buttons
                ]
            }
            
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
                "disable_notification": self.silent,
                "reply_markup": keyboard,
            }
            
            if self.thread_id:
                payload["message_thread_id"] = self.thread_id
            
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("Message with buttons sent successfully")
        except Exception as e:
            logger.error(f"Failed to send message with buttons: {e}", exc_info=True)
    
    def send_alert(self, title: str, message: str, level: str = "info") -> None:
        """
        Send a system alert message
        
        Args:
            title: Alert title
            message: Alert message
            level: Alert level - "info", "warning", "error", "critical"
        """
        emoji_map = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨",
        }
        
        emoji = emoji_map.get(level, "ℹ️")
        
        try:
            text = (
                f"{emoji} <b>{self._escape_html(title)}</b>\n\n"
                f"{self._escape_html(message)}"
            )
            self._send_message(text)
            logger.info(f"Alert sent: {title} ({level})")
        except Exception as e:
            logger.error(f"Failed to send alert: {e}", exc_info=True)
