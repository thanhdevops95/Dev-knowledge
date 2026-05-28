# 💼 Module 5.2: Interview Preparation

[![Duration](https://img.shields.io/badge/Duration-2%20weeks-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-All%20Levels-green?style=flat-square)](.)

> **Ace Your DevOps Interview** - Technical and behavioral preparation.
>
> *Chinh phục phỏng vấn DevOps - Chuẩn bị kỹ thuật và hành vi.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Answer common interview questions (Trả lời câu hỏi phổ biến)
- ✅ Tackle system design interviews (Xử lý phỏng vấn thiết kế hệ thống)
- ✅ Solve coding challenges (Giải quyết thử thách coding)
- ✅ Master behavioral questions - STAR method (Thành thạo câu hỏi hành vi)
- ✅ Negotiate salary (Đàm phán lương)

---

## 📚 Content (Nội dung)

### 1. Technical Questions (Câu hỏi kỹ thuật)

#### 🐧 Linux/Bash

- Process management (Quản lý tiến trình)
- File permissions, users, groups (Quyền file, users, groups)
- Scripting best practices (Best practices viết script)
- Troubleshooting commands (Các lệnh xử lý sự cố)

**Sample Questions (Câu hỏi mẫu):**

- What's the difference between `kill -9` and `kill -15`?
- How to find files larger than 100MB?
- Explain the Linux boot process.

---

#### 🌐 Networking (Mạng)

- TCP/IP, DNS, HTTP/HTTPS protocols
- Load balancing strategies (Chiến lược cân bằng tải)
- VPN, Firewalls, Security Groups
- Troubleshooting network issues (Xử lý sự cố mạng)

**Sample Questions (Câu hỏi mẫu):**

- How does DNS resolution work?
- What's the difference between L4 and L7 load balancing?
- How would you troubleshoot a "connection refused" error?

---

#### 🐳 Docker

- Image vs Container differences
- Dockerfile best practices (Multi-stage, caching)
- Networking modes (bridge, host, overlay)
- Storage (volumes, bind mounts)
- Security (non-root user, read-only filesystem)

**Sample Questions (Câu hỏi mẫu):**

- How does Docker layered filesystem work?
- What's the difference between COPY and ADD?
- How to reduce Docker image size?

---

#### ☸️ Kubernetes

- Architecture components (Kiến trúc: API Server, etcd, kubelet)
- Workloads: Deployments, StatefulSets, DaemonSets
- Services, Ingress, NetworkPolicy
- ConfigMaps, Secrets, RBAC
- Troubleshooting pods (Khắc phục sự cố pods)

**Sample Questions (Câu hỏi mẫu):**

- Explain Kubernetes pod lifecycle.
- What happens when you run `kubectl apply`?
- How would you debug a CrashLoopBackOff?

---

#### 🔄 CI/CD

> **Note (Lưu ý):** Be familiar with both GitLab CI and GitHub Actions!
> *Cần quen thuộc với cả GitLab CI và GitHub Actions!*

| Topic | GitLab CI | GitHub Actions |
|-------|-----------|----------------|
| Config file | `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| Pipeline structure | `stages` + `jobs` | `jobs` + `steps` |
| Artifacts | `artifacts:` | `actions/upload-artifact` |
| Cache | `cache:` | `actions/cache` |
| Variables | CI/CD Settings | Secrets/Variables |

**Sample Questions (Câu hỏi mẫu):**

- Design a CI/CD pipeline for a microservices application.
- What's the difference between GitLab CI stages and needs?
- How to implement blue/green deployment?
- How to handle secrets in pipelines?

---

#### ☁️ Cloud/AWS

- VPC design patterns (Thiết kế VPC)
- IAM best practices (principle of least privilege)
- High availability patterns (HA patterns)
- Cost optimization tips (Tối ưu chi phí)

**Sample Questions (Câu hỏi mẫu):**

- Design a VPC for a 3-tier application.
- How to secure access to EC2 instances?
- Explain the difference between EBS and EFS.

---

#### 🛠️ Infrastructure as Code

- Terraform vs Ansible differences (Sự khác biệt)
- State management in Terraform
- Idempotency concept (Khái niệm idempotency)
- Module design patterns

**Sample Questions (Câu hỏi mẫu):**

- How does Terraform state work?
- When to use Terraform vs Ansible?
- How to handle secrets in Terraform?

---

### 2. System Design (Thiết kế hệ thống)

Common system design questions (Các câu hỏi thiết kế phổ biến):

1. **Design scalable web app** (Thiết kế web app có khả năng mở rộng)
   - Load balancing, auto-scaling, caching

2. **Design CI/CD pipeline** (Thiết kế pipeline CI/CD)
   - Build, test, deploy stages
   - Security scanning, rollback strategies

3. **Design monitoring system** (Thiết kế hệ thống giám sát)
   - Metrics collection, alerting, dashboards

4. **Design disaster recovery** (Thiết kế khôi phục thảm họa)
   - RTO/RPO, backup strategies, failover

#### System Design Framework (Khung thiết kế)

```
1. Clarify Requirements (Làm rõ yêu cầu)
   - Functional requirements (Yêu cầu chức năng)
   - Non-functional: scale, availability, latency

2. High-Level Design (Thiết kế cấp cao)
   - Draw architecture diagram (Vẽ sơ đồ)
   - Identify main components (Xác định components)

3. Deep Dive (Đi sâu chi tiết)
   - Database choices (Lựa chọn database)
   - Scaling strategies (Chiến lược mở rộng)
   - Trade-offs (Đánh đổi)

4. Bottlenecks & Solutions (Nút thắt & giải pháp)
   - Identify potential issues (Xác định vấn đề)
   - Propose solutions (Đề xuất giải pháp)
```

---

### 3. Behavioral Questions - STAR (Câu hỏi hành vi)

Use STAR method for behavioral questions (Sử dụng phương pháp STAR):

- **S**ituation: Describe context (Mô tả bối cảnh)
- **T**ask: What was your responsibility (Trách nhiệm của bạn)
- **A**ction: What you did (Bạn đã làm gì)
- **R**esult: What was the outcome (Kết quả)

**Common Questions (Câu hỏi phổ biến):**

1. Tell me about a time you handled a production incident.
2. Describe a challenging project you worked on.
3. How did you deal with a difficult team member?
4. Tell me about a time you improved a process.
5. Describe a situation where you had to learn quickly.

---

## 💡 Interview Tips (Mẹo phỏng vấn)

| Tip | Description |
|-----|-------------|
| 🔧 **Practice hands-on** | Don't just read, practice with real tools (Thực hành với công cụ thực) |
| 📝 **Review your projects** | Know your portfolio in detail (Nắm rõ portfolio) |
| ❓ **Prepare questions** | Ask about team, stack, challenges (Hỏi về team, công nghệ) |
| 🏢 **Research the company** | Understand their products and tech (Tìm hiểu công ty) |
| 🤝 **Be honest** | Say "I don't know, but I would..." (Thành thật khi không biết) |
| ⏱️ **Think aloud** | Explain your thought process (Giải thích cách suy nghĩ) |

---

## 📖 Resources (Tài liệu tham khảo)

### Books (Sách)

- "Designing Data-Intensive Applications" by Martin Kleppmann
- "The DevOps Handbook"
- "Site Reliability Engineering" (Google SRE Book)

### Websites

- [DevOps Roadmap](https://roadmap.sh/devops)
- [LeetCode](https://leetcode.com/) - Coding practice
- [System Design Primer](https://github.com/donnemartin/system-design-primer)

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Practice questions (Câu hỏi luyện tập) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Mock interviews (Phỏng vấn giả) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [5.1 Certifications](../5.1_Certifications/) | **5.2 Interview Prep** | [5.3 Portfolio](../5.3_Portfolio_Launch/) |

---

**Ace your interview! 💼**

*Chinh phục buổi phỏng vấn!*

</div>
