# 📋 Templates — Copy-paste khi viết bài

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.3.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 16/05/2026

Bộ **9 template** để bắt đầu viết bài mới. Copy file phù hợp, đổi tên + nội dung theo bài thực tế. Mỗi template tuân theo chuẩn ở `_Blueprint/03_writing-style.md`.

## 📂 Danh mục template

| Template | Dùng cho | Ghi chú |
|---|---|---|
| [`lesson_template.md`](./lesson_template.md) | Bài học lý thuyết trong `lessons/` | 8 phần — REQUIRED và OPTIONAL có comment đánh dấu |
| [`exercise_template.md`](./exercise_template.md) | Bài tập trong `exercises/` | Đề bài + gợi ý ẩn + đáp án ẩn + verify + mở rộng |
| [`recipe_template.md`](./recipe_template.md) | Recipe trong `recipes/` (troubleshooting/patterns/operations) | Problem → Cause → Solution → Verify → Prevention |
| [`setup_template.md`](./setup_template.md) | Setup/install guide trong `setup/` — đặc biệt chi tiết trong `02_Tools/` | 9 section: tool là gì → multi-option install → verify → cấu hình → extensions → lỗi → update/uninstall → alternative |
| [`topic-readme_template.md`](./topic-readme_template.md) | `README.md` của chủ đề L1/L2 | Index + navigation cho cả chủ đề (Parent README) |
| [`roadmap_template.md`](./roadmap_template.md) | Career roadmap hoặc lab series | Dùng chung — đổi header cho từng loại |
| [`overview_template.md`](./overview_template.md) | `00_overview.md` của chủ đề L1/L2 | Giới thiệu chủ đề: là gì, vì sao, khi nào |
| [`contributing_template.md`](./contributing_template.md) | `CONTRIBUTING.md` ở gốc kho | Quy ước đóng góp + anti-patterns |
| [`master-catalog_template.md`](./master-catalog_template.md) | `MASTER-CATALOG.md` ở gốc kho | Tracking trạng thái mọi bài (✅/🚧/❌/🔄) |

## 🚀 Cách dùng

1. Identify loại bài cần viết → chọn template phù hợp
2. Copy nội dung template sang file mới
3. Đổi tên file theo `_Blueprint/04_naming-convention.md`
4. Điền nội dung — giữ structure, đổi nội dung
5. Xóa các phần OPTIONAL không dùng
6. Soát qua `_Blueprint/07_quality-checklist.md` trước khi commit

## ⚠️ Quy tắc

- **Đừng skip Metadata header** — bắt buộc mọi file
- **Đừng xóa câu dẫn** — phần đặc trưng của repo
- **OPTIONAL có thể bỏ** nếu bài không phù hợp
- **REQUIRED không bỏ** — bài lỗi structure
- **Xóa comment `<!-- OPTIONAL -->` và `<!-- REQUIRED nếu... -->` sau khi viết xong** — comment chỉ là chú thích cho template, không phải nội dung. Để lại sẽ làm source rối khi đọc.
- **Xóa các placeholder `<...>` chưa điền** — không để `<Tên bài học>` hay `<X-Y giờ>` trong file đã publish.
