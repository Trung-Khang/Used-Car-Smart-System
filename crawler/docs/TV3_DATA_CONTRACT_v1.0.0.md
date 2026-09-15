# TV3 DATA CONTRACT v1.0.0

**Project:** Used-Car-Smart-System  
**Owner:** TV3 — Data Engineering / Data Pipeline  
**Status:** Phase 1 Synchronization — LOCKED FOR HANDOFF  
**Contract scope:** Final cleaned dataset, not PostgreSQL schema

## 1. Link to Phase 0

Phase 0 identified the blocking mismatch: the repository implementation still validated/generated the old 14-field contract while the existing cleaned dataset already contained 17 fields. Phase 1 resolves that mismatch at the TV3 source/pipeline boundary without redesigning the database.

- Existing merged/raw boundary: **14 fields**.
- Final cleaned boundary after enrichment: **17 fields**.
- Dataset version: **v1.0.0**.
- No new crawling was required for synchronization.

## 2. Contract fields

| # | Field | Type | Unit | Null | Rule / provenance |
|---|---|---|---|---|---|
| 1 | `brand` | string | — | No | Normalized source manufacturer |
| 2 | `model` | string | — | No | Normalized source model |
| 3 | `variant` | string | — | Yes | Seller-provided trim/edition |
| 4 | `manufacture_year` | integer | year | No | 1980–2026 |
| 5 | `price` | integer | VND | No | Observed listing price; 5M–33B in current dataset |
| 6 | `mileage` | integer | km | Yes | Non-negative; no model-specific outlier deletion by TV3 |
| 7 | `fuel_type` | categorical | — | Yes | `Gasoline`, `Diesel`, `Electric`, `Hybrid` |
| 8 | `transmission` | categorical | — | Yes | `Automatic`, `Manual`, `CVT` |
| 9 | `body_type` | categorical | — | Yes | `Sedan`, `SUV / Crossover`, `Hatchback`, `Pickup`, `MPV`, `Van`, `Coupe`, `Convertible`, `Truck`, `Wagon` |
| 10 | `location` | string | — | No | Cleaned source location |
| 11 | `origin` | categorical | — | Yes | `Domestic` / `Imported`; source-explicit only |
| 12 | `engine_size` | float | L | Yes | Explicit displacement only; no inference |
| 13 | `seat_count` | integer | seats | Yes | Explicit seating only; no inference |
| 14 | `source_url` | string | URL | No | Absolute source URL; unique |
| 15 | `image_url` | string | URL | Yes | Absolute media URL |
| 16 | `listed_at` | string | — | Yes | Preserve source relative text when not an absolute date |
| 17 | `crawled_at` | string | ISO 8601 | No | Timezone-aware observation timestamp |

### Contract vocabulary status

The normalization targets above are the **TV3 operational vocabulary**. They are not a declaration of PostgreSQL schema ownership. Final cross-team acceptance by TV1/TV4/TV5 remains a handoff/review item where required.

`SUV` and `Crossover` are normalized to `SUV / Crossover`. `Van / Minivan` is normalized to `Van`. Explicit `Truck` and `Wagon` values are retained. Unresolvable `Other` values are represented as `null` rather than fabricated categories.

## 3. Pipeline boundary

```text
Chợ Tốt / Bonbanh
        ↓
raw crawler output
        ↓
14-field pre-enrichment merge
        ↓
cleaning / normalization
        ↓
explicit enrichment: origin / engine_size / seat_count
        ↓
17-field final validation (this contract)
        ↓
JSON / CSV clean dataset
        ↓
seed/import preparation
```

`merge_pipeline.py` intentionally remains 14-field. `clean_pipeline.py` now preserves enrichment fields when they are already present, so re-running cleaning cannot silently delete `origin`, `engine_size`, or `seat_count`.

`enrich_pipeline.py` now validates the final 17-field record set before writing the canonical cleaned files.

## 4. Current dataset quality evidence

- Records: **10,813**
- Bonbanh: **7,697**
- Chợ Tốt: **3,116**
- Fields per record: **17**
- Unique `source_url`: **10,813 / 10,813**
- Duplicate `source_url`: **0**
- Contract validation errors: **0**
- Records removed during synchronization: **0**

### Null counts

| Field | Nulls |
|---|---:|
| `brand` | 0 |
| `model` | 0 |
| `variant` | 1,473 |
| `manufacture_year` | 0 |
| `price` | 0 |
| `mileage` | 2,307 |
| `fuel_type` | 1 |
| `transmission` | 22 |
| `body_type` | 1,090 |
| `location` | 0 |
| `origin` | 9,225 |
| `engine_size` | 4,854 |
| `seat_count` | 9,475 |
| `source_url` | 0 |
| `image_url` | 0 |
| `listed_at` | 1 |
| `crawled_at` | 0 |

Missing enrichment values remain `null`; TV3 does not perform ML imputation.

## 5. Checksums

Generated from the synchronized working tree:

| Artifact | SHA-256 |
|---|---|
| `crawler/data/cleaned/vehicles_cleaned.json` | `93bb9cab4daa06edca528a89a6dfda9edd889554bdfdecb202e007b5900da916` |
| `crawler/data/cleaned/vehicles_cleaned.csv` | `bcec9df219fc75116cfd1d433d5f1a12509a5cccc11c1b87a49abf18a8eede8f` |
| `crawler/data/seed/vehicles_seed.json` | `f5b40c000f1903f8fc33c51cd0c21411bfb6dd8800c0a6ede86a45f5a2db1f2c` |
| `crawler/data/seed/vehicles_seed.csv` | `f3945048645a1051a0f7ac2cf80bfffd1a6aa732144f99b15f8709e8d2ac3513` |
| `crawler/data/seed/vehicles_seed.sql` | `e0878e345d6d72dca156e1a57cbaba3751f0e380ddc86dacdd2f8077c6484cf8` |

## 6. Seed/import boundary

Seed records contain the 17 contract fields plus deterministic `id` and derived `source`, for **19 seed fields** total.

The SQL artifact is now **data-only**. It intentionally contains no `CREATE TABLE` or competing DDL. TV5 remains the authoritative owner of table/PK/FK/schema design. Physical import is pending TV5 schema deployment/acceptance.

## 7. Phase 1 acceptance

- [x] 17-field contract defined and versioned.
- [x] Validator synchronized to 17 fields.
- [x] Cleaning preserves enrichment fields.
- [x] Enrichment has a final 17-field validation gate.
- [x] Final JSON/CSV validated.
- [x] Seed JSON/CSV preserve all 17 contract fields.
- [x] SQL seed no longer emits competing DDL.
- [x] Dataset count and URL uniqueness preserved.
- [x] Checksums recorded.
- [ ] TV1/TV4/TV5 cross-team vocabulary confirmation — handoff item, not silently assumed.
- [ ] TV5 physical DB import — Phase 2/3/4 dependency, not performed in Phase 1.
