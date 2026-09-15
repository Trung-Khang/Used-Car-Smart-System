package com.system.repository;

import com.system.entity.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * ===================================================================
 * REPOSITORY: VEHICLE REPOSITORY (THAO TÁC BẢNG vehicles)
 * ===================================================================
 * 
 * TẠI SAO DÙNG INTERFACE KẾ THỪA JpaRepository?
 * - JpaRepository<Vehicle, Long> là thư viện có sẵn của Spring Data JPA.
 * - Nó tự động cung cấp sẵn cho bạn các hàm cơ bản:
 *   + findAll(): Lấy tất cả danh sách xe.
 *   + findById(id): Tìm xe theo ID (Khóa chính).
 *   + save(vehicle): Thêm mới hoặc cập nhật xe.
 *   + deleteById(id): Xóa xe theo ID.
 * - Bạn KHÔNG cần phải viết câu lệnh SQL thủ công!
 */
@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    // Tìm danh sách xe theo Hãng (không phân biệt chữ hoa/thường)
    // Ví dụ: findByBrandIgnoreCase("toyota") -> SELECT * FROM vehicles WHERE LOWER(brand) = 'toyota'
    List<Vehicle> findByBrandIgnoreCase(String brand);

    // Tìm danh sách xe theo cả Hãng và Dòng xe (Ví dụ: Toyota Vios)
    List<Vehicle> findByBrandIgnoreCaseAndModelIgnoreCase(String brand, String model);
}
