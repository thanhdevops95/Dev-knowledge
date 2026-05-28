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

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You are working on a website with 3 other developers. You all edit the `index.html` file at the same time. When you save, you overwrite their changes. Then, a bug appears, but you don't know who wrote the bad code or when.
>
> *Bạn làm việc trên website cùng 3 developer khác. Tất cả cùng sửa file `index.html`. Khi bạn lưu, bạn ghi đè code của họ. Rồi lỗi xuất hiện, nhưng bạn không biết ai viết code lỗi hay khi nào.*
>
> **Git solves this by tracking every single change and merging work updates intelligently!**
>
> *Git giải quyết bằng cách theo dõi từng thay đổi nhỏ và gộp code thông minh!*

| Before Git | After Git |
|------------|-----------|
| ❌ Overwrite each other's code *(Ghi đè code của nhau)* | ✅ Merge work cleanly *(Gộp code gọn gàng)* |
| ❌ "Final_v1.zip", "Final_v2.zip" | ✅ `git commit`, `git tag` (clean history) |
| ❌ No undo button for files | ✅ Revert to any previous version *(Quay lại bất kỳ bản cũ nào)* |

- **What is it? (Là gì?)**:
  - A Distributed Version Control System (DVCS) that tracks changes in source code over time.
  - Industry standard for source code management.
  - *Hệ thống quản lý phiên bản phân tán, giúp theo dõi mọi thay đổi trong mã nguồn.*

- **Why learn it? (Tại sao học?)**:
  - **Collaboration**: Multiple people work on the same project seamlessly.
  - **History**: Know exactly who changed what, when, and why.
  - *Hợp tác mượt mà và quản lý lịch sử code chi tiết.*

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
> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You try to write code in Notepad or TextEdit. You have no syntax highlighting, no auto-complete, and no way to run the code easily. You spend hours finding a missing bracket `}` or a typo in a variable name.
>
> *Bạn viết code bằng Notepad hay TextEdit. Không có tô màu cú pháp, không gợi ý code, không chạy code được. Bạn tốn hàng giờ tìm dấu đóng ngoặc `}` bị thiếu hay lỗi chính tả tên biến.*
>
> **VS Code provides a smart coding environment with highlighting, auto-complete, and integrated tools!**
>
> *VS Code cung cấp môi trường code thông minh với tô màu, gợi ý, và công cụ tích hợp sẵn!*

| Before VS Code | After VS Code |
|----------------|---------------|
| ❌ Plain text, hard to read *(Chữ thường, khó đọc)* | ✅ Colorful, easy to read *(Đầy màu sắc, dễ đọc)* |
| ❌ Type every command manually | ✅ Auto-complete & Suggestions *(Gợi ý thông minh)* |
| ❌ Switch windows to run git/terminal | ✅ Integrated Terminal & Git *(Terminal & Git tích hợp)* |

- **What is it? (Là gì?)**:
  - A powerful source-code editor that runs on desktop.
  - Developed by Microsoft, open-source and free.
  - *Trình biên tập mã nguồn mạnh mẽ, đa nền tảng, do Microsoft phát triển.*

- **Why learn it? (Tại sao học?)**:
  - Huge ecosystem of extensions (Docker, K8s, Python, etc.).
  - Highly customizable and fast.
  - *Hệ sinh thái Extensions khổng lồ hỗ trợ mọi công cụ DevOps.*

- **Website**: <https://code.visualstudio.com/>
- **Recommended Extensions (Extensions khuyến nghị)**:
  - Docker
  - Remote - SSH
  - YAML
  - GitLens

#### 3. Docker

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You develop an app on your MacBook. It works perfectly. You send it to your colleague who uses Windows. They can't run it because of missing libraries or version conflicts. You both spend 3 days just fixing setup issues.
>
> *Bạn viết app trên MacBook. Chạy ngon lành. Bạn gửi cho đồng nghiệp dùng Windows. Họ không chạy được vì thiếu thư viện hoặc lệch phiên bản. Hai người mất 3 ngày chỉ để sửa lỗi cài đặt.*
>
> **Docker allows you to package the app with everything it needs, so it runs the same everywhere!**
>
> *Docker cho phép đóng gói app cùng mọi thứ cần thiết, nên nó chạy giống hệt nhau ở mọi nơi!*

| Before Docker | After Docker |
|---------------|--------------|
| ❌ "It works on my machine" *(Nó chạy trên máy tôi mà)* | ✅ Works everywhere exactly the same *(Chạy giống hệt nhau mọi nơi)* |
| ❌ Complex setup instructions | ✅ `docker run` (one command) |
| ❌ Version conflicts (Python 2 vs 3) | ✅ Isolated environments *(Môi trường cô lập)* |

- **What is it? (Là gì?)**:
  - An open platform for developing, shipping, and running applications in **containers**.
  - Separates applications from infrastructure.
  - *Nền tảng mở để phát triển và chạy ứng dụng trong các containers.*

- **Why learn it? (Tại sao học?)**:
  - **Standardization**: Eliminates environment inconsistencies.
  - **Efficiency**: Lightweight and fast startup.
  - *Loại bỏ vấn đề sai lệch môi trường.*

- **Website**: <https://www.docker.com/>
- **Verify Installation (Kiểm tra cài đặt)**:

  ```bash
  docker run hello-world
  ```

#### 4. NGINX

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You have a website running on a Node.js server. Suddenly, 10,000 users visit at once. The server crashes because it can't handle so many connections. Also, hackers try to attack your direct IP.
>
> *Bạn có website chạy trên server Node.js. Đột nhiên 10.000 người vào cùng lúc. Server sập vì không chịu nổi tải. Ngoài ra, hacker cố tấn công trực tiếp vào IP của bạn.*
>
> **NGINX acts as a shield and traffic manager, handling millions of connections efficiently!**
>
> *NGINX đóng vai trò tấm khiên và người điều phối giao thông, xử lý hàng triệu kết nối hiệu quả!*

| Before NGINX | After NGINX |
|--------------|-------------|
| ❌ Slow, easily crashes under load | ✅ High performance, load balancing |
| ❌ Direct exposure to internet | ✅ Reverse proxy security |
| ❌ Difficult to serve static files | ✅ Serves static content incredibly fast |

- **What is it? (Là gì?)**:
  - High-performance HTTP web server, reverse proxy, and load balancer.
  - *Web server hiệu năng cao, proxy ngược và cân bằng tải.*

- **Why learn it? (Tại sao học?)**:
  - **Popularity**: Most widely used web server.
  - **Performance**: Handles high concurrency with low memory.
  - *Web server phổ biến nhất, chịu tải cao với ít tài nguyên.*

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

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You have a Kubernetes cluster in the cloud. How do you talk to it? How do you tell it to run your app, or check logs? You can't just SSH into every server.
>
> *Bạn có một cluster K8s trên mây. Làm sao nói chuyện với nó? Làm sao bảo nó chạy app hay xem log? Bạn không thể SSH vào từng server được.*
>
> **kubectl is your universal remote control for Kubernetes!**
>
> *kubectl là điều khiển từ xa vạn năng cho Kubernetes!*

| Before kubectl | After kubectl |
|----------------|---------------|
| ❌ Login to each server manually | ✅ One tool to control entire cluster |
| ❌ Complex API calls | ✅ Simple commands: `kubectl apply`, `kubectl get` |

- **What is it?**: Official CLI to interact with Kubernetes.
- **Why learn it?**: Essential for managing K8s clusters.
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

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You want to learn Kubernetes. Cloud clusters cost $100/month. You don't want to pay that just to learn.
>
> *Bạn muốn học Kubernetes. Cluster trên cloud tốn $100/tháng. Bạn không muốn trả tiền đó chỉ để học.*
>
> **Minikube creates a real Kubernetes cluster right inside your laptop for FREE!**
>
> *Minikube tạo một cluster K8s thật ngay trong laptop của bạn MIỄN PHÍ!*

| Before Minikube | After Minikube |
|-----------------|----------------|
| ❌ Expensive cloud bills | ✅ Free local learning environment |
| ❌ Complex setup requiring 3+ servers | ✅ One command: `minikube start` |

- **What is it?**: Runs Kubernetes single-node locally.
- **Why learn it?**: Learn K8s without cloud costs.
- **Website**: <https://minikube.sigs.k8s.io/>
- **Start (Khởi động)**:

  ```bash
  minikube start --driver=docker
  ```

#### 3. Helm

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> To install an app on Kubernetes, you have to write 10 different YAML files manually. If you want to change one setting (like password), you have to edit all files. It's a nightmare.
>
> *Để cài app trên K8s, bạn phải viết 10 file YAML thủ công. Muốn đổi một setting (như password), bạn phải sửa tất cả file. Thật là ác mộng.*
>
> **Helm allows you to install complex apps with ONE command, like an App Store for K8s!**
>
> *Helm cho phép cài app phức tạp chỉ với MỘT lệnh, giống như App Store cho K8s!*

| Before Helm | After Helm |
|-------------|------------|
| ❌ Write 10 YAML files manually | ✅ `helm install my-app` |
| ❌ Hard to share or reuse configurations | ✅ Share Charts easily |
| ❌ Update manually file by file | ✅ `helm upgrade` in seconds |

- **What is it?**: Package manager for Kubernetes.
- **Why learn it?**: Install complex applications instantly.
- **Website**: <https://helm.sh/>
- **Example (Ví dụ)**:

  ```bash
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm install my-nginx bitnami/nginx
  ```

#### 4. Jenkins

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> A developer pushes code. They forget to run tests. The code breaks the production site. You have to manually ssh to the server, pull code, build, and restart. You do this 5 times a day.
>
> *Dev push code. Họ quên chạy test. Code làm sập trang production. Bạn phải thủ công ssh vào server, pull code, build, và restart. Bạn làm việc này 5 lần mỗi ngày.*
>
> **Jenkins automates ALL of this. Code pushed -> Jenkins builds -> Tests -> Deploys automatically!**
>
> *Jenkins tự động hóa TẤT CẢ. Có code mới -> Jenkins build -> Test -> Deploy tự động!*

| Before Jenkins | After Jenkins |
|----------------|---------------|
| ❌ Manual deployment, prone to error | ✅ 100% Automated |
| ❌ Slow feedback (find bugs next week) | ✅ Instant feedback (find bugs in minutes) |
| ❌ "Works on my machine" | ✅ Consistent build environment |

- **What is it? (Là gì?)**:
  - Leading open-source automation server.
  - *Máy chủ tự động hóa mã nguồn mở hàng đầu.*

- **Why learn it? (Tại sao học?)**:
  - Long-standing industry standard for CI/CD.
  - *Tiêu chuẩn công nghiệp lâu đời cho CI/CD.*

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

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You need to create 50 servers on AWS, then set up networks and firewalls. Doing this by clicking in the AWS Console takes days and is prone to mistakes.
>
> *Bạn cần tạo 50 server trên AWS, rồi thiết lập mạng và tường lửa. Làm thủ công bằng cách click trên AWS Console mất cả ngày và dễ sai sót.*
>
> **Terraform allows you to define your entire infrastructure as CODE. Create, update, destroy 50 servers in minutes!**
>
> *Terraform cho phép bạn định nghĩa toàn bộ hạ tầng bằng CODE. Tạo, cập nhật, xóa 50 server trong vài phút!*

| Before Terraform | After Terraform |
|------------------|-----------------|
| ❌ "ClickOps" - manual user interface actions | ✅ Infrastructure as Code (IaC) |
| ❌ Impossible to track changes history | ✅ Git history for infrastructure |
| ❌ Hard to replicate environments | ✅ Copy-paste code to creating Staging/Prod |

- **What is it? (Là gì?)**:
  - Open-source Infrastructure as Code (IaC) tool.
  - *Công cụ IaC mã nguồn mở.*

- **Why learn it? (Tại sao học?)**:
  - **Cloud Agnostic**: Manage AWS, Azure, GCP with one tool.
  - Automates lifecycle of infrastructure.
  - *Quản lý đa cloud (AWS, Azure, GCP) với cùng một công cụ.*

- **Website**: <https://www.terraform.io/>
- **Basic Workflow (Workflow cơ bản)**:

  ```bash
  terraform init    # Initialize (Khởi tạo)
  terraform plan    # Preview changes (Xem preview)
  terraform apply   # Apply changes (Áp dụng changes)
  terraform destroy # Destroy resources (Xóa resources)
  ```

#### 2. AWS CLI

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You want to upload a file to AWS S3 storage every day at midnight. You can't wake up to do it manually.
>
> *Bạn muốn upload file lên AWS S3 mỗi ngày lúc nửa đêm. Bạn không thể thức dậy để làm thủ công.*
>
> **AWS CLI allows you to write scripts to interact with AWS automatically!**
>
> *AWS CLI cho phép bạn viết script để tương tác với AWS tự động!*

- **What is it?**: Command line interface for Amazon Web Services.
- **Why learn it?**: Automate AWS operations instead of using the Console.
- **Website**: <https://aws.amazon.com/cli/>
- **Configuration (Cấu hình)**:

  ```bash
  aws configure
  # Enter: Access Key, Secret Key, Region, Output format
  # (Nhập: Access Key, Secret Key, Region, Output format)
  ```

#### 3. Ansible

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You have 100 servers. You need to update Linux and install Nginx on ALL of them. Logging into each one would take a week.
>
> *Bạn có 100 server. Bạn cần update Linux và cài Nginx trên TẤT CẢ. Đăng nhập vào từng máy sẽ mất cả tuần.*
>
> **Ansible allows you to push configuration to 100 servers at once!**
>
> *Ansible cho phép bạn đẩy cấu hình xuống 100 server cùng lúc!*

| Before Ansible | After Ansible |
|----------------|---------------|
| ❌ SSH into each server manually | ✅ Run one playbook for all servers |
| ❌ Inconsistent configurations (Snowflake servers) | ✅ Identical configuration everywhere |

- **What is it? (Là gì?)**:
  - Open-source IT automation and configuration management tool.
  - Agentless - connects via SSH.
  - *Công cụ tự động hóa và quản lý cấu hình, không cần agent.*

- **Why learn it? (Tại sao học?)**:
  - **Simple**: Uses YAML playbooks.
  - **Powerful**: Manage complex multi-tier deployments.
  - *Đơn giản (YAML) và mạnh mẽ.*

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

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You deploy a container to production. A hacker finds an old vulnerability in the OS library you used and hacks your server. You didn't know because you never scanned it.
>
> *Bạn deploy container lên production. Hacker tìm thấy lỗ hổng cũ trong thư viện OS bạn dùng và hack server. Bạn không biết vì chưa bao giờ quét nó.*
>
> **Trivy scans your containers and code to find known vulnerabilities before hackers do!**
>
> *Trivy quét container và code của bạn để tìm lỗ hổng đã biết trước khi hacker tìm ra!*

- **What is it?**: Vulnerability scanner for containers and IaC.
- **Why learn it?**: Find CVEs (Common Vulnerabilities and Exposures) early.
- **Website**: <https://trivy.dev/>
- **Scan image (Quét image)**:

  ```bash
  trivy image nginx:latest
  ```

#### 2. Hadolint

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You write a Dockerfile. You run `apt-get install` but forget to clean up the cache. Your image is 1GB instead of 100MB.
>
> *Bạn viết Dockerfile. Bạn chạy `apt-get install` nhưng quên dọn dẹp cache. Image của bạn nặng 1GB thay vì 100MB.*
>
> **Hadolint checks your Dockerfile against best practices to ensure it is small, safe, and efficient!**
>
> *Hadolint kiểm tra Dockerfile theo các quy chuẩn tốt nhất để đảm bảo nó nhỏ gọn, an toàn và hiệu quả!*

- **What is it?**: Dockerfile linter following best practices.
- **Why learn it?**: Write safe and optimized Dockerfiles.
- **Website**: <https://github.com/hadolint/hadolint>
- **Usage (Sử dụng)**:

  ```bash
  hadolint Dockerfile
  ```

#### 3. OWASP ZAP

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You built a login form. You didn't realize it is vulnerable to SQL Injection. A teenager deletes your entire database by typing a weird username.
>
> *Bạn xây dựng form đăng nhập. Bạn không biết nó bị lỗi SQL Injection. Một cậu thiếu niên xóa sạch database của bạn bằng các nhập username lạ.*
>
> **OWASP ZAP automatically attacks your website to find security holes so you can fix them!**
>
> *OWASP ZAP tự động tấn công website của bạn để tìm lỗ hổng bảo mật giúp bạn sửa chữa!*

- **What is it?**: Web application security scanner.
- **Why learn it?**: Find security vulnerabilities in web apps.
- **Website**: <https://www.zaproxy.org/>

---

---

## ✅ Checkpoint

> ✅ **Checkpoint - Before continuing, make sure you understand:**
> *(Trước khi tiếp tục, hãy chắc chắn bạn hiểu:)*
>
> - [ ] Why do we need Git for collaboration? *(Tại sao cần Git để hợp tác?)*
> - [ ] How does Docker solve "It works on my machine"? *(Docker giải quyết vấn đề "chạy trên máy tôi" như thế nào?)*
> - [ ] What is the difference between VS Code and Notepad? *(Khác biệt giữa VS Code và Notepad là gì?)*
> - [ ] When to use Terraform instead of AWS Console? *(Khi nào dùng Terraform thay vì AWS Console?)*
>
> *If you can't answer, please re-read the sections above!*

---

## ⚠️ Common Mistakes (Lỗi thường gặp)

> ⚠️ **Mistakes beginners often make when choosing tools:**
>
> | Mistake | Problem | Solution |
> |---------|---------|----------|
> | **Installing everything at once** | Overwhelmed, conflicts | **Install ONE Track at a time** *(Cài từng Track một)* |
> | **Skipping Verification** | Tools don't work later | **Run verify command immediately** *(Chạy lệnh kiểm tra ngay)* |
> | **Using old versions** | Missing features, bugs | **Use versions specified in tables** *(Dùng version được chỉ định)* |
> | **Not using Docker** | "It works on my machine" | **Prefer Docker-based tools** *(Ưu tiên tool chạy trên Docker)* |

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
