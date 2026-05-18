# 🛠️ 02_Tools

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.2.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026

> 🚀 **Status:** Có 1 bài đầu tiên ở [`shell/`](./shell/). Các L2 khác còn skeleton.

## 🎯 Chủ đề này có gì

Git, Shell, Editor, terminal tools, package managers, productivity — bộ công cụ coder dùng hàng ngày.

### ⭐ Vai trò đặc biệt — Central Setup Hub

`02_Tools/` không chỉ là chủ đề học **dùng** tool, mà còn là **NƠI CANONICAL** cho mọi hướng dẫn **cài đặt + cấu hình chi tiết** của các tool cross-cutting (dùng cho nhiều L1):

- **Setup chi tiết tối đa**: multi-option install, troubleshooting, extension recommendations, comparison với alternative
- **Lessons ở L1 khác** chỉ giới thiệu sơ bộ rồi link về `02_Tools/<l2>/setup/<tool>.md`
- **Tránh** lặp install instructions ở mọi bài cần tool đó (DRY)

→ Khi viết bài lesson cần tool, nếu tool **cross-cutting** (>1 L1 dùng) → setup chi tiết đặt ở `02_Tools/`. Tool **specific** 1 L1 → setup trong L1 đó.

Chi tiết quy tắc → [`../_Blueprint/02_folder-structure.md`](../_Blueprint/02_folder-structure.md) §3.2bis.

## 📂 L2 chủ đề con

| L2 | Trạng thái | Note |
|---|---|---|
| [`shell/`](./shell/) | 🚀 1 bài | Terminal + bash/zsh intro |
| [`editor/`](./editor/) | 🚀 1 setup | VS Code chi tiết |
| [`git/`](./git/) | ✅ 5 bài | **Bộ Git hoàn chỉnh**: setup + intro + 3 lessons (workflow đầy đủ) |
| `terminal-tools/` | ❌ Chưa có | tmux, fzf, ripgrep, lazygit |
| `package-managers/` | ❌ Chưa có | brew, apt, npm, pip |
| `productivity/` | ❌ Chưa có | Obsidian, Notion, Raycast |

> Chi tiết sitemap mở rộng → xem [`../_Blueprint/01_sitemap-detail.md`](../_Blueprint/01_sitemap-detail.md).

## 🚀 Khi nào đọc folder này

| Bạn là... | Đọc gì khi có content |
|---|---|
| 🟢 Beginner | `lessons/01_basic/` |
| 🟡 Người chuyển ngành | `00_overview.md` → `lessons/02_intermediate/` |
| 🟠 Senior ôn lại | `99_cheatsheet.md` (nếu có) + `_glossary.md` (nếu có) |
| 🔵 Tra cứu nhanh | `recipes/` + `99_cheatsheet.md` |
| 🧭 Theo roadmap | Xem [`../00_Roadmaps/career/`](../00_Roadmaps/career/) chọn career path đi qua chủ đề này |

## 🤝 Muốn viết bài cho chủ đề này?

1. Đọc [`../_Blueprint/00_blueprint-overview.md`](../_Blueprint/00_blueprint-overview.md)
2. Copy template từ [`../_Blueprint/templates/`](../_Blueprint/templates/) (lesson_template / exercise_template / recipe_template / ...)
3. Viết theo [`../_Blueprint/03_writing-style.md`](../_Blueprint/03_writing-style.md)
4. Soát qua [`../_Blueprint/07_quality-checklist.md`](../_Blueprint/07_quality-checklist.md)
5. Cập nhật [`../MASTER-CATALOG.md`](../MASTER-CATALOG.md)
6. Tham khảo `_Ref/` (nếu có content liên quan) — cherry-pick, KHÔNG copy

---

## 📌 Changelog

- **v0.4.0 (16/05/2026)** — **Bộ Git hoàn chỉnh** ở `git/` (5 bài: setup + intro + 3 lessons). L2 đầy đủ đầu tiên trong kho.
- **v0.3.0 (16/05/2026)** — Thêm `editor/setup/vs-code.md` ✅ — setup guide đầu tiên của kho, dogfood `setup_template`.
- **v0.2.0 (16/05/2026)** — Có bài đầu tiên ở `shell/` ✅ (Terminal Fundamentals).
- **v0.1.0 (16/05/2026)** — Skeleton — folder mới tạo, chưa có content.
