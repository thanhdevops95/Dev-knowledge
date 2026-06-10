# 🎓 GitHub Actions — Default CI/CD 2026

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [What is CI/CD](00_what-is-cicd.md)

> 🎯 *Master GitHub Actions: **workflow YAML**, **events**, **jobs + steps**, **actions marketplace**, **matrix**, **secrets + OIDC**, **caching**, **reusable workflows**, **environments**, **debug**. Sau bài này CI/CD project bất kỳ trong GitHub.*

## 🎯 Sau bài này bạn sẽ

- [ ] Viết workflow YAML đầy đủ
- [ ] Master **events** (push, PR, schedule, workflow_dispatch, ...)
- [ ] Dùng **actions marketplace** + **composite/Docker/JS** actions
- [ ] **Matrix** cho multi-version testing
- [ ] **Secrets** + **OIDC** (federated, no long-lived token)
- [ ] **Caching** speed up builds
- [ ] **Reusable workflows** DRY
- [ ] **Environments** + **deployment protection rules**
- [ ] Debug workflows (`ACTIONS_RUNNER_DEBUG`)

---

## 1️⃣ Giải phẫu workflow

GitHub Actions workflow là YAML file ở `.github/workflows/`. Structure cốt lõi: **on** (trigger) + **env** (vars) + **jobs** (parallel, mỗi job nhiều steps tuần tự). Template đầy đủ tham khảo:

```yaml
# .github/workflows/ci.yml
name: CI                                # Display name

on:                                     # ← Trigger events
  push:
    branches: [main, develop]
  pull_request:

env:                                    # ← Workflow-level env
  NODE_VERSION: "22"

jobs:
  test:                                # Job ID
    name: Run tests                     # Display name
    runs-on: ubuntu-latest              # ← Runner
    timeout-minutes: 15

    strategy:
      matrix:
        node: [18, 20, 22]              # ← Matrix
        os: [ubuntu-latest, macos-latest]

    steps:
    - name: Checkout code
      uses: actions/checkout@v4         # ← Action

    - name: Setup Node
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node }}
        cache: 'npm'

    - name: Install
      run: npm ci                       # ← Shell command

    - name: Test
      run: npm test
```

### Cấu trúc phân tầng

3 cấp hierarchy quan trọng — Workflow chứa nhiều Job (chạy parallel default), Job chứa nhiều Step (sequential), Step có `uses` (gọi Action) hoặc `run` (shell command):

```
Workflow
  └─ Job (parallel by default)
       └─ Step (sequential)
            └─ uses: action     OR
            └─ run: command
```

---

## 2️⃣ Events — Khi pipeline chạy

### Các event thường gặp

GitHub Actions hỗ trợ **~30 event** trigger — phổ biến nhất: push/pull_request (code event), schedule (cron), workflow_dispatch (manual), workflow_call (reusable). Phần `on:` định nghĩa:

```yaml
on:
  # Code events
  push:
    branches: [main, 'release/**']
    paths-ignore: ['**.md', 'docs/**']
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main]

  # Schedule (cron)
  schedule:
    - cron: '0 2 * * *'                  # 2 AM UTC daily

  # Manual trigger
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        type: choice
        options: [staging, production]

  # GitHub events
  issues:
    types: [opened]
  release:
    types: [published]

  # Other workflow
  workflow_call:                          # Reusable workflow
  workflow_run:                            # Run after another workflow
    workflows: [CI]
    types: [completed]
```

### Path filter

`paths`/`paths-ignore` tránh trigger workflow cho thay đổi không liên quan (vd commit chỉ sửa docs không cần chạy CI). Optimize quan trọng cho monorepo lớn — bỏ qua bằng `.md`/`docs/`:

```yaml
on:
  push:
    paths:
    - 'backend/**'
    - 'requirements.txt'
    paths-ignore:
    - '**.md'
    - 'docs/**'
```

→ Workflow chạy chỉ khi files match. Skip docs change save CI minutes.

### Kích hoạt thủ công với inputs

`workflow_dispatch` cho phép trigger thủ công với **inputs từ UI** — useful cho deploy command, hotfix, rollback. User pick từ dropdown (`choice`) hoặc nhập text:

```yaml
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version tag'
        required: true
        default: 'latest'
      environment:
        type: choice
        options: [staging, production]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - run: echo "Deploying ${{ inputs.version }} to ${{ inputs.environment }}"
```

→ "Run workflow" button trong GitHub UI → fill inputs.

---

## 3️⃣ Jobs + Steps chuyên sâu

### Phụ thuộc giữa job

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    needs: build                          # ← Wait for build
    steps: [...]

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]                  # ← Wait both
    if: github.ref == 'refs/heads/main'   # ← Conditional
    steps: [...]
```

### Chạy có điều kiện

```yaml
jobs:
  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

```yaml
steps:
- name: Notify Slack on fail
  if: failure()
  run: ./notify.sh
- name: Always cleanup
  if: always()
  run: ./cleanup.sh
- name: Only on success
  if: success()
  run: ./success.sh
```

### Điều kiện chạy

```
success()    job/step success
failure()    job/step failed
always()     always run
cancelled()  job cancelled
```

---

## 4️⃣ Actions — Khối xây dựng

**Action** = pre-built reusable unit. Marketplace: github.com/marketplace.

### 3 loại

| Type | Description |
|---|---|
| **JavaScript** | Node.js code, fast | actions/checkout@v4 |
| **Docker** | Container, language-agnostic | hashicorp/setup-terraform |
| **Composite** | YAML wrap multiple steps | Custom org actions |

### Dùng action

```yaml
- name: Checkout
  uses: actions/checkout@v4
  with:
    fetch-depth: 0                       # Full history (default 1)
    submodules: recursive
```

### Top 10 actions phổ biến

| Action | Purpose |
|---|---|
| **actions/checkout** | Clone repo |
| **actions/setup-node** | Install Node + cache npm |
| **actions/setup-python** | Install Python + cache pip |
| **actions/setup-go** | Install Go |
| **actions/cache** | Generic cache |
| **actions/upload-artifact / download-artifact** | Share files across jobs |
| **docker/build-push-action** | Build + push Docker image |
| **docker/login-action** | Login to registry |
| **aws-actions/configure-aws-credentials** | AWS auth (OIDC) |
| **google-github-actions/auth** | GCP auth (OIDC) |

### Pin theo SHA (bảo mật)

```yaml
- uses: actions/checkout@v4              # Tag — can be updated maliciously
- uses: actions/checkout@a12345678        # SHA — immutable
```

→ Production: pin to SHA. Dependabot keep updated.

---

## 5️⃣ Secrets + OIDC

### Repository secret

GitHub UI: Settings → Secrets → Actions → New secret.

```yaml
steps:
- run: |
    echo "DB password: $DB_PASSWORD"
  env:
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

→ Secrets **masked** trong logs. Never echo to print.

### Environment secret

```yaml
jobs:
  deploy-prod:
    environment: production               # ← Use env secrets
    steps:
    - env:
        API_KEY: ${{ secrets.API_KEY }}    # Different from staging API_KEY
```

→ Environment = scoped secrets + approval rules.

### Organization secret

GitHub Org settings → Secrets → Actions. Share secrets across repos.

### OIDC — Auth hiện đại lên cloud (không cần long-lived secret!)

**Old way**: AWS_ACCESS_KEY in secret → leak risk + rotation pain.

**New way**: OIDC token generated per workflow → trade for short-lived AWS credentials.

```yaml
jobs:
  deploy:
    permissions:
      id-token: write                     # ← OIDC token request
      contents: read
    steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789:role/github-deploy
        aws-region: us-east-1
    - run: aws s3 cp build/ s3://my-bucket/ --recursive
```

→ AWS IAM trust GitHub OIDC issuer. No `AWS_ACCESS_KEY_ID` secret. **2026 best practice**.

→ Same pattern for GCP (Workload Identity Federation), Azure, HashiCorp Vault.

---

## 6️⃣ Caching — Speed up builds

### Cache có sẵn (setup-* actions)

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: 'npm'                          # Auto cache ~/.npm + node_modules

- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'

- uses: actions/setup-go@v5
  with:
    go-version: '1.22'
    cache: true                            # Auto cache modules
```

### Cache thủ công

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/registry
      ~/.cargo/git
      target
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-
```

→ Key match → restore. Mismatch → restore from `restore-keys` partial match.

### Docker layer caching

```yaml
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha                  # ← GitHub Actions cache backend
    cache-to: type=gha,mode=max
    tags: myapp:latest
```

→ Reuse layers across builds. Image build 5min → 30s.

---

## 7️⃣ Matrix — Test nhiều cấu hình

### Cơ bản

```yaml
jobs:
  test:
    strategy:
      fail-fast: false                     # Don't cancel others on first fail
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
    runs-on: ${{ matrix.os }}
    steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node }}
```

→ Generates 9 jobs (3 OS × 3 Node).

### Include / exclude (thêm/bớt tổ hợp)

```yaml
matrix:
  os: [ubuntu, macos]
  node: [18, 22]
  include:
  - os: ubuntu
    node: 20                                # Add extra combo
    experimental: true
  exclude:
  - os: macos
    node: 18                                # Skip combo
```

### Truyền output giữa các job

```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.meta.outputs.version }}
    steps:
    - id: meta
      run: echo "version=v1.${{ github.run_number }}" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    steps:
    - run: echo "Deploying ${{ needs.build.outputs.version }}"
```

---

## 8️⃣ Reusable workflows — DRY

### Định nghĩa reusable workflow

```yaml
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      AWS_ROLE:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE }}
        aws-region: us-east-1
    - run: ./deploy.sh ${{ inputs.environment }}
```

### Cách dùng

```yaml
# .github/workflows/cd.yml
jobs:
  staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
    secrets:
      AWS_ROLE: ${{ secrets.AWS_STAGING_ROLE }}

  production:
    needs: staging
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets:
      AWS_ROLE: ${{ secrets.AWS_PROD_ROLE }}
```

→ DRY across repos: `uses: org/repo/.github/workflows/x.yml@v1`.

### Composite action

```yaml
# .github/actions/setup-app/action.yml
name: Setup App
description: Install deps + cache

inputs:
  python-version:
    required: true

runs:
  using: composite
  steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ inputs.python-version }}
      cache: 'pip'
  - shell: bash
    run: pip install -r requirements.txt
```

```yaml
# Use it
- uses: ./.github/actions/setup-app
  with:
    python-version: '3.12'
```

---

## 9️⃣ Environments + Bảo vệ deployment

### Định nghĩa environment

GitHub UI: Settings → Environments → New.

Settings per environment:
- **Required reviewers** — manual approve before deploy.
- **Wait timer** — delay before deploy.
- **Deployment branches** — only certain branches.
- **Environment secrets** — scoped.

### Dùng trong workflow

```yaml
jobs:
  deploy:
    environment:
      name: production
      url: https://acmeshop.vn
    steps:
    - run: ./deploy.sh
```

→ Action **wait** for approval. Click "Approve and deploy" trong GitHub UI. Plus `url` show "View deployment" link.

### Pattern: staging tự động, prod thủ công

```yaml
jobs:
  deploy-staging:
    environment: staging                  # No approval
    steps: [...]

  deploy-prod:
    needs: deploy-staging
    environment: production               # Approval required
    steps: [...]
```

---

## 1️⃣0️⃣ Debug workflow

### Hiển thị biến

```yaml
- name: Show context
  run: echo "${{ toJSON(github) }}"
```

### Bật debug logs

GitHub UI: Settings → Secrets → Actions →

```
ACTIONS_RUNNER_DEBUG = true
ACTIONS_STEP_DEBUG = true
```

→ Re-run with debug. Logs verbose.

### `act` — Chạy workflow ở local

```bash
brew install act
act push                                 # Simulate push event
act -j test                              # Run specific job
```

→ Fast iterate without push.

### Trace workflow

```yaml
- name: Trace
  run: |
    echo "Branch: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Event: ${{ github.event_name }}"
    env                                  # Print all env vars
```

---

## 1️⃣1️⃣ Full FastAPI workflow của bạn

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: 'pip'
    - run: pip install ruff black mypy
    - run: ruff check .
    - run: black --check .
    - run: mypy app/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:18
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 10s
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: 'pip'
    - run: pip install -r requirements.txt
    - run: pytest --cov=app --cov-report=xml
      env:
        DATABASE_URL: postgresql://postgres:test@localhost:5432/test
    - uses: codecov/codecov-action@v4
      with:
        file: ./coverage.xml

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      digest: ${{ steps.build.outputs.digest }}
    steps:
    - uses: actions/checkout@v4
    - uses: docker/setup-buildx-action@v3
    - uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - uses: docker/metadata-action@v5
      id: meta
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=sha
          type=ref,event=branch
          type=semver,pattern={{version}}
    - uses: docker/build-push-action@v5
      id: build
      with:
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.acmeshop.vn
    permissions:
      id-token: write
    steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_STAGING_ROLE }}
        aws-region: us-east-1
    - run: |
        aws eks update-kubeconfig --name acmeshop-staging
        kubectl set image deployment/fastapi \
          fastapi=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build.outputs.digest }} \
          -n staging
        kubectl rollout status deployment/fastapi -n staging --timeout=5m

  deploy-prod:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://acmeshop.vn
    permissions:
      id-token: write
    steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_PROD_ROLE }}
        aws-region: us-east-1
    - run: |
        aws eks update-kubeconfig --name acmeshop-prod
        kubectl set image deployment/fastapi \
          fastapi=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build.outputs.digest }} \
          -n production
        kubectl rollout status deployment/fastapi -n production --timeout=10m
```

→ Production-grade pipeline: 4 jobs parallel optimization, OIDC auth (no long-lived secrets), GitHub registry, immutable image digest, staging → prod manual approve.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Tags `v4`** thay SHA → supply chain attack vector. Pin SHA cho 3rd-party. Official `actions/*` OK tag.
2. **Secret echo to log** → logs leak (sometimes masking miss). Never `echo $SECRET`.
3. **No cache** → 10min build every time. `cache: 'npm'` + Docker GHA cache.
4. **Workflow chạy ngẫu nhiên** → no path filter. Use `paths: ['backend/**']`.
5. **Long-lived secrets cho cloud** → leak = compromise forever. Use OIDC (federated).

---

## 🧠 Tự kiểm tra (Self-check)

1. **3 events** thường dùng trong workflow?
2. Cách share output từ **job A** sang **job B**?
3. **OIDC** giải quyết vấn đề gì so với long-lived secrets?
4. **Matrix** + `fail-fast: false` — khi nào dùng?
5. Pin action `actions/checkout@v4` vs `@SHA` — chọn cái nào prod?

<details>
<summary>Gợi ý đáp án</summary>

1. **`push`** (commit on branch), **`pull_request`** (PR), **`workflow_dispatch`** (manual + inputs). Bonus: `schedule` (cron), `release`, `workflow_call` (reusable).

2. Set output trong job A via `$GITHUB_OUTPUT`:
   ```yaml
   jobs:
     a:
       outputs:
         version: ${{ steps.x.outputs.version }}
       steps:
       - id: x
         run: echo "version=v1.0" >> $GITHUB_OUTPUT
     b:
       needs: a
       steps:
       - run: echo ${{ needs.a.outputs.version }}
   ```

3. **Long-lived secrets** (AWS_ACCESS_KEY in repo) = leak forever, rotation pain. **OIDC**: GitHub generate token per workflow → AWS IAM trust GitHub OIDC issuer → trade for short-lived AWS creds (1hr default). No secret in repo. **2026 best practice cho cloud auth**.

4. **`fail-fast: false`** = don't cancel siblings on first fail. Use khi: want all matrix cells run (full test report), independent jobs. Default `true` = stop early to save CI minutes (preferred when fail = clear bug).

5. **Production: SHA**. Tag mutable — maintainer could push malicious code dưới tag `v4`. SHA immutable. Dependabot auto-PR update SHA. Trade-off: noisy PRs vs security. Official `actions/*` (GitHub-owned) trust tag OK; community actions pin SHA.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Workflow tối thiểu

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 22
        cache: 'npm'
    - run: npm ci && npm test
```

### Matrix

```yaml
strategy:
  matrix:
    node: [18, 20, 22]
    os: [ubuntu, macos]
```

### Điều kiện

```yaml
if: github.event_name == 'push'
if: github.ref == 'refs/heads/main'
if: success() / failure() / always() / cancelled()
```

### OIDC AWS

```yaml
permissions:
  id-token: write
steps:
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123:role/x
    aws-region: us-east-1
```

### Cache

```yaml
cache: 'npm' / 'pip' / 'gradle' / true  # in setup-*

# manual:
- uses: actions/cache@v4
  with:
    path: ~/.cargo
    key: ${{ hashFiles('Cargo.lock') }}
```

### Reusable

```yaml
on:
  workflow_call:
    inputs: { env: { required: true, type: string } }
    secrets: { TOKEN: { required: true } }

# Caller:
uses: ./.github/workflows/reusable.yml
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Workflow** | YAML file định nghĩa CI/CD |
| **Job** | Group of steps on a runner |
| **Step** | Single command or action |
| **Action** | Reusable unit from marketplace |
| **Runner** | Machine (ubuntu/macos/windows) executing |
| **Trigger / Event** | What starts workflow |
| **Matrix** | Multi-config job expansion |
| **Cache** | Persist files between runs |
| **Artifact** | Files saved between jobs |
| **Secret** | Sensitive data, masked in logs |
| **OIDC** | OpenID Connect — federated auth |
| **Environment** | Scoped secrets + protection rules |
| **Reusable workflow** | Workflow callable from another |
| **Composite action** | YAML wrap multiple steps |
| **`act`** | Run workflows locally for testing |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [CI/CD là gì? — Automate build, test, deploy](00_what-is-cicd.md)
- ➡️ **Bài tiếp theo:** [GitLab CI — Pipeline cho GitLab + self-host](02_gitlab-ci.md)
- ↑ **Về cụm:** [ci-cd README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [GitHub Actions docs](https://docs.github.com/en/actions)
- 📖 [Actions marketplace](https://github.com/marketplace?type=actions)
- 📖 [act — run workflows locally](https://github.com/nektos/act)
- 📖 [Awesome Actions list](https://github.com/sdras/awesome-actions)
- 📖 [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

---

> 🎯 *Sau bài này GitHub Actions thuần thục. Bài kế tiếp đi sâu **GitLab CI** — alternative cho GitLab repos.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster ci-cd basic lesson 2/5. Cover: workflow YAML structure + events (push/PR/schedule/dispatch) + jobs/steps + matrix + actions/setup-* + secrets + OIDC + reusable workflow + composite actions + caching.
- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước §1 Anatomy + Hierarchy + §2 Common events + Path filter + Manual inputs.
- **v1.1.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
