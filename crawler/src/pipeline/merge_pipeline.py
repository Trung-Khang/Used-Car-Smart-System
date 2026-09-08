"""
Merge Pipeline - Phase 3: Combine Production Raw Data

Merges raw records from multiple sources (Chotot, Bonbanh) into a single canonical
merged raw dataset while preserving exact raw values and full source traceability.

Author: TV3 — Data Engineering / Data Pipeline Developer
Project: Used-Car-Smart-System
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

# Canonical 14-field schema contract
CANONICAL_FIELDS = [
    "brand",
    "model",
    "variant",
    "manufacture_year",
    "price",
    "mileage",
    "fuel_type",
    "transmission",
    "body_type",
    "location",
    "source_url",
    "image_url",
    "listed_at",
    "crawled_at",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("merge_pipeline")


def natural_sort_key(s: str):
    """Sort strings containing numbers naturally (batch1, batch2, ... batch10)."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", str(s))]


def discover_production_raw_files(raw_dir: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Discovers all production raw JSON files in raw_dir.
    Separates into chotot production files, bonbanh production files, and excluded files (e.g. smoke tests).
    """
    chotot_files = []
    bonbanh_files = []
    excluded_files = []

    all_json = list(raw_dir.glob("*.json"))
    for file_path in all_json:
        name = file_path.name
        # Match production batches: *_raw_production_batch*.json
        if "chotot_raw_production" in name:
            chotot_files.append(file_path)
        elif "bonbanh_raw_production" in name:
            bonbanh_files.append(file_path)
        else:
            # Smoke tests or other files, e.g. *_raw_20260907_*.json
            excluded_files.append(file_path)

    chotot_files.sort(key=lambda p: natural_sort_key(p.name))
    bonbanh_files.sort(key=lambda p: natural_sort_key(p.name))
    excluded_files.sort(key=lambda p: natural_sort_key(p.name))

    return chotot_files, bonbanh_files, excluded_files


def identify_source_from_url(url: Optional[str]) -> str:
    """Identify source origin based on source_url."""
    if not url:
        return "unknown"
    domain = urlparse(url).netloc.lower()
    if "chotot" in domain:
        return "chotot"
    elif "bonbanh" in domain:
        return "bonbanh"
    return "unknown"


def validate_record_schema(record: dict, record_idx: int, file_name: str) -> Tuple[bool, List[str]]:
    """
    Validates that a record contains exactly the 14 canonical fields.
    Does NOT modify or clean any values.
    """
    missing = [f for f in CANONICAL_FIELDS if f not in record]
    extra = [f for f in record.keys() if f not in CANONICAL_FIELDS]
    errors = []
    if missing:
        errors.append(f"Missing fields: {missing}")
    if extra:
        errors.append(f"Unexpected extra fields: {extra}")
    return len(errors) == 0, errors


def load_and_merge_datasets(
    raw_dir: Path,
) -> Tuple[List[dict], dict]:
    """
    Loads Chợ Tốt and Bonbanh production files, validates schema, deduplicates by exact source_url,
    and returns the merged records and an audit metadata dict.
    """
    chotot_files, bonbanh_files, excluded_files = discover_production_raw_files(raw_dir)

    logger.info("Found %d Chotot production files", len(chotot_files))
    for f in chotot_files:
        logger.info("  Chotot batch: %s", f.name)

    logger.info("Found %d Bonbanh production files", len(bonbanh_files))
    for f in bonbanh_files:
        logger.info("  Bonbanh batch: %s", f.name)

    logger.info("Excluded %d files (smoke tests / non-production):", len(excluded_files))
    for f in excluded_files:
        logger.info("  Excluded: %s", f.name)

    stats = {
        "chotot_files": [f.name for f in chotot_files],
        "bonbanh_files": [f.name for f in bonbanh_files],
        "excluded_files": [f.name for f in excluded_files],
        "files_loaded": {},
        "total_records_read": 0,
        "chotot_records_read": 0,
        "bonbanh_records_read": 0,
        "schema_errors": 0,
        "duplicate_urls_removed": 0,
        "duplicate_records_detail": [],
        "final_merged_records": 0,
        "final_chotot_records": 0,
        "final_bonbanh_records": 0,
    }

    seen_urls: Set[str] = set()
    merged_records: List[dict] = []

    # Processing helper
    def process_file_list(files: List[Path], source_label: str):
        count_read = 0
        for fpath in files:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                logger.error("Failed to load %s: %s", fpath.name, e)
                raise

            if not isinstance(data, list):
                raise ValueError(f"File {fpath.name} does not contain a JSON array.")

            file_record_count = len(data)
            stats["files_loaded"][fpath.name] = file_record_count
            count_read += file_record_count

            for idx, rec in enumerate(data):
                is_valid, errs = validate_record_schema(rec, idx, fpath.name)
                if not is_valid:
                    stats["schema_errors"] += 1
                    logger.warning("Schema violation in %s rec #%d: %s", fpath.name, idx, errs)

                # Preserve exact values in canonical field order
                ordered_rec = {field: rec.get(field, None) for field in CANONICAL_FIELDS}

                url = ordered_rec.get("source_url")
                if not url:
                    logger.warning("Empty source_url in %s record #%d", fpath.name, idx)
                    merged_records.append(ordered_rec)
                    continue

                if url in seen_urls:
                    stats["duplicate_urls_removed"] += 1
                    stats["duplicate_records_detail"].append({
                        "file": fpath.name,
                        "source_url": url,
                    })
                    logger.warning("Duplicate source_url found in %s: %s (Skipping)", fpath.name, url)
                else:
                    seen_urls.add(url)
                    merged_records.append(ordered_rec)
                    if source_label == "chotot":
                        stats["final_chotot_records"] += 1
                    elif source_label == "bonbanh":
                        stats["final_bonbanh_records"] += 1

        return count_read

    # 1. Process Chợ Tốt files first in batch order
    logger.info("--- Processing Chotot Files ---")
    stats["chotot_records_read"] = process_file_list(chotot_files, "chotot")

    # 2. Process Bonbanh files second in batch order
    logger.info("--- Processing Bonbanh Files ---")
    stats["bonbanh_records_read"] = process_file_list(bonbanh_files, "bonbanh")

    stats["total_records_read"] = stats["chotot_records_read"] + stats["bonbanh_records_read"]
    stats["final_merged_records"] = len(merged_records)

    logger.info("Read total: %d (Chotot: %d, Bonbanh: %d)",
                stats["total_records_read"], stats["chotot_records_read"], stats["bonbanh_records_read"])
    logger.info("Duplicate URLs removed: %d", stats["duplicate_urls_removed"])
    logger.info("Final merged count: %d (Chotot: %d, Bonbanh: %d)",
                stats["final_merged_records"], stats["final_chotot_records"], stats["final_bonbanh_records"])

    return merged_records, stats


def save_merged_json(records: List[dict], output_path: Path):
    """Saves records as nicely formatted JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    logger.info("Saved canonical JSON dataset: %s (Size: %.2f MB)",
                output_path, output_path.stat().st_size / (1024 * 1024))


def save_merged_csv(records: List[dict], output_path: Path):
    """Saves records as companion CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_FIELDS)
        writer.writeheader()
        for r in records:
            writer.writerow(r)
    logger.info("Saved companion CSV dataset: %s (Size: %.2f MB)",
                output_path, output_path.stat().st_size / (1024 * 1024))


def run_merge(raw_dir: Path, output_json: Path, output_csv: Optional[Path]) -> dict:
    """Orchestrates the merge process and returns execution stats."""
    merged_records, stats = load_and_merge_datasets(raw_dir)

    save_merged_json(merged_records, output_json)
    if output_csv:
        save_merged_csv(merged_records, output_csv)

    return stats


def main():
    parser = argparse.ArgumentParser(description="Phase 3: Production Raw Data Merge Pipeline")
    parser.add_argument(
        "--input-dir",
        "--raw-dir",
        dest="raw_dir",
        type=Path,
        default=Path("crawler/data/raw"),
        help="Directory containing production raw JSON batches",
    )
    parser.add_argument(
        "--output",
        "--output-json",
        dest="output_json",
        type=Path,
        default=Path("crawler/data/merged/vehicles_raw_merged.json"),
        help="Output path for merged JSON dataset",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("crawler/data/merged/vehicles_raw_merged.csv"),
        help="Output path for companion CSV dataset",
    )
    parser.add_argument(
        "--skip-csv",
        action="store_true",
        help="Skip generating the companion CSV file",
    )

    args = parser.parse_args()

    raw_dir = args.raw_dir.resolve()
    output_json = args.output_json.resolve()
    output_csv = None if args.skip_csv else args.output_csv.resolve()

    logger.info("Starting Phase 3: Raw Data Merge")
    logger.info("Raw directory: %s", raw_dir)
    logger.info("Output JSON:   %s", output_json)
    if output_csv:
        logger.info("Output CSV:    %s", output_csv)

    if not raw_dir.exists():
        logger.error("Raw directory does not exist: %s", raw_dir)
        sys.exit(1)

    stats = run_merge(raw_dir, output_json, output_csv)
    logger.info("Merge completed successfully.")


if __name__ == "__main__":
    main()
