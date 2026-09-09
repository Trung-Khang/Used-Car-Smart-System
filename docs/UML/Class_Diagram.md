# Class Diagram — Initial Design

This diagram separates the core backend/domain objects from the decision-support
objects. It is an initial design and should be synchronized with Member 01's
Spring Boot package structure.

```mermaid
classDiagram
    class Vehicle {
        +Long vehicleId
        +String make
        +String model
        +Integer year
        +BigDecimal mileage
        +String fuel
        +String transmission
        +BigDecimal listingPrice
        +BigDecimal predictedPrice
        +BigDecimal differencePercent
        +String modelVersion
        +String sourceUrl
    }

    class VehicleComparison {
        +Long comparisonId
        +LocalDateTime createdAt
    }

    class ComparisonVehicle {
        +Long comparisonId
        +Long vehicleId
    }

    class RecommendationResult {
        +BigDecimal recommendationScore
        +Integer ranking
    }

    VehicleComparison "1" --> "*" ComparisonVehicle
    Vehicle "1" --> "*" ComparisonVehicle
    Vehicle --> RecommendationResult : evaluated for
```

`RecommendationResult` is a design-level class for Increment 4; the workflow
does not yet define its persistence fields in PostgreSQL.
