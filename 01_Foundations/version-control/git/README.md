# 🌿 Git — Version Control

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026

> 🎯 *Git là **distributed version control system** dùng bởi 90%+ developer. Folder này cover từ "cài Git lần đầu" tới workflow team chuyên nghiệp với GitHub.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:

- [ ] Cài + cấu hình Git xong
- [ ] Hiểu mô hình 3 vùng (working/staging/repo) + commit cycle
- [ ] Tạo branch + merge + resolve conflict
- [ ] Push/pull với GitHub
- [ ] Mở Pull Request, code review
- [ ] Recover từ tình huống "lỡ tay" (xóa file, commit sai, ...)

---

## 📂 Cấu trúc

### setup/ — Cài đặt + cấu hình

| File | Trạng thái | Note |
|---|---|---|
| ✅ 🌟 [`setup/git.md`](./setup/git.md) | Done | Cài Git 5 OS + config user.name/email + GUI tools |
| ❌ `setup/ssh-key-github.md` | Chưa có | Setup SSH key cho GitHub |
| ❌ `setup/github-cli.md` | Chưa có | `gh` CLI |

### lessons/01_basic/ — Workflow cơ bản

| # | Bài | Trạng thái | Loại |
|---|---|---|---|
| 00 | [What is Git](./lessons/01_basic/00_what-is-git.md) | ✅ 🌟 | 🌱 Intro |
| 01 | [Init + First commit](./lessons/01_basic/01_init-and-first-commit.md) | ✅ 🌟 | 🌳 Lesson |
| 02 | [Branching + Merging](./lessons/01_basic/02_branching-and-merging.md) | ✅ 🌟 | 🌳 Lesson |
| 03 | [Remote + GitHub](./lessons/01_basic/03_remote-and-github.md) | ✅ 🌟 | 🌳 Lesson |
| 04 | [Undo + Recovery](./lessons/01_basic/04_undo-and-recovery.md) | ✅ 🌟 | 🌳 Lesson |
| 05 | Rebase + Cherry-pick | ❌ Chưa có | 🌳 Lesson (power user) |

### lessons/02_intermediate/, 03_advanced/

❌ Chưa có (dự kiến: stash patterns, interactive rebase, hooks, submodules, worktrees)

### exercises/, projects/, recipes/

❌ Chưa có (dự kiến: bài tập thực tế, fix scenarios, workflow patterns)

---

## 🚀 Lộ trình đề xuất

| Bạn là... | Đi theo |
|---|---|
| 🟢 **Beginner zero-base** | [setup/git.md](./setup/git.md) → [00_what-is-git](./lessons/01_basic/00_what-is-git.md) → 01 → 02 → 03 |
| 🟡 **Đã biết git add/commit nhưng confuse branch** | Nhảy thẳng [02_branching-and-merging](./lessons/01_basic/02_branching-and-merging.md) |
| 🟠 **Senior ôn lại** | Cheatsheet ở mỗi bài + skim các pitfall |
| 🧭 **Theo Zero-to-Coder roadmap** | 4 bài (setup + 00 → 03) đủ cho Stage 1 |

---

## 🌟 Sản phẩm sau bộ bài này

Sau 4 bài (setup + 00-03), bạn có thể:
- Tạo project mới + init git + commit lịch sử
- Tạo feature branch + merge về main
- Resolve conflict khi gặp
- Push project lên GitHub
- Clone repo về máy mới
- Tham gia workflow team qua Pull Request

→ Đây là **80% kỹ năng Git dùng daily**. 20% còn lại (rebase, recovery, hooks) học dần khi cần.

---

## 💡 Khuyến nghị

| Nhu cầu | Hành động |
|---|---|
| Học cùng visual | Dùng [Learn Git Branching](https://learngitbranching.js.org/) — game |
| Cần ôn kiến thức | Xem [Pro Git tiếng Việt](https://git-scm.com/book/vi/v2) — free |
| Cần GUI thay CLI | Cài GitLens extension cho VS Code (xem [VS Code setup](../editor/setup/vs-code.md) §6) |

---

## 🤝 Muốn viết thêm bài cho Git?

1. Đọc [`../../_Blueprint/00_blueprint-overview.md`](../../_Blueprint/00_blueprint-overview.md)
2. Chọn template:
   - Setup → `setup_template.md`
   - Lesson tool feature → `lesson_template.md`
3. Tham khảo 4 bài có sẵn làm reference
4. Cập nhật bảng trên + [`../../MASTER-CATALOG.md`](../../MASTER-CATALOG.md)

---

## 📌 Changelog

- **v0.1.0 (16/05/2026)** — Bộ Git đầu tiên hoàn thành: setup + 4 bài (intro + 3 lesson). Stage 1 zero-to-coder có Git foundation đủ.
