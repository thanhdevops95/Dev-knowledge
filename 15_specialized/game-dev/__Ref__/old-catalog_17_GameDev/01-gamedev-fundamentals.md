# 🎮 Game Development — Phát triển game cơ bản

> `[BEGINNER → INTERMEDIATE]` — Từ ý tưởng đến game chạy được

---

## Tại sao học Game Dev?

- **Kết hợp mọi kỹ năng:** Math, physics, graphics, AI, networking, optimization
- **Thị trường lớn:** Gaming > $200B — lớn hơn cả phim + nhạc cộng lại
- **Transferable skills:** Game logic = real-time systems, simulation, AI

---

## 1. Game Loop — Vòng lặp chính

```
Mọi game đều chạy theo loop:

while (game is running) {
    processInput();     // Đọc keyboard, mouse, gamepad
    update(deltaTime);  // Cập nhật logic: vị trí, va chạm, AI
    render();           // Vẽ lên màn hình
}

60 FPS = loop chạy 60 lần/giây = 16.67ms mỗi frame
```

```javascript
// JavaScript — Canvas Game Loop
let lastTime = 0;

function gameLoop(timestamp) {
    const deltaTime = (timestamp - lastTime) / 1000;  // seconds
    lastTime = timestamp;

    processInput();
    update(deltaTime);
    render();

    requestAnimationFrame(gameLoop);  // ~60 FPS
}

requestAnimationFrame(gameLoop);
```

---

## 2. Game Engine vs Framework vs From Scratch

| | Engine | Framework | From Scratch |
|---|---|---|---|
| **Ví dụ** | Unity, Unreal, Godot | Phaser, Pygame, Love2D | Canvas, WebGL |
| **Bao gồm** | Editor + renderer + physics + audio + UI | Library + tools | Chỉ có API cơ bản |
| **Learning** | Trung bình | Dễ | Khó nhất |
| **Control** | Ít | Trung bình | Hoàn toàn |
| **Khi nào** | Game 3D, game lớn | Game 2D đơn giản | Learning, jam |

---

## 3. Các khái niệm cốt lõi

### Entity — Thực thể trong game

```javascript
class Entity {
    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.velocityX = 0;
        this.velocityY = 0;
        this.alive = true;
    }

    update(dt) {
        this.x += this.velocityX * dt;
        this.y += this.velocityY * dt;
    }

    draw(ctx) {
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }

    getBounds() {
        return {
            left: this.x,
            right: this.x + this.width,
            top: this.y,
            bottom: this.y + this.height,
        };
    }
}
```

### Collision Detection — Phát hiện va chạm

```javascript
// AABB — Axis-Aligned Bounding Box (phổ biến nhất)
function checkCollision(a, b) {
    return (
        a.x < b.x + b.width &&
        a.x + a.width > b.x &&
        a.y < b.y + b.height &&
        a.y + a.height > b.y
    );
}

// Circle collision
function circleCollision(a, b) {
    const dx = a.x - b.x;
    const dy = a.y - b.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    return distance < a.radius + b.radius;
}
```

### State Machine — Quản lý trạng thái

```javascript
// Player states: idle → running → jumping → falling → idle
class StateMachine {
    constructor() {
        this.states = {};
        this.currentState = null;
    }

    addState(name, { enter, update, exit }) {
        this.states[name] = { enter, update, exit };
    }

    change(newState) {
        if (this.currentState) this.states[this.currentState].exit?.();
        this.currentState = newState;
        this.states[newState].enter?.();
    }

    update(dt) {
        this.states[this.currentState]?.update?.(dt);
    }
}

// Sử dụng
const playerFSM = new StateMachine();
playerFSM.addState('idle', {
    enter: () => player.setAnimation('idle'),
    update: (dt) => {
        if (input.left || input.right) playerFSM.change('running');
        if (input.jump) playerFSM.change('jumping');
    },
});
playerFSM.addState('jumping', {
    enter: () => { player.velocityY = -500; player.setAnimation('jump'); },
    update: (dt) => {
        if (player.velocityY > 0) playerFSM.change('falling');
    },
});
```

---

## 4. Game Engines phổ biến

| Engine | Ngôn ngữ | Platform | Giá | Phù hợp |
|---|---|---|---|---|
| **Unity** | C# | All | Free + revenue share | Mobile, 3D, indie |
| **Unreal** | C++, Blueprint | All | Free + 5% royalty | AAA, 3D, photorealistic |
| **Godot** | GDScript, C# | All | **Free, open source** | Indie, 2D & 3D |
| **Phaser** | JavaScript | Web | Free | Web games, 2D |
| **Pygame** | Python | Desktop | Free | Learning, prototyping |

---

## 5. Ví dụ — Simple Game (HTML5 Canvas)

```html
<canvas id="game" width="800" height="600"></canvas>
<script>
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

const player = { x: 400, y: 500, w: 40, h: 40, speed: 300 };
const bullets = [];
const enemies = [];
let score = 0;
let keys = {};

document.addEventListener('keydown', e => keys[e.key] = true);
document.addEventListener('keyup', e => keys[e.key] = false);

function spawnEnemy() {
    enemies.push({
        x: Math.random() * 760, y: -40,
        w: 40, h: 40, speed: 100 + Math.random() * 100,
    });
}

function update(dt) {
    if (keys['ArrowLeft'])  player.x -= player.speed * dt;
    if (keys['ArrowRight']) player.x += player.speed * dt;
    if (keys[' '] && bullets.length < 5) {
        bullets.push({ x: player.x + 15, y: player.y, w: 10, h: 20, speed: 500 });
        keys[' '] = false;
    }
    player.x = Math.max(0, Math.min(760, player.x));

    bullets.forEach(b => b.y -= b.speed * dt);
    enemies.forEach(e => e.y += e.speed * dt);

    // Collision
    for (let i = bullets.length - 1; i >= 0; i--) {
        for (let j = enemies.length - 1; j >= 0; j--) {
            if (checkCollision(bullets[i], enemies[j])) {
                bullets.splice(i, 1);
                enemies.splice(j, 1);
                score += 10;
                break;
            }
        }
    }

    // Cleanup
    bullets.filter(b => b.y > 0);
    enemies.filter(e => e.y < 640);
}

function render() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, 800, 600);

    ctx.fillStyle = '#4ade80';
    ctx.fillRect(player.x, player.y, player.w, player.h);

    ctx.fillStyle = '#fbbf24';
    bullets.forEach(b => ctx.fillRect(b.x, b.y, b.w, b.h));

    ctx.fillStyle = '#ef4444';
    enemies.forEach(e => ctx.fillRect(e.x, e.y, e.w, e.h));

    ctx.fillStyle = '#fff';
    ctx.font = '20px monospace';
    ctx.fillText(`Score: ${score}`, 10, 30);
}

setInterval(spawnEnemy, 1000);
let last = 0;
function loop(ts) {
    const dt = (ts - last) / 1000;
    last = ts;
    update(dt);
    render();
    requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
</script>
```

---

## Các lỗi thường gặp

```
❌ Sai: Update logic dựa vào FPS (frame-dependent)
✅ Đúng: Dùng deltaTime → chạy mượt trên mọi máy

❌ Sai: Check collision mọi entity vs mọi entity (O(n²))
✅ Đúng: Spatial partitioning (quadtree, grid) → O(n log n)

❌ Sai: Bắt đầu bằng game 3D MMORPG
✅ Đúng: Bắt đầu bằng Pong → Breakout → Platformer → Rồi mới phức tạp
```

---

## Bài tập thực hành

- [ ] Build Pong game (2 paddle, 1 ball, score)
- [ ] Build Space Shooter (player, enemies, bullets, collision)
- [ ] Thêm: particle effects, sound, power-ups
- [ ] Thử Godot: build platformer đơn giản

---

## Tài nguyên thêm

- [Game Programming Patterns](https://gameprogrammingpatterns.com/) — Free book
- [Godot Docs](https://docs.godotengine.org/) — Free engine
- [CS50 Game Dev (Harvard)](https://cs50.harvard.edu/games/) — Free course
