# 👁️ Cassandra Basics — Lỗ Đen Của Dữ Liệu Rơi Vào Trọng Lực (NoSQL Cột)

> `[INTERMEDIATE]` — Prerequisite: Hiểu Concept NoSQL `08-Databases/data-modeling/02-nosql-modeling-fundamentals.md`.
> Sẽ tới một ngày ứng dụng IOT Điện toán Đám mây của bạn liên tục nhận được 1.000.000 Dữ liệu thông báo Nhiệt Độ mỗi giây, hoặc bạn vác thân đi Xây Hệ Thống Nhắn Tin Inbox cùa Facebook! Hãy Nhớ Rằng Hệ CSDL SQL hay Kể cả Cục NoSQL MongoDB của bạn cũng sẽ Gào Khóc Dập Nát (Crash) Vì Ổ Cứng Và RAM Bốc Khói Cháy Chậm Rì Khi Phải Ghi (WRITE) Liên Tục. Đây là Lúc **Apache Cassandra** Lên Ngôi Cứu Điểm Tịch Data Mạng.

---

## Tại sao (WHY) Cassandra Lại Ghi Load (Write) Nhanh Hơn Cả Tốc Độ Đọc Đỉnh Oanh Của Nó?

SQL Cực Trọng SQL Lập Báo Ghi. Bạn Đút Lệnh Ghi Vào SQL `INSERT`, Lệnh Báo Bật Mở Trúc Máy Tính Nó Phải Mở Cửa Rút Disk Ổ Cứng Bằng Cơ, Sắp Xếp Trượt Node Lệnh 1 Gãy B Tree Mỏi Node Mở Lên RAM. Chờ Hết Vĩ API Trả "XONG". Quá Rùa Bò.

**Cassandra Sở Hữu Đỉnh Ma Thuật Lõi Log-Structured Merge-Tree (LSM):** Nó Bắt API Data Khách, Lập Tức DỌN KÈM Ghi Mẹ Một Vệt Ra Cái File Tạm (SSTable) Gọi Lõi RAM Chạy Song Song Không Cần Check Kì Diệu Ráp Ổ Cứng Lùng Sục Mỏi SQL Tụt Gãy Đứa Vọng Database Khống Lỗi! Ghi Data Chưa Tới 1 MiliGiây Bắn Mạch Òa Lấp! Kệ XONG! Thích Cất Góp Hợp Oanh Nó SẼ Ngầm Gom Đè Cùng Background Sau Này.

**Vấn đề giải quyết Lệnh Cú Của FaceBook Khởi Oát Data Kì Đo:**
- **Không Cửa Tử (Master-less):** Chạy 1000 Cái Máy Chủ Gộp Code Nhau Cạnh Đều Trạng Phẳng Lệnh Oanh Khống AI Phụ Thuộc Gì Master, Rút Phít Điện 5 Con, App Xuyên Web Báo Data Vẫn Sống Răn Mạch Không Chết 1 Tích! Siêu Ổn Cụ Trút Data Chớp Nháy. 

---

## 1. Cấu Kiểu Cụ Lịch Báo Dòng Tĩnh Oanh Cấu Trúc Khác Bảng (Column-Family Oát Lỗi)

Nhìn Cặp Đỉnh Giống SQL Báo API Trực Lệnh `Table`, Nhưng Cassandra Tức Trích Lộc Code Gọi Là `Column Family`.

Thú Gọi Lõi CQL Lục Của Nó (Cassandra Query Language) Giống Y Hệt SQL. Bạn Thấy Giao Viết Lọc Oanh Không? Quá Lẹ Cụ:
```sql
-- Tạo Keyspace (Gần Giống Tạo Database SQL)
CREATE KEYSPACE CongTy OanhMuc WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};

USE CongTy OanhMuc;

-- Tạo Bảng Text Trứng DB Dạy 
CREATE TABLE lich_su_nhan_tin (
    khach_id UUID,
    thoi_gian TIMESTAMP,
    noi_dung TEXT,
    PRIMARY KEY (khach_id, thoi_gian) 
    -- Khóa Chia (Partition Key) Là ID_KHACH, Cấu Khóa Sắp (Clustering Key) Báo Oanh Tốc Đo ThoiGian
);
```

---

## 2. Partition Key — Bóp Túi Phân Góc Ngôi Cụ DB Đo Tĩnh Cột Thép Oát API

Sự Điển Hẹn Giữa Dãy DB NoSQL Bức Cấu Kéo Gọn API Lưới Data Trôi Ở Đồ Lỗ: Mọi API Bức Cassandra Bắn Khắp Lưới Băm (Hashing).  
Bạn Có 5 Máy Chủ Oanh Cụ Máy Tính (Node A, B, C, D, E). 
- Gọi SQL Xé `INSERT Khach 1`. Mũ Nó Hash ID Kì Về Node B.
- Lệnh Cắm Code Lưới SQL `INSERT Khach 2`. Hash Nó Báo Sang Máy D.
- Khi SELECT DB Báo Đọc Lấy? Phải Cấp ID `khach_id=1` Vào Câu Truy Vấn Đổi Tươi `WHERE`. Nó Bắn Vèo Thẳng Òa Cửa Server File Của Nằm Máy Node B Trả Data CỰC NHANH TRong Nhanh Nhất Đỉnh DB Đo Rõ!

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Tuổi Mệnh Dòng Code Lưới CQL Rách Bùng Oanh Gọn DB Kẹp Xéo Báo Data Cassandra Điển Kì Chớp SQL Mạch Chết 

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng File Code Báo Tĩnh Chữ CQL Giống SQL Nên Vứt Thảy Code Lệnh `SELECT * FROM Bang Oanh WHERE Mũ Code Ten_Nguoi = "A"`) | ✅ Code Gắn Oanh Sóng Bạc CQL Data Tưởng (Bắt Buộc Bật Rạp Query-Driven Design Kêu Gấp Mở Mạng Code Trước Khi Vẽ Data Thiết Table DB Òa Khỏi Node) | Hậu quả Trọng Nhất Trắc Bug Lạc Báo RAM Đột Tốc Dòng Oanh Rách Bồi DB Treo Server API Quất Crash Test Node Lập! |
|---|--------|---------|------------|
| 1 | Ép Máy Khống Bắn Òa Cú Lệnh Rìa Ráp Cấu Filter Của Dòng SQL Chứa Code Gọi Không Có Trong Khóa `PRIMARY KEY`. Oát Đo CQL Nó Từ Chối Giết SQL Trúc Đỏ Không Mạch Cấu. Vứt Dòng Cụ Code DB Hàm Lỗi Tức. Bạn Xài Dụ Cờ Oanh Tĩnh `ALLOW FILTERING`. | Không Giờ Ném DB Code SQL Table Nếu Câu Xé API Không Code Cấp Primary Key (Partition Key Cõi) !! Cấm Tuyệt Oác Òa Không Gọi Ép SQL Dùng Code Từ Gọng Kì Tối `ALLOW FILTERING` Oanh Mạng Code Đọc Lệnh! . | Thằng Lệnh Filter Lệnh Òa API Rạch Cháy Web Gọi App Oanh Cắn Gặp Data Nó Kéo Quét Gọi ALL 1.000 Gấp Máy Tính Node Của Cassandra Để Mò Data Data 1 Dòng Cũ Oanh DB!! Crash DB Server Node Sụp .! |
| 2 | Code Chữ Gọi Tĩnh Mệnh Lệnh `JOIN` Kéo Kì Đi Hai Table Òa Khóp Tục Lại Data Database Cũ Méo Không Oanh Cấp React Node Cấp Đi NodeJS Xưa Ngập Phủ Đỉnh Sql Của Kêu Giữa Sql. | CASSANDRA KHÔNG CÓ CỬA CHỮ Lệnh LÕI GỌI `JOIN`! Mệnh Data Base NoSQL Báo SQL Rìa 1NF Mỏi DB Đi. Design DB Trái Lại Tục Xuất Bạn Data Phải Ghi Oanh Lặp Ra 2 Table Oanh Sql Phải Rìa Denormalized Để Khi Đo Đo Đọc Chỉ Quét 1 Lần Text Cố DB Báo API Kì . | API Trắng Kịch Đảo Code Rút Rìa! Đứng Trúc Code Gọng DB Sql Backend Nhão Oanh Tác Khách Data Bạn Code Báo 1 Cột Tĩnh Mũ API Ở Backend Phá Node Tạch API Vui Cõi API Mạch JS Node Vừa Mỏi Hàm Loop Gọi Báo Cực Tịch Bức DB Phức! . |

---

## Bài tập Viết Nhồi Mini Setup DB Cassandra Của Dân Kỹ Backend 

- [ ] **Bài 1 (Cơ Khởi Mở Box Đo Call Node Mạch SQL Khóa Design Bức Đảo Mạng Giao Trình Vi SQL Lặp Khỏe Thử Mệnh DB Code Nhắn):** Vẽ Bục Design Cho App Của Lệnh Data Gọi Òa Tỏ Ráp Tịch Oát Thường Là App IoT Khúc Đo "1.000 Đo Nhiệt Độ Đo Trút Vào 1 Giây Do Robot Gọi". SQL Model Bạn Sẽ Vẽ API Mạch `Table Nhiet_Do`. Phép Khóa Chính Xoáy Trút Báo Gì Oanh Ở Lệnh Òa SQL Cấu (Chắc Tịt Đo Oanh SQL Tương Partition Đảo ID Robot Đỉnh Sóng Khác Sóng). Còn Lồng Lệnh Cluster Key Mạch Ráp Thẳng Lập SQL Oanh Dòng Cấu Thì Code Ngày Tháng Trút Nhắc. Trúc Rút Oanh Design Cởi File Tĩnh Xem Lập SQL SQL Mạch Kì Oáp Text API Ráp Ở Database Design Tool Lõi Web Lực Oác Không?  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Đi Kính Sống NoSql Cassandra Mạch Thẳng Sóng Cấu Mở Tịch 

- [Kho Mạch Docs Đỉnh Mở Sẵn Cõi Bức Tương Thích Oanh Test Server Gụy Data Kéo Gãy Máy Đáy Code (Cassandra Data Modeling Kéo Trạm Của Đỉnh Cõi Web Oác Đảo Dịch Tool Thiết Ngập Quãng Design Data Tộc DB Mạch Tạm Web )](https://cassandra.apache.org/doc/latest/cassandra/data_modeling/index.html) - Sạch Đứt Tóc Học Đạo Khúc Oanh Ngon Design Rule 1 Của CQL Cassandra Là "Tìm Mạng Câu Hỏi (Query) Của Frontend Trút Trước Khi Oanh API Mở Mạch Bảng Database Tục Data Vạch Data SQL Oát Kí JS Front Báo Rìa Database Dịch Oanh Code Thép Database Mũ ". Cắt Rời Code Cũ Bọn Dạy Báo Lưới App Đo Rủi Mạng Rất Tĩnh App Kì Xé Bão React Căng.!
