from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict
import requests

OUT_PATH = Path("data/company_to_ticker.json")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


def normalize_company_name(name: str) -> str:
    if not name:
        return ""

    name = name.lower().strip()
    name = name.replace("&", " and ")

    # keep letters/numbers/spaces
    name = re.sub(r"[^\w\s]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    stop = {
        "inc", "incorporated", "corp", "corporation", "ltd", "limited",
        "plc", "co", "company", "holdings", "holding", "group",
        "class", "ordinary", "shares", "common", "stock", "the",
    }

    parts = [p for p in name.split() if p not in stop and len(p) > 1]
    return " ".join(parts).strip()


def fetch_sp500() -> Dict[str, str]:
    """
    Wikipedia table: Symbol + Security.
    FIX: download HTML with requests+headers to avoid 403, then pandas.read_html(html).
    """
    try:
        import pandas as pd  # noqa
    except ImportError as e:
        raise RuntimeError("Need pandas + lxml/html5lib. Run: pip install pandas lxml html5lib") from e

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    r = requests.get(url, headers=HEADERS, timeout=40)
    r.raise_for_status()

    # Read tables from HTML string (not URL) -> avoids 403 from pandas/urllib
    tables = pd.read_html(r.text)
    df = tables[0]

    out: Dict[str, str] = {}
    for _, row in df.iterrows():
        symbol = str(row["Symbol"]).strip().upper().replace(".", "-")
        name = str(row["Security"]).strip()

        if not symbol or not name:
            continue

        norm = normalize_company_name(name)
        if norm:
            out[norm] = symbol

        # extra variants (some titles omit punctuation)
        norm2 = normalize_company_name(name.replace(",", " "))
        if norm2:
            out[norm2] = symbol

    return out


def fetch_nasdaq_listed() -> Dict[str, str]:
    """
    Try NASDAQ screener API first (may block bots).
    Fallback: nasdaqtrader listed file (official).
    """
    try:
        return _fetch_nasdaq_from_api()
    except Exception as e:
        print(f"  ⚠️ NASDAQ API failed: {e} -> trying nasdaqtrader file...")
        return _fetch_nasdaq_from_trader_file()

def _fetch_nasdaq_from_api() -> Dict[str, str]:
    url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&exchange=nasdaq"

    session = requests.Session()
    headers = dict(HEADERS)
    headers.update({
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.nasdaq.com/",
        "Origin": "https://www.nasdaq.com",
    })

    r = session.get(url, headers=headers, timeout=40)
    r.raise_for_status()

    # Sometimes it returns HTML even with 200
    ct = (r.headers.get("Content-Type") or "").lower()
    if "json" not in ct:
        raise RuntimeError(f"Expected JSON but got Content-Type={ct}")

    data = r.json()
    rows = data.get("data", {}).get("rows", [])
    if not rows:
        raise RuntimeError("NASDAQ API returned 0 rows (blocked or empty response)")

    out: Dict[str, str] = {}
    for row in rows:
        symbol = (row.get("symbol") or "").strip().upper()
        name = (row.get("name") or "").strip()
        if not symbol or not name:
            continue

        norm = normalize_company_name(name)
        if norm:
            out[norm] = symbol

    return out

def _fetch_nasdaq_from_trader_file() -> Dict[str, str]:
    """
    Official NASDAQ Trader file (listed NASDAQ symbols).
    Note: this file includes symbol + security name.
    """
    url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"

    r = requests.get(url, headers=HEADERS, timeout=40)
    r.raise_for_status()

    lines = r.text.splitlines()
    if len(lines) < 5:
        raise RuntimeError("nasdaqlisted.txt looks empty/unexpected")

    out: Dict[str, str] = {}
    # format: Symbol|Security Name|Market Category|...
    for line in lines[1:]:
        if line.startswith("File Creation Time"):
            break
        parts = line.split("|")
        if len(parts) < 2:
            continue

        symbol = parts[0].strip().upper()
        name = parts[1].strip()

        if not symbol or not name:
            continue

        norm = normalize_company_name(name)
        if norm:
            out[norm] = symbol

    if not out:
        raise RuntimeError("nasdaqlisted.txt parsed but produced 0 mappings")

    return out
    
def merge_maps(primary: Dict[str, str], secondary: Dict[str, str]) -> Dict[str, str]:
    """
    Merge by keeping primary first when conflicts exist.
    """
    merged = dict(primary)
    for k, v in secondary.items():
        merged.setdefault(k, v)
    return merged


def main() -> None:
    print("Fetching S&P 500 (Wikipedia)...")
    sp = fetch_sp500()
    print(f"  ✅ S&P 500 mappings: {len(sp)}")

    print("Fetching NASDAQ listed (Nasdaq API)...")
    nas = fetch_nasdaq_listed()
    print(f"  ✅ NASDAQ mappings: {len(nas)}")

    merged = merge_maps(sp, nas)

    OUT_PATH.write_text(
        json.dumps(merged, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n✅ Saved {len(merged)} company→ticker mappings to {OUT_PATH}")


if __name__ == "__main__":
    main()
