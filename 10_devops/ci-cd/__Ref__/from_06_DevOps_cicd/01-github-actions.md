# ⚙️ CI/CD — Tự động hóa build, test và deploy

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Nền tảng DevOps hiện đại

---

## CI/CD là gì?

**CI (Continuous Integration)** — Mỗi lần push code → tự động chạy test, lint, build.

**CD (Continuous Delivery/Deployment)**:
- **Continuous Delivery** — Tự động chuẩn bị sẵn để deploy (cần approve thủ công)
- **Continuous Deployment** — Tự động deploy thẳng lên production

```
Developer push code
        │
        ▼
  ┌─────────────┐
  │   CI Stage  │  Lint → Test → Build → Scan security
  └──────┬──────┘
         │ Pass
  ┌──────▼──────┐
  │  CD Stage   │  Build Docker → Push Registry → Deploy Staging
  └──────┬──────┘
         │ Approved
  ┌──────▼──────┐
  │  Production │  Deploy → Health check → Notify
  └─────────────┘
```

---

## GitHub Actions ⭐

### Cấu trúc workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ── Job 1: Test ─────────────────────────────────
  test:
    name: Test
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: secret
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint with ruff
        run: ruff check .

      - name: Type check with mypy
        run: mypy .

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:secret@localhost:5432/testdb
        run: pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  # ── Job 2: Build & Push Image ───────────────────
  build:
    name: Build Docker Image
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to container registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=sha-
            type=raw,value=latest

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ── Job 3: Deploy ───────────────────────────────
  deploy:
    name: Deploy to Production
    needs: build
    runs-on: ubuntu-latest
    environment: production   # Cần approval trong GitHub

    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app
            docker compose pull
            docker compose up -d --no-deps api
            docker system prune -f
            echo "✅ Deployed successfully"
```

---

## Workflow cho Node.js / TypeScript

```yaml
# .github/workflows/node-ci.yml
name: Node.js CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]  # Test nhiều Node version

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm

      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test -- --coverage
      - run: npm run build
```

---

## Workflow cho Next.js + Vercel deploy

```yaml
# .github/workflows/preview.yml
name: Preview Deployment

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  deploy-preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        id: vercel-preview
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Comment preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🚀 Preview deployed: ${{ steps.vercel-preview.outputs.preview-url }}`
            })
```

---

## Secrets Management

```bash
# GitHub Secrets — Settings → Secrets and variables → Actions
# Thêm các secrets:
SERVER_HOST         # IP/hostname của server
SERVER_USER         # SSH username
SSH_PRIVATE_KEY     # Private key (không phải public!)
DATABASE_URL        # Connection string production
JWT_SECRET          # Secret key cho JWT
```

```yaml
# Dùng secrets trong workflow
- name: Deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    JWT_SECRET: ${{ secrets.JWT_SECRET }}
  run: ./deploy.sh
```

---

## Branch Protection Rules

Cấu hình trên GitHub: Settings → Branches → Add rule

```
Branch: main
✅ Require a pull request before merging
   ✅ Require approvals: 1
   ✅ Dismiss stale reviews
✅ Require status checks to pass
   → test (job trong CI)
✅ Require branches to be up to date
✅ Do not allow bypassing the above settings
```

---

## Best Practices

```yaml
# ✅ 1. Cache dependencies
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

# ✅ 2. Fail fast — dùng matrix
strategy:
  fail-fast: true
  matrix:
    python-version: ["3.11", "3.12"]

# ✅ 3. Pin action versions (security)
uses: actions/checkout@v4    # ✅ Pinned
uses: actions/checkout@main  # ❌ Mutable

# ✅ 4. Timeout jobs
jobs:
  test:
    timeout-minutes: 15

# ✅ 5. Conditionals
if: github.ref == 'refs/heads/main' && github.event_name == 'push'

# ✅ 6. Reusable workflows
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
```

---

## Bài tập thực hành

- [ ] Tạo CI pipeline cho 1 project: lint → test → build
- [ ] Thêm CD: build Docker image và push lên registry
- [ ] Cấu hình Branch Protection trên GitHub
- [ ] Deploy tự động lên staging khi merge vào develop

---

## Tài nguyên thêm

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [act](https://github.com/nektos/act) — Chạy GitHub Actions locally để test
