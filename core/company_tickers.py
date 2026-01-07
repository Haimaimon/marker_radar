"""
Company Name to Ticker Symbol Mapping

High-quality database of company names → ticker symbols
Supports fuzzy matching, aliases, and common variations
"""

from __future__ import annotations
from typing import Dict, Set

# Primary mapping: normalized company name → ticker
# Key format: lowercase, no punctuation, no "inc", "corp", etc.
COMPANY_TO_TICKER: Dict[str, str] = {
    # FAANG / Mag 7
    "apple": "AAPL",
    "amazon": "AMZN",
    "alphabet": "GOOGL",
    "google": "GOOGL",
    "microsoft": "MSFT",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",
    "nvidia": "NVDA",
    "tesla": "TSLA",

    # Other Tech Giants
    "adobe": "ADBE",
    "salesforce": "CRM",
    "oracle": "ORCL",
    "ibm": "IBM",
    "intel": "INTC",
    "amd": "AMD",
    "qualcomm": "QCOM",
    "cisco": "CSCO",
    "broadcom": "AVGO",
    "texas instruments": "TXN",
    "micron": "MU",
    "applied materials": "AMAT",
    "servicenow": "NOW",
    "workday": "WDAY",
    "snowflake": "SNOW",
    "datadog": "DDOG",
    "crowdstrike": "CRWD",
    "palantir": "PLTR",
    "shopify": "SHOP",
    "square": "SQ",
    "block": "SQ",
    "paypal": "PYPL",
    "uber": "UBER",
    "lyft": "LYFT",
    "doordash": "DASH",
    "airbnb": "ABNB",
    "zoom": "ZM",
    "slack": "WORK",
    "twilio": "TWLO",
    "okta": "OKTA",
    "mongodb": "MDB",
    "elastic": "ESTC",
    "confluent": "CFLT",
    "unity": "U",
    "roblox": "RBLX",

    # Semiconductors
    "asml": "ASML",
    "taiwan semiconductor": "TSM",
    "tsmc": "TSM",
    "arm": "ARM",
    "marvell": "MRVL",
    "analog devices": "ADI",
    "nxp": "NXPI",
    "microchip": "MCHP",
    "on semiconductor": "ON",
    "skyworks": "SWKS",
    "qorvo": "QRVO",

    # Cloud/SaaS
    "aws": "AMZN",
    "azure": "MSFT",
    "gcp": "GOOGL",

    # Finance
    "jpmorgan": "JPM",
    "jp morgan": "JPM",
    "bank of america": "BAC",
    "wells fargo": "WFC",
    "citigroup": "C",
    "goldman sachs": "GS",
    "morgan stanley": "MS",
    "blackrock": "BLK",
    "visa": "V",
    "mastercard": "MA",
    "american express": "AXP",
    "amex": "AXP",
    "coinbase": "COIN",
    "robinhood": "HOOD",

    # Retail/Consumer
    "walmart": "WMT",
    "target": "TGT",
    "costco": "COST",
    "home depot": "HD",
    "lowes": "LOW",
    "nike": "NKE",
    "adidas": "ADDYY",
    "starbucks": "SBUX",
    "mcdonalds": "MCD",
    "chipotle": "CMG",
    "yum brands": "YUM",

    # Healthcare/Pharma
    "johnson & johnson": "JNJ",
    "johnson and johnson": "JNJ",
    "pfizer": "PFE",
    "moderna": "MRNA",
    "merck": "MRK",
    "abbvie": "ABBV",
    "eli lilly": "LLY",
    "bristol myers": "BMY",
    "amgen": "AMGN",
    "gilead": "GILD",
    "regeneron": "REGN",
    "biogen": "BIIB",
    "vertex": "VRTX",
    "illumina": "ILMN",
    "dexcom": "DXCM",
    "intuitive surgical": "ISRG",
    "edwards lifesciences": "EW",
    "boston scientific": "BSX",
    "medtronic": "MDT",
    "abbott": "ABT",
    "thermo fisher": "TMO",
    "danaher": "DHR",
    
    # ✅ NEW: GSK mapping (your case)
    "glaxo smith kline": "GSK",
    # =========================
    # Healthcare / Medical Imaging
    # =========================
    "radnet": "RDNT",
    "rad net": "RDNT",
    "radnet inc": "RDNT",

    "envision healthcare": "EHC",
    "mednax": "MD",
    "us radiology specialists": "USRS",
    "akumin": "AKU",
    "lucidhealth": "LUCID",
    "rayus radiology": "RAYUS",

    # =========================
    # Healthcare Providers / Hospitals
    # =========================
    "hca healthcare": "HCA",
    "tenet healthcare": "THC",
    "community health systems": "CYH",
    "universal health services": "UHS",
    "select medical": "SEM",
    "lifepoint health": "LPNT",

    # =========================
    # Medical Devices
    # =========================
    "ge healthcare": "GEHC",
    "siemens healthineers": "SHL",
    "philips healthcare": "PHG",
    "stryker": "SYK",
    "zimmer biomet": "ZBH",
    "becton dickinson": "BDX",
    "boston scientific": "BSX",
    "medtronic": "MDT",
    "abbott laboratories": "ABT",
    "edwards lifesciences": "EW",

    # =========================
    # Pharma / Biotech (common in press releases)
    # =========================
    "glaxosmithkline": "GSK",
    "gsk": "GSK",
    "sanofi": "SNY",
    "astrazeneca": "AZN",
    "novartis": "NVS",
    "roche": "RHHBY",
    "takeda": "TAK",
    "bayer": "BAYRY",
    "pfizer": "PFE",
    "eli lilly": "LLY",
    "bristol myers squibb": "BMY",
    "merck": "MRK",
    "abbvie": "ABBV",
    "gilead sciences": "GILD",
    "vertex pharmaceuticals": "VRTX",
    "regeneron pharmaceuticals": "REGN",
    "biogen": "BIIB",

    # =========================
    # Small / Mid-cap Biotech (high-impact news)
    # =========================
    "ionis pharmaceuticals": "IONS",
    "alnylam pharmaceuticals": "ALNY",
    "bluebird bio": "BLUE",
    "sarepta therapeutics": "SRPT",
    "crispr therapeutics": "CRSP",
    "beam therapeutics": "BEAM",
    "intellia therapeutics": "NTLA",
    "editas medicine": "EDIT",
    "moderna": "MRNA",
    "biontech": "BNTX",

    # Automotive
    "ford": "F",
    "general motors": "GM",
    "gm": "GM",
    "stellantis": "STLA",
    "rivian": "RIVN",
    "lucid": "LCID",
    "nio": "NIO",
    "xpeng": "XPEV",
    "li auto": "LI",

    # Energy
    "exxon": "XOM",
    "exxonmobil": "XOM",
    "chevron": "CVX",
    "conocophillips": "COP",
    "schlumberger": "SLB",
    "halliburton": "HAL",
    "occidental": "OXY",
    "marathon": "MRO",
    "enphase": "ENPH",
    "solaredge": "SEDG",
    "first solar": "FSLR",
    "plug power": "PLUG",
    "bloom energy": "BE",

    # Aerospace/Defense
    "boeing": "BA",
    "lockheed martin": "LMT",
    "northrop grumman": "NOC",
    "raytheon": "RTX",
    "general dynamics": "GD",

    # Telecom/Media
    "att": "T",
    "at&t": "T",
    "verizon": "VZ",
    "t-mobile": "TMUS",
    "tmobile": "TMUS",
    "comcast": "CMCSA",
    "disney": "DIS",
    "spotify": "SPOT",
    "roku": "ROKU",

    # E-commerce/Marketplace
    "ebay": "EBAY",
    "etsy": "ETSY",
    "wayfair": "W",
    "chewy": "CHWY",
    "carvana": "CVNA",

    # Gaming
    "electronic arts": "EA",
    "ea": "EA",
    "take-two": "TTWO",

    # Crypto-related
    "microstrategy": "MSTR",
    "marathon digital": "MARA",
    "riot platforms": "RIOT",

    # Chinese ADRs
    "alibaba": "BABA",
    "jd.com": "JD",
    "jd": "JD",
    "baidu": "BIDU",

    # Other Notable
    "berkshire hathaway": "BRK.B",
    "berkshire": "BRK.B",
    "3m": "MMM",
    "caterpillar": "CAT",
    "deere": "DE",
    "honeywell": "HON",
    "ge": "GE",
    "general electric": "GE",
    "fedex": "FDX",
    "ups": "UPS",
}

# Aliases: alternative names that map to the same ticker
ALIASES: Dict[str, str] = {
    "msft": "MSFT",
    "aapl": "AAPL",
    "amzn": "AMZN",
    "googl": "GOOGL",
    "goog": "GOOGL",
    "fb": "META",
    "nflx": "NFLX",
    "nvda": "NVDA",
    "tsla": "TSLA",

    # Common abbreviations
    "aws": "AMZN",
    "jnj": "JNJ",
    "bac": "BAC",
    "bofa": "BAC",
    "jpmorgan chase": "JPM",

    # Brand variations
    "meta platforms": "META",
    "alphabet inc": "GOOGL",
    "amazon.com": "AMZN",
    "amazon web services": "AMZN",

    # ✅ NEW: GSK aliases
    "gsk plc": "GSK",
    "glaxosmithkline plc": "GSK",

    # Common misspellings
    "appl": "AAPL",
    "microsft": "MSFT",
    "amazn": "AMZN",
    "tesela": "TSLA",
}

# Words to remove when normalizing company names
STOP_WORDS: Set[str] = {
    "inc", "incorporated", "corp", "corporation", "ltd", "limited",
    "company", "co", "plc", "group", "holdings", "holding",
    "technologies", "technology", "tech", "systems", "solutions",
    "the", "a", "an", "&", "and",
}

# Common false positives to exclude
BLACKLIST: Set[str] = {
    "usa", "us", "ceo", "cfo", "cto", "cio",
    "ipo", "etf", "esg", "ai", "ml", "api",
    "sec", "fda", "fcc", "ftc", "doj",
    "nft", "nfts", "pr", "hr", "it", "rd",
    "q1", "q2", "q3", "q4", "fy",
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec",
    "monday", "tuesday", "wednesday", "thursday", "friday",
    "nyse", "nasdaq", "amex", "otc",
}

def normalize_company_name(name: str) -> str:
    """
    Normalize a company name for matching.

    - Convert to lowercase
    - Remove punctuation
    - Remove common suffixes (Inc, Corp, etc.)
    - Strip whitespace
    """
    if not name:
        return ""

    name = name.lower()

    import string
    for char in string.punctuation:
        name = name.replace(char, " ")

    words = name.split()
    filtered = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    return " ".join(filtered)

def get_all_tickers() -> Set[str]:
    """Get set of all known ticker symbols."""
    tickers = set(COMPANY_TO_TICKER.values())
    tickers.update(ALIASES.values())
    return tickers

def get_company_names() -> Set[str]:
    """Get set of all known company names."""
    return set(COMPANY_TO_TICKER.keys())
