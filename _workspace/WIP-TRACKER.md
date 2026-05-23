# 🚧 Work-In-Progress Tracker

> **Tác giả:** Mr.Rom (+ Claude maintain)\
> **Phiên bản:** v0.5.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 23/05/2026

> 🎯 *Lịch sử các việc đang dở, chưa xong, hoặc đang chờ làm rõ — để khi user/Claude switch task vẫn nhớ quay lại.*

---

## 📌 Cách dùng file này

| Khi nào | Hành động |
|---|---|
| Bắt đầu task mới | Thêm vào `🔥 Đang làm` (hoặc `📋 Backlog` nếu chưa làm ngay) |
| Pause giữa chừng (chuyển task khác) | Cập nhật "next step" + để ở `🔥 Đang làm` |
| Bị block (chờ user quyết) | Move sang `🚨 Blocked` với lý do |
| Xong hoàn toàn | Move sang `✅ Done gần đây`, để lại 3-7 ngày rồi xoá |
| Bỏ luôn | Xoá hẳn + ghi note vào changelog |

**Quy ước item entry:**
```
- [ ] <Title>
  - 📅 Started: YYYY-MM-DD
  - 📍 Last update: YYYY-MM-DD
  - 🎯 Next step: <cụ thể bước tiếp theo>
  - 🚨 Blocker (nếu có): <cần gì để unblock>
  - 📁 Files đang đụng: <list>
```

---

## 🔥 Đang làm (current)

_(none — Docker refactor vừa xong, chuyển sang ✅ Done)_

---

## 📋 Backlog (planned, chưa làm)



### Lesson series tiếp theo (sau Docker)
- 📅 Added: 20/05/2026
- 💡 Candidates (priority cao):
  - HTTP/networking basics (`05_Networking/http-https/`) — referenced bởi nhiều career roadmap
  - SQL fundamentals (`06_Databases/sql-fundamentals/`) — backend/data engineer roadmap link
  - Postgres (`06_Databases/postgresql/`) — backend-dev Stage 3 link
  - FastAPI (`07_Web/backend/python-fastapi/`) — backend roadmap
  - K8s basic lessons (`10_DevOps/kubernetes/`) — devops/sre/platform roadmap
- 🎯 Cần user pick priority sau khi Docker done

### Phase 3: Lab Series
- 📅 Added: 20/05/2026
- 🎯 Khi làm: viết 4 lab series ở `00_Roadmaps/lab-series/`:
  - `docker-to-k8s_lab-series.md` (50 bài)
  - `full-stack-web-app_lab-series.md`
  - `home-lab-self-hosted_lab-series.md`
  - `python-zero-to-production_lab-series.md`
- ⏳ Dependency: cần Phase 2 lessons xong trước (đặc biệt Docker + K8s + FastAPI + React)

### __Ref__ improvements candidates (cherry-pick khi rảnh)
- 📅 Added: 21/05/2026
- 💡 Content có sẵn trong `__Ref__/` có thể nâng:
  - **Python** (`03_Languages/python/__Ref__/python_from_05Languages/`): có `01-python-basics`, `02-python-advanced`, `03-packaging-setup`, `04-testing-practices`, `05-performance-practices`, `06-cheatsheet`
    - → Cherry-pick cho lessons mới: `04_io-and-files`, `05_modules-and-packages`, `06_error-handling` + tạo `99_cheatsheet.md`
  - **Linux** (`04_OS/linux/__Ref__/linux/`): có `01-essentials-basics`, `02-administration-advanced`, `03-networking-advanced`
    - → Cherry-pick cho `lessons/02_intermediate/` (systemd, ssh, networking)
  - **Docker** (`10_DevOps/docker/__Ref__/`): có `_Draft_Syntax.md`, `from_06_DevOps_docker/_quizzes/`, `_projects/simple-webapp-dockerized`
    - → Cherry-pick cho `exercises/` (quiz), `projects/` (webapp), `99_cheatsheet.md`
  - **Shell/terminal** (`02_Tools/terminal-emulators/__Ref__/`): có `02-bash-scripting-basics`, `04-vim-neovim-basics`, `03-shell-tools-cheatsheet`
    - → Cherry-pick cho `02_Tools/shell/lessons/01_basic/` lessons mới (bash scripting, vim intro)
  - **Git** (`01_Foundations/version-control/__Ref__/git_*`): đã có nội dung tham khảo — git bộ đã viết v2.0.0, có thể bổ sung lesson `05_rebase-cherrypick` nếu cần
- 🎯 KHÔNG ưu tiên — Phase 2 chính trước. Note để khỏi quên.

---

## ✅ Done gần đây (3-7 ngày)

### 23/05/2026

- ✅ **🎉 git-clients CLUSTER HOÀN CHỈNH 7/7** — Thêm 5 file: github-desktop (~400), gitlab (~600), bitbucket (~500), codeberg (~450), gitea (~500). Tool category đầu tiên của `02_Tools/` đóng đủ pattern (category + 6 individual). README v1.0.0 + MASTER-CATALOG v1.14.0. Tổng bài 48 → 53.
- ✅ **GitHub user guide** — `github.md` (~720 dòng): account+2FA, SSH/PAT/gh auth, repo+UI tour, PR Long+Mai, Actions, Pages, gh CLI, security. Unblock 3 "(chưa có)" link → ✅. README v0.3.0 + MASTER-CATALOG v1.13.0. Tổng bài 47 → 48.
- ✅ **Tool category git-clients mở** — `00_what-is-git-hosting.md` (~520 dòng): so sánh 7 platform, 7 case khuyến nghị, vendor lock-in, AI 2026. README v0.2.0 + MASTER-CATALOG v1.12.0.
- ✅ **🎉 Computing-environment CLUSTER BASIC HOÀN CHỈNH 6/6** — Thêm `05_io-redirection.md` (~520 dòng): 3 streams + redirect + pipe + /dev/null + tee + 3 ví dụ kết hợp. README v1.0.0 + MASTER-CATALOG v1.11.0. Cluster đầu tiên của Foundations đóng hoàn chỉnh.
- ✅ **Computing-environment 04_env-variables** (~470 dòng): env var + $PATH + 3 scope + inheritance + `.env`/`.env.example` + secrets vs config + vault tools + Docker env. README v0.6.0 + MASTER-CATALOG v1.10.0. Cluster basic 5/6.
- ✅ **Computing-environment 03_process-and-pid** (~470 dòng): Program vs Process, PID tree, PID 1 (systemd/launchd/Docker), 4 trạng thái + Zombie, signal SIGTERM/SIGKILL, fg/bg/nohup/disown, Docker context. README v0.5.0 + MASTER-CATALOG v1.9.0. Cluster basic 4/6.
- ✅ **Computing-environment 02_filesystem-concept** (~420 dòng): filesystem 3 OS, absolute/relative path, 5 ký hiệu, CWD, hidden files, permissions, symlink. README v0.4.0 + MASTER-CATALOG v1.8.0. Cluster basic 3/6.
- ✅ **Computing-environment buildout** — viết `01_what-is-shell.md` (~350 dòng): phân biệt 3 lớp Terminal/Shell/Command + so sánh bash/zsh/fish (10 tiêu chí) + cách check shell + đổi shell + intro `.bashrc`/`.zshrc`. Mở bằng tình huống tutorial nói "thêm vào ~/.bashrc". Update README v0.3.0 + MASTER-CATALOG v1.7.0. Cluster basic computing-environment giờ 2/6 bài.

### 21/05/2026

- ✅ **Move terminal intro** `02_Tools/shell/lessons/01_basic/00_what-is-terminal.md` → `01_Foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md` (v2.0.0 → v2.1.0). Sweep 6 external + 2 internal refs. Update shell README (v0.4.0) + computing-environment README (v0.2.0) + MASTER-CATALOG (v1.6.0).
- ✅ **Python 4 lessons refactor v2.0.0** — `00_what-is-python` (tình huống cài Python, mở terminal không biết gõ gì), `01_variables-and-types` (viết script tính lương, TypeError vì chưa biết types), `02_control-flow` (tax theo bậc + lặp 30 nhân viên), `03_functions` (lặp 180 chỗ vì chưa biết function). Headers câu hỏi tự nhiên. Content kỹ thuật KHÔNG đổi.
- ✅ **Linux 3 lessons refactor v2.0.0** — `01_navigation` (terminal mở lần đầu, 3 câu hỏi), `02_file-operations` (tạo cấu trúc project + cảnh báo rm), `03_view-file-content` (debug log production 50,000 dòng). Style v0.5.1.
- ✅ **Shell intro refactor v2.0.0** — Tutorial bảo "mở terminal" mà beginner không biết. Style v0.5.1.
- ✅ **Fix 3 stale § refs** trong Docker `02_dockerfile-basics.md` (§6 → §5, §5 → §4 sau renumber).

### 20/05/2026

- ✅ **Docker bộ refactor v2.0.0** — 4 lesson files (intro + 01 images + 02 dockerfile + 03 compose) áp Long story arc tiếp git: Long ship project → Mai pull về máy gặp "works on my machine" → discover Docker → 8 lệnh CRUD → Dockerfile build myapp → Compose ghép 4 service. Headers đổi sang câu hỏi tự nhiên (writing-style v0.5.1). KHÔNG đổi content kỹ thuật.
- ✅ **WIP-TRACKER + memory** — tạo `_workspace/WIP-TRACKER.md` + 3 memory (expert collab, __Ref__ intentional, WIP tracker auto-load)
- ✅ **Folder skeleton đầy đủ** — 146 L2 + 15 L3 web + 264 README placeholder + 608 .gitkeep theo Blueprint sitemap
- ✅ **Fix broken anchor** — `#stage-1--tools-cơ-bản` → `#stage-1--tools-tối-thiểu` ở 8 file
- ✅ **Tool category đầu tiên** — `02_Tools/ide/` với `00_what-is-ide.md` + `vs-code.md` v2.0.0 (move từ `editor/setup/`)
- ✅ **MASTER-CATALOG** v1.1.0 → v1.2.0 → v1.3.0

### 19/05/2026

- ✅ **Move git folder** từ `02_Tools/git/` → `01_Foundations/version-control/git/`
- ✅ **Git lessons refactor v2.0.0** — 5 bài (intro + 01-04) với "Long story arc" narrative
- ✅ **zero-to-coder v2.0.0** — thêm Stage 0 (bản đồ ngành) + Stage 2 đổi sang "Chọn 1 ngôn ngữ"
- ✅ **industry-landscape lesson** — NEW (~470 dòng) cho Stage 0
- ✅ **Writing style v0.5.1** — WHY/WHAT/HOW từ "tiêu đề bắt buộc" → "tiêu chí đánh giá"
- ✅ **Blueprint cleanup** — sync MASTER-CATALOG, 01_Foundations README, version-control git README

---

## 🚨 Blocked / Cần user quyết định

### Tool category priority sau ide/
- ⚠️ Đã đề xuất 4 candidate (`git-clients/`, `terminal-emulators/`, `k8s-local/`, `docker-tools/`) — chưa pick
- 🎯 Decision needed: làm cái nào trước theo nhu cầu thực tế

### Lesson series tiếp theo (sau Docker)
- ⚠️ Đã list 5 candidate (HTTP, SQL, Postgres, FastAPI, K8s) trong Backlog — chưa pick priority
- 🎯 Decision needed: chọn 1 để làm tiếp Phase 2

---

## 📌 Changelog

- **v0.4.0 (23/05/2026)** — Computing-environment buildout: thêm `01_what-is-shell.md` (cluster basic 2/6 bài).
- **v0.3.0 (21/05/2026)** — Move terminal intro xong (02_Tools/shell → 01_Foundations/computing-environment), Backlog "Move terminal" → Done.
- **v0.2.0 (21/05/2026)** — Audit + refactor cycle:
  - ✅ Done 8 lesson refactor v2.0.0 (Python 4 + Linux 3 + Shell intro 1)
  - ✅ Fix 3 stale § refs trong Docker file 02
  - ➕ Add **__Ref__ improvements** backlog (Python/Linux/Docker/Shell content có sẵn để cherry-pick)
- **v0.1.0 (20/05/2026)** — Bản đầu tiên. Pre-seed với 1 đang làm + 4 backlog + 11 done (3 ngày 18-20/05) + 2 blocked.
