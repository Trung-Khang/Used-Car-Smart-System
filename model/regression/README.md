# TV4 Regression Foundation

This folder contains the Increment 1 foundation for the used-car valuation model.

The official model is not trained. TV3's 17-field cleaned dataset is available, but its authentic missing values require EDA and an approved missing-feature strategy in Increment 2. The small CSV in `data/fixture_used_cars.csv` exists only for smoke testing the pipeline shape.

## Expected Structure

```text
model/regression/
  data/
  src/
  models/
  reports/
  train_model.R
  evaluate_model.R
```

## Official Training Gate

The authoritative input is:

```text
crawler/data/cleaned/vehicles_cleaned.csv
```

Do not create `regression_v1.rds` until the Increment 2 EDA, exclusion/imputation rules, and split strategy are reviewed. When that gate is accepted, run with an explicit input path:

```powershell
& "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" model/regression/train_model.R --input=crawler/data/cleaned/vehicles_cleaned.csv
```

Output:

```text
model/regression/models/regression_v1.rds
model/regression/reports/metrics.csv
model/regression/reports/model_evaluation.md
```

## Smoke Test Only

```powershell
& "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" model/regression/train_model.R --smoke
```

This writes `regression_v1_fixture.rds` and fixture metrics. These artifacts are not official demo metrics.

## Contract

- `price` is the VND target for training.
- `observed_year = year(crawled_at)`; it replaces the obsolete `listed_year` input.
- `vehicle_age = observed_year - manufacture_year`.
- `mileage` is km; `engine_size` is liters; `seat_count` is seats.
- Allowed categories are `Gasoline`, `Diesel`, `Hybrid`, `Electric`; `Automatic`, `Manual`, `CVT`; and `Domestic`, `Imported`.
- `source_url`, `image_url`, `listed_at`, brand/model/variant are provenance or future-feature candidates, not regression_v1 numeric inputs.
- An Electric source record may have `engine_size = NULL`; preprocessing derives `engine_non_ev = 0` without changing the raw value.

## Increment 2 EDA

Run the reproducible EDA directly against the TV3 canonical CSV:

```powershell
& "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" model/regression/eda_dataset.R
```

It writes field availability, quality summaries, category/numeric breakdowns, and PNG charts under `reports/` and `reports/eda/`. It does not modify or copy the TV3 dataset, train a model, or publish metrics. Read `reports/data_quality_report.md` and `reports/candidate_strategy.md` before evaluating an experimental candidate.
