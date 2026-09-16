package com.system.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "listings")
public class Listing {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Khóa ngoại liên kết với bảng "vehicles"
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "vehicle_id", nullable = false)
    private Vehicle vehicle;

    // Khóa ngoại liên kết với bảng "sources" (Nguồn cào: Chotot, Bonbanh...)
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "source_id", nullable = false)
    private Source source;

    // Giá rao bán thực tế của người bán (VND)
    @Column(name = "price", nullable = false, precision = 15, scale = 2)
    private BigDecimal price;

    // Số km đã đi (ODO) - Nullable
    @Column(name = "mileage")
    private Integer mileage;

    // Màu sắc xe
    @Column(name = "color", length = 30)
    private String color;

    // Khu vực / Tỉnh thành rao bán
    @Column(name = "location", length = 100)
    private String location;

    // Đường dẫn bài viết gốc (Khóa duy nhất UNIQUE để chống trùng lặp)
    @Column(name = "source_url", nullable = false, unique = true, columnDefinition = "TEXT")
    private String sourceUrl;

    // Đường dẫn ảnh đại diện của xe phục vụ hiển thị UI
    @Column(name = "image_url", length = 500)
    private String imageUrl;

    // Chuỗi thời gian gốc từ nguồn (VD: "2 giờ trước", "14/09/2026")
    @Column(name = "listed_at_raw", columnDefinition = "TEXT")
    private String listedAtRaw;

    // Thời gian đăng tin đã được xác minh/chuẩn hóa (nếu có)
    @Column(name = "listed_at")
    private Instant listedAt;

    // Thời gian hệ thống cào dữ liệu về (bảo toàn múi giờ)
    @Column(name = "crawled_at", nullable = false)
    private Instant crawledAt;

    // Thời gian tạo bản ghi trong Database
    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    // Thời gian cập nhật bản ghi gần nhất
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public Listing() {
    }

    public Listing(Vehicle vehicle, Source source, BigDecimal price, Integer mileage, 
                   String location, String sourceUrl, String imageUrl, Instant crawledAt) {
        this.vehicle = vehicle;
        this.source = source;
        this.price = price;
        this.mileage = mileage;
        this.location = location;
        this.sourceUrl = sourceUrl;
        this.imageUrl = imageUrl;
        this.crawledAt = crawledAt;
    }

    @PrePersist
    protected void onCreate() {
        Instant now = Instant.now();
        if (this.createdAt == null) {
            this.createdAt = now;
        }
        if (this.updatedAt == null) {
            this.updatedAt = now;
        }
        if (this.crawledAt == null) {
            this.crawledAt = now;
        }
    }

    @PreUpdate
    protected void onUpdate() {
        this.updatedAt = Instant.now();
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

    public Vehicle getVehicle() {
        return vehicle;
    }

    public void setVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
    }

    public Source getSource() {
        return source;
    }

    public void setSource(Source source) {
        this.source = source;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public Integer getMileage() {
        return mileage;
    }

    public void setMileage(Integer mileage) {
        this.mileage = mileage;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getSourceUrl() {
        return sourceUrl;
    }

    public void setSourceUrl(String sourceUrl) {
        this.sourceUrl = sourceUrl;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getListedAtRaw() {
        return listedAtRaw;
    }

    public void setListedAtRaw(String listedAtRaw) {
        this.listedAtRaw = listedAtRaw;
    }

    public Instant getListedAt() {
        return listedAt;
    }

    public void setListedAt(Instant listedAt) {
        this.listedAt = listedAt;
    }

    public Instant getCrawledAt() {
        return crawledAt;
    }

    public void setCrawledAt(Instant crawledAt) {
        this.crawledAt = crawledAt;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Instant updatedAt) {
        this.updatedAt = updatedAt;
    }
}
