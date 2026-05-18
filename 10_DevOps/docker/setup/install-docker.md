# Docker — Cài đặt + chạy container đầu tiên

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026\
> **OS hỗ trợ:** macOS / Linux / Windows\
> **Thời lượng cài:** ~15-30 phút (tải image hơi nặng)\
> **Khó:** ⭐⭐ Medium (cần hiểu engine vs Desktop)

> 🎯 *Cài Docker trên máy local + chạy container đầu tiên (`hello-world`, `nginx`). Đây là nền tảng cho mọi thứ DevOps modern.*

---

## 1️⃣ Docker là gì + Khi nào cài

**Docker** là platform để **đóng gói app + dependencies** thành 1 unit (container) chạy trên bất kỳ máy nào có Docker.

**Khi nào nên cài**:
- ✅ Stage 3+ zero-to-coder (cần containerize app)
- ✅ Backend developer / DevOps / data engineer
- ✅ Học K8s — Docker là prerequisite

**Khi nào KHÔNG cần**:
- ❌ Frontend pure (HTML/CSS/JS browser only) — chưa cần Docker
- ❌ Học Python/Python basic — đợi Stage 4 mới cần

> 💡 *Lý thuyết Docker, xem [What is Docker](../lessons/01_basic/00_what-is-docker.md) — bài này tập trung CÀI.*

---

## 2️⃣ Yêu cầu hệ thống

| Yêu cầu | Min | Recommend |
|---|---|---|
| **OS** | macOS 11+ / Win 10 Pro/Edu / Ubuntu 20.04+ | macOS 13+ / Win 11 / Ubuntu 22+ |
| **RAM** | 4 GB | 8 GB+ (Docker chiếm 2-4 GB) |
| **CPU** | 64-bit | Apple Silicon / AMD64 |
| **Disk** | 10 GB free | 50 GB+ (image + container) |
| **Virtualization** | Bật trong BIOS (Win/Linux) | macOS auto |
| **Win Home edition** | ⚠️ Cần Win 10 Pro/Edu (hoặc Win 11 + WSL2) | — |

---

## 3️⃣ Cách cài Docker

### So sánh nhanh — Docker Desktop vs Docker Engine

| | **Docker Desktop** | **Docker Engine (Linux only)** |
|---|---|---|
| GUI | ✅ Có (quản lý container, image, volume...) | ❌ Chỉ CLI |
| Cài qua | Installer `.dmg`/`.exe`/`.deb` | apt/yum |
| Tài nguyên | Nặng (chạy VM) | Nhẹ (native Linux) |
| Free | ✅ Cá nhân + small biz (<250 emp + <$10M) | ✅ Hoàn toàn free |
| Phù hợp | Beginner, dev local | Server, CI/CD, power user |

→ **Beginner**: Docker Desktop. **Linux server**: Docker Engine.

### 🅰️ macOS — Docker Desktop

1. Tải [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) — chọn đúng chip:
   - **Apple Silicon** (M1/M2/M3/M4) — Apple chip
   - **Intel** — Mac đời 2020 trở về trước
2. Mở `.dmg` → kéo Docker.app vào Applications
3. Mở Docker.app → đợi 1-2 phút để Docker engine khởi động
4. Hiện icon Docker (🐳) ở menu bar = OK

Verify:

```bash
docker --version
# Docker version 25.0.0
docker info
```

### 🅱️ macOS — Homebrew (CLI only)

Nếu KHÔNG muốn GUI (chỉ dùng CLI):

```bash
brew install --cask docker      # full Docker Desktop
# hoặc CLI only
brew install docker docker-compose
```

> ⚠️ CLI-only trên Mac/Win cần 1 VM Linux phụ — không tiện. Dùng Docker Desktop trên Mac/Win.

### 🅲 Linux — Docker Engine (RECOMMEND)

**Ubuntu / Debian:**

```bash
# 1. Cài prerequisites
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# 2. Thêm Docker GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 3. Thêm repo
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Cài
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. Cho user hiện tại chạy docker không cần sudo
sudo usermod -aG docker $USER
newgrp docker    # apply ngay không cần logout
```

**Fedora:**

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

### 🅳 Windows — Docker Desktop

**Yêu cầu**: Windows 10 Pro/Edu/Enterprise (hoặc Windows 11) + **WSL2** bật.

1. Cài WSL2 (nếu chưa):
   ```powershell
   wsl --install
   ```
2. Tải [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
3. Chạy installer — tích "Use WSL 2 instead of Hyper-V"
4. Restart máy
5. Mở Docker Desktop từ Start Menu

Verify trong PowerShell:

```powershell
docker --version
docker info
```

### 🅴 Cloud / Server — Linux script tự động

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

→ Script chính thức cho hầu hết Linux distro. Tiện cho VPS/server.

---

## 4️⃣ Verify cài đúng

### Bước 1: Check version

```bash
docker --version
docker compose version
```

```
Docker version 25.0.0, build abc1234
Docker Compose version v2.24.0
```

### Bước 2: Chạy `hello-world` container

```bash
docker run hello-world
```

Output mong đợi:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

✅ Thấy "Hello from Docker!" = Docker đã chạy đúng!

### Bước 3: Chạy nginx web server

```bash
docker run -d -p 8080:80 --name my-nginx nginx
```

Mở browser → `http://localhost:8080` → thấy trang "Welcome to nginx!" = OK.

Dọn:

```bash
docker stop my-nginx
docker rm my-nginx
```

---

## 5️⃣ Cấu hình ban đầu

### Tăng RAM/CPU cho Docker Desktop

Default: 4 GB RAM + 2 CPU. Khi build image lớn (Node, Python, Java) → cần tăng:

- **macOS/Win**: Docker Desktop → ⚙️ Settings → Resources → Advanced
- Recommend: 8 GB RAM, 4 CPU (nếu máy có 16 GB+)

### Disk image location

Mặc định lưu trong:
- macOS: `~/Library/Containers/com.docker.docker/Data/`
- Win: `C:\Users\<user>\AppData\Local\Docker`
- Linux: `/var/lib/docker/`

Image + container nặng dần → có thể >50 GB sau vài tháng. Dọn định kỳ:

```bash
docker system prune -a              # xóa image + container không dùng
docker volume prune                 # xóa volume mồ côi
docker system df                    # xem disk usage
```

### Tạo Docker Hub account (optional)

[hub.docker.com](https://hub.docker.com) — public registry mặc định. Cần account để:
- Push image của mình
- Pull private image
- Tránh rate limit (anonymous pull có limit)

Login:

```bash
docker login
```

---

## 6️⃣ Extensions / tools phổ biến

### VS Code extensions

| Extension | Vai trò |
|---|---|
| **Docker** (`ms-azuretools.vscode-docker`) | Microsoft chính thức — manage container/image trong VS Code |
| **Dev Containers** (`ms-vscode-remote.remote-containers`) | Develop INSIDE container |
| **Docker Compose** (built-in trong Docker extension) | Compose support |

### GUI tools (nếu cần)

| Tool | Vai trò |
|---|---|
| **Docker Desktop** (built-in) | Manage containers/images visual |
| **Portainer** | Web UI quản lý Docker (deploy 1 container) |
| **Lazydocker** | Terminal UI |

### CLI tools nâng cao

```bash
brew install dive           # phân tích image layer
brew install hadolint       # linter cho Dockerfile
brew install ctop           # top cho container
```

---

## 7️⃣ Lỗi thường gặp

### ❌ Lỗi 1: `Cannot connect to the Docker daemon`

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

- **macOS/Win**: Docker Desktop chưa khởi động → mở Docker.app
- **Linux**: daemon chưa start → `sudo systemctl start docker`

### ❌ Lỗi 2: `permission denied` (Linux)

```
permission denied while trying to connect to the Docker daemon socket
```

- **Nguyên nhân**: user chưa trong group `docker`
- **Fix**: `sudo usermod -aG docker $USER` → **logout/login** (hoặc `newgrp docker`)

### ❌ Lỗi 3: Port already in use

```
Error response from daemon: driver failed programming external connectivity:
Bind for 0.0.0.0:8080 failed: port is already allocated
```

- **Nguyên nhân**: port 8080 đã có container/app khác dùng
- **Fix**:
  ```bash
  docker ps                          # xem container đang chạy
  docker stop <container-id>          # dừng cái đang giữ port
  # Hoặc dùng port khác
  docker run -d -p 9090:80 nginx
  ```

### ❌ Lỗi 4: Image quá nặng, disk full

```
no space left on device
```

- **Fix**:
  ```bash
  docker system prune -a    # xóa unused image + container + network
  docker volume prune       # xóa volume mồ côi
  ```

### ❌ Lỗi 5: WSL2 không bật (Windows)

```
Docker Desktop requires WSL 2 to be enabled
```

- **Fix**: Mở PowerShell admin:
  ```powershell
  wsl --install
  wsl --set-default-version 2
  ```
- Restart máy → mở lại Docker Desktop

### ❌ Lỗi 6: Apple Silicon vs Intel image conflict

Image build cho Intel (x86_64) không chạy native trên M1/M2 → chậm + đôi khi lỗi.

- **Fix**:
  ```bash
  docker run --platform linux/amd64 some-image     # force x86 (chậm hơn)
  ```
- Tốt hơn: tìm image có ARM64 build (đa số image official đã có multi-arch)

---

## 8️⃣ Update + Uninstall

### Update

| OS | Cách |
|---|---|
| macOS/Win Docker Desktop | Click "Update" trong app, hoặc tải installer mới |
| Linux apt | `sudo apt update && sudo apt upgrade docker-ce` |
| Linux dnf | `sudo dnf upgrade docker-ce` |

### Uninstall

| OS | Cách |
|---|---|
| macOS | Xóa Docker.app khỏi Applications + `rm -rf ~/Library/Containers/com.docker.docker` |
| Win | Settings → Apps → Uninstall "Docker Desktop" |
| Linux | `sudo apt remove docker-ce docker-ce-cli containerd.io` + `sudo rm -rf /var/lib/docker /var/lib/containerd` |

---

## 9️⃣ Alternative

| Tool | Khi nào dùng |
|---|---|
| **Docker** (đang nói) | Mặc định, ecosystem lớn nhất |
| **Podman** | Rootless containers (security), Red Hat ecosystem |
| **Colima** (macOS) | Open source thay Docker Desktop |
| **Rancher Desktop** | Open source, có K8s sẵn |
| **OrbStack** (macOS) | Cực nhanh, modern thay Docker Desktop trên Mac |
| **Lima** (macOS) | VM lightweight cho container |

> 💡 **2026 trend**: **OrbStack** đang phổ biến trên Mac (nhanh hơn Docker Desktop nhiều). Đáng thử nếu Mac chậm.

---

## 🔗 Liên kết

### Bài học dùng Docker

- [What is Docker](../lessons/01_basic/00_what-is-docker.md) — sau khi cài, đọc bài này
- [Images & Containers](../lessons/01_basic/01_images-and-containers.md)
- [Dockerfile basics](../lessons/01_basic/02_dockerfile-basics.md)

### Tài nguyên ngoài

- [Docker Official Docs](https://docs.docker.com/) — chính thức
- [Play with Docker](https://labs.play-with-docker.com/) — sandbox online (4h free)
- [Docker Hub](https://hub.docker.com) — image registry

---

## 📌 Changelog

- **v1.0.0 (16/05/2026)** — Bản đầu tiên — Docker Desktop + Engine 5 OS + verify (hello-world, nginx) + 6 lỗi thường gặp.
