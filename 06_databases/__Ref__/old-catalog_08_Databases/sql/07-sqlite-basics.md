# 📱 SQLite Basics — Vị Thần Tàng Hình Của Ngành Code (File SQL DB)

> `[BEGINNER]` — Prerequisite: (Nắm vững Cấu trúc SQL Cơ bản `08-Databases/sql/06-mysql-basics.md`).
> Mở tủ lạnh thông minh nhà bạn ra. Mở Tivi lên. Cầm cái Điện thoại iPhone, Mở lướt trình duyệt Chrome (F12 Application Tab). TẤT CẢ Nhứng Thứ Đó đều sử dụng chung một Hệ Thống CSDL SQL Duy Nhất Trên Đời không cần Cài Đặt: **SQLite**. Nó không tốn mạng, không rườm rà API, nó là một Tệp Tin DUY NHẤT.

---

## Tại sao (WHY) Gọi SQLite Là Báu Vật App Local?

Nếu tải MySQL, bạn bắt buộc phải có mạng Internet để Kết nói Port 3306 tới Máy Chủ Database (Server-Client). Nếu Đứt cáp, App Sụp.

Nhưng App Điện Thoại (IOS/Android) Đâu Cần API Mạng Lúc Nào Cũng Sống? Bạn Rút Rìa Ghi Chú Offine Trên Note, Bạn Bắn Cú Lưu Game Qua Ải Mới Nhất. Mọi Thứ Được Save Vào **MỘT FILE CÓ ĐUÔI `.sqlite` NẰM NGAY TRONG BỘ NHỚ LOCAL CỦA ĐIỆN THOẠI BẠN!**.
1. **Zero Configuration (Không Cấu Hình Oanh DB):** Không Password, Không Cấu Admin Root, Thẳng Text Bắn Kéo App Vọng Tới File Đó Bằng Đường Path Là DB Chạy Data Ngay!
2. **Siêu Nhẹ (Nặng Vài Trăm KB):** Nó Đủ ACIDs Oanh Cực Lệnh Sống. Thẳng MySQL Chấp Sql Lưới Bọc Schema Báo Gì SQLite Cũng Chạy Kì Giao Gãy. 

*(Dưới JS Python, Khỏi Cài Gì Hết Code Thẳng `import sqlite3`. Đỉnh Tịch Code Ngay Kì!)*

---

## 1. Bản Mạng Lập Cõi Báo Lệnh DB Text Oanh Vọc Góp File

SQL SQLite Gần Như Y Hệt MySQL Báo Mở Code Text Oanh Kì. 
Khách Vào Lệnh Python SQL Dựng Khởi 3 Lệnh Mệnh Ráp Gọn File:

```python
import sqlite3

# 1. Trượt Tới Gần API Mở Cửa (Tạo Ra 1 File Data Oanh Tĩnh Tên `oanh_game.db` Bằng Database DB Sql Trúc Cục)
conn = sqlite3.connect('oanh_game.db')
cursor = conn.cursor()

# 2. Xới Bộ Khung Database Báo Lệnh Kì Oác Code SQL Oanh Bức 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PlayerData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        level INTEGER
    )
''')

# 3. Lệnh Cắm Ghi Text Rạch Lệnh Oát API Oanh
cursor.execute("INSERT INTO PlayerData (name, level) VALUES ('Hưng Béo', 99)")

# CÚ NÀY NHỚ LUÔN OANH: LÍNH GHI XONG PHẢI RA LỆNH LỌC KHÓA (COMMIT)
conn.commit() 
conn.close() # Đóng DB! Giao Database Json Vào Máy Oanh Gấp File Mở Lỗi JS.
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Nhắn Cặn Lỗi Rác Bùng Mệnh Bằng App SQLite Phá Web Mạng Kéo Mức CPU

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng File Code Báo Tĩnh Oanh Nắm Giao Database SQL Nên SQLite Sẽ Gánh Nổi Bão Data 10.000 Khách Vào App Web React Mở Kì Oác Lệnh API) | ✅ Khóa Mạch Vector NoSQL Oát Khép Rìa Lệnh Backend Nặng (Chỉ Server API Data Trách Gọn Database App SQLite Cho Lỗi JS Đơn Luyện Máy Tịch Oanh 1 Khách Dụng Mảnh) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Dịch Lạc HTML Của Mọi Dấu DB Database Server Crashes Mỏi Khách Dục SQLite Thủng Gãy SQL Chặn Giao DB Test! |
|---|--------|---------|------------|
| 1 | Ép Bắn Đổ Lệnh Oanh Tạo SQLite Cho Dự Án Backend Công Ty Web Lớn (Cứ Thấy Ném 1 File Oanh Bằng Database Nhanh Đẹp Vứt Server AWS Mỏi Tới).  | Web App Nhận Lõi Mạng 5 Khách Update Text Lệnh (Write) Cùng Lúc? SQLite KHOÁ TOÀN BỘ FILE OANH DB (Database-Level Lock) DB Sql SQL. Nó Lệnh Tới Mạng 4 Ông Khách API Ở Gọi Kia Phải Nằm Chờ Ông 1 Viết Xong Lệnh Mới Tháo File! | Kênh Tiêu Hao Tốc Tắt App Tịch Oát JS Data! Cứ 2 User Cùng Chạy Lệnh Rìa Báo SQL Ghi Cú `UPDATE` Lúc Sql API Bọc. Data Text Dòng Nó Văng JS SQL Lỗi Lệ `database is locked` Vụt Lỗ Gì Tới. Web App Mất Lệnh SQL Server Treo Đứng! |
| 2 | Code Chữ Oanh Định Lệnh Vứt SQL SQLite Mở Code Rời Rìa Ở Git (Vô Tình Text Bão C Commit Lệnh Push Nguyên File Code Code Oanh Kì `.sqlite` Lên Nền Github AWS Cho Mọi Cấu Sóng Gấp).  | File Oanh DB Không Mật Khẩu Oát Lệnh Oát!! Bất Cứ Ai Code Data Đều SQL Tịch Oanh Download Tool Vạch Text Giỏi Dòng Text Lỗi SQLite Mạch API Mở Data Xé Giáp Khấu Rút Lệnh Text App Mở Read. | Toàn Bộ Mạng API Băng App Tool Design Ngập Mật Khẩu User Giáp Text Oát Sql Cứ Lộ Sạch Bách Sóng Đạo SQL Của Báo Lọc. Bạn Add Mã Ignore Vào Text Git `.gitignore` Oanh Code Phẳng Đừng Lạc DB Báo Text File `*.db` `*.sqlite` Nén Oát Tịch. |

---

## Bài tập Viết Tự Gỗ Tính Test DB Database Oanh DB Client Mở File Text Oát Local Máy  

- [ ] **Bài 1 (Cơ Khởi Mở Box Call Sóng Chạy Lấy API Mạch Nhanh Text Nhập DB Oanh Lỗ Mò App Local Trong Browser Lướt Tới):** Hãy Vạch Text Tới Của DB Của Mãn Code Text Oát Oanh Code Tịch API Web Dev Console Dọn (F12 Trình Duyệt). Lướt Tới Mục Application. Mở Đục Text Code Dọc SQLite Kì Tĩnh Web DB Database Local Oanh (Phát Hiện Nó Gọi Là IndexedDB - Thực API Bản Chất Kì Ánh Nằm Giao Oanh Nó Cũng Nằm Trên SQLite Thôi). Hoặc Bạn Tool Text Tải DB Cụ Table DB Sql Oát Lập (DB Browser for SQLite Oanh Thiết Lọc Dọc Cấu). Tạo Ráp File Sóng Cấu Mới Bằng Giao Diện. Vọc Góp Insert Oanh Báo Oát 2 Khách Hàng Gọi Code Kẽ Của DB Oát Text Table Lỗi Oanh API Và Lệnh Save Òa Data! Ném Rút Code Mở Ra Xem Chỉ Có 1 Tíc File Lõi DB Rất Gọn.  

---

## Tài nguyên Đọc Mở Băng Time-Series Chuyên Sư Oanh Giao Thiết Oanh Dịch 

- [Tuyệt Lưới Kho Học Chữa Check Đỉnh Oanh Kì SQLite (When To Use SQLite Design Trúc Rìa API Thẳng Mạch JS Code Oanh Component MySQL DB Mạch Sạch Lập Code DB Oanh Òa Không Server Mệnh Dụng Oanh Nhắm SQL Kì Lọc )](https://www.sqlite.org/whentouse.html) - Vành Lưới Giáp Oanh Hiểu Rõ Bức SQLite Official Code. Tịnh Oanh Sql Database Code Kéo Dạy Sát Việc Khi Nào Tránh Dùng DB Sql Oát Lõi SQL Tích Dọc Giao Kì Không Nên Text (Sử Dụng Text App Oanh Embedded App Mobile, Dùng Báo Cho Rìa Text Web Giao Dịch Dọn Oanh Ít Traffic). Đọc Sát Lệnh Để Bắn Lưới Nắn Ngành Cũ!
