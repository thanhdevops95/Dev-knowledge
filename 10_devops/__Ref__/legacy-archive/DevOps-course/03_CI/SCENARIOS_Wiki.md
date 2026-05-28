# 🚨 MODULE 03: SCENARIOS - CI Issues

## Scenario 1: Tests Pass Locally, Fail on CI

### 🚨 Bối cảnh

Tests pass trên máy developer, nhưng fail trên GitHub Actions.

### 🕵️ Điều tra

```yaml
# GitHub Actions log:
ModuleNotFoundError: No module named 'redis'
```

Local có Redis installed, CI runner thì không.

### 💡 Giải pháp

**Add Redis service to workflow:**

```yaml
jobs:
  test:
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
```

### 🧠 Bài học

- CI environment khác local
- Use services cho dependencies
- Test trên clean environment

---

## Scenario 2: Build Timeout (6 giờ)

### 🚨 Bối cảnh

GitHub Actions job chạy > 6 giờ → timeout

### 🕵️ Điều tra

- Dependencies install lâu
- Docker build không cache layers

### 💡 Giải pháp

**1. Cache dependencies:**

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**2. Docker layer caching:**

```yaml
- uses: docker/build-push-action@v4
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### 🧠 Bài học

- Cache để tăng tốc
- Optimize Dockerfile layers

---

## Scenario 3: Flaky Tests

### 🚨 Bối cảnh

Test đôi khi pass, đôi khi fail (không deterministic).

### 🕵️ Điều tra

```python
def test_timestamp():
    now = time.time()
    time.sleep(0.1)
    later = time.time()
    assert later - now == 0.1  # ❌ Flaky! (0.100001 != 0.1)
```

### 💡 Giải pháp

**Use tolerances:**

```python
assert abs((later - now) - 0.1) < 0.01  # ✅ Stable
```

**Mock time:**

```python
from unittest.mock import patch

@patch('time.time', return_value=1000)
def test_timestamp(mock_time):
    assert get_timestamp() == 1000
```

### 🧠 Bài học

- Avoid time-dependent tests
- Mock external dependencies
- Flaky tests worse than no tests

---

## Scenario 4: Secrets Leaked in Logs

### 🚨 Bối cảnh

GitHub Actions log hiển thị API key:

```
Building with AWS_KEY=AKIA1234567890ABCDEF
```

### 🕵️ Điều tra

Developer dùng `echo` để debug.

### 💡 Giải pháp

**1. Use GitHub Secrets:**

```yaml
env:
  AWS_KEY: ${{ secrets.AWS_ACCESS_KEY }}
```

GitHub tự động mask secrets trong logs.

**2. Never echo secrets:**

```yaml
❌ run: echo "Key is $AWS_KEY"
✅ run: aws configure set aws_access_key_id $AWS_KEY
```

### 🧠 Bài học

- Always use GitHub Secrets
- GitHub auto-masks secrets
- Review logs before public repos

---

## Scenario 5: CI Overload (Too Many Commits)

### 🚨 Bối cảnh

Developer push 50 commits liên tục → GitHub Actions queue 50 builds → Tốn minutes.

### 🕵️ Điều tra

Mỗi commit trigger CI, không cần thiết cho commits nhỏ.

### 💡 Giải pháp

**1. Squash commits before push:**

```bash
# Locally
git rebase -i HEAD~5  # Squash 5 commits into 1

# Or use PR squash merge
```

**2. Skip CI for docs:**

```yaml
on:
  push:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

**3. Concurrency control:**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel old runs
```

### 🧠 Bài học

- Squash small commits
- Use paths-ignore
- Cancel redundant runs

---

## 🎯 Tổng kết Module 03

| Scenario | Vấn đề | Giải pháp |
|----------|--------|-----------|
| 1 | Tests fail on CI | Add services |
| 2 | Build timeout | Caching |
| 3 | Flaky tests | Mock + Tolerances |
| 4 | Secrets leaked | GitHub Secrets |
| 5 | CI overload | Squash + Concurrency |

✅ **Next:** Module 04 - CD!
