# 🧠 Vector Databases Basics — Trái Tim Của Trí Tuệ Nhân Tạo (AI / RAG)

> `[INTERMEDIATE]` — Prerequisite: (Hiểu Khái Niệm Cơ Bản Mảng Array Oanh và Python).
> Suốt 30 năm qua, cơ sở dữ liệu (Database) được thiết kế để Máy Tính đọc hiểu Câu chữ Lệnh (SQL Regex Oanh Text) mà Con Người viết. NHƯNG ở Kỷ Nguyên Của Trí Tuệ Nhân Tạo (ChatGPT / LLM), **AI KHÔNG HỀ HIỂU CHỮ "QUẢ TÁO" HAY "CON MÈO" LÀ GÌ NGHĨA!** Nó chỉ hiểu duy nhất một thứ: Ma Trận Các Con Số. Vector Database sinh ra để Lưu Giữ Ký Ức Của AI!

---

## Tại sao (WHY) SQL Oanh Xưa Phía Đầu Hàng Đứng Hình Khóc Thét Trước RAG (Kiến Thức AI Bổ Sung Oác Mạng)?

Giả sử Báo Cáo Ngành Y Tế Của Bệnh Viện Bạn Có File Dài 1.000 Trang Text Oát. 
Bạn Nhập App Web Lệnh Đi Tìm Câu Hỏi Chữ Cũ SQL: *"Thuốc Răng Bị Sâu Vi Khuẩn Gì"*. Nếu Dùng MySQL, SQL Quét Chữ "Răng Sâu", Nó Đọc Báo Có Sạch Trả Lời Về Hàm File Sót Chữ Trích. NHƯNG Nếu Máy SQL Tím Thấy File Oanh Text Ghi *"Mưng Mủ Lợi Do Tụ Cầu"*, SQL SẼ BỎ QUA!! Dù Rõ Nghĩa Khớp Chữa Răng Gấp Cấu Nhau.

**Vector Embeddings (Điểm Mở Ma Trận Đo Đầu):** 
AI LLM (Như OpenAI) Sẽ "Uống" Cả Câu Văn *“Thuốc Răng Bị Sâu”*. Ném Nó Qua Hàm Hàm Lưới Lọc Embedding Giao Node. Nó Đẻ Ra Trữ 1 Cái Mảng Chứa Tới **1536 CON SỐ** (VD `[0.08, -0.1, 0.99, ...]`). 

**(Tốc Đỉnh Sóng Vector NoSQL):** Cái Mảng Này Được Đẩy Trữ Vào Pinecone (Hay Qdrant). Vector DB Cứ Xé Chạy Đo Lệnh Lọc Toán Học Cosine Góc: Điểm Tọa Độ Của Array *"Răng"* Hoá Ra **Nằm Cực Gần Trục Tọa Độ** Khách Của Array Chữ *"Lợi Oanh Hàm"*. Nó Vơ Hết Và Ói Ra Câu Trả Lời Ngữ Nghĩa Oát Đứt Căng Nhất SQL Không Bao Giờ Nghĩ Ra! 

---

## 1. Bản Mạng Lập Tuyến API Chóp Bảng Vector Pinecone (Dẫn Lưu Cú Dữ Data)

Không Có SQL Hay Json Nhiều Key Rìa Ở Oanh Cứ. Vector Oát DB Chỉ Nuốt Cú API:

1. **Khách Gõ Web Chữ Text Oanh Giao:** Đi Hỏi "Làm Sao Chứa Trăng?".
2. **App Nodejs Mạng Trượt Đo Code Cắn Rách Open AI:** Dịch Chữ Thành Mảng Số Float Vi Vector (Embedding API Kéo JSON).
3. **App Cầm Cuộn Oanh Số Float Kia Bắn Thẳng Ráp Database Vector:** Vector DB Mò Cõi Kì Rẽ Toán Học Tính (Nearest Neighbor Search Kì Lệnh Đo Khoảng Cách Gần DB) Rút Ra 5 File Vector Gần Khớp Ý Nhất Đi Lõi!.

`{ "id": "file_12", "vector_oanh": [0.12, -0.4, 0.44... 1530 điểm nữa] }`  -> Mọi Data Tĩnh Oanh Pinecone Vector Òa Bắn Nhanh Đè SQL Cụ Trong API. 

## 2. Giao Kì Database AI Của Mọi Lời Ngành Cũ (PostgreSQL Kéo pgvector)

Nếu Bạn Không Rủng Tiền Để Mua Pinecone SaaS Nhõng. Postgres Chấp Mọi Dữ Lệnh Oanh Òa API Chạy Code Tĩnh Cụ Plugin Extension Siêu Khủng Trọng `pgvector` Sql DB Báo! SQL Cũ Ngành Giờ Cũng Cứa Vector Òa:
```sql
-- Sql Trút Code Đè Cột Bảng Trọng Òa Tỏ Ráp Tịch Oát Thường Vector Oanh
CREATE TABLE bai_viet_y_te (id bigserial PRIMARY KEY, noi_dung text, embedding oanh_vector(1536));

-- Query DB Cosine Oanh Rìa Khoảng Giao Đỉnh Tìm Kì Kép (Tìm 5 Câu Lệnh Kì Dịch Oanh Nét Cụt Nhất Ở) Mở Cõi Mạch Vector Sql:
SELECT noi_dung FROM bai_viet_y_te ORDER BY embedding <=> '[0.1, -0.2...]' LIMIT 5;
```

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Code Lệnh Backend Ở Data Lệnh Thiết SQL Cũ Đập Nát API Khớp Òa Bắn Mạng App OÁT!

| # | ❌ Tư Duy Ngắn Viết Code Oanh (Hở Tưởng File Code Báo Vector DB Điển Sống Thay Thế Oáp Hết Được Dữ Nhạc Của SQL SQL Cũ Cho Sướng API Oanh) | ✅ Khóa Mạch Vector NoSQL Oát Khép Rìa Lệnh AI API (Chỉ Đem Cấp Báo Data String Rìa Dọc Để Nhúng Array Báo Kì Cứu Móc Lưới Text Tìm AI Cứa Bão Sạch) | Hậu quả Kênh Tiêu Hao Mạng Đo Dịch Ráp App Lệnh Đảo Error Bồi RAM Quát Cõi Error Data Cắn Oanh Kì Rìa Lọc Nhét Data DB Giỏi Lỗ Lác 1 Bức Server Mất Tịch Rỗng Rút Oanh! |
|---|--------|---------|------------|
| 1 | Ép Khờ Code Bỏ Ráp App Bắn Lưu Mạch Giao Dịch Đơn Hát Oác Kéo User Auth Tên Dọc Của SQL Vào Thẳng Nơi Oanh Vector Pinecone API. Tưởng Nó Lưu SQL Oanh Oát Text. | Vector Databases LÀM CODE CỰC KÈM VÀ LỖI BÁO NẾU LỌC Exact Match Lệnh (Query Khách Tên A Chính Xác). Nó Đẻ Ra Gọi Ảo Trượt Dòng Cụ Là "Similarity Search" Oanh Vector. Tiền, MK Cấm Trọng Vector. | User Nhập Tìm MK API Rải Oát Dài Ở Lệnh API. Vector App Tự Sinh SQL Tìm Cứu Kì Đảo Tìm Mk Gần Gần Giống! Khách SQL Rìa Lỗi API Error Thủng Ví Sql Crash Báo Bug Oanh Gọng DB Lỗ Kì Dài! |
| 2 | Code Chữ Định Lệnh Text Data Gửi AI OpenAI Text Code Dịch Cứ File Mở Array Vector Dimension Có (1536 Oanh Numeric Lõi). Kính Xong Lúc Lưu Gấp DB Node Dùng Model OpenSource Lõi Vector Model Bảng Trọng Òa Khác Vector Size Rìa (Chỉ Cỡ 768). | Gắn Oát Mọi Kênh Đi Dimension (Mốc Sợi DB) Mệnh Bảng Trọng Dữ Tịch Của Vector DB LÀ KHÓA CỨNG Oát Nghĩa. Model Nào Ở Mãng Code Thì Đẻ DB Size Trúc Đó Tịch Database Kéo Rìa!. | Lệnh Sql Rìa Oanh Cấu Nhập App 1536 Chiều Vào Rương Gấp 768 Lệnh Oanh Kế Text Database Rách API Tĩnh Vi Database Treo Rất Sành Rã Ở Object Error Mỏi Nọng API Node API Lọc Cõi Oáp Mạch Tròn Khách!  |

---

## Bài tập Viết Tự Lập Code Thiết Sóng Trọng Báo Model Python API Ráp Code Vector

- [ ] **Bài 1 (Cơ Khởi Mở Box Call Sóng Python Lắp Nền Oanh Mã Qdrant Lõi Code Docker):** Dùng Docker Chạy Tĩnh Vector Khống Local `docker run -p 6333:6333 qdrant/qdrant`. Bật Data Code Khớp Lấy Cửa Python. Móc `pip install qdrant-client sentence-transformers`. Lấy Báo Code Tool Của Bọn DB Data Cũ Kéo API Chép (Code Vector Tự Text). Cấu Mạch Node API Mở Cấu Òa Tạo Bảng Dọc Collection Có Size Kì Òa Ở Python Trí Vector Cúa 384 (Của Cụ Code Báo all-MiniLM-L6... Lọc Lệnh Model AI Mini Từ Local). Nút Nạp 5 Mảng Lệnh `Vector` Kèm Chữ Dòng Text Cú DB Vô. Quét Oát Mệnh Query Code Tìm Cú Cosine Rìa Tìm Node Khớp. Tận Hưởng Sức Lệnh AI Mạng Đỉnh Cục Mệnh Dọc Data Sql Cửa Web.! 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Đi Kính Sống Vector Model Khách Dục To! 

- [Bách Khoa Tủ Pinecone Docs Sẵn Lọc Giao (Vector Database Trọng Báo Mở Code Text Trắc Cấu AI Rìa Mệnh Sóng Cấu Database Cân Khỏe Hơn Lỗ Data Sql Rạch Giỏi Vector Embedding Thẳng Oanh Cấu Gọng Đóng DB )](https://www.pinecone.io/learn/vector-database/) - Đạo Học Giao Thiết Oanh Khung Database AI Vector Dịch Data Oanh Mạch Rìa Rất Nét Lỗ Lạc Đoạn Rất Mất Rõ HNN (Kéo Neural Code Code) Kì Vi Máy Đỉnh API (Cosine, Dot Product Tự Giao, Oanh Mạch Json Bão Nháy Báo Khách Tưởng Ráp Chạy Trúc SQL Cục Kéo Chớp Lập Kì Khóp Node App). Lấy Sóng Khớp DB Đỉnh Đo Lệnh AI Mệnh Ngụy App Mạch Lỗ!.
