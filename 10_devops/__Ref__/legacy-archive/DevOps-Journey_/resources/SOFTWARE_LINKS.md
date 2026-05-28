# 🔧 Software Links

> **Installation guides for all DevOps tools**
>
> *Tài liệu cài đặt tất cả công cụ DevOps*

---

## 📋 Overview (Giới thiệu)

This document contains official download links and installation guides for tools used in this course.

*Tài liệu này tổng hợp link tải chính thức và hướng dẫn cài đặt các công cụ.*

> ⚠️ **Note (Lưu ý):** Only download from official sources for security. (Chỉ tải từ nguồn chính thức để đảm bảo an toàn.)

---

## 1. Git Platforms (Nền tảng Git)

### 1.1 GitLab (Primary - Chính)

| Info | Link |
|------|------|
| **Website** | [gitlab.com](https://gitlab.com) |
| **Documentation** | [docs.gitlab.com](https://docs.gitlab.com) |
| **Sign Up** | [gitlab.com/users/sign_up](https://gitlab.com/users/sign_up) |

### 1.2 GitHub (Alternative - Thay thế)

| Info | Link |
|------|------|
| **Website** | [github.com](https://github.com) |
| **Documentation** | [docs.github.com](https://docs.github.com) |
| **GitHub CLI** | [cli.github.com](https://cli.github.com/) |

**GitHub CLI Installation:**

```bash
# Windows
choco install gh

# macOS
brew install gh

# Linux
sudo apt install gh
```

### 1.3 GitLab CLI (glab)

| Info | Link |
|------|------|
| **Download** | [gitlab.com/gitlab-org/cli](https://gitlab.com/gitlab-org/cli) |
| **Documentation** | [glab.readthedocs.io](https://glab.readthedocs.io/) |

**Installation:**

```bash
# Windows
choco install glab

# macOS
brew install glab

# Linux
sudo apt install glab
```

---

## 2. Basic Environment (Môi trường cơ bản)

### 2.1 Windows Subsystem for Linux (WSL2)

| Info | Link |
|------|------|
| **Documentation** | [Microsoft Docs](https://learn.microsoft.com/en-us/windows/wsl/install) |
| **Requirements** | Windows 10 version 2004+ or Windows 11 |

**Installation:**

```powershell
# PowerShell as Administrator
wsl --install
```

### 2.2 Docker Desktop

| Info | Link |
|------|------|
| **Download** | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Documentation** | [docs.docker.com](https://docs.docker.com/desktop/) |

| OS | Installation |
|----|--------------|
| Windows | [Download](https://www.docker.com/products/docker-desktop/) or `choco install docker-desktop` |
| macOS | `brew install --cask docker` |
| Linux | [Install Docker Engine](https://docs.docker.com/engine/install/) |

**Verify:**

```bash
docker --version
docker compose version
```

### 2.3 Git

| Info | Link |
|------|------|
| **Download** | [git-scm.com](https://git-scm.com/downloads) |
| **Documentation** | [git-scm.com/doc](https://git-scm.com/doc) |

| OS | Installation |
|----|--------------|
| Windows | [Download](https://git-scm.com/download/win) or `winget install Git.Git` |
| macOS | `brew install git` |
| Linux | `sudo apt install git` |

**Verify:**

```bash
git --version
```

---

## 3. Code Editor

### 3.1 Visual Studio Code

| Info | Link |
|------|------|
| **Download** | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Documentation** | [code.visualstudio.com/docs](https://code.visualstudio.com/docs) |

| OS | Installation |
|----|--------------|
| Windows | [Download](https://code.visualstudio.com/Download) or `winget install Microsoft.VisualStudioCode` |
| macOS | `brew install --cask visual-studio-code` |
| Linux | `sudo snap install code --classic` |

**Verify:**

```bash
code --version
```

### 3.2 Recommended Extensions (Extensions khuyến nghị)

```bash
# Install via command line (Cài đặt qua command line)
code --install-extension ms-vscode-remote.remote-wsl
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-python.python
code --install-extension hashicorp.terraform
code --install-extension redhat.ansible
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension gitlab.gitlab-workflow      # GitLab integration
code --install-extension github.vscode-github-actions # GitHub Actions
code --install-extension eamodio.gitlens
code --install-extension redhat.vscode-yaml
```

---

## 4. Container & Orchestration

### 4.1 kubectl (Kubernetes CLI)

| Info | Link |
|------|------|
| **Documentation** | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/) |

| OS | Installation |
|----|--------------|
| Windows | `choco install kubernetes-cli` |
| macOS | `brew install kubectl` |
| Linux | See [official docs](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) |

**Verify:**

```bash
kubectl version --client
```

### 4.2 Minikube (Local Kubernetes)

| Info | Link |
|------|------|
| **Download** | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/) |

| OS | Installation |
|----|--------------|
| Windows | `choco install minikube` |
| macOS | `brew install minikube` |
| Linux | See [official docs](https://minikube.sigs.k8s.io/docs/start/) |

**Verify:**

```bash
minikube version
```

### 4.3 Helm (Kubernetes Package Manager)

| Info | Link |
|------|------|
| **Download** | [helm.sh](https://helm.sh/docs/intro/install/) |

| OS | Installation |
|----|--------------|
| Windows | `choco install kubernetes-helm` |
| macOS | `brew install helm` |
| Linux | See [official docs](https://helm.sh/docs/intro/install/) |

**Verify:**

```bash
helm version
```

---

## 5. Infrastructure as Code

### 5.1 Terraform

| Info | Link |
|------|------|
| **Download** | [terraform.io](https://developer.hashicorp.com/terraform/downloads) |
| **Documentation** | [terraform.io/docs](https://developer.hashicorp.com/terraform/docs) |

| OS | Installation |
|----|--------------|
| Windows | `choco install terraform` |
| macOS | `brew install terraform` |
| Linux | See [official docs](https://developer.hashicorp.com/terraform/downloads) |

**Verify:**

```bash
terraform version
```

### 5.2 Ansible

| Info | Link |
|------|------|
| **Documentation** | [docs.ansible.com](https://docs.ansible.com/ansible/latest/installation_guide/index.html) |

**Installation:**

```bash
pip install ansible
```

**Verify:**

```bash
ansible --version
```

---

## 6. CI/CD Tools

### 6.1 Jenkins

| Info | Link |
|------|------|
| **Download** | [jenkins.io](https://www.jenkins.io/download/) |
| **Documentation** | [jenkins.io/doc](https://www.jenkins.io/doc/) |

**Docker Installation:**

```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  --name jenkins \
  jenkins/jenkins:lts
```

### 6.2 GitLab Runner

| Info | Link |
|------|------|
| **Download** | [docs.gitlab.com](https://docs.gitlab.com/runner/install/) |

**Docker Installation:**

```bash
docker run -d --name gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v gitlab-runner-config:/etc/gitlab-runner \
  gitlab/gitlab-runner:latest
```

---

## 7. Monitoring & Logging

### 7.1 Prometheus + Grafana

**Docker Installation:**

```bash
# Prometheus
docker run -d -p 9090:9090 --name prometheus prom/prometheus

# Grafana
docker run -d -p 3000:3000 --name grafana grafana/grafana
```

| Tool | Default URL | Default Login |
|------|-------------|---------------|
| Prometheus | <http://localhost:9090> | N/A |
| Grafana | <http://localhost:3000> | admin/admin |

---

## 8. Cloud CLIs

### 8.1 AWS CLI

| Info | Link |
|------|------|
| **Download** | [aws.amazon.com/cli](https://aws.amazon.com/cli/) |

**Installation:**

```bash
pip install awscli
```

**Configure:**

```bash
aws configure
```

### 8.2 Azure CLI

| Info | Link |
|------|------|
| **Download** | [docs.microsoft.com](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) |

### 8.3 Google Cloud CLI

| Info | Link |
|------|------|
| **Download** | [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install) |

---

## 9. Utilities

### 9.1 jq (JSON processor)

```bash
# Windows
choco install jq

# macOS
brew install jq

# Linux
sudo apt install jq
```

### 9.2 yq (YAML processor)

```bash
# macOS
brew install yq

# Linux/pip
pip install yq
```

### 9.3 curl & wget

```bash
# Usually pre-installed on Linux/macOS
# Windows
choco install curl wget
```

---

## ✅ Installation Checklist (Danh sách cần cài đặt)

### Track 1 Requirements (Yêu cầu Track 1)

- [ ] WSL2 (Windows only)
- [ ] Docker Desktop
- [ ] Git
- [ ] VS Code + Extensions
- [ ] GitLab/GitHub account (Tài khoản GitLab/GitHub)

### Track 2 Requirements (Yêu cầu Track 2)

- [ ] kubectl
- [ ] Minikube or Kind
- [ ] Helm

### Track 3 Requirements (Yêu cầu Track 3)

- [ ] Terraform
- [ ] Ansible
- [ ] AWS CLI (with Free Tier account)

### Track 4 Requirements (Yêu cầu Track 4)

- [ ] Trivy (`brew install trivy` or `choco install trivy`)
- [ ] SonarQube (Docker)

---

*Last Updated: 2025-12-30*

*Cập nhật lần cuối: 2025-12-30*
