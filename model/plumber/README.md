# TV4 Plumber API Foundation

Increment 1 prepares the model API contract and basic service files. `GET /health` reports `waiting_for_model` and `POST /predict` returns a structured `503` error until an official artifact exists.

## Run API

```powershell
& "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" -e "plumber::pr('model/plumber/plumber.R')$run(host='0.0.0.0', port=8004)"
```

## Endpoints

- `GET /health`
- `POST /predict`

Example request:

```json
{
  "brand": "Toyota",
  "model": "Vios",
  "manufacture_year": 2021,
  "observed_year": 2026,
  "mileage": 45000,
  "fuel_type": "Gasoline",
  "transmission": "Automatic",
  "origin": "Domestic",
  "engine_size": 1.5,
  "seat_count": 5
}
```

`observed_year` is the year at which the vehicle is valued. For TV3 training rows it is derived from timezone-aware `crawled_at`; it is not the seller's publication year. `engine_size` may be `null` only for `Electric` payloads. The current `regression_v1` contract still requires the other model features, so production prediction remains pending Increment 2 missing-feature decisions.

Example success response:

```json
{
  "predicted_price": 495000000,
  "currency": "VND",
  "model_version": "regression_v1",
  "preprocessing_version": "preprocessing_v1",
  "predicted_at": "2026-09-07T10:00:00+0700"
}
```
