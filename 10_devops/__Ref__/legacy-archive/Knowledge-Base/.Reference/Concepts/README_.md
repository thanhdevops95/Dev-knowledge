# 📖 _NoiDungMau - Nội Dung Mẫu

---

## 📋 Mô Tả

Thư mục này chứa **các nội dung đã được viết sẵn** từ nhiều nguồn khác nhau. Dùng để **tham khảo cách viết**, cấu trúc bài học, và lấy ý tưởng khi xây dựng nội dung mới cho DevOps-Journey.

---

## 📁 Cấu Trúc

```
_NoiDungMau/
│
├── Setup_Environment/            # Mẫu setup môi trường (chuẩn)
├── Track1_Foundation_StaticWeb/  # Mẫu Track 1 (chuẩn)
├── Track2_Orchestration_Automation/
├── Track3_Cloud_Network_Design/
├── Track4_DevSecOps/
├── Track5_Career_Path/
│
├── DevOps-1_TrainingRoadmap/     # Nguồn 1: Roadmap 7 Lessons
├── DevOps-2/                     # Nguồn 2: 15 Modules chi tiết
├── DevOps-3/                     # Nguồn 3: Foundation
└── DevOps-course/                # Nguồn 4: DevOps Lifecycle
```

---

## 📚 Chi Tiết Từng Nguồn

### 🎯 Nội dung chuẩn (Setup + 5 Tracks)

**Đặc điểm:** Đã được cấu trúc theo chuẩn của dự án DevOps-Journey.

| Thư mục | Nội dung | Số modules |
|---------|----------|------------|
| `Setup_Environment/` | Cài đặt môi trường, WSL, Docker Desktop | 1 |
| `Track1_Foundation_StaticWeb/` | Linux, Network, Git, Docker, NGINX, CI/CD | 7 |
| `Track2_Orchestration_Automation/` | Docker Advanced, Compose, Jenkins, K8s, Monitoring | 6 |
| `Track3_Cloud_Network_Design/` | AWS, Terraform, System Design | 5 |
| `Track4_DevSecOps/` | Security Pipeline, Infra Security | 3 |
| `Track5_Career_Path/` | Certifications, Interview Prep | 3 |

**Cấu trúc mỗi module:**

```
X.Y_ModuleName/
├── images/          # Ảnh riêng module
├── README.md        # Giáo trình lý thuyết
├── CHEATSHEET.md    # Tra cứu nhanh
├── LABS.md          # Thực hành có hướng dẫn
├── QUIZ.md          # Câu hỏi trắc nghiệm
├── EXERCISES.md     # Bài tập tình huống
├── PROJECT.md       # Dự án mini
└── SOLUTIONS.md     # Đáp án chi tiết
```

---

### 📘 DevOps-1_TrainingRoadmap

**Nguồn:** Roadmap đào tạo 7 Lessons

| Lesson | Nội dung |
|--------|----------|
| Lesson01 | Foundation (What is DevOps, Linux CLI, Scripting, Networking) |
| Lesson02 | SCM & CI (Git, CI/CD Theory, GitLab CI) |
| Lesson03 | Containerization (Docker, Kubernetes) |
| Lesson04 | CM & IaC (Ansible, Terraform) |
| Lesson05 | Monitoring & Logging (Prometheus/Grafana, EFK) |
| Lesson06 | Cloud (AWS Core) |
| Lesson07 | Final Project & Career |

**Đặc điểm:** Mỗi lesson có README chi tiết bằng tiếng Việt.

---

### 📗 DevOps-2

**Nguồn:** Bộ 15 Modules chi tiết nhất

| Module | Tên | Files |
|--------|-----|-------|
| 01 | LINUX | README.md, LABS.md, SCENARIOS.md |
| 02 | NETWORKING | 11 files chi tiết (IP/OSI, TCP/UDP, Load Balancing...) |
| 03 | SCRIPTING | README, LABS |
| 04 | GIT | README, LABS |
| 05 | WEB_SERVERS | NGINX |
| 06 | DATABASES | SQL/NoSQL |
| 07 | DOCKER | Fundamentals + Advanced |
| 08 | CI | Continuous Integration |
| 09 | KUBERNETES | Core concepts |
| 10 | CD | Continuous Deployment |
| 11 | CLOUD | AWS/GCP/Azure |
| 12 | IAC | Terraform |
| 13 | SECURITY | DevSecOps |
| 14 | OBSERVABILITY | Monitoring, Logging, Tracing |
| 15 | SRE | Site Reliability Engineering |

**Đặc điểm:**

- README rất chi tiết với câu chuyện, ẩn dụ
- Có bảng thuật ngữ đầu mỗi bài
- Labs thực tế
- Scenarios tình huống

**👉 Khuyến nghị tham khảo:** Module 01_LINUX là mẫu xuất sắc nhất.

---

### 📙 DevOps-3

**Nguồn:** Foundation track

| Module | Tên |
|--------|-----|
| 01 | LINUX_BASICS |
| 02 | GIT_GITHUB |
| 03 | NETWORKING_INTRO |
| 04 | HTML_CSS_JS_BASICS |
| 05 | DOCKER_BASICS |
| 06 | CI_BASICS |
| 07 | WEB_SERVERS_BASICS |
| 08 | DEPLOYMENT_BASICS |
| 09 | MONITORING_BASICS |
| FINAL | FINAL_PROJECT |
| INTEGRATION | INTEGRATION_PROJECTS |

**Đặc điểm:** Focus vào basics, phù hợp cho người mới.

---

### 📕 DevOps-course

**Nguồn:** Cấu trúc theo DevOps Lifecycle

```
01_PLAN → 02_BUILD → 03_CI → 04_CD → 05_OPERATE → 06_MONITOR → 07_FEEDBACK
```

**Đặc điểm:**

- Có source-code mẫu
- Scripts cài đặt
- Capstone Project

---

## 🔍 Cách Sử Dụng

### Khi viết README mới

```bash
# Tham khảo mẫu tốt nhất
open DevOps-2/01_LINUX/README.md
```

### Khi viết LABS mới

```bash
# Xem cách viết labs chi tiết
open DevOps-2/01_LINUX/LABS.md
```

### Khi cần ý tưởng cho scenarios

```bash
open DevOps-2/01_LINUX/SCENARIOS.md
open DevOps-2/02_NETWORKING/SCENARIOS.md
```

---

## ⭐ Khuyến Nghị

| Mục đích | Tham khảo |
|----------|-----------|
| Viết README chi tiết | `DevOps-2/01_LINUX/README.md` |
| Viết với câu chuyện/ẩn dụ | `DevOps-2/` (tất cả modules) |
| Cấu trúc 7 files chuẩn | `Track1_Foundation_StaticWeb/1.1_Linux_Bash/` |
| Labs step-by-step | `DevOps-2/*/LABS.md` |
| Nội dung cho beginner | `DevOps-3/FOUNDATION/` |

---

*Cập nhật: 2025-12-28*
