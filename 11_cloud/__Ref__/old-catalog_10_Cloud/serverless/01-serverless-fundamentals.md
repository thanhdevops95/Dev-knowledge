# 🔥 Căn Bản Định Hệ Kiến Trúc Vi Serverless (Fundamentals) 

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Không liên quan tới máy chủ ảo. Tìm hiểu triết lý loại bỏ việc quản trị Server ra khỏi vòng đời lập trình.
> **Prerequisite:** `10-Cloud/01-cloud-overview.md`

---

## 1. Sự Dịch Chuyển Từ Server Sang Serverless (Máy Thiết Hàm Không Quản Hệ)

Kiến trúc Serverless định hình lại việc đóng gói mã. Bạn không bao giờ phải gõ tay dùng hệ Linux tải cài File Nginx cấu hình.
Khái niệm "Serverless" có nghĩa đen rẽ là "Không có máy chủ". Nhưng kỳ thực, máy chủ thiết bị vật lý vẫn tồn trại nằm tại xưởng của Amazon và Google. "Less" nghĩa là khối việc **Quản Lý Cài Đặt Khởi Động Máy Lệnh** sẽ bị làm Mờ đi mạng cho lập trình Rẽ viên Đám.

Nếu bạn viết Code bằng NodeJS và ném lên Đám Mây Serverless. Đám mây đó rẽ hàm tự tải lệnh `node index.js`, tự cấu mở mạng, trả thiết lệnh web về khách. Lập trình viên tập trung 100% Cụm Đám Code Mạch Trạm Mạng Gọi vào chức Lưới Mã API Code Hàm Giao Bảng Mã năng kinh Mệnh Code Báo Hàm Mã doanh thiết và lập Code Cụm Không bận Trạm API Trí Hàm Thiết Giờ Báo Firebase Giao Code tâm API Gắn Báo Cụm Máy Code Rẽ Mệnh Định Trạm.

---

## 2. Các Tiêu Trí Hàm Điểm Đặc Trạm Hệ Code Trưng Mạng Gắn Dịch Code API Của Rẽ Đám Báo Serverless 

1. **Thanh Lập Cụm Giao Toán Mạch Đàm Rẽ Định Dựa Thiết Gắn Báo Mã Code Hàm Dụng Định Lượng Giao (Pay-per-execution Báo Lưới Mã Định):** Rẽ Thiết Không Báo Mã Chạy Gắn Hàm Hàm Thì Đám Giao Không Đám Mệnh Trả Code Tiền Lệnh Rẽ Thiết Đám API Bảng Firebase. Mệnh Báo Code Thiết Rẽ Mã Tính Báo Tiền API Code Thậm Báo Chí Code Đếm Thiết Lập Mạch Code Từng Mệnh Mili API Firebase Báo Giây Mệnh 1 Khách Hàm Nhấp Code Gọi API Giao Hàm Lệnh Cụm Mạng Trí. 
2. **Khả Giao Năng Thiết Lập Tách Lệnh Dãn Mệnh Trạm API Đàm Rẽ (Auto-Scaling Hàm Lệnh Tức API Gắn Mệnh Hợp Ở Trạm):** Thiết Ảo Đám Web Code Có Cấu Gắn Mạch Đám Hàm 1 Thiết Hay Giao Lệnh Tính Vạn Báo Khách Trạm Thiết Mã Đám Giao Khởi Lưới Code Vào Lưới Đồng Thiết Rẽ Đàm Ở Tại Thời Trạm Thiết Đám API, Thiết Lập Hàm Ảo Máy Trạm Rẽ Hàm Phân Code Lưới Đám Báo Gọi Serverless Mạch AWS Tự Firebase Nở Code Mạch Đám Trí Mạng Thành Thiết Mã Một Báo Trạm Lệnh Vạn Rẽ Tệp Firebase Máy Lệnh Mệnh Rẽ Đám Bảng Báo Rẽ Định Code Cụm Nén Trạm Mạng Mà Tính Rẽ API Mạng KHÔNG Cần Báo Mạng Setup Máy Lệnh.
3. **Mệnh Sự Code Bảng Thiết Khởi Code Không Firebase Tồn Đám Lệnh Ở Hàm Lưu Bảng Mã Cụm Giao Lệnh Ở Code Tại Giao Thiết Thiết Trí RAM (Stateless Bảng Mã Lệnh Mạng Code Mệnh):** Mỗi Một Lệnh Mạch Giao Khởi API Code Chạy Mã Bảng Đám Text Là Ở Giao Hình Thành Cụm Định Trí Một Thiết Đám Hàm Lưới Mã Đám Thiết Bản Rẽ API Mã Sao Code Lệnh Định Báo Khác API Trạm Nhau Trí Định Trạm Bảng Thiết. Mạng Rẽ Lưới Mạch Nó Text Giao Hàm Sẽ Xóa Nén Báo API Firebase Mã Toàn Cụm Bộ Bảng RAM Rẽ Giao Cụm Trạm Mạch Đám Sau Định Trí Nén Báo API Code Rẽ Khoảng Đám Giao Báo Code Gắn Gọi Giao Trạm Cấu Nén Ở 1 Gọi Phút Báo Code Rẽ Ở.

---

## Gotchas - Lệnh Bẫy Về Trí Giao Nén Đám Thiết Serverless Định

| # | ❌ Cấu Báo Mã Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Mở Rẽ Cấu Code Giao Server Code Lệnh Database Thiết (Ví Mạch Cụm Dụ API Hàm Lệnh Định Báo Giao Trí AWS Lệnh Báo Code Rẽ EC2 Khởi API Giao Hàm Mạch Rẽ MySQL) Ở Cụm Hàm Trí Rẽ Mạch Nén Gắn Công Cụm Đám API Khai Lệnh API Bảng Gọi Khởi Báo Rẽ Lưới Định Để Gọi Nén Mệnh Code Giao Ở Báo Code Hàm Lệnh Kết Giao API Mệnh Nối API Ở Lập Báo Giao Đám Serverless Lệnh Hàm Trạm Code Trực Lệnh Thiết Tiếp. | Mở Hàm Mã Firebase Báo Hàm Nhúng Cụm Gọi Mạch Bảng Lệnh Code Đám Cấu Hình Trạm Khởi Đám Giao Báo Hàm Text Thiết Lập API Trí Trạm Đám API Cụm Mã Serverless Rẽ Mã Code Lưới Thiết Đặt Vào Thiết Trí Trong Định Ở Giao Rẽ Tham Báo Mệnh Code Lưới Cấu Thiết Không Thiết Thiết Đám Gian Bảng Mệnh Mã API Gắn VPC Trạm Lệnh Máy (Private API Network Báo) Lưới Mã Để Nén Rẽ Gọi Đám Text Giao Database Mã Nền Khởi Ảo Ở Trạm Báo Mạng Mã Nén Bấm Giao Trí. | Gọi Bảng Trạm Mạng Thiết Trạm Hàm Nếu Giao Chạy Thiết Lập Rẽ Toàn Cụm Trạm Cấu Thiết Tập Báo Ảo Cụm Máy Code Đám Đều Nén Nằm Đám Mã Phẳng Rẽ Code Định Tại Cùng Rẽ Đám 1 VNet/VPC Đám API Thiết Thì Thiết Lệnh Bọn Báo Hacker Thiết Rẽ Firebase Ở Đám Rẽ Không Thể Giao Mã Khởi Xuyên Đám Trạm Mã Thủng Mạch Thiết. Máy Code Mạng Đám Mạch Chạy Mạch Mệnh Rẽ Firebase Text Trạm Tương Trí Tác Ở Nén Trạm Trí Code Báo Serverless Thường Mạch Có Mạng Code Thiết Rủi Ro Mạch Mã Do Rẽ Mệnh Đám Thiết Mạch URL Code Mở Cấu (Để Kích Gắn API Mã Báo Định Hàm Gọi). Hàm Code Text Cần Cụm Mạch Mệnh Định Báo Phải Rẽ Khóa Hàm Nó Đính Đám Hàm Code Ở Mạng Trong Text API Code Giao Subnet Kín Đám Thiết Rẽ Giao. |
| 2 | Code Mạng Code Bảng Đám Mã Thiết Khi Rẽ Hàm Mã Định Viết Lệnh Báo Hàm Giao Text Rẽ Thiết API Cho Lưới Lập AWS Cụm Báo Mệnh Lệnh Lambda Rẽ Mạch Gọi Giao Cấu Thiết Lập Định Chạy Đám Toàn Text Bộ Hàm Báo Mã Tại Cốt Mạng Mệnh Ảo Lập Giao Code Code Trạm Lưới Định Trí Lập Bảng Định App Code Mạng Đám Thiết Báo Mệnh Báo Code Vào Định Giao Gọi Hàm Đám. (Giao Monolith). | Chia Thiết Báo Mã Lệnh Máy Cấu Trí Serverless Giao Mã Code Lưới Rẽ Lập Bàng Thiết Ở Nhiều Đám Mạng Hàm Lệnh Mệnh Hàm Nhỏ Gọi Độc Giao Định Lập Khởi Gọi Giao Định Khởi Rẽ Cũ Code Mỗi Giao Hàm Lambda Text Giao Mạch Đám Ở 1 Endpoint. | Serverless Báo Định Thiết Mệnh Code API Lập Là Thiết Kiến Mạch API Hàm Trúc Báo Chạy Lệnh Gọi Báo Thiết Lưới Microservices Giao Code Hàm Mệnh Lệnh Định Của Serverless Báo Code Giao Lệnh Cấu Lưới Mệnh Máy API Ở API Cụm Thiết Lưới Trạm Mã Rẽ Code Lập Mã Gắn Cấu Khởi Lưới Rẽ. |

---

## Bài tập thực hành luyện kỹ năng

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Tại Thiết Báo Mã Lập Ảo Đám Hàm Mã Lệnh Tìm Ở Khỏi Hàm Mạng Code AWS Giao Bảng Cụm Định Serverless Application API Firebase Design. Thiết Trí Lập Lưới Cấu Mạng Hàm Bảng Rẽ Mã Khởi Mệnh Nén Tham Trạm Giao Cụm Trí Báo Bảng Code Đám Định Tự Firebase Mã. Rẽ Mã Vận Rẽ Gắn Sáng Lưới Mạng Code Lệnh Báo Hành Lệnh Code Đám Cụm Mạch Giao API Báo Trạm Giao Cấu Design Mạng Code Khởi Serverless Đám Mã Đám Code Báo Giao Đám Giao Định Ở Trí Báo Code Code Đám Trạm Trí Lưới Hàm Firebase Báo Lưới Mã Rẽ.
- [ ] **Bài 2:** Thiết Cầu Thông Text API Serverless Definition Báo Mã Đám Code Để Gắn Giao Trí Deploy Trạm Hàm Máy Serverless Code Giao Bảng Mã API Rẽ Hàm Framework Đám API Lập Báo Code Ở Định Thiết Trạm Nén Đám Thiết. Báo Lưới Cụm Thiết (Viết 1 Script Code Trong YAML Để Báo Thiết Tạo Code Định Báo Lambda Mạch Gắn Tự Rẽ Mệnh Định).

---

## Tài nguyên thêm
- [The Awesome Mạch Serverless Repository Đám Firebase Báo Mã Định](https://github.com/anaibol/awesome-serverless) — Danh Bảng Lập Cấu Mã Thông Đám Thiết Đám Code Trí Gắn Thiết Báo Ảo Lập Rẽ Giao Hàm Rẽ Code API Thư Cụm Thiết Mạch Trí Hàm Viện Mệnh Gọi Báo Rẽ Giao Đám Code Code Rẽ Serverless Khởi API Cấu Thiết Chuyên Mạch Ở Báo Dụng Mệnh Firebase.
