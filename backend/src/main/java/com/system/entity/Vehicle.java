package com.system.entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "vehicles")
public class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "brand", nullable = false, length = 50)
    private String brand;

    @Column(name = "model", nullable = false, length = 50)
    private String model;

    @Column(name = "variant", length = 100)
    private String variant;

    @Column(name = "manufacture_year", nullable = false)
    private Integer manufactureYear;

    @Column(name = "fuel_type", length = 30)
    private String fuelType;

    @Column(name = "transmission", length = 30)
    private String transmission;

    // Trường Enrich: Dung tích xi lanh (L)
    @Column(name = "engine_size")
    private Double engineSize;

    // Trường Enrich: Số chỗ ngồi
    @Column(name = "seat_count")
    private Integer seatCount;

    // Trường Enrich: Xuất xứ (Lắp ráp trong nước / Nhập khẩu)
    @Column(name = "origin", length = 50)
    private String origin;

    @Column(name = "body_type", length = 50)
    private String bodyType;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    public Vehicle() {
    }

    public Vehicle(String brand, String model, String variant, Integer manufactureYear, 
                   String bodyType, String fuelType, String transmission) {
        this.brand = brand;
        this.model = model;
        this.variant = variant;
        this.manufactureYear = manufactureYear;
        this.bodyType = bodyType;
        this.fuelType = fuelType;
        this.transmission = transmission;
    }

    public Vehicle(String brand, String model, String variant, Integer manufactureYear, 
                   String fuelType, String transmission, Double engineSize, 
                   Integer seatCount, String origin, String bodyType) {
        this.brand = brand;
        this.model = model;
        this.variant = variant;
        this.manufactureYear = manufactureYear;
        this.fuelType = fuelType;
        this.transmission = transmission;
        this.engineSize = engineSize;
        this.seatCount = seatCount;
        this.origin = origin;
        this.bodyType = bodyType;
    }

    @PrePersist
    protected void onCreate() {
        if (this.createdAt == null) {
            this.createdAt = Instant.now();
        }
    }

    // ---------------------------------------------------------------
    // GETTERS & SETTERS
    // ---------------------------------------------------------------
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getVariant() {
        return variant;
    }

    public void setVariant(String variant) {
        this.variant = variant;
    }

    public Integer getManufactureYear() {
        return manufactureYear;
    }

    public void setManufactureYear(Integer manufactureYear) {
        this.manufactureYear = manufactureYear;
    }

    public String getFuelType() {
        return fuelType;
    }

    public void setFuelType(String fuelType) {
        this.fuelType = fuelType;
    }

    public String getTransmission() {
        return transmission;
    }

    public void setTransmission(String transmission) {
        this.transmission = transmission;
    }

    public Double getEngineSize() {
        return engineSize;
    }

    public void setEngineSize(Double engineSize) {
        this.engineSize = engineSize;
    }

    public Integer getSeatCount() {
        return seatCount;
    }

    public void setSeatCount(Integer seatCount) {
        this.seatCount = seatCount;
    }

    public String getOrigin() {
        return origin;
    }

    public void setOrigin(String origin) {
        this.origin = origin;
    }

    public String getBodyType() {
        return bodyType;
    }

    public void setBodyType(String bodyType) {
        this.bodyType = bodyType;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }
}
