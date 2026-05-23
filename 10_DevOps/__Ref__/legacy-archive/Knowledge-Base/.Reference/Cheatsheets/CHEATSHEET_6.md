# CI Basics - Cheatsheet

> **GitHub Actions & CI/CD essentials**

---

## 🔄 GITHUB ACTIONS BASICS

### Workflow File Structure

```yaml
# .github/workflows/ci.yml
name: CI Pipeline                    # Workflow name

on:                                 # Triggers
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'            # Daily at midnight
  workflow_dispatch:                # Manual trigger

jobs:
  build:                            # Job name
    runs-on: ubuntu-latest          # Runner OS
    
    steps:
      - name: Checkout code         # Step name
        uses: actions/checkout@v3   # Action
      
      - name: Run command
        run: echo "Hello CI"        # Shell command
```

---

## 🎯 COMMON TRIGGERS

```yaml
# Push to specific branches
on:
  push:
    branches:
      - main
      - develop
      - 'release/*'

# Pull requests
on:
  pull_request:
    branches: [ main ]

# Tags
on:
  push:
    tags:
      - 'v*'

# Multiple events
on: [push, pull_request]

# Schedule (cron)
on:
  schedule:
    - cron: '0 0 * * 0'    # Weekly Sunday midnight

# Manual trigger
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
```

---

## 🛠️ COMMON ACTIONS

### Checkout Code

```yaml
- name: Checkout
  uses: actions/checkout@v3
  with:
    fetch-depth: 0         # Full history
```

### Setup Languages

```yaml
# Python
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.9'
    cache: 'pip'

# Node.js
- name: Setup Node
  uses: actions/setup-node@v3
  with:
    node-version: '16'
    cache: 'npm'

# Java
- name: Setup Java
  uses: actions/setup-java@v3
  with:
    distribution: 'temurin'
    java-version: '11'
```

### Cache Dependencies

```yaml
- name: Cache npm
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Upload/Download Artifacts

```yaml
# Upload
- name: Upload artifact
  uses: actions/upload-artifact@v3
  with:
    name: my-artifact
    path: dist/

# Download
- name: Download artifact
  uses: actions/download-artifact@v3
  with:
    name: my-artifact
```

---

## 🐳 DOCKER IN ACTIONS

### Build Docker Image

```yaml
- name: Build Docker image
  run: docker build -t myapp:${{ github.sha }} .

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v2

- name: Build and export
  uses: docker/build-push-action@v4
  with:
    context: .
    tags: myapp:latest
    outputs: type=docker,dest=/tmp/myimage.tar
```

### Push to Docker Hub

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}

- name: Build and push
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: |
      username/myapp:latest
      username/myapp:${{ github.sha }}
```

---

## 🧪 TESTING

### Python Tests

```yaml
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    pip install pytest pytest-cov

- name: Run tests
  run: |
    pytest tests/ -v
    pytest --cov=app tests/
```

### Node.js Tests

```yaml
- name: Install dependencies
  run: npm ci

- name: Lint
  run: npm run lint

- name: Test
  run: npm test

- name: Build
  run: npm run build
```

### Multiple Python Versions

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10']

steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
```

---

## 🔐 SECRETS

### Using Secrets

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
  run: ./deploy.sh
```

### Setting Secrets

```
GitHub Repo → Settings → Secrets → Actions
→ New repository secret

Add:
- DOCKER_USERNAME
- DOCKER_PASSWORD
- SERVER_HOST
- SSH_PRIVATE_KEY
```

---

## 📤 DEPLOYMENT

### SSH Deploy

```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /var/www/myapp
      git pull
      docker-compose up -d --build
```

### Deploy with rsync

```yaml
- name: Deploy files
  uses: burnett01/rsync-deployments@5.2
  with:
    switches: -avzr --delete
    path: dist/
    remote_path: /var/www/html/
    remote_host: ${{ secrets.SERVER_HOST }}
    remote_user: ${{ secrets.SERVER_USER }}
    remote_key: ${{ secrets.SSH_PRIVATE_KEY }}
```

---

## 🔗 JOB DEPENDENCIES

### Sequential Jobs

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  test:
    needs: lint              # Wait for lint
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    needs: test              # Wait for test
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  deploy:
    needs: build             # Wait for build
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

### Parallel Jobs

```yaml
jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - run: pytest

  test-node:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  # Both run simultaneously
```

---

## 🎭 CONDITIONAL EXECUTION

### If Conditions

```yaml
# Run only on main branch
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

# Run on success
- name: Notify success
  if: success()
  run: ./notify.sh "Success"

# Run on failure
- name: Notify failure
  if: failure()
  run: ./notify.sh "Failed"

# Run always
- name: Cleanup
  if: always()
  run: ./cleanup.sh

# Multiple conditions
- name: Deploy staging
  if: github.ref == 'refs/heads/develop' && success()
  run: ./deploy-staging.sh
```

---

## 🌍 ENVIRONMENTS

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging           # Environment name
    steps:
      - run: ./deploy-staging.sh

  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    steps:
      - run: ./deploy-production.sh
```

**Setup environment in GitHub:**

```
Settings → Environments → New environment
→ Add protection rules, secrets
```

---

## 📊 STATUS BADGES

### Add to README.md

```markdown
![CI](https://github.com/username/repo/workflows/CI/badge.svg)
![Build](https://github.com/username/repo/actions/workflows/ci.yml/badge.svg)
```

Shows: ✅ passing or ❌ failing

---

## 🔍 DEBUGGING

### Enable debug logging

```
Repo Settings → Secrets
Add: ACTIONS_RUNNER_DEBUG = true
Add: ACTIONS_STEP_DEBUG = true
```

### Print context

```yaml
- name: Dump GitHub context
  run: echo '${{ toJSON(github) }}'

- name: Dump runner context
  run: echo '${{ toJSON(runner) }}'
```

### Manual trigger for testing

```yaml
on:
  workflow_dispatch:    # Enable "Run workflow" button
```

---

## 📝 COMPLETE EXAMPLES

### Python Flask CI/CD

```yaml
name: Python CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
      
      - name: Lint
        run: flake8 app/ --max-line-length=100
      
      - name: Test
        run: pytest tests/ --cov=app
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: username/myapp:latest
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/myapp
            docker-compose pull
            docker-compose up -d
```

### Node.js CI/CD

```yaml
name: Node.js CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [14, 16, 18]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

---

## 💡 BEST PRACTICES

```yaml
# ✅ Use specific action versions
uses: actions/checkout@v3          # Good
uses: actions/checkout@main        # Bad (can break)

# ✅ Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ hashFiles('package-lock.json') }}

# ✅ Fail fast
strategy:
  fail-fast: true

# ✅ Set timeouts
jobs:
  test:
    timeout-minutes: 10

# ✅ Use environments for sensitive deploys
environment: production

# ✅ Don't commit secrets
# Use repository/environment secrets

# ✅ Matrix for multiple versions
strategy:
  matrix:
    python: ['3.8', '3.9', '3.10']
```

---

<div align="center">

**CI/CD = Ship code with confidence! ⚡🚀**

**Automate everything! 🤖**

</div>
