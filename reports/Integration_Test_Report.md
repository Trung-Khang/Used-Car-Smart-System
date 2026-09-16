# Database and Data Import Integration Test Report

Schema version: v2.0.1  
Owner: TV5  
Date: 16/09/2026

## Status

Static review is complete. Runtime PostgreSQL and full import verification are pending because this workspace has no `psql` command, Docker executable, or running PostgreSQL service available for this review.

| Test | Status | Evidence / next owner |
|---|---|---|
| Bootstrap SQL syntax on PostgreSQL | Pending | TV5 runs `database/schema/schema.sql` on disposable PostgreSQL database. |
| v2.0.0 to v2.0.1 migration | Pending | TV5 runs `database/migrations/V2_0_1__schema_patch.sql` on a backed-up v2.0.0 database. |
| `image_url` accepts a listing image URL | Pending runtime | Covered by `database/tests/schema_v2_0_1_smoke_test.sql`. |
| PK/FK and BIGINT/Long alignment | Static pass | Schema uses BIGSERIAL/BIGINT; TV1 entities use `Long`. Runtime Hibernate validation remains pending. |
| `UNIQUE(source_url)` | Pending runtime | Smoke test attempts duplicate insert. TV3 verifies UPSERT during import. |
| CHECK constraints and nullable optional fields | Pending runtime | Smoke test covers valid NULL specs and invalid `Petrol`. |
| `updated_at` trigger | Pending runtime | Smoke test updates a listing then verifies audit timestamp. |
| Hibernate `ddl-auto=validate` | Pending | TV1 starts Backend against v2.0.1 schema. |
| Full 10,813-row import and re-import | Pending | TV3 runs import using Mapping Matrix v2.0.1; TV5 validates counts and duplicates. |

## Static contract checks completed

- The 17 TV3 dataset fields have destinations in Mapping Matrix v2.0.1.
- `image_url` maps to `listings.image_url` and `Listing.imageUrl`.
- `color` is documented as an optional database extension, not a TV3 input field.
- Vocabulary is `Gasoline`, `Diesel`, `Hybrid`, `Electric`; `Automatic`, `Manual`, `CVT`; and `Domestic`, `Imported`.
- `listed_at` remains source text in `listed_at_raw`; `crawled_at` remains a required timezone-aware timestamp.

## Acceptance evidence required before Increment 2 completion

TV5 attaches PostgreSQL execution output for bootstrap/migration and smoke test. TV1 provides Hibernate validation output. TV3 provides full import row counts, rejected rows with reasons, and a repeated-import result showing no duplicate `source_url` rows.
