# ERD — Increment 1

The workflow explicitly requires PostgreSQL and the system contains vehicle listing,
pricing/prediction, recommendation and comparison concepts. The following ERD is
the proposed foundation model; it must be reviewed against the actual Spring Boot
entities before implementation.

```mermaid
erDiagram
    VEHICLE ||--o{ COMPARISON_VEHICLE : "selected in"
    VEHICLE_COMPARISON ||--o{ COMPARISON_VEHICLE : contains

    VEHICLE {
        bigint vehicle_id PK
        varchar make
        varchar model
        int year
        numeric mileage
        varchar fuel
        varchar transmission
        numeric listing_price
        numeric predicted_price
        numeric difference_percent
        varchar model_version
        text source_url
        timestamp created_at
        timestamp updated_at
    }

    VEHICLE_COMPARISON {
        bigint comparison_id PK
        timestamp created_at
    }

    COMPARISON_VEHICLE {
        bigint comparison_id PK, FK
        bigint vehicle_id PK, FK
    }
```

## Relationship
- One comparison contains multiple selected vehicles.
- One vehicle can participate in multiple comparisons.
- `comparison_vehicle` resolves the many-to-many relationship.

## Not yet fixed by the workflow
- User/account entity
- Recommendation persistence
- Raw/clean staging tables
- Exact crawler-source entity
- Exact authentication model
