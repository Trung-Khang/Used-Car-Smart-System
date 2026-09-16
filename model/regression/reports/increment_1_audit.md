# TV4 Increment 1 Audit and Handoff

Date: 2026-09-17  
Scope: TV4 regression foundation and Plumber contract only.

## Verdict

Increment 1 is **achieved as a source-code foundation**. It contains the regression directory layout, preprocessing and metric modules, separated train/test scripts, a fixture-only smoke path, and a Plumber `/health` and `/predict` skeleton. No official model artifact, evaluation result, or reported model metric exists.

Runtime smoke verification is **pending** because `Rscript` was not available in the audit environment. Existing fixture outputs are not evidence for the project model and must not be copied into the thesis, slides, or demo claims.

## Confirmed Data Contract

| Field | TV4 use | Contract |
|---|---|---|
| `price` | Training target | VND; observed listing price; never a prediction feature. |
| `manufacture_year` | Feature input | Integer. |
| `crawled_at` | Training observation time | ISO-8601 with timezone; `observed_year = year(crawled_at)`. |
| `mileage` | Feature input | km; nullable in the source. |
| `fuel_type` | Feature input | `Gasoline`, `Diesel`, `Hybrid`, `Electric`, or NULL. |
| `transmission` | Feature input | `Automatic`, `Manual`, `CVT`, or NULL. |
| `origin` | Feature input | `Domestic`, `Imported`, or NULL. |
| `engine_size` | Feature input | Liters; nullable, including Electric vehicles. Raw NULL is preserved and derived `engine_non_ev` is 0 for Electric only. |
| `seat_count` | Feature input | Integer seats; nullable. |
| `brand`, `model`, `variant` | Identifier / future feature candidates | Not inputs to `regression_v1` formula. |
| `source_url` | Provenance | Never a model feature. |
| `listed_at` | Source text | Not used until a trustworthy absolute-time parser exists. |

`listed_year` is not a TV3 field and is no longer required by the TV4 source contract. It is replaced by `observed_year`; this name prevents confusing crawl observation time with the seller's actual publication year.

## Dataset Audit

TV3 Phase 1 lock supplies 10,813 records and the exact 17-field contract. Required source fields are present and `source_url` is unique. Current authentic null counts that affect the baseline model are: `mileage` 2,307, `fuel_type` 1, `transmission` 22, `origin` 9,225, `engine_size` 4,854, and `seat_count` 9,475.

The categorical values match the agreed vocabulary after NULL handling: fuel has Gasoline, Diesel, Electric, Hybrid; transmission has Automatic and Manual plus NULL; origin has Domestic, Imported, plus NULL. The old strict complete-case check finds about 715 rows before its range filtering; the TV3 handoff review reports about 710 eligible rows after the old regression ranges. This is too small to present as an approved official-model cohort without EDA.

## Mismatches Fixed

- Replaced obsolete required `listed_year` with `observed_year`; training derives it from `crawled_at`.
- Renamed age feature documentation to `vehicle_age = observed_year - manufacture_year`.
- Replaced the fixture-only `trim` identifier with the canonical optional `variant` reference.
- Made the request schema allow `engine_size: null` for Electric vehicles; non-Electric records remain rejected if it is unavailable.
- Changed preprocessing from dataset-wide failure on any malformed/missing row to row-level filtering in the batch path. Strict prediction still returns a clear validation error for an invalid payload.
- Updated stale documentation that said TV4 was waiting for TV3 data; the actual gate is now Increment 2 feature coverage and modelling decisions.

## Increment 2 Decisions

Do not train or publish `regression_v1` until TV4 documents and the group reviews:

1. EDA by source, brand/model, price, year, mileage, and the missingness pattern.
2. A justified handling policy for missing `origin`, `engine_size`, `seat_count`, and `mileage`; database NULL must remain source-truth.
3. Outlier treatment for prices below 50 million VND, above 15 billion VND, mileage above 1,000,000 km, and manufacture years before 1990.
4. A reproducible train/test split and model comparison/evaluation protocol.
5. Whether brand/model/variant and body type should be included, encoded, or deliberately excluded.

## Confirmations Requested From TV3

- Confirm the Phase 1 lock checksum/version is the dataset TV4 must use for EDA and later training.
- Notify TV4 whenever enrichment changes `origin`, `engine_size`, or `seat_count`, and provide a new version/checksum plus field-completeness counts.
- Keep `crawled_at` timezone-aware ISO-8601 and do not synthesize a `listed_year` column.
- Preserve NULL for unavailable attributes and do not infer origin, engine size, or seat count for ML convenience.

## Smoke-Test Status

`train_model.R --smoke` is the designated fixture smoke command. It uses a separate fixture input, fixture artifact (`regression_v1_fixture.rds`), and fixture metrics/report. It cannot produce the official artifact path. The Plumber service reports `waiting_for_model` without `regression_v1.rds`, and `/predict` is designed to return structured HTTP 503 in that state. These assertions received static review only; runtime execution is pending installation of R/Rscript and the Plumber dependencies.

Predicted price is a market reference, not a legal appraisal.
