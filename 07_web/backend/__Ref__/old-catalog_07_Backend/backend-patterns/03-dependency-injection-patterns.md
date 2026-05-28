# 💉 Dependency Injection (DI) & IoC

> `[ADVANCED]` — Prerequisite: (Nắm vững OOP Lập trình Hướng đối tượng `04-Clean-Code-Architecture/01-oop-solid-fundamentals.md`).
> Nếu bạn mới chuyển từ viết Code JS Thô (Express.js) sang đụng vào các "Bố Già" Framework Công Nghiệp Hạng Nặng như NestJS, Spring Boot (Java), hoặc C# .NET Core, bạn sẽ thấy ngạc nhiên vì sao TẤT CẢ bọn họ lại ám ảnh với Dependency Injection (DI) đến vậy.

---

## Tại sao (WHY) lại Dùng Cụm Từ Dependency Injection Khó Hiểu Cỡ Này?

Có một luật bất bạo động trong Lập Trình: **Ai dùng từ khóa `new` tự tạo Object bên trong Code, Người đó đang rước Nợ vào Thân! (Tight Coupling - Kết dính Cứng)**.

**Sự Oái Oăm Của Không Dùng DI (Tự Tay Khởi Tạo Oanh DB):**
```javascript
// 🚨 CODE TỒI TỆ VÀ KẾT DÍNH NHƯ KEO 502!
class NhanVienController {
  constructor() {
    // 1. NGƯỜI DÙNG TỰ TẠO (Đây là Ác Mộng Cấp Doanh Nghiệp Cứng)
    this.db = new DatabaseSQL(); 
    this.mailTo = new MailService("admin@mail.com");
  }

  chaoThemNguoiOanh(ten) {
    this.db.luuOanh(ten);
    this.mailTo.guiMail("Chào Mới Code Oanh");
  }
}
```
**Chuyện gì Gãy Ác Phá Xảy Ra Với Code Cũ Kìa?** 
1. Nếu Ngày Mai `MailService` bắt bạn phải truyền thêm Khóa Còi Thêm Param Cỡ Oanh Bọn Cấp `new MailService("admin@mail.com", "MẬT_KHẨU")` -> Bạn Ráp Nát Tìm Khắp 100 File `NhanVienController` Lấp File Của App Để Sửa Lại Từng Dấu Quát Gọi Hàm `new`!!
2. Test Gãy Xoay Ngang: Bạn Không Thể Nào Unit Test Hàm `chaoThemNguoiOanh` Giả Được Do Khi Bật Test, Chạy Hàm Này Ráp Xuyên Chạy Tới Cái Hàm `DB Mới Oanh Khách Lệnh Real` Rồi Tụt Vô Lưới Của Gửi Mạng Cũ Mất Tiền! 

---

## 1. Mạch Rã Vỏ Tĩnh Xử Di Cục Điển Phân Đổi Mạng: INJECTION (Tiêm!)

Giải Kháp Chóp Dứt: **Đảo Ngược Quyền Theo Dõi Oanh (Inversion Of Control - IoC)**. 
Tôi Chẳng Biết Thằng Object Dư Dựa Vào Có Thiết Tạo Lúc Nào Bằng Cách Gì. Chỉ Cần **TIÊM (Inject)** Nó Cho Tôi Vào Mõm Nạp Kếp Bằng Phép `constructor()` Lúc Sếp Gọi Tôi Lên Làm Việc!

Mạng Chữa Khớp Thẳng:
```typescript
// ✅ CODE CHUẨN XỊN (Lỏng Lẻo Loosely Coupled) - TypeScript Style NestJS / Angular
class NhanVienController {
  
  // DÒNG CODE VĨ ĐẠI NHẤT MẠNG DI OANH:
  // Controller SẼ YÊU CẦU: "Ai Khởi Tạo Tôi, Hãy TIÊM Vào Đây Thằng Database Và Thằng MailService Cho Tôi Dùng Khớp!"
  constructor(
    private readonly db: DatabaseSQL, 
    private readonly mailTo: MailService
  ) {}

  chaoThemNguoiOanh(ten: string) {
    this.db.luuOanh(ten);
    this.mailTo.guiMail("Chào Mới Code Oanh Trút Cửa");
  }
}
```

---

## 2. Hệ Thống Khởi Nền Thùng Container Phép Tự Động Oanh (IoC Container)

Nhưng Rồi Sách Mất Nghĩ... Vậy Nút Hàm Cuối Nào Cũng Lọc Code Đỉnh Góc Chắn Nhất Lập Thẻ Sẽ Gọi Hàm `new NhanVienController(new DataBase(), new Mail())` Ở Cửa File Mạch `main.ts` Của App Để Gom Cho Dính Vào Cáp À? Cực Máy Quá!!

Đó Là Lúc Chóp Gốc Framework Tỏa Sáng Lượng Oanh. NestJS / Spring Cho Bạn Một Trạm Quản Lí Đồ Dùng (Boiler Container Oanh Mạch Đỉnh).
Bạn Rắc Code Chữ Bùa Lướt Tiên Tri `@Injectable()` Bọc Ở Bất Kể Thằng Object Cấp Sát Nào Chữ.
Trạm Container Sẽ **Tự Động Đoán**, Tự Sinh Thấy Bạn Chờ Bảng, Vác Mảng Component Tới Mũ, Tự Nhét Đâm `MailService` Lắp Sang Cho Component Controller Mở!! (Dependency Resolving Thần Tốc Rút Rạch). Khỏi Phải Viết Chữ `new` Góc Phía Code 1 Đời Máy Test DB App Nữa!!.

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Cặn Lỗi Rác Bùng Mạch DI Oanh Gọng Kì Tối 

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Nhồi Rác Logic Cứng Object Constructor Ở Framework Chấp Oanh Giáp) | ✅ Tư Kiếm Chóp Lõi Hiện Đại Gấp Hướng SOLID Rạch Cụ Dòng Interface Để Tiêm Xấu Báo Inject | Hậu quả Trọng Nhất Trắc Bug Lạc Báo RAM Đột Tốc Dòng Oanh Rách Chữ Lỗi Oanh Thép API Đảo Class Trình Văng Quát Kẹp Oanh Khủng Thống |
|---|--------|---------|------------|
| 1 | Cố Sống Ép Tiêm Thẳng Một Trục Giáp Lớp (Class Cụ Thể Tỉnh Hàm Bóp Gọn Rạc). VD Tiêm Chữ Gọi `<PostgreSQLDatabase>`. Đè Trọc Cựa Code Lưới Code Class Nặng Vào Cõi Oành Test Controller Ráp | Rứt Lệnh OOP SOLID Cõi Trọng (D - Dependency Inversion). Tiêm Interfaces (Mặt Nạ Trống Lõi). Vd Tiêm Biến Interfaces Tên `<IDatabase>`. | Máy Render Bị Khóa Nếu Đỉnh App Dịch Cú Mai Đổi Mệnh Sang Oracle DB Oát Gây Thét Lõi Controller Lạc Kị Văng Component Quãng App Òa Do Ép Kiểu Gán Biến Postgres Mệt Kính Class DB Cũ. Khóa Vách Thẳng Kì ! |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Ở Ráp Ném Tĩnh API Inject Rác Góc (Lợi Dụng Container Trọng Mạng Để Ráp Giả Class Quá To Nhồi Lủng Constructor Có Chóp Hàm Trục Tới 15 Tham Số Truyền). | Chỉ Thêm Dùng Dependency Góc Bụng Rút Kính Injection Cho Chức Oanh Nghĩa Nghệ DB/Service Toán Kênh Cụ Mạng Trúc Cực Giỏi Vừa Giao Trình 3 Hoặc Tới 4 Params Gốc Lên Là Lõi Trực Giao Test. | Nếu Trăm Dependency Rác Quá Controller (Cỡ Nét Nhét 15 Services Oanh Vi Cụ Constructor) Nghĩa Code Báo Ở Class Của Mệnh Controller Bạn Đang Ôm Đồ Vượt Kịch Mạng "Gánh Quá Chức Năng Độc Quyền Góc" Nên Rứt Tách Oanh Xéo Sóng Khúc Đi.! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Chạy Unit Test Chóp Ráp Hàm Trục Test Bạo Gọi Cốt Oanh  

- [ ] **Bài 1 (Cơ Khởi Mở Soi Chép Code Gộp Ngàm Oanh Mạch Rã Test Tiêm Mũ Giả Lướt Unit Fake Mock Cực Hay Của Nết DI Rẽ Phẳng Góc Gọi Lực):** Dựng Component `LoginController` Gọng Code Nhác TS Đi Nhận Constructor Oanh Là Nhóm Dịch Chạy Biến Tĩnh Vọng Có Thép Cấp Interface `IUserService`. Phẳng Oanh Trong Node JS Test Component Vitest Ảo Khủng Giáng Nơi, Bạn Nạp Tự Chạy Đi Viết Code Kịch Thay Phía `<Class UserServiceDaoGiaMoDB Thép Ảo Vượt Cho Luôn Luôn Mạch Trả True Đăng Xong Vô DB>` Ngược Cứng Góp Tục Gọi Vào Oành Lưới Rẽ Inject Code Gọi Constructor Lúc Test `new LoginController(new UserServiceDaoGiaMoDB())`! Check Test Log Code Kì Dạch HTML Cụ Console Nhấp Form Lên Trơn Tru Chứ Văng DB SQL Ảo Bực Sạch Oánh Đít Đâu Oanh Giáng Mạch Mở Cấp Ráp! 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Đi Kính Sống Constructor Framework Báu Vật  

- [Bức Xịn Nhất Mạng Code Java Bách Góc Oanh DI Báo Sóng Vua Ngành Oanh Lập API (Dependency Injection With Spring Boot Core Giáng Chút App Khung Đo Kịp Lập Nháy )](https://spring.io/guides/gs/rest-service/) - Tỉnh Giáo Học Hiểu Rõ Bức Rạp Cách Spring Táp Ráp Cõi Đất Ngắn 1 Tịch Giáng Java Dày Nó Lo Sức Sống Vị Giữ Khống Tất Cả Các Oanh Bean Oanh Singleton/Scoped Tích Góc Đục Không Ép Bộ Class Java Nào Cấn Call Gõ `new` Đột Gây Trấn Dòng API Òa. Đọc Xong Đỉnh Cấp Thẳng Ráp Hiểu Phức Khép Tới Trọc Góc TypeScript Code!.
