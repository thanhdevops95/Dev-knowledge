# 🎮 Game Development — Làm game từ vòng lặp tới engine

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 22/06/2026

> 🎯 *Nền tảng phát triển game: game là chương trình thời gian thực vẽ lại liên tục ~60 FPS. Học game loop + delta time, rendering 2D/3D cơ bản, physics/input/audio (vector, AABB collision), rồi ráp lại thành game 2D nhỏ bằng engine **Godot 4** (GDScript). CÓ code chạy được (GDScript Godot 4, JS minh hoạ loop/collision), nhiều sơ đồ + ví dụ xuyên suốt một game nhặt xu.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu game khác app thường ra sao + **landscape engine 2026** (Unity/Unreal/**Godot**), chọn engine đúng
- [x] Nắm **game loop** (input → update → render) + **delta time** + fixed vs variable timestep
- [x] Hiểu **rendering** 2D/3D cơ bản: hệ toạ độ, sprite vs mesh, camera, pipeline CPU→GPU, draw call
- [x] Dùng **vector + AABB collision** + xử lý input + audio cho gameplay
- [x] **Ráp một game 2D nhỏ với Godot 4**: scene tree, `_process(delta)`, `CharacterBody2D`, signal

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic (5 bài)

| # | Bài học | Trạng thái | Nội dung chính |
|---|---|---|---|
| **00** | [`Phát triển game là gì?`](./lessons/01_basic/00_what-is-game-development.md) | ✅ | Game = real-time loop, thành phần cốt lõi, engine landscape, vai trò team. |
| **01** | [`Game Loop & kiến trúc game`](./lessons/01_basic/01_game-loop-and-architecture.md) | ✅ | input→update→render, delta time, fixed/variable timestep, scene tree, ECS. |
| **02** | [`Đồ hoạ & Rendering cơ bản`](./lessons/01_basic/02_graphics-and-rendering-basics.md) | ✅ | Hệ toạ độ, sprite vs mesh, camera, pipeline CPU→GPU, draw call/batching. |
| **03** | [`Physics, Input & Audio`](./lessons/01_basic/03_physics-input-and-audio.md) | ✅ | Vector 2D, AABB collision, rigidbody/gravity, input, SFX/nhạc nền. |
| **04** | [`Làm game đầu tiên với Godot`](./lessons/01_basic/04_building-a-game-with-an-engine.md) | ✅ | Godot 4, scene tree, GDScript, CharacterBody2D, Area2D signal, export. |

---

## 🚀 Lộ trình đề xuất

Đọc tuần tự 00 → 04. Bài [01 (game loop + delta time)](./lessons/01_basic/01_game-loop-and-architecture.md) là khái niệm "vỡ lòng" quan trọng nhất — hiểu nó trước khi đụng engine. Muốn code ngay: nắm [01](./lessons/01_basic/01_game-loop-and-architecture.md) + [03 (vector/collision)](./lessons/01_basic/03_physics-input-and-audio.md) rồi vào thẳng [04 (Godot)](./lessons/01_basic/04_building-a-game-with-an-engine.md). Godot free + nhẹ, GDScript giống Python — hợp người mới.

## 🔗 Liên kết cụm liên quan

- [03_languages](../../03_languages/) — C#/C++ (Unity/Unreal) hoặc nền tảng lập trình chung.
- [ar-vr](../ar-vr/) — game engine cũng là nền cho AR/VR.
- [01_foundations](../../01_foundations/) — toán/vector, cấu trúc dữ liệu cho game.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (22/06/2026)** — Hoàn thiện cụm **Basic 5/5** (game là gì + game loop + rendering + physics/input/audio + làm game với Godot).
