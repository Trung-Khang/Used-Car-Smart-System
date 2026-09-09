# Data Dictionary — Increment 1

## VEHICLE

| Field | Type | Key | Description |
|---|---|---|---|
| vehicle_id | BIGSERIAL | PK | Unique vehicle identifier |
| make | VARCHAR(100) | | Vehicle manufacturer |
| model | VARCHAR(100) | | Vehicle model |
| year | INTEGER | | Vehicle year |
| mileage | NUMERIC(12,2) | | Vehicle mileage |
| fuel | VARCHAR(50) | | Fuel type |
| transmission | VARCHAR(50) | | Transmission type |
| listing_price | NUMERIC(14,2) | | Market/listing price |
| predicted_price | NUMERIC(14,2) | | Price predicted by the regression model |
| difference_percent | NUMERIC(8,2) | | Percentage difference used by valuation logic |
| model_version | VARCHAR(50) | | Version of the model producing the prediction |
| source_url | TEXT | | Original listing source |
| created_at | TIMESTAMP | | Record creation time |
| updated_at | TIMESTAMP | | Last update time |

## VEHICLE_COMPARISON

| Field | Type | Key | Description |
|---|---|---|---|
| comparison_id | BIGSERIAL | PK | Unique comparison |
| created_at | TIMESTAMP | | Comparison creation time |

## COMPARISON_VEHICLE

| Field | Type | Key | Description |
|---|---|---|---|
| comparison_id | BIGINT | PK/FK | Comparison reference |
| vehicle_id | BIGINT | PK/FK | Selected vehicle reference |

## Validation notes
- `make` and `model` are required in the proposed foundation schema.
- `year`, `mileage`, and prices should be validated by the backend.
- `difference_percent` should be calculated consistently by the pricing workflow.
- `model_version` should identify the model version used for a prediction.
