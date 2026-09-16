# PostgreSQL Schema v2.0.1

This is the official database contract for Increment 2. It defines `sources`, `vehicles`, and `listings` and matches the TV3 17-field cleaned dataset, TV1 JPA entities, and the database documents in `docs/Database/`.

## Requirements

- PostgreSQL 14 or newer.
- A database account allowed to create tables, indexes, functions, and triggers.

## New or disposable development database

Run `schema.sql` only on a new or disposable database:

```powershell
psql -d used_car_db -f database/schema/schema.sql
```

`schema.sql` begins with `DROP TABLE ... CASCADE`. It removes existing `sources`, `vehicles`, and `listings` data and is not safe for a populated shared database.

## Existing v2.0.0 database

Back up the database, then apply the non-destructive patch once:

```powershell
psql -d used_car_db -f database/migrations/V2_0_1__schema_patch.sql
```

The migration adds `listings.image_url`, aligns identifiers to BIGINT for JPA `Long`, adds named foreign keys, and adds the v2.0.1 data constraints/indexes. It does not run the reset script.

## Verification

After bootstrapping an empty test database, run:

```powershell
psql -d used_car_db -f database/tests/schema_v2_0_1_smoke_test.sql
```

The smoke test verifies a listing with `image_url`, nullable optional fields, `UNIQUE(source_url)`, vocabulary checks, and the `updated_at` trigger. The test rolls back its sample rows.

TV1 must also start Spring Boot with `HIBERNATE_DDL_AUTO=validate` against this schema. TV3 must update the import pipeline to use the Mapping Matrix before importing the full dataset.
