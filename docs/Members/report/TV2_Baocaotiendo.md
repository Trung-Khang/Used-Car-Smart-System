# BÁO CÁO TIẾN ĐỘ THÀNH VIÊN 02 (TV2) — FRONTEND DEVELOPER

---

## INCREMENT 1 — FOUNDATION

### Báo cáo Task 1: Khởi tạo React + Vite Project

- **Việc đã hoàn thành:**
  - Khởi tạo thành công project React + Vite trong thư mục `frontend/`.
  - Cài đặt đầy đủ các dependencies cốt lõi: `axios`, `react-router-dom`, `react-icons`, `@vitejs/plugin-react`.
  - Cấu hình file `vite.config.js` có sẵn proxy chuyển tiếp request `/api` về Backend Spring Boot (`http://localhost:8080`).
  - Tạo template `index.html`, entry point `src/main.jsx`, `src/App.jsx`.
  - Tạo file cấu hình môi trường `.env.example` chứa biến `VITE_API_BASE_URL=http://localhost:8080/api/v1` và tạo `.env` local.
  - Test build production (`npm run build`) thành công 100%.

- **Sinh ra file/module gì:**
  - `frontend/package.json` & `frontend/package-lock.json`
  - `frontend/vite.config.js`
  - `frontend/index.html`
  - `frontend/.env.example`
  - `frontend/src/main.jsx`
  - `frontend/src/App.jsx`

- **Để làm gì:**
  - Làm nền tảng ứng dụng Frontend SPA (Single Page Application) cho toàn bộ hệ thống Used-Car Smart Decision Support System.
  - Sẵn sàng tích hợp Router, Service API và các UI component ở các task tiếp theo.

- **Bàn giao lại cho ai:**
  - TV2 tiếp tục thực hiện Task 2 (Setup cấu trúc thư mục).
  - Toàn team (đặc biệt TV1 Backend) nắm được cấu hình API base URL và proxy dev server.

- **Còn thiếu hay cần bổ sung gì:**
  - Chưa tổ chức đầy đủ cấu trúc thư mục phân lớp bên trong `src/` (Sẽ làm ở Task 2).
  - Chưa có layout dùng chung (Navbar, Footer...) và các trang (Sẽ làm ở Task 3 & 4).

- **Cách thức và thao tác Run/Debug hoặc test thử:**
  - Di chuyển vào thư mục frontend: `cd frontend`
  - Cài dependencies (nếu clone mới): `npm install`
  - Khởi chạy dev server: `npm run dev` (mặc định tại port `http://localhost:5173`)
  - Kiểm tra build: `npm run build`

- **Chú ý/ Ghi chú:**
  - File `.env` chứa cấu hình local đã được đưa vào `.gitignore` để bảo mật, chỉ commit file `.env.example`.

---

### Báo cáo Task 2: Cấu trúc thư mục dự án

- **Việc đã hoàn thành:**
  - Chuẩn hóa toàn bộ kiến trúc thư mục nguồn theo tiêu chuẩn module React bên trong `frontend/src/`.
  - Di chuyển và tổ chức các thư mục phân lớp (`pages`, `services`, `hooks`, `context`, `utils`, `styles`) vào trong `frontend/src/`.
  - Thiết lập đầy đủ các phân khu component chuyên biệt:
    - `components/common/`: components dùng chung cho toàn ứng dụng.
    - `components/vehicle/`: components hiển thị thẻ xe, lưới xe, chi tiết xe (Inc 1).
    - `components/filter/`: bộ lọc tìm kiếm (Inc 2).
    - `components/valuation/`: form và kết quả định giá tự động (Inc 3).
    - `components/recommendation/`: danh sách và thẻ xe đề xuất (Inc 4).
    - `components/comparison/`: bảng và biểu đồ so sánh xe (Inc 4).
  - Loại bỏ các file rác và boilerplate mặc định.

- **Sinh ra file/module gì:**
  - Cấu trúc cây thư mục chuẩn trong `frontend/src/`:
    ```
    frontend/src/
    ├── assets/
    │   ├── icons/
    │   └── images/
    ├── components/
    │   ├── common/
    │   ├── vehicle/
    │   ├── filter/
    │   ├── valuation/
    │   ├── recommendation/
    │   └── comparison/
    ├── context/
    ├── hooks/
    ├── pages/
    ├── services/
    ├── styles/
    ├── utils/
    ├── App.jsx
    └── main.jsx
    ```

- **Để làm gì:**
  - Giúp dự án có cấu trúc rõ ràng, dễ mở rộng và tuân thủ nguyên tắc separation of concerns.
  - Sẵn sàng triển khai các components layout (Navbar, Footer, Loading...) ở Task 3 và Vehicle UI ở Task 4.

- **Bàn giao lại cho ai:**
  - TV2 tiếp tục thực hiện Task 3 (Layout chung: Navbar, Footer, Loading, ErrorMessage, Router).

- **Còn thiếu hay cần bổ sung gì:**
  - Chưa triển khai code các component cụ thể trong `components/common` và routing trong `App.jsx` (Sẽ làm ở Task 3).

- **Cách thức và thao tác Run/Debug hoặc test thử:**
  - Kiểm tra cây thư mục: `Get-ChildItem -Recurse frontend/src`
  - Build thử nghiệm: `cd frontend; npm run build`

- **Chú ý/ Ghi chú:**
  - Các thư mục dành cho Increment 2, 3, 4 đã được tạo sẵn file `.gitkeep` để duy trì track trên Git.
