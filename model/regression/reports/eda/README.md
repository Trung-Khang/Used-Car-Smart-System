# EDA Outputs

Run `Rscript model/regression/eda_dataset.R` from the repository root after installing R. The script reads `crawler/data/cleaned/vehicles_cleaned.csv` directly and creates these reproducible outputs here:

- `numeric_summary.csv`
- category distributions for fuel, transmission, origin, and body type
- `complete_case_breakdown.csv`
- `missingness.png`, `price_distribution.png`, `mileage_distribution.png`, and `vehicle_age_distribution.png`

No input data is copied, changed, or imputed by this command. Runtime generation is pending because this environment has no `Rscript`.
