# 🛠️ 02_tools

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.6.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 20/05/2026

> 🚀 **Status:** Có 1 bài đầu tiên ở [`shell/`](./shell/). Các L2 khác còn skeleton.

## 🎯 Chủ đề này có gì

Git, Shell, Editor, terminal tools, package managers, productivity — bộ công cụ coder dùng hàng ngày.

### ⭐ Vai trò đặc biệt — Central Setup Hub

`02_tools/` không chỉ là chủ đề học **dùng** tool, mà còn là **NƠI CANONICAL** cho mọi hướng dẫn **cài đặt + cấu hình chi tiết** của các tool cross-cutting (dùng cho nhiều L1):

- **Setup chi tiết tối đa**: multi-option install, troubleshooting, extension recommendations, comparison với alternative
- **Lessons ở L1 khác** chỉ giới thiệu sơ bộ rồi link về `02_tools/<l2>/setup/<tool>.md`
- **Tránh** lặp install instructions ở mọi bài cần tool đó (DRY)

→ Khi viết bài lesson cần tool, nếu tool **cross-cutting** (>1 L1 dùng) → setup chi tiết đặt ở `02_tools/`. Tool **specific** 1 L1 → setup trong L1 đó.

Chi tiết quy tắc → [`../_blueprint/02_folder-structure.md`](../_blueprint/02_folder-structure.md) §3.2bis.

## 📂 L2 chủ đề con

| L2 | Trạng thái | Note |
|---|---|---|
| [`ide/`](./ide/) | ✅ 2 bài 🆕 | **Tool category đầu tiên** — category file `00_what-is-ide.md` (so sánh 7 editor) + `vs-code.md` v2.0 user guide |
| [`shell/`](./shell/) | 🚀 1 bài | Terminal + bash/zsh intro (sẽ chuyển sang Foundations/computing-environment) |
| ~~`editor/`~~ | 🔄 Đã move | Rename → `ide/` (20/05/2026) |
| ~~`git/`~~ | 🔄 Đã move | Git concept đã chuyển sang [`../01_foundations/version-control/git/`](../01_foundations/version-control/git/) — git là VCS concept, không phải tool guide |
| `terminal-emulators/` | ❌ Chưa có | iTerm, Kitty, Alacritty, Warp, ... |
| `git-clients/` | ❌ Chưa có | GitHub/GitLab UI, GitHub Desktop, GitKraken |
| `k8s-local/` | ❌ Chưa có | Minikube vs Kind vs k3d |
| `terminal-tools/` | ❌ Chưa có | tmux, fzf, ripgrep, lazygit |
| `package-managers/` | ❌ Chưa có | brew, apt, npm, pip |
| `productivity/` | ❌ Chưa có | Obsidian, Notion, Raycast |

> Chi tiết sitemap mở rộng → xem [`../_blueprint/01_sitemap-detail.md`](../_blueprint/01_sitemap-detail.md).

## 🚀 Khi nào đọc folder này

| Bạn là... | Đọc gì khi có content |
|---|---|
| 🟢 Beginner | `lessons/01_basic/` |
| 🟡 Người chuyển ngành | `00_overview.md` → `lessons/02_intermediate/` |
| 🟠 Senior ôn lại | `_cheatsheet.md` (nếu có) + `_glossary.md` (nếu có) |
| 🔵 Tra cứu nhanh | `recipes/` + `_cheatsheet.md` |
| 🧭 Theo roadmap | Xem [`../00_roadmaps/career/`](../00_roadmaps/career/) chọn career path đi qua chủ đề này |

## 🤝 Muốn viết bài cho chủ đề này?

1. Đọc [`../_blueprint/README.md`](../_blueprint/README.md)
2. Copy template từ [`../_blueprint/templates/`](../_blueprint/templates/) (lesson_template / exercise_template / recipe_template / ...)
3. Viết theo [`../_blueprint/03_writing-style.md`](../_blueprint/03_writing-style.md)
4. Soát qua [`../_blueprint/07_quality-checklist.md`](../_blueprint/07_quality-checklist.md)
5. Cập nhật [`../MASTER-CATALOG.md`](../MASTER-CATALOG.md)
6. Tham khảo `_Ref/` (nếu có content liên quan) — cherry-pick, KHÔNG copy

---

## 📌 Changelog

- **v0.6.0 (20/05/2026)** — **Tool category đầu tiên hoàn chỉnh** ở `ide/`:
  - `00_what-is-ide.md` — category overview, so sánh 7 editor (VS Code, Cursor, Neovim, JetBrains, Zed, Sublime, Xcode), bảng AI integration 2026, 7 case khuyến nghị theo profile
  - `vs-code.md` v2.0.0 — restructure từ setup-only → full user guide với UI tour, workflows, profile theo vai trò (Python/Frontend/DevOps/Data)
  - Move `editor/setup/vs-code.md` → `ide/vs-code.md` (rename L2 theo tool category convention)
  - 15 file cross-link auto-updated
- **v0.5.0 (19/05/2026)** — **Restructure theo phân vai trò 3 bucket**:
  - **Move `git/` sang `01_foundations/version-control/git/`** — git là VCS concept, không phải tool guide. 02_tools dành cho tool category với 2-level (category overview + individual tools).
  - Thêm danh sách L2 dự kiến: `ide/`, `terminal-emulators/`, `git-clients/`, `k8s-local/` — mỗi cái là 1 tool category với 1 file `00_what-is-X.md` (so sánh + chọn) + N file `<tool>.md` (focused individual).
  - `editor/` sẽ rename thành `ide/` để khớp tool category naming.
  - `shell/` content terminal-concept sẽ chuyển sang `01_foundations/computing-environment/`.
- **v0.4.0 (16/05/2026)** — **Bộ Git hoàn chỉnh** ở `git/` (5 bài: setup + intro + 3 lessons). L2 đầy đủ đầu tiên trong kho.
- **v0.3.0 (16/05/2026)** — Thêm `editor/setup/vs-code.md` ✅ — setup guide đầu tiên của kho, dogfood `setup_template`.
- **v0.2.0 (16/05/2026)** — Có bài đầu tiên ở `shell/` ✅ (Terminal Fundamentals).
- **v0.1.0 (16/05/2026)** — Skeleton — folder mới tạo, chưa có content.
