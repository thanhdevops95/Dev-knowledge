# 🛠️ GIAI ĐOẠN 8: CHUẨN BỊ VPS DEPLOYMENT

## 📌 MỤC TIÊU
Để thực hành CD (Deployment), bạn cần một "Server" đích.

### Phương án 1: VPS Thực (Khuyên dùng)
Nếu bạn có VPS (DigitalOcean, AWS EC2, Google Cloud, hoặc Cloud cá nhân):
1. SSH vào VPS.
2. Cài Docker & Docker Compose trên VPS (giống Giai đoạn 2 & 4).
3. Tạo thư mục `/root/todo-app`.

### Phương án 2: Giả lập Local (Nếu không có VPS)
Bạn có thể coi chính máy tính của mình (hoặc máy ảo VM Ubuntu) là Server.
Để GitLab (trên mây) kết nối được về máy bạn, bạn cần dùng **Ngrok** hoặc **Cloudflare Tunnel** để mở port SSH. Tuy nhiên cách này khá phức tạp và rủi ro bảo mật.

👉 **Khuyến nghị cho bài học này:** Nếu không có VPS, bạn hãy **đọc hiểu cơ chế** thay vì cố gắng setup SSH tunnel về máy cá nhân (vì IP động và NAT).
*Dưới đây mình sẽ hướng dẫn theo kịch bản có VPS Ubuntu.*

---

## 1. TẠO SSH KEY PAIR
GitLab cần "chìa khóa" để SSH vào VPS của bạn mà không cần nhập mật khẩu.

Trên máy cá nhân (hoặc Cloud Shell):
```bash
# Tạo cặp khóa (không đặt passphrase)
ssh-keygen -t rsa -b 4096 -f gitlab_deploy_key
```
Bạn sẽ có 2 file:
- `gitlab_deploy_key` (Private Key - Đưa cho GitLab)
- `gitlab_deploy_key.pub` (Public Key - Đưa vào VPS)

## 2. CẤU HÌNH TRÊN VPS
Copy nội dung file `.pub` và chạy lệnh sau trên VPS:
```bash
# Thêm vào authorized_keys
echo "nội_dung_file_pub" >> ~/.ssh/authorized_keys
```

## 3. CẤU HÌNH TRÊN GITLAB
Vào Settings -> CI/CD -> Variables. Thêm các biến:
1. `SSH_PRIVATE_KEY`: Copy toàn bộ nội dung file `gitlab_deploy_key` (cả dòng BEGIN/END).
2. `SSH_HOST`: IP của VPS.
3. `SSH_USER`: User đăng nhập (thường là root hoặc ubuntu).

---

## ✅ CHECKLIST
- VPS đã cài Docker, Docker Compose.
- GitLab đã có Private Key.
- VPS đã có Public Key.

Sẵn sàng để Deploy tự động!
