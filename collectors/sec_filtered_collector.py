"""
SEC Filtered Collector
======================
Collects only high-impact SEC filings:
- 8-K: Current events (M&A, earnings, management changes, bankruptcy, etc.)
- S-4: Registration for M&A

Also identifies clinical trial and vaccine-related filings which can significantly impact stock prices.

Author: Market Radar Team
"""

from __future__ import annotations
import logging
import re
from typing import List, Set
import feedparser
from core.models import NewsItem
from utils.date_utils import parse_date

logger = logging.getLogger(__name__)


class SECFilteredCollector:
    """
    Collects filtered SEC filings focusing on high-impact forms.
    
    Filtered Forms:
    - 8-K: Current Events (most important!)
    - S-4: Registration for M&A
    
    Special Keywords (boost score):
    - Clinical trials (Phase I, II, III, FDA approval)
    - Vaccines (vaccine, immunization, clinical study)
    - Drug approvals (FDA, EMA, drug candidate)
    """
    
    # High-impact SEC forms we want to track
    ALLOWED_FORMS = {
        "8-K",    # Current Events - most important
        "8-K/A",  # Amended 8-K
        "S-4",    # Registration for M&A
        "S-4/A",  # Amended S-4
    }
    
    # Clinical trial and pharma keywords that significantly impact stock prices
    CLINICAL_KEYWORDS = [
        # Clinical trials
        r"\bphase\s+[I1]\b",
        r"\bphase\s+[I2]\b", 
        r"\bphase\s+[I3]\b",
        r"\bphase\s+1\b",
        r"\bphase\s+2\b",
        r"\bphase\s+3\b",
        r"\bclinical\s+trial",
        r"\bclinical\s+study",
        r"\btrial\s+results?",
        r"\bstudy\s+results?",
        
        # FDA and approvals
        r"\bFDA\s+approval",
        r"\bFDA\s+clearance",
        r"\bFDA\s+granted",
        r"\bFDA\s+accepted",
        r"\bbreakthrough\s+therapy",
        r"\bfast\s+track",
        r"\borphan\s+drug",
        r"\bpriority\s+review",
        r"\bEMA\s+approval",
        
        # Vaccines
        r"\bvaccine",
        r"\bimmunization",
        r"\bimmunotherapy",
        r"\bantibody",
        r"\bmonoclonal",
        
        # Drug development
        r"\bdrug\s+candidate",
        r"\btherapeutic",
        r"\btreatment\s+candidate",
        r"\binvestigational\s+drug",
        r"\bIND\s+application",
        r"\bNDA\s+submission",
        r"\bBLA\s+submission",
        
        # Success indicators
        r"\bprimary\s+endpoint",
        r"\bstatistically\s+significant",
        r"\bpositive\s+results?",
        r"\bsuccessful\s+completion",
        r"\bmeets?\s+endpoint",
    ]
    
    def __init__(self, rss_url: str = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=100&output=atom"):
        """
        Initialize the SEC Filtered Collector.
        
        Args:
            rss_url: SEC EDGAR RSS feed URL (default: latest 100 filings)
        """
        self.rss_url = rss_url
        self.clinical_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.CLINICAL_KEYWORDS]
        
    def fetch(self) -> List[NewsItem]:
        """
        Fetch filtered SEC filings.
        
        Returns:
            List of NewsItem objects for high-impact SEC filings
        """
        try:
            feed = feedparser.parse(self.rss_url)
            news_items: List[NewsItem] = []
            
            filtered_count = 0
            clinical_count = 0
            
            for entry in feed.entries:
                # Extract filing type from title
                # Title format: "8-K - COMPANY NAME (0001234567) (Filer)"
                title = entry.get("title", "")
                form_type = self._extract_form_type(title)
                
                # Filter: only allow specific forms
                if form_type not in self.ALLOWED_FORMS:
                    filtered_count += 1
                    continue
                
                # Extract ticker from entry (SEC provides CIK, we'll extract from title)
                ticker = self._extract_ticker_from_title(title)
                
                # Get summary and link
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                published = entry.get("published", "")
                
                # Parse date
                published_dt = parse_date(published)
                published_str = published_dt.isoformat() if published_dt else ""
                
                # Check for clinical trial / vaccine keywords
                is_clinical = self._is_clinical_related(title, summary)
                if is_clinical:
                    clinical_count += 1
                
                # Create NewsItem with enhanced raw data
                news_items.append(NewsItem(
                    source=f"SEC ({form_type})",
                    title=title,
                    link=link,
                    published=published_str,
                    summary=summary,
                    ticker=ticker,
                    raw={
                        "form_type": form_type,
                        "is_clinical": is_clinical,
                        "filing_url": link,
                    }
                ))
            
            logger.info(
                f"🏛️  SEC Filtered: fetched {len(news_items)} items "
                f"(filtered out {filtered_count}, {clinical_count} clinical/pharma)"
            )
            return news_items
            
        except Exception as e:
            logger.exception(f"Error fetching SEC filings: {e}")
            return []
    
    def _extract_form_type(self, title: str) -> str:
        """
        Extract form type from SEC filing title.
        
        Args:
            title: Filing title (e.g., "8-K - APPLE INC (0000320193) (Filer)")
            
        Returns:
            Form type (e.g., "8-K") or empty string
        """
        # Form type is usually at the start, before the first " - "
        match = re.match(r"^([\w-]+/?\w*)\s*-", title)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_ticker_from_title(self, title: str) -> str | None:
        """
        Extract ticker symbol from SEC filing title.
        
        Note: SEC titles don't always include tickers, but we can try to extract
        company names and match them using our company_tickers mapping.
        
        Args:
            title: Filing title
            
        Returns:
            Ticker symbol or None
        """
        # SEC titles format: "FORM - COMPANY NAME (CIK) (Filer)"
        # We'll extract company name and let ticker_extraction.py handle it
        match = re.match(r"^[\w-]+/?\w*\s*-\s*([^(]+)", title)
        if match:
            company_name = match.group(1).strip()
            # Return None here, let the main ticker extraction logic handle it
            # We'll store the company name in the title for extraction
            return None
        return None
    
    def _is_clinical_related(self, title: str, summary: str) -> bool:
        """
        Check if filing is related to clinical trials, vaccines, or drug development.
        
        Args:
            title: Filing title
            summary: Filing summary
            
        Returns:
            True if filing contains clinical/pharma keywords
        """
        combined_text = f"{title} {summary}".lower()
        
        for pattern in self.clinical_patterns:
            if pattern.search(combined_text):
                return True
        
        return False


def main():
    """Test the SEC Filtered Collector."""
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("🏛️  Testing SEC Filtered Collector\n")
    print("=" * 80)
    
    collector = SECFilteredCollector()
    items = collector.fetch()
    
    print(f"\n📊 Total filtered items: {len(items)}")
    print(f"📋 Allowed forms: {', '.join(sorted(collector.ALLOWED_FORMS))}")
    print("\n" + "=" * 80)
    
    if items:
        print("\n🔍 Sample items:\n")
        for i, item in enumerate(items[:5], 1):
            is_clinical = item.raw.get("is_clinical", False)
            form_type = item.raw.get("form_type", "")
            
            print(f"{i}. [{form_type}] {item.title[:80]}...")
            print(f"   🔗 {item.link}")
            if is_clinical:
                print(f"   💊 CLINICAL/PHARMA RELATED!")
            print()
    else:
        print("\n⚠️  No items found. This might be normal if no 8-K/S-4 filings in latest 100.")
    
    print("=" * 80)


if __name__ == "__main__":
    main()

