# 🦋 Flutter — UI đa nền tảng với Dart

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 15/06/2026

> 🎯 *Flutter (Google, ngôn ngữ Dart) tự vẽ mọi pixel bằng engine riêng → UI nhất quán trên iOS/Android/web/desktop từ một codebase. Học Dart + widget, layout + Material 3, quản lý state (setState → Provider/Riverpod), và navigation + build/publish. CÓ code Dart chạy được (Flutter 3.x, null-safety, Material 3).*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu **Flutter** + kiến trúc (Framework/Engine/Embedder), "everything is a widget", vs React Native
- [x] Viết **Dart** đủ dùng + phân biệt **StatelessWidget vs StatefulWidget**, dựng widget tree
- [x] Bố cục bằng **Row/Column/Expanded/Stack** + hiểu mô hình **constraints**, Material 3 + theming
- [x] Quản lý **state**: setState → Provider/Riverpod, chọn đúng theo quy mô
- [x] **Navigation** (go_router) + **build/publish** lên store + DevTools

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`Flutter là gì`](./lessons/01_basic/00_what-is-flutter.md) | ✅ | Dart, tự vẽ UI (Skia/Impeller), hot reload, kiến trúc, vs React Native. |
| **01** | [`Dart & Widgets`](./lessons/01_basic/01_dart-and-widgets.md) | ✅ | Dart null-safety, StatelessWidget vs StatefulWidget, build(), widget tree. |
| **02** | [`Layout & Styling`](./lessons/01_basic/02_layout-and-styling.md) | ✅ | Row/Column/Expanded/Stack, mô hình constraints, Material 3, theming. |
| **03** | [`Quản lý State`](./lessons/01_basic/03_state-management.md) | ✅ | setState, InheritedWidget, Provider/Riverpod, ephemeral vs app state. |
| **04** | [`Navigation, Build & Deploy`](./lessons/01_basic/04_navigation-build-and-deploy.md) | ✅ | go_router, flutter build, publish store, DevTools, flavor. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04. Nên đọc [cross-platform-concepts](../cross-platform-concepts/) trước để biết vì sao chọn Flutter. Bắt đầu code từ [Bài 01](./lessons/01_basic/01_dart-and-widgets.md); app nhiều màn + state thì [Bài 03](./lessons/01_basic/03_state-management.md).

## 🔗 Liên kết cụm liên quan

- [cross-platform-concepts](../cross-platform-concepts/) — chọn Flutter hay framework khác.
- [react-native](../react-native/) — đối thủ cross-platform chính.
- [mobile-architecture](../mobile-architecture/) — kiến trúc app mobile.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (15/06/2026)** — Hoàn thiện cụm **Basic 5/5** (Flutter là gì + Dart/widgets + layout/styling + state management + navigation/build/deploy).
