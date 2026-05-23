# 🧪 MODULE 03: LABS - CI with GitHub Actions

## LAB 1: Viết Unit Tests

### Tạo file tests/test_app.py

```python
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_increment(client):
    client.get('/reset')
    response = client.get('/increment')
    assert response.status_code == 200
```

### Run tests locally

```bash
pip install pytest
pytest tests/ -v
```

---

## LAB 2: Thiết lập GitHub Actions

### Tạo .github/workflows/main.yml

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pytest
      - run: pytest tests/
```

### Push and verify

```bash
git add .github/workflows/main.yml tests/
git commit -m "Add CI workflow"
git push

# Check GitHub → Actions tab
```

---

## LAB 3: Thêm Kiểm tra Chất lượng Code

### Update workflow

```yaml
- name: Lint with flake8
  run: |
    pip install flake8
    flake8 app.py --max-line-length=100

- name: Format check with black
  run: |
    pip install black
    black --check app.py
```

---

## LAB 4: Build và Push Docker Image

```yaml
build:
  needs: test
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Build image
      run: docker build -t ${{ secrets.DOCKER_USERNAME }}/counter:${{ github.sha }} .
    - name: Push to Docker Hub
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push ${{ secrets.DOCKER_USERNAME }}/counter:${{ github.sha }}
```

✅ **Checklist**

- [ ] Tests pass locally
- [ ] GitHub Actions workflow created
- [ ] Linting added
- [ ] Docker build automated
