import axios from 'axios';

// Lấy API base URL từ biến môi trường Vite (.env)
// Fallback mặc định là http://localhost:8080/api/v1 (Spring Boot Backend TV1)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Request Interceptor: đính kèm header hoặc logging nếu cần
apiClient.interceptors.request.use(
  (config) => {
    // Có thể bổ sung Authorization token tại đây trong tương lai nếu có
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: chuẩn hóa cấu trúc lỗi từ Spring Boot Backend
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    let errorMessage = 'Không thể kết nối đến máy chủ. Vui lòng kiểm tra lại đường truyền.';

    if (error.response) {
      // Backend phản hồi với mã trạng thái lỗi (4xx, 5xx)
      const data = error.response.data;
      if (typeof data === 'string') {
        errorMessage = data;
      } else if (data && data.message) {
        errorMessage = data.message;
      } else if (error.response.status === 404) {
        errorMessage = 'Không tìm thấy dữ liệu yêu cầu.';
      } else if (error.response.status === 500) {
        errorMessage = 'Lỗi nội bộ từ máy chủ Backend. Vui lòng thử lại sau.';
      }
    } else if (error.request) {
      // Đã gửi request nhưng không nhận được phản hồi (Backend chưa bật hoặc CORS)
      errorMessage = 'Không nhận được phản hồi từ Backend (Spring Boot chưa khởi động hoặc lỗi mạng).';
    }

    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;
