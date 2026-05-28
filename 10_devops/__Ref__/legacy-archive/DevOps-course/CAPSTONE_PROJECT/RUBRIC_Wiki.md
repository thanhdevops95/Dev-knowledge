# 📊 Capstone Project Grading Rubric

> **Chi tiết tiêu chí đánh giá (100 điểm)**

---

## 1. Application Functionality (20 điểm)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Hoạt động ổn định** | 8đ | App chạy không lỗi, không crash |
| **Features đầy đủ** | 7đ | Các tính năng cốt lõi hoàn chỉnh |
| **UI/UX** | 3đ | Giao diện đẹp, dễ dùng |
| **Security basics** | 2đ | HTTPS, secure passwords, env vars |

---

## 2. Infrastructure as Code (20 điểm)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Terraform valid** | 5đ | `terraform plan` pass, no errors |
| **Modularity** | 5đ | Sử dụng modules, variables |
| **Best practices** | 5đ | Remote state, workspaces |
| **Documentation** | 5đ | README rõ ràng, comments |

---

## 3. CI/CD Pipeline (20 điểm)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Automated testing** | 6đ | Unit + Integration tests tự động |
| **Build & Deploy** | 6đ | Auto build Docker, deploy staging |
| **Quality gates** | 4đ | Code quality, security scan |
| **Production deploy** | 4đ | Manual approval, rollback strategy |

---

## 4. Monitoring & Logging (15 điểm)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Metrics collection** | 5đ | Prometheus thu thập metrics |
| **Dashboards** | 5đ | Grafana có ít nhất 2 dashboards |
| **Alerting** | 3đ | Cấu hình alerts, test được |
| **Logging** | 2đ | Centralized logs |

---

## 5. Documentation (10 điểm)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **README.md** | 3đ | Overview, setup instructions |
| **ARCHITECTURE.md** | 3đ | Diagrams, tech stack explained |
| **RUNBOOK.md** | 2đ | Troubleshooting guide |
| **POST_MORTEM.md** | 2đ | 1 incident analysis |

---

## 6. Code Quality (10 điểm)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Test coverage** | 4đ | ≥70% unit test coverage |
| **Code organization** | 3đ | Clean structure, naming |
| **Git history** | 2đ | Meaningful commits, PR reviews |
| **Linting** | 1đ | Pass linter checks |

---

## 7. Presentation (5 điểm)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Demo video** | 3đ | Clear, comprehensive (5-10 min) |
| **Slides** | 2đ | Professional, well-structured |

---

## 🎯 Thang điểm

| Điểm | Grade | Đánh giá |
|------|-------|----------|
| 90-100 | A | Xuất sắc |
| 80-89 | B | Tốt |
| 70-79 | C | Đạt (Pass) |
| <70 | F | Chưa đạt |

---

## ⭐ Bonus Points (Tối đa +10đ)

- **+3đ**: Sử dụng Kubernetes thay vì EC2
- **+2đ**: Multi-region deployment
- **+2đ**: Load testing với k6/JMeter
- **+2đ**: Security scanning (Trivy, SonarQube)
- **+1đ**: Custom Grafana dashboards (>3)

---

## ✅ Checklist tự đánh giá

Trước khi nộp, check:

- [ ] Application deployed và accessible
- [ ] All tests passing in CI
- [ ] Terraform code validated
- [ ] Monitoring dashboards working
- [ ] Documentation complete
- [ ] Demo video uploaded
- [ ] Costs monitored (AWS billing alert)

---

**Điểm tối thiểu để pass: 70/100**

Good luck! 🍀
