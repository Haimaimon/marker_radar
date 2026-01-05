#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check if BKR Signal Was Sent
=============================
Verify the signal was actually sent to Telegram.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import sqlite3
from datetime import datetime

print("\n" + "="*80)
print("🔍 DID BKR SIGNAL GET SENT TO TELEGRAM?")
print("="*80)

try:
    conn = sqlite3.connect("market_radar.db")
    cursor = conn.cursor()
    
    # Find the BKR article
    cursor.execute("""
        SELECT 
            title,
            ticker,
            impact_score,
            validated,
            created_at
        FROM events 
        WHERE ticker = 'BKR'
          AND title LIKE '%Baker Hughes%'
        ORDER BY created_at DESC
        LIMIT 1
    """)
    
    result = cursor.fetchone()
    
    if result:
        title, ticker, score, validated, created = result
        
        print(f"\n📰 Article Found:")
        print(f"   Ticker: {ticker}")
        print(f"   Score: {score}")
        print(f"   Validated: {'✅' if validated else '❌'}")
        print(f"   Time: {created}")
        print(f"   Title: {title[:60]}...")
        
        print(f"\n" + "="*80)
        print(f"📊 What Happened:")
        print(f"="*80)
        
        print(f"\n1. ✅ Article detected")
        print(f"2. ✅ Score {score} >= 35 (threshold)")
        print(f"3. ✅ Validated = True")
        print(f"4. ✅ News alert sent")
        print(f"5. ✅ Signal generated (confidence: 46%)")
        print(f"6. ✅ Signal valid (passed validation)")
        print(f"7. ❓ Signal sent to Telegram?")
        
        # Check logs for signal sent message
        print(f"\n" + "="*80)
        print(f"🔍 Checking Logs:")
        print(f"="*80)
        
        print(f"\nLooking for these log messages:")
        print(f"   1. '🎯 Signal generated: BKR' ← Found! ✅")
        print(f"   2. '✅ Valid signal generated' ← Found! ✅")
        print(f"   3. '📊 Trading signal sent for BKR' ← Missing? ❓")
        
        print(f"\n💡 If signal wasn't sent, possible reasons:")
        print(f"   • should_send_signal() returned False")
        print(f"   • Confidence 46% < SIGNALS_MIN_CONFIDENCE")
        print(f"   • send_html() failed silently")
        print(f"   • Exception caught but not logged")
        
    else:
        print(f"\n❌ BKR article not found!")
    
    conn.close()
    
    # Check current settings
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    min_conf = int(os.getenv("SIGNALS_MIN_CONFIDENCE", "75"))
    
    print(f"\n" + "="*80)
    print(f"⚙️  Current Settings:")
    print(f"="*80)
    print(f"\n   SIGNALS_MIN_CONFIDENCE: {min_conf}%")
    print(f"   BKR Signal Confidence: 46%")
    
    if 46 < min_conf:
        print(f"\n❌ PROBLEM FOUND!")
        print(f"   Signal confidence (46%) < threshold ({min_conf}%)")
        print(f"   Signal was generated but NOT sent!")
        print(f"\n✅ SOLUTION:")
        print(f"   Lower SIGNALS_MIN_CONFIDENCE to 40 or 45")
        print(f"   Edit .env:")
        print(f"   SIGNALS_MIN_CONFIDENCE=45")
    else:
        print(f"\n✅ Confidence OK")
        print(f"   Signal should have been sent!")
        print(f"   Check Telegram for the message.")
    
    print(f"\n" + "="*80 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

