#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
מייצא כתבות עם ציון גבוה ל-CSV/HTML לסקירה ידנית
"""
import sqlite3
import csv
import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def export_to_csv(db_path="market_radar.db", output="high_score_articles.csv", days=1, min_score=70):
    """
    מייצא כתבות עם ציון גבוה ל-CSV
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        created_at,
        ticker,
        impact_score,
        impact_reason,
        validated,
        validation_reason,
        gap_pct,
        vol_spike,
        source,
        title,
        link
    FROM events
    WHERE impact_score >= ?
    AND created_at >= datetime('now', '-' || ? || ' days')
    ORDER BY impact_score DESC, created_at DESC
    """
    
    cursor.execute(query, (min_score, days))
    results = cursor.fetchall()
    
    # כתיבה ל-CSV
    with open(output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'תאריך',
            'טיקר',
            'ציון',
            'סיבת ציון',
            'עבר אימות?',
            'סיבת אימות',
            'Gap %',
            'Vol Spike',
            'מקור',
            'כותרת',
            'קישור'
        ])
        
        for row in results:
            created, ticker, score, reason, validated, val_reason, gap, vol, source, title, link = row
            writer.writerow([
                created,
                ticker or 'N/A',
                score,
                reason,
                'כן' if validated else 'לא',
                val_reason,
                f"{gap:.2f}" if gap else '',
                f"{vol:.2f}" if vol else '',
                source,
                title,
                link
            ])
    
    conn.close()
    
    print(f"✅ {len(results)} כתבות יוצאו ל-{output}")
    print(f"   ניתן לפתוח ב-Excel או Google Sheets")
    
    return len(results)

def export_to_html(db_path="market_radar.db", output="high_score_articles.html", days=1, min_score=70):
    """
    מייצא כתבות עם ציון גבוה ל-HTML מעוצב
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        created_at,
        ticker,
        impact_score,
        impact_reason,
        validated,
        validation_reason,
        gap_pct,
        vol_spike,
        source,
        title,
        link
    FROM events
    WHERE impact_score >= ?
    AND created_at >= datetime('now', '-' || ? || ' days')
    ORDER BY impact_score DESC, created_at DESC
    """
    
    cursor.execute(query, (min_score, days))
    results = cursor.fetchall()
    
    # HTML template - using double braces {{}} to escape CSS braces
    html = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>כתבות עם ציון גבוה - Market Radar</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            direction: rtl;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .stats {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .article {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 5px solid #2196F3;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .article.validated {{
            border-left-color: #4CAF50;
        }}
        .article.not-validated {{
            border-left-color: #FF9800;
        }}
        .score {{
            display: inline-block;
            background: #2196F3;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin-left: 10px;
        }}
        .ticker {{
            display: inline-block;
            background: #673AB7;
            color: white;
            padding: 5px 15px;
            border-radius: 4px;
            font-weight: bold;
            margin-left: 10px;
        }}
        .validated-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 10px;
        }}
        .validated-badge.yes {{
            background: #4CAF50;
            color: white;
        }}
        .validated-badge.no {{
            background: #FF9800;
            color: white;
        }}
        .title {{
            font-size: 18px;
            font-weight: bold;
            margin: 15px 0;
            color: #333;
        }}
        .meta {{
            color: #666;
            font-size: 14px;
            margin: 10px 0;
        }}
        .link {{
            display: inline-block;
            background: #2196F3;
            color: white;
            padding: 8px 20px;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 10px;
        }}
        .link:hover {{
            background: #1976D2;
        }}
        .market-data {{
            background: #f9f9f9;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 כתבות עם ציון גבוה - Market Radar</h1>
        
        <div class="stats">
            <h2>📈 סטטיסטיקה</h2>
            <p><strong>סה"כ כתבות:</strong> {total}</p>
            <p><strong>תקופה:</strong> {days} ימים אחרונים</p>
            <p><strong>ציון מינימלי:</strong> {min_score}</p>
            <p><strong>תאריך יצירה:</strong> {date}</p>
        </div>
        
        <h2>🗞️ כתבות</h2>
"""
    
    for row in results:
        created, ticker, score, reason, validated, val_reason, gap, vol, source, title, link = row
        
        validated_class = "validated" if validated else "not-validated"
        validated_badge_class = "yes" if validated else "no"
        validated_text = "✅ עבר אימות" if validated else "⚠️ לא עבר אימות"
        
        gap_text = f"{gap:.2f}%" if gap else "N/A"
        vol_text = f"{vol:.2f}x" if vol else "N/A"
        
        html += f"""
        <div class="article {validated_class}">
            <div>
                <span class="score">{score}</span>
                <span class="ticker">{ticker or 'N/A'}</span>
                <span class="validated-badge {validated_badge_class}">{validated_text}</span>
            </div>
            
            <div class="title">{title}</div>
            
            <div class="meta">
                <strong>📰 מקור:</strong> {source}<br>
                <strong>🕒 תאריך:</strong> {created}<br>
                <strong>💡 סיבת ציון:</strong> {reason}
            </div>
            
            <div class="market-data">
                <strong>📊 נתוני שוק:</strong><br>
                Gap: {gap_text} | Volume Spike: {vol_text}<br>
                <strong>סיבת אימות:</strong> {val_reason}
            </div>
            
            <a href="{link}" class="link" target="_blank">🔗 קרא את הכתבה המלאה</a>
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    # החלפת ערכים
    html = html.format(
        total=len(results),
        days=days,
        min_score=min_score,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    conn.close()
    
    print(f"✅ {len(results)} כתבות יוצאו ל-{output}")
    print(f"   ניתן לפתוח בדפדפן")
    
    return len(results)

if __name__ == "__main__":
    import sys
    
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    min_score = int(sys.argv[2]) if len(sys.argv) > 2 else 70
    
    try:
        print("\n" + "="*100)
        print("📤 מייצא כתבות...")
        print("="*100 + "\n")
        
        csv_count = export_to_csv(days=days, min_score=min_score)
        html_count = export_to_html(days=days, min_score=min_score)
        
        print("\n" + "="*100)
        print("✅ הייצוא הושלם בהצלחה!")
        print("="*100)
        
    except sqlite3.OperationalError as e:
        print(f"❌ שגיאה: {e}")

