# 🎨 Lộ trình Frontend Developer

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** `[BEGINNER → ADVANCED]`
> **Tags:** `[MUST-KNOW]` — Từ HTML đến React/Vue chuyên nghiệp
> **Prerequisite:** Đã nắm kiến thức nền tảng ([00-overview.md](./00-overview.md))

---

## Tại sao học Frontend?

Frontend Developer là người biến thiết kế thành sản phẩm sống — những gì người dùng nhìn thấy, chạm vào và tương tác. Hãy nghĩ Frontend như người trang trí nội thất: kiến trúc sư (Backend) dựng khung nhà, nhưng Frontend quyết định trải nghiệm khi bạn bước vào — bố cục, màu sắc, ánh sáng, sự tiện nghi. Một ngày làm việc của FE developer bao gồm: code giao diện, đảm bảo responsive trên mọi thiết bị, tối ưu tốc độ tải trang, và cộng tác với designer + backend team.

---

## Sơ đồ lộ trình

```
HTML/CSS ──► JavaScript ──► TypeScript ──► React / Vue ──► State Mgmt
   │                                           │              │
   ▼                                           ▼              ▼
Accessibility                              Next.js /      Zustand /
  & SEO                                    Nuxt.js        TanStack Query
                                               │
                         ┌─────────────────────┤
                         ▼                     ▼
                    Build Tools           Testing
                   (Vite, npm)        (Vitest, Playwright)
                         │                     │
                         └──────────┬──────────┘
                                    ▼
                            Performance & SSR
                                    │
                                    ▼
                          Nâng cao (Tailwind, PWA,
                          Micro-FE, WebAssembly)
```

---

## Giai đoạn 1 — Nền tảng Web (HTML, CSS, JavaScript)

### HTML
- [ ] Semantic elements, forms, tables, metadata → [html basics](../06-Frontend/html/01-html-basics.md)
- [ ] HTML nâng cao: canvas, web components → [html advanced](../06-Frontend/html/02-html-advanced.md)
- [ ] Accessibility cơ bản (ARIA, screen reader) → [a11y basics](../06-Frontend/accessibility/01-a11y-basics.md)

### CSS
- [ ] Box model, Flexbox, Grid, responsive design → [css basics](../06-Frontend/css/01-css-basics.md)
- [ ] Variables, custom properties, nesting → [css advanced](../06-Frontend/css/02-css-advanced.md)
- [ ] SASS / SCSS preprocessor → [sass scss basics](../06-Frontend/css/03-sass-scss-basics.md)
- [ ] Animations & transitions → [animation fundamentals](../06-Frontend/css/04-animation-fundamentals.md)

### JavaScript
- [ ] Syntax, DOM manipulation, async/await, ES6+ → [js basics](../05-Languages/javascript/01-javascript-basics.md)
- [ ] Closures, prototype, event loop, modules → [js advanced](../05-Languages/javascript/02-javascript-advanced.md)
- [ ] Module systems (ESM, CJS) → [js modules](../05-Languages/javascript/03-js-modules-fundamentals.md)

---

## Giai đoạn 2 — TypeScript & Tooling

- [ ] TypeScript basics: types, interfaces, generics → [ts basics](../05-Languages/typescript/01-typescript-basics.md)
- [ ] TypeScript advanced: utility types, type guards → [ts advanced](../05-Languages/typescript/02-typescript-advanced.md)
- [ ] Package managers (npm / yarn / pnpm) → [npm yarn pnpm basics](../06-Frontend/package-managers/01-npm-yarn-pnpm-basics.md)
- [ ] Bun runtime & package manager → [bun basics](../06-Frontend/package-managers/02-bun-basics.md)
- [ ] Build tools: Vite → [vite basics](../06-Frontend/build-tools/01-vite-basics.md)
- [ ] Webpack (legacy projects) → [webpack basics](../06-Frontend/build-tools/02-webpack-basics.md)

---

## Giai đoạn 3 — Framework (chọn 1 để chuyên sâu)

### React (phổ biến nhất)
- [ ] Components, hooks, state, lifecycle → [react basics](../06-Frontend/react/01-react-basics.md)
- [ ] Suspense, memo, transitions, concurrent → [react advanced](../06-Frontend/react/02-react-advanced.md)
- [ ] Patterns: compound, render props, HOC → [react patterns](../06-Frontend/react/03-react-patterns.md)
- [ ] Next.js (SSR/SSG framework) → [nextjs basics](../06-Frontend/nextjs/01-nextjs-basics.md)
- [ ] Next.js advanced: middleware, caching → [nextjs advanced](../06-Frontend/nextjs/02-nextjs-advanced.md)

### Vue (lựa chọn thay thế)
- [ ] Composition API, reactivity, Pinia → [vue basics](../06-Frontend/vue/01-vue-basics.md)
- [ ] Vue advanced: custom directives, plugins → [vue advanced](../06-Frontend/vue/02-vue-advanced.md)

---

## Giai đoạn 4 — State Management

- [ ] Tổng quan state management → [state management fundamentals](../06-Frontend/state-management/01-state-management-fundamentals.md)
- [ ] Zustand (lightweight, modern) → [zustand basics](../06-Frontend/state-management/02-zustand-basics.md)
- [ ] Redux Toolkit (enterprise standard) → [redux toolkit basics](../06-Frontend/state-management/01-redux-toolkit-basics.md)
- [ ] TanStack Query (server state) → [react query basics](../06-Frontend/state-management/03-react-query-tanstack-basics.md)

---

## Giai đoạn 5 — Testing

- [ ] Unit & component testing (Vitest + RTL) → [unit component practices](../06-Frontend/testing/01-unit-component-practices.md)
- [ ] E2E testing (Playwright) → [e2e playwright practices](../06-Frontend/testing/02-e2e-playwright-practices.md)
- [ ] Visual regression testing → [visual regression practices](../06-Frontend/testing/03-visual-regression-practices.md)

---

## Giai đoạn 6 — Performance & SEO

- [ ] Core Web Vitals (LCP, FID, CLS) → [web vitals fundamentals](../06-Frontend/performance/01-web-vitals-fundamentals.md)
- [ ] Code splitting & lazy loading → [code splitting practices](../06-Frontend/performance/03-code-splitting-practices.md)
- [ ] DevTools profiling → [devtools profiling](../06-Frontend/performance/02-devtools-profiling-practices.md)
- [ ] Browser rendering pipeline → [browser rendering deep dive](../06-Frontend/performance/04-browser-rendering-deep-dive.md)
- [ ] Technical SEO → [seo technical practices](../06-Frontend/seo/01-seo-technical-practices.md)

---

## Giai đoạn 7 — Nâng cao

- [ ] Tailwind CSS → [tailwindcss basics](../06-Frontend/css-frameworks/01-tailwindcss-basics.md)
- [ ] shadcn/ui component library → [shadcn ui basics](../06-Frontend/css-frameworks/03-shadcn-ui-basics.md)
- [ ] Progressive Web Apps → [pwa basics](../06-Frontend/pwa/01-pwa-basics.md)
- [ ] Micro-frontends → [micro frontends basics](../06-Frontend/micro-frontends/01-micro-frontends-basics.md)
- [ ] WebAssembly → [webassembly basics](../06-Frontend/web-apis/03-webassembly-basics.md)
- [ ] Browser APIs & Web Workers → [browser apis](../06-Frontend/web-apis/01-browser-apis-basics.md)

---

## Project thực hành

| Giai đoạn | Project gợi ý | Kỹ năng rèn |
|---|---|---|
| 1 | Landing page responsive (HTML/CSS thuần) | Flexbox, Grid, media queries |
| 1 | Interactive form with validation (JS) | DOM, events, form handling |
| 2 | Todo app với TypeScript + Vite | TS types, build tools, modules |
| 3 | Blog app với React + Next.js | Components, routing, SSR |
| 4 | Dashboard với Zustand + TanStack Query | State management, data fetching |
| 5 | Full project với test suite (>80% coverage) | Unit, integration, E2E testing |
| 6-7 | E-commerce SPA với PWA + Tailwind | Performance, SEO, offline-first |

---

## Tài nguyên

- [MDN Web Docs](https://developer.mozilla.org) — Tài liệu chuẩn cho HTML/CSS/JS
- [React Docs](https://react.dev) — Tài liệu chính thức React (mới)
- [Vue Docs](https://vuejs.org) — Tài liệu chính thức Vue 3
- [web.dev](https://web.dev) — Best practices từ Google về performance & SEO
- [Frontend Masters](https://frontendmasters.com) — Khóa học chuyên sâu từ chuyên gia
