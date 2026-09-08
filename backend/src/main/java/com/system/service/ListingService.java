package com.system.service;

import com.system.entity.Listing;
import com.system.exception.ResourceNotFoundException;
import com.system.repository.ListingRepository;
import com.system.repository.VehicleRepository;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * ===================================================================
 * SERVICE: LISTING SERVICE (TẦNG XỬ LÝ LOGIC TIN ĐĂNG BÁN XE)
 * ===================================================================
 */
@Service
public class ListingService {

    private final ListingRepository listingRepository;
    private final VehicleRepository vehicleRepository;

    public ListingService(ListingRepository listingRepository, VehicleRepository vehicleRepository) {
        this.listingRepository = listingRepository;
        this.vehicleRepository = vehicleRepository;
    }

    // 1. Lấy toàn bộ danh sách tin đăng rao bán xe
    public List<Listing> getAllListings() {
        return listingRepository.findAll();
    }

    // 2. Lấy chi tiết một tin đăng theo ID
    public Listing getListingById(Long id) {
        return listingRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Khong tim thay tin dang voi ID: " + id));
    }

    // 3. Thêm mới một tin đăng bán xe
    public Listing createListing(Listing listing) {
        // Kiểm tra xem dòng xe (Vehicle) liên kết có tồn tại hay không
        if (listing.getVehicle() != null && listing.getVehicle().getId() != null) {
            vehicleRepository.findById(listing.getVehicle().getId())
                    .orElseThrow(() -> new ResourceNotFoundException(
                            "Khong tim thay dong xe voi ID: " + listing.getVehicle().getId()));
        }
        return listingRepository.save(listing);
    }

    // 4. Xóa tin đăng theo ID
    public void deleteListing(Long id) {
        Listing listing = getListingById(id);
        listingRepository.delete(listing);
    }

    // 5. Lấy danh sách tin đăng theo dòng xe
    public List<Listing> getListingsByVehicleId(Long vehicleId) {
        return listingRepository.findByVehicleId(vehicleId);
    }
}
