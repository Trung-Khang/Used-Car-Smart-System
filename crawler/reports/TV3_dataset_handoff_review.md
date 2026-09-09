# Báo cáo rà soát dataset và bàn giao TV3

**Dataset được kiểm tra:** `crawler/data/cleaned/vehicles_cleaned.csv` và `vehicles_cleaned.json`  
**Thời điểm rà soát:** 09/09/2026  
**Phạm vi:** khả năng dùng dataset cho TV1, TV2, TV4 và TV5; không chỉnh sửa hay suy diễn dữ liệu nguồn.

## Kết luận

Dataset hiện có **10.813 listing thực tế**, vượt mục tiêu 2.000-5.000 record. CSV và JSON cùng có 17 trường, cùng 10.813 dòng, cùng thứ tự trường và cùng record đầu tiên. File CSV là UTF-8 with BOM, nên đọc tiếng Việt được trong PowerShell, Excel và R khi dùng encoding UTF-8.

**Đạt để bắt đầu Increment 2:** TV1/TV2/TV5 có thể dùng dataset để import, hiển thị, tìm kiếm, lọc, so sánh và kiểm thử database.  
**Chưa đạt để huấn luyện chính thức `regression_v1`:** model hiện tại yêu cầu đủ `price`, `manufacture_year`, `listed_year`, `mileage`, `fuel_type`, `transmission`, `origin`, `engine_size`, `seat_count`. `listed_year` có thể suy ra từ `crawled_at`, nhưng chỉ còn **710/10.813 dòng (6,57%)** hợp lệ sau khi áp đầy đủ các feature và range của model. Không nên dùng 710 dòng này làm tập train chính thức vì quá nhỏ và dễ lệch theo nguồn, dòng xe, xuất xứ.

## 1. Schema hiện có

| Trường | Kiểu/kỳ vọng | Đầy đủ | Đánh giá sử dụng |
|---|---|---:|---|
| `brand`, `model` | text | 100% | Đạt cho hiển thị, tìm kiếm, database và model tương lai |
| `variant` | text | 86,38% | Dùng để hiển thị; không phải blocker |
| `manufacture_year` | integer | 100% | Đạt |
| `price` | integer, VND | 100% | Đạt, cần lọc outlier ở downstream |
| `mileage` | integer, km | 78,66% | Dùng được cho web; thiếu nhiều cho regression |
| `fuel_type` | categorical | 99,99% | Đạt sau chuẩn hóa |
| `transmission` | categorical | 99,80% | Đạt sau chuẩn hóa |
| `body_type` | categorical | 90,19% | Đạt cho filter/UI, cần quy về danh mục chung |
| `location` | text | 100% | Đạt cho hiển thị/lọc địa điểm |
| `origin` | `Domestic`/`Imported` | 14,69% | Chưa đủ cho feature bắt buộc của `regression_v1` |
| `engine_size` | number, L | 55,11% | Chưa đủ nếu model bắt buộc đủ feature |
| `seat_count` | integer | 12,37% | Chưa đủ nghiêm trọng cho `regression_v1` |
| `source_url` | URL tuyệt đối, unique | 100% | Đạt truy vết nguồn/dedup |
| `image_url` | URL ảnh | 100% | Đạt cho UI |
| `listed_at` | ngày công bố hoặc text tương đối | 99,99% | Đạt truy vết, chưa phù hợp làm ngày chuẩn hóa |
| `crawled_at` | ISO-8601 datetime | 100% | Đạt; dùng làm thời điểm quan sát listing |

Nguồn dữ liệu gồm 7.697 listing từ `bonbanh.com` và 3.116 listing từ `xe.chotot.com`. Không có URL trùng hoàn toàn.

## 2. Đánh giá theo thành viên

### TV1 - Backend và tích hợp

**Có thể bắt đầu ngay:** map `brand`, `model`, `variant`, `manufacture_year`, `body_type`, `fuel_type`, `transmission` vào Vehicle; map `price`, `mileage`, `location`, `source_url`, `image_url`, `listed_at`, `crawled_at` vào Listing.

**TV3 cần phối hợp xác nhận:** `origin`, `engine_size`, `seat_count` phải được giữ trong seed/import khi database đã có cột tương ứng. Hiện `crawler/src/pipeline/import_pipeline.py` chỉ liệt kê schema 14 trường, vì vậy seed được tạo lại có nguy cơ làm mất 3 trường enrich này.

**Cần chờ TV5:** TV5 chốt migration/schema thực tế và mapping Vehicle/Listing. Sau đó TV1 chạy import thử và xác nhận số dòng import, null mapping, URL unique và filter/sort/pagination.

### TV2 - Frontend

**Có thể bắt đầu ngay:** đủ dữ liệu cho card/detail và các filter theo hãng-model, giá, năm, ODO, nhiên liệu, hộp số, kiểu dáng và địa điểm. `image_url` đầy đủ cho danh sách xe.

**Lưu ý:** `body_type` đang có các giá trị gần nghĩa như `SUV`, `SUV / Crossover`, `Crossover`, `Van`, `Van / Minivan`. TV3 cần chốt một vocabulary hiển thị/lọc chung với TV1/TV2, hoặc backend phải map các nhóm tương đương. Không để frontend tự xử lý toàn bộ biến thể danh mục.

### TV4 - Regression/R Plumber

**Feature có sẵn:** `price`, `manufacture_year`, `mileage`, `fuel_type`, `transmission`, `origin`, `engine_size`, `seat_count`, `crawled_at`.

**Quy ước thời gian:** không cần thêm cột `listed_year` vào dataset. TV4 sẽ tạo `listed_year = year(crawled_at)` tại preprocessing và phải gọi rõ nó là *năm quan sát/crawl*, không phải ngày người bán đăng tin. `listed_at` hiện là dữ liệu hỗn hợp: có ngày ISO và có các chuỗi như `3 ngày trước`, nên chưa dùng làm biến thời gian chuẩn hóa.

**Blocker hiện tại:** tỷ lệ thiếu của `origin` 85,31%, `engine_size` 44,89%, `seat_count` 87,63%, cộng thêm `mileage` thiếu 21,34%. Áp các yêu cầu và range hiện hành của `model/regression/src/preprocessing.R` chỉ còn 710 dòng hợp lệ. Tập này gồm 381 xe Imported, 329 xe Domestic; 566 Gasoline, 126 Diesel, 18 Hybrid và không có Electric. Nó không đại diện đủ thị trường để công bố metrics/model chính thức.

**Khuyến nghị cho TV4:** chưa train/chốt `regression_v1` bằng complete-case này. TV4 sẽ nhận data để phân tích EDA và cùng TV3 chốt hướng: (1) TV3 enrich thêm feature, hoặc (2) TV4 thiết kế model version khác cho phép imputation/missing indicator và cập nhật feature contract trước khi train. Không được tự tạo dữ liệu giả để lấp null.

### TV5 - Database, recommendation và testing

**Có thể bắt đầu ngay:** dataset đáp ứng price, year, mileage, fuel, transmission, source URL và timestamp để thiết kế seed, search performance, comparison cơ bản và test constraint.

**Cần chờ TV1/TV4:** `predicted_price`, `model_version`, `predicted_at`, `difference_percent`, `price_label` chỉ có sau khi TV4 train model chính thức và TV1 tích hợp R API. Recommendation không cần TV3 cào thêm dữ liệu preference của user; preference là input UI/API, không phải thuộc tính listing.

## 3. Các vấn đề cần TV3 xử lý

### P0 - Đồng bộ code pipeline với schema 17 trường

Các file dưới đây vẫn khai báo canonical schema 14 trường, trong khi dataset cuối là 17 trường:

- `crawler/src/cleaning/validator.py`
- `crawler/src/pipeline/clean_pipeline.py`
- `crawler/src/pipeline/merge_pipeline.py`
- `crawler/src/pipeline/import_pipeline.py`

TV3 cần thêm đúng ba trường `origin`, `engine_size`, `seat_count` vào field list, expected type, validation, transform record và seed fields. CSV seed cần xuất UTF-8 with BOM tương tự cleaned CSV.

**Xác nhận hoàn thành P0:** chạy lại pipeline hoặc test tối thiểu; validator chấp nhận record 17 trường; seed JSON/CSV/SQL có đủ 17 trường cộng các field kỹ thuật của seed; so sánh số record và null count của ba trường trước/sau không đổi.

### P1 - Tăng coverage feature cho model

TV3 không được suy đoán `origin`, `engine_size`, `seat_count`. Tuy nhiên, nếu có thể crawl/enrich tiếp từ trang detail hợp lệ hoặc bổ sung nguồn có các thông số này, ưu tiên theo thứ tự:

1. `seat_count`: hiện chỉ có 1.338 record. Đây là nút thắt lớn nhất của model hiện tại.
2. `origin`: hiện chỉ có 1.588 record. Cần lấy trực tiếp từ thông số xuất xứ, không suy từ hãng.
3. `engine_size`: hiện có 5.959 record. Tiếp tục lấy từ dung tích L hoặc cc rồi chuẩn hóa về L.
4. `mileage`: chỉ nhận khi nguồn công bố rõ; giữ null nếu xe mới hoặc thiếu ODO.

Do nhiều listing detail đã 403/404/410, việc enrich lại không phải blocker cho web/database. TV3 chỉ cần ghi log nguồn, URL, thời điểm, status và số record thành công; không dùng giá trị từ bên thứ ba không truy vết được để bổ sung vào record gốc.

**Mục tiêu bàn giao lại cho model:** chưa áp đặt một tỷ lệ đủ cứng khi nguồn không công bố specs. Thay vào đó, TV3 cần báo số dòng đủ toàn bộ feature sau mỗi lượt enrich. Nếu vẫn thấp, TV4 sẽ thay đổi model contract thay vì TV3 tạo dữ liệu giả.

### P1 - Chuẩn hóa danh mục và semantic timestamp

- Chốt enum `body_type` cho Backend/UI. Ví dụ có thể gom `SUV`, `SUV / Crossover`, `Crossover` thành một nhãn filter; nhưng phải ghi rõ mapping và giữ raw/canonical nhất quán.
- Giữ `listed_at` là nullable text nếu nguồn chỉ trả relative time. Không tự đổi `3 ngày trước` thành ngày tuyệt đối nếu thiếu mốc thời gian đáng tin cậy.
- Duy trì `crawled_at` ISO-8601 có timezone. Đây là timestamp chuẩn để audit và suy diễn năm quan sát.
- Chuẩn hóa `fuel_type` chỉ còn `Gasoline`, `Diesel`, `Hybrid`, `Electric` hoặc null; `transmission` chỉ còn `Automatic`, `Manual`, `CVT` hoặc null. Điều này khớp contract TV4 hiện tại.

### P2 - Metadata thuận tiện cho database (không phải feature model)

Sau khi TV5 chốt schema, TV3/TV1 nên có mapping hoặc field kỹ thuật sau trong seed/import:

| Field | Cách có | Mục đích |
|---|---|---|
| `source` | derive từ domain URL | bảng nguồn và truy vết |
| `source_listing_id` | parse ổn định từ URL nếu nguồn hỗ trợ | idempotent import/dedup |
| `crawl_batch_id` hoặc manifest batch | pipeline tạo | audit một lượt crawl/import |
| `dataset_version` / SHA-256 | pipeline tạo | truy vết bản dữ liệu train/seed |

Các field này không cần crawler lấy lại; không đưa chúng vào payload dự đoán.

## 4. Anomaly và rule downstream

Dataset giữ lại dữ liệu gốc là đúng, nhưng downstream phải xử lý rõ:

| Kiểm tra | Kết quả | Hành động |
|---|---:|---|
| Giá dưới 50 triệu VND | 68 | TV4 loại/đánh cờ khi train do có thể là giá trả trước/trả góp |
| Giá trên 15 tỷ VND | 5 | TV4 quyết định giữ hoặc đánh cờ theo phạm vi model; không sửa dữ liệu gốc |
| ODO trên 1.000.000 km | 8 | TV4 loại/đánh cờ trong preprocessing |
| Năm sản xuất trước 1990 | 11 | TV4 loại theo range `regression_v1` hiện tại hoặc tách model khác |
| `listed_at` relative text | 3.115 dòng | Không parse thành ngày giả; chỉ dùng `crawled_at` cho audit/năm quan sát |

## 5. Trình tự phối hợp và xác nhận bàn giao

1. **TV3** sửa P0, chạy validator/seed, push code cùng báo cáo field completeness mới.
2. **TV5** chốt migration schema và thông báo mapping Vehicle/Listing/Source/CrawlBatch cho TV1, TV3.
3. **TV1** import seed vào PostgreSQL, xác nhận tổng số dòng, URL unique, null mapping và API filter/sort/pagination.
4. **TV2** gọi API của TV1, kiểm tra card, detail, ảnh, filter và empty state với các giá trị null.
5. **TV4** nhận đúng bản cleaned/seed đã có version/checksum, chạy EDA và số dòng eligible. Chỉ train official model sau khi feature contract được TV1/TV3/TV4 cùng chấp nhận.
6. **TV5** chạy integration test Backend-Database; chỉ bật smart tag/recommendation khi TV1 nhận prediction hợp lệ từ TV4.

Một bàn giao được xem là xác nhận khi có: commit/hash dataset, data dictionary 17 trường, kết quả validator, số record import thành công, mapping database đã ký hiệu rõ, và test API hiển thị/filter được một record có null optional field.

## 6. Trạng thái cuối của đợt rà soát

| Hạng mục | Trạng thái |
|---|---|
| Dataset cho web/search/database foundation | PASS WITH WARNINGS |
| Truy vết URL, encoding, record count | PASS |
| Schema dataset 17 trường | PASS |
| Code pipeline/seed đồng bộ 17 trường | BLOCKED - TV3 cần cập nhật P0 |
| Train official `regression_v1` complete-case | NOT READY - chỉ 710 dòng eligible |
| EDA/model redesign của TV4 trên dataset thật | READY |
| Physical PostgreSQL import | PENDING TV5 schema và TV1 integration |

**Kết luận:** TV3 đã cung cấp một dataset thật, đủ lớn và rất hữu ích cho các Increment về market data. Việc cần làm ngay không phải cào dữ liệu giả, mà là bảo toàn schema 17 trường xuyên suốt pipeline/seed và tiếp tục enrich có chứng cứ nếu nguồn cho phép. TV4 sẽ không công bố model/metrics chính thức cho đến khi model contract xử lý được tỷ lệ missing một cách hợp lệ.
