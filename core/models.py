from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class NewsItem(BaseModel):
    source: str
    title: str
    link: str
    published: str = ""
    summary: str = ""

    # Enrichment
    ticker: Optional[str] = None
    impact_score: int = 0
    impact_reason: str = ""

    # Validation
    gap_pct: Optional[float] = None
    vol_spike: Optional[float] = None
    validated: bool = False
    validation_reason: str = ""

    uid: str = Field(default="", description="Dedup hash")
    raw: Dict[str, Any] = Field(default_factory=dict)
