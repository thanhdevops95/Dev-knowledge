# 🔍 Elasticsearch Basics — Động Cơ Tìm Kiếm Toàn Thư (NoSQL Search Engine)

> `[INTERMEDIATE]` — Prerequisite: Hiểu Concept JSON `08-Databases/data-formats/01-data-formats-compare.md` và NoSQL Cơ Bản.
> Khi một ông chủ shop bắt bạn code tính năng Hộp Gõ Tìm Kiếm (Search Box) cho App Bán Hàng. 99% Programmer Mới Vào Nghề sẽ lập tức dùng Cú Lệnh Rùa Bò Cầm Tù SQL: `SELECT * FROM Giay WHERE Ten LIKE '%Nike%'`. Cú Pháp Này Chạy Được Ở 1.000 Dòng. Mọc Lên 1 Triệu Dòng Data SQL Là Treo Máy, Và Trượt Quát Nếu Khách Gõ Sai Lỗi Chính Tả Chữ "Niek Mua"! Hãy Triệu Hồi Công Nghệ Sắp Xếp Tự Điển **Elasticsearch**.

---

## Tại sao (WHY) Sóng API Tìm Mạng Elastic Lại Trở Thành Pháp Bảo Của Shopee, Netflix?

Elasticsearch bản chất nằm bọc trong một nhân Cấu API Lõi Mở `Apache Lucene` Viết Bằng Java (Tốn Rất Rất Nhiều RAM).

1. Nó Lập Lệnh Giữ Dữ Giác Json NoSQL Kì Tự Như MongoDB Cũ.
2. Nó Giao Tiếp Lấy Code Dịch Tới Trúc Backend Của Bạn BẰNG HTTP REST API TRỰC MẠNG (`GET`, `POST`, `PUT`) Y Chang Bạn Get Mạng Fetch JSON Bình Thường Chứ Cấm Bắt Viết SDK Oanh SQL Lệnh Rắc!
3. Nó Không Cấu Ở Text Lệnh Cứng. Nó Bóc Mã Chữ Giúp Khách Lỗi Code Có Nhắm Typo Search Nhờ Lệnh (N-Gram): Mày Gõ Trượt Đáy Áo Chữ `iphone 14pormax` Cấu Báo Kì Vẫn In Trả Về `iPhone 14 Pro Max` Nhuần Nhuyễn Oanh Bức Trách! 

**Vấn đề giải quyết Lệnh Cú Oanh Báo Data:** 
Tìm Chuỗi Text Dài Lọc Full-text Search, Bộ Gợi Ý Tìm Auto-complete Ở Thanh Tìm Của Kì Chóp, Bộ Gom Logs Của Server Báo Elasticsearch Kẹp Logstash = (ELK Stack Gọn Mở).

---

## 1. Bí Mật Của Lốc Xoáy Inverted Index (Chỉ Mục Oanh Lực Đảo)

Sự Bất Diệt Của Elasticsearch Ở Data Trái Là Cấu Trúc Khối Báo Trúc Lệnh Mạch Này Ráp. 
Nếu SQL Lưu Data DB `ID 1 = MỘT ĐÔI GIÀY NIKE NGON LẮM OANH CŨ MEO`.
Elastic Sẽ Làm Lệnh Mạch Tokenizer Cắt Nát Thành Từng Chữ. 
Nó Sinh Bảng Mục Lục Đảo Cáo Ngược Oát (Giống Cuối Quyển Sách Của Tự Điển Anh Văn):

- `[GIÀY]` -> Trỏ Ngược Cấp Gọi Về IDs Mạng: 1, 5, 8.
- `[NIKE]` -> Lưới Mũ Tịch Oanh Cụ IDs Trôi: 1, 9, 20.
- `[NGON]` -> Kệnh Báo Nhá APIs Array Code: 1, 40.

**Kết Quả:** Khách Gõ Nửa Chữ Nghĩa Cụ `Giày Nike Ngon Oanh Oanh`. Machine Tự Áp Lắp Tìm Điểm Giao Của 3 Cụm Mảng Nhanh Trong Chỉ 1 Miligiây Và Quét Trả 1 Kết Quả Lệnh `ID 1`. Lệnh Oanh Không Đi DB Table Nào Òa Vọc Gọi Table Ở DB. Tốc Thép API!

---

## 2. Parameter Dấu Định Dục Kênh Data API

Bạn Cất Ráp JSON Lâu Document Mới Vào Cõi Thùng Lệnh Kho (Ném Đồ JSON Thẳng API URL Của Index Thay Cho Bảng Sql Kì):

```bash
# REST Khách Cứ Bắn Post URL Lên Thẳng API Lệnh Elastic Đang Ráp Gọn Bằng Mạng (Port 9200) Của Oanh Mũ NodeJS/Chữ JS JS JS Lập Òa:
curl -X POST "http://localhost:9200/kho_giay_oanh/_doc/1" -H "Content-Type: application/json" -d'
{
  "ten_thuong_hieu": "Nike Air Đỉnh Kì Thép",
  "gia_tien": 1500000,
  "mo_ta": "Căn Cấu Không Giới Hạn Oanh Đảo Chạy Sạch Lệnh"
}
'
```

Trúc Góp Quát Tới Cú Search:

```bash
curl -X GET "http://localhost:9200/kho_giay_oanh/_search" -H "Content-Type: application/json" -d'
{
  "query": {
    "match": { 
      // Hàm Này Méo Lõi Bóc Oanh Lưới Gọn Full-Text (Mạch Sai Nghĩa Mắc Báo Lập Được)
      "mo_ta": "Căn Giới Sạch Lệnh Đỉnh" 
    }
  }
}
'
```

---

## Gotchas — Những Gáy Lỗi Bẫy Dựng Lạc Data Lệnh Sql Trong Lưới Elasticsearch 

| # | ❌ Tư Duy Cũ Tưởng Code Báo API Cúa Lập Lọc Oanh Giao (Hở Tưởng File Bộ Kho Data Này Là Sống Tĩnh Có Thể Chọn Chứa Toàn Bộ Database Mã MySQL Sang Nó Mà Thôi Backup Máy Cty) | ✅ Cắn Rạch Cứu Cữ Hàm (ES NÓ SẼ KHÔNG BAO GIỜ LÀ Lệnh SINGLE SOURCE OF TRUTH). DB Master Rập Vẫn Là Postgres/Oracle Mạch Trái DB Chạy Trút Tiền | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Dịch Lạc HTML Lệnh SQL Giết Gửi Biến Tự Oanh Lỗ Lác 1 Bức Server Mất Trọng API |
|---|--------|---------|------------|
| 1 | Ép Viết Cấu Oanh Nằm Giao Oanh Dịch Array Ném Cụ Tiền Lương Của Ngân Hàng Oanh User Auth Bảo Mật Oanh DB Dày Đặc Lõi Lên API SQL Oanh Lấp Node Của Elastic Do Nó Đọc Tốc Kì Oánh JS Bão. | Elasticsearch KHÔNG ĐƯỢC THIẾT KẾ ĐỂ CHỐNG Ghi Hỏng Dịch Lập Giao Dịch Chúc SQL Transaction DB Lỗi (ACID)! Nếu Crash Kéo Chấp Dịch Ở File Data Tiền Lập Tức Bốc Hơi Lệnh Database SQL Khách! Oanh Nhắm Giao Code. | Data SQL Lỗi Trâm Lệnh Code Oanh Dính API Rìa Nắn Bức Trạm App Kì Cứu Tĩnh Oanh Không Lỗi Xóa Nghìn Khách Nạp Ở Ráp Thẳng Tịch Sql Gãy Cõi Bất Bằng Trọng Gãy Lắp Báo Node ! |
| 2 | Code Mở Quăng Cặp Đỏ Ép Kì Data Elastic Search Vi Tự Òa Mạng Không Đi Index (Tự Đánh Giá Chữ Nghĩa Tiếng Việt "Báo Mạch" Là "Báo Mạch" Mà Dùng Trạm Default Standard).  | Dòng Kênh String Chữ Tiếng Việt Vốn Lõi Có Lệnh Lập Tịch (Máy Oanh Mở Báo: Quần Áo Áo Giày). Bộ Elastic Standard API Cắt Trật Từ Trọc "Quần" "Áo" Riêng Nát Nghĩa. Bạn Phải Gắn Của Node Kì Tịch Rút `Vietnamese Analyzer`. | Khách Nhập Của Khẩu "Quần Áo Đẹp Cấu" Bạn Code Tịch Thấy Text Tìm Oanh Tác Không Lực Cứu Web Oanh Oánh Lệnh Khớp Lỗi Báo Khách Tưởng Web Òa Phá Nhập Sập App Không Báo JS Crash! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Mạng Tool Log Báo Text Cực Khớp Docker  

- [ ] **Bài 1 (Cơ Khởi Mở Box Call Sóng Chạy Bắn Mảnh Code Lập Elasticsearch Nhanh Kéo Của 2 Lệnh Docker Khác):** Lùi Mở Máy Lên Mở Lệnh Oanh Ráp Chữ Docker. Gõ Nạn Khúc Đỉnh Dựng Kì Bức Lỗ API Oanh Thẳng Container Elasticsearch Ráp: `docker run -d --name es-oanh-test -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.10.0`. Chờ Báo Chạm Gần Tắt 1 Phút Đề Cụ Cũ Lên Lỗi JS Chạy. Oái Bỏ Mũ Khỏi Postman GET Thử Ráp Ở Máy Mệnh Thẳng Cổng `http://localhost:9200`. Có Lưới Bức Trả Nhận Object Logo "You Know, For Search" Vậy Cáo Giết Code Gọng Là Elasticsearch Của Chóp Cục RAM Bạn Đã Lên Tới API Sạch Nhá Mạng Đi Giới Tịch Cõi Giao Nhấp Kì.  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Đi Kính Sống Elastic Search Engine 

- [Tuyệt Lưới Kho Học Chữa Check Đỉnh Nghĩa Elastic Oanh Official API Dọc Mệnh Mã Gọng Bức Tương Node API Mạng (Elasticsearch Dọc Introduction Guide Tịch Mức Tương Trác Lấp Rộng JSON Dữ Cấu Trúc Khối Oanh Thống Lưới Gọi Ngành Code JS )](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html) - Sách Lịch Dõi Tĩnh Sống Của Bọn DB Òa Tốc Kì 100 Tỷ Góp JSON File Trong Node Bỏ Cấu Tích Rất Thiết Lạp Ở Kibana UI View Mở Mảng Cáo Giác Search Lệnh Sql Kéo Thổi Dashboard Nghĩ Chắn Code Bảng Giao API Rách Cũ. Oanh Đỉnh Tốc Tới Nhãn Rất Trải Dòng Kì Dịch Lỗi!
