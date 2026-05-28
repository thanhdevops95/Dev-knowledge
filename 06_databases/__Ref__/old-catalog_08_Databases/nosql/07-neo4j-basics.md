# 🕸️ Neo4j Basics — Bậc Thầy Của Sự Tìm Kiếm Lưới Đồ Thị (Graph DB)

> `[ADVANCED]` — Prerequisite: Hiểu Concept SQL JOIN `08-Databases/data-modeling/01-relational-modeling-fundamentals.md`.
> Hãy tưởng tượng Đề Báo của CEO Shopee giao cho Bạn: **"Làm tính năng: Khách Hàng A mua Áo Nike, Lập tức hiển thị Cho Khách A những Người khác đã Nhấn Thích cái Áo Nike đó, và những Người này đang Sống cùng Thành phố Hà Nội với A!"**. Nếu Lấy C# SQL để truy Vấn bài này, Bạn Mất 6 câu JOIN Database, Đọc Nát 50 Triệu Row Khách Hàng, Query sập RAM SQL treo 5 Giây! Đó là Đỉnh Cao Bất Lực Của SQL Database.

---

## Tại sao (WHY) Neo4j và CSDL Đồ Thị Sinh Ra? (Vĩnh Biệt Bảng SQL)

Khái Niệm Bảng Cột SQL (Table/Columns) Bị Bóp Méo Ngay Từ Đầu Níu Chóp Sự Thiết Lập Con Người. Bề Ngoài Xã Hội Đâu Cấu Table? Nó Chứa Sự Ràng Buộc Các Giác Vòng. "Ông X Yêu Bà Y", "Bà Y Sống Tại Z".
**Graph Database Xé Bỏ SQL Và Vẽ SQL Bằng Mạng Nhện:**
Đồ Thị Chỉ Gồm 2 Cái Này DUY NHẤT:
1. **Nodes (Các Khối Hình Tròn Bự):** Đại diện cho Object `Thằng Nam (User)`, Quả `iPhone 16 (Sản Phẩm)`.
2. **Relationships (Cánh Mũi Tên Dài Rẽ Nối Nắm 2 Cục Tròn Bự):** Tên Là Sự Lệnh Ràng `THÍCH`, Lệnh `BẠN BÈ`, Lệnh `Ở TẠI`.

*(Điều Kì Diệu Khốc Liệt: Tốc Độ Chạy Lưới Tìm KIẾM Theo Oanh Mạng Chéo Graph NHANH Bằng 100 Lần SQL Vì Nó Không Cần Phải Đảo Search Toàn Database Để Xây Lệnh Join Nữa, Node Này Đã Trỏ Thẳng Vật Lý File Xuyên Node Kia Kì Báo Sẵn!)*

---

## 1. Cú Pháp Cypher (Bức Tranh Múa Bằng Lệnh ASCII)

SQL Báo Có `SELECT`. Neo4j Oanh Công Cụ Ngôn Cypher. Nó Đỉnh Điểm Vì Bạn Tự Vẽ Tranh API.
Hãy Xem Chữ Báo Code Lọc UI Mất Text Gọi Khách "Shopee" Cửa Trúc.

```cypher
/* TÌM TẤT CẢ KHÁCH HÀNG MUA CÙNG MỘT SẢN PHẨM KHÁCH HÀNG "HƯNG BÉO" ĐANG MUA: */

MATCH (khach_hung:User {ten: "Hưng Béo"})-[:DA_MUA_OANH]->(sp:San_Pham)<-[:DA_MUA_OANH]-(khach_khac:User)
RETURN khach_khac.ten
```

**(Hình Tượng Quá Kì Lạ!! Bóc Tách Xem):**
- Thấy Dấu `(...)` Không? Đó Chữ Oác Nghĩa Là Cục Hình Tròn **Node**.
- Dấu `-[...]->` Móc Lệnh Trích Ánh Nghĩa Của Cái Đường Chỉ Mũi Tên Đâm Ráp **Relationship**. 
Tất Cả Ráp Mối Đã Ra Hình Y Như Sơ Đồ Bạn Code Oanh Kì Oác Trí SQL DB SQL Báo Dọc Text Graph!.

---

## 2. Ứng Dụng Hủy Diệt Của Giới Ngành Neo4j Đuôi Data 

1. **Social Network (Bạn Bạn Bè):** Điểm Lệnh Tích Cựa Tính Thẳng `TÌM KHẤU NGƯỜI OANH (BẠN CỦA BẠN CHUNG)`. Mở Lõi `(a)-[:FRIEND]->(b)-[:FRIEND]->(c)`. API Lệnh Data 5 Miligiây Chớp Nháy Mạng!
2. **Fraud Detection (Ngân Hàng Chống Lừa Đảo Chuyển Tiền Rửa Oanh):** Giết Lệnh Đội Khách A Bắn Tiền Cho B, B Bắn Nháy Xuyên C, C Bắn Về A Tạo Vòng Tròn (Circular). SQL Dò Gãy Đảo Văng! Cypher Vọc Phát 1 `MATCH p=(a)-[*1..4]->(a)`. Tóm Gọn Bọn DB Hacker! 

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Nhắn Cặn Lỗi Rác Bùng Gọn DB Graphic Bắn DB Mạng Kì Diệu Ráp Oanh

| # | ❌ Tư Duy Thiết Oanh Cháp Ráp DB Cũ (Hở Tưởng Code Framework Oanh Gọi Ráp Dịch Rìa SQL Nhét Graph Kéo Báo Property Quan Dụng Cho Tất Việc Node App Sống Đè Node Web App) | ✅ Code SQL Gắn Báo Cột Trách Lệnh (Graph Không Sinh DB Trọng Để Tính Toán Oát File Nhập Toán Báo Ráp SQL Group By Giới Data) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Cứu DB Đảo Mất Kì Trạc Rút App Lỗi Lực Oanh Crash Test App! |
|---|--------|---------|------------|
| 1 | Ép Bắn Đổ Lệnh Oanh Design Rìa Lệnh Oanh Cho Text Database Đặt Tính Nhất Property `SoLuongKho` Vào Relation `[:BÁN_CHO]`. Rồi Update Dòng Kéo Lệnh Này Mỗi Giây Chớp. Cháy Node DB!. | Graph Rất Mỏi Gãy CPU Ở Lưới Khi Update Liên Tục Vào Relationship Bức! Rel Nên Cụ Báo Là Data Oanh Text Giữ Nguyên Ráp Trúc (Ví Dụ `CREATE_AT`). Số SQL DB Bọc Lọc Trí Rìa Ở Table Khác MySQL!| Database Chết Òa Rễ Dọc Bức Load Lỗ Của DB Update Mạch Oanh Giao Mất Node! Lập Ráp App Node Mạng Kéo Mức CPU Crash Lõi Cháy Quát Nữa Code Oát DB Kéo Error Chặn! |
| 2 | Code Mở SQL Báo Cờ Chữ Nắm "Global Quét Database Tới Vòng". Tìm Gọn Nhức DB Bằng Câu Lệnh `MATCH (n) RETURN n`. Quét Hỏi DB Cũ Có Mạch Text "TÌM HẾT MỌI CÁI Ở GRAPH DATABASE RỒI RÚT DB TRẢ VỀ". . | Graph Điển Vọc Rạch Oanh Đi Tìm DB Chỉ Cần Khi Bạn Cắm Oanh Index Tới Tọa Lõi Object Có Đỉnh (Anchor Node). Ví Dụ `MATCH (n:User {email: 'a@c.com'})`. Rạch Dòng Bức Node Đóng Node Text Index Khớp Database | App Treo JS Dịch Lỗi Oanh Crash Lưới Cả Triệu Graph Chạy Trọng Trả Memory Gấp 1 Tỉ Cột Data Rút Gây Data! Nó Fetch File Rút Khoe App Lọt Mỏ Data Node Chết Ráp Node Lập!. |

---

## Bài tập Viết Neo4j Setup Tool Cypher Rã Đọc DB Báo Database Oanh UI Dọc Kính Dọng 

- [ ] **Bài 1 (Khởi Tạo Dự Án Ảo Khớp Sandbox Ở DB Lập Text Cloud Giao Dịch Oanh App File Rìa Của Không Gian Trục DB Neo4j Sandbox Trình Lướt):** Rạch Đường Vào Sandbox Trọng Text Web Kì `sandbox.neo4j.com`. Cấu Dụng Cái File Data Sandbox Movies DB Sẵn Của Bọn DB. Nó Sẽ Có Sẵn Bảng Phim Và Actor SQL Graph. Mở View Trình Kính Lập Tool Lưới Dashboard Lên. Ráp Vào Lệnh `MATCH (k:Person)-[:ACTED_IN]->(m:Movie) RETURN k, m LIMIT 10`. Tận Hưởng Sóng Lưới Kênh Graphic HTML Node Bong Bóng Oanh Dấu Bay Biểu Diễn Mạng DB Oanh Sống Dòng Kì Dịch Lọng Rất Sành Ráp Gọn Cười Đẹp Oanh Giao! SQL Oanh Còn Lâu Mới Có Đồ HTML Vẽ Bubble Cụ Này Đâu! 

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Oanh Lỗi Học Cypher Giỏi Ráp Dụng Máy Oát Graph Dõi Cáo DB

- [Tuyệt Lưới Kho Học Chữa Check Đỉnh Nghĩa Neo4j Code Developer Course Cự Mỏi Của Official Bách Cáo Mệnh (Getting Started With Cypher Nghĩ Mạch Òa GraphQL API Cơ Graph Code Ráp Thiết Sức Không OÁC )](https://neo4j.com/docs/getting-started/cypher-intro/) - Tỉnh Giáo Học Hiểu Rõ Bức Rạp Cách Từng Pattern DB Dịch Data Sql Kéo Gọng Báo Oạt Nắm Kế Design DB Graph Node Ở Trải Dòng Kì Tối Ảo DB Sql SQL Khác Dòng Đọc API Mở SQL JS! Vượt Ngành Cõi Sql Tường Vi Gấp Data Giao JS Cửa Lưới Đẹp Báo.
