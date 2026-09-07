import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { FaCar, FaBars, FaTimes } from 'react-icons/fa';
import './Navbar.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  return (
    <header className="navbar-header">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo" onClick={closeMenu}>
          <div className="logo-icon-wrapper">
            <FaCar className="logo-icon" />
          </div>
          <div className="logo-text">
            <span className="logo-title">SmartCar</span>
            <span className="logo-subtitle">Decision Support</span>
          </div>
        </Link>

        {/* Mobile toggle button */}
        <button
          className="navbar-toggle"
          onClick={toggleMenu}
          aria-label="Toggle navigation"
        >
          {isOpen ? <FaTimes /> : <FaBars />}
        </button>

        {/* Navigation links */}
        <nav className={`navbar-nav ${isOpen ? 'open' : ''}`}>
          <NavLink
            to="/"
            end
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            onClick={closeMenu}
          >
            Trang chủ
          </NavLink>
          <NavLink
            to="/vehicles"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            onClick={closeMenu}
          >
            Danh sách xe
          </NavLink>
          <div className="nav-item-disabled" title="Khả dụng từ Increment 3">
            <span className="nav-link disabled">
              Định giá tự động
              <span className="nav-badge">Inc 3</span>
            </span>
          </div>
          <div className="nav-item-disabled" title="Khả dụng từ Increment 4">
            <span className="nav-link disabled">
              Gợi ý & So sánh
              <span className="nav-badge">Inc 4</span>
            </span>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
