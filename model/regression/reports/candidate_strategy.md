# TV4 Candidate Preprocessing Strategy

Status: proposal for Increment 2. No strategy is official and no candidate has been evaluated in this environment.

## Separation Of Responsibilities

1. Schema validation checks exactly 17 TV3 columns, types, timestamp format, and URL uniqueness. It does not discard source data.
2. Row-level flags identify missing values and training-range anomalies. Flags are preserved for reporting.
3. A candidate's training exclusion rule selects rows only after the data split policy is chosen.
4. Prediction transformation validates a single request, uses a fitted transformer, and never changes crawler/database NULL values.

`candidate_preprocessing.R` implements the first two layers and train-only `fit_missing_transformer()` / `apply_missing_transformer()` scaffolding. The transformer must be fit on training rows only, then applied unchanged to validation/test rows and future prediction requests.

## Candidates

| Candidate | Inputs | Missing strategy | Coverage | Tradeoff |
|---|---|---|---:|---|
| A. Complete-case reference | age, mileage, fuel, transmission, origin, engine, seats | Drop any missing model feature; Electric engine NULL maps only to derived zero | 747 rows with EV exception; 710 under legacy raw complete-case | Simple and explainable, but source/brand/fuel biased and too small for a production decision. |
| B. Reduced-feature baseline | age, mileage, fuel, transmission; optionally broad body type after TV3 normalization | Drop missing mileage/fuel/transmission and training outliers | 8,407 rows | Good coverage and simple user form. It intentionally omits origin, engine size, and seats, losing relevant signal. |
| C. Missing-aware candidate | age, mileage, fuel, transmission, origin, engine, seats, optional body/brand/model | Training-median numeric imputation plus missing indicators; categorical `Unavailable`; Electric engine derived to 0 only in feature matrix | 8,428 rows before train-only transformations | Best coverage but requires careful explainability, rare-category handling, and test-set leakage controls. |

Do not select C merely because it has more rows. Compare hold-out error, residual fairness by source/fuel/age/price band, form coverage, and calibration against A/B.

## Leakage-Safe Evaluation Protocol

- Remove exact duplicate `source_url` before splitting and record the count (currently zero).
- Set and record a seed. Use an initial 80/20 train/test split.
- Prefer a group split by `brand + model + manufacture_year` for the final comparison, because random split can put the same configuration in train and test. Report both random and group-split results if data volume allows.
- Fit medians, category levels, rare-category buckets, and any encoding only on the training split.
- Apply the frozen transformer to test rows. Compute R2, MAE, RMSE, and MAPE only on that untouched test set.
- Report residuals by price band, fuel, vehicle-age band, and source where group sizes are sufficient. MAPE must be caveated because relative error is unstable for low-price listings.
- Never use `price` as an input feature. It is the training target only.

## Candidate Evaluation Gate

The current machine lacks R/Rscript, so no candidate metric is reported. After runtime is available, evaluate candidates under the protocol above with output names such as `candidate_a_complete_case_metrics.csv`; never overwrite `regression_v1.rds`, `metrics.csv`, or the official evaluation report.
