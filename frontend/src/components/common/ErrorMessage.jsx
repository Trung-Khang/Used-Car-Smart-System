import React from 'react';
import { FaExclamationTriangle, FaRedo } from 'react-icons/fa';
import './ErrorMessage.css';

const ErrorMessage = ({
  message = 'Đã có lỗi xảy ra khi tải dữ liệu.',
  onRetry = null,
}) => {
  return (
    <div className="error-card">
      <div className="error-icon-wrapper">
        <FaExclamationTriangle className="error-icon" />
      </div>
      <div className="error-content">
        <h3 className="error-title">Thông báo lỗi</h3>
        <p className="error-message">{message}</p>
      </div>
      {onRetry && (
        <button onClick={onRetry} className="btn btn-primary error-retry-btn">
          <FaRedo /> Thử lại
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;

