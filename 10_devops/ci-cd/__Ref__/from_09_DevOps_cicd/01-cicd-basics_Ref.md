# 🔄 CI/CD — Tự động hóa build, test, deploy

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Nền tảng DevOps hiện đại

---

## Tại sao cần CI/CD?

```
❌ Không có CI/CD:
Developer commit → Quên test → Deploy thủ công → Bug production → Fix gấp → Lại quên test → 💀

✅ Có CI/CD:
Developer commit → Auto test → Auto build → Auto deploy → Mọi thứ OK → 🎉
```

**CI** (Continuous Integration): Mỗi commit tự động build + test  
**CD** (Continuous Delivery/Deployment): Tự động deploy lên staging/production

---

## 1. Pipeline — Luồng CI/CD

```
┌────────┐    ┌──────┐    ┌──────┐    ┌────────┐    ┌──────────┐
│  Code  │───►│ Build│───►│ Test │───►│ Deploy │───►│Production│
│ (push) │    │      │    │      │    │Staging │    │          │
└────────┘    └──────┘    └──────┘    └────────┘    └──────────┘
                 │            │            │
                 ▼            ▼            ▼
              Fail? ───► Notify developer
              Pass? ───► Tiếp tục ──────►
```

---

## 2. GitHub Actions — CI/CD phổ biến nhất

### Cấu trúc cơ bản

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

# Khi nào chạy?
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Job 1: Test
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20]     # Test trên nhiều Node versions

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

### Build + Deploy

```yaml
  # Job 2: Build Docker image
  build:
    needs: test                     # Chỉ chạy sau test pass
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'  # Chỉ trên main

    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: myapp:${{ github.sha }}

  # Job 3: Deploy
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production         # Cần approval

    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            docker pull myapp:${{ github.sha }}
            docker stop myapp || true
            docker run -d --name myapp -p 80:3000 myapp:${{ github.sha }}
```

---

## 3. Ví dụ thực tế

### Python + pytest

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:                     # Service container
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/test_db
        run: pytest --cov=app --cov-report=xml

      - name: Check coverage
        run: |
          coverage=$(python -c "import xml.etree.ElementTree as ET; print(ET.parse('coverage.xml').getroot().attrib['line-rate'])")
          echo "Coverage: $coverage"
```

### Next.js + Vercel

```yaml
name: Preview Deploy

on:
  pull_request:
    branches: [main]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm i -g vercel@latest

      - name: Deploy Preview
        run: vercel --token=${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## 4. Secrets — Quản lý bí mật

```bash
# GitHub: Settings → Secrets → Actions
# Thêm secrets qua UI hoặc CLI:
gh secret set DOCKER_TOKEN

# Sử dụng trong workflow:
${{ secrets.DOCKER_TOKEN }}

# ⚠️ KHÔNG BAO GIỜ hardcode secrets trong workflow file!
```

---

## 5. So sánh CI/CD Tools

| Tool | Hosting | Đặc điểm | Free tier |
|---|---|---|---|
| **GitHub Actions** | Cloud | Tích hợp GitHub, marketplace lớn | 2000 min/month |
| **GitLab CI** | Cloud/Self | Tích hợp GitLab, powerful | 400 min/month |
| **Jenkins** | Self-hosted | Linh hoạt nhất, plugin nhiều | Free (tự host) |
| **CircleCI** | Cloud | Nhanh, config dễ | 6000 min/month |
| **Vercel** | Cloud | Next.js deploy tự động | Free cho cá nhân |
| **Netlify** | Cloud | Static sites, serverless | Free tier |

---

## 6. Best Practices

```yaml
# ✅ Cache dependencies — tăng tốc 3-5x
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

# ✅ Fail fast — dừng ngay khi có lỗi
strategy:
  fail-fast: true

# ✅ Timeout — tránh workflow chạy vô hạn
jobs:
  test:
    timeout-minutes: 10

# ✅ Concurrency — cancel workflow cũ khi có push mới
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

---

## Các lỗi thường gặp

```
❌ Sai: Chạy tất cả tests trên mỗi push → chậm, tốn tiền
✅ Đúng: Push → fast tests, PR → full tests, merge → deploy

❌ Sai: Deploy trực tiếp lên production không qua staging
✅ Đúng: main → staging → manual approval → production

❌ Sai: Secrets trong code / commit history
✅ Đúng: Dùng GitHub Secrets, KHÔNG commit .env
```

---

## Bài tập thực hành

- [ ] Tạo GitHub Actions workflow: lint + test cho 1 project Node.js
- [ ] Thêm Docker build + push lên Docker Hub khi merge vào main
- [ ] Setup matrix testing (Node 18, 20 + OS ubuntu, macos)
- [ ] Tạo deploy workflow với manual approval cho production

---

## Tài nguyên thêm

- [GitHub Actions Docs](https://docs.github.com/en/actions) — Official
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) — Actions có sẵn
- [CI/CD Pipeline Tutorial](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment) — Atlassian
