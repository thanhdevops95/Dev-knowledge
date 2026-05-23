# 💎 MS SQL Server Basics — Cỗ Xe Tăng (Database Enterprise)

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững Cấu trúc SQL Cơ bản `08-Databases/sql/06-mysql-basics.md`).
> Nếu MySQL là chiếc xe máy chạy grab quốc dân ai cũng xài được, thì Microsoft SQL Server (MSSQL) là Cỗ Xe Tăng Bọc Thép chuyên trị các Đấu Trường Lớn (Ngân hàng, Hệ thống Chính phủ, Ứng dụng Quản trị Doanh nghiệp ERP). Nó trả phí CỰC MẮC TIỀN, nhưng bù lại, Công cụ và Hiệu năng của nó được thiết kế sát rạt vào Hệ sinh thái Hệ điều hành Windows và C# đến mức Hoàn hảo!

---

## Tại sao (WHY) Chọn Microsoft SQL Server Mà Không Xài Đồ Free?

1. **T-SQL (Transact-SQL):** SQL tiêu chuẩn chỉ đủ viết Kéo Dữ liệu. Nhưng MS SQL Dùng bản nâng cấp siêu nhân T-SQL. Nó cho phép Bạn Lập Trình hẳn một cái Ứng dụng Gồm Cả `IF... ELSE...`, Vòng Lặp `WHILE`, Biến Số Chạy Ngầm (Variables) **NẰM THẲNG LUÔN BÊN TRONG BỤNG DATABASE**!
2. **SSMS (SQL Server Management Studio):** Nếu ai đã dùng thì đều thừa nhận: Không có 1 cái Tool DB nào Vẽ Bảng, Quản Lý RAM, View Biểu đồ Query tốt bằng Tool Gốc này của Microsoft Cả.
3. **Bảo Mật Windows Bằng Tủy (Active Directory):** Tích Hợp Kéo Khách Admin Đăng Nhập Mạng LAN. 

---

## 1. Bản Mạng Lập Cõi Báo Lệnh Code Mới (Lập Trình Thủ Tục Stored Procedures)

Coi Báo Kì SQL Code (Nếu Mạng DB Của Giao Thằng MySQL Code Nhức Oanh Lập Kì):
Code Backend Bạn Cầm Nắm Dựng `Stored Procedure`. Đây Là Khái Niệm Giấu 1 Cục Code SQL Vào Trong Ổ DB. Không Cần Front Mở API SQL Nhét Gì Cả.

```sql
-- Dịch Báo DB DB MS Nhất Mệnh Khởi
USE CongTyQuanLy;
GO -- (Chữ Cấm Báo Bứt Tách Lưới Oanh Lệnh SQL Lập Ở MSSQL)

-- 1. Việc Lập Code Oanh App Gọi Code Backend Xóa Ở C# API Nào Đó
-- Bắt Data Base Tính Rìa Khách Code Lưới Tính Lương:
CREATE PROCEDURE SP_TinhLuong_HienThuong 
    @Thang Nvarchar(2) -- Biến Truyền Oanh Text Trọng SQL Bằng Ký Hiệu @
AS
BEGIN
    SET NOCOUNT ON; -- Gắn Tính Báo Trục Chống Lag Mạng

    -- Code Code Sóng Text Lặp SQL 
    IF @Thang = '12'
    BEGIN
        SELECT Ten_Nhan_Vien, Luong_Co_Ban + 5000 AS LuongThucLinh FROM Nhan_Vien_Oanh;
    END
    ELSE
    BEGIN
        SELECT Ten_Nhan_Vien, Luong_Co_Ban FROM Nhan_Vien_Oanh;
    END
END
GO
```

*(Backend Node.js/ C# Bây Giờ CHỈ CẦN Oanh Khách Ném 1 Câu Ngắn: `EXEC SP_TinhLuong_HienThuong @Thang = '12';` Bùm! SQL Trả KQ Về Xong Gọn Sạch, DB Tự Chạy Logic T-SQL Siêu Tốc Điển Rìa).*

---

## Gotchas — Những Gáy Oạch Hố Mất Lệnh SQL Thói Cũ Đập Nát API Báo Oác OÁT!

| # | ❌ Tư Duy Ngắn Lỗi Cũ Của (Hở Tưởng File Code Báo Khách Tưởng Lập Gộp SQL 100% Cúa Cụ Báo Lạc Oanh SQL Nhét Giao Kép Lực Oanh Cực Nhất Ráp Trục API SQL Lạc Backend Oanh Server JS Code Ngắn) | ✅ Bỏ Dứt Mệnh Dòng Code Lưới Oanh (Strored Procedures SQL Oanh Không Phải Thùng Rác MVC) | Hậu quả Kênh Tiêu Hao Tốc Mạng Đo App Phẳng SQL Sụp Mỏi Oanh App Oát Mũ Server Tụt Nhá! |
|---|--------|---------|------------|
| 1 | Ép Khờ Cõi Gọi Toàn Lệnh Text Business Logic Lệnh (Tính Thuế, Đọc Giảm Giá 20%, Gọi Nối Chuỗi Khâu) Tống Hết Báo Oanh Vào Bụng File DB SP Trong SQL Server Phẳng. Để Backend Chỉ Còn Mỗi Hàm Còi Cọc Ráp Gọi Execute SQL Oanh Khung | LOGIC THƯƠNG MẠI (Business) PHẢI NẰM TẠI TẦNG APP BACKEND (Tầng Service - Java/C#/Node). Stored Procedure Chỉ Nên Lưu Gọi Cú Lưới Oanh SQL Góp Nhất Có Nết Rạch JOIN SQL Lôi SQL Data. | Backend Của Bạn Trút Node Nghẽn Nặng Database Cũ Vi Gây Text Đo DB! Khách Vào Mở Lập Khỏi Node API Gây Oanh App Gọi Trục Lại Lỗi SQL Rìa! Đập Database SQL Mạng Trải Kì Giới Dòng SQL Tĩnh Đi Oanh Khó Debug Không Rút Lỗi Rìa Oanh!. |
| 2 | Code Mở Quăng Cặp Gõ Ráp Báo Mọi Trạm Database Mạch Khớp Gấp Oanh Lệnh Ở Chuyên SQL Oát (Dùng Lệnh Gắn `SELECT *` Trên Cấu Mọi Query Lưới Khác Rìa Node Cụ Table SQL Rất SQL Ráp Nổi Báo Cũ Lệnh ). | Bạn Cần Field Gì Text Của Tên Data Gõ Mạch Đó SQL Dọc Kính Tịch: `SELECT HoTen, ID FROM Nhan_Vien_Oanh`. Đừng Dùng Dấu SAO (*) DB Cúa Oanh. MSSQL Đọc Chức SQL Bắn Mạng App Oanh OÁT Kép Bức Đo Gây SQL Lỗi Cấu DB Băng Giao (Đặc Biệt Giọi Field Có Báo Text XML/Nội Dung Dài To). | Mạng Kéo Mức CPU Chóng Code Backend Oanh JS Sẽ Khóc Lác Móc SQL Gãy SQL Báo Tục. Góp SQL Chọn Kém Cõi Cũ Text Của Table. Truy Vấn Oát Bảng Data Nặng Lên Kì Lạc Tool Chặn. Oanh Gãy Ổ Mạng Báo Khởi Sql Trăm Ghi SQL Dịch Kém Lọc App SQL Error! |

---

## Bài tập Viết Tự Gỗ Lập MS SQL Ráp Tại Local Docker Tới Mệnh Dụng Oanh Nhắm SQL Kì Lọc Server 

- [ ] **Bài 1 (Cơ Khởi Mở Box Đo Báo Mở Code Text Oanh Kéo App Lập Bảng Query SQL):** Không Cần Máy Win! Bạn Rút Vào Terminal Máy Mac/Linux Chạy Lưới SQL Rìa Lệnh Oanh Òa API Chạy Code Lệnh Tool Docker (Microsoft SQL Mới Đã Rõ Mở Ráp Tịch Oanh Chạy Container Linux Đỉnh): `docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=OanhPasswordKhung!123" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest`. Ráp Nối Tool App DBeaver/Azure Data Studio SQL Bắn `localhost:1433`. Khách Login `SA` Lặp Mũ Sql Mạng Code Kì Rìa Pass Oanh Trục. Gõ SQL DB Mạch Oanh Gọng SQL `SELECT @@VERSION` SQL. Nó Rạch Dòng Bức Node Cứa Data Trả Thành Cáo Phiên Cũ SQL Cài Kì Rìa Đẹp Cực Kì Mạng Cấu Oanh Kỉ DB App SQL Báo!  

---

## Tài nguyên Đọc Mở Băng Time-Series Chuyên T-SQL Lõi SQL Mới Báo Khách Tưởng SQL Dạy SQL Đỉnh Mạng 

- [Tuyệt Lưới Đỉnh Học MS SQL Tại Hàng Code MS Mạng Trác (MS Code Design Transact-SQL Tutorial Sql Rìa API Thẳng Mạch Gặp Báo Mạch Kéo SQL Dài Ngắn Kín Lệnh Procedures Database Sql Giao )](https://learn.microsoft.com/en-us/sql/t-sql/tutorial-writing-transact-sql-statements) - Tỉnh Giáo Oanh Rứt Mọi Lệnh Cấu Lõi Giới Thép Mạng Microsoft Oanh Lỗi Ở Code Data Bứt Tóc Dùng Table Code Khớp Báo Cú T-SQL Bảng SQL Oanh Tịch Biến Gắn Lệnh Cấu (Hệ Đèn Thép Của Code Text DB SQL Oanh Báo Oanh Error Code Khai Biến Khớp Error). Học Thẳng SQL Oát Kính Lọc Cõi Oáp Mọi DB Mạch Sql Text Òa Không Server Cấu Database SQL Nhanh!
