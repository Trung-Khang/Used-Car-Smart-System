# Model Evaluation

Status: no official model or metrics.

Increment 1 prepares the source code, preprocessing contract, training script, evaluation script, and model-service structure. TV3's real cleaned dataset is available, but official metrics are intentionally not reported until Increment 2 completes EDA and approves how authentic missing values and outliers are handled.

## Planned Model

- Version: `regression_v1`
- Algorithm: Linear regression on log price
- Target: `log(price)`
- Output price unit: VND

## Features

- `observed_year = year(crawled_at)`
- `vehicle_age = observed_year - manufacture_year`
- `mileage_k = mileage / 1000`
- `engine_non_ev = 0` for electric cars, otherwise `engine_size`
- `fuel`
- `is_auto`
- `is_imported`
- `seat_count`

## Required Next Step

Run Increment 2 EDA on `crawler/data/cleaned/vehicles_cleaned.csv`, document feature coverage, choose and review a missing-feature/outlier policy, then create a versioned train/test evaluation. Fixture metrics remain smoke-test evidence only.

Predicted price is a reference market estimate, not a legal appraisal.
