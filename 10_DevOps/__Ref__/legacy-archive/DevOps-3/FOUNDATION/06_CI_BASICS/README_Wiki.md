# Module 06: CI BASICS - Continuous Integration với GitHub Actions

> **Thời gian học:** 2 tuần
>
> **Prerequisite:** Module 02 (Git/GitHub), Module 05 (Docker)
>
> **Difficulty:** ⭐⭐⭐⭐☆

---

## 📋 Mục lục

1. [CI/CD là gì?](#1-cicd-là-gì)
2. [GitHub Actions Fundamentals](#2-github-actions-fundamentals)
3. [Workflow Syntax](#3-workflow-syntax)
4. [Build & Test Automation](#4-build--test-automation)
5. [Docker Build trong CI](#5-docker-build-trong-ci)
6. [Secrets Management](#6-secrets-management)
7. [Advanced Workflows](#7-advanced-workflows)
8. [Best Practices](#8-best-practices)
9. [Troubleshooting](#9-troubleshooting)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **CI/CD pipeline** và lợi ích của automation
- ✅ Nắm vững **GitHub Actions** architecture
- ✅ Viết **YAML workflows** để automate tasks
- ✅ Setup **automated testing** cho mọi commit
- ✅ **Build Docker images** tự động trong CI
- ✅ **Push images** lên Docker Hub
- ✅ Quản lý **secrets** an toàn
- ✅ Debug workflow **failures**
- ✅ Tạo **badge** hiển thị build status

---

## 1. CI/CD là gì?

### 1.1. Vấn đề khi không có CI/CD

**Traditional development workflow:**

```
Developer A:
1. Code feature trong 2 tuần
2. Cuối tuần 2: git push
3. QA test: phát hiện 50 bugs ❌
4. Developer A quên code đã viết thế nào
5. Fix mất 1 tuần nữa
6. Deploy manual: SSH vào server, copy files, restart
7. Deploy fail: "Forgot to install library!"
8. Production down 2 hours ❌

Developer B cùng lúc:
- Cũng code 2 tuần
- Push cùng ngày
- Merge conflicts khủng khiếp ❌
- Integration hell! (địa ngục tích hợp)
```

**Problems (vấn đề):**

- ❌ **Late feedback** - Bugs phát hiện quá muộn
- ❌ **Integration problems** - Code của nhiều devs conflict
- ❌ **Manual testing** - Chậm, dễ miss bugs
- ❌ **Manual deployment** - Error-prone, không consistent
- ❌ **No rollback** - Nếu deploy lỗi thì sao?
- ❌ **Fear of deployment** - Deploy = stressful event

### 1.2. CI/CD Solution

**CI/CD = Continuous Integration / Continuous Delivery (Deployment)**

#### Continuous Integration (CI)

**Định nghĩa:**
Tự động **build, test** code mỗi khi có commit/push.

**Workflow:**

```
Developer push code
     ↓
CI server detect push
     ↓
Automatically:
├── Checkout code
├── Install dependencies
├── Run tests
├── Build application
└── Report results (✅ or ❌)

If ❌: Email/Slack notification → Fix ngay!
If ✅: Code ready to merge
```

**Benefits:**

- ✅ **Early bug detection** - Bugs catch trong minutes, không phải weeks
- ✅ **Always integrat**ed - Mọi người push thường xuyên, ít conflicts
- ✅ **Automated testing** - Không skip tests
- ✅ **Fast feedback** - Devs biết code broken ngay lập tức

#### Continuous Delivery (CD)

**Định nghĩa:**
Code luôn sẵn sàng deploy, nhưng **cần manual approval**.

**Workflow:**

```
CI pass ✅
     ↓
Build artifacts (Docker image, .jar, .zip)
     ↓  
Push to registry/storage
     ↓
WAIT for manual approval
     ↓
[Manager clicks "Deploy to Production"]
     ↓
Deploy to production
```

#### Continuous Deployment (CD)

**Định nghĩa:**
Tự động deploy lên production **không cần approval**.

**Workflow:**

```
CI pass ✅
     ↓
Automatically:
├── Build artifacts
├── Deploy to staging
├── Run integration tests
├── Deploy to production
└── Monitor

Rollback tự động nếu metrics abnormal
```

**Continuous Delivery vs Deployment:**

```
Delivery:    CI → Build → [WAIT] → Deploy
                              ↑
                         Human approval

Deployment:  CI → Build → Deploy (fully automated)
```

### 1.3. CI/CD Tools Landscape

**Phổ biến:**

| Tool | Type | Hosting | Pros | Cons |
|------|------|---------|------|------|
| **GitHub Actions** | CI/CD | Cloud (GitHub) | Free, tight Git integration | Chỉ cho GitHub repos |
| **GitLab CI** | CI/CD | Cloud/Self-hosted | Powerful, built-in | Phức tạp hơn |
| **Jenkins** | CI/CD | Self-hosted | Free, plugin-rich | Cần maintain server |
| **CircleCI** | CI/CD | Cloud | Fast, good Docker support | Paid tiers |
| **Travis CI** | CI/CD | Cloud | Simple, OSS friendly | Slow builds |
| **Azure Pipelines** | CI/CD | Cloud | Good Windows support | Microsoft ecosystem |

**Lựa chọn cho course:**

- **GitHub Actions** - Vì:
  - ✅ Free cho public repos
  - ✅ Dễ setup (no infrastructure)
  - ✅ YAML syntax đơn giản
  - ✅ Marketplace với hàng ngàn actions có sẵn
  - ✅ Tích hợp sâu với GitHub (issues, PRs, releases)

### 1.4. Use Cases trong DevOps

**1. Automated Testing:**

```yaml
Every push:
├── Run unit tests
├── Run integration tests
├── Run linting (code style check)
└── Fail build nếu any test fails
```

**2. Docker Image Building:**

```yaml
When push to main:
├── Build Docker image
├── Tag with version
├── Push to Docker Hub
└── Update production deployment
```

**3. Documentation Deployment:**

```yaml
When docs/ folder changes:
├── Build static site (Hugo, Jekyll)
├── Deploy to GitHub Pages
└── Update API docs
```

**4. Security Scanning:**

```yaml
Daily or on push:
├── Scan dependencies for vulnerabilities
├── Check for secrets in code
├── Run SAST (Static Application Security Testing)
└── Report issues
```

**5. Multi-Environment Deployment:**

```yaml
Push to develop branch → Deploy to dev environment
Push to staging branch → Deploy to staging
Push to main branch → Deploy to production
```

---

## 2. GitHub Actions Fundamentals

### 2.1. Architecture

**Components:**

```
┌─────────────────────────────────────────────────┐
│  GitHub Repository                              │
│  ├── .github/workflows/                         │
│  │   ├── ci.yml        ← Workflow definitions   │
│  │   └── deploy.yml                             │
│  └── Code...                                     │
└──────────────┬──────────────────────────────────┘
               │
               │ Trigger (push, PR, schedule...)
               ↓
┌─────────────────────────────────────────────────┐
│  GitHub Actions (SaaS)                          │
│  ┌───────────────────────────────────────────┐  │
│  │  Workflow Runner (Virtual Machine)        │  │
│  │  ├── Ubuntu 22.04 / Windows / macOS      │  │
│  │  ├── Pre-installed tools: Git, Node, ... │  │
│  │  └── Run jobs & steps                    │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Workflow = YAML file định nghĩa automation**

**Hierarchy:**

```
Workflow (1 YAML file)
└── Jobs (chạy parallel hoặc sequential)
    └── Steps (sequential trong job)
        └── Actions (reusable tasks)
```

**Example structure:**

```yaml
name: CI Workflow

on: [push]  # Trigger

jobs:
  build:  # Job 1
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3  # Step 1: Action
      - name: Run tests            # Step 2: Command
        run: npm test

  deploy:  # Job 2 (depends on build)
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying..."
```

### 2.2. Where Workflows Live

**Location:** `.github/workflows/` directory

```
my-repo/
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI pipeline
│       ├── deploy.yml       # Deployment
│       └── security.yml     # Security scans
├── src/
│   └── app.py
└── README.md
```

**GitHub auto-detects** YAML files trong `.github/workflows/` và runs them!

### 2.3. Runners

**Runner = Server chạy workflows**

**GitHub-hosted runners (free tiers):**

- Ubuntu (22.04, 20.04)
- Windows Server 2022
- macOS (12, 11)

**Specs của free runners:**

- 2-core CPU
- 7 GB RAM
- 14 GB SSD

**Usage limits (free tier):**

- Public repos: **Unlimited** minutes ✅
- Private repos: **2,000 minutes/month**

**Self-hosted runners:**

- Bạn cung cấp infrastructure
- Không giới hạn minutes
- Can access internal resources
- Setup: Settings → Actions → Runners → Add runner

---

## 3. Workflow Syntax

### 3.1. Basic Structure

**Minimal workflow:**

```yaml
# .github/workflows/hello.yml
name: Hello World  # Workflow name (hiển thị trên GitHub)

on: push  # Trigger event

jobs:
  greet:  # Job ID
    runs-on: ubuntu-latest  # Runner OS
    
    steps:
      - name: Say hello  # Step name
        run: echo "Hello, GitHub Actions!"
```

**Khi push:**

```bash
git add .github/workflows/hello.yml
git commit -m "Add workflow"
git push
```

**GitHub sẽ:**

1. Detect workflow file
2. Spin up Ubuntu VM
3. Run `echo "Hello, GitHub Actions!"`
4. Report results trong "Actions" tab

### 3.2. Triggers (Events)

**Common triggers:**

```yaml
# Single event
on: push

# Multiple events
on: [push, pull_request]

# Specific branches
on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

# Specific paths
on:
  push:
    paths:
      - 'src/**'
      - '!docs/**'  # Ignore docs changes

# Scheduled (cron syntax)
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

# Manual trigger (workflow_dispatch)
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'

# Multiple triggers combined
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:
```

**Cron syntax quick reference:**

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, 0=Sunday)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)

Examples:
'0 */2 * * *'   # Every 2 hours
'0 0 * * 1'     # Every Monday at midnight
'30 5 * * 1-5'  # Weekdays at 5:30 AM
```

### 3.3. Jobs

**Sequential jobs (default - chạy parallel):**

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Job 1"
  
  job2:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Job 2"

# job1 và job2 chạy cùng lúc
```

**Sequential with dependencies:**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
  
  test:
    needs: build  # Chờ build xong
    runs-on: ubuntu-latest
    steps:
      - run: npm test
  
  deploy:
    needs: [build, test]  # Chờ cả 2 xong
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

**Visual:**

```
Parallel:
build ──┐
        ├─→ [Both run cùng lúc]
test ───┘

Sequential:
build → test → deploy
```

**Matrix strategy (chạy với nhiều versions):**

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [14, 16, 18]
    
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
      - run: npm test

# Tạo 3 × 3 = 9 jobs chạy parallel!
# ubuntu+node14, ubuntu+node16, ..., macos+node18
```

### 3.4. Steps

**Checkout code:**

```yaml
steps:
  - uses: actions/checkout@v3  # Clone repo vào runner
```

**Run commands:**

```yaml
steps:
  - name: Install dependencies
    run: npm install
  
  - name: Run multi-line script
    run: |
      echo "Line 1"
      echo "Line 2"
      npm test
```

**Use actions từ Marketplace:**

```yaml
steps:
  - name: Setup Node.js
    uses: actions/setup-node@v3
    with:
      node-version: '18'
  
  - name: Setup Python
    uses: actions/setup-python@v4
    with:
      python-version: '3.11'
```

**Conditional steps:**

```yaml
steps:
  - name: Run only on main branch
    if: github.ref == 'refs/heads/main'
    run: echo "This is main branch"
  
  - name: Run only on Linux
    if: runner.os == 'Linux'
    run: echo "Running on Linux"
```

**Environment variables:**

```yaml
steps:
  - name: Set env var
    run: echo "DEPLOY_PATH=/var/www" >> $GITHUB_ENV
  
  - name: Use env var
    run: echo "Deploying to $DEPLOY_PATH"
```

### 3.5. Context & Expressions

**Built-in contexts:**

```yaml
steps:
  - name: Print contexts
    run: |
      echo "Repository: ${{ github.repository }}"
      echo "Branch: ${{ github.ref }}"
      echo "Commit SHA: ${{ github.sha }}"
      echo "Actor: ${{ github.actor }}"
      echo "Event: ${{ github.event_name }}"
      echo "Runner OS: ${{ runner.os }}"

# Output example:
# Repository: username/repo-name
# Branch: refs/heads/main
# Commit SHA: abc123def456...
# Actor: username
# Event: push
# Runner OS: Linux
```

**Expressions:**

```yaml
steps:
  - name: Check if production
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    run: echo "Deploying to production"
  
  - name: Check PR status
    if: github.event_name == 'pull_request' && github.event.pull_request.merged == true
    run: echo "PR was merged"
```

**Functions:**

```yaml
steps:
  - name: Check if contains text
    if: contains(github.event.head_commit.message, '[skip ci]')
    run: echo "Skipping CI"
  
  - name: Success handler
    if: success()
    run: echo "Previous steps succeeded"
  
  - name: Failure handler
    if: failure()
    run: echo "Previous step failed"
  
  - name: Always run
    if: always()
    run: echo "Runs regardless of success/failure"
```

---

## 4. Build & Test Automation

### 4.1. NodeJS App Example

**Project structure:**

```
my-node-app/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── app.js
│   └── utils.js
├── tests/
│   └── app.test.js
├── package.json
└── README.md
```

**package.json:**

```json
{
  "name": "my-app",
  "scripts": {
    "test": "jest",
    "lint": "eslint src/",
    "build": "webpack --mode production"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "webpack": "^5.0.0"
  }
}
```

**CI Workflow:**

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
      # 1. Checkout code
      - name: Checkout repository
        uses: actions/checkout@v3
      
      # 2. Setup Node.js
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'  # Cache node_modules
      
      # 3. Install dependencies
      - name: Install dependencies
        run: npm ci  # Faster than npm install, uses package-lock.json
      
      # 4. Run linter
      - name: Run ESLint
        run: npm run lint
      
      # 5. Run tests
      - name: Run tests
        run: npm test
      
      # 6. Build
      - name: Build application
        run: npm run build
      
      # 7. Upload artifacts
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-${{ matrix.node-version }}
          path: dist/
```

**Execution flow:**

```
Push to GitHub
     ↓
Workflow triggers
     ↓
Spin up 3 runners (parallel):
├── Runner 1: Node 16
├── Runner 2: Node 18
└── Runner 3: Node 20

Each runner:
1. Checkout code (5s)
2. Setup Node.js (10s)
3. npm ci (30s)
4. Lint code (5s)
5. Run tests (20s)
6. Build (15s)
7. Upload artifacts (5s)

Total: ~90s per runner
All 3 finish: ~90s (not 270s, because parallel!)
```

### 4.2. Python App Example

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
      
      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      
      - name: Test with pytest
        run: |
          pytest --cov=src tests/ --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### 4.3. Test Reports & Coverage

**Generate test reports:**

```yaml
- name: Run tests with coverage
  run: npm test -- --coverage --coverageReporters=json-summary

- name: Create coverage badge
  if: github.ref == 'refs/heads/main'
  run: |
    COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
    echo "Coverage: $COVERAGE%"
```

**Badge trong README:**

```markdown
![CI](https://github.com/username/repo/workflows/CI/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-green)
```

---

## 5. Docker Build trong CI

### 5.1. Build & Push Docker Image

**Workflow:**

```yaml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags:
      - 'v*'  # v1.0, v2.1, etc.

jobs:
  docker:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: username/my-app
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=username/my-app:latest
          cache-to: type=inline
```

**Tags generated:**

```
Push to main branch:
→ username/my-app:main

Push tag v1.2.3:
→ username/my-app:v1.2.3
→ username/my-app:1.2
→ username/my-app:sha-abc123
```

### 5.2. Multi-Platform Build

```yaml
- name: Build for multiple platforms
  uses: docker/build-push-action@v4
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: username/my-app:latest
```

**Platforms supported:**

- `linux/amd64` - Intel/AMD (most servers)
- `linux/arm64` - ARM (Raspberry Pi, M1 Macs, AWS Graviton)
- `linux/arm/v7` - Older ARM devices

### 5.3. Scan for Vulnerabilities

```yaml
- name: Run Trivy scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: username/my-app:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload Trivy results to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

---

## 6. Secrets Management

### 6.1. GitHub Secrets

**Add secrets:**

```
GitHub repo → Settings → Secrets and variables → Actions → New repository secret

Name: DOCKER_PASSWORD
Value: your-docker-hub-token
```

**Use trong workflow:**

```yaml
steps:
  - name: Login to Docker Hub
    run: |
      echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
```

**Best practices:**

- ✅ Never hardcode secrets trong workflow
- ✅ Use repository secrets for repo-specific
- ✅ Use organization secrets for shared across repos
- ✅ Use environment secrets for production keys
- ✅ Rotate secrets regularly

**Secret types:**

| Level | Scope | Use case |
|-------|-------|----------|
| **Repository** | Single repo | API keys cho repo này |
| **Environment** | Specific environment (prod, staging) | Production DB password |
| **Organization** | All repos trong org | Shared Docker Hub account |

### 6.2. Environment Protection

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying with secret: ${{ secrets.PROD_API_KEY }}"
```

**Environment settings:**

- Required reviewers (cần approval trước khi deploy)
- Wait timer (delay 10 minutes trước khi deploy)
- Deployment branches (chỉ main branch được deploy)

---

## 7. Advanced Workflows

### 7.1. Reusable Workflows

**Define reusable workflow:**

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
```

**Call reusable workflow:**

```yaml
# .github/workflows/ci.yml
name: CI

on: [push]

jobs:
  test-node-16:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '16'
  
  test-node-18:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '18'
```

### 7.2. Composite Actions

**Create custom action:**

```yaml
# .github/actions/setup-app/action.yml
name: 'Setup Application'
description: 'Install dependencies and build app'

inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '18'

runs:
  using: "composite"
  steps:
    - uses: actions/setup-node@v3
      with:
        node-version: ${{ inputs.node-version }}
    
    - run: npm ci
      shell: bash
    
    - run: npm run build
      shell: bash
```

**Use custom action:**

```yaml
steps:
  - uses: actions/checkout@v3
  - uses: ./.github/actions/setup-app
    with:
      node-version: '18'
```

### 7.3. Monorepo Support

**Trigger only khi specific paths change:**

```yaml
on:
  push:
    paths:
      - 'packages/frontend/**'

jobs:
  build-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build frontend
        run: |
          cd packages/frontend
          npm ci
          npm run build
```

**Use path filters action:**

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      frontend: ${{ steps.filter.outputs.frontend }}
      backend: ${{ steps.filter.outputs.backend }}
    steps:
      - uses: actions/checkout@v3
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            frontend:
              - 'packages/frontend/**'
            backend:
              - 'packages/backend/**'
  
  build-frontend:
    needs: changes
    if: needs.changes.outputs.frontend == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building frontend"
  
  build-backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building backend"
```

---

## 8. Best Practices

### 8.1. Performance Optimization

**1. Use caching:**

```yaml
- uses: actions/setup-node@v3
  with:
    node-version: '18'
    cache: 'npm'  # Auto-cache node_modules

- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

**2. Matrix strategy efficiently:**

```yaml
strategy:
  matrix:
    node: [16, 18]
    os: [ubuntu-latest, windows-latest]
  fail-fast: false  # Continue other jobs nếu 1 job fail
```

**3. Parallel jobs:**

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]
  
  test:
    runs-on: ubuntu-latest
    steps: [...]
  
  build:
    runs-on: ubuntu-latest
    steps: [...]

# All 3 chạy parallel!
```

### 8.2. Security

**1. Pin action versions:**

```yaml
# ❌ BAD - uses latest (có thể breaking changes)
- uses: actions/checkout@v3

# ✅ GOOD - pin to SHA (immutable)
- uses: actions/checkout@f43a0e5ff2bd294095638e18286ca9a3d1956744
```

**2. Minimize permissions:**

```yaml
permissions:
  contents: read  # Only read access
  packages: write  # Write to package registry

jobs:
  deploy:
    permissions:
      contents: read
      id-token: write  # For OIDC
```

**3. Use OIDC instead của long-lived tokens:**

```yaml
- uses: aws-actions/configure-aws-credentials@v2
  with:
    role-to-assume: arn:aws:iam::123456789012:role/my-role
    aws-region: us-east-1
```

---

## 9. Troubleshooting

### 9.1. Common Issues

**Issue: Workflow không trigger**

**Check:**

```yaml
# File location correct?
.github/workflows/ci.yml  ✅
github/workflows/ci.yml   ❌ (missing dot)

# YAML syntax valid?
# Use: https://www.yamllint.com/

# Trigger correct?
on:
  push:
    branches: [main]  # Only triggers on main
```

**Issue: "Resource not accessible by integration"**

**Fix:** Add permissions

```yaml
permissions:
  contents: write
  packages: write
```

**Issue: Job fails but no clear error**

**Add debug logging:**

```yaml
steps:
  - name: Debug
    run: |
      echo "PWD: $(pwd)"
      echo "Files: $(ls -la)"
      echo "Env: $(env)"
```

**Or enable debug logs:**

```
Repository → Settings → Secrets → Add secret:
ACTIONS_RUNNER_DEBUG = true
ACTIONS_STEP_DEBUG = true
```

### 9.2. Debugging Workflows

**Use tmate for SSH access:**

```yaml
- name: Setup tmate session
  if: failure()
  uses: mxschmitt/action-tmate@v3
  timeout-minutes: 30
```

**Check previous runs:**

```
GitHub repo → Actions → Click workflow → Click run → View logs
```

**Re-run failed jobs:**

```
Click "Re-run failed jobs" button
```

---

## 📚 Tổng kết

### Key Takeaways

1. **CI/CD** - Automate build, test, deploy
2. **GitHub Actions** - YAML workflows, free for public repos
3. **Triggers** - push, PR, schedule, manual
4. **Jobs & Steps** - Parallel jobs, sequential steps
5. **Docker** - Build & push images tự động
6. **Secrets** - Manage credentials an toàn
7. **Matrix** - Test multiple versions
8. **Caching** - Speed up workflows

### Checklist

- [ ] Hiểu CI/CD benefits
- [ ] Viết basic workflow với triggers
- [ ] Setup automated testing mỗi push
- [ ] Build Docker image trong CI
- [ ] Push image lên Docker Hub
- [ ] Use secrets an toàn
- [ ] Add build status badge
- [ ] Debug workflow failures
- [ ] Optimize với caching

### Next: Module 07 - WEB_SERVERS_BASICS

👉 Deploy apps với NGINX!

---

> **"Automate everything you can. Manual is error-prone." - DevOps Mantra** 🤖
