# Test Plan — Increment 1 Foundation

## 1. Objective
Provide the initial testing framework for the database, API contract and core
system flows. The workflow later expands this into integration, system and
performance testing.

## 2. Scope

### Database
- Schema creation
- Primary/foreign key constraints
- Required fields
- Data types
- Basic indexes

### API
- Vehicle list
- Vehicle detail
- Search/filter contract
- Comparison contract
- Basic error handling

### Integration preparation
- Spring Boot ↔ PostgreSQL
- Later: Spring Boot ↔ R Plumber

## 3. Test cases

| ID | Area | Test | Expected result | Priority |
|---|---|---|---|---|
| DB-01 | DB | Create schema | All tables created successfully | High |
| DB-02 | DB | Insert valid vehicle | Record inserted | High |
| DB-03 | DB | Insert vehicle without make/model | Insert rejected | High |
| DB-04 | DB | Duplicate comparison_vehicle pair | Duplicate rejected | Medium |
| API-01 | API | GET vehicle list | 200 + paginated JSON | High |
| API-02 | API | GET existing vehicle | 200 + vehicle JSON | High |
| API-03 | API | GET missing vehicle | 404 | High |
| API-04 | API | Search/filter valid values | Correct filtered result | High |
| API-05 | API | Invalid filter input | 400 or agreed validation response | Medium |
| CMP-01 | Comparison | Create comparison with valid IDs | Comparison created | High |
| CMP-02 | Comparison | Compare nonexistent vehicle | Validation/error response | High |
| INT-01 | Integration | Backend connects to PostgreSQL | Connection successful | High |

## 4. Later test expansion
Increment 3:
- Spring Boot ↔ R Plumber integration
- input validation
- prediction response
- error handling

Increment 4:
- recommendation API
- comparison API
- system test
- performance test
- final test report

## 5. Entry criteria
- Foundation schema reviewed.
- Backend can connect to PostgreSQL.
- API contracts agreed by team.

## 6. Exit criteria
- Critical foundation tests pass.
- No unresolved blocker prevents Increment 2.
- Test results are recorded.
