import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div className="footer-left">
          <span className="footer-dot">●</span>
          <span className="footer-brand">SmartCar</span>
          <span className="footer-ext">.ai</span>
        </div>
        <div className="footer-right">
          <p>Đồ án môn Công nghệ phần mềm — Hệ thống Gợi ý & Định giá Xe hơi Cũ Thông minh</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
