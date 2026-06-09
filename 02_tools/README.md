# 🛠️ 02_tools

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.6.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 20/05/2026

> 🚀 **Status:** 3 tool category đã có bài: [`git/`](./git/) (đầy đủ Basic→Advanced + bài tập), [`git-clients/`](./git-clients/) (7/7 bài), [`ide/`](./ide/) (category overview + VS Code). Các L2 khác còn skeleton.

## 🎯 Chủ đề này có gì

Git, Shell, Editor, terminal tools, package managers, productivity — bộ công cụ coder dùng hàng ngày.

### ⭐ Vai trò đặc biệt — Central Setup Hub

`02_tools/` không chỉ là chủ đề học **dùng** tool, mà còn là **NƠI CANONICAL** cho mọi hướng dẫn **cài đặt + cấu hình chi tiết** của các tool cross-cutting (dùng cho nhiều L1):

- **Setup chi tiết tối đa**: multi-option install, troubleshooting, extension recommendations, comparison với alternative
- **Lessons ở L1 khác** chỉ giới thiệu sơ bộ rồi link về `02_tools/<l2>/setup/<tool>.md`
- **Tránh** lặp install instructions ở mọi bài cần tool đó (DRY)

→ Khi viết bài lesson cần tool, nếu tool **cross-cutting** (>1 L1 dùng) → setup chi tiết đặt ở `02_tools/`. Tool **specific** 1 L1 → setup trong L1 đó.

## 📂 L2 chủ đề con

| L2 | Trạng thái | Note |
|---|---|---|
| [`git/`](./git/) | ✅ Đầy đủ | Bộ Git từ Basic → Advanced: setup + 8 lesson + 7 bài tập (quiz/lab) |
| [`git-clients/`](./git-clients/) | ✅ 7/7 bài | Category `00_what-is-git-hosting.md` + GitHub/GitHub Desktop/GitLab/Bitbucket/Codeberg/Gitea |
| [`ide/`](./ide/) | ✅ 2 bài | Category `00_what-is-ide.md` (so sánh 7 editor) + `vs-code.md` user guide |
| `shell/` | ❌ Chưa có | Terminal + bash/zsh intro |
| `terminal-emulators/` | ❌ Chưa có | iTerm, Kitty, Alacritty, Warp, ... |
| `terminal-tools/` | ❌ Chưa có | tmux, fzf, ripgrep, lazygit |
| `package-managers/` | ❌ Chưa có | brew, apt, npm, pip |
| `k8s-local/` | ❌ Chưa có | Minikube vs Kind vs k3d |
| `docker-tools/` | ❌ Chưa có | Docker Desktop, Compose, ... |
| `api-clients/` | ❌ Chưa có | Postman, Insomnia, ... |
| `db-clients/` | ❌ Chưa có | DBeaver, TablePlus, ... |
| `productivity/` | ❌ Chưa có | Obsidian, Notion, Raycast |

## 🚀 Khi nào đọc folder này

| Nhu cầu | Đọc gì |
|---|---|
| Mới bắt đầu một tool | `00_what-is-X.md` (category overview) → `lessons/01_basic/` |
| Đào sâu một tool cụ thể | File `<tool>.md` của tool đó (vd `git-clients/github.md`) |
| Tra cứu nhanh | `recipes/` + `_cheatsheet.md` (nếu có) |
| Theo nghề | Xem [`../00_roadmaps/career/`](../00_roadmaps/career/) chọn career path đi qua chủ đề này |

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.6.0 (20/05/2026)** — **Tool category đầu tiên hoàn chỉnh** ở `ide/`:
  - `00_what-is-ide.md` — category overview, so sánh 7 editor (VS Code, Cursor, Neovim, JetBrains, Zed, Sublime, Xcode), bảng AI integration 2026, 7 case khuyến nghị theo profile
  - `vs-code.md` v2.0.0 — mở rộng từ setup-only thành full user guide với UI tour, workflows, profile theo vai trò (Python/Frontend/DevOps/Data)
  - Đổi `editor/` → `ide/` theo cách đặt tên tool category
  - Cập nhật cross-link giữa các file
- **v0.5.0 (19/05/2026)** — Tổ chức lại theo tool category 2 cấp (category overview + individual tools):
  - Thêm danh sách L2 dự kiến: `ide/`, `terminal-emulators/`, `git-clients/`, `k8s-local/` — mỗi cái là 1 tool category với 1 file `00_what-is-X.md` (so sánh + chọn) + N file `<tool>.md` (focused individual).
  - Đổi `editor/` thành `ide/` để khớp cách đặt tên tool category.
- **v0.4.0 (16/05/2026)** — **Bộ Git hoàn chỉnh** ở `git/` (setup + intro + lessons). L2 đầy đủ đầu tiên trong kho.
- **v0.3.0 (16/05/2026)** — Thêm setup guide VS Code đầu tiên.
- **v0.2.0 (16/05/2026)** — Có bài đầu tiên ở `shell/` (Terminal Fundamentals).
- **v0.1.0 (16/05/2026)** — Skeleton — folder mới tạo, chưa có content.
