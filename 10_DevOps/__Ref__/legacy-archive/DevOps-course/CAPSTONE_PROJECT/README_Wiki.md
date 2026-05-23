# 🎓 Capstone Project: Triển khai Ứng dụng Web Full Stack

> **Dự án tổng hợp kiến thức từ 7 modules DevOps**

---

## 📖 Tổng quan

Capstone Project là dự án cuối khóa để bạn áp dụng TẤT CẢ kiến thức đã học từ Module 01 đến Module 07. Bạn sẽ triển khai một ứng dụng web hoàn chỉnh từ đầu đến cuối với đầy đủ pipeline DevOps.

---

## 🎯 Mục tiêu

Sau khi hoàn thành dự án này, bạn sẽ có:

- ✅ **1 ứng dụng production-ready** trên cloud (AWS)
- ✅ **CI/CD pipeline tự động** (GitHub Actions)
- ✅ **Infrastructure as Code** (Terraform)
- ✅ **Monitoring & Alerting** (Prometheus/Grafana)
- ✅ **Portfolio project** để showcase cho nhà tuyển dụng
- ✅ **Kinh nghiệm thực chiến** giải quyết vấn đề

---

## 🏗️ Yêu cầu Dự án

### 1. Ứng dụng

Chọn **1 trong 3** ứng dụng sau:

#### Option A: E-commerce Shop (Khuyến nghị)

- **Frontend**: React/Next.js
- **Backend**: Node.js + Express/FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Tính năng**:
  - User authentication
  - Product catalog
  - Shopping cart
  - Order management
  - Payment integration (Stripe test mode)

#### Option B: Blog Platform

- **Frontend**: React/Vue.js
- **Backend**: Django/Express
- **Database**: PostgreSQL
- **File Storage**: S3
- **Tính năng**:
  - User auth với roles (admin/writer/reader)
  - Create/Edit/Delete posts
  - Markdown editor
  - Comments system
  - Search functionality

#### Option C: Task Management System

- **Frontend**: React
- **Backend**: FastAPI/Node.js
- **Database**: MongoDB
- **Real-time**: WebSockets
- **Tính năng**:
  - User management
  - Create boards/tasks (Trello-like)
  - Drag & drop
  - Real-time collaboration
  - File attachments

### 2. Infrastructure (Terraform)

Phải tạo infrastructure bằng IaC:

```
Required AWS Resources:
├── VPC + Subnets (public/private)
├── EC2 / ECS / EKS (chọn 1)
├── RDS (PostgreSQL/MySQL)
├── ElastiCache (Redis)
├── S3 (static files)
├── ALB (Load Balancer)
├── Route53 (Domain)
└── CloudWatch (Logs)
```

### 3. CI/CD Pipeline (GitHub Actions)

```yaml
Pipeline phải bao gồm:
- 🧪 Unit Tests (coverage ≥ 70%)
- 🔍 Code Quality (ESLint/Pylint/Flake8)
- 🐳 Docker build & push
- 🚀 Deploy to staging
- ✅ Integration tests
- 🎯 Deploy to production (manual approve)
```

### 4. Configuration Management (Ansible)

- Deploy application bằng Ansible playbooks
- Automated server configuration
- Application deployment
- Database migrations

### 5. Monitoring & Logging

```
Required:
├── Prometheus - Metrics collection
├── Grafana - Dashboards
├── Application metrics
│   ├── HTTP requests/sec
│   ├── Response time
│   ├── Error rate
│   └── Database connections
├── Infrastructure metrics
│   ├── CPU/Memory/Disk
│   └── Network I/O
└── Alerts
    ├── High error rate
    ├── Slow response time
    └── Resource exhaustion
```

### 6. Documentation

```
Phải có:
├── README.md (overview)
├── ARCHITECTURE.md (diagrams)
├── SETUP.md (how to run locally)
├── DEPLOY.md (deployment guide)
├── RUNBOOK.md (troubleshooting)
└── POST_MORTEM.md (1 incident mô phỏng)
```

---

## 📁 Cấu trúc Dự án Đề xuất

```
capstone-project/
├── README.md
├── ARCHITECTURE.md
├── docs/
│   ├── SETUP.md
│   ├── DEPLOY.md
│   └── RUNBOOK.md
├── app/
│   ├── frontend/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── package.json
│   └── backend/
│       ├── src/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── tests/
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── ansible/
│       ├── playbooks/
│       └── inventory/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── k8s/ (nếu dùng Kubernetes)
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── monitoring/
    ├── prometheus/
    │   └── prometheus.yml
    └── grafana/
        └── dashboards/
```

---

## 🚀 Timeline (4-6 tuần)

### Week 1-2: Planning & Development

- [ ] Chọn ứng dụng
- [ ] Thiết kế architecture
- [ ] Setup Git repository
- [ ] Develop MVP locally
- [ ] Write unit tests

### Week 3: Infrastructure & CI/CD

- [ ] Write Terraform code
- [ ] Provision infrastructure
- [ ] Setup CI/CD pipeline
- [ ] Deploy to staging

### Week 4: Configuration & Automation

- [ ] Write Ansible playbooks
- [ ] Automate deployment
- [ ] Setup monitoring
- [ ] Configure alerts

### Week 5: Testing & Optimization

- [ ] Load testing
- [ ] Security scanning
- [ ] Performance optimization
- [ ] Documentation

### Week 6: Finalization

- [ ] Deploy to production
- [ ] Demo video
- [ ] Write post-mortem
- [ ] Prepare presentation

---

## ✅ Checklist Hoàn thành

### Code & Application

- [ ] Application chạy được local
- [ ] Unit tests coverage ≥ 70%
- [ ] Integration tests pass
- [ ] Docker images optimized (<500MB)

### Infrastructure

- [ ] Terraform code valid (`terraform plan`)
- [ ] Infrastructure deployed thành công
- [ ] Security groups configured đúng
- [ ] Backups enabled

### CI/CD

- [ ] GitHub Actions pipeline working
- [ ] Auto deploy to staging on merge
- [ ] Manual approval for production
- [ ] Rollback strategy có sẵn

### Monitoring

- [ ] Prometheus collecting metrics
- [ ] Grafana dashboards tạo xong
- [ ] Alerts configured
- [ ] Test alerts (fire manually)

### Documentation

- [ ] README với badges (build status, coverage)
- [ ] Architecture diagram
- [ ] API documentation
- [ ] Runbook cho common issues

---

## 🎥 Demo & Presentation

### Demo Video (5-10 phút)

Bao gồm:

1. **Overview** (1 phút): Giới thiệu app
2. **Architecture** (2 phút): Sơ đồ và giải thích
3. **CI/CD** (2 phút): Show pipeline running
4. **Monitoring** (2 phút): Grafana dashboards
5. **Troubleshooting** (2 phút): Simulate & fix 1 incident

### Presentation Slides (10-15 slides)

1. Title & Introduction
2. Problem Statement
3. Solution Architecture
4. Technology Stack
5. Infrastructure Design
6. CI/CD Pipeline
7. Monitoring & Alerting
8. Challenges & Solutions
9. Lessons Learned
10. Future Improvements

---

## 🌟 Đánh giá (100 điểm)

Xem chi tiết tại [RUBRIC.md](./RUBRIC.md)

| Hạng mục | Điểm |
|----------|------|
| Application Functionality | 20đ |
| Infrastructure as Code | 20đ |
| CI/CD Pipeline | 20đ |
| Monitoring & Logging | 15đ |
| Documentation | 10đ |
| Code Quality | 10đ |
| Presentation | 5đ |

**Điểm tối thiểu để pass: 70/100**

---

## 💡 Tips

1. **Bắt đầu nhỏ** - MVP trước, features sau
2. **Git commit thường xuyên** - Mỗi tính năng 1 commit
3. **Document ngay** - Đừng để cuối mới viết docs
4. **Test trên staging trước** - Đừng test thẳng production
5. **Backup state file** - Terraform state rất quan trọng
6. **Monitor costs** - Set billing alerts trên AWS
7. **Destroy resources khi không dùng** - Tiết kiệm chi phí

---

## 🆘 Resources

- [Example Project](https://github.com/example/devops-capstone)
- [AWS Free Tier Limits](https://aws.amazon.com/free)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## 📬 Nộp bài

Tạo Pull Request vào repo này với:

1. Link GitHub repo của bạn
2. Link demo video (YouTube/Loom)
3. Link ứng dụng đang chạy (nếu còn deploy)
4. Slides presentation

**Deadline**: Tuần cuối của khóa học

---

**Chúc bạn thành công! 🚀**

Questions? [Open an issue](https://github.com/thanhlehoang0107/devops-course/issues)
