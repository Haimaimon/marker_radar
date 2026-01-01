#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Stock Market Filter
=========================
Tests the stock market relevance filtering.
"""

import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from core.stock_filter import is_stock_market_related


def main():
    print("\n" + "="*80)
    print("🧪 Testing Stock Market Relevance Filter")
    print("="*80 + "\n")
    
    # Test cases
    test_cases = [
        # Should PASS (stock market related)
        ("Apple Announces Record Earnings",
         "AAPL shares surge 5% after company reports quarterly earnings beat",
         True),
        
        ("FDA Approves New Drug for Cancer Treatment",
         "Biotech company XYZ receives FDA approval, stock up 20%",
         True),
        
        ("Tesla Announces Stock Split",
         "TSLA to implement 3-for-1 stock split next month",
         True),
        
        ("Amazon Reports Q4 Results",
         "Amazon beats Wall Street expectations with strong revenue growth",
         True),
        
        ("Merger Deal: Company A to Acquire Company B",
         "NYSE-listed Company A announces $5B acquisition deal",
         True),
        
        ("SEC Files Complaint Against Company",
         "Securities and Exchange Commission takes action against publicly traded firm",
         True),
        
        ("Analyst Upgrades Stock to Buy",
         "Morgan Stanley raises price target on MSFT to $400",
         True),
        
        ("IPO: New Tech Company Goes Public",
         "Company XYZ files S-1 for initial public offering on NASDAQ",
         True),
        
        # Should FAIL (not stock market related)
        ("New Restaurant Opens Downtown",
         "Popular chef opens new dining establishment",
         False),
        
        ("Movie Review: Latest Hollywood Blockbuster",
         "Film receives positive reviews from critics",
         False),
        
        ("Sports: Team Wins Championship",
         "Local team celebrates victory in final game",
         False),
        
        ("Weather: Heavy Rain Expected",
         "Meteorologists predict storms this weekend",
         False),
        
        ("Recipe: Best Chocolate Cake",
         "Simple steps to make delicious dessert at home",
         False),
        
        ("Celebrity News: Actor Gets Married",
         "Hollywood star ties the knot in private ceremony",
         False),
        
        ("Gaming: New Video Game Released",
         "Popular franchise launches latest installment",
         False),
    ]
    
    passed = 0
    failed = 0
    
    print("Testing articles:\n")
    
    for i, (title, summary, expected) in enumerate(test_cases, 1):
        is_relevant, reason = is_stock_market_related(title, summary)
        
        if is_relevant == expected:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed += 1
        
        print(f"{status} | {title[:50]:50} | Expected: {expected:5} | Got: {is_relevant:5}")
        print(f"       Reason: {reason}")
        print()
    
    # Summary
    print("="*80)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("="*80)
    
    if failed == 0:
        print("\n🎉 All tests passed! Filter is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed - review filter logic")
    
    print("\n" + "="*80)
    print("✅ Test completed!")
    print("="*80 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

