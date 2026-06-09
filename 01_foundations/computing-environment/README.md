# 💻 Computing Environment — Terminal, Shell, OS interaction

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0 — **Cluster basic HOÀN CHỈNH 6/6** ✅\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 23/05/2026\
> **Status:** ✅ 6/6 bài basic — Terminal + Shell + Filesystem + Process + Env Vars + I/O Redirect

> 🎯 *Folder này dạy **khái niệm tính toán nền tảng** liên quan đến terminal, shell, file system, process — **agnostic OS** (không phụ thuộc Mac/Linux/Windows cụ thể). Lệnh OS-specific (vd `pwd` Linux) thuộc `04_os/linux/`. Tool guide cho terminal emulator (vd iTerm) thuộc `02_tools/terminal-emulators/`.*

---

## ⚖️ Scope — Phân biệt rõ với folder khác

| ✅ Ở đây CÓ | ❌ Ở folder khác |
|---|---|
| **Terminal/Shell concept** — terminal là gì, shell vs terminal vs command | Lệnh `pwd`, `ls`, `cd` → [`04_os/linux/`](../../04_os/linux/) |
| **Filesystem concept** — root, paths, working directory | Lệnh `mkdir`, `cp`, `mv` → [`04_os/linux/`](../../04_os/linux/) |
| **Process concept** — process là gì, PID, signal | Lệnh `ps`, `kill` → [`04_os/linux/`](../../04_os/linux/) |
| **Environment variables concept** — env var là gì, scope | Lệnh `export`, `setenv` → [`04_os/`](../../04_os/) tương ứng |
| **I/O Redirection concept** — stdin/stdout/stderr, pipe | Cú pháp shell cụ thể → [`02_tools/shell/`](../../02_tools/shell/) |
| Cài iTerm/Kitty/Alacritty cụ thể | (đi tool guide) → [`02_tools/terminal-emulators/`](../../02_tools/terminal-emulators/) |
| Customize zsh/bash/fish (aliases, prompt) | (đi tool guide) → [`02_tools/shell/`](../../02_tools/shell/) |

> 💡 Quy tắc: **Concept ở đây (Foundations), lệnh ở OS, tool ở Tools.**

---

## 📂 Cấu trúc + Status

### lessons/01_basic/

| # | Bài | Status |
|---|---|---|
| 00 | [What is Terminal](./lessons/01_basic/00_what-is-terminal.md) | ✅ 🌟 — Intro terminal/shell/command, 3 OS, prompt structure |
| 01 | [What is a Shell (bash/zsh/fish)](./lessons/01_basic/01_what-is-shell.md) | ✅ 🌟 — Phân biệt 3 lớp Terminal/Shell/Command + so sánh bash/zsh/fish + config file |
| 02 | [Filesystem concept (paths, root, working dir)](./lessons/01_basic/02_filesystem-concept.md) | ✅ 🌟 — `/`, `~`, `.`, `..`, hidden files, permissions, symlink |
| 03 | [Process & PID concept](./lessons/01_basic/03_process-and-pid.md) | ✅ 🌟 — Program vs Process, PID tree, 4 trạng thái + Zombie, signal SIGTERM/SIGKILL, fg/bg |
| 04 | [Environment variables](./lessons/01_basic/04_env-variables.md) | ✅ 🌟 — Env var, $PATH, 3 scope, inheritance, `.env`/`.env.example`, secrets vs config, vault tools, Docker context |
| 05 | [I/O Redirection](./lessons/01_basic/05_io-redirection.md) | ✅ 🌟 🆕 — 3 streams (stdin/stdout/stderr), `>`/`>>`/`2>&1`/`&>`, pipe `\|`, `/dev/null`, `tee` |

### lessons/02_intermediate/, 03_advanced/

❌ Chưa có (dự kiến: signal/job control concept, shell as Turing-complete language, ...)

### exercises/, recipes/

❌ Chưa có

---

## 🚀 Lộ trình đề xuất

| Nhu cầu | Đọc gì |
|---|---|
| **Chưa từng mở terminal** | [00_what-is-terminal](./lessons/01_basic/00_what-is-terminal.md) → rồi [`04_os/linux/lessons/01_basic/`](../../04_os/linux/lessons/01_basic/) học lệnh thật |
| **Đã dùng terminal nhưng lẫn lộn terminal / shell / command** | [00_what-is-terminal](./lessons/01_basic/00_what-is-terminal.md) (phân biệt 3 lớp) |
| **Theo Zero-to-Coder roadmap** | Stage 1 link tới 00_what-is-terminal |

---

## 🔗 Liên kết & Tài nguyên

| Nhu cầu | Đi đâu |
|---|---|
| Học lệnh Linux thật (`pwd`, `ls`, `cd`, ...) | [`04_os/linux/lessons/01_basic/`](../../04_os/linux/lessons/01_basic/) |
| Cài terminal đẹp (iTerm/Kitty/Warp) | [`02_tools/terminal-emulators/`](../../02_tools/terminal-emulators/) (chưa có) |
| Customize zsh/bash (alias, prompt) | [`02_tools/shell/`](../../02_tools/shell/) (chưa có content) |
| PowerShell / CMD (Windows) | [`04_os/windows/`](../../04_os/windows/) (chưa có) |

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Bản khởi tạo.
- **v0.2.0 (21/05/2026)** — Có bài đầu tiên `00_what-is-terminal.md`. Viết lại README cho rõ phạm vi (concept nền tảng, không phải tool guide hay lệnh OS) + danh sách 6 lesson dự kiến + bảng phân biệt với `02_tools`/`04_os`.
- **v0.3.0 (23/05/2026)** — Thêm bài thứ 2: `01_what-is-shell.md` — Phân biệt Terminal/Shell/Command 3 lớp + so sánh bash/zsh/fish + config file `.bashrc`/`.zshrc`. Cluster basic giờ có 2/6 bài.
- **v0.4.0 (23/05/2026)** — Thêm bài thứ 3: `02_filesystem-concept.md` — Filesystem 3 OS + absolute/relative path + 5 ký hiệu (`/` `~` `.` `..` `-`) + Working Directory + hidden files + permissions `rwxr-xr-x` + symlink. Cluster basic 3/6 bài.
- **v0.5.0 (23/05/2026)** — Thêm bài thứ 4: `03_process-and-pid.md` — Program vs Process + PID tree với mermaid + PID 1 (systemd/launchd/Docker) + 4 trạng thái + Zombie + signal (SIGTERM vs SIGKILL) + fg/bg + nohup/disown + Docker context. Cluster basic 4/6 bài.
- **v0.6.0 (23/05/2026)** — Thêm bài thứ 5: `04_env-variables.md` — Env var concept + $PATH với mermaid lookup + 3 scope + inheritance parent-child + `.env` pattern + secrets vs config + vault tools (HashiCorp/AWS Secrets Manager/...) + Docker env 3 cách. Cluster basic 5/6 bài.
- **v1.0.0 (23/05/2026)** — 🎉 **CLUSTER BASIC HOÀN CHỈNH 6/6**. Thêm bài cuối: `05_io-redirection.md` — 3 streams (stdin/stdout/stderr) + redirect `>`/`>>`/`2>&1`/`&>` + pipe `|` + `/dev/null` + `tee`. Beginner giờ có **toàn bộ kiến thức computing environment OS-agnostic** để hiểu shell sâu.
