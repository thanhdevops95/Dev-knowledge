# 🚨 Tình huống Thực chiến - CI/CD

Đây là 5 tình huống thực tế mà DevOps Engineer thường gặp khi vận hành CI/CD pipelines.

---

## Scenario 1: Flaky Tests - CI fail 30% không lý do rõ ràng

### 📋 Bối cảnh

Pipeline chạy **pass, fail, pass, fail** ngẫu nhiên với cùng code. Team bắt đầu ignore CI status.

> "Cứ merge đi, chắc lại flaky test thôi"

### 🔍 Triệu chứng

```
Run #123: ✅ Pass
Run #124: ❌ Fail - Test: test_api_response timeout
Run #125: ✅ Pass
Run #126: ❌ Fail - Test: test_api_response timeout
```

Cùng code, cùng branch, kết quả khác nhau.

### 🕵️ Điều tra

**Nguyên nhân thường gặp:**

| Nguyên nhân | Dấu hiệu |
|-------------|----------|
| **Race conditions** | Tests depend on timing |
| **Shared state** | Tests không isolated |
| **External dependencies** | API/DB không stable |
| **Resource limits** | Runner chậm/thiếu memory |
| **Date/time dependent** | Tests fail vào cuối tháng |

```yaml
# Kiểm tra test logs
- name: test_api_response
  Error: Expected response in 5s, got timeout after 10s
  # Timeout quá ngắn cho slow CI runner
```

### 💡 Giải pháp

**1. Tăng timeouts cho CI:**

```python
# test_api.py
def test_api_response():
    timeout = 30 if os.getenv('CI') else 5  # Timeout dài hơn trong CI
    response = call_api(timeout=timeout)
```

**2. Retry flaky tests:**

```yaml
# pytest.ini
[pytest]
reruns = 3
reruns_delay = 1

# hoặc trong CI
- name: Run tests with retry
  run: pytest --reruns 3 --reruns-delay 2
```

**3. Isolate tests:**

```python
# Mỗi test có database riêng
@pytest.fixture
def db():
    db = create_test_database()
    yield db
    db.drop()  # Clean up
```

**4. Mock external services:**

```python
# Không gọi API thật trong unit tests
@patch('myapp.external_api.call')
def test_api(mock_call):
    mock_call.return_value = {"status": "ok"}
    result = my_function()
    assert result == expected
```

**5. Quarantine flaky tests:**

```yaml
# CI workflow
- name: Run stable tests
  run: pytest -m "not flaky"

- name: Run flaky tests (allow failure)
  run: pytest -m "flaky"
  continue-on-error: true
```

### 🧠 Bài học

- **Flaky tests làm CI vô nghĩa** - Team sẽ ignore
- **Track flaky tests** - Dashboard để monitor
- **Fix hoặc quarantine** - Không để flaky test block deployment
- **CI environment ≠ local** - Có thể chậm hơn, ít resources hơn

---

## Scenario 2: CI Pipeline quá chậm - 30+ phút

### 📋 Bối cảnh

Developer commit code, phải đợi **30 phút** mới biết kết quả CI.

> "Tôi không nhớ mình làm gì 30 phút trước nữa"

### 🔍 Triệu chứng

```
Job: install-deps     5 min
Job: lint             3 min
Job: unit-tests      10 min
Job: integration      8 min
Job: build           5 min
Job: security-scan   4 min
───────────────────────────
Total:              35 min
```

### 🕵️ Điều tra

```yaml
# Phân tích bottlenecks
- install-deps: npm ci mỗi lần 5 phút
- unit-tests: 500 tests chạy sequential
- build: Không cache Docker layers
```

### 💡 Giải pháp

**1. Cache dependencies:**

```yaml
# GitHub Actions
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

**2. Parallel jobs:**

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
  tests:
    runs-on: ubuntu-latest
  security:
    runs-on: ubuntu-latest
  # Chạy song song thay vì tuần tự!
  
  build:
    needs: [lint, tests, security]  # Chỉ đợi khi cần
```

**3. Parallel tests:**

```bash
# pytest-xdist
pytest -n auto  # Chạy parallel theo số CPU

# Jest
jest --maxWorkers=4
```

**4. Docker layer caching:**

```yaml
- name: Build Docker
  uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**5. Skip không cần thiết:**

```yaml
# Chỉ run security scan khi có file changes
- name: Security scan
  if: contains(github.event.commits.*.modified, 'package.json')
```

**Kết quả sau optimize:**

```
Job: install (cached)   30s
Job: lint               2 min (parallel)
Job: tests              2 min (parallel, faster runner)
Job: build (cached)     1 min
───────────────────────
Total:                  5 min  ← Từ 35 phút → 5 phút!
```

### 🧠 Bài học

- **Cache everything** - Dependencies, Docker layers, test fixtures
- **Parallel > Sequential** - Không để jobs chờ nhau không cần thiết
- **Faster runners** - Đôi khi worth paying for better CI
- **Skip intelligently** - Không run tất cả cho mọi commit

---

## Scenario 3: Secret bị lộ trong CI logs

### 📋 Bối cảnh

Security team alert: Database password xuất hiện trong CI logs **public**!

> Pull request logs ai cũng xem được

### 🔍 Triệu chứng

```
# CI Log output
Step: Deploy to production
$ echo "Connecting to database..."
$ psql postgres://admin:SuperSecret123@db.company.com:5432/prod  ← PASSWORD LỘ!
Connection successful
```

### 🕵️ Điều tra

```yaml
# Workflow file
- name: Deploy
  run: |
    echo "Connecting to $DATABASE_URL"  # ← In ra secrets!
    psql $DATABASE_URL
```

### 💡 Giải pháp

**1. KHÔNG ECHO secrets:**

```yaml
- name: Deploy
  run: |
    # Không echo URL
    psql $DATABASE_URL > /dev/null 2>&1
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

**2. GitHub tự động mask secrets:**

```yaml
# Secrets trong ${{ secrets.* }} được auto-mask
- run: echo ${{ secrets.PASSWORD }}
# Output: ***
```

**3. Nhưng cẩn thận với encoding:**

```yaml
# ❌ Secrets trong base64 KHÔNG được mask!
- run: echo ${{ secrets.PASSWORD }} | base64
# Output: U3VwZXJTZWNyZXQxMjM=  ← Có thể decode!
```

**4. Dùng OIDC thay vì long-lived secrets:**

```yaml
# Thay vì AWS credentials
- name: Configure AWS
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/github-actions
    aws-region: us-east-1
  # Không cần AWS_ACCESS_KEY_ID!
```

**5. Audit workflow files:**

```bash
# Scan for potential secret leaks
grep -r "echo.*\$" .github/workflows/
grep -r "print.*\$" .github/workflows/
```

### 🧠 Bài học

- **CI logs thường public** - PRs, forks có thể xem
- **Đừng bao giờ echo secrets** - Ngay cả để debug
- **OIDC > long-lived secrets** - Không cần store credentials
- **Rotate secrets bị lộ** - Ngay lập tức!

---

## Scenario 4: Deployment fail nhưng không ai biết

### 📋 Bối cảnh

Merge PR, CI pass, deploy... nhưng production vẫn chạy **version cũ**.

> "Tôi đã merge PR hôm qua mà, sao feature chưa lên?"

### 🔍 Triệu chứng

```bash
# CI shows
✅ Build successful
✅ Tests passed  
✅ Deploy to production  # <- Này fail silently

# Nhưng production
curl https://api.company.com/version
# v1.2.3  ← Version cũ, không phải v1.2.4 mới deploy
```

### 🕵️ Điều tra

```yaml
# Workflow
- name: Deploy
  run: |
    kubectl apply -f deployment.yaml
  # Không check kết quả!
```

```bash
# Thực tế kubectl apply OK, nhưng rollout fail
kubectl rollout status deployment/myapp
# error: deployment "myapp" exceeded its progress deadline
```

### 💡 Giải pháp

**1. Check rollout status:**

```yaml
- name: Deploy
  run: |
    kubectl apply -f deployment.yaml
    kubectl rollout status deployment/myapp --timeout=5m
    # Fail nếu rollout không complete!
```

**2. Smoke test sau deploy:**

```yaml
- name: Smoke test
  run: |
    sleep 30  # Wait for pods
    VERSION=$(curl -s https://api.company.com/version)
    if [ "$VERSION" != "${{ github.sha }}" ]; then
      echo "Deploy failed! Expected ${{ github.sha }}, got $VERSION"
      exit 1
    fi
```

**3. Notifications:**

```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: 'deployments'
    payload: |
      {
        "text": "❌ Deploy failed: ${{ github.repository }}"
      }
```

**4. Deploy verification:**

```yaml
- name: Verify deployment
  run: |
    # Check pods healthy
    kubectl wait --for=condition=Ready pods -l app=myapp --timeout=120s
    
    # Check endpoints
    ENDPOINTS=$(kubectl get endpoints myapp -o jsonpath='{.subsets[*].addresses[*].ip}')
    if [ -z "$ENDPOINTS" ]; then
      echo "No healthy endpoints!"
      exit 1
    fi
```

### 🧠 Bài học

- **kubectl apply ≠ deploy success** - Chỉ là submit request
- **Verify rollout** - Check pods thực sự healthy
- **Smoke tests** - Gọi API và verify
- **Notifications** - Team phải biết khi deploy fail

---

## Scenario 5: CI/CD downtime - Không thể deploy

### 📋 Bối cảnh

**Hotfix cần deploy GẤP** nhưng CI/CD platform đang down.

> GitHub Actions: Major outage in progress

Production có bug critical, không thể deploy fix!

### 🔍 Triệu chứng

```
GitHub Status Page:
🔴 Actions - Major outage
   Investigating - We are investigating reports of degraded performance
```

### 💡 Giải pháp

**1. Manual deploy backup:**

```bash
# Document quy trình deploy thủ công
# deploy-manual.md

1. Build locally
   docker build -t myapp:hotfix .

2. Push to registry
   docker push registry.company.com/myapp:hotfix

3. Connect to cluster
   kubectl config use-context production

4. Update deployment
   kubectl set image deployment/myapp myapp=registry.company.com/myapp:hotfix

5. Verify
   kubectl rollout status deployment/myapp
```

**2. Multi-CI strategy:**

```yaml
# Có backup CI system
# .github/workflows/ci.yaml - Primary
# .gitlab-ci.yml - Backup
# Jenkinsfile - Emergency
```

**3. Self-hosted runners:**

```yaml
# Runners trong infrastructure của bạn
jobs:
  deploy:
    runs-on: [self-hosted, production]
    # Ít phụ thuộc vào GitHub infrastructure
```

**4. CD without CI:**

```bash
# Nếu CI down, có thể manually trigger CD
# ArgoCD, Flux vẫn hoạt động nếu manifest được update

git push origin main  # Trigger GitOps
argocd app sync myapp --force  # Manual sync
```

**5. Hotfix branch strategy:**

```bash
# Pre-build hotfix images
docker build -t myapp:hotfix-base .
docker push ...

# Khi cần, chỉ cần apply config change
kubectl edit deployment myapp
# Change image tag
```

### 🧠 Bài học

- **Single point of failure** - Đừng phụ thuộc 100% vào 1 CI
- **Document manual process** - Team phải biết deploy không có CI
- **Self-hosted runners** - Ít phụ thuộc vào cloud
- **GitOps helps** - ArgoCD/Flux có thể deploy độc lập

---

## 📝 CI/CD Health Checklist

- [ ] Pipeline < 10 phút
- [ ] Flaky test rate < 1%
- [ ] Secrets properly masked
- [ ] Deploy verification in place
- [ ] Failure notifications configured
- [ ] Manual deploy documented
- [ ] Backup CI available
