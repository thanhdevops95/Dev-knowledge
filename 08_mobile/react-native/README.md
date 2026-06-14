# 📱 React Native — Viết app native bằng React

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 15/06/2026

> 🎯 *React Native: dùng React + JS/TS để render UI **native thật** trên iOS + Android từ một codebase. Học core components + styling (Flexbox, không CSS), navigation + state, truy cập API thiết bị, và build/publish lên store. Phù hợp người đã biết React web. CÓ code RN chạy được (RN 0.7x + New Architecture, Expo).*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu **RN là gì** + kiến trúc (New Architecture: JSI/Fabric/Hermes), Expo vs bare, RN vs Flutter vs native
- [x] Dựng UI bằng **core components + StyleSheet/Flexbox**, list với FlatList
- [x] Điều hướng nhiều màn bằng **React Navigation** + quản lý state/fetch dữ liệu
- [x] Truy cập **API thiết bị** (storage/camera/location) + xử lý permissions + khác biệt nền tảng
- [x] **Build + publish** lên App Store/Play Store với EAS, dùng OTA update

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`React Native là gì`](./lessons/01_basic/00_what-is-react-native.md) | ✅ | UI native thật, New Architecture (JSI/Fabric/Hermes), Expo vs bare, RN vs Flutter/native. |
| **01** | [`Core Components & Styling`](./lessons/01_basic/01_core-components-and-styling.md) | ✅ | View/Text/Image/FlatList, StyleSheet + Flexbox (khác web), SafeAreaView. |
| **02** | [`Navigation & State`](./lessons/01_basic/02_navigation-and-state.md) | ✅ | React Navigation (stack/tab), params, state (Context/Zustand), fetch dữ liệu. |
| **03** | [`Native APIs & nền tảng`](./lessons/01_basic/03_native-apis-and-platform.md) | ✅ | AsyncStorage, camera/location, permissions, Platform API, native modules. |
| **04** | [`Build, Debug & Publish`](./lessons/01_basic/04_build-debug-and-publish.md) | ✅ | Metro/Fast Refresh, debug, EAS Build, publish store, OTA update. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04. Cần nắm React web trước ([07_web/frontend/react](../../../07_web/frontend/react/)). Bắt đầu code ngay từ [Bài 01](./lessons/01_basic/01_core-components-and-styling.md); app nhiều màn thì [Bài 02](./lessons/01_basic/02_navigation-and-state.md); chuẩn bị ra mắt thì [Bài 04](./lessons/01_basic/04_build-debug-and-publish.md).

## 🔗 Liên kết cụm liên quan

- [cross-platform-concepts](../cross-platform-concepts/) — bức tranh tổng cross-platform (RN/Flutter/KMP).
- [07_web/frontend/react](../../../07_web/frontend/react/) — nền tảng React (bắt buộc trước).
- [mobile-architecture](../mobile-architecture/) — kiến trúc app mobile.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Khởi tạo placeholder (1 bài intro).
- **v1.0.0 (15/06/2026)** — Hoàn thiện cụm **Basic 5/5** (viết lại 00 + components/styling + navigation/state + native APIs + build/publish).
