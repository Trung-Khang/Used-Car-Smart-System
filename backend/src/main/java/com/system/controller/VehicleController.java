package com.system.controller;

import com.system.entity.Vehicle;
import com.system.service.VehicleService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * ===================================================================
 * CONTROLLER: VEHICLE CONTROLLER (REST API QUẢN LÝ XE)
 * ===================================================================
 * 
 * - @RestController: Đánh dấu class này là Controller trả về dữ liệu dạng JSON.
 * - @RequestMapping("/api/v1/vehicles"): Tiền tố đường dẫn cho toàn bộ API trong class này.
 * - @Tag: Đặt tên nhóm API trên giao diện Swagger UI.
 */
@RestController
@RequestMapping("/api/v1/vehicles")
@Tag(name = "1. Vehicle API", description = "Các API quản lý thông tin dòng xe (CRUD cơ bản)")
public class VehicleController {

    private final VehicleService vehicleService;

    // Tiêm (Inject) VehicleService vào Controller
    public VehicleController(VehicleService vehicleService) {
        this.vehicleService = vehicleService;
    }

    // 1. GET: Lấy danh sách xe (Có thể lọc theo hãng nếu truyền ?brand=toyota)
    @GetMapping
    @Operation(summary = "Lấy danh sách tất cả các xe", description = "Trả về danh sách xe trong hệ thống, hỗ trợ lọc theo hãng")
    public ResponseEntity<List<Vehicle>> getAllVehicles(
            @RequestParam(required = false) String brand) {
        if (brand != null && !brand.trim().isEmpty()) {
            return ResponseEntity.ok(vehicleService.getVehiclesByBrand(brand));
        }
        return ResponseEntity.ok(vehicleService.getAllVehicles());
    }

    // 2. GET /{id}: Lấy chi tiết một xe theo ID
    @GetMapping("/{id}")
    @Operation(summary = "Lấy chi tiết một xe theo ID", description = "Nhận vào ID và trả về thông tin chi tiết của xe đó")
    public ResponseEntity<Vehicle> getVehicleById(@PathVariable Long id) {
        Vehicle vehicle = vehicleService.getVehicleById(id);
        return ResponseEntity.ok(vehicle);
    }

    // 3. POST: Thêm mới một dòng xe vào hệ thống
    @PostMapping
    @Operation(summary = "Tạo mới một dòng xe", description = "Nhận thông tin xe từ request body và lưu vào cơ sở dữ liệu")
    public ResponseEntity<Vehicle> createVehicle(@RequestBody Vehicle vehicle) {
        Vehicle createdVehicle = vehicleService.createVehicle(vehicle);
        return new ResponseEntity<>(createdVehicle, HttpStatus.CREATED); // Trả về HTTP 201 Created
    }

    // 4. PUT /{id}: Cập nhật thông tin dòng xe theo ID
    @PutMapping("/{id}")
    @Operation(summary = "Cập nhật thông tin một dòng xe", description = "Cập nhật các thuộc tính của xe theo ID chỉ định")
    public ResponseEntity<Vehicle> updateVehicle(
            @PathVariable Long id, 
            @RequestBody Vehicle vehicleDetails) {
        Vehicle updatedVehicle = vehicleService.updateVehicle(id, vehicleDetails);
        return ResponseEntity.ok(updatedVehicle);
    }

    // 5. DELETE /{id}: Xóa một dòng xe theo ID
    @DeleteMapping("/{id}")
    @Operation(summary = "Xóa một dòng xe theo ID", description = "Xóa bản ghi xe khỏi hệ thống theo ID")
    public ResponseEntity<String> deleteVehicle(@PathVariable Long id) {
        vehicleService.deleteVehicle(id);
        return ResponseEntity.ok("Da xoa thanh cong xe voi ID: " + id);
    }
}
