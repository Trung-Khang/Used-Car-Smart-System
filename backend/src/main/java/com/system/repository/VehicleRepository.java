package com.system.repository;

import com.system.entity.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    // Tìm danh sách xe theo Hãng (không phân biệt chữ hoa/thường)
    List<Vehicle> findByBrandIgnoreCase(String brand);

    // Tìm danh sách xe theo cả Hãng và Dòng xe
    List<Vehicle> findByBrandIgnoreCaseAndModelIgnoreCase(String brand, String model);
}
