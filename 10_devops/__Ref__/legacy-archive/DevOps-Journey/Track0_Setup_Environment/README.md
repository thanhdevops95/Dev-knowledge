# 🛠️ Setup Environment

[![Prerequisites](https://img.shields.io/badge/Prerequisites-None-green?style=flat-square)](.)

> **Development Environment Setup Guide** for DevOps Journey.
>
> *Hướng dẫn cài đặt môi trường phát triển cho DevOps Journey.*

---

## 📋 Table of Contents (Mục Lục)

- [System Requirements](#-system-requirements-yêu-cầu-hệ-thống)
- [Installation by OS](#-installation-by-os-cài-đặt-theo-os)
- [Git Platform Setup](#-git-platform-setup-cài-đặt-git-platform)
- [Tools Overview](#-tools-overview)
- [Verification](#-verification)
- [Troubleshooting](#-troubleshooting)

---

## 💻 System Requirements (Yêu Cầu Hệ Thống)

### Hardware Requirements (Yêu cầu phần cứng)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 8 GB | 16 GB |
| **Storage** | 50 GB SSD | 100 GB SSD |
| **CPU** | 4 cores | 8 cores |
| **Network** | Stable internet | Stable internet |

### Supported Operating Systems (Hệ điều hành hỗ trợ)

- ✅ **Windows 10/11** (with WSL2)
- ✅ **macOS** (Monterey or later)
- ✅ **Linux** (Ubuntu 20.04+, Fedora 35+)

---

## 🔧 Installation by OS (Cài Đặt Theo OS)

### Windows 10/11

#### 1. Install WSL2 (Cài đặt WSL2)

```powershell
# Open PowerShell as Administrator (Mở PowerShell với quyền Admin)
wsl --install

# Restart your computer (Restart máy tính)
# After restart, Ubuntu will be installed automatically
# (Sau khi restart, Ubuntu sẽ được cài đặt tự động)
```

#### 2. Install Windows Terminal (Cài đặt Windows Terminal)

```powershell
# From Microsoft Store or (Từ Microsoft Store hoặc)
winget install Microsoft.WindowsTerminal
```

#### 3. Install Docker Desktop (Cài đặt Docker Desktop)

1. Download from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Run the installer (Chạy installer)
3. Enable WSL2 backend in settings (Bật WSL2 backend trong settings)
4. Restart Docker Desktop

#### 4. Install Git (Cài đặt Git)

```powershell
winget install Git.Git
```

#### 5. Install VS Code (Cài đặt VS Code)

```powershell
winget install Microsoft.VisualStudioCode
```

#### 6. Install Python (Cài đặt Python)

```powershell
winget install Python.Python.3.12
```

---

### macOS

#### 1. Install Homebrew (Cài đặt Homebrew)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install Tools (Cài đặt các tools)

```bash
# Git
brew install git

# Docker Desktop
brew install --cask docker

# VS Code
brew install --cask visual-studio-code

# Python
brew install python@3.12

# iTerm2 (optional but recommended - tùy chọn nhưng khuyến nghị)
brew install --cask iterm2
```

---

### Linux (Ubuntu/Debian)

#### 1. Update System (Cập nhật hệ thống)

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Git (Cài đặt Git)

```bash
sudo apt install git -y
```

#### 3. Install Docker (Cài đặt Docker)

```bash
# Add Docker's GPG key (Thêm GPG key của Docker)
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add repository (Thêm repository)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker (Cài đặt Docker)
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# Add user to docker group (Thêm user vào docker group)
sudo usermod -aG docker $USER
newgrp docker
```

#### 4. Install Python (Cài đặt Python)

```bash
sudo apt install python3 python3-pip python3-venv -y
```

#### 5. Install VS Code (Cài đặt VS Code)

```bash
sudo snap install code --classic
```

---

## 🌐 Git Platform Setup (Cài Đặt Git Platform)

> **This course supports both GitLab and GitHub!**
>
> *Khóa học hỗ trợ cả GitLab và GitHub!*

### Option A: GitLab (Primary - Chính)

GitLab is the **primary platform** for this course, especially for CI/CD content.

*GitLab là **nền tảng chính** cho khóa học này, đặc biệt cho nội dung CI/CD.*

#### 1. Create GitLab Account (Tạo tài khoản GitLab)

1. Go to [gitlab.com](https://gitlab.com)
2. Click **"Register"** or **"Sign up"**
3. Fill in your information (Điền thông tin của bạn)
4. Verify your email (Xác nhận email)

#### 2. SSH Setup for GitLab (Cấu hình SSH cho GitLab)

```bash
# Generate SSH key (Tạo SSH key)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key (Thêm key)
ssh-add ~/.ssh/id_ed25519

# Copy public key (Copy public key)
cat ~/.ssh/id_ed25519.pub
# Paste this key to: GitLab > Preferences > SSH Keys
# (Dán key này vào: GitLab > Preferences > SSH Keys)

# Test connection (Kiểm tra kết nối)
ssh -T git@gitlab.com
# Expected: Welcome to GitLab, @username!
```

#### 3. Git Configuration for GitLab (Cấu hình Git cho GitLab)

```bash
# User information (Thông tin user)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Default branch
git config --global init.defaultBranch main

# Editor
git config --global core.editor "code --wait"

# Pull strategy
git config --global pull.rebase false
```

---

### Option B: GitHub (Alternative - Thay thế)

GitHub is also fully supported if you prefer it.

*GitHub cũng được hỗ trợ đầy đủ nếu bạn thích.*

#### 1. Create GitHub Account (Tạo tài khoản GitHub)

1. Go to [github.com](https://github.com)
2. Click **"Sign up"**
3. Fill in your information (Điền thông tin của bạn)
4. Verify your email (Xác nhận email)

#### 2. SSH Setup for GitHub (Cấu hình SSH cho GitHub)

```bash
# Generate SSH key (if not created already)
# (Tạo SSH key nếu chưa có)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key (Thêm key)
ssh-add ~/.ssh/id_ed25519

# Copy public key (Copy public key)
cat ~/.ssh/id_ed25519.pub
# Paste this key to: GitHub > Settings > SSH and GPG Keys
# (Dán key này vào: GitHub > Settings > SSH and GPG Keys)

# Test connection (Kiểm tra kết nối)
ssh -T git@github.com
# Expected: Hi username! You've successfully authenticated...
```

---

### Using Both Platforms (Sử dụng cả hai nền tảng)

You can use both GitLab and GitHub with the same SSH key!

*Bạn có thể dùng cả GitLab và GitHub với cùng một SSH key!*

```bash
# Test both connections (Kiểm tra cả hai kết nối)
ssh -T git@gitlab.com
ssh -T git@github.com
```

---

## 📦 Tools Overview

For detailed information about all tools → **[TOOLS_OVERVIEW.md](./TOOLS_OVERVIEW.md)**

*Xem chi tiết về các tools → **[TOOLS_OVERVIEW.md](./TOOLS_OVERVIEW.md)***

| Track | Tools |
|-------|-------|
| **Track 1** | Linux, Bash, Python, Git, Docker, NGINX, GitLab CI |
| **Track 2** | Docker Compose, Jenkins, Kubernetes, Prometheus, Grafana |
| **Track 3** | AWS CLI, Terraform, Ansible, MySQL, PostgreSQL, Redis |
| **Track 4** | Trivy, SonarQube, HashiCorp Vault, OWASP ZAP |
| **Track 5** | N/A (Career focused) |

---

## ✅ Verification

Run these commands to verify installation:

*Chạy các lệnh sau để kiểm tra cài đặt:*

```bash
# Git
git --version
# Expected: git version 2.x.x

# Docker
docker --version
# Expected: Docker version 24.x.x

docker compose version
# Expected: Docker Compose version v2.x.x

# Python
python3 --version
# Expected: Python 3.x.x

# VS Code
code --version
# Expected: 1.x.x
```

### Quick Test (Kiểm tra nhanh)

```bash
# Test Docker
docker run hello-world

# Test Git config (Kiểm tra cấu hình Git)
git config --list

# Test Python
python3 -c "print('Hello DevOps!')"

# Test GitLab connection (Kiểm tra kết nối GitLab)
ssh -T git@gitlab.com

# Test GitHub connection (optional - Kiểm tra kết nối GitHub)
ssh -T git@github.com
```

---

## 🔧 VS Code Extensions

### Recommended Extensions (Extensions khuyến nghị)

```bash
# Install via command line (Cài đặt qua command line)
code --install-extension ms-vscode-remote.remote-wsl
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-python.python
code --install-extension hashicorp.terraform
code --install-extension redhat.ansible
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension gitlab.gitlab-workflow
code --install-extension eamodio.gitlens
```

### Extension List (Danh sách extensions)

| Extension | Purpose (Mục Đích) |
|-----------|-------------------|
| Remote - WSL | Work with WSL in VS Code (Làm việc với WSL) |
| Docker | Docker support |
| Python | Python language support |
| Terraform | Terraform syntax & validation |
| Ansible | Ansible playbook support |
| Kubernetes | K8s cluster management |
| GitLab Workflow | GitLab integration (Tích hợp GitLab) |
| GitLens | Advanced Git features |

---

## ❓ Troubleshooting

See detailed troubleshooting guide → **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**

*Xem hướng dẫn xử lý lỗi chi tiết → **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)***

### Common Issues (Các lỗi thường gặp)

| Issue | Solution |
|-------|----------|
| Docker daemon not running | Restart Docker Desktop |
| WSL2 not working | `wsl --update` |
| Permission denied (Docker) | `sudo usermod -aG docker $USER` |
| Git authentication failed | Setup SSH key (Cấu hình SSH key) |
| GitLab SSH not working | Check SSH key in Preferences > SSH Keys |
| GitHub SSH not working | Check SSH key in Settings > SSH and GPG Keys |

---

## 📋 Cheatsheet

See all important commands → **[CHEATSHEET.md](./CHEATSHEET.md)**

*Xem tất cả commands quan trọng → **[CHEATSHEET.md](./CHEATSHEET.md)***

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [Main README](../README.md) | **Setup Environment** | [Track 1: Foundation](../Track1_Foundation_StaticWeb/) |

---

<div align="center">

**After setup is complete, start with [Track 1 →](../Track1_Foundation_StaticWeb/)! 🚀**

*Sau khi cài đặt xong, hãy bắt đầu với Track 1!*

</div>
