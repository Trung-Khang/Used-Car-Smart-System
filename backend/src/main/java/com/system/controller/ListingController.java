package com.system.controller;

import com.system.entity.Listing;
import com.system.service.ListingService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * ===================================================================
 * CONTROLLER: LISTING CONTROLLER (REST API QUẢN LÝ TIN ĐĂNG BÁN XE)
 * ===================================================================
 */
@RestController
@RequestMapping("/api/v1/listings")
@Tag(name = "2. Listing API", description = "Các API quản lý tin đăng rao bán xe trên thị trường")
public class ListingController {

    private final ListingService listingService;

    public ListingController(ListingService listingService) {
        this.listingService = listingService;
    }

    // 1. GET: Lấy danh sách tin đăng (Hỗ trợ lọc theo vehicleId nếu có)
    @GetMapping
    @Operation(summary = "Lấy danh sách tất cả tin đăng xe", description = "Trả về danh sách các tin rao bán xe thực tế")
    public ResponseEntity<List<Listing>> getAllListings(
            @RequestParam(required = false) Long vehicleId) {
        if (vehicleId != null) {
            return ResponseEntity.ok(listingService.getListingsByVehicleId(vehicleId));
        }
        return ResponseEntity.ok(listingService.getAllListings());
    }

    // 2. GET /{id}: Lấy chi tiết tin đăng theo ID
    @GetMapping("/{id}")
    @Operation(summary = "Lấy chi tiết tin đăng theo ID", description = "Nhận vào ID tin đăng và trả về thông tin chi tiết kèm thông số xe")
    public ResponseEntity<Listing> getListingById(@PathVariable Long id) {
        Listing listing = listingService.getListingById(id);
        return ResponseEntity.ok(listing);
    }

    // 3. POST: Thêm mới một tin đăng bán xe
    @PostMapping
    @Operation(summary = "Tạo mới tin đăng xe", description = "Nhận thông tin tin đăng từ người dùng/crawler và lưu vào Database")
    public ResponseEntity<Listing> createListing(@RequestBody Listing listing) {
        Listing createdListing = listingService.createListing(listing);
        return new ResponseEntity<>(createdListing, HttpStatus.CREATED);
    }

    // 4. DELETE /{id}: Xóa một tin đăng theo ID
    @DeleteMapping("/{id}")
    @Operation(summary = "Xóa một tin đăng theo ID", description = "Xóa bài đăng rao bán khỏi hệ thống theo ID chỉ định")
    public ResponseEntity<String> deleteListing(@PathVariable Long id) {
        listingService.deleteListing(id);
        return ResponseEntity.ok("Da xoa thanh cong tin dang voi ID: " + id);
    }
}
