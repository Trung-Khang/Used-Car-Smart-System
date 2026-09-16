# TV4 - Bao cao tien do

## Increment 2 - Dataset Integration va EDA

Trang thai: **EDA da hoan thanh tren local snapshot; candidate model va official training chua duoc chot.**

### Dataset da su dung

- Input truc tiep: `crawler/data/cleaned/vehicles_cleaned.csv`; khong copy hay sua dataset TV3.
- Contract: 17 cot, 10,813 dong, `source_url` unique, CSV UTF-8 with BOM.
- Local SHA-256: `5a70b532173c897531440105b47ddccfb839198d631ea0375050c57010201b27`.
- Canh bao provenance: hash tren khac hash `bcec...3513` trong TV3 Phase 1 lock report. TV3 can xac nhan local snapshot la canonical hoac cap nhat lock report truoc official training.

### Ket qua EDA

- `crawled_at` parse dung 100%; `observed_year = year(crawled_at)` va khong co vehicle age am. `listed_at` giu raw text, khong dung lam timestamp.
- Missing: mileage 2,307 (21.34%), origin 9,225 (85.31%), engine_size 4,854 (44.89%), seat_count 9,475 (87.63%). Khong coi missing mileage la 0 va khong suy dien origin/engine/seats.
- 68 gia duoi 50 trieu VND, 5 gia tren 15 ty VND, 8 mileage tren 1,000,000 km, 11 xe truoc 1990. Day la training flags, khong sua du lieu goc.
- Electric co 1,204 dong; 100% `engine_size = NULL`, khong co gia tri 0. `engine_non_ev = 0` chi la feature dan xuat trong model.
- `body_type` thuc te chua dong bo hoan toan voi document: con `SUV`, `Crossover`, `Van / Minivan`, `Truck`, `Other`, `Wagon`.

### Do phu candidate

- Complete-case legacy: 710 dong (6.57%).
- Complete-case co EV exception: 747 dong (6.91%).
- Reduced-feature baseline: 8,407 dong (77.75%).
- Missing-aware candidate input: 8,428 dong (77.94%).

Complete-case bi lech mau manh: Chotot eligible 11.42% trong khi Bonbanh 4.60%. Khong duoc dung no lam model chinh thuc chi vi no de giai thich.

### Candidate va leakage control

- A: complete-case chi de tham chieu.
- B: reduced-feature dung age, mileage, fuel, transmission; de day du form hon nhung mat origin/engine/seat.
- C: missing-aware dung median fit tren train split, missing indicators, category `Unavailable`, va xu ly EV rieng.
- Khi runtime co san, split truoc preprocessing, fit median/encoding chi tren train, test tren hold-out, ghi seed, va can nhac group split `brand + model + manufacture_year`.
- Chua co R2/MAE/RMSE/MAPE candidate hay official vi may hien tai chua co Rscript. Khong co `.rds` official.

### Bao cao / ban giao

- `model/regression/eda_dataset.R`: EDA tai lap duoc tu CSV goc.
- `model/regression/reports/data_quality_report.md`: ket qua EDA va bias/coverage.
- `model/regression/reports/candidate_strategy.md`: proposal A/B/C va leakage protocol.
- `model/regression/reports/prediction_contract_proposal.md`: de xuat form/API, chua doi Plumber official.
- `model/regression/reports/tv3_confirmation.md`: bang chung da co va 2 cau hoi thuc su cho TV3.

### Dieu kien truoc official training

1. TV3 xac nhan checksum/version local va vocabulary body type.
2. TV4 chay lai EDA/candidate evaluation bang R tren snapshot da xac nhan.
3. Nhom review missing/outlier policy, group/random split, test metrics va residual analysis.
4. TV1/TV3/TV4 chot prediction contract phu hop candidate duoc chon.

## Increment 1 - Regression Foundation

Trang thai: **Hoan thanh khung source code va contract; chua co model chinh thuc.**

TV3 da khoa Data Contract 17 truong va ban cleaned dataset 10,813 dong da co san. TV4 khong train hay cong bo `regression_v1` trong Increment 1 vi missing cua cac feature hien tai can duoc EDA va thong nhat xu ly o Increment 2.

### Da hoan thanh

- Co du cau truc `model/regression/{data,src,models,reports}` va `model/plumber/`.
- Co preprocessing, metrics, train/test split, evaluation skeleton va fixture smoke path rieng.
- Dong bo preprocessing va JSON prediction contract voi 17-field TV3 contract va Database Schema v2.0.1.
- Doi `listed_year` cu thanh `observed_year = year(crawled_at)`; khong nham lan voi nam nguoi ban dang tin.
- Xac nhan don vi: `price` VND, `mileage` km, `engine_size` lit, `seat_count` seats; `crawled_at` ISO-8601 co timezone.
- Xac nhan vocabulary `Gasoline/Diesel/Hybrid/Electric`, `Automatic/Manual/CVT`, va `Domestic/Imported`.
- Giu NULL nguon cho `origin`, `engine_size`, `seat_count`, `mileage`; EV co the NULL `engine_size`, preprocessing chi tao `engine_non_ev = 0` o feature dan xuat.
- Them bao cao audit/handoff: `model/regression/reports/increment_1_audit.md`.

### Ket qua kiem tra

- Static review: PASS cho duong dan smoke, tach biet fixture artifact/metrics voi official artifact, va Plumber waiting/error contract.
- Runtime smoke: PENDING. Moi truong audit khong co `Rscript`, nen chua chay `train_model.R --smoke` hay HTTP Plumber.
- Khong co official `.rds`, R2, RMSE, MAE, MAPE, hoac ket qua nao duoc dung cho bao cao do an.

### Tinh hinh dataset va rui ro model

- Dataset dung 17 field, 10,813 records, URL unique theo TV3 Phase 1 lock.
- Missing cao o `origin` (9,225), `engine_size` (4,854), `seat_count` (9,475), va `mileage` (2,307). Complete-case baseline cu chi con khoang 710-715 dong tuy range filter.
- Vi vay khong duoc coi complete-case regression hien tai la model chinh thuc. Khong yeu cau TV3 tao du lieu gia hoac suy dien feature chi de lam day model.

### Ban giao va phoi hop

- TV3: xac nhan dataset checksum/version cho EDA; thong bao version moi va completeness neu enrichment thay doi `origin`, `engine_size`, `seat_count`; bao toan NULL va `crawled_at` timezone-aware.
- TV1: chua goi prediction de demo. Khi Increment 2 chap nhan contract, doi `listed_year` sang `observed_year` trong request adapter/API contract.
- TV2: form valuation sau nay dung `observed_year`, khong hien thi nhu nam dang tin.
- TV5: database da bao toan cac field ML nullable; khong ep NULL thanh gia tri gia.

### Viec chuyen sang Increment 2

1. Chay EDA va ghi nhan missingness, outlier, distribution theo source/brand/model.
2. De xuat va xin review policy xu ly missing, outlier, feature selection va train/test split.
3. Sau khi duoc chap nhan, train model versioned tren dataset that, danh gia hold-out, va moi cong bo metrics/artifact.
4. Cai R/Rscript va `plumber`, `jsonlite` de chay lai fixture smoke va Plumber runtime test.
