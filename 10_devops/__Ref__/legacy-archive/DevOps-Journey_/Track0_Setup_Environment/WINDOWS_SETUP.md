# Windows Setup Guide

> 🪟 Guide to set up DevOps environment on Windows 10/11
>
> *Hướng dẫn thiết lập môi trường DevOps trên Windows 10/11*

---

## Track 1 Setup

### Method 1: Automatic (Recommended) - Cách 1: Tự động (Khuyến nghị)

```powershell
# Open PowerShell as Administrator (Mở PowerShell với quyền Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force
.\scripts\windows\setup_track1.ps1
```

### Method 2: Manual (Cách 2: Thủ công)

#### Step 1: Install WSL2 (Bước 1: Cài đặt WSL2)

1. Open PowerShell as Administrator *(Mở PowerShell với quyền Administrator)*
2. Run the command *(Chạy lệnh)*:

   ```powershell
   wsl --install
   ```

3. Restart your computer *(Khởi động lại máy tính)*

#### Step 2: Install Docker Desktop (Bước 2: Cài đặt Docker Desktop)

1. Download from [Docker Desktop](https://www.docker.com/products/docker-desktop/) *(Tải từ Docker Desktop)*
2. Run the installer *(Chạy installer)*
3. Start Docker Desktop *(Khởi động Docker Desktop)*

#### Step 3: Install Git (Bước 3: Cài đặt Git)

1. Download from [Git SCM](https://git-scm.com/download/win) *(Tải từ Git SCM)*
2. Run installer with default options *(Chạy installer với default options)*

#### Step 4: Install VS Code (Bước 4: Cài đặt VS Code)

1. Download from [VS Code](https://code.visualstudio.com/) *(Tải từ VS Code)*
2. Install extensions: Docker, Remote WSL *(Cài đặt extensions: Docker, Remote WSL)*

### Verify Track 1

```powershell
.\scripts\windows\verify_track1.ps1
```

---

## Track 2 Setup (Orchestration)

### Method 1: Automatic (Recommended)

```powershell
.\scripts\windows\setup_track2.ps1
```

### Method 2: Manual (Thủ công)

#### Step 1: Install Kubernetes Tools (Cài đặt công cụ K8s)

Run in PowerShell Administrator:

```powershell
# Install kubectl
winget install Kubernetes.kubectl

# Install Minikube
winget install Kubernetes.Minikube

# Install Helm
winget install Helm.Helm
```

#### Step 2: Configure Minikube (Cấu hình Minikube)

```powershell
minikube start --driver=docker
```

#### Step 3: Verify Track 2

```powershell
kubectl version --client
minikube status
helm version
```

---

## Track 3 Setup (Cloud & IaC)

### Method 1: Automatic (Recommended)

```powershell
.\scripts\windows\setup_track3.ps1
```

### Method 2: Manual (Thủ công)

#### Step 1: Install Terraform & AWS CLI

```powershell
# Install Terraform
winget install Hashicorp.Terraform

# Install AWS CLI
winget install Amazon.AWSCLI
```

#### Step 2: Install Ansible (via WSL)

> ⚠️ **Note:** Ansible does not run natively on Windows. You **MUST** install it inside WSL (Ubuntu).
>
> *Ansible không chạy trực tiếp trên Windows. Bạn PHẢI cài nó trong WSL (Ubuntu).*

1. Open Ubuntu (WSL) terminal.
2. Run:

   ```bash
   sudo apt update
   sudo apt install -y ansible
   ```

### Verify Track 3

```powershell
terraform -v
aws --version
wsl ansible --version
```

---

## Track 4 Setup (DevSecOps)

### Method 1: Automatic (Recommended)

```powershell
.\scripts\windows\setup_track4.ps1
```

### Method 2: Manual (Thủ công)

#### Step 1: Install Security Tools

We recommend using Docker images for these tools to keep your system clean.
*(Chúng tôi khuyên dùng Docker images cho các công cụ này để giữ máy sạch.)*

**Trivy:**

```powershell
winget install AquaSecurity.Trivy
```

**Hadolint:**

```powershell
# Install via Scoop or just use Docker
docker pull hadolint/hadolint
```

**OWASP ZAP:**

```powershell
# Run via Docker
docker pull owasp/zap2docker-stable
```

### Verify Track 4

```powershell
trivy -v
docker run --rm hadolint/hadolint hadolint --version
```

---

## ⚠️ Common Mistakes & Troubleshooting (Lỗi thường gặp & Xử lý)

> ⚠️ **WSL2 Issues:**
>
> **Error:** `WslRegisterDistribution failed with error: 0x800701bc`
> **Fix:** You need to update the WSL 2 kernel. Download it from Microsoft website.
> *(Bạn cần cập nhật WSL 2 kernel. Tải từ trang chủ Microsoft.)*

> ⚠️ **Hyper-V Conflicts:**
>
> **Error:** VirtualBox or VMware stops working.
> **Reason:** WSL2 uses Hyper-V which might conflict.
> **Fix:** Use Docker Desktop with WSL2 backend (recommended).

> ✅ **Checkpoint:**
>
> - [ ] Can you run `wsl` in PowerShell?
> - [ ] Does `docker run hello-world` work?
> - [ ] Can you access the internet from WSL?

---

## 🔗 Navigation

[⬅️ README](./README.md) | [macOS Setup ➡️](./MACOS_SETUP.md)
