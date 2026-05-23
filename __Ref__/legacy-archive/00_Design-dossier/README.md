# Hồ sơ thiết kế — Dev-Knowledge rebuild

> **Author:** Mr.Rom\
> **Version:** v1.0.0\
> **Created:** 15/05/2026\
> **Last updated:** 15/05/2026

Thư mục này gom **toàn bộ bản thảo kế hoạch tái cấu trúc** từng được soạn ở các phiên làm việc khác nhau (Claude Code, Cursor, TRAE, Windsurf, OpenCode) và **bản kế hoạch riêng** cho loạt bài K8s-training (phạm vi khác: biên soạn từ phụ đề video).

## Mục lục tài liệu

| File | Phạm vi / góc nhìn |
|------|---------------------|
| [REBUILD_PLAN_Claudecode.md](REBUILD_PLAN_Claudecode.md) | Phân tích trùng lặp, 8 phase + MASTER-CATALOG, cấu trúc parent lesson (`README`, `index`, `lesson`, `_sub-lessons/`, …), tích hợp `.Old`, timeline ~10 tuần. |
| [REBUILD_PLAN_Cursor.md](REBUILD_PLAN_Cursor.md) | Nguyên tắc V2: tách domain vs loại tài sản; `00-META` + 11 domain; nhãn migration A/B/C/D; roadmap 6 tuần; ưu tiên chất lượng thực học. |
| [REBUILD_PLAN_TRAE.md](REBUILD_PLAN_TRAE.md) | Góc “sản phẩm”: KPI, WBS Audit→Design→Migrate→Optimize, template YAML frontmatter, CI/search/feedback (tầm nhìn web). |
| [REBUILD_PLAN_Windsurf.md](REBUILD_PLAN_Windsurf.md) | Cây `Dev-Knowledge-v2/` theo **lớp học 10–90** (Foundations → Career); bảng mapping chi tiết từng block cũ → mới; checklist merge. |
| [REBUILD-PLAN_Opencode.md](REBUILD-PLAN_Opencode.md) | Learning path 01–20 + roadmaps/templates; workflow audit → migration → cleanup; template bài viết có level/tags. |
| [REBUILD-PLAN_K8s-training.md](REBUILD-PLAN_K8s-training.md) | **Bản sao** (canonical vẫn nằm tại `../K8s-training/REBUILD-PLAN.md`): module hóa 40 bài từ phụ đề, glossary, template bài học — *không* phải blueprint toàn kho Dev-Knowledge. |

## Ghi chú

- Các file ở đây **không đồng bộ số thứ tự** domain với nhau (ví dụ Cursor 11 domain vs Windsurf 10–90 vs Claude theo MASTER-CATALOG 00–21). Bước tiếp theo là **hòa giải** trong một tài liệu chuẩn duy nhất (sau khi bạn chốt quy ước đặt tên thư mục theo `00_Skills` / Dev workspace).

## Changelog

- **v1.0.0 (15/05/2026)**: Tạo thư mục, di chuyển 5 plan gốc `_Ref/`, copy plan K8s-training.
