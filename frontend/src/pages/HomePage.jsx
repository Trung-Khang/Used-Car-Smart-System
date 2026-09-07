import React from 'react';
import { Link } from 'react-router-dom';
import { FaSearch, FaRobot, FaBalanceScale, FaCar, FaArrowRight } from 'react-icons/fa';
import VehicleGrid from '../components/vehicle/VehicleGrid';
import { MOCK_VEHICLES } from '../utils/mockVehicles';
import './HomePage.css';

const HomePage = () => {
  // Lấy 4 xe đầu tiên làm xe nổi bật
  const featuredVehicles = MOCK_VEHICLES.slice(0, 4);

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <span className="hero-badge">Hệ thống Thông minh Hỗ trợ Ra quyết định</span>
          <h1 className="hero-title">
            Tìm mua xe ô tô cũ với <span>Giá thị trường minh bạch</span>
          </h1>
          <p className="hero-description">
            Ứng dụng công nghệ dữ liệu thực tế và mô hình định giá hồi quy để hỗ trợ người mua xe đánh giá mức độ hợp lý của giá bán, gợi ý những mẫu xe tối ưu ngân sách.
          </p>
          <div className="hero-actions">
            <Link to="/vehicles" className="btn btn-primary btn-lg">
              <FaSearch /> Khám phá danh sách xe ({MOCK_VEHICLES.length} xe)
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Highlights */}
      <section className="features-section">
        <div className="feature-item">
          <div className="feature-icon-box blue">
            <FaSearch />
          </div>
          <h3>Dữ liệu Thực tế</h3>
          <p>Thu thập và làm sạch liên tục từ các sàn mua bán xe uy tín tại Việt Nam.</p>
        </div>

        <div className="feature-item">
          <div className="feature-icon-box amber">
            <FaRobot />
          </div>
          <h3>Định giá AI / R Model</h3>
          <p>Mô hình hồi quy dự đoán giá thị trường chính xác theo tuổi xe, số km, dòng xe.</p>
        </div>

        <div className="feature-item">
          <div className="feature-icon-box green">
            <FaBalanceScale />
          </div>
          <h3>Gợi ý & So sánh</h3>
          <p>Thuật toán tính điểm thông minh xếp hạng các xe đáng mua nhất theo ngân sách.</p>
        </div>
      </section>

      {/* Featured Vehicles Section */}
      <section className="featured-section">
        <div className="section-header">
          <div>
            <h2 className="section-title">Xe nổi bật trên thị trường</h2>
            <p className="section-subtitle">Các mẫu xe đang được quan tâm nhiều nhất</p>
          </div>
          <Link to="/vehicles" className="view-all-link">
            Xem tất cả <FaArrowRight />
          </Link>
        </div>

        <VehicleGrid vehicles={featuredVehicles} />
      </section>
    </div>
  );
};

export default HomePage;
