# 🔧 Troubleshooting

> **Common errors and solutions for environment setup**
>
> *Các giải pháp cho lỗi thường gặp khi cài đặt môi trường*

---

## 📋 Table of Contents (Mục lục)

1. [Docker Issues](#-docker-issues)
2. [WSL2 Issues (Windows)](#-wsl2-issues-windows)
3. [Git Issues](#-git-issues)
4. [Kubernetes Issues](#-kubernetes-issues)
5. [Network Issues](#-network-issues)

---

## 🐳 Docker Issues

### Docker daemon not running (Docker daemon không chạy)

**Error (Lỗi):**

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution (Giải pháp):**

```bash
# Linux
sudo systemctl start docker
sudo systemctl enable docker

# Windows - Open Docker Desktop from Start Menu
# (Mở Docker Desktop từ Start Menu)

# macOS - Open Docker Desktop from Applications
# (Mở Docker Desktop từ Applications)
```

---

### Permission denied when running docker (Permission denied khi chạy docker)

**Error (Lỗi):**

```
Got permission denied while trying to connect to the Docker daemon socket
```

**Solution - Linux (Giải pháp - Linux):**

```bash
# Add user to docker group (Thêm user vào group docker)
sudo usermod -aG docker $USER

# Logout and login again, or (Logout và login lại, hoặc):
newgrp docker
```

---

### Docker build slow or timeout (Docker build chậm hoặc timeout)

**Solution (Giải pháp):**

```bash
# Clear cache and unused images (Xóa cache và images không dùng)
docker system prune -a

# Increase resources for Docker Desktop (Tăng resources cho Docker Desktop):
# Settings → Resources → Increase Memory/CPU
```

---

### Port already in use (Port đã được sử dụng)

**Error (Lỗi):**

```
Bind for 0.0.0.0:80: failed: port is already allocated
```

**Solution (Giải pháp):**

```bash
# Find process using the port (Tìm process đang dùng port)
# Windows
netstat -ano | findstr :80

# Linux/macOS
lsof -i :80

# Kill process or use different port (Kill process hoặc dùng port khác)
docker run -p 8080:80 nginx
```

---

## 🪟 WSL2 Issues (Windows)

### WSL2 not installed (WSL2 chưa được cài đặt)

**Error (Lỗi):**

```
WSL 2 requires an update to its kernel component
```

**Solution (Giải pháp):**

```powershell
# Run PowerShell as Admin (Chạy PowerShell với quyền Admin)
wsl --install
wsl --update

# Restart computer (Restart máy tính)
```

---

### WSL2 won't start (WSL2 không start được)

**Solution (Giải pháp):**

```powershell
# Check if virtualization is enabled in BIOS
# (Kiểm tra virtualization đã bật chưa trong BIOS)

# Enable Windows features (Bật Windows features):
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Restart
```

---

### Docker integration with WSL2 not working

**Solution (Giải pháp):**

1. Open Docker Desktop (Mở Docker Desktop)
2. Settings → Resources → WSL Integration
3. Tick "Enable integration with my default WSL distro"
4. Tick your distro (Ubuntu, etc.) (Tick distro bạn đang dùng)
5. Apply & Restart

---

## 📦 Git Issues

### SSH key not recognized (Git không nhận SSH key)

**Error (Lỗi):**

```
Permission denied (publickey)
```

**Solution for GitLab (Giải pháp cho GitLab):**

```bash
# Generate new SSH key (Tạo SSH key mới)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key (Copy public key)
cat ~/.ssh/id_ed25519.pub

# Add to GitLab (Thêm vào GitLab):
# GitLab → Preferences → SSH Keys

# Test connection (Kiểm tra kết nối)
ssh -T git@gitlab.com
```

**Solution for GitHub (Giải pháp cho GitHub):**

```bash
# Same key generation steps as above
# (Các bước tạo key giống như trên)

# Add to GitHub (Thêm vào GitHub):
# GitHub → Settings → SSH and GPG Keys

# Test connection (Kiểm tra kết nối)
ssh -T git@github.com
```

---

### Git push rejected (Git push bị từ chối)

**Error (Lỗi):**

```
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do not have locally
```

**Solution (Giải pháp):**

```bash
# Pull changes first (Pull changes trước)
git pull origin main --rebase

# Then push again (Rồi push lại)
git push origin main
```

---

### Line ending issues (CRLF/LF)

**Solution (Giải pháp):**

```bash
# Windows - auto convert (tự động convert)
git config --global core.autocrlf true

# Linux/macOS
git config --global core.autocrlf input
```

---

### Protected branch error (Lỗi branch được bảo vệ)

**Error (Lỗi):**

```
remote: GitLab: You are not allowed to push code to protected branches
# or (hoặc)
remote: error: GH006: Protected branch update failed
```

**Solution (Giải pháp):**

```bash
# Create a new branch (Tạo branch mới)
git checkout -b feature/my-changes

# Push the branch (Push branch)
git push origin feature/my-changes

# Create Merge Request (GitLab) or Pull Request (GitHub)
# Then merge through the web interface
# (Tạo MR/PR rồi merge qua web interface)
```

---

## ☸️ Kubernetes Issues

### kubectl cannot connect to cluster (kubectl không connect được cluster)

**Error (Lỗi):**

```
The connection to the server localhost:8080 was refused
```

**Solution (Giải pháp):**

```bash
# Check if minikube is running (Kiểm tra minikube đang chạy)
minikube status

# Start if not running (Start nếu chưa chạy)
minikube start

# Set kubectl context
kubectl config use-context minikube
```

---

### Minikube start fails (Minikube start thất bại)

**Solution (Giải pháp):**

```bash
# Delete old cluster and create new (Xóa cluster cũ và tạo mới)
minikube delete
minikube start --driver=docker

# If still failing, try different driver (Nếu vẫn lỗi, thử driver khác)
minikube start --driver=virtualbox
```

---

### Pod stuck in Pending (Pod stuck ở Pending)

**Check (Kiểm tra):**

```bash
kubectl describe pod <pod-name>
kubectl get events
```

**Common causes (Nguyên nhân phổ biến):**

- Not enough resources → Increase minikube resources (Không đủ resources → Tăng minikube resources)
- ImagePullBackOff → Check image name, registry credentials (Kiểm tra image name, registry credentials)

---

## 🌐 Network Issues

### Cannot pull Docker images (Không thể pull Docker images)

**Error (Lỗi):**

```
Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: request canceled
```

**Solution (Giải pháp):**

```bash
# Check DNS (Kiểm tra DNS)
nslookup registry-1.docker.io

# Try using a mirror - add to Docker daemon.json
# (Thử dùng mirror - thêm vào Docker daemon.json)
{
  "registry-mirrors": ["https://mirror.gcr.io"]
}

# Or use VPN if registry is blocked (Hoặc dùng VPN nếu registry bị block)
```

---

### Proxy issues (Vấn đề Proxy)

**Solution (Giải pháp):**

```bash
# Set proxy for Docker
# Windows: Docker Desktop → Settings → Resources → Proxies

# Linux: Add to /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"

# Reload
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## 💡 General Tips (Tips chung)

### Check logs (Kiểm tra logs)

```bash
# Docker container logs
docker logs <container_id>

# Docker system logs - Linux
journalctl -u docker.service

# Kubernetes pod logs
kubectl logs <pod-name>
```

### Complete environment reset (Reset môi trường hoàn toàn)

```bash
# Docker - delete everything (xóa tất cả)
docker system prune -a --volumes

# Minikube - delete cluster (xóa cluster)
minikube delete --all

# Git - reset repo
git clean -fdx
git reset --hard HEAD
```

---

## 🆘 Still not resolved? (Vẫn không giải quyết được?)

1. **Google the error message** - Copy exact error and search (Copy chính xác error và search)
2. **Stack Overflow** - Search with tags [docker], [kubernetes], [gitlab-ci], etc.
3. **GitLab/GitHub Issues** - Search in the tool's repository
4. **Ask in community** - Discord/Slack of the projects

### Official Documentation (Tài liệu chính thức)

| Tool | Documentation |
|------|---------------|
| Docker | [docs.docker.com](https://docs.docker.com/) |
| GitLab CI | [docs.gitlab.com/ee/ci](https://docs.gitlab.com/ee/ci/) |
| GitHub Actions | [docs.github.com/actions](https://docs.github.com/en/actions) |
| Kubernetes | [kubernetes.io/docs](https://kubernetes.io/docs/home/) |
| Git | [git-scm.com/doc](https://git-scm.com/doc) |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [Tools Overview](./TOOLS_OVERVIEW.md) | **Troubleshooting** | [Cheatsheet](./CHEATSHEET.md) |

---

*Last Updated: 2025-12-30*

*Cập nhật lần cuối: 2025-12-30*
