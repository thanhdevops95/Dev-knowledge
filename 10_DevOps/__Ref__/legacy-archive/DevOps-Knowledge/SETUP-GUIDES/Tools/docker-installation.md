# Docker Installation Guide

> Hướng dẫn cài đặt Docker trên các hệ điều hành

## 📋 Mục lục

- [Ubuntu/Debian](#ubuntudebian)
- [CentOS/RHEL](#centosrhel)
- [macOS](#macos)
- [Windows](#windows)
- [Verify Installation](#verify-installation)
- [Post-Installation](#post-installation)

## Ubuntu/Debian

### 1. Gỡ cài đặt phiên bản cũ (nếu có)

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

### 2. Cập nhật package index

```bash
sudo apt-get update
```

### 3. Cài đặt dependencies

```bash
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

### 4. Thêm Docker's official GPG key

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### 5. Setup repository

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 6. Cài đặt Docker Engine

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## CentOS/RHEL

### 1. Gỡ cài đặt phiên bản cũ

```bash
sudo yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine
```

### 2. Cài đặt yum-utils

```bash
sudo yum install -y yum-utils
```

### 3. Setup repository

```bash
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

### 4. Cài đặt Docker Engine

```bash
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 5. Start Docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## macOS

### Option 1: Docker Desktop (Recommended)

1. Download Docker Desktop từ [docker.com](https://www.docker.com/products/docker-desktop)
2. Mở file `.dmg` và kéo Docker vào Applications
3. Chạy Docker Desktop từ Applications
4. Đợi Docker khởi động (icon trên menu bar)

### Option 2: Homebrew

```bash
brew install --cask docker
```

## Windows

### Requirements
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- WSL 2 feature enabled

### Installation Steps

1. Download Docker Desktop từ [docker.com](https://www.docker.com/products/docker-desktop)
2. Chạy installer
3. Follow installation wizard
4. Restart computer
5. Start Docker Desktop

### Enable WSL 2

```powershell
# Run in PowerShell as Administrator
wsl --install
wsl --set-default-version 2
```

## Verify Installation

```bash
# Check Docker version
docker --version
docker version

# Check Docker Compose
docker compose version

# Run test container
docker run hello-world
```

**Expected output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

## Post-Installation

### Linux: Run Docker without sudo

```bash
# Create docker group
sudo groupadd docker

# Add user to docker group
sudo usermod -aG docker $USER

# Activate changes
newgrp docker

# Verify
docker run hello-world
```

### Configure Docker to start on boot

```bash
# Ubuntu/Debian
sudo systemctl enable docker.service
sudo systemctl enable containerd.service

# CentOS/RHEL
sudo systemctl enable docker
```

### Configure Docker daemon

Create/edit `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```

Restart Docker:
```bash
sudo systemctl restart docker
```

## Troubleshooting

### Cannot connect to Docker daemon

```bash
# Check if Docker is running
sudo systemctl status docker

# Start Docker
sudo systemctl start docker

# Check permissions
sudo usermod -aG docker $USER
newgrp docker
```

### Port already in use

```bash
# Find process using port
sudo lsof -i :80

# Kill process
sudo kill -9 <PID>
```

---

