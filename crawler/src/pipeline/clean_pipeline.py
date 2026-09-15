"""
Clean Pipeline - Phase 4: Data Cleaning & Normalization

Transforms the merged raw dataset into a standardized clean dataset
suitable for validation, analysis, ML, and database import.

Author: TV3 — Data Engineering / Data Pipeline Developer
Project: Used-Car-Smart-System
"""

import argparse
import csv
import hashlib
import json
import logging
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add parent directories to sys.path so imports work whether run from root or within dir
CURRENT_DIR = Path(__file__).resolve().parent
CRAWLER_SRC = CURRENT_DIR.parent
if str(CRAWLER_SRC) not in sys.path:
    sys.path.insert(0, str(CRAWLER_SRC))

from cleaning import (
    clean_vehicle_record,
    validate_dataset,
)

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
logger = logging.getLogger("clean_pipeline")


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 checksum of a file for immutability verification."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def count_nulls(records: List[dict]) -> Dict[str, int]:
    """Count null values for each canonical field in a dataset."""
    counts = {field: 0 for field in CANONICAL_FIELDS}
    for r in records:
        for f in CANONICAL_FIELDS:
            if r.get(f) is None:
                counts[f] += 1
    return counts


def run_clean_pipeline(
    input_path: Path,
    output_json: Path,
    output_csv: Optional[Path],
    report_path: Path,
) -> dict:
    """Executes the full cleaning and normalization pipeline."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # 1. Immutability Pre-Check
    input_sha256_pre = compute_sha256(input_path)
    input_size_pre = input_path.stat().st_size
    logger.info("Loaded input raw dataset: %s (Size: %.2f MB)", input_path, input_size_pre / (1024 * 1024))
    logger.info("Raw Input SHA256 (Pre): %s", input_sha256_pre)

    with open(input_path, "r", encoding="utf-8") as f:
        raw_records = json.load(f)

    input_count = len(raw_records)
    logger.info("Total raw records to clean: %d", input_count)

    # Calculate initial nulls
    nulls_before = count_nulls(raw_records)

    # 2. Process Records
    cleaned_records = []
    transformations_counter: Dict[str, Counter] = {
        "brand": Counter(),
        "model": Counter(),
        "variant": Counter(),
        "manufacture_year": Counter(),
        "price": Counter(),
        "mileage": Counter(),
        "fuel_type": Counter(),
        "transmission": Counter(),
        "body_type": Counter(),
        "location": Counter(),
        "listed_at": Counter(),
    }

    records_removed = 0
    parse_failures = {field: 0 for field in CANONICAL_FIELDS}

    for idx, raw_rec in enumerate(raw_records):
        try:
            cleaned_rec, trans_log = clean_vehicle_record(raw_rec)
            cleaned_records.append(cleaned_rec)

            for field, (before_val, after_val) in trans_log.items():
                if field in transformations_counter:
                    transformations_counter[field][f"{before_val} -> {after_val}"] += 1

                # Track if a previously non-null value failed to parse and became null
                if before_val is not None and after_val is None:
                    parse_failures[field] += 1

        except Exception as e:
            logger.error("Failed to clean record #%d: %s", idx, e)
            records_removed += 1

    output_count = len(cleaned_records)
    nulls_after = count_nulls(cleaned_records)

    logger.info("Cleaning finished. Records processed: %d | Records output: %d | Records removed: %d",
                input_count, output_count, records_removed)

    # 3. Validate Cleaned Dataset
    is_valid, val_summary = validate_dataset(cleaned_records)
    if not is_valid:
        logger.error("Dataset validation failed! Errors: %s", val_summary["sample_errors"])
        raise ValueError(f"Cleaned dataset failed validation: {val_summary['sample_errors']}")
    logger.info("Cleaned dataset validation: PASSED (100%% 14-field contract + unique URLs)")

    # 4. Save Outputs
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(cleaned_records, f, ensure_ascii=False, indent=2)
    logger.info("Saved canonical clean JSON dataset: %s (Size: %.2f MB)",
                output_json, output_json.stat().st_size / (1024 * 1024))

    if output_csv:
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with open(output_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CANONICAL_FIELDS)
            writer.writeheader()
            for r in cleaned_records:
                writer.writerow(r)
        logger.info("Saved companion clean CSV dataset: %s (Size: %.2f MB)",
                    output_csv, output_csv.stat().st_size / (1024 * 1024))

    # 5. Immutability Post-Check
    input_sha256_post = compute_sha256(input_path)
    if input_sha256_pre != input_sha256_post:
        raise RuntimeError("CRITICAL INTEGRITY FAILURE: Raw input file was modified during pipeline execution!")
    logger.info("Raw Input SHA256 (Post): %s (IMMUTABILITY VERIFIED)", input_sha256_post)

    # 6. Build Quality Report Data
    # Convert Counter to sorted dict for JSON serialization
    transformations_report = {
        field: dict(counter.most_common())
        for field, counter in transformations_counter.items()
        if len(counter) > 0
    }

    report_data = {
        "pipeline": "Phase 4 - Data Cleaning & Normalization",
        "input_file": str(input_path),
        "input_sha256": input_sha256_post,
        "input_records": input_count,
        "output_file": str(output_json),
        "output_records": output_count,
        "records_removed": records_removed,
        "null_counts_before": nulls_before,
        "null_counts_after": nulls_after,
        "parse_failures": parse_failures,
        "validation_summary": val_summary,
        "normalization_counts": transformations_report,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    logger.info("Saved quality report: %s", report_path)

    return report_data


def main():
    parser = argparse.ArgumentParser(description="Phase 4: Data Cleaning & Normalization Pipeline")
    parser.add_argument(
        "--input",
        dest="input_path",
        type=Path,
        default=Path("crawler/data/merged/vehicles_raw_merged.json"),
        help="Path to canonical merged raw JSON file",
    )
    parser.add_argument(
        "--output",
        dest="output_json",
        type=Path,
        default=Path("crawler/data/cleaned/vehicles_cleaned.json"),
        help="Path to canonical cleaned JSON file",
    )
    parser.add_argument(
        "--output-csv",
        dest="output_csv",
        type=Path,
        default=Path("crawler/data/cleaned/vehicles_cleaned.csv"),
        help="Path to companion cleaned CSV file",
    )
    parser.add_argument(
        "--skip-csv",
        action="store_true",
        help="Skip generating CSV companion",
    )
    parser.add_argument(
        "--report",
        dest="report_path",
        type=Path,
        default=Path("crawler/data/quality_report/phase4_cleaning_report.json"),
        help="Path to output quality report JSON",
    )

    args = parser.parse_args()

    input_path = args.input_path.resolve()
    output_json = args.output_json.resolve()
    output_csv = None if args.skip_csv else args.output_csv.resolve()
    report_path = args.report_path.resolve()

    logger.info("Starting Phase 4: Data Cleaning Pipeline")
    logger.info("Input path:   %s", input_path)
    logger.info("Output JSON:  %s", output_json)
    if output_csv:
        logger.info("Output CSV:   %s", output_csv)
    logger.info("Report path:  %s", report_path)

    report_data = run_clean_pipeline(input_path, output_json, output_csv, report_path)
    logger.info("Phase 4 Pipeline completed successfully.")


if __name__ == "__main__":
    main()
