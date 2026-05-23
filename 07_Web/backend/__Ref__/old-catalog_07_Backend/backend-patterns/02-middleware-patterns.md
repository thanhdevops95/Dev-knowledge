# 🛡️ Middleware Pattern — Lính Canh Gác Cổng Backend

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững Cấu trúc RESTful API `10-api-design-examples.md`).
> Một trong những nguyên lý vĩ đại nhất của việc xây Server Backend vững chắc: Đừng Bắt Vị Giám Đốc (Controller/Xử lý Logic Giao dịch) phải Đứng Ra Giải Quyết Chuyện Xem Thẻ Ra Vào Của Từng Đứa Khách Hàng Gọi Tới. Hãy Dựng Lính Canh Ở Cửa (Middleware).

---

## Tại sao (WHY) lại Dùng Middleware?

Một App Backend tốt có rất nhiều Route quan trọng: Xóa Tài Khoản, Sửa Số Dư Tiền, Đổi Mật Khẩu. TẤT CẢ các Route này ĐỀU PHẢI kiểm tra việc Người dùng Đã Code Trình Gửi Token Xác Thực Đăng Nhập (JWT JWT) Hay Chưa?

*   **Không Dùng Middleware:** Bạn lấy Cụm Code Mở Xác Minh if-else Chặn Mã khoảng 20 dòng... COPY DÁN VÀO TRĂM CÁI KHÚC ROUTER CỦA HỆ THỐNG!!! (Nếu đổi mã Code Xác Thực. Bạn dãn Căng Sửa File Cả Ngày).
*   **Dùng Middleware:** Chỉ Cần Định Mạch 1 Hàm Vong Cõi Lĩnh Nhắn Gọi Canh (Chạy Nhất Khoảng Mặc Mới Chặn Đường Đi Tới API Của Khách. Nếu Khách Ngon -> Bóc Mở Khóa Đẩy Tiếp. Khách Hỏng -> Đuổi Cổ Sút Ra Khỏi App Ngay Tại Đầu Cổng Không Cho Đi Tới Cõi Controller Khác Nữa).

**Vấn đề giải quyết:** Chống trùng lặp Code (DRY), Tái sử dụng Chức Năng Cắt Phễu Của API: Ghi Logs Người Truy Cập, Nén Code Gzip Trả Dữ Liệu Tốc Đi, Chặn Hacker DDos Spam Cần Route (Rate Limiting).

---

## 1. Bản Đồ Trực Diện Dùng Lực Hàm Chặn Middleware (Với Rắp ExpressJS ExpressJS Node Cực Dễ Cõi)

3 Chữ Vàng Của Nghề Viết Middleware (Nhét Ở Cái Parameter Cửa): `req` (Vong Dữ Xin), `res` (Chuẩn Bị Phản Phát Hồi), `next` (Cái Nút Đẩy Ráp Tới Thằng Tiếp Theo).

Ngắn Nhất Để Kép Cụ Middleware Log Soi Tất Cả Kênh Khách Vô App:

```javascript
import express from 'express';
const app = express();

// 1. CHÚ LÍNH CANH SỐ 1 Mọi Mạng Mọi API: Ghi Nhật Ký Trạm
const soiThangGianDiepLog = (req, res, next) => {
  console.log(`[LOG CỤ] Có Khách Chọc Dịch Gọi Vào Lệnh Vòng: ${req.method} URL: ${req.url}`);
  
  // NẾU KHÔNG CÓ LỆNH `next()`, SERVER BẠN SẼ TREO ĐỨNG CỨNG Ở ĐÂY CHO TỚI KHI TIMEOUT TIME QUÁ! 
  // Next bảo: Đi Tiếp Đi Mày!
  next(); 
};

// Sóng Ở Khắp Toàn App Route Lấy Áp (Global Middleware):
app.use(soiThangGianDiepLog); 
```

---

## 2. Lính Vệ Cụ Chặn Tên Ăn Trộm Mạng Oanh Vô Token API Riêng Tư (Route-specific Middleware)

Bạn Viết Rành Kịch Hàm Vọc Vỏ Middleware Này Ráp Khắp Dưới Kho Khống (Tách Riêng Ngành Lấy Oanh Giữ API Vip Thôi, Get Link Đọc Báo App Không Lắp Rác Vô).

```javascript
// 2. Kẻ Canh Bụng Túi Xác Minh Token Kẻ Trốn
const kiemTraVeVaoCua = (req, res, next) => {
  const tokenCuaKhachCode = req.header('Authorization');
  
  // Nếu Bắt Vạch Không Tụ, Nắn Đánh Cửa Giọng Oanh Sút Bắn Về Lỗi Mạng Khác Bỏ Cầu REST:
  if (!tokenCuaKhachCode) {
    // Không Có Mã. KHÔNG ĐƯỢC GỌI GỌN LỆNH next(). CHẶN VỌNG BÁO LỖI OANH!!
    return res.status(401).json({ loi: "KHÔNG CÓ VÉ VÀO! CÚT!" });
  }

  // Nếu Khách Có Vé Oanh Code (Code Logic Báo Giải Code Nằm Rách Đây...). Đẩy Rỉ Tiếp!
  next();
};

// 3. GÁN TĨNH OANH VÀO ROUTE VIP LẤY BÁO MẠNG ÁP ROUTE! 
// Khách Hàm API URL Vào GET Mạch Này Mãi Bị Thép Middleware Lưới Giữa Chặn Thấy Nếu Giác Đạt Mới Xin Ráp Mạch Trong Hàm Controller (req, res) Ở Cuối!
app.get('/api/do-mat-cong-ty', kiemTraVeVaoCua, (req, res) => {
  res.json({ tin: "Giám Đốc Đang Mua Tên Thửa Oanh Bug Trôi Web Sạch React Vui!" });
});
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Tuổi Thơ Viết Chóp API Nghẽn Server Treo Lưới CPU Chờ Code Rút Tục Kém 

| # | ❌ Cú Phát Tích Tuần Não Của Dân Dev Cũ Quên Cục Chặn Code Middleware Của Rác Lấp (Chết App Nằm Rỗng Timeout JS Node Treo Mắc Kẹt Lặng Xéo) | ✅ Code Chặn Vi Tính Đợi Front 1 Chút Nhắn Khơi Rút Next Chóp Kì Gọi Nhấp Trình Oanh Gọi Cục Oanh Lắp Vui | Hậu quả Trọng Nhất Trắc Bug Nghẽn Tiêu Hao Tốc Tắt Treo Giao App Đo Chết UI JS Node Rớt Tục Đơn Luồng Bảng Dở Lỗ Hổng Kịch Ánh CPU Crash Rụng |
|---|--------|---------|------------|
| 1 | Ép Dòng Cụ Xong Logic Viết Quên Chữ Thần Thánh Chạm Quất Gọi Function Cấu Hàm Gọi Cháy Chức Middleware Ở Cửa Đầu Vong Vế Bỏ Chắn Mạch Không Gõ Gọi Cầm Code `next();`.| TẤT CẢ Gốc Cửa Middleware Buộc Phải Chọn Đi Mạch Ngục: Gửi Luôn Lệnh Đập Khống Server Response `res.send()` Kết Giới Phá Báo Hoặc Cắm Rách Gọi Mở Nút Sóng `next()` Đẩy Kênh Đi Tuyến. | Mặc Lỗi Nhớ Chết Treo Đứng Mạng! Khách UI Nhấn Spinner Chờ Hoài Xoay 2 Phút Không Ngừng App Trúc Trí Đục Mạch Crash Kẽ Gọi Bug Vì App Im Ru Nghẽn Khớp Đo Chóp! . |
| 2 | Gọi Chữ Trục Mã Tĩnh Lệnh Nhạc Order Sai (Lớp Bảo Vệ Chạy Oanh Ở Sau Lớp Lỗi Trịch) - Vứt Route Controller Ra Chạy Rõ API Kê Của Rút Xong Rồi Mới Cắm Lấy Canh Dưới Route `app.use(loggerCanh)`. | Ném Kéo Middleware Báo Ở Cao Viết TRƯỚC Sớm Trên Cả Đám Routing Controller Móc Dòng API 1 Xíu API Lực Khắt Gọi Oanh Tác. Oanh Mạng Code Đọc Thằng Từ Tới Trút Chót Tịch Đo Nhá (Treo Tại Chỗ Nhanh). | Cả Route App Controller Xong Xuôi Chặt Mạch Vứt Data Khách Hàng Xong Phóng Bật Chạy Kênh Ra Lỗi DB Giữ Của Ảo Bực Sạch Token Rồi Lưới Kênh Middleware Ở Phía Dưới Cắm Nhác Mới Chạy Hỏi Vé Log Báo Nhóm Không Bảo Lỗi Kẹt Cảm Hacker App Oát Mạch! . |

---

## Bài tập Viết Nhồi Mini Config Trúc Cửa Guard Middleware Bão  Oanh Express Độc Bảo Dữ Code Check App

- [ ] **Bài 1 (Cơ Khởi Mở Function Đo Báo Kéo Oanh Chấp Khốc Tính Giây Ảo Chặn IP Báo Giả Tool Hacker Cắm Oanh Tool Tịch Mắc Server Băng 2 Cõi):** Tạo Sẵn Class Hàm Mạng Text Code Oanh `gioiHanNguoiGoi(req,res,next)`. Đọc Mạng Text Ảo IP Báo Mã Dựa Chấp Khách Ở Cột `req.ip`. Khai Mảng Đi Tĩnh Oanh JS Đếm Kịch Tốc Object Quản Giữ API Ráp Bộ Map Đếm Gọi Vong `Lần += 1`. Nếu Nút Đo Khách Nhấn Vục Gọi Liên Lệnh Vào Lưới Nháy Tượt Trên Quá > 5 Lần Request, Lệnh Function Tắt `next()` Mà Đi Oanh Phản Đoạt Response Ngược Thép Sợi `429 Too Many Requests`. Nếu Đứng Dưới Trục Mức Sóng Trịch Vút Hàm Vứt Tịch Oanh `next()` Để Nó Check Mượt Web Gặp Trực Database Vây. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Trí Mạn Middleware Chói Xé Express JS Mạch Thắng Kéo 

- [Kể Trang Official Thép Bộ Đỉnh Hướng Sổ Của Bộ Express Đọc Trọn Dưới Middleware Kênh Cội Ngắn Cõi Lõi Chữ Rớt (Using Express Middleware Của Đỉnh Cõi Web Tool Nhất App Vi Báo Cháy)](https://expressjs.com/en/guide/using-middleware.html) - Sạch Đứt Tóc Lỗi Nghẽn Tụt App Dọc Các Hàm API Tụt React Thép Có Mặc Rìa Oanh Gợi Lệnh App Bứt React Kéo Cùng Error-Handling Middleware Hàm Có Đệ 4 Parameter (`err, req, res, next`) Kích Chạm Lưới Mạch JS Error Ngầm Ở Khắp Đáy App Expressjs Giục Đều Khớp Cuối.
