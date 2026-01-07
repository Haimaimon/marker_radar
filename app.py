from __future__ import annotations
import time
import logging
import os

from config import settings
from utils.log import setup_logging
from utils.date_utils import is_today, get_today, get_age_in_days

from collectors.rss_collector import RSSCollector
from collectors.sec_collector import SECRSSCollector
from collectors.sec_filtered_collector import SECFilteredCollector
from collectors.alpha_vantage_collector import AlphaVantageCollector
from collectors.thenewsapi_collector import TheNewsAPICollector
from collectors.newsapi_ai_collector import NewsAPIaiCollector

from core.dedup import make_uid
from core.scoring import score
from core.ticker_extraction import extract_ticker
from core.validation import validate_market_impact
from core.stock_filter import is_stock_market_related

from market_data.yfinance_provider import YFinanceProvider
from market_data.market_data_manager import MarketDataManager, ProviderType
from storage.sqlite_store import SQLiteStore

from notifier.console import ConsoleNotifier
from notifier.telegram import TelegramNotifier


logger = logging.getLogger("market_radar")

def build_notifier():
    console = ConsoleNotifier()
    notifiers = [console]
    
    if settings.enable_telegram and settings.telegram_bot_token and settings.telegram_chat_id:
        tg = TelegramNotifier(
            bot_token=settings.telegram_bot_token,
            chat_id=settings.telegram_chat_id,
            silent=settings.telegram_silent,
            thread_id=settings.telegram_thread_id if settings.telegram_thread_id else None,
            retry_attempts=settings.telegram_retry_attempts,
            retry_delay=settings.telegram_retry_delay,
        )
        
        # Send test message on startup to verify connection
        logger.info("Testing Telegram connection...")
        if tg.send_test_message():
            logger.info("✅ Telegram notifier initialized successfully")
            notifiers.append(tg)
        else:
            logger.error("❌ Telegram test failed - notifier disabled")
    
    return notifiers

def main():
    setup_logging()
    logger.info("Starting Market Radar...")
    logger.info(f"Settings: poll_seconds={settings.poll_seconds}, min_impact_score={settings.min_impact_score}")
    logger.info(f"Validation: min_gap_pct={settings.min_gap_pct}, min_vol_spike={settings.min_vol_spike}")
    logger.info(f"Verbose logging: {'ENABLED' if settings.verbose_logging else 'DISABLED'}")
    logger.info(f"Date filtering: {'TODAY ONLY' if settings.only_today_news else 'ALL DATES'}")
    logger.info(f"Today's date (Israel): {get_today('Asia/Jerusalem')}")

    store = SQLiteStore("market_radar.db")
    
    # Initialize Market Data Manager with multiple providers
    md_manager = MarketDataManager()
    
    # Add Finnhub (if enabled)
    if settings.enable_finnhub and settings.finnhub_api_key:
        try:
            from market_data.finnhub_provider import FinnhubProvider
            finnhub = FinnhubProvider(settings.finnhub_api_key, rate_limit_delay=1.0)
            md_manager.add_provider(ProviderType.FINNHUB, finnhub, priority=1)
            logger.info("✅ Finnhub provider enabled (priority 1)")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Finnhub: {e}")
    
    # Add Polygon (if enabled)
    if settings.enable_polygon and settings.polygon_api_key:
        try:
            from market_data.polygon_provider import PolygonProvider
            polygon = PolygonProvider(settings.polygon_api_key, rate_limit_delay=12.0)
            md_manager.add_provider(ProviderType.POLYGON, polygon, priority=2)
            logger.info("✅ Polygon provider enabled (priority 2)")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Polygon: {e}")
    
    # Add yfinance as fallback (always enabled)
    yfinance = YFinanceProvider(cache_ttl_seconds=20, rate_limit_delay=0.5)
    md_manager.add_provider(ProviderType.YFINANCE, yfinance, priority=99)
    logger.info("✅ yfinance provider enabled (priority 99 - fallback)")
    
    notifiers = build_notifier()
    
    # Daily cleanup: Remove old news from database
    if settings.auto_cleanup_old_news:
        try:
            deleted = store.cleanup_old_news(keep_days=1)
            if deleted > 0:
                logger.info(f"📅 Daily cleanup: Removed {deleted} old news items")
            stats = store.get_stats()
            logger.info(f"📊 DB Stats: {stats['total_events']} total, {stats['today_events']} today, {stats['validated_events']} validated")
        except Exception as e:
            logger.warning(f"Cleanup warning: {e}")

    # Initialize Ticker Filter (NASDAQ & S&P 500 only) - reduces noise
    ticker_filter = None
    if settings.enable_ticker_filter:
        from core.ticker_filter import get_ticker_filter
        ticker_filter = get_ticker_filter()
        stats_filter = ticker_filter.get_stats()
        logger.info(f"🎯 Ticker filter enabled: {stats_filter['total_tickers']} tickers (NASDAQ + S&P 500)")
        logger.info(f"   Cache age: {stats_filter['cache_age_hours']:.1f}h, Valid: {stats_filter['cache_valid']}")
    else:
        logger.info("🎯 Ticker filter disabled - all tickers allowed")
    
    # Initialize Trading Signals (NEW - optional, doesn't affect existing system)
    signals_integration = None
    if settings.enable_trading_signals:
        try:
            from signals import SignalEngine, SignalsIntegration
            signal_engine = SignalEngine()
            signals_integration = SignalsIntegration(
                signal_engine=signal_engine,
                market_data=md_manager,
                min_signal_confidence=settings.signals_min_confidence,
                enabled=True,
            )
            logger.info(f"📊 Trading Signals enabled (min_confidence={settings.signals_min_confidence}%, style={settings.signals_style})")
        except Exception as e:
            logger.error(f"Failed to initialize Trading Signals: {e}")
            signals_integration = None
    else:
        logger.info("📊 Trading Signals disabled")

    # 1) News RSS Sources (verified working - tested 2025-12-29)
    rss_sources = [
        # Wire Services (HIGH PRIORITY - Press releases from companies)
        ("PR Newswire", "https://www.prnewswire.com/rss/news-releases-list.rss"),  # 20 items
        ("GlobeNewswire", "https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire%20-%20News%20Release"),  # NEW! Company announcements
        ("Business Wire", "https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeGVtUWA=="),  # NEW! Company announcements
        
        # Financial News (high volume, good quality)
        ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),  # 50 items
        ("MarketWatch Top", "https://feeds.marketwatch.com/marketwatch/topstories/"),  # 10 items
        ("MarketWatch Breaking", "https://feeds.marketwatch.com/marketwatch/marketpulse/"),  # 30 items
        ("CNBC Top News", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),  # 30 items
        ("CNBC Investing", "https://www.cnbc.com/id/15839135/device/rss/rss.html"),  # 30 items
        
        # Investment Analysis
        ("Seeking Alpha Market", "https://seekingalpha.com/market_currents.xml"),  # 7 items
        ("Seeking Alpha Articles", "https://seekingalpha.com/feed.xml"),  # 30 items
        
        # Tech & Startups (for tech stock news)
        ("TechCrunch", "https://techcrunch.com/feed/"),  # 20 items
        ("VentureBeat", "https://venturebeat.com/feed/"),  # 7 items
        ("The Verge", "https://www.theverge.com/rss/index.xml"),  # 10 items
        
        # Crypto/Fintech (optional - comment out if not needed)
        ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),  # 25 items
        ("Decrypt", "https://decrypt.co/feed"),  # 52 items
    ]
    wire_collector = RSSCollector(rss_sources)

    # 2) SEC RSS (material filings)
    # Options:
    # - SECFilteredCollector() = Only 8-K/S-4 (high-impact events) [RECOMMENDED]
    # - SECRSSCollector() = All filings (100 items, lots of noise)
    if settings.enable_sec_filtered:
        sec_collector = SECFilteredCollector()
        logger.info("🏛️  SEC Filtered collector enabled (8-K, S-4 + clinical trials)")
    elif settings.enable_sec_legacy:
        sec_collector = SECRSSCollector()
        logger.info("🏛️  SEC Legacy collector enabled (all forms)")
    else:
        sec_collector = None
        logger.info("🏛️  SEC collector disabled")
    
    # 3) Alpha Vantage News API (premium news with sentiment)
    alpha_vantage_collector = None
    if settings.enable_alpha_vantage and settings.alpha_vantage_api_key:
        logger.info("Alpha Vantage API enabled")
        alpha_vantage_collector = AlphaVantageCollector(
            api_key=settings.alpha_vantage_api_key,
            topics="technology,earnings,ipo,mergers_and_acquisitions",
            limit=50,
        )
        logger.info(f"Alpha Vantage config: {alpha_vantage_collector.get_usage_info()}")
    
    # 4) TheNewsAPI (global news coverage)
    thenewsapi_collector = None
    if settings.enable_thenewsapi and settings.thenewsapi_token:
        logger.info("TheNewsAPI enabled")
        thenewsapi_collector = TheNewsAPICollector(
            api_token=settings.thenewsapi_token,
            categories="business,tech",
            limit=50,
        )
        logger.info(f"TheNewsAPI config: {thenewsapi_collector.get_usage_info()}")
    
    # 5) NewsAPI.ai (advanced analytics)
    newsapi_ai_collector = None
    if settings.enable_newsapi_ai and settings.newsapi_ai_key:
        logger.info("NewsAPI.ai enabled")
        newsapi_ai_collector = NewsAPIaiCollector(
            api_key=settings.newsapi_ai_key,
            category_uri="news/Business",
            limit=50,
        )
        logger.info(f"NewsAPI.ai config: {newsapi_ai_collector.get_usage_info()}")
    
    poll_count = 0
    max_iterations = int(os.getenv("MAX_ITERATIONS", "0"))  # 0 = infinite

    while True:
        try:
            poll_count += 1
            
            # Check if we should exit after this iteration (for scheduled tasks)
            if max_iterations > 0 and poll_count > max_iterations:
                logger.info(f"✅ Reached max iterations ({max_iterations}), exiting...")
                break
            logger.info(f"{'='*80}")
            logger.info(f"Poll #{poll_count} - Fetching news...")
            
            # Statistics for this poll
            stats = {
                "fetched": 0,
                "duplicates": 0,
                "new": 0,
                "not_stock_related": 0,  # NEW!
                "no_ticker": 0,
                "low_score": 0,
                "high_score": 0,
                "not_validated": 0,
                "validated": 0,
                "notified": 0,
            }
            
            items = []
            items.extend(wire_collector.fetch())
            if sec_collector:
                items.extend(sec_collector.fetch())
            
            # Premium APIs (if enabled)
            if alpha_vantage_collector:
                items.extend(alpha_vantage_collector.fetch())
            
            if thenewsapi_collector:
                items.extend(thenewsapi_collector.fetch())
            
            if newsapi_ai_collector:
                items.extend(newsapi_ai_collector.fetch())
            
            stats["fetched"] = len(items)
            logger.info(f"📥 Fetched {len(items)} total items from all sources")

            for item in items:
                item.uid = make_uid(item.title, item.link, item.published)
                
                if store.exists(item.uid):
                    stats["duplicates"] += 1
                    if settings.verbose_logging:
                        logger.debug(f"⏭️  SKIP (duplicate): {item.title[:60]}...")
                    continue
                
                # Date filtering: Only today's news (Israel time)
                if settings.only_today_news and item.published:
                    if not is_today(item.published, tz_name="Asia/Jerusalem"):
                        age_days = get_age_in_days(item.published, tz_name="Asia/Jerusalem")
                        if settings.verbose_logging:
                            logger.debug(f"📅 SKIP (old news, {age_days} days): {item.title[:60]}...")
                        continue
                
                stats["new"] += 1

                # 0.5) Stock Market Relevance Check (NEW!)
                is_relevant, relevance_reason = is_stock_market_related(item.title, item.summary)
                if not is_relevant:
                    stats["not_stock_related"] += 1
                    if settings.verbose_logging:
                        logger.debug(f"🚫 NOT STOCK-RELATED: {item.title[:60]}... | Reason: {relevance_reason}")
                    continue  # Skip this article

                # 1) Ticker Extraction
                item.ticker = extract_ticker(item.title, item.summary)
                
                # 1.5) Ticker Filtering (NASDAQ & S&P 500 only) - reduces noise
                if ticker_filter and item.ticker:
                    if not ticker_filter.is_valid_ticker(item.ticker):
                        if settings.verbose_logging:
                            logger.debug(f"🎯 FILTERED OUT (not NASDAQ/S&P 500): {item.ticker} - {item.title[:50]}...")
                        continue  # Skip this article
                
                if not item.ticker and settings.verbose_logging:
                    stats["no_ticker"] += 1
                    logger.debug(f"⚠️  No ticker found: {item.title[:60]}...")

                # 2) Impact Scoring
                item.impact_score, item.impact_reason = score(item.source, item.title, item.summary)
                
                if item.impact_score < settings.min_impact_score:
                    stats["low_score"] += 1
                    if settings.verbose_logging:
                        logger.debug(
                            f"❌ LOW SCORE ({item.impact_score}): "
                            f"{item.ticker or 'N/A'} - {item.title[:50]}... | Reason: {item.impact_reason}"
                        )
                    store.save(item)  # keep history if you want
                    continue
                
                stats["high_score"] += 1
                if settings.verbose_logging:
                    logger.debug(
                        f"✅ HIGH SCORE ({item.impact_score}): "
                        f"{item.ticker or 'N/A'} - {item.title[:50]}... | Reason: {item.impact_reason}"
                    )

                # 3) Market Validation (gap/volume) - optional
                if settings.enable_market_validation and item.ticker:
                    try:
                        ok, reason = validate_market_impact(
                            item=item,
                            md=md_manager,
                            min_gap_pct=settings.min_gap_pct,
                            min_vol_spike=settings.min_vol_spike,
                        )
                        item.validated = ok
                        item.validation_reason = reason
                    except Exception as e:
                        # Handle rate limits and other errors gracefully
                        logger.warning(f"Market validation failed for {item.ticker}: {e}")
                        item.validated = True  # Allow through if validation fails
                        item.validation_reason = f"Validation skipped: {str(e)[:50]}"
                        time.sleep(1)  # Brief pause before continuing
                else:
                    # Skip validation if disabled or no ticker
                    item.validated = True
                    item.validation_reason = "Market validation disabled or no ticker"

                # Save always
                store.save(item)

                if not item.validated:
                    stats["not_validated"] += 1
                    if settings.verbose_logging:
                        logger.debug(
                            f"⚠️  NOT VALIDATED: {item.ticker or 'N/A'} - {item.title[:50]}... | "
                            f"Reason: {reason}"
                        )
                    continue
                
                stats["validated"] += 1
                logger.info(
                    f"🔥 VALIDATED EVENT: {item.ticker or 'N/A'} (score={item.impact_score}) - {item.title[:60]}..."
                )

                # 4) Notify only if validated
                if item.validated:
                    stats["notified"] += 1
                    for n in notifiers:
                        n.notify(item)
                    
                    # 5) Generate Trading Signal (NEW - optional, doesn't affect existing flow)
                    if signals_integration and signals_integration.enabled:
                        try:
                            signal = signals_integration.process_news_item(item)
                            
                            if signal and signals_integration.should_send_signal(signal):
                                # Format signal message
                                signal_message = signals_integration.format_signal_message(
                                    signal,
                                    style=settings.signals_style
                                )
                                
                                # Send signal (same notifiers as news)
                                for n in notifiers:
                                    if hasattr(n, 'send_html'):
                                        n.send_html(signal_message)
                                    else:
                                        # Fallback for notifiers without HTML support
                                        logger.info(signal_message)
                                
                                logger.info(f"📊 Trading signal sent for {signal.ticker}")
                        except Exception as e:
                            logger.error(f"Error generating/sending signal: {e}", exc_info=True)
            
            # Print poll summary
            logger.info(f"📊 Poll #{poll_count} Summary:")
            logger.info(f"   Fetched: {stats['fetched']} | New: {stats['new']} | Duplicates: {stats['duplicates']}")
            if stats['not_stock_related'] > 0:
                logger.info(f"   🚫 Not Stock-Related: {stats['not_stock_related']}")
            if stats['no_ticker'] > 0:
                logger.info(f"   No Ticker: {stats['no_ticker']}")
            logger.info(f"   Low Score: {stats['low_score']} | High Score: {stats['high_score']}")
            logger.info(f"   Not Validated: {stats['not_validated']} | Validated: {stats['validated']}")
            logger.info(f"   🔔 Notified: {stats['notified']}")
            logger.info(f"Next poll in {settings.poll_seconds} seconds...")

            time.sleep(settings.poll_seconds)

        except KeyboardInterrupt:
            logger.info("Stopped by user.")
            break
        except Exception as e:
            logger.exception(f"Loop error: {e}")
            time.sleep(settings.poll_seconds)

if __name__ == "__main__":
    main()
