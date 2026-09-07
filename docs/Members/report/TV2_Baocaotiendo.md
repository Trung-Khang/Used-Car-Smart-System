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
