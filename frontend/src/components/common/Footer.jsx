import React from 'react';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer-container">
      <div className="footer-content">
        <div className="footer-brand">
          <h3>Used-Car Smart Decision Support System</h3>
          <p>
            Hệ thống thông minh hỗ trợ ra quyết định mua xe ô tô đã qua sử dụng, tích hợp mô hình định giá hồi quy và thuật toán gợi ý đa tiêu chí.
          </p>
        </div>

        <div className="footer-info">
          <div className="footer-col">
            <h4>Đồ án Chuyên ngành</h4>
            <p>Công nghệ Phần mềm (CNPM)</p>
            <p>Trường Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)</p>
          </div>

          <div className="footer-col">
            <h4>Nhóm phát triển</h4>
            <p>TV1: Spring Boot Core Backend</p>
            <p>TV2: ReactJS Frontend & UI/UX</p>
            <p>TV3: Python Crawler Pipeline</p>
            <p>TV4: Machine Learning & Plumber API</p>
            <p>TV5: PostgreSQL & Testing Lead</p>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <p>© {currentYear} Used-Car Smart Decision Support System. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
