import apiClient from './api';
import { MOCK_VEHICLES } from '../utils/mockVehicles';

/**
 * Service giao tiếp với Vehicle REST API của Spring Boot Backend (TV1).
 * Khi Backend chưa sẵn sàng, service tự động fallback về Mock Data để UI hoạt động thông suốt.
 */
export const vehicleApi = {
  /**
   * Lấy danh sách xe (hỗ trợ phân trang, tìm kiếm, lọc)
   * @param {Object} params - Query parameters (page, size, brand, model...)
   * @returns {Promise<Array>} Danh sách xe
   */
  getVehicles: async (params = {}) => {
    try {
      // TODO: Khi TV1 Backend hoàn tất endpoint GET /vehicles, kết quả sẽ trả về từ API
      const data = await apiClient.get('/vehicles', { params });
      // Xử lý dữ liệu trả về: có thể là mảng trực tiếp hoặc đối tượng phân trang { content: [...] }
      if (Array.isArray(data)) {
        return data;
      }
      if (data && Array.isArray(data.content)) {
        return data.content;
      }
      return data;
    } catch (error) {
      console.warn('Backend API chưa sẵn sàng hoặc kết nối lỗi. Đang sử dụng Mock Data cho Increment 1.', error.message);
      // Giả lập độ trễ mạng nhỏ (300ms) để trải nghiệm loading chân thực
      await new Promise((resolve) => setTimeout(resolve, 300));
      return MOCK_VEHICLES;
    }
  },

  /**
   * Lấy thông tin chi tiết một chiếc xe theo ID
   * @param {string|number} id - Mã định danh xe
   * @returns {Promise<Object>} Thông tin chi tiết xe
   */
  getVehicleById: async (id) => {
    try {
      // TODO: Khi TV1 Backend hoàn tất endpoint GET /vehicles/{id}
      const data = await apiClient.get(`/vehicles/${id}`);
      return data;
    } catch (error) {
      console.warn(`Backend API chưa sẵn sàng hoặc không tìm thấy xe #${id}. Đang fallback sang Mock Data.`, error.message);
      await new Promise((resolve) => setTimeout(resolve, 200));
      const found = MOCK_VEHICLES.find((v) => String(v.id) === String(id));
      if (!found) {
        throw new Error(`Không tìm thấy xe với ID #${id}`);
      }
      return found;
    }
  },
};

export default vehicleApi;
