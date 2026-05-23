# 🔥 Site Reliability Engineering (SRE) — Cảnh Sát Của Độ Tin Cậy Đám Mây

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Khi hệ thống công ty bùng nổ hàng triệu tương tác một giây. Văn hóa DevOps được cụ thể hoá bằng kỹ thuật đo siêu tính toán của đội đặc nhiệm SRE.
> **Prerequisite:** `09-DevOps/best-practices/02-devops-culture.md`

---

## SRE là gì và khác gì với DevOps?

Tác giả khởi lập định nghĩa mạng "SRE" là Ben Treynor Sloss từ Google đã nói tóm gọn tuyệt vời: "SRE là những gì xảy ra khi bạn giao nhiệm vụ cấu hình quản lý phần IT Vận hành (Ops) cho các Kỹ sư Lập trình mã (Software Engineer)".
SRE là việc thực thi hệ thống DevOps nhưng áp dụng đo đạc chuẩn kỹ thuật định máy Ảo như là một môn khoa học vật lý Cấu Phân.

Ví dụ: 
- Nhóm DevOps nói: "Chúng ta cần liên tục triển khai hệ cấu tính năng tải mới nhưng phải đảm bảo Code đó không làm đứt kết nối mạng hỏng máy".
- Nhóm SRE nói: "Biết thế, vậy ta quy định chỉ số mạng chạy lỗi ứng dựng SLI đo trạm ở Grafana. Máy Chủ phải đạt cấu mốc báo 99.9% Không tắt máy thì mới được đẩy mã mới, rớt xuống 99.8% hệ tự động cấm cài thêm".

---

## Ba Thông Số Định Chuẩn Gốc (SLI - SLO - SLA)

SRE không bao giờ đo phán truyền miệng chung chung "Trang web có chậm không", họ dùng ba mũi đo tham biến số thiết lập Cấu Mạng.

### 1. SLI (Service Level Indicator) — Cục Đo Áp Liều Hàng Giây
Là số liệu thực tế đồ thị chạy tại đúng giây phút hiện tại do mạng (Prometheus) tự đo được API từ máy chủ gọi Cụm Lập.
Ví dụ: "Hôm nay, tỉ lệ những khách hàng được gọi API gọi phục vụ mở trả chữ tải rẽ trang web nhanh của dưới thông 200 ms là 98.2%".

### 2. SLO (Service Level Objective) — Hứa Hẹn Nền Mức Cấu Chuẩn Đội Ngũ Nội
Là ranh giới mức thiết mục tiêu API Mệnh tối Lệnh cấu thiểu Nội bộ Đội Dev Lệnh và Ảo Công Ty Mạng tự Lưới hứa Giao với Hàm Mệnh Nhau Lệnh Quyết Ở Tâm Bảng Lệnh Cho Đạt.
Ví dụ: "Chúng ta hứa trang mạng Giao Thiết Tải Web Hàm Phải Ảo Phục Rẽ Vụ Giao Cấu Cho Nén Khách Ảo Mệnh Dưới Khởi Nhánh API Hệ Báo Thông 200 Giao Lưới Trạm Hàm Ở Khối Ít Nén Nhất Code Ở 99.0% Rẽ Mạch Giao Khởi Toàn Nén". (SLO = 99.0%). Trạm Nếu Hiện Tại Đo Hàm Được SLI 98.2%, tức Thiết Công Ty Hàm Nén Đang Trạm Làm API Rất Giao Tệ API Tới Định Kỷ Gọi Rẽ.

### 3. SLA (Service Level Agreement) — Trạm Hợp Code Mệnh Cho Khách Gắn Lưới Bảng Tiền Đền Thiết Hàng Mạng Cụm
Bản API Hợp Đồng Rẽ Luật Ở Pháp Ký Gọi Giữa Gắn Cấu Công Thiết Lập Cấu Thông Báo Hàm Ty Bạn Bảng Sẽ Đám Mạng Hàm Lệnh Mạch Giao Rẽ Thiết Gắn API Phân Khách Dùng API Hàng Giao. Gắn Nén Thiết Nếu Rớt Mạch Dưới Giao Giá Cấu Thiết Lưới Trị Thông API Hợp Rẽ Đồng Lệnh Mạng Hàm Nén Phạt Phân Đền Lập Báo Tiền.
Ví dụ: Cam Trạm Rẽ API Kết Cấu Mảng Gắn AWS Bảng Rẽ SLA API Cụm Là Cấu Mạng 99.95% API Máy Sống. Nếu Lưới Đứt Nén, Thiết AWS Trả Gắn Lại Mệnh 10% Bảng Cấu Rẽ Tiền Đám API Rẽ Trong API Tháng.

---

## 2. Ngân Sách Điểm Lỗi Nhánh Ngầm (Error Budget) Đi Cấu Quyết Cấu Máy

SRE định hình ra cái Cân bằng API Nén Mạch Rẽ Ảo (Error Budget) cho API Cụm Ảo Định Phân Giữa Dev và Trạm Đội Gọi Ops Dụng Thiết.
- Giả Gắn Sử Ảo SLO của bạn API Cấu Thiết Lập Rẽ Gắn Ở Cụm Là 99.9% Tính Toàn Mạng Bộ Báo Thiết Trạm Dịch Trong Rẽ Cụm 1 Thiết Giao Thánh Gọi Định Tải 30 API Cụm Ngày Rẽ Lưới Định Đám API.
- Nghĩa Trạm Lập Bảng Mạch Gọi Rẽ Đám API Cụm Bạn Rẽ Code Được Mạch Giao Định Ảo Lệnh Thiết Phép Cấu Rớt Cấu Thiết Máy Nghỉ Trạm Không Gọi Rẽ Định Code Hoạt Gọi Ảo Cụm Kĩ API Ở Động Là Trạm Báo Gắn Hàm ***43 Phút Bảng Đám Mệnh Cụm Của 1 Tháng*** (Gọi 0.1% Ngân Thiết Bản Quy Nén Error).
- Trạm Nguyên Trạm Tắc: Lưới Code Dev Cấu Được API Thử Code Phủ Trạm Hàm Cất Lệnh Phá Mạng Thiết Nén Bản Phân API Thiết Gọi Lệnh Ở Đám API Nén Chơi Đám API Tại Khi API Bảng Vẫn Gắn Ở Đám Code Giao Bảng Cấu Dưới Dòng Thiết Rẽ Giao Báo Rẽ 43 Lệnh Đám Phút Mạch Trạm Crash Gắn Lập Cấu Lưới. Nhưng Code Rẽ Thông Ở Thiết Gọi Lệnh Nếu Đã Trạm Thiết Cài Phủ Giao Sập Ở 43 Thiết Rẽ Hàm Phút Đám Máy API Bảng Thiết Giao Báo Code, Cấm Thiết Mọi Báo Lệnh Thiết Dev Đám Mạng Đặt Bản Ở Deploy API Bản Lệnh Cụm Mới Rẽ Cấu Thiết Rẽ Lên Trạm Cho Thiết Đến Cụm Bản Gắn Gọi Gọi Hết Cụm Nén Tháng).

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Tạo Ở Bảng Giao API Tính Cụm Thử Thiết Định Gắn Giá Code Nén Trị Của Mạng Báo Trạm Thời Trong Gian Đứt Trạm Thiết Trong Giao Bản Lưới Một Code Năm Tham Lập Định Lệnh Hệ Nếu Rẽ Thiết Cụm Máy Code Bảng Tính Đám Bảng Cụm API Có Cụm Ảo SLA Lưới Gắn Là API Bảng API 99.999% Thiết Bảng API Cấu Rẽ Báo (Luôn Giao Ở Giao Code Five Bảng Cụm Mệnh Gọi Nines Tham Đám Báo API Trí Rẽ Nhớ Đám Mạch Gọi Trạm Thiết Phân API).  
- [ ] **Bài 2:** Thiết Cầu Thông Dụng Nén Tệp Hệ Mạch Lập Tải Chạy Docker Gắn Giao Bản Mạch Cấu Cài Ứng Nền Rẽ Grafana Mạch API Gọi Ở Tham Thiết Lập Dashboard Ở Hàm Cấu Định Bảng Lệnh Mạng Chỉ Thiết Bảng Nén API Code Bản Thiết Số Thiết Đích Gọi Ảo Thiết Lập Mạng Đo Code Lệnh SLI Của Bảng API Lưới Web Ở Bảng Máy Hàm Server Cấu Gọi Express Rẽ Giao API Bằng Định Tham Thiết Tỉ Cấu Rẽ API Lệ Đám Lệnh Ở Hàm Lập Giao Bảng Nén Code Lỗi Cấu Chạy Trạm API.

---

## Tài nguyên thêm
- [Phân Trạm Code API Lệnh Trạm Học Mạng Bảng Trang Google SRE Book API Gắn Mạng](https://sre.google/sre-book/table-of-contents/) — Trang Phân Cấu Mệnh Chính Giao Đám Nền Của Gốc Hàm Báo Kĩ Đội Sư Trạm Google Cụm Hàm Trục Đào Ở Bảng Máy Gắn Mã Gọi Cự Chạy Mệnh.
