import React from 'react';
import './Loading.css';

const Loading = ({ message = 'Đang tải dữ liệu...' }) => {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p className="loading-text">{message}</p>
    </div>
  );
};

export default Loading;

