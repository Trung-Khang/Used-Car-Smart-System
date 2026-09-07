import React, { useState } from 'react';
import VehicleGrid from '../components/vehicle/VehicleGrid';
import { MOCK_VEHICLES } from '../utils/mockVehicles';
import { FaCar } from 'react-icons/fa';
import './VehicleListPage.css';

const VehicleListPage = () => {
  // Ở Increment 1, sử dụng mock data để hoàn thiện giao diện
  // Ở Task 5 sẽ kết nối với vehicleApi service
  const [vehicles] = useState(MOCK_VEHICLES);
  const [isLoading] = useState(false);
  const [error] = useState(null);

  return (
    <div className="vehicle-list-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Danh sách xe đang bán</h1>
          <p className="page-subtitle">
            Khám phá các mẫu xe đã qua sử dụng với đầy đủ thông số kỹ thuật và nguồn gốc tin cậy
          </p>
        </div>
        <div className="vehicle-count-badge">
          <FaCar /> <span>{vehicles.length} xe đang có sẵn</span>
        </div>
      </div>

      <VehicleGrid
        vehicles={vehicles}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
};

export default VehicleListPage;
