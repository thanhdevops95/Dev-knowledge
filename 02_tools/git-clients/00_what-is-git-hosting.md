# 🛠️ Git Hosting — Chọn nền tảng nào? (GitHub vs GitLab vs Bitbucket vs ...)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Loại:** Tool category — overview + so sánh + khuyến nghị\
> **Đọc trước:** [Git là gì](../../01_foundations/version-control/git/lessons/01_basic/00_what-is-git.md) — phân biệt Git (tool) vs Git hosting (platform)

> 🎯 *Bạn đã biết Git (concept VCS), giờ cần chọn **nền tảng cloud** để host repo + collab team. File này so sánh 5 lựa chọn chính (GitHub/GitLab/Bitbucket/Codeberg/Gitea) + recommend theo profile. Chi tiết từng platform → file riêng (`github.md`, `gitlab.md`, ...).*

---

## Tình huống — beginner choose platform lần đầu

Bạn vừa học Git xong (clone, commit, push). Sếp bảo *"push lên git hosting của team"*. Hoặc bạn solo dev, muốn host project portfolio.

Search Google "git hosting": GitHub, GitLab, Bitbucket, Codeberg, Gitea, Sourcehut, Gitee... **chục lựa chọn**. Mỗi blog nói khác:
- *"GitHub là default, ai cũng dùng"*
- *"GitLab tốt hơn cho enterprise"*
- *"Bitbucket free cho team < 5 người"*
- *"Codeberg cho người ghét big tech"*

→ Choice paralysis. Bài này cắt qua bằng:
1. Liệt kê **5 lựa chọn chính** + 2 niche
2. So sánh **khách quan** (giá, features, ai dùng)
3. **Recommend theo profile** cụ thể

---

## 1️⃣ Trước tiên — Git Hosting là gì?

**Git hosting** = nền tảng cloud cho phép bạn **lưu Git repo từ xa** + cung cấp **web UI + tool collab** xung quanh.

Không phải Git. Git là **tool VCS chạy local** (xem [Git lesson 00](../../01_foundations/version-control/git/lessons/01_basic/00_what-is-git.md)). Git hosting là **dịch vụ cloud** dùng Git làm backbone, thêm:

| Service | Mô tả |
|---|---|
| **Remote repo** | Lưu code trên cloud server |
| **Web UI** | Browse code, commits, history qua trình duyệt |
| **Pull Request / Merge Request** | Workflow review code trước khi merge |
| **Issue tracker** | Quản bug + feature request |
| **CI/CD** | Build/test/deploy tự động khi push |
| **Wiki + Docs** | Tài liệu project |
| **Access control** | Public/private repo + team permissions |
| **Releases + Tags** | Phát hành version |
| **Insights** | Stats commits, contributors, traffic |

🪞 **Ẩn dụ**: Git giống **máy ảnh** (chụp snapshot code). Git hosting giống **Google Photos / Flickr** — lưu cloud + share + comment + organize.

> 💡 Bạn có thể dùng Git **không cần hosting** (project local). Nhưng 95% dev dùng hosting → portfolio + collab + backup.

---

## 2️⃣ Thị trường hiện có gì (2026)?

7 lựa chọn chính, chia 3 nhóm:

### Nhóm 1: SaaS lớn (cloud, đa số dev dùng)

| Platform | Owner | Free? | Đặc trưng |
|---|---|---|---|
| **GitHub** ⭐ | Microsoft (mua 2018) | ✅ Free unlimited public+private repos | #1 thị phần, ecosystem mạnh nhất, Copilot tích hợp |
| **GitLab** | GitLab Inc. | ✅ Free tier rộng | CI/CD mạnh nhất, all-in-one DevOps, self-host được |
| **Bitbucket** | Atlassian | ✅ Free cho team ≤ 5 | Tích hợp Jira sâu, phù hợp công ty đang dùng Atlassian |

### Nhóm 2: Open source friendly (alternative)

| Platform | Owner | Free? | Đặc trưng |
|---|---|---|---|
| **Codeberg** | NPO (non-profit) | ✅ Free | Open source, ethical, không tracking, dựa trên Forgejo |
| **Gitea** | Community | ✅ Free (self-host) | Self-host trên VPS, lightweight, "GitHub-lite" |

### Nhóm 3: Niche / Regional

| Platform | Owner | Free? | Đặc trưng |
|---|---|---|---|
| **Sourcehut** | Drew DeVault | 💸 Paid ($2-10/mo) | Minimal UI, hỗ trợ mailing list workflow truyền thống |
| **Gitee** | OSChina (China) | ✅ Free | Chính của TQ, cần khi dùng cho thị trường China |

---

## 3️⃣ Bảng so sánh chi tiết 5 lựa chọn chính

| Tiêu chí | **GitHub** | **GitLab** | **Bitbucket** | **Codeberg** | **Gitea (self-host)** |
|---|---|---|---|---|---|
| **Owner** | Microsoft | GitLab Inc | Atlassian | NPO non-profit | Community (OSS) |
| **Founded** | 2008 | 2011 | 2008 | 2019 | 2016 |
| **Thị phần dev** | ⭐ ~70% | ~10% | ~6% | <1% | (self-host, không đo) |
| **Free public repo** | ✅ Unlimited | ✅ Unlimited | ✅ Unlimited (≤5 user) | ✅ Unlimited | ✅ |
| **Free private repo** | ✅ Unlimited | ✅ 5 collab/repo | ✅ 5 user team | ✅ Unlimited | ✅ |
| **Free CI/CD minutes** | 2,000/mo (private) | 400/mo (shared runner) | 50/mo (build) | (chưa có CI tự host) | Tùy server bạn |
| **PR/MR review** | ⭐ Tốt | ⭐ Tốt nhất (built-in approval rules) | ⭐ Tích hợp Jira | ✓ Cơ bản | ✓ Cơ bản |
| **CI/CD built-in** | GitHub Actions ⭐ | GitLab CI ⭐⭐ (mạnh nhất) | Bitbucket Pipelines | (qua Forgejo Actions) | Drone CI / external |
| **AI Coding** | ⭐ Copilot tích hợp | Duo AI | Atlassian Intelligence | ❌ | ❌ |
| **Issue tracker** | ✓ Tốt, có Projects (Kanban) | ⭐ Mạnh, có epic/iteration | ⭐ Jira integration deep | ✓ Cơ bản | ✓ Cơ bản |
| **Wiki / Docs** | ✓ Wiki + Pages | ✓ Wiki + Pages | ✓ Wiki | ✓ Wiki | ✓ Wiki |
| **Self-host?** | 💸 GitHub Enterprise (paid) | ✅ Community Edition free | ❌ Cloud-only | ✅ Forgejo free | ✅ Free (chính là self-host) |
| **API + CLI** | `gh` CLI ⭐⭐ | `glab` CLI | `bb` CLI (community) | (Forgejo API) | API + tea CLI |
| **Cộng đồng VN** | ⭐⭐⭐ Lớn nhất | ⭐ Trung | ⭐ Ít | (chưa có) | (chưa có) |
| **Trang chủ** | github.com | gitlab.com | bitbucket.org | codeberg.org | gitea.com / gitea.io |

> 💡 Số liệu tham khảo 2026 — có thể đổi nhẹ.

---

## 4️⃣ Khuyến nghị theo profile

### 🟢 Case 1: Beginner / Solo dev / Portfolio

→ **GitHub** (default, không cần suy nghĩ)

**Lý do**:
- Thị phần ~70% → mọi tutorial Việt + thế giới đều dùng GitHub
- Mọi recruiter expect bạn có GitHub profile làm portfolio
- Free unlimited repo (public + private)
- Tích hợp Copilot, GitHub Actions, GitHub Pages
- Cộng đồng VN lớn → dễ hỏi khi vướng

→ Cài chi tiết: [📄 github.md](./github.md) (chưa có) — account, 2FA, SSH key, PR workflow, GitHub Actions

### 🟡 Case 2: Team / Startup ≤ 5 người

→ **GitHub** (Free Team) hoặc **Bitbucket** (nếu đang dùng Jira)

**Lý do**:
- GitHub Free Team đủ cho mọi tính năng cơ bản
- Bitbucket — nếu team đang dùng Jira/Confluence, tích hợp sâu hơn nhiều

### 🟠 Case 3: Enterprise / Self-host / Compliance

→ **GitLab** (Cloud hoặc Self-Managed) hoặc **GitHub Enterprise**

**Lý do**:
- GitLab Community Edition (CE) — **free self-host**, mọi tính năng cốt lõi
- CI/CD GitLab mạnh nhất thị trường (matrix builds, complex pipelines, runner pool)
- Audit log, IAM phức tạp, SSO/SAML, complitance (SOC2, HIPAA)
- Đặc biệt phù hợp **công ty không muốn code ở cloud bên ngoài** (banking, healthcare, gov)

→ Cài chi tiết: [📄 gitlab.md](./gitlab.md) (chưa có)

### 🟣 Case 4: CI/CD heavy + DevOps focused

→ **GitLab**

**Lý do**:
- GitLab CI yaml syntax mạnh nhất + dễ đọc
- Free 400 min/tháng shared runner — đủ side project
- Self-host runner unlimited
- Auto DevOps — pipeline tự động build/test/deploy/security scan
- Container registry built-in

### 🔵 Case 5: Open source / Ethical / Privacy

→ **Codeberg** hoặc **Gitea self-host**

**Lý do**:
- Codeberg là **non-profit** — không tracking, không AI training trên code bạn
- Forgejo (engine của Codeberg) hardfork của Gitea, governance OSS
- Phù hợp project OSS không muốn dependency Microsoft/Big Tech

### ⚪ Case 6: Cần host trong nội bộ + lightweight

→ **Gitea** (self-host trên VPS bạn)

**Lý do**:
- Single binary, RAM < 100 MB
- Setup 5 phút trên VPS rẻ
- "GitHub-lite" — UI quen thuộc
- Phù hợp solo dev / homelab muốn full control

→ Cài chi tiết: [📄 gitea.md](./gitea.md) (chưa có)

### 🟤 Case 7: Mở rộng thị trường Trung Quốc

→ **Gitee** (mã nguồn tiếng Trung, server TQ — vượt firewall)

---

## 5️⃣ Vendor lock-in — Có nên lo?

Tin vui: **Git decentralized**. Bạn **không bị lock-in** với bất kỳ platform nào.

```bash
# Đang dùng GitHub, muốn chuyển GitLab?
git clone https://github.com/user/repo
git remote add gitlab git@gitlab.com:user/repo.git
git push -u gitlab --all
# DONE — toàn bộ code + history sang GitLab
```

→ **Mọi commit, branch, history** — clone đem đi. Chỉ những thứ "platform-specific" mất:
- Issues / PR comments (cần export/import tool)
- CI/CD config (mỗi platform format khác — GitHub Actions vs GitLab CI vs Bitbucket Pipelines)
- Wiki (export thủ công)
- Project settings, integrations

**Tools chuyển platform**:
- [github-to-gitlab](https://github.com/piceaTech/node-gitlab-2-github) — migration script
- GitLab có built-in Import Project từ GitHub
- Manual: `git push` repo qua + setup lại CI

---

## 6️⃣ Tích hợp AI 2026

AI coding trở thành **dealbreaker** cho nhiều team. Bảng đối chiếu:

| Platform | AI tool | Tính năng chính |
|---|---|---|
| **GitHub** | **Copilot** ⭐ ($10/mo cá nhân, $19/mo business) | Code completion, chat, PR summary, code review |
| **GitHub** | **Copilot Workspace** | Spec → PR tự động (beta) |
| **GitLab** | **GitLab Duo** ($19/mo) | Code suggestions, security explanation, root cause analysis |
| **Bitbucket** | Atlassian Intelligence | AI cho Jira tickets + Bitbucket integrated |
| **Codeberg / Gitea** | ❌ Không tích hợp | (dùng IDE AI riêng như Cursor / Continue) |

→ Nếu AI là critical: **GitHub Copilot** vẫn là gold standard. GitLab Duo đang catch up.

---

## 7️⃣ Đi vào từng tool

> 💡 Mỗi tool guide chỉ tập trung **chính nó** — không so sánh nữa (đã có ở file này).

| Tool | User guide |
|---|---|
| **GitHub** | [📄 github.md](./github.md) (chưa có) — account, 2FA, SSH, PR, Actions, Pages |
| **GitHub Desktop** | [📄 github-desktop.md](./github-desktop.md) (chưa có) — GUI cho người ghét CLI |
| **GitLab** | [📄 gitlab.md](./gitlab.md) (chưa có) — cloud + self-host |
| **Bitbucket** | [📄 bitbucket.md](./bitbucket.md) (chưa có) — Jira integration |
| **Codeberg** | [📄 codeberg.md](./codeberg.md) (chưa có) — non-profit OSS |
| **Gitea** | [📄 gitea.md](./gitea.md) (chưa có) — self-host lightweight |

---

## 8️⃣ Câu hỏi thường gặp

### "Tôi nên có account ở mọi platform không?"

🟡 **Có 2 tài khoản phổ biến**:
1. **GitHub** — bắt buộc (portfolio + đa số OSS ở đó)
2. **GitLab** hoặc **Bitbucket** — tùy team đang dùng

→ Không cần 5 account. 2 là đủ 95% nhu cầu.

### "GitHub Free đủ cho team thực không?"

✅ **Có cho team nhỏ**. GitHub Free Team (2020+) cho:
- Unlimited private repo
- Unlimited collaborators
- 2,000 GitHub Actions minutes/tháng
- Branch protection, code review

Khi cần: SAML SSO, audit log, advanced security → mới phải upgrade Team ($4/user/mo) hoặc Enterprise.

### "Migrate từ GitHub sang GitLab có dễ không?"

✅ **Dễ vì Git decentralized**. GitLab có wizard Import Project từ GitHub — kéo cả code + issues + PR + wiki sang trong 10 phút.

CI/CD thì phải viết lại (GitHub Actions yaml != GitLab CI yaml). 1-2 ngày work cho project trung bình.

### "Codeberg / Gitea có ổn không?"

🟡 **Ổn cho cá nhân / small team**, **không phù hợp** enterprise (thiếu compliance, audit log mạnh).

Codeberg: non-profit, free, ethical. Nhưng community nhỏ, ít integration.
Gitea: self-host trên VPS bạn — control 100%, nhưng tự bảo trì security + backup.

### "Mã đang public sẽ bị steal hoặc dùng để train AI không?"

Cần đọc Terms of Service:
- **GitHub**: training Copilot trên **public code có license cho phép** (CC-BY-SA, MIT, ...). Public repo của bạn có thể bị dùng nếu license permissive.
- **GitLab**: ToS hiện không train AI trên user code (2026).
- **Codeberg**: KHÔNG train, no tracking.

→ Nếu muốn opt-out: GitHub có setting "Block AI training" (Settings → Copilot).

---

## 🔗 Liên kết

### Trong kho

- 🎓 [Git là gì](../../01_foundations/version-control/git/lessons/01_basic/00_what-is-git.md) — Git concept (đọc trước)
- 🎓 [Git Remote + GitHub](../../01_foundations/version-control/git/lessons/01_basic/03_remote-and-github.md) — bài lesson đồng nghiệp join project
- 🧭 [Zero to Coder Roadmap](../../00_roadmaps/career/zero-to-coder_career-roadmap.md) — Stage 1 cài git + tạo GitHub account
- 🛠️ [02_tools README](../README.md) — danh sách tool category khác

### Tài nguyên ngoài

- [GitHub Docs](https://docs.github.com/) — chính thức, đầy đủ nhất
- [GitLab Docs](https://docs.gitlab.com/) — chính thức
- [Bitbucket Docs](https://support.atlassian.com/bitbucket-cloud/) — chính thức
- [Codeberg Documentation](https://docs.codeberg.org/) — chính thức
- [Gitea Documentation](https://docs.gitea.com/) — chính thức
- [Octoverse Report](https://octoverse.github.com/) — GitHub thống kê hàng năm
- [Awesome Self-Hosted](https://awesome-selfhosted.net/tags/git-hosting.html) — list các tool git hosting self-host

---

## 📌 Changelog

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Tool category git-clients hoàn chỉnh. Cover: 7 platform (GitHub/GitLab/Bitbucket/Codeberg/Gitea/Sourcehut/Gitee) + bảng so sánh 14 tiêu chí 5 chính + 7 case khuyến nghị + vendor lock-in section + AI integration 2026 + 5 FAQ + link sang 6 file tool individual sẽ viết.
