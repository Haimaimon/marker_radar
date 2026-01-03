#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Trading Signals Status
=============================
Why AMZN didn't get a signal?
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
import os

load_dotenv()

print("\n" + "="*80)
print("🔍 TRADING SIGNALS STATUS CHECK")
print("="*80)

# Check environment variables
enable_signals = os.getenv("ENABLE_TRADING_SIGNALS", "false")
min_confidence = os.getenv("SIGNALS_MIN_CONFIDENCE", "75")
signals_style = os.getenv("SIGNALS_STYLE", "rich")

print(f"\n📊 Current Settings:")
print(f"   ENABLE_TRADING_SIGNALS: {enable_signals}")
print(f"   SIGNALS_MIN_CONFIDENCE: {min_confidence}")
print(f"   SIGNALS_STYLE: {signals_style}")

# Check if enabled
is_enabled = enable_signals.lower() in ("true", "1", "yes", "y", "on")

if is_enabled:
    print(f"\n✅ Trading Signals are ENABLED!")
    print(f"   Min confidence: {min_confidence}%")
    print(f"   Format: {signals_style}")
    
    # Test if we can import
    try:
        from signals import SignalEngine, SignalsIntegration
        print(f"\n✅ Signals module imports successfully!")
        
        # Check if we can create engine
        engine = SignalEngine()
        print(f"   Min confidence (engine): {engine.min_confidence}%")
        print(f"   Max risk: {engine.max_risk_pct}%")
        print(f"   Min R/R: {engine.min_rr_ratio}")
        
    except Exception as e:
        print(f"\n❌ Failed to import signals: {e}")
        
else:
    print(f"\n❌ Trading Signals are DISABLED!")
    print(f"\n💡 To enable:")
    print(f"   1. Edit .env")
    print(f"   2. Add: ENABLE_TRADING_SIGNALS=true")
    print(f"   3. Restart app.py")

# Check why AMZN might not get signal
print(f"\n" + "="*80)
print(f"🔍 Why AMZN (score 100) didn't get a signal?")
print(f"="*80)

if not is_enabled:
    print(f"\n❌ REASON: Trading Signals are DISABLED")
    print(f"   Enable them in .env: ENABLE_TRADING_SIGNALS=true")
else:
    print(f"\n✅ Signals are enabled, checking other reasons...")
    
    # Possible reasons:
    print(f"\n📋 Checklist:")
    print(f"   1. ✅ Signals enabled: {is_enabled}")
    print(f"   2. ❓ Market data available: Need to check")
    print(f"   3. ❓ Confidence score: Need to check")
    print(f"   4. ❓ Risk/reward valid: Need to check")
    
    print(f"\n💡 Most common reasons:")
    print(f"   • Market closed (need real-time data)")
    print(f"   • Confidence too low (< {min_confidence}%)")
    print(f"   • Can't get market snapshot (no price data)")
    print(f"   • Risk/reward ratio too low")

print(f"\n" + "="*80)
print(f"💡 SOLUTION")
print(f"="*80)

if not is_enabled:
    print(f"\nEdit your .env file and add:")
    print(f"```")
    print(f"ENABLE_TRADING_SIGNALS=true")
    print(f"SIGNALS_MIN_CONFIDENCE=60")
    print(f"SIGNALS_STYLE=rich")
    print(f"```")
    print(f"\nThen restart: python app.py")
else:
    print(f"\nSignals are enabled. Check logs for:")
    print(f"   • 'No market data for AMZN'")
    print(f"   • 'Confidence XX% < {min_confidence}%'")
    print(f"   • 'Risk/reward too low'")

print(f"\n" + "="*80 + "\n")

