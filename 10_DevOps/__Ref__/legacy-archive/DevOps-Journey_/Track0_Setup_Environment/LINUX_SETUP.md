# Linux Setup Guide

> 🐧 Guide to set up DevOps environment on Linux (Ubuntu/Debian)
>
> *Hướng dẫn thiết lập môi trường DevOps trên Linux (Ubuntu/Debian)*

---

## Track 1 Setup

### Method 1: Automatic (Recommended) - Cách 1: Tự động (Khuyến nghị)

```bash
chmod +x ./scripts/linux/setup_track1.sh
./scripts/linux/setup_track1.sh
```

### Method 2: Manual (Cách 2: Thủ công)

#### Step 1: Update system (Bước 1: Cập nhật hệ thống)

```bash
sudo apt update && sudo apt upgrade -y
```

#### Step 2: Install Git (Bước 2: Cài đặt Git)

```bash
sudo apt install -y git
```

#### Step 3: Install Docker (Bước 3: Cài đặt Docker)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Verify Track 1

```bash
./scripts/linux/verify_track1.sh
```

---

## Track 2 Setup (Orchestration)

### Method 1: Automatic (Recommended)

```bash
chmod +x ./scripts/linux/setup_track2.sh
./scripts/linux/setup_track2.sh
```

### Method 2: Manual (Thủ công)

#### Step 1: Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

#### Step 2: Install Minikube

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

#### Step 3: Configure Minikube

```bash
minikube start --driver=docker
```

### Verify Track 2

```bash
kubectl version --client
minikube status
```

---

## Track 3 Setup (Cloud & IaC)

### Method 1: Automatic (Recommended)

```bash
chmod +x ./scripts/linux/setup_track3.sh
./scripts/linux/setup_track3.sh
```

### Method 2: Manual (Thủ công)

#### Step 1: Install Terraform

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

#### Step 2: Install Ansible & AWS CLI

```bash
sudo apt install -y ansible unzip

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
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
chmod +x ./scripts/linux/setup_track4.sh
./scripts/linux/setup_track4.sh
```

### Method 2: Manual (Thủ công)

#### Step 1: Install Trivy

```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

#### Step 2: Install Hadolint & ZAP

```bash
# Hadolint via docker
docker pull hadolint/hadolint

# OWASP ZAP via docker
docker pull owasp/zap2docker-stable
```

### Verify Track 4

```bash
trivy -v
```

---

## ⚠️ Common Mistakes & Troubleshooting (Lỗi thường gặp & Xử lý)

> ⚠️ **Permission Denied (Docker):**
>
> **Problem:** `Got permission denied while trying to connect to the Docker daemon socket`.
> **Fix:** You forgot to add user to docker group.
> `sudo usermod -aG docker $USER` -> **Logout and Login again**.

> ⚠️ **Sudo required:**
>
> **Problem:** `apt-get` or `install` fails.
> **Reason:** Linux requires root privileges for installing software.
> **Fix:** Always check if you need `sudo`.

> ✅ **Checkpoint:**
>
> - [ ] Can you run `docker run hello-world` without sudo?
> - [ ] Is `kubectl` installed?
> - [ ] Is `terraform` installed?

## 🔗 Navigation

[⬅️ macOS Setup](./MACOS_SETUP.md) | [README ➡️](./README.md)
