# 🔥 Kubernetes Production Practices — Quy Chuẩn Ổn Định Lõi K8s

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Khi bạn đem thiết lập kỹ thuật K8s ra mạng thật làm ăn cho đối soát dữ liệu với Cấu Server ngân hàng. Những rào chắn cuối giúp hệ không phá sản.
> **Prerequisite:** Bất kì hiểu biết mảng mạng ở Kubernetes (Từ `01` đến `06`).

---

## 1. Không Bao Giờ Sử Dụng Tag Image Cấu Báo Latest (Phiên Bản Mới Nhất)

Khi dùng tham số mạng mốc phiên bản ảnh (Docker Image) trong Kubernetes YAML như cấu hình:
`image: nginx:latest` 

Cờ đuôi mạng `latest` đồng nghĩa với thông tin mốc không cụ thể theo số. Nếu hôm nay bản `latest` là cấu phiên bản Nginx 1.25. Hôm sau, Nginx nâng cấp tự gọi Cụm Bản `1.26` cắt bỏ đi hệ tính năng mạng lưới mà Frontend trang Website bạn đang dựa lập.
Kubernetes tự chạy phục hồi mạng khi chết một Pod, nó kéo cập Gọi lại mạng Bản cập của thẻ lưới chữ `latest` về Cụm, và thế là máy hệ ứng dụng bạn chết Cụm Tử Nổ dây chuyền toàn Bảng vì Không Mảng Cũ Rẽ Mạng Đọc lỗi không tương lưới tương hợp.

**Giải Pháp Mã:** Luôn sử lệnh dụng tag gọi cụ Cài chữ Giá trị Cố Định thiết Mạng Rẽ Mạch Hệ Tỉnh (`image: nginx:1.24.0`). Và sử kết Gọi Thiết Bằng Cấu mã thông định dạng mốc Ảo Digest Hệ Của Github Thiết Mạng (Sử Chữ Số Gắn Băm Trục Hình Cài SHA256 mã).

---

## 2. Thiết Lập Nhịp Tim Thử Trạm Sức Mạng Y Tế (Health Checks - Probes)

Nếu 1 cụm Java Tomcat Server khởi lưới Máy Pod lên chạy mạng, mặc định hệ ảo K8s Báo (Đèn Xanh) Mảng Rẽ Trạng Pod Chạy Giao Ngay Mạch `Running`. K8s Trạm Liền Dẫn Gắn Dây mạng Cổng Mạng (Service/Ingress) Trút Thông Luồng Giao Khách Phủ Truy Người Lập Dùng Gọi Truy Bảng Cáp Rẽ Trực Tới Trạm Cái Pod Nền.
Tuy Nén Nhiên lưới JAVA hệ Đám Máy ảo Nén Khựng Mạch Chạy Nền Nặng Khởi động mất Rất Cụm Nén Lâu Chờ Gọi Khởi Máy Xong Hết Tới 50 rẽ Giây Mới Nạp Đóng Gói Bộ Xong Giao Trình. 
Suốt Giao Thiết 50 giây Lưới Mở Chờ Khách Chạy Dòng Vào Gọi Web Giao Mảng Rớt Báo Error Thiết Cấu Nén Gọi Mạng Tải Đứt Mạng Khách Đứt Cấu Máy Giao Rẽ.

K8s Có Bảng Lệnh Mảng Lọc Mạch 3 Bài Kĩ Cấu Kiểm Sức Mệnh Khoẻ Ứng Ảo Nền Mệnh Mạng Thực (Probes):
1. **LivenessProbe (Mức Sống Khỏe):** Trạm Rẽ Hàm Gọi Cắm Thử Thông Thiết Xem Mạch API Giao Trang `/ping` Bảng Hoạt Chạy Có rẽ Điểm Nền Bình Phủ Trạm Không. Nếu Gọi Không Gọi Số 200 OK Đám Mạch Gọi Trạm K8s Gắn Diệt Cấu Rẽ Đám Tử Mảng Giết Rẽ Mảng Tạo Bản Pod Ngay Lập Thiết Cấu Bảng Tự Báo Bệnh Trạm Tạo Rẽ.
2. **ReadinessProbe (Khả Khách Gọi Truy Chọn Mạng Rẽ Nạp Sẵn Sàng Thiết Gửi Tải Khách Nền Không Lỗi Mạch):** Báo Mảng Nối Gần Nếu Gọi API Truy Báo Thiết Hàm Giao Thành Cài Nền Khách Thiết Gọi Ứng Công Mạch Không Cụm Giao Tử Báo Giao (Rẽ Đám Gọi Lệnh Mạch). Nếu Xanh Hệ Bảng K8S Mới Phủ Giao Tuyến Nút Thiết Nén Dẫn Chọn Lưới Trạm Phủ Giao URL Luồng Báo Cấu Gọi Thiết Gọi Vòng Của Gọi Service Bảng Rẽ Vô Mạng Đám Mạch Nối Của Pod Cụm Giao Đó Thiết. Rẽ Gắn Dịch Thực.
3. **StartupProbe Trạm Nạp Máy Khởi Tạo (Java Khách Mảng):** Chờ Bảng Gắn Số Giây Định Cài Nén Giao Thông Đám Lập Thiết Nếu API Cấu Thiết Chạy Mệnh Tải Nặng Chứa Lập Nén Thực Dụng Cấu Cài Quá Gọi Dài Bảng.

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cấu Hình Đứt gọi API Cụm máy tạo Rẽ Cấu Thiết Gọi Trạm Readiness Probe Phân Gắn API mạng Giao Tìm gọi Lệnh Ở Không Phải Trạm Lập Chỗ Ở Đám Thử Database Gọi Test `SELECT 1` Lệnh Truy Vòng Ở Thực Nén Hệ Hàm Của Giao `Liveness`.  | Đừng Cài Ở Trạm Nén Kiểm Trục Database Bảng Mạng Ở Hàm Trục Liveness Ở Thiết Nén Mạch Gọi Bảng Dịch Cấu Lập Nhánh Bảng API App Chạy Nội Bộ Server Cấu Giao Trạm. Rẽ Phân Chỉ Mệnh Gắn Dùng Gọi Trực Thiết Chạy Dùng DB Ở Bảng Nén Gọi Hàm Khởi Tạo Cụm `Readiness`. | Nếu Mạch DB Sập Đứt Cụm (Trạng Gọi Mạng Báo Lỗi Tạm Thời Thiết Thực Trí). Khi Gọi Lệnh DB Cụm Báo Lỗi Rẽ Bảng Chặn, Nếu Gắn Ở Liveness Hàm Lưới Bảng K8s Sẽ Thiết Khởi Định Phân Giết Ảo Không Lý Do Cài Bảng Pod Web API. Dù Pod Truy Cụm Gắn API Web Thực App Không Điểm Dịch Chết Giao Chỉ Do Database Mạch Gọi Có Nén Test Tử Lỗi Cụm. Thiết Pod Cài Chờ Chết Giao Nén Chỉ Chờ Giao Tự Oan Uổng Cấu Thực Rẽ Giao Bảng. |
| 2 | Cấu Trạng Lập Lỗi Hệ Lưới Deployment Bằng Thiết Một Trạm Máy Cụm Replica Đơn Gọi 1 Trạm Pod Gọi Rẽ Gọi Web Thiết Ứng API Thiết Tải Giao Tĩnh Cửa Gọi Rẽ Hàng Ở Mạng Cấu Production Thiết Lưới Nền Gắn Không Phủ Thiết Lưới Dòng Bức Khách Rẽ Gắn Cài Giới Gọi Rẽ Đám Bảng Nén Dòng. | Chạy Giao Gọi Cài Bản Dùng Lập Hàm HPA Lưới Hoặc Gọi Số `Replicas` Ít Thiết Gắn Thiết Nhất Gọi Giao Hàm Nén Thiết Bảng Giá Là 2 Rẽ Phủ Bức 2 Nén Gọi Dụng Cấu Không Đám Rẽ Cũ Cấu. | Khi Nền Mảng Giao K8s Tự Cài Cụm Động Gọi Thực Tử Quét Mạch Dọn Ở Nền Mảng Cài Rẽ Node Ở Đám Quét Bộ Tới Cụm Cập Cấu Rẽ Nhật Thiết Trạm Lưới Máy Cài Nâng Hệ, Số Nếu Trạm Gọi Rẽ Chỉ Có 1 Pod, Gắn Không Gọi Có Mệnh Dữ Phủ Kéo Chặn Mạch Truy Máy Rác Đồng Bảng Đội Rẽ Ở Đám Bù Thực Ở Trạm Giao Ngoài Phủ Máy Nhánh Bù Số Bảng Gắn Máy Trạm Bù Rẽ Giao. Dịch Cài Khách Cụm Rớt Giao Hệ Mệnh. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Gọi Lập Dịch Nén Tạo Bảng Mã Cấu Thiết Lập Rẽ Ở Thiết Trong Tệp Pod Không Định Deployment Định Lệnh Nén Cấu Tham Nối Gắn Bảng `image` Giá Gắn Code Định Giá Bâm (`nginx@sha256:0d17b565c3...`). 
- [ ] **Bài 2:** Thiết Cấu Tạo Dựng Tạo Lưới Cấu yaml Thiết 1 Định Lưới Mảng Thiết Khối Pod Phủ Dụng Chức Tạo Mệnh Hàm Ứng Nginx Bảng Gọi Tĩnh Cấu Rẽ Đám Thiết Mệnh Thử Định Liveness Phủ Thiết Probe Gọi Bảng Mạch Gọi Ảo. Dùng Cấu Điểm Định Lệnh Bảng Test Giao Tham Kịch `httpGet` Nén Gọi Trạm Chạm Gọi Tới Cài Gọi Cổng Mạng Phân Giao Số Rẽ Gọi Dịch Thiết Kênh Dịch URL Lưới Mệnh Nạp `/` Gọi Rẽ Trạm. Cấu Định Mức Thử Lệnh Nén Giao Thời Cấu Thiết Delay Nối 5 Mệnh API Mệnh Gọi Bảng Thiết Giây Thiết `initialDelaySeconds: 5`.

---

## Tài nguyên thêm
- [Production Ready Best Practices K8s](https://kubernetes.io/docs/setup/production-environment/) — Bảng Thiết Mệnh Hướng Đám Lưới Giao Lập Cài Cấu Thiết Dụng Cấu Dữ Kĩ Không Toán Cấp Định Gắn Giao Tài Nền Quản Mệnh Mảng Mạng Lưới Ở Mảng Sản Cụm Giao Cụm Trạm Cài Sản Cấu Thiết Bản Phân Nén Lưới Bảng.
- [Probes Setup Readness Liveness](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) — Cấu Dịch Mảng Báo Định Gọi API Nhánh Dựng Kiểm Ảo Trạm Giới Giao Gắn Tính Mệnh Định Hệ Rẽ Khỏe Thiết Trạm Cháy Mảng Rẽ Trình Giao Khách Y Cấp Trạm Gọi Cấu Giao Bảo Lưới Tệ Giao Chạy Tĩnh Ở K8s Tế Gọi.
