# Module 08: CI Labs

---

## 🎯 Mục tiêu

Sau labs này, bạn sẽ:

- Setup GitHub Actions pipeline
- Chạy tests tự động
- Build Docker image trong CI

---

## 🔧 Lab 1: First Workflow

### Bước 1: Tạo repo mới

Tạo repo trên GitHub, clone về local.

### Bước 2: Tạo workflow

```bash
mkdir -p .github/workflows
```

```yaml
# .github/workflows/ci.yml
name: First CI

on: [push]

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - name: Say Hello
        run: echo "Hello, GitHub Actions!"
      
      - name: Show date
        run: date
      
      - name: Show system info
        run: |
          uname -a
          cat /etc/os-release
```

### Bước 3: Push và xem kết quả

```bash
git add .
git commit -m "Add first workflow"
git push
```

Vào GitHub → Actions tab để xem workflow chạy.

### ✅ Checkpoint Lab 1

- [ ] Workflow runs successfully
- [ ] Xem được logs

---

## ✅ Lab 2: Testing Pipeline

### Bước 1: Tạo Python app với tests

```python
# app.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b
```

```python
# test_app.py
from app import add, subtract, multiply

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 5) == 0
```

```
# requirements.txt
pytest==7.4.0
```

### Bước 2: CI workflow

```yaml
# .github/workflows/test.yml
name: Python Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest -v
```

### Bước 3: Push và verify tests

```bash
git add .
git commit -m "Add Python tests and CI"
git push
```

### ✅ Checkpoint Lab 2

- [ ] Tests run trong CI
- [ ] All tests pass

---

## 🐳 Lab 3: Docker Build trong CI

### Bước 1: Add Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py ./
CMD ["python", "-c", "from app import add; print(f'2+3={add(2,3)}')"]
```

### Bước 2: Docker workflow

```yaml
# .github/workflows/docker.yml
name: Docker Build

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      
      - name: Run Docker container
        run: docker run myapp:${{ github.sha }}
      
      - name: Run tests in Docker
        run: docker run myapp:${{ github.sha }} pytest -v
```

### ✅ Checkpoint Lab 3

- [ ] Docker builds trong CI
- [ ] Tests run inside container

---

## 🔐 Lab 4: Secrets Management

### Bước 1: Add secrets trong GitHub

1. Repo → Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `MY_SECRET`, Value: `super-secret-value`

### Bước 2: Sử dụng secret

```yaml
name: Secrets Demo

on: [push]

jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - name: Use secret
        env:
          SECRET_VALUE: ${{ secrets.MY_SECRET }}
        run: |
          echo "Secret length: ${#SECRET_VALUE}"
          # KHÔNG echo giá trị secret!
```

### ✅ Checkpoint Lab 4

- [ ] Secret configured
- [ ] Secret masked trong logs

---

## 📊 Lab 5: Matrix Strategy

### Test trên nhiều versions

```yaml
name: Matrix Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install and test
        run: |
          pip install pytest
          pytest -v
```

### ✅ Checkpoint Lab 5

- [ ] Tests run trên multiple Python versions
- [ ] Matrix status hiển thị

---

## 🎓 Tổng kết Labs

| Lab | Skill | Output |
|-----|-------|--------|
| 1 | Basic workflow | First CI running |
| 2 | Testing | Automated tests |
| 3 | Docker CI | Container builds |
| 4 | Secrets | Secure config |
| 5 | Matrix | Multi-version tests |

---

## ⏭️ Tiếp theo

👉 **[SCENARIOS.md - Tình huống CI](SCENARIOS.md)**
