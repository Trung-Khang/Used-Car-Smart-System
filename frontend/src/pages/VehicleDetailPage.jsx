import React, { useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';
import VehicleInfo from '../components/vehicle/VehicleInfo';
import ErrorMessage from '../components/common/ErrorMessage';
import { MOCK_VEHICLES } from '../utils/mockVehicles';
import './VehicleDetailPage.css';

const VehicleDetailPage = () => {
  const { id } = useParams();

  // Tìm xe theo ID (hỗ trợ cả kiểu number lẫn string)
  const vehicle = useMemo(() => {
    return MOCK_VEHICLES.find((v) => String(v.id) === String(id));
  }, [id]);

  if (!vehicle) {
    return (
      <div className="vehicle-detail-page">
        <Link to="/vehicles" className="btn btn-secondary back-btn">
          <FaArrowLeft /> Quay lại danh sách xe
        </Link>
        <ErrorMessage
          message={`Không tìm thấy thông tin cho xe mã #${id}. Xe có thể đã được gỡ hoặc liên kết không tồn tại.`}
        />
      </div>
    );
  }

  return (
    <div className="vehicle-detail-page">
      <div className="detail-navigation-bar">
        <Link to="/vehicles" className="btn btn-secondary back-btn">
          <FaArrowLeft /> Quay lại danh sách xe
        </Link>
        <span className="breadcrumb-text">
          Danh sách xe / {vehicle.brand} / {vehicle.model}
        </span>
      </div>

      <VehicleInfo vehicle={vehicle} />
    </div>
  );
};

export default VehicleDetailPage;
