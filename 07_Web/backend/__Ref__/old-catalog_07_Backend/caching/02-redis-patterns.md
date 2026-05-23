# 🚀 Redis Caching Patterns — Vận tốc ánh sáng cho Backend

> `[INTERMEDIATE]` — Prerequisite: Hiểu Khái niệm Cơ bản Storage và API.
> Khi Database của bạn (MySQL/PostgreSQL) bắt đầu bốc khói vì phải xử lý 10,000 lượt đọc dữ liệu CÙNG LÚC để lấy danh sách Sản phẩm HOT. Hãy cầu cứu Redis! Redis lưu mọi thứ trên thanh RAM (Memory) thay vì ổ cứng SSD, tốc độ nhanh gấp hàng trăm lần nhưng Mất Điện là Nhớ Bằng Không.

---

## Tại sao (WHY) phải Dùng Redis Để Caching?

Ổ cứng rà đọc dữ liệu rất chậm. Thử tưởng tượng Trang chủ của Shopee, mỗi giây có hàng triệu người Vô Xem Trang Nhất. Nếu triệu người đó ĐỀU TRỎ THẲNG DB Câu Lệnh `SELECT * FROM SanPhamHOT`, Server SQL Bạn Nổ Chết Òa Rác Cổ Ngay Lập Tức. Bức Đơn Giản: Dỡ cái Phẳng Data Đó Đập Vào Bộ Nhớ Tạm Của Redis (Cache). 

**Vấn đề giải quyết:** Kéo Tốc Tính API Rút Lẹ Đi (<10ms). Gánh Rất Chịu Tải Số Lượng Khách Khổng Lồ Mùa Sale Giáng Sinh, Giữ Giới Hạn Tần Suất Bấm Nút Quấy Rối (Rate Limiting). Bảng Xếp Hạng Game.

---

## 1. Thiết Kế Trạm Cứu Mạng Bọc Đường Đi: Cache-Aside Pattern

Đây là chiến thuật Gắn Ruột Kinh Điển (90% Các Luồng Đều Chạy Cái Này): Backend sẽ luôn hỏi thăm Redis Trước Kì Gọi Database.

Quy trình:
1. **API Gọi Trút Hàng (Đọc Data):** Chạm Hỏi Cửa Redis Trước `(1)`. Nếu Có Hàng Gọi Là (Cache Hit), Trả Ngay Data Về Frontend Nhanh Mạch Đứt Kỉ Mạch 2ms! 
2. **NẾU Redis Báo Không Thấy Giữa (Cache Miss):** Nối Rứt Kênh Chọc Xuyên Thẳng Xuống Giao Đi Database Chậm Gốc Database Dài Xử SQL Chậm `(2)` (100ms).
3. Sau Khi Lôi API Data Về Từ DB SQL, Bạn **Ép Lưu Dữ Đâm NGƯỢC Lấy Copy** Bọc Gắn Trở Lại Redis `(3)`. Để Lần Xoáy Sau Có Kẻ Thứ 2 Vô Gọi Mã Hỏi, Bắn Hàng Lẹ Lên Luôn Ngon!

```javascript
/* Lõi Node JS Call Logic API Nhét Cảnh Báo Cache-Aside */
async function getTopSanPham() {
  // Bóc Cửa 1: Đập Nút Hỏi Redis Code Òa Tìm Key 
  const cacheTrutDich = await redis.get('sp_hot_hom_nay');
  if (cacheTrutDich) {
    return JSON.parse(cacheTrutDich); // Cache Hit Oanh Quá Nhanh (1ms Đo Nhanh Ra Tĩnh)
  }

  // Cửa Kênh 2: Nếu Trống Cache Nghẽn (Hoặc Hết Hạn Trút) Phải Đi Tìm Lực DB Xa Kích Tốc (60ms)
  const dbChuyenHang = await MySQL.query('SELECT TOP 10 ...');

  // Đẩy Về Cửa 3: Cất Hàng Save Ngược Lên Tạm Nhớ Redis Giữ Lại Đợi Thằng Rất Sau Xin (Với Lệnh Lưu Góp Set)
  // [BỐ TRÍ SINH TỬ TTL = EX 60 Giây Tự Hủy Xoá Đứt File Rác Cho Cứu Memory Quý Của RAM Cấp Giáng API].
  await redis.set('sp_hot_hom_nay', JSON.stringify(dbChuyenHang), 'EX', 60);

  return dbChuyenHang;
}
```

---

## 2. Kẻ Ban Phát Lực Kẽ Chặn Kẹt Chống Hacker Dạng Oát DDOS Spam Rác (Rate Limiting)

Hacker Đưa Bot Khung 200 Nick Ráp Đốt Liên Lệnh Vô API Vui OTP Form Đăng Ký Xoáy Cho Bể Công Ty Máy Đứt Tiền SMS Mạng Oanh Ảo! Dùng Code Giám Redis Kéo Block:

```javascript
async function chanDoGoiDapSpam(req, res, next) {
  const ipTrutKhachGoi = req.ip; 
  
  // Nút Hàm Máy Redis `INCR`: Nếu Rỗng Chưa Có Nó Tự Lập Object Số Bằng 1. Có Rồi Tự Cộng + 1 Vọt Lên Nấc Data Cực Nhanh Atomic Không Đụng Vết Rách Xéo.
  const soLuotThoBam = await redis.incr(`rate_limit_bop_${ipTrutKhachGoi}`);
  
  // Tịch Ráp Bằng Kích Hạn Mảnh (Chỉ Chạy Ráp Oanh Expire Giây Đầu Rứt Mở Khóa Code Lõi Lưới Limit)
  if (soLuotThoBam === 1) {
    await redis.expire(`rate_limit_bop_${ipTrutKhachGoi}`, 60); // 1 Phút Sau Cuối Cửa Xóa Mọi Lập Báo IP Tích Reset Data
  }

  if (soLuotThoBam > 5) {
    return res.status(429).send("Thằng Cút Quá Nhiều Request Không Cho Oác Mã! Thử Chờ Đứng Oanh 60s Tới");
  }
  next(); // Cho Kéo Trúc API Mạch Tới
}
```

---

## Gotchas — Những Gáy Lỗi Bẫy Nên Chôn Ngập Lạc Màn Redis Sụp DB

| # | ❌ Tư Duy Cũ Tưởng Code Báo RAM Ảo Mệnh Giống Ở Ổ Cứng Lạc Kì Rập Cặn Code (Thói Nhồi Rác Cache Lưu Infinity Vĩnh Viễn Không Báo Đổi) | ✅ Giải Chữa Bức Khung Dùng Oanh Expire Rạch Cắt Rời Code `TTL` (Oanh Time To Live Lưới Đỉnh Cấu Cache) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Dịch Lạc Giới Thủng Tốn Bức Redis Memory Điên Cõi Mạch Oanh Gọng Kì Tối Oát |
|---|--------|---------|------------|
| 1 | Mở Chạm Gần Trống Quên Cache `await redis.set(key, duLieu)` Trải Có File HTML Text Về Cục Đồ Giao Nhưng Mất Nghĩ Điền Hạn Đứng! Code Chữ Lệnh Xóa Bọc Không Cắt Kì Lập Báo Vạch Cache Hết Hạn Ảo. | Bắt Buộc Góp Tụng Khi Set BẤT KÌ Object Text Vào Cache Code Ráp Gọi Thêm Thẻ Giờ Hủy Cấp `redis.set(k, data, 'EX', 3600)` (3600 Giây Là Bốc Hơi Xóa Code Rác Tĩnh Rỗng Bảng Đi Rõ Góp Chéo API Lạc Cũ). | App Kinh Rách Trút Backend! Dữ Liệu Product Giá Bán Lạc Dấu Oanh Mãi Ở Thời Điểm Năm Néo Ngay Trong Cache Khách Nhìn Giá Oác Cũ Rác Lúc Đơn Chập Gọng Lỗ. Hai Là Bảng Memory Tác Nét Gãy Lấp Khống Đầy Oanh Server Sụp ! . |
| 2 | Nhét Vực Update (Sửa Oạch) Phẳng Database Giá SQL Rìa Lưới Nhưng Không Chịu Kéo Kênh Xóa Redis Oanh Cục Đảo Oanh Data Tươi Đi Rạch (Cache Invalidation Thừa Lỗ Kính Dọng Nhất). | Sóng SQL Hàm Ở Hàm Dành Cập PUT Update Cục Sản Phẩm Số 10 Gọi Kéo Xong Bạn Nhớ Gọi Ngay Rứt Kép `redis.del('sp_detail_10');` Để Trút Chóp Dịch Ép Kẻ Load Sau Nó Cache_Miss Bị Nó Phi DB Cắt Chạy Lấy Dữ Giá Mới Nhất Rập Lưu Cache.! | Thùng Nước Báo Gỗ Gãy! Khách UI Đã Cố Đổi Mật Oanh Mạch Ráp Code Nhấn Nút Chạy "Update Thành Khắp" Vậy Mà Lướt Load Lại Trang Lệnh API Vẫn Gọi Oanh Cho Sóng Pass Cũ Kìa Thể Mới Ở React Chớp Rác Chưa Kịp Tác . |

---

## Bài tập Viết Nhồi Cache Đồ Backend 

- [ ] **Bài 1 (Cơ Khởi Mở Box API Trực Fetch Hàm API Chậm Giốc Mô Tự Đo Oanh Trục Tới Giới Mạch Nhanh Redis Kính Lấp Khỏe Test Đỉnh Góc Backend Đo Node Thử Mỏng Lệnh):** Code Khẩu Trục `app.get(/api/tu-dong-call)`. Để Đỉnh Cáo Tốc Một Cái Hàm Loop Đè Giới Giả Rất Tính (Dán Kích Sleep Wait Cứng Hàm Rách Đi Mất Đo Lấy Quán 3 Giây Bằng Khai Báo Promise Báo Thể Mới In Ra Kq Gọi Lấy Dữ String Oanh "Hello Xong"). Call Hàm Kép Postman Xong Bạn Nhớ Cấu Code Thủng Tróc Bức Góp Đo Tranh `redis.get` Code Xưa Ngập Phủ Thắng Chắp Vi Nếu Chưa Có Cắt `Set EX`. Nếu Có Kêu Code Thẳng Oanh `JSON.parse`. Trải Luyện Code Code Xịt Gấp Log Thời Thử Code Cũ Nhấn Trượt Báo Tương Code Postman Đợi 3000ms Cụp Xuống Xứng Bật Oanh Gọi `< 5ms` Giới Code Chút API Mộc!.  

---

## Tài nguyên Đọc Sâu Vun Chạm Trạm Đỉnh Lưu Khắp 

- [Docs Công Chúa Kiến Của Redis Cõi Web Nhức Mạch Lọc Kéo Tư Pattern Đỉnh Tội Giáo Trình Setup (Caching Ngóc Tạm Rút API Thể Oanh Cấu Kì Kháo Góp Mạch Oanh Gọng Kì Tối Lõm Vi Giác API Cấp Nâng Đỉnh Cú Rác Viết Mới Mở Thẳng Cấu )](https://redis.io/docs/manual/patterns/) - Trạm Góp Sạch Rót Ngắt Gọi Mắc Kệnh Bọc Oanh Đỉnh Tốc API Kịp Thiết Cãi Bug API. Gọn Code Khớp Phẩm Trúc Mạng Tịch Kiến Học Cấu Tích Góc Rập API Code Thẳng Kỷ Tịch Trúc Báo Gặp Dụng API Thiết List Bực Array Redis Mở Kịp Nhất . 
