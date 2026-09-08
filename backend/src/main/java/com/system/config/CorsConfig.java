package com.system.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * ===================================================================
 * CẤU HÌNH CORS (CROSS-ORIGIN RESOURCE SHARING)
 * ===================================================================
 * 
 * TẠI SAO CẦN FILE NÀY?
 * - Frontend của bạn TV2 chạy ở cổng 5173 (React/Vite) hoặc 3000.
 * - Backend của bạn (TV1) chạy ở cổng 8080.
 * - Trình duyệt mặc định sẽ CHẶN nếu 2 cổng khác nhau gọi nhau (lỗi CORS).
 * - File này giúp "mở cửa" cho phép Frontend gọi vào Backend mà không bị lỗi.
 */
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // Cho phép tất cả các đường dẫn API
                .allowedOrigins(
                    "http://localhost:3000",
                    "http://localhost:5173",
                    "http://localhost:8080"
                ) // Các cổng Frontend được phép gọi vào
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS") // Các phương thức HTTP được phép
                .allowedHeaders("*") // Chấp nhận mọi loại Header
                .allowCredentials(true);
    }
}
