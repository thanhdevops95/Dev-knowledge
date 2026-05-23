# 🛠️ GIAI ĐOẠN 2: CHUẨN BỊ MÔI TRƯỜNG DOCKER

## 📌 MỤC TIÊU
Để thực hiện Giai đoạn 2 (Docker Hóa), bạn bắt buộc phải cài đặt Docker Engine và Docker CLI. Đây là công cụ quan trọng nhất trong lộ trình này.

---

## 1. CÀI ĐẶT DOCKER

Tùy vào hệ điều hành của bạn, hãy chọn cách cài đặt phù hợp.

### 🍎 macOS
Khuyến nghị dùng **Docker Desktop for Mac**.
1. Truy cập: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Chọn "Download for Mac" (chú ý chọn đúng chip Intel hay Apple Silicon/M1/M2/M3).
3. Kéo thả vào Applications như bình thường.
4. Mở ứng dụng Docker lên và đợi icon cá voi trên thanh menu đứng yên (Running).
5. **OrbStack (Lựa chọn thay thế nhẹ hơn):** Nếu máy yếu, bạn có thể dùng [OrbStack](https://orbstack.dev/) thay cho Docker Desktop. Nó nhanh và nhẹ hơn rất nhiều.

### 🪟 Windows
Sử dụng **Docker Desktop for Windows** (Yêu cầu WSL2).
1. Bật WSL2 (Windows 10/11):
   - Mở PowerShell (Admin): `wsl --install`
   - Restart máy.
2. Tải & Cài Docker Desktop từ trang chủ.
3. Trong Setting của Docker Desktop, đảm bảo tích chọn **"Use the WSL 2 based engine"**.

### 🐧 Linux (Ubuntu)
```bash
# Gỡ version cũ
sudo apt-get remove docker docker.io containerd runc

# Cài đặt dependency
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# Add Docker GPG Key
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Setup Repo
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Cấp quyền user (để chạy docker không cần sudo)
sudo usermod -aG docker $USER
# Log out rồi Log in lại để áp dụng
```

---

## 2. CÀI ĐẶT VS CODE EXTENSION (NẾU CHƯA CÓ)
Để viết Dockerfile dễ dàng hơn:
1. Mở VS Code Extension.
2. Tìm **"Docker"** (publisher: Microsoft).
3. Install.

---

## ✅ CHECKLIST KIỂM TRA
Mở Terminal và chạy:

```bash
docker --version
# Output mong đợi: Docker version 24.x.x (hoặc mới hơn)

docker run hello-world
# Output mong đợi: "Hello from Docker! This message shows that your installation appears to be working correctly."
```

Nếu chạy được `hello-world`, chúc mừng bạn đã sở hữu sức mạnh của Containerization!
Sẵn sàng vào **Giai đoạn 2**.
