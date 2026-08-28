# TV3.md — Data Engineering, Crawler & Data Cleaning

## 1. Vai trò

**Vai trò:** Data Engineer / Data Pipeline Developer

TV3 chịu trách nhiệm xây dựng pipeline thu thập, làm sạch, chuẩn hóa, validation và chuẩn bị dữ liệu xe cho PostgreSQL.

### Phạm vi chính

```text
crawler/
database/seed/
```

TV3 không chịu trách nhiệm chính về:
- Spring Boot.
- React.
- Huấn luyện Regression.
- Recommendation algorithm.

---

# 2. Mục tiêu dữ liệu

Dataset mục tiêu:

```text
2.000–5.000+ listings
```

Mỗi listing nên có thông tin đủ để:

- Hiển thị lên Web.
- Lọc/tìm kiếm.
- Đưa feature vào model nếu phù hợp.
- Truy xuất nguồn.

Các field mục tiêu:

```text
brand
model
variant
manufacture_year
price
mileage
fuel_type
transmission
body_type
location
source_url
image_url
listed_at
crawled_at
```

---

# 3. Increment 1 — Foundation

## 3.1. Chốt Data Contract

Làm việc với:

- TV4 để xác định feature Model.
- TV5 để xác định field Database.
- TV1 để xác định backend API contract.

Tạo documentation tại:

```text
crawler/README.md
```

## 3.2. Chuẩn bị Seed Dataset

Trước khi crawler hoàn chỉnh, chuẩn bị dataset nhỏ:

```text
500–1.000 records
```

để các thành viên khác development.

Vị trí:

```text
crawler/data/seed/
```

---

# 4. Increment 2 — Market Data

## 4.1. Crawler Chợ Tốt

Vị trí:

```text
crawler/src/crawlers/chotot/
├── crawler.py
└── parser.py
```

`crawler.py` chịu trách nhiệm lấy dữ liệu.

`parser.py` chịu trách nhiệm chuyển dữ liệu nguồn thành schema nội bộ.

## 4.2. Crawler Bonbanh

Vị trí:

```text
crawler/src/crawlers/bonbanh/
├── crawler.py
└── parser.py
```

Nếu nguồn không cần/không thể triển khai thực tế, không được tự tạo dữ liệu giả để tuyên bố là crawl.

## 4.3. Data Cleaning

Vị trí:

```text
crawler/src/cleaning/
├── clean_price.py
├── clean_mileage.py
├── clean_vehicle.py
└── validator.py
```

### Giá

Ví dụ:

```text
750 triệu
↓
750000000
```

### ODO

```text
45.000 km
↓
45000
```

### Năm

Kiểm tra range hợp lý.

### Missing

Xử lý theo rule đã thống nhất với TV4/TV5.

## 4.4. Duplicate Detection

Kiểm tra duplicate dựa trên các trường phù hợp như:

```text
source_url
source + source_id nếu có
```

Không được xóa hai listing khác nhau chỉ vì cùng model/giá.

---

# 5. Pipeline

Vị trí:

```text
crawler/src/pipeline/
├── crawl_pipeline.py
├── clean_pipeline.py
└── import_pipeline.py
```

Luồng:

```text
Source
 ↓
Raw
 ↓
Cleaning
 ↓
Validation
 ↓
Cleaned
 ↓
Database
```

Scripts:

```text
crawler/scripts/
├── crawl.py
├── clean.py
└── seed_database.py
```

---

# 6. Data Directory

Cấu trúc:

```text
crawler/data/
├── raw/
├── cleaned/
└── seed/
```

Quy tắc:

- Raw: dữ liệu thô.
- Cleaned: dữ liệu sau cleaning.
- Seed: dataset ổn định phục vụ demo/dev.

Không commit file dữ liệu dung lượng quá lớn nếu không cần thiết.

---

# 7. Increment 3 — Hỗ trợ Model

TV3 phải cung cấp cho TV4:

```text
Clean Dataset
```

đúng schema.

Cần document rõ:

```text
field name
type
unit
missing rule
example
```

TV4 không được phải tự đoán ý nghĩa field.

Ví dụ:

```text
price → VND
mileage → km
manufacture_year → integer
```

---

# 8. Increment 4 — Final Dataset

Chuẩn bị:

```text
2.000–5.000+ clean records
```

Kiểm tra:

- Không có price âm.
- Không có mileage âm.
- Year hợp lệ.
- URL tồn tại nếu source yêu cầu.
- Field bắt buộc không rỗng.
- Encoding tiếng Việt đúng.
- Không duplicate bất hợp lý.

Chuẩn bị dataset phục vụ:

```text
demo
database seed
performance test
model validation
```

---

# 9. Bàn giao

### TV4

Bàn giao:

```text
clean dataset
data dictionary
feature availability
data quality report
```

TV4 dùng cho Regression.

### TV5

Bàn giao:

```text
seed dataset
listing fields
source information
crawl timestamps
```

### TV1

Bàn giao:

```text
database-ready dataset
import instructions
field mapping
```

### TV2

Không cần code, nhưng phải cung cấp field/format hiển thị nếu có yêu cầu.

---

# 10. Tiêu chí nghiệm thu TV3

- Có pipeline crawl.
- Có parser.
- Có cleaning.
- Có validation.
- Có duplicate handling.
- Có seed dataset.
- Có dataset tối thiểu khoảng 2.000 records ở bản cuối.
- Các field theo Data Contract đầy đủ.
- Import vào PostgreSQL thành công.
- Có source_url/listed_at/crawled_at phù hợp.
- Có README hướng dẫn chạy pipeline.

---

# 11. Không làm ngoài phạm vi

Không xây:

- Spring Boot.
- React.
- Regression model.
- Deep Learning.
- Recommendation engine.
- Payment/chat.
