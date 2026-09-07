import React, { useState } from 'react';
import {
  FaCalendarAlt,
  FaRoad,
  FaGasPump,
  FaCogs,
  FaCarSide,
  FaMapMarkerAlt,
  FaExternalLinkAlt,
  FaTag,
} from 'react-icons/fa';
import { formatFullPrice, formatMileage, formatYear } from '../../utils/formatters';
import './VehicleInfo.css';

const DEFAULT_CAR_IMAGE = 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&auto=format&fit=crop&q=80';

const VehicleInfo = ({ vehicle }) => {
  const [imgSrc, setImgSrc] = useState(vehicle?.image_url || DEFAULT_CAR_IMAGE);

  if (!vehicle) return null;

  return (
    <div className="vehicle-info-container">
      <div className="vehicle-info-gallery">
        <img
          src={imgSrc}
          alt={`${vehicle.brand} ${vehicle.model}`}
          className="vehicle-info-main-image"
          onError={() => setImgSrc(DEFAULT_CAR_IMAGE)}
        />
      </div>

      <div className="vehicle-info-details">
        <div className="vehicle-info-header">
          <span className="info-brand-badge">{vehicle.brand}</span>
          <h1 className="info-title">
            {vehicle.model} {vehicle.variant}
          </h1>
          <div className="info-price-section">
            <span className="price-label">Giá niêm yết:</span>
            <span className="price-value">{formatFullPrice(vehicle.price)}</span>
          </div>
        </div>

        <div className="specs-table-container">
          <h3 className="specs-section-title">Thông số kỹ thuật</h3>
          <div className="specs-grid-detailed">
            <div className="spec-row">
              <span className="spec-label">
                <FaCalendarAlt className="icon" /> Năm sản xuất:
              </span>
              <span className="spec-value">{formatYear(vehicle.manufacture_year)}</span>
            </div>

            <div className="spec-row">
              <span className="spec-label">
                <FaRoad className="icon" /> Số km đã đi:
              </span>
              <span className="spec-value">{formatMileage(vehicle.mileage)}</span>
            </div>

            <div className="spec-row">
              <span className="spec-label">
                <FaGasPump className="icon" /> Nhiên liệu:
              </span>
              <span className="spec-value">{vehicle.fuel_type || 'Xăng'}</span>
            </div>

            <div className="spec-row">
              <span className="spec-label">
                <FaCogs className="icon" /> Hộp số:
              </span>
              <span className="spec-value">{vehicle.transmission || 'Tự động'}</span>
            </div>

            <div className="spec-row">
              <span className="spec-label">
                <FaCarSide className="icon" /> Kiểu dáng:
              </span>
              <span className="spec-value">{vehicle.body_type || 'Sedan'}</span>
            </div>

            <div className="spec-row">
              <span className="spec-label">
                <FaMapMarkerAlt className="icon" /> Khu vực bán:
              </span>
              <span className="spec-value">{vehicle.location || 'Toàn quốc'}</span>
            </div>
          </div>
        </div>

        {vehicle.description && (
          <div className="vehicle-description-box">
            <h3 className="specs-section-title">Mô tả người bán</h3>
            <p className="description-text">{vehicle.description}</p>
          </div>
        )}

        {vehicle.source_url && (
          <div className="source-link-box">
            <a
              href={vehicle.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-secondary source-link-btn"
            >
              <FaExternalLinkAlt /> Xem tin đăng gốc
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default VehicleInfo;
