# CSS Advanced — Layout, Animation, Variables

> **Tags:** `css` `flexbox` `grid` `animations` `custom-properties` `responsive` `performance`
> **Level:** Intermediate to Advanced | **Prerequisite:** `css/01-css-basics.md`

---

## 1. CSS Grid — Complete Guide

```css
/* Grid container */
.grid {
  display: grid;
  
  /* Define columns */
  grid-template-columns: 200px 1fr 1fr;       /* Fixed + flexible */
  grid-template-columns: repeat(4, 1fr);       /* 4 equal columns */
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));  /* Responsive! */
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));   /* auto-fit vs auto-fill */
  
  /* Define rows */
  grid-template-rows: auto 1fr auto;           /* header, main, footer */
  grid-auto-rows: 200px;                       /* Implicit rows = 200px */
  
  /* Gap */
  gap: 1rem;                 /* Both row and column */
  row-gap: 1rem;
  column-gap: 0.5rem;
  
  /* Named areas */
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
}

/* Place items using named areas */
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }

/* Grid item placement */
.item {
  grid-column: 1 / 3;         /* Span from column 1 to 3 */
  grid-column: 1 / span 2;    /* Start at 1, span 2 */
  grid-column: span 3;        /* Span 3 columns (auto start) */
  grid-row: 1 / 4;
  
  /* Alignment */
  justify-self: center;   /* Horizontal: start | end | center | stretch */
  align-self: end;        /* Vertical */
  place-self: center;     /* Shorthand: align-self justify-self */
}

/* Container-level alignment */
.grid {
  justify-items: center;    /* Align all items horizontally */
  align-items: center;      /* Align all items vertically */
  justify-content: space-between;  /* Align grid tracks horizontally */
  align-content: center;           /* Align grid tracks vertically */
}
```

### Responsive Grid Layouts
```css
/* Card grid — auto-responsive, no media queries! */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
}

/* Holy Grail Layout */
.page {
  display: grid;
  grid-template-columns: 250px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: 0;
}

/* RAM (Repeat, Auto, Minmax) pattern */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  grid-auto-rows: 250px;         /* Square cells */
  gap: 1rem;
}

/* Grid for article layout */
.article-layout {
  display: grid;
  grid-template-columns: 1fr min(65ch, 100%) 1fr;  /* ch = character width */
}
.article-layout > * {
  grid-column: 2;   /* Everything in center column */
}
.article-layout > .full-bleed {
  grid-column: 1 / -1;  /* Full width (sidebar images, etc.) */
}
```

---

## 2. Custom Properties (CSS Variables)

```css
/* Define in :root for global scope */
:root {
  /* Colors */
  --color-primary: hsl(240, 70%, 60%);
  --color-primary-light: hsl(240, 70%, 75%);
  --color-primary-dark: hsl(240, 70%, 45%);
  --color-secondary: hsl(160, 60%, 50%);
  
  /* Semantic colors */
  --color-text: hsl(0, 0%, 10%);
  --color-text-muted: hsl(0, 0%, 50%);
  --color-background: hsl(0, 0%, 100%);
  --color-surface: hsl(0, 0%, 97%);
  --color-border: hsl(0, 0%, 88%);
  
  /* Typography */
  --font-family-body: 'Inter', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-size-base: 1rem;
  --font-size-sm: 0.875rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;
  --font-size-2xl: 2rem;
  --line-height: 1.6;
  
  /* Spacing (8px base) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
  
  /* Border radius */
  --radius-sm: 0.25rem;
  --radius: 0.5rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -1px rgb(0 0 0 / 0.06);
  --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.1);
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition: 250ms ease;
  --transition-slow: 400ms ease;
  
  /* Z-index scale */
  --z-tooltip: 100;
  --z-modal: 200;
  --z-toast: 300;
}

/* Dark mode */
[data-theme="dark"],
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: hsl(0, 0%, 90%);
    --color-text-muted: hsl(0, 0%, 60%);
    --color-background: hsl(220, 15%, 8%);
    --color-surface: hsl(220, 15%, 13%);
    --color-border: hsl(220, 15%, 22%);
  }
}

/* Component using variables */
.button {
  background: var(--color-primary);
  color: white;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius);
  font-family: var(--font-family-body);
  transition: background var(--transition-fast);
}
.button:hover {
  background: var(--color-primary-dark);
}

/* Dynamic theming */
.themed-button {
  --btn-color: var(--color-primary);
  background: var(--btn-color);
}
.themed-button.danger {
  --btn-color: hsl(0, 70%, 55%);  /* Override locally */
}
```

---

## 3. Animations & Transitions

### Transitions
```css
/* Basic transition */
.button {
  transform: translateY(0);
  box-shadow: var(--shadow);
  transition: transform var(--transition-fast), 
              box-shadow var(--transition-fast);
}
.button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
.button:active {
  transform: translateY(0);
}

/* Transition properties */
transition-property: transform, opacity;
transition-duration: 300ms;
transition-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1);  /* Spring feel */
transition-delay: 0ms;
```

### Keyframe Animations
```css
/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Slide in from right */
@keyframes slideInRight {
  from { transform: translateX(100%); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.05); }
}

/* Spinner */
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Shimmer (skeleton loading) */
@keyframes shimmer {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}

/* Apply animations */
.card {
  animation: fadeIn 400ms ease-out both;
  animation-delay: calc(var(--index, 0) * 50ms);  /* Stagger with custom property */
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 600ms linear infinite;
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface) 25%,
    var(--color-border) 50%,
    var(--color-surface) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

/* Stagger animation on list items */
.list-item {
  opacity: 0;
  animation: fadeIn 400ms ease-out forwards;
}
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
/* Or with JS: element.style.setProperty('--index', i) */
```

### CSS Transitions — Respect User Preferences
```css
/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 4. Modern CSS Features

### Container Queries
```css
/* Component adjusts based on ITS OWN container, not viewport! */
.card-container {
  container-type: inline-size;
  container-name: card;   /* Optional name */
}

@container card (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
  }
  .card-image {
    width: 200px;
    flex-shrink: 0;
  }
}

@container (min-width: 600px) {
  .product {
    grid-template-columns: 1fr 1fr;
  }
}
```

### :has() Selector (Relational Pseudo-class)
```css
/* Style parent based on its children — "parent selector"! */
.card:has(img) {
  padding-top: 0;   /* Remove top padding if card has image */
}

.form-group:has(input:invalid) label {
  color: red;    /* Label red when input invalid */
}

nav:has(.nav-item:hover) .nav-item:not(:hover) {
  opacity: 0.5;  /* Dim siblings on hover */
}
```

### Logical Properties
```css
/* Physical → Logical (RTL-friendly!) */
margin-left   → margin-inline-start
margin-right  → margin-inline-end
margin-top    → margin-block-start
margin-bottom → margin-block-end

padding-left  → padding-inline-start
border-top    → border-block-start
width         → inline-size
height        → block-size
```

### CSS Nesting (Native)
```css
/* Native CSS nesting (no preprocessor needed!) */
.button {
  padding: 0.5rem 1rem;
  background: var(--color-primary);
  
  & span {     /* Nested selector */
    font-weight: bold;
  }
  
  &:hover {    /* Nested pseudo-class */
    background: var(--color-primary-dark);
  }
  
  &.large {    /* Nested modifier */
    padding: 0.75rem 1.5rem;
  }
  
  @media (max-width: 768px) {   /* Nested media query */
    width: 100%;
  }
}
```

### clamp() — Fluid Typography
```css
/* clamp(min, preferred, max) */
h1 {
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);  /* Fluid, no media queries! */
}

.container {
  width: clamp(320px, 90%, 1200px);
  padding: clamp(1rem, 5vw, 3rem);
}

/* Fluid space scale */
:root {
  --space-4: clamp(1rem, 2vw, 1.5rem);
  --space-8: clamp(2rem, 4vw, 3rem);
}
```

---

## 5. Responsive Design

```css
/* Mobile-first approach */
/* Base styles = mobile */
.container {
  padding: 1rem;
  max-width: 100%;
}

/* Tablet */
@media (min-width: 640px) {
  .container {
    padding: 1.5rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin-inline: auto;
    padding: 2rem;
  }
}

/* Common breakpoints */
/* xs: 0-639px (mobile) */
/* sm: 640px-767px (large mobile) */
/* md: 768px-1023px (tablet) */
/* lg: 1024px-1279px (laptop) */
/* xl: 1280px-1535px (desktop) */
/* 2xl: 1536px+ (large desktop) */

/* Responsive images */
img {
  max-width: 100%;
  height: auto;   /* Maintain aspect ratio */
}

/* Modern aspect-ratio */
.video-wrapper {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.square-thumbnail {
  aspect-ratio: 1;
  object-fit: cover;
}
```

---

## 6. Performance Optimization

```css
/* 1. Use transform/opacity for animations (GPU composited, no repaint) */
/* Bad: */
@keyframes bad { from { left: 0; } to { left: 100px; } }  /* triggers layout!*/
/* Good: */
@keyframes good { from { transform: translateX(0); } to { transform: translateX(100px); } }

/* 2. will-change (hint for GPU layering) */
.animated-element {
  will-change: transform, opacity;  /* Only on elements that WILL animate */
}
/* Remove when animation done: element.style.willChange = 'auto' */

/* 3. CSS containment */
.card {
  contain: layout paint;  /* Limit layout/paint scope */
}

/* 4. content-visibility (skip off-screen rendering) */
.content-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;  /* Estimated height (prevents scroll jump) */
}

/* 5. Critical CSS (inline in <head>, defer rest) */
/* Only inline above-the-fold styles */

/* 6. font-display */
@font-face {
  font-family: 'Inter';
  font-display: swap;    /* Show fallback immediately, swap when loaded */
}
```

---

## 7. Advanced Selectors

```css
/* :is() — group selectors */
:is(h1, h2, h3, h4) {
  line-height: 1.2;
  color: var(--color-text);
}

/* :where() — same as :is() but no specificity */
:where(h1, h2, h3) { margin-top: 0; }  /* Easily overridable */

/* :not() with complex selectors */
.form-control:not(:disabled):not([readonly]):hover {
  border-color: var(--color-primary);
}

/* Attribute selectors */
a[href^="https"]  { /* Starts with https */ }
a[href$=".pdf"]   { /* Ends with .pdf */ }
a[href*="example"] { /* Contains example */ }
input[type~="text"] { /* Space-separated list contains "text" */ }

/* :nth-child tricks */
li:nth-child(3n+1) { color: red; }    /* Every 3rd, starting at 1 */
li:nth-child(-n+3) { font-weight: bold; }  /* First 3 items */
li:nth-last-child(2) { color: blue; } /* 2nd from end */

/* First/last of type */
p:first-of-type { font-size: var(--font-size-lg); }
p:last-of-type { margin-bottom: 0; }
```

---

## 8. CSS Architecture — BEM

```css
/* BEM: Block__Element--Modifier */

/* Block */
.card { }

/* Elements (belong to block, double underscore) */
.card__header { }
.card__body { }
.card__footer { }
.card__image { }
.card__title { }

/* Modifiers (variant/state, double dash) */
.card--featured { }
.card--compact { }
.card--loading { }

/* Combined */
.card__title--large { }

/* In HTML: */
/*
<div class="card card--featured">
  <img class="card__image" src="...">
  <div class="card__header">
    <h2 class="card__title card__title--large">Title</h2>
  </div>
  <div class="card__body">...</div>
  <footer class="card__footer">...</footer>
</div>
*/
```

---

## 9. Utility Classes / Design Tokens Pattern

```css
/* Spacing utilities */
.mt-0 { margin-top: 0; }
.mt-1 { margin-top: var(--space-1); }
.mt-2 { margin-top: var(--space-2); }
.mt-4 { margin-top: var(--space-4); }

/* Flexbox utilities */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.gap-4 { gap: var(--space-4); }
.flex-1 { flex: 1; }

/* Text utilities */
.text-sm { font-size: var(--font-size-sm); }
.text-center { text-align: center; }
.font-bold { font-weight: 700; }
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Visibility */
.sr-only {                /* Visually hidden but accessible */
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## 10. Glassmorphism & Modern UI Effects

```css
/* Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
}

/* Gradient backgrounds */
.hero {
  background: linear-gradient(135deg, hsl(240, 80%, 55%) 0%, hsl(280, 80%, 60%) 100%);
}
.mesh-gradient {
  background-color: hsl(240, 80%, 55%);
  background-image:
    radial-gradient(at 40% 20%, hsl(28, 100%, 74%) 0px, transparent 50%),
    radial-gradient(at 80% 0%, hsl(189, 100%, 56%) 0px, transparent 50%),
    radial-gradient(at 0% 50%, hsl(355, 100%, 93%) 0px, transparent 50%);
}

/* Neumorphism */
.neu-card {
  background: #e0e5ec;
  border-radius: var(--radius-lg);
  box-shadow:
    6px 6px 16px rgba(163, 177, 198, 0.6),
    -6px -6px 16px rgba(255, 255, 255, 0.8);
}

/* Text gradient */
.gradient-text {
  background: linear-gradient(135deg, hsl(240, 80%, 55%), hsl(280, 80%, 60%));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

*Tài liệu liên quan: `css/01-css-basics.md` | `html/02-html-semantics.md` | `react/04-css-in-js.md`*
