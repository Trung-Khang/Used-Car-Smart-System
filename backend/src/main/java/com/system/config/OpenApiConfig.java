package com.system.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * ===================================================================
 * CẤU HÌNH THÔNG TIN CHO TRANG SWAGGER / OPENAPI UI
 * ===================================================================
 * 
 * - Giúp trang Swagger hiển thị tiêu đề, mô tả và thông tin nhóm đồ án
 *   chuyên nghiệp khi giảng viên hoặc bạn TV2 vào xem.
 */
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Smart Used-Car Decision Support System API")
                        .description("RESTful API Documentation cho Do an He thong Ho tro Dinh gia & Goi y Xe cu - HCMUTE")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("Used-Car Team - Member 01 (Backend Lead)")
                        )
                );
    }
}
