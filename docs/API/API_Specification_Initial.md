# Initial API Specification

The workflow assigns Spring Boot as the backend API layer and ReactJS as the
frontend consumer. These are initial contracts for Increment 1. Exact endpoint
paths and DTO names must be agreed with Member 01 before implementation.

## Vehicle

### GET /api/vehicles
Purpose: return a paginated vehicle list.

Query parameters:
- `page`
- `size`
- `sort`
- optional search/filter parameters

Response concept:
```json
{
  "content": [],
  "page": 0,
  "size": 20,
  "totalElements": 0
}
```

### GET /api/vehicles/{vehicleId}
Purpose: return vehicle detail.

Success: `200 OK`

Not found: `404 Not Found`

### GET /api/vehicles/search
Purpose: search/filter vehicles.

Possible parameters:
- `keyword`
- `minPrice`
- `maxPrice`
- `minYear`
- `maxYear`
- `minMileage`
- `maxMileage`

These parameter names are proposed from the workflow's stated price/year/mileage
filters and should be finalized with Member 01.

## Comparison

### POST /api/comparisons
Purpose: create a comparison from selected vehicle IDs.

Proposed request:
```json
{
  "vehicleIds": [1, 2]
}
```

### GET /api/comparisons/{comparisonId}
Purpose: return comparison result.

## Valuation — prepared for Increment 3

### POST /api/valuation
Purpose: request predicted price.

Proposed request:
```json
{
  "vehicleId": 1
}
```

Proposed response:
```json
{
  "vehicleId": 1,
  "predictedPrice": 0,
  "differencePercent": 0,
  "modelVersion": "regression_v1"
}
```

## Recommendation — prepared for Increment 4

### GET /api/recommendations
Purpose: return ranked recommended vehicles.

The workflow defines recommendation score/ranking conceptually, but does not
define a final request/response schema. Final DTO fields must be agreed by the team.

## HTTP conventions
- `200 OK`: successful read/request.
- `201 Created`: successful resource creation.
- `400 Bad Request`: invalid input.
- `404 Not Found`: resource does not exist.
- `500 Internal Server Error`: unexpected server error.
