from __future__ import annotations
from core.models import NewsItem

class ConsoleNotifier:
    def notify(self, item: NewsItem) -> None:
        print("\n" + "=" * 100)
        print(f"SOURCE: {item.source}")
        print(f"TICKER: {item.ticker or 'N/A'}")
        print(f"SCORE : {item.impact_score}  ({item.impact_reason})")
        print(f"VALID : {item.validated}  ({item.validation_reason})")
        if item.gap_pct is not None:
            print(f"GAP   : {item.gap_pct:.2f}%")
        if item.vol_spike is not None:
            print(f"VOLx  : {item.vol_spike:.2f}x")
        print(f"TIME  : {item.published}")
        print(f"TITLE : {item.title}")
        print(f"LINK  : {item.link}")
