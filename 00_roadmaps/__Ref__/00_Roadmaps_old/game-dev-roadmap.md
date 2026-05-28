# 🎮 Lộ trình Game Developer

> `[BEGINNER → ADVANCED]` — Xem trước [Tổng quan Lộ trình](./00-overview.md)

---

## Tại sao Game Dev?

Game development là nơi giao nhau của nghệ thuật và kỹ thuật — bạn vừa là lập trình viên, vừa là nhà thiết kế trải nghiệm. Mỗi game là một thế giới thu nhỏ với vật lý, AI, đồ họa, và hàng triệu trạng thái cần quản lý. Đây là lĩnh vực đòi hỏi kiến thức rộng nhất trong software engineering.

Ngành game toàn cầu vượt cả Hollywood về doanh thu. Từ indie game một người làm đến AAA studio hàng trăm người — cơ hội luôn có cho mọi cấp độ.

---

## Chọn Engine

| Tiêu chí | Unity | Unreal Engine | Godot | Web (Three.js) |
|---|---|---|---|---|
| Ngôn ngữ | C# | C++ / Blueprints | GDScript / C# | JavaScript/TS |
| Độ khó học | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ |
| Platform | All | All | All | Browser/Mobile |
| Use case | Mobile, Indie, VR | AAA, FPS, Open World | Indie, 2D, Learning | Web games, 3D web |
| Giá | Free (có điều kiện) | Free (5% royalty) | 100% miễn phí | Miễn phí |

---

## Sơ đồ lộ trình

```
Game Concepts (Game loop, Physics, Input)
    │
    ▼
Chọn Engine
    │
    ├──► Unity (C#)
    ├──► Unreal (C++/Blueprints)
    ├──► Godot (GDScript)
    └──► Web (Three.js/Phaser)
            │
            ▼
    Math & Physics (Vectors, Collisions)
            │
            ▼
    Gameplay (Input, UI, Audio, Animation)
            │
            ▼
    Advanced (AI, Networking, Shaders)
            │
            ▼
    Publishing (Steam, App Store, itch.io)
```

---

## Giai đoạn 1 — Game Concepts

- [ ] Game Loop fundamentals → [../17-GameDev/concepts/01-game-loop-fundamentals.md](../17-GameDev/concepts/01-game-loop-fundamentals.md)
- [ ] Physics cơ bản cho game → [../17-GameDev/concepts/02-physics-fundamentals.md](../17-GameDev/concepts/02-physics-fundamentals.md)
- [ ] Game networking → [../17-GameDev/concepts/03-game-networking-fundamentals.md](../17-GameDev/concepts/03-game-networking-fundamentals.md)
- [ ] Entity Component System (ECS) pattern

---

## Giai đoạn 2 — Chọn Engine & Học cơ bản

### Unity (C#)
- [ ] Unity basics → [../17-GameDev/unity/01-unity-basics.md](../17-GameDev/unity/01-unity-basics.md)
- [ ] Scenes, GameObjects, Components, Prefabs

### Unreal Engine (C++ / Blueprints)
- [ ] Unreal basics → [../17-GameDev/unreal/01-unreal-basics.md](../17-GameDev/unreal/01-unreal-basics.md)
- [ ] Blueprints visual scripting, Actors, Levels

### Godot (GDScript)
- [ ] Godot basics → [../17-GameDev/godot/01-godot-basics.md](../17-GameDev/godot/01-godot-basics.md)
- [ ] Nodes, Scenes, Signals, GDScript syntax

### Web Games
- [ ] Three.js cơ bản → [../17-GameDev/web-game/01-threejs-basics.md](../17-GameDev/web-game/01-threejs-basics.md)
- [ ] Phaser cơ bản → [../17-GameDev/web-game/02-phaser-basics.md](../17-GameDev/web-game/02-phaser-basics.md)

---

## Giai đoạn 3 — Math & Physics

- [ ] Linear algebra: Vectors, Matrices, Transformations
- [ ] Collision detection (AABB, Circle, SAT)
- [ ] Raycasting, Trigonometry cho game
- [ ] Interpolation (Lerp, Slerp) và Easing functions

---

## Giai đoạn 4 — Gameplay Systems

- [ ] Input handling (keyboard, mouse, gamepad, touch)
- [ ] UI systems (HUD, menus, inventory)
- [ ] Audio (SFX, music, spatial audio)
- [ ] Animation (sprite, skeletal, state machines)
- [ ] Camera systems (follow, cinematic, shake)

---

## Giai đoạn 5 — Advanced Topics

- [ ] Game AI (Finite State Machine, Behavior Trees, A* pathfinding)
- [ ] Multiplayer networking (client-server, prediction, lag compensation)
- [ ] Shaders & VFX (particle systems, post-processing)
- [ ] Procedural generation (terrain, dungeons, loot)

---

## Giai đoạn 6 — Publishing

- [ ] Build & optimization (draw calls, LOD, object pooling)
- [ ] Steam, itch.io, App Store, Google Play
- [ ] Marketing, trailers, community building
- [ ] Analytics & monetization

---

## 📦 Project thực hành

| Giai đoạn | Project |
|---|---|
| Sau basics | Pong hoặc Breakout clone |
| Sau Physics | Platformer 2D (Mario-style) |
| Sau Gameplay | Top-down RPG với inventory & dialogue |
| Sau AI | Tower defense hoặc RTS đơn giản |
| Nâng cao | Multiplayer game, publish lên Steam/itch.io |

---

## 📚 Tài nguyên

- [Unity Learn](https://learn.unity.com/) — Tutorials chính thức từ Unity
- [Unreal Engine Learning](https://dev.epicgames.com/community/unreal-engine/learning) — Tài liệu chính thức Unreal
- [GDQuest](https://www.gdquest.com/) — Godot tutorials chất lượng cao
- [Game Programming Patterns](https://gameprogrammingpatterns.com/) — Sách miễn phí về design patterns trong game
- [Kenney Assets](https://kenney.nl/) — Free game assets cho prototyping
