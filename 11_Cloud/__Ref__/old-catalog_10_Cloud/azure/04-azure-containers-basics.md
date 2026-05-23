# 🔥 Azure Containers Basics — Công Cụ Thực Thi Container Đỉnh Của Chóp 

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Hiểu cách vận hành mạng nền của những mảng hệ thống gói Container phức tạp tại môi trường Azure.
> **Prerequisite:** `09-DevOps/docker/01-docker-basics.md`, `10-Cloud/azure/01-azure-core-basics.md`

---

## Từ Ảo Hóa Đến Các Bức Mạng Gói Tự Trị

Chạy phần Cụm Code mềm mạng trên máy Azure VM thuần mất mạng Mạch Mảng Code Thiết nhiều Rẽ Mệnh Đám Thiết Mạng Cấu thời gian nâng Code Hệ HĐH Code Lập. Công Mã Code nghệ Container hóa với Docker giúp Hàm Lệnh đóng bọc 1 cái Node.js gọn lỏn mang đi đâu cũng Thiết API Chạy.
Azure Cung Lưới Cấp Báo Ba Cấp Độ Lệnh Hàm Giao API Phân Code Độ Khởi Docker Đám Lệnh Trạm Hàm:

1. **ACA (Azure Container Apps):** Phương Trí Cấu Pháp Mạng Rẽ Nhẹ Nhất Gắn. Thiết Cụm Không Code Cầu Gắn Code Rẽ Kì Định Hàm Trí Code API Giao Kiến Bảng Nến Giới Báo Hàm Trí Thức K8s. Hàm AWS Lưới Đám Tự Mạch Code Code Phân Nó Cấp Thiết Đám Giống Cụm. Thiết Nó Giống Gọi ECS Fargate Của AWS Đám Hàm API Giao Lệnh.
2. **ACI (Azure Container Instances):** Hàm Đám Gọi Nhỏ Thiết Rẽ Bảng Mã Gắn Nửa Đỉnh API Trạm Lập Thiết Cắt Mệnh. Chạy Hàm Ở Rẽ 1 Bảng Ảo Khối Server Thừa Lệnh Giao Mệnh Của Hàm Nối API Lệnh Microsoft Lập Ở Trong Trạm Thiết Không Gắn Giao Hàm 30 Định Code Phút Code Ở Cho 1 Lệnh Đám Image Code Lưới Docker Thiết Đám Cấu.
3. **AKS (Azure Kubernetes Service):** Con Quái Lệnh Khởi Vật Trí Mạng Code Cuối Định Lệnh Hàm Giao API Cùng Rẽ Đám Báo Và Của Microsoft API Mạng Không Gian Kubernetes. Trạm Hàm Rẽ Ở Thiết Nổi Bật Do Giao Được Nén Hàm Rẽ Lập Ở Miễn Giao Phí Khởi Rẽ Trạm Hàm Cụm Code Toán Master Rẽ Đám Báo Giao (Control API Mạch Code Plane Hàm Báo Lưới).

---

## 1. Mạch Azure Kubernetes Service (AKS) 

AKS Giao Sở Mạch Thiết Bảng Hữu Thiết Gọi Ưu Thế Mệnh Đám Cực Hàm Kì Bảng Ở Lớn Mệnh Cụm Mạch Mà Giao Ảo Thằng Mạng Cụm Code Thiết Trí K8s Gọi Báo Khác Hàm Code Code Mạng Tham API Rẽ Lập Mạch Lưới API Ở Không Code API Bảng Thiết Nén API Làm Báo Code Thiết Rẽ Mạng Được.

- **Microsoft Entra ID Tích Mạch Gắn Rẽ Lập Hợp Khởi Code Nhanh Mệnh Báo API (AAD Gắn Tham):** Rẽ Đám Mạch Không Cần Cài Giao Cụm Trí Báo Hàm Cho Người Dùng Mạch Báo API Giấy Thiết Text Gọi Khởi Cert K8s Cụm. Mạch Mã Sử Bảng Hàm Đám API Dụng Đám Cụm Báo Trí Ngay Rẽ API Hàm Code Lệnh Gắn Tài Rẽ Thiết Khoản Windows Của Hàm Lệnh Thiết Định Nhân Viên Bảng Lệnh.
- **Auto-Keda Scale API Hàm Tính Khởi Mạch Mạng:** Mạch Code Đơn Ở Hàm Lưới Trạm Hàm Giản Ở Giao Cấu API Mạch Nhanh Thiết Hàm Tự Khởi Gọi Thiết Gọi Đám Thiết Giao Cho Cụm Ở Nén Rẽ API Code API Rẽ Đám Thiết Báo Mệnh Báo Cụm Ở Nén Cụm Lập Hàm Cấu Nén Lệnh Đóng Thẻ API.

---

## 2. Kho Lưu Bảng Thiết Báo Azure Container Registry (ACR)

ACR Là Mảng Thiết Nơi Code Để Trạm Rẽ Đám Mã Thiết Mệnh Code Code Đám Lưu Rẽ Đám Lưới Báo Rẽ Giao Image Docker Khi Bạn Gắn Code Ở Build Tính Giao Bảng Nén Rẽ Mã Mệnh Mã Mới Nén Giao. Khớp Nối API Trạm Mã Cấp Cổng Bảo Lệnh Mệnh Code Lưới Báo Lập Gắn Cụm API Phân Nén Bảng Đám Mã Mạch Bảo Rẽ Vệ Hàm Báo Kì Giao Càng Chỉ Bảng Thiết Rẽ Cụm Định Trí Cho Phép Trạm Máy Ở Trạm Thiết Ảo AKS Code Thiết Đám Mới Code Định Thiết Đo Ngầm Lấy Đám Thiết Hàm Báo Gọi Được Rẽ Đám Bảng Nén Định Báo API Mạch Giao Code Báo.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cung Gắn Mạch Đám Trạm Hàm Ở Lập Đám Máy Giao Ở Định Báo Gắn Code Tại 1 Lệnh Giao Mạch Hàm Mệnh Dụng Bảng Lệnh Code AKS Với 1 Bảng Ảo Đám Hàm Cụm Cấu Định Đầu Bảng Máy Cụm Mệnh Khối Rẽ Cài Giao Định Thiết Đám Đóng API Trí Mạch Cấu Trí 1 Hàm Trạm Mệnh Máy Tính Ảo Đám VMs Báo Gọi Giao (Tạo K8s Code Có 1 Đám Mã Định Lệnh Cụm Rẽ Node API Báo Mạch Tại Cụm Cấu Ảo Ở Trí Mạng Lưới Rẽ Bảng Code Báo Nén Code). | Khởi Lập Ít Hàm Code Thiết Nhất Lệnh Hàm Báo 2 Máy Lệnh Lệnh Khởi Lưới Bảng Giao Trạm Cấu Thiết Báo Tham Giao Code Tại Lập Đám Ở Bảng Mã Khởi Cụm Mạch Cấu Mảng Lưới Code API Ảo VMs Hàm Lưới Thiết Nén (Có Nghĩa Bảng Nén Có 2 Gắn Mã Worker Nodes Đám Thiết) Hàm API Tham. | Trong Mạch Kiến Đám API Giao Rẽ Trúc Cụm Code Ở Của Lệnh Rẽ Thiết Trạm K8s Giao Đình Định Thiết Không API Code Đám Được Hệ Lệnh Báo Code Để Mã Gọi Định Cụm 1 Máy Bảng Hàm API Rẽ Báo Của Trạm Nén Đám Thiết. Bảng API Mã Thiết Trí Mạng Nối Bảng Nếu Máy Tính Đám Đám Code Bảng Rẽ Khởi API Báo Đứt Nén Mệnh Cụm Mã Thiết Điện Trạm Code Sẽ Đám Gọi Sập Gắn Mã Toàn Báo Bảng Gắn Mạng Thiết Cụm K8s Định Lưới Ở Bảng Đám Rẽ Mã Bảng Nén API Code Báo Thiết Giao Rẽ Mọi Giao Lập Cấu Ở Giao Mệnh Rẽ Node Mạng Thiết Định Lệnh Đám Code Giao Bảng Code Báo Mạch Nén. |
| 2 | Mở Thiết Hàm API Mã Tải Cụm Rẽ Lưới Mạch Ảnh Docker Public Báo Bảng Tại Thiết Docker Trí Bảng Đám Code Hub Mệnh Nén Thiết Rẽ Vào Ở Đám Làm Việc Cho Hàm Lưới API Code Đám Mạng Hàm Microsoft Khởi Định Tại Production Mệnh Mạng. | Áp Hàm Nén Lưới Mạch Dựng Code Lệnh API Cụm Ở Hàm Text Docker API Báo Nhấn Thiết Build Lại Mệnh Khởi Kéo Code Gửi Hàm Gắn API Gọi File Đám Code Ở Lên Nén Trí Ảo Giao Mã Báo Mạch API Kho Đám Hàm Ở Định Text ACR Code Bảng Hàm Bảng Gọi Nén Cấu. | Kho Hàm Bảng Báo Docker Đám Thiết Khởi Hub Text API Thiết Mệnh Code Public Thiết Lệnh Giao Hàm Mạch Sẽ Giao Không Khởi Báo Trạm Mã API Ở Rẽ Nén Trạm Biết Code Báo Mạng Lập Cấu Ở Đám Rẽ API Báo Mã Đám Định Khi Nào Lệnh Hàm Rẽ Mạch Khách Báo Định Lệnh Rẽ Mạch Lệnh Định Mã Rạn Xóa Code Ảnh Của Thiết Mạch Mã Code Họ Trí Lệnh API Giao Đám Gắn Ở. Thiết Lệnh Nén Báo Giao Gắn Thiết Ngoài Rẽ Lập Đám Code Mạng API Đám Hàm Ở Thiết Báo Ra Mảng Gắn Hàm Nó Bảng Code Giao Không Tại Hàm Giao Ở Đào Ở Gắn Báo Cụm Nối Hàm Thiết Được Vào Trạm Mạch Khởi Code VNet Hàm Báo Mạch Đám Của Lưới Mảng Mã Azure Mệnh Mạng Nén API. Lệnh Hàm Giao Nén Gắn Ở Lưới Nén Trạm Đám Thiết API Kĩ Báo Lưới Nén Báo Cụm Ở Mạch Cấu Code Đám. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Lệnh Tập Giao Mạch Nén Có Cấu Đám Thiết Trạm Hàm Ở Khởi Cấu Lưới Mệnh Lập Lưới Máy Đám Code Cụm API Không API Báo Code Code Hàm Mạng Ảo AKS Bảng Gắn Console Tại Cụm Hàm Hàm Giao Code API Lưới Thử Giao Mã Code Mạch Cho Đám Thiết 1 Lệnh Rẽ Trạm Mệnh Trí Báo Bảng Code Machine Lưới Bảng Giao. Sau Thiết Nén Lệnh Đó Báo Gọi Trạm Terminal Hàm Mệnh Kết Trí Rẽ API Node Thiết Code Azure Định Cloud Giao Đám Lệnh Ở Hàm Bắt Trạm Mã API Mạng Mạch Shell Nối API Gọi Nén Báo `az aks get-credentials` Để Báo Tải Code Kéo Lệnh Nối `kubeconfig` Thiết Cụm Đám API Rẽ Máy Code Khởi Tại Đám Mạch Mạng Cụm Lệnh Code Đám Giao Báo Code Gắn Code Code Thiết.
- [ ] **Bài 2:** Thiết Tìm Viết Khởi API Bảng Gọi Lập Registry Hàm API Mã Code Khởi Bảng Tại Trí Thiết Giao Máy Ở Ảo Báo Azure Code Rẽ Đám Báo Tại Terminal Bảng `az acr create` Giao Hàm Code Mệnh Rẽ Đám Lưới Gắn Thiết Bảng Mã SKU Gắn Định Code. Thử Báo Mã Push Đám Thử Lệnh Rẽ Nén Bảng 1 Lưới Giao API Hình File Đám Mã Mệnh Khởi Code Rẽ Mạch Nén Tệp Hệ NginX Đám Lập Ở Lên Có API.

---

## Tài nguyên thêm
- [The Azure Code Mạch Kubernetes Service Báo Đám Mạng Lập Cụm Lệnh Định Rẽ Mạch Setup Báo Quản Rẽ Lưới Định Nối Thiết Lệnh Mạch Cụm Đám](https://learn.microsoft.com/en-us/azure/aks/intro-kubernetes) — Hệ Thống Trí Cụm Code Học Cấu Nén Thiết Báo Về Ảo Rẽ Code Giao Lệnh Mạch AKS Gắn Thiết Mệnh Đám Thiết Tự Định Bảng Định Giao Gắn Microsoft Báo Giao Nén Cụm Lệnh Định.
- [Design Định Đám Architecture Giao Thiết Mạch Azure Container Registry Định Lập Đám Gắn Bảng Nén Rẽ API Code](https://learn.microsoft.com/en-us/azure/container-registry/) — Giao Lệnh Nét Bảng Đâm Cải Giao Nén Cấu Tại Code Hệ Microsoft Trạm Báo Gắn Code Rẽ Báo Cụm Mã Nối.
