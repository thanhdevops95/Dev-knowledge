# Hướng dẫn CI/CD với GitHub Actions

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

CI/CD (Continuous Integration/Continuous Deployment) là quy trình tự động hóa việc test, build và deploy code.

### CI vs CD

| CI (Continuous Integration) | CD (Continuous Deployment) |
|---------------------------|---------------------------|
| Tự động chạy tests | Tự động deploy |
| Merge code thường xuyên | Deploy sau khi pass CI |
| Phát hiện lỗi sớm | Giảm thời gian release |

---

## 🔧**GITHUB ACTIONS CƠ BẢN**

### Cấu trúc

```
.github/
└── workflows/
    ├── ci.yml
    ├── deploy.yml
    └── release.yml
```

### Workflow đơn giản

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
```

---

## 📝**CÚ PHÁP YAML**

### Triggers (on)

```yaml
on:
  # Push to branches
  push:
    branches:
      - main
      - 'release/*'
    paths:
      - 'src/**'
      - '!docs/**'
  
  # Pull request
  pull_request:
    branches: [main]
  
  # Schedule (cron)
  schedule:
    - cron: '0 0 * * *'  # Mỗi ngày lúc 00:00
  
  # Manual trigger
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
```

### Jobs và Steps

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        run: echo "Hello"
      
      - name: Step 2
        run: |
          echo "Line 1"
          echo "Line 2"
  
  job2:
    needs: job1  # Chạy sau job1
    runs-on: ubuntu-latest
    steps:
      - run: echo "After job1"
```

### Matrix

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pytest
```

### Environment Variables

```yaml
env:
  GLOBAL_VAR: "global"

jobs:
  build:
    env:
      JOB_VAR: "job level"
    runs-on: ubuntu-latest
    steps:
      - name: Print vars
        env:
          STEP_VAR: "step level"
        run: |
          echo $GLOBAL_VAR
          echo $JOB_VAR
          echo $STEP_VAR
```

### Secrets

```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
    run: ./deploy.sh
```

---

## 🐍**PYTHON CI WORKFLOW**

### Full CI Pipeline

```yaml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install linters
        run: pip install flake8 black isort
      
      - name: Run flake8
        run: flake8 src/
      
      - name: Check black formatting
        run: black --check src/
      
      - name: Check import sorting
        run: isort --check-only src/

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests with coverage
        run: pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Build package
        run: |
          pip install build
          python -m build
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
```

---

## 🟢**NODE.JS CI WORKFLOW**

```yaml
name: Node.js CI

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
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

---

## 🐳**DOCKER CI/CD**

```yaml
name: Docker CI/CD

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            username/app:latest
            username/app:${{ github.sha }}
```

---

## 🚀**DEPLOYMENT**

### Deploy to Server (SSH)

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/app
            git pull origin main
            pip install -r requirements.txt
            sudo systemctl restart app
```

### Deploy to Vercel

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Deploy to AWS

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy to S3
        run: aws s3 sync ./build s3://my-bucket
      
      - name: Invalidate CloudFront
        run: aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DISTRIBUTION_ID }} --paths "/*"
```

---

## 📦**ACTIONS PHỔ BIẾN**

| Action | Mô tả |
|--------|-------|
| `actions/checkout@v4` | Checkout code |
| `actions/setup-python@v4` | Setup Python |
| `actions/setup-node@v4` | Setup Node.js |
| `actions/cache@v3` | Cache dependencies |
| `actions/upload-artifact@v3` | Upload artifacts |
| `docker/build-push-action@v5` | Build & push Docker |

---

## 🔐**BẢO MẬT**

### Sử dụng Secrets

1. Vào **Settings** → **Secrets and variables** → **Actions**
2. Thêm secret mới
3. Sử dụng: `${{ secrets.SECRET_NAME }}`

### Environment Protection

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Cần approval
    steps:
      - run: ./deploy.sh
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
