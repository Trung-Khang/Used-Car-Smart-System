# BÁO CÁO TIẾN ĐỘ — MEMBER 05

**Dự án:** Smart Used-Car Decision Support System
**Thành viên:** Member 05 — Database / System Design / Testing
**Giai đoạn:** Increment 1 — Foundation
**File báo cáo:** `docs/Members/report/TV5_Baocaotiendo.md`
**Thời điểm cập nhật:** 09/09/2026  

---

## 1. Tổng quan nhiệm vụ

Trong Increment 1 — Foundation, Member 05 phụ trách xây dựng nền tảng về **Database và System Design**, làm cơ sở để các thành viên khác triển khai Backend, Data Pipeline, Machine Learning và Frontend.

Theo workflow của project, các nhiệm vụ chính của Member 05 gồm:

* Hoàn thiện ERD.
* Xây dựng Data Dictionary.
* Xây dựng Database Schema.
* Chuẩn bị Use Case.
* Chuẩn bị Class Diagram.
* Chuẩn bị API Specification ban đầu.
* Chuẩn bị Test Plan khung.

Các đầu ra được tổ chức trong:

```text
database/
docs/UML/
docs/Database/
docs/API/
docs/Testing/
```

---

# 2. Công việc đã thực hiện

## 2.1. Database Schema

### File

```text
database/schema/schema.sql
```

### Công việc

Xây dựng schema ban đầu sử dụng **PostgreSQL** cho hệ thống.

Các bảng chính hiện tại:

```text
vehicle
vehicle_comparison
comparison_vehicle
```

### `vehicle`

Lưu thông tin xe ô tô cũ và các thông tin liên quan đến định giá.

Các trường chính:

```text
vehicle_id
make
model
year
mileage
fuel
transmission
listing_price
predicted_price
difference_percent
model_version
source_url
created_at
updated_at
```

### `vehicle_comparison`

Lưu thông tin một phiên so sánh xe.

```text
comparison_id
created_at
```

### `comparison_vehicle`

Là bảng trung gian giữa `vehicle` và `vehicle_comparison`, phục vụ quan hệ nhiều-nhiều.

```text
comparison_id
vehicle_id
```

### Constraint

Schema đã chuẩn bị:

* Primary Key.
* Foreign Key.
* Composite Primary Key cho bảng trung gian.
* `NOT NULL` cho các trường bắt buộc.
* `ON DELETE CASCADE` cho quan hệ bảng trung gian.

### Index

Đã chuẩn bị index cho các trường thường xuyên phục vụ tìm kiếm/lọc:

```text
make + model
year
listing_price
mileage
```

---

# 3. ERD

## File

```text
docs/UML/ERD.md
```

Đã xây dựng ERD ở mức Foundation nhằm mô tả các entity database chính và mối quan hệ giữa chúng.

Quan hệ chính:

```text
VEHICLE
    1
    │
    │
    N
COMPARISON_VEHICLE
    N
    │
    │
    1
    ▼
VEHICLE_COMPARISON
```

### Ý nghĩa

* Một vehicle có thể xuất hiện trong nhiều comparison.
* Một comparison có thể chứa nhiều vehicle.
* `comparison_vehicle` được dùng để xử lý quan hệ nhiều-nhiều.

ERD hiện tại được xem là **initial foundation design** và sẽ tiếp tục được đồng bộ khi Backend và Data Pipeline hoàn thiện entity/schema thực tế.

---

# 4. Data Dictionary

## File

```text
docs/Database/Data_Dictionary.md
```

Đã mô tả:

* Tên bảng.
* Tên column.
* Data type.
* Primary Key / Foreign Key.
* Cho phép NULL hay không.
* Ý nghĩa của từng trường.
* Một số validation rule cơ bản.

Ví dụ đối với `vehicle`:

| Field                | Ý nghĩa                                 |
| -------------------- | --------------------------------------- |
| `vehicle_id`         | ID duy nhất của xe                      |
| `make`               | Hãng xe                                 |
| `model`              | Model xe                                |
| `year`               | Năm sản xuất                            |
| `mileage`            | Số km đã đi                             |
| `fuel`               | Loại nhiên liệu                         |
| `transmission`       | Loại hộp số                             |
| `listing_price`      | Giá đăng bán                            |
| `predicted_price`    | Giá dự đoán từ model                    |
| `difference_percent` | Chênh lệch giữa giá đăng và giá dự đoán |
| `model_version`      | Phiên bản model                         |
| `source_url`         | Nguồn dữ liệu                           |

---

# 5. Use Case

## File

```text
docs/UML/Use_Case.md
```

Đã chuẩn bị các use case ban đầu:

```text
View Vehicle List
Search / Filter Vehicles
View Vehicle Detail
Compare Vehicles
Request Vehicle Valuation
View Recommendations
```

### Actor chính

```text
User
```

### Các thành phần hệ thống liên quan

```text
Backend
Data Pipeline
R / ML Service
```

### Use Case được mô tả chi tiết

`View Vehicle Detail`

Luồng chính:

```text
User
 ↓
Frontend
 ↓
Spring Boot Backend
 ↓
PostgreSQL
 ↓
Backend Response
 ↓
Frontend
 ↓
Vehicle Detail
```

---

# 6. Class Diagram

## File

```text
docs/UML/Class_Diagram.md
```

Đã chuẩn bị class diagram Foundation gồm:

```text
Vehicle
VehicleComparison
ComparisonVehicle
RecommendationResult
```

### `Vehicle`

Đại diện cho vehicle trong hệ thống.

### `VehicleComparison`

Đại diện cho một phiên comparison.

### `ComparisonVehicle`

Entity/bảng liên kết vehicle với comparison.

### `RecommendationResult`

Được chuẩn bị ở mức thiết kế để phục vụ Recommendation trong Increment 4.

---

# 7. API Specification ban đầu

## File

```text
docs/API/API_Specification_Initial.md
```

Đã chuẩn bị API contract ban đầu cho Backend Spring Boot.

### Vehicle API

```http
GET /api/vehicles
```

Dùng để lấy danh sách vehicle.

---

### Vehicle Detail

```http
GET /api/vehicles/{vehicleId}
```

Dùng để lấy thông tin chi tiết một xe.

---

### Search / Filter

```http
GET /api/vehicles/search
```

Các tham số dự kiến:

```text
keyword
minPrice
maxPrice
minYear
maxYear
minMileage
maxMileage
```

---

### Comparison

```http
POST /api/comparisons
```

Ví dụ request:

```json
{
    "vehicleIds": [1, 2, 3]
}
```

---

### Get Comparison

```http
GET /api/comparisons/{comparisonId}
```

---

### Valuation

API được chuẩn bị trước cho Increment 3:

```http
POST /api/valuation
```

---

### Recommendation

API được chuẩn bị trước cho Increment 4:

```http
GET /api/recommendations
```

Các endpoint này hiện là **initial API specification**, chưa phải API contract cuối cùng.

---

# 8. Test Plan

## File

```text
docs/Testing/Test_Plan.md
```

Đã chuẩn bị test plan khung cho:

### Database Testing

* Kiểm tra tạo schema.
* Kiểm tra insert vehicle hợp lệ.
* Kiểm tra validation field bắt buộc.
* Kiểm tra Foreign Key.
* Kiểm tra composite key.
* Kiểm tra cascade delete.

### API Testing

* Vehicle List.
* Vehicle Detail.
* Search.
* Filter.
* Error 400.
* Error 404.

### Comparison Testing

* Tạo comparison.
* Kiểm tra vehicle tồn tại.
* Kiểm tra vehicle không tồn tại.
* Lấy comparison.

### Integration Testing

Chuẩn bị hướng kiểm thử:

```text
Spring Boot
      ↕
PostgreSQL
```

Các giai đoạn sau sẽ mở rộng thêm:

```text
Spring Boot
      ↕
R Plumber
```

---

# 9. Chức năng của phần đã hoàn thành

Sau Increment 1, phần System Design của Member 05 đã hình thành nền tảng cho các chức năng:

```text
Vehicle Management
        │
        ├── Vehicle List
        ├── Vehicle Detail
        ├── Search
        └── Filter

Comparison
        │
        └── Compare Vehicles

Valuation
        │
        └── Predicted Price

Recommendation
        │
        └── Recommendation / Ranking

Testing
        │
        ├── Database Test
        ├── API Test
        └── Integration Test
```

---

# 10. Ghi chú

## 10.1. PostgreSQL

Database được thiết kế trên **PostgreSQL** theo kiến trúc của project.

## 10.2. Schema hiện tại

Schema hiện tại là **Foundation Schema**.

Workflow chưa xác định đầy đủ tất cả entity cuối cùng của hệ thống, vì vậy một số thành phần sẽ được mở rộng ở các Increment tiếp theo.

Ví dụ:

```text
Recommendation
User Preference
Raw Data
Crawler Source
Model Management
Authentication
```

chưa được đưa thành bảng chính thức trong schema hiện tại.

## 10.3. API

API Specification hiện tại là bản thiết kế ban đầu để thống nhất hướng giao tiếp giữa Frontend và Backend.

API có thể được điều chỉnh khi Member 01 hoàn thiện Controller, DTO và Service thực tế.

## 10.4. Coordination

Database cần được đồng bộ với:

```text
Member 01 → Spring Boot Entity / Repository
Member 03 → Clean Dataset / Seed Dataset
Member 04 → ML Feature / Prediction Output
Member 02 → API sử dụng cho Frontend
```

---

# 11. Đánh giá kết quả

### Hoàn thành

```text
[x] ERD
[x] Data Dictionary
[x] PostgreSQL Database Schema
[x] Use Case
[x] Class Diagram
[x] Initial API Specification
[x] Test Plan
```

### Mức độ hoàn thành

**Foundation Design: Hoàn thành**

Các tài liệu nền tảng cần thiết cho Increment 1 đã được chuẩn bị và tổ chức vào đúng các thư mục theo workflow.

### Hạn chế hiện tại

* Database chưa có dataset thực tế hoàn chỉnh.
* Recommendation logic chưa triển khai.
* Comparison business logic chưa triển khai hoàn chỉnh.
* API chưa phải implementation cuối cùng.
* Integration test giữa toàn bộ các module chưa thực hiện ở Increment 1.

Các phần này thuộc các Increment tiếp theo.

---

# 12. Kết quả nghiệm thu

## Kết quả

```text
DATABASE
    ↓
PostgreSQL Schema
    ↓
ERD
    ↓
Data Dictionary
```

```text
SYSTEM DESIGN
    ↓
Use Case
    ↓
Class Diagram
    ↓
Initial API Specification
```

```text
TESTING
    ↓
Initial Test Plan
```

### Kết luận nghiệm thu

Phần công việc **Member 05 — Increment 1 Foundation** đã hoàn thành ở mức thiết kế nền tảng.

Các tài liệu có thể được sử dụng làm cơ sở để:

* Member 01 triển khai Backend.
* Member 03 chuẩn bị dữ liệu và import vào PostgreSQL.
* Member 04 xác định feature/output cho model.
* Member 02 sử dụng API contract cho Frontend.

Workflow của project xác định PostgreSQL là trung tâm kết nối giữa Data Pipeline, Backend và Member 05.

---

# 13. Bàn giao

## Bàn giao cho Member 01

```text
database/schema/schema.sql
docs/UML/Class_Diagram.md
docs/API/API_Specification_Initial.md
```

Mục đích:

* Đồng bộ Entity.
* Đồng bộ Database.
* Đồng bộ API.
* Chuẩn bị Repository / Service / Controller.

---

## Bàn giao cho Member 03

```text
database/schema/schema.sql
docs/UML/ERD.md
docs/Database/Data_Dictionary.md
```

Mục đích:

* Xác định cấu trúc dữ liệu.
* Xác định field cần import.
* Chuẩn bị Seed Dataset.
* Chuẩn bị Clean Dataset phù hợp với database.

---

## Bàn giao cho Member 04

```text
docs/Database/Data_Dictionary.md
database/schema/schema.sql
```

Mục đích:

* Xác định các feature liên quan đến model.
* Xác định `predicted_price`.
* Xác định `model_version`.
* Đồng bộ output của Regression Model với hệ thống.

---

## Bàn giao cho Member 02

```text
docs/API/API_Specification_Initial.md
```

Mục đích:

* Nắm được API dự kiến.
* Chuẩn bị service gọi Backend.
* Chuẩn bị Vehicle List / Detail / Search / Filter.

---

# 14. Công việc tiếp theo

## Increment 2 — Market Data

Member 05 sẽ phối hợp với Member 03 và Member 01 để:

* Kiểm tra dữ liệu sau Import.
* Kiểm tra Database Integrity.
* Kiểm tra dữ liệu thực tế trong PostgreSQL.
* Kiểm thử Search API.
* Kiểm thử Filter API.
* Chuẩn bị Performance Test cơ bản.

Workflow quy định Increment 2 tập trung đưa dữ liệu thị trường qua:

```text
Crawler
 ↓
Raw Data
 ↓
Cleaning
 ↓
Validation
 ↓
Clean Data
 ↓
Batch Import
 ↓
PostgreSQL
```

và Member 05 có trách nhiệm kiểm tra dữ liệu sau Import và Database Integrity.

---

## Increment 3 — Automated Pricing

Member 05 sẽ tham gia:

* Integration Test giữa Spring Boot và R Plumber.
* Test Input Validation.
* Test Error Handling.
* Test Prediction Response.

Workflow xác định phần Integration Testing này thuộc trách nhiệm Member 05 trong Increment 3.

---

## Increment 4 — Recommendation & Decision Support

Đây là giai đoạn chính của Member 05.

Các nhiệm vụ:

### Recommendation

```text
Candidate Vehicles
       ↓
Price Score
       ↓
ODO Score
       ↓
Age Score
       ↓
Preference Score
       ↓
Market Fairness Score
       ↓
Recommendation Score
       ↓
Ranking
       ↓
Top Recommended Cars
```

### Comparison

So sánh:

```text
Price
Predicted Price
Difference
Year
ODO
Fuel
Transmission
Recommendation Score
```

### Testing

* Integration Test.
* API Test.
* System Test.
* Performance Test.
* Test Report.

Các nội dung trên phù hợp với trách nhiệm chính của Member 05 trong Increment 4 theo workflow.

---

# 15. Trạng thái tổng thể

```text
INCREMENT 1
    │
    ├── Database Schema          ✅
    ├── ERD                     ✅
    ├── Data Dictionary         ✅
    ├── Use Case                ✅
    ├── Class Diagram           ✅
    ├── Initial API             ✅
    └── Test Plan               ✅
    
    ↓

INCREMENT 2
    │
    ├── Database Integrity      ⏳
    ├── Data Import Validation  ⏳
    ├── Search API Test         ⏳
    ├── Filter API Test         ⏳
    └── Performance Test        ⏳
    
    ↓

INCREMENT 3
    │
    ├── R Plumber Integration   ⏳
    ├── Prediction Testing      ⏳
    └── Error Handling Test     ⏳
    
    ↓

INCREMENT 4
    │
    ├── Recommendation          ⏳
    ├── Comparison              ⏳
    ├── Ranking                 ⏳
    ├── Integration Test        ⏳
    ├── System Test             ⏳
    └── Performance Test        ⏳
```

---

# 16. Kết luận

Member 05 đã hoàn thành phần **Database / System Design Foundation** của Increment 1.

Kết quả hiện tại tạo nền tảng để hệ thống tiếp tục phát triển theo workflow:

```text
Member 03
Data Pipeline
      ↓
PostgreSQL
      ↓
Member 01
Spring Boot
      ↓
Member 02
ReactJS

Member 04
R / ML
      ↓
Prediction
      ↓
PostgreSQL

Member 05
Recommendation
Comparison
Testing
```

Trong các Increment tiếp theo, Member 05 sẽ chuyển trọng tâm từ **thiết kế nền tảng** sang **Database Testing → Integration Testing → Recommendation / Comparison / Decision Support**.
