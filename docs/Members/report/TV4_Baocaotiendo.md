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
