from __future__ import annotations
from typing import Protocol, List
from core.models import NewsItem

class Collector(Protocol):
    def fetch(self) -> List[NewsItem]: ...
