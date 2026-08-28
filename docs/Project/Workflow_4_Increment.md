# PROJECT WORKFLOW — SMART USED-CAR DECISION SUPPORT SYSTEM

## 1. Mục đích tài liệu

Tài liệu này mô tả **workflow tổng quát của toàn bộ đồ án** nhằm giúp các thành viên:

- Hiểu vị trí của mình trong toàn bộ hệ thống.
- Biết công việc bắt đầu ở giai đoạn nào.
- Biết công việc phụ thuộc vào đầu ra của thành viên nào.
- Biết đầu ra của mình được sử dụng ở đâu.
- Tránh tình trạng mỗi thành viên làm việc độc lập nhưng không khớp với workflow chung.
- Bám đúng 4 giai đoạn phát triển Incremental của dự án.

---

# 2. Tổng quan nhân sự và vai trò

```text
PROJECT
│
├── FRONTEND
│   └── Member 02
│       └── ReactJS
│
├── BACKEND
│   └── Member 01
│       └── Spring Boot Core Backend
│
└── DATA / AI
    │
    ├── Member 03
    │   └── Python Crawler
    │       ├── Crawling
    │       ├── Cleaning
    │       ├── Validation
    │       └── Seed / Import
    │
    └── Member 04
        └── R / Machine Learning
            ├── Regression Model
            ├── Preprocessing
            ├── Model Evaluation
            └── R Plumber API
```

## PostgreSQL và các chức năng tích hợp

```text
Member 03 ─────┐
               │
               ▼
        PostgreSQL Database
               │
               ▼
           Member 05
               │
               ├── Recommendation
               ├── Comparison
               └── Testing
```

---

# 3. Workflow tổng quát của dự án

```text
┌─────────────────────────────────────────────────────────────────────┐
│                            PROJECT                                  │
│         Smart Used-Car Decision Support System                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌────────────────────────────┐
              │ INCREMENT 1 – FOUNDATION   │
              └────────────────────────────┘
                              │
      ┌───────────────────────┼────────────────────────┐
      │                       │                        │
      ▼                       ▼                        ▼
  Member 01               Member 02                Team / Member 05
  BACKEND                 FRONTEND                 SYSTEM DESIGN
      │                       │                        │
      ├── Spring Boot         ├── React Setup         ├── ERD
      ├── Entity              ├── Pages               ├── API Structure
      ├── Repository          ├── Components          ├── UML
      ├── Basic CRUD          └── Basic UI            └── Documentation
      │                       │
      └───────────────┬───────┘
                      ▼
              BASIC RUNNABLE SYSTEM
                      │
                      ▼
              ┌────────────────────────────┐
              │ INCREMENT 2 – MARKET DATA  │
              └────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
             Member 03                 Member 01
          DATA PIPELINE                 BACKEND
                 │                         │
          ┌──────┴──────┐                  │
          │             │                  │
          ▼             ▼                  ▼
       Crawler       Cleaning          Search / Filter
          │             │                  │
          └──────┬──────┘                  │
                 ▼                         │
             Validation                    │
                 │                         │
                 ▼                         │
          Seed / Batch Import ─────────────┘
                 │
                 ▼
           PostgreSQL Database
                 │
                 ▼
           Member 02 Frontend
                 │
                 ▼
        Vehicle List / Filter / Detail
                 │
                 ▼
              MARKET DATA SYSTEM
                 │
                 ▼
       ┌───────────────────────────────────┐
       │ INCREMENT 3 – AUTOMATED PRICING   │
       └───────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
        Member 04          Member 01        Member 02
        R / ML             BACKEND          FRONTEND
            │                 │                 │
            ├── Model         ├── R Client     ├── Valuation Form
            ├── Train         ├── Gateway      ├── Result UI
            ├── Evaluate      ├── Batch        └── Smart Tags
            ├── Versioning    │   Prediction
            └── Plumber API   └── Smart Tagging
            │                 │
            └────────┬────────┘
                     ▼
                 HTTP/JSON
                     │
                     ▼
                R Plumber API
                     │
                     ▼
              Regression Model
                     │
                     ▼
              Predicted Price
                     │
                     ▼
               Spring Boot
                     │
                     ▼
               PostgreSQL
                     │
                     ▼
                 ReactJS
                     │
                     ▼
              AUTOMATED PRICING
                     │
                     ▼
    ┌─────────────────────────────────────────────┐
    │ INCREMENT 4 – DECISION SUPPORT              │
    │ Recommendation + Comparison + Testing       │
    └─────────────────────────────────────────────┘
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
              Member 05               All Members
                  │                       │
                  ├── Recommendation      ├── Integration
                  ├── Comparison          ├── System Test
                  ├── Ranking             ├── Performance
                  ├── Test Planning       └── Bug Fixing
                  └── Test Cases
                  │
                  ▼
         Recommendation / Compare APIs
                  │
                  ▼
               Member 01
               Spring Boot
                  │
                  ▼
               Member 02
               React UI
                  │
                  ▼
          FINAL DECISION SUPPORT SYSTEM
```

---

# 4. Kiến trúc kỹ thuật và workflow nhân sự

```text
                         ┌──────────────────────┐
                         │      MEMBER 02       │
                         │      FRONTEND        │
                         │       ReactJS        │
                         └──────────┬───────────┘
                                    │
                                HTTP/JSON
                                    │
                                    ▼
              ┌─────────────────────────────────────────┐
              │                MEMBER 01                │
              │            SPRING BOOT API              │
              │                                         │
              │ Search / Filter                         │
              │ Vehicle Management                      │
              │ Comparison                              │
              │ Recommendation                          │
              │ Smart Tagging                           │
              │ Valuation Gateway                       │
              └───────────────┬───────────────┬─────────┘
                              │               │
                            SQL│               │HTTP
                              ▼               ▼
                    ┌───────────────┐   ┌───────────────┐
                    │   MEMBER 05   │   │   MEMBER 04   │
                    │  PostgreSQL   │   │   R Plumber   │
                    │   Database    │   │   Model API   │
                    └───────▲───────┘   └───────────────┘
                            │                    │
                            │ Batch Ingestion    │ Prediction
                            │                    │
                    ┌───────┴──────────┐         │
                    │    MEMBER 03      │        │
                    │ Python Data       │        │
                    │ Pipeline          │        │
                    │                   │        │
                    │ Crawler           │        │
                    │ Cleaning          │        │
                    │ Validation        │        │
                    │ Seed / Import     │        │
                    └───────────────────┘        │
                                                 │
                  ┌──────────────────────────────┘
                  ▼
           Predicted Price + Model Version
                  │
                  ▼
             PostgreSQL
                  │
                  ▼
             Smart Tagging
                  │
                  ▼
         Recommendation / Comparison
                  │
                  ▼
             React Frontend
```

---

# 5. Workflow theo 4 Increment

---

## INCREMENT 1 — FOUNDATION

### Mục tiêu

Tạo nền móng kỹ thuật để toàn bộ hệ thống có thể bắt đầu phát triển.

### Member 01 — Backend

**Nhiệm vụ**

- Khởi tạo Spring Boot.
- Thiết kế package structure.
- Cấu hình Database Connection.
- Xây dựng Entity cơ bản.
- Xây dựng Repository.
- Xây dựng Service.
- Xây dựng Controller.
- CRUD cơ bản.

**Đầu ra**

```text
backend/
├── config/
├── controller/
├── service/
├── repository/
├── entity/
├── dto/
├── mapper/
├── exception/
└── resources/
```

**Bàn giao cho**

- Member 02 sử dụng API.
- Member 03 hiểu Database Schema để import dữ liệu.
- Member 04 hiểu schema feature đầu vào cho Model.
- Member 05 chuẩn bị Recommendation/Comparison dựa trên dữ liệu hệ thống.

---

### Member 02 — Frontend

**Nhiệm vụ**

- Khởi tạo ReactJS.
- Xây dựng layout chung.
- Navbar.
- Footer.
- Loading.
- Error handling.
- Trang danh sách xe cơ bản.
- Trang chi tiết xe cơ bản.

**Đầu ra**

```text
frontend/
├── components/
├── pages/
├── services/
├── hooks/
├── context/
├── utils/
└── styles/
```

**Phụ thuộc**

```text
Member 01 API
```

**Bàn giao**

```text
Basic React UI
```

---

### Member 03 — Data Pipeline

**Nhiệm vụ trong Increment 1**

- Chuẩn bị cấu trúc crawler.
- Xác định nguồn dữ liệu.
- Xác định Raw Data Schema.
- Xác định Clean Data Schema.
- Chuẩn bị Seed Dataset mẫu.

**Đầu ra**

```text
crawler/
├── crawlers/
├── cleaning/
├── pipeline/
├── config/
└── data/
```

---

### Member 04 — R/ML

**Nhiệm vụ trong Increment 1**

- Kiểm tra mô hình Regression hiện có.
- Xác định feature đầu vào.
- Xác định preprocessing cần thiết.
- Xác định output.
- Chuẩn bị cấu trúc Model Service.

**Đầu ra**

```text
model/
├── regression/
└── plumber/
```

---

### Member 05 — Database / System Design

**Nhiệm vụ**

- Hoàn thiện ERD.
- Data Dictionary.
- Database Schema.
- Chuẩn bị Use Case.
- Chuẩn bị Class Diagram.
- Chuẩn bị API Specification ban đầu.
- Chuẩn bị Test Plan khung.

**Đầu ra**

```text
database/
docs/UML/
docs/Database/
docs/API/
docs/Testing/
```

---

# INCREMENT 2 — MARKET DATA

## Mục tiêu

Đưa dữ liệu thị trường thực tế vào hệ thống và hoàn thiện chức năng tìm kiếm/lọc.

### Member 03 — Trọng tâm chính

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

**Trách nhiệm**

- Crawling theo Batch.
- Parser dữ liệu.
- Clean Price.
- Clean Mileage.
- Clean Vehicle Information.
- Validation.
- Duplicate Detection.
- Seed Dataset.
- Import Database.

**Đầu ra bàn giao**

```text
Cleaned Dataset
+
Seed Dataset
+
Import Pipeline
```

---

### Member 01 — Backend

**Trách nhiệm**

- Search API.
- Filter API.
- Pagination.
- Sorting.
- Vehicle Detail API.
- Listing API.

---

### Member 02 — Frontend

**Trách nhiệm**

- Vehicle List.
- Vehicle Card.
- Filter Panel.
- Price Filter.
- Year Filter.
- Mileage Filter.
- Vehicle Detail Page.

---

### Member 05 — Database / Testing

**Trách nhiệm**

- Kiểm tra dữ liệu sau Import.
- Kiểm tra Database Integrity.
- API Test Search.
- API Test Filter.
- Chuẩn bị Performance Test cơ bản.

---

# INCREMENT 3 — AUTOMATED PRICING

## Mục tiêu

Tích hợp mô hình Regression vào hệ thống để định giá xe tự động.

### Member 04 — Trọng tâm chính

```text
Train Dataset
      │
      ▼
Preprocessing
      │
      ▼
Train Regression
      │
      ▼
Evaluate Model
      │
      ▼
Model Version
      │
      ▼
regression_v1.rds
      │
      ▼
R Plumber API
      │
      ▼
POST /predict
```

**Đầu ra bàn giao**

```text
Model File
+
Prediction API
+
Model Version
+
Evaluation Metrics
```

---

### Member 01 — Backend Integration

**Trách nhiệm**

- RModelClient.
- Valuation Gateway.
- ValuationService.
- Error Handling từ R API.
- Prediction Persistence.
- Batch Prediction.
- Smart Tagging.

---

### Member 02 — Frontend

**Trách nhiệm**

- ValuationPage.
- ValuationForm.
- ValuationResult.
- Hiển thị:
  - Predicted Price.
  - Difference Percent.
  - Price Label.

---

### Member 05 — Testing

**Trách nhiệm**

- Integration Test:

```text
Spring Boot
      ↔
R Plumber
```

- Test Input Validation.
- Test Error Handling.
- Test Prediction Response.

---

# INCREMENT 4 — RECOMMENDATION & DECISION SUPPORT

## Mục tiêu

Hoàn thiện hệ thống theo định hướng Decision Support System.

### Member 05 — Trọng tâm chính

#### Recommendation

```text
Candidate Vehicles
       │
       ▼
Price Score
       │
       ├── ODO Score
       │
       ├── Age Score
       │
       ├── Preference Score
       │
       └── Market Fairness Score
                 │
                 ▼
        Recommendation Score
                 │
                 ▼
              Ranking
                 │
                 ▼
       Top Recommended Cars
```

#### Comparison

```text
Selected Cars
     │
     ▼
Vehicle Data
     │
     ├── Price
     ├── Predicted Price
     ├── Difference
     ├── Year
     ├── ODO
     ├── Fuel
     ├── Transmission
     └── Recommendation Score
     │
     ▼
Comparison Result
```

#### Testing

- Integration Test.
- API Test.
- System Test.
- Performance Test.
- Test Report.

---

### Member 01 — Backend Support

- Recommendation API.
- Comparison API.
- Business Logic Integration.
- Database Integration.

---

### Member 02 — Frontend Support

- RecommendationPage.
- RecommendationCard.
- RecommendationList.
- ComparePage.
- CompareTable.
- CompareChart.

---

### Member 03 — Data Support

- Kiểm tra chất lượng dữ liệu.
- Hỗ trợ bổ sung Seed Dataset.
- Data Validation.
- Fix dữ liệu lỗi ảnh hưởng đến Recommendation.

---

### Member 04 — Model Support

- Hỗ trợ kiểm tra Prediction.
- Kiểm tra model_version.
- Đánh giá các prediction bất thường.

---

# 6. Workflow phụ thuộc giữa các thành viên

```text
Member 03
DATA PIPELINE
      │
      │ Cleaned / Seed Data
      ▼
Member 05
POSTGRESQL
      │
      │ System Data
      ├───────────────────────────┐
      ▼                           ▼
Member 01                     Member 04
BACKEND                       R MODEL
      │                           │
      │ API / Features            │ Prediction API
      │                           │
      └─────────────┬─────────────┘
                    ▼
             Valuation Result
                    │
                    ▼
                Member 02
                FRONTEND
                    │
                    ▼
                User UI
                    │
                    ▼
          User Preferences / Actions
                    │
                    ▼
                Member 05
       Recommendation + Comparison
                    │
                    ▼
                Member 02
                Result UI
```

---

# 7. Ma trận trách nhiệm tổng quát

| Thành viên | Vai trò chính | Increment 1 | Increment 2 | Increment 3 | Increment 4 |
|---|---|---|---|---|---|
| Member 01 | Backend | Foundation | Search / Filter | Pricing Integration | API Integration |
| Member 02 | Frontend | Basic UI | Vehicle Feed | Valuation UI | Recommendation / Compare UI |
| Member 03 | Data Pipeline | Data Structure | Crawler / Cleaning / Import | Data Support | Data Quality Support |
| Member 04 | R / ML | Model Analysis | Model Preparation | Regression + Plumber | Model Support |
| Member 05 | Database / Decision Support / Testing | DB + Design | Data / API Testing | Integration Testing | Recommendation + Comparison + Testing |

---


# 8. Workflow cuối cùng của toàn hệ thống

```text
                    MARKET DATA SOURCES
                           │
                           ▼
                 MEMBER 03 — CRAWLER
                           │
                           ▼
                    RAW DATASET
                           │
                           ▼
              CLEANING + VALIDATION
                           │
                           ▼
                   SEED / BATCH DATA
                           │
                           ▼
                MEMBER 05 — POSTGRESQL
                           │
                           ▼
              ┌─────────────────────┐
              │ SYSTEM OF RECORD    │
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     MEMBER 01       MEMBER 04       MEMBER 05
      BACKEND         R / MODEL      DECISION SUPPORT
          │              │              │
          │              │              ├── Recommendation
          │              │              └── Comparison
          │              │
          │              ▼
          │          R PLUMBER
          │              │
          │              ▼
          │        PREDICTED PRICE
          │              │
          └──────────────┘
                 │
                 ▼
            SMART TAGGING
                 │
                 ▼
        RECOMMENDATION / RANKING
                 │
                 ▼
           MEMBER 02 — REACTJS
                 │
                 ├── Search
                 ├── Filter
                 ├── Vehicle Detail
                 ├── Valuation
                 ├── Recommendation
                 └── Comparison
                 │
                 ▼
                USER
```

---
