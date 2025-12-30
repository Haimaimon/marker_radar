from __future__ import annotations
from typing import Tuple

KEYWORDS = {
    # M&A
    "merger": 35, "acquisition": 35, "acquire": 25, "definitive agreement": 35,
    "tender offer": 35, "s-4": 40, "business combination": 30,

    # Clinical / biotech
    "phase 3": 35, "phase iii": 35, "phase 2": 25, "phase ii": 25,
    "topline": 30, "primary endpoint": 35, "met its primary endpoint": 45,
    "statistically significant": 30, "fda approval": 45, "fda accepts": 35,
    "nda": 25, "bla": 25, "pdufa": 25, "fast track": 20, "breakthrough therapy": 25,

    # Material / risk
    "bankruptcy": 45, "going concern": 30, "restatement": 30,
    "investigation": 25, "8-k": 30,

    # Dilution
    "public offering": 30, "registered direct offering": 35, "atm offering": 25,
    "convertible notes": 25, "dilution": 25,
}

SOURCE_BONUS = {
    "SEC EDGAR": 25,
    "GlobeNewswire": 10,
    "PR Newswire": 10,
    "Business Wire": 10,
}

def score(source: str, title: str, summary: str) -> Tuple[int, str]:
    text = f"{title} {summary}".lower()
    score_val = SOURCE_BONUS.get(source, 0)
    hits = []

    for k, w in KEYWORDS.items():
        if k in text:
            score_val += w
            hits.append(k)

    score_val = min(score_val, 100)
    reason = ", ".join(hits[:8]) if hits else "no-keyword-hit"
    return score_val, reason
