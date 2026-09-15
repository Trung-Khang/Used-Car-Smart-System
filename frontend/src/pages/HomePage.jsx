import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import VehicleGrid from '../components/vehicle/VehicleGrid';
import { MOCK_VEHICLES } from '../utils/mockVehicles';
import './HomePage.css';

const HomePage = () => {
  // Lấy 3 xe đầu tiên hiển thị dạng gợi ý tiêu biểu giống hình mẫu
  const topVehicles = MOCK_VEHICLES.slice(0, 3);

  // Form ước tính nhanh ở Hero
  const [quickBrand, setQuickBrand] = useState('Toyota');
  const [quickModel, setQuickModel] = useState('Vios 1.5G');
  const [quickYear, setQuickYear] = useState('2020');
  const [quickKm, setQuickKm] = useState('45.000 km');
  const [isCalculated, setIsCalculated] = useState(true);

  const handleQuickEstimate = (e) => {
    e.preventDefault();
    setIsCalculated(true);
  };

  return (
    <div className="homepage-wrapper">
      {/* 1. HERO SECTION (Dark Navy) */}
      <section className="hero-dark-section">
        <div className="hero-inner">
          <div className="hero-left-column">
            <h1 className="hero-headline">
              Biết giá thật của một chiếc xe cũ, trước khi bạn đặt cọc.
            </h1>
            <p className="hero-lead">
              SmartCar.ai đối chiếu đặc điểm xe của bạn với hàng trăm nghìn tin đăng và giao dịch thực tế đang diễn ra trên thị trường, để đưa ra một mức giá có căn cứ — không phải cảm tính người bán.
            </p>

            <div className="hero-cta-group">
              <Link to="/vehicles" className="btn btn-gold">
                Định giá xe của tôi
              </Link>
              <Link to="/vehicles" className="btn btn-outline-white">
                Xem xe được gợi ý
              </Link>
            </div>

            <p className="hero-footnote">
              Mô hình học từ dữ liệu thị trường cập nhật liên tục, không phải bảng giá cố định theo năm sản xuất.
            </p>
          </div>

          {/* Khung ước tính nhanh bên phải */}
          <div className="hero-right-column">
            <div className="quick-estimate-card">
              <h3 className="estimate-card-title">ƯỚC TÍNH NHANH</h3>
              
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
                    <label>Số km đã đi</label>
                    <input
                      type="text"
                      value={quickKm}
                      onChange={(e) => setQuickKm(e.target.value)}
                    />
                  </div>
                </div>

                <button type="submit" className="btn-estimate-submit">
                  Ước tính giá trị
                </button>
              </form>

              {isCalculated && (
                <div className="estimate-result-box">
                  <div className="estimate-price-range">465 – 495 triệu đ</div>
                  <div className="estimate-meta-text">
                    Dựa trên 342 tin đăng & 58 giao dịch tương đồng trong 30 ngày
                  </div>
                  <div className="confidence-bar-wrapper">
                    <div className="confidence-label">
                      <span>Độ tin cậy mô hình</span>
                      <span className="confidence-val">92%</span>
                    </div>
                    <div className="progress-track">
                      <div className="progress-fill" style={{ width: '92%' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* 2. STATS KPI BAR (Dark Navy strip) */}
      <section className="stats-kpi-bar">
        <div className="stats-inner">
          <div className="stat-item">
            <span className="stat-number">128.450</span>
            <span className="stat-desc">tin đăng đang được theo dõi</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">15 phút</span>
            <span className="stat-desc">tần suất cập nhật dữ liệu</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">4,2%</span>
            <span className="stat-desc">sai số trung bình (MAPE)</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">3.200+</span>
            <span className="stat-desc">giao dịch thực tế mỗi tháng</span>
          </div>
        </div>
      </section>

      {/* 3. SECTION GỢI Ý CHO BẠN (Warm beige background) */}
      <section className="recommendation-showcase-section">
        <div className="section-content-limit">
          <div className="showcase-header">
            <span className="gold-subheading">Gợi ý cho bạn</span>
            <h2 className="showcase-title">
              Xe phù hợp, xếp hạng theo mức độ hời so với thị trường
            </h2>
            <p className="showcase-desc">
              Mỗi xe được gắn nhãn dựa trên khoảng cách giữa giá rao bán và giá mô hình dự đoán cho cùng cấu hình.
            </p>
          </div>

          <VehicleGrid vehicles={topVehicles} />

          <div className="showcase-bottom-action">
            <Link to="/vehicles" className="btn btn-secondary">
              Xem tất cả danh sách xe ({MOCK_VEHICLES.length} xe)
            </Link>
          </div>
        </div>
      </section>

      {/* 4. SECTION VỀ MÔ HÌNH (4 Bước xử lý) */}
      <section className="model-process-section">
        <div className="section-content-limit">
          <div className="showcase-header">
            <span className="gold-subheading">Về mô hình</span>
            <h2 className="showcase-title">
              Từ dữ liệu rao vặt đến một con số bạn có thể tin
            </h2>
            <p className="showcase-desc">
              Bốn bước xử lý biến hàng trăm nghìn tin đăng rời rạc thành một mức giá và một khuyến nghị cụ thể.
            </p>
          </div>

          <div className="process-steps-grid">
            <div className="step-card">
              <span className="step-index">01</span>
              <h4>Thu thập dữ liệu</h4>
              <p>Đồng bộ tin đăng và tin đã bán từ nhiều sàn giao dịch xe cũ theo thời gian gần thực.</p>
            </div>

            <div className="step-card">
              <span className="step-index">02</span>
              <h4>Làm sạch & chuẩn hóa</h4>
              <p>Loại bỏ tin trùng lặp, chuẩn hóa tên hãng, phiên bản và các thông số kỹ thuật.</p>
            </div>

            <div className="step-card">
              <span className="step-index">03</span>
              <h4>Mô hình định giá</h4>
              <p>Gradient Boosting / Hồi quy đa biến học mối quan hệ giữa đặc trưng xe, khu vực và giá giao dịch.</p>
            </div>

            <div className="step-card">
              <span className="step-index">04</span>
              <h4>Gợi ý & độ tin cậy</h4>
              <p>Xếp hạng xe phù hợp với ngân sách, kèm khoảng giá và mức độ tin cậy của dự đoán.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
