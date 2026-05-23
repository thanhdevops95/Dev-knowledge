# 🛠️ Tools Overview (Tổng Quan Công Cụ DevOps)

> **Overview of all tools needed for each Track**
>
> *Hướng dẫn tổng quan tất cả tools cần thiết cho từng Track*

---

## 📋 Table of Contents (Mục lục)

1. [Tools Summary Table](#tools-summary-table-bảng-tổng-hợp-tools)
2. [Track 1: Foundation & Static Web](#-track-1-foundation--static-web)
3. [Track 2: Orchestration & Automation](#-track-2-orchestration--automation)
4. [Track 3: Cloud, Network & Design](#-track-3-cloud-network--design)
5. [Track 4: DevSecOps](#-track-4-devsecops)

---

## Tools Summary Table (Bảng tổng hợp Tools)

| Tool | Track 1 | Track 2 | Track 3 | Track 4 | Description (Mô tả) |
|------|:-------:|:-------:|:-------:|:-------:|---------------------|
| WSL2 (Windows) | ✅ | - | - | - | Linux subsystem for Windows *(Hệ thống con Linux cho Windows)* |
| Homebrew (macOS) | ✅ | - | - | - | Package manager for macOS *(Package manager cho macOS)* |
| Git | ✅ | - | - | - | Version control *(Quản lý phiên bản)* |
| VS Code | ✅ | - | - | - | Code editor *(Trình soạn thảo code)* |
| Docker | ✅ | - | - | - | Container runtime *(Môi trường chạy container)* |
| Docker Compose | ✅ | - | - | - | Multi-container orchestration *(Điều phối đa container)* |
| NGINX | ✅ | - | - | - | Web server |
| Node.js | ✅ | - | - | - | JavaScript runtime (optional) |
| kubectl | - | ✅ | - | - | Kubernetes CLI |
| Minikube/Kind | - | ✅ | - | - | Local Kubernetes |
| Helm | - | ✅ | - | - | K8s package manager |
| Jenkins | - | ✅ | - | - | CI/CD server |
| Terraform | - | - | ✅ | - | Infrastructure as Code |
| AWS CLI | - | - | ✅ | - | AWS command line |
| Ansible | - | - | ✅ | - | Configuration management *(Quản lý cấu hình)* |
| Trivy | - | - | - | ✅ | Container vulnerability scanner *(Quét lỗ hổng container)* |
| Hadolint | - | - | - | ✅ | Dockerfile linter |
| OWASP ZAP | - | - | - | ✅ | Web app security scanner *(Quét bảo mật web app)* |

---

## 🔵 Track 1: Foundation & Static Web

### Tools List (Danh sách Tools)

| # | Tool | Version | Check Command (Lệnh kiểm tra) | Expected Output (Output mong đợi) |
|---|------|---------|-------------------------------|-----------------------------------|
| 1 | WSL2 (Windows) | 2.x | `wsl --version` | `WSL version: 2.x.x` |
| 2 | Git | 2.40+ | `git --version` | `git version 2.4x.x` |
| 3 | VS Code | Latest | `code --version` | `1.8x.x` |
| 4 | Docker | 24.0+ | `docker --version` | `Docker version 24.x.x` |
| 5 | Docker Compose | 2.20+ | `docker compose version` | `v2.2x.x` |
| 6 | NGINX | Latest | `docker run --rm nginx:alpine nginx -v` | `nginx/1.2x.x` |

### Tool Details (Chi tiết từng Tool)

#### 1. Git

- **What is it? (Là gì?)**:
  - A Distributed Version Control System (DVCS) that tracks changes in source code over time.
  - Industry standard for source code management, from small personal projects to large open-source projects like Linux Kernel.
  - *Hệ thống quản lý phiên bản phân tán, giúp theo dõi mọi thay đổi trong mã nguồn theo thời gian.*

- **Why learn it? (Tại sao học?)**:
  - **Not just for DevOps**: Essential skill for all Developers, Testers, and DevOps Engineers.
  - **Collaboration**: Allows multiple people to work on the same project without overwriting each other's code.
  - **History Management**: Know exactly who changed what, when, and why. Easy to revert if there's a bug.
  - **Branching & Merging**: Develop features in separate branches without affecting main code.
  - *Không chỉ cho DevOps - kỹ năng bắt buộc cho mọi Developer, Tester, và DevOps Engineer.*

- **Website**: <https://git-scm.com/>
- **Quick Install (Cài đặt nhanh)**:

  ```bash
  # Windows (PowerShell Admin)
  winget install Git.Git
  
  # macOS
  brew install git
  
  # Linux (Ubuntu/Debian)
  sudo apt install git
  ```

#### 2. VS Code

- **What is it? (Là gì?)**:
  - A powerful source-code editor that runs on desktop and supports cross-platform (Windows, macOS, Linux).
  - Developed by Microsoft, open-source and free.
  - Supports IntelliSense, Debugging, and built-in Git integration.
  - *Trình biên tập mã nguồn mạnh mẽ, đa nền tảng, do Microsoft phát triển.*

- **Why learn it? (Tại sao học?)**:
  - Huge ecosystem of extensions supporting all DevOps languages and tools (Docker, Kubernetes, Terraform, Python, Go...).
  - Highly customizable with good performance.
  - *Hệ sinh thái Extensions khổng lồ hỗ trợ mọi ngôn ngữ và công cụ DevOps.*

- **Website**: <https://code.visualstudio.com/>
- **Recommended Extensions (Extensions khuyến nghị)**:
  - Docker
  - Remote - SSH
  - YAML
  - GitLens

#### 3. Docker

- **What is it? (Là gì?)**:
  - An open platform for developing, shipping, and running applications.
  - Uses OS-level virtualization to deliver software in packages called **containers**.
  - Separates applications from infrastructure for fast and consistent software delivery.
  - *Nền tảng mở để phát triển, vận chuyển và chạy ứng dụng trong các containers.*

- **Why learn it? (Tại sao học?)**:
  - **Standardization**: Eliminates "it works on my machine but not on server" problem.
  - **Efficiency**: Lightweight and starts much faster than Virtual Machines.
  - Foundation of most modern DevOps systems.
  - *Loại bỏ vấn đề "nó chạy trên máy tôi nhưng không chạy trên server".*

- **Website**: <https://www.docker.com/>
- **Verify Installation (Kiểm tra cài đặt)**:

  ```bash
  docker run hello-world
  ```

#### 4. NGINX

- **What is it? (Là gì?)**:
  - **NGINX** ("engine x") is an HTTP web server, reverse proxy, content cache, load balancer, TCP/UDP proxy server, and mail proxy server.
  - Known for its event-driven, asynchronous design, providing high performance and low resource consumption.
  - *Web server hiệu năng cao với thiết kế hướng sự kiện, không đồng bộ.*

- **Why learn it? (Tại sao học?)**:
  - Most popular web server in the world (according to Netcraft).
  - Plays a crucial role in security, load balancing, and speeding up modern web applications.
  - *Web server phổ biến nhất thế giới, quan trọng cho bảo mật và cân bằng tải.*

- **Website**: <https://nginx.org/>
- **Quick Run with Docker (Chạy nhanh với Docker)**:

  ```bash
  docker run -d -p 80:80 nginx:alpine
  ```

---

## 🟢 Track 2: Orchestration & Automation

### Additional Tools List (Danh sách Tools bổ sung)

| # | Tool | Version | Check Command (Lệnh kiểm tra) | Expected Output (Output mong đợi) |
|---|------|---------|-------------------------------|-----------------------------------|
| 1 | kubectl | 1.28+ | `kubectl version --client` | `v1.2x.x` |
| 2 | Minikube | 1.31+ | `minikube version` | `v1.3x.x` |
| 3 | Helm | 3.12+ | `helm version` | `v3.1x.x` |
| 4 | Jenkins | LTS | Docker container | - |

### Tool Details (Chi tiết từng Tool)

#### 1. kubectl

- **What is it?**: Official CLI to interact with Kubernetes *(CLI chính thức để tương tác với Kubernetes)*
- **Why learn it?**: Manage and debug K8s clusters *(Quản lý và debug K8s clusters)*
- **Website**: <https://kubernetes.io/docs/tasks/tools/>
- **Installation (Cài đặt)**:

  ```bash
  # Windows
  winget install Kubernetes.kubectl
  
  # macOS
  brew install kubectl
  
  # Linux
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  ```

#### 2. Minikube

- **What is it?**: Runs Kubernetes single-node locally *(Chạy Kubernetes single-node trên local)*
- **Why learn it?**: Learn K8s without needing a cloud account *(Học K8s mà không cần cloud account)*
- **Website**: <https://minikube.sigs.k8s.io/>
- **Start (Khởi động)**:

  ```bash
  minikube start --driver=docker
  ```

#### 3. Helm

- **What is it?**: Package manager for Kubernetes *(Package manager cho Kubernetes)*
- **Why learn it?**: Install complex applications with a single command *(Cài đặt ứng dụng phức tạp chỉ với 1 lệnh)*
- **Website**: <https://helm.sh/>
- **Example (Ví dụ)**:

  ```bash
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm install my-nginx bitnami/nginx
  ```

#### 4. Jenkins

- **What is it? (Là gì?)**:
  - Leading open-source automation server.
  - Provides hundreds of plugins to support building, deploying, and automating any project.
  - *Máy chủ tự động hóa mã nguồn mở hàng đầu với hàng trăm plugin.*

- **Why learn it? (Tại sao học?)**:
  - Long-standing industry standard for CI/CD (Continuous Integration/Continuous Delivery).
  - Extremely flexible thanks to plugin ecosystem and large community.
  - *Tiêu chuẩn công nghiệp lâu đời cho CI/CD, cực kỳ linh hoạt nhờ hệ sinh thái plugin.*

- **Website**: <https://www.jenkins.io/>
- **Run with Docker (Chạy với Docker)**:

  ```bash
  docker run -d -p 8080:8080 jenkins/jenkins:lts
  ```

---

## 🟡 Track 3: Cloud, Network & Design

### Additional Tools List (Danh sách Tools bổ sung)

| # | Tool | Version | Check Command (Lệnh kiểm tra) | Expected Output (Output mong đợi) |
|---|------|---------|-------------------------------|-----------------------------------|
| 1 | Terraform | 1.5+ | `terraform --version` | `v1.x.x` |
| 2 | AWS CLI | 2.x | `aws --version` | `aws-cli/2.x.x` |
| 3 | Ansible | 2.14+ | `ansible --version` | `ansible 2.1x.x` |

### Tool Details (Chi tiết từng Tool)

#### 1. Terraform

- **What is it? (Là gì?)**:
  - Open-source Infrastructure as Code (IaC) tool that helps define and provision data center infrastructure.
  - Uses a declarative configuration language called HCL (HashiCorp Configuration Language).
  - *Công cụ IaC mã nguồn mở giúp định nghĩa và cung cấp hạ tầng bằng ngôn ngữ khai báo HCL.*

- **Why learn it? (Tại sao học?)**:
  - **Cloud Agnostic**: Manage infrastructure across multiple cloud providers (AWS, Azure, GCP) with the same workflow.
  - Automates creation, modification, and destruction of infrastructure safely with version control.
  - *Quản lý hạ tầng trên nhiều cloud provider với cùng một workflow.*

- **Website**: <https://www.terraform.io/>
- **Basic Workflow (Workflow cơ bản)**:

  ```bash
  terraform init    # Initialize (Khởi tạo)
  terraform plan    # Preview changes (Xem preview)
  terraform apply   # Apply changes (Áp dụng changes)
  terraform destroy # Destroy resources (Xóa resources)
  ```

#### 2. AWS CLI

- **What is it?**: Command line interface for Amazon Web Services *(CLI cho Amazon Web Services)*
- **Why learn it?**: Automate AWS operations *(Tự động hóa AWS operations)*
- **Website**: <https://aws.amazon.com/cli/>
- **Configuration (Cấu hình)**:

  ```bash
  aws configure
  # Enter: Access Key, Secret Key, Region, Output format
  # (Nhập: Access Key, Secret Key, Region, Output format)
  ```

#### 3. Ansible

- **What is it? (Là gì?)**:
  - Open-source IT automation, configuration management, infrastructure provisioning, and application deployment tool.
  - Agentless - connects and executes via SSH (Linux) or WinRM (Windows).
  - *Công cụ tự động hóa CNTT, quản lý cấu hình, không cần cài agent.*

- **Why learn it? (Tại sao học?)**:
  - **Simple**: Uses easy-to-read YAML playbooks.
  - **Powerful**: Can manage complex systems, from servers to network devices.
  - *Sử dụng YAML playbook dễ đọc, có thể quản lý hệ thống phức tạp.*

- **Website**: <https://www.ansible.com/>

---

## 🔴 Track 4: DevSecOps

### Additional Tools List (Danh sách Tools bổ sung)

| # | Tool | Version | Check Command (Lệnh kiểm tra) | Expected Output (Output mong đợi) |
|---|------|---------|-------------------------------|-----------------------------------|
| 1 | Trivy | Latest | `trivy --version` | `Version: 0.x.x` |
| 2 | Hadolint | Latest | `hadolint --version` | `Haskell Dockerfile Linter` |
| 3 | OWASP ZAP | Latest | Docker container | - |

### Tool Details (Chi tiết từng Tool)

#### 1. Trivy

- **What is it?**: Vulnerability scanner for containers and IaC *(Quét lỗ hổng cho containers và IaC)*
- **Why learn it?**: Find CVEs in Docker images *(Tìm CVE trong Docker images)*
- **Website**: <https://trivy.dev/>
- **Scan image (Quét image)**:

  ```bash
  trivy image nginx:latest
  ```

#### 2. Hadolint

- **What is it?**: Dockerfile linter following best practices *(Linter Dockerfile theo best practices)*
- **Why learn it?**: Write safe and optimized Dockerfiles *(Viết Dockerfile an toàn và tối ưu)*
- **Website**: <https://github.com/hadolint/hadolint>
- **Usage (Sử dụng)**:

  ```bash
  hadolint Dockerfile
  ```

#### 3. OWASP ZAP

- **What is it?**: Web application security scanner *(Quét bảo mật ứng dụng web)*
- **Why learn it?**: Find security vulnerabilities in web apps *(Tìm lỗ hổng bảo mật trong web apps)*
- **Website**: <https://www.zaproxy.org/>

---

## 💡 Tips

### Recommended Installation Order (Thứ tự cài đặt khuyến nghị)

```
Track 1: Git → VS Code → Docker → Verify
    ↓
Track 2: kubectl → Minikube → Helm → Jenkins → Verify
    ↓
Track 3: Terraform → AWS CLI → Ansible → Verify
    ↓
Track 4: Trivy → Hadolint → OWASP ZAP → Verify
```

### Important Notes (Lưu ý quan trọng)

1. **Install by track** - Don't need to install all tools from the start *(Không cần cài tất cả tools từ đầu)*
2. **Verify after each install** - Run verify script to ensure tools work *(Chạy script verify để đảm bảo tools hoạt động)*
3. **Docker-first** - Many tools can run in Docker containers instead of local install *(Nhiều tools có thể chạy trong Docker thay vì cài local)*

---

## 🔗 Navigation

[⬅️ README](./README.md) | [Windows Setup](./WINDOWS_SETUP.md) | [Troubleshooting ➡️](./TROUBLESHOOTING.md)

---

*Last Updated: 2026-01-16*

*Cập nhật lần cuối: 2026-01-16*
