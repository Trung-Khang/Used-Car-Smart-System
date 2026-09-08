library(plumber)

source("model/plumber/config/config.R", encoding = "UTF-8")
source("model/plumber/handlers/prediction_handler.R", encoding = "UTF-8")

#* Health check for backend integration
#* @get /health
function() {
  artifact_exists <- file.exists(MODEL_FILE)
  list(
    status = if (artifact_exists) "ready" else "waiting_for_model",
    model_file = MODEL_FILE,
    model_version = MODEL_VERSION_FALLBACK
  )
}

#* Predict used-car market price
#* @post /predict
function(req, res) {
  tryCatch(
    {
      payload <- jsonlite::fromJSON(req$postBody, simplifyVector = FALSE)
      predict_price(payload)
    },
    error = function(e) {
      msg <- conditionMessage(e)
      if (grepl("not available yet", msg, fixed = TRUE)) {
        res$status <- 503
      } else {
        res$status <- 400
      }
      list(
        error = TRUE,
        message = msg,
        model_version = MODEL_VERSION_FALLBACK,
        predicted_at = format(Sys.time(), "%Y-%m-%dT%H:%M:%S%z")
      )
    }
  )
}
