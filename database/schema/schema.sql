-- PostgreSQL Schema v2.0.1 for Increment 2
-- Owner: TV5
-- Purpose: destructive bootstrap/reset script for a NEW or disposable development database.
-- WARNING: this script drops sources, vehicles, and listings with CASCADE.
-- For an existing v2.0.0 database, run database/migrations/V2_0_1__schema_patch.sql instead.

DROP TABLE IF EXISTS listings CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS sources CASCADE;

CREATE TABLE sources (
    id BIGSERIAL PRIMARY KEY,
    source_name VARCHAR(50) NOT NULL UNIQUE,
    base_url VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vehicles (
    id BIGSERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    variant VARCHAR(100),
    manufacture_year INT NOT NULL,
    fuel_type VARCHAR(30),
    transmission VARCHAR(30),
    engine_size DOUBLE PRECISION,
    seat_count INT,
    origin VARCHAR(50),
    body_type VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_vehicles_manufacture_year
        CHECK (manufacture_year BETWEEN 1900 AND 2100),
    CONSTRAINT chk_vehicles_fuel_type
        CHECK (fuel_type IS NULL OR fuel_type IN ('Gasoline', 'Diesel', 'Hybrid', 'Electric')),
    CONSTRAINT chk_vehicles_transmission
        CHECK (transmission IS NULL OR transmission IN ('Automatic', 'Manual', 'CVT')),
    CONSTRAINT chk_vehicles_engine_size
        CHECK (engine_size IS NULL OR engine_size > 0),
    CONSTRAINT chk_vehicles_seat_count
        CHECK (seat_count IS NULL OR seat_count BETWEEN 2 AND 60),
    CONSTRAINT chk_vehicles_origin
        CHECK (origin IS NULL OR origin IN ('Domestic', 'Imported'))
);

CREATE TABLE listings (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL,
    source_id BIGINT NOT NULL,
    price NUMERIC(15, 2) NOT NULL,
    mileage INT,
    -- Optional system field; the current TV3 17-field dataset does not provide color.
    color VARCHAR(30),
    location VARCHAR(100),
    source_url TEXT NOT NULL UNIQUE,
    image_url VARCHAR(500),
    listed_at_raw TEXT,
    listed_at TIMESTAMPTZ,
    crawled_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_listings_vehicle
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE RESTRICT,
    CONSTRAINT fk_listings_source
        FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE RESTRICT,
    CONSTRAINT chk_listings_price CHECK (price > 0),
    CONSTRAINT chk_listings_mileage CHECK (mileage IS NULL OR mileage >= 0)
);

-- Search/filter/sort indexes required by Increment 2 queries.
CREATE INDEX idx_listings_price ON listings(price);
CREATE INDEX idx_listings_mileage ON listings(mileage) WHERE mileage IS NOT NULL;
CREATE INDEX idx_listings_crawled_at ON listings(crawled_at DESC);
CREATE INDEX idx_listings_vehicle_id ON listings(vehicle_id);
CREATE INDEX idx_vehicles_search ON vehicles(brand, model, manufacture_year);
CREATE INDEX idx_vehicles_fuel_type ON vehicles(fuel_type) WHERE fuel_type IS NOT NULL;
CREATE INDEX idx_vehicles_transmission ON vehicles(transmission) WHERE transmission IS NOT NULL;
CREATE INDEX idx_vehicles_body_type ON vehicles(body_type) WHERE body_type IS NOT NULL;

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_listings_updated_at
    BEFORE UPDATE ON listings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
