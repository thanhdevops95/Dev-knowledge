# 📝 Quiz & Self-Test - CI/CD

Kiểm tra kiến thức CI/CD của bạn với 20 câu hỏi từ cơ bản đến nâng cao.

---

## 🟢 Cơ bản (1-7)

### Q1: CI vs CD

CI và CD khác nhau như thế nào?

- [ ] A. CI và CD là như nhau
- [ ] B. CI = Build/Test, CD = Deploy
- [ ] C. CI = Deploy, CD = Build/Test
- [ ] D. CI dùng cho frontend, CD dùng cho backend

<details>
<summary>💡 Đáp án</summary>

**B đúng**

- **CI (Continuous Integration)**: Merge code thường xuyên + Automated build/test
- **CD (Continuous Delivery/Deployment)**: Automated deployment

```
Developer push → CI (build, test, lint) → CD (deploy staging/prod)
```

</details>

---

### Q2: Continuous Delivery vs Continuous Deployment

Continuous Delivery khác Continuous Deployment như thế nào?

<details>
<summary>💡 Đáp án</summary>

| Continuous Delivery | Continuous Deployment |
|---------------------|----------------------|
| Deploy **ready** nhưng cần manual approval | Deploy **automatic** lên production |
| Human gate trước production | No human gate |
| Ít risk hơn | Cần test coverage cao |

```
Continuous Delivery:    CI → Artifact → Manual Approve → Deploy
Continuous Deployment:  CI → Artifact → Auto Deploy
```

</details>

---

### Q3: GitHub Actions Workflow

File GitHub Actions workflow phải đặt ở đâu?

- [ ] A. Root folder
- [ ] B. .github/workflows/
- [ ] C. .actions/
- [ ] D. workflows/

<details>
<summary>💡 Đáp án</summary>

**B đúng**

```
project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── src/
└── README.md
```

</details>

---

### Q4: Pipeline Triggers

Event nào trigger workflow khi có PR?

- [ ] A. push
- [ ] B. pull_request
- [ ] C. workflow_dispatch
- [ ] D. schedule

<details>
<summary>💡 Đáp án</summary>

**B đúng**

```yaml
on:
  push:             # Khi push code
    branches: [main]
  pull_request:     # Khi tạo/update PR
    branches: [main]
  workflow_dispatch: # Manual trigger
  schedule:          # Cron schedule
    - cron: '0 0 * * *'
```

</details>

---

### Q5: Build Artifacts

Artifact trong CI/CD là gì?

<details>
<summary>💡 Đáp án</summary>

**Artifact** = Output của build process:

- Docker image
- JAR/WAR file
- Compiled binary
- Build logs
- Test reports

```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v3
  with:
    name: build-output
    path: dist/
```

</details>

---

### Q6: Environment Variables

Cách nào safe để pass secrets vào CI/CD?

- [ ] A. Hardcode trong workflow file
- [ ] B. Commit vào .env file
- [ ] C. Dùng Repository Secrets
- [ ] D. Pass qua URL

<details>
<summary>💡 Đáp án</summary>

**C đúng**

```yaml
# ✅ Safe - dùng secrets
env:
  API_KEY: ${{ secrets.API_KEY }}

# ❌ KHÔNG safe
env:
  API_KEY: "abc123"  # Hardcoded!
```

Secrets được encrypt và chỉ available khi run.

</details>

---

### Q7: Job Dependencies

Làm sao để Job B chạy sau Job A?

<details>
<summary>💡 Đáp án</summary>

Dùng `needs`:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm build

  test:
    needs: build  # Đợi build xong
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  deploy:
    needs: [build, test]  # Đợi cả build và test
    runs-on: ubuntu-latest
```

</details>

---

## 🟡 Trung bình (8-14)

### Q8: Matrix Builds

Matrix strategy dùng để làm gì?

<details>
<summary>💡 Đáp án</summary>

Matrix = Run job với nhiều configurations:

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [16, 18, 20]
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
# Chạy 6 jobs: 3 node versions × 2 OS
```

</details>

---

### Q9: Caching

Cache trong CI giúp gì?

<details>
<summary>💡 Đáp án</summary>

Cache giúp:

- **Faster builds** - Không download lại dependencies
- **Less network** - Tiết kiệm bandwidth
- **Cheaper** - Ít compute time

```yaml
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

Cache hit → Skip `npm install` → Save 3-5 minutes

</details>

---

### Q10: Conditional Steps

Làm sao để step chỉ chạy khi push vào main?

<details>
<summary>💡 Đáp án</summary>

Dùng `if`:

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

# Chỉ chạy khi failure
- name: Notify on failure
  if: failure()
  run: curl -X POST $SLACK_WEBHOOK

# Chạy mọi trường hợp
- name: Cleanup
  if: always()
  run: rm -rf tmp/
```

</details>

---

### Q11: Reusable Workflows

Làm sao để reuse workflow giữa các repos?

<details>
<summary>💡 Đáp án</summary>

```yaml
# .github/workflows/reusable.yml (repo A)
on:
  workflow_call:
    inputs:
      environment:
        type: string
        required: true
    secrets:
      API_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: deploy --env ${{ inputs.environment }}
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

```yaml
# .github/workflows/main.yml (repo B)
jobs:
  call-reusable:
    uses: org/repo-a/.github/workflows/reusable.yml@main
    with:
      environment: production
    secrets:
      API_KEY: ${{ secrets.API_KEY }}
```

</details>

---

### Q12: Branch Protection

Branch protection rules bao gồm gì?

<details>
<summary>💡 Đáp án</summary>

Branch protection rules:

- **Require PR** - Không push trực tiếp
- **Require CI pass** - Status checks phải pass
- **Require reviews** - Ít nhất 1-2 approvals
- **Require signed commits** - GPG signed
- **No force push** - Protect history

```
Settings > Branches > Branch protection rules
☑ Require a pull request before merging
☑ Require status checks to pass before merging
  ☑ ci / build
  ☑ ci / test
☑ Require review from Code Owners
```

</details>

---

### Q13: Self-hosted Runners

Khi nào dùng self-hosted runners?

<details>
<summary>💡 Đáp án</summary>

Self-hosted runners khi:

- **Special hardware** - GPU, specific CPU
- **Long-running jobs** - Vượt time limits
- **Network access** - Private resources
- **Cost optimization** - Cheaper cho high usage
- **Compliance** - Data không ra cloud

```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64]
```

Trade-offs:

- Phải manage và secure
- Phải scale manually

</details>

---

### Q14: Deployment Strategies

Blue-Green deployment hoạt động như thế nào?

<details>
<summary>💡 Đáp án</summary>

Blue-Green:

1. **Blue** = Current production (live)
2. **Green** = New version (staging)
3. Test Green fully
4. Switch traffic từ Blue → Green
5. Blue becomes standby (rollback)

```
Before:  Traffic → [Blue v1] ← Live
                   [Green v2] ← Testing

Switch:  Traffic → [Green v2] ← Live
                   [Blue v1] ← Standby

Rollback: Traffic → [Blue v1] ← Live (instant!)
```

</details>

---

## 🔴 Nâng cao (15-20)

### Q15: Pipeline Security

Supply chain attacks trong CI/CD là gì?

<details>
<summary>💡 Đáp án</summary>

Supply chain attacks:

- **Compromised dependencies** - Malicious npm packages
- **Compromised actions** - Malicious GitHub actions
- **Compromised base images** - Malware in Docker images

Prevention:

```yaml
# Pin versions exactly
uses: actions/checkout@v4.1.0  # Không @v4 hoặc @main

# Verify checksums
- run: npm ci  # Lockfile integrity check

# Scan dependencies
- name: Dependency scan
  uses: snyk/actions/node@master
```

</details>

---

### Q16: GitOps

GitOps khác traditional CI/CD như thế nào?

<details>
<summary>💡 Đáp án</summary>

| Traditional CD | GitOps |
|----------------|--------|
| Push-based | Pull-based |
| CI pushes to cluster | Agent pulls from Git |
| CI needs cluster creds | Agent runs in cluster |

```
Traditional:
CI → kubectl apply → Cluster

GitOps:
Git ← ArgoCD watches ← Cluster
Developer push → Git → ArgoCD detects → Cluster updates
```

Benefits:

- **Git = Single source of truth**
- **Audit trail** - All changes in Git history
- **No CI cluster access** - More secure

</details>

---

### Q17: Pipeline Optimization

Pipeline mất 30 phút. Làm sao optimize?

<details>
<summary>💡 Đáp án</summary>

Optimization strategies:

1. **Cache dependencies**

```yaml
- uses: actions/cache@v3
```

2. **Parallel jobs**

```yaml
jobs:
  lint:  # Parallel
  test:  # Parallel
  scan:  # Parallel
  build:
    needs: [lint, test, scan]  # Wait after all
```

3. **Skip unnecessary**

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
```

4. **Faster runners**

```yaml
runs-on: ubuntu-latest-4-cores
```

5. **Parallel tests**

```bash
pytest -n auto  # Parallel test execution
```

</details>

---

### Q18: Secrets Management

Làm sao rotate secrets mà không downtime?

<details>
<summary>💡 Đáp án</summary>

Dual-secret rotation:

1. **Add new secret** (OLD + NEW both valid)
2. **Update application** to use new secret
3. **Verify** application works
4. **Remove old secret**

```yaml
# Step 1: Add new secret, keep old
secrets:
  API_KEY: "new-key"
  API_KEY_OLD: "old-key"  # Temporary

# Step 2: App tries new first, fallback to old
def get_api_key():
    return os.environ.get('API_KEY') or os.environ.get('API_KEY_OLD')

# Step 3: Verify working
# Step 4: Remove API_KEY_OLD
```

</details>

---

### Q19: Rollback Strategies

Có những cách rollback nào khi deployment fail?

<details>
<summary>💡 Đáp án</summary>

1. **Instant rollback** (Blue-Green)

```bash
kubectl patch service myapp -p '{"spec":{"selector":{"version":"v1"}}}'
```

2. **Git revert** (GitOps)

```bash
git revert HEAD
git push
# ArgoCD auto-deploys previous state
```

3. **Helm rollback**

```bash
helm rollback myapp 1
```

4. **Kubernetes rollback**

```bash
kubectl rollout undo deployment/myapp
```

5. **Feature flags**

```python
if feature_flag.enabled('new-feature'):
    new_code()
else:
    old_code()  # Instant "rollback" by toggling flag
```

</details>

---

### Q20: DORA Metrics

DORA metrics đo gì?

<details>
<summary>💡 Đáp án</summary>

**DORA** (DevOps Research and Assessment) 4 key metrics:

| Metric | Measure | Elite |
|--------|---------|-------|
| **Deployment Frequency** | How often deploy | Multiple times/day |
| **Lead Time for Changes** | Commit → Production | < 1 hour |
| **Change Failure Rate** | % deployments cause failure | < 15% |
| **Mean Time to Recover** | Time to fix failure | < 1 hour |

```
Elite teams:
- Deploy 100+ times/day
- Lead time < 1 hour
- Failure rate < 5%
- MTTR < 1 hour
```

</details>

---

## 📊 Đánh giá

| Score | Level |
|-------|-------|
| 0-7 | 🟢 Beginner - Cần học thêm basics |
| 8-14 | 🟡 Intermediate - Đang tiến bộ |
| 15-18 | 🔴 Advanced - Hiểu sâu |
| 19-20 | ⭐ Expert - Sẵn sàng interview |

---

[← Về README](README.md) | [LABS.md →](LABS.md) | [SCENARIOS.md →](SCENARIOS.md)
