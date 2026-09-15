# Model Evaluation

Status: waiting for TV3 cleaned dataset.

Increment 1 prepares the source code, preprocessing contract, training script, evaluation script, and model-service structure. Official model metrics are intentionally not reported yet because they must come from the real cleaned dataset.

## Planned Model

- Version: `regression_v1`
- Algorithm: Linear regression on log price
- Target: `log(price)`
- Output price unit: VND

## Features

- `vehicle_age = listed_year - manufacture_year`
- `mileage_k = mileage / 1000`
- `engine_non_ev = 0` for electric cars, otherwise `engine_size`
- `fuel`
- `is_auto`
- `is_imported`
- `seat_count`

## Required Next Step

TV3 should provide `model/regression/data/training_data.csv` with the columns documented in `model/plumber/schemas/prediction_schema.json` plus `price` for training.

Predicted price is a reference market estimate, not a legal appraisal.
