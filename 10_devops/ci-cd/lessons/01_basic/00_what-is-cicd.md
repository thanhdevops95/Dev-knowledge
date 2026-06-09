# 🎓 CI/CD là gì? — Automate build, test, deploy

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [Git basics](../../../../02_tools/git/), [Docker](../../../docker/)

> 🎯 *Bài INTRO. Hiểu **CI/CD** (Continuous Integration + Continuous Delivery/Deployment), **why** + **lịch sử**, **landscape 2026** (GitHub Actions / GitLab CI / CircleCI / Jenkins / Drone), **anatomy pipeline**, **trunk-based vs Gitflow**, **DORA metrics**.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **CI** vs **CD** (delivery vs deployment)
- [ ] Hiểu lịch sử: Jenkins → Travis → CircleCI → GitHub Actions
- [ ] So sánh **5 tools** chính 2026
- [ ] **Anatomy pipeline**: trigger → build → test → deploy
- [ ] **Trunk-based** vs **Gitflow** development model
- [ ] **DORA metrics** (Deployment frequency, Lead time, MTTR, Change failure rate)
- [ ] Khi nào **self-host** runner vs cloud
- [ ] Lộ trình setup CI/CD đầu tiên

---

## Tình huống — Bạn deploy thủ công, đời khổ

Bạn viết FastAPI + React. Mỗi lần update code:
```bash
ssh prod-server
git pull
cd backend && pip install + alembic upgrade
docker build -t myapp:latest .
docker compose up -d
cd ../frontend && npm install && npm run build
rsync dist/ /var/www/
sudo systemctl reload nginx
```

→ 30 phút SSH + clicking. Bug giờ deploy không nhớ steps. **Manual** = **error-prone + slow**.

Bạn ngơ:
- **CI/CD** giúp gì cụ thể?
- Tools nào — GitHub Actions, Jenkins, GitLab CI?
- Setup mất bao lâu?
- Test có cần phần này?

Senior:
> *"Push code → GitHub Actions auto build + test + deploy. Bug detect trong 5 phút. Deploy 1 click hoặc auto. **Mọi team modern dùng CI/CD** — không có không scale được."*

→ Bài này tổng quan + lộ trình.

---

## 1️⃣ CI vs CD vs CD — Definitions

### CI — Continuous Integration

**CI** = mỗi push code → auto:
- Lint
- Build
- Run tests
- Static analysis

→ Catch bug **sớm** (vài phút sau commit) thay vì cuối sprint.

### CD — Continuous Delivery

**CD** (Delivery) = mọi commit pass CI → **ready to deploy** at any time. Deployment **manual trigger**.

### CD — Continuous Deployment

**CD** (Deployment) = mỗi commit pass CI → **auto deploy production** (no human).

| Practice | Auto deploy prod? | Common at |
|---|---|---|
| CI | No (just build/test) | Everyone |
| Continuous **Delivery** | No (manual trigger) | Enterprise, banking |
| Continuous **Deployment** | YES (auto) | Tech startups, FAANG |

→ **Confusion**: "CI/CD" thường nghĩa cả workflow (CI + Delivery hoặc Deployment).

### Visualization

Flow CI/CD đầy đủ từ commit code đến production gồm **4 stage** nối tiếp — build/test (CI), deploy staging, deploy prod. Bước cuối là **manual gate** (Delivery) hoặc **auto** (Deployment) — khác biệt cốt lõi 2 khái niệm:

```
Developer push code
        │
        ▼
   [CI: Build + Test]   ← Mỗi commit
        │
   pass / fail
        │
        ▼
   [CD: Deploy staging]
        │
        ▼
   [CD: Deploy prod]    ← Manual (Delivery) hoặc Auto (Deployment)
```

---

## 2️⃣ Lịch sử + Tools landscape 2026

### Evolution

CI/CD tool có **6 thế hệ** qua 20 năm — từ Jenkins on-premise (2005) đến cloud-native GitHub Actions (2018) và Dagger programmable (2020+). Mỗi thế hệ giải quyết pain point của thế hệ trước:

| Year | Tool | Innovation |
|---|---|---|
| 2005 | **Jenkins** (Hudson) | First popular CI server, plugin ecosystem |
| 2011 | **Travis CI** | First cloud CI for open source |
| 2012 | **CircleCI** | Container-based, fast |
| 2014 | **GitLab CI** | Integrated with GitLab |
| 2018 | **GitHub Actions** | YAML workflow, free for OSS |
| 2020+ | **Drone, BuildKite, Dagger** | Specialized |

### Tools 2026 — Compare

8 tool CI/CD chính 2026 — bảng so sánh 3 trục: type (cloud/self-host), free tier, strengths. Pick đúng tool tiết kiệm hàng giờ ops + cost:

| Tool | Type | Free tier | Strengths |
|---|---|---|---|
| **GitHub Actions** | Cloud + self-host | Generous public/free | **Default 2026** — integrate GitHub tightly |
| **GitLab CI** | Cloud + self-host | 400 CI mins/mo | All-in-one (DevOps platform) |
| **CircleCI** | Cloud | 6000 min/mo | Fast, mature |
| **Jenkins** | Self-host | Free (need ops) | Plugin king, mature, but old UX |
| **Drone** | Self-host | Free | Lightweight, container-native |
| **BuildKite** | Hybrid | Free public | Self-host runners + SaaS UI |
| **Dagger** | Programmable | Free | "CI as code" via SDK |
| **Argo Workflows** | K8s-native | Free | DAG workflows on K8s |

### Pick cho 2026

Decision matrix nhanh cho 6 use case phổ biến nhất. Quy tắc đơn giản: **dùng CI cùng platform** với code repo (GitHub Actions cho GitHub, GitLab CI cho GitLab):

| Use case | Choose |
|---|---|
| **GitHub repo** | **GitHub Actions** (default) |
| **GitLab repo** | **GitLab CI** (integrated) |
| **Self-host all** | Jenkins (mature) or Drone (modern) |
| **Mono-repo big** | Buildkite, BuildKite |
| **K8s-native** | Argo Workflows + Tekton |
| **Polyglot, complex flows** | Dagger (programmable) |

→ **Default 2026 cho 80% project**: **GitHub Actions** nếu code trên GitHub, **GitLab CI** nếu GitLab.

---

## 3️⃣ Anatomy of a pipeline

Mọi CI/CD pipeline (dù GitHub Actions, GitLab CI, Jenkins) đều có **4 thành phần cơ bản** — trigger, jobs, steps, secrets. Hiểu skeleton này sẽ đọc được mọi pipeline YAML:

```yaml
# Generic pipeline
name: CI/CD

on:                                   # ← Trigger
  push:
    branches: [main]
  pull_request:

jobs:
  build:                              # ← Job 1
    runs-on: ubuntu-latest             # ← Runner (where it runs)
    steps:                             # ← Sequence of actions
    - uses: actions/checkout@v4         # Step 1: get code
    - run: npm install                  # Step 2: install
    - run: npm run build                # Step 3: build

  test:                                # ← Job 2 (parallel with build)
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: npm test

  deploy:                              # ← Job 3
    needs: [build, test]                # ← Wait for build + test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'  # Only on main branch
    steps:
    - run: ./deploy.sh
```

### Components

| Component | Role |
|---|---|
| **Trigger** | Event start pipeline (push, PR, schedule, manual) |
| **Job** | Group of steps run on 1 runner |
| **Step** | Single command or action |
| **Runner** | Machine executing (GitHub-hosted or self-hosted) |
| **Artifact** | Output saved between jobs (built binary, test results) |
| **Cache** | Speed up subsequent runs (npm cache, Docker layers) |
| **Secret** | Sensitive data (API tokens, deploy keys) |
| **Matrix** | Run same job với multiple configs (Node 18 + 20, OS Linux + Mac) |

### Typical stages

```
1. Lint        (5s)   - ESLint, Black, Prettier
2. Build       (30s)  - Compile, bundle
3. Unit test    (1m)   - Pytest, Jest
4. Integration  (2m)  - Database tests, API tests
5. E2E          (5m)   - Playwright, Cypress
6. Security     (1m)   - SAST, dep scan
7. Build image  (2m)   - Docker build + push
8. Deploy       (30s)  - kubectl apply, terraform apply
```

→ Total ~10 phút. Run mọi PR + main commit.

---

## 4️⃣ Branching strategy — Trunk-based vs Gitflow

### Trunk-based (modern, recommended 2026)

```
main ─────●────●────●────●────●────●─→  (always deployable)
           ↑    ↑    ↑    ↑    ↑    ↑
          PR   PR   PR   PR   PR   PR
          (short-lived feature branches, 1-2 days)
```

- **Short-lived branches** (1-2 days).
- Merge to `main` frequently (multiple times/day).
- **Feature flags** for incomplete features.
- **CI/CD continuous**.

→ DORA "Elite performers" 80%+ trunk-based.

### Gitflow (classic, 2010)

```
main ────────────────────●────────●──→  (release)
                          │        │
develop ────●─●─●─●─●─────┴────●───┴──→  (integration)
            │ │ │
feature ────●─┘ │
                 │
release ─────────●─→
```

- Long-lived branches: `develop`, `release/*`, `hotfix/*`.
- Heavy merge conflict.
- Slow release cycle.

→ Outdated cho most teams. OK cho **versioned products** (libraries, OS).

### Compare

| Aspect | Trunk-based | Gitflow |
|---|---|---|
| Branch lifetime | Hours-days | Weeks-months |
| Deployment frequency | Multiple per day | Per sprint/month |
| Merge complexity | Low (small PRs) | High |
| Best for | SaaS, web apps | Versioned products |
| 2026 adoption | **70%+** | Declining |

---

## 5️⃣ DORA metrics — Đo CI/CD performance

**DORA** (DevOps Research and Assessment, by Google) — 4 metrics:

| Metric | Elite | High | Medium | Low |
|---|---|---|---|---|
| **Deployment frequency** | Multiple/day | Weekly | Monthly | <Monthly |
| **Lead time for changes** | <1 hour | <1 day | <1 week | <1 month |
| **Mean time to recovery (MTTR)** | <1 hour | <1 day | <1 day | <1 week |
| **Change failure rate** | 0-15% | 16-30% | 16-30% | 46-60% |

→ Goal: move **Low → Elite**. CI/CD foundation cho mọi metric.

### Get Elite

- Auto deploy mỗi commit pass CI.
- Comprehensive tests catch bugs.
- Feature flags cho safe rollout.
- Observability (metrics + logs) cho fast detect issues.
- Rollback mechanism (revert + auto rollback).

→ Sách "Accelerate" (Forsgren, Humble, Kim) bible.

---

## 6️⃣ Hosted vs Self-hosted runners

### Hosted runners (cloud)

```yaml
jobs:
  build:
    runs-on: ubuntu-latest      # ← GitHub-hosted
```

- ✅ Zero ops.
- ✅ Free tier (2000-3000 min/mo for private repos).
- ❌ Limited compute (2 cores, 7GB RAM).
- ❌ Can't access private infra.
- ❌ Slow Docker builds (no layer cache between runs default).

### Self-hosted runners

```yaml
jobs:
  build:
    runs-on: self-hosted
```

- ✅ More compute (GPU, big RAM).
- ✅ Access private network (corporate VPN).
- ✅ Persistent cache (faster builds).
- ❌ Need ops (patch, security).
- ❌ Cost (compute + maintenance).

### Hybrid

```yaml
jobs:
  test:
    runs-on: ubuntu-latest      # Cloud — fast spin-up
  deploy:
    runs-on: self-hosted         # Self-host — access private cluster
```

### Cost calc

- GitHub Actions free: 2000 min/mo private (Linux). $0.008/min after.
- Self-hosted on $10/mo VPS: unlimited (if 1 runner enough).
- Threshold: ~1250 min/mo → self-host cheaper.

→ Most startups stay cloud. Enterprise mixed.

---

## 7️⃣ Best practices 2026

### Pipeline design

- ✅ **Fast feedback** — fail in first 1-5 minutes.
- ✅ **Cache aggressive** — `npm`, `pip`, Docker layers, language deps.
- ✅ **Parallel jobs** — lint + test + security same time.
- ✅ **Matrix tests** — multiple OS / language versions.
- ✅ **Reusable workflows** — DRY pipeline YAML.

### Security

- ✅ **Don't commit secrets** — use secrets store.
- ✅ **OIDC over long-lived secrets** — federate GitHub → AWS/GCP.
- ✅ **Scan dependencies** — Dependabot, Renovate, Snyk.
- ✅ **SAST + DAST** — CodeQL, Semgrep, OWASP ZAP.
- ✅ **Sign artifacts** — Sigstore, Cosign.
- ✅ **Pin actions to SHA** — `actions/checkout@v4` → `actions/checkout@a12...`.

### Deploy

- ✅ **Blue-green or rolling** — zero downtime.
- ✅ **Canary** — release to 5% → 100%.
- ✅ **Feature flags** — decouple deploy from release.
- ✅ **Auto-rollback** on metrics regression.
- ✅ **GitOps** for K8s — ArgoCD, Flux.

→ Chi tiết deploy strategies ở [bài 04](04_deploy-strategies.md).

---

## 8️⃣ Lộ trình setup CI/CD đầu tiên

```
Week 1 — Basic CI
  ☐ GitHub Actions hello-world workflow
  ☐ Lint + test on PR
  ☐ Cache deps

Week 2 — Build + artifact
  ☐ Docker build + push to GHCR
  ☐ Tag với SHA + semver
  ☐ Matrix tests (Python 3.11, 3.12)

Week 3 — Deploy
  ☐ Deploy to staging on merge main
  ☐ Manual approve → prod
  ☐ Smoke tests post-deploy

Week 4 — Advanced
  ☐ Reusable workflows
  ☐ OIDC to cloud provider
  ☐ Security scanning
  ☐ Auto-rollback
```

→ 4 tuần đủ CI/CD production-grade cho mọi project.

---

## 9️⃣ Pipeline CI/CD đầu tiên của bạn

Bạn set up GitHub Actions cho FastAPI + React project.

### `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: 'pip'
    - run: pip install ruff black
    - run: ruff check .
    - run: black --check .

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:18
        env:
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: --health-cmd pg_isready
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: 'pip'
    - run: pip install -r requirements.txt
    - run: pytest --cov

  build-image:
    needs: [lint, test]
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
    - uses: actions/checkout@v4
    - uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - uses: docker/build-push-action@v5
      with:
        push: true
        tags: ghcr.io/acmeshop/fastapi:${{ github.sha }}

  deploy-staging:
    needs: build-image
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - uses: actions/checkout@v4
    - run: |
        kubectl set image deployment/fastapi \
          fastapi=ghcr.io/acmeshop/fastapi:${{ github.sha }} \
          -n staging
        kubectl rollout status deployment/fastapi -n staging
```

→ Push code → lint + test + build image + deploy staging. **Hết SSH manual**.

→ Chi tiết GitHub Actions ở [bài 01](01_github-actions.md). Deploy strategies ở [bài 04](04_deploy-strategies.md).

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Long-running branches** → merge hell. Trunk-based + feature flags.
2. **Slow CI** (15+ min) → devs frustrated, skip. Optimize: cache, parallel, only run affected.
3. **Secrets in code** → leak in git history forever. Always secret store.
4. **No test = no CI** → CI build pass nhưng prod bug. Tests are foundation.
5. **Auto-deploy without tests** → break production. Tests gate deploy.

---

## 🧠 Tự kiểm tra (Self-check)

1. Khác **Continuous Delivery** vs **Continuous Deployment**?
2. **4 DORA metrics** + target Elite?
3. **GitHub Actions** vs **Jenkins** — chọn cái nào 2026?
4. **Trunk-based** vs **Gitflow** — khi nào dùng cái nào?
5. **Self-hosted runner** — khi nào cần?

<details>
<summary>Gợi ý đáp án</summary>

1. **Delivery**: mọi commit pass CI → **ready** to deploy (deploy manual trigger). **Deployment**: mọi commit pass CI → **auto** deploy prod (no human). Both "CD" — confusing. Delivery: enterprise/banking. Deployment: tech startups.

2. (a) **Deployment frequency** — Elite: multiple/day. (b) **Lead time for changes** — Elite: <1 hour. (c) **MTTR** — Elite: <1 hour. (d) **Change failure rate** — Elite: 0-15%. DORA = bible đo DevOps performance.

3. **GitHub Actions 2026** for new projects on GitHub — integrate native, YAML workflow, generous free tier, marketplace actions. **Jenkins** mature + plugin king nhưng UX cũ + self-host overhead. New project: GitHub Actions/GitLab CI. Legacy/complex existing Jenkins: maintain.

4. **Trunk-based** for **SaaS / web apps** — fast iteration, short branches, deploy multiple/day. **Gitflow** for **versioned products** (libraries, OS releases) — version bump, release branches. 2026: 70%+ teams trunk-based.

5. **Self-hosted runner** khi: (a) need GPU/big RAM cloud doesn't offer cheap. (b) access private corp network. (c) persistent cache for fast Docker builds. (d) cost optimize cho heavy CI usage (>1250 min/mo). Most startups stay cloud.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Generic pipeline (any tool)

```
Trigger (push, PR) → Build → Test → Deploy
                       ↓        ↓        ↓
                     cache    parallel  manual/auto
```

### Tools 2026

```
GitHub Actions   Default for GitHub repos
GitLab CI         Default for GitLab repos
CircleCI          Fast, mature alternative
Jenkins           Self-host mature
Drone, BuildKite   Lightweight self-host
```

### DORA Elite targets

```
Deployment: multiple/day
Lead time:   <1 hour
MTTR:        <1 hour
Failure:     0-15%
```

### Best practices

```
[ ] Trunk-based + feature flags
[ ] Fast feedback (<5 min)
[ ] Cache deps + Docker layers
[ ] Parallel jobs
[ ] Secrets in store, not code
[ ] OIDC over long-lived tokens
[ ] Auto rollback
[ ] DORA metrics dashboard
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **CI** | Continuous Integration — auto build + test on push |
| **CD (Delivery)** | Ready to deploy, manual trigger |
| **CD (Deployment)** | Auto deploy to prod every commit |
| **Pipeline** | Sequence of jobs (build/test/deploy) |
| **Job** | Group of steps on a runner |
| **Step** | Single command/action |
| **Runner** | Machine executing pipeline |
| **Artifact** | Output between jobs |
| **Trigger** | Event start pipeline |
| **DORA metrics** | 4 metrics measure DevOps perf |
| **Trunk-based** | Short-lived branches, merge main frequently |
| **Gitflow** | Multiple long-lived branches (develop/release) |
| **Feature flag** | Toggle features without deploy |
| **OIDC** | OpenID Connect — federated auth (CI → cloud) |
| **SAST / DAST** | Static / Dynamic security testing |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ➡️ **Bài tiếp theo:** [GitHub Actions — Default CI/CD 2026](01_github-actions.md)
- ↑ **Về cụm:** [ci-cd README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [Git basics](../../../../02_tools/git/) — branching foundation
- [Docker](../../../docker/) — CI build images
- [Kubernetes](../../../kubernetes/) — CI deploy K8s

### 🌐 Tài nguyên tham khảo khác
- 📖 [DORA reports](https://dora.dev/) — yearly state of DevOps
- 📖 [Accelerate book](https://nicolefv.com/book) — DORA research
- 📖 [GitHub Actions docs](https://docs.github.com/en/actions)
- 📖 [GitLab CI docs](https://docs.gitlab.com/ee/ci/)
- 📖 [Jenkins docs](https://www.jenkins.io/doc/)
- 📖 [CNCF CI/CD landscape](https://landscape.cncf.io/?group=projects&category=continuous-integration-delivery)

---

> 🎯 *Sau bài này hiểu CI/CD landscape. Bài kế tiếp đi sâu **GitHub Actions** — default 2026.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster ci-cd basic lesson 1/5. Cover: CI vs CD vs CD (Delivery vs Deployment) + history + 8 tool 2026 compare + decision matrix + anatomy pipeline (trigger/jobs/steps/secrets) + first GitHub Actions workflow.
- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Visualization + Evolution + Tools compare + Pick 2026 + §3 Anatomy pipeline.
