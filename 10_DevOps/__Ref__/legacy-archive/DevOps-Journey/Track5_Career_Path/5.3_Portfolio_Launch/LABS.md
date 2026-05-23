# 🔬 Labs: Portfolio & Launch

> **Hands-on portfolio building exercises**
>
> *Bài thực hành xây dựng portfolio*

---

## 🔬 Lab 1: GitLab/GitHub Profile Setup (Thiết lập Profile)

### Option A: GitLab Profile (Primary - Chính)

1. Go to **Preferences** → **Main Settings**
2. Update your profile with (Cập nhật hồ sơ với):
   - Professional photo (Ảnh chuyên nghiệp)
   - Bio with DevOps keywords (Tiểu sử với từ khóa DevOps)
   - Location and website (Vị trí và website)

### Option B: GitHub Profile (Alternative - Thay thế)

Create a profile README by creating a repository with your username:
*Tạo README cho profile bằng cách tạo một repository trùng với username của bạn:*

```bash
# Create repo with your username
# e.g., github.com/username/username
mkdir username && cd username
```

```markdown
<!-- README.md -->
# Hi, I'm [Your Name] 👋

## 🚀 DevOps Engineer

I'm passionate about automation, cloud infrastructure, and building reliable systems.

*Tôi đam mê về tự động hóa, hạ tầng cloud, và xây dựng hệ thống đáng tin cậy.*

### 🔧 Tech Stack (Công nghệ)

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GitLab](https://img.shields.io/badge/GitLab-FC6D26?style=for-the-badge&logo=gitlab&logoColor=white)

### 📈 GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=yourusername&show_icons=true)

### 📫 Connect (Kết nối)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitLab](https://img.shields.io/badge/GitLab-FC6D26?style=for-the-badge&logo=gitlab)](https://gitlab.com/yourprofile)
```

---

## 🔬 Lab 2: Portfolio Projects (Dự án Portfolio)

### Project 1: CI/CD Pipeline

```
Repository: my-cicd-project
Contents:
├── .gitlab-ci.yml        # GitLab CI (Primary)
├── .github/workflows/    # GitHub Actions (Alternative)
├── app/
├── Dockerfile
├── README.md (with architecture diagram)
└── docs/
```

### Project 2: Infrastructure as Code

```
Repository: aws-infrastructure
Contents:
├── terraform/
│   ├── modules/
│   ├── environments/
│   └── main.tf
├── ansible/
├── .gitlab-ci.yml        # Terraform CI pipeline
├── README.md
└── architecture.png
```

### Project 3: Kubernetes Deployment

```
Repository: k8s-microservices
Contents:
├── k8s/
│   ├── deployments/
│   ├── services/
│   └── ingress/
├── monitoring/
├── .gitlab-ci.yml
├── README.md
└── Makefile
```

---

## 🔬 Lab 3: README Best Practices (Best Practices README)

```markdown
# Project Name

Brief description of what this project does.

*Mô tả ngắn về dự án.*

## 🏗️ Architecture (Kiến trúc)

![Architecture](./docs/architecture.png)

## 🚀 Quick Start (Bắt đầu nhanh)

\`\`\`bash
git clone https://gitlab.com/user/project  # or github.com
cd project
make deploy
\`\`\`

## 📋 Prerequisites (Điều kiện tiên quyết)

- Docker
- AWS CLI
- Terraform

## 🛠️ Technologies (Công nghệ)

- Kubernetes
- Prometheus
- Grafana
- GitLab CI

## 📖 Documentation (Tài liệu)

- [Setup Guide](./docs/setup.md)
- [Contributing](./CONTRIBUTING.md)

## 📝 License

MIT
```

---

## 🔬 Lab 4: LinkedIn Optimization (Tối ưu LinkedIn)

### Profile Sections (Các phần Profile)

1. **Headline**: "DevOps Engineer | AWS | Kubernetes | GitLab CI | Terraform"

2. **About (Giới thiệu)**:
   "DevOps Engineer with experience in cloud infrastructure, CI/CD pipelines, and container orchestration. Passionate about automation and building reliable systems."

   *"Kỹ sư DevOps với kinh nghiệm về hạ tầng đám mây, quy trình CI/CD và điều phối container. Đam mê tự động hóa và xây dựng các hệ thống tin cậy."*

3. **Experience**:
   - Use bullet points (Dùng bullet points)
   - Include metrics (reduced deploy time by 80%) (Bao gồm số liệu)
   - List technologies used (Liệt kê công nghệ sử dụng)

4. **Skills**:
   AWS, Docker, Kubernetes, Terraform, GitLab CI, Jenkins, Python, Linux

5. **Projects**:
   Link to GitLab/GitHub repositories (Link đến repo GitLab/GitHub)

---

## 🔬 Lab 5: Technical Blog (Blog kỹ thuật)

### Platform Options (Lựa chọn nền tảng)

| Platform | Pros (Ưu điểm) |
|----------|----------------|
| Dev.to | Built-in audience, easy setup (Có sẵn độc giả, thiết lập dễ) |
| Hashnode | Custom domain, good SEO (Tên miền riêng, SEO tốt) |
| Medium | Large audience (Lượng độc giả lớn) |
| Personal blog | Full control (Hugo/Jekyll) (Toàn quyền kiểm soát) |

### Blog Post Ideas (Ý tưởng bài viết)

1. "How I Built a CI/CD Pipeline with GitLab CI" (Cách tôi xây dựng pipeline với GitLab CI)
2. "Kubernetes Deployment Best Practices" (Các thực hành tốt nhất khi triển khai Kubernetes)
3. "My AWS Solutions Architect Certification Journey" (Hành trình đạt chứng chỉ AWS Solutions Architect của tôi)
4. "Monitoring Docker Containers with Prometheus and Grafana" (Giám sát Docker Container với Prometheus và Grafana)
5. "Infrastructure as Code with Terraform - Getting Started" (Làm quen với Infrastructure as Code và Terraform)

---

## ✅ Portfolio Checklist (Danh sách kiểm tra)

- [ ] GitLab/GitHub profile README (Profile README)
- [ ] 3+ portfolio projects (3+ dự án portfolio)
- [ ] Detailed READMEs with bilingual content (README chi tiết song ngữ)
- [ ] LinkedIn updated (LinkedIn đã cập nhật)
- [ ] Blog with 2+ posts (Blog với 2+ bài viết)

---

**[← Back to README](./README.md)**
