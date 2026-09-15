# TV4 Plumber API Foundation

Increment 1 prepares the model API contract and basic service files. The API becomes fully ready after `model/regression/models/regression_v1.rds` is trained from TV3 data.

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
  "listed_year": 2026,
  "listed_month": 9,
  "mileage": 45000,
  "fuel_type": "Gasoline",
  "transmission": "Automatic",
  "origin": "Domestic",
  "engine_size": 1.5,
  "seat_count": 5
}
```

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
