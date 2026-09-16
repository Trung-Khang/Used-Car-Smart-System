-- Run after schema.sql on an empty disposable database.
-- The transaction rolls back all sample rows after verifying constraints and trigger behavior.

BEGIN;

INSERT INTO sources (source_name, base_url)
VALUES ('smoke-source', 'https://example.test');

INSERT INTO vehicles (
    brand, model, manufacture_year, fuel_type, transmission,
    engine_size, seat_count, origin, body_type
) VALUES (
    'Toyota', 'Vios', 2021, 'Gasoline', 'Automatic',
    1.5, 5, 'Domestic', 'Sedan'
);

INSERT INTO listings (
    vehicle_id, source_id, price, mileage, location, source_url,
    image_url, listed_at_raw, crawled_at
) VALUES (
    (SELECT id FROM vehicles WHERE brand = 'Toyota' AND model = 'Vios'),
    (SELECT id FROM sources WHERE source_name = 'smoke-source'),
    495000000, 45000, 'Ho Chi Minh City', 'https://example.test/listing/1',
    'https://images.example.test/listing/1.jpg', '2 gio truoc', CURRENT_TIMESTAMP
);

-- Optional values must be accepted as NULL.
INSERT INTO vehicles (brand, model, manufacture_year)
VALUES ('VinFast', 'VF 3', 2025);

DO $$
BEGIN
    BEGIN
        INSERT INTO listings (vehicle_id, source_id, price, source_url, crawled_at)
        VALUES (
            (SELECT id FROM vehicles WHERE brand = 'Toyota' AND model = 'Vios'),
            (SELECT id FROM sources WHERE source_name = 'smoke-source'),
            495000000, 'https://example.test/listing/1', CURRENT_TIMESTAMP
        );
        RAISE EXCEPTION 'UNIQUE(source_url) did not reject a duplicate';
    EXCEPTION WHEN unique_violation THEN
        NULL;
    END;

    BEGIN
        INSERT INTO vehicles (brand, model, manufacture_year, fuel_type)
        VALUES ('Invalid', 'Fuel', 2021, 'Petrol');
        RAISE EXCEPTION 'fuel_type CHECK did not reject Petrol';
    EXCEPTION WHEN check_violation THEN
        NULL;
    END;
END;
$$;

UPDATE listings
SET price = 496000000
WHERE source_url = 'https://example.test/listing/1';

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM listings
        WHERE source_url = 'https://example.test/listing/1'
          AND image_url = 'https://images.example.test/listing/1.jpg'
          AND updated_at >= created_at
    ) THEN
        RAISE EXCEPTION 'listing image_url or updated_at trigger verification failed';
    END IF;
END;
$$;

ROLLBACK;
