# TV1.md — Backend & System Integration

## 1. Vai trò

**Vai trò:** Backend Developer & System Integration Lead

TV1 phụ trách xây dựng Core Backend bằng Java Spring Boot, kết nối PostgreSQL, giao tiếp với R Model API và tích hợp các nghiệp vụ chính của hệ thống.

### Phạm vi chính

```text
backend/
docker-compose.yml
docs/UML/Sequence_Diagram/
docs/UML/Deployment_Diagram/
```

TV1 không chịu trách nhiệm chính về:
- Giao diện React.
- Logic crawl dữ liệu.
- Huấn luyện Regression.
- Thiết kế Recommendation thuật toán chi tiết.

TV1 chịu trách nhiệm biến các module đó thành một hệ thống có thể giao tiếp với nhau.

---

# 2. Nguyên tắc làm việc

- Không truy cập PostgreSQL trực tiếp từ Frontend.
- Frontend chỉ gọi REST API của Spring Boot.
- Spring Boot giao tiếp với PostgreSQL bằng JPA/Repository.
- Spring Boot giao tiếp với R Plumber bằng HTTP qua `RModelClient`.
- Không nhúng code R trực tiếp vào Java.
- Không đưa mật khẩu Database/API thật vào Git.
- API phải có validation và xử lý lỗi cơ bản.

Luồng tổng quát:

```text
React
  ↓ HTTP/JSON
Spring Boot
  ├── PostgreSQL
  └── R Plumber
```

---

# 3. Increment 1 — Foundation

## 3.1. Khởi tạo Spring Boot

Vị trí:

```text
backend/
├── pom.xml
├── mvnw
├── mvnw.cmd
└── src/
```

Cần cấu hình tối thiểu:

- Spring Web.
- Spring Data JPA.
- PostgreSQL Driver.
- Validation.
- Lombok nếu nhóm thống nhất sử dụng.

Kiểm tra:

```bash
./mvnw clean test
```

hoặc trên Windows:

```powershell
.\mvnw.cmd clean test
```

## 3.2. Xây dựng cấu trúc package

Tạo:

```text
backend/src/main/java/com/system/

├── config/
├── controller/
├── service/
├── repository/
├── entity/
├── dto/
├── mapper/
├── client/
├── exception/
└── util/
```

## 3.3. Cấu hình Database

Vị trí:

```text
backend/src/main/resources/
├── application.properties
├── application-dev.properties
└── application-prod.properties
```

Cấu hình kết nối PostgreSQL theo environment variable.

Không hard-code password.

## 3.4. Vehicle CRUD

Phối hợp với TV5 để xác định schema.

Tạo:

```text
entity/Vehicle.java
repository/VehicleRepository.java
service/VehicleService.java
controller/VehicleController.java
dto/vehicle/
```

Chức năng:

```text
Create
Read
Update
Delete
Get by ID
Get all
```

API dự kiến:

```text
GET    /api/v1/vehicles
GET    /api/v1/vehicles/{id}
POST   /api/v1/vehicles
PUT    /api/v1/vehicles/{id}
DELETE /api/v1/vehicles/{id}
```

## 3.5. Listing

Tạo các thành phần tương ứng:

```text
Listing.java
ListingRepository.java
ListingService.java
ListingController.java
dto/listing/
```

Thực hiện các API đọc dữ liệu Listing cơ bản.

## 3.6. Exception Handling

Vị trí:

```text
backend/.../exception/
```

Tạo:

```text
GlobalExceptionHandler.java
ResourceNotFoundException.java
```

API cần trả lỗi có cấu trúc thay vì stack trace.

---

# 4. Increment 2 — Market Data

## 4.1. Search API

Phụ trách API tìm kiếm:

```text
GET /api/v1/vehicles
```

Hỗ trợ các điều kiện:

- Brand.
- Model.
- Price min/max.
- Manufacture year min/max.
- Mileage min/max.
- Fuel type.
- Transmission.
- Body type.
- Location nếu cần.

## 4.2. Pagination

Hỗ trợ:

```text
page
size
```

Ví dụ:

```text
?page=0&size=20
```

## 4.3. Sorting

Hỗ trợ các trường phù hợp:

```text
price
manufacture_year
mileage
```

Không để frontend tự xử lý toàn bộ dữ liệu; Backend phải phân trang/lọc ở Database.

## 4.4. Phối hợp với TV3

TV3 chịu trách nhiệm:

```text
Crawler
Cleaning
Seed Data
```

TV1 cần nhận dataset/schema cuối từ TV3 và TV5 để đảm bảo API đọc đúng field.

## 4.5. Phối hợp với TV2

Gửi cho TV2:

- API URL.
- HTTP method.
- Request parameters.
- JSON response.
- Error format.

---

# 5. Increment 3 — Automated Pricing

## 5.1. R Model Client

Vị trí:

```text
backend/src/main/java/com/system/client/
└── RModelClient.java
```

Nhiệm vụ:

- Gửi request HTTP tới Plumber.
- Mapping request/response.
- Timeout.
- Xử lý lỗi khi R Model không hoạt động.

## 5.2. Valuation Service

Vị trí:

```text
backend/.../service/ValuationService.java
```

Luồng:

```text
Frontend
   ↓
ValuationController
   ↓
ValuationService
   ↓
RModelClient
   ↓
R Plumber
   ↓
Prediction
```

## 5.3. Valuation Controller

Vị trí:

```text
controller/ValuationController.java
```

API dự kiến:

```text
POST /api/v1/valuation
```

Input là các feature mà TV4 xác định cho model.

Output tối thiểu:

```json
{
  "predicted_price": 495000000,
  "model_version": "regression_v1"
}
```

Không tự ý thay đổi feature contract. TV1 phải thống nhất với TV4.

## 5.4. Prediction cho Listing

Khi cần tạo prediction cho dữ liệu trong Database:

```text
Listing
   ↓
Valuation Service
   ↓
R Model
   ↓
Prediction
   ↓
Database
```

Không gọi R API lại mỗi lần frontend mở một danh sách nếu prediction đã được tính và lưu.

---

# 6. Increment 4 — Recommendation & Decision Support

## 6.1. Recommendation API

TV5 chịu trách nhiệm chính về thuật toán score.

TV1 phụ trách tích hợp thành Backend service/API.

Vị trí:

```text
controller/RecommendationController.java
service/RecommendationService.java
```

API dự kiến:

```text
GET/POST /api/v1/recommendations
```

## 6.2. Comparison API

Vị trí:

```text
controller/ComparisonController.java
service/ComparisonService.java
```

Cho phép nhận 2–3 vehicle/listing IDs và trả về dữ liệu so sánh.

## 6.3. Smart Tagging

TV5 thống nhất rule:

```text
difference < -5%      → GOOD_DEAL
-5% ≤ difference ≤ 5% → FAIR_PRICE
difference > 5%       → OVERPRICED
```

TV1 triển khai service/DTO/response theo business rule đã chốt.

Công thức:

```text
difference_percent =
(actual_price - predicted_price)
/
predicted_price × 100
```

## 6.4. Model version

Prediction phải lưu/return:

```text
predicted_price
model_version
predicted_at
```

---

# 7. Docker & Deployment

## 7.1. Phạm vi

TV1 phụ trách:

```text
docker-compose.yml
```

Mục tiêu cuối:

```text
PostgreSQL
R Plumber
Spring Boot
```

có thể chạy cùng nhau.

## 7.2. Environment

Không commit:

```text
.env
```

Chỉ commit:

```text
.env.example
```

TV1 cần document:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USERNAME
DB_PASSWORD
R_MODEL_URL
```

## 7.3. Kiểm thử

Tối thiểu:

```bash
docker compose up -d
docker compose ps
docker compose logs
```

Kiểm tra:

```text
Frontend → Backend
Backend → PostgreSQL
Backend → R Plumber
```

---

# 8. Tài liệu UML phải bàn giao

## Sequence Diagram

Vị trí:

```text
docs/UML/Sequence_Diagram/
```

Ít nhất có:

1. Search Vehicle.
2. User Valuation.
3. Recommendation.
4. Compare Vehicle.

## Deployment Diagram

Vị trí:

```text
docs/UML/Deployment_Diagram/
```

Thể hiện:

```text
Browser
 ↓
React
 ↓
Spring Boot
 ├── PostgreSQL
 └── R Plumber
```

---

# 9. Tiêu chí nghiệm thu TV1

TV1 hoàn thành khi:

- Spring Boot build thành công.
- Kết nối PostgreSQL thành công.
- Vehicle CRUD hoạt động.
- Listing API hoạt động.
- Search/filter/pagination/sorting hoạt động.
- API Valuation gọi được R Plumber.
- Recommendation API tích hợp được logic của TV5.
- Comparison API hoạt động.
- Exception handling hoạt động.
- Không hard-code secret.
- Docker Compose khởi động được các service phụ trách.
- Sequence và Deployment Diagram hoàn thành.

---

# 10. Bàn giao cho ai?

### Bàn giao cho TV2

```text
API Specification
Endpoint
Request
Response
Error format
```

để TV2 tích hợp Frontend.

### Bàn giao cho TV3

Schema/contract của dữ liệu mà Backend cần nhận từ pipeline.

### Bàn giao cho TV4

Model API contract:

```text
Input features
Output JSON
model_version
```

### Bàn giao cho TV5

Service interface liên quan:

```text
Prediction data
Vehicle data
Listing data
```

để xây Recommendation.

### Bàn giao cho toàn nhóm

```text
backend/
docker-compose.yml
docs/UML/Sequence_Diagram/
docs/UML/Deployment_Diagram/
```

---

# 11. Không làm ngoài phạm vi

TV1 không tự phát triển:

- Crawler.
- Regression training.
- UI React.
- Deep Learning.
- Authentication phức tạp.
- Payment.
- Chat.
- Kafka/Kubernetes.
