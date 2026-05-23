# 🔥 Terraform Cheatsheet — Từ Điển Lệnh Tìm Kiếm Nhanh

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Toàn bộ các nhóm lệnh cấu trúc vòng lặp thao tác Terraform cốt lõi rút gọn nhất cho người dùng hàng ngày.
> **Prerequisite:** `09-DevOps/iac/01-terraform-basics.md`

---

## 1. Mệnh lệnh Bắt Đầu và Dọn Dẹp Cơ Bản (Core Workflow)

Là quy trình 3 bước sử dụng mọi lúc khi phát hành hệ thống.

```bash
# KHỞI TẠO MÔI TRƯỜNG DỰ ÁN
# Lệnh tải các Plugins/Thư viện liên kết với đơn vị cung cấp (AWS/Azure) về máy
terraform init

# HOẠCH ĐỊNH KIỂM TRA MÃ DỰ KIẾN (DRY-RUN)
# Xem Terraform sẽ làm gì. Liệt kê các lỗi tạo sửa mạng trước khi thực thi
terraform plan
# Xuất cấu trúc bản đồ dự định tải chạy ra một file kế hoạch cố định (Out File) 
terraform plan -out=tfplan

# ÁP DỤNG MÃ VÀO THỰC TẾ HỆ THỐNG
terraform apply
# Chạy bộ kế hoạch định sẵn ở file tải trên (Khuyến cáo dùng khi cấu tạo)
terraform apply tfplan
# Nếu bạn đã kiểm tra và muốn ứng dụng bỏ yêu cầu nhập "yes"
terraform apply -auto-approve

# XÓA TOÀN BỘ CỤM HỆ THỐNG TRÊN ĐÁM MÂY
# Gỡ và Phá hủy hoàn toàn những tài nguyên hệ điều hành từ trước đến giờ
terraform destroy
terraform destroy -auto-approve
```

---

## 2. Các Thao Tác Trạng Thái Dữ Liệu TFState (State Management)

Toàn bộ thông tin máy được lưu giữ mã tại hệ thống tệp `.tfstate`. Bất kì cấu tác can thiệp đều phải báo lên hệ thống. Đừng sửa bằng tay!

```bash
# LIỆT KÊ DANH SÁCH MÁY MẠNG ẢO
# Danh sách thiết bị bạn đã cài cấu tải trên tệp mạng
terraform state list

# XEM ĐỊNH CẤU CẤP CHI TIẾT 1 THIẾT BỊ 
# Hiện bảng kết thiết lập cấu biến của cái máy (Ví dụ có thẻ `aws_instance.web`)
terraform state show aws_instance.web

# ĐỔI TÊN MỘT THIẾT BỊ HOẶC DI CHUYỂN
# Nếu main.tf bạn đổi tên máy resource từ "web" sang "web_moi", gọi tệp này đổi theo state
terraform state mv aws_instance.web aws_instance.web_moi

# GỠ THÔNG TIN MÁY KHỎI DO TẠO TERRAFORM QUẢN LÍ
# Loại bỏ dòng cấu danh máy trạm ở tệp State. Thực tế máy AWS ảo vẫn sống! Nhưng Terraform quên nó đi.
terraform state rm aws_instance.web

# NẠP MÁY LÀM THỦ CÔNG NGOÀI WEB DO TERRAFORM KÉO VÀO STATE (HAY HỎI THI)
# (Id máy aws ở đây ví dụ là i-12345)
terraform import aws_instance.web_nguoi_dung_tao i-12345
```

---

## 3. Cấu Gọn Dữ Liệu Mã Nguồn Nhánh Trạm

Các cấu thiết lập dọn rác tập tệp lỗi hoặc định chữ cho mảng báo.

```bash
# THIẾT GỌN TỆP VÀ FORMAT CHỮ THEO TRUẨN 
# Định thiết lại dấu cách, cấu tab tệp HCL cho sạch cấu dễ đọc
terraform fmt

# QUÉT KIỂM ĐỊNH THIẾT LỖI CÚ PHÁP
terraform validate

# LẤY MẢNG CẢNH BÁO MỞ RA CONSOLE
# Chỉ trích cấu các điểm gán (Outputs.tf) ra màn hình kết tệp
terraform output
```

---

## 4. Quản Lý Khu Vực Nén Không Gian Môi Trường (Workspaces)

Workspaces là các nhóm biến lưu cài tệp trạng thái khác nhau. Phù thiết cho lập ứng đa mạng chạy tạo ứng `dev`, `staging`, `prod` từ cùng 1 bộ mã. 

```bash
# Bảng danh thiết các tên môi trường biến đang chứa có tệp lệnh
terraform workspace list

# Tạo mới tài khoản và chuyển thư máy lập ngay đến lưới môi trường mới
terraform workspace new production

# Đổi thay bộ chạy máy rẽ nhánh mạng nhảy sang môi trường Dev Cấp
terraform workspace select dev

# Bỏ gỡ xóa xóa một môi trường khối khỏi kho lưu TF State  
terraform workspace delete testing
```
