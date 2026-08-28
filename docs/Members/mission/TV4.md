# TV4.md — Machine Learning, Regression & R Plumber

## 1. Vai trò

**Vai trò:** Machine Learning Engineer / R Developer

TV4 chịu trách nhiệm biến mô hình Regression từ môn Lập trình R thành Model Engine có thể được Backend gọi qua REST API.

### Phạm vi chính

```text
model/
```

TV4 không phụ trách Spring Boot business logic hay React UI.

---

# 2. Mục tiêu

Hệ thống cần hỗ trợ hai use case:

### Use case A — User Valuation

Người dùng nhập một chiếc xe:

```text
features
↓
Regression
↓
Estimated Market Price
```

### Use case B — Listing Valuation

Một listing có sẵn:

```text
Listing features
↓
Regression
↓
Predicted Price
↓
Smart Tagging
```

Database price là **giá rao bán quan sát được**, còn Regression tạo **giá ước lượng**.

---

# 3. Increment 1 — Regression Foundation

## 3.1. Đưa model cũ vào project

Vị trí:

```text
model/regression/
```

Cấu trúc:

```text
data/
src/
models/
reports/
```

## 3.2. Preprocessing

Vị trí:

```text
model/regression/src/preprocessing.R
```

Xác định:

- Feature.
- Encoding.
- Missing values.
- Data type.
- Unit.
- Feature engineering.

## 3.3. Train/Test

Không đánh giá model bằng cách predict chính training data.

Luồng:

```text
Dataset
 ↓
Train/Test split
 ↓
Train
 ↓
Test
 ↓
Evaluation
```

## 3.4. Training

Vị trí:

```text
train_model.R
```

Output:

```text
model/regression/models/regression_v1.rds
```

## 3.5. Evaluation

Vị trí:

```text
evaluate_model.R
```

Báo cáo:

```text
R²
MAE
RMSE
MAPE nếu phù hợp
```

Không tự đặt số liệu đẹp; phải dùng kết quả thực tế.

---

# 4. Feature Contract

TV4 phải chốt với TV3 và TV1:

```text
Input feature
Data type
Required/Optional
Unit
Allowed values
Example
```

Đặc biệt với:

```text
vehicle_age
listed_year
listed_month
```

Nếu model dùng thời gian, phải phân biệt:

```text
manufacture_year
listed_year
crawled_at
```

Không mặc định dùng:

```text
Current Year - Manufacture Year
```

cho mọi bối cảnh.

Với listing historical:

```text
vehicle_age =
listed_year - manufacture_year
```

nếu model/thiết kế sử dụng feature này.

---

# 5. Increment 2 — Dataset Integration

Nhận:

```text
crawler/data/cleaned/
```

từ TV3.

Kiểm tra:

- Data types.
- Missing.
- Category mismatch.
- Distribution shift.
- Outlier.
- Unit.

Nếu feature model không có trong crawler data:

- Báo ngay cho TV3.
- Cùng điều chỉnh schema.
- Không tự tạo dữ liệu giả để lấp feature.

---

# 6. Increment 3 — Plumber API

## 6.1. Cấu trúc

```text
model/plumber/
├── plumber.R
├── handlers/
│   └── prediction_handler.R
├── schemas/
│   └── prediction_schema.json
└── config/
    └── config.R
```

## 6.2. Prediction Endpoint

Ví dụ:

```text
POST /predict
```

Input:

```json
{
  "brand": "Toyota",
  "model": "Vios",
  "manufacture_year": 2021,
  "mileage": 45000,
  "fuel_type": "Gasoline",
  "transmission": "Automatic"
}
```

Output:

```json
{
  "predicted_price": 495000000,
  "model_version": "regression_v1"
}
```

Output có thể mở rộng khi thống nhất.

## 6.3. Validation

R API phải kiểm tra:

- Missing required field.
- Sai type.
- Giá trị không hợp lệ.
- Category không tồn tại.

Không để lỗi R thô trả thẳng cho người dùng.

---

# 7. Model Versioning

Mỗi model phải có version:

```text
regression_v1
regression_v2
...
```

Kết quả dự đoán cần có:

```text
model_version
predicted_at
```

Nếu thay model:

```text
regression_v2
```

không được ghi đè khiến nhóm mất khả năng truy vết.

---

# 8. Smart Tagging — Phối hợp TV5

TV4 chịu trách nhiệm **Prediction**.

TV5/Backend chịu trách nhiệm chính về **business classification**.

Công thức thống nhất:

```text
difference_percent =
(actual_price - predicted_price)
/
predicted_price × 100
```

Rule:

```text
< -5%           → Giá tốt
-5% đến +5%     → Giá hợp lý
> +5%           → Giá cao
```

TV4 không được tự thay đổi rule mà không thông báo TV5/TV1.

---

# 9. Model Quality

Tài liệu:

```text
model/regression/reports/
├── metrics.csv
└── model_evaluation.md
```

Phải ghi:

- Dataset.
- Train/test method.
- Features.
- Metrics.
- Hạn chế của model.

Cần nêu rõ:

> Giá dự đoán là giá tham khảo, không phải giá thẩm định pháp lý.

---

# 10. Bàn giao

### TV3

Nhận:

```text
feature contract
required columns
data quality requirements
```

### TV1

Bàn giao:

```text
R API endpoint
input schema
output schema
R_MODEL_URL expectation
model_version
error behavior
```

### TV2

Bàn giao:

```text
Valuation input fields
Prediction output
model version
```

### TV5

Bàn giao:

```text
predicted_price
model_version
prediction metadata
```

để TV5 xây Smart Tagging/Recommendation.

---

# 11. Tiêu chí nghiệm thu TV4

- Model train được.
- Có test/evaluation.
- Có `.rds`.
- Có metrics report.
- Plumber chạy được.
- POST `/predict` trả kết quả đúng schema.
- Validation hoạt động.
- Backend TV1 gọi được R API.
- Model version được trả về.
- Không phụ thuộc trực tiếp vào Frontend/Database.

---

# 12. Không làm ngoài phạm vi

Không xây:

- Spring Boot.
- React.
- Crawler.
- Recommendation Deep Learning.
- Payment/chat.
- Kubernetes.
