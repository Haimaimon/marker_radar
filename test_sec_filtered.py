"""
Test SEC Filtered Collector
============================
Tests the new SEC filtered collector that only fetches high-impact forms (8-K, S-4)
and identifies clinical trial/vaccine-related filings.

Usage:
    python test_sec_filtered.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from collectors.sec_filtered_collector import SECFilteredCollector


def main():
    print("🏛️  Testing SEC Filtered Collector")
    print("=" * 80)
    print("\n📋 This collector filters SEC filings to:")
    print("   • 8-K: Current events (M&A, earnings, management changes, bankruptcy)")
    print("   • S-4: Registration for M&A")
    print("   • Clinical trials & vaccine keywords (Phase I/II/III, FDA approval, etc.)")
    print("\n" + "=" * 80)
    
    collector = SECFilteredCollector()
    
    print("\n🔍 Fetching SEC filings...")
    items = collector.fetch()
    
    print(f"\n📊 Results:")
    print(f"   Total filtered items: {len(items)}")
    print(f"   Allowed forms: {', '.join(sorted(collector.ALLOWED_FORMS))}")
    
    # Count clinical/pharma items
    clinical_count = sum(1 for item in items if item.raw.get("is_clinical", False))
    print(f"   Clinical/pharma related: {clinical_count}")
    
    print("\n" + "=" * 80)
    
    if items:
        print("\n📄 Sample filings:\n")
        for i, item in enumerate(items[:10], 1):
            form_type = item.raw.get("form_type", "")
            is_clinical = item.raw.get("is_clinical", False)
            
            print(f"{i}. [{form_type}] {item.title[:70]}...")
            print(f"   📅 {item.published}")
            print(f"   🔗 {item.link}")
            if is_clinical:
                print(f"   💊 CLINICAL/PHARMA RELATED ⭐")
            print()
    else:
        print("\n⚠️  No items found.")
        print("   This might be normal if no 8-K/S-4 filings in latest 100.")
        print("   SEC RSS feeds update throughout the day.")
    
    print("=" * 80)
    print("\n✅ Test complete!")
    print("\n💡 Tips:")
    print("   • 8-K filings = Most important (material events)")
    print("   • S-4 filings = M&A activity")
    print("   • Clinical keywords = Pharma stock movers")
    print("   • Set ENABLE_SEC_FILTERED=true in .env to use this collector")


if __name__ == "__main__":
    main()

