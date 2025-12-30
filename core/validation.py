from __future__ import annotations
from typing import Tuple
from market_data.base import MarketDataProvider
from core.models import NewsItem

def validate_market_impact(
    item: NewsItem,
    md: MarketDataProvider,
    min_gap_pct: float,
    min_vol_spike: float,
) -> Tuple[bool, str]:
    """
    Validates that the market is reacting:
    - gap_pct = (price - prev_close)/prev_close * 100
    - vol_spike = volume / avg_volume_10d
    """
    if not item.ticker:
        return False, "no-ticker"

    snap = md.get_snapshot(item.ticker)
    if snap.price is None or snap.prev_close is None or snap.prev_close == 0:
        return False, "no-price-or-prev-close"

    gap_pct = ((snap.price - snap.prev_close) / snap.prev_close) * 100.0
    item.gap_pct = gap_pct

    vol_spike = None
    if snap.volume is not None and snap.avg_volume_10d is not None and snap.avg_volume_10d > 0:
        vol_spike = snap.volume / snap.avg_volume_10d
    item.vol_spike = vol_spike

    # Rules
    gap_ok = abs(gap_pct) >= min_gap_pct
    vol_ok = (vol_spike is not None) and (vol_spike >= min_vol_spike)

    if gap_ok and vol_ok:
        return True, f"gap={gap_pct:.2f}% vol_spike={vol_spike:.2f}x"
    if gap_ok:
        return True, f"gap={gap_pct:.2f}% (vol not confirmed)"
    if vol_ok:
        return True, f"vol_spike={vol_spike:.2f}x (gap not confirmed)"

    return False, f"weak reaction gap={gap_pct:.2f}% vol_spike={vol_spike if vol_spike else 'n/a'}"
