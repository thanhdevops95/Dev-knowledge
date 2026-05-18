# 📘 Blueprint — Repo Tri thức CNTT

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026

Đây là **bản thiết kế chi tiết** (blueprint) để hiện thực hóa ý tưởng đã phác thảo trong [`../_idea-overview.md`](../_idea-overview.md).

Mọi quyết định về *cách kho được xây dựng* (cấu trúc, tên file, chuẩn viết, link chéo, template...) đều nằm trong thư mục này. Khi viết bài mới, đầu tiên tra blueprint, sau đó mới viết nội dung.

---

## 🗂️ Danh mục file

| # | File | Vai trò |
|---|---|---|
| — | [`README.md`](./README.md) | File bạn đang đọc — index của blueprint |
| — | [`_CONCEPT-MAP.md`](./_CONCEPT-MAP.md) | **SSOT register** — concept nào ở file nào (tra trước khi sửa) |
| 00 | [`00_blueprint-overview.md`](./00_blueprint-overview.md) | Blueprint là gì, dùng thế nào, đối tượng đọc |
| 01 | [`01_sitemap-detail.md`](./01_sitemap-detail.md) | Sitemap mở rộng L1 → L2 → L3 của toàn bộ kho |
| 02 | [`02_folder-structure.md`](./02_folder-structure.md) | Cấu trúc folder/file chuẩn + spec MASTER-CATALOG + CONTRIBUTING |
| 03 | [`03_writing-style.md`](./03_writing-style.md) | Chuẩn viết: khung 8 phần, WHY→WHAT→HOW, văn phong, emoji |
| 04 | [`04_naming-convention.md`](./04_naming-convention.md) | Đặt tên file/folder/anchor trong kho nội dung |
| 05 | [`05_linking-strategy.md`](./05_linking-strategy.md) | Link chéo, glossary, cross-L2 pattern |
| 06 | [`06_roadmap-design.md`](./06_roadmap-design.md) | Cách thiết kế roadmap, template, ví dụ |
| 07 | [`07_quality-checklist.md`](./07_quality-checklist.md) | Checklist kiểm tra trước khi publish bài |

## 📁 Thư mục con

| Thư mục | Nội dung |
|---|---|
| [`templates/`](./templates/) | Các template thật để copy-paste khi viết bài (`lesson_template.md`, `topic-readme_template.md`, `roadmap_template.md`, `overview_template.md`) |
| [`examples/`](./examples/) | 1 chủ đề mẫu viết hoàn chỉnh để tham chiếu |

---

## 🔄 Trạng thái

| File | Phiên bản |
|---|---|
| `README.md` | v0.1 |
| `_CONCEPT-MAP.md` | v0.1.0 — **MỚI (SSOT register)** |
| `_CONCEPT-MAP.md` | v0.5.0 (29 concept) |
| `00_blueprint-overview.md` | v0.2.0 |
| `01_sitemap-detail.md` | v0.4.0 |
| `02_folder-structure.md` | v0.4.0 (**+ §3.0 Intro vs Lesson + §3.2bis 02_Tools Hub**) |
| `03_writing-style.md` | v0.4.0 (metaphor rule) |
| `04_naming-convention.md` | v0.1.0 |
| `05_linking-strategy.md` | v0.1.0 |
| `06_roadmap-design.md` | v0.1.0 |
| `07_quality-checklist.md` | v0.3.0 (Reference workflow) |
| `templates/setup_template.md` | ✅ **MỚI** (9 section install chi tiết) |
| `templates/README.md` | v0.2.0 |
| `templates/lesson_template.md` | ✅ |
| `templates/exercise_template.md` | ✅ **MỚI v1.2** |
| `templates/recipe_template.md` | ✅ **MỚI v1.2** |
| `templates/topic-readme_template.md` | ✅ |
| `templates/roadmap_template.md` | ✅ |
| `templates/overview_template.md` | ✅ |
| `templates/contributing_template.md` | ✅ |
| `templates/master-catalog_template.md` | ✅ |
| `examples/sample_kubernetes-pod/` | ✅ (5 file — long lesson) |
| `examples/sample_short-lesson_git-status.md` | ✅ **MỚI** (short lesson dogfood) |
| `examples/sample_exercise_create-first-pod.md` | ✅ **MỚI** (exercise dogfood) |
| `examples/sample_recipe_pod-crashloopbackoff.md` | ✅ **MỚI** (recipe dogfood) |
| `examples/_DOGFOOD-FINDINGS.md` | ✅ **MỚI** (findings vòng 1+2) |

> ✅ **Blueprint v1.4 hoàn thành** — SSOT + 5 recommendations + dogfood + metaphor + Reference workflow + **02_Tools Central Setup Hub**.
>
> ⚠️ **Approach quan trọng**:
> - Viết bài theo Blueprint + ý tưởng riêng làm **CHỦ ĐẠO**. `_Ref/` chỉ cherry-pick ý hay.
> - **Setup chi tiết** đặt ở `02_Tools/<l2>/setup/` cho tool cross-cutting. Bài lesson ở L1 khác chỉ giới thiệu sơ bộ + link về `02_Tools`.
