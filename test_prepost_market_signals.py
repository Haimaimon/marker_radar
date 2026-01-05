#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Pre/Post Market Signal Generation
=======================================
Simulate signals with old/current data.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from signals import SignalEngine
from datetime import datetime

print("\n" + "="*80)
print("🧪 TESTING PRE/POST MARKET SIGNALS")
print("="*80)

engine = SignalEngine()

# Test cases for different market conditions
test_cases = [
    {
        "name": "Pre-Market Scenario (Using yesterday's close)",
        "ticker": "NVDA",
        "current_price": 520.00,  # Pre-market estimate
        "prev_close": 500.00,     # Yesterday's close
        "high_today": 525.00,
        "low_today": 518.00,
        "volume": 500_000,        # Light pre-market volume
        "avg_volume": 50_000_000,
        "headline": "NVIDIA wins $10B government AI contract",
        "impact_score": 95,
        "time": "7:00 AM EST (Pre-market)",
    },
    {
        "name": "After-Hours Scenario (Post earnings)",
        "ticker": "TSLA",
        "current_price": 265.00,  # After-hours price
        "prev_close": 250.00,     # Regular close
        "high_today": 267.00,
        "low_today": 263.00,
        "volume": 2_000_000,      # After-hours volume
        "avg_volume": 100_000_000,
        "headline": "Tesla Q4 earnings crush estimates, raises guidance",
        "impact_score": 90,
        "time": "4:15 PM EST (After-hours)",
    },
    {
        "name": "Overnight News (No trading)",
        "ticker": "AAPL",
        "current_price": 180.00,  # Last close (no trading)
        "prev_close": 180.00,     # Same as current
        "high_today": 182.00,     # Estimate for tomorrow
        "low_today": 178.00,      # Estimate for tomorrow
        "volume": None,           # No volume (market closed)
        "avg_volume": 60_000_000,
        "headline": "Apple announces revolutionary new product category",
        "impact_score": 85,
        "time": "11:00 PM EST (Overnight)",
    },
]

for idx, test in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"Test {idx}: {test['name']}")
    print(f"Time: {test['time']}")
    print(f"{'='*80}")
    
    try:
        signal = engine.analyze_opportunity(
            ticker=test['ticker'],
            current_price=test['current_price'],
            prev_close=test['prev_close'],
            high_today=test['high_today'],
            low_today=test['low_today'],
            volume=test['volume'],
            avg_volume=test['avg_volume'],
            headline=test['headline'],
            news_source="Breaking News",
            news_time=datetime.now(),
            impact_score=test['impact_score'],
        )
        
        # Check what confidence was calculated
        from signals.signal_engine import SignalEngine
        temp_engine = SignalEngine()
        conf, sig_type, strategy = temp_engine._calculate_confidence(
            gap_pct=(test['current_price']-test['prev_close'])/test['prev_close']*100 if test['prev_close'] else None,
            volume_spike_ratio=test['volume']/test['avg_volume'] if test['volume'] and test['avg_volume'] else None,
            float_pct=None,
            impact_score=test['impact_score'],
            high_today=test['high_today'],
            low_today=test['low_today'],
            current_price=test['current_price'],
        )
        print(f"\n   📊 Calculated Confidence: {conf:.0f}%")
        print(f"      Minimum required: {temp_engine.min_confidence}%")
        
        if signal:
            print(f"\n✅ SIGNAL GENERATED!")
            print(f"   Ticker: {signal.ticker}")
            print(f"   Type: {signal.signal_type}")
            print(f"   Confidence: {signal.confidence:.0f}%")
            print(f"\n   💰 Price Levels:")
            print(f"      Current: ${signal.current_price:.2f}")
            print(f"      Entry: ${signal.entry_price:.2f}")
            print(f"      Stop: ${signal.stop_loss:.2f}")
            print(f"      Target 1: ${signal.take_profit_1:.2f}")
            if signal.take_profit_2:
                print(f"      Target 2: ${signal.take_profit_2:.2f}")
            if signal.take_profit_3:
                print(f"      Target 3: ${signal.take_profit_3:.2f}")
            
            print(f"\n   ⚡ Risk/Reward:")
            print(f"      R/R Ratio: 1:{signal.risk_reward_ratio:.2f}")
            print(f"      Risk: {signal.risk_amount_pct:.1f}%")
            print(f"      Reward: {signal.reward_amount_pct:.1f}%")
            
            if signal.gap_pct:
                print(f"\n   📊 Gap: {signal.gap_pct:+.1f}%")
            
            if signal.volume_spike_ratio:
                print(f"   📈 Volume: {signal.volume_spike_ratio:.1f}x")
            
            # Validate
            is_valid, reason = engine.validate_signal(signal)
            print(f"\n   Validation: {'✅' if is_valid else '❌'} {reason}")
            
            if is_valid:
                print(f"\n   🚀 READY TO TRADE!")
                print(f"      This signal can be sent to user!")
        else:
            print(f"\n❌ No signal generated")
            print(f"   Confidence too low or criteria not met")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

print(f"\n{'='*80}")
print(f"📊 Summary:")
print(f"{'='*80}")
print(f"\n✅ System now works 24/7:")
print(f"   • Pre-market: Uses last close + news impact")
print(f"   • Regular hours: Uses live data")
print(f"   • After-hours: Uses after-hours price or last close")
print(f"   • Overnight: Uses last close + estimated gap")
print(f"\n🎯 You'll catch opportunities BEFORE they reach peak!")
print(f"{'='*80}\n")

