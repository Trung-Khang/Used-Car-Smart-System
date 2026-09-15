source("model/regression/src/preprocessing.R", encoding = "UTF-8")
source("model/regression/src/metrics.R", encoding = "UTF-8")

parse_arg <- function(name, default = NULL) {
  args <- commandArgs(trailingOnly = TRUE)
  prefix <- paste0("--", name, "=")
  hit <- args[startsWith(args, prefix)]
  if (!length(hit)) return(default)
  sub(prefix, "", hit[[1]], fixed = TRUE)
}

has_flag <- function(name) {
  paste0("--", name) %in% commandArgs(trailingOnly = TRUE)
}

input_file <- parse_arg("input", "model/regression/data/training_data.csv")
output_model <- parse_arg("output", "model/regression/models/regression_v1.rds")
metrics_file <- parse_arg("metrics", "model/regression/reports/metrics.csv")
report_file <- parse_arg("report", "model/regression/reports/model_evaluation.md")
seed <- as.integer(parse_arg("seed", "42"))
test_ratio <- as.numeric(parse_arg("test-ratio", "0.2"))
min_rows <- as.integer(parse_arg("min-rows", "100"))

if (has_flag("smoke")) {
  input_file <- "model/regression/data/fixture_used_cars.csv"
  output_model <- "model/regression/models/regression_v1_fixture.rds"
  metrics_file <- "model/regression/reports/metrics_fixture.csv"
  report_file <- "model/regression/reports/model_evaluation_fixture.md"
  min_rows <- 10
}

if (!file.exists(input_file)) {
  stop(sprintf(
    "Training dataset not found: %s. Put TV3 cleaned data here or run with --smoke for fixture validation.",
    input_file
  ), call. = FALSE)
}

raw_df <- read.csv(input_file, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM")
df <- prepare_model_features(raw_df, require_price = TRUE, drop_incomplete = TRUE)

if (nrow(df) < min_rows) {
  stop(sprintf("Not enough valid rows for training: %d rows, minimum is %d", nrow(df), min_rows), call. = FALSE)
}

set.seed(seed)
test_size <- max(1, floor(nrow(df) * test_ratio))
test_idx <- sample(seq_len(nrow(df)), size = test_size)
train_df <- df[-test_idx, , drop = FALSE]
test_df <- df[test_idx, , drop = FALSE]

model <- lm(MODEL_FORMULA, data = train_df)
predicted_price <- exp(predict(model, newdata = test_df))
metrics <- regression_metrics(test_df$price, predicted_price)
metrics$model_version <- MODEL_VERSION
metrics$dataset <- input_file
metrics$n_train <- nrow(train_df)
metrics$n_test <- nrow(test_df)
metrics$generated_at <- format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z")
metrics <- metrics[, c("model_version", "dataset", "metric", "value", "unit", "n_train", "n_test", "generated_at")]

artifact <- list(
  model = model,
  model_version = MODEL_VERSION,
  preprocessing_version = PREPROCESSING_VERSION,
  formula = deparse(MODEL_FORMULA),
  feature_contract = list(
    required_predict_columns = REQUIRED_PREDICT_COLUMNS,
    required_train_columns = REQUIRED_TRAIN_COLUMNS,
    fuel_levels = FUEL_LEVELS,
    transmission_levels = TRANSMISSION_LEVELS,
    origin_levels = ORIGIN_LEVELS
  ),
  trained_at = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z"),
  training_dataset = input_file,
  metrics = metrics
)

dir.create(dirname(output_model), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(metrics_file), recursive = TRUE, showWarnings = FALSE)
saveRDS(artifact, output_model)
write.csv(metrics, metrics_file, row.names = FALSE, fileEncoding = "UTF-8")

write_metrics_report(
  metrics,
  report_file,
  list(
    model_version = MODEL_VERSION,
    dataset = input_file,
    generated_at = metrics$generated_at[[1]],
    n_train = nrow(train_df),
    n_test = nrow(test_df),
    split_method = sprintf("random split with seed %d and test ratio %.2f", seed, test_ratio)
  )
)

cat(sprintf("Saved model artifact: %s\n", output_model))
cat(sprintf("Saved metrics: %s\n", metrics_file))
cat(sprintf("Saved report: %s\n", report_file))
