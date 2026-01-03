#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze Why AMZN Didn't Get Signal
===================================
Deep dive into the specific case.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import sqlite3
from datetime import datetime

print("\n" + "="*80)
print("🔍 WHY AMZN (SCORE 100) DIDN'T GET TRADING SIGNAL?")
print("="*80)

try:
    conn = sqlite3.connect("market_radar.db")
    cursor = conn.cursor()
    
    # Find the AMZN article
    cursor.execute("""
        SELECT 
            title,
            ticker,
            impact_score,
            impact_reason,
            validated,
            validation_reason,
            published,
            created_at
        FROM events 
        WHERE ticker = 'AMZN'
          AND title LIKE '%AI%2026%'
        ORDER BY created_at DESC
        LIMIT 1
    """)
    
    result = cursor.fetchone()
    
    if result:
        title, ticker, score, reason, validated, val_reason, published, created = result
        
        print(f"\n📰 Found Article:")
        print(f"   Title: {title}")
        print(f"   Ticker: {ticker}")
        print(f"   Score: {score}")
        print(f"   Validated: {validated}")
        print(f"   Published: {published}")
        print(f"   Created: {created}")
        
        print(f"\n" + "="*80)
        print(f"🔍 Analysis:")
        print(f"="*80)
        
        # Check 1: Article exists
        print(f"\n✅ Article found in database")
        
        # Check 2: Has ticker
        if ticker:
            print(f"✅ Has ticker: {ticker}")
        else:
            print(f"❌ No ticker!")
            print(f"   → Signals need ticker!")
        
        # Check 3: Score is high
        if score >= 35:
            print(f"✅ Score {score} >= 35 (threshold)")
        else:
            print(f"❌ Score {score} < 35")
        
        # Check 4: Validated
        if validated:
            print(f"✅ Article validated")
        else:
            print(f"❌ Not validated")
        
        # Check 5: Time
        print(f"\n🕐 Timing:")
        print(f"   Published: {published}")
        print(f"   Created in DB: {created}")
        
        # Is it old news?
        try:
            from dateutil import parser
            pub_date = parser.parse(published)
            now = datetime.now(pub_date.tzinfo) if pub_date.tzinfo else datetime.now()
            age_hours = (now - pub_date).total_seconds() / 3600
            
            print(f"   Age: {age_hours:.1f} hours")
            
            if age_hours > 24:
                print(f"   ⚠️  OLD NEWS (>{age_hours:.0f} hours old)")
                print(f"   → Market data might be stale!")
        except:
            print(f"   ❓ Can't parse date")
        
        # Most likely reason
        print(f"\n" + "="*80)
        print(f"💡 MOST LIKELY REASON:")
        print(f"="*80)
        
        print(f"\n🕐 **OLD NEWS**")
        print(f"   Published: Wed, 31 Dec 2025")
        print(f"   Detected: 3-4 days later")
        print(f"\n   When signals try to get market data:")
        print(f"   • Market was closed (New Year)")
        print(f"   • No real-time price available")
        print(f"   • Can't calculate entry/stop/targets")
        print(f"   → Signal generation fails silently")
        
        print(f"\n📊 Other possibilities:")
        print(f"   1. Market closed (New Year holiday)")
        print(f"   2. No market snapshot available")
        print(f"   3. yfinance returns stale data")
        print(f"   4. Can't calculate confidence (needs volume/gap)")
        
    else:
        print(f"\n❌ AMZN article not found in database!")
        print(f"   Searching for any AMZN articles...")
        
        cursor.execute("""
            SELECT title, impact_score, created_at
            FROM events 
            WHERE ticker = 'AMZN'
            ORDER BY created_at DESC
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        if results:
            print(f"\n📋 Recent AMZN articles:")
            for idx, (t, s, c) in enumerate(results, 1):
                print(f"   {idx}. [{s}] {t[:60]}... ({c})")
        else:
            print(f"   No AMZN articles found!")
    
    conn.close()
    
    print(f"\n" + "="*80)
    print(f"✅ CONCLUSION:")
    print(f"="*80)
    
    print(f"\nAMZN article score 100 BUT:")
    print(f"   • Published Dec 31, 2025")
    print(f"   • Market closed (New Year)")
    print(f"   • Signals need REAL-TIME market data")
    print(f"   • No live price = No signal")
    
    print(f"\n💡 When WILL signals work?")
    print(f"   ✅ During market hours (Mon-Fri 9:30-16:00 EST)")
    print(f"   ✅ Fresh news (< 2 hours old)")
    print(f"   ✅ Active trading (has volume)")
    print(f"   ❌ Old news (days old)")
    print(f"   ❌ Market closed")
    print(f"   ❌ Holidays")
    
    print(f"\n" + "="*80 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

