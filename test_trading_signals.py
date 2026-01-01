#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Trading Signals System
============================
Comprehensive tests for the trading signals engine.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from datetime import datetime
from signals import SignalEngine, SignalFormatter


def test_signal_generation():
    """Test signal generation with various scenarios."""
    
    print("\n" + "="*80)
    print("🧪 Testing Trading Signals System")
    print("="*80 + "\n")
    
    engine = SignalEngine()
    formatter = SignalFormatter()
    
    passed = 0
    failed = 0
    
    # Test cases
    test_cases = [
        {
            "name": "Strong Breakout (High confidence)",
            "ticker": "LCFY",
            "current_price": 7.69,
            "prev_close": 7.41,
            "high_today": 7.74,
            "low_today": 7.41,
            "volume": 74_000,
            "avg_volume": 10_000,
            "headline": "Locally Announces First Signed Contracts Through its Partnership Agreement With eiDNA",
            "news_source": "GlobeNewswire",
            "impact_score": 75,
            "expected_signal": True,
            "expected_type": "BUY",
        },
        {
            "name": "Strong FDA Approval",
            "ticker": "BNTX",
            "current_price": 150.00,
            "prev_close": 140.00,
            "high_today": 155.00,
            "low_today": 145.00,
            "volume": 5_000_000,
            "avg_volume": 1_500_000,
            "headline": "FDA Approves BioNTech's New Cancer Treatment",
            "news_source": "PR Newswire",
            "impact_score": 90,
            "expected_signal": True,
            "expected_type": "BUY",
        },
        {
            "name": "Low Volume Event (Should Fail)",
            "ticker": "TEST",
            "current_price": 50.00,
            "prev_close": 50.00,
            "high_today": 50.50,
            "low_today": 49.50,
            "volume": 100_000,
            "avg_volume": 100_000,
            "headline": "Test Company Announces Something",
            "news_source": "Generic News",
            "impact_score": 50,
            "expected_signal": False,
            "expected_type": None,
        },
        {
            "name": "Massive Gap Up + Volume",
            "ticker": "GME",
            "current_price": 25.00,
            "prev_close": 20.00,
            "high_today": 26.00,
            "low_today": 24.00,
            "volume": 50_000_000,
            "avg_volume": 5_000_000,
            "headline": "GameStop Announces Strategic Partnership with Major Tech Company",
            "news_source": "Business Wire",
            "impact_score": 85,
            "expected_signal": True,
            "expected_type": "BUY",
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print("-" * 80)
        
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
                news_source=test['news_source'],
                news_time=datetime.now(),
                impact_score=test['impact_score'],
            )
            
            # Check if signal generated matches expectation
            if test['expected_signal']:
                if signal:
                    # Validate signal type
                    if signal.signal_type == test['expected_type']:
                        print(f"✅ PASS - Signal generated correctly")
                        print(f"   Ticker: {signal.ticker}")
                        print(f"   Type: {signal.signal_type}")
                        print(f"   Confidence: {signal.confidence:.0f}%")
                        print(f"   Entry: ${signal.entry_price:.2f}")
                        print(f"   Stop: ${signal.stop_loss:.2f}")
                        print(f"   Target: ${signal.take_profit_1:.2f}")
                        print(f"   R/R: 1:{signal.risk_reward_ratio:.2f}")
                        print(f"   Strategy: {signal.strategy}")
                        
                        # Validate signal
                        is_valid, reason = engine.validate_signal(signal)
                        if is_valid:
                            print(f"   Validation: ✅ {reason}")
                            passed += 1
                        else:
                            print(f"   Validation: ❌ {reason}")
                            failed += 1
                    else:
                        print(f"❌ FAIL - Wrong signal type: expected {test['expected_type']}, got {signal.signal_type}")
                        failed += 1
                else:
                    print(f"❌ FAIL - Expected signal but none generated")
                    failed += 1
            else:
                if signal:
                    print(f"❌ FAIL - Signal generated when none expected")
                    print(f"   Confidence: {signal.confidence:.0f}%")
                    failed += 1
                else:
                    print(f"✅ PASS - No signal generated (as expected)")
                    passed += 1
            
            print()
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
            print()
    
    # Summary
    print("="*80)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("="*80)
    
    if failed == 0:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    return failed == 0


def test_signal_formatting():
    """Test signal formatting."""
    
    print("\n" + "="*80)
    print("🎨 Testing Signal Formatting")
    print("="*80 + "\n")
    
    # Create sample signal
    engine = SignalEngine()
    signal = engine.analyze_opportunity(
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
    
    if signal:
        formatter = SignalFormatter()
        
        print("📱 Rich Format (Telegram):")
        print("-" * 80)
        rich_msg = formatter.format_telegram_rich(signal)
        print(rich_msg)
        print()
        
        print("="*80)
        print("📱 Compact Format:")
        print("-" * 80)
        compact_msg = formatter.format_telegram_compact(signal)
        print(compact_msg)
        print()
        
        print("="*80)
        print("💻 Console Format:")
        print("-" * 80)
        console_msg = formatter.format_console(signal)
        print(console_msg)
        
        return True
    else:
        print("❌ Failed to generate signal for formatting test")
        return False


def main():
    """Run all tests."""
    
    print("\n" + "="*100)
    print("🚀 Market Radar - Trading Signals System - Comprehensive Tests")
    print("="*100)
    
    # Test 1: Signal generation
    test1_passed = test_signal_generation()
    
    # Test 2: Signal formatting
    test2_passed = test_signal_formatting()
    
    # Final summary
    print("\n" + "="*100)
    print("📊 Final Summary")
    print("="*100)
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! System is ready.")
        print("\n✅ Trading Signals System:")
        print("   ✅ Signal generation working")
        print("   ✅ Signal validation working")
        print("   ✅ Signal formatting working")
        print("   ✅ Risk/Reward calculation working")
        print("\n🚀 Ready to generate trading signals!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

