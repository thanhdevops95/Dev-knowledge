# Hướng Dẫn 2: Triển Khai Trên Máy Chủ Remote (Ubuntu/OrbStack)

File này mô phỏng quy trình Deployment thực tế: Bạn ngồi code trên máy Mac cá nhân, nhưng ứng dụng sẽ chạy trên một máy chủ Linux (Ubuntu) từ xa (hoặc giả lập bằng OrbStack/VM).

## Mục tiêu
- Biết cách SSH vào server.
- Biết cách chuyển source code từ Mac lên server (SCP).
- Cài đặt môi trường Docker trên Ubuntu.
- Triển khai và xử lý quyền (Permissions) trên Linux.

---

## 1. Kết nối SSH

Giả sử bạn có thông tin server:
- **IP:** `192.168.1.100` (hoặc IP OrbStack/VM của bạn).
- **User:** `ubuntu`.
- **Key/Password**: (Tùy cấu hình).

Từ Terminal trên Mac:
```bash
# Cú pháp: ssh user@ip
ssh ubuntu@192.168.1.100
```
*Kết quả:* Dấu nhắc lệnh đổi từ `MacBook-Pro%` sang `ubuntu@server$`. Bạn đã ở trong máy Linux.

---

## 2. Chuẩn bị Môi trường trên Server (Ubuntu)

Trên màn hình SSH (trong máy Ubuntu), chạy các lệnh sau để cài Docker:

```bash
# 1. Cập nhật danh sách gói
sudo apt-get update

# 2. Cài đặt Docker
sudo apt-get install -y docker.io

# 3. Kiểm tra Docker (cần sudo)
sudo docker --version

# 4. (Tùy chọn) Để chạy docker không cần gõ sudo mỗi lần:
sudo usermod -aG docker $USER
# Sau lệnh này cần logout và login lại SSH để có hiệu lực.
```

---

## 3. Chuyển Source Code (Deploy)

Ở bước này, ta sẽ copy thư mục `TwoAppSystem` đã làm ở Hướng Dẫn 1 từ Mac lên Ubuntu.

**Mở một tab Terminal mới trên Mac (Local Terminal):**
Không gõ lệnh này trong SSH, mà gõ trên Mac.

```bash
# scp: Secure Copy
# -r: recursive (copy cả thư mục)
# ~/TwoAppSystem: Nguồn (trên Mac)
# ubuntu@...:/home/ubuntu/: Đích (trên Server)

scp -r ~/TwoAppSystem ubuntu@192.168.1.100:/home/ubuntu/
```

**Quay lại tab SSH trên Ubuntu:**
Kiểm tra xem file đã lên chưa:
```bash
ls -F /home/ubuntu/TwoAppSystem
# Thấy folder go-app/ và python-app/ là thành công.
```

---

## 4. Build Images trên Linux

Các lệnh tương tự như trên Mac, nhưng chú ý quyền `sudo` nếu chưa cấu hình user group.

```bash
cd ~/TwoAppSystem/go-app
# Build Go Image
sudo docker build -t my-go-backend:linux .

cd ~/TwoAppSystem/python-app
# Build Python Image
sudo docker build -t my-py-frontend:linux .
```
*Kết quả:* `sudo docker images` sẽ hiển thị 2 image mới.

---

## 5. Chạy Ứng Dụng (Production Mode)

### 5.1 Tạo Network
```bash
sudo docker network create prod-net
```

### 5.2 Xử lý Volume & Permissions (Quan trọng)
Trên Linux, vấn đề quyền truy cập file (Permissions) ngặt nghèo hơn Mac/Windows.
Khi ta map volume, thư mục trên Host phải cho phép Container user ghi vào.

```bash
# 1. Tạo thư mục chứa data trên Host Linux
mkdir -p /home/ubuntu/app-data

# 2. Cấp quyền (chmod) cho thư mục này để container có thể ghi
# 777 cho phép đọc/ghi thoải mái (Dễ nhất cho lab)
chmod 777 /home/ubuntu/app-data
```

### 5.3 Chạy Containers

**Chạy Go Backend:**
```bash
sudo docker run -d \
  --name go-prod \
  --network prod-net \
  --restart always \
  -v /home/ubuntu/app-data:/data \
  my-go-backend:linux
```
- `--restart always`: Tự động khởi động lại container nếu nó bị crash hoặc server reboot (Đặc thù Production).

**Chạy Python Frontend:**
```bash
sudo docker run -d \
  --name py-prod \
  --network prod-net \
  --restart always \
  -p 80:5001 \
  -e GO_APP_URL="http://go-prod:8080" \
  my-py-frontend:linux
```
- `-p 80:5001`: Mở cổng 80 (cổng web mặc định) của máy chủ và trỏ vào cổng 5001 của container. Người dùng chỉ cần gõ IP là vào được, không cần `:5001`.

---

## 6. Kiểm tra & Verify

Từ trình duyệt trên máy Mac của bạn (Client):
Truy cập: `http://192.168.1.100/do-ping`
(Thay IP bằng IP thật của server Ubuntu).

**Kịch bản Test mất dữ liệu:**
1. Refresh trình duyệt vài lần để tăng số count.
2. Trên SSH Ubuntu: `sudo docker rm -f go-prod`. (Xóa container)
3. Chạy lại lệnh docker run Go ở bước 5.3.
4. Refresh trình duyệt. Số đếm vẫn tiếp tục tăng từ mốc cũ -> **Thành công lưu trữ**.
5. Kiểm tra file trên server: `cat /home/ubuntu/app-data/db.json`.

---

## 7. Các lệnh Debug hữu ích trên Server

Khi chạy remote, bạn không thấy cửa sổ log trực tiếp. Hãy dùng các lệnh sau:

- **Xem logs:**
  ```bash
  sudo docker logs -f go-prod
  sudo docker logs -f py-prod
  ```
- **Kiểm tra process:**
  ```bash
  sudo docker ps -a
  ```
- **Chui vào container đang chạy:**
  ```bash
  sudo docker exec -it go-prod sh
  # Sau đó ls /data để xem file bên trong
  ```
