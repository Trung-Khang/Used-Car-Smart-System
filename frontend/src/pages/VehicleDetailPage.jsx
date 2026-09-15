import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';
import VehicleInfo from '../components/vehicle/VehicleInfo';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import vehicleApi from '../services/vehicleApi';
import './VehicleDetailPage.css';

const VehicleDetailPage = () => {
  const { id } = useParams();
  const [vehicle, setVehicle] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchVehicleDetail = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await vehicleApi.getVehicleById(id);
      setVehicle(data);
    } catch (err) {
      setError(err.message || `Không thể tải thông tin xe #${id}. Vui lòng thử lại sau.`);
    } finally {
      setIsLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchVehicleDetail();
  }, [fetchVehicleDetail]);

  if (isLoading) {
    return (
      <div className="vehicle-detail-page">
        <Link to="/vehicles" className="btn btn-secondary back-btn">
          <FaArrowLeft /> Quay lại danh sách xe
        </Link>
        <Loading message={`Đang tải thông tin xe #${id}...`} />
      </div>
    );
  }

  if (error || !vehicle) {
    return (
      <div className="vehicle-detail-page">
        <Link to="/vehicles" className="btn btn-secondary back-btn">
          <FaArrowLeft /> Quay lại danh sách xe
        </Link>
        <ErrorMessage
          message={error || `Không tìm thấy thông tin cho xe mã #${id}.`}
          onRetry={fetchVehicleDetail}
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
