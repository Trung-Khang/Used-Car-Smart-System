# TV4 Prediction Contract Proposal

Status: proposal only. It does not modify the current Plumber official schema.

| Field | User form | Unit / values | Candidate handling |
|---|---|---|---|
| `manufacture_year` | Required | integer, 1990 to current year + 1 | Required for all candidates. |
| `observed_year` | System-supplied or required valuation context | integer | For listings derive from `crawled_at`; for user valuation use the valuation year. It is not `listed_at` publication year. |
| `mileage` | Required for reduced baseline; optional for missing-aware candidate | km, >= 0 | Never interpret NULL as 0. |
| `fuel_type` | Required | Gasoline, Diesel, Hybrid, Electric | Reject unknown values. |
| `transmission` | Required for reduced baseline; optional for missing-aware candidate | Automatic, Manual, CVT | Use `Unavailable` only in a selected missing-aware model, not as a silently accepted raw value. |
| `origin` | Optional | Domestic, Imported | Preserve NULL; do not infer. |
| `engine_size` | Optional for Electric; candidate-dependent otherwise | liters, > 0 for combustion vehicles | Electric source NULL maps to derived `engine_non_ev = 0` only inside preprocessing. |
| `seat_count` | Optional | integer, 2 to 60 | Preserve NULL; do not infer. |
| `brand`, `model`, `variant`, `body_type` | Optional until candidate decision | text / TV3 normalized vocabulary | Needed only if a selected model handles categories and rare values. |

Prediction errors must be structured: missing required field, wrong type/unit, value outside range, or unsupported category. A form must not require origin, engine size, or seat count until the selected model handles their current real-world missingness reliably.
