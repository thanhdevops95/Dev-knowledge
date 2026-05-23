# ⚙️ Lộ trình Backend Developer

> `[BEGINNER → ADVANCED]` ⭐ `[MUST-KNOW]` — Từ API đầu tiên đến hệ thống production-ready
> **Prerequisite:** Đã nắm kiến thức nền tảng ([00-overview.md](./00-overview.md))

---

## Tại sao học Backend?

Backend Developer là người xây dựng "bộ não" của ứng dụng — nơi xử lý logic, lưu trữ dữ liệu và điều phối mọi thứ phía sau màn hình. Nếu Frontend là phần mặt tiền nhà hàng mà khách nhìn thấy, thì Backend là nhà bếp: nơi nhận order, chế biến, quản lý kho nguyên liệu và đảm bảo mọi món ăn ra đúng tiêu chuẩn. Một ngày của Backend developer: thiết kế API, viết business logic, tối ưu database query, xử lý authentication, và đảm bảo hệ thống chịu được hàng nghìn request đồng thời.

---

## Sơ đồ lộ trình

```
Chọn ngôn ngữ ──► Framework ──► API Design ──► Database ──► Auth & Security
(Python/Node/       │          (REST, GraphQL)  (SQL +       │
 Go/Java/C#)        │                           NoSQL)       │
                    ▼                              │         ▼
               ORM / Query                         │    Caching &
               Builder                             │    Messaging
                    │                              │         │
                    └──────────────┬───────────────┘         │
                                   ▼                         │
                           DevOps basics ◄───────────────────┘
                          (Docker, CI/CD)
                                   │
                                   ▼
                           System Design &
                           Architecture
```

---

## Giai đoạn 1 — Ngôn ngữ lập trình (chọn 1)

| Ngôn ngữ | Framework chính | Khi nào nên chọn | Link |
|---|---|---|---|
| **Python** | FastAPI, Django | Startup nhanh, AI/ML integration | [python basics](../05-Languages/python/01-python-basics.md) |
| **Node.js** | Express, NestJS | JS fullstack, realtime apps | [js basics](../05-Languages/javascript/01-javascript-basics.md) |
| **Go** | Gin, Fiber | High performance, microservices | [go basics](../05-Languages/go/01-go-basics.md) |
| **Java** | Spring Boot | Enterprise, tổ chức lớn | [java basics](../05-Languages/java/01-java-basics.md) |
| **C#** | ASP.NET Core | Hệ sinh thái Microsoft/Azure | [csharp basics](../05-Languages/csharp/01-csharp-basics.md) |

> 💡 Người mới nên bắt đầu với **Python** (dễ học) hoặc **Node.js** (dùng chung JS với frontend).

---

## Giai đoạn 2 — Framework

- [ ] Chọn framework phù hợp với ngôn ngữ → [frameworks compare](../07-Backend/frameworks/11-backend-frameworks-compare.md)
- [ ] FastAPI (Python) → [fastapi basics](../07-Backend/frameworks/01-fastapi-basics.md)
- [ ] Express (Node.js) → [express basics](../07-Backend/frameworks/02-express-nodejs-basics.md)
- [ ] NestJS (Node.js, enterprise) → [nestjs fundamentals](../07-Backend/frameworks/02-nestjs-fundamentals.md)
- [ ] Django (Python, batteries-included) → [django basics](../07-Backend/frameworks/03-django-basics.md)
- [ ] Spring Boot (Java) → [spring boot basics](../07-Backend/frameworks/05-spring-boot-basics.md)
- [ ] Gin (Go) → [gin basics](../07-Backend/frameworks/07-gin-go-basics.md)
- [ ] ASP.NET Core (C#) → [aspnet basics](../07-Backend/frameworks/06-aspnet-core-basics.md)

---

## Giai đoạn 3 — API Design

- [ ] REST API: principles, HTTP methods, status codes → [rest api fundamentals](../07-Backend/api-design/01-rest-api-fundamentals.md)
- [ ] GraphQL → [graphql fundamentals](../07-Backend/api-design/02-graphql-fundamentals.md)
- [ ] gRPC (cho microservices) → [grpc fundamentals](../07-Backend/api-design/03-grpc-fundamentals.md)
- [ ] OpenAPI / Swagger documentation → [openapi swagger setup](../07-Backend/api-design/06-openapi-swagger-setup.md)
- [ ] API versioning, pagination → [api versioning patterns](../07-Backend/api-design/09-api-versioning-patterns.md)
- [ ] API security → [api security practices](../07-Backend/api-design/05-api-security-practices.md)

---

## Giai đoạn 4 — Database

### SQL (bắt buộc)
- [ ] SQL fundamentals: SELECT, JOIN, GROUP BY → [sql basics](../08-Databases/sql/01-sql-basics.md)
- [ ] PostgreSQL advanced: indexing, CTE, window functions → [postgresql advanced](../08-Databases/sql/02-postgresql-advanced.md)
- [ ] Query optimization → [query optimization practices](../08-Databases/sql/03-query-optimization-practices.md)
- [ ] Transactions & isolation levels → [transactions fundamentals](../08-Databases/sql/04-transactions-isolation-fundamentals.md)

### NoSQL (chọn theo use case)
- [ ] MongoDB → [mongodb basics](../08-Databases/nosql/01-mongodb-basics.md)
- [ ] Redis (caching + data structure) → [redis basics](../08-Databases/nosql/03-redis-basics.md)
- [ ] Elasticsearch (full-text search) → [elasticsearch basics](../08-Databases/nosql/06-elasticsearch-basics.md)

### ORM & Data Access
- [ ] ORM fundamentals (Prisma, SQLAlchemy, TypeORM) → [orm basics](../08-Databases/orm/01-orm-basics.md)
- [ ] Database migrations → [migrations practices](../08-Databases/orm/02-migrations-practices.md)

---

## Giai đoạn 5 — Authentication & Security

- [ ] Web security fundamentals (XSS, CSRF, injection) → [web security fundamentals](../12-Security/01-web-security-fundamentals.md)
- [ ] Authentication: JWT, OAuth2, session → [authentication fundamentals](../12-Security/02-authentication-fundamentals.md)
- [ ] Authentication deep dive: SSO, MFA → [authentication deep dive](../12-Security/03-authentication-deep-dive.md)
- [ ] OWASP Top 10 → [web security owasp](../12-Security/04-web-security-owasp.md)

---

## Giai đoạn 6 — Caching & Messaging

- [ ] Caching strategies (write-through, write-back, TTL) → [caching strategies](../07-Backend/caching/01-caching-strategies-patterns.md)
- [ ] Redis patterns → [redis patterns](../07-Backend/caching/02-redis-patterns.md)
- [ ] Message brokers (RabbitMQ, Kafka) → [message brokers fundamentals](../07-Backend/messaging/01-message-brokers-fundamentals.md)
- [ ] WebSockets & realtime → [websockets fundamentals](../07-Backend/realtime/01-websockets-fundamentals.md)

---

## Giai đoạn 7 — DevOps cơ bản

- [ ] Docker: containerize ứng dụng → [docker basics](../09-DevOps/docker/01-docker-basics.md)
- [ ] Docker Compose: multi-service setup → [docker compose basics](../09-DevOps/docker/03-docker-compose-basics.md)
- [ ] CI/CD fundamentals → [cicd basics](../09-DevOps/ci-cd/01-cicd-basics.md)
- [ ] GitHub Actions → [github actions basics](../09-DevOps/cicd/01-github-actions-basics.md)

---

## Giai đoạn 8 — System Design & Architecture

- [ ] System design fundamentals → [system design fundamentals](../11-Architecture/system-design/01-system-design-fundamentals.md)
- [ ] Scalability patterns → [scalability fundamentals](../11-Architecture/system-design/04-scalability-fundamentals.md)
- [ ] Design patterns (GoF) → [gof patterns](../11-Architecture/design-patterns/01-gof-patterns.md)
- [ ] Microservices architecture → [microservices patterns](../11-Architecture/microservices/01-microservices-patterns.md)
- [ ] Event-driven architecture → [event driven patterns](../11-Architecture/microservices/02-event-driven-architecture-patterns.md)
- [ ] Distributed systems → [distributed systems fundamentals](../11-Architecture/system-design/07-distributed-systems-fundamentals.md)

---

## Project thực hành

| Giai đoạn | Project gợi ý | Kỹ năng rèn |
|---|---|---|
| 1-2 | REST API CRUD (todo/notes) | Framework basics, routing, middleware |
| 3 | Blog API với auth + pagination | REST design, JWT, query params |
| 4 | E-commerce backend (products, orders, users) | SQL relations, transactions, indexing |
| 5 | API với OAuth2 + rate limiting | Security, auth flow, middleware |
| 6 | Chat service với WebSocket + Redis pub/sub | Realtime, caching, message queue |
| 7 | Dockerized app với CI/CD pipeline | Container, automated deploy |
| 8 | URL shortener (system design exercise) | Scalability, caching, database design |

---

## Tài nguyên

- [Backend Roadmap — roadmap.sh](https://roadmap.sh/backend) — Lộ trình trực quan
- [System Design Primer](https://github.com/donnemartin/system-design-primer) — Học system design miễn phí
- [High Scalability](http://highscalability.com) — Case studies kiến trúc hệ thống lớn
- [ByteByteGo](https://bytebytego.com) — System design từ Alex Xu
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com) — Học PostgreSQL từ cơ bản
