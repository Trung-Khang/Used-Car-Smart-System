# TV4 Model Service

This module belongs to Member 04 and contains the R regression foundation plus Plumber API contract for used-car price prediction.

## Increment 1 Status

Done:

- Regression folder structure
- Feature contract
- Preprocessing source
- Train/test/evaluation scripts
- Placeholder official metrics/report waiting for TV3 data
- Plumber API skeleton with `/health` and `/predict`
- Fixture dataset for smoke testing only

Waiting:

- TV3 cleaned training dataset
- Official `regression_v1.rds`
- Official model metrics regenerated from real data
- Local R package `plumber` for running the HTTP API

## R Dependencies

Base regression scripts use base R only.

The Plumber API needs:

```r
install.packages(c("plumber", "jsonlite"))
```

## Smoke Test

```powershell
& "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" model/regression/train_model.R --smoke
```

Fixture outputs are ignored by git because they are not official project results.
