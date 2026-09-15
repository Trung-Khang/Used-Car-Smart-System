/**
 * Định dạng giá tiền VND
 * @param {number} price Giá tiền tính theo VND
 * @returns {string} Chuỗi hiển thị (ví dụ: "750 triệu" hoặc "750,000,000 ₫")
 */
export const formatPrice = (price) => {
  if (price === null || price === undefined || isNaN(price)) {
    return 'Liên hệ';
  }

  // Nếu trên 1 tỷ đồng
  if (price >= 1000000000) {
    const ty = price / 1000000000;
    return `${ty.toLocaleString('vi-VN', { maximumFractionDigits: 2 })} tỷ`;
  }

  // Nếu trên 1 triệu đồng
  if (price >= 1000000) {
    const trieu = price / 1000000;
    return `${trieu.toLocaleString('vi-VN', { maximumFractionDigits: 1 })} triệu`;
  }

  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
  }).format(price);
};

/**
 * Định dạng giá tiền đầy đủ có ký hiệu ₫
 * @param {number} price
 * @returns {string} Ví dụ: "750,000,000 ₫"
 */
export const formatFullPrice = (price) => {
  if (price === null || price === undefined || isNaN(price)) {
    return 'Liên hệ';
  }
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
  }).format(price);
};

/**
 * Định dạng số km đã đi (Mileage / ODO)
 * @param {number} km Số km
 * @returns {string} Ví dụ: "45,000 km"
 */
export const formatMileage = (km) => {
  if (km === null || km === undefined || isNaN(km)) {
    return 'Chưa xác định';
  }
  return `${Number(km).toLocaleString('vi-VN')} km`;
};

/**
 * Định dạng năm sản xuất
 * @param {number} year Năm
 * @returns {string}
 */
export const formatYear = (year) => {
  if (!year) return 'Chưa xác định';
  return `${year}`;
};

