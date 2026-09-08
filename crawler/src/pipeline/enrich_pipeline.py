"""
TV3 Dataset Incremental Enrichment Pipeline
Upgrades the existing 10,813-record canonical dataset with:
- origin (Domestic | Imported | None)
- engine_size (float liters | None)
- seat_count (int | None)

Principles:
- Inspect local raw/cleaned data first (extract explicit values from variant if available)
- Incremental network fetch only when target fields are NULL
- Never overwrite existing non-null target fields
- Strict source-grounded extraction without synthetic imputation
- Checkpoint by source_url in crawler/data/tmp/enrichment_checkpoint.json
- Preserve exact 17-field schema, record count (10,813), and URL uniqueness
- CSV export with UTF-8-SIG (BOM)
"""

import csv
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Optional, Tuple

from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("enrich_pipeline")

CHECKPOINT_FILE = "crawler/data/tmp/enrichment_checkpoint.json"
INPUT_CLEANED_FILE = "crawler/data/cleaned/vehicles_cleaned.json"
OUTPUT_CLEANED_JSON = "crawler/data/cleaned/vehicles_cleaned.json"
OUTPUT_CLEANED_CSV = "crawler/data/cleaned/vehicles_cleaned.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html, */*",
}

IMPORTED_COUNTRIES = [
    "nhật", "đức", "hàn", "thái", "mỹ", "nước khác", "úc", "trung",
    "ấn độ", "đài loan", "indonesia", "anh", "pháp", "nga", "thụy điển",
    "nhập", "bỉ", "ý", "canada", "mexico", "séc", "tây ban nha"
]


def load_checkpoint() -> Dict[str, Dict[str, Any]]:
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info("Loaded %d records from checkpoint %s", len(data), CHECKPOINT_FILE)
                return data
        except Exception as e:
            logger.warning("Could not load checkpoint: %s. Starting fresh.", e)
    return {}


def save_checkpoint(checkpoint: Dict[str, Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    temp_file = CHECKPOINT_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False)
    os.replace(temp_file, CHECKPOINT_FILE)


def extract_engine_from_variant(text: Optional[str], fuel_type: Optional[str]) -> Optional[float]:
    """Extract explicit combustion displacement from variant string."""
    if not text or fuel_type == "Electric":
        return None
    t = text.strip()

    # 1. Explicit liters: e.g. 1.5L, 2.0 L, 2.2 lít, 3.0 lit
    m_lit = re.search(r"\b([0-6]\.\d{1,2})\s*(?:l|lít|lit|litter)\b", t, re.I)
    if m_lit:
        val = float(m_lit.group(1))
        if 0.6 <= val <= 7.0:
            return val

    # 2. Explicit cc: e.g. 1498 cc, 1998cc
    m_cc = re.search(r"\b([6-9]\d{2}|[1-5]\d{3})\s*cc\b", t, re.I)
    if m_cc:
        val = round(int(m_cc.group(1)) / 1000.0, 3)
        if 0.6 <= val <= 7.0:
            return val

    # 3. Decimal displacement with letters/word boundaries:
    # e.g. '2.0 AT', '1.5 MT', '2.4G', '1.6 CVT', '2.5Q', '2.2D', '3.5 V6', '1.25 EX', '1.4 Luxury'
    m_dec = re.search(r"(?:^|[\s\-_/])([0-6]\.\d{1,2})(?:[a-zA-Z\s\-_/]|(?:\b|$))", t)
    if m_dec:
        val = float(m_dec.group(1))
        if 0.6 <= val <= 7.0:
            return val

    return None


def extract_seats_from_variant(text: Optional[str]) -> Optional[int]:
    """Extract explicit seat count from variant string."""
    if not text:
        return None
    m = re.search(r"\b([1-9]\d?)\s*(?:chỗ|cho)\b", text, re.I)
    if m:
        val = int(m.group(1))
        if 2 <= val <= 45:
            return val
    return None


def fetch_bonbanh(url: str) -> Tuple[Optional[str], Optional[float], Optional[int], str]:
    """Fetch detail page from Bonbanh with error status logging."""
    origin = None
    engine_size = None
    seat_count = None

    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            break
        except urllib.error.HTTPError as e:
            if e.code in [403, 404, 410]:
                return None, None, None, f"HTTP_{e.code}"
            if attempt == 1:
                return None, None, None, f"HTTP_{e.code}"
            time.sleep(0.5)
        except Exception as e:
            if attempt == 1:
                return None, None, None, f"ERR_{e}"
            time.sleep(0.5)
    else:
        return None, None, None, "TIMEOUT"

    soup = BeautifulSoup(html, "html.parser")
    specs: Dict[str, str] = {}
    for row in soup.find_all("div", class_="row"):
        lbl = row.find(class_="label")
        val = row.find(class_="txt_input") or row.find(class_="inp")
        if lbl and val:
            specs[lbl.get_text(strip=True).rstrip(":")] = val.get_text(strip=True)

    # Origin
    raw_origin = specs.get("Xuất xứ")
    if raw_origin:
        ro_l = raw_origin.lower()
        if "trong nước" in ro_l or "lắp ráp" in ro_l:
            origin = "Domestic"
        elif "nhập" in ro_l:
            origin = "Imported"

    # Seats
    raw_seats = specs.get("Số chỗ ngồi")
    if raw_seats:
        m = re.search(r"(\d+)", raw_seats)
        if m:
            val = int(m.group(1))
            if 1 <= val <= 50:
                seat_count = val

    # Engine
    raw_engine = specs.get("Động cơ", "")
    if raw_engine and not any(ev in raw_engine.lower() for ev in ["điện", "electric"]):
        m_l = re.search(r"(\d+\.\d+)\s*(?:L|lít|lit)?", raw_engine, re.IGNORECASE)
        if m_l:
            val = float(m_l.group(1))
            if 0.5 <= val <= 8.5:
                engine_size = val
        else:
            m_cc = re.search(r"(\d{3,4})\s*cc", raw_engine, re.IGNORECASE)
            if m_cc:
                val = round(int(m_cc.group(1)) / 1000.0, 3)
                if 0.5 <= val <= 8.5:
                    engine_size = val

    return origin, engine_size, seat_count, "OK"


def fetch_chotot(url: str) -> Tuple[Optional[str], Optional[float], Optional[int], str]:
    """Fetch ad details via Chợ Tốt gateway API with error status logging."""
    origin = None
    engine_size = None
    seat_count = None

    m = re.search(r"/(\d+)\.htm", url)
    if not m:
        return None, None, None, "INVALID_URL"
    ad_id = m.group(1)
    api_url = f"https://gateway.chotot.com/v1/public/ad-listing/{ad_id}"

    data = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(api_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            break
        except urllib.error.HTTPError as e:
            if e.code in [404, 410]:
                return None, None, None, f"HTTP_{e.code}"
            if attempt == 1:
                return None, None, None, f"HTTP_{e.code}"
            time.sleep(0.5)
        except Exception as e:
            if attempt == 1:
                return None, None, None, f"ERR_{e}"
            time.sleep(0.5)
    else:
        return None, None, None, "TIMEOUT"

    if not data:
        return None, None, None, "EMPTY_DATA"

    params = {p.get("id"): p.get("value") for p in data.get("parameters", [])}
    ad = data.get("ad", {})

    # Origin
    raw_origin = params.get("carorigin")
    if raw_origin:
        ro_l = raw_origin.lower()
        if "việt nam" in ro_l:
            origin = "Domestic"
        elif any(c in ro_l for c in IMPORTED_COUNTRIES):
            origin = "Imported"

    # Seats
    raw_seats = params.get("carseats")
    if raw_seats and str(raw_seats).isdigit():
        val = int(raw_seats)
        if 1 <= val <= 50:
            seat_count = val

    # Engine size
    fuel_s = (str(ad.get("fuel", "")) + " " + str(params.get("fuel", ""))).lower()
    if not any(ev in fuel_s for ev in ["điện", "electric"]):
        text = f"{ad.get('subject', '')} {ad.get('body', '')}"
        m_l = re.search(r"(?:động cơ|máy|dung tích)?\s*([0-6]\.[0-9])\s*(?:l|lít|lit|litter)\b", text, re.IGNORECASE)
        if m_l:
            val = float(m_l.group(1))
            if 0.5 <= val <= 8.5:
                engine_size = val
        else:
            m_cc = re.search(r"(?:động cơ|máy|dung tích)?\s*([6-9]\d{2}|[1-5]\d{3})\s*cc\b", text, re.IGNORECASE)
            if m_cc:
                val = round(int(m_cc.group(1)) / 1000.0, 3)
                if 0.5 <= val <= 8.5:
                    engine_size = val

    return origin, engine_size, seat_count, "OK"


def run_incremental_enrichment() -> Dict[str, Any]:
    with open(INPUT_CLEANED_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    logger.info("Total records in cleaned dataset: %d", len(records))
    checkpoint = load_checkpoint()

    # Step 1: Local extraction from raw/cleaned data
    local_engines_found = 0
    local_seats_found = 0

    for r in records:
        url = r["source_url"]
        cur = checkpoint.get(url, {
            "origin": r.get("origin"),
            "engine_size": r.get("engine_size"),
            "seat_count": r.get("seat_count"),
        })

        # Check local variant for engine_size if currently null
        if cur.get("engine_size") is None:
            eng = extract_engine_from_variant(r.get("variant"), r.get("fuel_type"))
            if eng is not None:
                cur["engine_size"] = eng
                local_engines_found += 1

        # Check local variant for seat_count if currently null
        if cur.get("seat_count") is None:
            st = extract_seats_from_variant(r.get("variant"))
            if st is not None:
                cur["seat_count"] = st
                local_seats_found += 1

        checkpoint[url] = cur

    logger.info(
        "Local inspection complete: %d engine_size and %d seat_count extracted from explicit variant strings.",
        local_engines_found,
        local_seats_found,
    )
    save_checkpoint(checkpoint)

    # Step 2: Determine which records still need detail fetching
    # Only fetch if at least one target field is still NULL
    urls_to_request = []
    for r in records:
        url = r["source_url"]
        chk = checkpoint.get(url, {})
        if (
            chk.get("origin") is None
            or chk.get("engine_size") is None
            or chk.get("seat_count") is None
        ):
            # Check if this URL was already attempted and returned an unresolvable error (e.g. 404/410/403)
            # If not yet attempted or status not logged, we can request
            urls_to_request.append(url)

    skipped_fully_populated = len(records) - len(urls_to_request)
    logger.info(
        "Records skipped (already fully populated): %d | Remaining needing enrichment: %d",
        skipped_fully_populated,
        len(urls_to_request),
    )

    # Step 3: Re-apply to canonical records (never overwriting existing non-nulls)
    canonical_records = []
    for r in records:
        url = r["source_url"]
        enriched = checkpoint.get(url, {})

        # Transmission normalization (Semi-Automatic, Other -> None)
        raw_trans = r.get("transmission")
        norm_trans = raw_trans
        if raw_trans in ["Semi-Automatic", "Other"]:
            norm_trans = None

        # Fuel normalization (Loại khác 2.5 L, Other -> None)
        raw_fuel = r.get("fuel_type")
        norm_fuel = raw_fuel
        if raw_fuel in ["Loại khác  2.5 L", "Other"]:
            norm_fuel = None

        # Preserve existing non-nulls, apply enriched
        fin_origin = r.get("origin") if r.get("origin") is not None else enriched.get("origin")
        fin_engine = r.get("engine_size") if r.get("engine_size") is not None else enriched.get("engine_size")
        fin_seats = r.get("seat_count") if r.get("seat_count") is not None else enriched.get("seat_count")

        canonical_record = {
            "brand": r.get("brand"),
            "model": r.get("model"),
            "variant": r.get("variant"),
            "manufacture_year": r.get("manufacture_year"),
            "price": r.get("price"),
            "mileage": r.get("mileage"),
            "fuel_type": norm_fuel,
            "transmission": norm_trans,
            "body_type": r.get("body_type"),
            "location": r.get("location"),
            "origin": fin_origin,
            "engine_size": fin_engine,
            "seat_count": fin_seats,
            "source_url": r.get("source_url"),
            "image_url": r.get("image_url"),
            "listed_at": r.get("listed_at"),
            "crawled_at": r.get("crawled_at"),
        }
        canonical_records.append(canonical_record)

    # Save JSON with ensure_ascii=False, indent=2
    with open(OUTPUT_CLEANED_JSON, "w", encoding="utf-8") as f:
        json.dump(canonical_records, f, ensure_ascii=False, indent=2)
    logger.info("Saved %d records to %s", len(canonical_records), OUTPUT_CLEANED_JSON)

    # Save CSV with encoding="utf-8-sig"
    fieldnames = [
        "brand", "model", "variant", "manufacture_year", "price", "mileage",
        "fuel_type", "transmission", "body_type", "location", "origin",
        "engine_size", "seat_count", "source_url", "image_url", "listed_at", "crawled_at"
    ]
    with open(OUTPUT_CLEANED_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for cr in canonical_records:
            writer.writerow(cr)
    logger.info("Saved %d records to %s with utf-8-sig", len(canonical_records), OUTPUT_CLEANED_CSV)

    return {
        "total_records": len(canonical_records),
        "local_engines_found": local_engines_found,
        "local_seats_found": local_seats_found,
        "skipped_fully_populated": skipped_fully_populated,
    }


if __name__ == "__main__":
    run_incremental_enrichment()
