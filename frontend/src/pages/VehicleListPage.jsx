import React, { useState, useEffect, useCallback } from 'react';
import VehicleGrid from '../components/vehicle/VehicleGrid';
import vehicleApi from '../services/vehicleApi';
import { FaCar } from 'react-icons/fa';
import './VehicleListPage.css';

const VehicleListPage = () => {
  const [vehicles, setVehicles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchVehicles = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await vehicleApi.getVehicles();
      setVehicles(data);
    } catch (err) {
      setError(err.message || 'Không thể tải danh sách xe. Vui lòng thử lại.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchVehicles();
  }, [fetchVehicles]);

  return (
    <div className="vehicle-list-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Danh sách xe đang bán</h1>
          <p className="page-subtitle">
            Khám phá các mẫu xe đã qua sử dụng với đầy đủ thông số kỹ thuật và nguồn gốc tin cậy
          </p>
        </div>
        {!isLoading && !error && (
          <div className="vehicle-count-badge">
            <FaCar /> <span>{vehicles.length} xe đang có sẵn</span>
          </div>
        )}
      </div>

      <VehicleGrid
        vehicles={vehicles}
        isLoading={isLoading}
        error={error}
        onRetry={fetchVehicles}
      />
    </div>
  );
};

export default VehicleListPage;
