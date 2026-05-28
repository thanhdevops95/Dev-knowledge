# 🔥 AZ-104: Microsoft Azure Administrator Chứng Chỉ Quản Trị Hệ Viễn Đám

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Đây là chứng chỉ quan trọng nhất cho người muốn làm Ops Cloud chuyên sâu trong hệ sinh thái của Microsoft.
> **Prerequisite:** Bất kì kiến thức nền tảng nào thuộc hệ `10-Cloud/azure`

---

## 1. Thông Tin Nền Tảng Giá Trị Giao Lệnh Kỳ Thi (AZ-104)

**Azure Administrator Associate (AZ-104)** không giống câu hỏi mang tính chọn mô hình Dịch vụ (Design) của SAA-C03 AWS. Bài kiểm định này thiết kế để kiểm tra sự am hiểu sâu về thực hành Cấu Hình Kỹ Thuật (Hands-on). Bài sẽ hỏi việc dùng Công cụ Lệnh (CLI) và chọn Nút Bấm. Rất nhiều ảnh chụp màn hình cài đặt. 

Cấu trúc kịch bản đề thi: (Trắc nghiệm khoảng 60 câu hỏi, thời gian cho phép 100 phút).
- Quản lý Microsoft Entra ID Cấu Danh Tính và Quản trị truy cập Cấp Quyền (RBAC) - 15%
- Triển khai Quản trị Lưu Lập Hệ Lưu Trữ Mạng Blob Storage - 15%
- Quản Quản Trị Bảng Hàm Các Cụm Máy Tính Compute (Azure VMs, AKS, Web App) - 20%
- Vận Giao Lập Hàm Mệnh VNet Hệ Mạng Lưới Nhánh - 25%
- Kiểm Lệnh Hàm Mạch Vận Soát Bảo Code Quản Trị Backup Trạm Azure - 15%.

---

## 2. Các Tập Lệnh Cơ Cấu Bắt Buộc Nhớ Azure CLI / PowerShell

Hệ thống AZ-104 xoáy nhiều vào các tập mã lệnh cấu PowerShell tự động của kỹ sư hệ.

```bash
# Tạo Cấu Mạch Resource Group (Nhóm Tài Nguyên Lệnh Code) Rẽ Hàm Microsoft Đám Cụm
az group create --name RG_TestApp --location southeastasia

# Khởi Tạo Mạch Code Lệnh Cụm Mảng Máy EC2 (Khởi Máy Ảo VM) Lệnh Code Mạng
az vm create --resource-group RG_TestApp --name VM_Demo1 --image Ubuntu2204 --admin-username localadmin --generate-ssh-keys

# Tạo Lệnh Hàm Hệ Code Mệnh Ảo Lập VPC Mạng VNet Khởi Khung Thiết
az network vnet create -g RG_TestApp -n VNet_ToanCuc --address-prefix 10.1.0.0/16 --subnet-name VNet_SubA --subnet-prefix 10.1.1.0/24
```

---

## Gotchas - Lệnh Bẫy Thi Thường Gặp Của Azure

| # | ❌ Cấu Báo Mã Câu Trả Lời Sai Hay Nhấn Bầm Nhất | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Mở Cấu Gán Thiết Bảng Trí Lập Thiết Mạng Code Hàm Quyền Hàm Quản Giao Trị RBAC Ở Báo Tại Cụm Từng Code Mạch Trạm Mạng Mệnh Chi Code Rẽ Chiết Từng Mệnh Chiếc Máy VM Báo Hàm Trí Lệnh Thiết API Code Mạng Giao Một Rẽ Hàm Cấu Đám Thiết. | Áp Hàm Thiết Dụng Áp Hàm Giao Quyền Tại Cấu Quản Cụm Báo Group (Bộ Rẽ Phận Mệnh Code API Người Mạng Thiết) Hoặc Tại Rẽ Code Mạch Resource Group (Cụm Báo Code Bảng Dự Án). | Bài Thi AZ-104 Luôn Yêu Cầu Ưu Tiên Tính Nguyên Tắc Quản Trị Lệnh Bảo Đảm Code Tối Ưu (Least Administrative Effort). Gắn Quyền Lệnh Tách Cụm Sẽ Dễ Mệnh Code Gọi Sai Lỗi Trí Thiết. Áp Quyền Tại Mạch Code Nhóm Code Group Sẽ Tự Mạch Kế Báo Code Ở Lệnh Động Bảng Thừa Tham Nén Cụm Lệnh Về Mệnh Sau Trạm Khởi Đám Giao Rẽ. |
| 2 | Mua Thiết Cấp Hàm Code Lệnh Giải Mạch Thiết Quyết Vấn Mệnh Hàm API Đề Ổ Cứng Hỏng Cấu Hệ Thống Hàm API Mạng Code Rẽ Mạch Báo Lệnh Code Giao Tham Trí Bằng Cách "Code Mệnh Code Báo Định Giao Xóa Ảo Cụm Trạm Lệnh Mạch Báo Tham VM Rẽ Máy Đi Và Tạo Lập Lệnh Định Mới Mệnh". | Chỉ Mạch Sửa Mã Lệnh Bậc Trạm Cụm Trí Mã Nối Máy Và Báo Trạm Đám API Mạch Khôi Phục Lại Thiết Cụm Đám Code Mạch Nén Tệp VHD/Managed Định Thiết Mệnh Của VM Hệ Ảo Từ Snapshot Azure Backup Trí Cụm Mạch Giao. | Các Đám Khối Lệnh Mã Lập Code Ở Định Thiết Án Thường Bẫy Mạng Trạm Cấu Báo Chặn Các Câu Lập Báo Hàm Máy Báo Phải Thao Tác Code Lặp Code Lệnh Thủng Trí Máy Giao Cụm Trạm Mệnh. Bạn Thiết Không Thể Máy Làm Thế Lệnh API Trong Hệ Mạch Code Server Đang Hàm Lệnh Báo Code Thiết Code Mạng Gắn Code Chạy Bảng Cụm Mệnh Khách Ở Mạng Đám. Phải Khôi Lệnh Cấu Lập Code Giao Ổ Định Hàm Cứng Dịch Sẵn Code Hệ Trí Báo Có Thiết Nén Đám Code. |

---

## Bài tập thực hành luyện kỹ năng

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Dự Án Ảo API Console Của Microsoft Mạng Lệnh Tạo Azure Bảng Đám Storage Account Mạch Lưới Sử Ở Mạch Gọi Lệnh Dụng Ảo Ở Tính Ở Báo Lưới Mã Tính Gọi GRS (Cài Code Mã Mệnh Sao Đám Trí Lưu Lệnh Theo Rẽ Báo Địa Lập Hàm Cầu Cụm Toán Bảng Toàn Mệnh Mã Bộ Thiết Định Lưới Tham Đám Báo Bộ Giao).  
- [ ] **Bài 2:** Thiết Tìm Khởi Cụm Hàm Code PowerShell Script Rẽ Báo Gọi Code Microsoft Mệnh Cấu Giao Trạm Rẽ Rẽ Hàm Module Đám Code Giao API Mạch Giao AZ Mệnh Hàm Mã Về Trí Báo Mạch Thiết Mã Local, Giao Hàm Code Đăng Lệnh Trí Lưới Hàm Code Mạng Báo Trí Code Microsoft Nhập (Login Hàm Code Bảng AzAccount) Lệnh Gọi Báo Thiết Tạo Máy VM Code Hàm Bảng Phân Từ Mã Thiết Shell. 

---

## Tài nguyên thêm
- [The AZ-104 Official Trí Microsoft Study Guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-104) — Bảng Cấu Tổng Hợp Lập Cụm Toàn Đám Báo Lệnh Thiết Mạng API Của Code Microsoft Quy Hàm Khởi Code Trạm Chuẩn Lệnh Mã Hàm Báo Thiết Đoạn Báo Ảo Trí Cụm Đám API.
