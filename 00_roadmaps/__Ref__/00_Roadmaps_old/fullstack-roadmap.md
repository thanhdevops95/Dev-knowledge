# 🗺️ Lộ trình Fullstack Developer
 
> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** `[BEGINNER → ADVANCED]`
> **Tags:** `[MUST-KNOW]` — Làm được từ giao diện đến server & database
> **Prerequisite:** Đã nắm kiến thức nền tảng ([00-overview.md](./00-overview.md))

---
## Table of Contents



---

## Tại sao học Fullstack?

Fullstack Developer là người có thể xây dựng **cả Frontend lẫn Backend** — từ giao diện người dùng nhìn thấy đến database lưu trữ dữ liệu. Hãy hình dung Fullstack như một đầu bếp vừa biết nấu (Backend) vừa biết bày trí món ăn đẹp mắt (Frontend)

Bạn không cần giỏi đều cả hai, thông thường sẽ thiên về 1 phía, nhưng hiểu và làm được cả hai phía giúp bạn tự xây được sản phẩm hoàn chỉnh, giao tiếp tốt hơn với team, và linh hoạt trong công việc. Đây là lựa chọn phổ biến nhất cho startup và freelancer.

---

## Sơ đồ lộ trình

```
        Frontend basics                   Backend basics
     (HTML, CSS, JS, React)         (Node/Python, API, DB)
              │                              │
              └──────────────┬───────────────┘
                             ▼
                    Kết hợp FE + BE
              (API integration, auth flow,
                CORS, environment config)
                             │
                             ▼
                   DevOps & Deployment
              (Docker, CI/CD, cloud basics)
                             │
                             ▼
                        Nâng cao
              (Monorepo, TypeScript fullstack,
               E2E testing, system design)
```

---

## Stack phổ biến

| Stack | Frontend | Backend | Database | Khi nào chọn |
|---|---|---|---|---|
| **T3** | Next.js + React | tRPC + Next.js | PostgreSQL (Prisma) | Type-safe fullstack, modern |
| **MERN** | React | Node.js (Express) | MongoDB | Phổ biến, nhiều tài liệu |
| **PERN** | React | Node.js (Express) | PostgreSQL | MERN + SQL database |
| **Django + React** | React | Python (Django) | PostgreSQL | AI/ML integration |
| **Next.js Fullstack** | Next.js | Next.js API Routes | PostgreSQL | All-in-one framework |
| **Laravel + Vue** | Vue | PHP (Laravel) | MySQL | Rapid prototyping |

---

## Giai đoạn 1 — Frontend cơ bản

> 📖 Xem chi tiết tại [frontend-roadmap.md](./frontend-roadmap.md) — Giai đoạn 1-3

- [ ] HTML semantic + accessibility → [html basics](../06-Frontend/html/01-html-basics.md)
- [ ] CSS: Flexbox, Grid, responsive → [css basics](../06-Frontend/css/01-css-basics.md)
- [ ] JavaScript ES6+, DOM, async → [js basics](../05-Languages/javascript/01-javascript-basics.md)
- [ ] TypeScript fundamentals → [ts basics](../05-Languages/typescript/01-typescript-basics.md)
- [ ] React: components, hooks, state → [react basics](../06-Frontend/react/01-react-basics.md)
- [ ] Tailwind CSS → [tailwindcss basics](../06-Frontend/css-frameworks/01-tailwindcss-basics.md)

---

## Giai đoạn 2 — Backend cơ bản

> 📖 Xem chi tiết tại [backend-roadmap.md](./backend-roadmap.md) — Giai đoạn 1-4

- [ ] Node.js / Python cơ bản → [nodejs basics](../07-Backend/nodejs/01-nodejs-basics.md) · [python basics](../05-Languages/python/01-python-basics.md)
- [ ] Framework: Express hoặc FastAPI → [express basics](../07-Backend/frameworks/02-express-nodejs-basics.md) · [fastapi basics](../07-Backend/frameworks/01-fastapi-basics.md)
- [ ] REST API design → [rest api fundamentals](../07-Backend/api-design/01-rest-api-fundamentals.md)
- [ ] SQL fundamentals → [sql basics](../08-Databases/sql/01-sql-basics.md)
- [ ] PostgreSQL → [postgresql advanced](../08-Databases/sql/02-postgresql-advanced.md)
- [ ] ORM (Prisma / SQLAlchemy) → [orm basics](../08-Databases/orm/01-orm-basics.md)

---

## Giai đoạn 3 — Kết hợp Frontend + Backend

Đây là giai đoạn quan trọng nhất — nơi bạn kết nối hai phía thành một ứng dụng hoàn chỉnh:

- [ ] API integration: fetch/axios từ React gọi API backend
- [ ] CORS configuration — hiểu và xử lý cross-origin requests
- [ ] Authentication flow: login → JWT/session → protected routes (cả FE lẫn BE)
  - [authentication fundamentals](../12-Security/02-authentication-fundamentals.md)
- [ ] Environment variables: `.env` cho FE và BE riêng biệt
- [ ] Error handling end-to-end: API errors → UI error states
- [ ] File upload: multipart form từ FE → xử lý ở BE → lưu storage
- [ ] Next.js fullstack: API Routes + Server Components → [nextjs basics](../06-Frontend/nextjs/01-nextjs-basics.md)

---

## Giai đoạn 4 — DevOps & Deployment

- [ ] Docker: containerize cả FE lẫn BE → [docker basics](../09-DevOps/docker/01-docker-basics.md)
- [ ] Docker Compose: chạy app + database + cache → [docker compose basics](../09-DevOps/docker/03-docker-compose-basics.md)
- [ ] CI/CD: auto test + deploy khi push code → [cicd basics](../09-DevOps/ci-cd/01-cicd-basics.md)
- [ ] GitHub Actions → [github actions basics](../09-DevOps/cicd/01-github-actions-basics.md)
- [ ] Cloud basics: deploy lên Vercel / Railway / AWS → [cloud overview](../10-Cloud/01-cloud-overview.md)
- [ ] Web security cơ bản → [web security fundamentals](../12-Security/01-web-security-fundamentals.md)

---

## Giai đoạn 5 — Nâng cao

- [ ] TypeScript fullstack: shared types giữa FE ↔ BE
- [ ] Monorepo tools (Turborepo, Nx) → [monorepo tools basics](../06-Frontend/build-tools/05-monorepo-tools-basics.md)
- [ ] E2E testing toàn bộ ứng dụng → [e2e playwright practices](../06-Frontend/testing/02-e2e-playwright-practices.md)
- [ ] Caching strategies → [caching strategies](../07-Backend/caching/01-caching-strategies-patterns.md)
- [ ] Message queues (background jobs) → [message brokers](../07-Backend/messaging/01-message-brokers-fundamentals.md)
- [ ] System design fundamentals → [system design fundamentals](../11-Architecture/system-design/01-system-design-fundamentals.md)
- [ ] Microservices (khi hệ thống lớn) → [microservices patterns](../11-Architecture/microservices/01-microservices-patterns.md)

---

## Kiến trúc project Fullstack

```
my-fullstack-app/
├── frontend/               # React/Next.js app
│   ├── src/
│   │   ├── components/
│   │   ├── pages/ (hoặc app/)
│   │   ├── hooks/
│   │   ├── services/       # API calls
│   │   └── types/
│   └── package.json
│
├── backend/                # Node.js/FastAPI
│   ├── src/
│   │   ├── routes/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── middleware/
│   │   └── services/
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## Project thực hành

| Giai đoạn | Project gợi ý | Kỹ năng rèn |
|---|---|---|
| 1-2 | Personal blog (React + Express + PostgreSQL) | CRUD, routing, SQL, REST |
| 3 | Auth system: register, login, protected pages | JWT, cookies, middleware, CORS |
| 3 | E-commerce store (Next.js + Prisma + Stripe) | Fullstack Next.js, payment API |
| 4 | Deploy project lên cloud với Docker + CI/CD | Container, pipeline, env config |
| 5 | Real-time chat app (WebSocket + Redis + React) | Realtime, pub/sub, caching |
| 5 | SaaS dashboard (multi-tenant, role-based) | Architecture, auth, system design |

---

## Tài nguyên

- [The Odin Project — Fullstack](https://www.theodinproject.com) — Curriculum fullstack mã nguồn mở
- [Fullstack Open](https://fullstackopen.com) — Khóa fullstack miễn phí từ University of Helsinki
- [Next.js Docs](https://nextjs.org/docs) — Tài liệu chính thức Next.js
- [Prisma Docs](https://www.prisma.io/docs) — ORM hiện đại cho TypeScript/Node.js
- [roadmap.sh — Fullstack](https://roadmap.sh/full-stack) — Lộ trình trực quan
