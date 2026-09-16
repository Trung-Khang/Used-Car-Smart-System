suppressWarnings({
  options(stringsAsFactors = FALSE)
})

MODEL_VERSION <- "regression_v1"
PREPROCESSING_VERSION <- "preprocessing_v1"

# Training observes a listing at crawled_at; observed_year is derived from it.
REQUIRED_TRAIN_COLUMNS <- c(
  "price", "manufacture_year", "mileage", "fuel_type", "transmission",
  "origin", "engine_size", "seat_count", "crawled_at"
)
REQUIRED_PREDICT_COLUMNS <- c(
  "manufacture_year", "observed_year", "mileage", "fuel_type",
  "transmission", "origin", "seat_count"
)

OPTIONAL_ID_COLUMNS <- c(
  "brand", "model", "variant", "source_url", "image_url", "listed_at",
  "crawled_at", "listed_month"
)

FUEL_LEVELS <- c("Gasoline", "Diesel", "Hybrid", "Electric")
TRANSMISSION_LEVELS <- c("Automatic", "Manual", "CVT")
ORIGIN_LEVELS <- c("Domestic", "Imported")

MODEL_FORMULA <- log_price ~ vehicle_age + mileage_k + engine_non_ev +
  fuel + is_auto + is_imported + seat_count

normalize_text <- function(x) {
  x <- trimws(as.character(x))
  x[x == ""] <- NA_character_
  x
}

normalize_fuel <- function(x) {
  y <- tolower(normalize_text(x))
  ifelse(y %in% c("gasoline", "petrol", "xang"), "Gasoline",
    ifelse(y %in% c("diesel", "dau"), "Diesel",
      ifelse(y %in% "hybrid", "Hybrid",
        ifelse(y %in% c("electric", "ev", "dien"), "Electric", NA_character_)
      )
    )
  )
}

normalize_transmission <- function(x) {
  y <- tolower(normalize_text(x))
  ifelse(y %in% c("automatic", "auto", "at", "tu dong"), "Automatic",
    ifelse(y %in% c("manual", "mt", "so san", "san"), "Manual",
      ifelse(y %in% "cvt", "CVT", NA_character_)
    )
  )
}

normalize_origin <- function(x) {
  y <- tolower(normalize_text(x))
  ifelse(y %in% c("domestic", "trong nuoc", "lap rap", "viet nam"), "Domestic",
    ifelse(y %in% c("imported", "import", "nhap khau"), "Imported", NA_character_)
  )
}

as_number <- function(x) suppressWarnings(as.numeric(gsub("[^0-9.]", "", as.character(x))))
as_integer_safe <- function(x) suppressWarnings(as.integer(as_number(x)))

validate_required_columns <- function(df, required_columns) {
  missing_columns <- setdiff(required_columns, names(df))
  if (length(missing_columns)) {
    stop(sprintf("Missing required column(s): %s", paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

derive_observed_year <- function(df, training = FALSE) {
  if (!training && "observed_year" %in% names(df)) {
    df$observed_year <- as_integer_safe(df$observed_year)
    return(df)
  }

  if (!"crawled_at" %in% names(df)) {
    stop("observed_year is required for prediction; training data must provide crawled_at.", call. = FALSE)
  }

  timestamp <- normalize_text(df$crawled_at)
  df$observed_year <- suppressWarnings(as.integer(sub("^([0-9]{4}).*$", "\\1", timestamp)))
  invalid_timestamp <- !is.na(timestamp) & !grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}T", timestamp)
  if (any(invalid_timestamp)) {
    stop("crawled_at must be an ISO-8601 timestamp with a four-digit year.", call. = FALSE)
  }
  if (training && any(is.na(df$observed_year))) {
    stop("Training data contains missing or invalid crawled_at.", call. = FALSE)
  }
  df
}

invalid_feature_rows <- function(df, require_price = FALSE) {
  current_year <- as.integer(format(Sys.Date(), "%Y"))
  invalid <- is.na(df$manufacture_year) |
    is.na(df$observed_year) |
    df$manufacture_year < 1990 | df$manufacture_year > current_year + 1 |
    df$observed_year < 1990 | df$observed_year > current_year + 1 |
    df$vehicle_age < 0 |
    df$mileage < 0 | df$mileage > 1000000 |
    df$seat_count < 2 | df$seat_count > 60 |
    (!is.na(df$engine_size) & (df$engine_size < 0 | df$engine_size > 10)) |
    (df$fuel_type != "Electric" & is.na(df$engine_size)) |
    is.na(df$fuel_type) | is.na(df$transmission) | is.na(df$origin)

  if (require_price) {
    invalid <- invalid | is.na(df$price) | df$price < 50000000 | df$price > 15000000000
  }
  invalid[is.na(invalid)] <- TRUE
  invalid
}

prepare_model_features <- function(df, require_price = FALSE, drop_incomplete = TRUE) {
  required_columns <- if (require_price) REQUIRED_TRAIN_COLUMNS else REQUIRED_PREDICT_COLUMNS
  validate_required_columns(df, required_columns)
  df <- derive_observed_year(df, training = require_price)

  df$price <- if ("price" %in% names(df)) as_number(df$price) else NA_real_
  df$manufacture_year <- as_integer_safe(df$manufacture_year)
  df$mileage <- as_number(df$mileage)
  df$engine_size <- if ("engine_size" %in% names(df)) as_number(df$engine_size) else NA_real_
  df$seat_count <- as_integer_safe(df$seat_count)
  df$fuel_type <- normalize_fuel(df$fuel_type)
  df$transmission <- normalize_transmission(df$transmission)
  df$origin <- normalize_origin(df$origin)

  df$vehicle_age <- df$observed_year - df$manufacture_year
  df$mileage_k <- df$mileage / 1000
  df$is_electric <- as.integer(df$fuel_type == "Electric")
  # Raw EV engine_size remains NULL in TV3/TV5; only the derived model feature is zero.
  df$engine_non_ev <- ifelse(df$is_electric == 1, 0, df$engine_size)
  df$is_auto <- as.integer(df$transmission %in% c("Automatic", "CVT"))
  df$is_imported <- as.integer(df$origin == "Imported")
  df$fuel <- factor(df$fuel_type, levels = FUEL_LEVELS)

  model_columns <- c("vehicle_age", "mileage_k", "engine_non_ev", "fuel", "is_auto", "is_imported", "seat_count")
  if (require_price) {
    df$log_price <- log(df$price)
    model_columns <- c("log_price", model_columns)
  }

  complete_rows <- complete.cases(df[, model_columns, drop = FALSE])
  valid_rows <- !invalid_feature_rows(df, require_price)
  retained_rows <- complete_rows & valid_rows

  if (!drop_incomplete && !all(retained_rows)) {
    stop("Missing, invalid, or out-of-range prediction feature values. Check observed_year, mileage, categories, origin, seat_count, and engine_size for non-Electric vehicles.", call. = FALSE)
  }

  dropped <- sum(!retained_rows)
  if (drop_incomplete) df <- df[retained_rows, , drop = FALSE]
  attr(df, "preprocessing_audit") <- list(
    input_rows = length(retained_rows),
    retained_rows = if (drop_incomplete) nrow(df) else length(retained_rows),
    dropped_rows = if (drop_incomplete) dropped else 0L,
    complete_rows = sum(complete_rows),
    range_or_contract_invalid_rows = sum(!valid_rows)
  )
  df
}

prediction_payload_to_dataframe <- function(payload) {
  if (!is.list(payload)) stop("Request body must be a JSON object", call. = FALSE)
  as.data.frame(payload, stringsAsFactors = FALSE)
}
