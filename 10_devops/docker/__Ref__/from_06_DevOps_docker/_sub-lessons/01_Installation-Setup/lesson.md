# 🐳 Docker — Installation & Setup

---

## 📋 Metadata

- **Parent Lesson:** [Docker — Containerization Platform](../README.md)
- **Level:** `[BEGINNER]`
- **Prerequisites:** None
- **Estimated Time:** 45 phút
- **Last Updated:** 30/04/2026
- **Author:** Mr.Rom

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ có thể:

- [ ] Cài đặt Docker Desktop trên macOS/Windows hoặc Docker Engine trên Linux
- [ ] Verify Docker installation với `docker --version` và `docker run hello-world`
- [ ] Hiểu Docker architecture cơ bản (Client-Server model)
- [ ] Sử dụng Docker Desktop UI cơ bản
- [ ] Configure Docker resources (CPU, Memory)

---

## 📚 Nội Dung

### 1. Docker Desktop vs Docker Engine

**Docker Desktop** (cho macOS/Windows):
- All-in-one package: GUI + CLI + Kubernetes (optional)
- Dễ cài đặt, user-friendly
- Chạy Docker trong lightweight VM (HyperKit trên Mac, WSL2 trên Windows)

**Docker Engine** (cho Linux):
- Chỉ CLI + daemon
- Chạy trực tiếp trên kernel (không cần VM)
- lighter weight

**Recommendation:** 
- macOS/Windows → Docker Desktop
- Linux → Docker Engine hoặc Docker Desktop (tùy preference)

---

### 2. Cài Đặt Docker Desktop (macOS)

**Bước 1:** Tải Docker Desktop

- Truy cập [Docker Official Website](https://www.docker.com/products/docker-desktop/)
- Tải Docker Desktop for Mac (Apple Chip hoặc Intel)

**Bước 2:** Install

- Double-click `.dmg` file
- Kéo Docker icon vào Applications folder
- Mở Docker từ Applications

**Bước 3:** First Run

- Khi mở lần đầu, Docker sẽ yêu cầu permissions:
  - ✅ Allow Docker to access filesystem
  - ✅ Allow networking
- Docker icon sẽ xuất hiện trên menu bar (top right)
- Đợi Docker finish starting (whale icon stable)

**Bước 4:** Verify Installation

```bash
# Check Docker version
docker --version
# Expected output: Docker version 24.x.x, build xxxxx

# Check Docker is running
docker info

# Test with hello-world
docker run hello-world
```

Nếu bạn thấy:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

→ 🎉 **Chúc mừng! Docker đã cài đặt thành công.**

---

### 3. Cài Đặt Docker Desktop (Windows)

**Yêu cầu hệ thống:**
- Windows 10 64-bit: Pro, Enterprise, hoặc Education (Build 19044+)
- WSL2 feature enabled (Docker sẽ tự enable)
- 4GB RAM minimum (8GB recommended)

**Bước 1:** Tải Docker Desktop for Windows từ [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-windows)

**Bước 2:** Run installer

- Double-click `.exe` file
- Follow wizard
- Khi prompted, enable WSL2 (recommended)

**Bước 3:** Restart máy tính

**Bước 4:** Mở Docker Desktop từ Start Menu

- Docker icon sẽ xuất hiện trên system tray
- Đợi Docker khởi động

**Bước 5:** Verify

```powershell
# Open PowerShell hoặc Command Prompt
docker --version
docker run hello-world
```

---

### 4. Cài Đặt Docker Engine (Linux — Ubuntu/Debian)

**Bước 1:** Uninstall old versions (nếu có)

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

**Bước 2:** Set up repository

```bash
# Update apt package index
sudo apt-get update

# Install dependencies
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Bước 3:** Install Docker Engine

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

**Bước 4:** Verify & Post-install

```bash
# Run hello-world
sudo docker run hello-world

# (Optional) Run Docker as non-root user
sudo usermod -aG docker $USER
# Log out and log back in để áp dụng
```

---

### 5. Docker Architecture Overview

**Client-Server Model:**

```
┌─────────────┐
│   You       │ ← Gõ command: docker run nginx
│ (docker CLI)│
└──────┬──────┘
       │ HTTP request
       ▼
┌─────────────────┐
│  Docker Daemon  │ ← Xử lý request, pull image, tạo container
│   (dockerd)     │
└────────┬────────┘
         │
    ┌────┴─────┐
    ▼          ▼
 ┌──────┐  ┌──────┐
 │Image │  │Container│
 │Layer │  │Layer   │
 └──────┘  └──────┘
```

**Key components:**

- **Docker Client** (`docker` command): CLI tool bạn tương tác
- **Docker Daemon** (`dockerd`): Background service quản lý Docker objects
- **Docker Registry:** Nơi lưu images (Docker Hub, private registry)
- **Images:** Read-only templates
- **Containers:** Running instances

---

### 6. Docker Desktop UI Basics (Optional)

Nếu dùng Docker Desktop (Mac/Windows):

**Menu bar icon:** Click vào whale icon trên menu bar/system tray

**Dashboard:**
- **Containers / Apps:** List containers đang chạy, start/stop buttons
- **Images:** List downloaded images
- **Settings:** Configure resources, features, general settings
- **Troubleshoot:** Diagnose issues, reset Docker

**Settings → Resources:**
- CPUs: Number of CPUs allocated to Docker (default: 2)
- Memory: RAM allocated (default: 2GB) — **Tăng lên nếu cần**
- Disk image size: Default 64GB — **Tùy nhu cầu**
- Swap: Optional

---

### 7. Common Issues & Troubleshooting

#### Issue 1: "Cannot connect to the Docker daemon"

**Lỗi:** `Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`

**Nguyên nhân:** Docker chưa start hoặc bạn không có permission

**Giải pháp:**
- Mac/Windows: Mở Docker Desktop app
- Linux: `sudo service docker start` hoặc `sudo systemctl start docker`

#### Issue 2: "Permission denied" (Linux)

**Lỗi:** `Got permission denied while trying to connect to the Docker daemon socket`

**Giải pháp:**
```bash
# Thêm user vào docker group (đã đề cập ở trên)
sudo usermod -aG docker $USER
# Log out và log back in
```

Hoặc chạy command với `sudo` (temporary)

#### Issue 3: Docker Desktop won't start (Mac/Windows)

**Nguyên nhân:** WSL2 corrupted, virtualization disabled

**Giải pháp:**
- Windows: Enable virtualization in BIOS, enable WSL2 feature
- Mac: Ensure HyperKit installed correctly
- Reset Docker Desktop: Settings → Troubleshoot → Reset to factory defaults

---

## 💻 Hands-On Exercises

### Exercise 1: Verify Installation

**Mục tiêu:** Confirm Docker đã cài đặt và chạy đúng

**Tasks:**
1. Mở terminal (macOS/Linux) hoặc PowerShell (Windows)
2. Chạy `docker --version`. Ghi ra version number.
3. Chạy `docker info`. Scroll và tìm:
   - `Operating System:`
   - `Kernel Version:`
   - `Number of CPUs:`
4. Chạy `docker run hello-world`

**Expected Output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

**Success Criteria:**
- ✅ `docker --version` chạy không lỗi
- ✅ `docker run hello-world` in ra message "Hello from Docker!"

---

### Exercise 2: Explore Docker Desktop UI

**Mục tiêu:** Làm quen với Docker Desktop interface

**Tasks:**
1. Mở Docker Desktop app
2. Click vào **Settings** (gear icon)
3. Đi đến **Resources** tab
4. Ghi lại:
   - CPUs: [số]
   - Memory: [số GB]
   - Disk image size: [số GB]
5. Click **Apply & Restart** nếu bạn thay đổi gì

**Kỳ vọng:** Bạn biết cách cấu hình Docker resources

---

### Exercise 3: Docker Version Command Deep Dive

**Mục tiêu:** Hiểu output của `docker version`

**Tasks:**
```bash
docker version
```

**Phân tích output:**
- **Client:** Docker CLI version bạn đang dùng
- **Server:** Docker Engine version (daemon)
- **API version:** Version của Docker Remote API

**Câu hỏi:**
1. Client và Server version có khác nhau không? (Có thể)
2. API version dùng để làm gì? (Clients và daemon communicate qua API)

---

## ✅ Kiểm Tra & Đánh Giá

### Self-Check Questions

1. **Docker Desktop chạy trên macOS/Windows sử dụng công nghệ nào?**
   - A. Native Linux kernel
   - B. Lightweight VM (HyperKit/WSL2)
   - C. Full virtualization (VirtualBox)
   
   **Đáp án:** B

2. **Command nào để verify Docker installation?**
   - A. `docker check`
   - B. `docker run hello-world`
   - C. `docker verify`
   
   **Đáp án:** B

3. **Docker Daemon là gì?**
   - A. CLI tool bạn gõ command
   - B. Background service quản lý containers
   - C. Registry để lưu images
   
   **Đáp án:** B

---

### Checklist Tự Đánh Giá

Sau khi hoàn thành bài này, check các mục sau:

- [ ] Tôi đã cài Docker Desktop/Docker Engine thành công
- [ ] Tôi chạy được `docker --version` và thấy version output
- [ ] Tôi chạy được `docker run hello-world` và thấy message thành công
- [ ] Tôi hiểu Docker Client-Server architecture
- [ ] Tôi biết cách mở Docker Desktop UI (nếu dùng Desktop)
- [ ] Tôi biết cách xem và cấu hình Docker resources

**Nếu có >2 checkbox chưa tick:** Quay lại và lặp lại exercises.

---

## 🔗 Liên Kết

### Navigation

- ← [Quay lại bài mẹ](index.md)
- → [Bài tiếp theo: Images & Containers](../02-Images-Containers/lesson.md)

### Troubleshooting

- [Docker Docs — Install Docker](https://docs.docker.com/engine/install/)
- [Docker Troubleshooting Guide](https://docs.docker.com/config/daemon/)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
