import React from 'react';
import { Link } from 'react-router-dom';
import { FaSearch, FaCalculator, FaBalanceScale } from 'react-icons/fa';

const HomePage = () => {
  return (
    <div className="home-placeholder">
      <h2>Chào mừng đến với Smart Used-Car Decision Support System</h2>
      <p>Hệ thống hỗ trợ tìm kiếm, định giá thông minh và so sánh xe ô tô cũ.</p>
      <div style={{ marginTop: '20px' }}>
        <Link to="/vehicles" className="btn btn-primary">
          <FaSearch /> Xem danh sách xe
        </Link>
      </div>
    </div>
  );
};

export default HomePage;
