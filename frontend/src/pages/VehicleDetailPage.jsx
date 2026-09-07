import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';

const VehicleDetailPage = () => {
  const { id } = useParams();

  return (
    <div className="page-container">
      <Link to="/vehicles" className="btn btn-secondary" style={{ marginBottom: '16px' }}>
        <FaArrowLeft /> Quay lại danh sách
      </Link>
      <h2>Chi tiết xe #{id}</h2>
      <p>Thông tin kỹ thuật, định giá thị trường và phân tích chi tiết.</p>
    </div>
  );
};

export default VehicleDetailPage;
