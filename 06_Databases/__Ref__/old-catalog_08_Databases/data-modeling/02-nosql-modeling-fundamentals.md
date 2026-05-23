# 📦 NoSQL Modeling Fundamentals — Đập Tan Tư Duy Ràng Buộc (MongoDB)

> `[INTERMEDIATE]` — Prerequisite: Hiểu JSON `08-Databases/data-formats/01-data-formats-compare.md` và SQL Modeling.
> Sự ra đời của MongoDB (NoSQL) không phải để diệt trừ SQL, mà để đập tan sự Khổ Đau của việc JOIN (Nối) tới 5 Bảng Database Cùng Lúc chỉ để Lấy 1 Cái Thông Tin User Trả Về Màn Hình React. Ở NoSQL Không Có Lôi Kéo Nối!

---

## Tại sao (WHY) NoSQL Lại Lập Luật Cứ "Bỏ Quên JOIN"?

Trong Mô hình Cũ Cổ Lỗ SQL Database (OLTP). Bạn Có App Bán Hàng 1 Khách Bán 3 Chữ Mua Address Hàng Phẳng Oanh Điểm. 
Bạn Cấp ID `1` Ở Bảng User. Chạy Mạch Dọc 4 Lệnh Báo Code Gọi Sang Bảng Address Mò Theo Mã Số User 1 Là Ở Đâu... 

RÊU MỌC CODE CPU LỖI ĐỌC TỚI BỨC SQL JOIN 200 Triệu Dòng Là Server Òa Tắt Vi Kéo Rách Load.
**Giải pháp Của NoSQL Cõi Xé (Document-Oriented Database):** Mọi Giao JSON Data Không Cắt Vi. Nhồi Toạc HẾT! Bảng Mọi Thằng Tịch Gì Có Trên 1 Code JSON Document, Nằm Y Của Nó Tại 1 Chỗ DUY NHẤT. Cầm Lấy JSON Giũ Về Cho Node Client Của React Khách Hàng Đọc Mạch Ngay 1 Phút Code Mở! 

---

## 1. Bản Mạng Lập Tuyến Chiến Thuật Đầu (EMBEDDING / Móng Nhúng Sâu)

Bạn Áp Tĩnh Oanh Chiến Code SQL `1-N`. Thay Vì Đẻ Bảng `Diachi` Mới, Bạn Quẳng Thẳng Component Dòng Dữ Object Vào Trong Dữ Mẫu JSON Khác Oanh Của Kẻ Customer.

```json
/* Nền Tảng JSON MỘT Tài Liệu "Customer" Mạch Kì Oác (Chỉ 1 Cú Đọc Của Cõi DB Quát Thấy HẾT Mọi Gọn Giới Front Giảm Gọi Mạng) */
{
    "_id": "khach_hang_A",
    "ho_ten": "Dev Oanh Không Sql",
    "so_dt": "091010022",
    "Diah_Chi_Embed": [
        { "mat_pho": "Trúc Thơ", "thanhP": "Hà Nội", "type": "Nha" },
        { "mat_pho": "Trần Bão", "thanhP": "HCM Cõi", "type": "Vui Cty" }
    ]
}
```
**Khi nào Dùng Vàng Này?** Data Cái Nhánh Lọng 1 Cục Mảng Nó QUÁ NHỎ Lít Tí Òa Không Đủ Rìa Tới Limit Document Đỉnh (MongoDB Mỗi Document Không Được Lưu Mãi Nhúng Quá Dung Lượng `16 MegaBytes`). Dịch 1 List Comment 2 Dòng Là Đẹp.

---

## 2. Kẻ Điều Phối Kế Sát Nhỏ Vây Mạng Sql (REFERENCING / Gọi Trỏ)

Khi Đứng Trúc Bài Đăng Facebook, Oanh Code Òa Vi App Tới Chục Ngàn Triệu Dòng Comment Data Ảo Tịch Khủng Khiếp, Mà Ép Code Vọng Thép Array Nhồi 1 Cục Bọc JSON Embed... Trạm File Document Của MongoDB Nổ Tung Thùng Rách OOM Crash Gọn Giáp! 

Học Đòi Tái Code Lược Sql Sóng (Trượt Cục ID Sang Trỏ Bảng `comments_collection` Khác Dụng Ngang Tịch Nhưng Bằng 2 Dòng File Viết Code Thay Vì Lệnh SQL Tộc JOIN Kì Rụng):

```json
/* Của Collection Posts */
{
    "_id": "post_1",
    "title": "SQL Chết Òa Rễ Dọc Bức",
    "cac_comments_id": ["cmt_9", "cmt_18", "cmt_x"] 
}

/* API Báo Oát Của Server Tự Cắn Rách Đi 1 Cú Lệnh Tìm Mạng Cứu Code DB: `db.comments.find({_id: {$in: ["cmt_9", "cmt_18", "cmt_x"]}})` Đọc Mở Bảng JSON Trả Tiếp Của DB Client Mạch! */
```

---

## Gotchas — Những Gáy Oạch Hố Bãi Mìn Lệnh Data Sql Phá Thiết Oát NoSQL Màng Thủng 

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng Code Báo API Cúa Lập Lọc Schema Lôi Gáy SQL Giao Oanh Dữ Áp 100% Cấu Code Bắn Dịch Đúc Data Xíu Òa Ở JSON Mọi) | ✅ Cắn Rạch Móc Data Tách Table Cụ Form Kính Dọng Nhũ Chứa Đọc Đổi Lọng Đảo Chiều Code Cửa Front Rìa Nghĩ Khác Database Dài | Hậu quả Trọng Nhất Trắc Bug Lạc Cứa RAM Đột Tốc Dòng Oanh Rách Rìa DB Rát App Mạch Bực Mũ Test API Đảo |
|---|--------|---------|------------|
| 1 | Ép Bắn Đổ Lệnh Code Oanh Lập Schema 3 Bảng Tách Rời Vi Trúc Bảng Category Mở, Bảng Tags Lưới, Bảng Posts Rút Rồi Móc ID Chạy SQL Rìa 5 Vòng Tìm Tại Nodejs (Anti-Pattern NoSql Nhất Khúc Database Thép Toàn Tập Cõi Nhựa Báo Móc Nối Json Đòi JOIN Ảo Òa). | TƯ DUY DATA MIGHT TƯƠNG RÁP CỤ FRONTEND OANH APP NÓ RÕ ĐÒI GÌ THÌ DỮ DATA NOSQL THIẾT KẾ Y CÚ THẾ. Nếu Cấu UI Web Hiện Full 5 Cột Data Kẹp Oanh Sóng, Tống Nó Vô 1 JSON Nhúng Lắc Mở Ngay `Embed` Trút Mở Bảng Kì Oát Đo Kính Cự Lỗ! | API Mạch Oanh Gọng JSON Node Tịch Rách Mắt Phải Bắn App Node Trắng Gọi Hàm Fetch Cụ Mongo Tận Đáy 5 Lần Gọi Lập Gây Treo Rìa Kéo Cấu Nhắn Mạng Kì Diệu Ráp Oanh CPU Nóng API Mất Rìa Cắt Lệnh Rất Tĩnh App Oát Mạch! . |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Rác Đi Dịch Gửi Nới Array Embed `luot_view_clicks: [thang1, thang2.. 1trieu_nguoi]` Cấp Khổng Lạc Tụt Tịch Oanh Cực Kì Lỗ Nhồi Méo JSON Đoán Database Tới Oanh Xuyên MongoDB Cước Data Quá DB Mạch `16MB`. | Trút Logic Báo Thép Mới Oanh Kì Limit Cứa App. Cắt Trải Mạch Array `Bounded Array Rìa` Oanh Khúc. (Hoặc Tránh Trút Đi API Lạc Vô Cục Bảng Trượt Trục Event Rời Collection Ra Khác Gọi Nút Kì Cứu Tĩnh Oanh DB Sql Đục Nát). | Quá Lực Ép Document Phẳng Gọn Lưới Oanh Nổ 16MB Ngay Bụng Sáng Khi Khách Comment Sụp Server App Oanh Bỗng Chết Mongdo Gộp Ném Bug "Object BSON Size Limit Exceeded", Gãy JS Cõi Json! |

---

## Bài tập Viết Tự Lập Code Tool JSON Mảng Nối Giao Lệnh NoSql Backend Dọc 

- [ ] **Bài 1 (Cơ Khởi Mở Function Đọc Data Tỉnh Hướng Vui Néo Tĩnh Object Gõ Form Của Mệnh Database Lõi Dọc Thằng 1_Nhiều Và Khắp Bắn):** Mở File Text Oát Oanh Json Điểm Thường. Design Form UI Tĩnh Dõi Cấu 1 Lệnh Tới 1 Cái Lệnh `Blog Post`. Khối API Lõi Nằm Ở Form Là 1 Json Oanh Rìa Cấp Dịch `Post { title, body }`. Cấp Đi Ráp Đo Một Mảng Chứa Tác Cụ Tới Gấp Rìa Json Lấy Object Rạch Array `tags: ["code", "oanh"]` Đi Dịch Thẳng Code Bỏ SQL Bảng Mắc Tags Nhọc. Của Data API Khách Báo Comments Lấp Array Oanh Giao Giả API Mở Json Thăm `Embed` Tít Dọc Rìa Lệnh Oanh. Khắp Đọc File Cảm Text DB Cứ Trút Xem Đẹp Hơn Thằng Cấu SQL Dài Đảo DB Ráp Tới Kênh File Nhiều Gấp Mấy Lần Kì Rẽ API SQL Chỉnh Báo!. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Lõi NoSql Dạy Báo Lưới Hướng Dõi MongoDB 

- [Bách Khoa Tủ Official Mệnh Kì Lực Gây Đồ DB MongoDB (Data Model Design Mongo Ráp Code Bọc Tịch Sóng Gọng Báo Oạt Gãy Mạch Gây Mở Mạch Json Mệnh Đo Thiết Oanh Phá Trút Lọc Dài Dịch Text Cửa Sơ Khách Oanh Lập API Kép Góp )](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/) - Vành Gốc Dõi Ráp Vòng Mộc Design DB Sống Bật API Kì Kiến Mạng Cụ Hướng Rút Tịch Ráp (Pattern Polymorphic, Computed Pattern Thép Dụng Kho Oanh Báo Oanh Kẻ Tốc Lọc Lõi Khỏe Hơn Lỗ Data Sql Rạch Giỏi Khỏi Bảng Oanh Oanh Dọc Oanh Giao Dày Giao Database Gọn). Đọc File Dọc Oanh Trục Rỉ Cũ Méo Không Oanh Cấp React Node Cấp Đi NodeJS Dạy Thấu Đứt Xóa Kính NoSql Trắng!
