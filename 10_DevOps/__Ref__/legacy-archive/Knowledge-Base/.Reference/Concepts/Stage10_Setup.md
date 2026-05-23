# 🛠️ GIAI ĐOẠN 10: CHUẨN BỊ AWS & EKS

## ⚠️ CẢNH BÁO CHI PHÍ (COST WARNING)
Giai đoạn này sử dụng tài nguyên thật trên AWS. Kể cả với Free Tier, EKS (Elastic Kubernetes Service) **KHÔNG MIỄN PHÍ**. Nó tốn khoảng **$0.10/giờ** cho Control Plane + phí EC2 Worker Nodes.
- Hãy chắc chắn bạn có thẻ VISA/MasterCard.
- **QUAN TRỌNG:** Làm xong phải xóa ngay (Phần Clean Up ở cuối bài) để tránh mất tiền oan (vài chục $ nếu quên).

---

## 1. TẠO TÀI KHOẢN AWS & USER IAM
1. Đăng ký tại: [aws.amazon.com](https://aws.amazon.com/)
2. Tạo IAM User với quyền `AdministratorAccess` (Dùng cho thực hành).
   - Lấy `Access Key ID` và `Secret Access Key`.

## 2. CÀI ĐẶT AWS CLI
Để gõ lệnh điều khiển AWS từ máy tính.
- **macOS**: `brew install awscli`
- **Windows**: [Tải installer AWS CLI v2](https://aws.amazon.com/cli/).
- **Cấu hình:**
  ```bash
  aws configure
  # Nhập ID, Key, Region (chọn us-east-1 hoặc ap-southeast-1), Output format (json)
  ```

## 3. CÀI ĐẶT EKSCTL
Tool chuyên dụng để tạo EKS Cluster nhanh chóng.
- **macOS**:
  ```bash
  brew tap weaveworks/tap
  brew install weaveworks/tap/eksctl
  ```
- **Windows**: `choco install eksctl`

## 4. CÀI ĐẶT K6 (LOAD TEST TOOL)
Để test tính năng Autoscaling, ta cần "bắn" ngàn request vào server.
- **macOS**: `brew install k6`
- **Windows**: `choco install k6`

---

## ✅ CHECKLIST
- Đã có tài khoản AWS.
- `aws sts get-caller-identity` -> Ra thông tin user.
- `eksctl version` -> Ra version.

Sẵn sàng "đốt tiền" (một chút) để học công nghệ xịn nhất!
