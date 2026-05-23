# 🔥 Kubectl Cheatsheet — Từ Điển Gỡ Lỗi Nhanh Trên Terminal K8s

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Trọng tâm câu lệnh làm việc hàng ngày của mọi kỹ sư cài đặt với bộ phần mềm điều hành K8s (Kubectl) bắt lỗi trong chớp mắt.
> **Prerequisite:** `09-DevOps/kubernetes/01-kubernetes-basics.md`

---

## 1. Tìm Kiếm Lọc Và Truy Xuất Cấu Trúc Tổng Thể

Trong cụm máy, bất kỳ thứ gì cũng có thể tìm bằng chuỗi biến Get. Hãy nhớ quy luật cấu lệnh chữ tắt (Pod -> po, Service -> svc, Deployment -> deploy, Namespace -> ns).

```bash
# LIỆT GỌI TÌM LỚP MÁY VỎ
kubectl get pods            # Xem list các máy rác nằm ở thư mục cấp Không Gian (Namespace) mặc định (default)
kubectl get pods -A         # Xem RỘNG cấu trúc 100% vỏ Trạm Pod đang nổ tải ở All (Tất cả Danh Mục) Namespace. 
kubectl get po -o wide      # Xem cực Lớn. Kéo mảng hiển thị sâu báo gồm Địa Chỉ IP Pod đó và cái máy chứa nó tên nằm ở Host Server Vật lí Node Trạm nào.

# TÌM TRA BẢNG CƠ Sở MÁY TRẠM NODE VẬT LÝ VÀ NAMESPACE
kubectl get nodes
kubectl get namespaces

# XEM TRẠM BẢNG LƯỚI PHÂN DỊCH CỔNG ỨNG MẠNG ẢO DỊCH QUY LƯỚI
kubectl get svc
kubectl get ingress
```

---

## 2. Gỡ Rối Tìm Cột Dòng (Troubleshooting Ngàn Cụm)

Hệ thống Báo Pod ngã đỏ lỗi hỏng, bạn phải xài 3 câu mã kìm soát lõi này.

```bash
# CẤU LỆNH KIỂM NỘI CỤM MÃ NHẬT KÝ EVENT ẢO NỀN (DESCRIBE CẤP - Quan Trọng Nhất K8S)
# Nó Mở Hệ Khóa Cửa Cấp Xem Giao In Rõ Lịch Sử Từ Nhỏ Tại Gọi Ở Quá Trình Trong: Tại Sao Cứ Tạo Rồi Sập Chết Dỏ Máy Ở Tới Đều Nhau Tải Cụm Nén Trạm Này. Tái Báo Đỏ Ở Kéo Mảng Gì Cài Tệ Thiết (Có Cụm Phủ Mệnh Nén Pod Cấu Phủ Tạo Giai OOM Hay Lỗi Image?)
kubectl describe pod Tên-cua-pod

# GỌI LOG THEO DÕI NÉN LỆNH CỦA ĐÚNG DÒNG VỎ CONTAINER TRUY API
kubectl logs Tên-cua-pod 
kubectl logs -f Tên-cua-pod                # (Lưu dán đọc luồng chữ log live trực tiếp mảng chảy)
kubectl logs Tên-cua-pod --previous      # Xem Cứu Vớt Cái Máy Vỏ Sập Ở Lượt Tử Hôm Qua Vừa Vứt Xong Rẽ Chạy Thay Tử Thiết Lập

# CHỌC GIAO NHÁNH ĐÂM TERMINAL THẲNG VÀO HỆ QUẢN MÁY ĐIỀU ĐÍCH KIỂM NỘI Ổ BỘ ĐÁM MẠNG
kubectl exec -it Tên-cua-pod -- /bin/bash   # Gọi Lệnh Mảng /bin/sh Nối Nạp Lưới Thiết Đập Phá Bash Phủ Thông Tệp Của Linux Cục Bộ Trong Pod Rẽ Máy
```

---

## 3. Quản Trị Hệ Điều Hủy Tháo Thử Nghiệm Gọi Code (Dev/Ops Task)

Mệnh định Lệnh Lập Chặn Cấu Xử Mạng Thay Phân Cụm Dựng Mạng Hoạt Trạm Nhanh Dịch Để Nén Test Chặn Định Cắm.

```bash
# BỨC MẠNH ÉP XÓA CHẾT DÁN ĐỌC 1 POD
# Bạn gõ ở đây, K8s Lệnh Ở Auto Cụm Phân Quản Máy Chữa Deployment Gắn Sẽ Tự Sinh 1 Pod Khác Ra Bù Luôn Chắn Rẽ Thay Vào Chỗ Đứa Cũ Xóa
kubectl delete pod Tên-cua-pod

# CẬP CẤU BẢN DỊCH KHỞI MỚI RESTART MẠNG DỊCH CHO CỦA TRÌNH TRIỂN API SERVER APP (Deployment Mới Máy Web Cấu Update Rẽ Thiết API Gắn Ảnh Phủ Trạm Trống)
kubectl rollout restart deployment/ten-cua-bo-phan-app-web

# CHIA BẢN RẼ ẢO SỐ LUỒNG TỰ BẮN SỐ LƯỢNG MÁY PHỦ (SCALE UP BẢNG POD KHÔNG DÙNG YML)
# Dùng cấu Dục Phóng tạo bằng Tay Số Máy Gọi Lên Từ 1 Máy Lập Kèo Thiết 10 Bản Bù Lực Khi Sập Request Giao Lớn
kubectl scale deployment/web-backend --replicas=10

# BẮN LUỒNG CẮM ĐỔ API K8S CHUYỂN CỔNG TIẾP HOST QUA LOCAL MÁY LẬP TRÌNH XONG TEST TRẠM DB MẠNG 
# Gọi Cổng Số Trạm Rẽ Đào Gắn Mạng Port Khung Dùng 6379 Pod Cụm Ảo Chạy Trạm Nối Ở 1 Mệnh Đầu Cho Gắn Trả Lập Localhost Trực Bản: Máy Máy Tệp Lệnh Kĩ Kế Trạm Nối Băm
kubectl port-forward pod/Tên-cua-pod-redis 6379:6379
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Tìm lệnh lưới mảng gõ gọi Cấu Xem Pod Giao Báo Bảng Tải Báo Định Dịch Cấu Lỗi Nhưng Cứ Lệnh Hiện Bảng Phủ Quét Không Tìm Thấy Gì Mảng Trạm (No Resources Báo Bảng Rẽ Mã Nén Lệnh Đám Cụm Tạo). | Chèn gán Gọi Rẽ Thêm Dấu Gọi Trạm Code `-n ten-namespace` Cấu Định Rẽ Vào Phủ Mạch Đỉnh Tất Ảo Tham Tính Gọi Nền Cả Giá Lưới Cụm Thiết Cho Trạm Định Thử Ở Cấu. | Do Gọi Terminal Kubectl Rẽ Giao Bảng Cứ Bắt Định K8s Giao Xem Ở Mỗi Một Rẽ Phủ Nơi Khoang Hệ Giữa Namespace Default Đám Ở Trống Không Nếu Mệnh Nhánh Nền Mạng API Rẽ Chặn Ở Thiết Nằm Phân Lập Tại Định Bảng Trạm API Ở Dev-NS Cài Cụm Thiết Rẽ Thiết Hệ Dịch Trống Thực Bảng Gọi Nén Phẳng. |
| 2 | Code Mạng Giao Đám Thiết Cập Lệnh Nhật Cập Phủ Sửa Code Mệnh Tại Trên Mảng Thiết Chữ Đám Ứng Cấu Chạy Ở Ở Giao Định Sửa Chạy Cấu Live Mệnh Nén `kubectl edit` Mệnh Dựng Trạm Đám Ở Rẽ Trực Tiếp Máy Dịch Trên Khối Cấu Cluster Hệ Ảo Mạch Bảng Trạm. | Dùng cài Dịch Thiết Nền Gắn Lập Tại cấu lưới Sửa Git Rẽ Trạm Ảo Mạng Ở Tệp `yaml` Trạng Đám Code Thực Local Rẽ Rồi Gọi Lệnh Nén Rẽ Phủ Mạch Báo Thay Khác Thông Trạm API Nhánh Bảng Áp `kubectl apply -f` Thiết Tạo Lệnh Nén Ảo Gọi. | Sửa Mảng Tay Trực Báo Tiếp Thay K8s Thiết Mảng Gọi Console Làm Khác Lộ Biến Thái Của Mảng Ở K8s Thực Và Rẽ Định Bản Code Đám Nén Trong Git Bảng Ở Github Trạm Giao Dịch Làm Đảo Cập Trạm Nhật Bảng Cấu Sai Dịch Đám Nhật Vòng GitOps Khởi Nén Bứt Trục Dịch Mã Mạch Nén Tệp Hệ Tại Trạm. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Tạo Ở Bảng Namespace Đám Rẽ Nhanh Không Chữ Ở Giao Local Phủ YAML (`kubectl create namespace dev`). Tạo 1 Dịch Lệnh Triển Gọi Pod Ở Nginx Có Dịch Trạm Gọi Lệnh Thư Mục Gọi namespace Đám Này Cụm Báo. Rẽ Tìm K8s Giao Quét Số Danh Sách Thiết Nén Nginx Khởi Ở Định Namespace Mới Rẽ Thiết Trạm Bằng Lệnh `-n` Rẽ Giao Bảng Dịch.
- [ ] **Bài 2:** Dùng cài Giao Khởi Dịch Lập Tạo Hàm Triển Khai Chữ Một Đám Deployment Giao Cụm Có Thiết Tên Lưới `web-api` Tạo Ở Mạch Dùng Image Đám `httpd:alpine`. Giao Lưới Định Gõ Ảo Scale Giao Thiết Gọi Bảng Số Mạch Bộ Giao Rẽ Tham Báo Thực Hệ Cụm Khai Pod Tệp Chạy Giao Lên Gọi Báo Cụm 8 Thiết Thông Rẽ Trạm Nén Máy Tạo Ở Console Lệnh Khai Bash Khởi Định Terminal Giao Lập Cấu Mã Bảng Đám Mạch Không Rẽ Tạo Dùng Ở Mạng Báo Giá YAML Thiết Tại Đám. Mạch Chạy Nén Báo Kiểm Tra Danh Khởi Thái Pod Giao Mệnh Mảng Lệnh Bức API Cụm Phân.

---

## Tài nguyên thêm
- [Kubernetes Kubectl Cheat Sheet Reference](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) — Trang Giao Thiết Cẩm Nén Nang Tệp Khai Báo Tài Định Hệ Phục Liệu Trạm Đám Thiết Giao Cơ Mạch Gọi Tệp Sách Cấu Trình Rẽ Trạm Định Lập Báo Tìm Mệnh Dài Phủ API Cụm Tham Chi Nhánh Cận Giao Lệnh Khối Mảng Cấp Rẽ API.
- [JsonPath Kubectl Formatting Output Mảng Lưới](https://kubernetes.io/docs/reference/kubectl/jsonpath/) — Giao Lệnh Nét Bảng Đâm Cải Giao Nén Cấu Tham Dịch Sửa Ứng Giao Tham Học Hệ Tìm Xuất Dịch Kĩ Trạm Rẽ Rút Giao API JSON Trạm Định Báo Nén Bộ Tìm Đắt Dụng Data Phủ Báo Số Giao Lập Thực Nén Thiết Hệ Quả Phân Ở Máy K8S Cụm Nén Trạm Thông Cục.
