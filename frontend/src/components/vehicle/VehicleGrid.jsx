import React from 'react';
import VehicleCard from './VehicleCard';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';
import { FaInbox } from 'react-icons/fa';
import './VehicleGrid.css';

const VehicleGrid = ({
  vehicles = [],
  isLoading = false,
  error = null,
  onRetry = null,
}) => {
  if (isLoading) {
    return <Loading message="Đang tải danh sách xe từ hệ thống..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={onRetry} />;
  }

  if (!vehicles || vehicles.length === 0) {
    return (
      <div className="empty-vehicles-card">
        <FaInbox className="empty-icon" />
        <h3 className="empty-title">Không tìm thấy xe nào</h3>
        <p className="empty-desc">
          Hiện tại chưa có dữ liệu xe phù hợp với tiêu chí tìm kiếm của bạn. Vui lòng thử lại sau.
        </p>
      </div>
    );
  }

  return (
    <div className="vehicle-grid">
      {vehicles.map((vehicle) => (
        <VehicleCard key={vehicle.id} vehicle={vehicle} />
      ))}
    </div>
  );
};

export default VehicleGrid;

