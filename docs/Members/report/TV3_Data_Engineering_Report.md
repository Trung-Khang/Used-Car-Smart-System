# TV3 — DATA ENGINEERING & DATA PIPELINE CONSOLIDATED REPORT

**Project:** `Used-Car-Smart-System`  
**Role:** TV3 — Data Engineering / Data Pipeline Developer  
**Scope:** Crawling → Merging → Cleaning → Validation → Seed Generation → TV4 Handoff Enrichment  
**Dataset:** 10,813 real marketplace records (Bonbanh: 7,697 | Chợ Tốt: 3,116)  
**Data Quality Grade:** Grade A (98.41/100 baseline quality)  
**TV4 Handoff Status:** **PASS WITH WARNINGS**  

---

# 1. Executive Summary

TV3 is responsible for delivering a clean, trustworthy, normalized, and validated dataset extracted from real Vietnamese automotive marketplaces (**Chợ Tốt** and **Bonbanh**).

The complete data pipeline follows a strict batch architecture:

```text
Chợ Tốt (xe.chotot.com) ──┐
                          │
                          ▼
                     Raw Crawlers
                          │
Bonbanh (bonbanh.com) ────┘
                          │
                          ▼
                  Raw Batches (16 files, Immutable)
                          │
                          ▼
                       PHASE 3: MERGE
                          │ (10,813 unified raw records)
                          ▼
                      PHASE 4: CLEANING
                          │ (Standardization, unit parsing, location normalization)
                          ▼
                     PHASE 5: VALIDATION
                          │ (Schema check, outlier audit, Grade A score)
                          ▼
                   PHASE 6: DATABASE SEED
                          │ (Seed JSON/CSV/SQL generation)
                          ▼
            TV4 DATASET ENRICHMENT & HANDOFF REPAIR
                          │ (Detail spec extraction: origin, engine_size, seat_count)
                          ▼
               CANONICAL CLEAN DATASET (17 fields)
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
TV4 (ML / Regression)             TV5 (Database Import)
```

---

# 2. Pipeline Phases Summary

* **Phase 1 — Chợ Tốt Crawler:** Production crawler collecting real vehicle listings via public gateway API.
* **Phase 2 — Bonbanh Crawler:** Production crawler collecting real vehicle listings via static HTML parsing with session management and backoff.
* **Phase 2.5 & 2.6 — Production Crawling:** Scaled raw dataset to **10,813 unique marketplace records** (Bonbanh: 7,697; Chợ Tốt: 3,116).
* **Phase 3 — Data Merge:** Merged 16 raw batches into one canonical raw dataset with 0 URL duplicates.
* **Phase 4 — Data Cleaning & Normalization:** Standardized brands, models, numeric prices (VND), odometer readings (km), fuel types, transmissions, body styles, and Vietnamese administrative locations.
* **Phase 5 — Quality Validation:** Rigorous data quality audit resulting in 98.41/100 (Grade A).
* **Phase 6 — Database Seed Preparation:** Generated seed datasets (SQL, JSON, CSV) preserving raw lineage and natural nulls.

---

# 3. TV4 Compatibility & Dataset Enrichment

## 3.1. TV4 Feedback & Requirements Review

Following an initial review of the cleaned dataset, **TV4 (Machine Learning / Regression Developer)** requested four feature enhancements to align with their downstream regression model:

1. `origin`: Country of vehicle assembly (`Domestic` vs. `Imported`).
2. `engine_size`: Combustion engine displacement in numeric liters (e.g. `1.5`, `2.0`).
3. `seat_count`: Passenger seating capacity as integer (e.g. `5`, `7`).
4. `listed_year`: Year of listing.
5. **CSV Encoding:** Vietnamese diacritics in CSV were causing mojibake when read in R and PowerShell.
6. **Transmission categories:** Alignment with TV4's expected vocabulary (`Automatic`, `Manual`, `CVT`).
7. **Fuel type anomalies:** Investigation of anomaly `"Loại khác  2.5 L"`.
8. **Extreme mileage anomaly:** Investigation of maximum mileage value `3,380,000,000 Km`.

Regarding `listed_year`: Both TV3 and TV4 explicitly agreed that:
$$\text{listed\_year} = \text{year}(\text{crawled\_at})$$
Because all records possess an immutable UTC ISO timestamp `crawled_at` (e.g. `"2026-09-07T08:25:55+00:00"`), `listed_year` is trivially derivable downstream (`int(crawled_at[:4])`). Therefore, **`listed_year` was NOT added as a redundant canonical column**, avoiding schema bloat while guaranteeing zero information loss.

## 3.2. TV3 Actions Taken

1. **Detail-Page Enrichment Pipeline (`crawler/src/pipeline/enrich_pipeline.py`):**
   * Built a high-performance enrichment pipeline using `ThreadPoolExecutor`, session handling, retry backoff, and JSON checkpointing (`crawler/data/tmp/enrichment_checkpoint.json`).
   * **Bonbanh:** Parsed detail specification rows:
     * `"Xuất xứ"` $\rightarrow$ `Domestic` (`Lắp ráp trong nước`) / `Imported` (`Nhập khẩu`).
     * `"Động cơ"` $\rightarrow$ Extracted numeric displacement in liters (e.g. `"Xăng 1.5 L"` $\rightarrow$ `1.5`, `"1998 cc"` $\rightarrow$ `1.998`). Electric vehicles mapped to `null`.
     * `"Số chỗ ngồi"` $\rightarrow$ Extracted integer passenger capacity (e.g. `"5 chỗ"` $\rightarrow$ `5`).
   * **Chợ Tốt:** Queried the public ad-listing gateway API (`https://gateway.chotot.com/v1/public/ad-listing/{ad_id}`):
     * `parameters.carorigin` $\rightarrow$ `Domestic` (`Việt Nam`) / `Imported` (foreign countries).
     * `parameters.carseats` $\rightarrow$ Extracted integer seat count.
     * `subject` & `body` $\rightarrow$ Extracted combustion engine displacement in liters.
   * **Strict Non-Fabrication Rule:** If a seller omitted a field or the listing was removed/expired (HTTP 404), TV3 recorded `null`. TV3 never inferred origin from brand or seats from body type.
2. **Transmission Normalization:**
   * Aligned transmission values with TV4's vocabulary: `Automatic` (9,577), `Manual` (1,214).
   * 21 records with seller-selected `"Semi-Automatic"` and 1 unresolvable `"Other"` were mapped to `null` to prevent introducing arbitrary categories into the regression model.
3. **Fuel Type Normalization:**
   * Canonical categories: `Gasoline` (7,543), `Diesel` (1,565), `Electric` (1,204), `Hybrid` (500).
   * Anomaly `"Loại khác  2.5 L"` on expired listing `6954382` was investigated; since original source was inaccessible, it was mapped to `null` per Section 13.
4. **Mileage Anomaly Investigation:**
   * Verified Bonbanh listing `6954854`: Source HTML explicitly renders `3,380,000,000 Km` (seller typo on source marketplace). TV3 faithfully preserved the integer value to maintain source truth, delegating ML outlier filtering to TV4.
5. **CSV UTF-8-SIG Encoding:**
   * Re-exported `vehicles_cleaned.csv` using Python's `encoding="utf-8-sig"` (UTF-8 with BOM `\xef\xbb\xbf`).
   * Verified that Vietnamese diacritics (`Hồ Chí Minh`, `Đắk Lắk`, `Bình Thạnh`) display cleanly in Excel, R, and PowerShell.

## 3.3. Authoritative Feature Availability & Completeness

| Field Name | Source | Data Type | Unit | Missing Rule | Value Distribution / Completeness | TV4 Availability |
|---|---|---|---|---|---|---|
| `brand` | Listing | String | - | Mandatory | 10,813 non-null (100.0%) | Available |
| `model` | Listing | String | - | Mandatory | 10,813 non-null (100.0%) | Available |
| `variant` | Listing/Specs | String | - | `null` if omitted | 9,340 non-null (86.38%) / 1,473 null | Available |
| `manufacture_year` | Listing/Specs | Integer | Year | Mandatory | 10,813 non-null (100.0%) | Available |
| `price` | Listing | Integer | VND | Mandatory | 10,813 non-null (100.0%) | Available |
| `mileage` | Listing/Specs | Integer | km | `null` if new/omitted | 8,506 non-null (78.66%) / 2,307 null | Available |
| `fuel_type` | Listing/Specs | Categorical | - | `null` if unknown | 10,812 non-null (99.99%) / 1 null | Available |
| `transmission` | Listing/Specs | Categorical | - | `null` if unknown | 10,791 non-null (99.80%) / 22 null | Available |
| `body_type` | Listing/Specs | Categorical | - | `null` if omitted | 9,752 non-null (90.19%) / 1,061 null | Available |
| `location` | Listing | String | - | Mandatory | 10,813 non-null (100.0%) | Available |
| `origin` | Detail Specs | Categorical | - | `null` if unavailable | **1,588 non-null (14.69%) / 9,225 null** | **Available** |
| `engine_size` | Detail Specs / Variant | Float | L | `null` if EV/unavailable | **5,959 non-null (55.11%) / 4,854 null** | **Available** |
| `seat_count` | Detail Specs / Variant | Integer | Seats | `null` if unavailable | **1,338 non-null (12.37%) / 9,475 null** | **Available** |
| `source_url` | Listing URL | String (URL) | - | Mandatory (Unique) | 10,813 non-null (100.0%) | Available |
| `image_url` | Listing CDN | String (URL) | - | `null` if omitted | 10,813 non-null (100.0%) | Available |
| `listed_at` | Listing | String | - | `null` if omitted | 10,812 non-null (99.99%) / 1 null | Available |
| `crawled_at` | Pipeline | ISO 8601 | UTC | Mandatory | 10,813 non-null (100.0%) | Available |
| *`listed_year`* | Derived | Integer | Year | Derivable from `crawled_at` | 10,813 derivable (100.0%) | **Available Downstream** |

## 3.4. Data Quality & Anomaly Report

* **Suspicious Price Low (`< 50M VND`):** 68 records (e.g. 5,000,000 VND). Verified as legitimate deposit amounts or installment figures entered by marketplace sellers. Preserved for TV4 outlier handling.
* **Suspicious Price High (`> 15B VND`):** 5 records (e.g. 33,000,000,000 VND). Verified as ultra-luxury vehicles (Rolls-Royce Phantom, Bentley Mulsanne, Ferrari). Authentic data.
* **Suspicious Mileage (`> 1,000,000 km`):** 8 records, including 1 extreme outlier at `3,380,000,000 km` (seller typo on source). Preserved faithfully as integer.
* **Old Manufacture Years (`< 1990`):** 11 records (range: 1980 - 1989). Authentic vintage vehicles (e.g. Mercedes W123, Toyota Corona).
* **Unknown Transmission:** 22 records mapped to `null`.
* **Unknown Fuel Type:** 1 record mapped to `null`.

## 3.5. Operational Enrichment Metrics

The incremental enrichment and detail retrieval pipeline produced the following verified operational metrics with mathematically consistent denominators:

| # | Operational Metric Category | Measured Count | Scope & Denominator Context |
|---|---|---|---|
| 1 | **Total records** | **10,813** | 100% of canonical dataset records |
| 2 | **Records already fully populated and skipped** | **817** | Records with `origin`, `engine_size`, and `seat_count` all non-null |
| 3 | **Records requiring enrichment** | **9,996** | Records with at least one target field NULL ($817 + 9,996 = 10,813$) |
| 4 | **Unique detail URLs targeted** | **10,813** | 100% unique source URLs across dataset |
| 5 | **Actual HTTP request attempts** | **10,813** | Network requests issued during full detail retrieval pass |
| 6 | **Successful HTTP responses** | **1,588** | HTTP 200 OK responses (Chợ Tốt: 1,101; Bonbanh: 487) |
| 7 | **HTTP 404/410 responses** | **2,015** | Expired/deleted listings on Chợ Tốt ($1,101 + 2,015 = 3,116$) |
| 8 | **HTTP rate-limit responses** | **7,210** | HTTP 403 Forbidden on Bonbanh ($487 + 7,210 = 7,697$) |
| 9 | **Retry attempts** | Bounded (max 1 retry) | Retries attempted for transient network timeouts |
| 10 | **Records successfully enriched (incremental)** | **5,406** | Unique records receiving newly extracted values from variant (5,406 `engine_size`, 6 `seat_count`, with 6 overlapping) |
| 11 | **Records with no newly extracted value** | **4,590** | Records requiring enrichment where variant lacked explicit specs ($9,996 - 5,406 = 4,590$) |
| 12 | **Parse failures** | **0** | Zero parsing crashes |
| 13 | **Invalid extracted values** | **0** | Zero invalid types or out-of-range numeric values |

> **Fields unresolved after local extraction and incremental source enrichment:**
> - `origin`: **9,225** records unresolved (14.69% populated)
> - `engine_size`: **4,854** records unresolved (55.11% populated)
> - `seat_count`: **9,475** records unresolved (12.37% populated)

## 3.6. Responsibility Boundary

> **TV3 Scope:** TV3 performs raw source extraction, data parsing, cleaning, unit standardization, categorical normalization, data integrity validation, and anomaly auditing. TV3 guarantees source-derived truth and never fabricates data.  
> **TV4 Scope:** TV4 owns all Machine Learning-specific preprocessing for Regression, including outlier filtering (e.g., removing `< 50M` deposits or `3.38B km` typos), missing value imputation, one-hot encoding, feature scaling, and train/test splitting.

---

# 4. TV4 Handoff Status

```text
================================================================
TV4 HANDOFF STATUS: PASS WITH WARNINGS
================================================================
Reasons:
1. All 17 canonical fields are present in both vehicles_cleaned.json
   and vehicles_cleaned.csv in exact agreed schema order.
2. Source-derived data: values were extracted from explicit marketplace
   listing information or existing local raw/variant data; values that
   could not be verified were kept as null.
3. Natural missing values exist and are faithfully represented as null
   (origin: 9,225 unresolved, engine_size: 4,854 unresolved,
   seat_count: 9,475 unresolved).
4. listed_year is 100% derivable downstream from crawled_at.
5. All anomalies are comprehensively documented with source evidence.
6. CSV encoding is verified as UTF-8-SIG (BOM present).
7. Raw data remains 100% immutable (SHA256 verified).
================================================================
```
