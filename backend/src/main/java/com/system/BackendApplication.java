package com.system;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class BackendApplication {

    public static void main(String[] args) {
        // Khởi động toàn bộ hệ thống Spring Boot
        SpringApplication.run(BackendApplication.class, args);
        System.out.println("Used-Car-Smart-System Backend dang chay tai: ");
        System.out.println("-> API Server: http://localhost:8080");
        System.out.println("-> Swagger UI: http://localhost:8080/swagger-ui.html");
    }

}
