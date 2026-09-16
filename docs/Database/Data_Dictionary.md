# Data Dictionary - Increment 2, PostgreSQL Schema v2.0.1

Owner: TV5. This document matches `database/schema/schema.sql` and the Mapping Matrix v2.0.1.

## `sources`

| Column | Type | Null | Constraint | Description |
|---|---|---|---|---|
| `id` | BIGSERIAL | No | PK | Source identifier. |
| `source_name` | VARCHAR(50) | No | UNIQUE | Stable source name, such as `bonbanh` or `chotot`. |
| `base_url` | VARCHAR(255) | Yes | - | Source home URL. |
| `created_at` | TIMESTAMPTZ | No | default current timestamp | Source creation time. |

## `vehicles`

| Column | Type | Null | Constraint | Unit / allowed values |
|---|---|---|---|---|
| `id` | BIGSERIAL | No | PK | - |
| `brand` | VARCHAR(50) | No | - | Vehicle brand. |
| `model` | VARCHAR(50) | No | - | Vehicle model. |
| `variant` | VARCHAR(100) | Yes | - | Trim/variant. |
| `manufacture_year` | INT | No | 1900-2100 | Year. |
| `fuel_type` | VARCHAR(30) | Yes | CHECK | `Gasoline`, `Diesel`, `Hybrid`, `Electric`, NULL. |
| `transmission` | VARCHAR(30) | Yes | CHECK | `Automatic`, `Manual`, `CVT`, NULL. |
| `engine_size` | DOUBLE PRECISION | Yes | greater than 0 when present | Liters. |
| `seat_count` | INT | Yes | 2-60 when present | Seats. |
| `origin` | VARCHAR(50) | Yes | CHECK | `Domestic`, `Imported`, NULL. |
| `body_type` | VARCHAR(50) | Yes | - | TV3 normalized body type. |
| `created_at` | TIMESTAMPTZ | No | default current timestamp | Row creation time. |

## `listings`

| Column | Type | Null | Constraint | Unit / description |
|---|---|---|---|---|
| `id` | BIGSERIAL | No | PK | Listing identifier. |
| `vehicle_id` | BIGINT | No | FK to `vehicles.id` | Vehicle configuration. |
| `source_id` | BIGINT | No | FK to `sources.id` | Crawl source. |
| `price` | NUMERIC(15,2) | No | greater than 0 | Observed listing price in VND. |
| `mileage` | INT | Yes | non-negative when present | Odometer in km. |
| `color` | VARCHAR(30) | Yes | - | Optional future system field; absent from current TV3 dataset. |
| `location` | VARCHAR(100) | Yes | - | Listing location. |
| `source_url` | TEXT | No | UNIQUE | Original listing URL and idempotency key. |
| `image_url` | VARCHAR(500) | Yes | - | Primary listing image URL from TV3. |
| `listed_at_raw` | TEXT | Yes | - | Original listing-time text from TV3 `listed_at`. |
| `listed_at` | TIMESTAMPTZ | Yes | - | Parsed and verified listing time only. |
| `crawled_at` | TIMESTAMPTZ | No | - | Crawl observation timestamp, UTC offset preserved. |
| `created_at` | TIMESTAMPTZ | No | default current timestamp | First database insertion time. |
| `updated_at` | TIMESTAMPTZ | No | trigger-managed | Last database update time. |

## Query indexes

`listings.price`, non-null `listings.mileage`, `listings.crawled_at`, and `listings.vehicle_id` support market list filtering/sorting. `vehicles(brand, model, manufacture_year)`, non-null `fuel_type`, `transmission`, and `body_type` support vehicle filters.

## Boundary with ML

Database constraints protect valid storage and source traceability. They do not apply TV4 model outlier thresholds such as maximum model mileage or price. `listed_year` is derived downstream from `crawled_at`, not stored as a duplicate dataset column.
