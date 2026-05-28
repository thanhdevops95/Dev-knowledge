# 🎨 CSS — Tạo kiểu cho Web

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Làm cho web đẹp và responsive

---

## CSS là gì?

**CSS (Cascading Style Sheets)** điều khiển _giao diện_ của HTML: màu sắc, font chữ, khoảng cách, bố cục, animation...

---

## Cách thêm CSS vào HTML

```html
<!-- 1. External (khuyên dùng) -->
<link rel="stylesheet" href="styles.css">

<!-- 2. Internal -->
<style>
    body { margin: 0; }
</style>

<!-- 3. Inline (tránh dùng) -->
<p style="color: red;">Text</p>
```

---

## Selectors

```css
/* Element */
p { color: blue; }

/* Class */
.card { border-radius: 8px; }

/* ID */
#header { height: 60px; }

/* Attribute */
input[type="email"] { border: 2px solid blue; }
a[href^="https"] { color: green; }  /* href bắt đầu bằng https */

/* Pseudo-class */
a:hover { text-decoration: underline; }
li:first-child { font-weight: bold; }
li:nth-child(2n) { background: #f0f0f0; }  /* chẵn */
input:focus { outline: 2px solid blue; }
button:disabled { opacity: 0.5; }
p:not(.special) { color: gray; }

/* Pseudo-element */
p::first-line { font-variant: small-caps; }
.quote::before { content: '"'; }
.quote::after { content: '"'; }

/* Combinators */
.parent > .child { }          /* Direct child */
.prev + .next { }             /* Adjacent sibling */
.item ~ .sibling { }          /* General sibling */
.ancestor .descendant { }     /* Descendant */
```

---

## Box Model ⭐

```
┌─────────────────────────────┐
│          MARGIN             │
│  ┌─────────────────────┐   │
│  │       BORDER        │   │
│  │  ┌───────────────┐  │   │
│  │  │    PADDING    │  │   │
│  │  │  ┌─────────┐  │  │   │
│  │  │  │ CONTENT │  │  │   │
│  │  │  └─────────┘  │  │   │
│  │  └───────────────┘  │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

```css
.box {
    /* Content */
    width: 200px;
    height: 100px;

    /* Padding */
    padding: 16px;                          /* Tất cả 4 phía */
    padding: 8px 16px;                      /* top/bottom left/right */
    padding: 4px 8px 12px 16px;            /* top right bottom left */

    /* Border */
    border: 2px solid #333;
    border-radius: 8px;
    border-top: 1px dashed red;

    /* Margin */
    margin: 24px auto;                      /* auto căn giữa */

    /* QUAN TRỌNG: box-sizing */
    box-sizing: border-box;  /* width bao gồm padding + border */
}

/* Áp dụng cho toàn trang (best practice) */
*, *::before, *::after {
    box-sizing: border-box;
}
```

---

## Flexbox ⭐

```css
.container {
    display: flex;

    /* Hướng */
    flex-direction: row;          /* row | row-reverse | column | column-reverse */

    /* Căn chỉnh trục chính */
    justify-content: center;      /* flex-start | flex-end | center | space-between | space-around | space-evenly */

    /* Căn chỉnh trục phụ */
    align-items: center;          /* flex-start | flex-end | center | stretch | baseline */

    /* Xuống dòng */
    flex-wrap: wrap;              /* nowrap | wrap | wrap-reverse */

    /* Gap */
    gap: 16px;
    gap: 16px 24px;               /* row-gap column-gap */
}

.item {
    flex: 1;                      /* Tự co giãn */
    flex: 0 0 200px;             /* flex-grow flex-shrink flex-basis */
    align-self: flex-end;        /* Override align-items cho item này */
    order: 2;                    /* Thứ tự hiển thị */
}
```

---

## CSS Grid ⭐

```css
.grid {
    display: grid;

    /* Định nghĩa columns */
    grid-template-columns: 1fr 2fr 1fr;
    grid-template-columns: repeat(3, 1fr);
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));

    /* Định nghĩa rows */
    grid-template-rows: auto 1fr auto;

    /* Gap */
    gap: 24px;

    /* Named areas */
    grid-template-areas:
        "header header header"
        "sidebar main main"
        "footer footer footer";
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }

/* Vị trí item thủ công */
.item {
    grid-column: 1 / 3;          /* Từ line 1 đến line 3 */
    grid-column: span 2;         /* Chiếm 2 columns */
    grid-row: 2 / 4;
}
```

---

## Responsive Design

```css
/* Mobile-first approach (khuyên dùng) */

/* Mobile (default) */
.container {
    padding: 16px;
    width: 100%;
}

/* Tablet: 768px trở lên */
@media (min-width: 768px) {
    .container {
        padding: 24px;
        max-width: 768px;
        margin: 0 auto;
    }
}

/* Desktop: 1024px trở lên */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        padding: 32px;
    }
}

/* Responsive typography */
h1 {
    font-size: clamp(1.5rem, 4vw, 3rem);  /* min, preferred, max */
}

/* Responsive images */
img {
    max-width: 100%;
    height: auto;
}
```

---

## CSS Variables (Custom Properties)

```css
/* Định nghĩa ở :root (global) */
:root {
    /* Colors */
    --color-primary: #6366f1;
    --color-primary-dark: #4f46e5;
    --color-background: #0f0f23;
    --color-surface: #1e1e3f;
    --color-text: #e2e8f0;
    --color-text-muted: #94a3b8;

    /* Typography */
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --font-size-base: 1rem;
    --line-height: 1.6;

    /* Spacing */
    --space-1: 4px;
    --space-2: 8px;
    --space-4: 16px;
    --space-8: 32px;

    /* Borders */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 16px;
    --radius-full: 9999px;

    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.2);

    /* Transitions */
    --transition: 200ms ease;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
    :root {
        --color-background: #0f0f23;
        --color-text: #e2e8f0;
    }
}

/* Sử dụng */
.button {
    background: var(--color-primary);
    color: var(--color-text);
    border-radius: var(--radius-md);
    transition: background var(--transition);
}

.button:hover {
    background: var(--color-primary-dark);
}
```

---

## Animations & Transitions

```css
/* Transition — Hiệu ứng khi thay đổi state */
.button {
    transition: all 200ms ease;
    /* property duration timing-function delay */
    transition: background 200ms ease, transform 150ms ease;
}

.button:hover {
    background: #4f46e5;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

/* Keyframe Animation */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.card {
    animation: fadeIn 400ms ease both;
}

.loader {
    animation: spin 1s linear infinite;
}

/* CSS Transform */
.element {
    transform: translateX(20px) translateY(-10px);
    transform: scale(1.05);
    transform: rotate(45deg);
    transform: skewX(10deg);
}
```

---

## Best Practices

```css
/* 1. Đặt base styles */
*, *::before, *::after { box-sizing: border-box; }
body {
    margin: 0;
    font-family: var(--font-sans);
    line-height: 1.6;
    color: var(--color-text);
    background: var(--color-background);
}

/* 2. Mobile-first responsive */
/* 3. Dùng CSS Variables cho design tokens */
/* 4. BEM hoặc utility-first naming convention */

/* BEM: Block__Element--Modifier */
.card { }
.card__header { }
.card__body { }
.card--featured { }

/* 5. Tránh magic numbers */
/* ❌ */
.element { margin-top: 37px; }
/* ✅ */
.element { margin-top: var(--space-8); }
```

---

## Bài tập thực hành

- [ ] Xây dựng layout 3 cột với Flexbox và với Grid
- [ ] Tạo dark mode toggle thuần CSS
- [ ] Clone UI của một component: card, button, navbar
- [ ] Tạo animation loading spinner và page transition

---

## Tài nguyên thêm

- [CSS Tricks](https://css-tricks.com/) — Tricks và A Complete Guide to Flexbox/Grid
- [MDN CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) — Tài liệu chính thức
- [Flexbox Froggy](https://flexboxfroggy.com/) — Game học Flexbox
- [Grid Garden](https://cssgridgarden.com/) — Game học CSS Grid
- [Animista](https://animista.net/) — CSS Animations library
