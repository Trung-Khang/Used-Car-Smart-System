# TV3 — DATA ENGINEERING & DATA PIPELINE REPORT

**Project:** `Used-Car-Smart-System`
**Role:** TV3 — Data Engineering / Data Pipeline Developer
**Scope:** Data Crawling → Data Merge → Data Cleaning → Data Validation → Seed Generation
**Final Dataset:** **10,813 real marketplace records**
**Final Data Quality:** **98.41 / 100 — Grade A**
**Final Status:** **COMPLETE — READY FOR DATABASE HANDOFF**

---

# 1. Executive Summary

TV3 chịu trách nhiệm xây dựng và hoàn thiện toàn bộ quy trình Data Engineering cho hệ thống `Used-Car-Smart-System`.

Phạm vi công việc bao gồm:

```text
Chợ Tốt ───────┐
               │
               ▼
          Raw Crawling
               │
Bonbanh ───────┘
               │
               ▼
        Raw Dataset
               │
               ▼
            MERGE
               │
               ▼
      Unified Raw Dataset
               │
               ▼
           CLEANING
               │
               ▼
       Cleaned Dataset
               │
               ▼
          VALIDATION
               │
               ▼
       Validated Dataset
               │
               ▼
       SEED GENERATION
               │
               ▼
       Database-ready Data
               │
               ▼
       DATABASE HANDOFF
               │
               ▼
     TV5 / Database Owner
```

Sau toàn bộ pipeline, TV3 đã tạo được:

* **10,813 records thực tế**
* **3,116 records từ Chợ Tốt**
* **7,697 records từ Bonbanh**
* 14-field canonical data contract
* 100% source URL hợp lệ và unique
* 0 exact duplicate records
* 100% critical-field completeness
* Quality Score **98.41/100 — Grade A**
* Seed JSON, CSV và SQL
* Import pipeline có khả năng tái sử dụng
* Báo cáo machine-readable
* Documentation đầy đủ
* Raw và cleaned dataset được kiểm chứng checksum

Physical database import **không nằm trong phạm vi hoàn thành của TV3**, do database schema/migration thuộc thành viên phụ trách Database. TV3 đã dừng đúng tại điểm bàn giao để không tự ý thiết kế hoặc thay đổi database architecture.

---

# 2. Responsibility & Scope

## 2.1. TV3 chịu trách nhiệm

TV3 chịu trách nhiệm:

* Web crawling
* Raw data collection
* Checkpoint/resume
* Retry và rate limiting
* Parser
* Dataset merge
* Data cleaning
* Data normalization
* Data validation
* Data quality assessment
* Seed generation
* Import preparation
* Data lineage
* Documentation

## 2.2. TV3 không chịu trách nhiệm

Các nội dung sau nằm ngoài phạm vi TV3:

* Thiết kế database architecture
* Database migration
* Thay đổi backend entity
* Spring Boot API
* Frontend
* Regression model
* Recommendation system
* Real-time data synchronization

Đặc biệt, pipeline của TV3 là **batch pipeline**, không phải real-time pipeline.

---

# 3. Data Contract

Toàn bộ pipeline sử dụng canonical schema gồm 14 trường:

|  # | Field              | Ý nghĩa         |
| -: | ------------------ | --------------- |
|  1 | `brand`            | Thương hiệu     |
|  2 | `model`            | Dòng xe         |
|  3 | `variant`          | Phiên bản       |
|  4 | `manufacture_year` | Năm sản xuất    |
|  5 | `price`            | Giá bán, VND    |
|  6 | `mileage`          | Số km đã đi     |
|  7 | `fuel_type`        | Loại nhiên liệu |
|  8 | `transmission`     | Hộp số          |
|  9 | `body_type`        | Kiểu thân xe    |
| 10 | `location`         | Địa điểm        |
| 11 | `source_url`       | URL nguồn       |
| 12 | `image_url`        | URL hình ảnh    |
| 13 | `listed_at`        | Thời điểm đăng  |
| 14 | `crawled_at`       | Thời điểm crawl |

Các trường được duy trì nhất quán xuyên suốt Raw → Merge → Clean → Validation → Seed.

---

# 4. Data Sources

TV3 thu thập dữ liệu từ hai marketplace thực tế:

| Source     |    Records |    Tỷ lệ |
| ---------- | ---------: | -------: |
| Chợ Tốt Xe |      3,116 |   28.82% |
| Bonbanh    |      7,697 |   71.18% |
| **Total**  | **10,813** | **100%** |

Dữ liệu được crawl từ các listing thực tế tại thời điểm crawl.

`crawled_at` chỉ biểu thị thời điểm dữ liệu được thu thập.

Hệ thống **không triển khai real-time synchronization**.

---

# 5. Crawling & Data Acquisition

## 5.1. Chợ Tốt

Crawler sử dụng browser automation để xử lý nội dung động.

Các cơ chế chính:

* Playwright
* Browser channel fallback
* Pagination
* Scrolling/lazy-loading
* URL discovery
* Detail-page parsing
* Retry
* Rate limiting
* Checkpoint
* Batch output
* Logging

Checkpoint cuối:

```text
Page: 181
Records: 3,116
```

Kết quả production:

```text
Previous records: 976
Additional records: 2,140
Final records: 3,116
Duplicate URLs skipped: 218
Parse failures: 0
Network failures: 0
```

---

## 5.2. Bonbanh

Crawler sử dụng HTTP session với:

* Persistent cookies
* Browser-like headers
* Retry
* Backoff
* Rate limiting
* Pagination
* Detail-page parsing
* Checkpoint
* Batch output

Checkpoint cuối:

```text
Page: 512
Records: 7,697
```

Kết quả production:

```text
Previous records: 913
Additional records: 6,784
Final records: 7,697
Duplicate URLs skipped: 1,268
Parse failures: 0
Network failures: 0
```

---

# 6. Production Dataset

Sau khi hoàn thành production crawl:

```text
Chợ Tốt:       3,116
Bonbanh:       7,697
----------------------
Total:        10,813
```

Smoke-test records được loại khỏi production dataset và không được sử dụng để làm tăng giả số lượng dữ liệu.

TV3 không sử dụng dữ liệu giả hoặc duplicate nhân tạo để đạt target.

---

# 7. Phase 3 — Data Merge

Tất cả production raw batches được hợp nhất thành:

```text
crawler/data/merged/vehicles_raw_merged.json
```

Kết quả:

```text
Input records:       10,813
Output records:      10,813
Discarded:                 0
Duplicate URLs:            0
Schema violations:         0
```

Dataset giữ nguyên:

* source
* source_url
* raw values
* crawled_at
* listed_at

Không thực hiện cross-source vehicle deduplication.

Điều này có nghĩa là nếu cùng một mẫu xe xuất hiện trên Chợ Tốt và Bonbanh, hai listing vẫn được giữ riêng.

---

# 8. Phase 4 — Data Cleaning

## 8.1. Cleaning Architecture

Pipeline cleaning được tổ chức theo module:

```text
crawler/src/cleaning/
├── __init__.py
├── clean_price.py
├── clean_mileage.py
├── clean_vehicle.py
└── validator.py

crawler/src/pipeline/
└── clean_pipeline.py
```

Mục tiêu là biến đổi dữ liệu về dạng thống nhất nhưng vẫn giữ nguyên thông tin thực tế.

---

## 8.2. Cleaning Rules

### Price

Chuyển giá về integer VND.

Ví dụ:

```text
590 triệu
→
590000000
```

### Mileage

Chuyển mileage về integer km.

Giá trị không parse được được giữ là:

```text
NULL
```

Không tự động thay thế bằng 0.

### Manufacture Year

Chuẩn hóa về:

```text
INT
```

### Transmission

Chuẩn hóa về vocabulary:

```text
Automatic
Manual
Semi-Automatic
Other
```

### Fuel Type

Chuẩn hóa về:

```text
Gasoline
Diesel
Electric
Hybrid
Other
```

### Brand / Model

Chuẩn hóa casing và một số tên thương hiệu:

```text
Mercedes Benz → Mercedes-Benz
LandRover → Land Rover
Rolls Royce → Rolls-Royce
```

### Location

Chuẩn hóa một số cách viết địa phương:

```text
TP HCM → Hồ Chí Minh
Đăk Lăk → Đắk Lắk
```

### Null Values

Null-like values được chuyển thành:

```text
NULL
```

Không thực hiện synthetic imputation.

---

# 9. Cleaning Result

Input:

```text
10,813
```

Output:

```text
10,813
```

Không record nào bị xóa trong cleaning.

| Field           |  Null |
| --------------- | ----: |
| `mileage`       | 2,307 |
| `variant`       | 1,473 |
| `body_type`     | 1,061 |
| `listed_at`     |     1 |
| Critical fields |     0 |

Raw dataset vẫn giữ nguyên.

SHA-256 của raw merged dataset:

```text
6353550dc7f7f8ce20797ddfab9ac9f8b7b4d2452f14f28363aa8ef377db1fcd
```

---

# 10. Phase 5 — Data Validation

Validation được thực hiện trên toàn bộ:

```text
10,813 / 10,813 records
```

Coverage:

```text
100%
```

---

# 11. Schema Validation

14-field contract:

```text
Missing fields:       0
Extra fields:         0
Malformed records:    0
```

Kết quả:

```text
PASS
```

---

# 12. Type Validation

Các trường:

```text
price
mileage
manufacture_year
```

được kiểm tra theo:

```text
int | null
```

Timestamp được kiểm tra theo ISO-8601.

Kết quả:

```text
Type errors: 0
Timestamp errors: 0
```

---

# 13. Critical Field Completeness

Các critical fields:

```text
brand
model
manufacture_year
price
location
source_url
crawled_at
```

đạt:

```text
100% completeness
```

Không có critical field bị NULL.

---

# 14. Source Traceability

Toàn bộ 10,813 records có:

* HTTPS `source_url`
* source lineage
* `crawled_at`

Kiểm tra:

```text
Valid URLs:       10,813
Unique URLs:      10,813
Duplicate URLs:        0
```

Kết quả:

```text
PASS
```

---

# 15. Statistical Validation & Anomalies

## 15.1. Price

Distribution:

```text
Min:       5,000,000 VND
Q1:      390,000,000 VND
Median:  590,000,000 VND
Mean:    993,567,814 VND
Q3:      960,000,000 VND
P95:   2,980,000,000 VND
P99:   7,199,000,000 VND
Max:  33,000,000,000 VND
```

Có 6 listing giá dưới 10 triệu VND.

Kiểm tra cho thấy các listing này có đặc điểm liên quan đến:

* trả trước
* trả góp
* phí thuê/thanh toán định kỳ

Do đó các record được giữ nguyên.

---

## 15.2. Mileage

```text
Populated: 8,506
NULL:      2,307
Median:   54,000 km
P99:     300,000 km
```

Có 8 giá trị cực đoan trên 1 triệu km.

Ví dụ:

```text
3,380,000,000 km
150,000,000 km
```

Các giá trị này được giữ lại vì có thể là seller typo và việc tự động xóa dữ liệu nằm ngoài phạm vi validation.

---

## 15.3. Manufacture Year

```text
Range: 1980–2026
Future years: 0
Vintage (<1990): 11
Vehicles >=2020: 7,991
```

Không phát hiện manufacture year vượt quá 2026.

---

# 16. Categorical Validation

## Transmission

| Category       | Count |
| -------------- | ----: |
| Automatic      | 9,577 |
| Manual         | 1,214 |
| Semi-Automatic |    21 |
| Other          |     1 |

Record `Other` xuất phát từ raw value:

```text
"5"
```

Record được giữ nguyên và ghi nhận là parser anomaly.

---

## Fuel Type

| Category | Count |
| -------- | ----: |
| Gasoline | 7,543 |
| Diesel   | 1,565 |
| Electric | 1,204 |
| Hybrid   |   500 |
| Other    |     1 |

Record `Other` xuất phát từ:

```text
"Loại khác 2.5 L"
```

Có khả năng đây là thông tin động cơ được parser lấy nhầm vào fuel type.

Record vẫn được giữ lại.

---

# 17. Cross-Source Similarity

Validation phát hiện:

```text
986 potential overlapping listings
```

Tỷ lệ:

```text
9.12%
```

Điều kiện matching bảo thủ:

```text
brand
model
manufacture_year
price ±5%
mileage ±10%
```

Đây chỉ là **potential similarity**, không phải bằng chứng cùng một chiếc xe.

Do đó:

```text
Cross-source deduplication = NOT PERFORMED
```

Tất cả records vẫn được giữ.

---

# 18. Data Quality Score

Quality score sử dụng mô hình 100 điểm:

| Component                 |     Max |     Score |
| ------------------------- | ------: | --------: |
| Schema Integrity          |      20 |     20.00 |
| Type Integrity            |      20 |     20.00 |
| Source Traceability       |      20 |     20.00 |
| Critical Completeness     |      20 |     20.00 |
| Non-Critical Completeness |      10 |      8.51 |
| Semantic Validity         |      10 |      9.90 |
| **Total**                 | **100** | **98.41** |

Final:

```text
98.41 / 100
Grade A
PASS WITH WARNINGS
```

Các warnings phản ánh dữ liệu marketplace thực tế thay vì lỗi hệ thống nghiêm trọng.

---

# 19. Downstream Recommendations

Một số anomaly không bị xóa khỏi dataset nhưng cần được lưu ý khi TV4/TV5 sử dụng dữ liệu cho ML.

### Price

Có thể cân nhắc:

```text
price >= 30,000,000 VND
```

khi xây dựng model dự đoán giá để giảm ảnh hưởng của các listing trả trước/trả góp.

### Mileage

Có thể cân nhắc:

```text
mileage <= 500,000 km
```

ở bước feature engineering.

### Null Mileage

Không nên coi mọi NULL mileage là lỗi.

Một phần lớn NULL mileage đến từ xe mới/xe chưa đăng ký.

ML pipeline có thể xử lý NULL như một feature/category riêng tùy model.

**Lưu ý:** các rule trên là downstream recommendations, không phải thay đổi đối với dataset chính thức của TV3.

---

# 20. Phase 6 — Seed Generation

Sau validation, TV3 chuyển dataset sang dạng database-ready seed.

Input:

```text
crawler/data/cleaned/vehicles_cleaned.json
```

Records:

```text
10,813
```

Output:

```text
crawler/data/seed/
├── vehicles_seed.json
├── vehicles_seed.csv
├── vehicles_seed_dev.json
└── vehicles_seed.sql
```

---

# 21. Seed Transformation

Seed pipeline thực hiện:

* deterministic ID generation
* source derivation
* field mapping
* NULL preservation
* SQL escaping
* batch generation
* JSON export
* CSV export
* SQL generation

Kết quả:

```text
Input:        10,813
Transformed:  10,813
Skipped:           0
Failed:            0
```

---

# 22. Seed Deliverables

| File                        | Records | Purpose                       |
| --------------------------- | ------: | ----------------------------- |
| `vehicles_seed.json`        |  10,813 | Full database-ready dataset   |
| `vehicles_seed.csv`         |  10,813 | Analytical/export format      |
| `vehicles_seed_dev.json`    |   1,000 | Development subset            |
| `vehicles_seed.sql`         |  10,813 | PostgreSQL import preparation |
| `phase6_import_report.json` |       — | Machine-readable report       |

Seed pipeline:

```text
crawler/src/pipeline/import_pipeline.py
```

CLI wrapper:

```text
crawler/scripts/seed_database.py
```

---

# 23. Database Handoff Boundary

Tại thời điểm hoàn thành Phase 6, repository chưa có database schema thực tế để TV3 import trực tiếp.

TV3 đã kiểm tra:

```text
database/schema/
database/migrations/
database/seed/
backend/
```

Các thư mục database/migration hiện chưa chứa schema triển khai thực tế.

Vì database thuộc trách nhiệm của thành viên phụ trách Database, TV3 **không tự ý tạo competing database architecture**.

Do đó:

```text
TV3 responsibility
        │
        ▼
Validated Dataset
        │
        ▼
Seed Generation
        │
        ▼
Database-ready Data
        │
        ▼
HANDOFF
        │
        ▼
Database Owner / TV5
```

Physical database import được thực hiện sau khi database owner cung cấp schema/migration và môi trường PostgreSQL tương ứng.

---

# 24. Database Import Readiness

TV3 đã chuẩn bị:

```text
import_pipeline.py
seed_database.py
vehicles_seed.sql
vehicles_seed.json
vehicles_seed.csv
```

Pipeline hỗ trợ:

* batch insert
* transaction handling
* NULL preservation
* source lineage
* source_url uniqueness
* idempotent loading strategy
* PostgreSQL-compatible SQL generation

Tuy nhiên:

```text
Physical INSERT:
PENDING DATABASE SCHEMA DEPLOYMENT
```

TV3 không báo cáo số dòng database đã insert khi chưa có database thực tế.

---

# 25. Immutability Verification

Raw merged dataset:

```text
SHA-256:
6353550dc7f7f8ce20797ddfab9ac9f8b7b4d2452f14f28363aa8ef377db1fcd
```

Cleaned dataset:

```text
SHA-256:
87be41066ff5331e7aae954e4424144dcc3675f809fd435cb9779e950c1fb2aa
```

Cả hai checksum được xác nhận không thay đổi trong quá trình Phase 6.

Kết quả:

```text
Raw dataset:      IMMUTABLE
Clean dataset:    IMMUTABLE
```

---

# 26. Git Safety

TV3 chỉ thay đổi các thành phần thuộc Data Engineering.

Không thay đổi:

```text
backend/
frontend/
```

Database architecture cũng không bị tự ý thay đổi.

`.gitignore` được bổ sung để tránh commit generated runtime datasets:

```text
crawler/data/cleaned/
crawler/data/quality_report/
crawler/data/seed/
```

Các dataset production dung lượng lớn không nên được commit trực tiếp vào Git history nếu repository policy không yêu cầu.

---

# 27. Main Deliverables

Các thành phần chính của TV3:

```text
crawler/
├── src/
│   ├── crawlers/
│   │   ├── chotot/
│   │   └── bonbanh/
│   │
│   ├── cleaning/
│   │   ├── clean_price.py
│   │   ├── clean_mileage.py
│   │   ├── clean_vehicle.py
│   │   └── validator.py
│   │
│   └── pipeline/
│       ├── clean_pipeline.py
│       ├── merge_pipeline.py
│       └── import_pipeline.py
│
├── scripts/
│   └── seed_database.py
│
└── requirements.txt
```

Documentation:

```text
docs/Members/report/
└── TV3_Data_Engineering_Report.md
```

Runtime/generated artifacts:

```text
crawler/data/raw/
crawler/data/merged/
crawler/data/cleaned/
crawler/data/quality_report/
crawler/data/seed/
```

---

# 28. Overall Pipeline Result

| Stage                       | Result           |
| --------------------------- | ---------------- |
| Workflow Audit              | ✅ COMPLETE       |
| Chợ Tốt Crawler             | ✅ COMPLETE       |
| Bonbanh Crawler             | ✅ COMPLETE       |
| Production Crawl            | ✅ COMPLETE       |
| Dataset Expansion           | ✅ COMPLETE       |
| Merge                       | ✅ COMPLETE       |
| Cleaning                    | ✅ COMPLETE       |
| Validation                  | ✅ COMPLETE       |
| Seed Generation             | ✅ COMPLETE       |
| Database Import Preparation | ✅ COMPLETE       |
| Physical Database Import    | ⏳ Database Owner |
| Real-time Pipeline          | ❌ Not in scope   |

Final dataset:

```text
10,813 real records
```

Data quality:

```text
98.41 / 100
Grade A
PASS WITH WARNINGS
```

---

# 29. Final TV3 Status

```text
================================================================
                 TV3 DATA ENGINEERING STATUS
================================================================

Data Crawling                 COMPLETE
Raw Data Collection           COMPLETE
Production Dataset            COMPLETE
Dataset Merge                 COMPLETE
Data Cleaning                 COMPLETE
Data Validation               COMPLETE
Quality Assessment            COMPLETE
Seed Generation               COMPLETE
Import Preparation            COMPLETE

Final Records                 10,813
Data Quality                  98.41 / 100
Grade                         A
Validation Status             PASS WITH WARNINGS

Database Schema               OWNED BY DATABASE MEMBER
Physical DB Import            PENDING DATABASE DEPLOYMENT

Raw Dataset                   IMMUTABLE
Clean Dataset                 IMMUTABLE

Backend Modified              NO
Frontend Modified             NO
Database Architecture         NOT MODIFIED

TV3 FINAL STATUS:
COMPLETE — READY FOR DATABASE HANDOFF
================================================================
```

# 30. Conclusion

TV3 đã hoàn thành toàn bộ phần Data Engineering được phân công.

Pipeline đã đi qua đầy đủ các bước:

```text
Crawl
  ↓
Raw
  ↓
Merge
  ↓
Clean
  ↓
Validate
  ↓
Seed
  ↓
Database Handoff
```

Dataset cuối cùng gồm **10,813 records thực tế** từ Chợ Tốt và Bonbanh.

Dữ liệu đạt:

* 100% schema compliance
* 100% critical-field completeness
* 100% source traceability
* 0 exact duplicate records
* 0 type errors
* 98.41/100 overall quality score

Các anomaly còn tồn tại được ghi nhận minh bạch và không bị xóa hoặc sửa giả tạo.

TV3 dừng tại **Database Handoff** vì database schema và physical database provisioning thuộc thành viên phụ trách Database. Đây là boundary của trách nhiệm TV3 và giúp tránh việc tự ý thay đổi kiến trúc database của nhóm.

**Final conclusion:**

> **TV3 — Data Engineering & Data Pipeline: COMPLETE.**
> **Dataset: 10,813 real records.**
> **Quality: 98.41/100 — Grade A.**
> **Seed: READY.**
> **Next owner: Database member / TV5 for schema deployment and physical import.**
