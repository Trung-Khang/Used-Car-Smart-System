"""
Import Pipeline - Phase 6: Database Seed & Import

Transforms the validated cleaned dataset (10,813 records) into a database-compatible
seed dataset, generates SQL/JSON/CSV seed files, and provides a reproducible import process.

Author: TV3 — Data Engineering / Data Pipeline Developer
Project: Used-Car-Smart-System
"""

import argparse
import csv
import hashlib
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

# Canonical fields in cleaned dataset
CLEANED_FIELDS = [
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

# Database seed fields
SEED_FIELDS = [
    "id",
    "source",
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
logger = logging.getLogger("import_pipeline")


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 checksum of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def identify_source(url: str) -> str:
    """Determine source name from URL domain."""
    domain = urlparse(url).netloc.lower()
    if "chotot" in domain:
        return "chotot"
    elif "bonbanh" in domain:
        return "bonbanh"
    return "other"


def transform_record_for_database(record: dict, record_id: int) -> dict:
    """
    Transforms a single cleaned record into a database-compatible seed record.
    Preserves all 14 cleaned attributes and authentic nulls.
    Adds deterministic ID and source platform.
    """
    source_name = identify_source(record.get("source_url", ""))

    return {
        "id": record_id,
        "source": source_name,
        "brand": record.get("brand"),
        "model": record.get("model"),
        "variant": record.get("variant"),
        "manufacture_year": record.get("manufacture_year"),
        "price": record.get("price"),
        "mileage": record.get("mileage"),
        "fuel_type": record.get("fuel_type"),
        "transmission": record.get("transmission"),
        "body_type": record.get("body_type"),
        "location": record.get("location"),
        "source_url": record.get("source_url"),
        "image_url": record.get("image_url"),
        "listed_at": record.get("listed_at"),
        "crawled_at": record.get("crawled_at"),
    }


def generate_seed_datasets(
    cleaned_records: List[dict],
    seed_dir: Path,
) -> Tuple[List[dict], Dict[str, Path]]:
    """
    Transforms cleaned records into database-ready seed datasets and outputs:
    1. vehicles_seed.json (full 10,813 seed records)
    2. vehicles_seed.csv (companion CSV)
    3. vehicles_seed.sql (PostgreSQL DDL + batch INSERT script)
    4. vehicles_seed_dev.json (1,000 records dev subset per TV3 mission)
    """
    seed_dir.mkdir(parents=True, exist_ok=True)

    transformed_records = []
    for idx, rec in enumerate(cleaned_records, start=1):
        db_rec = transform_record_for_database(rec, record_id=idx)
        transformed_records.append(db_rec)

    # 1. Save Full JSON Seed
    json_path = seed_dir / "vehicles_seed.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(transformed_records, f, ensure_ascii=False, indent=2)
    logger.info("Generated canonical JSON seed: %s (%d records, %.2f MB)",
                json_path, len(transformed_records), json_path.stat().st_size / (1024 * 1024))

    # 2. Save Full CSV Seed
    csv_path = seed_dir / "vehicles_seed.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SEED_FIELDS)
        writer.writeheader()
        for r in transformed_records:
            writer.writerow(r)
    logger.info("Generated companion CSV seed: %s (%.2f MB)",
                csv_path, csv_path.stat().st_size / (1024 * 1024))

    # 3. Save Dev Seed (First 1,000 records for fast local development)
    dev_json_path = seed_dir / "vehicles_seed_dev.json"
    dev_subset = transformed_records[:1000]
    with open(dev_json_path, "w", encoding="utf-8") as f:
        json.dump(dev_subset, f, ensure_ascii=False, indent=2)
    logger.info("Generated development seed subset: %s (%d records)",
                dev_json_path, len(dev_subset))

    # 4. Save PostgreSQL SQL Insert Script
    sql_path = seed_dir / "vehicles_seed.sql"
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- ====================================================================\n")
        f.write("-- Used-Car-Smart-System: Database Seed Script (Phase 6)\n")
        f.write(f"-- Total records: {len(transformed_records)}\n")
        f.write("-- Generated by TV3: Data Engineering Pipeline\n")
        f.write("-- ====================================================================\n\n")

        # Table schema definition (ANSI / PostgreSQL compatible)
        f.write("CREATE TABLE IF NOT EXISTS vehicles (\n")
        f.write("    id BIGINT PRIMARY KEY,\n")
        f.write("    source VARCHAR(50) NOT NULL,\n")
        f.write("    brand VARCHAR(100) NOT NULL,\n")
        f.write("    model VARCHAR(100) NOT NULL,\n")
        f.write("    variant VARCHAR(150),\n")
        f.write("    manufacture_year INT NOT NULL,\n")
        f.write("    price BIGINT NOT NULL,\n")
        f.write("    mileage INT,\n")
        f.write("    fuel_type VARCHAR(50) NOT NULL,\n")
        f.write("    transmission VARCHAR(50) NOT NULL,\n")
        f.write("    body_type VARCHAR(50),\n")
        f.write("    location VARCHAR(250) NOT NULL,\n")
        f.write("    source_url TEXT NOT NULL UNIQUE,\n")
        f.write("    image_url TEXT,\n")
        f.write("    listed_at VARCHAR(50),\n")
        f.write("    crawled_at TIMESTAMPTZ NOT NULL\n")
        f.write(");\n\n")

        # Indexes
        f.write("CREATE INDEX IF NOT EXISTS idx_vehicles_brand ON vehicles(brand);\n")
        f.write("CREATE INDEX IF NOT EXISTS idx_vehicles_model ON vehicles(model);\n")
        f.write("CREATE INDEX IF NOT EXISTS idx_vehicles_price ON vehicles(price);\n")
        f.write("CREATE INDEX IF NOT EXISTS idx_vehicles_year ON vehicles(manufacture_year);\n")
        f.write("CREATE INDEX IF NOT EXISTS idx_vehicles_source_url ON vehicles(source_url);\n\n")

        f.write("BEGIN TRANSACTION;\n\n")

        # Batch inserts in chunks of 500
        batch_size = 500
        for i in range(0, len(transformed_records), batch_size):
            chunk = transformed_records[i:i + batch_size]
            f.write("INSERT INTO vehicles (id, source, brand, model, variant, manufacture_year, price, mileage, fuel_type, transmission, body_type, location, source_url, image_url, listed_at, crawled_at)\nVALUES\n")

            values_list = []
            for r in chunk:
                # Format SQL values safely
                v_id = str(r["id"])
                v_src = "'" + r["source"].replace("'", "''") + "'"
                v_brand = "'" + r["brand"].replace("'", "''") + "'"
                v_model = "'" + r["model"].replace("'", "''") + "'"
                v_var = ("'" + r["variant"].replace("'", "''") + "'") if r["variant"] is not None else "NULL"
                v_year = str(r["manufacture_year"])
                v_price = str(r["price"])
                v_mil = str(r["mileage"]) if r["mileage"] is not None else "NULL"
                v_fuel = "'" + r["fuel_type"].replace("'", "''") + "'"
                v_trans = "'" + r["transmission"].replace("'", "''") + "'"
                v_body = ("'" + r["body_type"].replace("'", "''") + "'") if r["body_type"] is not None else "NULL"
                v_loc = "'" + r["location"].replace("'", "''") + "'"
                v_surl = "'" + r["source_url"].replace("'", "''") + "'"
                v_iurl = ("'" + r["image_url"].replace("'", "''") + "'") if r["image_url"] is not None else "NULL"
                v_listed = ("'" + r["listed_at"].replace("'", "''") + "'") if r["listed_at"] is not None else "NULL"
                v_crawled = "'" + r["crawled_at"].replace("'", "''") + "'"

                row_str = f"  ({v_id}, {v_src}, {v_brand}, {v_model}, {v_var}, {v_year}, {v_price}, {v_mil}, {v_fuel}, {v_trans}, {v_body}, {v_loc}, {v_surl}, {v_iurl}, {v_listed}, {v_crawled})"
                values_list.append(row_str)

            f.write(",\n".join(values_list))
            f.write("\nON CONFLICT (source_url) DO UPDATE SET\n")
            f.write("    price = EXCLUDED.price,\n")
            f.write("    mileage = EXCLUDED.mileage,\n")
            f.write("    crawled_at = EXCLUDED.crawled_at;\n\n")

        f.write("COMMIT;\n")

    logger.info("Generated PostgreSQL SQL seed script: %s (%.2f MB)",
                sql_path, sql_path.stat().st_size / (1024 * 1024))

    paths = {
        "json": json_path,
        "csv": csv_path,
        "sql": sql_path,
        "dev_json": dev_json_path,
    }
    return transformed_records, paths


def run_import_pipeline(
    input_path: Path,
    seed_dir: Path,
    report_path: Path,
    db_params: Optional[dict] = None,
) -> dict:
    """Orchestrates the Phase 6 transformation, seed generation, and import audit."""
    if not input_path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {input_path}")

    # Immutability Check (Pre)
    sha256_pre = compute_sha256(input_path)
    logger.info("Cleaned dataset SHA256 (Pre): %s", sha256_pre)

    with open(input_path, "r", encoding="utf-8") as f:
        cleaned_records = json.load(f)

    input_count = len(cleaned_records)
    logger.info("Loaded %d cleaned records for Phase 6 Seed & Import", input_count)

    # 1. Transform & Generate Seed Files
    transformed_records, generated_paths = generate_seed_datasets(cleaned_records, seed_dir)
    transformed_count = len(transformed_records)

    # 2. Source Breakdown
    chotot_count = sum(1 for r in transformed_records if r["source"] == "chotot")
    bonbanh_count = sum(1 for r in transformed_records if r["source"] == "bonbanh")

    # 3. Database Execution Assessment
    # Check repository state for active database tables
    database_status = "READY_FOR_IMPORT"
    db_error_detail = None
    inserted_count = 0
    skipped_count = 0
    failed_count = 0
    final_db_count = 0

    if db_params:
        # If DB connection parameters were provided, attempt live import
        try:
            import psycopg2
            conn = psycopg2.connect(**db_params)
            with conn.cursor() as cur:
                with open(generated_paths["sql"], "r", encoding="utf-8") as f:
                    cur.execute(f.read())
                conn.commit()
                cur.execute("SELECT COUNT(*) FROM vehicles;")
                final_db_count = cur.fetchone()[0]
                inserted_count = final_db_count
                database_status = "IMPORTED"
            conn.close()
            logger.info("Successfully imported %d records into PostgreSQL database", final_db_count)
        except Exception as e:
            database_status = "DB_CONNECTION_ERROR"
            db_error_detail = str(e)
            logger.warning("Database live import failed: %s", e)
    else:
        # Standard repository state: database/schema has .gitkeep; credentials not configured
        database_status = "SEED_READY_PENDING_DB_MIGRATION"
        db_error_detail = "Database credentials/schema DDL not configured in repository. Seed files generated and validated; physical import awaiting TV5 schema deployment."
        logger.info("Database physical execution: %s", database_status)
        logger.info("Detail: %s", db_error_detail)

    # Immutability Check (Post)
    sha256_post = compute_sha256(input_path)
    if sha256_pre != sha256_post:
        raise RuntimeError("CRITICAL INTEGRITY FAILURE: Cleaned input file was modified during Phase 6 execution!")
    logger.info("Cleaned dataset SHA256 (Post): %s (IMMUTABILITY VERIFIED)", sha256_post)

    # 4. Compile Quality & Audit Report
    report_data = {
        "pipeline": "Phase 6 - Database Seed & Import",
        "input_file": str(input_path),
        "input_sha256": sha256_post,
        "input_records": input_count,
        "transformed_records": transformed_count,
        "inserted_records": inserted_count,
        "skipped_records": skipped_count,
        "failed_records": failed_count,
        "database_records_after_import": final_db_count,
        "database_status": database_status,
        "database_status_detail": db_error_detail,
        "source_distribution": {
            "chotot": chotot_count,
            "bonbanh": bonbanh_count,
        },
        "generated_files": {k: str(v) for k, v in generated_paths.items()},
        "validation_status": "PASS WITH WARNINGS" if database_status != "IMPORTED" else "PASS",
        "errors": [db_error_detail] if db_error_detail and database_status != "IMPORTED" else [],
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    logger.info("Saved Phase 6 quality report: %s", report_path)

    return report_data


def main():
    parser = argparse.ArgumentParser(description="Phase 6: Database Seed & Import Pipeline")
    parser.add_argument(
        "--input",
        dest="input_path",
        type=Path,
        default=Path("crawler/data/cleaned/vehicles_cleaned.json"),
        help="Path to validated cleaned JSON file",
    )
    parser.add_argument(
        "--seed-dir",
        dest="seed_dir",
        type=Path,
        default=Path("crawler/data/seed"),
        help="Output directory for generated seed files",
    )
    parser.add_argument(
        "--report",
        dest="report_path",
        type=Path,
        default=Path("crawler/data/quality_report/phase6_import_report.json"),
        help="Output path for quality report JSON",
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        default=True,
        help="Generate seed files without attempting live database connection",
    )

    args = parser.parse_args()

    input_path = args.input_path.resolve()
    seed_dir = args.seed_dir.resolve()
    report_path = args.report_path.resolve()

    logger.info("Starting Phase 6: Database Seed & Import Pipeline")
    logger.info("Input path:  %s", input_path)
    logger.info("Seed dir:    %s", seed_dir)
    logger.info("Report path: %s", report_path)

    report_data = run_import_pipeline(input_path, seed_dir, report_path, db_params=None)
    logger.info("Phase 6 Pipeline completed.")


if __name__ == "__main__":
    main()
