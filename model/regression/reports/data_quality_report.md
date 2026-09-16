# TV4 Dataset Quality Report

Analysis date: 2026-09-17. This report analyzes the TV3 CSV in place; no row was edited, imputed, or copied into a training dataset.

## Dataset Identity

- Input: `crawler/data/cleaned/vehicles_cleaned.csv`
- Data Contract: TV3 v1.0.0, exactly 17 canonical columns in the documented order.
- Local snapshot: 10,813 records, 17 columns, 0 duplicate `source_url` values.
- Encoding: UTF-8 with BOM (`utf-8-sig`).
- Local SHA-256: `5a70b532173c897531440105b47ddccfb839198d631ea0375050c57010201b27`.
- TV3 Phase 1 lock report SHA-256: `bcec9df219fc7511a0f7ac2cf80bfffd1a6aa732144f99b15f8709e8d2ac3513`.

The local checksum differs from the value in the lock report. The schema, 10,813 record count, source distribution, and URL uniqueness match, so EDA is useful on this snapshot. TV3 must confirm this SHA-256 or publish a revised lock report before any official training/evaluation uses it.

## Parsing And Contract Checks

- `crawled_at`: 10,813 timezone-aware ISO-8601 values; no parsing failure. `observed_year = year(crawled_at)` and no negative `vehicle_age` were found.
- `listed_at`: raw source text only. It includes relative/listing text and is not a trustworthy timestamp feature.
- `price` is VND. `mileage` is km. `engine_size` is liters. `seat_count` is seats.
- Numeric values parsed for all non-null values. Their ranges are: price 5,000,000 to 33,000,000,000 VND; mileage 0 to 3,380,000,000 km; manufacture year 1980 to 2026; engine size 0.7 to 6.75 L; seats 2 to 36.
- The actual `body_type` data does not fully match the documented normalized vocabulary: `SUV` (3,797), `Crossover` (683), `Van / Minivan` (509), `Truck` (31), `Other` (29), and `Wagon` (4) require a TV3 normalization decision before this field is used as a candidate feature.

## Missingness And Distribution

See `feature_availability.csv` for all 17 fields. The model-impacting missing rates are mileage 21.34%, origin 85.31%, engine size 44.89%, and seat count 87.63%.

Fuel values are Gasoline 7,543, Diesel 1,565, Electric 1,204, Hybrid 500, and NULL 1. Transmission is Automatic 9,577, Manual 1,214, and NULL 22. Origin is Domestic 650, Imported 938, and NULL 9,225. The dataset has 1,204 Electric listings; all 1,204 have `engine_size = NULL`, none has zero or a positive engine size. This matches the TV3 rule and must remain distinct from the derived model representation `engine_non_ev = 0`.

Bonbanh provides 7,697 listings (71.18%) and Chotot provides 3,116 (28.82%). Mean observed price differs strongly by source: about 1.166 billion VND for Bonbanh and 568 million VND for Chotot. Source effects must be inspected in later evaluation rather than assuming a random split is representative.

## Quality Flags

- Price below 50 million VND: 68 rows.
- Price above 15 billion VND: 5 rows.
- Mileage above 1,000,000 km: 8 rows.
- Manufacture year before 1990: 11 rows.
- Vehicle age below zero: 0 rows.

These are TV4 training flags, not instructions to alter the crawler or database source of truth.

## Coverage And Sample Bias

| Strategy | Usable rows | Coverage | Interpretation |
|---|---:|---:|---|
| Strict legacy complete-case (requires raw engine size for all fuels) | 710 | 6.57% | Reference only; materially biased by missing origin/seat/engine. |
| Complete-case with documented Electric exception | 747 | 6.91% | Still severely biased; 37 Electric rows become eligible. |
| Reduced-feature candidate (`price`, year, observation year, mileage, fuel, transmission) | 8,407 | 77.75% | Better coverage, but loses origin/engine/seat information. |
| Missing-aware candidate after price/year/age quality exclusions | 8,428 | 77.94% | Preserves the broadest cohort; requires train-only transforms. |

Legacy complete-case coverage is 11.42% for Chotot (356/3,116) but only 4.60% for Bonbanh (354/7,697), so it is not representative of the full market. It also over-represents Toyota, Ford, Kia, Hyundai, Mercedes-Benz, Mazda, VinFast, and Mitsubishi. There are 38 brands and 278 models with fewer than 10 records, so high-cardinality brand/model encoding needs rare-category handling and group-aware evaluation.

## Runtime Status

`model/regression/eda_dataset.R` reproduces the availability CSV, distributions, breakdown CSV, Markdown summary, and PNG charts from the original CSV. R/Rscript is not installed in the current environment, so generated `eda/*.csv` and `eda/*.png` remain pending runtime execution. No official model, artifact, or metric was created.
