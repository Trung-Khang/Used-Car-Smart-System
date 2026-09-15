-- PostgreSQL Schema Version 2.0.0 for Increment 2
-- Author: TV5 (Database Master)
-- Date: 15/09/2026

DROP TABLE IF EXISTS listings CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS sources CASCADE;

-- 1. Bảng Nguồn Dữ Liệu (Sources)
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,       -- 'bonbanh', 'chotot'
    name VARCHAR(100) NOT NULL,              -- 'Bốn Bánh', 'Chợ Tốt'
    base_url TEXT
);

INSERT INTO sources (code, name, base_url) VALUES 
('bonbanh', 'Bốn Bánh', 'https://bonbanh.com'),
('chotot', 'Chợ Tốt', 'https://xe.chotot.com');

-- 2. Bảng Thông Số Cấu Hình Xe (Vehicles)
CREATE TABLE vehicles (
    id BIGSERIAL PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    variant VARCHAR(100),
    manufacture_year INT NOT NULL CHECK (manufacture_year >= 1900),
    body_type VARCHAR(50),
    fuel_type VARCHAR(50),
    transmission VARCHAR(50),
    engine_size VARCHAR(50),                -- Giữ dạng chuỗi dung tích (vd: '2.0L')
    seat_count INT,
    origin VARCHAR(100)                      -- 'Domestic' / 'Imported'
);

-- 3. Bảng Tin Rao Bán (Listings)
CREATE TABLE listings (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT REFERENCES vehicles(id) ON DELETE CASCADE,
    source_id INT REFERENCES sources(id),
    price NUMERIC(15, 2) NOT NULL CHECK (price >= 0),
    mileage INT CHECK (mileage >= 0),
    color VARCHAR(50),
    location VARCHAR(100) NOT NULL,
    source_url TEXT NOT NULL UNIQUE,          -- Unique Key chống trùng khi import lặp
    image_url TEXT,
    crawled_at TIMESTAMPTZ NOT NULL,         -- Mốc thời gian quan sát chuẩn có timezone
    listed_at_raw VARCHAR(255),              -- Giữ nguyên chuỗi thời gian tương đối
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Indexes phục vụ tìm kiếm, lọc và sắp xếp (TV1)
CREATE INDEX idx_vehicles_brand_model ON vehicles(brand, model);
CREATE INDEX idx_vehicles_specs ON vehicles(fuel_type, transmission, body_type);
CREATE INDEX idx_listings_price ON listings(price);
CREATE INDEX idx_listings_crawled_at ON listings(crawled_at DESC);