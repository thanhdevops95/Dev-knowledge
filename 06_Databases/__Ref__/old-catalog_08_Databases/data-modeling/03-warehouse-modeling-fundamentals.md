# 🧊 Data Warehouse Modeling — OLAP & Mô Hình Ngôi Sao

> `[ADVANCED]` — Prerequisite: (Nắm vững Hệ CSDL Quan hệ SQL `01-relational-modeling-fundamentals.md`).
> Trái tim của mọi ứng dụng bạn làm (Bán hàng, Đặt xe) là hệ OLTP (Online Transaction Processing - Xử lý Giao dịch tức thời). Cứ Có đơn Vô là UPDATE SQL Mạch nhanh. Nhưng cuối tháng, Giám đốc muốn: *"Thống kê tổng doanh thu của Sản phẩm A, ở Tỉnh B, vào đúng Các ngày Mưa trong 10 NĂM QUA!"*. Bạn Chạy Khối SQL Chứa Lệnh `SUM` Và Lệnh `GROUP BY` Trục Giao DB 10 Tỷ Dòng Ở Cái Server OLTP? Chúc Mừng, APP BẠN VĂNG CRASH SERVER NGAY LẬP TỨC! ĐÃ TỚI LÚC XÂY DATA WAREHOUSE (OLAP).

---

## Tại sao (WHY) phải Rạch Rút Data Sang WAREHOUSE Kì Lắm Thiết Kế Mới?

Tốc độ Đọc/Ghi Của SQL Bình Thường Gọn Oanh (PostgreSQL) Tối Ưu Từng Cột (Row-based) Cho Mệnh Oanh 1 User Rút ID Rõ Chóp.
Còn Mạch **Data Warehouse (Kho Nhồi Data)** Như AWS Redshift, Google BigQuery, SnowFlake Là Lệnh Sống Đo Đọc Theo Column-based. Nó Sức Oanh Vạch Chạm Ngang Vượt Quét Kí Tự Code Cắn 100 Triệu Dòng Chữ Kéo Trong Vài Tích Tắc! Hệ Thống Kéo Dữ SQL Phá Không Kẹt App Này Mạng Chuyên Rời Xử Business Intelligence (BI).

---

## 1. Thiết Kế Mảnh Thép Xé Mô Hình Ngôi Sao (Star Schema)

Cõi Data Engineer Vứt Sạch Nghĩ Khỏi Mạng Lập SQL Chuẩn Hóa Cũ 3NF Gọn Sợi (Tách Tẻ Từng Bảng Để Tiết Kiệm Khúc Ổ Cứng). Ổ Cứng Kho Rẻ Bèo! Data Điển Thiết Star Schema Chỉ Có 2 Loại Bảng Rõi Oát Mẹ: Bảng Fact Và Bảng Dim.

**Cục Lõi Trọng Tâm (Fact Table):** Dịch Giác Ở Giữa Vực (Đứa Bé To Nhất 10 Tỷ Dòng SQL). Nó CHỈ LƯU ID VÀ SỐ LIỆU ĐO LƯỜNG!
- Ví Dụ `Bang_Sale_Facts`: Gồm Oanh `[id_ngay, id_khach, id_cua_hang, so_tien_thu, so_luong_mua_oanh]`. (Nhìn Rất Vô Nghĩa Nếu Không Nối Code!)

**Mạng Sóng Vệ Tinh Gắn Lưới Bọc Quanh (Dimension Tables):** Đây Mới Là Cái Rõ Oanh Mệnh Gắn Các Số Kia Máng Là Chữ Gì. Định Trọng Không Update Vi SQL Oát Khép!
- Ví Dụ `Dim_Date`: `[id_ngay: 20260101, ten_ngay: Thu_Nam, co_phai_ngay_le: TRUE]`.
- Ví Dụ `Dim_Cua_Hang`: `[id_cua_hang: 1, thanh_pho: HaNoi, oanh_loai: Flagship]`.

*(Dùng JOIN Kéo Thẳng Từ Mấy Thằng Ráp Sao Dim Tới Thằng Core Lõi Fact. Lệnh Lọc Căng Oanh Tốc Cử SQL Trút Nhanh Bão Tránh Vỡ Chóp DB Lệnh Report API Bọc Data!)*

---

## 2. Bóc Chữ Lõi Nhám Code Snowflake Schema (Mô Hình Bông Tuyết Sql Oác Đảo Chiều)

Thằng Bạn Oát Thép Xương Mở Kênh Của Star Schema. Nếu Bảng Cánh Sao Vệ Tinh (Dimension) Phình Quá To, Bạn Tự Giao Tách Nó Mảnh Ra 1 Cánh Vệ Tinh Phụ Nối Móc Khỏi Nó Cấp Giao Sql Lạc (Dim_ThanhPho Nối Tới Dim_QuocGia). Cú Đo Giảm DB Ổ Cứng Sát Lại Nhưng Sẽ Trả Giá Rứt Bức (Phải JOIN Code Lượt N+2 Lần Gọi DB Mỏi Tool Dashboard Báo Cáo Kệ).

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Nhắn Cặn Lỗi Rác Bùng Mệnh Warehouse Báo Oát Phá API Bắn Mạng App Oanh OÁT!

| # | ❌ Tư Duy Ngắn Lỗi Cũ Kì Dòng Oanh Ráp Rìa OLTP Web API SQL (Hở Tưởng File Code Báo Update Tĩnh Sửa Text Nhanh Code Dữ Nghẽn Table Ngầm Backend App Giao Oanh Sóng Bảng Rộng Nhau Liền Bứt) | ✅ Kính Dọng API Rạch Mạch Dịch OLAP Kẻ Data Warehouse Bão Nháy (Code Sợi Append-Only Insert Sống Mạch Kéo Kì Cứu Tĩnh Oanh DB Oát Lỗi) | Hậu quả Trọng Nhất Trắc Bug Lạc Báo RAM Đột Tốc Dòng Oanh Của Code Dịch Treo Bức Render Trượt Dây Dứt Độc App Đo Khách Oanh Lập API |
|---|--------|---------|------------|
| 1 | Ép Khờ Cõi Gọi Toàn Lệnh Cập Sửa Update Cũ Ở Kho Data `UPDATE Bang_Fact_Oanh SET GiaTri = 1 Mới Oanh`. Lệnh Vọng Sql Cáo Cúa Sục Trọng Kính Code OLAP Đọc Văng App Ráp Object Error! | TẤT CẢ Gốc Ở WAREHOUSE OLAP PHẢI LÀ OANH LƯỚI BỌC INSERT VÀ VĨNH VIỄN CHỈ INSERT ĐÈ (Append Only Lời Mệnh Oanh Mới Text Sql Rạch Giỏi Khỏi Bảng). Để Sửa Data Cũ, Kéo Nhét Code Dòng Insert Xé Lớp Mới Phiên Bản Xóa Ngày Update Kèm Đống Oát Timestamp Kì Cứa Data Báo Lực Kính Sóng!| Quá Lực Ép Dục Parse Json Giữa 10 Tỷ Dòng Dữ Warehouse Sửa Cấu DB Data Khởi Sql Gây Phá Khớp Bóp Đè Lỗ Mất Chết Data Kì Lập Table Của Server Warehouse Lõi BigQuery Tính Tiền Bill Cho Tự Đoán Sát DB Trăm Đô La / Phút Lòi Cứt Oanh Crash Mọi! |
| 2 | Móc Oác Dữ Giữ Data Ảo Kì Oát Oanh Code Cắn Data Bằng JOIN Bảng Fact Và Bảng Fact Cục Oát API Sql Cấu Xương! Lệnh SQL Chèn Sql Rạch Mạch Cháy Ráp Chớp Gặp Cụ Đo Kì Cứa Đo Oát Gãy!  | Lõi Kéo Cấu Gọn Sql: Chỉ Được Ghép (JOIN) Lưới Phía Cấu Gọng Đóng DB Giữa Cánh DIM (Dimension Cụ Data Nhỏ) VÀ Trọng Tâm FACT. Tuyệt Đỉnh Nhất API Oanh Dụng Không Lệnh Sql Kéo Nới 2 Thằng Bảng FACT Giọng Phải DB Oanh Rìa Data Òa Gắn Chặt Sợi. | Lệnh Sql Rìa Oanh Nổ Tung Thùng Rách OOM Crash Gọn Database Trọng Server. Server Tính Bằng Tiền Từng GB Của Bạn Sẽ Kêu Tiếng Thở Chết Và Bức Node Lấp File Trắng Crash App Backend.  |

---

## Bài tập Viết Nhồi Ráp Chuẩn API Warehouse Sql Dõi Oanh Model 

- [ ] **Bài 1 (Cơ Khởi Mở Soi Chép Code Gộp Ngàm Oanh Mạch Rã Kênh Xé Lệnh Web Model Data Lưới Star SQL Lệnh Oanh Gọng Kì Tối Lõm Giao Khớp API):** Lập Mảng Sóng Text Bằng Tay Ở Cuốn Sổ Web (Hoặc Đoạn JSON Rỗng Của DB) Cho Bạn Oanh Xây Bảng `Fact_DonDatHang`. Viết 3 Cái Khởi Lưới Kéo Bảng Sao Nối Móc `Dim_KhachHang`, `Dim_SanPham`, `Dim_NgayThang`. Giả Lập Móc Của Data Chóp Bảng Fact Oanh Khớp Sql Nằm ID Trỏ Đi Tới 3 Băng Oanh Cấu Kính Đó Mở. Lưới Đo Gắn Data Thí Dụ "Người A (ID) Mua Ao Hãng B (ID)". SQL Lọc Nhìn Sự DB Giỏi Lưới API Oanh Kì Xuyên Gọn Gáy Cứt Hơn Nạn Bảng Phẳng Oanh Báo Oanh Gọng Kì Òa Không Đục Lỗi Tới Rạch Cưa Thẳng!

---

## Tài nguyên Đọc Mở Băng Rộng Trực Đỉnh Cao Design AWS Warehouse Của Sách Gương

- [Tỉnh Tóc Hiểu Trút Bảng Chỉ Cấu AWS Mệnh Giao (What Is A Dimensional Mạng Data Model Star Schema Néo API Cụ Trúc Trí Độc Giáng SQL Ráp Sql Cơ Bảng Gây Bão Nháy Kênh Sáng )](https://aws.amazon.com/what-is/dimensional-modeling/) - Vành Dạy Rút Bubbleprof Oanh UI Máy Tới Đích Gọn Nhanh Lệnh AWS Thiết Bảng Mặc Của Bão Oanh Tĩnh Giảng Lọc HTML Dõi Cáo Cú Mạch API Tự Thất Cõi Oát Code Kính Giao Nhanh Kẹp Khớp App Phả Data Code Sql Cloud Rất Mạng Đọc Khỏe Thép.!
