package com.system.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * ===================================================================
 * ENTITY: LISTING (BẢNG: listings)
 * ===================================================================
 * 
 * Đại diện cho một tin đăng rao bán xe thực tế trên thị trường (Chợ Tốt, v.v.).
 * - @Entity: Khai báo bảng CSDL.
 * - @Table(name = "listings"): Tên bảng trong PostgreSQL là "listings".
 */
@Entity
@Table(name = "listings")
public class Listing {

    // 1. Khóa chính (Primary Key), tự động tăng ID
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 2. Khóa ngoại liên kết với bảng "vehicles" (Quan hệ: Nhiều tin đăng có thể thuộc về 1 dòng xe)
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "vehicle_id", nullable = false)
    private Vehicle vehicle;

    // 3. Giá rao bán thực tế của người bán (Đơn vị: VNĐ, dùng BigDecimal để tính toán tiền tệ chính xác)
    @Column(name = "price", nullable = false, precision = 15, scale = 2)
    private BigDecimal price;

    // 4. Số km đã đi (ODO - Mileage)
    @Column(name = "mileage", nullable = false)
    private Integer mileage;

    // 5. Khu vực / Tỉnh thành rao bán (Ví dụ: TP.HCM, Hà Nội, Đà Nẵng...)
    @Column(name = "location", length = 100)
    private String location;

    // 6. ID của nguồn cào dữ liệu (Khóa ngoại tới bảng sources)
    @Column(name = "source_id")
    private Long sourceId;

    // 7. Đường dẫn (URL) tới bài viết gốc trên sàn xe cũ
    @Column(name = "source_url", length = 500)
    private String sourceUrl;

    // 8. Đường dẫn ảnh đại diện của xe
    @Column(name = "image_url", length = 500)
    private String imageUrl;

    // 9. Thời gian bài viết được đăng lên sàn rao vặt
    @Column(name = "listed_at")
    private LocalDateTime listedAt;

    // 10. Thời gian hệ thống (TV3) cào dữ liệu về
    @Column(name = "crawled_at")
    private LocalDateTime crawledAt;

    // 11. Thời gian tạo bản ghi trong Database
    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // ---------------------------------------------------------------
    // CONSTRUCTORS (HÀM KHỞI TẠO)
    // ---------------------------------------------------------------
    public Listing() {
    }

    public Listing(Vehicle vehicle, BigDecimal price, Integer mileage, String location, 
                   String sourceUrl, String imageUrl, LocalDateTime listedAt) {
        this.vehicle = vehicle;
        this.price = price;
        this.mileage = mileage;
        this.location = location;
        this.sourceUrl = sourceUrl;
        this.imageUrl = imageUrl;
        this.listedAt = listedAt;
    }

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
        if (this.crawledAt == null) {
            this.crawledAt = LocalDateTime.now();
        }
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

    public Vehicle getVehicle() {
        return vehicle;
    }

    public void setVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
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

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public Long getSourceId() {
        return sourceId;
    }

    public void setSourceId(Long sourceId) {
        this.sourceId = sourceId;
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

    public LocalDateTime getListedAt() {
        return listedAt;
    }

    public void setListedAt(LocalDateTime listedAt) {
        this.listedAt = listedAt;
    }

    public LocalDateTime getCrawledAt() {
        return crawledAt;
    }

    public void setCrawledAt(LocalDateTime crawledAt) {
        this.crawledAt = crawledAt;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
