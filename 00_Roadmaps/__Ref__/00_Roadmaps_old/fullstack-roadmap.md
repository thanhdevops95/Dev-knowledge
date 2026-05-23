# 🗺️ Lộ trình Fullstack Developer

> `[BEGINNER → ADVANCED]` — Làm được từ giao diện đến server

---

## Fullstack là gì?

Fullstack Developer là người có thể xây dựng **cả Frontend lẫn Backend** — từ UI người dùng thấy đến database lưu trữ dữ liệu.

**Không cần giỏi đều cả hai.** Thông thường bạn sẽ thiên về 1 phía, nhưng hiểu và làm được phía còn lại.

---

## Stack phổ biến

| Stack | Frontend | Backend | Database |
|---|---|---|---|
| **MERN** | React | Node.js (Express) | MongoDB |
| **MEAN** | Angular | Node.js (Express) | MongoDB |
| **PERN** | React | Node.js (Express) | PostgreSQL |
| **T3** | Next.js + React | tRPC + Next.js | PostgreSQL (Prisma) |
| **Django + React** | React | Python Django | PostgreSQL |
| **Laravel + Vue** | Vue | PHP Laravel | MySQL |

---

## Giai đoạn 1 — Nền tảng

Bắt buộc trước khi bắt đầu:
- [ ] Git & Terminal → [../01-Fundamentals/git/](../01-Fundamentals/git/)
- [ ] HTML + CSS → [../03-Frontend/html/](../03-Frontend/html/) | [../03-Frontend/css/](../03-Frontend/css/)
- [ ] JavaScript cơ bản → [../02-Languages/javascript/](../02-Languages/javascript/)
- [ ] HTTP & Networking → [../01-Fundamentals/networking/](../01-Fundamentals/networking/)

---

## Giai đoạn 2 — Frontend

- [ ] React (hoặc Vue) → [../03-Frontend/react/](../03-Frontend/react/)
- [ ] TypeScript → [../02-Languages/typescript/](../02-Languages/typescript/)
- [ ] State management cơ bản
- [ ] Fetch API, async/await

---

## Giai đoạn 3 — Backend

- [ ] Node.js (Express hoặc Fastify)
- [ ] REST API design → [../04-Backend/api-design/](../04-Backend/api-design/)
- [ ] Database: PostgreSQL hoặc MongoDB → [../05-Databases/](../05-Databases/)
- [ ] Authentication (JWT, OAuth) → [../09-Security/](../09-Security/)

---

## Giai đoạn 4 — Kết nối Frontend + Backend

- [ ] CORS configuration
- [ ] Environment variables
- [ ] API error handling và loading states
- [ ] Form validation (client + server)

---

## Giai đoạn 5 — Deploy & DevOps cơ bản

- [ ] Docker cơ bản → [../06-DevOps/docker/](../06-DevOps/docker/)
- [ ] Deploy lên VPS (DigitalOcean, Railway, Render)
- [ ] Nginx reverse proxy cơ bản
- [ ] HTTPS với Let's Encrypt
- [ ] CI/CD đơn giản (GitHub Actions)

---

## Giai đoạn 6 — Next level

- [ ] Next.js (React full-stack) hoặc Nuxt.js (Vue)
- [ ] Server-Side Rendering vs Client-Side Rendering vs Static Generation
- [ ] WebSockets cho realtime features
- [ ] Caching với Redis
- [ ] Testing (unit + integration + e2e)

---

## 📦 Project thực hành theo giai đoạn

| Giai đoạn | Project |
|---|---|
| Sau HTML/CSS/JS | Portfolio cá nhân |
| Sau React | Todo app với local storage |
| Sau Backend cơ bản | Blog API + React frontend |
| Sau Authentication | Full auth system (register, login, logout, protected routes) |
| Sau Deploy | App chạy thật trên domain của bạn |
| Nâng cao | E-commerce, Discord clone, Twitter clone |

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
