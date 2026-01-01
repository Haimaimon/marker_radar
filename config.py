from __future__ import annotations
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

def _get_bool(key: str, default: bool = False) -> bool:
    v = os.getenv(key, str(default)).strip().lower()
    return v in ("1", "true", "yes", "y", "on")

@dataclass(frozen=True)
class Settings:
    poll_seconds: int = int(os.getenv("POLL_SECONDS", "30"))
    min_impact_score: int = int(os.getenv("MIN_IMPACT_SCORE", "70"))
    
    # Logging
    verbose_logging: bool = _get_bool("VERBOSE_LOGGING", False)
    
    # Date Filtering
    only_today_news: bool = _get_bool("ONLY_TODAY_NEWS", True)  # Filter to today's news only
    auto_cleanup_old_news: bool = _get_bool("AUTO_CLEANUP_OLD_NEWS", True)  # Clean old news from DB
    
    # Market Data - General
    enable_market_validation: bool = _get_bool("ENABLE_MARKET_VALIDATION", True)
    
    # Market Data - Finnhub
    enable_finnhub: bool = _get_bool("ENABLE_FINNHUB", False)
    finnhub_api_key: str = os.getenv("FINNHUB_API_KEY", "")
    
    # Market Data - Polygon
    enable_polygon: bool = _get_bool("ENABLE_POLYGON", False)
    polygon_api_key: str = os.getenv("POLYGON_API_KEY", "")
    
    # SEC Filtered Collector
    enable_sec_filtered: bool = _get_bool("ENABLE_SEC_FILTERED", True)  # Use filtered SEC (8-K, S-4)
    enable_sec_legacy: bool = _get_bool("ENABLE_SEC_LEGACY", False)  # Use old SEC collector (all forms)
    
    # Alpha Vantage API
    enable_alpha_vantage: bool = _get_bool("ENABLE_ALPHA_VANTAGE", False)
    alpha_vantage_api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    
    # TheNewsAPI
    enable_thenewsapi: bool = _get_bool("ENABLE_THENEWSAPI", False)
    thenewsapi_token: str = os.getenv("THENEWSAPI_TOKEN", "")
    
    # NewsAPI.ai
    enable_newsapi_ai: bool = _get_bool("ENABLE_NEWSAPI_AI", False)
    newsapi_ai_key: str = os.getenv("NEWSAPI_AI_KEY", "")

    # Validation
    min_gap_pct: float = float(os.getenv("MIN_GAP_PCT", "4.0"))
    min_vol_spike: float = float(os.getenv("MIN_VOL_SPIKE", "1.8"))
    
    # Ticker Filtering (Noise Reduction)
    enable_ticker_filter: bool = _get_bool("ENABLE_TICKER_FILTER", True)  # Only NASDAQ & S&P 500
    
    # Trading Signals (NEW!)
    enable_trading_signals: bool = _get_bool("ENABLE_TRADING_SIGNALS", False)  # Trading signals system
    signals_min_confidence: int = int(os.getenv("SIGNALS_MIN_CONFIDENCE", "75"))  # Min confidence %
    signals_style: str = os.getenv("SIGNALS_STYLE", "rich")  # "rich", "compact", "console"

    # Telegram
    enable_telegram: bool = _get_bool("ENABLE_TELEGRAM", False)
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    telegram_silent: bool = _get_bool("TELEGRAM_SILENT", False)  # Disable notification sound
    telegram_thread_id: str = os.getenv("TELEGRAM_THREAD_ID", "")  # For topic-enabled groups
    telegram_retry_attempts: int = int(os.getenv("TELEGRAM_RETRY_ATTEMPTS", "3"))
    telegram_retry_delay: int = int(os.getenv("TELEGRAM_RETRY_DELAY", "2"))

settings = Settings()
