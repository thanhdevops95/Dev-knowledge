# 🚀 DevOps Journey

[![GitHub](https://img.shields.io/badge/GitHub-DevOps--Journey-blue?style=flat-square&logo=github)](https://github.com/thanhlehoang0107/DevOps-Journey)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

> **From Zero to DevOps Engineer** - Comprehensive learning path with hands-on labs, real projects, and industry best practices.
>
> *Hành trình từ Zero đến DevOps Engineer - Lộ trình học tập toàn diện với labs thực hành, projects thực tế và best practices.*
>
> 🚀 **Refined Edition 2026:** Enhanced with Deep Dive Mechanics, Golang, and Platform Engineering.

---

## 📋 Table of Contents (Mục Lục)

- [What is DevOps?](#-what-is-devops-devops-là-gì)
- [Introduction](#-introduction-giới-thiệu)
- [Prerequisites](#-prerequisites-yêu-cầu)
- [Roadmap Structure](#-roadmap-structure-cấu-trúc)
- [Track Details](#-track-details-chi-tiết-các-track)
- [Quick Start](#-quick-start)
- [Contributing](#-contributing-đóng-góp)

---

## 🤔 What is DevOps? (DevOps là gì?)

### Definition (Định nghĩa)

**DevOps** is the combination of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity. DevOps is short for **Dev**elopment and **Op**eration**s**.

*DevOps là sự kết hợp giữa nhiều triết lý văn hóa, biện pháp thực hành và công cụ giúp tăng khả năng phân phối ứng dụng và dịch vụ của một tổ chức ở tốc độ cao. DevOps là viết tắt của **Dev**elopment (Phát triển) và **Op**eration**s** (Vận hành).*

### How it Works (Cách thức hoạt động)

In the DevOps model, **Development (Dev)** and **Operations (Ops)** teams are no longer siloed. They are merged into a single team where engineers work across the **entire application lifecycle**—from development, testing, deployment to operations.

*Trong mô hình DevOps, các nhóm phát triển (Dev) và vận hành (Ops) không còn bị tách rời. Họ được hợp nhất thành một nhóm duy nhất, trong đó các kỹ sư làm việc với toàn bộ vòng đời của ứng dụng.*

```
┌───────────────────────────────────────────────────────────────────┐
│                    DEVOPS LIFECYCLE (Vòng đời DevOps)              │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│        PLAN → CODE → BUILD → TEST → RELEASE → DEPLOY → OPERATE   │
│          ▲                                                    │    │
│          └────────────────── MONITOR ◄────────────────────┘    │
│                                                                    │
│   [DEV]─────────────────────────────────────────────────────[OPS] │
│         Merged into a Continuous Process (Kết hợp quy trình)      │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

### Why DevOps Matters (Tại sao DevOps lại quan trọng?)

Software has become an integral part of every business. Companies must change how they develop and deliver software to:

*Phần mềm đã trở thành một phần không thể tách rời trong mọi doanh nghiệp. Các công ty cần phải thay đổi cách phát triển và phân phối phần mềm để:*

- **Respond to customer needs faster** (Đáp ứng nhu cầu khách hàng nhanh hơn).
- **Compete more effectively** (Cạnh tranh hiệu quả hơn trên thị trường).
- **Release new features and bug fixes quickly** (Phát hành các tính năng mới và sửa lỗi nhanh chóng).

### Benefits of DevOps (Lợi ích của DevOps)

| Benefit (Lợi ích) | Description (Mô tả) |
|-------------------|----------------------|
| 🚀 **Speed (Tốc độ)** | Allows teams to improve products faster, adapt better to the market. *(Cho phép các nhóm cải tiến sản phẩm nhanh hơn.)* |
| 📦 **Rapid Delivery (Phân phối nhanh)** | Increase frequency and pace of releases. *(Tăng tần suất và nhịp độ phát hành.)* |
| ✅ **Reliability (Độ tin cậy)** | Ensure quality with CI/CD, monitoring, and logging. *(Đảm bảo chất lượng bằng CI/CD, giám sát và ghi log.)* |
| 📈 **Scale (Quy mô)** | Automation enables efficient management of complex systems. *(Tự động hóa giúp quản lý hiệu quả.)* |
| 🤝 **Collaboration (Cộng tác)** | Dev and Ops teams collaborate closely. *(Các nhóm Dev và Ops cộng tác chặt chẽ.)* |
| 🔒 **Security (Bảo mật)** | Integrate security into the process (DevSecOps). *(Tích hợp bảo mật vào quy trình.)* |

### Key DevOps Practices (Các phương pháp thực hành DevOps chính)

1. **Continuous Integration (CI):** Developers frequently merge code to the main repository; automated builds and tests run to find bugs early.
   *(Tích hợp liên tục: Các developer thường xuyên merge code về repository chính.)*
2. **Continuous Delivery/Deployment (CD):** Every change that passes tests is automatically deployed to staging or production.
   *(Phân phối liên tục: Mọi thay đổi được duyệt qua test sẽ tự động được triển khai.)*
3. **Infrastructure as Code (IaC):** Manage infrastructure using code (Terraform, Ansible) instead of manual operations.
   *(Cơ sở hạ tầng dưới dạng mã: Quản lý hạ tầng bằng code thay vì thao tác thủ công.)*
4. **Monitoring & Logging:** Track application and infrastructure performance in real-time.
   *(Giám sát và ghi log: Theo dõi hiệu năng ứng dụng và hạ tầng trong thời gian thực.)*

---

## 🎯 Introduction (Giới Thiệu)

**DevOps Journey** is a comprehensive DevOps learning path, designed for:

*Lộ trình học tập DevOps toàn diện, được thiết kế cho:*

- 🌱 **Beginners** - No IT experience (Người mới bắt đầu)
- 💻 **Developers** - Want to transition to DevOps (Developer muốn chuyển sang DevOps)
- 🔧 **SysAdmins** - Want to improve automation skills (SysAdmin muốn nâng cao kỹ năng)
- 📈 **DevOps Engineers** - Want to strengthen knowledge (Muốn củng cố kiến thức)

### ✨ Key Features (Điểm Nổi Bật)

- 🦀 **Modern Tech Stack**: Added Golang & GitOps (Cập nhật công nghệ mới).
- 🇻🇳 **Professional Bilingual**: Optimized Vietnamese/English terminology (Song ngữ chuyên ngành).

| Feature | Description |
|---------|-------------|
| 📚 **5 Tracks** | From Foundation to Career Path (Từ nền tảng đến sự nghiệp) |
| 🔬 **Hands-on Labs** | Step-by-step practical exercises (Bài thực hành chi tiết) |
| 🎯 **Capstone Projects** | Real-world projects per Track (Dự án tổng hợp) |
| 📝 **Quizzes** | Knowledge checks (Kiểm tra kiến thức) |
| 📖 **Cheatsheets** | Quick reference guides (Tài liệu tra cứu nhanh) |
| 🛠️ **Real-world Tools** | Docker, Kubernetes, Terraform, AWS... |

---

## 📋 Prerequisites (Yêu Cầu Tiên Quyết)

Before starting, you need to prepare (Trước khi bắt đầu, bạn cần chuẩn bị):

### Hardware (Phần Cứng)

- **RAM**: Minimum 8GB, recommended 16GB (Tối thiểu 8GB, khuyến nghị 16GB)
- **Storage**: 50GB free space (50GB trống)
- **CPU**: 4 cores or more (4 cores trở lên)

### Software (Phần Mềm)

- **OS**: Windows 10/11, macOS, or Linux
- **Git**: Installed and configured (Đã cài đặt và cấu hình)
- **Docker Desktop**: Installed (Đã cài đặt)
- **Code Editor**: VS Code (recommended)
- **Terminal**: PowerShell, Bash, or Zsh

### Accounts (Tài Khoản)

- **GitLab Account** (Primary): Created with SSH configured (Đã tạo và cấu hình SSH)
- **GitHub Account** (Optional): Alternative platform (Nền tảng thay thế)
- **Docker Hub Account**: For push/pull images (Để push/pull images)
- **AWS Free Tier** (Track 3+): For cloud practice (Để thực hành cloud)

👉 **[View detailed setup guide → (Xem hướng dẫn chi tiết)](./Track0_Setup_Environment/README.md)**

---

## 🗺️ Roadmap Structure (Cấu Trúc Lộ Trình)

```
DevOps-Journey/
├── 📁 Track0_Setup_Environment/      # Environment setup guide (Hướng dẫn cài đặt)
│
├── 📁 Track1_Foundation_StaticWeb/    # 🏗️ Foundation & Static Web (Nền tảng)
│   ├── 1.1_Linux_Bash/
│   ├── 1.2_Python_Basics/
│   ├── 1.3_Network_Basics/
│   ├── 1.4_Git_GitLab/
│   ├── 1.5_Docker_Fundamentals/
│   ├── 1.6_NGINX_Basic/
│   ├── 1.7_CICD_Basic/
│   └── 1.8_Capstone_Project/
│
├── 📁 Track2_Orchestration_Automation/ # ⚙️ Orchestration & Automation
│   ├── 2.1_Docker_Advanced/
│   ├── 2.2_Docker_Compose/
│   ├── 2.3_Jenkins/
│   ├── 2.4_Kubernetes_Core/
│   ├── 2.5_Monitoring_Logging/
│   └── 2.6_Capstone_Project/
│
├── 📁 Track3_Cloud_Network_Design/    # ☁️ Cloud & Infrastructure
│   ├── 3.1_Network_Advanced/
│   ├── 3.2_AWS_Core_Services/
│   ├── 3.3_Databases_for_DevOps/
│   ├── 3.4_Config_Management_Ansible/
│   ├── 3.5_Terraform_IaC/
│   ├── 3.6_System_Design_Reliability/
│   └── 3.7_Capstone_Project/
│
├── 📁 Track4_DevSecOps/               # 🔐 Security
│   ├── 4.1_Security_in_Pipeline/
│   ├── 4.2_Infra_Security/
│   └── 4.3_Capstone_Project/
│
└── 📁 Track5_Career_Path/             # 🎓 Career & Certification
    ├── 5.1_Certifications/
    ├── 5.2_Interview_Prep/
    ├── 5.3_Portfolio_Launch/
    └── 5.4_Grand_Capstone/
```

---

## 📚 Track Details (Chi Tiết Các Track)

### 🏗️ Track 1: Foundation & Static Web
>
> **Duration (Thời gian)**: 4-6 weeks | **Level**: Beginner

Build solid foundation with Linux, Git, Docker and basic CI/CD.

*Xây dựng nền tảng vững chắc với Linux, Git, Docker và CI/CD cơ bản.*

| Module | Content | Duration |
|--------|---------|----------|
| [1.1 Linux & Bash](./Track1_Foundation_StaticWeb/1.1_Linux_Bash/) | Linux OS, Bash scripting | 1 week |
| [1.2 Python Basics](./Track1_Foundation_StaticWeb/1.2_Python_Basics/) | Python for DevOps automation | 1 week |
| [1.3 Network Basics](./Track1_Foundation_StaticWeb/1.3_Network_Basics/) | TCP/IP, DNS, HTTP, OSI model | 3-4 days |
| [1.4 Git & GitLab](./Track1_Foundation_StaticWeb/1.4_Git_GitLab/) | Version control, branching, Git flow | 1 week |
| [1.5 Docker Fundamentals](./Track1_Foundation_StaticWeb/1.5_Docker_Fundamentals/) | Container, Dockerfile, Images | 1 week |
| [1.6 NGINX Basic](./Track1_Foundation_StaticWeb/1.6_NGINX_Basic/) | Web server, reverse proxy | 3-4 days |
| [1.7 CI/CD Basic](./Track1_Foundation_StaticWeb/1.7_CICD_Basic/) | GitLab CI/CD fundamentals | 1 week |
| [1.8 Capstone](./Track1_Foundation_StaticWeb/1.8_Capstone_Project/) | Deploy Static Website with CI/CD | 3-4 days |

👉 **[Start Track 1 → (Bắt đầu Track 1)](./Track1_Foundation_StaticWeb/README.md)**

---

### ⚙️ Track 2: Orchestration & Automation
>
> **Duration (Thời gian)**: 6-8 weeks | **Level**: Intermediate

Level up skills with Docker Compose, Kubernetes and monitoring.

*Nâng cao kỹ năng với Docker Compose, Kubernetes và monitoring.*

| Module | Content | Duration |
|--------|---------|----------|
| [2.1 Docker Advanced](./Track2_Orchestration_Automation/2.1_Docker_Advanced/) | Multi-stage builds, optimization | 1 week |
| [2.2 Docker Compose](./Track2_Orchestration_Automation/2.2_Docker_Compose/) | Multi-container applications | 1 week |
| [2.3 Jenkins](./Track2_Orchestration_Automation/2.3_Jenkins/) | CI/CD pipelines with Jenkins | 1-2 weeks |
| [2.4 Kubernetes Core](./Track2_Orchestration_Automation/2.4_Kubernetes_Core/) | K8s fundamentals, deployments | 2 weeks |
| [2.5 Monitoring & Logging](./Track2_Orchestration_Automation/2.5_Monitoring_Logging/) | Prometheus, Grafana, ELK | 1-2 weeks |
| [2.6 Capstone](./Track2_Orchestration_Automation/2.6_Capstone_Project/) | Microservices on Kubernetes | 1 week |

👉 **[Start Track 2 → (Bắt đầu Track 2)](./Track2_Orchestration_Automation/README.md)**

---

### ☁️ Track 3: Cloud & Network Design
>
> **Duration (Thời gian)**: 8-10 weeks | **Level**: Intermediate-Advanced

Master cloud infrastructure with AWS, Terraform and Ansible.

*Thành thạo cloud infrastructure với AWS, Terraform và Ansible.*

| Module | Content | Duration |
|--------|---------|----------|
| [3.1 Network Advanced](./Track3_Cloud_Network_Design/3.1_Network_Advanced/) | VPC, Load Balancing, Security Groups | 1-2 weeks |
| [3.2 AWS Core Services](./Track3_Cloud_Network_Design/3.2_AWS_Core_Services/) | EC2, S3, RDS, IAM | 2 weeks |
| [3.3 Databases for DevOps](./Track3_Cloud_Network_Design/3.3_Databases_for_DevOps/) | MySQL, PostgreSQL, Redis, MongoDB | 1-2 weeks |
| [3.4 Ansible](./Track3_Cloud_Network_Design/3.4_Config_Management_Ansible/) | Configuration management | 1-2 weeks |
| [3.5 Terraform](./Track3_Cloud_Network_Design/3.5_Terraform_IaC/) | Infrastructure as Code | 2 weeks |
| [3.6 System Design](./Track3_Cloud_Network_Design/3.6_System_Design_Reliability/) | High availability, scalability | 1 week |
| [3.7 Capstone](./Track3_Cloud_Network_Design/3.7_Capstone_Project/) | Full AWS infrastructure with Terraform | 1-2 weeks |

👉 **[Start Track 3 → (Bắt đầu Track 3)](./Track3_Cloud_Network_Design/README.md)**

---

### 🔐 Track 4: DevSecOps
>
> **Duration (Thời gian)**: 4-6 weeks | **Level**: Advanced

Integrate security into DevOps pipeline.

*Tích hợp security vào DevOps pipeline.*

| Module | Content | Duration |
|--------|---------|----------|
| [4.1 Security in Pipeline](./Track4_DevSecOps/4.1_Security_in_Pipeline/) | SAST, DAST, Container scanning | 2 weeks |
| [4.2 Infrastructure Security](./Track4_DevSecOps/4.2_Infra_Security/) | Secrets management, compliance | 2 weeks |
| [4.3 Capstone](./Track4_DevSecOps/4.3_Capstone_Project/) | Secure CI/CD pipeline | 1-2 weeks |

👉 **[Start Track 4 → (Bắt đầu Track 4)](./Track4_DevSecOps/README.md)**

---

### 🎓 Track 5: Career Path
>
> **Duration (Thời gian)**: 4-6 weeks | **Level**: All

Get ready for DevOps Engineer career.

*Chuẩn bị sẵn sàng cho career DevOps Engineer.*

| Module | Content | Duration |
|--------|---------|----------|
| [5.1 Certifications](./Track5_Career_Path/5.1_Certifications/) | AWS, CKA, Terraform Associate | Ongoing |
| [5.2 Interview Prep](./Track5_Career_Path/5.2_Interview_Prep/) | Technical interview, system design | 2 weeks |
| [5.3 Portfolio Launch](./Track5_Career_Path/5.3_Portfolio_Launch/) | GitHub profile, resume, LinkedIn | 1 week |
| [5.4 Grand Capstone](./Track5_Career_Path/5.4_Grand_Capstone/) | Production-ready infrastructure | 2-3 weeks |
| [5.5 Golang for DevOps](./Track5_Career_Path/5.5_Golang/) | CLI Tools & K8s Operators | 2 weeks |
| [5.6 GitOps & Platform Eng](./Track5_Career_Path/5.6_GitOps_Platform/) | ArgoCD & Internal Dev Platforms | 2 weeks |

👉 **[Start Track 5 → (Bắt đầu Track 5)](./Track5_Career_Path/README.md)**

---

## 📖 Usage Guide (Hướng Dẫn Sử Dụng)

### Module Structure (Cấu Trúc Mỗi Module)

```
Module_Name/
├── README.md          # 📖 Theory and detailed guide (Lý thuyết)
├── CHEATSHEET.md      # 📋 Quick reference (Tham khảo nhanh)
├── LABS.md            # 🔬 Hands-on labs (Bài thực hành)
├── QUIZ.md            # ❓ Knowledge check (Kiểm tra kiến thức)
├── EXERCISES.md       # 💪 Practice exercises (Bài tập)
├── PROJECT.md         # 🎯 Mini project (Dự án nhỏ)
├── SOLUTIONS.md       # ✅ Solutions - view after completing (Đáp án)
└── images/            # 🖼️ Illustrations (Hình ảnh)
```

### Recommended Learning Workflow (Workflow Học Tập Đề Xuất)

```
1. 📖 Read README.md      → Understand theory (Hiểu lý thuyết)
2. 🔬 Do LABS.md          → Follow guided practice (Thực hành theo hướng dẫn)
3. 💪 Do EXERCISES.md     → Self practice (Tự luyện tập)
4. ❓ Do QUIZ.md          → Test knowledge (Test kiến thức)
5. 🎯 Do PROJECT.md       → Apply in practice (Áp dụng thực tế)
6. 📋 Save CHEATSHEET.md  → Reference when needed (Tham khảo khi cần)
7. ✅ Check SOLUTIONS.md  → Compare answers (So sánh đáp án)
```

---

## 📊 Progress Tracking (Tiến Độ Học Tập)

Use the checklist below to track your progress (Sử dụng checklist dưới đây để theo dõi tiến độ):

### Track 1: Foundation & Static Web

- [ ] 1.1 Linux & Bash
- [ ] 1.2 Python Basics
- [ ] 1.3 Network Basics
- [ ] 1.4 Git & GitLab
- [ ] 1.5 Docker Fundamentals
- [ ] 1.6 NGINX Basic
- [ ] 1.7 CI/CD Basic
- [ ] 1.8 Capstone Project

### Track 2: Orchestration & Automation

- [ ] 2.1 Docker Advanced
- [ ] 2.2 Docker Compose
- [ ] 2.3 Jenkins
- [ ] 2.4 Kubernetes Core
- [ ] 2.5 Monitoring & Logging
- [ ] 2.6 Capstone Project

### Track 3: Cloud & Network Design

- [ ] 3.1 Network Advanced
- [ ] 3.2 AWS Core Services
- [ ] 3.3 Databases for DevOps
- [ ] 3.4 Ansible
- [ ] 3.5 Terraform
- [ ] 3.6 System Design & Reliability
- [ ] 3.7 Capstone Project

### Track 4: DevSecOps

- [ ] 4.1 Security in Pipeline
- [ ] 4.2 Infrastructure Security
- [ ] 4.3 Capstone Project

### Track 5: Career Path

- [ ] 5.1 Certifications
- [ ] 5.2 Interview Prep
- [ ] 5.3 Portfolio Launch
- [ ] 5.4 Grand Capstone
- [ ] 5.5 Golang for DevOps
- [ ] 5.6 GitOps & Platform Engineering

---

## 🛠️ Quick Start

```bash
# Clone repository
git clone https://github.com/thanhlehoang0107/DevOps-Journey.git
cd DevOps-Journey
```

```bash
# Start with Setup Environment (Bắt đầu với Setup Environment)
cd Track0_Setup_Environment
cat README.md
```

```bash
# Then start Track 1 (Sau đó bắt đầu Track 1)
cd ../Track1_Foundation_StaticWeb/1.1_Linux_Bash
cat README.md
```

---

## 🤝 Contributing (Đóng Góp)

Contributions are always welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

*Đóng góp luôn được chào đón! Xem CONTRIBUTING.md để biết thêm chi tiết.*

### How to Contribute (Cách đóng góp)

1. Fork repository
2. Create new branch (Tạo branch mới): `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add some AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request (Mở Pull Request)

---

## 📞 Contact (Liên Hệ)

- **GitHub**: [@thanhlehoang0107](https://github.com/thanhlehoang0107)
- **Email**: <thanhlehoang0107@gmail.com>

---

## 📄 License (Giấy Phép)

This project is distributed under the MIT License. See [LICENSE](LICENSE) for more details.

*Dự án này được phân phối dưới giấy phép MIT. Xem file LICENSE để biết thêm chi tiết.*

---

<div align="center">

**⭐ If this project is helpful, please give it a star! ⭐**

*Nếu dự án hữu ích, hãy cho một star!*

Made with ❤️ by [ThanhRòm](https://github.com/thanhlehoang0107)

</div>
