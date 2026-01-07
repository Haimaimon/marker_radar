from __future__ import annotations
import sqlite3
from typing import Optional
from core.models import NewsItem
from utils.date_utils import parse_datetime_utc

class SQLiteStore:
    def __init__(self, db_path: str = "market_radar.db"):
        self.db_path = db_path
        self._init()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init(self) -> None:
        with self._conn() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS events (
                uid TEXT PRIMARY KEY,
                source TEXT,
                title TEXT,
                link TEXT,
                published TEXT,
                published_utc TEXT,        -- ✅ חדש
                ticker TEXT,
                impact_score INTEGER,
                impact_reason TEXT,
                validated INTEGER,
                validation_reason TEXT,
                gap_pct REAL,
                vol_spike REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)
            c.commit()

            # ✅ migrate old DBs (add published_utc if missing)
            cols = {row[1] for row in c.execute("PRAGMA table_info(events)").fetchall()}
            if "published_utc" not in cols:
                c.execute("ALTER TABLE events ADD COLUMN published_utc TEXT")
                c.commit()
    def exists(self, uid: str) -> bool:
        with self._conn() as c:
            row = c.execute("SELECT 1 FROM events WHERE uid = ? LIMIT 1", (uid,)).fetchone()
            return row is not None

    def save(self, item: NewsItem) -> None:
        # try to convert item.published -> utc string (best effort)
        published_utc = ""
        try:
            from utils.date_utils import parse_datetime_utc
            dt = parse_datetime_utc(item.published) if item.published else None
            published_utc = dt.isoformat() if dt else ""
        except Exception:
            published_utc = ""

        with self._conn() as c:
            c.execute("""
            INSERT OR IGNORE INTO events
            (uid, source, title, link, published, published_utc, ticker, impact_score, impact_reason,
             validated, validation_reason, gap_pct, vol_spike)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.uid, item.source, item.title, item.link, item.published, published_utc,
                item.ticker, item.impact_score, item.impact_reason,
                1 if item.validated else 0, item.validation_reason,
                item.gap_pct, item.vol_spike
            ))
            c.commit()
    
    def cleanup_old_news(self, keep_days: int = 1) -> int:
        """
        Remove news older than N days from the database
        
        Args:
            keep_days: Number of days to keep (default: 1 = today only)
        
        Returns:
            Number of rows deleted
        """
        with self._conn() as c:
            result = c.execute("""
                DELETE FROM events 
                WHERE created_at < datetime('now', ? || ' days')
            """, (f'-{keep_days}',))
            deleted = result.rowcount
            c.commit()
            return deleted
            
    def get_stats(self) -> dict:
        """Get database statistics"""
        with self._conn() as c:
            total = c.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            today = c.execute("""
                SELECT COUNT(*) FROM events 
                WHERE created_at >= date('now')
            """).fetchone()[0]
            validated = c.execute("""
                SELECT COUNT(*) FROM events 
                WHERE validated = 1
            """).fetchone()[0]
            
            return {
                "total_events": total,
                "today_events": today,
                "validated_events": validated,
            }
    
    def clear_all(self) -> None:
        """Clear all events from database (use with caution!)"""
        with self._conn() as c:
            c.execute("DELETE FROM events")
            c.commit()