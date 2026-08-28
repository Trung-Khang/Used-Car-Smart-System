# TV2.md — Frontend & UI/UX

## 1. Vai trò

**Vai trò:** Frontend Developer & UI/UX

TV2 xây dựng toàn bộ giao diện ReactJS, kết nối Spring Boot REST API và trình bày dữ liệu định giá, Recommendation và Comparison.

### Phạm vi chính

```text
frontend/
docs/UML/Use_Case/
```

TV2 không phụ trách logic truy vấn Database hay code Regression.

---

# 2. Nguyên tắc làm việc

- Không gọi PostgreSQL trực tiếp.
- Chỉ gọi Spring Boot API.
- Không nhúng logic Regression vào React.
- Không hard-code dữ liệu demo khi API đã sẵn sàng.
- Components phải tái sử dụng.
- Tách Page, Component, API service.
- Giao diện phải responsive.

---

# 3. Increment 1 — Foundation

## 3.1. Khởi tạo React

Vị trí:

```text
frontend/
```

Khởi tạo React + Vite.

Kiểm tra:

```bash
npm install
npm run dev
```

## 3.2. Cấu trúc

Duy trì:

```text
src/
├── components/
├── pages/
├── services/
├── hooks/
├── context/
├── utils/
├── assets/
└── styles/
```

## 3.3. Layout

Tạo:

```text
components/common/
├── Navbar.jsx
├── Footer.jsx
├── Loading.jsx
└── ErrorMessage.jsx
```

Tạo:

```text
pages/HomePage.jsx
```

## 3.4. Vehicle UI

Tạo:

```text
components/vehicle/
├── VehicleCard.jsx
├── VehicleGrid.jsx
└── VehicleInfo.jsx
```

Tạo:

```text
pages/
├── VehicleListPage.jsx
└── VehicleDetailPage.jsx
```

## 3.5. Kết nối Backend

Vị trí:

```text
src/services/
├── api.js
└── vehicleApi.js
```

TV2 nhận API contract từ TV1.

---

# 4. Increment 2 — Market Data

## 4.1. Filter UI

Vị trí:

```text
components/filter/
├── FilterPanel.jsx
├── PriceFilter.jsx
├── YearFilter.jsx
└── MileageFilter.jsx
```

Filter mục tiêu:

- Hãng/model.
- Khoảng giá.
- Năm.
- ODO.
- Nhiên liệu.
- Hộp số.
- Kiểu dáng.

## 4.2. Search

Search phải gọi Backend:

```text
GET /api/v1/vehicles
```

Không lấy toàn bộ 5.000 record rồi filter bằng JavaScript nếu API đã hỗ trợ server-side filter.

## 4.3. Pagination

Hiển thị:

```text
Previous
1 2 3 ...
Next
```

## 4.4. Sorting

Cho phép:

```text
Giá thấp → cao
Giá cao → thấp
Xe đời mới
ODO thấp
```

---

# 5. Increment 3 — Automated Pricing

## 5.1. Valuation Page

Vị trí:

```text
pages/ValuationPage.jsx
```

Components:

```text
components/valuation/
├── ValuationForm.jsx
└── ValuationResult.jsx
```

Form lấy chính xác feature contract từ TV4.

Ví dụ:

```text
Brand
Model
Manufacture Year
Mileage
Fuel
Transmission
...
```

## 5.2. Valuation API

Vị trí:

```text
services/valuationApi.js
```

Gọi:

```text
POST /api/v1/valuation
```

Hiển thị:

```text
Giá thị trường ước tính
Model version
```

## 5.3. Smart Tagging

Vehicle Card/Detail phải hiển thị:

```text
Giá rao
Giá dự đoán
Chênh lệch %
Nhãn:
- Giá tốt
- Giá hợp lý
- Giá cao
```

---

# 6. Increment 4 — Decision Support

## 6.1. Recommendation

Tạo:

```text
pages/RecommendationPage.jsx

components/recommendation/
├── RecommendationCard.jsx
└── RecommendationList.jsx
```

API:

```text
services/recommendationApi.js
```

Hiển thị:

```text
Top recommended vehicles
Recommendation Score
Reason
```

## 6.2. Compare

Tạo:

```text
pages/ComparePage.jsx

components/comparison/
├── CompareTable.jsx
└── CompareChart.jsx
```

Cho phép chọn 2–3 xe.

Hiển thị tối thiểu:

```text
Price
Predicted Price
Difference
Year
Mileage
Fuel
Transmission
Recommendation Score
```

## 6.3. Visualization

Dùng Recharts hoặc Plotly.

Biểu đồ tối thiểu:

- Giá rao bán vs giá dự đoán.
- So sánh score.
- Có thể thêm ODO/tuổi xe nếu cần.

---

# 7. UX & Responsive

Kiểm tra:

```text
Desktop
Tablet
Mobile
```

Các trạng thái phải có:

```text
Loading
Empty result
API error
Invalid input
No recommendation
```

---

# 8. Use Case Documentation

Vị trí:

```text
docs/UML/Use_Case/
```

TV2 phụ trách xây dựng/hoàn thiện:

- Actor.
- Search Vehicle.
- View Vehicle Detail.
- Valuation.
- Recommendation.
- Comparison.

TV2 phối hợp TV1 và TV5 để bảo đảm Use Case khớp hệ thống thực tế.

---

# 9. Tiêu chí nghiệm thu TV2

- React build/run thành công.
- Home page hoạt động.
- Vehicle list hoạt động.
- Vehicle detail hoạt động.
- Search/filter hoạt động.
- Pagination hoạt động.
- Valuation hoạt động.
- Smart Tagging hiển thị đúng.
- Recommendation hiển thị đúng.
- Compare 2–3 xe hoạt động.
- Chart hoạt động.
- Responsive.
- Không hard-code business result.

---

# 10. Bàn giao

### TV1

Bàn giao:

```text
API endpoints
Request/response
Error contract
```

### TV3

Không cần trực tiếp nhận code, chỉ cần nhận yêu cầu field để hiển thị.

### TV4

Nhận:

```text
Valuation input fields
Prediction output format
```

### TV5

Nhận:

```text
Recommendation response
Comparison data structure
```

### Toàn nhóm

Bàn giao:

```text
frontend/
docs/UML/Use_Case/
```
