# 🔧 DevOps Environment Setup Guide

> **Hướng dẫn chi tiết cài đặt môi trường cho 3 hệ điều hành**

---

## 📋 Tổng quan

### Tools cần cài đặt

| Tool | Mục đích | Bắt buộc |
|------|----------|----------|
| Git | Version control | ✅ |
| Docker | Containers | ✅ |
| kubectl | Kubernetes CLI | ✅ |
| Terraform | Infrastructure as Code | ✅ |
| Python 3 | Scripting | ✅ |
| VS Code | Editor | ✅ |
| Helm | Kubernetes package manager | ⭐ |
| AWS CLI | AWS operations | ⭐ |
| minikube/kind | Local K8s | ⭐ |

---

## 🍎 macOS Setup

### Option A: Automated (Recommended)

```bash
# Clone repo và chạy script
git clone https://github.com/thanhlehoang0107/DevOps-Mastery.git
cd DevOps-Mastery
bash scripts/setup-mac.sh
```

### Option B: Manual

#### 1. Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Install tools

```bash
# Git
brew install git

# Docker Desktop
brew install --cask docker

# kubectl
brew install kubectl

# Terraform
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Python 3
brew install python3

# VS Code
brew install --cask visual-studio-code

# Optional
brew install helm
brew install awscli
brew install minikube
```

#### 3. Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 4. Start Docker Desktop

Mở Docker Desktop từ Applications.

---

## 🐧 Linux (Ubuntu/Debian) Setup

### Option A: Automated

```bash
git clone https://github.com/thanhlehoang0107/DevOps-Mastery.git
cd DevOps-Mastery
bash scripts/setup-linux.sh
```

### Option B: Manual

#### 1. Update system

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Git

```bash
sudo apt install -y git
```

#### 3. Install Docker

```bash
# Remove old versions
sudo apt remove docker docker-engine docker.io containerd runc

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 4. Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl
```

#### 5. Install Terraform

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

#### 6. Install Python 3

```bash
sudo apt install -y python3 python3-pip python3-venv
```

#### 7. Install VS Code

```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install -y code
rm packages.microsoft.gpg
```

---

## 🪟 Windows Setup (WSL2)

### Step 1: Enable WSL2

```powershell
# PowerShell as Administrator
wsl --install
# Restart computer
```

### Step 2: Install Ubuntu

```powershell
wsl --install -d Ubuntu-22.04
```

### Step 3: Setup Ubuntu

Sau khi restart, mở Ubuntu và:

```bash
# Update
sudo apt update && sudo apt upgrade -y

# Follow Linux setup above
bash scripts/setup-linux.sh
```

### Step 4: Install Docker Desktop

1. Download từ [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Chạy installer
3. Enable "Use WSL 2 based engine"
4. Resources → WSL Integration → Enable Ubuntu

### Step 5: Install VS Code

1. Download từ [code.visualstudio.com](https://code.visualstudio.com/)
2. Install extension "Remote - WSL"
3. Mở VS Code trong WSL: `code .`

---

## ✅ Verification

Chạy script verify:

```bash
bash scripts/verify-tools.sh
```

Hoặc kiểm tra manual:

```bash
git --version
docker --version
docker compose version
kubectl version --client
terraform version
python3 --version
code --version
```

---

## 🔧 VS Code Extensions

### Recommended extensions

```bash
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension hashicorp.terraform
code --install-extension ms-python.python
code --install-extension redhat.vscode-yaml
code --install-extension yzhang.markdown-all-in-one
```

---

## 📦 Optional Tools

```bash
# Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

# kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

---

## 🚨 Troubleshooting

### Docker không start

**Linux:**

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

**Windows:**

- Mở Docker Desktop manually
- Check WSL2 enabled

### Permission denied với Docker

```bash
sudo usermod -aG docker $USER
newgrp docker
# Hoặc logout và login lại
```

### kubectl không connect cluster

```bash
# Check config
kubectl config view

# Check context
kubectl config current-context
```

---

## 🎉 Ready

Khi verify thành công, bạn đã sẵn sàng bắt đầu khóa học!

👉 **[Quay lại Module 00](../00_INTRODUCTION/README.md)**
