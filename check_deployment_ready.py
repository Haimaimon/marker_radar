#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
בדיקת מוכנות לפריסה
===================
בודק שהכל מוכן להעלאה לענן
"""

import sys
import os
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_file(filename, required=True):
    """Check if file exists."""
    exists = Path(filename).exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "חובה" if required else "אופציונלי"
    print(f"{status} {filename:30} ({req_text})")
    return exists

def check_env_var(var_name, required=True):
    """Check if environment variable is set."""
    value = os.getenv(var_name)
    exists = bool(value)
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "חובה" if required else "אופציונלי"
    
    if exists:
        # Show partial value for security
        if len(value) > 10:
            display = value[:10] + "..."
        else:
            display = value
        print(f"{status} {var_name:25} = {display:20} ({req_text})")
    else:
        print(f"{status} {var_name:25} = <לא מוגדר>          ({req_text})")
    
    return exists

def main():
    print("\n" + "="*80)
    print("🔍 בדיקת מוכנות לפריסה - Market Radar")
    print("="*80 + "\n")
    
    all_good = True
    
    # Check files
    print("📁 קבצים נדרשים:")
    print("-" * 80)
    
    required_files = [
        ("requirements.txt", True),
        ("app.py", True),
        ("config.py", True),
        ("Dockerfile", True),
        (".dockerignore", True),
        ("render.yaml", False),
        ("railway.json", False),
        ("fly.toml", False),
        (".gitignore", True),
    ]
    
    for filename, required in required_files:
        if not check_file(filename, required) and required:
            all_good = False
    
    # Check .env (should NOT be committed)
    print("\n🔐 אבטחה:")
    print("-" * 80)
    
    if Path(".env").exists():
        print("⚠️  .env קיים - ודא שהוא ב-.gitignore!")
        
        # Check if .env is in .gitignore
        if Path(".gitignore").exists():
            gitignore_content = Path(".gitignore").read_text()
            if ".env" in gitignore_content:
                print("✅ .env מופיע ב-.gitignore - טוב!")
            else:
                print("❌ .env לא מופיע ב-.gitignore - סכנה!")
                all_good = False
    else:
        print("✅ .env לא קיים - טוב (נשתמש ב-Environment Variables)")
    
    # Load .env if exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    # Check environment variables
    print("\n🔧 Environment Variables (חובה לפריסה):")
    print("-" * 80)
    
    required_vars = [
        ("TELEGRAM_BOT_TOKEN", True),
        ("TELEGRAM_CHAT_ID", True),
        ("ENABLE_TELEGRAM", True),
    ]
    
    for var_name, required in required_vars:
        if not check_env_var(var_name, required) and required:
            all_good = False
    
    print("\n🔧 Environment Variables (מומלץ):")
    print("-" * 80)
    
    optional_vars = [
        ("FINNHUB_API_KEY", False),
        ("ENABLE_FINNHUB", False),
        ("MIN_GAP_PCT", False),
        ("MIN_VOL_SPIKE", False),
        ("ENABLE_TICKER_FILTER", False),
        ("VERBOSE_LOGGING", False),
    ]
    
    for var_name, required in optional_vars:
        check_env_var(var_name, required)
    
    # Check Python version
    print("\n🐍 Python:")
    print("-" * 80)
    
    py_version = sys.version_info
    print(f"✅ גרסה: {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
        print("⚠️  מומלץ Python 3.8 ומעלה")
        all_good = False
    
    # Check dependencies
    print("\n📦 Dependencies:")
    print("-" * 80)
    
    try:
        import feedparser
        print("✅ feedparser מותקן")
    except ImportError:
        print("❌ feedparser לא מותקן")
        all_good = False
    
    try:
        import requests
        print("✅ requests מותקן")
    except ImportError:
        print("❌ requests לא מותקן")
        all_good = False
    
    try:
        import dotenv
        print("✅ python-dotenv מותקן")
    except ImportError:
        print("⚠️  python-dotenv לא מותקן (אופציונלי)")
    
    try:
        import pydantic
        print("✅ pydantic מותקן")
    except ImportError:
        print("❌ pydantic לא מותקן")
        all_good = False
    
    # Check Git
    print("\n🔀 Git:")
    print("-" * 80)
    
    if Path(".git").exists():
        print("✅ Git repository מאותחל")
        
        # Check if there are uncommitted changes
        import subprocess
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout.strip():
                print("⚠️  יש שינויים שלא בcommit:")
                lines = result.stdout.strip().split("\n")
                for line in lines[:5]:
                    print(f"     {line}")
                if len(lines) > 5:
                    remaining = len(lines) - 5
                    print(f"     ... ועוד {remaining} קבצים")
            else:
                print("✅ אין שינויים שלא בcommit")
        except:
            print("⚠️  לא הצלחתי לבדוק git status")
    else:
        print("⚠️  Git repository לא מאותחל")
        print("   הרץ: git init")
    
    # Summary
    print("\n" + "="*80)
    if all_good:
        print("🎉 הכל מוכן לפריסה!")
        print("="*80)
        print("\n📝 צעדים הבאים:")
        print("   1. git add .")
        print("   2. git commit -m 'Ready for deployment'")
        print("   3. git push")
        print("   4. צור Background Worker ב-Render.com")
        print("   5. הוסף Environment Variables")
        print("   6. Deploy!")
        print("\n📚 קרא: DEPLOY_QUICK_START.md")
    else:
        print("⚠️  יש בעיות שצריך לתקן לפני פריסה")
        print("="*80)
        print("\n📝 תקן את הבעיות המסומנות ב-❌ למעלה")
    
    print("\n" + "="*80 + "\n")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())

