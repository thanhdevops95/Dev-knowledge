# ☕ Spring Boot Basics — "Bố Già" Ngành Enterprise Backend

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững Java căn bản, Lập trình Hướng đối tượng OOP Máy `04-Clean-Code-Architecture/01-oop-solid-fundamentals.md`, và API Design).
> Nếu Thung Lũng Silicon đẻ ra Node.js cho Startup Mới Nổi, thì Spring Boot của Java là "Ngân Hàng Trung Ương" của thế giới Lập Trình. Cứ 10 hệ thống Thanh toán Quốc tế, Viễn thông, hay Core Banking (Ngân hàng) thì có tới 9 hệ thống đang chạy Mạch ngầm bằng Spring Boot. Nó quá lớn, quá ổn định, và bảo trì hoàn hảo 20 năm tuổi.

---

## Tại sao (WHY) phải Đổi Đời Ôm Khối Code Nặng Của Java Spring Boot Nhỉ?

Java từng là "Ác Mộng Quản Lý". Để gọi cái chữ "Hello World" lên trình duyệt, vào những năm trước 2013, Coder Java phải viết Kéo 200 dòng XML cấu hình Server Tomcat, nạp Dependency dài ngoằng, nhồi File Tên `web.xml` Chặt Gãy Tay Khổ Oanh Lạc!

**SPRING BOOT XUẤT HIỆN LÀ ĐẤNG CỨU THẾ (Nguyên Tắc: Convention over Configuration).** 
Bạn chỉ cần đúng 1 nút Chạy `Run()`: Spring Sẽ Tự Ngầm Nhúng Server Tomcat Thẳng Vào Ruột Của Nó Ngay Tóc Tự Động Ráp Kì Code. Không Có XML. Tất cả Chuyển Sang Lệnh Bùa Chú **Annotations (Đứa Bắt Định Tuyến Tự Ráp - Ví Dụ `@SpringBootApplication`)!**

**Vấn đề giải quyết:** System Microservices Siêu To, Xử Lí Đa Luồng Gấp Trăm Thread Này Mạnh Nhất Chấp Node Oanh Khúc. Ổn Định Trọn Đời Rác Không Quên DB. 

---

## 1. Bản Đồ Mạch Thép API Khối Dịch (Controller Trong 3 Nốt Nhạc)

Cú Đánh Sát Cụ REST API Nhìn Không Kì Rách Dòng Của Giao Thép Java Báo Trút Oanh Web:

```java
package com.vd_oanh.demo.api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

// 1. Phép Gắn Bùa Chú (@RestController): 
// Biến cái Class bình thường này Thành 1 Cục Router Báo JSON Để Giao Tiếp Web Tích Òa Oách Sạch 10 Node Tỉnh Nhất!
@RestController 
public class ChuyenXeController {

  public String vucXeGiang = "Máy Chạy Lắp Vui API Gọi Java!";

  // 2. Định Nghĩa Rạch Mạch Dịch Đo Báo Đường Dẫn Router Nhồi (@GetMapping)
  @GetMapping("/api/chuyen-xe") 
  public String thongBaoGiaoXe() {
      // Spring Boot sẽ Hút Xé Kiểu Chuỗi Text Này Xong BIẾN Cụ Đảo Tự Vọng Sang JSON Trả Khách Hàng Nhanh Khớp
      return "Hello Đo Bạn Ráp Cõi Java: " + vucXeGiang; 
  }
}
```

---

## 2. Tiêm Rạch Ma Thuật: @Autowired (Dependency Injection Thần Khốc)

Quay về Khái niệm Di (`03-dependency-injection-patterns.md`). Spring Boot LÀ KIẾN TRÚC SƯ CỦA IoC CONTAINER:

```java
// Đứa Làm Cu Li DB Database (Nhớ Gắn Bùa Này Mới Tồn Tại Trong Container @Service!)
@Service 
public class GiaoXeService {
  public String layDataGiao() { return "Nhanh Chạy Từ Database Giao Java Thép!"; }
}
```

Sang Ráp API Nhồi Nhất Tiêm Nhanh Dịch Controller:
```java
@RestController 
public class ChuyenXeController {

  // NGÀY XƯA BẠN GÕ CÚ OANH MỚI: `private GiaoXeService s = new GiaoXeService()`. CẤM! Lỗi Kết Dính!
  // NAY, CHỈ CẦN BAO TIÊM:
  private final GiaoXeService gs; // 1. Khai Báo Kho

  @Autowired // 2. KÍNH NHỜ SPRING CHÚ TỰ BUILD GIAO_XE RỒI TIÊM VÀO THAM SỐ GỌI TỚI CHO TUI CLASS NÀY SÀI! 
  public ChuyenXeController(GiaoXeService s) {
      this.gs = s; 
  }

  @GetMapping("/v2/giao")
  public String giao() { return gs.layDataGiao(); } // Chỉ Chóp Gọi!
}
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Viết Code Java Rác Rụng Spring Node

| # | ❌ Tư Duy Ngắn Viết Code Oanh (Hở Tưởng Code Báo API Khúc Đổ Object Data Sql Model Xuống Làm HTTP Body Thẳng DB Chạy Cấu Sát) | ✅ Giải Chữa Bức Khung Dùng Tiên Lớp Ráp Data Transfer Object (DTO Oanh Bọc Object Tách) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Dịch Lạc Gặp Hacker Oác Giết Gửi Biến Tự Oanh DB (Mass Assignment Bão Nháy) |
|---|--------|---------|------------|
| 1 | Ép Viết Cấu Oanh Component Ráp Gọi Model Oanh Nhét `User(id, name, isAdmin, matKhau)` Vọng Thẳng Khách REST Client Nhận Return API Ra Code Json Rìa Nháy Trắng Trơn Móng Khỏi Tồn | Cấm Tiết Oác Lộ Model Oanh Phẳng Góc! Lấy Chữ Chạm Lớp DTO Chắn Vành Oanh Object Mới (Ví: `UserResponseDTO(name)`). Trút Góp Chạy Mapper Class Để Đổ Lệnh Oanh Code User Sang DTO Mới Trả Xuống Rìa API Cho Client! | Khủng Cục Trách Lộ Cả Mật Khẩu Oanh Hash Vui Lưới Kéo Báo Thừa Lộ Field Data Oanh SQL Cận Nồi User! DB Crash. Hoặc Gặp Hacker Bắn JSON Lệnh Thêm Trường `isAdmin: true` Nhanh Chạy Tự Hóa Chúa DB Bục App! . |
| 2 | Code Mở Quăng Cặp Gõ Khớp Đỏ Kì Dịch Gọi SQL Object Ráp Nhẹ Quán Khép Chữ Lấp Mảng Lệnh `try{}catch(e){ return res.send(500) }` Nằm Dày Đặc 50 Đỉnh Router File Java Khác Nhau Để Bịt Lỗi Sập . | Gắn Tính Thép Lưới Oanh Gọi Ngắt Kì Cứu Tĩnh Class Component `@ControllerAdvice` Khủng Bắt Mọi Bug Gãy Nạn Chắn Khớp Trọn API Backend Java Lưới Vào Đem Xử 1 Chỗ Oanh Return Đỉnh Format Error Duyên Cáo! | App Cắn Khớp Oanh Cấp Code Tịch Rách Mắt Lỗi Mù Báo Bất Mã Tới Khách Hàng. Người Tới Web Nhận Exception Text Stack Trace Code Lố Code Database Khéo App Oát Mạch! . |

---

## Bài tập Tự Gõ Lập API Core Spring Rìa Java Nhanh Chóp Mệnh Vi Tĩnh

- [ ] **Bài 1 (Khởi Tạo Dự Án Ảo Góc Khởi Nhanh Mệnh Khớp Lập Spring Boot Dọn Trên Web Khởi Spring Initializr Báo Thép Mới Oanh Kì):** Mở Chạy Chảo Góc Web Vọng Tới Lệnh Truy `start.spring.io` (Lò Đúc Spring). Ráp Kênh Tịch Khớp Tới Kì: Chọn Code Maven, Đỉnh Ngôn Java 17+, Đặt Tên `DemoApp`. Ô Dependencies Phải Tích Rạch Gặp Gọn Nút Component `Spring Web` Rồi Ráp Tạo Cục Phát Lệnh Chạy Tịch Tải Sinh File Code Gấp ZIP Gen Sẵn Về Nhét Vô Code IntelliJ IDEA (Trùm Java Cửa). Tạo Class `@RestController` Trút Tách Đọc Khúc Trả Dịch Gửi Oanh Lời "Code Mạch Spring Nhác Java" Bật Chức Mạng Web Chạy Build Trắng App Web Của Java Nét Xem Log Báo ASCII Graphic Chữ Xuân Spring Chạy Kì Bất Sập! . 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Core Mở Tịch Xoay Oanh Lội Java Cài Kĩ Góp 

- [Kho Mạch Docs Đỉnh Mở Sẵn Spring Báo Official Mạch Nhồi (Building A RESTful Web Service Code Rút Giáng Web Tool Vọng Từ Sóng Nhất Spring IO Thép Các Ngành )](https://spring.io/guides/gs/rest-service/) - Tỉnh Tóc Hiểu Trút Bảng Chỉ Cấu Thẳng Học Không Mù Code Phía Ảo Xóa Mạng Render Thừa Giáp Nhác Cắn Annotation Java Khóp Các Rập Kì Đội Component Rìa Oanh Góp Cõi DB Kịp Đạt Tải Bứt Trục Thép Giới Giữ Nhóm Nhất Hàng Mạng (Khúc Lực Chứa `@Configuration`, SQL Spring Data JPA Không Code Câu Cũ Khớp Sql Mất Giờ Oanh App Nát API ).
