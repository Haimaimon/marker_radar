#!/usr/bin/env python3
"""
Test script for enhanced ticker extraction
Demonstrates company name → ticker mapping
"""

from core.ticker_extraction import extract_ticker, extract_all_tickers

# Test cases: (title, expected_ticker)
TEST_CASES = [
    # Explicit formats
    ("NASDAQ:AAPL hits new high", "AAPL"),
    ("Apple (AAPL) announces new iPhone", "AAPL"),
    ("$TSLA stock jumps 10% after earnings", "TSLA"),
    
    # Company names (NEW!)
    ("Apple announces new MacBook Pro", "AAPL"),
    ("Microsoft beats earnings expectations", "MSFT"),
    ("Tesla stock jumps after delivery numbers", "TSLA"),
    ("Nvidia unveils new AI chip", "NVDA"),
    ("Amazon Web Services expands globally", "AMZN"),
    ("Meta releases new VR headset", "META"),
    ("Facebook parent company Meta announces...", "META"),
    ("Alphabet's Google launches new product", "GOOGL"),
    
    # Finance companies
    ("JPMorgan Chase reports strong quarter", "JPM"),
    ("Bank of America increases dividend", "BAC"),
    ("Goldman Sachs downgrades tech sector", "GS"),
    ("Visa processes record transactions", "V"),
    
    # Tech companies
    ("Adobe announces Creative Cloud update", "ADBE"),
    ("Salesforce acquires startup", "CRM"),
    ("Oracle wins cloud contract", "ORCL"),
    ("Intel unveils new processor", "INTC"),
    ("AMD launches new GPU", "AMD"),
    ("Qualcomm settles patent dispute", "QCOM"),
    
    # Pharma/Healthcare
    ("Pfizer gets FDA approval", "PFE"),
    ("Moderna announces vaccine update", "MRNA"),
    ("Johnson & Johnson beats estimates", "JNJ"),
    
    # Automotive
    ("Ford announces electric vehicle", "F"),
    ("General Motors invests in batteries", "GM"),
    ("Rivian stock drops after recall", "RIVN"),
    
    # Retail
    ("Walmart reports holiday sales", "WMT"),
    ("Target misses earnings", "TGT"),
    ("Nike launches new shoe line", "NKE"),
    ("Starbucks raises prices", "SBUX"),
    
    # Variations and edge cases
    ("NVDA beats earnings with record revenue", "NVDA"),  # ALL-CAPS at start
    ("Analysis: AAPL stock undervalued", "AAPL"),  # ALL-CAPS ticker
    ("Apple Inc. announces", "AAPL"),  # With Inc suffix
    ("Microsoft Corporation beats", "MSFT"),  # With Corporation suffix
    
    # Should NOT match (negative tests)
    ("Market commentary on tech sector", None),  # No company
    ("CEO discusses AI strategy", None),  # Generic terms
    ("USA economy grows", None),  # Blacklisted
]


def run_tests():
    """Run all test cases and report results"""
    print("=" * 80)
    print("Ticker Extraction - Test Results")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for title, expected in TEST_CASES:
        result = extract_ticker(title, "")
        status = "[PASS]" if result == expected else "[FAIL]"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status} {title}")
        print(f"   Expected: {expected}")
        print(f"   Got:      {result}")
    
    print("\n" + "=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")
    print(f"Success rate: {passed/len(TEST_CASES)*100:.1f}%")
    print("=" * 80)
    
    return failed == 0


def demo_extract_all():
    """Demo the extract_all_tickers function"""
    print("\n\n" + "=" * 80)
    print("Demo: Extract Multiple Tickers from Text")
    print("=" * 80)
    
    examples = [
        "Apple (AAPL) and Microsoft (MSFT) lead tech stocks higher",
        "FAANG stocks: Facebook, Apple, Amazon, Netflix, Google all up",
        "$TSLA, $NVDA, and $AMD are top picks according to analyst",
    ]
    
    for text in examples:
        tickers = extract_all_tickers(text)
        print(f"\nText: {text}")
        print(f"Tickers found: {', '.join(tickers) if tickers else 'None'}")


def interactive_mode():
    """Interactive testing mode"""
    print("\n\n" + "=" * 80)
    print("Interactive Mode - Test Your Own Headlines")
    print("=" * 80)
    print("Enter a headline to extract tickers (or 'quit' to exit)")
    
    while True:
        try:
            text = input("\n> ").strip()
            if not text or text.lower() == 'quit':
                break
            
            ticker = extract_ticker(text, "")
            all_tickers = extract_all_tickers(text)
            
            print(f"Primary ticker: {ticker or 'None found'}")
            if len(all_tickers) > 1:
                print(f"All tickers: {', '.join(all_tickers)}")
        except (KeyboardInterrupt, EOFError):
            break
    
    print("\nGoodbye!")


if __name__ == "__main__":
    import sys
    
    # Run automated tests
    success = run_tests()
    
    # Demo extract_all
    demo_extract_all()
    
    # Interactive mode if requested
    if "--interactive" in sys.argv or "-i" in sys.argv:
        interactive_mode()
    else:
        print("\nTip: Run with --interactive for interactive testing mode")
    
    sys.exit(0 if success else 1)

