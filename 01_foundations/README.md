# 🧠 01_foundations

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.2.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 20/05/2026

> 🚀 **Status:** Có 2 L2 đã có content thật (industry-landscape + version-control/git). Các L2 lý thuyết khác (dsa, os-theory, networking-theory, ...) còn skeleton.

## 🎯 Chủ đề này có gì

01_foundations là **kiến thức nền tảng** — bền vững 10+ năm. Bao gồm: bản đồ ngành IT, computational thinking, version control concept, DSA, OS theory, networking theory, math, programming paradigms.

**Khác với 02_tools** (user guide cho phần mềm cụ thể): Foundations dạy **khái niệm bản chất** không lệ thuộc tool/phiên bản.

## 📂 L2 chủ đề con

| L2 | Trạng thái | Note |
|---|---|---|
| [`industry-landscape/`](./industry-landscape/) | 🚀 1 bài 🆕 | **Bản đồ ngành IT** — entry point cho beginner zero-base. Stage 0 của zero-to-coder |
| [`version-control/`](./version-control/) | ✅ 6 bài | **Git concept** (move từ `02_tools/git/` ngày 19/05/2026) — setup + 5 lesson bạn story arc |
| `computing-environment/` | ❌ Chưa có | Terminal/shell/OS concept (sẽ chuyển 1 bài từ `02_tools/shell/`) |
| `computational-thinking/` | ❌ Chưa có | Logic + problem solving + algorithm cơ bản |
| `dsa/` | ❌ Chưa có | Data Structure + Algorithm |
| `os-theory/` | ❌ Chưa có | Process, memory, file system concept |
| `networking-theory/` | ❌ Chưa có | TCP/IP, OSI — concept thuần |
| `math-for-cs/` | ❌ Chưa có | Discrete math, logic, set theory |
| `programming-paradigms/` | ❌ Chưa có | OOP/FP/Procedural — so sánh |

> Chi tiết sitemap mở rộng → xem [`../_blueprint/01_sitemap-detail.md`](../_blueprint/01_sitemap-detail.md).

## 🚀 Khi nào đọc folder này

| Bạn là... | Đọc gì |
|---|---|
| 🟢 **Zero-base** (chưa biết IT) | [industry-landscape](./industry-landscape/lessons/01_basic/00_what-is-it-industry.md) **trước nhất** — 20 phút đọc, hiểu cả bức tranh |
| 🟡 **Đã code 1 ngôn ngữ** | [version-control/git/](./version-control/git/) — git là MUST-KNOW mọi nhánh |
| 🟠 **Senior ôn nền tảng** | dsa/, os-theory/, networking-theory/ (chưa có content, đang phát triển) |
| 🧭 **Theo Zero-to-Coder roadmap** | Stage 0 link sang industry-landscape, Stage 1 link sang version-control/git |

## 📊 Đặc trưng Foundations vs các L1 khác

| Tiêu chí | Foundations | Tools | Domain (10_devops, 13_ai-ml, ...) |
|---|---|---|---|
| Bản chất | Lý thuyết / concept bền vững | User guide phần mềm | Concept domain cụ thể |
| Lifespan | 10+ năm | Khi UI tool update | 2-5 năm |
| OS-specific? | Không | Tuỳ | Tuỳ |
| Theory:Hands-on | 70:30 | 0:100 (chỉ UI tour) | 50:50 |

## 🤝 Muốn viết bài cho chủ đề này?

1. Đọc [`../_blueprint/README.md`](../_blueprint/README.md)
2. Copy template từ [`../_blueprint/templates/`](../_blueprint/templates/) (`lesson_template.md` cho Foundation lesson)
3. Viết theo [`../_blueprint/03_writing-style.md`](../_blueprint/03_writing-style.md) v0.5.1+ — mở bằng tình huống, headers câu hỏi tự nhiên
4. Tham khảo bài có sẵn:
   - [industry-landscape lesson](./industry-landscape/lessons/01_basic/00_what-is-it-industry.md) — narrative style mẫu
   - [git intro với bạn story](./version-control/git/lessons/01_basic/00_what-is-git.md) — situation-led definition mẫu
5. Soát qua [`../_blueprint/07_quality-checklist.md`](../_blueprint/07_quality-checklist.md)
6. Cập nhật [`../MASTER-CATALOG.md`](../MASTER-CATALOG.md)

---

## 📌 Changelog

- **v0.2.0 (20/05/2026)** — Update toàn bộ README phản ánh content thật:
  - Trạng thái Skeleton → "Có 2 L2 content thật"
  - List L2 đầy đủ với trạng thái mỗi cái (industry-landscape ✅, version-control ✅, các L2 khác ❌)
  - Thêm bảng "khi nào đọc" + bảng "Foundations vs Tools vs Domain"
  - Hướng dẫn viết bài link sang 2 reference mẫu (industry-landscape + git)
- **v0.1.0 (16/05/2026)** — Skeleton — folder mới tạo, chưa có content.
