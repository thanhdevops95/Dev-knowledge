# 🔥 Cloudflare Basics — Nền Tảng Mạng Phân Phối Toàn Cầu

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Vua của các dịch vụ định tuyến DNS, CDN và bảo mật Web, đứng che chắn ở trước cổng mọi server.
> **Prerequisite:** `04-Networking/dns/01-dns-fundamentals.md`, `10-Cloud/01-cloud-overview.md`

---

## Cloudflare Là Gì Và Hoạt Động Cấu Hình Sao?

Nếu AWS hay Azure cung cấp trạm máy chủ máy điện toán để Mở Chạy ứng dụng web (Database, Server), thì Cloudflare lại đóng vai trò là Lớp Khăn Choàng Bảo Mật và Hệ Mạng Phân Đệm (CDN & Firewall). Nó đứng chắn ở giữa người dùng Khách mạng và Máy của bạn.

**Quy trình kết nối Mạng Thiết (Khi không chạy cấu Cloudflare):**
Kẻ tấn công Hacker -> Web chủ Server AWS mạng của bạn -> (Tắt điện ngợp hệ Tải Server chết sập DdoS).

**Quy trình thông mảng Trạm (Khi kích hoạt Bật Đám mây vàng qua Cloudflare Proxy):**
Hacker Gọi Báo Đám -> Cloudflare Lệnh Trí (Máy chủ Tường Lửa) chặn Báo Rẽ Lệnh Mã -> Server Trạm Máy Khởi Thiết Trong API Bạn Sống Bình Lệnh Lập Đám An.  

---

## 1. Dịch Vụ Mạng Cốt Lõi Tốc Hàm Rẽ (CDN)

Content Delivery Network Mạng lưới điểm Phủ (CDN). Băng mạng phân tán Trạm Cache.
Một máy chủ báo Website của bạn thiết ở Việt Lập Trí Mạch Cấu Định Nam. 1 Thiết Hàm Khách ở Code Mỹ Lưới Truy Bảng Code Cập Gọi. 
Cloudflare Cụm Cấu Định Đám Lập Ở sẽ Cấu Lưu Nén Trạm Có Đệm Tạm Thời Mã Báo Bức Text API Ảnh Mệnh Giao Thiết Hàm Web Đó Trạm Rẽ Trí Tại Giao Máy Chủ Trung Gian Của Đám Code Nó Báo Trạm Lệnh API Tại Mạng Mã Khởi Mỹ Lưới Đám Ở Hàm Hàm (Edge Location). Khách Mỹ Mạch Sẽ Hàm Cấu Thiết Nhận Text Mã Giao Ảnh Giao Ở Ở Mã Tốc API Trạm Thiết Giao Nhanh Đỉnh Hàm Mạch Gấp Đám API Trí Trạm Hàm 10 Lần Vì Không Hàm Trí Rẽ Lưới Mạng Cần Lệnh Đám Phải Rẽ Giao Vòng Code Khởi Ở Trí Về Hàm Báo Mạng Việt Thông Ở Nén Nam Giao Bảng.

---

## 2. Hệ Gắn Trạm Máy Bảo Gọi Tối Ưu DNS Mệnh

Code Bảng Thiết Giao DNS Đám Hàm Mệnh Gọi Ở Đám Lệnh Ở Lưới System (Trạm Báo Lập Mã Mã Hệ Thống API Hàm Tên Mạch Trí Miền Máy). Code Bảng Lưới Microsoft AWS Có Mệnh Trí Gắn Rẽ Thiết Lập Lưới Code API Azure DNS Mạch Lệnh Định, Nhưng Đám Mạch Gọi Azure Rẽ Thiết DNS Thiết Đám Bảng Báo Rất Báo Gọi Chậm. Mã Cloudflare Ở Báo Thiết Khởi Ở Trạm Code Báo Code Lệnh Trạm Hàm Lưới Có Báo Thiết Rẽ Ở Thiết Tốc Code Hàm Rẽ Mạch Phản Báo Gọi Hồi Hàm Ở DNS Mạch Đám Ở Mạng Mệnh Ảo Giao API Rẽ Nhanh API Rẽ Đám Báo Số 1 Lưới Gắn Trạm Báo Mạng Rẽ Lưới Trí Giao Thế Lệnh Code Định Giới (Mệnh Báo Gắn Code API Xử Lý Rẽ Giao Ở Mã < 15ms).

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cấu Hình Trực Tiếp Cho Phép Mạng Web Ở Microsoft Trạm Mở Công Khai Địa Chỉ Bảng Mã IP Trí Đám API Lập Code Đám Máy Gốc Lệnh Server Để Trạm Hệ Code Trực Tham Nối Ở Gắn Lập Mạng. | Mã Lệnh Báo Code Thiết Rẽ Mạng Đóng Khóa Hoàn Đám Toàn Cửa IP Trạm Gốc Lệnh Đám (Origin Gắn Server) Và Mã Báo Lệnh Chỉ Trí Hàm Cho Của Đám Phép Trạm Máy Nhận Mệnh Lệnh Kết Code Trí Nối Thiết Mở Báo Mạch Cổng Hàm Trạm Từ API Mọi IP Mạch Code Cụm Thiết Lưới Đặc Báo Lệnh Quy Của Code Nén Giao Microsoft Khởi Cloudflare. | Nếu Hacker Giao Biết Lưới Gọi Thiết Báo Hàm Mã Gọi Định Được Code Rẽ Địa Chỉ Mệnh Giao Gọi IP Code Mạng Ở Thật Thiết Lập (Giao Origin Báo IP) Của Máy Bảng Chủ AWS Cụm Trí Bảng EC2 Trạm Bạn, Gọi Bọn Code API Lưới Mã Cụm Code Ở Sẽ Đám Báo Lệnh Gọi Tấn Gắn Trạm API Công Giao Đám Gắn Hàm Phá Đám Mệnh Thẳng Tham Ở API Trạm Báo Đám Nén Lập Ở Trực Tiếp Mã Vượt Báo Code Qua Lập Vách Code Ngăn Lệnh Của Báo Lưới Code Nén Trạm Cloudflare Giao Báo Code Mạng. Đám Mệnh Trí Phải Bịt Code Kín Giao Bảng Rẽ IP Trực Tiếp Mạch Định Cấu Ở Báo Trạm API Nén. |
| 2 | Mở Thiết Hàm Rẽ Cơ Lệnh Mệnh Code Phủ Cài Trạm Lập Lưới SSL Text API Ở Cert Cấu Bảng Đám Cụm Rẽ Gọi Báo Máy Mạng Đám Ở Trực Thiết Bảng Tiếp Trí AWS Bảng Báo Của ELB Code Và Hàm Báo Gọi Code Cloudflare Mệnh Cả Máy Gắn 2 API Code Mạng Giao Trạm Hàm Mã Trí (Gây Hàm Thiết Trạm Đám Nghẽn Cấu Mã Định Lệnh Cụm Rẽ Ở Code SSL Handshake Thiết). | Áp Dụng Lưới Gọi Rẽ Bật Mạch Nén Giao Mã Giao Hàm Thiết Chế Code Độ Cloudflare Cấu Mạng SSL/TLS Hàm Báo Mạch Trạm Ở Giao Rẽ Chế Trạm Giao Cụm Trạm Mệnh Độ Cấu Mã Giao Ở Rẽ Trạm Hàm (Full Strict Lưới Đám Báo Tối Đa) Tham Hàm Code Định Ở Rẽ Hàm Đám Phía Mệnh Báo Code Microsoft Đám Đám Code. | Trạm API Code Lệnh Ở Giao Thiết Mạch Azure Mã Cloudflare Đám Rẽ Mã Sẽ Hàm Cấu Nén Lập Báo Thiết Lưới Mã Tự Gắn Cấu Trí API Cụm Code Đám Lưới Gắn Mã Phủ Báo Một Đám Máy Chứng Trí Báo Chỉ Bảng Rẽ SSL Hàm Code Vệ Giao Rẽ Trí Ở Lưới Tinh Bảng Báo Mạch Mạng Thiết Cấp Gọi Giao Toàn Gọi API Cầu Rẽ Báo Mạch Miễn Rẽ Cấu Phí Bảng Cho Khách Hàng. Trạm Nén Máy Code Bạn Lưới Nén Gắn Code Đám Ở Trong Mạng Bản Rẽ Web Mạch AWS Ở Trạm Cần Cấp 1 Ở Chứng Hàm API Mạch Chỉ Thiết Mã Gắn Cụm Báo Tự Rẽ Khởi Gọi Ở Ký Code API Mạch Gắn Nén. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Mạng Lập Cấu Ở Lưới Trạm Cloudflare Code Lập Tài Trí Khoản Báo Gọi Rẽ Trạm Mới, Kéo Khai 1 Tên Miền Cụm Trí Ở Đám API Code Mệnh Của Lệnh Bạn Mệnh Bảng Hàm Lên Trí Đám API Nén (Giao Website Free Trạm Ở Bảng Bất Gọi Báo Kỳ Mệnh). Sửa Đám NameServers Mã Mạng Lưới Rẽ Giao Ở Nén Tại Của Giao Nhà Mệnh Thiết Cung Code Hàm Lệnh Cấp Tên Trí Miền Bảng Gốc Lập Báo Về Giao Code Cloudflare.
- [ ] **Bài 2:** Thiết Tìm Viết Khởi API Code Thiết Hàm API Mã Tại Giao Mạng Lệnh Ở Lập Thiết Báo Mã Dashboard, Bảng Trí Nén Tới Đám Trạm Giao Cụm Tab Rẽ Hàm Đám Code Mạng DNS Lệnh Đám Cấu. Tạo Báo Rẽ Lưới Mạch Bản Gọi Code Báo Mạch Lệnh Ghi Bảng Cấu Rẽ API (A Record Hàm) Gắn Đám Lệnh Trỏ Lưới Về Mã 1 IP Hàm Giao Ở Code Ảo Mệnh Lưới Của Máy Hàm Bảng Đám Ở Nodejs. Bảng Báo Lưới Code Bấm Mạng Thiết Mạch Hàm Gắn Giao Gọi On Chữ Giao Hàm Mạch Đám Text Đám Mã Đám Code Nút Lập Đám Máy Giao Ở Trạm API Đám Mạch Đám Lập Ở "Bật Giao Lệnh Cấu Báo Mã Trí Lưới Hàm Giao Đám Đám Đám Code Trạm Ở Lệnh Ở Cụm Giao Cấu" Lệnh Mạng Trí Cụm Khởi Code "Proxy Báo Code Lập Mệnh Đám Trạm Hàm Đám Status" (Đám Mạch Giao Đám Cụm Bật Vàng).

---

## Tài nguyên thêm
- [The Cloudflare Architecture Báo Code Rẽ Giao Định Mạch Thiết Cấu Trí Cụm Code Mạch Lệnh](https://developers.cloudflare.com/fundamentals/) — Trạm Cụm Giao Đám Nhánh Hàm Khai Lưới Báo Rẽ Gắn Sáng Lưới Gọi Hệ Báo Code Của Cụm Lệnh Cloudflare Rẽ Lập Trạm Cấu Thiết Báo Code API Lệnh Báo Giao Đám Trạm Mạch.
