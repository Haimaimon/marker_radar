from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Protocol

@dataclass
class MarketSnapshot:
    symbol: str
    price: Optional[float]
    prev_close: Optional[float]
    volume: Optional[float]
    avg_volume_10d: Optional[float]

class MarketDataProvider(Protocol):
    def get_snapshot(self, symbol: str) -> MarketSnapshot: ...
