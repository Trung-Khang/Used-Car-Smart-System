# Database Mapping Matrix - Increment 2, Schema v2.0.1

This matrix is the handoff contract from TV3's cleaned 17-field dataset to the PostgreSQL schema and TV1 JPA entities. The source dataset has 10,813 records and does not contain `color`.

| # | TV3 dataset field | PostgreSQL destination | JPA destination | Nullable | Transform or validation |
|---:|---|---|---|---|---|
| 1 | `brand` | `vehicles.brand` VARCHAR(50) | `Vehicle.brand` String | No | Trim; required. |
| 2 | `model` | `vehicles.model` VARCHAR(50) | `Vehicle.model` String | No | Trim; required. |
| 3 | `variant` | `vehicles.variant` VARCHAR(100) | `Vehicle.variant` String | Yes | Empty value becomes NULL. |
| 4 | `manufacture_year` | `vehicles.manufacture_year` INT | `Vehicle.manufactureYear` Integer | No | 1900-2100. |
| 5 | `price` | `listings.price` NUMERIC(15,2) | `Listing.price` BigDecimal | No | VND; must be greater than zero. |
| 6 | `mileage` | `listings.mileage` INT | `Listing.mileage` Integer | Yes | km; NULL when absent; otherwise non-negative. |
| 7 | `fuel_type` | `vehicles.fuel_type` VARCHAR(30) | `Vehicle.fuelType` String | Yes | `Gasoline`, `Diesel`, `Hybrid`, `Electric`, or NULL. |
| 8 | `transmission` | `vehicles.transmission` VARCHAR(30) | `Vehicle.transmission` String | Yes | `Automatic`, `Manual`, `CVT`, or NULL. |
| 9 | `body_type` | `vehicles.body_type` VARCHAR(50) | `Vehicle.bodyType` String | Yes | Keep TV3 normalized value; NULL when absent. |
| 10 | `location` | `listings.location` VARCHAR(100) | `Listing.location` String | Yes | Listing location text. |
| 11 | `origin` | `vehicles.origin` VARCHAR(50) | `Vehicle.origin` String | Yes | `Domestic`, `Imported`, or NULL. |
| 12 | `engine_size` | `vehicles.engine_size` DOUBLE PRECISION | `Vehicle.engineSize` Double | Yes | Liters; must be greater than zero when present. |
| 13 | `seat_count` | `vehicles.seat_count` INT | `Vehicle.seatCount` Integer | Yes | 2-60 when present. |
| 14 | `source_url` | `listings.source_url` TEXT | `Listing.sourceUrl` String | No | Unique idempotency key. |
| 15 | `image_url` | `listings.image_url` VARCHAR(500) | `Listing.imageUrl` String | Yes | Primary listing image URL for UI. |
| 16 | `listed_at` | `listings.listed_at_raw` TEXT | `Listing.listedAtRaw` String | Yes | Preserve source text. Do not invent an absolute date from relative text. |
| 17 | `crawled_at` | `listings.crawled_at` TIMESTAMPTZ | `Listing.crawledAt` Instant | No | Preserve source UTC offset. |

## Database-generated and derived columns

| Column | Purpose | JPA mapping |
|---|---|---|
| `sources.id`, `vehicles.id`, `listings.id` | BIGSERIAL primary keys | `Long` |
| `listings.vehicle_id`, `listings.source_id` | BIGINT foreign keys | `Listing.vehicle`, `Listing.source` |
| `listings.listed_at` | Parsed and verified absolute listing timestamp, if available | `Listing.listedAt` Instant |
| `listings.created_at`, `listings.updated_at` | Database audit timestamps | `Listing.createdAt`, `Listing.updatedAt` Instant |
| `vehicles.created_at`, `sources.created_at` | Database audit timestamps | `Vehicle.createdAt`, `Source.createdAt` Instant |
| `listings.color` | Optional future system field | `Listing.color` String |

`color` is intentionally not an input field in the current TV3 dataset. An importer must set it to NULL unless a later, documented source supplies it.

## Import identity rules

1. Resolve the source from the listing URL domain and upsert `sources` by `source_name`.
2. Resolve a vehicle configuration using the documented composite attributes: `brand`, `model`, `variant`, `manufacture_year`, `fuel_type`, `transmission`, and `engine_size`. Null-safe comparison is required for nullable attributes.
3. Insert or update a listing using `source_url` as the idempotency key. On conflict, update mutable market fields such as `price`, `mileage`, `image_url`, `listed_at_raw`, and `crawled_at`.
4. Store TV3 `listed_at` only in `listed_at_raw`. Populate `listed_at` only after a separate verified parsing rule exists.
