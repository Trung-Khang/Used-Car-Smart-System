# BÁO CÁO TIẾN ĐỘ THÀNH VIÊN 01 (TV1 — BACKEND LEAD)

> **Dự án:** Smart Used-Car Decision Support System  
> **Giai đoạn:** Increment 1 — Foundation  
> **Trạng thái:** HOÀN THÀNH 100% INCREMENT 1  
> **Thời điểm cập nhật:** 08/09/2026  

---

## 1. Việc đã hoàn thành

1. **Khởi tạo và cấu hình nền móng Spring Boot (Java 17):**
   - Đã cấu hình file `pom.xml` với 5 thư viện cốt lõi: Spring Web, Spring Data JPA, PostgreSQL Driver, Springdoc OpenAPI (Swagger UI 2.5.0), Spring Boot Test.
   - Cấu hình Maven Wrapper (`mvnw.cmd`, `maven-wrapper.properties`).
2. **Cấu hình hệ thống & Kết nối cơ sở dữ liệu (`application.properties`):**
   - Cổng chạy Backend: `8080`.
   - Kết nối PostgreSQL linh hoạt thông qua biến môi trường.
   - Bật cơ chế tự động đồng bộ bảng (`spring.jpa.hibernate.ddl-auto=update`) và log SQL (`show-sql=true`).
   - Cấu hình Swagger UI path: `/swagger-ui.html`.
3. **Xây dựng Entry Point & Cấu hình bảo mật giao tiếp:**
   - Tạo class chạy chính `BackendApplication.java`.
   - Tạo `CorsConfig.java` cho phép ReactJS (cổng 5173/3000) gọi API vào Backend cổng 8080.
   - Tạo `OpenApiConfig.java` cấu hình tiêu đề và metadata cho trang tài liệu Swagger UI.
4. **Mô hình Dữ liệu (JPA Entities):**
   - `Vehicle.java`: Bảng `vehicles` (brand, model, variant, manufacture_year, body_type, fuel_type, transmission, created_at).
   - `Listing.java`: Bảng `listings` (vehicle_id @ManyToOne, price, mileage, location, source_id, source_url, image_url, listed_at, crawled_at, created_at).
5. **Tầng thao tác CSDL (JPA Repositories):**
   - `VehicleRepository.java`: Kế thừa `JpaRepository<Vehicle, Long>`, hỗ trợ tìm kiếm xe theo Hãng và Model.
   - `ListingRepository.java`: Kế thừa `JpaRepository<Listing, Long>`, hỗ trợ tìm tin đăng theo địa điểm và vehicle_id.
6. **Tầng Nghiệp vụ (Business Services):**
   - `VehicleService.java`: Toàn bộ logic nghiệp vụ CRUD cho dòng xe (getAll, getById, create, update, delete, getByBrand).
   - `ListingService.java`: Logic nghiệp vụ quản lý tin đăng bán xe (getAll, getById, create, delete, getByVehicleId).
7. **Tầng Điều khiển REST API (Controllers):**
   - `VehicleController.java`: Cung cấp đầy đủ REST endpoints cho Xe (`GET /api/v1/vehicles`, `GET /{id}`, `POST`, `PUT /{id}`, `DELETE /{id}`) kèm tài liệu Swagger.
   - `ListingController.java`: Cung cấp REST endpoints cho Tin đăng (`GET /api/v1/listings`, `GET /{id}`, `POST`, `DELETE /{id}`).
8. **Xử lý Ngoại lệ tập trung (Global Exception Handling):**
   - `ResourceNotFoundException.java`: Exception báo lỗi không tìm thấy dữ liệu.
   - `ErrorResponse.java`: Chuẩn hóa JSON phản hồi lỗi (status, error, message, path, timestamp).
   - `GlobalExceptionHandler.java`: `@RestControllerAdvice` bắt lỗi 404, 400, 500 trả về JSON sạch sẽ cho Frontend.

---

## 2. Cấu trúc mã nguồn đã sinh ra hoàn chỉnh

```text
backend/
├── pom.xml                                               # Quản lý thư viện Maven
├── mvnw.cmd                                              # Script chạy Maven trên Windows
├── .mvn/wrapper/maven-wrapper.properties                 # Cấu hình tải Maven 3.9.6
└── src/
    └── main/
        ├── resources/
        │   └── application.properties                    # Cấu hình Port 8080, PostgreSQL, JPA, Swagger
        └── java/com/system/
            ├── BackendApplication.java                   # Class khởi chạy chính
            ├── config/
            │   ├── CorsConfig.java                       # Cấu hình CORS cho ReactJS
            │   └── OpenApiConfig.java                    # Cấu hình tài liệu Swagger UI
            ├── controller/
            │   ├── VehicleController.java                # REST API quản lý Xe (/api/v1/vehicles)
            │   └── ListingController.java                # REST API quản lý Tin đăng (/api/v1/listings)
            ├── entity/
            │   ├── Vehicle.java                          # Entity bảng vehicles
            │   └── Listing.java                          # Entity bảng listings (@ManyToOne với Vehicle)
            ├── exception/
            │   ├── ErrorResponse.java                    # DTO trả về lỗi chuẩn
            │   ├── ResourceNotFoundException.java        # Exception khi không tìm thấy xe/tin đăng
            │   └── GlobalExceptionHandler.java           # Bộ xử lý lỗi tập trung @RestControllerAdvice
            ├── repository/
            │   ├── VehicleRepository.java                # JPA Repository cho Vehicle
            │   └── ListingRepository.java                # JPA Repository cho Listing
            └── service/
                ├── VehicleService.java                   # Business Logic cho Vehicle
                └── ListingService.java                   # Business Logic cho Listing
```

---

## 3. Các file trên được tạo ra để làm gì?

- Cung cấp một **hệ thống Backend chạy được hoàn chỉnh (Runnable Skeleton)** cho đồ án.
- Cung cấp đầy đủ các cổng giao tiếp REST API chuẩn JSON và tài liệu Swagger UI trực quan.
- Tự động đồng bộ và tạo cấu trúc 2 bảng cốt lõi `vehicles` và `listings` trong PostgreSQL.
- Xử lý lỗi tập trung, không làm sập server hay trả về lỗi thô (stack trace) cho Client.

---

## 4. Bàn giao cho ai?

- **TV2 (Frontend):** 
  - Đã có đầy đủ URL endpoints (`/api/v1/vehicles`, `/api/v1/listings`) để gọi lấy danh sách và thêm mới xe.
  - Đã có Swagger UI tại `http://localhost:8080/swagger-ui.html` để TV2 xem chi tiết cấu trúc Request/Response JSON và test thử.
  - Đã mở CORS cho Frontend kết nối.
- **TV5 (Database & Testing):**
  - Đã sẵn sàng các API để TV5 bắt đầu viết và thực hiện các Test Cases kiểm thử CRUD cho Increment 1.
  - Schema JPA trong code khớp 100% với bản vẽ ERD của TV5.

---

## 5. Còn thiếu hay cần fix / bổ sung gì nữa không?

- **Increment 1 đã hoàn thành trọn vẹn 100%.**
- **Chuẩn bị cho Increment 2:** Xây dựng API Tìm kiếm và Lọc nâng cao (Search & Filter đa tiêu chí kèm phân trang `Pageable` và sắp xếp `Sort`) khi TV3 import dữ liệu lớn vào CSDL.

---

## 6. Cách thức và thao tác Run / Debug / Test thử

1. **Chuẩn bị Database trong PostgreSQL:**
   - Mở pgAdmin hoặc SQL Shell (psql), chạy lệnh tạo database:
     ```sql
     CREATE DATABASE used_car_db;
     ```
2. **Khởi chạy ứng dụng:**
   - Chạy lệnh sau tại thư mục `backend/`:
     ```bash
     .\mvnw.cmd spring-boot:run
     ```
   - Hoặc mở IDE (IntelliJ IDEA / VS Code) và Run file `BackendApplication.java`.
3. **Kiểm tra kết quả:**
   - Mở trình duyệt vào link: `http://localhost:8080/swagger-ui.html`
   - Bấm vào các API `POST /api/v1/vehicles` để thêm xe mẫu, và `GET /api/v1/vehicles` để xem danh sách trả về.

---

## 7. Chú ý / Ghi chú

- Đảm bảo PostgreSQL service đang chạy trước khi khởi động Spring Boot.
- Mọi dữ liệu trả về đều theo chuẩn mã UTF-8 và định dạng JSON.
