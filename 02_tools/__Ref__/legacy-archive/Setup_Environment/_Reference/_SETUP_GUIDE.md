# 💻 Hướng dẫn Cài đặt Môi trường DevOps

> **Hướng dẫn chi tiết thiết lập môi trường cho macOS, Linux và Windows**

---

## 📋 Tổng quan

Trước khi bắt đầu khóa học, bạn cần chuẩn bị môi trường làm việc với các công cụ sau:

### ✅ Công cụ bắt buộc

- **Git** - Version control
- **Docker** - Containerization  
- **VS Code** - Code editor
- **Python 3.11+** - Programming language
- **Terminal** - Command line interface

### ✅ Tài khoản cần tạo (Miễn phí)

1. **GitHub** - <https://github.com>
2. **Docker Hub** - <https://hub.docker.com>
3. **(Tùy chọn) AWS Free Tier** - <https://aws.amazon.com/free>

---

## 🍎 Setup cho macOS

### Cách 1: Tự động (Khuyến nghị)

```bash
# Clone repo
git clone https://github.com/thanhlehoang0107/devops-course.git
cd devops-course

# Chạy script tự động
bash scripts/setup-mac.sh
```

### Cách 2: Thủ công

#### 1. Cài đặt Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Cài đặt công cụ cơ bản

```bash
brew install git python@3.11
brew install --cask visual-studio-code docker iterm2
```

#### 3. Cài đặt công cụ DevOps

```bash
brew install kubectl helm k9s terraform ansible awscli
```

#### 4. Kiểm tra

```bash
bash scripts/verify-tools.sh
```

---

## 🐧 Setup cho Linux (Ubuntu/Debian)

### Cách 1: Tự động (Khuyến nghị)

```bash
# Clone repo
git clone https://github.com/thanhlehoang0107/devops-course.git
cd devops-course

# Chạy script tự động
bash scripts/setup-linux.sh
```

### Cách 2: Thủ công

#### 1. Cập nhật hệ thống

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Cài đặt Git và Python

```bash
sudo apt install -y git python3.11 python3-pip
```

#### 3. Cài đặt Docker

```bash
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
# Logout và login lại
```

#### 4. Cài đặt VS Code

```bash
# Download .deb từ: https://code.visualstudio.com
sudo dpkg -i code_*.deb
```

#### 5. Cài đặt công cụ DevOps

```bash
# Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Ansible
sudo apt install ansible

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

---

## 🪟 Setup cho Windows 10/11

### Bước 1: Cài đặt WSL 2 (Windows Subsystem for Linux)

#### 1.1. Mở PowerShell với quyền Administrator

```powershell
# Cài WSL2 với Ubuntu
wsl --install -d Ubuntu

# Khởi động lại máy nếu được yêu cầu
```

#### 1.2. Cài đặt Windows Terminal

```powershell
winget install Microsoft.WindowsTerminal
```

### Bước 2: Setup bên trong WSL Ubuntu

Sau khi mở Windows Terminal → chọn tab Ubuntu:

```bash
# Cập nhật Ubuntu
sudo apt update && sudo apt upgrade -y

# Clone repo
git clone https://github.com/thanhlehoang0107/devops-course.git
cd devops-course

# Chạy script setup Linux
bash scripts/setup-linux.sh
```

### Bước 3: Cài đặt Docker Desktop (trên Windows)

1. Download từ: <https://www.docker.com/products/docker-desktop>
2. Cài đặt và enable WSL 2 backend
3. Khởi động Docker Desktop

### Bước 4: Cài đặt VS Code (trên Windows)

```powershell
winget install Microsoft.VisualStudioCode
```

Sau đó, trong WSL terminal:

```bash
code .  # Tự động cài VS Code Server
```

### ⚠️ Lưu ý quan trọng cho Windows

> **Luôn chạy tất cả lệnh DevOps trong WSL Ubuntu, KHÔNG phải PowerShell/CMD**

---

## 🎨 (Tùy chọn) Nâng cấp Terminal

### Oh My Zsh

```bash
# macOS & Linux
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### Zsh Plugins

```bash
# Autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Syntax highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Thêm vào `~/.zshrc`:

```bash
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
```

### Nerd Fonts (Icon đẹp cho terminal)

1. Download [FiraCode Nerd Font](https://www.nerdfonts.com/font-downloads)
2. Cài đặt font
3. Đặt làm font mặc định trong Terminal/iTerm2/Windows Terminal

---

## 🔧 Cấu hình Git

```bash
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
```

---

## 📦 VS Code Extensions

Mở VS Code → Extensions (Ctrl+Shift+X) → Cài đặt:

- **GitLens** - Git supercharged
- **Docker** - Docker management
- **Kubernetes** - K8s support
- **HashiCorp Terraform** - Terraform syntax
- **Ansible** - Ansible playbooks
- **YAML** - YAML validation
- **Remote - WSL** (Windows only)

---

## ✅ Kiểm tra cài đặt

```bash
# Chạy script kiểm tra
bash scripts/verify-tools.sh
```

Kết quả mong đợi:

```
🔍 Kiểm tra môi trường DevOps...

✅ git: git version 2.x.x
✅ docker: Docker version x.x.x
✅ kubectl: Client Version: x.x.x
✅ terraform: Terraform vx.x.x
✅ ansible: ansible [core x.x.x]
✅ python3: Python 3.11.x
✅ code: x.x.x

🎉 Tất cả công cụ đã được cài đặt!
```

---

## 🚀 Test nhanh

```bash
# Test Docker
docker run hello-world

# Test Git
git --version

# Test Python
python3 --version

# Test Counter App
cd source-code
docker-compose up -d
# Mở http://localhost:5000
```

---

## 🆘 Troubleshooting

### Docker không chạy

```bash
# macOS/Windows: Khởi động Docker Desktop
# Linux: 
sudo systemctl start docker
sudo systemctl enable docker
```

### Permission denied cho Docker

```bash
sudo usermod -aG docker $USER
# Logout và login lại
```

### kubectl not found

```bash
# Check PATH
echo $PATH

# Homebrew thường cài vào:
# macOS: /opt/homebrew/bin
# Linux: /home/linuxbrew/.linuxbrew/bin
```

### VS Code `code` command không hoạt động

```bash
# macOS: Mở VS Code
# Cmd+Shift+P → "Shell Command: Install 'code' command in PATH"
```

---

## 📚 Tài nguyên thêm

- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

---

## ⏭️ Bước tiếp theo

Khi đã hoàn tất setup:

👉 **Bắt đầu với [Module 01: PLAN](./01_PLAN/README.md)**

---

💡 **Mẹo**: Bookmark trang này để tham khảo khi cần!
