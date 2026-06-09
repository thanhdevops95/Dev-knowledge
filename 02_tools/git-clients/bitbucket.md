# 🛠️ Bitbucket — User Guide (Atlassian ecosystem)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Loại:** Tool individual — focused vào Bitbucket Cloud\
> **Đọc trước:** [00_what-is-git-hosting.md](./00_what-is-git-hosting.md)

> 🎯 *User guide cho Bitbucket — git hosting của Atlassian, **tích hợp sâu Jira + Confluence + Trello**. Phù hợp công ty đã dùng Atlassian stack. CHỈ về Bitbucket — so sánh với GitHub/GitLab đã ở [00_what-is-git-hosting.md](./00_what-is-git-hosting.md).*

---

## Tình huống — team đã dùng Jira

Bạn vào công ty mới. Sếp:
> *"Chúng ta dùng Atlassian — Jira cho ticket, Confluence cho docs, Bitbucket cho code. Tạo account Atlassian, mọi thứ link sẵn."*

Bạn search "Bitbucket vs GitHub" — đa số reviewer ca ngợi GitHub. Vậy tại sao công ty này chọn Bitbucket? Tại sao 2026 vẫn nhiều team dùng?

→ Lý do: **Atlassian ecosystem**. Khi team đã invest vào Jira (project management) + Confluence (wiki), Bitbucket integrate **siêu sâu**:
- PR auto-link Jira ticket (vd `JIRA-123` → click vào ticket)
- Branch tạo từ Jira ticket → tự đặt tên `JIRA-123-feature-name`
- Smart Commits — commit message `JIRA-123 #close` → tự close ticket
- CI build status → hiện trong Jira ticket

→ Đó là **value Bitbucket** không match được bởi GitHub/GitLab. Bài này dạy bạn dùng.

---

## 1️⃣ Vậy Bitbucket là gì?

**Bitbucket** = git hosting của **Atlassian** (Australia, công ty làm Jira/Confluence/Trello). Sinh 2008, mua bởi Atlassian 2010.

**2 phiên bản**:

| Version | Mô tả |
|---|---|
| **Bitbucket Cloud** (bitbucket.org) | SaaS, free cho team ≤ 5 user |
| **Bitbucket Data Center** | Self-host, enterprise, paid (đã thay thế "Bitbucket Server" deprecated 2024) |

> ⚠️ **2026 lưu ý**: Bitbucket Server / Bitbucket Data Center self-host đắt + complex. Đa số dùng Bitbucket Cloud. Self-host needs → cân nhắc GitLab CE.

**Số liệu 2026**:
- ~6% thị phần dev (sau GitHub 70%, GitLab 10%)
- ~10 triệu user
- Strong ở enterprise có sẵn Atlassian stack

🪞 **Ẩn dụ**: Bitbucket giống **Microsoft Teams trong bộ Office** — không phải tốt nhất so với chuyên gia (Slack), nhưng tích hợp seamless với phần còn lại (Word, Excel, Outlook). Đó là điểm mạnh.

---

## 2️⃣ Bitbucket vs GitHub/GitLab — Khi nào chọn?

| Tiêu chí | GitHub | GitLab | **Bitbucket** |
|---|---|---|---|
| **Thị phần** | 70% | 10% | 6% |
| **Free private repo** | ✅ Unlimited | ✅ Unlimited | ✅ Unlimited team ≤ 5 |
| **CI/CD** | Actions ⭐⭐ | GitLab CI ⭐⭐⭐ | Pipelines ⭐ (50 min free) |
| **AI Coding** | Copilot ⭐⭐⭐ | Duo ⭐⭐ | Atlassian Intelligence ⭐ |
| **Jira integration** | ✓ (qua app) | ✓ (qua webhook) | ⭐⭐⭐ **Native built-in** |
| **Confluence integration** | ❌ | ❌ | ⭐⭐⭐ Native |
| **Trello integration** | ❌ | ❌ | ⭐⭐⭐ Native |
| **Self-host** | Enterprise paid | CE free ⭐ | Data Center paid |
| **Cộng đồng** | ⭐⭐⭐ | ⭐⭐ | ⭐ |

### Pick Bitbucket khi:

- ✅ **Team đã dùng Jira** → tích hợp Smart Commits + auto-link ticket
- ✅ **Atlassian Cloud** subscription (Jira + Confluence + Bitbucket gói chung)
- ✅ **Team ≤ 5 user** muốn free tier
- ✅ **Workflow heavy ticket-driven** (Agile/Scrum strict)

### KHÔNG pick Bitbucket khi:

- ❌ Team > 5 user mà không subscribe Atlassian — đắt hơn GitHub/GitLab
- ❌ OSS project — community ở GitHub
- ❌ AI heavy — Copilot tốt hơn nhiều
- ❌ Cần self-host → GitLab CE ngon hơn

---

## 3️⃣ Bước 1: Tạo account Atlassian

Bitbucket dùng **Atlassian account** chung — 1 account access Jira + Confluence + Bitbucket + Trello.

1. Vào [bitbucket.org](https://bitbucket.org) → **Sign up free** (hoặc đăng nhập nếu đã có Atlassian)
2. Email + password — hoặc Sign in with Google
3. Chọn **username** Bitbucket (riêng với Atlassian display name)
4. Verify email

### 2FA

1. Bitbucket → **Personal settings** → **Two-step verification**
2. Chọn authenticator app (recommend)
3. Scan QR + lưu recovery codes

### SSH key (giống GitHub/GitLab)

1. Cùng `~/.ssh/id_ed25519` đã setup
2. Bitbucket → **Personal settings** → **SSH keys** → **Add key**
3. Paste public key + label
4. Test: `ssh -T git@bitbucket.org`

### App Password (= PAT của GitHub)

Bitbucket gọi là **App Password** thay PAT:

1. Personal settings → **App passwords** → **Create app password**
2. Label + scopes (`Repositories: Read/Write`)
3. Create → copy NGAY

Dùng: HTTPS push hỏi password → paste app password (không phải Atlassian password).

---

## 4️⃣ Workspace + Repository

Bitbucket có **3 cấp tổ chức** (khác GitHub/GitLab):

```
Workspace (= "Organization" GitHub)
└── Project (group repos logically — KHÁC project GitLab)
    └── Repository
```

### Tạo workspace

1. **Create** (top-right) → **Workspace**
2. Name + slug + member type
3. Plan: Free / Standard ($3/user/mo) / Premium ($6/user/mo)

### Tạo project (group repos)

1. Workspace → **Projects** → **Create project**
2. Name + key (vd `MYAPP`) + access level
3. → Trong project này tạo nhiều repos

### Tạo repository

1. **Create** → **Repository**
2. Owner: workspace + project
3. Repository name: `myapp`
4. Access: Public / Private
5. Include README, .gitignore
6. Create

### Push project local

```bash
cd ~/projects/myapp
git remote add origin git@bitbucket.org:<workspace>/myapp.git
git branch -M main
git push -u origin main
```

---

## 5️⃣ Repository UI Tour

```
Repo navigation (left sidebar):
┌─────────────────────┐
│ 📂 Source           │  ← Browse code
│ ➕ Commits          │  ← Commit history
│ 🔀 Branches         │  ← Branch list
│ 🔃 Pull requests    │  ← PRs (Bitbucket gọi là PR, không phải MR)
│ 📦 Pipelines        │  ← CI/CD
│ 🚀 Deployments      │  ← Deploy tracking
│ 🔒 Security         │  ← Vuln scan
│ 📊 Reports          │  ← Code review, code quality
│ ⚙️ Repository settings│
└─────────────────────┘
```

| Tab | Tương đương GitHub |
|---|---|
| Source | Code |
| Commits | (Commits dưới Code → Commits) |
| Branches | Branches |
| Pull requests | Pull requests |
| Pipelines | Actions |
| Deployments | Environments |
| Security | Security |
| Reports | Insights |

### File browser shortcut

- Click file → view + edit (online editor)
- Press `t` → file finder

---

## 6️⃣ Pull Request workflow + Jira integration

Bitbucket gọi **Pull Request (PR)** như GitHub (không phải MR như GitLab).

### Tạo PR

```bash
git checkout -b JIRA-123-add-search    # branch tên có Jira ticket key
git push -u origin JIRA-123-add-search
```

Bitbucket auto-detect Jira ticket key `JIRA-123` trong tên branch → link sẵn.

Trên Bitbucket web:
1. **Pull requests** → **Create pull request**
2. Source: `JIRA-123-add-search` → Destination: `main`
3. **Title**: tự fill từ commit (Bitbucket có suggest theo Jira ticket title)
4. **Description**: markdown
5. **Reviewers**: chọn
6. ✅ **Close source branch when merged**
7. Create

### Smart Commits — Magic ⚡

Commit message với syntax đặc biệt → auto thực thi action trong Jira:

```bash
git commit -m "JIRA-123 #close Fixed search bug"
# → Jira ticket JIRA-123 tự close

git commit -m "JIRA-456 #time 2h #comment 'Implemented feature' Add login"
# → Log 2h vào Jira + add comment
```

| Magic command | Tác dụng Jira |
|---|---|
| `#close` | Close ticket |
| `#in-progress` | Set status In Progress |
| `#time 2h 30m` | Log time |
| `#comment '...'` | Add comment |
| `#resolve` | Resolve ticket |

→ Đây là **value chính** của Bitbucket — không platform khác có Smart Commits native.

### Branch từ Jira ticket

Trong Jira ticket:
- **Create branch** (right panel "Development")
- Auto-name: `JIRA-123-feature-search`
- Auto-push lên Bitbucket
- → Bạn `git fetch && git checkout JIRA-123-feature-search` local

→ Workflow Agile/Scrum: pick ticket → click "Create branch" → code → PR → smart commit close → ticket done. Hoàn toàn link.

### Review

- **Diff view**: side-by-side hoặc unified
- Inline comment
- **Code Insights**: badge "✓ Test passed" hoặc "❌ SonarQube quality gate failed"
- **Approve** button (yêu cầu N approvers theo settings)
- **Merge** với 3 option: merge commit / squash / fast-forward

### Default Reviewers + Branch Permissions

Repo settings → **Branch permissions**:
- Branch `main`: prevent direct push, require N approvals, require successful build
- Default reviewers auto-assign khi tạo PR

---

## 7️⃣ Bitbucket Pipelines — CI/CD built-in

`bitbucket-pipelines.yml` (root project):

```yaml
image: node:20

pipelines:
  default:
    - parallel:
        - step:
            name: Test
            caches:
              - node
            script:
              - npm ci
              - npm test
        - step:
            name: Lint
            script:
              - npm run lint

  branches:
    main:
      - step:
          name: Build
          script:
            - npm run build
          artifacts:
            - dist/**
      - step:
          name: Deploy to staging
          deployment: staging
          script:
            - curl -X POST $DEPLOY_URL
```

### Free tier

- **50 build minutes/tháng** (chia sẻ trong workspace)
- Mở rộng: $10/mo cho 1,000 min, etc.

> ⚠️ **Weakest CI/CD** trong 3 platform lớn. 50 min free là **rất ít** so với GitHub (2,000 min) hoặc GitLab (400 min). Heavy CI → pick GitHub hoặc GitLab.

### Use case

- Project nhỏ + Atlassian ecosystem
- Test/lint cơ bản trên PR
- Deploy đơn giản

Heavy CI/CD → external tools (Jenkins, Buildkite) hoặc GitLab CI.

---

## 8️⃣ Integration với Atlassian stack

### Jira integration (chính)

1. Bitbucket workspace settings → **Integrations** → **Jira**
2. Connect Jira site URL
3. → Sau đó:
   - Branch có Jira key → auto-link
   - Smart Commits hoạt động
   - Jira ticket có panel "Development" hiện branches/PRs liên quan
   - PR merge → Jira ticket auto transition (configurable)

### Confluence integration

- Embed code snippets từ Bitbucket vào Confluence page
- Link PR vào docs
- Auto-update docs từ commit (Confluence macro)

### Trello integration

- Card Trello link tới Bitbucket PR
- Show PR status (open/merged/closed) trong card

→ Đây là điểm **lock-in** vào Atlassian — đã invest stack thì giữ Bitbucket. Không thì các integration này không nhiều ý nghĩa.

---

## 9️⃣ Code Insights — Quality Reports

Bitbucket có **Code Insights** API — third-party tool gửi report về vào PR:

- **SonarQube** — code quality
- **Snyk** — security vuln
- **CodeClimate** — maintainability
- **Codecov** — test coverage

PR sẽ hiện:
```
✓ SonarQube: A grade
⚠ Snyk: 2 high vulnerabilities
✓ Coverage: 87% (+2%)
```

→ Reviewer thấy đỏ → block merge cho đến khi fix.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Free tier 50 min CI/CD hết quá nhanh

```yaml
# Mỗi PR trigger:
# - Test (5 min) × 3 steps parallel = 15 min/PR
# - 4 PR/ngày × 30 ngày = ~1,800 min/tháng > 50 min free
```

- **Hậu quả**: build queue dài, dev chờ
- **Cách fix**: cache aggressive, parallel jobs, hoặc upgrade plan

### ❌ Cạm bẫy: Smart Commit không hoạt động

```bash
git commit -m "JIRA-123 #close fixed bug"
# → Jira ticket KHÔNG close
```

**Lý do thường gặp**:
- Jira chưa connect Bitbucket workspace (Settings → Integrations)
- User git commit (`user.email`) không match với Atlassian account
- Jira ticket key sai (case-sensitive, vd `jira-123` vs `JIRA-123`)

**Fix**:
- Verify Jira integration setup
- `git config user.email <atlassian-email>`
- Check Jira project key exact

### ❌ Cạm bẫy: Mistake Bitbucket Server (deprecated) với Bitbucket Cloud

**Atlassian deprecated Bitbucket Server 2024** → migration sang Bitbucket Data Center. Tutorial cũ có thể dạy Bitbucket Server — KHÔNG còn áp dụng.

**Cách tránh**: dùng tutorial 2024+ chỉ. Bitbucket Cloud cho mọi use case thường.

### ❌ Cạm bẫy: Free tier 5 user nhưng team scale

Team scale > 5 user → **buộc upgrade** Standard ($3/user/mo) hoặc Premium ($6/user/mo). Tổng cost có thể đắt hơn GitHub Team.

**So sánh team 10 user**:
- GitHub Team: $4/user × 10 = $40/mo
- Bitbucket Standard: $3/user × 10 = $30/mo (vẫn rẻ hơn ⭐)
- GitLab Premium: $19/user × 10 = $190/mo ($$$)

→ Team size ảnh hưởng quyết định.

### ✅ Best practice: Setup branch permissions + default reviewers ngay từ đầu

Repo settings → Branch permissions → `main`:
- ✅ Prevent direct push
- ✅ Require 1+ approvals
- ✅ Require successful build
- ✅ Default reviewers: tech lead + senior

→ Tránh ai đó push thẳng `main` "vì gấp" → break CI/CD chain.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Khi nào CÓ sense chọn Bitbucket?

<details>
<summary>💡 Đáp án</summary>

**4 case duy nhất**:

1. **Team đã dùng Jira** + Confluence — Bitbucket integrate native, không platform khác match được
2. **Team ≤ 5 user** muốn free private repo (GitHub Free Team cũng free, nhưng nếu đã Atlassian, gắn liền)
3. **Workflow Agile/Scrum strict** với ticket-driven dev
4. **Enterprise đã subscribe Atlassian Cloud** suite

→ Còn lại: GitHub > Bitbucket trong mọi metric khác.

</details>

**Q2.** Smart Commits là gì? Khác commit thường ra sao?

<details>
<summary>💡 Đáp án</summary>

**Smart Commits** = commit message với syntax đặc biệt → auto trigger action trong Jira ticket.

Khác commit thường:

| Commit thường | Smart Commit |
|---|---|
| `"Fix login bug"` | `"JIRA-123 #close Fix login bug"` |
| Jira ticket KHÔNG update | Jira ticket `JIRA-123` tự close |

**Magic syntax** (yêu cầu integration Jira-Bitbucket setup):
- `JIRA-123 #close` — close ticket
- `JIRA-123 #time 2h` — log time
- `JIRA-123 #comment "..."` — add comment
- `JIRA-123 #in-progress` — change status

→ Workflow Agile: code + push + ticket update — chỉ 1 git commit.

</details>

**Q3.** Bitbucket Pipelines yếu nhất trong 3 platform lớn. Khi nào không nên dùng?

<details>
<summary>💡 Đáp án</summary>

**KHÔNG dùng Bitbucket Pipelines khi**:

- **CI heavy** (> 50 min/tháng free) — phải upgrade $10+/mo cho 1,000 min, kém value
- **Matrix builds phức tạp** — Pipelines yaml syntax kém GitLab CI / GitHub Actions
- **Cần marketplace actions** — Pipelines ít plugin community
- **Self-host runner unlimited** — Bitbucket support self-host runner nhưng phức tạp hơn GitLab

**Alternative**:
- Repo trên Bitbucket nhưng CI ở **GitHub Actions** (webhook trigger) — hybrid
- Hoặc **Jenkins / Buildkite** external
- Hoặc move full sang **GitLab CI** nếu CI là focus chính

→ Nhiều team dùng Bitbucket cho repo + Jira integration, CI external cho mạnh hơn.

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Action | Cách |
|---|---|
| Tạo PR | Pull requests → Create |
| Smart Commit | `git commit -m "JIRA-123 #close <message>"` |
| Branch từ Jira | Jira ticket → Development → Create branch |
| App Password | Personal settings → App passwords → Create |
| Setup CI | Tạo `bitbucket-pipelines.yml` ở root |
| Connect Jira | Workspace settings → Integrations → Jira |

### `bb` CLI (community, không official)

Atlassian không có CLI official cho Bitbucket. Community alternatives:
- [`bb`](https://github.com/poljuxon/bb) — CLI cho Bitbucket Cloud
- API direct qua curl + Personal Access Token

→ Đa số dùng web UI + Jira CLI nếu cần automation.

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| EN | VN | Giải thích |
|---|---|---|
| Workspace | Không gian làm việc | "Organization" trong Bitbucket |
| Project (Bitbucket) | Dự án | Group nhiều repo logically (KHÁC GitLab Project = repo) |
| Repository | Kho | Git repo |
| Pull Request (PR) | Yêu cầu kéo | Như GitHub (KHÁC GitLab gọi MR) |
| Smart Commit | (giữ EN) | Commit message với magic syntax → trigger Jira |
| Pipelines | (giữ EN) | CI/CD của Bitbucket |
| App Password | (giữ EN) | = PAT của GitHub |
| Code Insights | (giữ EN) | Third-party report (SonarQube, Snyk, ...) vào PR |
| Default reviewer | Reviewer mặc định | Auto-assign khi tạo PR |
| Branch permission | Quyền branch | Như branch protection của GitHub |
| Atlassian | (giữ EN) | Công ty sở hữu Bitbucket + Jira + Confluence + Trello |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

- 🛠️ [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — So sánh git hosting
- 🛠️ [github.md](./github.md) — User guide GitHub
- 🛠️ [gitlab.md](./gitlab.md) — User guide GitLab
- 🎓 [Git lessons](../git/lessons/01_basic/) — Git concept (dùng cho mọi platform)

### 🌐 Tài nguyên tham khảo khác

- [Bitbucket Cloud Docs](https://support.atlassian.com/bitbucket-cloud/) — chính thức
- [Bitbucket Pipelines reference](https://support.atlassian.com/bitbucket-cloud/docs/configure-bitbucket-pipelinesyml/)
- [Smart Commits guide](https://support.atlassian.com/jira-software-cloud/docs/process-issues-with-smart-commits/)
- [Jira ↔ Bitbucket integration](https://support.atlassian.com/jira-software-cloud/docs/integrate-jira-cloud-with-bitbucket-cloud/)
- [Atlassian Marketplace](https://marketplace.atlassian.com/) — apps + integrations

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Tool individual #4 trong git-clients/. Cover: tình huống team đã Jira → §1 Bitbucket là gì + 2 phiên bản → §2 vs GitHub/GitLab (4 case pick / 4 case không pick) → §3 Account + SSH + App Password → §4 Workspace + Project + Repo (3-tier) → §5 UI tour → §6 PR + **Smart Commits magic** + Jira branch creation → §7 Pipelines yếu nhất → §8 Atlassian integration → §9 Code Insights. 5 pitfall + 3 self-check.
