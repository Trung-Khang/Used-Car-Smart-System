import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import VehicleGrid from '../components/vehicle/VehicleGrid';
import { MOCK_VEHICLES } from '../utils/mockVehicles';
import './HomePage.css';

const HomePage = () => {
  // Lấy 3 xe làm mẫu tiêu biểu cho phần gợi ý
  const topVehicles = MOCK_VEHICLES.slice(0, 3);

  // Form ước tính nhanh ở Hero
  const [quickBrand, setQuickBrand] = useState('Toyota');
  const [quickModel, setQuickModel] = useState('Vios 1.5G');
  const [quickYear, setQuickYear] = useState('2021');
  const [quickKm, setQuickKm] = useState('38.000 km');
  const [isCalculated, setIsCalculated] = useState(true);

  const handleQuickEstimate = (e) => {
    e.preventDefault();
    setIsCalculated(true);
  };

  return (
    <div className="homepage-wrapper">
      {/* 1. HERO SECTION */}
      <section className="hero-dark-section">
        <div className="hero-inner">
          <div className="hero-left-column">
            <span className="hero-kicker">Hệ Thống Hỗ Trợ Ra Quyết Định Thông Minh</span>
            <h1 className="hero-headline">
              Định giá minh bạch & gợi ý xe ô tô cũ tối ưu ngân sách
            </h1>
            <p className="hero-lead">
              Hệ thống thu thập dữ liệu thị trường thực tế, ứng dụng mô hình hồi quy để ước lượng giá trị thật của xe và thuật toán xếp hạng đa tiêu chí, giúp người mua đưa ra quyết định chính xác và tự tin trước khi giao dịch.
            </p>

            <div className="hero-cta-group">
              <Link to="/vehicles" className="btn btn-gold">
                Khám phá danh sách xe
              </Link>
              <a href="#recommendations" className="btn btn-outline-white">
                Xem xe gợi ý theo mức giá
              </a>
            </div>

            <p className="hero-footnote">
              Đồ án kết hợp Data Pipeline (Python), Mô hình Định giá Hồi quy (R Plumber), Core Backend (Spring Boot) và Giao diện (ReactJS).
            </p>
          </div>

          {/* Khung mô phỏng ước tính giá nhanh */}
          <div className="hero-right-column">
            <div className="quick-estimate-card">
              <h3 className="estimate-card-title">MÔ PHỎNG ĐỊNH GIÁ NHANH</h3>
              
              <form onSubmit={handleQuickEstimate} className="estimate-form">
                <div className="form-row-2">
                  <div className="form-group">
                    <label>Hãng xe</label>
                    <select
                      value={quickBrand}
                      onChange={(e) => setQuickBrand(e.target.value)}
                    >
                      <option value="Toyota">Toyota</option>
                      <option value="Mazda">Mazda</option>
                      <option value="Honda">Honda</option>
                      <option value="Hyundai">Hyundai</option>
                      <option value="Kia">Kia</option>
                      <option value="Ford">Ford</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Dòng xe</label>
                    <select
                      value={quickModel}
                      onChange={(e) => setQuickModel(e.target.value)}
                    >
                      <option value="Vios 1.5G">Vios 1.5G</option>
                      <option value="Mazda 3 1.5L">Mazda 3 1.5L</option>
                      <option value="CR-V 1.5L">CR-V 1.5L</option>
                      <option value="Accent 1.4 AT">Accent 1.4 AT</option>
                      <option value="Seltos 1.4 Turbo">Seltos 1.4 Turbo</option>
                    </select>
                  </div>
                </div>

                <div className="form-row-2">
                  <div className="form-group">
                    <label>Năm sản xuất</label>
                    <input
                      type="text"
                      value={quickYear}
                      onChange={(e) => setQuickYear(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label>Số km đã đi (ODO)</label>
                    <input
                      type="text"
                      value={quickKm}
                      onChange={(e) => setQuickKm(e.target.value)}
                    />
                  </div>
                </div>

                <button type="submit" className="btn-estimate-submit">
                  Ước tính giá thị trường
                </button>
              </form>

              {isCalculated && (
                <div className="estimate-result-box">
                  <div className="estimate-price-range">470 – 495 triệu ₫</div>
                  <div className="estimate-meta-text">
                    Giá dự đoán từ mô hình hồi quy đa biến dựa trên dữ liệu giao dịch cùng phân khúc
                  </div>
                  <div className="confidence-bar-wrapper">
                    <div className="confidence-label">
                      <span>Độ phù hợp dữ liệu thị trường</span>
                      <span className="confidence-val">94%</span>
                    </div>
                    <div className="progress-track">
                      <div className="progress-fill" style={{ width: '94%' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* 2. STATS KPI BAR */}
      <section className="stats-kpi-bar">
        <div className="stats-inner">
          <div className="stat-item">
            <span className="stat-number">2.000+</span>
            <span className="stat-desc">dữ liệu xe thị trường thực tế</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">R Plumber</span>
            <span className="stat-desc">mô hình định giá hồi quy tự động</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">5 Tiêu chí</span>
            <span className="stat-desc">thuật toán chấm điểm gợi ý xe</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">Smart Tag</span>
            <span className="stat-desc">đánh giá giá tốt / hợp lý / giá cao</span>
          </div>
        </div>
      </section>

      {/* 3. SECTION GỢI Ý CHO BẠN */}
      <section id="recommendations" className="recommendation-showcase-section">
        <div className="section-content-limit">
          <div className="showcase-header">
            <span className="gold-subheading">Hỗ trợ ra quyết định</span>
            <h2 className="showcase-title">
              Danh sách xe tiêu biểu & Đánh giá mức độ hợp lý của giá bán
            </h2>
            <p className="showcase-desc">
              Mỗi xe được so sánh giữa giá rao bán thực tế và mức giá ước lượng từ mô hình định giá, giúp người mua nhận biết ngay những xe có giá tốt trên thị trường.
            </p>
          </div>

          <VehicleGrid vehicles={topVehicles} />

          <div className="showcase-bottom-action">
            <Link to="/vehicles" className="btn btn-secondary">
              Xem toàn bộ danh sách xe ({MOCK_VEHICLES.length} xe)
            </Link>
          </div>
        </div>
      </section>

      {/* 4. SECTION QUY TRÌNH HỆ THỐNG */}
      <section className="model-process-section">
        <div className="section-content-limit">
          <div className="showcase-header">
            <span className="gold-subheading">Kiến trúc hệ thống</span>
            <h2 className="showcase-title">
              Quy trình xử lý dữ liệu và hỗ trợ ra quyết định
            </h2>
            <p className="showcase-desc">
              Hệ thống liên kết chặt chẽ qua 4 công đoạn chính giữa các thành viên để đưa ra kết quả phân tích đáng tin cậy.
            </p>
          </div>

          <div className="process-steps-grid">
            <div className="step-card">
              <span className="step-index">01</span>
              <h4>Thu thập dữ liệu (TV3)</h4>
              <p>Pipeline Python thu thập tin rao bán xe ô tô cũ thực tế từ các nguồn sàn trực tuyến.</p>
            </div>

            <div className="step-card">
              <span className="step-index">02</span>
              <h4>Làm sạch & Chuẩn hóa (TV3, TV5)</h4>
              <p>Lọc trùng lặp, chuẩn hóa giá VND, số km ODO, năm sản xuất và lưu trữ vào PostgreSQL Database.</p>
            </div>

            <div className="step-card">
              <span className="step-index">03</span>
              <h4>Mô hình định giá (TV4)</h4>
              <p>Mô hình hồi quy trong R được đóng gói qua Plumber API để dự đoán mức giá hợp lý theo thông số xe.</p>
            </div>

            <div className="step-card">
              <span className="step-index">04</span>
              <h4>Gợi ý & Quyết định (TV1, TV2, TV5)</h4>
              <p>Spring Boot tính điểm xếp hạng xe theo ngân sách và ReactJS hiển thị so sánh trực quan cho người dùng.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
