\# TV3 — Phase 3: Raw Data Merge Report



\*\*Role:\*\* TV3 — Data Engineering / Data Pipeline Developer  

\*\*Project:\*\* `Used-Car-Smart-System`  

\*\*Phase:\*\* Phase 3 — Merge / Combine Production Raw Data  

\*\*Date:\*\* 2026-09-08  

\*\*Status:\*\* COMPLETED — ALL AUDITS PASSED  



\---



\## 1. Executive Summary



Phase 3 successfully unified all production raw vehicle listings crawled during Phase 2.5 and Phase 2.6 from two independent automotive platforms: \*\*Chợ Tốt Xe\*\* (`xe.chotot.com`) and \*\*Bonbanh\*\* (`bonbanh.com`).



All records were validated against the canonical \*\*14-field data contract\*\*, checked for exact URL duplicates, and assembled into a single canonical merged raw dataset (`vehicles\_raw\_merged.json`) alongside an analytical companion CSV (`vehicles\_raw\_merged.csv`). 



Strict boundary discipline was maintained: \*\*zero cleaning, zero normalization, zero value translation, and zero cross-source heuristic deduplication\*\* were performed in this phase.



```text

Chợ Tốt Production Batches (3,116)

&#x20;              \\

&#x20;               \\

&#x20;                ──→  vehicles\_raw\_merged.json (10,813 records)

&#x20;               /

&#x20;              /

Bonbanh Production Batches (7,697)

```



\---



\## 2. Input Inventory



\### 2.1 Production Batches Loaded



| Platform | Batch File | Record Count | Unique URLs | Status |

| :--- | :--- | :--- | :--- | :--- |

| \*\*Chợ Tốt\*\* | `chotot\_raw\_production\_batch1.json` | 71 | 71 | Included |

| \*\*Chợ Tốt\*\* | `chotot\_raw\_production\_batch2.json` | 82 | 82 | Included |

| \*\*Chợ Tốt\*\* | `chotot\_raw\_production\_batch3.json` | 823 | 823 | Included |

| \*\*Chợ Tốt\*\* | `chotot\_raw\_production\_batch4.json` | 1,500 | 1,500 | Included |

| \*\*Chợ Tốt\*\* | `chotot\_raw\_production\_batch5.json` | 640 | 640 | Included |

| \*\*Chợ Tốt Subtotal\*\* | \*\*5 files\*\* | \*\*3,116\*\* | \*\*3,116\*\* | \*\*100% Unique\*\* |

| \*\*Bonbanh\*\* | `bonbanh\_raw\_production\_batch1.json` | 70 | 70 | Included |

| \*\*Bonbanh\*\* | `bonbanh\_raw\_production\_batch2.json` | 358 | 358 | Included |

| \*\*Bonbanh\*\* | `bonbanh\_raw\_production\_batch3.json` | 485 | 485 | Included |

| \*\*Bonbanh\*\* | `bonbanh\_raw\_production\_batch4.json` | 1,184 | 1,184 | Included |

| \*\*Bonbanh\*\* | `bonbanh\_raw\_production\_batch5.json` | 2,500 | 2,500 | Included |

| \*\*Bonbanh\*\* | `bonbanh\_raw\_production\_batch6.json` | 600 | 600 | Included |

| \*\*Bonbanh\*\* | `bonbanh\_raw\_production\_batch7.json` | 2,500 | 2,500 | Included |

| \*\*Bonbanh Subtotal\*\* | \*\*7 files\*\* | \*\*7,697\*\* | \*\*7,697\*\* | \*\*100% Unique\*\* |

| \*\*Total Production Raw\*\* | \*\*12 files\*\* | \*\*10,813\*\* | \*\*10,813\*\* | \*\*100% Unique\*\* |



\### 2.2 Excluded Files (Smoke Tests / Non-Production)



In strict accordance with Phase 3 instructions (Section 4), all early smoke-test runs were safely excluded from production merging:



| Excluded File | Source | Record Count | Reason for Exclusion |

| :--- | :--- | :--- | :--- |

| `chotot\_raw\_20260907\_132020.json` | Chợ Tốt | 5 | Phase 1 smoke test |

| `chotot\_raw\_20260907\_132201.json` | Chợ Tốt | 3 | Phase 1 smoke test |

| `bonbanh\_raw\_20260907\_140431.json` | Bonbanh | 5 | Phase 2 smoke test |

| `bonbanh\_raw\_20260907\_140805.json` | Bonbanh | 3 | Phase 2 smoke test |

| \*\*Total Excluded\*\* | \*\*4 files\*\* | \*\*16\*\* | \*\*Smoke tests excluded\*\* |



\---



\## 3. Merge Execution \& Statistics



The merge was orchestrated deterministically using `crawler/src/pipeline/merge\_pipeline.py`.



```text

================ MERGE AUDIT SUMMARY ================

Total input records read:        10,813

Exact duplicate source\_url:           0

Records removed:                      0

Final merged records:            10,813

=====================================================

```



\### 3.1 Source Distribution



| Source Platform | Origin Domain | Records | Percentage |

| :--- | :--- | :--- | :--- |

| \*\*Chợ Tốt Xe\*\* | `xe.chotot.com` | 3,116 | 28.82% |

| \*\*Bonbanh\*\* | `bonbanh.com` | 7,697 | 71.18% |

| \*\*Total\*\* | — | \*\*10,813\*\* | \*\*100.00%\*\* |



\### 3.2 URL Uniqueness Audit



\- Total records in merged dataset: \*\*10,813\*\*

\- Total unique `source\_url` values: \*\*10,813\*\*

\- Exact URL match ratio: \*\*100.00%\*\* (`unique source\_url count == final record count`)

\- Discarded / dropped records: \*\*0\*\*



\### 3.3 Ordering \& Determinism



The dataset was concatenated with strict determinism:

1\. Records 1 to 3,116: Chợ Tốt production batches 1 through 5 (in original order).

2\. Records 3,117 to 10,813: Bonbanh production batches 1 through 7 (in original order).



\---



\## 4. Schema Contract Audit



Every record was verified against the canonical 14-field data contract:



```text

14-field contract: PASS

Missing fields:    0

Extra fields:      0

Malformed records: 0

```



\### Canonical Field Specifications



| # | Field Name | Data Type | Description | Preservation Rule |

| :--- | :--- | :--- | :--- | :--- |

| 1 | `brand` | `str` / `null` | Vehicle manufacturer brand | Raw text preserved (e.g. `Toyota`, `HYUNDAI`, `Mercedes Benz`) |

| 2 | `model` | `str` / `null` | Vehicle model line | Raw text preserved (e.g. `Vios`, `SantaFe`, `Glc 300`) |

| 3 | `variant` | `str` / `null` | Trim level / specific edition | Raw text preserved (e.g. `1.5E`, `2.2L Dầu Cao Cấp`) |

| 4 | `manufacture\_year` | `int` / `null` | Year of manufacture | Integer year preserved |

| 5 | `price` | `int` / `null` | Listing price in VND | Exact integer or null preserved |

| 6 | `mileage` | `str` / `null` | Mileage string | Raw string preserved (e.g. `16,000 Km`, `50000 km`) |

| 7 | `fuel\_type` | `str` / `null` | Fuel engine type | Raw Vietnamese/mixed string preserved (e.g. `Xăng`, `Dầu`, `Hybrid`) |

| 8 | `transmission` | `str` / `null` | Gearbox transmission | Raw Vietnamese/mixed string preserved (e.g. `Số tự động`, `Tự động`, `Số sàn`) |

| 9 | `body\_type` | `str` / `null` | Vehicle chassis / body style | Raw string preserved (e.g. `Sedan`, `SUV`, `Crossover`) |

| 10 | `location` | `str` / `null` | Geographic location | Raw string preserved with diacritics (e.g. `Quận 7, Tp Hồ Chí Minh`, `Hà Nội`) |

| 11 | `source\_url` | `str` | Full canonical URL of listing | Exact URL preserved (used for lineage \& uniqueness) |

| 12 | `image\_url` | `str` / `null` | Primary listing vehicle photo | Raw CDN URL preserved |

| 13 | `listed\_at` | `str` / `null` | Original publish timestamp | Raw timestamp string preserved |

| 14 | `crawled\_at` | `str` | UTC ISO-8601 crawl timestamp | ISO timestamp preserved |



\---



\## 5. Output Artifacts



| Output File Path | Format | Size | Record Count | Role |

| :--- | :--- | :--- | :--- | :--- |

| `crawler/data/merged/vehicles\_raw\_merged.json` | JSON (UTF-8) | 6.13 MB | 10,813 | \*\*Canonical\*\* merged raw production dataset |

| `crawler/data/merged/vehicles\_raw\_merged.csv` | CSV (UTF-8) | 3.10 MB | 10,813 | \*\*Companion\*\* analytical export |



Both files reside in `crawler/data/merged/` (configured in `.gitignore` to prevent committing massive binary-like data files to the git history).



\---



\## 6. Scope Confirmation \& Boundaries



In compliance with Phase 3 instructions (Section 2 \& Section 15):



```text

Cleaning performed:                   NO (deferred to Phase 4)

Price cleaning / conversion:          NO (deferred to Phase 4)

Mileage cleaning / conversion:        NO (deferred to Phase 4)

Vehicle / brand normalization:        NO (deferred to Phase 4)

Missing-value imputation:             NO (deferred to Phase 4)

Outlier removal:                      NO (deferred to Phase 4)

Cross-source vehicle deduplication:   NO (distinct source URLs preserved)

Database import:                      NO (deferred to Phase 6)

Seed generation:                      NO (deferred to Phase 6)

Backend modification:                 NO

Frontend modification:                NO

```



\---



\## 7. Data Lineage



```text

&#x20;                               \[RAW PRODUCTION BATCHES]

&#x20;                               

&#x20;  xe.chotot.com (Chợ Tốt)                     bonbanh.com (Bonbanh)

&#x20;  ├── batch 1: 71 records                     ├── batch 1: 70 records

&#x20;  ├── batch 2: 82 records                     ├── batch 2: 358 records

&#x20;  ├── batch 3: 823 records                    ├── batch 3: 485 records

&#x20;  ├── batch 4: 1,500 records                  ├── batch 4: 1,184 records

&#x20;  └── batch 5: 640 records                    ├── batch 5: 2,500 records

&#x20;  Subtotal: 3,116 records                     ├── batch 6: 600 records

&#x20;                                              └── batch 7: 2,500 records

&#x20;                                              Subtotal: 7,697 records

&#x20;                   \\                                /

&#x20;                    \\                              /

&#x20;                     ▼                            ▼

&#x20;              ┌──────────────────────────────────────────┐

&#x20;              │    crawler/src/pipeline/merge\_pipeline.py│

&#x20;              │  - Exclude smoke tests (16 records)      │

&#x20;              │  - Validate 14-field canonical contract  │

&#x20;              │  - Deduplicate exact source\_url (0 dupes)│

&#x20;              │  - Preserve exact raw values             │

&#x20;              └────────────────────┬─────────────────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                    \[CANONICAL MERGED DATASET]

&#x20;            crawler/data/merged/vehicles\_raw\_merged.json

&#x20;                                +

&#x20;            crawler/data/merged/vehicles\_raw\_merged.csv

&#x20;                        (Total: 10,813 records)

```



\---



\## 8. Conclusion \& Readiness



\- \*\*Phase 3 Objective:\*\* Successfully accomplished.

\- \*\*Merged Production Volume:\*\* \*\*10,813 real vehicle listings\*\*.

\- \*\*Dataset Health:\*\* 100% compliant with schema; 0 duplicate URLs; 0 corrupted records.

\- \*\*Next Phase:\*\* \*\*Phase 4 — Data Cleaning \& Normalization\*\* (Ready to proceed).



