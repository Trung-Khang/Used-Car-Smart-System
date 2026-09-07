import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaRoad, FaGasPump, FaCogs, FaMapMarkerAlt } from 'react-icons/fa';
import { formatPrice, formatMileage, formatYear } from '../../utils/formatters';
import './VehicleCard.css';

const DEFAULT_CAR_IMAGE = 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600&auto=format&fit=crop&q=80';

const VehicleCard = ({ vehicle }) => {
  const [imgSrc, setImgSrc] = useState(vehicle.image_url || DEFAULT_CAR_IMAGE);

  if (!vehicle) return null;

  const handleImageError = () => {
    setImgSrc(DEFAULT_CAR_IMAGE);
  };

  return (
    <Link to={`/vehicles/${vehicle.id}`} className="vehicle-card">
      <div className="vehicle-image-wrapper">
        <img
          src={imgSrc}
          alt={`${vehicle.brand} ${vehicle.model}`}
          className="vehicle-image"
          onError={handleImageError}
          loading="lazy"
        />
        <div className="vehicle-badge-year">{formatYear(vehicle.manufacture_year)}</div>
      </div>

      <div className="vehicle-content">
        <div className="vehicle-header">
          <span className="vehicle-brand">{vehicle.brand}</span>
          <h3 className="vehicle-name">
            {vehicle.model} <span className="vehicle-variant">{vehicle.variant}</span>
          </h3>
        </div>

        <div className="vehicle-price-tag">
          {formatPrice(vehicle.price)}
        </div>

        <div className="vehicle-specs-grid">
          <div className="spec-item" title="Số km đã lăn bánh">
            <FaRoad className="spec-icon" />
            <span>{formatMileage(vehicle.mileage)}</span>
          </div>
          <div className="spec-item" title="Nhiên liệu">
            <FaGasPump className="spec-icon" />
            <span>{vehicle.fuel_type || 'Xăng'}</span>
          </div>
          <div className="spec-item" title="Hộp số">
            <FaCogs className="spec-icon" />
            <span>{vehicle.transmission || 'Tự động'}</span>
          </div>
          <div className="spec-item" title="Khu vực bán">
            <FaMapMarkerAlt className="spec-icon" />
            <span className="spec-location">{vehicle.location || 'Toàn quốc'}</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default VehicleCard;

