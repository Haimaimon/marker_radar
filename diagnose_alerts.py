#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Diagnostic - Why Am I Not Getting Alerts?
================================================
Analyzes your current database to show why articles aren't being notified.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import sqlite3
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()

# Get current settings
MIN_IMPACT_SCORE = int(os.getenv("MIN_IMPACT_SCORE", "70"))
MIN_GAP_PCT = float(os.getenv("MIN_GAP_PCT", "4.0"))
MIN_VOL_SPIKE = float(os.getenv("MIN_VOL_SPIKE", "1.8"))
ENABLE_MARKET_VALIDATION = os.getenv("ENABLE_MARKET_VALIDATION", "true").lower() in ("true", "1", "yes")

print("\n" + "="*80)
print("🔍 DIAGNOSTIC: Why Am I Not Getting Alerts?")
print("="*80)

# Connect to DB
try:
    conn = sqlite3.connect("market_radar.db")  # Changed from news.db
    cursor = conn.cursor()
    
    # Get recent articles
    cursor.execute("""
        SELECT 
            title, 
            ticker, 
            impact_score, 
            impact_reason,
            validated,
            validation_reason
        FROM events 
        WHERE date(created_at) = date('now', 'localtime')
        ORDER BY created_at DESC
        LIMIT 50
    """)
    
    articles = cursor.fetchall()
    
    if not articles:
        print("\n❌ No articles found in database today!")
        print("   This might be why you're not getting alerts.")
        print("\n🔧 Possible solutions:")
        print("   1. Check that news sources are working")
        print("   2. Wait a few minutes for news to arrive")
        print("   3. Check internet connection")
        sys.exit(0)
    
    print(f"\n📊 Found {len(articles)} articles from today")
    print(f"\n⚙️  Your Current Settings:")
    print(f"   MIN_IMPACT_SCORE: {MIN_IMPACT_SCORE}")
    print(f"   MIN_GAP_PCT: {MIN_GAP_PCT}%")
    print(f"   MIN_VOL_SPIKE: {MIN_VOL_SPIKE}x")
    print(f"   ENABLE_MARKET_VALIDATION: {ENABLE_MARKET_VALIDATION}")
    
    # Analyze
    scores = []
    validated_count = 0
    not_validated_count = 0
    low_score_count = 0
    
    failure_reasons = Counter()
    
    for title, ticker, score, impact_reason, validated, validation_reason in articles:
        if score is not None:
            scores.append(score)
        
        # Check why not notified
        if score and score < MIN_IMPACT_SCORE:
            low_score_count += 1
            failure_reasons[f"Low score ({score} < {MIN_IMPACT_SCORE})"] += 1
        elif validated == 1:
            validated_count += 1
        elif validated == 0:
            not_validated_count += 1
            if validation_reason:
                failure_reasons[f"Validation: {validation_reason[:50]}"] += 1
    
    print(f"\n📈 Score Distribution:")
    if scores:
        print(f"   Highest: {max(scores)}")
        print(f"   Average: {sum(scores)/len(scores):.1f}")
        print(f"   Lowest: {min(scores)}")
        print(f"   Threshold: {MIN_IMPACT_SCORE} ⚠️")
        
        above_threshold = sum(1 for s in scores if s >= MIN_IMPACT_SCORE)
        print(f"\n   Articles above threshold: {above_threshold}/{len(scores)} ({above_threshold/len(scores)*100:.0f}%)")
    
    print(f"\n🎯 Results:")
    print(f"   ✅ Validated (notified): {validated_count}")
    print(f"   ❌ Not Validated: {not_validated_count}")
    print(f"   📉 Low Score: {low_score_count}")
    
    if failure_reasons:
        print(f"\n🚫 Top Failure Reasons:")
        for reason, count in failure_reasons.most_common(5):
            print(f"   {count:3d}× {reason}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    if low_score_count > validated_count * 3:
        print(f"\n   🔴 PROBLEM: Too many articles have low scores!")
        print(f"      Current threshold: {MIN_IMPACT_SCORE}")
        print(f"      Average score: {sum(scores)/len(scores):.0f}")
        print(f"\n   ✅ SOLUTION: Lower MIN_IMPACT_SCORE")
        print(f"      Try: MIN_IMPACT_SCORE=50")
    
    if not_validated_count > validated_count * 3 and ENABLE_MARKET_VALIDATION:
        print(f"\n   🔴 PROBLEM: Market validation too strict!")
        print(f"      Current: GAP={MIN_GAP_PCT}%, VOL={MIN_VOL_SPIKE}x")
        print(f"\n   ✅ SOLUTION: Lower validation thresholds")
        print(f"      Try: MIN_GAP_PCT=2.0, MIN_VOL_SPIKE=1.3")
        print(f"      Or: ENABLE_MARKET_VALIDATION=false")
    
    if validated_count == 0:
        print(f"\n   🔴 CRITICAL: ZERO articles passing filters!")
        print(f"\n   ✅ QUICK FIX: Use these settings:")
        print(f"      MIN_IMPACT_SCORE=50")
        print(f"      MIN_GAP_PCT=2.0")
        print(f"      MIN_VOL_SPIKE=1.3")
    
    # Show some examples
    if low_score_count > 0:
        print(f"\n📋 Sample Articles (Low Score):")
        cursor.execute("""
            SELECT title, ticker, impact_score, impact_reason
            FROM events 
            WHERE date(created_at) = date('now', 'localtime')
              AND impact_score < ?
            ORDER BY impact_score DESC
            LIMIT 3
        """, (MIN_IMPACT_SCORE,))
        
        for idx, (title, ticker, score, reason) in enumerate(cursor.fetchall(), 1):
            print(f"\n   {idx}. Score: {score}/{MIN_IMPACT_SCORE}")
            print(f"      {title[:60]}...")
            if reason:
                print(f"      Reason: {reason[:60]}")
    
    if not_validated_count > 0:
        print(f"\n📋 Sample Articles (Not Validated):")
        cursor.execute("""
            SELECT title, ticker, impact_score, validation_reason
            FROM events 
            WHERE date(created_at) = date('now', 'localtime')
              AND validated = 0
              AND impact_score >= ?
            ORDER BY impact_score DESC
            LIMIT 3
        """, (MIN_IMPACT_SCORE,))
        
        for idx, (title, ticker, score, reason) in enumerate(cursor.fetchall(), 1):
            print(f"\n   {idx}. Score: {score} (passed!)")
            print(f"      {title[:60]}...")
            if reason:
                print(f"      Failed: {reason[:60]}")
    
    conn.close()
    
    print("\n" + "="*80)
    print("💡 Next Steps:")
    print("   1. Update .env with recommended settings")
    print("   2. Restart: python app.py")
    print("   3. Wait 5-10 minutes")
    print("   4. Check Telegram!")
    print("="*80 + "\n")

except sqlite3.Error as e:
    print(f"\n❌ Database error: {e}")
    print("   Make sure market_radar.db exists and app.py has run at least once.")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

