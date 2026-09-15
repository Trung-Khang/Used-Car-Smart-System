# TV3 — PHASE 1 SYNCHRONIZATION LOCK REPORT

**Project:** Used-Car-Smart-System  
**Owner:** TV3 — Data Engineering / Crawler / Data Pipeline  
**Phase:** Phase 1 — Data Contract Synchronization  
**Contract:** `v1.0.0`  
**Status:** **PASS — LOCKED FOR CROSS-TEAM HANDOFF**

## 1. Phase 0 → Phase 1 traceability

Phase 0 identified the blocker: the existing final dataset had 17 fields while the validator, cleaning pipeline and seed/import pipeline still implemented the old 14-field contract. Phase 1 synchronized those TV3 source components to the 17-field final contract while preserving the 14-field merged/raw boundary.

No additional crawl was required.

## 2. Source changes completed

### Contract / validation

- `crawler/src/cleaning/validator.py`
  - Added `DATA_CONTRACT_VERSION = "1.0.0"`.
  - Final `CANONICAL_FIELDS` is exactly 17 fields.
  - Added expected types, nullable handling, categorical vocabulary checks and integrity ranges.
  - Enforced timezone-aware ISO 8601 for `crawled_at`.
  - Enforced unique `source_url` at dataset level.
  - Kept the 14-field `PRE_ENRICHMENT_FIELDS` boundary explicit.

### Cleaning

- `crawler/src/cleaning/clean_vehicle.py`
  - Preserves `origin`, `engine_size`, `seat_count`.
  - Normalizes `SUV`/`Crossover` → `SUV / Crossover`.
  - Normalizes `Van / Minivan` → `Van`.
  - Unresolvable categorical values become `null` instead of synthetic `Other`.
  - No inference or ML imputation was added.

- `crawler/src/pipeline/clean_pipeline.py`
  - Uses the shared 17-field contract.
  - Can process the 14-field merged input and emits the 17-field shape with enrichment fields initially null.
  - If a 17-field dataset is re-cleaned, enrichment fields are preserved.

- `crawler/src/pipeline/enrich_pipeline.py`
  - Uses the shared canonical field order.
  - Added a final 17-field validation gate before writing the canonical cleaned dataset.
  - Record count is guarded against unexpected changes.

### Merge boundary

- `crawler/src/pipeline/merge_pipeline.py`
  - Remains intentionally 14-field because it is the **pre-enrichment** boundary.
  - No DB schema was introduced here.

### Seed / import preparation

- `crawler/src/pipeline/import_pipeline.py`
  - Seed now preserves all 17 cleaned fields.
  - Seed shape is 19 fields: `id`, `source` + 17 contract fields.
  - SQL output is data-only; TV3 no longer emits `CREATE TABLE` DDL.
  - Physical DB import remains dependent on TV5's authoritative schema.

### Documentation / tests

- `crawler/README.md` synchronized with the v1.0.0 final contract.
- `crawler/docs/TV3_DATA_CONTRACT_v1.0.0.md` created as the handoff contract.
- `crawler/tests/test_phase1_data_contract.py` created with 5 contract/preservation/seed tests.
- `crawler/data/quality_report/phase1_final_validation_report.json` created.
- Phase-specific cleaning/seed reports regenerated.

## 3. Final dataset evidence

- Records: **10,813**
- Bonbanh: **7,697**
- Chợ Tốt: **3,116**
- Fields: **17**
- Unique `source_url`: **10,813 / 10,813**
- Duplicate `source_url`: **0**
- Contract validation errors: **0**
- Records removed during synchronization: **0**
- JSON ↔ CSV value parity: **PASS**
- Cleaned → seed contract value parity: **PASS**
- SQL contains `CREATE TABLE`: **NO**

## 4. Null policy evidence

Missing values remain authentic `null` values. Current counts:

- `variant`: 1,473
- `mileage`: 2,307
- `fuel_type`: 1
- `transmission`: 22
- `body_type`: 1,090
- `origin`: 9,225
- `engine_size`: 4,854
- `seat_count`: 9,475
- `listed_at`: 1
- Required fields `brand`, `model`, `manufacture_year`, `price`, `location`, `source_url`, `crawled_at`: 0 nulls.

## 5. Verification commands/results

### Syntax

```text
python -m py_compile crawler/src/cleaning/validator.py \
  crawler/src/cleaning/clean_vehicle.py \
  crawler/src/pipeline/clean_pipeline.py \
  crawler/src/pipeline/enrich_pipeline.py \
  crawler/src/pipeline/import_pipeline.py
```

**Result:** PASS

### TV3 Phase 1 unit tests

```text
PYTHONPATH=crawler/src python -m unittest discover -s crawler/tests -v
```

**Result:** 5 tests, 5 passed, 0 failed.

### Final dataset audit

**Result:** PASS — 10,813 records, 17 fields, 10,813 unique URLs, 0 validation errors.

### Merged → cleaned compatibility check

The 14-field merged dataset was processed into a temporary 17-field cleaned dataset without record loss. The three enrichment fields were correctly introduced as `null` before enrichment.

**Result:** PASS — 10,813 records, 17 fields, 0 records removed.

## 6. Checksums

- `vehicles_cleaned.json`: `93bb9cab4daa06edca528a89a6dfda9edd889554bdfdecb202e007b5900da916`
- `vehicles_cleaned.csv`: `bcec9df219fc7511a0f7ac2cf80bfffd1a6aa732144f99b15f8709e8d2ac3513`
- `vehicles_seed.json`: `f5b40c000f1903f8fc33c51cd0c21411bfb6dd8800c0a6ede86a45f5a2db1f2c`
- `vehicles_seed.csv`: `f3945048645a1051a0f7ac2cf80bfffd1a6aa732144f99b15f8709e8d2ac3513`
- `vehicles_seed.sql`: `e0878e345d6d72dca156e1a57cbaba3751f0e380ddc86dacdd2f8077c6484cf8`

## 7. Scope guard

TV3 Phase 1 did **not**:

- redesign PostgreSQL tables;
- choose PK/FK architecture for TV5;
- perform physical DB import;
- perform ML outlier filtering;
- perform ML imputation;
- change backend/API ownership;
- add synthetic vehicle data;
- infer `origin`, `engine_size`, or `seat_count` from unrelated fields.

## 8. Remaining cross-team gates

These are intentionally not silently resolved by TV3:

1. TV1/TV4/TV5 confirm the operational categorical vocabulary.
2. TV5 accepts/deploys the authoritative PostgreSQL schema.
3. Phase 3/4 can then perform physical import and integration verification.

**Phase 1 verdict: PASS / LOCKED.**
