package com.system.specification;

import com.system.dto.ListingFilterRequest;
import com.system.entity.Listing;
import com.system.entity.Vehicle;
import jakarta.persistence.criteria.Join;
import jakarta.persistence.criteria.JoinType;
import jakarta.persistence.criteria.Predicate;
import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;

/**
 * Xây dựng truy vấn động đa tiêu chí (Criteria Specification) cho bảng listings.
 * Hỗ trợ tìm kiếm từ khóa, khoảng giá, khoảng năm, số km ODO, hãng xe, dòng xe, kiểu dáng, nhiên liệu...
 */
public class ListingSpecification {

    public static Specification<Listing> filterBy(ListingFilterRequest filter) {
        return (root, query, criteriaBuilder) -> {
            if (filter == null) {
                return criteriaBuilder.conjunction();
            }

            List<Predicate> predicates = new ArrayList<>();

            // LEFT JOIN với Vehicle để truy vấn thông số dòng xe
            Join<Listing, Vehicle> vehicleJoin = root.join("vehicle", JoinType.LEFT);

            // 1. Keyword search (tìm kiếm tự do trong brand, model, variant, location)
            if (filter.getKeyword() != null && !filter.getKeyword().trim().isEmpty()) {
                String pattern = "%" + filter.getKeyword().trim().toLowerCase() + "%";
                Predicate keywordPredicate = criteriaBuilder.or(
                        criteriaBuilder.like(criteriaBuilder.lower(vehicleJoin.get("brand")), pattern),
                        criteriaBuilder.like(criteriaBuilder.lower(vehicleJoin.get("model")), pattern),
                        criteriaBuilder.like(criteriaBuilder.lower(criteriaBuilder.coalesce(vehicleJoin.get("variant"), "")), pattern),
                        criteriaBuilder.like(criteriaBuilder.lower(criteriaBuilder.coalesce(root.get("location"), "")), pattern)
                );
                predicates.add(keywordPredicate);
            }

            // 1b. Vehicle ID
            if (filter.getVehicleId() != null) {
                predicates.add(criteriaBuilder.equal(vehicleJoin.get("id"), filter.getVehicleId()));
            }

            // 2. Hãng xe (Brand)
            if (filter.getBrand() != null && !filter.getBrand().trim().isEmpty()) {
                predicates.add(criteriaBuilder.equal(
                        criteriaBuilder.lower(vehicleJoin.get("brand")),
                        filter.getBrand().trim().toLowerCase()
                ));
            }

            // 3. Dòng xe (Model)
            if (filter.getModel() != null && !filter.getModel().trim().isEmpty()) {
                predicates.add(criteriaBuilder.equal(
                        criteriaBuilder.lower(vehicleJoin.get("model")),
                        filter.getModel().trim().toLowerCase()
                ));
            }

            // 4. Phiên bản (Variant)
            if (filter.getVariant() != null && !filter.getVariant().trim().isEmpty()) {
                predicates.add(criteriaBuilder.like(
                        criteriaBuilder.lower(vehicleJoin.get("variant")),
                        "%" + filter.getVariant().trim().toLowerCase() + "%"
                ));
            }

            // 5. Khoảng giá (Price min / max)
            if (filter.getMinPrice() != null) {
                predicates.add(criteriaBuilder.greaterThanOrEqualTo(root.get("price"), filter.getMinPrice()));
            }
            if (filter.getMaxPrice() != null) {
                predicates.add(criteriaBuilder.lessThanOrEqualTo(root.get("price"), filter.getMaxPrice()));
            }

            // 6. Khoảng năm sản xuất (Manufacture Year min / max)
            if (filter.getMinYear() != null) {
                predicates.add(criteriaBuilder.greaterThanOrEqualTo(vehicleJoin.get("manufactureYear"), filter.getMinYear()));
            }
            if (filter.getMaxYear() != null) {
                predicates.add(criteriaBuilder.lessThanOrEqualTo(vehicleJoin.get("manufactureYear"), filter.getMaxYear()));
            }

            // 7. Khoảng số km đã đi (Mileage min / max)
            if (filter.getMinMileage() != null) {
                predicates.add(criteriaBuilder.greaterThanOrEqualTo(root.get("mileage"), filter.getMinMileage()));
            }
            if (filter.getMaxMileage() != null) {
                predicates.add(criteriaBuilder.lessThanOrEqualTo(root.get("mileage"), filter.getMaxMileage()));
            }

            // 8. Loại nhiên liệu (Fuel Type: Gasoline, Diesel, Hybrid, Electric)
            if (filter.getFuelType() != null && !filter.getFuelType().trim().isEmpty()) {
                predicates.add(criteriaBuilder.equal(
                        criteriaBuilder.lower(vehicleJoin.get("fuelType")),
                        filter.getFuelType().trim().toLowerCase()
                ));
            }

            // 9. Hộp số (Transmission: Automatic, Manual, CVT)
            if (filter.getTransmission() != null && !filter.getTransmission().trim().isEmpty()) {
                predicates.add(criteriaBuilder.equal(
                        criteriaBuilder.lower(vehicleJoin.get("transmission")),
                        filter.getTransmission().trim().toLowerCase()
                ));
            }

            // 10. Kiểu dáng (Body Type: Sedan, SUV / Crossover...)
            if (filter.getBodyType() != null && !filter.getBodyType().trim().isEmpty()) {
                predicates.add(criteriaBuilder.equal(
                        criteriaBuilder.lower(vehicleJoin.get("bodyType")),
                        filter.getBodyType().trim().toLowerCase()
                ));
            }

            // 11. Xuất xứ (Origin: Domestic, Imported)
            if (filter.getOrigin() != null && !filter.getOrigin().trim().isEmpty()) {
                predicates.add(criteriaBuilder.equal(
                        criteriaBuilder.lower(vehicleJoin.get("origin")),
                        filter.getOrigin().trim().toLowerCase()
                ));
            }

            // 12. Địa điểm / Tỉnh thành (Location)
            if (filter.getLocation() != null && !filter.getLocation().trim().isEmpty()) {
                predicates.add(criteriaBuilder.like(
                        criteriaBuilder.lower(root.get("location")),
                        "%" + filter.getLocation().trim().toLowerCase() + "%"
                ));
            }

            return criteriaBuilder.and(predicates.toArray(new Predicate[0]));
        };
    }
}
