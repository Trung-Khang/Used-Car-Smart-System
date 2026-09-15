package com.system.exception;

/**
 * ===================================================================
 * NGOẠI LỆ TỰ ĐỊNH NGHĨA: KHÔNG TÌM THẤY DỮ LIỆU (NOT FOUND)
 * ===================================================================
 * 
 * Ném ra khi người dùng tìm kiếm một chiếc xe hoặc tin đăng theo ID
 * nhưng không tồn tại trong Database.
 */
public class ResourceNotFoundException extends RuntimeException {

    public ResourceNotFoundException(String message) {
        super(message);
    }
}
