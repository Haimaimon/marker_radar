"""
Ticker Filter - NASDAQ & S&P 500
=================================
Filters tickers to only major US indices (NASDAQ & S&P 500) to reduce noise.

Features:
- Auto-downloads ticker lists from reliable sources
- Daily cache refresh
- Fast O(1) lookup
- Automatic fallback if download fails

Author: Market Radar Team
"""

from __future__ import annotations
import logging
import json
import time
from pathlib import Path
from typing import Set, Optional
import requests

logger = logging.getLogger(__name__)


class TickerFilter:
    """
    Filters tickers to only NASDAQ and S&P 500 stocks.
    
    Uses cached lists that refresh daily.
    """
    
    CACHE_FILE = Path("ticker_cache.json")
    CACHE_TTL_SECONDS = 86400  # 24 hours
    
    # Backup static list (top 100 by market cap - in case download fails)
    FALLBACK_TICKERS = {
        # FAANG + Big Tech
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA", "AMD", "INTC",
        # Major companies
        "JPM", "JNJ", "V", "WMT", "PG", "MA", "HD", "CVX", "MRK", "ABBV",
        "KO", "PEP", "COST", "AVGO", "CSCO", "ADBE", "ACN", "NFLX", "DIS", "CRM",
        "VZ", "TMO", "NKE", "CMCSA", "MCD", "ABT", "ORCL", "TXN", "DHR", "UNP",
        "NEE", "LIN", "QCOM", "PM", "HON", "UPS", "RTX", "IBM", "AMGN", "LOW",
        "SPGI", "INTU", "BA", "EL", "CAT", "GS", "NOW", "SBUX", "BLK", "AXP",
        # Biotech/Pharma
        "GILD", "REGN", "VRTX", "BIIB", "AMGN", "MRNA", "BNTX",
        # Other major
        "PYPL", "AMAT", "ADI", "ISRG", "MDLZ", "BKNG", "LRCX", "SYK", "TJX", "ADP",
        "CI", "MMC", "ZTS", "CB", "DUK", "SO", "CME", "USB", "PNC", "TFC",
        "SCHW", "MS", "COF", "BK", "TRV", "AON", "ICE", "MCO", "AFL", "MET",
    }
    
    def __init__(self, cache_file: Optional[Path] = None):
        """
        Initialize ticker filter.
        
        Args:
            cache_file: Custom cache file path (optional)
        """
        self.cache_file = cache_file or self.CACHE_FILE
        self.tickers: Set[str] = set()
        self.last_update: float = 0
        self._load_or_refresh()
    
    def _load_or_refresh(self) -> None:
        """Load from cache or refresh if expired."""
        if self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text(encoding="utf-8"))
                self.tickers = set(data.get("tickers", []))
                self.last_update = data.get("timestamp", 0)
                
                # Check if cache is still valid
                age = time.time() - self.last_update
                if age < self.CACHE_TTL_SECONDS:
                    logger.info(f"✅ Loaded {len(self.tickers)} tickers from cache (age: {age/3600:.1f}h)")
                    return
                else:
                    logger.info(f"⏰ Cache expired (age: {age/3600:.1f}h), refreshing...")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
        
        # Refresh cache
        self._refresh_tickers()
    
    def _refresh_tickers(self) -> None:
        """Download fresh ticker lists from reliable sources."""
        logger.info("🔄 Refreshing ticker lists...")
        
        new_tickers = set()
        
        # Method 1: Download from Wikipedia (S&P 500)
        try:
            sp500_tickers = self._get_sp500_tickers()
            new_tickers.update(sp500_tickers)
            logger.info(f"✅ Downloaded {len(sp500_tickers)} S&P 500 tickers")
        except Exception as e:
            logger.warning(f"Failed to download S&P 500 list: {e}")
        
        # Method 2: Download from NASDAQ API
        try:
            nasdaq_tickers = self._get_nasdaq_tickers()
            new_tickers.update(nasdaq_tickers)
            logger.info(f"✅ Downloaded {len(nasdaq_tickers)} NASDAQ tickers")
        except Exception as e:
            logger.warning(f"Failed to download NASDAQ list: {e}")
        
        # Fallback to static list if download failed
        if not new_tickers:
            logger.warning("⚠️  Failed to download ticker lists, using fallback list")
            new_tickers = self.FALLBACK_TICKERS.copy()
        
        # Update instance
        self.tickers = new_tickers
        self.last_update = time.time()
        
        # Save to cache
        try:
            cache_data = {
                "tickers": sorted(list(self.tickers)),
                "timestamp": self.last_update,
                "count": len(self.tickers)
            }
            self.cache_file.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")
            logger.info(f"💾 Saved {len(self.tickers)} tickers to cache")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")
    
    def _get_sp500_tickers(self) -> Set[str]:
        """
        Get S&P 500 tickers from Wikipedia.
        
        Returns:
            Set of ticker symbols
        """
        try:
            import pandas as pd
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            
            # Add headers to avoid 403 Forbidden
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Read HTML with custom headers
            tables = pd.read_html(url, storage_options={'User-Agent': headers['User-Agent']})
            df = tables[0]
            tickers = set(df['Symbol'].str.replace('.', '-').tolist())
            return tickers
        except ImportError:
            logger.warning("pandas not installed, cannot fetch S&P 500 list")
            return set()
        except Exception as e:
            logger.warning(f"Error fetching S&P 500: {e}")
            return set()
            # Fallback: use a static API or smaller list
            logger.warning("pandas not available, using alternative method")
            return self._get_sp500_alternative()
    
    def _get_sp500_alternative(self) -> Set[str]:
        """Alternative method to get S&P 500 tickers without pandas."""
        # Use a public API or return a curated list
        # For now, return empty and rely on NASDAQ + fallback
        return set()
    
    def _get_nasdaq_tickers(self) -> Set[str]:
        """
        Get NASDAQ tickers from NASDAQ FTP.
        
        Returns:
            Set of ticker symbols
        """
        try:
            # NASDAQ provides a daily updated file
            url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&exchange=nasdaq"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            rows = data.get("data", {}).get("rows", [])
            
            tickers = {row["symbol"] for row in rows if "symbol" in row}
            
            # Filter out weird symbols (with dots, dashes, special chars)
            tickers = {t for t in tickers if len(t) <= 5 and t.isalpha()}
            
            return tickers
            
        except Exception as e:
            logger.warning(f"NASDAQ API failed: {e}, trying alternative...")
            return self._get_nasdaq_alternative()
    
    def _get_nasdaq_alternative(self) -> Set[str]:
        """Alternative method to get NASDAQ tickers."""
        # Fallback: download from FTP
        try:
            url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"
            response = requests.get(url.replace("ftp://", "http://"), timeout=30)
            response.raise_for_status()
            
            tickers = set()
            for line in response.text.split("\n")[1:]:  # Skip header
                parts = line.split("|")
                if len(parts) > 0 and parts[0]:
                    symbol = parts[0].strip()
                    if symbol and len(symbol) <= 5 and symbol.isalpha():
                        tickers.add(symbol)
            
            return tickers
        except Exception as e:
            logger.warning(f"Alternative NASDAQ source also failed: {e}")
            return set()
    
    def is_valid_ticker(self, ticker: Optional[str]) -> bool:
        """
        Check if ticker is in NASDAQ or S&P 500.
        
        Args:
            ticker: Ticker symbol to check
            
        Returns:
            True if ticker is valid, False otherwise
        """
        if not ticker:
            return False
        
        ticker_clean = ticker.upper().strip()
        
        # Check cache age
        age = time.time() - self.last_update
        if age > self.CACHE_TTL_SECONDS:
            logger.debug(f"Cache expired, refreshing in background...")
            try:
                self._refresh_tickers()
            except Exception as e:
                logger.warning(f"Background refresh failed: {e}")
        
        return ticker_clean in self.tickers
    
    def get_stats(self) -> dict:
        """Get filter statistics."""
        age_hours = (time.time() - self.last_update) / 3600
        return {
            "total_tickers": len(self.tickers),
            "cache_age_hours": age_hours,
            "cache_valid": age_hours < (self.CACHE_TTL_SECONDS / 3600),
            "cache_file": str(self.cache_file),
        }
    
    def force_refresh(self) -> None:
        """Force refresh ticker lists (useful for testing)."""
        logger.info("🔄 Forcing ticker list refresh...")
        self._refresh_tickers()


# Global instance (lazy initialization)
_global_filter: Optional[TickerFilter] = None


def get_ticker_filter() -> TickerFilter:
    """Get or create the global ticker filter instance."""
    global _global_filter
    if _global_filter is None:
        _global_filter = TickerFilter()
    return _global_filter


# Convenience function
def is_major_ticker(ticker: Optional[str]) -> bool:
    """
    Quick check if ticker is in NASDAQ or S&P 500.
    
    Args:
        ticker: Ticker symbol
        
    Returns:
        True if ticker is in major indices
    """
    return get_ticker_filter().is_valid_ticker(ticker)

