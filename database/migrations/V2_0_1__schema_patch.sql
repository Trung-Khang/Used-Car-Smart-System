-- PostgreSQL Schema v2.0.1 migration from v2.0.0.
-- Run once against an existing v2.0.0 database. This migration preserves rows.
-- Take a database backup before applying any production migration.

BEGIN;

ALTER TABLE listings DROP CONSTRAINT IF EXISTS listings_vehicle_id_fkey;
ALTER TABLE listings DROP CONSTRAINT IF EXISTS listings_source_id_fkey;
ALTER TABLE listings DROP CONSTRAINT IF EXISTS fk_listings_vehicle;
ALTER TABLE listings DROP CONSTRAINT IF EXISTS fk_listings_source;

ALTER SEQUENCE IF EXISTS sources_id_seq AS BIGINT;
ALTER SEQUENCE IF EXISTS vehicles_id_seq AS BIGINT;
ALTER SEQUENCE IF EXISTS listings_id_seq AS BIGINT;

ALTER TABLE sources ALTER COLUMN id TYPE BIGINT;
ALTER TABLE vehicles ALTER COLUMN id TYPE BIGINT;
ALTER TABLE listings ALTER COLUMN id TYPE BIGINT;
ALTER TABLE listings ALTER COLUMN vehicle_id TYPE BIGINT;
ALTER TABLE listings ALTER COLUMN source_id TYPE BIGINT;
ALTER TABLE listings ADD COLUMN IF NOT EXISTS image_url VARCHAR(500);

ALTER TABLE listings
    ADD CONSTRAINT fk_listings_vehicle
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE RESTRICT;
ALTER TABLE listings
    ADD CONSTRAINT fk_listings_source
    FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE RESTRICT;

ALTER TABLE vehicles
    ADD CONSTRAINT chk_vehicles_fuel_type
    CHECK (fuel_type IS NULL OR fuel_type IN ('Gasoline', 'Diesel', 'Hybrid', 'Electric'));
ALTER TABLE vehicles
    ADD CONSTRAINT chk_vehicles_transmission
    CHECK (transmission IS NULL OR transmission IN ('Automatic', 'Manual', 'CVT'));
ALTER TABLE vehicles
    ADD CONSTRAINT chk_vehicles_engine_size
    CHECK (engine_size IS NULL OR engine_size > 0);
ALTER TABLE vehicles
    ADD CONSTRAINT chk_vehicles_seat_count
    CHECK (seat_count IS NULL OR seat_count BETWEEN 2 AND 60);
ALTER TABLE vehicles
    ADD CONSTRAINT chk_vehicles_origin
    CHECK (origin IS NULL OR origin IN ('Domestic', 'Imported'));
ALTER TABLE listings
    ADD CONSTRAINT chk_listings_price CHECK (price > 0);
ALTER TABLE listings
    ADD CONSTRAINT chk_listings_mileage CHECK (mileage IS NULL OR mileage >= 0);

CREATE INDEX IF NOT EXISTS idx_listings_mileage ON listings(mileage) WHERE mileage IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_vehicles_fuel_type ON vehicles(fuel_type) WHERE fuel_type IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_vehicles_transmission ON vehicles(transmission) WHERE transmission IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_vehicles_body_type ON vehicles(body_type) WHERE body_type IS NOT NULL;

COMMIT;
