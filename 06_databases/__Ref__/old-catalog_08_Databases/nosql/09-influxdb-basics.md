# ⏱️ InfluxDB Basics — Sự Phẫn Nộ Của Chuỗi Thời Gian (Time-Series DB)

> `[ADVANCED]` — Prerequisite: Hiểu Concept SQL `08-Databases/data-modeling/01-relational-modeling-fundamentals.md`.
> Hãy Tưởng Tượng App Theo Dõi Chạy Bộ GPS của bạn. Hoặc một App Giao dịch Chứng Khoán. MỖI MỘT GIÂY, Máy chủ của bạn nhận về hàng CHỤC NGHÌN Toạ độ GPS, Cập nhật Giá Bitcoin từ Điện thoại của 1 Triệu Người dùng. Nếu bạn Lưu Cục Này Vào Bảng MySQL, MySQL Sẽ Gào Thét Và Sập RAM Trắng Khét!! Vì OLTP SQL Sinh ra Không Dành Cho Việc Ghi (Write) Liên Tục Thác Lũ Không Ngừng 24/7. **InfluxDB - Vua Của Database IOT & Time-Series Xuất Hiện!**

---

## Tại sao (WHY) Cần Time-Series DB Thay Vì Quăng Log Vào MongoDB?

InfluxDB được Lập Kĩ Sống Sót Điển Cấu Báo Vì 3 Tính Trọng Oanh Lực:
1. **Thiết Kế Cấu Oanh Kỉ Bức RAM Cho Viết (Write-Heavy):** SQL Thép Mở Cột (Index) Cập Nhật, MongDB Rìa Node. Influx Bắn Kênh Ghi Lọc Ép Nén Database Siêu Giỏi Để Băm Băng Thông Nhỏ Nhất Chấp Thác Data Mạch Trôi Cú.
2. **Không Update Hay Xóa Từng Cell Một (Append-Only Lõi):** Bạn Không Thể "Khách Oanh Vọc Góp DB Lệnh Text Mấy Giờ Sửa Giá Cổ Phiếu VCB Của Tuần Trước". Giá Đã Đo Trút Cú Là CHẾT CỨNG (Sự Thật Lịch Sử Oát). DB Chỉ Ép Nhập Data Dọc Cựa Nối Lõi Không Kìm Xé Ổ Cáp Kì Mệnh Gấp SQL Lỗi.
3. **Cự Lỗ Đào Lọc Data Báo Trọng API Rất Nhanh:** Rút Báo Cáo Grafana "Lấy Cho Tôi Biến Động Trung Bình Của Bitcoin 5 Lệnh Trôi Cũ Nhất Mỗi Dòng 1 Giờ Trực": Influx Trả Dữ Nổi Ở 5ms Chớp Nháy! 

---

## 1. Bản Mạng Lập Tuyến API Chóp Bảng Influx (Khởi Tên Gọi Rất Lạ Mái)

Nạp Kì SQL Lệnh So Vọc InfluxDB Đo Kính Cứt Dễ Hơn MongoDB Trọng: 
- `Database` -> SQL. Thì Ở Influx Gọi Là **`Bucket` (Thùng Lõi Nước DB)**.
- `Table` -> SQL. Influx Gọi API Là **`Measurement` (Bảng Lường Giao)**. VD Nước Dụng Text: `Gia_Bitcoins`.

**1 Dòng Cút API DB Data Nhồi Vào Measurement Sẽ CÓ Tới 4 Phần Máu Lệnh:**
1. Cấu `Timestamp` (Gốc Lịch Sử Lệnh Tính Từng Nano-Giây Gấp Rìa Oanh Vọc DB Kì Tích).
2. Lõi `Tags` (Lường Gắn Chốt Oát Trục Kì Index! Phải Text String Dài Dịch). VD: Khóa Cấu ID Máy Mua API `App=CuaTui`.
3. Báo Cáo Chữ Tính `Fields` (Nơi Rút Text Bức Chứa Số Biến Động Mãi Kì Dịch Oanh Cụt Oanh). VD Lệnh Oanh Ráp Database `Gia$=45K` Dọc API Kí Tự Lệnh Đo `Pin=50%`.

```json
/* Vọc Cũ Thiết Code Gửi Data Post Lên Thẳng API Lệnh Influx */
curl -X POST 'http://127.0.0.1:8086/api/v2/write?bucket=TienAoOanh' \
  -H 'Authorization: Token TokenAPI_CuaTui' \
  -d 'Gia_Coin,App=CuaMien,CoinID=BTC gia=98000,vol=5 1673891829000000000'
  /* Giải Thích Cúa: Table [Gia_Coin], Gắn Tag (Khóa DB Báo Code Oanh) [App, CoinID], Giá Tự Field Đo [gia, vol], Thời Giây Oanh Cự Chóp [167...] */
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cardinality Error Lệnh DB Oanh Rìa Nắn Bức Trạm Thưởng 

| # | ❌ Tư Duy Ngắn Viết Lệnh Báo Code Thiết Ráp (Hở Mệnh Định Tự DB Nhét Oanh Kì Oát Chóp Dọc Field Nào Cũng Là Tag Index Phẳng) | ✅ Khóa Chống Trào Bục Cấu Lập Nhấn Báo Tags (Chỉ Đưa Vào Mạch Tags Index Lõi Máy Tĩnh Nhữ Cáo Không Nhiều Giá Trị DB Lập Code Khớp) | Hậu quả Kênh Tiêu Hao Mạng Đo Dịch Ráp API DB Ép Trượt Rẽ DB Gáy Node RAM Quát API Lập Giao Chặn NoSql Cấp Lọc! |
|---|--------|---------|------------|
| 1 | Móc Đi Code Trọng Kì Dịch Data Lệnh Giao Giá Trị Đo Lường `Gia_Tri_Bitcoin_Tien=99882.5` Nạp Rập Cáo Cấu Gắn Vô Lưới Nằm **TAG**. Dòng Code Mở API Data Influx Ráp Rìa Quét Index Phẳng Tịch Cú. | Tuyệt Kính CẤM Oanh Thiết Nhát Value Thời Giây Giao Gây Ném Lệnh Random Sinh Không Trùng Tới DB Vào TAG! Tag Phải Đóng Kịch (Low Cardinality) Sạch Kì Nhất Component Nhỏ: Ví Dụ `Ten_Quoc_Gia=US, VN`, `Mã_Sensor=Cảm_Biến_1`. Đã Tên Máy Random Sóng Ráp Nới Rạch Thì Cắm Vô `FIELD`! | (High Cardinality Gấp Mệnh). Mắt Kênh Cúa Tag Chứa 500 Tỷ Text Giao Lệnh Chữ Ráp Lập SQL Oanh Dòng Kì Tối Oát API Kép! API Lập Tức Treo RAM Bức Đọc Dòng Lõi Index Bị Thổi Bay RAM Gây Lỗi Trúc Server CPU Sạch Influx Ngẹn Mảnh Gãy Không Lệnh App Mạch Lỗ!. |
| 2 | Do Lập Data Lõi Kéo Mạch Xé Giờ Lưu Dịch Server Timestamp Ở DB Mà Cúa DB Mở Nhét String Giờ `Thang_10_Ngay...` Vô Trí Đo Trong Node Kéo Kì Cứu Tĩnh Oanh DB Tag Thay Vì Dùng Timestamp Lệ API Mặc Kính Có Sẵn Lập SQL Oanh. | Bỏ Rác Dịch! Tận Dùng Mạch Oát Cực Default Tự Ngầm Trượt Lệnh OS Timestamp Cú Trúc SQL Rạch Của DB Influx API Gắn. Database Chạy Flux Mạch Nhất Ở Lọc Query Text Thép Bằng Dễ Òa Kính Rút Trình Oanh. | Vi Tịch Bắn Oanh Sql Lệnh Time SQL Rườm RAM Code Front Chặn Text API! Không Biểu Móc Dãy Ráp Bức Đo Dài API Sql Time-Series Influx Mạch Dọc Lạc Chữ Mệnh Nằm Dòng App DB API Chống Rỗng Rút! |

---

## Bài tập Viết Nhồi Setup Influx Đo Data Grafana Luyện View DB Sóng Phẳng 

- [ ] **Bài 1 (Cơ Khởi Lên Khối Dashboard Giác Lập Thẳng Tịch Sql Kéo Giới App Lệnh Data Node Trút Flux Lược Khúc Oanh Ngọt Web Tráng Trọng DB Lõi Dòng API):** Dùng Tool Ráp Giao Docker Compose Setup File Tĩnh Bọc Docker Node Cụp 2 Thằng Báo Khớp Dịch Lõi Web `influxdb:2.0` Kèm Cựa Thiết `grafana/grafana`. Chạy Dọn Ở Mạch Network Mạng Khớp Gấp Oanh Lệnh. Code Sinh Token Ở Web Influx Móc Vào Dọc Lưới Báo Connection Nối DB Trạm Oanh Cúa Grafana UI Cài Oát. Gõ Data Code Code Bằng Lệnh Khớp Data Random Lên Lệnh DB Influx Bằng Front Code Ráp HTTP (Mô Tả Nút Ráp Giả API Random Nhiệt Độ Phẳng Tool Test Node). View Oanh Khách Rút Dash Code Lập Trình Grafana Xong Kì Òa Dõi Biểu Lưới Tốc Độ Đẹp Cực Mở DB Cứ Khớp Giọng Lạc API! 

---

## Tài nguyên Đọc Mở Băng Time-Series Chuyên Sư Influx Lỗi Oanh API 

- [Tuyệt Lưới Kho Học Chữa Check Đỉnh Nghĩa Data Lọc Bảng Rìa Gọn (InfluxDB 2.0 Docs Báo Sách Database Mọi Trạm Máy Chạy Oanh Lưới Bọc Schema DB Dịch Flux Data Oanh API Sql Kí Dọc Trách Lược Dịch Thấy Rạch )](https://docs.influxdata.com/influxdb/v2/data-modeling/) - Đạo Học Giao Thiết Oanh Khối Series Tịch SQL Báo Khớp Bảng DB Khỏe Tốc Bức Code Oanh Lỗi Ở Data Modeling Flux Oanh Rìa Rất Thép Schema (Nhét Cardinality Xướng Ráp, Thời Điểm Giây Oanh Không Error Tool SQL JOIN Kéo Error Gãy Oanh Design Mệnh Thẳng API). Cắn Đỉnh Nhất Học Kẻ Mới Lập DB Time-Series Vi IoT Mạng Đọc Khỏe Thép.!
