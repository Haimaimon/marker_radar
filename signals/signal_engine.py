"""
Trading Signals Engine - Professional Grade
===========================================
Analyzes market data and generates actionable trading signals.

Features:
- Technical analysis (price action, volume, float)
- Entry/Stop/Target calculation
- Risk/Reward analysis
- Signal confidence scoring
- Multi-timeframe analysis
"""

from __future__ import annotations
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("market_radar.signals")


@dataclass
class TradingSignal:
    """Represents a trading signal with all relevant data."""
    
    # Basic info
    ticker: str
    signal_type: str  # "BUY", "SELL", "HOLD"
    confidence: float  # 0-100
    
    # Price levels
    current_price: float
    entry_price: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: Optional[float] = None
    take_profit_3: Optional[float] = None
    
    # Technical data
    volume: Optional[int] = None
    avg_volume: Optional[int] = None
    volume_spike_ratio: Optional[float] = None
    float_percentage: Optional[float] = None
    high_today: Optional[float] = None
    low_today: Optional[float] = None
    
    # Price movement
    price_change_pct: Optional[float] = None
    gap_pct: Optional[float] = None
    
    # Risk metrics
    risk_reward_ratio: Optional[float] = None
    risk_amount_pct: Optional[float] = None
    reward_amount_pct: Optional[float] = None
    
    # News context
    headline: Optional[str] = None
    news_source: Optional[str] = None
    news_time: Optional[datetime] = None
    impact_score: Optional[int] = None
    
    # Signal metadata
    generated_at: datetime = None
    timeframe: str = "intraday"  # "intraday", "swing", "position"
    strategy: str = "breakout"  # "breakout", "reversal", "momentum", "news"
    
    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now()
        
        # Calculate risk/reward if not provided
        if self.risk_reward_ratio is None and self.entry_price and self.stop_loss and self.take_profit_1:
            self._calculate_risk_reward()
    
    def _calculate_risk_reward(self):
        """Calculate risk/reward ratio."""
        risk = abs(self.entry_price - self.stop_loss)
        reward = abs(self.take_profit_1 - self.entry_price)
        
        if risk > 0:
            self.risk_reward_ratio = reward / risk
            self.risk_amount_pct = (risk / self.entry_price) * 100
            self.reward_amount_pct = (reward / self.entry_price) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/API."""
        return {
            "ticker": self.ticker,
            "signal_type": self.signal_type,
            "confidence": self.confidence,
            "current_price": self.current_price,
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "take_profit_1": self.take_profit_1,
            "take_profit_2": self.take_profit_2,
            "take_profit_3": self.take_profit_3,
            "volume": self.volume,
            "avg_volume": self.avg_volume,
            "volume_spike_ratio": self.volume_spike_ratio,
            "float_percentage": self.float_percentage,
            "high_today": self.high_today,
            "low_today": self.low_today,
            "price_change_pct": self.price_change_pct,
            "gap_pct": self.gap_pct,
            "risk_reward_ratio": self.risk_reward_ratio,
            "risk_amount_pct": self.risk_amount_pct,
            "reward_amount_pct": self.reward_amount_pct,
            "headline": self.headline,
            "news_source": self.news_source,
            "news_time": self.news_time.isoformat() if self.news_time else None,
            "impact_score": self.impact_score,
            "generated_at": self.generated_at.isoformat(),
            "timeframe": self.timeframe,
            "strategy": self.strategy,
        }


class SignalEngine:
    """
    Main engine for generating trading signals.
    
    Uses technical analysis, price action, volume analysis, and news sentiment
    to generate high-probability trading signals.
    
    ⚡ WORKS 24/7: Pre-market, Regular hours, After-hours!
    Uses last available market data to generate signals anytime.
    """
    
    def __init__(self):
        self.min_confidence = 40  # Minimum confidence (lowered for Pre/Post market)
        self.max_risk_pct = 15.0  # Maximum risk per trade (%) - higher for volatile Pre/Post
        self.min_rr_ratio = 1.5  # Minimum risk/reward ratio
    
    def analyze_opportunity(
        self,
        ticker: str,
        current_price: float,
        prev_close: Optional[float],
        high_today: Optional[float],
        low_today: Optional[float],
        volume: Optional[int],
        avg_volume: Optional[int],
        float_shares: Optional[int] = None,
        outstanding_shares: Optional[int] = None,
        headline: Optional[str] = None,
        news_source: Optional[str] = None,
        news_time: Optional[datetime] = None,
        impact_score: Optional[int] = None,
    ) -> Optional[TradingSignal]:
        """
        Analyze a trading opportunity and generate signal if criteria met.
        
        Args:
            ticker: Stock ticker
            current_price: Current price
            prev_close: Previous close price
            high_today: Today's high
            low_today: Today's low
            volume: Current volume
            avg_volume: Average volume (10-day)
            float_shares: Float shares
            outstanding_shares: Total outstanding shares
            headline: News headline
            news_source: News source
            news_time: News timestamp
            impact_score: News impact score (0-100)
            
        Returns:
            TradingSignal if opportunity found, None otherwise
        """
        
        # Calculate derived metrics
        gap_pct = None
        price_change_pct = None
        if prev_close and prev_close > 0:
            gap_pct = ((current_price - prev_close) / prev_close) * 100
            price_change_pct = gap_pct
        
        volume_spike_ratio = None
        if volume and avg_volume and avg_volume > 0:
            volume_spike_ratio = volume / avg_volume
        
        float_pct = None
        if float_shares and outstanding_shares and outstanding_shares > 0:
            float_pct = (float_shares / outstanding_shares) * 100
        
        # Score the opportunity
        confidence, signal_type, strategy = self._calculate_confidence(
            gap_pct=gap_pct,
            volume_spike_ratio=volume_spike_ratio,
            float_pct=float_pct,
            impact_score=impact_score,
            high_today=high_today,
            low_today=low_today,
            current_price=current_price,
        )
        
        # Only generate signal if confidence is high enough
        if confidence < self.min_confidence:
            logger.debug(f"Skipping {ticker}: confidence {confidence:.1f}% < {self.min_confidence}%")
            return None
        
        # Calculate entry/stop/targets
        entry, stop, targets = self._calculate_levels(
            current_price=current_price,
            high_today=high_today,
            low_today=low_today,
            prev_close=prev_close,
            signal_type=signal_type,
            strategy=strategy,
        )
        
        # Validate risk/reward
        risk = abs(entry - stop)
        reward = abs(targets[0] - entry)
        rr_ratio = reward / risk if risk > 0 else 0
        
        if rr_ratio < self.min_rr_ratio:
            logger.debug(f"Skipping {ticker}: R/R {rr_ratio:.2f} < {self.min_rr_ratio}")
            return None
        
        # Create signal
        signal = TradingSignal(
            ticker=ticker,
            signal_type=signal_type,
            confidence=confidence,
            current_price=current_price,
            entry_price=entry,
            stop_loss=stop,
            take_profit_1=targets[0],
            take_profit_2=targets[1] if len(targets) > 1 else None,
            take_profit_3=targets[2] if len(targets) > 2 else None,
            volume=volume,
            avg_volume=avg_volume,
            volume_spike_ratio=volume_spike_ratio,
            float_percentage=float_pct,
            high_today=high_today,
            low_today=low_today,
            price_change_pct=price_change_pct,
            gap_pct=gap_pct,
            headline=headline,
            news_source=news_source,
            news_time=news_time,
            impact_score=impact_score,
            strategy=strategy,
        )
        
        logger.info(f"🎯 Signal generated: {ticker} {signal_type} @ ${entry:.2f} (Confidence: {confidence:.0f}%)")
        
        return signal
    
    def _calculate_confidence(
        self,
        gap_pct: Optional[float],
        volume_spike_ratio: Optional[float],
        float_pct: Optional[float],
        impact_score: Optional[int],
        high_today: Optional[float],
        low_today: Optional[float],
        current_price: Optional[float],
    ) -> Tuple[float, str, str]:
        """
        Calculate signal confidence score (0-100).
        
        Returns:
            (confidence, signal_type, strategy)
        """
        confidence = 0
        signal_type = "BUY"  # Default
        strategy = "breakout"
        
        # News impact (+30 points max)
        if impact_score:
            confidence += min(impact_score * 0.3, 30)
        
        # Volume spike (+25 points max)
        # Note: In Pre/Post market, volume might be low or None
        if volume_spike_ratio:
            if volume_spike_ratio >= 5.0:
                confidence += 25
            elif volume_spike_ratio >= 3.0:
                confidence += 20
            elif volume_spike_ratio >= 2.0:
                confidence += 15
            elif volume_spike_ratio >= 1.5:
                confidence += 10
        elif volume_spike_ratio is None:
            # Pre/Post market - no volume data
            # Give partial credit based on news impact
            if impact_score and impact_score >= 80:
                confidence += 15  # Strong news compensates for no volume
            elif impact_score and impact_score >= 60:
                confidence += 10
        
        # Price gap (+20 points max)
        if gap_pct:
            if abs(gap_pct) >= 20:
                confidence += 20
            elif abs(gap_pct) >= 10:
                confidence += 15
            elif abs(gap_pct) >= 5:
                confidence += 10
            elif abs(gap_pct) >= 3:
                confidence += 8
            elif abs(gap_pct) >= 1:
                confidence += 5
            
            # Determine direction
            if gap_pct > 0:
                signal_type = "BUY"
                strategy = "breakout" if gap_pct > 10 else "momentum"
            else:
                signal_type = "SELL"
                strategy = "reversal"
        
        # Float analysis (+15 points max)
        if float_pct:
            if float_pct <= 5:
                confidence += 15  # Very low float = more volatile
            elif float_pct <= 10:
                confidence += 12
            elif float_pct <= 20:
                confidence += 8
            elif float_pct <= 30:
                confidence += 5
        
        # Price action (+10 points max)
        if high_today and low_today and current_price:
            range_size = high_today - low_today
            if range_size > 0:
                position_in_range = (current_price - low_today) / range_size
                
                if position_in_range >= 0.8:
                    confidence += 10  # Near highs
                elif position_in_range <= 0.2:
                    confidence += 8  # Near lows (reversal potential)
                else:
                    confidence += 5  # Mid-range
        
        return min(confidence, 100), signal_type, strategy
    
    def _calculate_levels(
        self,
        current_price: float,
        high_today: Optional[float],
        low_today: Optional[float],
        prev_close: Optional[float],
        signal_type: str,
        strategy: str,
    ) -> Tuple[float, float, list]:
        """
        Calculate entry, stop loss, and target prices.
        
        Returns:
            (entry, stop, [target1, target2, target3])
        """
        
        if signal_type == "BUY":
            # Entry: slightly above current (breakout confirmation)
            entry = current_price * 1.005  # 0.5% above
            
            # Stop loss: based on strategy
            if strategy == "breakout":
                # Stop below breakout level
                if prev_close:
                    stop = prev_close * 0.98  # 2% below previous close
                else:
                    stop = current_price * 0.95  # 5% stop
            elif strategy == "momentum":
                # Tighter stop for momentum
                stop = current_price * 0.97  # 3% stop
            else:
                # Standard stop
                stop = current_price * 0.96  # 4% stop
            
            # Targets: based on R/R ratio
            risk = entry - stop
            target1 = entry + (risk * 2)  # 2R
            target2 = entry + (risk * 3)  # 3R
            target3 = entry + (risk * 4)  # 4R
            
        else:  # SELL
            entry = current_price * 0.995  # 0.5% below
            stop = current_price * 1.05  # 5% stop
            risk = stop - entry
            target1 = entry - (risk * 2)
            target2 = entry - (risk * 3)
            target3 = entry - (risk * 4)
        
        return entry, stop, [target1, target2, target3]
    
    def validate_signal(self, signal: TradingSignal) -> Tuple[bool, str]:
        """
        Validate signal before sending.
        
        Returns:
            (is_valid, reason)
        """
        
        # Check confidence
        if signal.confidence < self.min_confidence:
            return False, f"Confidence too low: {signal.confidence:.0f}%"
        
        # Check R/R ratio
        if signal.risk_reward_ratio and signal.risk_reward_ratio < self.min_rr_ratio:
            return False, f"R/R too low: {signal.risk_reward_ratio:.2f}"
        
        # Check risk amount
        if signal.risk_amount_pct and signal.risk_amount_pct > self.max_risk_pct:
            return False, f"Risk too high: {signal.risk_amount_pct:.1f}%"
        
        # Check price levels make sense
        if signal.signal_type == "BUY":
            if signal.stop_loss >= signal.entry_price:
                return False, "Invalid levels: stop >= entry"
            if signal.take_profit_1 <= signal.entry_price:
                return False, "Invalid levels: target <= entry"
        else:
            if signal.stop_loss <= signal.entry_price:
                return False, "Invalid levels: stop <= entry"
            if signal.take_profit_1 >= signal.entry_price:
                return False, "Invalid levels: target >= entry"
        
        return True, "Valid"

