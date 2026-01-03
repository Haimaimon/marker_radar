#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Show Filtered Articles - Why Were They Rejected?
=================================================
Shows exactly which articles were filtered and why.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import sqlite3
from collections import Counter

print("\n" + "="*80)
print("🔍 FILTERED ARTICLES ANALYSIS")
print("="*80)

try:
    conn = sqlite3.connect("market_radar.db")
    cursor = conn.cursor()
    
    # Get today's articles
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
        ORDER BY impact_score DESC
        LIMIT 100
    """)
    
    articles = cursor.fetchall()
    
    if not articles:
        print("\n❌ No articles found!")
        sys.exit(0)
    
    print(f"\n📊 Analyzing {len(articles)} articles from today...")
    
    # Group by score ranges
    score_ranges = {
        "45-50": [],
        "40-44": [],
        "35-39": [],
        "30-34": [],
        "25-29": [],
        "20-24": [],
        "<20": []
    }
    
    for article in articles:
        title, ticker, score, reason, validated, val_reason = article
        
        if score is None:
            score = 0
        
        if score >= 45:
            score_ranges["45-50"].append(article)
        elif score >= 40:
            score_ranges["40-44"].append(article)
        elif score >= 35:
            score_ranges["35-39"].append(article)
        elif score >= 30:
            score_ranges["30-34"].append(article)
        elif score >= 25:
            score_ranges["25-29"].append(article)
        elif score >= 20:
            score_ranges["20-24"].append(article)
        else:
            score_ranges["<20"].append(article)
    
    # Display
    print("\n" + "="*80)
    print("📊 SCORE DISTRIBUTION")
    print("="*80)
    
    total_high_value = 0
    
    for range_name, articles_in_range in score_ranges.items():
        count = len(articles_in_range)
        if count > 0:
            print(f"\n{range_name}: {count} articles")
            
            # Show first 3 from each range
            for idx, (title, ticker, score, reason, validated, val_reason) in enumerate(articles_in_range[:3], 1):
                print(f"  {idx}. [{score:2d}] {ticker or 'NO-TICKER'} - {title[:50]}...")
                if reason:
                    print(f"      Why: {reason[:60]}")
            
            if count > 3:
                print(f"      ... and {count-3} more")
            
            # Count articles above score 35
            if range_name in ["45-50", "40-44", "35-39"]:
                total_high_value += count
    
    print("\n" + "="*80)
    print("💡 RECOMMENDATIONS")
    print("="*80)
    
    if total_high_value > 0:
        print(f"\n✅ You have {total_high_value} articles with score ≥35")
        print(f"   With MIN_IMPACT_SCORE=35, you'll get {total_high_value} alerts!")
        print(f"\n   Update .env:")
        print(f"   MIN_IMPACT_SCORE=35")
    else:
        print(f"\n⚠️  No articles with score ≥35 found")
        print(f"   Highest score: {articles[0][2] if articles else 0}")
        print(f"\n   Try lowering even more:")
        print(f"   MIN_IMPACT_SCORE=25")
    
    # Check validation
    validated_count = sum(1 for a in articles if a[4] == 1)
    if validated_count == 0:
        print(f"\n⚠️  VALIDATION: 0 articles validated")
        print(f"   Good that ENABLE_MARKET_VALIDATION=false")
    
    conn.close()
    
    print("\n" + "="*80 + "\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

