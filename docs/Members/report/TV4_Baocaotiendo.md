# TV4 - Bao cao tien do

## Increment 1 - Regression Foundation

Trang thai: da hoan thanh khung nen tang, dang cho du lieu cleaned tu TV3 de train model chinh thuc.

### Da thuc hien

- Tao cau truc `model/regression/` gom `data/`, `src/`, `models/`, `reports/`.
- Xay dung `model/regression/src/preprocessing.R` de chuan hoa feature, validate cot bat buoc, xu ly unit va feature engineering.
- Xay dung `model/regression/train_model.R` voi luong train/test split, train regression, tinh metrics va luu artifact `.rds`.
- Xay dung `model/regression/evaluate_model.R` de danh gia model tren dataset ngoai.
- Tao `model/plumber/` gom config, handler, schema va file `plumber.R`.
- Dinh nghia contract request/response trong `model/plumber/schemas/prediction_schema.json`.
- Tao fixture nho `model/regression/data/fixture_used_cars.csv` chi phuc vu smoke test pipeline.
- Ghi placeholder report/metrics de neu ro official metrics chua co vi chua nhan du lieu TV3.

### Feature contract hien tai

- `manufacture_year`: nam san xuat xe.
- `listed_year`: nam listing duoc quan sat.
- `listed_month`: thang listing duoc quan sat, optional trong `regression_v1`.
- `vehicle_age = listed_year - manufacture_year`.
- `mileage`: so km da di, don vi km.
- `mileage_k = mileage / 1000`.
- `fuel_type`: `Gasoline`, `Diesel`, `Hybrid`, `Electric`.
- `transmission`: `Automatic`, `Manual`, `CVT`.
- `origin`: `Domestic`, `Imported`.
- `engine_size`: dung tich dong co lit, xe dien dung `0`.
- `engine_non_ev = 0` voi xe dien, nguoc lai bang `engine_size`.
- `seat_count`: so cho ngoi.
- `price`: gia rao ban quan sat duoc, don vi VND, bat buoc khi train.

### Kiem tra da chay

- Da chay smoke test bang fixture: `train_model.R --smoke`.
- Ket qua smoke test tao duoc artifact fixture va metrics fixture.
- Da test truc tiep `predict_price()` voi artifact fixture va tra ve response gom `predicted_price`, `currency`, `model_version`, `preprocessing_version`, `predicted_at`.

### Han che / viec dang cho

- Chua train official `model/regression/models/regression_v1.rds` vi chua co cleaned dataset tu TV3.
- Chua co official R2/MAE/RMSE/MAPE, khong tu dat so lieu.
- May hien tai chua cai R package `plumber`, nen HTTP API chua chay local duoc cho den khi cai `plumber` va `jsonlite`.

### Ban giao cho nhom

- TV3: can cung cap cleaned dataset khop schema, dac biet cac cot nam/thoi gian va don vi gia/km.
- TV1: co the bam vao `model/plumber/schemas/prediction_schema.json` de chuan bi request den R Model API.
- TV2: co the dung schema de thiet ke form valuation sau nay.
- TV5: se nhan `predicted_price`, `model_version`, `predicted_at` de tinh smart tag khi sang Increment 3/4.


BÁO CÁO CHO TV3

Dataset TV3 hiện tại dùng được làm nền, nhưng chưa ổn để train TV4 theo model hiện tại nếu mình vẫn giữ engine_size và origin.

File có:
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


Đang thiếu so với TV4 hiện tại:
listed_year
origin
engine_size
seat_count

Trong đó:

- listed_year: không cần bắt TV3 cào thêm, vì có crawled_at rồi. TV4 có thể tự suy ra listed_year = year(crawled_at).
- origin: nên nhờ TV3 bổ sung nếu muốn giữ model giống bản cũ, ví dụ Domestic / Imported.
- engine_size: nên nhờ TV3 bổ sung nếu web có thông tin dung tích máy, ví dụ 1.5, 2.0, 2.4; xe điện có thể để 0 hoặc NA rồi TV4 xử lý.
- seat_count: cũng nên bổ sung, vì model hiện tại đang required và feature này khá có ích cho xe 5 chỗ/7 chỗ.
Ngoài thiếu cột, mình thấy vài vấn đề data quality cần nói TV3:
- Có 10813 dòng, khá ổn về số lượng.
- mileage thiếu khá nhiều, khoảng vài nghìn dòng; cần thống nhất để trống là NA hay cố crawl/bổ sung.
- Có outlier: price min 5,000,000, max 33,000,000,000; cần lọc giá quá thấp/quá cao.
- Có 68 xe giá dưới 50 triệu, 5 xe giá trên 15 tỷ.
- manufacture_year có 11 dòng trước năm 1990.
- mileage có max 3,380,000,000, chắc chắn lỗi parse.
- transmission có Semi-Automatic và Other, trong khi schema TV4 hiện chỉ có Automatic, Manual, CVT.
- fuel_type có Other 1 dòng, cần map hoặc loại.
- CSV đang có dấu tiếng Việt bị mojibake khi đọc bằng R/PowerShell; JSON ổn hơn. Nên nhờ TV3 đảm bảo CSV xuất chuẩn UTF-8.
Tin nhắn bạn có thể gửi TV3:
Dataset cleaned hiện đã có các cột lõi như brand, model, manufacture_year, price, mileage, fuel_type, transmission, body_type, location, crawled_at. 
Bên TV4 có thể tự suy ra listed_year từ crawled_at, nên không cần cào listed_year riêng.

Nhờ TV3 bổ sung thêm nếu cào được:

- origin: Domestic/Imported hoặc Trong nước/Nhập khẩu
- engine_size: dung tích động cơ, đơn vị lít; xe điện có thể để 0 hoặc NA
- seat_count: số chỗ ngồi

Ngoài ra cần kiểm tra data quality:

- mileage đang thiếu khá nhiều và có outlier rất lớn
- price có vài dòng quá thấp/quá cao
- manufacture_year có vài dòng trước 1990
- fuel_type/transmission cần chuẩn hóa category, tránh Other nếu không rõ
- CSV nên xuất UTF-8 để bên R đọc không lỗi dấu
Kết luận: dataset hiện chưa train chính thức được với TV4 hiện tại vì thiếu origin, engine_size, seat_count. Nhưng không tệ, nền crawler đã có rồi. crawled_at thay được listed_year, cái đó không cần bắt bạn TV3 bổ sung riêng.