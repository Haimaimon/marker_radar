from __future__ import annotations
from typing import Protocol
from core.models import NewsItem

class Notifier(Protocol):
    def notify(self, item: NewsItem) -> None: ...
