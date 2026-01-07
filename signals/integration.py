"""
Signals Integration Module
==========================
Integrates trading signals with the existing Market Radar system
WITHOUT modifying existing code.
"""

from __future__ import annotations
import logging
from typing import Optional
from datetime import datetime, timezone

from signals.signal_engine import SignalEngine, TradingSignal
from signals.signal_formatter import SignalFormatter
from core.models import NewsItem
from market_data.market_data_manager import MarketDataManager

logger = logging.getLogger("market_radar.signals")


class SignalsIntegration:
    """
    Integrates signals engine with Market Radar.
    
    Works alongside existing system without modifying it.
    """
    
    def __init__(
        self,
        signal_engine: SignalEngine,
        market_data: MarketDataManager,
        min_signal_confidence: int = 75,
        enabled: bool = True,
    ):
        """
        Initialize signals integration.
        
        Args:
            signal_engine: Signal generation engine
            market_data: Market data provider
            min_signal_confidence: Minimum confidence to send signal
            enabled: Enable/disable signals
        """
        self.signal_engine = signal_engine
        self.market_data = market_data
        self.min_signal_confidence = min_signal_confidence
        self.enabled = enabled
        self.formatter = SignalFormatter()
        
        logger.info(f"📊 Signals Integration initialized (enabled={enabled}, min_confidence={min_signal_confidence}%)")
    
    def process_news_item(self, item: NewsItem) -> Optional[TradingSignal]:
        """
        Process a news item and generate signal if opportunity exists.
        
        Args:
            item: NewsItem from existing system
            
        Returns:
            TradingSignal if generated, None otherwise
        """
        
        if not self.enabled:
            return None
        
        if not item.ticker:
            logger.debug(f"Skipping signal generation: no ticker for {item.title[:50]}")
            return None
        
        try:
            # Get market data snapshot
            # Note: Works with last available data (Pre/Post/Regular market)
            snapshot = self.market_data.get_snapshot(item.ticker)
            
            if not snapshot or not snapshot.price:
                logger.warning(f"No market data for {item.ticker} - skipping signal")
                return None
            
            # Use last available data (even if market closed)
            # This allows signals in Pre-market and After-hours!
            logger.debug(f"Got market data for {item.ticker}: price=${snapshot.price}")
            
            # Parse news time
            news_time = None
            if item.published:
                try:
                    from utils.date_utils import parse_datetime_utc
                    news_time = parse_datetime_utc(item.published)  # ✅ datetime UTC aware
                except:
                    news_time = datetime.now(timezone.utc)
            
            # Generate signal
            # Note: Works with LAST AVAILABLE data (Pre/Post/Regular market)
            # This allows signal generation 24/7 based on latest known prices!
            current_price = snapshot.price
            prev_close = snapshot.prev_close if snapshot.prev_close else current_price
            
            # Estimate high/low from price movement
            # Works with last available data even if market is closed
            if current_price and prev_close:
                price_change = abs(current_price - prev_close)
                # Conservative estimates for Pre/Post market
                estimated_high = max(current_price, prev_close) + (price_change * 0.15)
                estimated_low = min(current_price, prev_close) - (price_change * 0.1)
            else:
                # Use small range if no previous data
                estimated_high = current_price * 1.02  # +2%
                estimated_low = current_price * 0.98   # -2%
            
            logger.debug(f"Price data for {item.ticker}: current=${current_price:.2f}, prev_close=${prev_close:.2f}")
            
            signal = self.signal_engine.analyze_opportunity(
                ticker=item.ticker,
                current_price=current_price,
                prev_close=prev_close,
                high_today=estimated_high,
                low_today=estimated_low,
                volume=int(snapshot.volume) if snapshot.volume else None,
                avg_volume=int(snapshot.avg_volume_10d) if snapshot.avg_volume_10d else None,
                float_shares=None,  # TODO: Get from data provider
                outstanding_shares=None,  # TODO: Get from data provider
                headline=item.title,
                news_source=item.source,
                news_time=news_time,
                impact_score=item.impact_score,
            )
            
            if signal:
                # Validate signal
                is_valid, reason = self.signal_engine.validate_signal(signal)
                
                if is_valid:
                    logger.info(f"✅ Valid signal generated for {signal.ticker}")
                    return signal
                else:
                    logger.debug(f"❌ Invalid signal for {item.ticker}: {reason}")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating signal for {item.ticker}: {e}", exc_info=True)
            return None
    
    def format_signal_message(
        self,
        signal: TradingSignal,
        style: str = "rich"
    ) -> str:
        """
        Format signal for notification.
        
        Args:
            signal: Trading signal
            style: "rich" (detailed), "compact", or "console"
            
        Returns:
            Formatted message
        """
        return self.formatter.format_signal_alert(signal, style=style)
    
    def should_send_signal(self, signal: TradingSignal) -> bool:
        """
        Determine if signal should be sent to user.
        
        Args:
            signal: Trading signal
            
        Returns:
            True if should send, False otherwise
        """
        
        if not self.enabled:
            return False
        
        # Check confidence threshold
        if signal.confidence < self.min_signal_confidence:
            logger.debug(f"Signal confidence {signal.confidence:.0f}% < threshold {self.min_signal_confidence}%")
            return False
        
        # Additional filters can be added here
        # e.g., trading hours, blacklist tickers, etc.
        
        return True

