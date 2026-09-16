# TV3 Confirmation For TV4

## Confirmed By TV3 Documents

- Contract version: v1.0.0, 17 canonical fields, 10,813 records.
- `price` is VND; `mileage` is km and NULL means unavailable/new/omitted, not zero.
- `engine_size` is liters; Electric vehicles retain NULL, not zero.
- `crawled_at` is a timezone-aware observation timestamp. `observed_year` is derived from it.
- `listed_at` is raw or relative source text and must not be treated as an absolute timestamp.
- Fuel enum: Gasoline, Diesel, Hybrid, Electric, or NULL. Transmission enum: Automatic, Manual, CVT, or NULL. Origin enum: Domestic, Imported, or NULL.
- `source_url` is the unique listing identity and duplicate count is zero in the documented lock.
- Enrichment is explicitly not promised to fill origin, engine size, or seat count. NULL must remain authentic.
- The cleaned canonical dataset is for TV4 EDA/training; the seed/import output is for TV5/TV1 database integration.

## Confirmation Still Needed

1. The local CSV SHA-256 is `5a70b532173c897531440105b47ddccfb839198d631ea0375050c57010201b27`, while the Phase 1 lock reports `bcec9df219fc7511a0f7ac2cf80bfffd1a6aa732144f99b15f8709e8d2ac3513`. Confirm that the local snapshot is canonical or publish a new lock/checksum.
2. Confirm the actual body-type vocabulary or normalize it consistently. The local CSV still has `SUV`, `Crossover`, and `Van / Minivan` alongside the documented `SUV / Crossover` and `Van`, plus `Truck`, `Other`, and `Wagon`.

These are provenance/category questions only. TV4 does not request invented enrichment values.
