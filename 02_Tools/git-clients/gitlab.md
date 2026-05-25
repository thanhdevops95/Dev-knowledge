# 🛠️ GitLab — User Guide (Cloud + Self-host)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 24/05/2026\
> **Loại:** Tool individual — focused vào GitLab\
> **Đọc trước:** [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — đã chọn GitLab vì lý do gì

> 🎯 *User guide đầy đủ cho GitLab — account, SSH key, **Merge Request** (MR), **GitLab CI/CD** mạnh nhất, self-host **Community Edition**, Auto DevOps. CHỈ về GitLab — so sánh với GitHub đã ở [00_what-is-git-hosting.md](./00_what-is-git-hosting.md).*

---

## Tình huống — bạn join team mới dùng GitLab

Tiếp bạn story. Bạn đổi việc sang **fintech startup**. First day, sếp: *"Repo của tụi anh ở GitLab self-host trên server công ty. Tạo account đi."*

Bạn ngạc nhiên:
- Tại sao **không dùng GitHub** mà tự host GitLab?
- **Merge Request** là gì? — sao không phải Pull Request?
- File `.gitlab-ci.yml` cũng như GitHub Actions?
- GitLab có gì **khác** đáng học?

Sếp giải thích:
> *"Banking + finance không được lưu code ngoài cloud — compliance. GitLab Community Edition (CE) free + self-host được. Plus, GitLab CI là CI/CD mạnh nhất thị trường, all-in-one không cần thêm tool."*

→ Bạn cài account → bài này dạy mọi cái cần biết để **switch từ GitHub sang GitLab** + tận dụng strengths.

---

## 1️⃣ Vậy GitLab là gì?

**GitLab** là git hosting platform thành lập 2011 (sớm hơn GitHub bị Microsoft mua) bởi GitLab Inc. (công ty all-remote). 2 mode:

| Mode | Mô tả |
|---|---|
| **GitLab.com** (Cloud) | SaaS, free tier rộng, đa số dev cá nhân dùng cloud |
| **GitLab Self-Managed** | Cài trên server riêng — phổ biến cho enterprise, banking, gov |

**Số liệu 2026**:
- ~10% thị phần dev (sau GitHub ~70%)
- ~30 triệu user cloud
- Self-managed: hàng trăm nghìn instance (mỗi instance = 1 enterprise/team)
- Open source: **Community Edition (CE)** — FREE forever

🪞 **Ẩn dụ**: GitLab giống **Microsoft Office trên server công ty** (offline + control 100%). GitHub là **Google Docs cloud** (online, lock-in vendor).

---

## 2️⃣ Tại sao GitLab? — Strengths vs GitHub

| Khía cạnh | GitHub | GitLab | Winner |
|---|---|---|---|
| **Thị phần** | ~70% | ~10% | GitHub |
| **AI Copilot** | ⭐⭐⭐ Built-in | Duo (catching up) | GitHub |
| **Cộng đồng VN** | ⭐⭐⭐ | ⭐ | GitHub |
| **OSS ecosystem** | ⭐⭐⭐ | ⭐⭐ | GitHub |
| **CI/CD** | Actions (good) | **GitLab CI** (great) | **GitLab** ⭐ |
| **Self-host free** | ❌ (Enterprise paid) | ✅ **CE free unlimited** | **GitLab** ⭐ |
| **All-in-one DevOps** | Modular (cần thêm tool) | Built-in (issue + CI + registry + monitor) | **GitLab** ⭐ |
| **Issue tracker** | ✓ | ⭐ Epic + Iteration mạnh | **GitLab** |
| **Container Registry** | ⭐ GH Container Registry | ⭐ Built-in | Tie |
| **Compliance** | ⭐ Advanced (paid) | ⭐⭐⭐ Built-in (audit, SAST, license scan) | **GitLab** ⭐ |
| **Pricing model** | Generous free | Generous free + open source | Tie |

→ **GitLab thắng**: CI/CD, self-host, all-in-one, compliance. **GitHub thắng**: thị phần, OSS, AI, community.

**Pick GitLab khi**:
- Cần **self-host** (banking, healthcare, gov, sensitive code)
- **CI/CD heavy** (matrix builds, complex pipelines, runner pool)
- **All-in-one** — không muốn 10 tool khác nhau (issue/CI/registry/monitor)
- **Compliance** requirement (SAST, DAST, dependency scan built-in)

---

## 3️⃣ Bước 1: Tạo account + 2FA

### 3.1 Sign up GitLab.com

1. Vào [gitlab.com](https://gitlab.com) → **Register now**
2. Email + password + **username**:
   - URL profile: `gitlab.com/<username>`
   - Đổi sau được nhưng break links
3. Verify email
4. Plan **Free** (5 user/group, unlimited repo, 400 CI min/tháng)

> 💡 **Self-host**: nếu công ty bạn dùng instance riêng (vd `gitlab.company.com`), không sign up gitlab.com. Hỏi sếp link instance + cách tạo account (thường là LDAP/SSO).

### 3.2 Bật 2FA

GitLab khuyến nghị (không bắt buộc như GitHub) bật 2FA:

1. **Edit Profile** (top-right avatar → Edit profile)
2. **Account** tab → **Two-factor authentication** → **Enable two-factor authentication**
3. Authenticator app (1Password, Authy, Google Auth) → scan QR
4. Nhập code → **Submit**
5. **LƯU recovery codes** vào nơi an toàn

### 3.3 SSH key setup (similar GitHub)

Đã có SSH key từ GitHub (xem [github.md §3.1](./github.md))? Có thể **dùng chung 1 key** cho cả 2.

1. Copy public key: `cat ~/.ssh/id_ed25519.pub`
2. GitLab → Edit Profile → **SSH Keys** (left sidebar)
3. **Add new key** → paste → title `MacBook Pro` → expiration (optional)
4. **Add key**
5. Test: `ssh -T git@gitlab.com` → `Welcome to GitLab, @<username>!`

### 3.4 Personal Access Token (PAT)

1. Edit Profile → **Access Tokens** → **Add new token**
2. Name + Expiration + Scopes (`api`, `read_repository`, `write_repository`)
3. Create → copy token NGAY

---

## 4️⃣ Tạo project (GitLab gọi repo là "Project")

### 4.1 Trên GitLab web

1. **`+`** → **New project/repository**
2. **Create blank project**
3. Điền:
   - **Project name**: `myapp`
   - **Project URL**: `<group>/<myapp>` — group là namespace (user hoặc team)
   - **Visibility**: Private / Internal / Public
   - ✅ Initialize with README
4. **Create project**

> 💡 **Group** = tương đương "Organization" trên GitHub. Tạo group để chia sẻ project cho team.

### 4.2 Push project local

```bash
cd ~/projects/myapp
git remote add origin git@gitlab.com:<group>/myapp.git
git branch -M main
git push -u origin main
```

→ Refresh page → thấy code 🎉.

### 4.3 Project UI — Các tab chính

```
Project page navigation:
┌──────────────────────────────────────────────────────────────────┐
│  Project │ Repository │ CI/CD │ Deployments │ Packages │ ...    │
└──────────────────────────────────────────────────────────────────┘
```

| Tab | Mô tả |
|---|---|
| **Project** → Issues | Bug tracker, Epic, Iteration |
| **Repository** → Files, Commits, Branches, Tags | Browse code + history |
| **Code review** → **Merge requests** | Workflow MR (= GitHub PR) |
| **Build** → **Pipelines, Jobs, Schedules** | GitLab CI/CD |
| **Deploy** → **Environments, Releases, Feature flags** | Deploy tracking |
| **Operate** → **Container Registry, Kubernetes, Terraform** | Infra |
| **Monitor** → **Metrics, Logs, Alerts** | Observability (Prometheus integration) |
| **Analyze** → **Repository, Code Review, CI/CD analytics** | Stats |
| **Settings** | Config project |

→ Đặc trưng GitLab: **built-in nhiều mảng** — không cần Sentry, Datadog, Argo riêng. Trade-off: complexity cao hơn GitHub.

---

## 5️⃣ Merge Request (MR) — Equivalent của PR

GitLab gọi là **Merge Request** (MR), GitHub gọi là **Pull Request** (PR). **Cùng concept**.

### Tạo MR

```bash
# Same flow như GitHub
git checkout -b feature/add-search
# ... code + commit
git push -u origin feature/add-search
```

GitLab CLI tự gợi ý URL tạo MR:
```
remote: To create a merge request for feature/add-search, visit:
remote:   https://gitlab.com/group/myapp/-/merge_requests/new?merge_request[source_branch]=feature/add-search
```

Hoặc trên GitLab web: **Code review → Merge requests → New merge request**.

### MR UI

- **Title + Description** (markdown, support `Closes #123`)
- **Source branch** (`feature/add-search`) → **Target branch** (`main`)
- **Assignee** (người sẽ merge) + **Reviewer** (người review)
- **Labels** + **Milestone** + **Time tracking**
- ✅ **Mark as draft** — work-in-progress
- ✅ **Delete source branch when merge** — clean up tự động
- ✅ **Squash commits when merge** — gộp commit feature thành 1

### Review

- **Changes** tab: diff side-by-side hoặc inline
- Comment trên line: click `+` icon
- **Approve** button — required nếu setup "Approval rules"
- **Submit review**

### Setup Approval rules (= GitHub branch protection)

Settings → Merge requests → **Merge request approvals**:
- ✅ Required approvals: 1 (hoặc N)
- ✅ Prevent self-approval
- ✅ Required from code owners (đọc `CODEOWNERS` file)

→ Branch `main` được bảo vệ: phải có MR + approval + CI pass mới merge được.

### Merge

3 strategy như GitHub:
- **Merge commit** — default
- **Squash and merge** ⭐ — gộp commit feature thành 1
- **Rebase, then merge** — linear history

> 💡 **Khác biệt nhỏ với GitHub PR**:
> - GitLab có **WIP / Draft** indicator built-in
> - GitLab MR có **Time tracking** built-in (estimate + log)
> - GitLab có **Discussions** vs comment — discussion phải resolve trước khi merge

---

## 6️⃣ GitLab CI/CD — Strength chính

**GitLab CI/CD** built-in mọi instance (cloud + self-host). Tốt hơn GitHub Actions ở:
- **YAML syntax** rõ ràng hơn
- **Matrix builds** mạnh hơn (multi-dimension)
- **DAG pipelines** built-in (parallel + dependencies)
- **Runner pool** unlimited khi self-host
- **Container Registry** + **Artifacts** built-in

### File `.gitlab-ci.yml`

```yaml
# .gitlab-ci.yml (root project)
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"

cache:
  paths:
    - node_modules/

test:
  stage: test
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test
    - npm run lint
  coverage: '/Statements\s*:\s*([0-9.]+)/'

build:
  stage: build
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
  needs: [test]

deploy-staging:
  stage: deploy
  image: alpine:latest
  script:
    - apk add curl
    - curl -X POST $STAGING_DEPLOY_URL
  environment:
    name: staging
    url: https://staging.myapp.com
  only:
    - main
```

→ Pipeline chạy tự động khi push. CI/CD tab → xem realtime.

### Free tier

- **gitlab.com cloud**: 400 CI min/tháng (shared runner)
- **Self-host**: unlimited runner trên server bạn
- **Mở rộng**: $19/user/mo Premium, $99/user/mo Ultimate (audit, compliance, SAST)

### Auto DevOps — Magic ⚡

Enable Auto DevOps (Settings → CI/CD → Auto DevOps → enable):
- Tự detect language (Node/Python/Go/Java/...) → build pipeline phù hợp
- Build → test → SAST scan → dependency scan → container scan → deploy
- Bạn KHÔNG cần viết `.gitlab-ci.yml` — GitLab tự gen

→ Beginner / lazy dev: rất tiện. Production team: thường custom yaml để control kỹ.

---

## 7️⃣ Self-host GitLab Community Edition (CE)

**GitLab CE** = open source edition, **free forever**, self-host trên server của bạn.

### Use case

- Banking, healthcare, gov (compliance đòi không cloud)
- Khởi nghiệp ở nước có giới hạn cloud foreign (Trung Quốc, Nga)
- Học DevOps deep — control 100%
- Tránh vendor lock-in

### Cài CE trên Ubuntu (lightweight test)

```bash
# 1. Cài dependencies
sudo apt update
sudo apt install -y curl openssh-server ca-certificates tzdata perl

# 2. Add GitLab repo
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash

# 3. Cài
sudo EXTERNAL_URL="http://gitlab.local" apt install gitlab-ce

# 4. Truy cập
# Mở browser → http://gitlab.local (hoặc IP server)
# Default username: root
# Password ban đầu: /etc/gitlab/initial_root_password
sudo cat /etc/gitlab/initial_root_password
```

### Yêu cầu phần cứng

| Setup | RAM | Disk | Use |
|---|---|---|---|
| **Lab / personal** | 4 GB | 20 GB | 1 user, ~10 repo |
| **Small team** | 8 GB | 50 GB | 10 user, ~50 repo |
| **Production** | 16 GB+ | 100 GB+ | 100 user, runner pool |

> ⚠️ GitLab self-host **nặng** — Ruby on Rails + PostgreSQL + Redis + Sidekiq + Nginx + Prometheus. Không phù hợp VPS $5.

### Docker / K8s deployment

```bash
docker run -d \
  --name gitlab \
  -p 80:80 -p 443:443 -p 22:22 \
  -v gitlab-config:/etc/gitlab \
  -v gitlab-logs:/var/log/gitlab \
  -v gitlab-data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest
```

Hoặc Helm chart cho K8s production.

### Backup + maintain

```bash
# Backup
sudo gitlab-backup create

# Restore
sudo gitlab-backup restore BACKUP=<timestamp>

# Update version
sudo apt update && sudo apt install gitlab-ce
sudo gitlab-ctl reconfigure
```

> 💡 Production self-host: cần đội DevOps maintain. Không phải plug-and-play. Nếu team không có DevOps → dùng GitLab.com cloud.

---

## 8️⃣ Settings + Security

### Project Settings quan trọng

| Setting | Đường đi | Tác dụng |
|---|---|---|
| **Visibility** | Settings → General | Private/Internal/Public |
| **Protected branches** | Settings → Repository → Protected branches | Như GitHub branch protection |
| **MR approval rules** | Settings → Merge requests | Required approvers |
| **CI/CD variables** | Settings → CI/CD → Variables | Secrets cho pipeline (mask + protected) |
| **Webhooks** | Settings → Integrations → Webhooks | Notify Slack/Discord |
| **Mirror repository** | Settings → Repository → Mirroring | Sync 2 chiều với GitHub repo khác |

### Security best practices

1. **2FA bật** (xem §3.2)
2. **SSH key có passphrase**
3. **PAT scope hẹp** + expiration 30-90 days
4. **Protected branch** cho `main` (yêu cầu MR approval + CI pass)
5. **SAST + Dependency scanning** — bật trong `.gitlab-ci.yml`:
   ```yaml
   include:
     - template: Security/SAST.gitlab-ci.yml
     - template: Security/Dependency-Scanning.gitlab-ci.yml
   ```
6. **Secret detection** — built-in scanner tìm leaked credentials
7. **Compliance frameworks** (Ultimate tier): SOC 2, HIPAA, FedRAMP templates

---

## 9️⃣ GitLab CLI — `glab`

CLI tool tương tự `gh`:

```bash
# Cài
brew install glab           # Mac
sudo apt install glab       # Ubuntu

# Auth
glab auth login

# Common commands
glab repo clone group/project
glab mr create --title "feat: search" --description "..."
glab mr list
glab mr checkout 42
glab issue list
glab ci status              # CI pipeline hiện tại
glab ci view                # mở pipeline trong browser
```

→ Đầy đủ command: `glab --help`.

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: Quá tin GitLab Auto DevOps

Auto DevOps tự gen pipeline, nhưng:
- Có thể không match exact build process của project
- Kích hoạt tất cả security scan → pipeline chậm
- Khó debug khi fail (yaml tự gen, không thấy)

**Cách tránh**: dùng Auto DevOps để học → sau migrate sang `.gitlab-ci.yml` tự viết.

### ❌ Pitfall: Self-host CE cho team nhỏ

Self-host GitLab CE **nặng** (8+ GB RAM, maintain phức tạp). Team < 10 người KHÔNG đáng tự host — dùng gitlab.com cloud free tier đủ.

**Khi nào tự host xứng**:
- Compliance bắt buộc
- > 50 user
- Có đội DevOps đủ skill maintain

### ❌ Pitfall: Mirror GitHub repo → GitLab nhưng CI fail

Khi mirror repo từ GitHub sang GitLab, CI yaml giữ nguyên (GitHub Actions yaml) — GitLab KHÔNG hiểu format. Cần **convert sang `.gitlab-ci.yml`**.

**Tool migration**:
- [actions-importer](https://docs.gitlab.com/ee/user/project/import/index.html#by-importing-from-other-services) — GitLab import tool có actions converter

### ❌ Pitfall: Quên Protected variables trong CI

```yaml
deploy:
  script:
    - curl -X POST $PROD_API_KEY    # ❌ Nếu PROD_API_KEY không "Protected", branch feature/x cũng dùng được
```

**Cách tránh**: Settings → CI/CD → Variables → tick **Protect variable** cho secrets → chỉ branch protected (vd `main`) mới access được.

### ✅ Best practice: 1 repo per project + sub-group cho team

```
GitLab group: mycompany
├── frontend/         (sub-group)
│   ├── web-app
│   ├── mobile-app
│   └── design-system
├── backend/          (sub-group)
│   ├── api-gateway
│   ├── user-service
│   └── payment-service
└── infrastructure/   (sub-group)
    ├── terraform
    └── k8s-manifests
```

→ Permission inheritance: ai có access `mycompany` thấy toàn bộ. Có access `frontend/` chỉ thấy sub đó.

---

## 🧠 Self-check

**Q1.** Khi nào nên chọn GitLab thay GitHub?

<details>
<summary>💡 Đáp án</summary>

**4 use case chính**:

1. **Cần self-host** — banking, healthcare, gov, compliance requirement. GitLab CE free unlimited.
2. **CI/CD heavy** — matrix builds, complex pipelines, runner pool. GitLab CI mạnh hơn Actions.
3. **All-in-one DevOps** — không muốn 10 tool khác nhau. GitLab built-in issue + CI + registry + monitor + container scan.
4. **Compliance** — SAST, DAST, dependency scan, audit log built-in (đặc biệt Ultimate tier).

→ Còn lại, GitHub ưu thế: thị phần lớn nhất, ecosystem mạnh, Copilot, OSS community.

</details>

**Q2.** Merge Request (GitLab) vs Pull Request (GitHub) khác gì?

<details>
<summary>💡 Đáp án</summary>

**Concept same** — đề xuất merge branch → có review.

**Khác biệt nhỏ**:
- **Tên**: MR (GitLab) vs PR (GitHub). Cùng nghĩa.
- **WIP / Draft**: GitLab có nút "Mark as draft" built-in. GitHub Draft PR cũng có (sau 2019).
- **Approvals**: GitLab có "Approval rules" mạnh hơn (số approver tối thiểu, code owners, etc.). GitHub cũng có nhưng cần Branch protection setup.
- **Discussions vs Comments**: GitLab phân biệt "Discussion" (phải resolve trước merge) và "Comment" (chỉ note). GitHub chỉ có Comment + Review.
- **Time tracking**: GitLab built-in (estimate + log). GitHub cần extension.

→ Workflow giống nhau, chi tiết khác chút.

</details>

**Q3.** Khi nào nên tự host GitLab CE vs dùng gitlab.com cloud?

<details>
<summary>💡 Đáp án</summary>

**Self-host CE khi**:
- Compliance bắt buộc (banking, healthcare, gov)
- Team > 50 người (cost cloud cao)
- Có đội DevOps maintain
- Cần control 100% (audit, custom integration)

**Dùng cloud gitlab.com khi**:
- Team nhỏ (< 50 người) — free tier đủ
- Không có DevOps team
- Không yêu cầu compliance đặc biệt
- Muốn focus vào code thay vì maintain infra

→ Rule of thumb: dưới 50 dev → cloud. Trên 50 + có compliance → self-host.

</details>

---

## ⚡ Cheatsheet

### URLs

| URL pattern | Đi đến |
|---|---|
| `gitlab.com/<user>` | Profile |
| `gitlab.com/<group>/<project>` | Project |
| `gitlab.com/<group>/<project>/-/issues` | Issues |
| `gitlab.com/<group>/<project>/-/merge_requests` | MRs |
| `gitlab.com/<group>/<project>/-/pipelines` | CI Pipelines |
| `gitlab.com/<group>/<project>/-/settings` | Settings |

### `glab` CLI

| Command | Tác dụng |
|---|---|
| `glab auth login` | Login |
| `glab repo clone group/project` | Clone |
| `glab mr create` | Tạo MR |
| `glab mr list` | List MR |
| `glab mr checkout 42` | Checkout MR |
| `glab mr merge --squash` | Merge squash |
| `glab issue create` | Tạo issue |
| `glab ci status` | Xem pipeline hiện tại |
| `glab release create v1.0.0` | Tạo release |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Project | Dự án | "Repo" trong GitLab (cùng concept) |
| Group / Sub-group | Nhóm | Namespace chứa project, phân quyền team |
| Merge Request (MR) | Yêu cầu merge | Tương đương PR của GitHub |
| Approval rules | Quy tắc duyệt | Required reviewers cho MR |
| Protected branch | Nhánh được bảo vệ | Cấm push thẳng + yêu cầu MR |
| Pipeline | (giữ EN) | 1 lần chạy CI/CD |
| Runner | (giữ EN) | Worker chạy CI jobs (shared hoặc self-host) |
| Auto DevOps | (giữ EN) | Pipeline tự gen theo language detect |
| CE / EE | Community Edition / Enterprise Edition | Free OSS vs Paid |
| `.gitlab-ci.yml` | (giữ EN) | File config CI/CD ở root project |
| SAST / DAST | (giữ EN) | Security scan static/dynamic |
| `glab` | (giữ EN) | CLI tool GitLab official |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

- 🛠️ [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — So sánh với GitHub/Bitbucket
- 🛠️ [github.md](./github.md) — User guide GitHub
- 🎓 [Git lessons](../../01_Foundations/version-control/git/lessons/01_basic/) — Git concept (cùng dùng cho GitLab)

### Tài nguyên ngoài

- [GitLab Docs](https://docs.gitlab.com/) — chính thức
- [GitLab CI/CD reference](https://docs.gitlab.com/ee/ci/yaml/) — `.gitlab-ci.yml` đầy đủ
- [GitLab CE install](https://about.gitlab.com/install/) — self-host
- [GitLab Examples](https://docs.gitlab.com/ee/ci/examples/) — pipeline mẫu
- [Awesome GitLab CI](https://github.com/lorraine-campbell/awesome-gitlab-ci) — curated templates
- [Migrate from GitHub](https://docs.gitlab.com/ee/user/project/import/github.html) — guide chính thức

---

## 📌 Changelog

- **v1.1.0 (24/05/2026)** — Apply Blueprint v0.5.4 §3.5. Bulk replace fictional character "bạn" → "bạn"/"Bạn"/"Mình" theo context (generic role thay tên riêng tự bịa). Nội dung kỹ thuật giữ nguyên.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Tool individual #3 trong git-clients/. Cover: tình huống bạn join fintech → §1 GitLab là gì → §2 Strengths vs GitHub (bảng 11 tiêu chí) → §3 Account + 2FA + SSH + PAT → §4 Project + UI tour 8 tab → §5 MR workflow + approval rules → §6 GitLab CI/CD (yaml mẫu + Auto DevOps) → §7 Self-host CE chi tiết → §8 Settings + security + SAST → §9 `glab` CLI. 5 pitfall + 3 self-check + cheatsheet.
