# 🛠️ git-clients — Git hosting platforms

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0 — **Cluster HOÀN CHỈNH 7/7** ✅\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 23/05/2026\
> **Status:** ✅ 7/7 bài — 1 category + 6 tool individual

> 🎯 *Tool category cho **git hosting platforms** — nơi bạn host repo cloud + collab. Đọc category trước để chọn, rồi đi vào tool guide cụ thể.*

---

## 📂 Cấu trúc

| File | Vai trò | Status |
|---|---|---|
| [`00_what-is-git-hosting.md`](./00_what-is-git-hosting.md) | **Category overview** — so sánh 7 platform + recommend theo profile | ✅ |
| [`github.md`](./github.md) | GitHub user guide (account, 2FA, SSH, PR, Actions, Pages, CLI, security) | ✅ |
| [`github-desktop.md`](./github-desktop.md) | GUI client chính thức của GitHub | ✅ 🆕 |
| [`gitlab.md`](./gitlab.md) | GitLab cloud + self-host CE + CI/CD + Auto DevOps | ✅ 🆕 |
| [`bitbucket.md`](./bitbucket.md) | Atlassian ecosystem — Smart Commits + Jira integration | ✅ 🆕 |
| [`codeberg.md`](./codeberg.md) | Non-profit, ethical, Forgejo-based | ✅ 🆕 |
| [`gitea.md`](./gitea.md) | Self-host lightweight (Docker/binary, <100MB RAM) | ✅ 🆕 |

---

## 🚀 Khi nào đọc folder này

| Bạn là... | Đọc gì |
|---|---|
| 🟢 **Beginner chưa biết platform nào** | [`00_what-is-git-hosting.md`](./00_what-is-git-hosting.md) trước |
| 🟡 **Đã quyết GitHub** | `github.md` (chưa có) |
| 🟠 **Cần self-host** | `gitea.md` hoặc `gitlab.md` (chưa có) |
| 🧭 **Theo Zero-to-Coder Stage 1** | `github.md` — cài account + SSH + push lần đầu |

---

## ⚖️ Phân biệt với chỗ khác

| ✅ Ở đây CÓ | ❌ Ở folder khác |
|---|---|
| User guide **GitHub UI**, **GitLab UI** | Git CLI lệnh (`git push`, `git pull`) → [`01_foundations/version-control/git/`](../../01_foundations/version-control/git/) |
| So sánh platforms + chọn cái nào | Concept Version Control (commit, branch, merge) → [Foundations](../../01_foundations/version-control/git/lessons/01_basic/00_what-is-git.md) |
| Setup 2FA, SSH key, PAT từng platform | GitHub Desktop GUI → file riêng `github-desktop.md` |

---

## 📌 Changelog

- **v1.0.0 (23/05/2026)** — 🎉 **CLUSTER HOÀN CHỈNH 7/7**. Thêm 5 file tool individual còn lại:
  - `github-desktop.md` — GUI client GitHub (~400 dòng): đồng nghiệp sợ CLI, 5-phần UI, workflow clone/commit/PR, vs VS Code Source Control
  - `gitlab.md` — GitLab cloud + self-host (~600 dòng): bạn join fintech, MR vs PR, GitLab CI/Auto DevOps, CE self-host, `glab` CLI
  - `bitbucket.md` — Atlassian (~500 dòng): Smart Commits, Jira integration native, workspace 3-tier, Pipelines yếu nhất
  - `codeberg.md` — Non-profit (~450 dòng): Maria ethical dev, Codeberg vs Forgejo vs Gitea, migrate từ GitHub
  - `gitea.md` — Self-host lightweight (~500 dòng): homelab K8s lab, Docker setup 5 phút, vs GitLab CE 100MB vs 8GB
- **v0.3.0 (23/05/2026)** — Thêm `github.md` ✅ (~720 dòng): full user guide GitHub (account + 2FA + SSH/PAT/gh auth + repo + UI tour 8 tab + PR workflow bạn+đồng nghiệp + Actions CI/CD + Pages portfolio + gh CLI + security 7 must-do + settings nâng cao). Tool individual đầu tiên hoàn chỉnh.
- **v0.2.0 (23/05/2026)** — Tool category đầu tiên hoàn chỉnh. Thêm `00_what-is-git-hosting.md` — so sánh 7 platform (GitHub/GitLab/Bitbucket/Codeberg/Gitea/Sourcehut/Gitee) + bảng 14 tiêu chí + 7 case khuyến nghị + vendor lock-in + AI integration 2026.
- **v0.1.0 (20/05/2026)** — Skeleton.
