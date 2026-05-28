# 📋 CI/CD - Cheatsheet

> **Quick Reference for GitLab CI & GitHub Actions**
>
> *Tra cứu nhanh GitLab CI & GitHub Actions*

---

## 🦊 GitLab CI (Primary - Chính)

### Basic Pipeline (Pipeline cơ bản)

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  image: node:18-alpine
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  script:
    - npm test

deploy:
  stage: deploy
  script:
    - echo "Deploying..."
  only:
    - main
  when: manual
```

### Key Syntax (Cú pháp chính)

| Keyword | Description (Mô tả) |
|---------|---------------------|
| `stages` | Define stage order (Thứ tự stages) |
| `image` | Docker image to use (Docker image sử dụng) |
| `script` | Commands to run (Các lệnh chạy) |
| `artifacts` | Files to pass between jobs (Files truyền giữa jobs) |
| `only` | Branch filter (Lọc branch) |
| `when: manual` | Require manual trigger (Cần kích hoạt thủ công) |

### Predefined Variables (Biến có sẵn)

```yaml
$CI_COMMIT_SHA           # Full commit SHA
$CI_COMMIT_SHORT_SHA     # Short commit SHA
$CI_COMMIT_BRANCH        # Branch name
$CI_PROJECT_NAME         # Project name
$CI_REGISTRY_IMAGE       # Container registry URL
```

---

## 🐙 GitHub Actions (Alternative - Thay thế)

### Basic Workflow

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install
        run: npm install
      - name: Test
        run: npm test
```

### Key Syntax

| Keyword | Description (Mô tả) |
|---------|---------------------|
| `on` | Trigger events (Sự kiện kích hoạt) |
| `jobs` | Define jobs (Định nghĩa jobs) |
| `runs-on` | Runner to use (Runner sử dụng) |
| `steps` | Steps in job (Các bước trong job) |
| `uses` | Use action (Sử dụng action) |
| `run` | Run command (Chạy lệnh) |

---

## 🔄 Comparison (So sánh)

| Feature | GitLab CI | GitHub Actions |
|---------|-----------|----------------|
| Config file | `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| Stages | `stages:` | `jobs:` + `needs:` |
| Scripts | `script:` | `run:` |
| Docker | `image:` | `container:` |
| Manual | `when: manual` | `workflow_dispatch` |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
