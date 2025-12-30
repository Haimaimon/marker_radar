#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
סקריפט לניתוח הגדרות האימות ומציאת ערכים אופטימליים
"""
import sqlite3
import sys
from datetime import datetime, timedelta

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def analyze_validation_settings(db_path="market_radar.db", days=7):
    """
    מנתח את התפלגות ה-gap% ו-volume spike כדי לעזור להחליט על סף אימות
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        ticker,
        impact_score,
        gap_pct,
        vol_spike,
        validated,
        title,
        created_at
    FROM events
    WHERE impact_score >= 70
    AND created_at >= datetime('now', '-' || ? || ' days')
    AND gap_pct IS NOT NULL
    ORDER BY impact_score DESC
    """
    
    cursor.execute(query, (days,))
    results = cursor.fetchall()
    
    if not results:
        print(f"❌ אין נתונים מ-{days} ימים אחרונים")
        conn.close()
        return
    
    print(f"\n{'='*100}")
    print(f"📊 ניתוח הגדרות אימות - {days} ימים אחרונים")
    print(f"{'='*100}\n")
    
    # איסוף נתונים
    gaps = []
    vol_spikes = []
    
    for row in results:
        ticker, score, gap, vol, validated, title, created = row
        if gap is not None:
            gaps.append(abs(gap))
        if vol is not None:
            vol_spikes.append(vol)
    
    # ניתוח Gap%
    print("📈 Gap% Analysis")
    print("-" * 100)
    if gaps:
        gaps_sorted = sorted(gaps)
        print(f"Min: {min(gaps):.2f}%")
        print(f"Max: {max(gaps):.2f}%")
        print(f"Average: {sum(gaps)/len(gaps):.2f}%")
        print(f"Median: {gaps_sorted[len(gaps_sorted)//2]:.2f}%")
        
        # אחוזונים
        percentiles = [10, 25, 50, 75, 90]
        print("\nPercentiles:")
        for p in percentiles:
            idx = int(len(gaps_sorted) * p / 100)
            print(f"  {p}th: {gaps_sorted[idx]:.2f}%")
        
        # סימולציה של סטינגים שונים
        print("\n🔬 Simulation - כמה כתבות היו עוברות עם סטינגים שונים:")
        test_gaps = [1.0, 2.0, 3.0, 4.0, 5.0]
        for test_gap in test_gaps:
            passed = sum(1 for g in gaps if g >= test_gap)
            pct = passed / len(gaps) * 100
            print(f"  MIN_GAP_PCT={test_gap:.1f}% → {passed}/{len(gaps)} כתבות ({pct:.1f}%)")
    else:
        print("אין מספיק נתונים")
    
    # ניתוח Volume Spike
    print(f"\n📊 Volume Spike Analysis")
    print("-" * 100)
    if vol_spikes:
        vol_sorted = sorted(vol_spikes)
        print(f"Min: {min(vol_spikes):.2f}x")
        print(f"Max: {max(vol_spikes):.2f}x")
        print(f"Average: {sum(vol_spikes)/len(vol_spikes):.2f}x")
        print(f"Median: {vol_sorted[len(vol_sorted)//2]:.2f}x")
        
        # אחוזונים
        print("\nPercentiles:")
        for p in percentiles:
            idx = int(len(vol_sorted) * p / 100)
            print(f"  {p}th: {vol_sorted[idx]:.2f}x")
        
        # סימולציה
        print("\n🔬 Simulation - כמה כתבות היו עוברות עם סטינגים שונים:")
        test_vols = [1.0, 1.3, 1.5, 1.8, 2.0]
        for test_vol in test_vols:
            passed = sum(1 for v in vol_spikes if v >= test_vol)
            pct = passed / len(vol_spikes) * 100
            print(f"  MIN_VOL_SPIKE={test_vol:.1f}x → {passed}/{len(vol_spikes)} כתבות ({pct:.1f}%)")
    else:
        print("אין מספיק נתונים")
    
    # המלצות
    print(f"\n{'='*100}")
    print("💡 המלצות")
    print(f"{'='*100}")
    
    current_gap = 4.0
    current_vol = 1.8
    
    print(f"\nהגדרות נוכחיות:")
    print(f"  MIN_GAP_PCT={current_gap}%")
    print(f"  MIN_VOL_SPIKE={current_vol}x")
    
    if gaps:
        passed_gap = sum(1 for g in gaps if g >= current_gap)
        print(f"  → {passed_gap}/{len(gaps)} כתבות עוברות את סף ה-Gap")
    
    if vol_spikes:
        passed_vol = sum(1 for v in vol_spikes if v >= current_vol)
        print(f"  → {passed_vol}/{len(vol_spikes)} כתבות עוברות את סף ה-Volume")
    
    print("\n📝 אפשרויות:")
    print("  1. להוריד את הסף (יותר התראות, יותר רעש)")
    print("     MIN_GAP_PCT=2.0")
    print("     MIN_VOL_SPIKE=1.3")
    print()
    print("  2. להשאיר כמו שזה (מאוזן)")
    print("     MIN_GAP_PCT=4.0")
    print("     MIN_VOL_SPIKE=1.8")
    print()
    print("  3. להעלות את הסף (פחות התראות, יותר מדויק)")
    print("     MIN_GAP_PCT=5.0")
    print("     MIN_VOL_SPIKE=2.0")
    print()
    print("  4. לבטל אימות לגמרי (כל כתבה עם ציון גבוה תתריע)")
    print("     ENABLE_MARKET_VALIDATION=false")
    
    conn.close()

if __name__ == "__main__":
    import sys
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    
    try:
        analyze_validation_settings(days=days)
    except sqlite3.OperationalError as e:
        print(f"❌ שגיאה: {e}")

