# 🤖 Android (Kotlin + Compose) — Lập trình Android native

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 15/06/2026

> 🎯 *Lập trình Android native bằng **Kotlin** + **Jetpack Compose** (declarative, khuyến nghị 2026). Học Kotlin (null safety, data class, coroutines), Compose (@Composable, state, modifier), state/data/navigation (ViewModel, Retrofit, Room), và build/publish qua Android Studio → Play Console. Chạy trên mọi OS. CÓ code Kotlin chạy được (Kotlin 2.x, Material 3).*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu hệ sinh thái Android (Kotlin, Android Studio, XML View vs **Jetpack Compose**), phân mảnh thiết bị
- [x] Viết **Kotlin**: null safety, lambda, data class, `when`, **coroutines**/Flow
- [x] Dựng UI bằng **Compose** (@Composable, remember/mutableStateOf, Modifier, Material 3)
- [x] Quản lý state với **ViewModel + StateFlow**, navigation, networking (Retrofit), persistence (DataStore/Room)
- [x] Build **AAB** + ký + publish **Google Play Console**

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`Lập trình Android là gì`](./lessons/01_basic/00_what-is-android-development.md) | ✅ | Kotlin, Android Studio, XML vs Compose, phân mảnh thiết bị. |
| **01** | [`Kotlin cơ bản`](./lessons/01_basic/01_kotlin-basics.md) | ✅ | Null safety, lambda, data class, `when`, coroutines/Flow. |
| **02** | [`Jetpack Compose cơ bản`](./lessons/01_basic/02_jetpack-compose-fundamentals.md) | ✅ | @Composable, Column/LazyColumn, Modifier, remember/state, Material 3. |
| **03** | [`State, Data & Navigation`](./lessons/01_basic/03_state-data-and-navigation.md) | ✅ | ViewModel + StateFlow, Navigation Compose, Retrofit, DataStore/Room. |
| **04** | [`Android Studio, Build & Play Store`](./lessons/01_basic/04_android-studio-build-and-play-store.md) | ✅ | Gradle, AAB, signing/keystore, Play Console, publish. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04. Người mới Kotlin nắm [Bài 01](./lessons/01_basic/01_kotlin-basics.md) (null safety + coroutines) trước [Compose](./lessons/01_basic/02_jetpack-compose-fundamentals.md). Đang phân vân native vs cross-platform → xem [cross-platform-concepts](../cross-platform-concepts/).

## 🔗 Liên kết cụm liên quan

- [ios-swift](../ios-swift/) — đối chiếu native iOS (Swift + SwiftUI).
- [cross-platform-concepts](../cross-platform-concepts/) — khi nào native vs cross-platform.
- [mobile-architecture](../mobile-architecture/) — kiến trúc app (MVVM, Clean Architecture…).

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (15/06/2026)** — Hoàn thiện cụm **Basic 5/5** (Android landscape + Kotlin + Compose + state/data/navigation + Android Studio/Play Store).
