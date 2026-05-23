# 🐙 GitHub & GitLab — Nền tảng quản lý mã nguồn

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]`
> Prerequisite: `01-git-basics.md`

---

## Tại sao cần GitHub / GitLab?

Git là **công cụ command-line** quản lý version control trên máy local. Nhưng khi làm việc **nhóm**, bạn cần:
- **Remote repository** — nơi lưu trữ code trung tâm, ai cũng truy cập được
- **Code review** — đánh giá code trước khi merge
- **Issue tracking** — quản lý bugs và tasks
- **CI/CD** — tự động test và deploy
- **Collaboration** — fork, pull request, wiki

**GitHub** và **GitLab** là 2 nền tảng phổ biến nhất giải quyết tất cả nhu cầu trên.

| Tiêu chí | GitHub | GitLab |
|---|---|---|
| **Market share** | #1 (100M+ users) | #2 (30M+ users) |
| **CI/CD** | GitHub Actions | GitLab CI/CD (tích hợp sẵn) |
| **Free tier** | Unlimited public repos, 2000 Actions mins/month | Unlimited repos, 400 CI/CD mins/month |
| **Self-hosted** | GitHub Enterprise ($$) | GitLab CE (free, open-source) |
| **Best for** | Open source, community | Enterprise, DevOps pipeline |

---

## 1. Pull Requests (GitHub) / Merge Requests (GitLab)

### Tại sao cần Pull Request (PR)?

PR là **trung tâm của collaboration**: thay vì push thẳng vào main, bạn **đề xuất** thay đổi → team **review** → approved → **merge**.

```
Feature Branch Workflow:

1. git checkout -b feature/add-login
2. Viết code, commit
3. git push origin feature/add-login
4. Tạo Pull Request trên GitHub
5. Team review → request changes / approve
6. Merge → delete branch
```

### Tạo PR tốt

```markdown
## PR Title: [FE-123] Add login page with OAuth support

### What does this PR do?
- Add login page UI with email/password form
- Integrate Google OAuth 2.0 flow
- Add session management with JWT

### How to test?
1. `npm run dev`
2. Navigate to /login
3. Click "Login with Google"
4. Verify redirect to dashboard

### Screenshots
[Screenshot login page]

### Checklist
- [x] Unit tests added
- [x] E2E test for login flow
- [ ] Documentation updated
- [x] No breaking changes
```

### Code Review Best Practices

```
Reviewer:
  ✅ Đọc code, hiểu context trước khi comment
  ✅ Give actionable feedback: "Consider using X because Y"
  ✅ Approve khi "good enough", không cần "perfect"
  ❌ Đừng comment style nit-picks (dùng linter tự động)
  ❌ Đừng block PR vì personal preference

Author:
  ✅ Keep PR small (< 400 lines)
  ✅ Mô tả rõ context trong PR description
  ✅ Self-review trước khi request review
  ❌ Đừng force push sau khi có review comments
```

---

## 2. Issues & Project Management

### GitHub Issues

```markdown
## Bug Report

**Describe the bug:**
Login page crashes when email contains "+" character.

**To reproduce:**
1. Go to /login
2. Enter email: test+user@gmail.com
3. Click "Login"
4. See error in console

**Expected behavior:**
Login should work with "+" in email (valid RFC 5321).

**Environment:**
- OS: macOS 14.2
- Browser: Chrome 121
- Version: v2.1.0

**Labels:** bug, priority-high, frontend
```

### GitHub Projects (Kanban/Table View)

```
GitHub Projects (V2):
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Backlog  │  │   Todo   │  │   In     │  │  Done    │
│          │  │          │  │ Progress │  │          │
│ #45 Auth │  │ #50 API  │  │ #48 UI   │  │ #42 DB   │
│ #46 Perf │  │ #51 Test │  │ #49 Docs │  │ #43 CI   │
│ #47 Docs │  │          │  │          │  │ #44 Bug  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘

Features:
- Custom fields (priority, sprint, estimate)
- Automations (issue closed → move to Done)
- Multiple views (Board, Table, Roadmap)
```

---

## 3. GitHub Actions — CI/CD cơ bản

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build

  deploy:
    needs: test    # Chỉ deploy khi test pass
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      # Deploy steps...
```

### GitHub Actions Key Concepts

| Concept | Mô tả |
|---|---|
| **Workflow** | File YAML định nghĩa CI/CD pipeline |
| **Trigger (on)** | Sự kiện kích hoạt: push, PR, schedule, manual |
| **Job** | Tập hợp steps chạy trên 1 runner |
| **Step** | 1 action hoặc 1 command |
| **Action** | Reusable unit (checkout, setup-node, cache) |
| **Secret** | Variables ẩn (API keys, tokens) |
| **Matrix** | Chạy job trên nhiều config (Node 18/20/22) |

---

## 4. Protected Branches & CODEOWNERS

### Protected Branches

```
Settings → Branches → Branch protection rules:

Branch: main
  ✅ Require pull request before merging
     ✅ Require approvals (1-2 reviewers)
     ✅ Dismiss stale reviews when new commits pushed
  ✅ Require status checks to pass
     ✅ CI Pipeline (test job)
  ✅ Require linear history (no merge commits)
  ❌ Allow force pushes (NEVER on main!)
```

### CODEOWNERS

```bash
# .github/CODEOWNERS
# Khi file trong path này thay đổi → auto request review

# Frontend team owns all frontend code
/src/components/  @company/frontend-team
/src/pages/       @company/frontend-team

# Backend team owns API
/src/api/         @company/backend-team
/src/services/    @company/backend-team

# DevOps owns infrastructure
Dockerfile        @company/devops-team
.github/          @company/devops-team

# Tech lead reviews all architectural changes
/src/lib/         @tech-lead-username
```

---

## 5. GitHub Pages — Hosting static sites

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci && npm run build
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'
      - id: deployment
        uses: actions/deploy-pages@v4
```

URL: `https://<username>.github.io/<repo-name>/`

---

## 6. Forking Workflow — Open Source

```
Open Source Contribution:

1. FORK: github.com/original/repo → github.com/you/repo

2. Clone YOUR fork:
   git clone https://github.com/you/repo.git
   cd repo
   git remote add upstream https://github.com/original/repo.git

3. Sync with upstream:
   git fetch upstream
   git merge upstream/main

4. Create feature branch:
   git checkout -b fix/typo-readme

5. Make changes → commit → push TO YOUR FORK:
   git push origin fix/typo-readme

6. Create PR from your fork → original repo
   github.com/you/repo → "Compare & pull request"
```

---

## 7. GitLab Specifics

### GitLab CI/CD (.gitlab-ci.yml)

```yaml
# .gitlab-ci.yml — tương đương GitHub Actions
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm test
  cache:
    paths:
      - node_modules/

build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  only:
    - main
  script:
    - echo "Deploying..."
```

### GitLab vs GitHub — So sánh CI/CD

| | GitHub Actions | GitLab CI/CD |
|---|---|---|
| **Config file** | `.github/workflows/*.yml` | `.gitlab-ci.yml` |
| **Runner** | GitHub-hosted / self-hosted | GitLab-hosted / self-hosted |
| **Free mins** | 2000/month | 400/month |
| **Artifacts** | `actions/upload-artifact` | Built-in `artifacts:` |
| **Docker registry** | ghcr.io | Built-in Container Registry |
| **Environments** | `environment:` in workflow | `environment:` in job |

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Push credentials vào repo | Dùng GitHub Secrets + `.gitignore` | Credentials trong git history KHÔNG xóa được |
| 2 | PR quá lớn (2000+ lines) | Tách thành nhiều PR nhỏ (< 400 lines) | PR lớn → review kém → bugs lọt qua |
| 3 | Force push to main | KHÔNG BAO GIỜ force push to shared branches | Phá history của team member |
| 4 | Merge commit mess | Dùng squash merge hoặc rebase | Linear history dễ đọc hơn |
| 5 | Ignore CI failures | CI phải green trước khi merge | "Just this once" → technical debt |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Tạo repo GitHub, add CODEOWNERS + branch protection cho main
- [ ] **Bài 2 (Trung bình):** Setup GitHub Actions CI: lint → test → build cho Node/Python project
- [ ] **Bài 3 (Trung bình):** Fork 1 open source project, sửa typo trong docs, tạo PR
- [ ] **Bài 4 (Khó):** Deploy static site lên GitHub Pages tự động bằng Actions

---

## Tài nguyên thêm

- [GitHub Docs](https://docs.github.com/) — Official documentation
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) — Reusable actions
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/) — GitLab CI reference
- [First Contributions](https://github.com/firstcontributions/first-contributions) — Hướng dẫn contribute đầu tiên
