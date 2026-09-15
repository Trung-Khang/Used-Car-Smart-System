import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { formatPrice, formatMileage, formatYear } from '../../utils/formatters';
import './VehicleCard.css';

const DEFAULT_CAR_IMAGE = 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600&auto=format&fit=crop&q=80';

const VehicleCard = ({ vehicle }) => {
  const [imgSrc, setImgSrc] = useState(vehicle?.image_url || DEFAULT_CAR_IMAGE);

  if (!vehicle) return null;

  // Tính nhãn mô phỏng thông minh cho Inc 1 (Increment 3 sẽ lấy từ backend R model)
  // Quy ước tạm thời mô phỏng chuẩn theo hình mẫu:
  let tagClass = 'tag-good';
  let tagText = 'Giá tốt';
  let diffNote = 'Thấp hơn 6% so với mức giá mô hình dự đoán';

  if (vehicle.id % 3 === 2) {
    tagClass = 'tag-fair';
    tagText = 'Đúng giá thị trường';
    diffNote = 'Chênh lệch dưới 2% so với mức giá mô hình dự đoán';
  } else if (vehicle.id % 3 === 0) {
    tagClass = 'tag-high';
    tagText = 'Cao hơn thị trường';
    diffNote = 'Cao hơn 7% so với mức giá mô hình dự đoán';
  }

  return (
    <Link to={`/vehicles/${vehicle.id}`} className="vehicle-card-v2">
      <div className="card-top-media">
        <img
          src={imgSrc}
          alt={`${vehicle.brand} ${vehicle.model}`}
          className="card-car-img"
          onError={() => setImgSrc(DEFAULT_CAR_IMAGE)}
          loading="lazy"
        />
      </div>

      <div className="card-body">
        <h3 className="card-car-name">
          {vehicle.brand} {vehicle.model} {vehicle.variant} {formatYear(vehicle.manufacture_year)}
        </h3>
        
        <p className="card-car-subinfo">
          {formatMileage(vehicle.mileage)} · {vehicle.location || 'Toàn quốc'}
        </p>

        <div className="card-price-row">
          <span className="card-price-val">{formatPrice(vehicle.price)}</span>
          <span className={`card-smart-tag ${tagClass}`}>{tagText}</span>
        </div>

        <p className="card-diff-explanation">{diffNote}</p>
      </div>
    </Link>
  );
};

export default VehicleCard;
