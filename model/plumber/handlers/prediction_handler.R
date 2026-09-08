source("model/regression/src/preprocessing.R", encoding = "UTF-8")

load_model_artifact <- function(model_file = MODEL_FILE) {
  if (!file.exists(model_file)) {
    return(NULL)
  }
  readRDS(model_file)
}

predict_price <- function(payload, model_file = MODEL_FILE) {
  artifact <- load_model_artifact(model_file)
  if (is.null(artifact)) {
    stop(sprintf("Model artifact is not available yet: %s", model_file), call. = FALSE)
  }

  input_df <- prediction_payload_to_dataframe(payload)
  feature_df <- prepare_model_features(input_df, require_price = FALSE, drop_incomplete = FALSE)

  predicted_price <- exp(predict(artifact$model, newdata = feature_df))
  predicted_price <- round(as.numeric(predicted_price[[1]]))

  list(
    predicted_price = predicted_price,
    currency = "VND",
    model_version = artifact$model_version,
    preprocessing_version = artifact$preprocessing_version,
    predicted_at = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z")
  )
}
