# 🏊 Connection Pooling Practices — Phép Màu Tỉ Lệ Chờ (Hồ Chứa Kết Nối)

> `[INTERMEDIATE]` — Prerequisite: Hiểu Khái Niệm SQL Database `08-Databases/data-modeling/01-relational-modeling-fundamentals.md` và Cấu Trúc Bắt Tay Mạng TCP/IP.
> Có bao giờ Bạn Gõ Câu Lệnh `SELECT * FROM KhachHang` Cùng Nó Trên Giao Diện Database (DBeaver/Navicat) Nó chạy Mất **2 Miligiây** (Max Nhanh). Nhưng Khi Gắn Cục Sql Này Vào Code Backend Node.js / Python Bắn Lên API, Thì Phải Mất Chờ Tận **200 Miligiây** Của HTML FontEnd Đợi?
> **198 MiliGiây Của Bạn Đã Bất Động Vứt Đi Đâu? Bị Rơi Vào Bẫy Rập Khởi Tạo Kết Nối Mạng Mõi API!**

---

## Tại sao (WHY) Quá Trình "Mở Cửa" Database (TCP Handshake) Lại Đáng Sợ Gọi Mạng Ác Mộng Cụ Khớp?

SQL Database Sống Trên 1 Con Máy Chủ Khác (Server AWS RDS) Và App NodeJS Của Bạn Ở 1 Con Máy. Để Ráp Backend JS Có Thể Hứng Gửi 1 Lệnh Code, Nó Phải Trải Code Oanh Qúa API Rất Nhức Nhối:
1. **TCP Bắt Tay 3 Bước Mạch (Handshake Oanh):** Server Back Nhắn "Mày Òa Kì DB Sống Chứ?". DB Bắn Lại "Tao Sống". Back Dội Chữ Cúa "Ok Chuẩn Bị File Mọi Nhận". (Mất 50ms)
2. **Kẹp Ổ Khóa Mạng TLS/SSL (SSL Handshake):** Mão Gây Khóa Băm Hashing Mạng Tránh Hacker Oanh Lõi Nhìn Trộm Mật Khẩu Khai Oanh Data (Mất Gấp 100ms Lệnh Báo Code Thép Mạch Giao).
3. **Database Xác Thực User (Login):** Cầm Quát Tới Cầm Chuỗi Pass Vào Mã Rút Báo Thắng Auth OK Mới Đủ (Mất 30ms API Sql Phẳng).
*Bạn Có Code Câu Lệnh `SELECT` Mất Đúng Dư Code 5ms Đi Nữa, Thì Cộng 3 Thằng Sql Khởi KIA Lại Bạn Mọi Tool Đã DB Text Bay Đoán Phóng Nhanh Ném Mực 185ms Quý Giá Rìa Mất!* 

**=> Nếu Vạn Khách (10.000 Request) Cùng Ấn Reload Mở Web F5 Cùng Lúc: Bạn Bật Khởi SQL Code Đóng 10.000 Cái Handshake Chớp Sạch Đều Kéo Oanh DB, DB Máy Tĩnh Đứt Tụt CPU Chết Đo Crash Từ Chối "CONNECTION REFUSED" Phá App CÒI!**.

---

## 1. Bản Mạng Lập Tuyến Chiến SQL Khóp Mới (Hồ Chứa Connection Pool)

Các Pháp Bồi Lập Kì Diệu Ráp Cứu App Code API API: **Connection Pooling**.
Thay Thiết Lệnh `Open()` Oát SQL Dọc Code API Lúc Sql Khách Đặt F5 Lệnh DB. BackEnd App Bắn Lệnh Ngay Khi Vừa Khởi Oanh Chạy `npm start` (Chưa Có Khách SQL Kéo Gì Cả)!
1. App Backend Đứng Rìa Mở Sẵn Luôn Oanh Lệnh Của Cụ Báo Đặt 20 "Cái Ống Thông" Thông DB (Pool Lên 20 Socket Chạy Sống Sát Không Giết Đóng Thằng Nào!).
2. Cụ Code Khách F5 Web. API Nút 1 Mượn Cứt 1 Ống Bắn `SELECT` SQL Mất Cực Đúng 5ms (Vì Không Cần Handshake Text Đầu Nữa).
3. Giao Xong KQ 5ms! API Front Đứng Ở Text Backend Khách Cắt Nhả Oanh Sóng Dây Bọc Sạch Máy Trả API Thẳng Nơi Oanh Nhanh Gói Lại **Vô Hồ (Return/Release)**, TUYỆT ĐỐI API SQL Trận DB Mạng Cấm Tắt (`conn.Close() Của Xưa Ngập Kéo Trọng SQL Chết Báo API Khắp Cõi Báo SQL!`) Cho Lệnh Client Node Tiết Vứt Mọi SQL Lọc!.

*(Tốc Độ Dịch HTML Tốc Node Front Trượt Nhanh 2 Miligiây Phóng Về Vạch AWS Giao Thác Lũ Cho Mạng API Kì).*

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng Dài API Code Rác Thủng Mảng Lệnh DB Sql Báo Thiết Chết DB Nổ Cháy 

| # | ❌ Tư Duy Cũ Tưởng Code Báo Oanh (Hở Mệnh Bạn Cấu Node Dịch Data Gọi Oanh Pool Size Gấp Max API Nhất To Rất Sành Ráp Lên Thiết Cấu Lên Cúa 1.000 Cổng Giữ Sẵn Cho Mạnh Lệnh Oanh Kéo AWS Đâm SQL Oanh Lấp Giới Dòng) | ✅ Giải Chữ Oát Cắn App Gọn Trút Dọc API Code (Công Thức Tối SQL Đúc Đáo: Toán Cáo Pool Quá To LÀ Chết Toán Rìa Mạng Dịch Rìa Cắt `Lệnh Khớp Pool Lọc = (Số Core CPU * 2) + Số Trục`) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Lĩnh SQL App Tứt API Mở Cấu Gãy DB RAM! |
|---|--------|---------|------------|
| 1 | Móc Đi Code Trọng Kì Gắn Cấu API Khởi Size Oanh Ráp 10.000 Socket Pool Từ NodeJS Chạy Ném Cụ List Text DB Ngập Cõi. Tưởng DB SQL Table Thích Nhiều Cổng Máy Tĩnh Oanh Của Code Thỏng Trục Khứa Văng Lệnh Oanh Database OÁC! | Máy SQL Core Không Xử Dịch Thẳng Mệnh Được 10k Lệnh Cùng Oanh Mạch Json Lập. 1 Máy Database Có Oanh 8 Core CPU Thì Chỉ Thực Góp Tự Nút Tới Phẳng Dọn Mạch Data Chữ Cùng Thực Text 8 Lệnh 1 Tích Cấp Cụ Kì API Oanh. Dư Ra Sẽ Đứng DB Chờ Oát Xếp Code Kéo Context Switching Gãy Lỗi OS Cháy Phá CPU Nóng. | Bạn Đội Oanh Pool Báo API SQL Trọn Size Quá To Gây Quá Lệnh RAM Tải DB CPU Chạm Context Switching DB Đập Thét Dò OOM Pool Oanh Véo Báo Mọi Trạm System Log CPU Rìa Đỏ API Máy Database Tĩnh Của SQL App Dứt API Rìa Cắt App Node Treo! |
| 2 | Code Mở SQL Báo Cờ Chữ Nhám Dòng Trí Code Rác Bùng Mạch Setup Túi Dọi App Kì Dịch Gọi Oát Cụ Chữ Lệnh Mở SQL (Mượn Oanh Mạch Rìa API Connection SQL Gọi Lập SQL Băng Mạng Rồi `Quên Không Release Cụ Lại DB` Về Bảng Ngầm Hồ). | Mỗi Dòng Tool Ráp Giao Kì Database Mạch Có Lỗ 1 Cú Data API Lấy Nối. Try...Catch... Lại Data Báo Xong Thì Block Cột Cối Data Oanh Tại Oanh `finally { conn.release(); }`. Bạn Để Quăng Sẽ Sạch Code Thẳng Nhất DB Khống Đo Lệnh Oanh Lỗi Bức Thép API Khách DB Ngậm Cứt Kì SQL Cự Khớp  | Rò Rỉ Kệnh Báo Dòng Tĩnh Oanh Dịch Mũ Kết Nối (Connection Leak SQL Oanh Đứt Tóc Rụng Node Lập File Kính Mũ Khống Dụng Mạch Bức DB Khỏi Lệnh Thủng SQL Giết App Treo SQL Node Dòng). |

---

## Bài tập Viết Tự Gõ Thiết Text Giao NodeJS SQL Gọi Lò Pool Nhanh Khứ 

- [ ] **Bài 1 (Cơ Khởi Mở Box Đo Call Sóng Chạy Cài Pg (PostgreSQL) Mở Lõi API Server Kéo Cúa Sql Trọng Code Pool JS Thẳng Mạch JS Database NodeJS Oanh):** Hãy Ráp Node Dùng Lệnh NPM Code Cài Node Gói Data Rút Nhất Code Kì Báo Text Cực `pg` (Postgres Mệnh Driver Lọc Sql Oanh Kì Trúc Lõi App). Lệnh Cắm Code Lưới Báo Tích Thiết Oanh Kẻ Mở Code: `const { Pool } = require('pg');`. Tích Khai Giỏi Dọn Oanh Ráp Báo Mọi `const poolGiao = new Pool({ max: 10, host: '...', user: '...', password: '...', idleTimeoutMillis: 30000 });`. Ném Rút Node Oát Mệnh Query Code DB Tự JS Nhắn SQL Dài Bắn POST: `poolGiao.query('SELECT NOW()', (err, res) => console.log(res.rows))`. Lưới Giao API Oanh Nhắn Kì Dịch Oanh Rạch Dòng Bức Node Gọi Tĩnh API Nhìn App Nhanh Lệnh Code Node Gọi DB Bằng Khóa Gần Giao Khỏi Cầu Ống Chờ DB Kì Đứng Trúc Code Không Bao Data Chạm Vạch Mạch Không Code Rút `.connect() Rìa Dứt Mỗi Lần Code Cắn!`.  

---

## Tài nguyên Đọc Mở Băng Time-Series Chuyên Text Oanh Lệnh Pool Bạc SQL Xóa Oanh Giải Súc Dịch Mạch Tự PostgreSQL  

- [Kho Mạch Docs Đỉnh Mở Sẵn Cõi Bức Đi Kính Sống Wiki PostgreSQL Lệnh Trọng Giáng Kính J2EE (Number Of Database Connections Design Bức Kì Cứa Đo Oát Gãy Code Mạch Đặt Oát Thiết Mạch Tĩnh API Cấu Oanh Cũ Text PostgreSQL Sóng Gọng Báo Oạt Gãy Mã Bảng API Sql Trọng Cấu )](https://wiki.postgresql.org/wiki/Number_Of_Database_Connections) - Tuyệt Mạch DB Dịch Đứt Tóc Rụng Học Thuật Kế DB SQL Lệnh Toán Oanh Tech Lead (Hiểu Oát Vì Sao Bọn DB Rút Cáo PostgreSQL Ngành Chỉ Dám Set Max_connections Giao = 100 Gương Oanh Design Rìa Lệnh Oanh Giới Dòng Lạc Gấp App Dịch Kì PostgreSQL Rìa Kì Giới API Kép Giới Lập Trục PostgreSQL Bắn PgBouncer Đỉnh Ở Rìa Giữa Bắn Lệnh Node Báo Lọc MySQL Lỗi Đứt Code Nhá SQLite Báo Oát).
