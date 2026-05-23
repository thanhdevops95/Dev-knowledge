# Module 08: CONTINUOUS INTEGRATION (CI)

> **"CI là dây chuyền kiểm tra chất lượng - bắt lỗi trước khi đến tay khách"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu CI là gì và benefits
- ✅ GitHub Actions từ cơ bản đến nâng cao
- ✅ GitLab CI basics
- ✅ Jenkins basics
- ✅ Automated testing trong CI
- ✅ Code quality checks (linting, SAST)
- ✅ Build và push Docker images trong CI
- ✅ Artifacts và caching
- ✅ Matrix builds và parallel jobs
- ✅ CI best practices

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| CI | Continuous Integration | Tích hợp liên tục |
| Pipeline | CI Pipeline | Luồng CI tự động |
| Workflow | Workflow | Quy trình làm việc |
| Job | Job | Công việc trong pipeline |
| Step | Step | Bước trong job |
| Runner | Runner | Máy chạy CI jobs |
| Action | GitHub Action | Component tái sử dụng |
| Trigger | Trigger | Sự kiện kích hoạt CI |
| Artifact | Artifact | File output từ build |
| Cache | CI Cache | Lưu cache giữa các runs |
| Matrix | Matrix Build | Chạy nhiều configurations |
| Secret | Secret | Thông tin nhạy cảm |
| Environment | Environment | Môi trường deploy |
| Status Check | Status Check | Kiểm tra trước merge |
| Code Coverage | Code Coverage | Phần trăm code được test |
| Lint | Linting | Kiểm tra code style |
| SAST | Static Application Security Testing | Scan bảo mật tĩnh |

---

## ✅ Checklist Labs

### Labs GitHub Actions cơ bản

- [ ] Lab 1: First workflow - Hello World
- [ ] Lab 2: Workflow file structure
- [ ] Lab 3: Triggers (push, pull_request, schedule)
- [ ] Lab 4: Multiple jobs
- [ ] Lab 5: Job dependencies (needs)
- [ ] Lab 6: If conditions
- [ ] Lab 7: Environment variables
- [ ] Lab 8: Secrets usage
- [ ] Lab 9: Contexts (${{ github }}, ${{ env }})

### Labs GitHub Actions runners

- [ ] Lab 10: GitHub-hosted runners
- [ ] Lab 11: Runner labels và selection
- [ ] Lab 12: Self-hosted runner setup
- [ ] Lab 13: Runner groups

### Labs GitHub Actions advanced

- [ ] Lab 14: Matrix builds
- [ ] Lab 15: Fail-fast và continue-on-error
- [ ] Lab 16: Timeout và concurrency
- [ ] Lab 17: Reusable workflows
- [ ] Lab 18: Composite actions
- [ ] Lab 19: Workflow dispatch (manual trigger)
- [ ] Lab 20: Repository dispatch

### Labs Caching và Artifacts

- [ ] Lab 21: Actions cache
- [ ] Lab 22: Cache dependencies (npm, pip)
- [ ] Lab 23: Upload artifacts
- [ ] Lab 24: Download artifacts
- [ ] Lab 25: Artifacts between jobs

### Labs Testing trong CI

- [ ] Lab 26: Run unit tests
- [ ] Lab 27: Test report generation
- [ ] Lab 28: Code coverage report
- [ ] Lab 29: Upload coverage to Codecov
- [ ] Lab 30: Test với database (service containers)

### Labs Code Quality

- [ ] Lab 31: Python linting với flake8
- [ ] Lab 32: Python linting với pylint
- [ ] Lab 33: JavaScript linting với ESLint
- [ ] Lab 34: Markdown linting
- [ ] Lab 35: Pre-commit hooks trong CI
- [ ] Lab 36: SAST với Bandit (Python)
- [ ] Lab 37: Dependency scanning

### Labs Docker trong CI

- [ ] Lab 38: Build Docker image trong CI
- [ ] Lab 39: Push to Docker Hub
- [ ] Lab 40: Push to GitHub Container Registry
- [ ] Lab 41: Multi-platform builds
- [ ] Lab 42: Docker layer caching
- [ ] Lab 43: Image scanning trong CI

### Labs Counter App CI

- [ ] Lab 44: CI pipeline cho Counter App
- [ ] Lab 45: Test Counter App
- [ ] Lab 46: Build và push Counter App image
- [ ] Lab 47: Version tagging

### Labs GitLab CI

- [ ] Lab 48: .gitlab-ci.yml basics
- [ ] Lab 49: Stages và jobs
- [ ] Lab 50: GitLab runners
- [ ] Lab 51: GitLab CI variables
- [ ] Lab 52: GitLab CI artifacts

### Labs Jenkins

- [ ] Lab 53: Jenkins installation với Docker
- [ ] Lab 54: Jenkins job creation
- [ ] Lab 55: Jenkinsfile basics
- [ ] Lab 56: Jenkins Pipeline
- [ ] Lab 57: Jenkins credentials

### Labs Best Practices

- [ ] Lab 58: Branch protection với CI
- [ ] Lab 59: Required status checks
- [ ] Lab 60: PR preview deployments
- [ ] Lab 61: CI notifications (Slack)
- [ ] Lab 62: Monorepo CI patterns

---

## 🚨 Checklist Scenarios

### Scenarios về Workflow

- [ ] Scenario 1: Workflow không trigger
- [ ] Scenario 2: Workflow trigger quá nhiều lần
- [ ] Scenario 3: Job bị timeout
- [ ] Scenario 4: Workflow syntax error
- [ ] Scenario 5: Concurrency issues - jobs conflict

### Scenarios về Secrets

- [ ] Scenario 6: Secret không available trong fork PR
- [ ] Scenario 7: Secret bị expose trong logs
- [ ] Scenario 8: Secret rotation trong CI
- [ ] Scenario 9: Secret scope issues

### Scenarios về Testing

- [ ] Scenario 10: Tests pass local nhưng fail trong CI
- [ ] Scenario 11: Flaky tests (sometimes pass, sometimes fail)
- [ ] Scenario 12: Tests chạy quá lâu
- [ ] Scenario 13: Database tests fail trong CI
- [ ] Scenario 14: Timezone issues trong tests

### Scenarios về Docker

- [ ] Scenario 15: Docker build fails trong CI
- [ ] Scenario 16: Docker push authentication failed
- [ ] Scenario 17: Build chậm do không có cache
- [ ] Scenario 18: Disk space exhausted

### Scenarios về Dependencies

- [ ] Scenario 19: Cache miss gây build chậm
- [ ] Scenario 20: Dependency version conflict
- [ ] Scenario 21: npm/pip install timeout
- [ ] Scenario 22: Private dependency access

### Scenarios về Integration

- [ ] Scenario 23: Status check không update
- [ ] Scenario 24: PR merge blocked bởi CI
- [ ] Scenario 25: Notification spam
- [ ] Scenario 26: CI slow down developer velocity

### Scenarios về Security

- [ ] Scenario 27: Malicious PR running dangerous code
- [ ] Scenario 28: Dependency injection attack
- [ ] Scenario 29: GitHub token scope issues
- [ ] Scenario 30: Third-party action compromise

---

## ⏱️ Thời lượng

**Ước tính:** 6-8 giờ

| Phần | Thời gian |
|------|-----------|
| GitHub Actions basics (Labs 1-13) | 2 giờ |
| Advanced workflows (Labs 14-25) | 1.5 giờ |
| Testing & Quality (Labs 26-37) | 1.5 giờ |
| Docker trong CI (Labs 38-47) | 1.5 giờ |
| GitLab CI & Jenkins | 1 giờ |
| Best Practices | 0.5 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
