# Data Dictionary - Increment 2 (PostgreSQL Schema v2.0.0)

- **Phiên bản:** 2.0.0
- **Chủ sở hữu:** TV5 (Review & Đồng bộ: TV1, TV3, TV4)
- **Ngày áp dụng:** 15/09/2026
- **Mục đích:** Quy định định dạng, kiểu dữ liệu, ràng buộc và ý nghĩa của các bảng/cột trong PostgreSQL Database chính thức cho Increment 2.

---

## 1. Bảng `sources` (Nguồn dữ liệu / Sàn rao bán)

Lưu trữ thông tin các sàn thương mại điện tử hoặc nguồn cào dữ liệu xe.

| Cột | Kiểu PostgreSQL | Nullable | Khóa / Constraint | Mặc định | Đơn vị | Mô tả |
| :--- | :--- | :-: | :--- | :--- | :-: | :--- |
| `id` | SERIAL | **NO** | **PK** | Auto-increment | - | Mã định danh tự tăng của nguồn dữ liệu. |
| `source_name` | VARCHAR(50) | **NO** | **UNIQUE** | - | - | Tên ngắn gọn của sàn (VD: `Bonbanh`, `Chotot`, `Oto.com.vn`). |
| `base_url` | VARCHAR(255) | **YES** | - | `NULL` | - | Trang chủ hoặc URL gốc của sàn cào dữ liệu. |
| `created_at` | TIMESTAMPTZ | **NO** | - | `CURRENT_TIMESTAMP` | UTC | Thời điểm ghi nhận nguồn vào hệ thống. |

---

## 2. Bảng `vehicles` (Thông số kỹ thuật / Cấu hình xe)

Lưu trữ các thuộc tính kỹ thuật và cấu hình cố định của xe. Một dòng đại diện cho một cấu hình xe quan sát được.

| Cột | Kiểu PostgreSQL | Nullable | Khóa / Constraint | Mặc định | Đơn vị | Mô tả |
| :--- | :--- | :-: | :--- | :--- | :-: | :--- |
| `id` | SERIAL | **NO** | **PK** | Auto-increment | - | Mã định danh cấu hình xe. |
| `brand` | VARCHAR(50) | **NO** | - | - | - | Hãng sản xuất xe (VD: `Toyota`, `Honda`, `Ford`). |
| `model` | VARCHAR(50) | **NO** | - | - | - | Dòng xe (VD: `Camry`, `Civic`, `Ranger`). |
| `variant` | VARCHAR(100) | **YES** | - | `NULL` | - | Phiên bản xe (VD: `2.5Q`, `1.5 Turbo RS`). |
| `manufacture_year` | INT | **NO** | `CHECK (1900..2100)`| - | Năm | Năm sản xuất của xe. |
| `fuel_type` | VARCHAR(30) | **YES** | Enum chuẩn | `NULL` | - | Loại nhiên liệu (`Petrol`, `Diesel`, `Hybrid`, `Electric`). |
| `transmission` | VARCHAR(30) | **YES** | Enum chuẩn | `NULL` | - | Hộp số (`Automatic`, `Manual`). |
| `engine_size` | FLOAT | **YES** | - | `NULL` | Lit / cc | Dung tích động cơ (**Trường Enrich** từ TV3). |
| `seat_count` | INT | **YES** | - | `NULL` | Ghế | Số chỗ ngồi thiết kế (**Trường Enrich** từ TV3). |
| `origin` | VARCHAR(50) | **YES** | - | `NULL` | - | Xuất xứ (**Trường Enrich** - VD: `Lắp ráp trong nước`, `Nhập khẩu`). |
| `body_type` | VARCHAR(50) | **YES** | - | `NULL` | - | Kiểu dáng xe (VD: `Sedan`, `SUV`, `Hatchback`, `MPV`). |
| `created_at` | TIMESTAMPTZ | **NO** | - | `CURRENT_TIMESTAMP` | UTC | Thời điểm bản ghi cấu hình xe được tạo. |

---

## 3. Bảng `listings` (Bài rao bán xe)

Lưu trữ thông tin chi tiết từng tin đăng bán xe cụ thể trên thị trường.

| Cột | Kiểu PostgreSQL | Nullable | Khóa / Constraint | Mặc định | Đơn vị | Mô tả |
| :--- | :--- | :-: | :--- | :--- | :-: | :--- |
| `id` | SERIAL | **NO** | **PK** | Auto-increment | - | Mã định danh tin rao bán. |
| `vehicle_id` | INT | **NO** | **FK** (`vehicles.id`) | - | - | Liên kết tới thông số kỹ thuật xe tương ứng. |
| `source_id` | INT | **NO** | **FK** (`sources.id`) | - | - | Liên kết tới nguồn cào dữ liệu tương ứng. |
| `price` | NUMERIC(15,2) | **NO** | - | - | VND | **Giá rao bán thực tế**. Không thay thế bằng giá dự đoán. |
| `mileage` | INT | **YES** | - | `NULL` | km | Số kilomet xe đã đi. Cho phép `NULL` khi không công bố. |
| `color` | VARCHAR(30) | **YES** | - | `NULL` | - | Màu sắc ngoại thất của xe. |
| `location` | VARCHAR(100) | **YES** | - | `NULL` | - | Địa điểm/Tỉnh thành đăng tin rao bán. |
| `source_url` | TEXT | **NO** | **UNIQUE** | - | - | Đường dẫn URL gốc của bài đăng (**Dùng cho Idempotency**). |
| `listed_at_raw` | TEXT | **YES** | - | `NULL` | - | Văn bản thời gian đăng gốc từ nguồn (VD: `"2 giờ trước"`). |
| `listed_at` | TIMESTAMPTZ | **YES** | - | `NULL` | UTC | Thời gian đăng tin đã chuẩn hóa (nếu xác minh được). |
| `crawled_at` | TIMESTAMPTZ | **NO** | - | - | UTC | Thời điểm hệ thống thực hiện cào dữ liệu. |
| `created_at` | TIMESTAMPTZ | **NO** | - | `CURRENT_TIMESTAMP` | UTC | Thời điểm chèn bản ghi vào Database lần đầu. |
| `updated_at` | TIMESTAMPTZ | **NO** | - | `CURRENT_TIMESTAMP` | UTC | Thời điểm bản ghi được cập nhật gần nhất. |

---

## 4. Ràng buộc Danh mục Chuẩn hóa (Enum / Vocabulary Standard)

Để đảm bảo tính nhất quán giữa Database, Backend JPA và Machine Learning model:

*   **`fuel_type` (Loại nhiên liệu):**
    *   `Petrol`: Xăng
    *   `Diesel`: Dầu Diesel
    *   `Hybrid`: Xăng điện kết hợp
    *   `Electric`: Điện hoàn toàn
    *   `NULL`: Dữ liệu thiếu/Không xác định

*   **`transmission` (Hộp số):**
    *   `Automatic`: Số tự động
    *   `Manual`: Số sàn
    *   `NULL`: Dữ liệu thiếu/Không xác định

---

## 5. Danh mục Chỉ mục Tối ưu Truy vấn (Database Indexes)

Các Index được TV5 khởi tạo sẵn nhằm phục vụ cho các API Search/Filter/Paging/Sorting của TV1 ở Increment 2:

1.  **`idx_listings_price`**: Tối ưu lọc theo khoảng giá (`minPrice`, `maxPrice`) và sắp xếp theo giá (`price ASC/DESC`).
2.  **`idx_listings_crawled_at`**: Tối ưu lọc và sắp xếp bài đăng mới nhất theo thời gian cào.
3.  **`idx_listings_vehicle_id`**: Tối ưu truy vấn JOIN giữa `listings` và `vehicles`.
4.  **`idx_vehicles_search`**: Composite Index trên `(brand, model, manufacture_year)` tối ưu bộ lọc tìm kiếm xe theo hãng, dòng và năm sản xuất.