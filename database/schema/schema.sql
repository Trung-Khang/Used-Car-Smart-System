-- PostgreSQL Schema v2.0.0 for Increment 2
-- Owner: TV5 (Review & Approved: TV1, TV3, TV4)
-- Description: Official Database DDL schema for sources, vehicles, and listings

DROP TABLE IF EXISTS listings CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS sources CASCADE;

-- 1. Table: sources (Nguồn dữ liệu / Sàn rao bán)
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(50) NOT NULL UNIQUE,
    base_url VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table: vehicles (Thông số kỹ thuật / Cấu hình xe)
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    variant VARCHAR(100),
    manufacture_year INT NOT NULL,
    fuel_type VARCHAR(30),
    transmission VARCHAR(30),
    engine_size FLOAT,         -- Nullable (Trường Enrich)
    seat_count INT,            -- Nullable (Trường Enrich)
    origin VARCHAR(50),        -- Nullable (Trường Enrich)
    body_type VARCHAR(50),     -- Nullable
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_manufacture_year CHECK (manufacture_year >= 1900 AND manufacture_year <= 2100)
);

-- 3. Table: listings (Bài rao bán xe)
CREATE TABLE listings (
    id SERIAL PRIMARY KEY,
    vehicle_id INT NOT NULL REFERENCES vehicles(id) ON DELETE RESTRICT,
    source_id INT NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    price NUMERIC(15, 2) NOT NULL,
    mileage INT,               -- Nullable (km)
    color VARCHAR(30),
    location VARCHAR(100),
    source_url TEXT NOT NULL UNIQUE,
    listed_at_raw TEXT,
    listed_at TIMESTAMPTZ,
    crawled_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes tối ưu cho truy vấn Search / Filter / Page / Sort (Increment 2)
CREATE INDEX idx_listings_price ON listings(price);
CREATE INDEX idx_listings_crawled_at ON listings(crawled_at DESC);
CREATE INDEX idx_listings_vehicle_id ON listings(vehicle_id);
CREATE INDEX idx_vehicles_search ON vehicles(brand, model, manufacture_year);

-- Function & Trigger tự động cập nhật cột updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_listings_updated_at
    BEFORE UPDATE ON listings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();