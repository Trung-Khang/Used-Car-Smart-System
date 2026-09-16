# Candidate-only preprocessing helpers. No official model or artifact is created here.
validate_tv3_schema <- function(df, expected_columns) {
  if (!identical(names(df), expected_columns)) stop("TV3 dataset schema differs from the canonical 17-field order.", call. = FALSE)
  invisible(TRUE)
}

add_observation_columns <- function(df) {
  timestamp <- trimws(as.character(df$crawled_at))
  if (any(!grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*(Z|[+-][0-9]{2}:[0-9]{2})$", timestamp))) stop("crawled_at must be timezone-aware ISO-8601.", call. = FALSE)
  df$observed_year <- as.integer(substr(timestamp, 1, 4))
  df$vehicle_age <- df$observed_year - suppressWarnings(as.integer(df$manufacture_year))
  df
}

build_row_quality_flags <- function(df) {
  n <- function(x) suppressWarnings(as.numeric(x))
  price <- n(df$price); mileage <- n(df$mileage); engine <- n(df$engine_size); seats <- n(df$seat_count); year <- n(df$manufacture_year)
  fuel_ok <- df$fuel_type %in% c("Gasoline", "Diesel", "Hybrid", "Electric")
  transmission_ok <- df$transmission %in% c("Automatic", "Manual", "CVT")
  origin_ok <- df$origin %in% c("Domestic", "Imported")
  base_quality <- price >= 50000000 & price <= 15000000000 & year >= 1990 & year <= 2027 & !is.na(mileage) & mileage >= 0 & mileage <= 1000000 & !is.na(df$vehicle_age) & df$vehicle_age >= 0
  engine_ok <- (df$fuel_type == "Electric" & is.na(engine)) | (!is.na(engine) & engine > 0 & engine <= 10)
  seat_ok <- !is.na(seats) & seats >= 2 & seats <= 60
  data.frame(
    price_outlier_low = !is.na(price) & price < 50000000,
    price_outlier_high = !is.na(price) & price > 15000000000,
    mileage_outlier_high = !is.na(mileage) & mileage > 1000000,
    manufacture_year_before_1990 = !is.na(year) & year < 1990,
    negative_vehicle_age = !is.na(df$vehicle_age) & df$vehicle_age < 0,
    missing_mileage = is.na(mileage), missing_fuel_type = !fuel_ok,
    missing_transmission = !transmission_ok, missing_origin = !origin_ok,
    missing_engine_size = is.na(engine), missing_seat_count = is.na(seats),
    eligible_complete_case = base_quality & fuel_ok & transmission_ok & origin_ok & engine_ok & seat_ok,
    eligible_reduced_feature = base_quality & fuel_ok & transmission_ok,
    eligible_missing_aware = !is.na(price) & price >= 50000000 & price <= 15000000000 & year >= 1990 & year <= 2027 & !is.na(df$vehicle_age) & df$vehicle_age >= 0
  )
}

fit_missing_transformer <- function(train_df) {
  # Called only after a train/test split. It never reads test rows.
  numeric_fields <- c("mileage", "engine_size", "seat_count")
  medians <- vapply(numeric_fields, function(field) median(train_df[[field]], na.rm = TRUE), numeric(1))
  list(numeric_fields = numeric_fields, medians = medians, categorical_fields = c("fuel_type", "transmission", "origin", "body_type"), category_missing_label = "Unavailable")
}

apply_missing_transformer <- function(df, transformer) {
  out <- df
  for (field in transformer$numeric_fields) {
    out[[paste0(field, "_missing")]] <- as.integer(is.na(out[[field]]))
    out[[field]][is.na(out[[field]])] <- transformer$medians[[field]]
  }
  for (field in transformer$categorical_fields) {
    out[[field]] <- as.character(out[[field]])
    out[[field]][is.na(out[[field]]) | out[[field]] == ""] <- transformer$category_missing_label
  }
  out$engine_size[out$fuel_type == "Electric"] <- 0
  out
}
