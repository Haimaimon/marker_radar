from __future__ import annotations
import time
from typing import Dict
import yfinance as yf
from .base import MarketSnapshot, MarketDataProvider

class YFinanceProvider(MarketDataProvider):
    """
    Free-ish, not official. Works well enough for validation signals.
    Includes lightweight caching to avoid hammering yfinance.
    Now with rate limiting to avoid getting blocked.
    """

    def __init__(self, cache_ttl_seconds: int = 20, rate_limit_delay: float = 0.5):
        self.cache_ttl = cache_ttl_seconds
        self.rate_limit_delay = rate_limit_delay
        self._cache: Dict[str, tuple[float, MarketSnapshot]] = {}
        self._last_request_time: float = 0.0

    def get_snapshot(self, symbol: str) -> MarketSnapshot:
        now = time.time()
        
        # Check cache first
        if symbol in self._cache:
            ts, snap = self._cache[symbol]
            if now - ts < self.cache_ttl:
                return snap
        
        # Rate limiting: ensure minimum delay between requests
        time_since_last = now - self._last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self._last_request_time = time.time()
        t = yf.Ticker(symbol)

        # fast_info is usually fast, may not contain everything
        fi = getattr(t, "fast_info", {}) or {}

        price = _to_float(fi.get("lastPrice") or fi.get("last_price") or fi.get("regularMarketPrice"))
        prev_close = _to_float(fi.get("previousClose") or fi.get("previous_close"))
        volume = _to_float(fi.get("lastVolume") or fi.get("last_volume") or fi.get("regularMarketVolume"))
        avg10 = _to_float(fi.get("tenDayAverageVolume") or fi.get("ten_day_average_volume") or fi.get("averageDailyVolume10Day"))

        snap = MarketSnapshot(
            symbol=symbol,
            price=price,
            prev_close=prev_close,
            volume=volume,
            avg_volume_10d=avg10,
        )
        self._cache[symbol] = (now, snap)
        return snap

def _to_float(v):
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None
