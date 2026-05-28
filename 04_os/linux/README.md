# 🐧 Linux — Operating System

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026

> 🎯 *Linux là hệ điều hành **mã nguồn mở phổ biến nhất** — chạy 90%+ server trên thế giới, 100% supercomputer, là nền của Docker/K8s, Android, ChromeOS. Coder nào cũng cần biết cơ bản.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:

- [ ] Hiểu kiến trúc Linux (kernel, shell, user space)
- [ ] Thành thạo lệnh dòng lệnh: navigation, file ops, text processing
- [ ] Hiểu permissions, processes, networking cơ bản
- [ ] Tự setup 1 Linux server từ scratch
- [ ] Debug được lỗi thường gặp (disk full, high CPU, ...)

---

## 📂 Cấu trúc

### lessons/01_basic/ — Lệnh Linux cơ bản

| # | Bài | Trạng thái | Note |
|---|---|---|---|
| 00 | What is Linux | ❌ | Intro: Linux là gì, distro, kernel/shell/userland |
| 01 | [Linux Navigation](./lessons/01_basic/01_navigation.md) | ✅ 🌟 | `pwd`, `ls`, `cd`, paths |
| 02 | [Linux File Operations](./lessons/01_basic/02_file-operations.md) | ✅ 🌟 | `mkdir`, `touch`, `cp`, `mv`, `rm` |
| 03 | [Linux View File Content](./lessons/01_basic/03_view-file-content.md) | ✅ 🌟 | `cat`, `less`, `head`, `tail` |
| 04 | Text search & pipes | ❌ | `grep`, `find`, `awk`, `\|`, `>` |
| 05 | Process management | ❌ | `ps`, `kill`, `top`, `htop` |
| 06 | File permissions | ❌ | `chmod`, `chown`, umask, sticky bit |
| 07 | Users & groups | ❌ | `useradd`, `groupadd`, `/etc/passwd` |
| 08 | Package management | ❌ | `apt`, `yum`, `dnf`, `pacman` |

### lessons/02_intermediate/, 03_advanced/

❌ Chưa có (dự kiến: systemd, cron, networking, SELinux, kernel modules, performance tuning)

### setup/ — Cài Linux

❌ Chưa có (dự kiến: Ubuntu install, dual-boot, WSL setup, choose distro)

### recipes/ — Troubleshooting + Patterns

❌ Chưa có (dự kiến: disk-full, high-cpu, network-down, SSH connection issues)

---

## ⚖️ Lệnh Linux vs Shell Features

Phân biệt quan trọng (theo Blueprint v0.5 §3.2ter):

| Loại | Vị trí | Ví dụ |
|---|---|---|
| **Lệnh OS** (POSIX commands) | 🔵 **Folder này** (`04_os/linux/`) | `pwd`, `ls`, `cd`, `grep`, `chmod` |
| **Shell features** (bash/zsh) | `02_tools/shell/` | Aliases, prompt, scripting, oh-my-zsh |
| **Terminal apps** | `02_tools/shell/setup/` | iTerm2, Warp, Windows Terminal |

→ Vì lệnh Linux dùng được cả trên **Mac** (BSD Unix), **WSL** trên Windows, **Git Bash** — không bó hẹp Linux.

---

## 🚀 Lộ trình đề xuất

| Bạn là... | Đọc gì |
|---|---|
| 🟢 Beginner zero-base | Bắt đầu [01_navigation.md](./lessons/01_basic/01_navigation.md) → 02, 03 lần lượt |
| 🟡 Đã biết cơ bản | Skip basic, vào 04 (text search) + 06 (permissions) khi có |
| 🧭 Theo Zero-to-Coder Stage 1 | Đọc 4 bài: 01_navigation, 02_file-operations, 03_view-content + (sẽ có) 04_text-search |

---

## 📌 Changelog

- **v0.1.0 (16/05/2026)** — Skeleton. 3 bài basic ✅ (move từ `02_tools/shell/lessons/` theo Blueprint v0.5 §3.2ter).
