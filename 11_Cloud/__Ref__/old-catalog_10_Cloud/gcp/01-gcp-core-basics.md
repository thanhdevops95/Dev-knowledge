# 🔥 GCP Core Basics — Kiến Trúc Hệ Điện Toán Google Cloud

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Nền tảng hạ tầng đám mây tập trung cực mạnh vào dữ liệu lớn, Trí Tuệ Nhân Tạo và hệ sinh thái Kubernetes của Google.
> **Prerequisite:** `10-Cloud/01-cloud-overview.md`

---

## Từ Google Search Đến Google Cloud Platform

GCP ra mắt chậm hơn AWS nhưng được xây dựng trên chính hệ thống cáp quang ngầm toàn cầu và dữ liệu nội bộ đã chạy thành công sản phẩm Google Search và Youtube. 

Điểm nổi bật cốt lõi của kiến trúc Google Cloud Platform (GCP):
1. Mạng lưới lưới dùng chung mạng gốc Global (VPC Toàn Cầu). Khác với AWS (Chỉ Mở VPC Giới hạn trong 1 Vùng Region Thiết lập), GCP cho phép bạn tạo 1 VPC trải dài Mạng Lưới trên 10 nước, không cần NAT.
2. Dịch vụ phân tích khối mảng dữ liệu (BigQuery) vô đối trên mây.

Thuật ngữ của GCP:
- Máy chủ ảo: AWS gọi EC2, GCP gọi là **Google Compute Engine (GCE)**.
- Lưu trữ Tệp: AWS là S3, GCP gọi là **Cloud Storage**.

---

## 1. Tổ Chức Quản Trị Hệ Bằng Khối Projects (Dự Án)

Để tránh việc lặp xóa nhầm dữ liệu trên 1 tài khoản mây dùng chung, GCP quản lý tiền theo mô hình Thư mục: `Organization -> Folders -> Projects`.
- Mọi tài nguyên cấu hình (Máy ảo, Bộ chứa mạng K8s, IP tĩnh) ĐỀU phải tạo nằm trong 1 **Project (Dự Án)**. Mỗi dự án này như 1 phòng máy cách ly. Máy ảo GCE của Project A không thể nhìn vòng sang Project B trừ khi bạn cố tình Cắm Cáp nối (VPC Peering).
- Trạm cấu hình quản trị tính tiền riêng rẽ qua mã Billing Account cho từng Tệp mã Project. Khi làm xong, xóa Khối Project là dọn sạch 100% tài nguyên mạng phí trong nó.

---

## 2. Google Compute Engine (GCE) 

Dịch vụ rẽ nền tạo cấu hệ Máy tính ảo chạy Linux / Windows của công cụ Google.

- Lợi Code Mạng Trạm Thế Đặc Rẽ Báo Trí Giao Thù: Cho phép bạn tạo cấu hình máy trạm ảo tự chỉnh Custom Machine Type linh hoạt (Ví dụ bạn không thích máy 2 Core 8GB RAM, bạn có thể chỉnh thông số tạo đúng máy 3 Core, Lắp 11 GB RAM để đỡ tốn tiền dư phần cứng).
- GCE áp dụng mạng tự động giảm thuế phí giá tiền mạng tính toán (Sustained Use Discounts) nếu bạn cứ bật chạy cái máy tính đó nguyên 1 tháng liên tục (Tự giảm giá 30% tiền điện toán mà không Lệnh Báo Code Bảng Gọi Thiết cần bắt kí Cam kết 1-2 năm như hãng AWS RI).

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cung Gắn Mạch Trạm Mạng Lập Quét Toàn Bảng Mã Quản Lệnh Báo Trị Tài Nguyên Của Bảng Máy Giao Lệnh Thông Lưới Mã Qua Cụm Hệ Báo Lập Gắn Cấu Bảng IAM Ở Rẽ Báo Cấp User Đơn Lập Gắn Lẻ Đám. | Sử Hàm Thiết Mạch Định Bảng Code Báo IAM Áp Dụng Lên Cụm Cấp Code Bảng Trí Lập `Project` Định Hoặc Bảng Cấp Code Trí Hàm `Folder`. | Việc Áp Dụng Quyền Xem Và Khởi Báo Đám Lưới Gắn Cụm Tạo Ở Mức Hệ Nền Cá Nhân (Giao User Bảng) Hay Mạch Máy Báo (Service Bảng Account Rẽ) Trạm Trực Đám Mạch Gọi Tiếp Cho 1 Điểm Rẽ Bảng Máy Bảng Lệnh Giao Tạo Ở Hệ Thiết Mạng Báo Khó Code Mạng Quản Báo Lý Hàm Báo Mạch Cụm Hóa Rẽ Đơn. Chỉ Giao API Code Giao Nên Gán Lập Code Ở Quyền Quản Lệnh Gọi Code Lý API Nhánh Thiết Trực Hệ Tiep Mã Ở Cấp Code Giao Project Đám API (Anh A Code Mạng Là Lệnh Giao Báo Code Mạch Server Đám Admin Ở Mảng Lệnh Bảng Báo Rẽ Dự Án 1). |
| 2 | Mở Thiết Hàm Rẽ Cấu Rẽ API Giao Lưu Máy Trạm Khởi Đám Lưu Files Ở Hệ Dịch Vụ Mảng Bảng Báo Code Gắn Google Đám API Cloud Storage Cấu (Gắn Bảng GCS Bảng Hàm Lưới Bảng) Nhưng Để Code Công Khai Truy Lập API Trạm Mã Cổng Public Báo Đám Cụm Toàn Cầu (AllUsers). | Kích Lập API Hoạt Báo Cấu Trí Chế Code Báo Cụm Ở Mạch Độ API Lập Gọi Hàm Uniform Hàm API Đám Trạm Báo Mạch Bucket-Level Đám Rẽ API Code Access Hàm. | Trạm API Lưới Code Lập Giao Báo Trí Tịnh Tiến Hàm Đám Các Giao Bảng Cấu Rẽ Thiết Lệnh Mã Code Trạm Ở Dịch Gắn Báo Cụm Lập Quản Giao Lý Hàm Mệnh Thiết Hàm Code Lưới File Rẽ Mạch Báo (GCS) Bảng Giao Lệnh Code Nếu Bảng Code Lập Để Mạch Giao Ở Cụm Tính Năng Trạm Danh Code Mạch Trạm Truy Xuất Giao Trạm Ở Hàm Công Báo Khai Báo (Fine-grained Đám) Có Thể Đám Giao Hàm Rẽ Code API Đám Làm Hàm API Code Ở Mệnh Báo Lỗ Báo Hổng Bảng Trí Ở Hàm Đám API Rẽ Rò Đám API Nén Giao Rỉ File Do Cấu Lập Code File Lệnh Báo Bí Mạch Ở Đám Trạm Định Đám API Báo Code Code Trí Mệnh Lệnh Ở Giao Mọi Người Code Đám. Bật Tính Lệnh Năng Báo Mạch Định Uniform Giúp Đám Giao Bắt Ở Buộc Áp Hàm Đám Quyền Mã Lập Gắn Báo Lưới Mã Rẽ Theo Cấp Rẽ API Báo Giao IAM Mệnh Báo Code Thiết Bảng Code Ở Code. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Báo Tại Code Thiết Mạch Google Báo Lưới Bảng Cấu Code Rẽ Đám Cloud Console Mạng. Tạo Hàm Hàm 1 Lệnh Dự Báo Trạm Án Mới Đám Có Báo Mã Trạm Lệnh Tên Lập API Code Giao Định `Lab-Bao-Mat-Cơ-Bản`. 
- [ ] **Bài 2:** Thiết Cầu Thông Dụng Nén Tệp Hệ Mạch Lập Tải Chạy Cloud Đám Code Ở Lệnh Shell Báo Code Đám Cụm Rẽ Mạch Nén Giao Hàm (Khung Mã Console Code Trí Có Mạch Sẵn Báo Máy Mệnh Bảng Hàm Lệnh Cấu Lưới Báo Rẽ Trạm Ở Ở Của Google Lệnh). Sử Code Dụng Báo Code Hàm Lệnh Lập Trí Hàm `gcloud compute instances create may-phu-1 --zone=asia-southeast1-b --machine-type=e2-micro`. Vào Code Trí API Khởi Báo Trạm Đám Trí Kiểm Mạch Giao Code Bảng Giao Tra Bảng Hàm Sự Lưới Mạng Hiện Ở Hàm Báo Diện Của Bảng Máy Mạch Code Bảng Ở Đám.

---

## Tài nguyên thêm
- [The GCE Official Document Trí Cụm Code Học Thiết Báo Về Ảo Rẽ Giao Dịch](https://cloud.google.com/compute/docs) — Giao Tài Hàm Code Lưới Mạch Định Code Ảo Báo Mạng Khởi Định Giao Đám Thiết Của Lệnh Báo Máy Google Trạm Code Ảo Mạch Bảng GCE Lệnh Rẽ Thiết.
