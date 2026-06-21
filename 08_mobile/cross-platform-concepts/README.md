# 🔀 Cross-Platform Concepts — Xây app mobile đa nền tảng

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 15/06/2026

> 🎯 *Bức tranh tổng về phát triển mobile đa nền tảng (không đi sâu 1 framework): native vs cross-platform, 3 nhóm kiến trúc (WebView / bridge / compiled), so sánh + chọn framework (RN/Flutter/KMP/MAUI/Ionic), chia sẻ code + design system, và khi nào cross-platform vs native thuần. Nhiều bảng so sánh + decision matrix + sơ đồ.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu **native vs cross-platform** + landscape 2026, đánh đổi hiệu năng/native-feel
- [x] Phân biệt **3 kiến trúc**: WebView/hybrid, JS-bridge (RN), compiled/self-rendered (Flutter/KMP)
- [x] **Chọn framework** đúng bằng decision matrix (kỹ năng team, hiệu năng, ecosystem, native access)
- [x] Biết chiến lược **chia sẻ code** (logic vs UI) + design system đa nền tảng
- [x] Quyết định **cross-platform vs native thuần** theo loại app + ràng buộc thực tế

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`Cross-platform là gì`](./lessons/01_basic/00_what-is-cross-platform-mobile.md) | ✅ | Native vs cross-platform, landscape (RN/Flutter/KMP/MAUI/Ionic/PWA), đánh đổi. |
| **01** | [`Các cách tiếp cận`](./lessons/01_basic/01_approaches-and-architecture.md) | ✅ | WebView/hybrid vs JS-bridge vs compiled/self-rendered, so sánh kiến trúc. |
| **02** | [`Chọn framework`](./lessons/01_basic/02_choosing-a-framework.md) | ✅ | RN/Flutter/KMP/MAUI/Ionic, tiêu chí + decision matrix + cây quyết định. |
| **03** | [`Chia sẻ code & Design System`](./lessons/01_basic/03_sharing-code-and-design-system.md) | ✅ | Share logic vs UI, KMP, monorepo, design tokens, Material vs HIG. |
| **04** | [`Cross-platform vs native`](./lessons/01_basic/04_when-cross-platform-vs-native.md) | ✅ | Khi nào cross-platform thắng vs native thuần, hybrid, chi phí dài hạn. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04 TRƯỚC khi chọn học một framework cụ thể. Sau khi quyết, đi sâu cụm tương ứng: [react-native](../react-native/), [flutter](../flutter/), [ios-swift](../ios-swift/), [android-kotlin](../android-kotlin/).

## 🔗 Liên kết cụm liên quan

- [react-native](../react-native/) & [flutter](../flutter/) — 2 cross-platform phổ biến nhất.
- [mobile-architecture](../mobile-architecture/) — kiến trúc app sau khi chọn framework.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (15/06/2026)** — Hoàn thiện cụm **Basic 5/5** (cross-platform là gì + kiến trúc + chọn framework + chia sẻ code + cross-platform vs native).
