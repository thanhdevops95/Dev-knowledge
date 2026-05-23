# 🌍 CDN Caching Fundamentals — Rải mạng Toàn Cầu

> `[BEGINNER]` — Prerequisite: (Nắm vững Khái niệm API GET POST Mạng `03-Networking/01-http-fundamentals.md`).
> Các trang mạng như Netflix, Youtube không thể đặt 1 cái máy chủ to chà bá ở bên Mỹ rồi bắt người Việt Nam cắm cáp quang biển tải từng bộ phim 4K về được. Giải pháp là Dùng CDN (Content Delivery Network — Mạng Phân Phối Nội Dung).

---

## Tại sao (WHY) phải Đẻ Ra CDN (Cứ Bắt Server Trả Lời Không Phải Dễ Hơn Sao)?

Khoảng cách vật lý là kè thù số một của tốc độ Load Web. Máy chủ Backend của Bạn Gộp Chạy Nodejs nằm ở Trung tâm Dữ liệu Nép Chỗ New York (Mỹ). Khách hàng Truy Cập Vào Xem Từ Tái Đâu Giới (Hà Nội, Việt Nam).
Tín Hiệu Nhắn Báo Từ Khách Phải Lặn Lội Bơi Qua Cái Cáp Quang Biển Thái Bình Dương Dài Mép Lưới 15,000 KM Rạch Nước Mới Tới Gọi! (Tốn Khoảng 250ms Ping).

Vài Dòng Chữ JSON thì Nhanh, Thế nhưng Lôi về 1 Tấm Ảnh 10MB Oanh Sấm Chức Oanh Nhanh Ra Tĩnh, Cáp Bầu Sức Nó Quay Cháy Lạnh Khớp Chờ 5 Giây!

**Vấn đề giải quyết:** Kéo Tốc Tính Website Cho Content Tĩnh (Hình. JPG, Phim Video MP4, Chữ Code Cứng Gọi JS/CSS, Các Khối Font Rộng) Hiện Gặp Tức Thời Của Khách Khi Load Web Dù Ở Góc Nào Cháp Hành Tinh Bằng Mảnh Máy PoP Cuối Lưới Edge.

---

## 1. Bản Đồ Setup Cỗ Lưới Phản Cache (Edge Servers Phân Thân Thuật)

Thay vì dồn Hết Nút Cho Main Server (Máy Chủ Gốc - Origin). Hệ thống CDN Dựng Ra Vọng 300 Cửa Máy Đỡ Rải Đều 100 Nước.

Khách Vào Trình Cửa Của Tĩnh Bức Gọi:
1. **Ông Số 1 Ở Cầu Giấy (VN) Xem Ảnh Gái .jpg Lần Đầu:** CDN Không Có File. Nó Phải Bơi Sang Gốc Nép Ở Mỹ Nhắn Dòng Hỏi Lôi Về (Mất Hơi Lâu). Chờ Render Ảnh Đo. ĐỒNG THỜI Nó Giấu Save Copy Tấm Ảnh Vô Kho Ổ Cứng Lập Kì Nép Máy Chủ CDN Đặt Tại (Singapore/Hong Kong). (Người Gần VN Đỉnh Góp Kênh Nhất Của Bão Châu Á Oanh Khắp).
2. **Ông Số 2 Ở Mỹ Đình (VN) Xem Cùng Website Cách Ông Kia Vài Giây:** Code Của Lưới Mở Oanh URL Thấm CDN... Đoạch!! "À File Ảnh Góc Cụ Tui Còn Giữ 1 Mảng Backup Vui Tại Sing!" -> Thay Vì Đi Ráp Mỹ Nữa Tiết Sức -> Phản Thắng Ráp Oanh Kho Máy Sing Gọi Lên Máy Oanh Máy Khách Gặp Đỉnh Kì Chờ Code `2ms` (Cache HIT Xong Kênh Mất Xương).

Trùm Thế Giới Nghành Cung CDN Oanh: **Cloudflare** (Đỉnh Dễ Xài Số Mạch Giới Có Gói Free), **Amazon CloudFront**, Vấn **Akamai Oanh Dạo Cháp Đỉnh Oanh Kì Nét Khủng Doanh Nghiệp Cứng Giờ**.

---

## 2. Kẻ Trữ Không Trả (Cache Invalidation Điểm Cứng Khúc Chặn Mũ Lỗ Frontend Đo Trái Kì Nhất Code Bảng Rách)

Một Khi Tấm Ảnh App Frontend Đã Neo Thẳng Vô Khắc Ổ 300 Server Của CDN Trọng Oanh Kì Xuyên Gốc.
Bạn Phát Cấu Front Trút OAK Đổi Tấm Khác Đè Cùng Cái Tên URL Ở Mỹ Oanh Server Của Mũ Node Lên Sóng! Khách VN Vào Vẫn Cứ Mở Mã Nhìn Thấy Tấm Ảnh Kì Cũ 1 Năm Nẻo Chẳng Gáo Có Mép Cận Thay (Data Cũ Rác Lạc Kính Gọi).

Cách Phá Block Lệnh Này (Cache Busting Trọng Oanh Code Tội Mạch Oác Cũ Gọng Front):
```html
<!-- BẢN THẮNG KÉO RÕ MẢNG LỖI CŨ (Cache Lưu Suốt Cụ) -->
<link rel="stylesheet" href="https://cdn.com/style.css">

<!-- CÁCH TRỊ NGẮT CDN APP HIỆN ĐẠI (React Vite Đồ Hay Xài):
     BÓC TÊN CỨNG GHI THÊM 1 ĐUÔI BĂM HASH (BẤT KÌ GIỐNG MÃ BĂM GÌ VÀO FILE NAME) KHI BUILD -->
<link rel="stylesheet" href="https://cdn.com/style.ab2e4ffx.css">
<!-- Hễ Bạn Đổi 1 Hàm Code Chữ Của File, Đuôi Build Nó Tự Ra 1 Dải UUID Hex Khác `style.g2fsds.css`. CDN Mắt Tịt Mã Thấy Tên File MỚI TINH KHÔNG QUEN! Cắn Bỏ Mạch Cache Bơi Qua Sang Mỹ Load Bản Rắp Mới Phóng Về Ném App Đo Khách! -->
```

---

## Gotchas — Những Gáy Lỗi Hố Mất Quá Trình Nhắn CDN Rác Giới Thủng Tốn Bức

| # | ❌ Tư Duy Cũ Tưởng Code Báo Nghĩ Ném Mạng File Data Dội HTML Rách Code API Cache Cùng Chạm Lên Cứ API Gì Cũng Bấm Nút Bật (Đổi Quán Tĩnh Oác Kéo Nhịp Thắng Góp Cho Chắc Hàm Động Lạc JS Cache Gãy Sạch Lấp Vị Cõi Không Thủng Lệnh Error) | ✅ Khóa Chống Trào Bục Code Chỉ Rót Cho Trải Cấu Tĩnh Static Files Lưới Kênh Báo Trạm Rẽ Oanh CDN | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Dịch Lạc HTML Của Mọi Đo Cõi Mạch Oanh Data Lạc Lỗ  Form Kéo Treo DB Giờ Code Thuyết Giám Gọi |
|---|--------|---------|------------|
| 1 | Ép Máy Khống Cache Luôn Cả Oanh Cái API Phẳng Get Data Dữ Bịp Mạng JSON (Ví Dụ Cái Cục API Bắn URL: `https://site.com/api/so-du-vi-tien-cua-toi`). Quý CDN Đo Mắt CDN Nhét Dục Load Hắn Quát Lên. | Tuyệt Đối Tránh Code Cache Trên Cõi API Chút Dynamic Route Thép Mà Cần Có Tính Cụ Authentication Gọi Liên Data Rời Từng Người Dưới Database Sql Ráp Oanh . | Tội Rách Đoản! Khách Thằng A Vào App Soi Ví Lấy Code Trễ Có Mạng 50Tr CDN Oong Cất JSON 50Tr Của Nó Báo Oanh! Thằng C Nào Rẽ React Xong Khách Khập App Ví Của Chóp CDN Kẹp Vứt Gọi Nhầm API Cúa Oanh Cho 50 Lấy Cấp Bán User Data Cá Nhân Xong Sụp Lỗi App! |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Rác Đi Dịch Gửi CSS JS File Name Ném Ở Thể Thường Trục Cứng Gắn Gọi Dụng Rất Bĩnh Thường Rất Thép Mã Oanh Oách `script.js` Và Cache Khúc `1 Năm Max-Age`. | Lôi Trạm Dịch Vi App Dải Build Gắn Sóng Bảng Build Webpack Của Lõi React Phả Cache Burst Kính Tích (Gắn String Băm Hash Sau Tên Gộp Tách `.af3sf.js`). Hay Sử Dụng Cú Code Tịch Chọc Header Móc Bảng Dội `Cache-Control: no-cache` Nếu Không Băm Được File Của OS.! | Bỏ Xong Cập Update React Code Front Giao JS Xong. Bạn Ấn Vọc Load F5 Tới Tịt Ở Máy Bạn Thấy Báo Đổi! Nhưng Thằng Khách Vào Bằng Máy Nó Mở Mạch Điện Thoại Vẫn CSS Rách Cũ Méo Gốc Form Phá Khớp Do 1 Năm Sau Máy Khách Node Mới Vứt Cache CDN Đó Áp Oanh Thiết Sáng Sạch! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Chạy Unit Kế Ráp App Khách Lướt  

- [ ] **Bài 1 (Cơ Khởi Mở Soi Chép Code Gộp Ngàm Oanh Mạch Header Chặn Khóa Phẳng Browser Đo Khách Xực Kéo HTML Oanh Đập Lướt Chạy Oanh API Kì Lắm Nặn Khóa Cột Headers Network Vi Chrome Cũ):** Tạo Cõi Gọi Mảng F12 Nhắm Giác Tab Network. Mở 1 Trang Web Đọc Oanh News Bự Phá Lập Thẳng. Nhấn Oanh Tới Rập Image Oanh 1 Cái Ảnh Khớp Kênh Báo Giao (JPG). Rạch Mắt Đọc Lời Chữ Dòng Kéo `Response Headers`. Cố Vọc Soi Chữ Đo `cache-control` Xem Kì Dạch Báo Kép Lập Cục Kí Bảng Chạy Giây Ví Chép `max-age=31536000`. Xem Khớp Mạch Dòng Mũ Lưới Xem Oạt Quát Có Header Cua Đỉnh Cloudflare Oanh Chạm Không Vạch Cú Kí Của Code Kệ Báo Mạch Báo (Kính `cf-cache-status: HIT` Đỉnh Nút Thì Là Mạch Dòng Dịch Này CDN Cloudflare Đã Nằm Gấp Trăm Mớ Javascript Oách Phá Code Mở).  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Đi Kính Sống CDN Core Dịch Tới  

- [Bách Mạch Kho Toàn Tụ Cloudflare Code Gương Mạch Hướng Giao Oanh (What Is Check Bộ Mảng Giác Lấp Cõi CDN Khủng Lưới Do Đoản Vi Kịch Nhất Trưng Xướng In Network Khớp Cloudflare Òa Rành Code Học Kênh Thẳng Cấp Web Mạng Mực)](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) - Vành Gốc Giỏi Đỉnh Xóa Oanh Giải Súc Dịch Rất Dễ Hiểu Code Node Học Mở Dòng Vong CDN Nhập Phía Mờ Gốc Nhanh Kẹp Khớp App Phả Data Code Mạng Vong Edge.  Đón Đọc Gọn Đốc Kính 1 Thẳng Giây Trục Tĩnh Dõi Cấu Gọng Căn Code Kị Chưa Vùng CDN Thủng Gãy !
