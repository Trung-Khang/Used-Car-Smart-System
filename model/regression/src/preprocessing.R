suppressWarnings({
  options(stringsAsFactors = FALSE)
})

MODEL_VERSION <- "regression_v1"
PREPROCESSING_VERSION <- "preprocessing_v1"

REQUIRED_TRAIN_COLUMNS <- c(
  "price",
  "manufacture_year",
  "listed_year",
  "mileage",
  "fuel_type",
  "transmission",
  "origin",
  "engine_size",
  "seat_count"
)

REQUIRED_PREDICT_COLUMNS <- c(
  "manufacture_year",
  "listed_year",
  "mileage",
  "fuel_type",
  "transmission",
  "origin",
  "engine_size",
  "seat_count"
)

OPTIONAL_ID_COLUMNS <- c("brand", "model", "trim", "listed_month", "crawled_at", "source", "url")

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
  out <- ifelse(y %in% c("gasoline", "petrol", "xang"), "Gasoline",
    ifelse(y %in% c("diesel", "dau"), "Diesel",
      ifelse(y %in% c("hybrid"), "Hybrid",
        ifelse(y %in% c("electric", "ev", "dien"), "Electric", NA_character_)
      )
    )
  )
  out
}

normalize_transmission <- function(x) {
  y <- tolower(normalize_text(x))
  out <- ifelse(y %in% c("automatic", "auto", "at", "tu dong"), "Automatic",
    ifelse(y %in% c("manual", "mt", "so san", "san"), "Manual",
      ifelse(y %in% c("cvt"), "CVT", NA_character_)
    )
  )
  out
}

normalize_origin <- function(x) {
  y <- tolower(normalize_text(x))
  out <- ifelse(y %in% c("domestic", "trong nuoc", "lap rap", "viet nam"), "Domestic",
    ifelse(y %in% c("imported", "import", "nhap khau"), "Imported", NA_character_)
  )
  out
}

as_number <- function(x) {
  suppressWarnings(as.numeric(gsub("[^0-9.]", "", as.character(x))))
}

as_integer_safe <- function(x) {
  suppressWarnings(as.integer(as_number(x)))
}

median_safe <- function(x, default = NA_real_) {
  x <- suppressWarnings(as.numeric(x))
  x <- x[is.finite(x)]
  if (!length(x)) return(default)
  median(x, na.rm = TRUE)
}

validate_required_columns <- function(df, required_columns) {
  missing_columns <- setdiff(required_columns, names(df))
  if (length(missing_columns) > 0) {
    stop(sprintf("Missing required column(s): %s", paste(missing_columns, collapse = ", ")), call. = FALSE)
  }
  invisible(TRUE)
}

validate_feature_ranges <- function(df, require_price = FALSE) {
  current_year <- as.integer(format(Sys.Date(), "%Y"))
  errors <- character()

  if (any(!is.na(df$manufacture_year) & (df$manufacture_year < 1990 | df$manufacture_year > current_year + 1))) {
    errors <- c(errors, "manufacture_year must be between 1990 and next year")
  }
  if (any(!is.na(df$listed_year) & (df$listed_year < 1990 | df$listed_year > current_year + 1))) {
    errors <- c(errors, "listed_year must be between 1990 and next year")
  }
  if (any(!is.na(df$vehicle_age) & df$vehicle_age < 0)) {
    errors <- c(errors, "vehicle_age cannot be negative")
  }
  if (any(!is.na(df$mileage) & (df$mileage < 0 | df$mileage > 1000000))) {
    errors <- c(errors, "mileage must be between 0 and 1,000,000 km")
  }
  if (any(!is.na(df$engine_size) & (df$engine_size < 0 | df$engine_size > 10))) {
    errors <- c(errors, "engine_size must be between 0 and 10 liters")
  }
  if (any(!is.na(df$seat_count) & (df$seat_count < 2 | df$seat_count > 60))) {
    errors <- c(errors, "seat_count must be between 2 and 60")
  }
  if (require_price && any(!is.na(df$price) & (df$price < 50000000 | df$price > 15000000000))) {
    errors <- c(errors, "price must be between 50,000,000 and 15,000,000,000 VND")
  }
  if (any(is.na(df$fuel_type))) {
    errors <- c(errors, sprintf("fuel_type must be one of: %s", paste(FUEL_LEVELS, collapse = ", ")))
  }
  if (any(is.na(df$transmission))) {
    errors <- c(errors, sprintf("transmission must be one of: %s", paste(TRANSMISSION_LEVELS, collapse = ", ")))
  }
  if (any(is.na(df$origin))) {
    errors <- c(errors, sprintf("origin must be one of: %s", paste(ORIGIN_LEVELS, collapse = ", ")))
  }

  if (length(errors) > 0) {
    stop(paste(unique(errors), collapse = "; "), call. = FALSE)
  }

  invisible(TRUE)
}

prepare_model_features <- function(df, require_price = FALSE, drop_incomplete = TRUE) {
  required_columns <- if (require_price) REQUIRED_TRAIN_COLUMNS else REQUIRED_PREDICT_COLUMNS
  validate_required_columns(df, required_columns)

  if (!"listed_month" %in% names(df)) {
    df$listed_month <- NA_integer_
  }

  df$price <- if ("price" %in% names(df)) as_number(df$price) else NA_real_
  df$manufacture_year <- as_integer_safe(df$manufacture_year)
  df$listed_year <- as_integer_safe(df$listed_year)
  df$listed_month <- as_integer_safe(df$listed_month)
  df$mileage <- as_number(df$mileage)
  df$engine_size <- as_number(df$engine_size)
  df$seat_count <- as_integer_safe(df$seat_count)
  df$fuel_type <- normalize_fuel(df$fuel_type)
  df$transmission <- normalize_transmission(df$transmission)
  df$origin <- normalize_origin(df$origin)

  if (!drop_incomplete) {
    missing_required <- required_columns[vapply(required_columns, function(column) {
      any(is.na(df[[column]]))
    }, logical(1))]

    if (length(missing_required) > 0) {
      stop(sprintf("Missing or invalid required value(s): %s", paste(missing_required, collapse = ", ")), call. = FALSE)
    }
  }

  df$vehicle_age <- df$listed_year - df$manufacture_year
  df$mileage_k <- df$mileage / 1000
  df$is_electric <- as.integer(df$fuel_type == "Electric")
  df$engine_non_ev <- ifelse(df$is_electric == 1, 0, df$engine_size)
  df$is_auto <- as.integer(df$transmission %in% c("Automatic", "CVT"))
  df$is_imported <- as.integer(df$origin == "Imported")
  df$fuel <- factor(df$fuel_type, levels = FUEL_LEVELS)

  validate_feature_ranges(df, require_price = require_price)

  model_columns <- c(
    "vehicle_age",
    "mileage_k",
    "engine_non_ev",
    "fuel",
    "is_auto",
    "is_imported",
    "seat_count"
  )

  if (require_price) {
    df$log_price <- log(df$price)
    model_columns <- c("log_price", model_columns)
  }

  numeric_for_model <- setdiff(model_columns, "fuel")
  complete_columns <- c(numeric_for_model, "fuel")

  if (drop_incomplete) {
    df <- df[complete.cases(df[, complete_columns, drop = FALSE]), , drop = FALSE]
  }

  df
}

prediction_payload_to_dataframe <- function(payload) {
  if (!is.list(payload)) {
    stop("Request body must be a JSON object", call. = FALSE)
  }

  as.data.frame(payload, stringsAsFactors = FALSE)
}
