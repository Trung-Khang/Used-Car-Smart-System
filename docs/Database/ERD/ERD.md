# Entity Relationship Diagram (ERD) - Version 2.0.0

**Project:** Used-Car-Smart-System  
**Author:** TV5 (Database Master)  
**Date:** 15/09/2026  

## ERD Diagram

```mermaid
erDiagram
    SOURCES ||--o{ LISTINGS : "publishes"
    VEHICLES ||--o{ LISTINGS : "described_by"

    SOURCES {
        int id PK
        string code UK
        string name
        string base_url
    }

    VEHICLES {
        bigint id PK
        string brand
        string model
        string variant
        int manufacture_year
        string body_type
        string fuel_type
        string transmission
        string engine_size
        int seat_count
        string origin
    }

    LISTINGS {
        bigint id PK
        bigint vehicle_id FK
        int source_id FK
        numeric price
        int mileage
        string color
        string location
        string source_url UK
        string image_url
        timestamptz crawled_at
        string listed_at_raw
        timestamptz created_at
    }