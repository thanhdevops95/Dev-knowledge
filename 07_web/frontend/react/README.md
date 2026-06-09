# react — Component framework #1 cho frontend

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 23/05/2026\
> **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)

> 🎯 *Cluster thứ 3 của frontend. React + Hooks + React Router + Context — đủ build SPA hoàn chỉnh. Synthesis với FastAPI: React frontend gọi backend Bạn viết.*

---

## 🚀 Quick start

- **Mới hoàn toàn React?** → [00_what-is-react](lessons/01_basic/00_what-is-react.md).
- **Đã biết JSX, cần state?** → [02_state-and-events](lessons/01_basic/02_state-and-events.md).
- **Fetch API trong React?** → [03_useeffect-and-fetch](lessons/01_basic/03_useeffect-and-fetch.md).
- **Multi-page SPA?** → [04_routing-and-context](lessons/01_basic/04_routing-and-context.md).

---

## 📂 Cấu trúc cluster

```
react/
├── README.md                       ← (file này)
└── lessons/
    └── 01_basic/                   ← ✅ 5/5 bài hoàn chỉnh
        ├── 00_what-is-react.md
        ├── 01_components-and-props.md
        ├── 02_state-and-events.md
        ├── 03_useeffect-and-fetch.md
        └── 04_routing-and-context.md
```

> 🔜 *`02_intermediate/` (advanced hooks, memoization, performance, testing với Vitest) và `03_advanced/` (Server Components, Suspense, Next.js intro) sẽ thêm sau.*

---

## 📖 Lessons — Basic cluster (5 bài)

| # | Bài | Nội dung chính | Tag |
| --- | --- | --- | --- |
| 00 | [React là gì?](lessons/01_basic/00_what-is-react.md) | JSX + Virtual DOM + component philosophy + React vs Vue/Svelte + Vite setup | MUST-KNOW |
| 01 | [Components & Props](lessons/01_basic/01_components-and-props.md) | Function component + JSX rules + props + children + list/key + composition | MUST-KNOW |
| 02 | [State & Events](lessons/01_basic/02_state-and-events.md) | `useState` + immutable update + event handlers + controlled inputs + lifting state | MUST-KNOW |
| 03 | [useEffect & Fetch](lessons/01_basic/03_useeffect-and-fetch.md) | `useEffect` lifecycle + cleanup + fetch FastAPI + loading/error + custom hooks | MUST-KNOW |
| 04 | [Routing & Context](lessons/01_basic/04_routing-and-context.md) | React Router v6 + protected route + Context API + Zustand intro | MUST-KNOW |


---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ↑ **Về cụm:** [frontend grouping](../README.md)
- ↑ **Về cụm:** [07_web README](../../README.md)
- ↑ **Về cụm:** [html-css cluster](../html-css/) — HTML/CSS foundation
- ↑ **Về cụm:** [javascript-dom cluster](../javascript-dom/) — JS foundation
- 🐍 [FastAPI backend](../../backend/python-fastapi/) — backend Bạn gọi
- 🌐 [HTTP, REST, CORS](../../../05_networking/http-https/) — protocol foundation
- 🧭 [Frontend Developer roadmap](../../../00_roadmaps/career/frontend-developer_career-roadmap.md)
- 🧭 [Full-stack Developer roadmap](../../../00_roadmaps/career/fullstack-developer_career-roadmap.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [React docs (new)](https://react.dev/) — official, redesigned 2023
- 📖 [React Router docs](https://reactrouter.com/)
- 📖 [Vite docs](https://vitejs.dev/)
- 📖 [TanStack Query](https://tanstack.com/query) — server state
- 📖 [Zustand](https://zustand-demo.pmnd.rs/) — client state
- 📖 [State of React 2024](https://stateofreact.com/) — yearly survey

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (23/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. Cluster thứ 3 frontend, synthesis FastAPI fullstack.
