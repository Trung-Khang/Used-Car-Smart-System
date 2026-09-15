regression_metrics <- function(actual_price, predicted_price) {
  actual_price <- as.numeric(actual_price)
  predicted_price <- as.numeric(predicted_price)

  valid <- is.finite(actual_price) & is.finite(predicted_price) & actual_price > 0
  actual_price <- actual_price[valid]
  predicted_price <- predicted_price[valid]

  if (!length(actual_price)) {
    stop("No valid rows available for metric calculation", call. = FALSE)
  }

  residual <- actual_price - predicted_price
  sse <- sum(residual^2)
  sst <- sum((actual_price - mean(actual_price))^2)

  data.frame(
    metric = c("R2", "RMSE", "MAE", "MAPE"),
    value = c(
      ifelse(sst == 0, NA_real_, 1 - sse / sst),
      sqrt(mean(residual^2)),
      mean(abs(residual)),
      mean(abs(residual / actual_price)) * 100
    ),
    unit = c("ratio", "VND", "VND", "percent"),
    stringsAsFactors = FALSE
  )
}

write_metrics_report <- function(metrics, output_file, context) {
  lines <- c(
    "# Model Evaluation",
    "",
    sprintf("- Model version: `%s`", context$model_version),
    sprintf("- Dataset: `%s`", context$dataset),
    sprintf("- Generated at: `%s`", context$generated_at),
    sprintf("- Train rows: `%s`", context$n_train),
    sprintf("- Test rows: `%s`", context$n_test),
    sprintf("- Split method: `%s`", context$split_method),
    "",
    "## Metrics",
    "",
    "| Metric | Value | Unit |",
    "|---|---:|---|",
    apply(metrics, 1, function(row) {
      sprintf("| %s | %.6f | %s |", row[["metric"]], as.numeric(row[["value"]]), row[["unit"]])
    }),
    "",
    "## Features",
    "",
    "- vehicle_age = listed_year - manufacture_year",
    "- mileage_k = mileage / 1000",
    "- engine_non_ev = 0 for Electric, otherwise engine_size",
    "- fuel encoded as categorical with levels Gasoline, Diesel, Hybrid, Electric",
    "- is_auto = 1 for Automatic or CVT",
    "- is_imported = 1 for Imported",
    "- seat_count as numeric seat count",
    "",
    "## Notes",
    "",
    "- Predicted price is a reference market estimate, not a legal appraisal.",
    "- Official metrics must be regenerated from TV3 cleaned data before demo."
  )

  writeLines(lines, output_file, useBytes = TRUE)
}
