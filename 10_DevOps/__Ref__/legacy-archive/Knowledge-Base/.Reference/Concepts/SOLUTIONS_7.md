# Solutions: Module 06 - CI BASICS

> **Đáp Án CI/CD với GitHub Actions**

---

## TRẮC NGHIỆM

1. **B** - CI = Continuous Integration
2. **C** - .github/workflows/
3. **B** - on: push: branches: [main]
4. **A** - actions/checkout@v3
5. **C** - ${{ secrets.NAME }}
6. **B** - strategy: matrix:
7. **A** - actions/cache
8. **C** - workflow_dispatch
9. **B** - if: github.ref == 'refs/heads/main'
10. **A** - needs: test

---

## WORKFLOW EXAMPLES

**Basic CI:**

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
```

**Docker Build and Push:**

```yaml
- name: Login to DockerHub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}

- name: Build and push
  uses: docker/build-push-action@v4
  with:
    push: true
    tags: username/app:${{ github.sha }}
```

**Deploy via SSH:**

```yaml
- name: Deploy
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /var/www/app
      git pull
      docker-compose up -d
```

**Matrix Testing:**

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10']
    
steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
```

**Cache Dependencies:**

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**Conditional Deployment:**

```yaml
deploy:
  needs: test
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
```

---

## KEY CONCEPTS

| Concept | Description |
|---------|-------------|
| `on:` | Triggers (push, PR, schedule) |
| `jobs:` | Parallel job definitions |
| `steps:` | Sequential steps in job |
| `uses:` | Use existing action |
| `run:` | Execute command |
| `secrets:` | Encrypted variables |
| `needs:` | Job dependencies |
| `if:` | Conditional execution |

---

## COMPLETE CI/CD PIPELINE

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt pytest
      - run: pytest --cov=app

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: docker/build-push-action@v4
        with:
          push: true
          tags: user/app:latest

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          script: ./deploy.sh
```

---

**CI/CD = Ship faster, ship safer! 🚀**
