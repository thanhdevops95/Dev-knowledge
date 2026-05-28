# 📱 Lộ trình Mobile Developer

> `[BEGINNER → ADVANCED]` — Xem trước [Tổng quan Lộ trình](./00-overview.md)

---

## Tại sao Mobile?

Hơn 3 tỷ smartphone trên thế giới — và mỗi chiếc đều cần app. Mobile developer giống như kiến trúc sư xây nhà: bạn phải tính đến diện tích (màn hình nhỏ), tiện nghi (UX), và ngân sách (pin, bandwidth). App economy tạo ra hàng trăm tỷ USD mỗi năm, và nhu cầu tuyển dụng vẫn tăng đều.

Câu hỏi lớn nhất: **Native hay Cross-platform?** Native cho performance tối đa, Cross-platform cho tốc độ phát triển. Không có lựa chọn sai — chỉ có lựa chọn phù hợp với mục tiêu của bạn.

---

## Chọn hướng đi

| Tiêu chí | React Native | Flutter | Native iOS | Native Android |
|---|---|---|---|---|
| Ngôn ngữ | JavaScript/TS | Dart | Swift | Kotlin |
| Độ khó học | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Performance | Tốt | Rất tốt | Xuất sắc | Xuất sắc |
| Hệ sinh thái | Rất lớn (npm) | Đang lớn nhanh | Apple-only | Google-only |
| Thị trường VN | 🔥 Cao | 🔥 Đang tăng | Trung bình | Trung bình |

---

## Sơ đồ lộ trình

```
Chọn hướng
    │
    ├──► React Native Path          ├──► Flutter Path
    │       │                        │       │
    │   JS/TS basics                 │   Dart basics
    │       │                        │       │
    │   React basics                 │   Flutter basics
    │       │                        │       │
    │   React Native + Expo          │   Widgets & Layouts
    │       │                        │       │
    │   Navigation & State           │   Navigation & State
    │       │                        │       │
    │   APIs & Local Storage         │   APIs & Local Storage
    │       │                        │       │
    │   Push Notifications           │   Push Notifications
    │       │                        │       │
    └───────┴──► Mobile DevOps ──► App Store / Play Store
```

---

## Giai đoạn 1 — React Native Path

### Phase 1: Nền tảng ngôn ngữ
- [ ] JavaScript cơ bản → [../05-Languages/javascript/](../05-Languages/javascript/)
- [ ] TypeScript cơ bản → [../05-Languages/typescript/](../05-Languages/typescript/)

### Phase 2: React cơ bản
- [ ] Components, Props, State, Hooks → [../06-Frontend/react/01-react-basics.md](../06-Frontend/react/01-react-basics.md)

### Phase 3: React Native & Expo
- [ ] React Native core components → [../16-Mobile/react-native/01-react-native-basics.md](../16-Mobile/react-native/01-react-native-basics.md)
- [ ] Expo setup & workflow → [../16-Mobile/react-native/02-expo-basics.md](../16-Mobile/react-native/02-expo-basics.md)

### Phase 4: Navigation & State Management
- [ ] React Navigation (Stack, Tab, Drawer)
- [ ] State: Zustand / Redux Toolkit / Context API

### Phase 5: APIs & Storage
- [ ] REST API integration (Axios / fetch)
- [ ] AsyncStorage, SQLite, MMKV

### Phase 6: Push Notifications
- [ ] Firebase Cloud Messaging → [../16-Mobile/mobile/01-push-notifications-fundamentals.md](../16-Mobile/mobile/01-push-notifications-fundamentals.md)

### Phase 7: Mobile DevOps
- [ ] Fastlane → [../16-Mobile/mobile-devops/01-fastlane-setup.md](../16-Mobile/mobile-devops/01-fastlane-setup.md)
- [ ] App Store & Play Store deploy → [../16-Mobile/mobile-devops/02-app-store-deploy-practices.md](../16-Mobile/mobile-devops/02-app-store-deploy-practices.md)

---

## Giai đoạn 2 — Flutter Path

### Phase 1: Nền tảng ngôn ngữ
- [ ] Dart cơ bản → [../05-Languages/dart/01-dart-basics.md](../05-Languages/dart/01-dart-basics.md) hoặc [../16-Mobile/flutter/02-dart-basics.md](../16-Mobile/flutter/02-dart-basics.md)

### Phase 2: Flutter cơ bản
- [ ] Widgets, Layouts, Material Design → [../16-Mobile/flutter/01-flutter-basics.md](../16-Mobile/flutter/01-flutter-basics.md)

### Phase 3–7: Tương tự React Native
- [ ] Navigation (GoRouter), State (Riverpod / Bloc)
- [ ] HTTP client (Dio), local storage (Hive, SharedPreferences)
- [ ] Push Notifications (FCM) → [../16-Mobile/mobile/01-push-notifications-fundamentals.md](../16-Mobile/mobile/01-push-notifications-fundamentals.md)
- [ ] Fastlane + Store deploy → [../16-Mobile/mobile-devops/](../16-Mobile/mobile-devops/)

---

## 📦 Project thực hành

| Giai đoạn | Project |
|---|---|
| Sau basics | Todo App với local storage |
| Sau Navigation | App nhiều màn hình: News Reader, Recipe App |
| Sau APIs | Weather App, Movie Browser dùng REST API |
| Sau Notifications | Chat App với push notifications (Firebase) |
| Nâng cao | E-commerce App hoàn chỉnh, deploy lên Store |

---

## 📚 Tài nguyên

- [React Native Docs](https://reactnative.dev/docs/getting-started) — Tài liệu chính thức
- [Flutter Docs](https://docs.flutter.dev/) — Tài liệu chính thức Flutter
- [Expo Docs](https://docs.expo.dev/) — Framework phổ biến cho React Native
- [The Net Ninja — Flutter Tutorial](https://www.youtube.com/playlist?list=PL4cUxeGkcC9jLYyp2Aoh6hcWuxFDX6PBJ) — Video tutorial miễn phí
- [App Brewery](https://www.appbrewery.co/) — Khóa học Flutter & iOS toàn diện
