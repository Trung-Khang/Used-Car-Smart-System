source("model/regression/src/preprocessing.R", encoding = "UTF-8")
source("model/regression/src/metrics.R", encoding = "UTF-8")

parse_arg <- function(name, default = NULL) {
  args <- commandArgs(trailingOnly = TRUE)
  prefix <- paste0("--", name, "=")
  hit <- args[startsWith(args, prefix)]
  if (!length(hit)) return(default)
  sub(prefix, "", hit[[1]], fixed = TRUE)
}

input_file <- parse_arg("input", "model/regression/data/training_data.csv")
model_file <- parse_arg("model", "model/regression/models/regression_v1.rds")
metrics_file <- parse_arg("metrics", "model/regression/reports/metrics_external.csv")

if (!file.exists(model_file)) {
  stop(sprintf("Model artifact not found: %s", model_file), call. = FALSE)
}

if (!file.exists(input_file)) {
  stop(sprintf("Evaluation dataset not found: %s", input_file), call. = FALSE)
}

artifact <- readRDS(model_file)
raw_df <- read.csv(input_file, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM")
df <- prepare_model_features(raw_df, require_price = TRUE, drop_incomplete = TRUE)

predicted_price <- exp(predict(artifact$model, newdata = df))
metrics <- regression_metrics(df$price, predicted_price)
metrics$model_version <- artifact$model_version
metrics$dataset <- input_file
metrics$n_train <- NA_integer_
metrics$n_test <- nrow(df)
metrics$generated_at <- format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z")
metrics <- metrics[, c("model_version", "dataset", "metric", "value", "unit", "n_train", "n_test", "generated_at")]

dir.create(dirname(metrics_file), recursive = TRUE, showWarnings = FALSE)
write.csv(metrics, metrics_file, row.names = FALSE, fileEncoding = "UTF-8")
cat(sprintf("Saved evaluation metrics: %s\n", metrics_file))
