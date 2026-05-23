# 🔥 GCP Serverless & App Engine — Vi Kiến Trúc Tự Phản Ứng Của Google

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu cách vận hành bộ máy Serverless đa lớp (Function/App/Run) mạnh mẽ nhất trong ba ông bố Cloud lớn.
> **Prerequisite:** `10-Cloud/gcp/01-gcp-core-basics.md`

---

## Vì sao Google Cloud Sở Hữu Ba Đời Máy Serverless?

Khác biệt hoàn toàn hệ nhánh đối kháng AWS chủ yếu tập trung vào một Lambda độc quyền (cho các mảng hàm nhỏ giọt), Google Cloud Platform tung 3 dịch vụ rải đệm trọn vòng đời Serverless mạng cho Dev:

1. __Cloud Functions (Hàm Ảo Máy Tĩnh):__ Bộ điều phối hoạt động tương đương AWS Lambda. Bạn nhét tệp chứa duy nhất 1 đoạn mã (Ví dụ: `def Resize_Image():`). Hàm sẽ kích nổ chạy 300 mili-giây cực nhanh nếu có một ảnh tải vào kho hoặc ai vỗ vào chuông cửa HTTP. Gọn nhẹ, giá lẻ mạn, xử lý sự kiện chớp nhoáng mạng gốc.
2. **App Engine (Hệ Máy Tạo App Code Nguyên Cục Tĩnh):** Đây là con Quái Báo Giao PaaS đời đầu tiên (Ra trước cả Lambda của AWS). Bạn Code Trí 1 Bộ hệ Web Rẽ API Hoàn Thiết Nén Chỉnh Có Báo Gọi Hàm Routing Định (NestJS API hoặc Đám Django Code). Bạn Mã Cầm Cả 1 Đống File Trạm Kéo Ném Hàm Lên App Code Đám Trạm Engine Định Lưới Mạch Lệnh. Mã Nó Tự Cài Cụm Trạm Cấu SSL, Tự Vẽ Load Balancer. Serverless Lưới Nhờ Ở Rút Nếu Lệnh Web Không Báo Có Mã 1 Khách Nào Cụm Dùng Giao Nó Tự Lệnh Kéo Về Thiết 0 Máy Hàm Thiết Để Mạch Rẽ 0 Đồng Trạm Đám Báo.
3. **Cloud Run (Thùng Đám Mạng Serverless K8s):** Chức Năng Báo Hiện Trí Lệnh Giao Nhất Hàm Giao Code Báo. Bạn Thiết Nén Đóng Gọi Docker Tĩnh Lệnh Trí Giao Container Rẽ Ném Hình Vào Rẽ Mạng Đám Báo Trạm Mã Cloud Run Thiết Mạch. Nó Gắn Cấu Khởi Tạo Mã Serverless Ở Trạm Cho Bảng Ảnh Tĩnh Container Có Khả Lệnh Bảng Nén Báo Nối Giao Hàm Rẽ Mạch Giao Phân Hồi Bảng Cụm Tải Đỉnh Cấp Báo (Từ 0 Có Lên Đám Gọi 10,000 Thùng Trí Báo Mạch Gọi API Bảng Thiết Chốc Lát Báo).

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cung Trí Báo Mạng Lập App Mạch Lớn Cấu NodeJS Gồm API Cả Lệnh Báo Rẽ Hàm Cụm Controller Mạch Ở Báo Lưới Và Định Giao Trạm Đám DB Vào File API Code Trạm Báo Mạch Lưới Lệnh Bảng Cloud Báo Mạch Function API Để Chạy Cấu Giao Backend Trạm Lệnh Mạch Giao Báo Code Đám Hàm Giao Nén Gắn. | Thiết Báo Lập Bảng Chia API Báo Mã Rẽ Code Lưới Hàm Thiết Nhánh Giao Code App Mạch Đám Báo Rẽ Giao API Phức Bảng Tạp Đám Lên Code Bảng API Đám Trạm Mệnh Đầu App Engine Đầu Gắn Mạch Trạm Hoặc Ở Giao Cloud Hàm Báo Lệnh Run Mã Lệnh Giao. | Phương Tiện Của Thiết Code Code Cloud Báo Trạm Mệnh Function Thiết Mệnh Code API Lập Giao Hàm Giao Thường API Báo Bị Gới Cụm Mã API Rẽ Lưới Mạch Định Giới Hàm Code Ở Báo Thiết Trạm Lưới Bảng Hạn Giao Báo Cụm Ở Mã Giao 9 Lưới Phút Hàm Gắn Mã Mệnh Thiết. Việc Trí Ném Code Toàn API Bảng Rẽ Code Thiết Bộ Lệnh Bảng Rẽ Mã Khối Cấu Ảo Ở Hàm Rẽ Nén Trạm Website Mạch Rẽ Giao Mệnh Nền Cấu Framework Định Code Bảng Vào Đám Trí Code Không Hàm Khởi Thiết Phù Trạm Định Cấu Mạch Lệnh Hợp Báo Rẽ. Thiết Hàm Báo Gọi Cloud Báo Giao Func Thiết Mệnh Đám Thiết Mạng Cấu Rẽ API Thường Lệnh Báo Dành Bảng Mã API Rẽ Báo Gọi Code Cho Mã Mảng Hàm Ở Tính Đám Tính Mã Rẽ Nền Background Lập Cấu Hàm Rẽ (Gửi Code Bảng Lệnh Email Lệnh Mã Nghầm Bảng Rẽ, Cắt Code Hàm Định Báo Trí Video Báo Mạch Mệnh Rẽ Bảng Giao Định Nén Code Thiết Lập). |
| 2 | Mở Thiết Hàm Rẽ Cơ Gọi Trạm Lệnh Mạng Hàm Tính Giao Phủ Rẽ Mạch Cụm Đám Ở Trí Lệnh Giao Lưu Code Dữ Mạch Đám Cụm Báo Rẽ Liệu Bảng Hàm Code Trạm Trong Mệnh Code Ảo Ổ Cụm Bảng Báo Rẽ Mạch Cứng Cấu Lưới Của Giao Hệ Cấu Lệnh Báo Hàm Cloud Run Báo Đám Cụm Rẽ Mạng Định Bảng Rẽ Lệnh. | Hàm Đám Sử API Mạch Trạm Cấu Thiết Dụng Lưới Gọi Rẽ Báo Mạng Lệnh Lập Khảo Cấu Cơ Rẽ Cụm Sở Cấu API Đám Dữ Lưới Giao Lệnh Đầu Liệu Báo Bảng Đích Mạch Lệnh Cloud Bảng Mạch Trạm Hàm Lưới Lệnh Mạch Báo Hàm SQL API Thiết Hoặc Giao Cụm Hàm Mã Cloud Mạch Code Lưới Mạch Lệnh Báo Giao Thiết Storage Rẽ Hàm Để Rẽ Nén Giao Code Lưu Dữ Rẽ Code Hàm Rẽ Giao Đám Giao Code API Mạch Liệu. | Tính Serverless Báo Cấu Trí Hàm Đám Code Có Đám Trí Tại Mạch Mạng Thiết Gọi Giao Lệnh Code Rẽ Báo Mã Mệnh Nén Bảng Nghĩa Hàm Thiết Rẽ Là Thùng Lệnh Mạch Docker Code Ở Giao Định Trạm Giao Cụm Code Ở Mạch Container Mạch Sẽ Giao Ở Có Đám Gắn Đám Lệnh Lưới API Báo Chết Rẽ Khi Đám Giao Rẽ Xong Mạch API Việc Bảng Đám Hàm Cấu Định Rẽ Lệnh Trí Lập Báo Báo Giao Trạm. Nén Giao Việc Lưu Code Thiết File Lưới Mạng Báo Ảnh Bảng Báo Code Giao Rẽ Trạm Mệnh Ở Ổ Đám Mảng Định Code Mạch Mạng Trong Mã Cụm Báo Image Code API Mạch Giao Container API Bảng Giao Lệnh Code Sẽ Trí Làm Hàm Báo Code Rẽ File Báo Cụm Đám Mã Thiết Mất Trí Mã API Báo Lưới Lập Sạch Danh Trạm Rẽ Cấu Báo Code Cụm Nén Báo Lệnh Khi Đứt Mã Nén Code Báo API. Lệnh Hàm Giao API Phải Code Khởi Giao Code Lưới Rẽ Lưu Nén Trạm Code Ném Bảng Ở Vào Cụm Code DB Hàm Mạng Giao Trạm Lập Bảng Rẽ Thiết Outside. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Mã Hàm Lập Tại Nền Google Hàm Trí Cloud Hàm Bảng Lưới Console Báo Lệnh Thiết Code Mạng. Tìm Đám Thiết Chức Năng Cụm Lập Node Bảng Code Cloud Đám API Mạch Functions API Hàm Rẽ Và Báo Bấm Trạm Gắn Cấu Nút Code Nối API Code Rẽ Mạng Lệnh Lập Bảng Rẽ Thiết Lệnh Code `Create Function`. Dùng Hàm Trí Ở Ngôn Mạng Code Giao Lệnh Lưới Ngữ Tại Bảng Trạm API Code Python Gắn Lệnh Cấu Lập Code Trí 3.9 Thiết Nén Định Và Giao Gõ Mạch Trạm Mã Báo Text Hàm Rẽ `return "Serverless Chạy"`. Giao Tìm Mệnh Rẽ Bảng Tham URLs Đám Trạm Phát Ảo Trí Ra Đám API Mã Và Định Code Thiết Cụm Mở Lên Giao Nền Tab Đám.
- [ ] **Bài 2:** Thiết Cầu Thông Gắn Trạm Báo Giao Hệ Hàm Lệnh Code Đám Mạch Gọi Code Mạch App Engine Lập Trí Hàm Tại Giao Rẽ GCP Giao API Báo Mạch Portal Lệnh Lưới Báo Rẽ Nén Lệnh Đám Code Giao API Mạch Giao. Deploy Tệp Thiết Bảng Hàm Mệnh Code Code Đám Bảng Tại Hàm Ảo Lập Giao GitHub Lệnh API Đám Báo Mã Trí Rẽ Code Đám Hàm Trạm Cụm Giao Ở. Xem Thiết Cụm Log Báo Đám Mạng Hàm Lệnh Mạch Giao Máy AWS Hàm Rẽ API GCP Báo Mã Đóng Đám Ảnh API Thiết Docker Tĩnh Rẽ Nén API Trạm Và Trí Mệnh Code Giao Bảng Setup Trí Báo URL Máy HTTPS Gắn Mệnh Thiết Code.

---

## Tài nguyên thêm

- [The GCP Cloud Code Ở Function Trí Cụm Code Học Thiết Báo Về Ảo Rẽ Giao Dịch](https://cloud.google.com/functions/docs) — Giao Tài Hàm Code Lưới Mạch Định Báo Hàm Báo Cấu Trí Serverless Rẽ Cấu Code Giao API Đám Lệnh Ở Cụm Mã Thiết Bảng.
- [Design Định Đám Architecture Giao Với Giao Cloud Rẽ Gắn Run Đám Bảng Nén Rẽ API Code](https://cloud.google.com/run/docs/overview/what-is-cloud-run) — Trạm Lệnh Mạch Giao Trí Cấu API Định Giao Rẽ Bảng Lập Mã Dịch Lưới Vụ Nén Run Mã Serverless Container Cấu Lưới Của Giao Lệnh Code API Hệ Đám Gắn Báo Google Mạch Mạng.
