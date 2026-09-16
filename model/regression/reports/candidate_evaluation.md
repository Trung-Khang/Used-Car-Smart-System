# Candidate Evaluation Status

Status: **not run**. This is not an official evaluation report.

The current environment has no `Rscript`, so no candidate was fitted and no R2, MAE, RMSE, MAPE, residual, train/test, or prediction-coverage metric is claimed.

When R is available, every candidate report must include:

- dataset SHA-256 and input row count;
- candidate name, exact feature list, missing strategy, and exclusion count by reason;
- seed, split ratio, train/test counts, and whether random or group split was used;
- test-only R2, MAE, RMSE, and MAPE with a low-price limitation note;
- residual summaries by price band, fuel type, and vehicle-age band where group size is adequate;
- the percent of all listings and user-form payloads that the candidate can predict.

Candidate artifacts and metric files must be named `candidate_*`; they must not overwrite official `regression_v1.rds`, `metrics.csv`, or `model_evaluation.md`.
