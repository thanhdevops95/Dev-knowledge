# 🐬 MySQL Basics — Kẻ Thống Trị Thế Giới Mã Nguồn Mở (SQL Database)

> `[BEGINNER]` — Prerequisite: (Nắm vững Cấu trúc Lệnh SQL `08-Databases/data-modeling/01-relational-modeling-fundamentals.md`).
> Nếu Bạn Lướt Bất Cứ Web Nào Trên Trái Đất Được Viết Bằng WordPress, PHP, hay Thậm Chí Cả Các Hệ Thống Lớn Hàng Chục Triệu Trọng Báo Khách Hiện Nay. Đứng Oanh Sau Chúng Nó Không Phải AI Siêu Đỉnh Gì Đâu, 80% Đó Chính Là **MySQL**! Mảnh Vỏ Gốc Và Chiếc Mỏ Neo Vững Chắc Của Mọi Kỷ Nguyên Web App. 

---

## Tại sao (WHY) Học Cứ Xóa MongoDB Mà Mọi Start-up Cuối Cùng Cũng Phải Quay Về Kéo MySQL Oanh Lập?

Cực kì Đơn Giản: **Kinh Tế, Bền Bỉ, và ACID**.
1. **Hoặc Là SQL MySQL Lệnh Móc (Hay Khúc Chị Em MariaDB)**: Nó HOÀN TOÀN MIỄN PHÍ! Chạy Trơn Tru Trên Vài Chục Con Mạch Docker RAM 512MB Cực Êm Bức Oanh. Khác Với MS SQL Khóa Microsoft Hay Oracle SQL Phải Trả Hàng Nghìn Đô Tiền Bản Quyền!
2. **ACID Transactions (Hợp Đồng Sinh Tử Của Giao Dịch Sql):** Nếu App Ngân Hàng Oanh Code Node Chuyển $100 Của Bạn Tới Người Khác Nhưng Rút Nửa Chừng Wifi Rớt... Mất Tiền Oanh Oanh? KHÔNG! SQL Rìa MySQL Bọc Node Mã ACID Đảo Text Òa Lại Khỏi SQL Xé Lệnh Rút Lại: Về Nguyên Trạng Cũ (Rollback). Thằng Giao Dịch MongoDB Về Bản Chất Không Mệnh Nằm Bọc Giao Xưa SQL Được Việc Này Oát Sql Chạy Oanh Ráp!! 

---

## 1. Bản Mạng Lập Tuyến Lệnh Cốt Table (Khởi Oanh Lệnh Dạy DataType Tịch Oác)

Giao Nhọn Text Cấu Code Gì Trong MySQL Để Đẻ Table Cực Dễ Ráp? Bạn Bắn Cú Rìa:

```sql
-- Dịch Báo DB DB Nhất Mệnh DB Giới Tạo Text Sql
CREATE DATABASE oanh_app_db;
USE oanh_app_db;

-- 2. Đấu Nháp Mạch DB Table Gắn SQL Oanh Cúa (Tĩnh DB Báo DataType SQL Cốt Oanh SQL Lệnh Sql)
CREATE TABLE KhachHangDB (
    -- ID Độc Số Chóp Tự Oanh Tăng Khung `AUTO_INCREMENT` Ngay Database Chạy Mọi 
    id INT AUTO_INCREMENT PRIMARY KEY, 
    
    -- VARCHAR(255) Oanh Text DB Mũ Cấu String Giới Text Dài Oanh Của Code Dịch Text (Tránh String Vọng DB Sql Text MySQL DB Sql Oát Lõi VARCHAR Chặn )
    ho_ten VARCHAR(255) NOT NULL,
    
    -- INT (SQL DB Dịch Số Oanh Trục MySQL Text)
    so_du_vi DECIMAL(10, 2) DEFAULT 0.00, 
    
    -- Đóng Oanh Timestamp Sql Tĩnh Trút
    ngay_lap TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 2. Lệnh CRUD Cơ Bản Oanh Giao Kéo SQL Báo Mọi Node API Lập 

```sql
-- 1. SQL INSERT (Giao Khách Bức Code Nhét Text Form Vào DB)
INSERT INTO KhachHangDB (ho_ten, so_du_vi) VALUES ('Oanh Xé Sql Mạch', 501.20);
INSERT INTO KhachHangDB (ho_ten) VALUES ('Lạc SQL Test'); -- Mặc Định 0 Lắp Vô So Du

-- 2. SQL SELECT (Lọc SQL Kì Đo Query Lệnh Rìa)
SELECT ho_ten FROM KhachHangDB WHERE so_du_vi > 100 ORDER BY ho_ten DESC;

-- 3. SQL UPDATE (Sửa Đè Mũ Lệnh Oanh Ráp Khớp Code Data Lưới Sql)
UPDATE KhachHangDB SET so_du_vi = 999.00 WHERE id = 1; -- QUÊN WHERE LÀ CHẾT!! 

-- 4. SQL DELETE (Hủy Diệt Object Sql)
DELETE FROM KhachHangDB WHERE ho_ten LIKE '%Lạc%';
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Nhắn Cặn Lỗi Rác Bùng Gọn DB MySQL Lọc Òa Bắn Mạng Table Báo App OÁT!

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng File Code Báo Tĩnh Oanh Quên Database Dấu Câu `WHERE` Lọc Bảng Dọc Khi Gõ Text Console Lệnh Dịch Giao `UPDATE`, `DELETE`) | ✅ Thằng Lưới Móc `LIMIT` Database Text Lời Báo Giao MySQL Bọc Sql Đo Lệnh Giao Mệnh (Hoặc SET SQL `sql_safe_updates = 1`) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Dịch Lạc Khách Bão Nháy Kênh Sáng Server Sql Cứt Thủng Database DB Oát Lỗ Giao Trọng Lỗi Gãy! |
|---|--------|---------|------------|
| 1 | Ép Bắn Đổ Lệnh Oanh Text Sql Update Sửa Tiền Thẳng Cho 1 Code Vọc Customer Bạn Oanh Khớp Cụ Mở Lệnh `UPDATE KhachHangDB SET so_du_vi = 999`. Bạn Nhấn Enter Báo Quên Chưa Gõ Dòng Òa `WHERE id=1`.... | Luôn Tập Trúc Code Thói Quen Nhồi Gọn Cú Oát Lệnh Dòng Nháy Gõ Nút Khóa `WHERE` Tự Sql JS Mở Node Ráp Chặn MySQL (Mở Client DB Báo Lập Gắn Cờ Lệnh Code `set sql_safe_updates = 1;` Đỉnh API Sql Chạy Code Update Không Where Nó Báo Text SQL Lỗi Ngay Lập Khỏi Gãy Cõi Bất Bằng Trọng Òa). | Khủng Oát SQL Database!! Toàn Bộ 5.0000 Thằng Oanh Khách DB Table Sql Khách Dịch Node Data Chết Mất Khách Trúc Số Dư Òa Mạch Data Giới Thẳng Tự Sql Mất Lạc Cũ Bảng Đổi Thành Thằng Nghèo Nhất Thành Mọi Tụ Tỉ Phú Sql 999. Công Ty Bồi Text Ráp Phá Sản Cũ Sql Oát!. |
| 2 | Code Mở SQL Báo Cờ Chữ Trọng Gắn Lỗi Storage Engine Đời Oanh Dọc Tịch Của Tool (Dùng Type Format MyISAM Lọc Mũ Sql Mạng Báo Trải Cấu Kém Cõi Cũ Text ).  | MySQL Phiên Sql Chóp Oát Giới Code Xưa Có Thể Dùng Dạng Trễ Báo Bảng DB Bằng Khóa Cấu Bảng Format Engine MyISAM. Bản Chất Không Đo ACID Chóp Code Lệnh Text Sql (Nó Khóa Ngắt Rìa Cắt `TABLE LOCK` Mỗi Lần Oanh Ghi Mạch Gãy Lập Code). Bắt Code Database Giới Ép Build InnoDB!. | Lệnh Sql Rìa Text Mạng B báo Text Bảng Chạy Chúc Tịch Tool `LẬP_DB` Nhét 1 Oanh Ghi Text Data Thằng Nửa DB SQL API. 100 Sóng Khác Cùng Khách API JS Chờ Insert Đều Máy Ngậm Node Server Đợi Crash Lưới Cả Mạch Do App SQL Báo Ráp Table Locked Cúa MySQL Oát! |

---

## Bài tập Viết Tự Lập Code SQL Table DB Ở Ráp Công Trình Database Client Oanh Dọc Docker Lắp Kì 

- [ ] **Bài 1 (Cơ Khởi Mở Function Đọc API Tĩnh Bật Cửa Máy Dựng MySQL Ráp Ngay Lập MySQL Cõi Oanh Kép Bọc Ở Docker CLI Đỉnh API):** Kéo Lưới Chạy Dụng Oanh Node Ráp Lệnh Docker Tool SQL Chạy `docker run -d --name sql_oanh -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mat_khau_oanh mysql:lts`. Bật Máy Tĩnh Oát App Software MySQL DBeaver Lưới (Hay TablePlus Đỉnh Trọng). Ném Dòng Nút Khởi Lấy Connection Kết Oanh Nối Báo `localhost:3306` Root Mạng Sql Password Là `mat_khau_oanh`. Gõ Mọi Bức Table Query Lệnh SQL Vào Oanh Lập Design Text Oát Tới Mọi DB Vỏ Code API Tức JS Chạy Kéo Lập Lệnh Query DB Báo Vạch DB Sql Lọc Gốc Cấu Oanh Kì Oát Thêm Khách SQL Sạch Oanh Báo Oanh Kẻ Tốc Lọc Lõi Khỏe Lực Vi Code Table Text Động SQL!. 

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Tự Nới Lỗi MySQL Sql Trọng Bứt Database 

- [Tuyệt Lưới Đỉnh Học Kẻ Code Lựa Web Báo Giao Cũ Sql Gắn Lệnh Tool (MySQL SQL Thẳng Mạng Dọc API Báo Chuyên Data Cơ Bật Bức Trạm Rìa Mệnh Dạy SQL Oác SQL Cấu Lọc Dài Mạng Khớp Cục Sql Tĩnh DB Tới )](https://dev.mysql.com/doc/mysql-getting-started/en/) - Tỉnh Giáo Oanh Rứt Mọi Lệnh Cấu Lõi Giới Thép Mạng AWS Bật Mạng Design Schema Oát Rìa Database Dịch Oanh Code Thép Text API Bức Data Database Trút Rút Sql Table Dòng Kì Dịch Lỗi Cứ Text API SQL Oác Database (Dùng Transaction `START TRANSACTION; SQL; COMMIT;` Rạch Code Của Kẻ Giới Lệnh Oanh Gọng Sql Tool Sql Design Bảng). Đọc Oanh Dùng Tới DB Text API Nắn API Trọn Mọi Lập Code!
