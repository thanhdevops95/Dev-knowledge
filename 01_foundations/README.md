# 🧠 01_foundations

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.2.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 20/05/2026

> 🚀 **Status:** Đã có content thật ở industry-landscape, computing-environment và computer-architecture-theory. Các L2 lý thuyết khác (dsa, os-theory, networking-theory, ...) còn để trống.

## 🎯 Chủ đề này có gì

01_foundations là **kiến thức nền tảng** — bền vững 10+ năm. Bao gồm: bản đồ ngành IT, computing environment, computational thinking, DSA, OS theory, networking theory, math, programming paradigms.

**Khác với 02_tools** (user guide cho phần mềm cụ thể): Foundations dạy **khái niệm bản chất** không lệ thuộc tool/phiên bản.

## 📂 L2 chủ đề con

| L2 | Trạng thái | Note |
|---|---|---|
| [`industry-landscape/`](./industry-landscape/) | ✅ 1 bài | **Bản đồ ngành IT** — entry point cho người mới. Stage 0 của zero-to-coder |
| [`computing-environment/`](./computing-environment/) | ✅ 6 bài | Terminal / shell / filesystem / process / env var / I/O redirect — concept OS-agnostic |
| [`computer-architecture-theory/`](./computer-architecture-theory/) | ✅ 1 bài | **Máy tính hoạt động thế nào** — binary, CPU/RAM/ổ cứng, compiler vs interpreter |
| `computational-thinking/` | ❌ Chưa có | Logic + problem solving + algorithm cơ bản |
| `dsa/` | ❌ Chưa có | Data Structure + Algorithm |
| `os-theory/` | ❌ Chưa có | Process, memory, file system concept |
| `networking-theory/` | ❌ Chưa có | TCP/IP, OSI — concept thuần |
| `math-for-cs/` | ❌ Chưa có | Discrete math, logic, set theory |
| `programming-paradigms/` | ❌ Chưa có | OOP/FP/Procedural — so sánh |

> Git concept nằm ở [`02_tools/git/`](../02_tools/git/) — MUST-KNOW cho mọi nhánh.

## 🚀 Khi nào đọc folder này

| Nhu cầu | Đọc gì |
|---|---|
| **Mới bắt đầu** (chưa biết IT) | [industry-landscape](./industry-landscape/lessons/01_basic/00_what-is-it-industry.md) **trước nhất**, hiểu cả bức tranh |
| **Học dùng terminal / shell** | [computing-environment](./computing-environment/lessons/01_basic/00_what-is-terminal.md) — 6 bài từ terminal đến I/O redirect |
| **Học Git** | [`02_tools/git/`](../02_tools/git/) — git là MUST-KNOW mọi nhánh |
| **Theo Zero-to-Coder roadmap** | Stage 0 link sang industry-landscape, Stage 1 link sang computing-environment + git |

## 📊 Đặc trưng Foundations vs các L1 khác

| Tiêu chí | Foundations | Tools | Domain (10_devops, 13_ai-ml, ...) |
|---|---|---|---|
| Bản chất | Lý thuyết / concept bền vững | User guide phần mềm | Concept domain cụ thể |
| Lifespan | 10+ năm | Khi UI tool update | 2-5 năm |
| OS-specific? | Không | Tuỳ | Tuỳ |
| Theory:Hands-on | 70:30 | 0:100 (chỉ UI tour) | 50:50 |

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.3.0 (20/05/2026)** — Cập nhật README phản ánh content thật:
  - List L2 với trạng thái mỗi cái (industry-landscape ✅, computing-environment ✅, computer-architecture-theory ✅, các L2 khác ❌)
  - Thêm bảng "khi nào đọc" + bảng "Foundations vs Tools vs Domain"
- **v0.1.0 (16/05/2026)** — Bản khởi tạo.
