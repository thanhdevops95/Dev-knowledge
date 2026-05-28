# ✅ Solutions: CI/CD Basic

> **Solutions for Exercises. Try to solve it yourself first!**
>
> *Đáp án cho Exercises. Hãy thử tự giải trước!*

---

## Exercise 1: Basic Workflow

```yaml
# .github/workflows/hello.yml
name: Hello CI/CD

on:
  push:
    branches: [main]

jobs:
  hello:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Say Hello
        run: echo "Hello CI/CD!"
      
      - name: Git Info
        run: |
          echo "Commit: ${{ github.sha }}"
          echo "Author: ${{ github.actor }}"
          echo "Branch: ${{ github.ref_name }}"
```

---

## Exercise 2: Node.js CI

```yaml
name: Node.js CI

on: [push, pull_request]

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
      
      - name: Lint
        run: npm run lint
      
      - name: Test with coverage
        run: npm test -- --coverage
      
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

---

## Exercise 3: Docker Build

```yaml
name: Docker Build

on:
  push:
    branches: [main]

jobs:
  docker:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/app:${{ github.sha }}
            ${{ secrets.DOCKERHUB_USERNAME }}/app:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
```

---

## Exercise 4: Matrix Testing

```yaml
name: Matrix Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install
        run: npm ci
      
      - name: Test
        run: npm test
      
      - name: Report
        if: failure()
        run: echo "Tests failed on ${{ matrix.os }} with Node ${{ matrix.node-version }}"
```

---

## Exercise 5: Deployment Pipeline

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
      - name: Deploy to staging
        run: |
          echo "Deploying to staging..."
          # Deploy script here

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Deploy script here
```

---

## Exercise 6: Reusable Workflow

### Callable Workflow

```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
      environment:
        required: true
        type: string
    secrets:
      deploy-key:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      
      - run: npm ci
      - run: npm run build
      
      - name: Deploy
        env:
          DEPLOY_KEY: ${{ secrets.deploy-key }}
        run: echo "Deploying with key..."
```

### Calling Workflow

```yaml
# .github/workflows/main.yml
name: Main Pipeline

on: [push]

jobs:
  call-build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '18'
      environment: staging
    secrets:
      deploy-key: ${{ secrets.DEPLOY_KEY }}
```

---

## Exercise 7: Scheduled Jobs

```yaml
name: Security Scan

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:  # Manual trigger

jobs:
  audit:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run audit
        id: audit
        continue-on-error: true
        run: npm audit --json > audit-report.json
      
      - name: Check results
        run: |
          if [ -f audit-report.json ]; then
            vulnerabilities=$(cat audit-report.json | jq '.metadata.vulnerabilities.total')
            echo "Found $vulnerabilities vulnerabilities"
            if [ "$vulnerabilities" -gt 0 ]; then
              echo "::warning::Security vulnerabilities found!"
            fi
          fi
      
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: audit-report.json
```

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
