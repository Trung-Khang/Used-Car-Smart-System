# TV4 Regression Foundation

This folder contains the Increment 1 foundation for the used-car valuation model.

The official model is not trained yet because TV4 is waiting for TV3 cleaned data. The small CSV in `data/fixture_used_cars.csv` exists only for smoke testing the pipeline shape.

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

## Train With TV3 Data

Place the cleaned dataset from TV3 at:

```text
model/regression/data/training_data.csv
```

Then run:

```powershell
& "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" model/regression/train_model.R
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
