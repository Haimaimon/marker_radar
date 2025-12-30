#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בדיקת סטטוס Finnhub
"""
import sys
import os
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

print("\n" + "="*80)
print("🔍 בדיקת סטטוס Finnhub API")
print("="*80 + "\n")

# Check configuration
enable_finnhub = os.getenv("ENABLE_FINNHUB", "false").lower() in ("true", "1", "yes")
finnhub_key = os.getenv("FINNHUB_API_KEY", "")

print(f"📋 הגדרות ב-.env:")
print(f"   ENABLE_FINNHUB: {enable_finnhub}")
print(f"   FINNHUB_API_KEY: {'✅ מוגדר (' + finnhub_key[:10] + '...)' if finnhub_key else '❌ לא מוגדר'}")

if not enable_finnhub:
    print("\n⚠️  Finnhub מבוטל!")
    print("\n📝 כדי להפעיל:")
    print("   1. ערוך את .env")
    print("   2. שנה: ENABLE_FINNHUB=true")
    print("   3. אם אין לך API key, קבל אחד חינם מ: https://finnhub.io/register")
    print("   4. הוסף לקובץ: FINNHUB_API_KEY=your_key_here")
    sys.exit(0)

if not finnhub_key:
    print("\n❌ Finnhub מופעל אבל אין API key!")
    print("\n📝 כדי להוסיף key:")
    print("   1. הרשם ב: https://finnhub.io/register")
    print("   2. העתק את ה-API key")
    print("   3. ערוך .env והוסף: FINNHUB_API_KEY=your_key_here")
    sys.exit(1)

print("\n✅ Finnhub מוגדר נכון!")
print("\n🔬 בודק חיבור...")

try:
    from market_data.finnhub_provider import FinnhubProvider
    
    finnhub = FinnhubProvider(finnhub_key)
    
    # Test with a simple ticker
    print("\n📊 בודק עם AAPL...")
    snapshot = finnhub.get_snapshot("AAPL")
    
    if snapshot.price:
        print(f"\n🎉 החיבור עובד!")
        print(f"\n📈 נתונים:")
        print(f"   מחיר נוכחי: ${snapshot.price:.2f}")
        if snapshot.prev_close:
            print(f"   סגירה קודמת: ${snapshot.prev_close:.2f}")
            gap = ((snapshot.price - snapshot.prev_close) / snapshot.prev_close) * 100
            print(f"   שינוי: {gap:+.2f}%")
        if snapshot.volume:
            print(f"   נפח: {snapshot.volume:,}")
        if snapshot.avg_volume_10d:
            print(f"   נפח ממוצע: {snapshot.avg_volume_10d:,}")
        
        print(f"\n✅ Finnhub API עובד מצוין!")
        print(f"\n💡 יתרונות:")
        print(f"   • 60 בקשות לדקה (חינם)")
        print(f"   • נתונים מהימנים")
        print(f"   • שימוש במערכת כבר מוגדר")
    else:
        print(f"\n⚠️  החיבור הצליח אבל אין מחיר עבור AAPL")
        print(f"   זה יכול להיות תקין אם השוק סגור")
        
except Exception as e:
    print(f"\n❌ שגיאה בחיבור: {e}")
    print(f"\n🔧 פתרונות אפשריים:")
    print(f"   1. בדוק שה-API key נכון")
    print(f"   2. בדוק חיבור לאינטרנט")
    print(f"   3. נסה key חדש מ: https://finnhub.io/dashboard")
    sys.exit(1)

print("\n" + "="*80)
print("✅ הכל תקין! המערכת משתמשת ב-Finnhub")
print("="*80 + "\n")

