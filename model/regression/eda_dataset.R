# Reproducible TV4 Increment 2 EDA. It reads TV3's canonical CSV in place.
source("model/regression/src/candidate_preprocessing.R", encoding = "UTF-8")
input_file <- "crawler/data/cleaned/vehicles_cleaned.csv"
report_dir <- "model/regression/reports"
eda_dir <- file.path(report_dir, "eda")
dir.create(eda_dir, recursive = TRUE, showWarnings = FALSE)
if (!file.exists(input_file)) stop(sprintf("Dataset not found: %s", input_file), call. = FALSE)

expected_columns <- c("brand", "model", "variant", "manufacture_year", "price", "mileage", "fuel_type", "transmission", "body_type", "location", "origin", "engine_size", "seat_count", "source_url", "image_url", "listed_at", "crawled_at")
df <- read.csv(input_file, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM", check.names = FALSE)
validate_tv3_schema(df, expected_columns)
df <- add_observation_columns(df)
flags <- build_row_quality_flags(df)

missing_count <- vapply(df[expected_columns], function(x) sum(is.na(x) | (!is.na(x) & trimws(as.character(x)) == "")), integer(1))
availability <- data.frame(field = expected_columns, missing_count = unname(missing_count), available_count = nrow(df) - unname(missing_count), missing_rate_percent = round(100 * unname(missing_count) / nrow(df), 2))
write.csv(availability, file.path(report_dir, "feature_availability.csv"), row.names = FALSE)

numeric_summary <- do.call(rbind, lapply(c("price", "mileage", "manufacture_year", "engine_size", "seat_count", "vehicle_age"), function(field) {
  value <- suppressWarnings(as.numeric(df[[field]]))
  data.frame(field = field, available = sum(!is.na(value)), minimum = min(value, na.rm = TRUE), median = median(value, na.rm = TRUE), mean = mean(value, na.rm = TRUE), maximum = max(value, na.rm = TRUE))
}))
write.csv(numeric_summary, file.path(eda_dir, "numeric_summary.csv"), row.names = FALSE)
for (field in c("fuel_type", "transmission", "origin", "body_type")) {
  tab <- sort(table(ifelse(is.na(df[[field]]) | df[[field]] == "", "<NULL>", df[[field]])), decreasing = TRUE)
  write.csv(data.frame(field = field, value = names(tab), count = as.integer(tab)), file.path(eda_dir, paste0(field, "_distribution.csv")), row.names = FALSE)
}

source_name <- sub("^https?://([^/]+).*$", "\\1", df$source_url)
complete_breakdown <- data.frame(source = source_name, brand = df$brand, fuel_type = df$fuel_type, manufacture_year = df$manufacture_year, complete_case = flags$eligible_complete_case)
write.csv(complete_breakdown, file.path(eda_dir, "complete_case_breakdown.csv"), row.names = FALSE)

png(file.path(eda_dir, "missingness.png"), width = 1400, height = 800)
barplot(availability$missing_rate_percent, names.arg = availability$field, las = 2, col = "#C85151", main = "TV3 v1.0.0 local snapshot: missing rate by field", ylab = "Missing (%)")
dev.off()
png(file.path(eda_dir, "price_distribution.png"), width = 1200, height = 800)
hist(log10(df$price), breaks = 50, col = "#4C78A8", main = "Listing price distribution (VND, log10 scale)", xlab = "log10(price in VND)")
dev.off()
png(file.path(eda_dir, "mileage_distribution.png"), width = 1200, height = 800)
hist(df$mileage[df$mileage <= 1000000], breaks = 50, col = "#59A14F", main = "Mileage distribution (valid plotting range)", xlab = "Mileage (km; values > 1,000,000 excluded)")
dev.off()
png(file.path(eda_dir, "vehicle_age_distribution.png"), width = 1200, height = 800)
hist(df$vehicle_age, breaks = 30, col = "#F28E2B", main = "Vehicle age at crawler observation", xlab = "observed_year - manufacture_year")
dev.off()

flag_totals <- colSums(flags)
report <- c("# TV4 Dataset Quality Report", "", "## Reproducible input", "", sprintf("- Input: `%s`", input_file), sprintf("- Records / input columns: %d / %d", nrow(df), length(expected_columns)), "- CSV encoding: UTF-8 with BOM.", "- Schema: canonical 17 fields, validated in exact order.", sprintf("- Duplicate source_url: %d", sum(duplicated(df$source_url))), "- observed_year is derived from crawled_at. listed_at remains raw text.", "", "## Candidate coverage", "", sprintf("- Strict complete-case reference: %d (%.2f%%)", sum(flags$eligible_complete_case), 100 * mean(flags$eligible_complete_case)), sprintf("- Reduced-feature reference: %d (%.2f%%)", sum(flags$eligible_reduced_feature), 100 * mean(flags$eligible_reduced_feature)), sprintf("- Missing-aware candidate input: %d (%.2f%%)", sum(flags$eligible_missing_aware), 100 * mean(flags$eligible_missing_aware)), "", "## Row-level flags", "", sprintf("- `%s`: %d", names(flag_totals), flag_totals), "", "No official model, metric, or artifact is produced by this EDA script.")
writeLines(report, file.path(report_dir, "data_quality_report.md"), useBytes = TRUE)
cat("EDA outputs written to ", report_dir, "\n", sep = "")
