# 💪 Exercises: CI/CD Basic

> **Self-practice exercises for GitLab CI/CD**
>
> *Bài tập tự luyện GitLab CI/CD.*

---

## 📋 Overview (Tổng quan)

Complete these exercises to master GitLab CI/CD concepts.

*Hoàn thành các bài tập để thành thạo GitLab CI/CD.*

---

## Exercise 1: Basic Pipeline ⭐

Create a basic GitLab CI pipeline.

*Tạo pipeline GitLab CI cơ bản.*

### Requirements (Yêu cầu)

1. Create `.gitlab-ci.yml`
2. Add a `hello` stage
3. Print "Hello GitLab CI!" (In "Hello GitLab CI!")
4. Show current date and time (Hiển thị ngày giờ hiện tại)
5. Display commit info using CI variables (Hiển thị thông tin commit)

### Expected variables (Biến cần sử dụng)

- `$CI_COMMIT_SHA`
- `$CI_COMMIT_MESSAGE`
- `$CI_PROJECT_NAME`

---

## Exercise 2: Node.js CI Pipeline ⭐⭐

Create a CI pipeline for a Node.js application.

*Tạo CI pipeline cho ứng dụng Node.js.*

### Requirements (Yêu cầu)

1. Use `node:18-alpine` image (Sử dụng image `node:18-alpine`)
2. Install dependencies with `npm ci`
3. Run linting (Chạy linting)
4. Run unit tests (Chạy unit tests)
5. Upload coverage report as artifact (Upload báo cáo coverage)
6. Set up coverage extraction (Cấu hình extraction coverage)

### Hints (Gợi ý)

- Use `coverage` keyword for regex
- Use `artifacts.reports.coverage_report`

---

## Exercise 3: Docker Build ⭐⭐

Create a pipeline to build and push Docker images.

*Tạo pipeline để build và push Docker images.*

### Requirements (Yêu cầu)

1. Build Docker image (Build Docker image)
2. Tag with commit SHA (Gắn tag với commit SHA)
3. Push to GitLab Container Registry (Push lên GitLab Registry)
4. Add a second tag `latest` for main branch (Thêm tag `latest` cho branch main)

### Hints (Gợi ý)

- Use `docker:24` image with `docker:24-dind` service
- Use `$CI_REGISTRY_IMAGE` for image name
- Use `rules` or `only/except` for branch conditions

---

## Exercise 4: Multi-Stage Pipeline ⭐⭐

Create a pipeline with multiple stages and dependencies.

*Tạo pipeline với nhiều stages và dependencies.*

### Requirements (Yêu cầu)

1. Create 4 stages: lint, test, build, deploy (Tạo 4 stages)
2. Lint job runs first (Lint job chạy đầu tiên)
3. Test jobs run after lint (Test jobs chạy sau lint)
4. Build job runs after tests pass (Build job chạy sau khi tests pass)
5. Deploy job requires manual approval (Deploy job yêu cầu approval thủ công)
6. Use `needs` for job dependencies (Sử dụng `needs` cho dependencies)

### Hints (Gợi ý)

- Use `needs: ["job-name"]` for dependencies
- Use `when: manual` for manual trigger

---

## Exercise 5: Environment Deployment ⭐⭐⭐

Create a deployment pipeline with environments.

*Tạo pipeline triển khai với environments.*

### Requirements (Yêu cầu)

1. Deploy to staging automatically on main (Tự động deploy staging trên main)
2. Deploy to production with manual approval (Deploy production với approval)
3. Configure environment URLs (Cấu hình URLs cho environments)
4. Use GitLab CI/CD variables for secrets (Dùng variables cho secrets)
5. Add deployment notification (Thêm thông báo deployment)

### Hints (Gợi ý)

- Use `environment` keyword
- Configure variables in Settings > CI/CD > Variables
- Use `after_script` for notifications

---

## Exercise 6: Caching & Optimization ⭐⭐⭐

Optimize pipeline performance with caching.

*Tối ưu hiệu suất pipeline với caching.*

### Requirements (Yêu cầu)

1. Cache `node_modules` directory (Cache thư mục `node_modules`)
2. Cache Docker layers (Cache Docker layers)
3. Use cache key based on lock file (Dùng cache key dựa trên lock file)
4. Measure pipeline time improvement (Đo thời gian cải thiện)

### Hints (Gợi ý)

```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
```

---

## Exercise 7: Scheduled Pipeline ⭐⭐

Create a scheduled pipeline for regular tasks.

*Tạo pipeline theo lịch cho các tác vụ định kỳ.*

### Requirements (Yêu cầu)

1. Create a security scan job (Tạo job quét bảo mật)
2. Run dependency audit (Chạy kiểm tra dependencies)
3. Configure schedule in GitLab UI (Cấu hình lịch trong GitLab UI)
4. Send notification if issues found (Gửi thông báo nếu có vấn đề)

### How to set up schedule (Cách cấu hình lịch)

1. Go to **CI/CD > Schedules** (Vào CI/CD > Schedules)
2. Click **New schedule** (Click New schedule)
3. Set cron expression (e.g., `0 0 * * *` for daily)
4. Select branch and save (Chọn branch và lưu)

### Hints (Gợi ý)

- Use `rules: - if: $CI_PIPELINE_SOURCE == "schedule"`
- Use `npm audit` for Node.js projects

---

## 📝 Exercise Checklist (Danh sách bài tập)

- [ ] Exercise 1: Basic Pipeline ⭐
- [ ] Exercise 2: Node.js CI Pipeline ⭐⭐
- [ ] Exercise 3: Docker Build ⭐⭐
- [ ] Exercise 4: Multi-Stage Pipeline ⭐⭐
- [ ] Exercise 5: Environment Deployment ⭐⭐⭐
- [ ] Exercise 6: Caching & Optimization ⭐⭐⭐
- [ ] Exercise 7: Scheduled Pipeline ⭐⭐

---

## ⭐ Difficulty Levels (Mức độ khó)

| Level | Description (Mô tả) |
|-------|---------------------|
| ⭐ | Beginner - Basic concepts (Cơ bản) |
| ⭐⭐ | Intermediate - Multiple features (Trung bình) |
| ⭐⭐⭐ | Advanced - Complex scenarios (Nâng cao) |

---

**[← Back to README](./README.md)** | **[View Solutions →](./SOLUTIONS.md)**
