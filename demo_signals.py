#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Trading Signals Visual
=============================
Beautiful visual demo of trading signals system.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime
from signals import SignalEngine, SignalFormatter


def print_header(text: str):
    """Print a beautiful header."""
    print("\n" + "━" * 100)
    print(f"  {text}")
    print("━" * 100 + "\n")


def demo_signal(name: str, **kwargs):
    """Generate and display a demo signal."""
    print_header(f"📊 {name}")
    
    engine = SignalEngine()
    formatter = SignalFormatter()
    
    # Generate signal
    signal = engine.analyze_opportunity(**kwargs)
    
    if signal:
        # Show analysis
        print(f"✅ Signal Generated!")
        print(f"   Type: {signal.signal_type}")
        print(f"   Confidence: {signal.confidence:.0f}%")
        print(f"   Strategy: {signal.strategy.title()}")
        print()
        
        # Validate
        is_valid, reason = engine.validate_signal(signal)
        print(f"   Validation: {'✅' if is_valid else '❌'} {reason}")
        print()
        
        # Show formatted message
        print_header("📱 Telegram Alert (Rich Format)")
        print(formatter.format_telegram_rich(signal))
        
        print_header("📱 Telegram Alert (Compact Format)")
        print(formatter.format_telegram_compact(signal))
        
    else:
        print("❌ No signal generated (criteria not met)")
    
    print("\n" + "═" * 100 + "\n")


def main():
    """Run demo."""
    
    print("\n" + "═" * 100)
    print("🚀 TRADING SIGNALS SYSTEM - VISUAL DEMO")
    print("═" * 100)
    
    # Demo 1: Real example from your screenshot
    demo_signal(
        name="Real Example: LCFY - Partnership Announcement",
        ticker="LCFY",
        current_price=7.69,
        prev_close=7.41,
        high_today=7.74,
        low_today=7.41,
        volume=74_000,
        avg_volume=10_000,
        headline="Locally Announces First Signed Contracts Through its Partnership Agreement With eiDNA",
        news_source="GlobeNewswire",
        news_time=datetime.now(),
        impact_score=75,
    )
    
    # Demo 2: FDA Approval
    demo_signal(
        name="FDA Approval - High Impact Catalyst",
        ticker="BNTX",
        current_price=155.00,
        prev_close=145.00,
        high_today=157.00,
        low_today=152.00,
        volume=8_000_000,
        avg_volume=2_000_000,
        headline="FDA Approves BioNTech's Breakthrough Cancer Treatment - Phase 3 Results Exceed Expectations",
        news_source="PR Newswire",
        news_time=datetime.now(),
        impact_score=95,
    )
    
    # Demo 3: Earnings Beat
    demo_signal(
        name="Earnings Beat with Revenue Guidance Raise",
        ticker="NVDA",
        current_price=520.00,
        prev_close=480.00,
        high_today=525.00,
        low_today=515.00,
        volume=75_000_000,
        avg_volume=40_000_000,
        headline="NVIDIA Reports Record Q4 Earnings, Beats Estimates, Raises FY Guidance on Strong AI Demand",
        news_source="Business Wire",
        news_time=datetime.now(),
        impact_score=90,
    )
    
    # Demo 4: IPO Pop
    demo_signal(
        name="IPO First Day Trading - Strong Debut",
        ticker="RDDT",
        current_price=50.00,
        prev_close=34.00,  # IPO price
        high_today=52.00,
        low_today=48.00,
        volume=15_000_000,
        avg_volume=5_000_000,  # estimated
        headline="Reddit IPO Soars 47% on First Day of Trading as Social Media Euphoria Returns",
        news_source="MarketWatch",
        news_time=datetime.now(),
        impact_score=85,
    )
    
    # Summary
    print("\n" + "═" * 100)
    print("✅ DEMO COMPLETE!")
    print("═" * 100)
    print("\n💡 This is what your users will see when signals are generated!")
    print("📱 The Rich format is perfect for Telegram with HTML support.")
    print("📊 The Compact format is great for quick scanning on mobile.")
    print("\n🚀 Ready to make money with these signals!\n")


if __name__ == "__main__":
    main()

