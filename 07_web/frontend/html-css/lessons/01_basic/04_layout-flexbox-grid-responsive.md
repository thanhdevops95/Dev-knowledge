# 🎓 Layout — Flexbox, Grid, Responsive Design

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [CSS Fundamentals](03_css-fundamentals.md)

> 🎯 *Master 2 layout modern: **Flexbox** (1D — row hoặc column), **Grid** (2D — row + column). Plus **responsive design** (media queries, container queries, mobile-first). Sau bài này build được layout production: navbar, card grid, dashboard, holy grail.*

## 🎯 Sau bài này bạn sẽ

- [ ] Master **Flexbox** — `display: flex` + flex container/items properties
- [ ] Master **CSS Grid** — `display: grid` + template areas
- [ ] Phân biệt **khi nào Flexbox** vs **khi nào Grid**
- [ ] **Responsive design** — mobile-first + breakpoints
- [ ] Dùng **media queries** + **container queries** modern
- [ ] **Holy Grail layout** + 5 layout pattern phổ biến
- [ ] Hiểu **fluid typography** với `clamp()`
- [ ] Tránh 5 layout pitfall

---

## Tình huống — Bạn viết homepage Acme Shop responsive

Bạn cần layout:
```
Mobile (1 col):              Desktop (4 col):

┌─────────┐                  ┌──┬─────────────┬──┐
│ Header  │                  │L │   Header    │R │
├─────────┤                  ├──┼─────────────┼──┤
│ Nav     │                  │N │             │N │
├─────────┤                  │a │   Main      │a │
│ Main    │                  │v │             │v │
├─────────┤                  │  │             │  │
│ Sidebar │                  ├──┴─────────────┴──┤
├─────────┤                  │      Footer       │
│ Footer  │                  └───────────────────┘
└─────────┘
```

Bạn thử CSS cũ — `float`, `position: absolute`:
- 😱 Element chồng lên nhau.
- 😱 Responsive vỡ ở mobile.
- 😱 Vertical center button → search Google 10 giải pháp hacky.

Senior chỉ:
> *"Đó là 2010 style. Modern 2026: **Flexbox** cho 1 chiều (navbar, button row), **Grid** cho 2 chiều (page layout). 1 dòng CSS = solve. Plus **mobile-first** approach."*

Bạn ngơ:
- **Flexbox** với **Grid** khác sao?
- **Mobile-first** là gì?
- Khi nào media query, khi nào container query?
- Vertical center bằng CSS — bao nhiêu cách?

→ Bài này dạy đầy đủ.

---

## 1️⃣ Flexbox — 1D layout (row OR column)

### Setup container

Bật Flexbox **chỉ cần 1 dòng**: `display: flex` trên element cha. Mọi direct child tự động trở thành flex items, xếp ngang theo row mặc định. Đây là điểm khởi đầu mọi layout flex:

```css
.container {
  display: flex;            /* Bật flex */
}
```

→ Mọi direct child trở thành **flex items**, xếp **hàng ngang** mặc định.

### Container properties

5 property trên **container** điều khiển layout của toàn bộ flex items — direction (ngang/dọc), wrap, alignment 2 trục, gap. Hiểu 5 cái này là **giải được 80% layout case** trong web:

```css
.container {
  display: flex;

  /* Hướng */
  flex-direction: row;            /* row | row-reverse | column | column-reverse */

  /* Wrap khi không đủ space */
  flex-wrap: nowrap;               /* nowrap | wrap | wrap-reverse */

  /* Shorthand row + nowrap */
  flex-flow: row wrap;

  /* Căn theo TRỤC CHÍNH (main axis = direction) */
  justify-content: flex-start;     /* flex-start | flex-end | center
                                      | space-between | space-around | space-evenly */

  /* Căn theo TRỤC PHỤ (cross axis = vuông góc) */
  align-items: stretch;             /* stretch | flex-start | flex-end | center | baseline */

  /* Khoảng cách giữa items */
  gap: 1rem;                         /* row-gap + column-gap shorthand */
}
```

### Item properties

3 property trên **flex item** điều khiển từng item riêng — `align-self` override container, `order` đổi thứ tự visual, `flex` (shorthand grow/shrink/basis) chia space. Đây là cách fine-tune từng item:

```css
.item {
  /* Lệch theo cross axis (override align-items của container) */
  align-self: center;

  /* Thứ tự — default 0, càng lớn càng cuối */
  order: 2;

  /* 3 shorthand: grow, shrink, basis */
  flex: 1 1 200px;        /* grow=1 (chiếm space thừa), shrink=1, basis=200px */
  flex: 1;                  /* = flex: 1 1 0% — grow đều */
  flex: none;               /* = flex: 0 0 auto — không grow/shrink */
}
```

### Patterns Flexbox thường dùng

#### Navbar — logo trái, menu phải

Pattern phổ biến nhất Flexbox: navbar với logo bên trái + menu bên phải. Trick là `justify-content: space-between` đẩy 2 child ra 2 đầu, `align-items: center` căn dọc:

```css
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}
```

```html
<nav>
  <div class="logo">Acme Shop</div>
  <ul class="menu">
    <li>Home</li>
    <li>Products</li>
  </ul>
</nav>
```

#### Vertical center (cuối cùng dễ)

Trước Flexbox, **vertical center** là nightmare của CSS — phải dùng table, hack với position absolute, translateY. Flexbox giải quyết trong **3 dòng**. Đây là "killer pattern" khiến Flexbox phổ biến:

```css
.center {
  display: flex;
  justify-content: center;    /* horizontal */
  align-items: center;         /* vertical */
  height: 100vh;
}
```

→ Trước 2015, vertical center là **CSS interview question huyền thoại**. Giờ 3 dòng.

#### Card row — equal width

```css
.card-row {
  display: flex;
  gap: 1rem;
}
.card {
  flex: 1;                    /* Mỗi card chia đều space */
}
```

#### Sticky footer

```css
body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
main {
  flex: 1;                    /* Push footer xuống đáy */
}
```

---

## 2️⃣ CSS Grid — 2D layout (row + column)

### Setup container

```css
.grid {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;       /* 3 cột: 200px, rest chia đôi */
  grid-template-rows: auto 1fr auto;            /* 3 row: auto, fill, auto */
  gap: 1rem;
}
```

### `grid-template-columns` syntax

```css
grid-template-columns: 100px 200px 100px;      /* Fixed */
grid-template-columns: 1fr 2fr 1fr;             /* Fraction — chia tỉ lệ */
grid-template-columns: repeat(3, 1fr);          /* = 1fr 1fr 1fr */
grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));  /* Responsive! */
grid-template-columns: 200px auto 1fr;          /* Mix */
```

### `auto-fill` / `auto-fit` — **Magic responsive 1 dòng**

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
```

→ Mỗi card **tối thiểu 250px**, fill nhiều column nhất có thể. Resize browser → tự thêm/bớt cột. **Không cần media query!**

| Function | Khi |
|---|---|
| `auto-fill` | Tạo column dù không có item (giữ structure) |
| `auto-fit` | Collapse empty column (mở rộng item) |

### Item placement

```css
.item {
  grid-column: 1 / 3;            /* Từ line 1 đến line 3 (= 2 column) */
  grid-row: 2 / 4;                /* Row 2-3 */
}

/* Shorthand */
.item {
  grid-column: span 2;            /* = chiếm 2 column */
  grid-row: span 2;
}
```

### Named template areas — hay nhất

```css
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  gap: 1rem;
  min-height: 100vh;
}

header { grid-area: header; }
nav    { grid-area: nav; }
main   { grid-area: main; }
aside  { grid-area: aside; }
footer { grid-area: footer; }
```

→ **Holy Grail layout** trong 10 dòng CSS. Visual, dễ đọc, dễ rearrange.

### Responsive Holy Grail

```css
.layout {
  display: grid;
  grid-template-areas:
    "header"
    "nav"
    "main"
    "aside"
    "footer";
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .layout {
    grid-template-areas:
      "header header header"
      "nav    main   aside"
      "footer footer footer";
    grid-template-columns: 200px 1fr 200px;
  }
}
```

→ Mobile single column → desktop 3 column. Đơn giản hơn nhiều so với 2010.

---

## 3️⃣ Flexbox vs Grid — khi nào dùng cái nào?

| Use case | Chọn |
|---|---|
| **Navbar** (logo + menu) | Flexbox |
| **Button row** | Flexbox |
| **Card row** (1 chiều) | Flexbox |
| **Vertical center** | Flexbox |
| **Form fields stack** | Flexbox |
| **Page layout** (header/nav/main/footer 2D) | Grid |
| **Photo gallery** (responsive cards) | Grid + `auto-fill` |
| **Dashboard** (widgets nhiều kích thước) | Grid |
| **Magazine layout** | Grid |

### Quy tắc

```
1 chiều (row hoặc column) → Flexbox
2 chiều (row × column)    → Grid
```

→ **Có thể combine**: Grid cho page layout, Flexbox cho từng card bên trong.

---

## 4️⃣ Responsive design — Mobile-first

### Approach: Mobile-first

```css
/* Mobile (default) — viết style đơn giản */
.card {
  padding: 1rem;
  font-size: 1rem;
}

/* Tablet (768px+) — add complexity */
@media (min-width: 768px) {
  .card {
    padding: 2rem;
    font-size: 1.125rem;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .card {
    padding: 3rem;
    font-size: 1.25rem;
  }
}
```

### Vs Desktop-first (cũ — tránh)

```css
.card { padding: 3rem; }
@media (max-width: 1024px) { .card { padding: 2rem; } }
@media (max-width: 768px) { .card { padding: 1rem; } }
```

→ Mobile-first **better**: mobile load nhanh hơn (CSS đơn giản default), progressive enhancement, modern norm.

### Breakpoints phổ thông 2026

```css
/* Tailwind default — adopt cũng OK */
sm: 640px      Mobile landscape, small tablet
md: 768px      Tablet
lg: 1024px      Desktop
xl: 1280px      Large desktop
2xl: 1536px     Wide desktop
```

→ Đừng over-engineer. 2-3 breakpoint thường đủ.

### `@media` features

```css
@media (min-width: 768px) { ... }
@media (max-width: 1024px) { ... }
@media (min-width: 768px) and (max-width: 1023px) { ... }
@media (orientation: landscape) { ... }
@media (prefers-color-scheme: dark) { ... }       /* Dark mode! */
@media (prefers-reduced-motion: reduce) { ... }     /* A11y — disable animation */
@media print { ... }                                 /* Print styles */
```

### Dark mode tự động

```css
:root {
  --bg: white;
  --text: black;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #111;
    --text: #f9f9f9;
  }
}

body {
  background: var(--bg);
  color: var(--text);
}
```

→ Tự đổi theo OS preference. Plus toggle JS-driven nếu cần.

---

## 5️⃣ Container queries — Hot 2023

**Vấn đề media query**: dựa vào **viewport** (browser width). Nhưng card trong sidebar không cần biết viewport — chỉ cần biết **container nó ở** rộng bao nhiêu.

```css
/* Component card */
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: flex;
  flex-direction: column;          /* Default */
}

/* Khi container rộng > 400px, đổi card thành row */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
    align-items: center;
  }
}
```

→ Card **tự responsive theo container** — bất kể viewport. Component truly portable.

→ Support: Chrome/Safari/Firefox từ 2023. **Default 2026** thay nhiều media query.

---

## 6️⃣ Fluid typography với `clamp()`

```css
h1 {
  /* clamp(min, preferred, max) */
  font-size: clamp(1.5rem, 4vw, 3rem);
}

.container {
  width: clamp(320px, 100%, 1200px);
  padding: clamp(1rem, 3vw, 3rem);
}
```

| Argument | Ý nghĩa |
|---|---|
| `min` | Không nhỏ hơn (mobile) |
| `preferred` | Dynamic giá trị (theo viewport) |
| `max` | Không lớn hơn (desktop) |

→ **Smooth scale** từ mobile → desktop **không cần breakpoint**. Modern 2026 thay nhiều `@media` cho font size.

---

## 7️⃣ 5 layout pattern phổ biến

### Pattern 1 — Sticky header

```css
header {
  position: sticky;
  top: 0;
  background: white;
  z-index: 100;
}
```

→ Header cố định khi scroll. CSS native, không JS.

### Pattern 2 — Sticky footer

```css
body {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
}
main { /* Tự fill space */ }
```

### Pattern 3 — Card grid responsive

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
```

### Pattern 4 — Centered content with max-width

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}
```

### Pattern 5 — Aspect ratio (image / video)

```css
.video-thumb {
  aspect-ratio: 16 / 9;
  width: 100%;
  object-fit: cover;
}
```

→ Modern thay cho **padding hack** cũ.

---

## 8️⃣ Bạn viết layout full page

```html
<body>
  <div class="layout">
    <header class="header">Acme Shop</header>
    <nav class="nav">Menu</nav>
    <main class="main">
      <div class="card-grid">
        <article class="card">iPhone 15</article>
        <article class="card">AirPods</article>
        <article class="card">MacBook</article>
        <!-- ... -->
      </div>
    </main>
    <aside class="aside">Sidebar</aside>
    <footer class="footer">© 2026</footer>
  </div>
</body>
```

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: system-ui, sans-serif;
  line-height: 1.5;
}

/* Mobile-first layout */
.layout {
  display: grid;
  grid-template-areas:
    "header"
    "nav"
    "main"
    "aside"
    "footer";
  grid-template-rows: auto auto 1fr auto auto;
  min-height: 100vh;
  gap: 1rem;
}

/* Desktop layout */
@media (min-width: 1024px) {
  .layout {
    grid-template-areas:
      "header header header"
      "nav    main   aside"
      "footer footer footer";
    grid-template-columns: 200px 1fr 200px;
    grid-template-rows: auto 1fr auto;
  }
}

.header { grid-area: header; padding: 1rem; background: #2563eb; color: white; }
.nav    { grid-area: nav;    padding: 1rem; background: #f3f4f6; }
.main   { grid-area: main;   padding: clamp(1rem, 3vw, 3rem); }
.aside  { grid-area: aside;  padding: 1rem; background: #f3f4f6; }
.footer { grid-area: footer; padding: 1rem; background: #1f2937; color: white; text-align: center; }

/* Card grid trong main */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.card {
  padding: 1.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-2px);
  transition: all 0.2s ease;
}
```

→ Full layout production-ready với 40 dòng CSS. Responsive mobile/desktop. Tự dark mode-ready nếu thêm CSS variables.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Dùng `float`** cho layout → 2010 style. Giờ là Flexbox/Grid.
2. **`position: absolute`** cho layout thường → element chồng nhau. Chỉ dùng cho overlay (modal, tooltip).
3. **Không `box-sizing: border-box`** → tính width sai → vỡ. Reset đầu CSS.
4. **`100vh` mobile vỡ** → mobile browser có address bar dynamic → `100vh` lớn hơn screen. Dùng `100dvh` (dynamic viewport) modern.
5. **Quên `gap`** giữa items → margin hack đầu cuối phức tạp. Flexbox/Grid đều support `gap`.

---

## 🧠 Tự kiểm tra (Self-check)

1. **Flexbox** vs **Grid** — chọn cái nào cho navbar? Cho page layout?
2. Viết CSS center 1 div theo cả 2 trục — 3 dòng?
3. Card grid responsive **không media query** — code thế nào?
4. **Mobile-first** vs **desktop-first** — recommend cái nào 2026?
5. **`clamp(1rem, 2vw, 2rem)`** nghĩa là gì?

<details>
<summary>Gợi ý đáp án</summary>

1. **Navbar** (1 chiều: logo + menu) → **Flexbox**. **Page layout** (2 chiều: header/nav/main/footer) → **Grid**.

2. ```css
   .center {
     display: flex;
     justify-content: center;
     align-items: center;
   }
   ```
   (Cần `height` để có space vertical, vd `min-height: 100vh`)

3. ```css
   .grid {
     display: grid;
     grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
     gap: 1rem;
   }
   ```
   `auto-fill + minmax()` = magic responsive — items min 280px, fill column tối đa, resize tự đổi count.

4. **Mobile-first** — viết default mobile, add complexity với `@media (min-width)`. Better: mobile load nhanh hơn (CSS đơn giản default), progressive enhancement, ~60% traffic 2026 từ mobile.

5. `clamp(min, preferred, max)` = giá trị nằm trong khoảng [min, max], dùng `preferred` để dynamic. Cụ thể: tối thiểu `1rem` (16px), max `2rem` (32px), khoảng giữa scale theo viewport (`2vw`). Smooth font scale mobile → desktop **không cần `@media`**.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Flexbox quick

```css
.container {
  display: flex;
  flex-direction: row | column;
  justify-content: center | space-between | space-around | flex-end;
  align-items: center | flex-start | stretch;
  gap: 1rem;
  flex-wrap: wrap;
}

.item {
  flex: 1;                        /* Grow equal */
  flex: 0 0 200px;                /* Fixed 200px, no grow */
  align-self: center;
  order: 2;
}
```

### Grid quick

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-template-rows: auto 1fr auto;
  gap: 1rem;
  grid-template-areas: "header header" "nav main";
}

.item {
  grid-column: span 2;
  grid-row: 1 / 3;
  grid-area: header;
}
```

### Responsive

```css
/* Mobile-first */
.thing { padding: 1rem; }

@media (min-width: 768px) { .thing { padding: 2rem; } }
@media (min-width: 1024px) { .thing { padding: 3rem; } }
@media (prefers-color-scheme: dark) { ... }

/* Fluid */
font-size: clamp(1rem, 2vw, 1.5rem);
width: clamp(320px, 100%, 1200px);

/* Container query */
.card { container-type: inline-size; }
@container (min-width: 400px) { .card { flex-direction: row; } }
```

### Center methods

```css
/* Flex */
display: flex; justify-content: center; align-items: center;

/* Grid */
display: grid; place-items: center;

/* Absolute */
position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Flexbox** | 1D layout (row or column) — `display: flex` |
| **CSS Grid** | 2D layout (row + column) — `display: grid` |
| **Main axis / Cross axis** | Flex direction / vuông góc |
| **Flex grow / shrink / basis** | Control item size |
| **Grid track** | Row hoặc column trong grid |
| **`fr`** | Fraction unit — chia space còn lại |
| **`gap`** | Khoảng cách items (Flex + Grid) |
| **Grid template areas** | Named layout |
| **`auto-fill` / `auto-fit`** | Responsive grid magic |
| **Media query** | `@media (...)` responsive theo viewport |
| **Container query** | `@container (...)` responsive theo container |
| **Mobile-first** | Viết default mobile, add desktop với `min-width` |
| **`clamp(min, ideal, max)`** | Fluid sizing without breakpoints |
| **Holy Grail layout** | Classic: header + nav + main + aside + footer |
| **Sticky positioning** | `position: sticky` — scroll cố định |
| **`dvh` / `lvh` / `svh`** | Dynamic / Large / Small viewport height (mobile-safe) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [CSS Fundamentals — Selectors, Specificity, Box Model](03_css-fundamentals.md)
- ↑ **Về cụm:** [html-css README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [MDN — Flexbox guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)
- 📖 [MDN — CSS Grid guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)
- 📖 [Flexbox Froggy](https://flexboxfroggy.com/) — interactive game
- 📖 [Grid Garden](https://cssgridgarden.com/) — interactive game
- 📖 [CSS-Tricks — Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- 📖 [Every Layout](https://every-layout.dev/) — best practice patterns

---

> 🎯 *Cluster html-css basic 5/5 đóng. Bạn build được trang responsive đầy đủ. Bài kế tiếp ngoài cluster: **JavaScript DOM** (cluster `javascript-dom/`) — thêm interactivity. Hoặc **React** (cluster `react/`) — component-based.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `html-css/` lesson 5/5. Cover: Flexbox 1D (container + item properties + patterns) + Grid 2D (template areas + grid-template-columns/rows + responsive auto-fit) + media queries breakpoints + mobile-first + container queries + position properties.
- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước các mục Setup flex, Container properties, Item properties, Navbar pattern, Vertical center. Chuẩn hoá tên thương hiệu ví dụ thành `Acme Shop`. Thêm mục Changelog.
