# ⚙️ Module 1.7: CI/CD Basic - GitHub Actions

[![Duration](https://img.shields.io/badge/Duration-10--12%20hours-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Beginner--Intermediate-orange?style=flat-square)](.)

> **Continuous Integration / Continuous Deployment** - Automate with GitHub Actions.
>
> *Tích hợp liên tục / Triển khai liên tục với GitHub Actions.*

---

## 🔀 Platform Options (Lựa chọn nền tảng)

| Platform | Status | File |
|----------|--------|------|
| GitLab CI/CD | ⭐ **Primary (Chính)** | [README.md](./README.md) |
| **GitHub Actions** | Alternative (Thay thế) | This file |

> 💡 **Note:** This is the GitHub Actions alternative guide. For the primary GitLab CI/CD guide, see [README.md](./README.md).
>
> *Đây là hướng dẫn thay thế cho GitHub Actions. Xem hướng dẫn GitLab CI/CD chính tại README.md.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand what CI/CD is and why it's important (Hiểu CI/CD là gì và tại sao quan trọng)
- ✅ Learn concepts: Workflow, Job, Step, Artifact (Hiểu các concepts)
- ✅ Write GitHub Actions workflows (Viết workflow GitHub Actions)
- ✅ Build Docker images in pipeline (Build Docker image trong pipeline)
- ✅ Auto deploy when pushing code (Deploy tự động khi push code)

---

## 📚 Content (Nội dung)

### 1. What is CI/CD? (CI/CD là gì?) - 1 hour

> 📝 **Note:** This section is the same as in GitLab CI guide. See [README.md](./README.md#1-what-is-cicd-cicd-là-gì---1-hour) for details.
>
> *Phần này giống với hướng dẫn GitLab CI. Xem README.md để biết chi tiết.*

---

### 2. CI/CD Tools Overview (Tổng quan công cụ CI/CD) - 30 min

| Tool | Features | Use Case |
|------|----------|----------|
| **GitHub Actions** | Native GitHub, YAML (Tích hợp GitHub, YAML) | GitHub projects ⭐ |
| GitLab CI/CD | Native GitLab, powerful (Tích hợp GitLab, mạnh mẽ) | GitLab projects |
| Jenkins | Self-hosted, flexible (Tự host, linh hoạt) | Enterprise, legacy (Doanh nghiệp, cũ) |
| CircleCI | Cloud-based, fast (Trên cloud, nhanh) | Startups |
| Azure DevOps | Microsoft ecosystem (Hệ sinh thái Microsoft) | Azure, .NET |

**In this guide, we learn GitHub Actions.**

*Trong hướng dẫn này, chúng ta học GitHub Actions.*

---

### 3. GitHub Actions Fundamentals (Cơ bản GitHub Actions) - 2 hours

#### 3.1 Concepts (Khái niệm)

```
┌─────────────────────────────────────────────────────────────┐
│                GITHUB ACTIONS CONCEPTS                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WORKFLOW (.github/workflows/main.yml)                      │
│  ├── Trigger (on: push, pull_request, schedule)             │
│  │                                                           │
│  └── JOBS (runs in parallel by default - chạy song song)   │
│      ├── Job 1: build                                        │
│      │   ├── runs-on: ubuntu-latest                         │
│      │   └── STEPS                                           │
│      │       ├── Step 1: Checkout code                      │
│      │       ├── Step 2: Setup Node.js                      │
│      │       ├── Step 3: Install deps                       │
│      │       └── Step 4: Run tests                          │
│      │                                                       │
│      └── Job 2: deploy (needs: build)                       │
│          ├── runs-on: ubuntu-latest                         │
│          └── STEPS                                           │
│              ├── Step 1: Checkout                           │
│              └── Step 2: Deploy to server                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 3.2 Terminology (Thuật ngữ)

| Term | Description |
|------|-------------|
| **Workflow** | Automated process defined in YAML (Quy trình tự động trong YAML) |
| **Event** | Trigger that starts workflow - push, PR, etc. (Sự kiện kích hoạt) |
| **Job** | Set of steps that run on same runner (Tập hợp các bước) |
| **Step** | Individual task - run command or action (Bước riêng lẻ) |
| **Action** | Reusable unit - marketplace or custom (Đơn vị tái sử dụng) |
| **Runner** | Server that runs the jobs (Server chạy jobs) |
| **Artifact** | Files produced by job (Files tạo ra bởi job) |

---

### 4. Workflow Syntax (Cú pháp Workflow) - 2 hours

#### 4.1 Basic Workflow (Workflow cơ bản)

```yaml
# .github/workflows/ci.yml (đặt trong thư mục .github/workflows/)

name: CI Pipeline                    # Workflow name (Tên workflow)

on:                                   # Triggers (Kích hoạt)
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:                                 # Jobs (Các jobs)
  build:                              # Job name (Tên job)
    runs-on: ubuntu-latest            # Runner OS (Hệ điều hành runner)
    
    steps:                            # Steps (Các bước)
      - name: Checkout code
        uses: actions/checkout@v4     # Use an action (Dùng action)

      - name: Run a script
        run: echo "Hello World!"      # Run command (Chạy lệnh)

      - name: Multi-line script (Script nhiều dòng)
        run: |
          echo "Line 1"
          echo "Line 2"
          ls -la
```

#### 4.2 Triggers/Events (Kích hoạt/Sự kiện)

```yaml
on:
  # Push to specific branches (Push đến nhánh cụ thể)
  push:
    branches:
      - main
      - 'feature/**'        # Wildcard
    paths:
      - 'src/**'            # Only when src changes (Chỉ khi src thay đổi)
      - '!src/**/*.md'      # Except markdown (Ngoại trừ markdown)
    tags:
      - 'v*'                # Tags starting with v (Tags bắt đầu bằng v)

  # Pull requests
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

  # Schedule - cron syntax
  schedule:
    - cron: '0 0 * * *'     # Daily at midnight UTC (Hàng ngày lúc nửa đêm UTC)

  # Manual trigger (Kích hoạt thủ công)
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
```

#### 4.3 Jobs and Dependencies (Jobs và Dependencies)

```yaml
jobs:
  # Job 1: Build
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm run build

  # Job 2: Test (parallel with build - chạy song song với build)
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  # Job 3: Deploy (after build AND test complete - sau khi build VÀ test xong)
  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]          # Dependencies (Phụ thuộc)
    if: github.ref == 'refs/heads/main'  # Condition (Điều kiện)
    steps:
      - run: echo "Deploying..."
```

#### 4.4 Environment Variables and Secrets (Biến môi trường và Secrets)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    
    env:                           # Job-level env vars (Biến cấp job)
      NODE_ENV: production
    
    steps:
      - name: Use env vars (Sử dụng biến môi trường)
        env:                       # Step-level env vars (Biến cấp step)
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          echo "Node env: $NODE_ENV"
          echo "Running with API key..."

      - name: Use GitHub context (Sử dụng GitHub context)
        run: |
          echo "Repo: ${{ github.repository }}"
          echo "Branch: ${{ github.ref_name }}"
          echo "SHA: ${{ github.sha }}"
          echo "Actor: ${{ github.actor }}"
```

---

### 5. Common Actions (Các Actions phổ biến) - 1.5 hours

#### 5.1 Checkout Code (Lấy code)

```yaml
- name: Checkout
  uses: actions/checkout@v4
  with:
    fetch-depth: 0        # Full history for versioning (Toàn bộ lịch sử)
```

#### 5.2 Setup Languages (Cài đặt ngôn ngữ)

```yaml
# Node.js
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '18'
    cache: 'npm'

# Python
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'

# Go
- name: Setup Go
  uses: actions/setup-go@v5
  with:
    go-version: '1.21'
```

#### 5.3 Caching (Lưu cache)

```yaml
- name: Cache node_modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

#### 5.4 Upload/Download Artifacts (Tải lên/xuống Artifacts)

```yaml
# Upload artifact (Tải lên artifact)
- name: Upload build
  uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/

# Download artifact in another job (Tải xuống artifact trong job khác)
- name: Download build
  uses: actions/download-artifact@v4
  with:
    name: build-output
    path: dist/
```

---

### 6. Docker in GitHub Actions (Docker trong GitHub Actions) - 2 hours

#### 6.1 Build and Push Docker Image (Build và Push Docker Image)

```yaml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub (Đăng nhập Docker Hub)
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata (Trích xuất metadata)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myuser/myapp
          tags: |
            type=ref,event=branch
            type=ref,event=tag
            type=sha,prefix=

      - name: Build and push (Build và push)
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

### 7. Complete CI/CD Example (Ví dụ CI/CD hoàn chỉnh) - 2 hours

#### 7.1 Static Website CI/CD (CI/CD cho Website tĩnh)

```yaml
# .github/workflows/deploy.yml - Complete example (Ví dụ hoàn chỉnh)

name: Deploy Static Website

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # Job 1: Build (Giai đoạn build)
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies (Cài đặt dependencies)
        run: npm ci

      - name: Run linting (Chạy linting)
        run: npm run lint

      - name: Run tests (Chạy tests)
        run: npm test

      - name: Build
        run: npm run build

      - name: Upload build artifact (Tải lên artifact)
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  # Job 2: Deploy - only on main branch (Triển khai - chỉ trên nhánh main)
  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    environment:
      name: production
      url: https://example.com
    
    steps:
      - name: Download artifact (Tải xuống artifact)
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Deploy to GitHub Pages (Triển khai lên GitHub Pages)
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

### 8. Best Practices (Các thực hành tốt nhất) - 1 hour

#### 8.1 Security (Bảo mật)

```yaml
# Use specific versions (Dùng phiên bản cụ thể)
- uses: actions/checkout@v4.1.1  # Don't use @main (Không dùng @main)

# Limit permissions (Giới hạn quyền)
permissions:
  contents: read
  packages: write

# Use secrets properly (Sử dụng secrets đúng cách)
env:
  API_KEY: ${{ secrets.API_KEY }}

# Don't log secrets (Không log secrets)
run: |
  # ❌ Bad
  echo ${{ secrets.API_KEY }}
  
  # ✅ Good
  echo "Using API key..."
```

#### 8.2 Performance (Hiệu suất)

```yaml
# Use caching (Sử dụng caching)
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

# Fail fast (Dừng ngay khi lỗi)
strategy:
  fail-fast: true

# Set timeout (Đặt timeout)
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
```

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|-------------|
| [README.md](./README.md) | GitLab CI/CD primary guide (Hướng dẫn GitLab CI/CD chính) |
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

## 🔗 Resources (Tài nguyên)

### Official Documentation (Tài liệu chính thức)

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Marketplace - Actions](https://github.com/marketplace?type=actions)

### Free GitHub Actions Minutes (Phút miễn phí)

- Public repos: **Unlimited** (Không giới hạn cho repo công khai)
- Private repos: **2,000 minutes/month** on free tier (2000 phút/tháng miễn phí)

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:----------:|:-------:|:------:|
| [1.6 NGINX](../1.6_NGINX_Basic/) | **1.7 CI/CD** | [1.8 Capstone](../1.8_Capstone_Project/) |

---

**Master CI/CD with GitHub Actions! ⚙️**

*Thành thạo CI/CD với GitHub Actions!*

</div>
