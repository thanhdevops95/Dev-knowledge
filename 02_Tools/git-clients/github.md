# 🛠️ GitHub — User Guide

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 24/05/2026\
> **Loại:** Tool individual — focused vào GitHub\
> **Đọc trước:** [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — đã chọn GitHub vì lý do gì

> 🎯 *User guide đầy đủ cho GitHub — account + 2FA, SSH key, PR workflow, Actions, Pages, CLI, security. **CHỈ về GitHub** — so sánh với GitLab/Bitbucket đã ở [00_what-is-git-hosting.md](./00_what-is-git-hosting.md).*

---

## Tình huống — bạn tạo account GitHub lần đầu

Sau bộ Git ([5 lesson bạn story](../../01_Foundations/version-control/git/lessons/01_basic/)), bạn đã quen với `git init`, `commit`, `branch`. Sếp bảo *"push lên GitHub đi"*. Bạn vào github.com:

> *Sign up → đặt username gì? `dev123`? `nguyen-van-a`? Có thay đổi sau được không?*
> *Yêu cầu 2FA → cài app nào? Lỡ mất phone thì sao?*
> *Tạo repo: Public hay Private? README có check không?*
> *Push lên → bị từ chối "Authentication failed". Sao lúc local ok mà push lên server không được?*

5 câu hỏi đầu tiên. Bài này dẫn bạn (và bạn) qua **mọi setup cần thiết** trong 30 phút, từ account → push xong → setup PR workflow với đồng nghiệp → publish portfolio Pages → tự động CI/CD qua Actions.

→ Cuối bài bạn có **GitHub setup production-ready**, dùng cho mọi project tiếp theo.

---

## 1️⃣ Vậy GitHub là gì?

**GitHub** là **git hosting platform** lớn nhất thế giới (~70% thị phần dev), do **Microsoft** sở hữu từ 2018. Là cloud cho Git repo + bộ tool collab (Issues, PR, Actions, Pages, ...).

🪞 **Ẩn dụ**: GitHub giống **mạng xã hội cho dev** — profile của bạn = portfolio. Mỗi project = bài post. Star/Fork = like/share. Pull Request = comment + collab. Recruiter scroll qua GitHub bạn như scroll LinkedIn.

**Số liệu nhanh (2026)**:
- ~150 triệu user
- ~500 triệu repo (public + private)
- 95% trong top 100 OSS project host ở GitHub
- Owner Microsoft → tích hợp sâu VS Code, Copilot, Azure

---

## 2️⃣ Bước 1: Tạo account + 2FA

### 2.1 Sign up

1. Vào [github.com](https://github.com) → **Sign up** (top right)
2. Email + password + **username**:
   - **Username quan trọng**: hiện trong URL profile (`github.com/<username>`) + URL mọi repo. Đổi sau **được** nhưng break link cũ.
   - Khuyến nghị: dùng tên thật (vd `nguyenvana`), không số random (`user12345`). Recruiter tin tưởng tên thật hơn.
3. Verify email
4. Chọn plan **Free** (mọi tính năng cốt lõi, unlimited private repo)

### 2.2 BẮT BUỘC: Bật 2FA (Two-Factor Authentication)

GitHub yêu cầu 2FA **mandatory** từ 2024 — nếu không bật, account bị khoá sau warning period.

**3 option 2FA**:

| Option | An toàn | Tiện | Khuyến nghị |
|---|---|---|---|
| 🌟 **Authenticator app** (1Password, Authy, Google Auth) | ⭐⭐⭐ | ⭐⭐ | **Default cho hầu hết** |
| **Hardware key** (YubiKey) | ⭐⭐⭐⭐ | ⭐ | Power user, security paranoid |
| **SMS** | ⭐ (SIM swap risk) | ⭐⭐⭐ | KHÔNG khuyến nghị (GitHub đang deprecate) |

**Setup**:
1. Settings → Password and authentication → **Two-factor authentication** → **Enable 2FA**
2. Pick "Authenticator app"
3. Mở app (1Password / Authy / Google Auth) → scan QR
4. Nhập code 6 số từ app
5. **LƯU 10 RECOVERY CODE** vào nơi an toàn (1Password / paper note ở tủ) — KHÔNG screenshot vào Photos cloud
6. ✅ 2FA active

> ⚠️ **Mất phone + recovery code = mất account vĩnh viễn**. GitHub support không khôi phục được. Lưu recovery code riêng trong password manager.

### 2.3 Verify với SSH (sau)

Sau khi setup SSH key (§3), test: `ssh -T git@github.com` → output `Hi <username>! You've successfully authenticated`. → SSH OK.

---

## 3️⃣ Bước 2: Authentication — Chọn 1 trong 3 cách

Khi `git push` lên GitHub, cần auth. **3 cách**:

| Method | Setup | Bảo mật | Phù hợp |
|---|---|---|---|
| 🌟 **SSH key** | 1 lần (10 phút), dùng mãi | ⭐⭐⭐ | **Default cho dev** |
| **Personal Access Token (PAT)** | Gen token, paste khi push | ⭐⭐ | CI/CD, script automation |
| **GitHub CLI (`gh auth login`)** | 1 lệnh, auth qua browser | ⭐⭐ | Beginner muốn nhanh |

### 3.1 SSH Key (khuyến nghị)

**Bước 1**: Generate key

```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

- `ed25519` = thuật toán mới nhất, ngắn hơn RSA
- `-C` = comment (email để dễ nhận diện key sau)
- Khi hỏi passphrase → nhập (recommend) hoặc Enter bỏ qua

Key tạo ở `~/.ssh/`:
- `id_ed25519` — private key (BÍ MẬT, KHÔNG SHARE)
- `id_ed25519.pub` — public key (cái này upload GitHub)

**Bước 2**: Copy public key

```bash
# macOS
pbcopy < ~/.ssh/id_ed25519.pub

# Linux (cần xclip)
xclip -selection clipboard < ~/.ssh/id_ed25519.pub

# Windows (Git Bash)
cat ~/.ssh/id_ed25519.pub | clip
```

Hoặc cat ra rồi copy thủ công:
```bash
cat ~/.ssh/id_ed25519.pub
# ssh-ed25519 AAAA... your@email.com
```

**Bước 3**: Add public key lên GitHub

1. GitHub → **Settings** → **SSH and GPG keys** → **New SSH key**
2. **Title**: tên máy (vd `MacBook Pro 2024`)
3. **Key type**: Authentication Key
4. **Key**: paste public key
5. Add SSH key

**Bước 4**: Test

```bash
ssh -T git@github.com
# Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.
```

**Bước 5**: Sử dụng SSH URL khi clone/add remote

```bash
# HTTPS — yêu cầu PAT mỗi lần
git clone https://github.com/user/repo.git

# SSH — dùng key tự động, không hỏi password
git clone git@github.com:user/repo.git

# Đổi remote HTTPS → SSH
git remote set-url origin git@github.com:user/repo.git
```

### 3.2 Personal Access Token (PAT)

Dùng khi không setup được SSH (vd Windows, CI runner) hoặc cần token có scope cụ thể.

**Tạo PAT**:
1. Settings → Developer settings → **Personal access tokens** → **Fine-grained tokens** → Generate new token
2. **Name**: vd `Laptop work — push only`
3. **Expiration**: 30/60/90 days (KHÔNG `No expiration`)
4. **Repository access**: All public OR specific
5. **Permissions**: chỉ cần `Contents: Read and write` cho push/pull cơ bản
6. Generate → **COPY TOKEN NGAY** (chỉ hiện 1 lần)

**Dùng**:
```bash
git push https://github.com/user/repo
# Username: <github username>
# Password: <paste TOKEN, không phải password>
```

→ Token = "mật khẩu thay thế". KHÔNG dùng password GitHub thực để push.

### 3.3 GitHub CLI

Cài `gh` (xem §8 dưới) → 1 lệnh:

```bash
gh auth login
# Where? GitHub.com
# Protocol? HTTPS
# Authenticate Git with creds? Yes
# How? Login with browser
```

→ Browser mở, login, done. `gh` setup luôn git credentials.

> 💡 **Khuyến nghị**: Beginner → `gh auth login` (nhanh nhất). Dev daily → SSH key. CI/CD → PAT scope hẹp.

---

## 4️⃣ Bước 3: Tạo repository đầu tiên

### 4.1 Trên GitHub web

1. `+` (top right) → **New repository**
2. **Owner**: account bạn (hoặc org)
3. **Repository name**: vd `myapp` (tên ngắn, kebab-case)
4. **Description**: 1 dòng mô tả
5. **Visibility**:
   - **Public**: ai cũng đọc được. Phù hợp OSS, portfolio.
   - **Private**: chỉ bạn + collab thấy. Phù hợp commercial, learning.
6. **Initialize** (tuỳ):
   - ✅ Add README — nếu start repo mới rỗng
   - ❌ KHÔNG check nếu đã có repo local muốn push lên (sẽ conflict)
7. **gitignore template**: chọn theo ngôn ngữ (Python, Node, Go, ...) → tự gen `.gitignore` chuẩn
8. **License**: chọn nếu OSS (MIT phổ biến nhất)
9. Create repository

### 4.2 Push project local lên repo mới

```bash
cd ~/projects/myapp
git remote add origin git@github.com:<username>/myapp.git
git branch -M main          # đảm bảo branch tên 'main' (không phải master)
git push -u origin main     # -u = set upstream, lần sau chỉ git push
```

→ Refresh page GitHub → thấy code 🎉

---

## 5️⃣ Repository UI Tour — Hiểu mọi tab

```
Repo page navigation:
┌─────────────────────────────────────────────────────────────┐
│  <> Code  │  Issues  │  PR  │  Actions  │  Projects  │  Wiki │  Insights  │  Settings │
└─────────────────────────────────────────────────────────────┘
```

| Tab | Để làm gì |
|---|---|
| **Code** | Browse file/folder, README, README hiện ở dưới |
| **Issues** | Bug tracker, feature request, discussion |
| **Pull Requests** | Workflow merge code có review |
| **Actions** | CI/CD pipelines (xem §7) |
| **Projects** | Kanban board (To do / In progress / Done) |
| **Wiki** | Tài liệu project (markdown) |
| **Security** | Vulnerability alerts, secret scanning |
| **Insights** | Stats commits, contributors, traffic |
| **Settings** | Config repo (collab, branch protection, webhooks, ...) |

### File browser

- Click file → xem content + diff history qua `Blame`
- Press `t` (file finder fuzzy) — search file nhanh
- Press `.` ở repo → mở **github.dev** = VS Code trong browser ⭐ siêu tiện
- Press `,` ở repo → mở **github.codespaces** (paid)

### Branch switcher

- Default: `main` branch
- Click dropdown → switch branch hoặc tag

---

## 6️⃣ Pull Request Workflow — bạn + đồng nghiệp collab

Workflow chuẩn khi 2+ người làm chung. Tiếp bạn story:

### Setup branch protection (1 lần)

Trước khi team làm, bạn set rule cho `main`:

1. Settings → **Branches** → **Add rule**
2. **Branch name pattern**: `main`
3. ✅ Require a pull request before merging
4. ✅ Require approvals: **1** (đồng nghiệp approve mới merge được)
5. ✅ Require status checks (CI pass)
6. ✅ Do not allow bypassing (kể cả admin)
7. Save

→ Giờ KHÔNG ai (kể cả bạn admin) push thẳng vào `main`. Phải qua PR.

### Đồng nghiệp làm feature mới qua PR

```bash
# 1. Pull main mới nhất
git checkout main
git pull

# 2. Tạo branch
git checkout -b feature/add-search

# 3. Code + commit
echo "search logic" > search.js
git add search.js
git commit -m "feat: add search functionality"

# 4. Push branch lên GitHub
git push -u origin feature/add-search
```

GitHub return link:
```
remote: Create a pull request for 'feature/add-search' on GitHub by visiting:
remote:      https://github.com/acmeshop/myapp/pull/new/feature/add-search
```

### Mở Pull Request

5. Click link → trang **New Pull Request**
6. **Title**: `feat: add search functionality` (giống commit message)
7. **Description** (Markdown):

   ```markdown
   ## Summary
   Add search bar to homepage.

   ## Changes
   - New file `search.js` with search logic
   - Integrate vào header component

   ## Test plan
   - [x] Tested locally with keywords "test", "code"
   - [x] Empty search returns all items

   Closes #42
   ```

8. **Reviewers**: assign bạn
9. **Labels**: `feature`, `frontend`
10. **Projects**: link vào Sprint Board
11. Create pull request

### bạn review

Bạn nhận notification → vào PR:

- **Files changed** tab: xem diff
- Comment trên dòng cụ thể: hover dòng → `+` icon → viết comment
- **Review changes** (top right):
   - **Comment** — góp ý không block
   - **Approve** ✅ — OK merge
   - **Request changes** ❌ — chưa OK, đồng nghiệp phải sửa

### Đồng nghiệp sửa theo feedback

```bash
# Vẫn đang ở branch feature/add-search
# Sửa theo comment
git add .
git commit -m "fix: handle empty search case"
git push    # PR tự update với commit mới
```

→ Bạn re-review. OK → Approve.

### Merge

12. Click **Merge pull request**. 3 option:
   - **Create merge commit** — giữ history nguyên (default)
   - **Squash and merge** ⭐ — gộp 5 commit feature thành 1 commit clean (recommend cho main)
   - **Rebase and merge** — linear history (advanced)
13. Click **Confirm merge**
14. Click **Delete branch** (xoá branch trên GitHub, local thì `git branch -d feature/add-search`)

🎉 Code đã vào `main` qua PR có review.

---

## 7️⃣ GitHub Actions — CI/CD built-in

Actions = CI/CD chạy tự động khi event xảy ra (push, PR, schedule, ...).

### File config: `.github/workflows/*.yml`

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install deps
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest -v

      - name: Lint
        run: ruff check .
```

→ Mỗi push/PR vào `main` → GitHub spin up Ubuntu VM → chạy test + lint → báo pass/fail.

### Khi test fail → PR bị block (nếu setup branch protection)

```
✅ build (passed)
❌ test (failed)        ← đồng nghiệp phải sửa
✅ lint (passed)
```

→ Reviewer thấy đỏ → reject. đồng nghiệp phải fix test.

### Free tier

- **Public repo**: unlimited Actions minutes
- **Private repo**: 2,000 min/tháng (Linux), free Free plan

### Use cases phổ biến

| Workflow | Trigger |
|---|---|
| Run tests + lint | `on: push, pull_request` |
| Build + push Docker image | `on: push tag` |
| Deploy to AWS/Vercel | `on: push main` |
| Auto-merge dependabot PR | `on: pull_request_target` |
| Schedule daily backup | `on: schedule (cron)` |

→ Marketplace có **20,000+ pre-built actions** ở [github.com/marketplace](https://github.com/marketplace?type=actions) — tra cứu khi cần.

---

## 8️⃣ GitHub Pages — Host static site / portfolio

Mỗi user có **1 site free** ở `<username>.github.io`. Repo public + folder `docs/` hoặc branch `gh-pages` → tự deploy.

### Setup nhanh

1. Tạo repo tên `<username>.github.io` (chính xác)
2. Push `index.html` vào root
3. Settings → **Pages** → **Source**: Deploy from branch `main` → `/` root
4. Save → đợi 1-2 phút → site live ở `https://<username>.github.io`

### Cho portfolio repo bất kỳ

1. Repo Settings → Pages → Source: `main` → `/docs`
2. Tạo `docs/index.html` (hoặc đẩy build output của Vite/Next.js)
3. URL: `https://<username>.github.io/<repo-name>`

### Use cases

- Portfolio cá nhân
- Documentation static (MkDocs, Docusaurus)
- Blog (Jekyll built-in, hoặc Hugo/Astro)
- Demo project React/Vue static

> 💡 Custom domain: thêm CNAME → trỏ tới `<username>.github.io` → free HTTPS qua Let's Encrypt.

---

## 9️⃣ GitHub CLI (`gh`) — Power user

CLI tool chính thức quản GitHub từ terminal, **không cần web UI**.

### Cài

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
winget install GitHub.cli
```

### Auth + cơ bản

```bash
gh auth login                       # login qua browser
gh repo clone user/repo             # clone repo
gh repo create myapp --public       # tạo repo
gh repo view --web                  # mở repo trong browser
```

### PR workflow qua CLI

```bash
# Tạo PR (đang ở feature branch)
gh pr create --title "feat: search" --body "..."

# List PR đang mở
gh pr list

# Checkout PR của người khác
gh pr checkout 42

# Review PR
gh pr review 42 --approve
gh pr review 42 --request-changes --body "Need test"

# Merge
gh pr merge 42 --squash --delete-branch
```

### Issues

```bash
gh issue create --title "Bug: login fail"
gh issue list --label bug
gh issue close 10
```

### Actions

```bash
gh run list                # list workflow runs
gh run view 1234           # xem chi tiết run
gh run watch               # follow run đang chạy
gh run rerun 1234          # rerun failed
```

→ `gh` siêu tiện cho power user. Tutorial đầy đủ: `gh help` hoặc [cli.github.com/manual/](https://cli.github.com/manual/).

---

## 1️⃣0️⃣ Security best practices

### ✅ MUST DO

1. **2FA bật** — đã làm ở §2.2
2. **SSH key passphrase** — protect private key
3. **PAT scope hẹp** — chỉ cấp quyền cần thiết, expiration 30-90 days
4. **Branch protection** cho `main` (PR review + status check required)
5. **Secret scanning** — Settings → Code security → enable. GitHub scan repo tìm leaked AWS keys / tokens.
6. **Dependabot alerts** — tự động alert khi dependency có CVE
7. **Signed commits** (Advanced) — commit có GPG/SSH signature

### Signed Commits — verify identity

```bash
# Setup SSH signing (modern, 2023+)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Add SSH key as "Signing Key" trong GitHub Settings → SSH and GPG keys
# (cùng key authentication, nhưng add lần nữa với role "Signing Key")
```

→ Commit có badge "Verified" xanh trên GitHub. Không sao chép identity được.

### ❌ KHÔNG ĐƯỢC LÀM

- ❌ Commit `.env` chứa API key, password
- ❌ Share password GitHub (dùng 2FA, không share)
- ❌ Push code dùng git config tên/email người khác
- ❌ Clone private repo lên máy không trusted
- ❌ Disable 2FA "vì phiền" — bị khoá account

> 💡 Nếu lỡ commit secret: rotate secret NGAY, dùng `git filter-repo` xoá khỏi history. Xem [Git lesson 04 — Undo + Recovery](../../01_Foundations/version-control/git/lessons/01_basic/04_undo-and-recovery.md).

---

## 1️⃣1️⃣ Settings nâng cao đáng biết

| Setting | Đường đi | Tác dụng |
|---|---|---|
| **Profile picture + Bio** | Settings → Profile | Recruiter nhìn vào |
| **Email visibility** | Settings → Emails | Có thể "Keep my email private" — git commit dùng email noreply |
| **SSH/GPG keys** | Settings → SSH and GPG keys | Auth + signing |
| **Tokens** | Settings → Developer settings → Tokens | PAT scope hẹp |
| **OAuth Apps** | Settings → Applications | Review app nào đã grant access (revoke nếu không dùng) |
| **Sessions** | Settings → Sessions | Log out machine bị mất |
| **Block users** | Settings → Blocked users | Block troll trong issue/PR |
| **Notification** | Settings → Notifications | Filter notification (đỡ spam) |

### Pro tip: Repo-level settings

| Setting | Tác dụng |
|---|---|
| **Default branch** | Đổi tên (`main` recommend, KHÔNG `master`) |
| **Branch protection** | Như §6 |
| **Webhooks** | Notify Slack/Discord khi có push |
| **Pages** | Như §8 |
| **Secret variables** | Lưu API key dùng trong Actions |
| **Topics** | Tag repo (vd `python`, `web`, `cli`) — SEO |
| **Social preview** | Image hiển thị khi share Twitter/LinkedIn |

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: Mất phone + recovery code → mất account

**Hậu quả**: GitHub không khôi phục được. Repo private mất, OSS contributor mất.

**Cách tránh**:
- LƯU 10 recovery code → 1Password / paper note ở tủ
- Có 2 authenticator app trên 2 device (vd Authy multi-device)
- Backup recovery code in cứng

### ❌ Pitfall: Commit với git config sai email

```bash
# .gitconfig nhầm sang account khác → commit không count vào contribution graph
git log --format='%ae' | sort -u
# work@gmail.com — nhưng GitHub account dùng personal@gmail.com → KHÔNG hiện contribution
```

**Cách tránh**:
- Set email per-repo: `git config user.email personal@gmail.com`
- Hoặc dùng `<id>+<username>@users.noreply.github.com` (email noreply của GitHub)

### ❌ Pitfall: Push thẳng `main`, không qua PR

- **Hậu quả**: code chưa review vào prod, không ai biết "ai đã sửa cái này"
- **Cách tránh**: setup branch protection (§6) — kể cả admin cũng KHÔNG bypass được

### ❌ Pitfall: PAT có scope quá rộng + không expire

```
PAT scope: "admin:org, repo:full, delete_repo, ..."
Expiration: No expiration
```

- **Hậu quả**: PAT leak = hacker dùng MÃI MÃI với full access
- **Cách tránh**: scope chỉ cần, expiration 30-90 days, rotate định kỳ

### ❌ Pitfall: GitHub Pages không deploy

```
Pages settings: branch = main, folder = /docs
Nhưng file ở /
```

- **Cách check**:
  - Verify file `index.html` đúng folder set
  - Settings → Pages → xem URL deployment status
  - Build log trong Actions tab (nếu dùng custom build)

### ✅ Best practice: README repo phải chuẩn

Mỗi repo nên có README đầy đủ:

```markdown
# Project Name

> 1-line description

## Features
- ...

## Installation
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Usage
\`\`\`bash
python main.py
\`\`\`

## Tech stack
- Python 3.11
- FastAPI
- PostgreSQL

## Demo
![screenshot](docs/screenshot.png)

## License
MIT
```

→ Recruiter scroll qua GitHub bạn, README đẹp = ấn tượng tốt.

---

## 🧠 Self-check

**Q1.** Khi nào dùng SSH vs PAT vs `gh auth login`?

<details>
<summary>💡 Đáp án</summary>

| Method | Use case |
|---|---|
| **SSH key** | Dev daily — setup 1 lần, dùng mãi, không hỏi password mỗi lần push |
| **PAT** | Automation/CI runner — token có scope hẹp, expire định kỳ |
| **`gh auth login`** | Beginner — 1 lệnh, OAuth qua browser, setup luôn cả git credentials |

Recommend cho beginner: bắt đầu `gh auth login` (nhanh), khi quen → setup SSH key cho dev daily.

</details>

**Q2.** PR workflow — vì sao team chuyên nghiệp KHÔNG push thẳng `main`?

<details>
<summary>💡 Đáp án</summary>

**3 lý do**:

1. **Code review** — bug được peer phát hiện trước khi vào prod
2. **CI check** — test/lint chạy tự động trên PR, fail thì không merge được
3. **Audit trail** — mỗi thay đổi vào main có history "ai approve, khi nào, vì sao"

Setup branch protection trên `main` (Settings → Branches) force quy trình này. Kể cả admin không bypass được nếu chọn "Do not allow bypassing".

</details>

**Q3.** Lỡ commit `.env` chứa API key + push lên public repo. Phải làm gì?

<details>
<summary>💡 Đáp án</summary>

**Theo thứ tự khẩn cấp**:

1. **Rotate (đổi) API key NGAY** — vào provider (AWS/OpenAI/...) revoke key cũ, tạo key mới. Bots scan GitHub trong giây phút.
2. **Xoá khỏi git history** (không đủ chỉ `git rm`):
   ```bash
   git filter-repo --path .env --invert-paths
   git push --force
   ```
3. **Add `.env` vào `.gitignore`** ngay, force re-add:
   ```bash
   echo ".env" >> .gitignore
   git rm --cached .env
   git add .gitignore
   git commit -m "Add .env to gitignore"
   ```
4. **Notify team** — họ phải clone lại repo (history đã rewrite)

→ Phòng tránh: Setup **Secret scanning** (Settings → Code security) + **pre-commit hook** `gitleaks`.

</details>

**Q4.** Strangerd có thể đọc public repo bạn. Vậy sao đỡ leak?

<details>
<summary>💡 Đáp án</summary>

**Public repo** nghĩa là **code** public — KHÔNG có nghĩa **mọi thứ** public:

| Public | Private |
|---|---|
| Code (sources) | Secret variables (Settings → Secrets and variables) |
| README, Issues, PR | Webhook URLs |
| Contributors | Audit log |
| Insights stats | OAuth tokens |

→ Secret variable trong Actions:
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.PROD_API_KEY }}    # ← secret, không leak ra log
  run: ./deploy.sh
```

GitHub mask secret trong log. Nếu bạn `echo $API_KEY` → output hiển thị `***`.

</details>

---

## ⚡ Cheatsheet

### Common URLs

| URL pattern | Đi đến |
|---|---|
| `github.com/<user>` | Profile |
| `github.com/<user>/<repo>` | Repo |
| `github.com/<user>/<repo>/issues` | Issues |
| `github.com/<user>/<repo>/pulls` | PRs |
| `github.com/<user>/<repo>/actions` | Actions runs |
| `github.com/<user>/<repo>/settings` | Settings |
| `github.dev/<user>/<repo>` ⭐ | VS Code in browser |
| `github1s.com/<user>/<repo>` | Alternative VS Code in browser |

### Keyboard shortcuts (web UI)

| Key | Tác dụng |
|---|---|
| `?` | Show all shortcuts |
| `s` / `/` | Focus search |
| `g + i` | Go to Issues |
| `g + p` | Go to Pull Requests |
| `g + a` | Go to Actions |
| `t` (in repo) | Find file fuzzy |
| `,` (in repo) | Open in github.dev (VS Code) |
| `.` (in repo) | Same — VS Code |
| `l` (in PR/Issue) | Label |

### `gh` CLI essentials

| Command | Tác dụng |
|---|---|
| `gh auth login` | Login |
| `gh repo clone user/repo` | Clone |
| `gh repo create` | Tạo repo |
| `gh pr create` | Tạo PR |
| `gh pr checkout 42` | Checkout PR |
| `gh pr merge --squash` | Merge squash |
| `gh issue list` | List issues |
| `gh run watch` | Follow Actions run |
| `gh release create v1.0.0` | Tạo release |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Repository (repo) | Kho | Folder chứa code + git history trên GitHub |
| Fork | Nhánh hoá | Copy repo của người khác về account bạn |
| Star | (giữ EN) | Bookmark/like repo (không phải follow) |
| Watch | Theo dõi | Nhận notification mỗi update repo |
| Issue | Vấn đề | Bug report / feature request |
| Pull Request (PR) | Yêu cầu kéo | Đề xuất merge branch X → Y, có review |
| Merge | Gộp | Đưa code từ PR vào main branch |
| Squash | Nén | Gộp N commit thành 1 commit khi merge |
| Branch protection | Bảo vệ nhánh | Rule ngăn push thẳng main |
| 2FA | (giữ EN) | Two-Factor Authentication |
| Personal Access Token (PAT) | (giữ EN) | Token thay password, scope hẹp |
| SSH key | Khoá SSH | Cặp public/private auth không cần password |
| Actions | (giữ EN) | CI/CD pipelines built-in |
| Pages | (giữ EN) | Static site hosting free |
| Codespaces | (giữ EN) | Cloud dev environment (paid) |
| Dependabot | (giữ EN) | Bot auto-update dependency có CVE |
| Copilot | (giữ EN) | AI code completion ($10/mo) |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

- 🛠️ [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — So sánh GitHub với GitLab/Bitbucket
- 🎓 [Git lesson 03 — Remote + GitHub](../../01_Foundations/version-control/git/lessons/01_basic/03_remote-and-github.md) — bài lesson đồng nghiệp join project
- 🎓 [Git lesson 04 — Undo + Recovery](../../01_Foundations/version-control/git/lessons/01_basic/04_undo-and-recovery.md) — fix khi lỡ commit secret
- 🧭 [Zero to Coder Stage 1](../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-tối-thiểu-2-3-tuần) — beginner setup GitHub
- 🛠️ [GitHub Desktop](./github-desktop.md) (chưa có) — GUI nếu không thích CLI
- 🛠️ [VS Code](../ide/vs-code.md) — IDE tích hợp GitHub tốt nhất

### Tài nguyên ngoài

- [GitHub Docs](https://docs.github.com/) — chính thức, đầy đủ nhất
- [GitHub Skills](https://skills.github.com/) — interactive course free
- [gh CLI manual](https://cli.github.com/manual/) — tra cứu `gh` lệnh
- [Awesome GitHub Profile READMEs](https://github.com/abhisheknaiidu/awesome-github-profile-readme) — mẫu profile đẹp
- [Awesome Actions](https://github.com/sdras/awesome-actions) — bộ sưu tập Actions hay
- [GitHub Status](https://www.githubstatus.com/) — check khi GitHub down
- [Octoverse](https://octoverse.github.com/) — thống kê GitHub hàng năm

---

## 📌 Changelog

- **v1.1.0 (24/05/2026)** — Apply Blueprint v0.5.4 §3.5. Bulk replace fictional character "bạn" → "bạn"/"Bạn"/"Mình" theo context (generic role thay tên riêng tự bịa). Nội dung kỹ thuật giữ nguyên.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên — full user guide GitHub. 11 phần lớn: tình huống bạn tạo account → §1 GitHub là gì + ẩn dụ mạng xã hội cho dev → §2 Account + 2FA → §3 Auth 3 cách (SSH/PAT/gh login) → §4 Tạo repo + push → §5 UI tour 8 tab → §6 PR workflow chi tiết với bạn+đồng nghiệp → §7 Actions CI/CD → §8 Pages portfolio → §9 `gh` CLI → §10 Security 7 must-do + 5 không được → §11 Settings nâng cao. 5 pitfall + 4 self-check + cheatsheet URL/shortcut/gh + glossary 17 thuật ngữ.
