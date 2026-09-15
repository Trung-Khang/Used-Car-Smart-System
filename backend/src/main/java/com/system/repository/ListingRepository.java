package com.system.repository;

import com.system.entity.Listing;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * ===================================================================
 * REPOSITORY: LISTING REPOSITORY (THAO TÁC BẢNG listings)
 * ===================================================================
 * 
 * - Tự động có sẵn các hàm: findAll(), findById(), save(), deleteById().
 */
@Repository
public interface ListingRepository extends JpaRepository<Listing, Long> {

    // Tìm tất cả tin đăng theo ID dòng xe (Vehicle ID)
    List<Listing> findByVehicleId(Long vehicleId);

    // Tìm tin đăng theo địa điểm / tỉnh thành (Ví dụ: "TP.HCM", "Hà Nội")
    List<Listing> findByLocationContainingIgnoreCase(String location);
}
