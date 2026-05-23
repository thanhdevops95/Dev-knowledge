# macOS Setup Guide

> 🍎 Guide to set up DevOps environment on macOS
>
> *Hướng dẫn thiết lập môi trường DevOps trên macOS*

---

## Track 1 Setup

### Method 1: Automatic (Recommended) - Cách 1: Tự động (Khuyến nghị)

```bash
chmod +x ./scripts/macos/setup_track1.sh
./scripts/macos/setup_track1.sh
```

### Method 2: Manual (Cách 2: Thủ công)

#### Step 1: Install Homebrew (Bước 1: Cài đặt Homebrew)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install tools (Bước 2: Cài đặt các tools)

```bash
brew install git
brew install --cask docker
brew install --cask visual-studio-code
```

### Verify Track 1

```bash
./scripts/macos/verify_track1.sh
```

---

## Track 2 Setup (Orchestration)

### Method 1: Automatic (Recommended)

```bash
chmod +x ./scripts/macos/setup_track2.sh
./scripts/macos/setup_track2.sh
```

### Method 2: Manual (Thủ công)

#### Step 1: Install Kubernetes Tools

```bash
brew install kubectl minikube helm jenkins-lts
```

#### Step 2: Configure Minikube

```bash
minikube start --driver=docker
```

### Verify Track 2

```bash
kubectl version --client
minikube status
helm version
```

---

## Track 3 Setup (Cloud & IaC)

### Method 1: Automatic (Recommended)

```bash
chmod +x ./scripts/macos/setup_track3.sh
./scripts/macos/setup_track3.sh
```

### Method 2: Manual (Thủ công)

#### Step 1: Install Terraform, AWS CLI, Ansible

```bash
# Terraform
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# AWS CLI & Ansible
brew install awscli ansible
```

### Verify Track 3

```bash
terraform -v
aws --version
ansible --version
```

---

## Track 4 Setup (DevSecOps)

### Method 1: Automatic (Recommended)

```bash
chmod +x ./scripts/macos/setup_track4.sh
./scripts/macos/setup_track4.sh
```

### Method 2: Manual (Thủ công)

```bash
brew install trivy hadolint
docker pull owasp/zap2docker-stable
```

### Verify Track 4

```bash
trivy -v
hadolint --version
```

---

## ⚠️ Common Mistakes & Troubleshooting (Lỗi thường gặp & Xử lý)

> ⚠️ **Apple Silicon (M1/M2/M3) Issues:**
>
> **Problem:** Some Docker images crash with `exec format error`.
> **Example:** Running an image built for Intel (amd64) on Apple Silicon (arm64).
> **Fix:** Use `--platform linux/amd64` in docker run command.
> *(Dùng flag `--platform linux/amd64` khi chạy lệnh docker run.)*

> ⚠️ **Homebrew Issues:**
>
> **Problem:** `command not found` after brew install.
> **Reason:** Path not added to shell profile (zshrc).
> **Fix:** Run the command suggested by Homebrew output to add to path. usually:
> `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc`

> ✅ **Checkpoint:**
>
> - [ ] Can you run `docker run hello-world`?
> - [ ] Is `brew doctor` saying "Your system is ready to brew"?
> - [ ] Can you run `kubectl`?

## 🔗 Navigation

[⬅️ Windows Setup](./WINDOWS_SETUP.md) | [Linux Setup ➡️](./LINUX_SETUP.md)
