# Used-Car-Smart-System — Crawler & Data Pipeline (TV3)

## 1. Overview

This module is developed by **TV3 — Data Engineering / Data Pipeline Developer** for the `Used-Car-Smart-System` project.

It provides a batch crawling, merging, cleaning, enrichment, and validation pipeline that transforms raw marketplace listings from **Chợ Tốt** and **Bonbanh** into a validated dataset tailored for **TV4 — Machine Learning / Regression Pipeline** and **TV5 — Database / Backend Integration**.

---

## 2. Dataset Overview

* **Total Records:** `10,813` verified marketplace records
* **Source Distribution:**
  * Bonbanh (`bonbanh.com`): `7,697` records (71.18%)
  * Chợ Tốt (`chotot.com`): `3,116` records (28.82%)
* **Schema:** Exactly **17 canonical fields**
* **Traceability:** 100% unique `source_url` with original lineage preserved
* **Enriched Feature Completeness:**
  * `origin`: `1,588` / `10,813` (14.69%) | `null`: `9,225` (85.31%)
  * `engine_size`: `5,959` / `10,813` (55.11%) | `null`: `4,854` (44.89%)
  * `seat_count`: `1,338` / `10,813` (12.37%) | `null`: `9,475` (87.63%)
* **Encoding:**
  * Cleaned JSON: UTF-8 (`ensure_ascii=False`)
  * Cleaned CSV: UTF-8 with BOM (`utf-8-sig`) — prevents Vietnamese character corruption in Excel, R, and PowerShell

---

## 3. Authoritative 17-Field Data Dictionary

| # | Field Name | Data Type | Unit | Meaning | Normalization & Business Rules | Missing Rule | Example | Source |
|---|------------|-----------|------|---------|--------------------------------|--------------|---------|--------|
| 1 | `brand` | String | - | Vehicle manufacturer make | Standardized name (e.g., Toyota, Hyundai, VinFast, Mercedes-Benz) | Mandatory (100% complete) | `"Toyota"` | Listing / Parameters |
| 2 | `model` | String | - | Vehicle model name | Cleaned alphanumeric model name | Mandatory (100% complete) | `"Camry"` | Listing / Parameters |
| 3 | `variant` | String | - | Trim level or sub-model edition | Seller-specified edition/trim | `null` if omitted by seller | `"2.5Q"` | Listing title / Parameters |
| 4 | `manufacture_year` | Integer | Year | Year vehicle was produced | Integer year `1980 <= year <= 2026` | Mandatory (100% complete) | `2018` | Listing specs / Parameters |
| 5 | `price` | Integer | VND | Selling price in Vietnamese Dong | Integer amount `5,000,000 <= price <= 33,000,000,000` | Mandatory (100% complete) | `850000000` | Listing price string |
| 6 | `mileage` | Integer | km | Odometer reading | Non-negative integer kilometers | `null` for new cars or omitted | `45000` | Listing specs / Parameters |
| 7 | `fuel_type` | Categorical | - | Powertrain energy source | Standardized vocabulary: `Gasoline`, `Diesel`, `Electric`, `Hybrid`. Unresolvable values mapped to `null`. | `null` if unresolvable | `"Gasoline"` | Listing specs / Parameters |
| 8 | `transmission` | Categorical | - | Gearbox mechanism | Standardized vocabulary for TV4 regression: `Automatic`, `Manual`, `CVT`. Unresolvable (`Semi-Automatic`, `Other`) mapped to `null`. | `null` if unresolvable | `"Automatic"` | Listing specs / Parameters |
| 9 | `body_type` | Categorical | - | Vehicle chassis configuration | Standardized categories: `Sedan`, `SUV / Crossover`, `Hatchback`, `Pickup`, `MPV`, `Van`, `Coupe`, `Convertible` | `null` if unspecified | `"Sedan"` | Listing specs / Parameters |
| 10 | `location` | String | - | Administrative location of listing | Cleaned Vietnamese geographic name (Province / City / District) | Mandatory (100% complete) | `"Quận Cầu Giấy, Hà Nội"` | Listing / Contact details |
| 11 | `origin` | Categorical | - | Assembly / import origin | Standardized vocabulary: `Domestic` (Việt Nam, Lắp ráp trong nước) or `Imported` (Nhập khẩu, foreign nations). Never guessed or inferred. | `null` if unavailable | `"Domestic"` | Detail page specs |
| 12 | `engine_size` | Float | Liter (L) | Combustion engine displacement | Numeric liters (e.g. `1.5`, `2.0`, `1.498`). EVs set to `null`. Never inferred from brand/model/variant. | `null` if unavailable or EV | `1.998` | Detail page specs / text |
| 13 | `seat_count` | Integer | Seats | Total passenger seating capacity | Integer seating capacity (e.g. `4`, `5`, `7`). Never inferred from body type. | `null` if unavailable | `5` | Detail page specs |
| 14 | `source_url` | String | URL | Authoritative listing URL | Absolute canonical URL. Guaranteed unique across the dataset. | Mandatory (100% complete) | `"https://bonbanh.com/..."` | Source platform |
| 15 | `image_url` | String | URL | Primary listing thumbnail / photo | Absolute CDN URL | `null` if omitted | `"https://cdn.chotot.com/..."` | Listing media |
| 16 | `listed_at` | String | - | Listing publication date / relative time | Raw or normalized date string | `null` if unavailable | `"2026-09-07"` | Listing header |
| 17 | `crawled_at` | String | ISO 8601 | Pipeline ingestion timestamp | Standard UTC ISO 8601 timestamp | Mandatory (100% complete) | `"2026-09-07T08:25:55+00:00"` | Pipeline execution |

> **Note on `listed_year`:** Per agreement between TV3 and TV4, `listed_year` is **NOT** included as a redundant column in the canonical dataset. TV4 derives it downstream via `listed_year = int(crawled_at[:4])` with zero information loss.

---

## 4. Pipeline Components

```text
crawler/
├── data/
│   ├── raw/                 # Immutable original crawl batches (SHA256 verified)
│   ├── merged/              # Merged raw dataset (10,813 records)
│   ├── cleaned/
│   │   ├── vehicles_cleaned.json   # Canonical clean 17-field dataset (UTF-8)
│   │   └── vehicles_cleaned.csv    # Canonical clean 17-field dataset (UTF-8-SIG)
│   ├── quality_report/      # Data quality & TV4 compatibility audit reports
│   └── seed/                # Seed exports for database import
├── src/
│   ├── crawlers/
│   │   ├── chotot/          # Chợ Tốt crawler and parser modules
│   │   └── bonbanh/         # Bonbanh crawler and parser modules
│   └── pipeline/
│       ├── clean_pipeline.py    # Merging and cleaning transformation
│       ├── enrich_pipeline.py   # Detail specs enrichment (origin, engine, seats)
│       └── import_pipeline.py   # Database seed generation and import
└── scripts/
    └── seed_database.py     # CLI entry point for database seeding
```

---

## 5. Responsibility Boundary

* **TV3 Scope:**
  * Web crawling, parsing, deduplication, schema normalization, unit standardization.
  * Faithfully extracting explicit marketplace data (`origin`, `engine_size`, `seat_count`).
  * Validating integrity, ensuring raw immutability, flagging anomalies, producing audit reports.
* **TV4 Scope:**
  * Machine Learning regression modeling.
  * Regression-specific outlier filtering (e.g. vintage vehicles `< 1990`, extreme mileages, ultra-luxury prices `> 15B`).
  * Missing value imputation, one-hot encoding, feature scaling, train/test splitting.
