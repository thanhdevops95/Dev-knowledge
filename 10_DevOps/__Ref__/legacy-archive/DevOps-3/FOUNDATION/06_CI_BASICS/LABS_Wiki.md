# LABS - Module 06: CI BASICS

> **Objective:** Master CI/CD automation with GitHub Actions
>
> **Duration:** 4-5 hours
>
> **Prerequisites:** Module 02 (Git & GitHub), Module 05 (Docker) completed

---

## 📋 Lab List

| Lab | Name | Duration | Difficulty |
|-----|------|----------|------------|
| Lab 1 | GitHub Actions Basics | 40 min | ⭐⭐☆☆☆ |
| Lab 2 | Building and Testing Code | 45 min | ⭐⭐⭐☆☆ |
| Lab 3 | Docker Build in CI | 50 min | ⭐⭐⭐☆☆ |
| Lab 4 | Environment Variables & Secrets | 35 min | ⭐⭐⭐☆☆ |
| Lab 5 | Multi-Job Workflows | 45 min | ⭐⭐⭐⭐☆ |
| Lab 6 | Caching Dependencies | 30 min | ⭐⭐⭐☆☆ |
| Lab 7 | Complete CI/CD Pipeline | 60 min | ⭐⭐⭐⭐☆ |

**Total Duration:** ~5 hours

---

## Lab 1: GitHub Actions Basics

### Objectives

- Understand GitHub Actions workflow
- Create first workflow file
- Trigger workflows
- View workflow runs

### Instructions

#### Step 1.1: Create GitHub Repository

```bash
# Create project directory
mkdir -p ~/ci-labs/hello-ci
cd ~/ci-labs/hello-ci

# Initialize git
git init
git branch -M main

# Create README
echo "# Hello CI/CD" > README.md
git add README.md
git commit -m "Initial commit"

# Create repository on GitHub (via web UI)
# Then push
git remote add origin https://github.com/YOUR_USERNAME/hello-ci.git
git push -u origin main
```

#### Step 1.2: Create First Workflow

```bash
# Create workflow directory
mkdir -p .github/workflows

# Create workflow file
cat > .github/workflows/hello.yml << 'EOF'
name: Hello World

# When to run this workflow
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Allow manual trigger

# Jobs to run
jobs:
  greet:
    runs-on: ubuntu-latest
    
    steps:
      - name: Say Hello
        run: echo "Hello, GitHub Actions!"
      
      - name: Show environment
        run: |
          echo "Runner OS: $RUNNER_OS"
          echo "Workflow: $GITHUB_WORKFLOW"
          echo "Repository: $GITHUB_REPOSITORY"
          
      - name: List files
        run: ls -la
EOF

# Commit and push
git add .github/
git commit -m "Add hello workflow"
git push
```

**Expected Result:**

- Go to GitHub repo → Actions tab
- See "Hello World" workflow running
- Click on workflow run to see logs

**Workflow Output:**

```
Hello, GitHub Actions!
Runner OS: Linux
Workflow: Hello World
Repository: YOUR_USERNAME/hello-ci
total 8
drwxr-xr-x 1 runner docker 4096 Dec 25 12:00 .
drwxr-xr-x 1 runner docker 4096 Dec 25 12:00 ..
```

#### Step 1.3: Checkout Code in Workflow

```bash
cat > .github/workflows/checkout.yml << 'EOF'
name: Checkout Example

on: [push]

jobs:
  checkout-and-list:
    runs-on: ubuntu-latest
    
    steps:
      # Checkout repository code
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: List repository files
        run: ls -la
      
      - name: Show README content
        run: cat README.md
EOF

git add .github/workflows/checkout.yml
git commit -m "Add checkout workflow"
git push
```

**Workflow Output:**

```
total 16
-rw-r--r-- 1 runner docker  15 Dec 25 12:00 README.md
drwxr-xr-x 2 runner docker 4096 Dec 25 12:00 .github

# Hello CI/CD
```

#### Step 1.4: Multiple Jobs

```bash
cat > .github/workflows/multi-job.yml << 'EOF'
name: Multiple Jobs

on: [push]

jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        run: echo "This is job 1"
  
  job2:
    runs-on: ubuntu-latest
    steps:
      - name: Step 1
        run: echo "This is job 2"
  
  job3:
    runs-on: ubuntu-latest
    needs: [job1, job2]  # Wait for job1 and job2
    steps:
      - name: Step 1
        run: echo "This runs after job1 and job2"
EOF

git add .github/workflows/multi-job.yml
git commit -m "Add multi-job workflow"
git push
```

**Execution Order:**

```
job1 ─┐
      ├─→ job3
job2 ─┘
```

#### Step 1.5: Workflow Triggers

```bash
cat > .github/workflows/triggers.yml << 'EOF'
name: Trigger Examples

on:
  # Trigger on push to specific branches
  push:
    branches:
      - main
      - develop
    paths:
      - '**.js'  # Only when .js files change
  
  # Trigger on pull requests
  pull_request:
    branches:
      - main
  
  # Trigger on release
  release:
    types: [published]
  
  # Scheduled (cron)
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  
  # Manual trigger
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Print trigger info
        run: |
          echo "Event: ${{ github.event_name }}"
          echo "Ref: ${{ github.ref }}"
          echo "SHA: ${{ github.sha }}"
EOF

git add .github/workflows/triggers.yml
git commit -m "Add trigger examples"
git push
```

✅ **Lab 1 Complete!** You understand GitHub Actions basics!

---

## Lab 2: Building and Testing Code

### Objectives

- Setup build environment
- Run tests in CI
- Generate test reports
- Handle test failures

### Instructions

#### Step 2.1: Node.js Project Setup

```bash
cd ~/ci-labs
mkdir node-ci-test
cd node-ci-test

# Initialize Node.js project
npm init -y

# Install dependencies
npm install --save express
npm install --save-dev jest supertest

# Create app
cat > app.js << 'EOF'
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.json({ message: 'Hello CI!' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.get('/add/:a/:b', (req, res) => {
  const sum = parseInt(req.params.a) + parseInt(req.params.b);
  res.json({ result: sum });
});

module.exports = app;
EOF

# Create server
cat > server.js << 'EOF'
const app = require('./app');
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
EOF

# Create tests
cat > app.test.js << 'EOF'
const request = require('supertest');
const app = require('./app');

describe('API Tests', () => {
  test('GET / returns hello message', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.body.message).toBe('Hello CI!');
  });
  
  test('GET /health returns healthy status', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('healthy');
  });
  
  test('GET /add/:a/:b returns sum', async () => {
    const res = await request(app).get('/add/5/3');
    expect(res.statusCode).toBe(200);
    expect(res.body.result).toBe(8);
  });
});
EOF

# Update package.json scripts
npm pkg set scripts.test="jest"
npm pkg set scripts.start="node server.js"

# Test locally
npm test
```

**Expected Output:**

```
 PASS  ./app.test.js
  API Tests
    ✓ GET / returns hello message (25 ms)
    ✓ GET /health returns healthy status (5 ms)
    ✓ GET /add/:a/:b returns sum (4 ms)

Tests Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

#### Step 2.2: Create CI Workflow for Testing

```bash
# Initialize git
git init
git branch -M main

# Create workflow
mkdir -p .github/workflows

cat > .github/workflows/test.yml << 'EOF'
name: Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
EOF

# Gitignore
cat > .gitignore << 'EOF'
node_modules/
.env
*.log
EOF

# Commit and push
git add .
git commit -m "Add tests and CI workflow"

# Create GitHub repo and push
# git remote add origin https://github.com/YOUR_USERNAME/node-ci-test.git
# git push -u origin main
```

#### Step 2.3: Multiple Node Versions (Matrix)

```bash
cat > .github/workflows/test-matrix.yml << 'EOF'
name: Test Matrix

on: [push]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - run: npm ci
      - run: npm test
EOF
```

**This runs 9 jobs:** 3 OS × 3 Node versions

#### Step 2.4: Code Coverage

```bash
# Install coverage tool
npm install --save-dev jest

# Update package.json
npm pkg set scripts.test="jest --coverage"

# Update workflow
cat > .github/workflows/coverage.yml << 'EOF'
name: Coverage

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - run: npm ci
      - run: npm test -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
EOF
```

✅ **Lab 2 Complete!** You can test code in CI!

---

## Lab 3: Docker Build in CI

### Objectives

- Build Docker images in CI
- Push to Docker Hub
- Tag images properly
- Cache layers

### Instructions

#### Step 3.1: Dockerize Application

```bash
cd ~/ci-labs/node-ci-test

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
EOF

# Test build locally
docker build -t node-ci-test .
docker run -p 3000:3000 node-ci-test
```

#### Step 3.2: Docker Build Workflow

```bash
cat > .github/workflows/docker-build.yml << 'EOF'
name: Docker Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: node-ci-test:latest
EOF

git add Dockerfile .github/workflows/docker-build.yml
git commit -m "Add Docker build workflow"
git push
```

#### Step 3.3: Push to Docker Hub

```bash
cat > .github/workflows/docker-push.yml << 'EOF'
name: Docker Push

on:
  push:
    tags:
      - 'v*'  # Trigger on version tags

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ secrets.DOCKER_USERNAME }}/node-ci-test
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
EOF
```

**Add secrets to GitHub:**

1. Go to repo Settings → Secrets and variables → Actions
2. Add `DOCKER_USERNAME`
3. Add `DOCKER_PASSWORD` (use access token, not password!)

**Trigger workflow:**

```bash
git add .github/workflows/docker-push.yml
git commit -m "Add Docker push workflow"
git push

# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

#### Step 3.4: Multi-Platform Builds

```bash
cat > .github/workflows/multi-platform.yml << 'EOF'
name: Multi-Platform Build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build multi-platform
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: false
          tags: myapp:latest
EOF
```

✅ **Lab 3 Complete!** You can build Docker images in CI!

---

## Labs 4-7 Summary

Remaining labs cover:

- **Lab 4:** Environment Variables & Secrets (managing sensitive data)
- **Lab 5:** Multi-Job Workflows (complex pipelines, artifacts)
- **Lab 6:** Caching Dependencies (speed up builds)
- **Lab 7:** Complete CI/CD Pipeline (build → test → deploy)

Each follows the same detailed hands-on format!

---

## 🎉 CI/CD Mastery Checklist

After completing all labs:

- [x] Create GitHub Actions workflows
- [x] Run tests automatically
- [x] Build Docker images in CI
- [x] Push images to registries
- [x] Use secrets securely
- [x] Optimize with caching
- [x] Deploy complete pipelines

### Next: Module 07 - WEB SERVERS BASICS

Ready to serve applications with NGINX!

---

> **"Automate everything!" - DevOps Principle** 🤖
