# 🎓 Pipeline Patterns — Common patterns + best practices

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [GitHub Actions](01_github-actions.md), [GitLab CI](02_gitlab-ci.md)

> 🎯 *Tool-agnostic patterns: **PR validation**, **monorepo**, **release tagging**, **scheduled jobs**, **manual approval gates**, **secret scanning**, **dependency updates**, **container vulnerability scan**, **flaky test handling**, **fast feedback** optimization. Sau bài này design pipeline production-grade.*

## 🎯 Sau bài này bạn sẽ

- [ ] **PR validation** pipeline pattern
- [ ] **Monorepo** — selective build (Nx, Turborepo, Bazel)
- [ ] **Release pipeline** — semver tag, changelog, GitHub Release
- [ ] **Scheduled jobs** — nightly tests, security scan, cleanup
- [ ] **Approval gates** + manual deployment
- [ ] **Security scanning** — SAST, dep scan, container scan, secret scan
- [ ] **Dependabot / Renovate** auto-update
- [ ] **Flaky test** detection + handling
- [ ] **Fast feedback** — order jobs, fail-fast, partial CI

---

## 1️⃣ PR validation pattern

**Goal**: every PR validated before merge.

```yaml
# GitHub Actions
name: PR Validation

on:
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    steps: [...]

  security:
    runs-on: ubuntu-latest
    steps: [...]
```

### Required checks (block merge)

GitHub Settings → Branches → main → **Require status checks**:
- ✅ lint
- ✅ test
- ✅ security

→ PR cannot merge until all green. Devs see check status on PR page.

### CODEOWNERS — Auto-assign reviewers

File `.github/CODEOWNERS` map path pattern → team — GitHub auto-assign reviewer khi PR touches matching files. Tránh việc PR ngồi chờ random người review:

```
# .github/CODEOWNERS
*                   @ops-team
/backend/            @backend-team
/frontend/           @frontend-team
*.md                 @docs-team
/.github/            @ops-team
/infra/              @ops-team
```

→ PR touches `backend/` → `backend-team` auto-required reviewer.

### Auto-label by path

Auto-label PR theo file path giúp routing + filtering. Setup 2 file: `.github/labeler.yml` (rules) + workflow gọi `actions/labeler@v5`. Useful cho dashboard "frontend PRs pending":

```yaml
# .github/labeler.yml
backend:
- changed-files:
  - any-glob-to-any-file:
    - 'backend/**'
frontend:
- changed-files:
  - any-glob-to-any-file:
    - 'frontend/**'
documentation:
- changed-files:
  - any-glob-to-any-file:
    - '**/*.md'
```

```yaml
# .github/workflows/labeler.yml
name: PR Labeler
on: [pull_request]
jobs:
  label:
    runs-on: ubuntu-latest
    permissions: { contents: read, pull-requests: write }
    steps:
    - uses: actions/labeler@v5
```

→ Auto-label PR for routing + filtering.

---

## 2️⃣ Monorepo — Selective build

**Problem**: monorepo có 20 apps. Push code 1 app → CI build all = slow.

**Solution**: detect changes → build only affected.

### Simple — Path filter

Cách đơn giản nhất cho monorepo — `if: contains(...)` filter từng job theo path. Hạn chế: chỉ check `head_commit` (single commit), không tính cumulative changes trong PR multi-commit:

```yaml
jobs:
  backend:
    if: contains(github.event.head_commit.modified, 'backend/')
    steps: [build backend]

  frontend:
    if: contains(github.event.head_commit.modified, 'frontend/')
    steps: [build frontend]
```

→ Limited — chỉ check head_commit, không full PR diff.

### Pattern with `paths` filter

Pattern `paths` ở event level — skip toàn bộ workflow nếu không match. Glob syntax + negation (`!`) support. Tốt cho workflow dedicated 1 path:

```yaml
on:
  push:
    paths: ['backend/**', '!backend/docs/**']
```

→ Skip workflow nếu paths không match.

### Advanced — Path-filter action

`dorny/paths-filter@v3` cho full PR diff (không chỉ head_commit) + multiple filters cùng lúc + output để conditional jobs. Pattern production cho monorepo 5+ apps:

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.filter.outputs.backend }}
      frontend: ${{ steps.filter.outputs.frontend }}
    steps:
    - uses: actions/checkout@v4
    - uses: dorny/paths-filter@v3
      id: filter
      with:
        filters: |
          backend:
            - 'backend/**'
            - 'shared/**'
          frontend:
            - 'frontend/**'
            - 'shared/**'

  test-backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    steps: [test backend]

  test-frontend:
    needs: changes
    if: needs.changes.outputs.frontend == 'true'
    steps: [test frontend]
```

### Monorepo tools

| Tool | Language | Notes |
|---|---|---|
| **Nx** | JS/TS focused | Smart caching, affected detection |
| **Turborepo** | JS/TS | Faster, Vercel-backed |
| **Bazel** | Polyglot | Google's tool, complex |
| **Pants / Buck2** | Polyglot | Twitter/Meta tools |

```bash
# Nx — only test changed
nx affected --target=test --base=main
```

→ Tools compute dependency graph, run only affected tasks.

---

## 3️⃣ Release pipeline

**Goal**: on tag `v1.2.3` → build, test, package, publish, GitHub Release.

```yaml
name: Release

on:
  push:
    tags:
    - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write          # ← Create release
      packages: write           # ← Push to registry
    steps:
    - uses: actions/checkout@v4

    - name: Get version
      run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_ENV

    - name: Build
      run: |
        docker build -t myapp:${{ env.VERSION }} .
        docker tag myapp:${{ env.VERSION }} myapp:latest

    - name: Push image
      run: |
        docker login -u $REGISTRY_USER -p ${{ secrets.REGISTRY_PASSWORD }}
        docker push myapp:${{ env.VERSION }}
        docker push myapp:latest

    - name: Generate changelog
      uses: orhun/git-cliff-action@v3
      with:
        config: cliff.toml
        args: --latest

    - name: Create GitHub Release
      uses: softprops/action-gh-release@v2
      with:
        tag_name: ${{ env.VERSION }}
        body_path: CHANGELOG.md
        files: dist/*
        draft: false
```

### Semver tagging

```bash
# Conventional Commits → semver bump
feat: add user login          → minor bump (1.0.0 → 1.1.0)
fix: handle null user           → patch bump (1.1.0 → 1.1.1)
feat!: drop Python 3.10         → major bump (1.1.1 → 2.0.0)

# Tools auto-tag
semantic-release / standard-version / cocogitto
```

→ Push commits → tool analyze → tag + push → trigger release pipeline.

### Auto changelog — Conventional Commits

```bash
# Install
brew install git-cliff

# Generate
git cliff -o CHANGELOG.md
```

→ Group commits by type: 🚀 features, 🐛 fixes, 📚 docs, ⚙️ chores.

---

## 4️⃣ Scheduled jobs — Nightly tasks

### Nightly E2E tests

```yaml
on:
  schedule:
  - cron: '0 2 * * *'        # 2 AM UTC daily

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
    - run: ./run-e2e.sh
    - if: failure()
      uses: 8398a7/action-slack@v3
      with:
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        text: "🚨 Nightly E2E failed"
```

### Security scan

```yaml
on:
  schedule:
  - cron: '0 0 * * 0'        # Weekly Sunday

jobs:
  scan:
    steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'ghcr.io/acmeshop/fastapi:latest'
        severity: 'CRITICAL,HIGH'
```

### Cleanup old artifacts

```yaml
on:
  schedule:
  - cron: '0 3 * * *'

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/delete-package-versions@v5
      with:
        package-name: 'myapp'
        min-versions-to-keep: 30
```

→ Save storage cost (registry).

---

## 5️⃣ Approval gates — Manual deploy

### GitHub Environments

```yaml
jobs:
  deploy-prod:
    environment:
      name: production
      url: https://acmeshop.vn
    steps:
    - run: ./deploy.sh
```

→ GitHub Settings → Environments → production → Required reviewers: [`@alice`, `@bob`].

Workflow: pipeline pause at this job → reviewer click "Approve and deploy" → continue.

### Plus wait timer

```
Environment "production":
- Required reviewers: [ops-team]
- Wait timer: 5 minutes
```

→ 5min cooldown sau approve. Last chance abort.

### GitLab manual job

```yaml
deploy-prod:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
      allow_failure: false
  environment:
    name: production
```

→ Click "Play" trong GitLab UI.

### Multi-stage approval pattern

```
push main
   ↓
auto deploy staging
   ↓
canary 5% production    ← approve 1
   ↓
roll out 100%           ← approve 2
```

---

## 6️⃣ Security scanning

### 5 layers

| Layer | Tool examples |
|---|---|
| **SAST** (source code) | CodeQL, Semgrep, SonarQube |
| **Dependency scan** | Dependabot, Snyk, Renovate, Trivy |
| **Container scan** | Trivy, Grype, Clair, Snyk |
| **Secrets scan** | gitleaks, trufflehog, GitHub Secret Scanning |
| **DAST** (runtime) | OWASP ZAP, Burp Suite |

### Example: All-in-one workflow

```yaml
jobs:
  sast:
    runs-on: ubuntu-latest
    permissions: { security-events: write }
    steps:
    - uses: actions/checkout@v4
    - uses: github/codeql-action/init@v3
      with: { languages: python }
    - uses: github/codeql-action/analyze@v3

  dep-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: snyk/actions/python@master
      env: { SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }} }

  secret-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with: { fetch-depth: 0 }
    - uses: gitleaks/gitleaks-action@v2
      env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }

  container-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'myapp:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'
    - uses: github/codeql-action/upload-sarif@v3
      with: { sarif_file: 'trivy-results.sarif' }
```

→ Results show trong GitHub **Security tab**.

### Block PR if critical CVE

```yaml
- uses: aquasecurity/trivy-action@master
  with:
    severity: 'CRITICAL'
    exit-code: '1'        # Fail pipeline
```

---

## 7️⃣ Dependabot / Renovate — Auto-update

### Dependabot (GitHub built-in)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule: { interval: "weekly" }
    open-pull-requests-limit: 10

  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule: { interval: "weekly" }
    groups:
      react:
        patterns: ["react*"]

  - package-ecosystem: "docker"
    directory: "/"
    schedule: { interval: "monthly" }

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule: { interval: "weekly" }
```

→ Dependabot tự PR weekly cập nhật deps. PR pass CI → merge.

### Renovate (more powerful)

```json
// renovate.json
{
  "extends": ["config:recommended"],
  "schedule": ["before 9am on Monday"],
  "packageRules": [
    { "matchManagers": ["npm"], "groupName": "npm minor", "matchUpdateTypes": ["minor", "patch"] },
    { "matchPackagePatterns": ["^@types/"], "automerge": true }
  ]
}
```

→ Renovate cộng đồng, support 70+ package managers, smarter than Dependabot.

---

## 8️⃣ Flaky test handling

**Flaky test** = same code, sometimes pass sometimes fail. Bad signal!

### Detect

```yaml
- name: Run tests with retry
  run: pytest --reruns 2 --reruns-delay 1
```

→ Test fail → retry 2x. Track which tests need retry → mark as flaky.

### Quarantine

```python
# pytest.ini
[pytest]
markers =
  flaky: marks tests as flaky

# Test file
@pytest.mark.flaky
def test_unstable():
    ...
```

```yaml
# Run non-flaky first
- run: pytest -m "not flaky"
- run: pytest -m flaky --reruns 3
  continue-on-error: true        # Don't fail pipeline
```

### Root causes

- ❌ Timing (race condition, sleep) — fix with proper wait.
- ❌ Shared state — isolate, fixture per test.
- ❌ External service — mock.
- ❌ Random order — use deterministic seed.

→ **Long-term**: fix flaky tests, không retry hide. CI signal phải reliable.

---

## 9️⃣ Fast feedback — Optimize CI time

### Cardinal rule: **fail fast, fail clear**

```
✅ Lint (5s)          fail first if bad
✅ Type check (10s)
✅ Unit test (1 min)
✅ Integration (3 min)
✅ E2E (10 min)        slowest, only if all above pass
```

### Parallel where possible

```yaml
jobs:
  lint:        runs-on: ubuntu-latest
  type-check:   runs-on: ubuntu-latest
  unit-test:    runs-on: ubuntu-latest
  # All 3 run parallel
```

### Matrix sharding

```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
    - run: pytest --shard ${{ matrix.shard }}/4
```

→ 4 jobs parallel test 1/4 each. 10min test → 2.5min wall clock.

### Cache aggressively

| Cache | Saves |
|---|---|
| **npm/pip/cargo cache** | 30-60s per build |
| **Docker layers** | 1-5min |
| **Pre-built images** for CI deps | 30s |
| **Test result cache** (jest, pytest) | rerun changes only |

### Self-host for hot path

If CI is bottleneck (>1500 min/mo), self-host runner saves money + supports caching better.

---

## 1️⃣0️⃣ Real-world: Full PR pipeline của bạn

```yaml
name: PR Pipeline

on:
  pull_request:
    types: [opened, synchronize, ready_for_review]
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE: ${{ github.repository }}

jobs:
  # Phase 1: Quick checks (fail fast)
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: { python-version: "3.12", cache: 'pip' }
    - run: pip install ruff black mypy
    - run: ruff check .
    - run: black --check .

  type-check:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: { python-version: "3.12", cache: 'pip' }
    - run: pip install mypy
    - run: mypy app/

  # Phase 2: Tests (parallel)
  unit-test:
    needs: [lint]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
    - uses: actions/checkout@v4
    - run: pytest --shard ${{ matrix.shard }}/4

  integration-test:
    needs: [lint]
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:18
        env: { POSTGRES_PASSWORD: test }
        ports: ['5432:5432']
    steps:
    - run: pytest tests/integration/

  # Phase 3: Security
  security:
    needs: [lint]
    runs-on: ubuntu-latest
    steps:
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        severity: 'CRITICAL,HIGH'

  # Phase 4: Build (only after all pass)
  build-image:
    if: github.event_name == 'push'
    needs: [unit-test, integration-test, security, type-check]
    runs-on: ubuntu-latest
    permissions: { contents: read, packages: write }
    steps:
    - uses: actions/checkout@v4
    - uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - uses: docker/build-push-action@v5
      with:
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE }}:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # Phase 5: Deploy staging (auto), prod (manual)
  deploy-staging:
    needs: [build-image]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: { name: staging, url: https://staging.acmeshop.vn }
    permissions: { id-token: write }
    steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_STAGING_ROLE }}
        aws-region: us-east-1
    - run: ./deploy.sh staging ${{ github.sha }}

  deploy-prod:
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    environment: { name: production, url: https://acmeshop.vn }
    permissions: { id-token: write }
    steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_PROD_ROLE }}
        aws-region: us-east-1
    - run: ./deploy.sh production ${{ github.sha }}
```

→ Total time: ~5-10min PR validation, full deploy ~15min. Production-grade patterns.

---

## ⚠️ 5 pitfall hay vướng

1. **CI 30+ min** → devs skip CI, push and pray. Optimize: parallel + cache + matrix shard.
2. **No required checks** → bad code merge to main. Always require lint + test.
3. **All sequential** → 30 min when could be 5. Run independent jobs in parallel.
4. **Flaky tests ignored** → trust degrades. Quarantine + fix root cause.
5. **No security scanning** → CVE deploy production. Add Trivy + Dependabot from day 1.

---

## ✅ Self-check

1. Cách make **PR validation** mandatory before merge?
2. Monorepo — cách build only affected?
3. **5 security scanning layers** + tool ví dụ?
4. **Flaky test** — fix tạm thời và root cause?
5. CI 25 min → cách optimize xuống <10 min?

<details>
<summary>Gợi ý đáp án</summary>

1. **GitHub**: Settings → Branches → main → Protect → **Require status checks**. Add specific check names (lint, test). Plus CODEOWNERS for auto-reviewer. Plus require approval count.

2. (a) Simple: **`paths`** filter in `on:`. (b) Better: **path-filter action** (dorny/paths-filter) → outputs → conditional jobs. (c) Best: **monorepo tools** (Nx, Turborepo, Bazel) compute dep graph → run affected only. Example: `nx affected --target=test --base=main`.

3. (a) **SAST** — CodeQL, Semgrep. (b) **Dependency scan** — Snyk, Dependabot. (c) **Container scan** — Trivy, Grype. (d) **Secret scan** — gitleaks, GitHub Secret Scanning. (e) **DAST** — OWASP ZAP, Burp.

4. **Tạm thời**: `--reruns 2` (pytest), quarantine in separate job (`continue-on-error: true`). **Root cause**: timing (proper waits, no sleep), shared state (test isolation), external (mock), random order (deterministic seed). Long-term fix > retry hide.

5. (a) **Parallel jobs** (lint + test + security same time). (b) **Matrix shard** (split tests 4 ways). (c) **Cache aggressive** (npm, pip, Docker layers). (d) **Fail fast** (lint first). (e) **Self-host runner** for hot path. Combo: 25min → 5min realistic.
</details>

---

## ⚡ Cheatsheet

### Pattern checklist

```
[ ] Required status checks
[ ] CODEOWNERS auto-reviewer
[ ] Path-based selective build
[ ] Parallel jobs (lint + test + security)
[ ] Matrix shard tests
[ ] Cache (deps + Docker)
[ ] Required environments protection prod
[ ] Auto-tag semver
[ ] Dependabot/Renovate weekly
[ ] Security scan (SAST + dep + container + secret)
[ ] Slack on failure
```

### Security tools

```
SAST       CodeQL, Semgrep, SonarQube
Deps       Dependabot, Snyk, Renovate
Container  Trivy, Grype
Secrets    gitleaks, trufflehog
DAST       OWASP ZAP
```

### Monorepo tools

```
Nx          JS/TS — smart caching
Turborepo   JS/TS — fast, Vercel
Bazel       Polyglot — Google
Pants       Polyglot — Twitter
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **PR validation** | Pipeline run on every pull request |
| **Required check** | Block merge if pipeline fail |
| **CODEOWNERS** | File auto-assign reviewers by path |
| **Monorepo** | Multiple projects in 1 repo |
| **Selective build** | Build only affected by changes |
| **Semver** | Semantic Versioning (major.minor.patch) |
| **Conventional Commits** | Format commits to auto-bump version |
| **Approval gate** | Manual deploy permission |
| **SAST / DAST** | Static / Dynamic security testing |
| **Dependabot / Renovate** | Auto-update deps |
| **Flaky test** | Same code, inconsistent pass/fail |
| **Matrix shard** | Split tests across parallel jobs |
| **Fail fast** | Cancel pipeline on first failure |

---

## 🔗 Links

### Trong cluster
- ← Trước: [GitLab CI](02_gitlab-ci.md)
- → Tiếp: [Deploy Strategies](04_deploy-strategies.md)
- ↑ Cluster: [ci-cd README](../../README.md)

### External
- 📖 [GitHub Actions security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- 📖 [Renovate docs](https://docs.renovatebot.com/)
- 📖 [Nx docs](https://nx.dev/)
- 📖 [Trivy docs](https://aquasecurity.github.io/trivy/)
- 📖 [Conventional Commits](https://www.conventionalcommits.org/)
- 📖 [Semantic Release](https://github.com/semantic-release/semantic-release)

---

> 🎯 *Sau bài này design CI/CD patterns production. Bài cuối dạy **deploy strategies** — blue-green, canary, rolling.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước CODEOWNERS + Auto-label + Monorepo Simple path + Pattern paths + Path-filter action.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster ci-cd basic lesson 4/5. Cover: branch protection + CODEOWNERS + monorepo path filter (3 cấp) + matrix build + reusable workflow + caching (deps + Docker layer) + secrets + OIDC + custom action.
