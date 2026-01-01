"""
Signal Formatter - Robinhood Style
===================================
Formats trading signals in a beautiful, professional format.
"""

from __future__ import annotations
from signals.signal_engine import TradingSignal
from datetime import datetime
from typing import Optional


class SignalFormatter:
    """Formats signals in Robinhood-style beautiful format."""
    
    @staticmethod
    def format_telegram_rich(signal: TradingSignal) -> str:
        """
        Format signal with rich HTML for Telegram (like Robinhood).
        
        Returns HTML-formatted message.
        """
        
        # Emoji based on signal type
        if signal.signal_type == "BUY":
            emoji = "🔥" if signal.confidence >= 85 else "📈" if signal.confidence >= 75 else "🎯"
            action_color = "green"
        else:
            emoji = "⚠️"
            action_color = "red"
        
        # Confidence emoji
        if signal.confidence >= 90:
            conf_emoji = "🔥🔥🔥"
        elif signal.confidence >= 80:
            conf_emoji = "🔥🔥"
        elif signal.confidence >= 70:
            conf_emoji = "🔥"
        else:
            conf_emoji = "⚡"
        
        # Build message
        lines = []
        
        # Header
        lines.append(f"{emoji} <b>{signal.signal_type} SIGNAL</b>")
        lines.append("")
        
        # Ticker (large and bold)
        lines.append(f"<b><u>{signal.ticker}</u></b>")
        lines.append("")
        
        # Price section
        lines.append("💰 <b>Price Info:</b>")
        lines.append(f"   Current: <b>${signal.current_price:.2f}</b>")
        
        if signal.price_change_pct:
            change_emoji = "📈" if signal.price_change_pct > 0 else "📉"
            lines.append(f"   Change: {change_emoji} <b>{signal.price_change_pct:+.2f}%</b>")
        
        if signal.high_today and signal.low_today:
            lines.append(f"   Range: ${signal.low_today:.2f} - ${signal.high_today:.2f}")
        
        lines.append("")
        
        # Trading levels
        lines.append("🎯 <b>Trading Levels:</b>")
        lines.append(f"   Entry: <b>${signal.entry_price:.2f}</b>")
        lines.append(f"   Stop Loss: <code>${signal.stop_loss:.2f}</code>")
        lines.append(f"   Target 1: <b>${signal.take_profit_1:.2f}</b>")
        
        if signal.take_profit_2:
            lines.append(f"   Target 2: ${signal.take_profit_2:.2f}")
        if signal.take_profit_3:
            lines.append(f"   Target 3: ${signal.take_profit_3:.2f}")
        
        lines.append("")
        
        # Risk/Reward
        if signal.risk_reward_ratio:
            rr_emoji = "✅" if signal.risk_reward_ratio >= 2.5 else "⚡"
            lines.append(f"{rr_emoji} <b>Risk/Reward:</b> 1:{signal.risk_reward_ratio:.2f}")
        
        if signal.risk_amount_pct:
            lines.append(f"   Risk: <code>{signal.risk_amount_pct:.1f}%</code>")
        if signal.reward_amount_pct:
            lines.append(f"   Reward: <b>{signal.reward_amount_pct:.1f}%</b>")
        
        lines.append("")
        
        # Volume section
        if signal.volume_spike_ratio:
            vol_emoji = "🚀" if signal.volume_spike_ratio >= 3.0 else "📊"
            lines.append(f"{vol_emoji} <b>Volume Spike:</b> {signal.volume_spike_ratio:.1f}x")
            
            if signal.volume:
                lines.append(f"   Current: {SignalFormatter._format_number(signal.volume)}")
            if signal.avg_volume:
                lines.append(f"   Average: {SignalFormatter._format_number(signal.avg_volume)}")
            
            lines.append("")
        
        # Float
        if signal.float_percentage:
            float_emoji = "🔥" if signal.float_percentage <= 10 else "📌"
            lines.append(f"{float_emoji} <b>Float:</b> {signal.float_percentage:.1f}%")
            
            if signal.float_percentage <= 5:
                lines.append(f"   <i>Very Low Float - High Volatility Potential!</i>")
            elif signal.float_percentage <= 10:
                lines.append(f"   <i>Low Float - Good Volatility</i>")
            
            lines.append("")
        
        # News context
        if signal.headline:
            lines.append("📰 <b>Catalyst:</b>")
            # Truncate headline if too long
            headline = signal.headline if len(signal.headline) <= 80 else signal.headline[:77] + "..."
            lines.append(f"   <i>{headline}</i>")
            
            if signal.news_source:
                news_time_str = ""
                if signal.news_time:
                    news_time_str = f" • {signal.news_time.strftime('%b-%d %I:%M%p')}"
                lines.append(f"   <code>{signal.news_source}{news_time_str}</code>")
            
            lines.append("")
        
        # Confidence & Strategy
        lines.append(f"{conf_emoji} <b>Confidence:</b> {signal.confidence:.0f}%")
        lines.append(f"   Strategy: <i>{signal.strategy.title()}</i>")
        lines.append(f"   Timeframe: <i>{signal.timeframe.title()}</i>")
        
        lines.append("")
        
        # Timestamp
        time_str = signal.generated_at.strftime("%b-%d at %I:%M%p")
        lines.append(f"🕐 {time_str}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_telegram_compact(signal: TradingSignal) -> str:
        """
        Compact format for quick scanning.
        """
        emoji = "🔥" if signal.confidence >= 80 else "🎯"
        
        change_str = ""
        if signal.price_change_pct:
            change_emoji = "📈" if signal.price_change_pct > 0 else "📉"
            change_str = f" {change_emoji}{signal.price_change_pct:+.1f}%"
        
        vol_str = ""
        if signal.volume_spike_ratio:
            vol_str = f" | Vol: {signal.volume_spike_ratio:.1f}x"
        
        float_str = ""
        if signal.float_percentage:
            float_str = f" | Float: {signal.float_percentage:.1f}%"
        
        message = f"""
{emoji} <b>{signal.ticker}</b> {signal.signal_type}{change_str}

💰 Entry: <b>${signal.entry_price:.2f}</b> | Stop: ${signal.stop_loss:.2f}
🎯 Target: <b>${signal.take_profit_1:.2f}</b> ({signal.reward_amount_pct:+.1f}%)
⚡ R/R: 1:{signal.risk_reward_ratio:.1f}{vol_str}{float_str}

🔥 Confidence: {signal.confidence:.0f}% | {signal.strategy.title()}
"""
        
        if signal.headline:
            message += f"📰 {signal.headline[:60]}...\n"
        
        return message.strip()
    
    @staticmethod
    def format_console(signal: TradingSignal) -> str:
        """Format for console/log output."""
        price_change = signal.price_change_pct if signal.price_change_pct else 0.0
        rr = signal.risk_reward_ratio if signal.risk_reward_ratio else 0.0
        vol_spike = signal.volume_spike_ratio if signal.volume_spike_ratio else 0.0
        float_pct = signal.float_percentage if signal.float_percentage else 0.0
        headline = signal.headline[:60] if signal.headline else 'N/A'
        
        return f"""
{'='*80}
🎯 {signal.signal_type} SIGNAL: {signal.ticker} (Confidence: {signal.confidence:.0f}%)
{'='*80}
Price: ${signal.current_price:.2f} ({price_change:+.2f}% change)
Entry: ${signal.entry_price:.2f}
Stop:  ${signal.stop_loss:.2f}
Target 1: ${signal.take_profit_1:.2f}
Risk/Reward: 1:{rr:.2f}
Volume Spike: {vol_spike:.1f}x
Float: {float_pct:.1f}%
Strategy: {signal.strategy.title()}
News: {headline}
{'='*80}
"""
    
    @staticmethod
    def _format_number(num: int) -> str:
        """Format large numbers with K/M/B suffix."""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K"
        else:
            return str(num)
    
    @staticmethod
    def format_signal_alert(signal: TradingSignal, style: str = "rich") -> str:
        """
        Format signal alert based on style.
        
        Args:
            signal: Trading signal to format
            style: "rich", "compact", or "console"
            
        Returns:
            Formatted message
        """
        if style == "rich":
            return SignalFormatter.format_telegram_rich(signal)
        elif style == "compact":
            return SignalFormatter.format_telegram_compact(signal)
        elif style == "console":
            return SignalFormatter.format_console(signal)
        else:
            return SignalFormatter.format_telegram_rich(signal)

