# 🏛️ Mobile Architecture — Kiến trúc ứng dụng di động

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 22/06/2026

> 🎯 *Kiến trúc app mobile độc lập framework: vì sao cần tách lớp, các pattern tầng trình bày (MVC/MVP/MVVM/MVI), Clean Architecture (Domain/Data/Presentation + dependency rule), quản lý state + unidirectional data flow, và testing/modularization để app bền vững. Áp dụng được cho cả native (Swift/Kotlin) lẫn cross-platform (RN/Flutter). Nhiều sơ đồ + ví dụ đối chiếu đa nền tảng.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu **vì sao** cần kiến trúc (coupling, testability, đổi UI/đổi nguồn dữ liệu không vỡ logic)
- [x] Phân biệt các **pattern tầng trình bày**: MVC → MVP → **MVVM** → MVI, chọn đúng theo bối cảnh
- [x] Áp dụng **Clean Architecture**: tách Domain/Data/Presentation, **dependency rule** hướng vào trong
- [x] Quản lý **state** bằng **unidirectional data flow** (UDF), phân biệt UI state vs business state
- [x] **Test** theo tầng + **modularize** (chia module/feature) để app lớn vẫn build nhanh, dễ bảo trì

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`Vì sao cần kiến trúc app mobile?`](./lessons/01_basic/00_why-mobile-architecture.md) | ✅ | Coupling, spaghetti code, testability, vì sao tách lớp; bức tranh tổng. |
| **01** | [`MVC, MVP, MVVM, MVI`](./lessons/01_basic/01_presentation-patterns-mvvm.md) | ✅ | Pattern tầng trình bày, data binding, vì sao MVVM/MVI thắng thế. |
| **02** | [`Clean Architecture & phân tầng`](./lessons/01_basic/02_clean-architecture-and-layers.md) | ✅ | Domain/Data/Presentation, dependency rule, use case, repository. |
| **03** | [`Quản lý State & UDF`](./lessons/01_basic/03_state-management-and-data-flow.md) | ✅ | Unidirectional data flow, UI state vs business state, single source of truth. |
| **04** | [`Testing & Modularization`](./lessons/01_basic/04_testing-and-modularization.md) | ✅ | Test pyramid theo tầng, chia module/feature, build nhanh, dễ bảo trì. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04. Đây là cụm **độc lập framework** — nên đọc **sau** khi đã nắm 1 nền tảng cụ thể ([ios-swift](../ios-swift/), [android-kotlin](../android-kotlin/), [react-native](../react-native/) hoặc [flutter](../flutter/)) để các pattern có chỗ "neo". Người đã code app rồi nhưng thấy code rối → vào thẳng [Bài 02 (Clean Architecture)](./lessons/01_basic/02_clean-architecture-and-layers.md) và [Bài 03 (State)](./lessons/01_basic/03_state-management-and-data-flow.md).

## 🔗 Liên kết cụm liên quan

- [android-kotlin](../android-kotlin/) & [ios-swift](../ios-swift/) — MVVM/Clean Architecture trên native.
- [react-native](../react-native/) & [flutter](../flutter/) — pattern tương tự trên cross-platform.
- [cross-platform-concepts](../cross-platform-concepts/) — chọn nền tảng trước khi dựng kiến trúc.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (22/06/2026)** — Hoàn thiện cụm **Basic 5/5** (vì sao cần kiến trúc + pattern tầng trình bày + Clean Architecture + state/UDF + testing/modularization).
