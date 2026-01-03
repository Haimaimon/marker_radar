#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze Ticker Distribution
============================
Show how many articles have tickers and can generate signals.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import sqlite3

print("\n" + "="*80)
print("📊 TICKER ANALYSIS - Why Some Articles Don't Get Signals")
print("="*80)

try:
    conn = sqlite3.connect("market_radar.db")
    cursor = conn.cursor()
    
    # Get today's stats
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN ticker IS NOT NULL AND ticker != '' THEN 1 ELSE 0 END) as with_ticker,
            SUM(CASE WHEN impact_score >= 35 THEN 1 ELSE 0 END) as high_score,
            SUM(CASE WHEN ticker IS NOT NULL AND ticker != '' AND impact_score >= 35 THEN 1 ELSE 0 END) as signal_candidates
        FROM events 
        WHERE date(created_at) = date('now', 'localtime')
    """)
    
    total, with_ticker, high_score, signal_candidates = cursor.fetchone()
    without_ticker = total - with_ticker
    
    print(f"\n📈 Today's Articles:")
    print(f"   Total: {total}")
    print(f"   With Ticker: {with_ticker} ({with_ticker/total*100:.0f}%)")
    print(f"   Without Ticker: {without_ticker} ({without_ticker/total*100:.0f}%)")
    print(f"   High Score (≥35): {high_score}")
    print(f"   Signal Candidates: {signal_candidates} ⚡")
    
    print(f"\n💡 Signal Potential:")
    print(f"   Articles that CAN get signals: {signal_candidates}")
    print(f"   Articles that CAN'T (no ticker): {high_score - signal_candidates}")
    
    # Show top articles without tickers
    print(f"\n❌ Top High-Score Articles WITHOUT Tickers:")
    print("="*80)
    
    cursor.execute("""
        SELECT title, impact_score, impact_reason
        FROM events 
        WHERE date(created_at) = date('now', 'localtime')
          AND (ticker IS NULL OR ticker = '')
          AND impact_score >= 80
        ORDER BY impact_score DESC
        LIMIT 5
    """)
    
    for idx, (title, score, reason) in enumerate(cursor.fetchall(), 1):
        print(f"\n{idx}. Score: {score}")
        print(f"   {title[:70]}...")
        if reason:
            print(f"   Why: {reason[:60]}")
    
    # Show top articles WITH tickers
    print(f"\n\n✅ Top High-Score Articles WITH Tickers:")
    print("="*80)
    
    cursor.execute("""
        SELECT title, ticker, impact_score
        FROM events 
        WHERE date(created_at) = date('now', 'localtime')
          AND ticker IS NOT NULL 
          AND ticker != ''
          AND impact_score >= 35
        ORDER BY impact_score DESC
        LIMIT 5
    """)
    
    results = cursor.fetchall()
    
    if results:
        for idx, (title, ticker, score) in enumerate(results, 1):
            print(f"\n{idx}. [{score}] {ticker}")
            print(f"   {title[:70]}...")
            print(f"   → Can generate trading signal! ✅")
    else:
        print("\n⚠️  No articles with tickers found!")
        print("   This is why you're not getting trading signals.")
    
    conn.close()
    
    print("\n" + "="*80)
    print("💡 Summary:")
    print("="*80)
    
    if signal_candidates == 0:
        print("\n❌ PROBLEM: 0 signal candidates!")
        print("   Reasons:")
        print("   1. Articles don't have tickers extracted")
        print("   2. Ticker extraction might be failing")
        print("\n✅ SOLUTIONS:")
        print("   1. Check ticker extraction in scoring.py")
        print("   2. Lower MIN_IMPACT_SCORE more (currently 35)")
        print("   3. Wait for articles about public companies")
    elif signal_candidates < 5:
        print(f"\n⚠️  LOW: Only {signal_candidates} signal candidates")
        print("   Most high-score articles don't have tickers")
        print("\n💡 TIP: Signals work best during market hours")
        print("   (Mon-Fri 9:30-16:00 EST)")
    else:
        print(f"\n✅ GOOD: {signal_candidates} signal candidates!")
        print("   These articles can generate trading signals")
    
    print("\n" + "="*80 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

