# 🐚 Shell — Tool / Customize / Scripting

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.4.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 21/05/2026

> 🎯 *Folder này tập trung vào **shell as a tool** — cài terminal apps, chọn shell (bash/zsh/fish), customize (aliases, prompt, themes), shell scripting. **KHÔNG** dạy lệnh Linux (pwd/ls/cd/...) — đó thuộc [`04_OS/linux/`](../../04_OS/linux/).*

---

## ⚖️ Scope (theo Blueprint v0.5 §3.2ter)

| ✅ Ở đây CÓ | ❌ Ở đây KHÔNG có |
|---|---|
| Cài terminal apps (iTerm2, Warp, Windows Terminal) | Lệnh `pwd`, `ls`, `cd` — xem [04_OS/linux/](../../04_OS/linux/) |
| Cài + customize shell (zsh, oh-my-zsh, p10k) | Lệnh `mkdir`, `cp`, `mv`, `rm` — xem [04_OS/linux/](../../04_OS/linux/) |
| Aliases, prompt PS1, history config | Lệnh `grep`, `find`, `chmod` — xem [04_OS/linux/](../../04_OS/linux/) |
| Shell scripting (bash syntax: `if`, `for`, function) | Khái niệm filesystem (inode, mount) — xem 04_OS/ |
| So sánh bash vs zsh vs fish | |

> 💡 *Nguyên tắc vàng: "Ở 02_Tools là những cái chỗ khác không có"*. Lệnh OS thuộc `04_OS/linux/`, không lặp ở đây.

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:

- [ ] Cài + cấu hình terminal app đẹp + zsh + oh-my-zsh
- [ ] Tạo aliases riêng giúp tăng năng suất
- [ ] Customize prompt PS1, thêm git branch info
- [ ] Viết shell script đơn giản tự động hóa task hàng ngày
- [ ] Chọn được shell phù hợp (bash vs zsh vs fish)

---

## 📂 Cấu trúc

### setup/ — Cài đặt terminal + shell

| File | Trạng thái |
|---|---|
| ❌ `terminal-apps.md` | iTerm2 (Mac), Warp, Windows Terminal — so sánh + cài |
| ❌ `zsh-and-oh-my-zsh.md` | Cài zsh + Oh My Zsh |
| ❌ `powerlevel10k.md` | Theme prompt đẹp + git info |
| ❌ `wsl-setup.md` | Windows Subsystem for Linux |

### lessons/01_basic/ — Shell-as-tool features

| # | Bài | Trạng thái | Note |
|---|---|---|---|
| ~~00~~ | ~~What is Terminal~~ | 🔄 **MOVED** | Đã chuyển → [`01_Foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md`](../../01_Foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md) (terminal là concept Foundations) |
| 01 | Choosing a shell (bash/zsh/fish) | ❌ | Tool comparison |
| 02 | Aliases | ❌ | Shell feature |
| 03 | Prompt customization (PS1) | ❌ | Shell feature |
| 04 | History & completion | ❌ | Shell feature |
| 05 | Shell scripting intro | ❌ | Variables, control flow trong shell |

### lessons/02_intermediate/

❌ Chưa có (dự kiến: advanced scripting, functions, process substitution, job control)

### lessons/03_advanced/

❌ Chưa có (dự kiến: zsh deep features, oh-my-zsh plugin dev, performance tuning)

---

## 🔀 Liên kết quan trọng

| Nhu cầu | Đi đâu |
|---|---|
| Học lệnh Linux (`pwd`, `ls`, `cd`, ...) | [`04_OS/linux/lessons/01_basic/`](../../04_OS/linux/lessons/01_basic/) |
| Học PowerShell (Windows native) | (chưa có) `04_OS/windows/lessons/` |
| Hiểu khái niệm filesystem | (chưa có) `04_OS/linux/_concepts/filesystem.md` |
| Setup chi tiết tool terminal | `setup/` trong folder này (sắp có) |

---

## 🤝 Muốn viết bài cho chủ đề này?

1. **Xác nhận scope**: bài có thuộc shell-as-tool? Nếu thuộc Linux/OS → đặt vào `04_OS/linux/`
2. Đọc [`../../_Blueprint/00_blueprint-overview.md`](../../_Blueprint/00_blueprint-overview.md)
3. Copy template phù hợp:
   - Setup → `setup_template.md`
   - Lesson tool feature → `lesson_template.md`
4. Soát checklist
5. Cập nhật `MASTER-CATALOG.md`

---

## 📌 Changelog

- **v0.4.0 (21/05/2026)** — **Move `00_what-is-terminal.md`** sang `01_Foundations/computing-environment/lessons/01_basic/`. Lý do: terminal/shell là concept tính toán nền tảng → thuộc Foundations. Folder này giờ chỉ còn shell-as-tool features (zsh customize, scripting, aliases) — chưa có content. Tool guide từng terminal emulator (iTerm/Kitty/Alacritty/Warp) sẽ ở `02_Tools/terminal-emulators/`.
- **v0.3.0 (16/05/2026)** — Refactor scope theo Blueprint v0.5 §3.2ter: move 3 lessons (navigation, file-operations, view-content) sang `04_OS/linux/` (vì là lệnh POSIX, không phải shell-tool features). Reframe folder này focus shell-as-tool: terminal apps, customize, scripting.
- **v0.2.0 (16/05/2026)** — Refactor `00_terminal-fundamentals.md` thành 4 bài.
- **v0.1.0 (16/05/2026)** — Skeleton + bài terminal đầu tiên.
