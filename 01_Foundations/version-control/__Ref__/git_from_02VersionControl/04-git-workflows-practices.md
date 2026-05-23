# 🌿 Git Workflows & Branching Strategies

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Cách team collaborate hiệu quả trên Git
> **Prerequisite:** `git/01-git-basics.md`

---

## Tại sao cần Git Workflow?

Khi 1 mình code, `git add . && git commit && git push` là đủ. Nhưng khi **nhiều người cùng code**:

- Dev A push code lỗi lên `main` → production crash
- Dev B merge code chưa review → security bug lọt vào
- Dev C không biết feature nào đang develop, merge conflict liên tục

Git workflow là **quy tắc** cả team đồng ý: nhánh nào cho gì, merge kiểu nào, review ra sao. Không có workflow "đúng nhất" — có workflow **phù hợp nhất** cho team bạn.

---

## 1. Git Flow — Cấu trúc chặt chẽ nhất

Phù hợp: Sản phẩm release theo version (mobile apps, libraries, enterprise), scheduled releases.

```
main ──────●──────────────────●──────────── (production releases)
            \                / 
develop ─────●──●──●──●──●──●──●──●─────── (integration branch)
              \   /  \       /
               ●─●    ●──●──●
             feature  feature/payment
                          \
                           ●── hotfix (fix production bug)
                          /
main ────────────────────●──────────────────
```

```
Nhánh:
  main:       Chỉ chứa code đã release. Tag version: v1.0, v1.1
  develop:    Branch tích hợp. Merge features vào đây.
  feature/*:  1 branch per feature, tạo từ develop
  release/*:  Chuẩn bị release (QA, bug fixes), merge vào main + develop
  hotfix/*:   Fix bug production khẩn cấp, merge vào main + develop
```

### Commands (git-flow tool)

```bash
# Install
brew install git-flow-avh

# Initialize
git flow init

# Feature workflow
git flow feature start login
# ... code, commit ...
git flow feature finish login       # Merges into develop, deletes branch

# Release workflow
git flow release start 1.1.0
# ... QA, bug fixes only ...
git flow release finish 1.1.0       # Merges into main + develop, creates tag

# Hotfix (emergency)
git flow hotfix start critical-bug
git flow hotfix finish critical-bug  # Merges into main + develop
```

**Khi nào dùng Git Flow?**
- ✅ App có phiên bản (v1.0, v2.0) — mobile apps, libraries
- ✅ Multiple versions maintained cùng lúc
- ✅ Scheduled release cycle (weekly, bi-weekly)
- ❌ Web apps deploy nhiều lần/ngày → quá phức tạp

---

## 2. GitHub Flow — Đơn giản & phổ biến nhất

Phù hợp: Team nhỏ (2-10 người), deploy liên tục (CD), SaaS products.

```
main ─────●─────●─────●─────●─────●────── (always deployable!)
           \         /         \       /
            ●──●──●──          ●──●──● 
            feature/login       fix/navbar

Luồng:
  1. Tạo branch từ main: feature/user-profile
  2. Code + commit thường xuyên
  3. Push + mở Pull Request (PR) sớm (draft PR để discuss)
  4. Code review (đồng nghiệp review)
  5. CI/CD chạy tests tự động
  6. Merge vào main → auto deploy production
```

```bash
git checkout main
git pull origin main
git checkout -b feature/user-profile

# ... code, commit ...
git add .
git commit -m "feat: add user profile page"
git push -u origin feature/user-profile

# → Mở PR trên GitHub → Review → CI passes → Merge → Auto deploy
```

**Ưu điểm:** Đơn giản, nhanh, phù hợp continuous deployment.
**Nhược điểm:** Không có staging/release branch → khó nếu cần QA trước deploy.

---

## 3. Trunk-Based Development — Nhanh nhất

Phù hợp: Team có CI/CD mạnh, Google/Facebook/Netflix style, feature flags.

```
main (trunk) ──●──●──●──●──●──●──●──●──●──●─── (deploy liên tục!)
                \  /     |      \ /      |
                 ●      commit    ●     commit
              short-lived  trực tiếp  short-lived  trực tiếp
              (< 1-2 ngày)           (< 1-2 ngày)
```

**Nguyên tắc:**
- Commit **trực tiếp lên main** hoặc branches **sống < 1-2 ngày**
- **Feature flags** để ẩn code chưa hoàn thành
- CI/CD mạnh: mọi commit được test tự động, CI must pass < 10 phút
- Deploy nhiều lần/ngày

### Feature Flags — Ẩn code chưa hoàn thành

```typescript
// Code đã merge nhưng ẨN trong production
if (featureFlags.isEnabled('new-checkout-flow', user)) {
    return <NewCheckout />;  // Chỉ team QA thấy
} else {
    return <OldCheckout />;  // Users thấy phiên bản cũ
}
// Khi ready → bật flag → tất cả users thấy → xóa old code
```

```python
# LaunchDarkly / Unleash style
import unleash_client

def show_oauth_button(user):
    return unleash_client.is_enabled("oauth-login", {"userId": user.id})
```

**Ưu điểm:** Ít merge conflicts, feedback nhanh, deploy nhanh.
**Nhược điểm:** Cần CI/CD mạnh, feature flags management, code discipline.

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

| | Monorepo | Polyrepo |
|---|---|---|
| **Ưu điểm** | Atomic changes, code reuse dễ, consistent tooling | Team autonomy, CI đơn giản, repo nhỏ gọn |
| **Nhược điểm** | Repo lớn, cần tooling (Nx, Turborepo) | Dependency management phức tạp, atomic changes khó |
| **Best for** | 1 team / tightly-coupled services | Multiple teams / loosely-coupled services |

```bash
# Nx: chỉ test apps bị ảnh hưởng bởi changes
nx affected --target=test
nx graph                     # Visualize dependency graph

# Turborepo: build + remote caching
turbo run build --filter=./apps/web
```

---

## 5. Conventional Commits & Semantic Versioning

### Conventional Commits

Standard format cho commit messages → **auto-generate changelogs** + **auto version bumps**:

```
<type>[optional scope]: <description>
```

| Type | Khi nào dùng | SemVer bump |
|---|---|---|
| `feat` | Tính năng mới | MINOR (1.x.0) |
| `fix` | Bug fix | PATCH (1.0.x) |
| `feat!` hoặc `BREAKING CHANGE:` | Breaking API change | MAJOR (x.0.0) |
| `docs` | Chỉ documentation | — |
| `refactor` | Refactor không fix bug/add feature | — |
| `perf` | Performance improvement | — |
| `test` | Thêm/sửa tests | — |
| `chore` | Maintenance, deps | — |
| `ci` | CI config changes | — |

```bash
# Ví dụ
git commit -m "feat(auth): add Google OAuth2 login"
git commit -m "fix(api): handle null user in getProfile endpoint"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(db): extract query builder to separate module"

# Breaking change:
git commit -m "feat(api)!: change response format for /users endpoint"
# hoặc dùng footer:
# BREAKING CHANGE: Response now wraps data in { data, meta } object.
```

### Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH[-prerelease]

     1  .  2  .  3
     │     │     └── PATCH: backward-compatible bug fixes
     │     └──────── MINOR: new backward-compatible functionality  
     └────────────── MAJOR: incompatible API changes

1.0.0-alpha.1 → 1.0.0-beta.2 → 1.0.0-rc.1 → 1.0.0 (stable)
```

### Auto-versioning trong CI/CD

```bash
# semantic-release: auto bump version từ conventional commits
npx semantic-release
# feat → MINOR bump, fix → PATCH, BREAKING CHANGE → MAJOR
# Auto: update package.json + CHANGELOG.md + GitHub release + npm publish
```

---

## 6. Pull Request Best Practices

### PR Description Template

```markdown
## What
Brief description of what this PR does.

## Why
Link to issue/ticket. Closes #123

## How
Key implementation decisions.

## Testing
- [ ] Unit tests added/updated
- [ ] Tested locally
```

### PR Size & Review Guidelines

```
PR size:
  ✅ < 200 lines:    Easy to review (~15 phút)
  ⚠️ 200-400 lines:  Acceptable, nhưng review quality giảm
  ❌ > 400 lines:     Chia nhỏ!

Kỹ thuật chia nhỏ PR:
  → Separate refactoring from feature (2 PRs)
  → Split by layer: DB schema → API → UI
  → Use feature flags để merge incomplete code

Reviewer checklist:
  ✅ Logic đúng? Edge cases? Error handling?
  ✅ Tests: unit tests cho new code?
  ✅ Security: input validation, auth checks?
  ✅ Performance: N+1 queries, unnecessary re-renders?

Good review comments:
  ✅ "Consider using findOrCreate to avoid race condition here"
  ❌ "This is wrong" (không giải thích tại sao)
  ❌ Nitpicking formatting (để linter lo)
```

---

## 7. Branch Naming & CODEOWNERS

### Branch Naming Convention

```bash
# Format: type/TICKET-description
feature/AUTH-234-google-oauth
fix/SHOP-789-cart-calculation
hotfix/prod-memory-leak
docs/update-api-docs
refactor/extract-auth-service
release/v2.1.0
```

### CODEOWNERS — Auto-assign reviewers

```bash
# .github/CODEOWNERS
*                        @team-lead          # Default reviewer
/backend/                @backend-team
/frontend/               @frontend-team
/infra/                  @devops-team
/src/auth/               @security-team      # Sensitive files
/.github/workflows/      @devops-team
*.sql                    @database-team
```

---

## 8. So sánh tổng hợp

| | Git Flow | GitHub Flow | Trunk-Based |
|---|---|---|---|
| **Complexity** | Cao | Thấp | Trung bình |
| **Branches** | main + develop + feature + release + hotfix | main + feature | main + short-lived |
| **Deploy** | Scheduled (weekly/monthly) | Continuous (daily) | Continuous (nhiều lần/ngày) |
| **Feature flags** | Không cần | Không cần | **Bắt buộc** |
| **Team size** | TB-Lớn | Nhỏ-TB | Mọi size (cần senior) |
| **Best for** | Mobile apps, libraries | SaaS, web apps | Google, Meta, Netflix |
| **CI/CD** | Recommended | Cần | **Rất nghiêm ngặt** |
| **Risk** | Release chậm | Bug vào prod nhanh | Cần feature flags mgmt |

**Lời khuyên:**
- Mới bắt đầu → **GitHub Flow** (đơn giản, hiệu quả)
- Release mobile apps → **Git Flow** (cần version control)
- Team experienced, deploy > 1 lần/ngày → **Trunk-Based**

---

## Bài tập thực hành

- [ ] Setup GitHub Flow cho 1 project (branch protection + PR required)
- [ ] Conventional Commits: cấu hình commitlint + husky
- [ ] Feature flag: ẩn/hiện feature bằng environment variable
- [ ] CODEOWNERS: cấu hình auto-assign reviewers

---

## Tài nguyên thêm

- [GitHub Flow Guide](https://docs.github.com/en/get-started/quickstart/github-flow) — Official
- [Atlassian Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) — Detailed
- [Trunk-Based Development](https://trunkbaseddevelopment.com/) — In-depth
- [Conventional Commits](https://www.conventionalcommits.org/) — Specification

---

*Tài liệu liên quan: `git/02-git-advanced.md` | `git/04-github-gitlab-basics.md`*
