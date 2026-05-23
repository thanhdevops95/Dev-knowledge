# Git Workflows & Branching Strategies

> **Tags:** `git` `gitflow` `trunk-based` `monorepo` `conventional-commits` `semver`
> **Level:** Intermediate | **Prerequisite:** `git/01-git-basics.md`

---

## 1. GitFlow

GitFlow là branching strategy phù hợp với **scheduled releases** (apps có version cụ thể như mobile apps, desktop apps).

### Branch structure
```
main          ← Production code. ONLY release/hotfix merges here.
develop       ← Integration branch. Feature branches merge here.
feature/*     ← Individual features
release/*     ← Prepare for release (freeze feature, only bug fixes)
hotfix/*      ← Emergency fixes to production
```

### Lifecycle
```
main ────────────────────────────────────────────── v1.0 ── v1.1

develop ──────────────────────────────────── merge ──▶ release/1.1
                                              ↑
feature/login ───────────────────────── merge ↓
feature/payment ───────────────── merge ─────↓

hotfix/critical ─── (from main) ─── merge ──▶ main (v1.0.1)
                       └───────────────────▶ develop
```

### Commands (git-flow tool)
```bash
# Install
brew install git-flow-avh

# Initialize (interactive setup)
git flow init

# Feature
git flow feature start login
git flow feature finish login       # Merges into develop, deletes branch

# Release
git flow release start 1.1.0
git flow release finish 1.1.0       # Merges into main + develop, creates tag

# Hotfix
git flow hotfix start critical-bug
git flow hotfix finish critical-bug  # Merges into main + develop
```

### Khi nào dùng GitFlow?
✅ App có phiên bản (v1.0, v2.0)
✅ Multiple versions maintained cùng lúc
✅ Scheduled release cycle (weekly, bi-weekly)
❌ Web apps deploy nhiều lần/ngày → quá phức tạp

---

## 2. GitHub Flow (Simple & Popular)

Đơn giản nhất — phù hợp với **continuous deployment**:

```
main ──────────────────────────────────────────── always deployable
       ↑                                         
feature/login ───────── PR ────────── merge ──▶ main → deploy
feature/payment ─────── PR ────────── merge ──▶ main → deploy
```

### Rules
1. `main` luôn deployable
2. Tạo feature branch từ `main`
3. Commit thường xuyên
4. Mở Pull Request sớm (draft PR để discuss)
5. Merge sau khi review + CI passes
6. Deploy ngay sau khi merge

```bash
git checkout -b feature/add-oauth
# ... work ...
git push origin feature/add-oauth
# Open PR on GitHub
# CI runs automatically
# Reviewer approves
git checkout main; git pull
# Feature merged, deploy runs automatically
```

---

## 3. Trunk-Based Development (TBD)

Mạnh nhất cho **high-frequency deployment** (Google, Meta, Netflix):

```
main (trunk) ──────────────────────────────────────
    ↑         ↑         ↑         ↑
  dev1      dev2      dev3      dev4
  (commit   (commit   (commit   (commit
  directly  directly  directly  directly
  or short  or short  or short  or short
  lived PR) lived PR) lived PR) lived PR)
```

### Key principles
- **Everyone commits to trunk daily** (hoặc max 2-3 ngày)
- **Feature flags** để hide incomplete features khi merge
- **Short-lived branches** nếu không commit trực tiếp (max 2 ngày)
- **CI must be fast** (< 10 minutes) và pass trước khi merge

```bash
# TBD với feature flags
git checkout main
git pull
# ... make small change ...
git add -A
git commit -m "feat: add oauth button behind flag OAUTH_FLAG"
git push origin main  # Push directly to trunk
# CI runs → deploy to staging → if OK → deploy to prod
```

### Feature flags
```python
# LaunchDarkly / Unleash style
import unleash_client

def show_oauth_button(user):
    # Feature only visible when flag enabled
    return unleash_client.is_enabled("oauth-login", {"userId": user.id})
```

---

## 4. Monorepo vs Polyrepo

### Monorepo — Tất cả trong 1 repo

```
/repo
├── services/
│   ├── user-service/
│   ├── payment-service/
│   └── notification-service/
├── packages/
│   ├── ui-components/    ← shared
│   └── api-client/       ← shared
├── apps/
│   ├── web/
│   └── mobile/
└── tools/
    └── scripts/
```

**Ưu điểm:**
- Atomic changes (1 PR thay đổi service + shared lib)
- Code reuse dễ
- Consistent tooling/CI
- Easy to refactor cross-service

**Nhược điểm:**
- Git repo lớn → clone/checkout chậm
- CI cần hiểu dependency graph để chỉ test services bị ảnh hưởng
- Cần tooling (Nx, Turborepo)

### Polyrepo — Mỗi service 1 repo

**Ưu điểm:** Autonomy, team độc lập, CI đơn giản
**Nhược điểm:** Dependency management phức tạp, boilerplate lặp lại, atomic changes khó

### Tooling cho Monorepo

```bash
# Nx (Node/TS ecosystem)
npx create-nx-workspace@latest
nx affected --target=test    # Chỉ test apps/libs bị ảnh hưởng bởi changes
nx graph                     # Visualize dependency graph

# Turborepo
turbo run build --filter=./apps/web    # Build chỉ web app và dependencies
turbo run test --cache-dir=.turbo      # Remote caching
```

---

## 5. Conventional Commits

Standard format cho commit messages — cho phép **auto-generate changelogs** và semantic versioning:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
| Type | Khi nào dùng | SemVer |
|---|---|---|
| `feat` | Tính năng mới | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Chỉ documentation | - |
| `style` | Formatting, không thay đổi logic | - |
| `refactor` | Refactor không fix bug/add feature | - |
| `perf` | Performance improvement | - |
| `test` | Thêm/sửa tests | - |
| `build` | Build system changes | - |
| `ci` | CI config changes | - |
| `chore` | Maintenance | - |
| `revert` | Revert commit | - |

```
feat(auth): add Google OAuth login

Implements OAuth 2.0 Authorization Code flow with PKCE.
Supports Google as provider with extensible interface for future providers.

Closes #234
Co-authored-by: Alice <alice@example.com>

BREAKING CHANGE: `/api/auth/login` endpoint now requires `provider` field.
```

### Ví dụ thực tế
```bash
git commit -m "feat: add user avatar upload"
git commit -m "fix(api): handle null response from payment gateway"
git commit -m "docs: update README with Docker setup"
git commit -m "refactor(db): extract query builder to separate module"
git commit -m "feat!: remove deprecated v1 API endpoints"
# feat! hoặc BREAKING CHANGE footer → MAJOR version bump
```

---

## 6. Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH[-prerelease][+build]

1.2.3
│ │ └── PATCH: backward-compatible bug fixes
│ └──── MINOR: new backward-compatible functionality  
└────── MAJOR: incompatible API changes

1.0.0-alpha.1   ← Pre-release
1.0.0-beta.2
1.0.0-rc.1
1.0.0           ← Stable release
1.0.0+20240101  ← Build metadata (không ảnh hưởng versioning)
```

### Range specifiers (npm)
```json
{
  "dependencies": {
    "express": "^4.18.0",   // >=4.18.0 <5.0.0 (caret)
    "lodash": "~4.17.0",    // >=4.17.0 <4.18.0 (tilde — patch only)
    "react": "18.2.0",      // Exact version
    "next": ">=13.0.0",     // Any version >=13
    "vue": "*"              // Any version (nguy hiểm!)
  }
}
```

### Auto-versioning với Conventional Commits
```bash
# semantic-release
npm install -D semantic-release @semantic-release/git @semantic-release/changelog

# .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",   // Đọc conventional commits
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",          // Update CHANGELOG.md
    "@semantic-release/npm",               // Update package.json version
    "@semantic-release/git",               // Commit CHANGELOG + version
    "@semantic-release/github"             // Create GitHub release
  ]
}

# Chạy trong CI:
npx semantic-release
```

---

## 7. Pull Request Best Practices

### PR description template
```markdown
## What

Brief description of what this PR does.

## Why

Why is this change needed? Link to issue/ticket.
Closes #123

## How

How did you implement it? Key decisions made.

## Screenshots (if UI change)

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Tested locally

## Checklist

- [ ] Self-reviewed code
- [ ] Documentation updated
- [ ] No debug logs committed
```

### PR size guidelines
- **< 200 lines**: ✅ Easy to review
- **200-400 lines**: ⚠️ Acceptable, hard to review thoroughly
- **> 400 lines**: ❌ Break it up!

**Kỹ thuật chia nhỏ PR:**
- Separate refactoring from feature (2 PRs)
- Split by layer: DB schema → backend API → frontend UI
- Use feature flags để merge incomplete code

---

## 8. Branch Naming Conventions

```bash
# Format phổ biến
feature/TICKET-123-description
fix/TICKET-456-null-pointer
hotfix/critical-payment-bug
docs/update-api-docs
refactor/extract-auth-service
release/v2.1.0

# Examples
feature/AUTH-234-google-oauth
fix/SHOP-789-cart-calculation
hotfix/prod-memory-leak
```

---

## 9. CODEOWNERS

```
# .github/CODEOWNERS
# Format: path @user-or-team

*                        @team-lead          # Default: everyone
/backend/                @backend-team
/frontend/               @frontend-team
/infra/                  @devops-team
/docs/                   @tech-writers
*.sql                    @database-team

# Require specific reviewers for sensitive files
/src/auth/               @security-team @senior-backend
/.github/workflows/      @devops-team
```

---

## 10. Summary Bảng So Sánh

| | GitFlow | GitHub Flow | Trunk-Based |
|---|---|---|---|
| **Phù hợp với** | Versioned releases | Continuous deployment | High-frequency deploy |
| **Complexity** | Cao | Thấp | Trung bình |
| **Feature flags** | Không cần | Không cần | **Bắt buộc** |
| **Deploy frequency** | Thấp (weekly/monthly) | Vừa (daily/weekly) | Cao (nhiều lần/ngày) |
| **Examples** | Mobile apps | Most SaaS | Google, Meta |
| **CI requirement** | Thấp | Vừa | **Rất nghiêm ngặt** |

---

*Tài liệu liên quan: `git/02-git-advanced.md` | `git/04-github-gitlab.md` | `cicd/01-github-actions.md`*
