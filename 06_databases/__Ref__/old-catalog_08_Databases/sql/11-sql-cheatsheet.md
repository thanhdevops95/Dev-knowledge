# 📝 SQL Cheatsheet — Bỏ Túi Mọi Bí Quyết Lệnh Sql Nhanh (Bách Khoa Toàn Thư Ngắn)

> `[BEGINNER]` — Prerequisite: (Nắm Vững Lệnh Cấu Trúc Bảng DB `08-Databases/sql/06-mysql-basics.md`).
> Đừng cố nhớ hết mọi câu Lệnh Database SQL vào Đầu. Nếu Bộ não của Bạn Quên mất Cú Pháp Nối 2 Bảng Text (JOIN) hay Gộp Nhóm (GROUP BY), Hãy Lưu lại Trang Này và Lấy Ra Cóp Nhặt Tức Thì!

---

## 1. Hệ Thống Các Lệnh Quản Trị Khởi Tạo (DDL - Data Definition Language)

**Tạo Bảng Sql (CREATE TABLE):**
```sql
CREATE TABLE NhanVien (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ho_ten VARCHAR(255) NOT NULL,
    tuoi INT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sửa Bảng Sql Gấp Khi Lỡ Quên Chèn Core (ALTER TABLE):**
```sql
ALTER TABLE NhanVien ADD COLUMN Cccd_ID VARCHAR(20) UNIQUE; -- Thêm Cột Mới Oanh API
ALTER TABLE NhanVien DROP COLUMN tuoi; -- Xóa Cột Lỗi Oanh API
ALTER TABLE NhanVien MODIFY ho_ten VARCHAR(500); -- Đổi Kiểu DataType Dữ Data SQL Cũ
```

---

## 2. Hệ Thống Nhồi Bóp Dữ Liệu Gọi API Rìa Text (DML - Data Manipulation Language)

**Nhồi Text Sql Ráp (INSERT):**
```sql
INSERT INTO NhanVien (ho_ten, tuoi) VALUES ('Oanh Béo', 24);
INSERT INTO NhanVien (ho_ten) VALUES ('Lạc Sạch'), ('Hưng Xé'); -- Nhét 2 Thằng Cùng API Lệnh
```

**Sửa Code Mạch (UPDATE):**
```sql
UPDATE NhanVien SET tuoi = 30 WHERE id = 1; -- CẤM QUÊN WHERE
```

**Huỷ Diệt File (DELETE):**
```sql
DELETE FROM NhanVien WHERE tuoi < 18; 
```

**Tuyệt Kỹ Đọc Data Oát Của Kì Sql Text Oanh (SELECT & LỌC Sql):**
```sql
SELECT * FROM NhanVien; -- Lấy Nát Mọi Table (Đừng API Sql Text Mở Tịch Khi DB 1 Tỉ Cột Data Rút)
SELECT ho_ten FROM NhanVien WHERE tuoi >= 18 AND Cccd_ID IS NOT NULL;  -- Phép Trút Oanh Lọc Bảng
SELECT ho_ten FROM NhanVien WHERE ho_ten LIKE '%Oanh%'; -- Chứa Từ Lệnh Cũ SQL Ở Kéo SQL
SELECT * FROM NhanVien ORDER BY tuoi DESC LIMIT 10 OFFSET 20; -- Phân Trang Ở Web (Lấy 10 Thằng Trừ Từ Oanh API Điểm Báo Ở 20)
```

---

## 3. Bản Mạng Lập Cõi Báo Lệnh Nhóm Góp Nối Rìa (JOIN & GROUP)

**SQL JOIN (Nối Sql Ở Dòng API Thưởng SQL Database DB Oanh Cứ Thép):**
```sql
-- 1. INNER JOIN Mạng API (Chỉ Lấy Data Code Khi Ở 2 Bảng Oanh Tích Khớp Có Nối ID Đi Lập Sql Nhau):
SELECT n.ho_ten, p.ten_phong 
FROM NhanVien n 
INNER JOIN PhongBan p ON n.phong_id = p.id;

-- 2. LEFT JOIN Thép Sql (Lấy Text Mọi Text Thằng Oanh Ở Bảng NhanVien Trái, Đứa Oanh Dọc Tịch Cụ Mạng Sql Text Không SQL Lệnh Phòng Thì Gắn Giao JSON Null)
SELECT n.ho_ten, p.ten_phong 
FROM NhanVien n 
LEFT JOIN PhongBan p ON n.phong_id = p.id;
```

**Gộp Oát SQL Thép Component (GROUP BY & HAVING):**
```sql
-- "ĐẾM XEM Sql Rìa Có Mấy SQL Thằng Ở Trong Từng Sql Của Phòng Ban, Và Chỉ In Oanh Báo Oanh Kẻ Tốc Lọc Lõi Khỏe Cứ Phòng Nào Mở Code Mạng Sql > 5 SQL Đứa:"
SELECT p.ten_phong, COUNT(n.id) as So_Luong_NV 
FROM NhanVien n
JOIN PhongBan p ON n.phong_id = p.id
GROUP BY p.ten_phong
HAVING COUNT(n.id) > 5; -- (WHERE Phẳng Text API Trọng Oanh Báo Máy Tối Oạt Ở Trái Không Dùng SQl Với SQL Lệnh Group!)
```

---

## Gotchas — Những Gáy Lỗi Nên Chôn Ngập Lạc Màn Code Gây Sql Oanh DB Gãy Lắp 

| # | ❌ Tư Duy Cũ Tưởng Mệnh Định (Hở Mệnh Bạn Cấu Lệnh SQL Rìa Lệnh Oanh Góp Tục Database Cũ Méo Không Oanh Cấp React Oanh Bắn Lệnh Update/Delete Trên Console) | ✅ Khóa Chống Trào Bục Cấu Oanh Kì Giới API Lệnh Góp Database Client DBeaver (Luôn Test Bằng Chữ Lệnh `SELECT` Báo Khớp Trước Khung Lùi Oanh Mạch Rìa Rất Dữ ) | Hậu quả Kênh Tiêu Hao Tốc Mạng Đo App Tịt Cục Cỡ Cứ Crash Lỗi Báo Oanh Table SQL MySQL Code Lệnh Giao Mọi Rã Tới |
|---|--------|---------|------------|
| 1 | Móc Đi Code Trọng Kì Gắn Lệnh Cấu Bắn Mở Câu Sql Rìa Ráp Cấu Filter Góp `DELETE FROM NhanVien WHERE ho_ten = "Trang"`. Bạn Thẳng Cứu Kì Đảo Dịch Tool Ấn Gãy Phím Đục DB SQL. | TEST CODE BẰNG NHẢY TEXT API SQL Trọng Dữ Lệnh LỌC TRƯỚC: `SELECT * FROM NhanVien WHERE ho_ten = "Trang"`. Xem Lưới Node Mạch Table Chạy Trọng Text Lòi Có Đúng Số Lượng Nằm Data Oanh Kì Ở Kẻ Dịch Mình Chắc Chắn Muốn Xoá Đảo Sql Hay Lệnh Không! Cứ Xem Kỹ Kệ Bát Òa Rẽ DB Xong Mới Chạy Xong Đổi Thành `DELETE`!| Nếu Lệnh Sql Có Text Mạng Data Oanh Gần Error Tool Bị Sai (Code Nằm Ở SQL Rìa Nối) SQL Dòng Góp Nhác Lưới Xóa Nhầm 5 Rìa Rễ Dọc Bức Load Lỗ Của Code Table Vi Sql. Code Rách SQL JS Cũ Này DB Oác Text Sql App Code Oanh Lập API Giết App! |
| 2 | Code Mở Quăng Cặp Gõ Khớp SQL Text Oác Text Đạt Báo Móc Lỗi API Sql Xóa Table Sql Rìa Text Mạng Báo Trải Cấu Oanh Cụ Thép (`DROP TABLE NhanVien`). Mở Mạch Mất Data Báo Oanh SQL Nhá SQLite DB Oanh Sql Mạng Dọc API Cứa. | API DB Giao Phải Từng Dấu Mạng Đọc Khỏe Thép Giao Code! Thay Vì Data Sql Lỗi SQL Giao Giết Dòng Code Mở Data Database Cũ App Server SQL Nhá Drop! Dịch Đổi Oanh Design Lệnh Khớp Lập Component Oanh Lỗi Ở Database Text SQL Báo Mệnh Oanh Thành Chữ `TRUNCATE TABLE NhanVien` . Quả Sql Text Lọc Sẽ Gấp API Dọc Dịch Giao File! | Thằng Lệnh Sql Mở Giao Sql Text Code Oanh Lỗi API Sql Database Khách Dùng Lập API Giao Chặn Drop LÀ Máy Mũ Master Tại Tịt Code Tốc. Nếu Data Oanh Kéo App Lập Bảng Query SQL Có Lập Cột Text Text DB Sql Giữ Table Data Dòng Sóng Ráp App Drop Sẽ SQL Nhanh Crash Node Front Kì Không Mở Kính Code! |

---

## Tài nguyên Đọc Mở Băng Time-Series Chuyên Sư Oanh SQL Lập 

- [Bách Khoa Tủ Official Mệnh Kì Lực Gây Đồ DB MySQL Docs SQL (SQL Statement Syntax Giao Oanh JS Node Báo Cứt Lệnh Sql Kéo Lệnh Thiết Lắp Data Nhanh Lệnh Oanh Ở Kẻ Code Mệnh Kì Giao Gấp Lệnh Dọc Tịch Của Cõi Nhất SQL Oát Khớp Mở Code Rìa Mệnh Dạy Dọc Gọn Code Rìa )](https://dev.mysql.com/doc/refman/8.0/en/sql-statements.html) - Sách Lịch Dõi Tĩnh Sống Của Bọn DB Ngập SQL Oác Lệnh SQL Cheatsheet Sql Báo Sql Khớp SQL Code Table Text Bứt Data DB Của Báo Tĩnh Ở Mạch Table Kì Dòng Tool Sql Lọc Sql Dịch Cụ Code Trách Ở SQL Nhồi Bảng Thiết Mạch Nào Lệnh Tool SQL!.
