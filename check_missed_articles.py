#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
סקריפט לבדיקת כתבות עם ציון גבוה שלא עברו אימות
"""
import sqlite3
import sys
from datetime import datetime, timedelta

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_missed_articles(db_path="market_radar.db", days=1, min_score=70):
    """
    בודק כתבות עם ציון גבוה שלא עברו אימות
    
    Args:
        db_path: נתיב ל-DB
        days: כמה ימים אחורה לבדוק
        min_score: ציון מינימלי
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # שאילתה לכתבות עם ציון גבוה שלא עברו אימות
    query = """
    SELECT 
        title,
        ticker,
        impact_score,
        impact_reason,
        validated,
        validation_reason,
        gap_pct,
        vol_spike,
        created_at,
        link
    FROM events
    WHERE impact_score >= ?
    AND created_at >= datetime('now', '-' || ? || ' days')
    ORDER BY impact_score DESC, created_at DESC
    """
    
    cursor.execute(query, (min_score, days))
    results = cursor.fetchall()
    
    print(f"\n{'='*100}")
    print(f"📊 סיכום כתבות עם ציון גבוה (Score >= {min_score}) - {days} ימים אחרונים")
    print(f"{'='*100}\n")
    
    validated = []
    not_validated = []
    
    for row in results:
        title, ticker, score, reason, validated_flag, val_reason, gap, vol, created, link = row
        
        item = {
            'title': title,
            'ticker': ticker or 'N/A',
            'score': score,
            'reason': reason,
            'validated': validated_flag,
            'val_reason': val_reason,
            'gap': gap,
            'vol': vol,
            'created': created,
            'link': link
        }
        
        if validated_flag:
            validated.append(item)
        else:
            not_validated.append(item)
    
    # מציג כתבות שלא עברו אימות
    print(f"⚠️  כתבות עם ציון גבוה שלא עברו אימות: {len(not_validated)}")
    print(f"{'='*100}\n")
    
    for i, item in enumerate(not_validated, 1):
        print(f"{i}. [{item['score']}] {item['ticker']} - {item['title'][:70]}")
        print(f"   💡 סיבת הציון: {item['reason']}")
        print(f"   ❌ לא עבר אימות: {item['val_reason']}")
        if item['gap'] is not None:
            print(f"   📊 Gap: {item['gap']:.2f}%")
        if item['vol'] is not None:
            print(f"   📊 Volume Spike: {item['vol']:.2f}x")
        print(f"   🕒 {item['created']}")
        print(f"   🔗 {item['link']}")
        print()
    
    print(f"\n{'='*100}")
    print(f"✅ כתבות שעברו אימות והתריעו: {len(validated)}")
    print(f"{'='*100}\n")
    
    for i, item in enumerate(validated[:5], 1):  # מציג רק 5 הראשונות
        print(f"{i}. [{item['score']}] {item['ticker']} - {item['title'][:70]}")
        print(f"   ✅ {item['val_reason']}")
        if item['gap'] is not None:
            print(f"   📈 Gap: {item['gap']:.2f}%")
        if item['vol'] is not None:
            print(f"   📊 Volume Spike: {item['vol']:.2f}x")
        print()
    
    if len(validated) > 5:
        print(f"   ... ועוד {len(validated) - 5} כתבות\n")
    
    # סטטיסטיקה
    print(f"\n{'='*100}")
    print(f"📈 סטטיסטיקה")
    print(f"{'='*100}")
    print(f"סה\"כ כתבות עם ציון גבוה: {len(results)}")
    print(f"עברו אימות: {len(validated)} ({len(validated)/len(results)*100:.1f}%)")
    print(f"לא עברו אימות: {len(not_validated)} ({len(not_validated)/len(results)*100:.1f}%)")
    
    # ניתוח סיבות לאי-אימות
    if not_validated:
        print(f"\n📊 סיבות לאי-אימות:")
        reasons = {}
        for item in not_validated:
            reason = item['val_reason'].split(':')[0] if ':' in item['val_reason'] else item['val_reason']
            reasons[reason] = reasons.get(reason, 0) + 1
        
        for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {reason}: {count}")
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    # ברירת מחדל: בודק יום אחד אחורה
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    min_score = int(sys.argv[2]) if len(sys.argv) > 2 else 70
    
    try:
        check_missed_articles(days=days, min_score=min_score)
    except sqlite3.OperationalError as e:
        print(f"❌ שגיאה: לא ניתן לפתוח את ה-DB. האם המערכת רצה לפחות פעם אחת?")
        print(f"   {e}")

