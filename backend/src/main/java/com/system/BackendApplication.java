package com.system;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * ===================================================================
 * FILE KHỞI CHẠY CHÍNH CỦA ỨNG DỤNG BACKEND (SPRING BOOT)
 * ===================================================================
 * 
 * - @SpringBootApplication: Annotation quan trọng nhất của Spring Boot,
 *   tự động kích hoạt 3 tính năng:
 *   1. @Configuration: Đánh dấu class này chứa cấu hình của ứng dụng.
 *   2. @EnableAutoConfiguration: Tự động cấu hình các thư viện (JPA, Web, Swagger...).
 *   3. @ComponentScan: Tự động tìm kiếm và nhận diện các class Controller,
 *      Service, Repository trong package "com.system".
 */
@SpringBootApplication
public class BackendApplication {

    public static void main(String[] args) {
        // Khởi động toàn bộ hệ thống Spring Boot
        SpringApplication.run(BackendApplication.class, args);
        System.out.println("=================================================");
        System.out.println(" Used-Car-Smart-System Backend dang chay tai:   ");
        System.out.println(" -> API Server:  http://localhost:8080          ");
        System.out.println(" -> Swagger UI:  http://localhost:8080/swagger-ui.html ");
        System.out.println("=================================================");
    }

}
