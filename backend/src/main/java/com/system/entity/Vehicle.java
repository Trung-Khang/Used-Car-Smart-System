package com.system.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * ===================================================================
 * ENTITY: VEHICLE (BẢNG: vehicles)
 * ===================================================================
 * 
 * Đại diện cho thông tin kỹ thuật gốc của một dòng xe.
 * - @Entity: Báo cho Spring Data JPA / Hibernate biết đây là một bảng CSDL.
 * - @Table(name = "vehicles"): Tên bảng trong PostgreSQL là "vehicles".
 */
@Entity
@Table(name = "vehicles")
public class Vehicle {

    // 1. Khóa chính (Primary Key), tự động tăng ID (1, 2, 3...)
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 2. Hãng xe (Ví dụ: Toyota, Honda, Mazda, Hyundai, Kia...)
    @Column(name = "brand", nullable = false, length = 100)
    private String brand;

    // 3. Dòng xe (Ví dụ: Vios, City, CX-5, Accent, Morning...)
    @Column(name = "model", nullable = false, length = 100)
    private String model;

    // 4. Phiên bản (Ví dụ: 1.5G, 2.0 Premium, 1.4 AT...)
    @Column(name = "variant", length = 100)
    private String variant;

    // 5. Năm sản xuất (Ví dụ: 2020, 2021, 2022...)
    @Column(name = "manufacture_year", nullable = false)
    private Integer manufactureYear;

    // 6. Kiểu dáng xe (Ví dụ: Sedan, SUV, Hatchback, Crossover, CUV...)
    @Column(name = "body_type", length = 50)
    private String bodyType;

    // 7. Loại nhiên liệu (Ví dụ: Gasoline / Xang, Diesel / Dau, Hybrid, Electric / Dien)
    @Column(name = "fuel_type", length = 50)
    private String fuelType;

    // 8. Hộp số (Ví dụ: Automatic / Tu dong, Manual / So san)
    @Column(name = "transmission", length = 50)
    private String transmission;

    // 9. Thời gian tạo bản ghi trong hệ thống
    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // ---------------------------------------------------------------
    // CONSTRUCTORS (HÀM KHỞI TẠO)
    // ---------------------------------------------------------------
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

    // Tự động gán thời gian hiện tại khi thêm mới bản ghi
    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    // ---------------------------------------------------------------
    // GETTERS & SETTERS (ĐỌC VÀ GHI DỮ LIỆU)
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

    public String getBodyType() {
        return bodyType;
    }

    public void setBodyType(String bodyType) {
        this.bodyType = bodyType;
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

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
