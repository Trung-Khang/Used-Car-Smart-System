package com.system.service;

import com.system.entity.Vehicle;
import com.system.exception.ResourceNotFoundException;
import com.system.repository.VehicleRepository;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * ===================================================================
 * SERVICE: VEHICLE SERVICE (TẦNG XỬ LÝ LOGIC XE)
 * ===================================================================
 * 
 * - @Service: Đánh dấu class này là Service (chứa nghiệp vụ) của Spring Boot.
 * - Đóng vai trò làm "đầu bếp": Nhận yêu cầu từ Controller -> gọi Repository
 *   để lấy hoặc lưu dữ liệu -> xử lý logic và trả về kết quả.
 */
@Service
public class VehicleService {

    // Tiêm (Inject) VehicleRepository vào để sử dụng
    private final VehicleRepository vehicleRepository;

    public VehicleService(VehicleRepository vehicleRepository) {
        this.vehicleRepository = vehicleRepository;
    }

    // 1. Lấy toàn bộ danh sách xe
    public List<Vehicle> getAllVehicles() {
        return vehicleRepository.findAll();
    }

    // 2. Lấy thông tin chi tiết xe theo ID
    public Vehicle getVehicleById(Long id) {
        return vehicleRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Khong tim thay xe voi ID: " + id));
    }

    // 3. Thêm mới một dòng xe vào hệ thống
    public Vehicle createVehicle(Vehicle vehicle) {
        return vehicleRepository.save(vehicle);
    }

    // 4. Cập nhật thông tin dòng xe
    public Vehicle updateVehicle(Long id, Vehicle vehicleDetails) {
        Vehicle existingVehicle = getVehicleById(id);

        existingVehicle.setBrand(vehicleDetails.getBrand());
        existingVehicle.setModel(vehicleDetails.getModel());
        existingVehicle.setVariant(vehicleDetails.getVariant());
        existingVehicle.setManufactureYear(vehicleDetails.getManufactureYear());
        existingVehicle.setBodyType(vehicleDetails.getBodyType());
        existingVehicle.setFuelType(vehicleDetails.getFuelType());
        existingVehicle.setTransmission(vehicleDetails.getTransmission());

        return vehicleRepository.save(existingVehicle);
    }

    // 5. Xóa xe theo ID
    public void deleteVehicle(Long id) {
        Vehicle vehicle = getVehicleById(id);
        vehicleRepository.delete(vehicle);
    }

    // 6. Tìm kiếm danh sách xe theo Hãng
    public List<Vehicle> getVehiclesByBrand(String brand) {
        return vehicleRepository.findByBrandIgnoreCase(brand);
    }
}
