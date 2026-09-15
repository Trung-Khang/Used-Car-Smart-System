-- =========================================================
-- SMART USED-CAR DECISION SUPPORT SYSTEM
-- Member 05 - Increment 1: Foundation
-- Database: PostgreSQL
-- =========================================================


-- =========================================================
-- 1. VEHICLE
-- Lưu thông tin xe ô tô cũ
-- =========================================================

CREATE TABLE IF NOT EXISTS vehicle (
    vehicle_id BIGSERIAL PRIMARY KEY,

    make VARCHAR(100) NOT NULL,

    model VARCHAR(100) NOT NULL,

    year INTEGER,

    mileage NUMERIC(12, 2),

    fuel VARCHAR(50),

    transmission VARCHAR(50),

    listing_price NUMERIC(14, 2),

    predicted_price NUMERIC(14, 2),

    difference_percent NUMERIC(8, 2),

    model_version VARCHAR(50),

    source_url TEXT,

    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 2. VEHICLE_COMPARISON
-- Lưu thông tin một phiên so sánh xe
-- =========================================================

CREATE TABLE IF NOT EXISTS vehicle_comparison (
    comparison_id BIGSERIAL PRIMARY KEY,

    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 3. COMPARISON_VEHICLE
-- Bảng trung gian giữa vehicle và vehicle_comparison
-- Quan hệ nhiều - nhiều
-- =========================================================

CREATE TABLE IF NOT EXISTS comparison_vehicle (
    comparison_id BIGINT NOT NULL,

    vehicle_id BIGINT NOT NULL,

    PRIMARY KEY (comparison_id, vehicle_id),

    CONSTRAINT fk_comparison_vehicle_comparison
        FOREIGN KEY (comparison_id)
        REFERENCES vehicle_comparison(comparison_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_comparison_vehicle_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(vehicle_id)
        ON DELETE CASCADE
);


-- =========================================================
-- 4. INDEX
-- Hỗ trợ Search / Filter
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_vehicle_make_model
ON vehicle(make, model);

CREATE INDEX IF NOT EXISTS idx_vehicle_year
ON vehicle(year);

CREATE INDEX IF NOT EXISTS idx_vehicle_listing_price
ON vehicle(listing_price);

CREATE INDEX IF NOT EXISTS idx_vehicle_mileage
ON vehicle(mileage);