# 🎯 Project: CI/CD Basic

> **Mini Project: Complete CI/CD Pipeline with GitLab CI**
>
> *Dự án nhỏ: Pipeline CI/CD hoàn chỉnh với GitLab CI*

---

## 📋 Project Overview (Tổng quan dự án)

### Project Name: **Full CI/CD Pipeline Implementation**

Build a complete CI/CD pipeline using GitLab CI.

*Xây dựng pipeline CI/CD hoàn chỉnh sử dụng GitLab CI.*

### Duration (Thời gian): 2-3 days (2-3 ngày)

---

## 🎯 Requirements (Yêu cầu)

### Pipeline Stages (Các giai đoạn)

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Lint   │ -> │  Test   │ -> │  Build  │ -> │ Deploy  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### Features (Tính năng)

#### 1. Code Quality (Chất lượng code)

- Linting (ESLint/Prettier)
- Code formatting check (Kiểm tra định dạng code)
- Security scanning (Quét bảo mật)

#### 2. Testing

- Unit tests
- Integration tests (optional)
- Coverage report (Báo cáo coverage)
- Test result artifacts

#### 3. Build

- Docker image build
- Image tagging with version (Gắn tag version cho image)
- Image scanning (Quét image)
- Push to GitLab Container Registry

#### 4. Deployment (Triển khai)

- Deploy to staging (auto) - Tự động deploy staging
- Deploy to production (manual approval) - Deploy production cần approval
- Rollback capability (Khả năng rollback)
- Deployment notifications (Thông báo deployment)

---

## 📁 Project Structure (Cấu trúc dự án)

```
cicd-project/
├── .gitlab-ci.yml           # Main pipeline config
├── src/                     # Source code
├── tests/                   # Test files
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Local development
├── package.json             # Node.js dependencies
└── README.md                # Project documentation
```

---

## 📊 Expected Pipeline Configuration

### .gitlab-ci.yml

```yaml
# .gitlab-ci.yml - Main pipeline configuration

stages:
  - lint
  - test
  - build
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# ============= LINT STAGE =============
lint:
  stage: lint
  image: node:18-alpine
  script:
    - npm ci
    - npm run lint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

# ============= TEST STAGE =============
test:
  stage: test
  image: node:18-alpine
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    when: always
    paths:
      - coverage/
    reports:
      junit: junit.xml
  needs:
    - lint

# ============= BUILD STAGE =============
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $IMAGE_TAG
    - docker push $CI_REGISTRY_IMAGE:latest
  needs:
    - test
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# ============= DEPLOY STAGE =============
deploy-staging:
  stage: deploy
  image: alpine:latest
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - echo "Deploying to staging..."
    # Add your deployment commands here
  needs:
    - build
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

deploy-production:
  stage: deploy
  image: alpine:latest
  environment:
    name: production
    url: https://example.com
  script:
    - echo "Deploying to production..."
    # Add your deployment commands here
  needs:
    - deploy-staging
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

---

## 🔒 CI/CD Variables Setup (Cấu hình Variables)

Configure these variables in **Settings > CI/CD > Variables**:

*Cấu hình các variables này trong **Settings > CI/CD > Variables**:*

| Variable | Type | Description (Mô tả) |
|----------|------|---------------------|
| `SSH_PRIVATE_KEY` | File | SSH key for deployment |
| `STAGING_HOST` | Variable | Staging server address |
| `PROD_HOST` | Variable | Production server address |
| `SLACK_WEBHOOK` | Variable | Slack notification URL (optional) |

---

## ✅ Deliverables (Sản phẩm bàn giao)

### Required (Bắt buộc)

- [ ] `.gitlab-ci.yml` with all stages (với tất cả stages)
- [ ] CI pipeline working (lint, test, build) - Pipeline CI hoạt động
- [ ] CD pipeline working (staging, production) - Pipeline CD hoạt động
- [ ] Docker build & push to GitLab Registry
- [ ] Environment protection for production (Bảo vệ môi trường production)
- [ ] Variables properly configured (Variables được cấu hình đúng)

### Optional (Tùy chọn)

- [ ] Status badges in README (Badges trạng thái)
- [ ] Slack/Discord notifications (Thông báo)
- [ ] Security scanning with Trivy/SAST
- [ ] Performance testing (Kiểm tra hiệu suất)
- [ ] Documentation (Tài liệu)

---

## 📊 Evaluation (Đánh giá)

| Criteria (Tiêu chí) | Points (Điểm) |
|---------------------|---------------|
| CI Pipeline working (Pipeline CI hoạt động) | 30 |
| CD Pipeline working (Pipeline CD hoạt động) | 30 |
| Docker integration (Tích hợp Docker) | 15 |
| Security measures (Biện pháp bảo mật) | 15 |
| Documentation (Tài liệu) | 10 |
| **Total** | **100** |

---

## 📚 Resources (Tài liệu tham khảo)

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [GitLab Environments](https://docs.gitlab.com/ee/ci/environments/)
- [CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)

---

## 💡 Tips (Mẹo)

1. **Start simple**: Begin with a basic pipeline and add complexity gradually.

   *Bắt đầu đơn giản: Bắt đầu với pipeline cơ bản và thêm dần complexity.*

2. **Use caching**: Cache `node_modules` to speed up builds.

   *Sử dụng caching: Cache `node_modules` để tăng tốc builds.*

3. **Test locally**: Use `gitlab-runner exec` to test locally before pushing.

   *Test local: Dùng `gitlab-runner exec` để test trước khi push.*

4. **Check logs**: Always check job logs when something fails.

   *Kiểm tra logs: Luôn kiểm tra logs khi có lỗi.*

---

**Good luck! 🚀**

*Chúc may mắn!*

---

**[← Back to README](./README.md)** | **[View Labs →](./LABS.md)**
