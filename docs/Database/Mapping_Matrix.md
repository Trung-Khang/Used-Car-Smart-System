# Database Mapping Matrix - Increment 2

- **Phiên bản:** 2.0.0
- **Tác giả:** TV5 (Đồng bộ cùng TV3 & TV1)
- **Ngày cập nhật:** 14/09/2026
- **Trạng thái:** Chốt Data Contract & Schema chính thức

Tài liệu này quy định ánh xạ chi tiết giữa **17 trường dữ liệu đầu vào (TV3 Dataset)**, **PostgreSQL Schema (TV5)** và **JPA Entity (TV1)** để đảm bảo tính toàn vẹn dữ liệu trong toàn hệ thống.

---

## 1. Bảng Ma trận Ánh xạ (Mapping Matrix)

| STT | Trường Dataset (TV3) | Bảng & Cột SQL (TV5) | Kiểu PostgreSQL | Entity & Field JPA (TV1) | Kiểu Java | Nullable | Quy tắc Biến đổi & Validation |
| :-: | :--- | :--- | :--- | :--- | :--- | :-: | :--- |
| 1 | `brand` | `vehicles.brand` | VARCHAR(50) | `Vehicle.brand` | `String` | **NO** | Uppercase chữ cái đầu, trim khoảng trắng thừa. |
| 2 | `model` | `vehicles.model` | VARCHAR(50) | `Vehicle.model` | `String` | **NO** | Giữ nguyên chữ gốc, trim khoảng trắng. |
| 3 | `variant` | `vehicles.variant` | VARCHAR(100) | `Vehicle.variant` | `String` | **YES** | Phiên bản xe. Nếu trống thì để `NULL`. |
| 4 | `manufacture_year` | `vehicles.manufacture_year` | INT | `Vehicle.manufactureYear` | `Integer` | **NO** | Chuyển thành số nguyên. Ràng buộc `1900 <= year <= 2100`. |
| 5 | `fuel_type` | `vehicles.fuel_type` | VARCHAR(30) | `Vehicle.fuelType` | `String` / `Enum` | **YES** | Ánh xạ về Enum chuẩn: `Petrol`, `Diesel`, `Hybrid`, `Electric`. Nếu không xác định để `NULL`. |
| 6 | `transmission` | `vehicles.transmission` | VARCHAR(30) | `Vehicle.transmission` | `String` / `Enum` | **YES** | Ánh xạ về Enum chuẩn: `Automatic`, `Manual`. Nếu không xác định để `NULL`. |
| 7 | `engine_size` | `vehicles.engine_size` | FLOAT | `Vehicle.engineSize` | `Double` | **YES** | **Trường Enrich**: Đơn vị Lit/cc. Cho phép `NULL` khi nguồn không có. |
| 8 | `seat_count` | `vehicles.seat_count` | INT | `Vehicle.seatCount` | `Integer` | **YES** | **Trường Enrich**: Số chỗ ngồi (VD: 4, 5, 7). Cho phép `NULL`. |
| 9 | `origin` | `vehicles.origin` | VARCHAR(50) | `Vehicle.origin` | `String` | **YES** | **Trường Enrich**: Xuất xứ (VD: "Lắp ráp trong nước", "Nhập khẩu"). Cho phép `NULL`. |
| 10 | `body_type` | `vehicles.body_type` | VARCHAR(50) | `Vehicle.bodyType` | `String` | **YES** | Kiểu dáng xe (Sedan, SUV, Hatchback, Crossover, MPV...). |
| 11 | `price` | `listings.price` | NUMERIC(15,2) | `Listing.price` | `BigDecimal` | **NO** | Giá rao bán chính thức. Đơn vị: **VND**. Không dùng giá dự đoán ML. |
| 12 | `mileage` | `listings.mileage` | INT | `Listing.mileage` | `Integer` | **YES** | Số km đã đi. Nếu thiếu hoặc bất thường, lưu `NULL` và đánh cờ. |
| 13 | `color` | `listings.color` | VARCHAR(30) | `Listing.color` | `String` | **YES** | Màu sắc xe. Chuẩn hóa chuỗi văn bản. |
| 14 | `location` | `listings.location` | VARCHAR(100) | `Listing.location` | `String` | **YES** | Tỉnh/Thành phố bài đăng rao bán. |
| 15 | `source_url` | `listings.source_url` | TEXT | `Listing.sourceUrl` | `String` | **NO** | **Khóa duy nhất (`UNIQUE`)**. Dùng để chống trùng lặp khi import lặp. |
| 16 | `crawled_at` | `listings.crawled_at` | TIMESTAMPTZ | `Listing.crawledAt` | `Instant` / `ZonedDateTime` | **NO** | Thời điểm cào dữ liệu. Bắt buộc bảo toàn múi giờ (UTC). |
| 17 | `listed_at_raw` | `listings.listed_at_raw` | TEXT | `Listing.listedAtRaw` | `String` | **YES** | Giữ chuỗi thời gian gốc từ nguồn (VD: "2 giờ trước", "14/09/2026"). |

---

## 2. Các Trường Khóa & Metadata Sinh Bởi Database (System Columns)

| Bảng SQL | Cột SQL | Kiểu PostgreSQL | Entity & Field JPA | Mới / Khóa | Quy tắc Khóa & Liên kết |
| :--- | :--- | :--- | :--- | :-: | :--- |
| `sources` | `id` | SERIAL | `Source.id` | **PK** | Khóa chính tự tăng của nguồn/sàn. |
| `sources` | `source_name` | VARCHAR(50) | `Source.sourceName` | **UK** | Tên nguồn dữ liệu (VD: Bonbanh, Chotot). |
| `vehicles` | `id` | SERIAL | `Vehicle.id` | **PK** | Khóa chính tự tăng đại diện cho 1 cấu hình xe. |
| `listings` | `id` | SERIAL | `Listing.id` | **PK** | Khóa chính tự tăng của bài đăng. |
| `listings` | `vehicle_id` | INT | `Listing.vehicle` (`@ManyToOne`) | **FK** | Khóa ngoại trỏ đến `vehicles.id`. |
| `listings` | `source_id` | INT | `Listing.source` (`@ManyToOne`) | **FK** | Khóa ngoại trỏ đến `sources.id`. |
| `listings` | `listed_at` | TIMESTAMPTZ | `Listing.listedAt` | Attribute | Ngày đăng đã được xác minh/parse từ `listed_at_raw` (cho phép `NULL`). |
| `listings` | `created_at` | TIMESTAMPTZ | `Listing.createdAt` | Attribute | Thời điểm bản ghi được ghi vào Database (`DEFAULT CURRENT_TIMESTAMP`). |

---

## 3. Quy tắc Tích hợp & Xử lý Đặc biệt

1. **Ràng buộc Idempotency (Import Lặp Không Trùng):**
   - Import pipeline (TV3) thực hiện câu lệnh `UPSERT` dựa trên `source_url`.
   - Nếu `source_url` đã tồn tại: Cập nhật `price`, `mileage`, `crawled_at`, `updated_at`. KHÔNG chèn thêm dòng mới vào bảng `listings`.

2. **Quy tắc Liên kết Cấu hình Xe (`vehicles`):**
   - Khi import một listing mới, tìm kiếm cấu hình khớp bộ khóa `(brand, model, variant, manufacture_year, fuel_type, transmission, engine_size)`.
   - Nếu đã có `vehicle` tương ứng $\rightarrow$ lấy `vehicle_id` gán cho listing.
   - Nếu chưa có $\rightarrow$ tạo mới 1 dòng trong `vehicles` rồi gán `vehicle_id`.

3. **Chính sách Mất Dữ liệu (Nullable & Enriched Fields):**
   - Ba trường bổ sung: `origin`, `engine_size`, `seat_count` cho phép giá trị `NULL`.
   - Backend (TV1) và Machine Learning (TV4) phải xử lý được trường hợp `NULL` mà không làm ngắt kết nối hoặc phát sinh Exception.