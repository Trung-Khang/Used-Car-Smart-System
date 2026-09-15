---
# Data Dictionary & Mapping Matrix - Schema v2.0.0

**Project:** Used-Car-Smart-System  
**Author:** TV5 (Database Master)  
**Target Contract:** TV3 Data Contract v1.0.0 (17 Fields)  

## 1. Bảng Ánh Xạ Dữ Liệu (Mapping Matrix)

| STT | Trường Dataset (TV3 v1.0.0) | Cột PostgreSQL (TV5) | Kiểu SQL | Null? | Tương ứng JPA Entity (TV1) | Kiểu Java |
| :-: | :--- | :--- | :--- | :-: | :--- | :--- |
| 1 | `brand` | `vehicles.brand` | `VARCHAR(100)` | **NO** | `Vehicle.brand` | `String` |
| 2 | `model` | `vehicles.model` | `VARCHAR(100)` | **NO** | `Vehicle.model` | `String` |
| 3 | `variant` | `vehicles.variant` | `VARCHAR(100)` | YES | `Vehicle.variant` | `String` |
| 4 | `manufacture_year` | `vehicles.manufacture_year` | `INT` | **NO** | `Vehicle.manufactureYear` | `Integer` |
| 5 | `price` | `listings.price` | `NUMERIC(15,2)` | **NO** | `Listing.price` | `BigDecimal` |
| 6 | `mileage` | `listings.mileage` | `INT` | YES | `Listing.mileage` | `Integer` |
| 7 | `fuel_type` | `vehicles.fuel_type` | `VARCHAR(50)` | YES | `Vehicle.fuelType` | `String` |
| 8 | `transmission` | `vehicles.transmission` | `VARCHAR(50)` | YES | `Vehicle.transmission` | `String` |
| 9 | `body_type` | `vehicles.body_type` | `VARCHAR(50)` | YES | `Vehicle.bodyType` | `String` |
| 10 | `origin` | `vehicles.origin` | `VARCHAR(100)` | YES | `Vehicle.origin` | `String` |
| 11 | `engine_size` | `vehicles.engine_size` | `VARCHAR(50)` | YES | `Vehicle.engineSize` | `String` |
| 12 | `seat_count` | `vehicles.seat_count` | `INT` | YES | `Vehicle.seatCount` | `Integer` |
| 13 | `color` | `listings.color` | `VARCHAR(50)` | YES | `Listing.color` | `String` |
| 14 | `location` | `listings.location` | `VARCHAR(100)` | **NO** | `Listing.location` | `String` |
| 15 | `source_url` | `listings.source_url` | `TEXT` | **NO (UK)** | `Listing.sourceUrl` | `String` |
| 16 | `image_url` | `listings.image_url` | `TEXT` | YES | `Listing.imageUrl` | `String` |
| 17 | `listed_at` | `listings.listed_at_raw` | `VARCHAR(255)` | YES | `Listing.listedAtRaw` | `String` |
| 18 | `crawled_at` | `listings.crawled_at` | `TIMESTAMPTZ` | **NO** | `Listing.crawledAt` | `OffsetDateTime` |
| 19 | *(Derived)* | `sources.code` / `source_id` | `INT (FK)` | **NO** | `Listing.source` | `Source` |

## 2. Các nguyên tắc thiết kế quan trọng

- **Bảo toàn trường Enrich:** Giữ nguyên 3 trường `origin`, `engine_size`, `seat_count` với chính sách `NULL` tự nhiên để không mất dữ liệu.
- **Giá rao bán:** `listings.price` chỉ lưu giá gốc rao bán VND. Không đưa giá dự đoán của AI vào cột này.
- **Xử lý thời gian:** `crawled_at` dùng `TIMESTAMPTZ` làm chuẩn audit. `listed_at_raw` lưu chuỗi nguyên văn từ web cào.
- **Chống trùng lặp:** `source_url` có thuộc tính `UNIQUE` phục vụ việc chạy lại seed/import mà không sinh record trùng.