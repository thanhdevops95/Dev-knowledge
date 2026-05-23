# Module 00: Introduction Labs

---

## 🎯 Mục tiêu

Trong lab này, bạn sẽ:

1. Setup môi trường làm việc hoàn chỉnh
2. Xác nhận tất cả tools hoạt động
3. Tạo tài khoản cần thiết
4. Làm quen với workflow của khóa học

---

## 🔧 Lab 1: Cài đặt môi trường theo OS

### 🪟 Windows Users

**Bước 1: Cài WSL2 (Windows Subsystem for Linux)**

Đây là cách chạy Linux bên trong Windows - cực kỳ tiện cho DevOps!

```powershell
# Mở PowerShell với quyền Administrator
# (Right-click → Run as Administrator)

# Cài WSL với Ubuntu mặc định
wsl --install
```

**Sau khi chạy xong:**

- Restart máy tính
- Mở "Ubuntu" từ Start Menu
- Đợi cài đặt lần đầu (vài phút)
- Tạo username và password khi được hỏi

**Bước 2: Xác nhận WSL hoạt động**

```bash
# Trong Ubuntu terminal
cat /etc/os-release
```

**Output mong đợi:**

```
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
...
```

**Bước 3: Cài Windows Terminal (Khuyến nghị)**

1. Mở Microsoft Store
2. Tìm "Windows Terminal"
3. Cài đặt (miễn phí)

Windows Terminal cho phép mở nhiều tabs Linux/PowerShell cùng lúc.

---

### 🍎 macOS Users

**Bước 1: Cài Homebrew**

Homebrew là package manager cho macOS - giống apt của Ubuntu.

```bash
# Mở Terminal.app và chạy:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Làm theo hướng dẫn trên màn hình.** Có thể mất 5-10 phút.

**Bước 2: Xác nhận Homebrew hoạt động**

```bash
brew --version
```

**Output mong đợi:**

```
Homebrew 4.x.x
```

---

### 🐧 Linux (Ubuntu) Users

Bạn đã có sẵn môi trường tốt nhất! Chỉ cần đảm bảo system updated:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🔧 Lab 2: Cài đặt các tools DevOps

### Cách 1: Chạy script tự động (Khuyến nghị)

**Clone repo về máy:**

```bash
# Trong terminal (WSL/macOS/Linux)
cd ~
git clone https://github.com/thanhlehoang0107/DevOps-Mastery.git
cd DevOps-Mastery
```

**Chạy script phù hợp với OS:**

```bash
# macOS
bash scripts/setup-mac.sh

# Linux/WSL
bash scripts/setup-linux.sh
```

**Đợi 5-15 phút tùy tốc độ mạng.**

---

### Cách 2: Cài thủ công từng tool

Nếu bạn muốn hiểu đang cài gì:

**Git:**

```bash
# Ubuntu/WSL
sudo apt install git -y

# macOS
brew install git

# Kiểm tra
git --version
```

**Docker:**

```bash
# Ubuntu/WSL
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER

# macOS - Tải Docker Desktop
# https://www.docker.com/products/docker-desktop

# Kiểm tra (sau khi restart terminal)
docker --version
docker run hello-world
```

**kubectl:**

```bash
# Ubuntu/WSL
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# macOS
brew install kubectl

# Kiểm tra
kubectl version --client
```

**Terraform:**

```bash
# Ubuntu/WSL
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform -y

# macOS
brew install terraform

# Kiểm tra
terraform --version
```

---

## ✅ Lab 3: Xác nhận môi trường

Chạy script kiểm tra:

```bash
cd ~/DevOps-Mastery
bash scripts/verify-tools.sh
```

**Output mong đợi (tất cả phải ✅):**

```
=== DevOps Tools Verification ===

Checking essential tools...
✅ git: git version 2.40.1
✅ docker: Docker version 24.0.7
✅ docker-compose: Docker Compose version v2.23.0
✅ kubectl: Client Version: v1.28.4
✅ terraform: Terraform v1.6.5
✅ python3: Python 3.11.6
✅ node: v20.10.0
✅ jq: jq-1.7

All essential tools are installed!

Checking optional tools...
✅ aws: aws-cli/2.13.39
✅ helm: v3.13.2
⚠️ minikube: not installed (optional - install when needed)

Environment ready for DevOps Mastery course!
```

**Nếu có tool báo ❌:** Quay lại Lab 2 và cài tool đó.

---

## 👤 Lab 4: Tạo tài khoản

### GitHub Account

**Tại sao cần:** Lưu code, CI/CD với GitHub Actions, collaboration.

1. Vào [github.com](https://github.com)
2. Click "Sign up"
3. Điền email, password, username
4. Xác nhận email

**Sau khi có account:**

```bash
# Cấu hình Git local
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Kiểm tra
git config --list
```

### Docker Hub Account

**Tại sao cần:** Lưu container images.

1. Vào [hub.docker.com](https://hub.docker.com)
2. Click "Sign up"
3. Dùng cùng email với GitHub để dễ nhớ

**Sau khi có account:**

```bash
# Login Docker CLI
docker login
# Nhập username và password
```

### (Optional) AWS Free Tier

**Tại sao cần:** Chạy production infrastructure (Module 11+).

1. Vào [aws.amazon.com/free](https://aws.amazon.com/free)
2. Click "Create a Free Account"
3. Điền thông tin (cần credit card nhưng không charge)
4. Chọn "Basic Support - Free"

**Lưu ý:** Bạn chưa cần AWS ngay. Có thể tạo sau khi đến Module 11.

---

## 🚀 Lab 5: Chạy thử Counter App

### Mục tiêu

Đảm bảo Docker hoạt động bằng cách chạy app mẫu.

### Bước 1: Vào thư mục source code

```bash
cd ~/DevOps-Mastery/source-code
ls
```

**Output:**

```
Dockerfile  README.md  app.py  docker-compose.yml  requirements.txt
```

### Bước 2: Chạy app với Docker Compose

```bash
docker-compose up -d
```

**Output:**

```
Creating network "source-code_default" with the default driver
Creating source-code_redis_1 ... done
Creating source-code_web_1   ... done
```

### Bước 3: Truy cập app

Mở browser, vào: [http://localhost:5000](http://localhost:5000)

**Bạn sẽ thấy Counter App!**

- Bấm nút +1 để tăng số
- Số được lưu vào Redis database
- Refresh trang - số vẫn còn

### Bước 4: Xem logs

```bash
docker-compose logs -f web
```

**Output:**

```
web_1    | * Running on http://0.0.0.0:5000
web_1    | 192.168.1.1 - - [15/Jan/2024 10:00:00] "GET / HTTP/1.1" 200 -
```

Nhấn `Ctrl+C` để thoát.

### Bước 5: Dọn dẹp

```bash
docker-compose down
```

**Output:**

```
Stopping source-code_web_1   ... done
Stopping source-code_redis_1 ... done
Removing source-code_web_1   ... done
Removing source-code_redis_1 ... done
```

---

## 📝 Lab 6: Làm quen với cấu trúc khóa học

### Xem cấu trúc thư mục

```bash
cd ~/DevOps-Mastery
ls -la
```

**Giải thích:**

```
DevOps-Mastery/
├── README.md              ← Hướng dẫn tổng quan
├── 00_INTRODUCTION/       ← Module đang học
├── 01_LINUX/              ← Module tiếp theo
├── 02_NETWORKING/         
├── ...                    
├── 15_SRE/               
├── CAPSTONE_PROJECT/      ← Dự án cuối khóa
├── RESOURCES/             ← Tài liệu bổ sung
├── scripts/               ← Scripts setup
└── source-code/           ← Counter App
```

### Xem nội dung một module

```bash
ls 01_LINUX/
```

**Output:**

```
README.md     ← Lý thuyết
LABS.md       ← Thực hành
SCENARIOS.md  ← Tình huống thực tế
```

**Quy trình học mỗi module:**

1. Đọc README.md - Hiểu khái niệm
2. Làm LABS.md - Thực hành từng bước
3. Giải SCENARIOS.md - Xử lý tình huống production

---

## ✅ Checklist hoàn thành Module 00

Đánh dấu những gì đã làm:

- [ ] Cài WSL2 (Windows) hoặc Homebrew (macOS)
- [ ] Cài đặt Git, Docker, kubectl, Terraform
- [ ] Chạy verify-tools.sh thành công
- [ ] Tạo GitHub account
- [ ] Tạo Docker Hub account
- [ ] Chạy thử Counter App với Docker Compose
- [ ] Hiểu cấu trúc thư mục khóa học

---

## ⏭️ Bạn đã sẵn sàng

Môi trường đã setup xong. Bắt đầu học thực sự!

👉 **[SCENARIOS.md - Khám phá thêm](SCENARIOS.md)**

Hoặc nhảy thẳng vào module đầu tiên:

👉 **[Module 01: Linux Fundamentals](../01_LINUX/README.md)**
