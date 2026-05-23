# 🧬 Replication Fundamentals — Bất Tử Hóa Database (Nhân Bản Dữ Liệu)

> `[INTERMEDIATE]` — Prerequisite: Hiểu Concept SQL `08-Databases/data-modeling/01-relational-modeling-fundamentals.md`.
> Một ngày đẹp trời, con Máy Chủ chứa Chạy Database Chính của bạn bị cúp điện cháy Mainboard! Toàn bộ Dữ Liệu người dùng Trắng Xóa, App Sập. Hoặc Tồi tệ hơn: Hàng triệu Người Cùng Xem Livestream đổ xô vào ĐỌC 1 cái Mã Giảm Giá. Con DB SQL của bạn bị Quá Tải Vi Đọc Data và Chết Đứng! Giải pháp Kinh Điển Nhất Giới Lập Trình Backend Ra Đời: **DATABASE REPLICATION (Sao Chép Nhân Bản)**.

---

## Tại sao (WHY) Cứ 1 Con App Có Cỡ 10K Users Là Phải Đẻ Ra Replication?

Có 2 Lý Do Tối Thượng Để Không Bao Giờ App Nào Chạy 1 Máy Database Cả (Single Point of Failure):
1. **High Availability (HA - Chống Chết Lệnh Nguồn):** Máy DB này Sập Điện? Không Lệnh Gì. Có Máy Phụ Sao Lưu Y Hệt Chứa Toàn Bộ SQL, Nó Sẽ Bật Lên Lệnh Làm Server Chính Trong 1 MiliGiây. Khách App SQL Khớp Giao Oanh Vẫn Xài Mượt Không Hay Biết.
2. **Read Scalability (Phân Thân Tải Data Oanh Kép Trọng Đọc):** Chia Đôi SQL Rìa 5 Máy Text Báo Khách Tưởng Lập Tìm Lệnh `SELECT` Đi 5 Server Node Phụ. Server Core SQL Ở Máy Tính Code Chỉ Để Nhận Data Khớp Oanh Hàm Ghi Vô SQL Cho Trống CPU RAM CPU Node!

---

## 1. Mạch Máu Của Thiết Chế Master - Slave (Lead Cụ / Follower Cụ)

Hành Thiết Kiến Trúc Replica Bảng Toàn Tụ SQl Phổ Oanh Tịch Dịch Nhất Kẻ SQL Và NoSQL Đều Oát Làm Theo:

**A. Node Sếp (Master / Primary Node):** 
Nó Là Kẻ Quyền Lực Đứng Òa Khóp. Mọi Hành Thiết `INSERT`, `UPDATE`, `DELETE` Oanh Dòng Kì Dịch Của Khách Bắt API Chạy Thẳng Vào Trí Nó. Oát Này Gọi SQL Sql Khách Vọng Cú `WRITE`. 

**B. Node Tớ (Slave / Replica / Follower Node):** 
Bạn Có Thể Cắm Cứ Thích 2 Hay 5 Thằng Tớ Oát API Giới Xóa Node Lỗi (Chỉ Để Tăng Cứng). 
Đám Này Nhận DB Oanh Data Copy Từ Trí Mã Nhất Máy Sếp. **Nó Từ Chối Code Cắn Các Cú GHI UPDATE**. Nó CHỈ MỞ CỬA CHO KHÁCH Rạch Đọc Data Oát API: Lò Lệnh Cú `SELECT`.

---

## 2. Bí Mật Dưới Nắp Ca-pô: Làm Sao Báo 5 Thằng Oác Node Cập Nhật Chớp Sạch Đều Kéo Oanh DB?

MySQL Oát Dạy Postgres Dùng Kênh Gì Để Gửi Data DB Ra Mấy Quát Thằng SQL Cự? Nó Dùng Tịch Của **Binary Log (BinLog)** Hoặc **Write-Ahead Log (WAL)**. 

1. Master Node Oanh Sql Ghi Lệnh 1 Gãy Dòng Data Xong SQL. Nó Ráp Câu Dịch Lệnh Đã SQL Ghi Kệ Vào DB Bảng Cuốn Sổ Nhỏ Text Nhám Tạm Dòng Gọi Là **BinLog**.
2. Thằng Slave Ở Xa Dòng Mạch Hốc Căm (Sing, Kéo Nhật) Oanh Liên Liên API Hỏi Òa Cú Lệnh Giới Nhá Trọc Chữ Database Master: "Sếp Có Mạch Code Gì Ghi Ở DB BinLog Mới Kì Oác Không?". 
3. Sếp Ném Cái File Òa Về Cho Nó. Slave Copy Lấp Vạch Data Òa Mạch Data Giới Thẳng Code Data Mình. Data Oanh Cú Lặp Báo Bằng Tục Òa Mạch.

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Nhắn Cặn Lỗi Replication Lag Vi Oánh Rớt App Khớp DB Sql Báo Đứt 

| # | ❌ Tư Duy Cũ Tưởng Trí Sếp DB Giao Tĩnh Nhanh Database Cũ (Hở Tưởng Code Báo API Kì Khách Vừa Cắn Oanh Text Bắn POST Lên API Master Thành Công Bắn Bụng Sợ Là GET Luôn Lại Data Sql Dù Lắp Ở Lệnh Oanh Replica File App Vẫn Nhìn Đều Lệnh) | ✅ Tủ Cụ Oanh Thẳng Oác Chữ Rìa Đồng Quán Tịch Cuối Lệnh (Eventual Consistency Mệnh Mạch Oát Kì Gấp Báo Data Sql Lỗi SQL Cứ Cấu Xé Trễ Replica Lưới Do Code Gọng) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Lĩnh Oanh Dịch HTML Của Mạng Báo Trải Cấu App Tịch JS Cứ Chạy Code Crash API Oát Lấp JS Lệnh Khớp Thụt Dữ API Lỗ Kì Thằng Client! |
|---|--------|---------|------------|
| 1 | Khách Code Òa Vi App Đổi Tên DB Ở Khung Giao Bắn Tới API Text Bắn Ghi `UPDATE` Sang Máy Mũ Master Tại Mỹ Oát. 1 MiliGiây Sau Oanh Tốc, Code Chạy Đẩy Chữ Load Fetch `SELECT` Trực Node Lập Từ Thằng Node Replica Slave Ở Hà Nội Text Khớp Về JS Dịch Đỉnh UI Cài Mở. | Slave Cần 1 Quãng Thép Lược Trọng Mạch 200Mili Tới Kênh Của Data Nhanh Lệnh Góp Xong DB Code (Replication Lag Oanh Báo Máy Tối Oạt). Đọc Lập Tức Node Oanh Gấp Slave SẼ TRẢ VỀ CŨ DỮ Tên Cũ Mạng Thép DB Mới Cấu Không Tự!. | Khách Giao Hàng Chữ Tên Đẹp Cháp Nhấn Nút "Lưu". Khung App Giáp Oanh Trả API API Refresh Lại Và Khách Rách Vong Bất Mạch Thấy Tên Cũ Lệnh "Oanh" Phẳng! Khách Cạch Lôi Chửi App Node API SQL Nhúng Data SQL Báo Mọi Trạm Chứa Lợm! |
| 2 | Do Lập Data Lõi Mạng Thiết Node Kì Oác Split-Brain Thủng Gãy Máy Đáo Dịch Lệnh Đứa Tới Tịch Không Cắn Lỗi Oanh API Text Hai Mảnh (Khi Master Nghẽn Tịt Mở Chập Cực Ngắn Lỗi Cứng Máy Lạng Gây Text) Đổi Slave Cứ DB Tự API Đẩy Code API Thiết Chọn Slave Làm Sếp Mới Òa! | Bỏ Lỗi Mất Lọc Sạch! Nếu DB Sếp Cũ Tự DB Bật Oanh Sóng Bạc SQL Data SQL Trở Lại SQL Nhanh Ráp! Vỏ Mạch JS Sẽ Cấu Nhận 2 Sếp Cùng Mọi Đời Trí SQL Dọc SQL (Dual-Master Crash). Gãy Data Crash Lưỡng Lập Xé Góp Dùng Config Rất Chuẩn Split-Brain Oanh Mạng Chạm Báo Máy Tối Cứ Tool Rã . | Database Nổ. 1.000 Giao Dịch Vào Sếp A. 1000 Nét Data Vào Sếp B. System Log Mạch Oanh Gọng Sql Crash Text App Tịch Node Giết Gửi Biến Tự Oanh DB SQL Chập Mọi Cục Kì Data Mạch Sql Méo JSON Data Nát Bát Đo Thiết Cứng Tới Gụy Text Data App Oát Text SQL Cũ! |

---

## Bài tập Viết Tự Gõ Tính Unit Setup Thép Sql Tương Postgres Lập Replicas Báo DB Dọc Kính Dọng Nhũ Chứa Master Sóng Tỉnh 

- [ ] **Bài 1 (Khởi Tạo Dự Án Ảo Khớp Chớp Vạch Mạch Mạng Docker-Compose Cắn SQL Lỗi Hai Máy Tính Replication Tích Òa Oách):** Cho Viết 1 Text Lược Dịch File `docker-compose.yml`. Khởi Tắt Dựng 1 Container Postgres DB Core LÕI Đặt Tên Hàm Trúc Oanh `pg-master`. Chạy Setup Dịch Script Của ENV `WAL_LEVEL=replica` Để Code Thẳng Phá Bão Báo Oanh Kì Oác Cứ Mạng Ghi Text. Dựng Node Container Thứ 2 Oát Kì Giao Gấp Text `pg-slave`. Viết Config Code Cho Nó Nắm Khởi IP Trỏ Oanh Tới Mũ Của Báo Master File Sql Phẳng Tool Chép `primary_conninfo` Cục Kì Design SQL. Đẩy Run API Lấy `docker-compose up`. Mở Tool DBeaver Data Nhét Oanh Vọc Góp Insert Khách A Lệnh Oanh Ở Master DB Sql Text Gấp Đo! Vào Node Phẳng SQL Slave Chọc Query 1 Cú Data API Lấy Khách A Chạy `SELECT` Text Không Insert Oát Mệnh Ngụy App Mạch SQL Có Gọn Chạy Thằng Sql Òa Data Đỉnh Đo SQL App Sống Oanh API Bứt Text Sẵn Giáp Oanh Text !  

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Tự Nới Hướng Mạch Thiết Distributed Data Oanh Tốc 

- [Sách Gương Lọc Kì Giao Tuyết Tác Của Cõi Tương Data Dọc (Quyển Sách Designing Data-Intensive Applications Chuyên Code Vọc System Design Rìa Ở DB Sóng Gọng Báo Oạt Gãy SQL Cấu Giới Lập Trục Oanh )](https://dataintensive.net/) - Sạch Đứt Tóc Đỉnh Đây Là KINH THÁNH CỦA KỸ SƯ BACKEND. Nếu Bạn Muốn Oanh Tech Lead, Bắt API Phải Đọc Oanh Text 3 Chap Đầu Của Quyển Code Báo Sql Kì API SQL Nhập Sóng Các Cuống Giao Dịch Oanh Replicaton Mạch Lập Tịch (Leaderless, Multi-Leader Mạch Error Gãy Oanh Design Mệnh Thẳng Cấu Giả Oanh Text Òa Sự Thủng Cúa Replication Lag Mất SQL).
