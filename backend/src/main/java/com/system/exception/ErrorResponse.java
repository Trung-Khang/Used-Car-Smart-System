package com.system.exception;

import java.time.LocalDateTime;

/**
 * ===================================================================
 * ĐỐI TƯỢNG PHẢN HỒI LỖI CHUẨN (ERROR RESPONSE DTO)
 * ===================================================================
 * 
 * Giúp trả về cấu trúc lỗi JSON đồng nhất và sạch sẽ cho Frontend (TV2),
 * tránh làm lộ raw stack trace hay lỗi dài dòng của server.
 */
public class ErrorResponse {

    private int status;             // Mã lỗi HTTP (Ví dụ: 404, 400, 500)
    private String error;           // Tên loại lỗi (Ví dụ: Not Found, Bad Request)
    private String message;         // Thông báo lỗi chi tiết dễ hiểu
    private String path;            // Đường dẫn API bị lỗi
    private LocalDateTime timestamp;// Thời điểm xảy ra lỗi

    public ErrorResponse() {
        this.timestamp = LocalDateTime.now();
    }

    public ErrorResponse(int status, String error, String message, String path) {
        this.status = status;
        this.error = error;
        this.message = message;
        this.path = path;
        this.timestamp = LocalDateTime.now();
    }

    // Getters and Setters
    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
}
