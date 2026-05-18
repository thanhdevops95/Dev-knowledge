# 🧭 [Sample] Backend Developer — Stage 3 excerpt

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 19/05/2026\
> **Cập nhật:** 19/05/2026\
> **Loại:** Sample — minh hoạ 1 stage trong career roadmap

> 🎯 *Đây là **đoạn trích 1 stage** của 1 career roadmap, viết theo chuẩn mới — tập trung navigation + link, KHÔNG dạy concept. Concept đẩy hết sang lesson, deep tool đẩy sang tool guide.*

---

## (Trích) Stage 3 — Database + ORM (2 tháng)

### Tại sao stage này?

Stage 2 bạn đã build được API in-memory với FastAPI. Đẹp, chạy nhanh — nhưng restart server là mất hết data. App thật không thể vậy.

Stage 3 này dạy cách *gắn database thật* vào API: thiết kế schema, dùng ORM, viết query, migration khi schema đổi. Sau stage này, API của bạn lưu được data lâu dài và scale được tới hàng triệu record.

### 📚 Lý thuyết cần đọc

> 💡 Đây là **link sang lesson** — đọc tuần tự. Nếu lesson chưa có, sẽ ghi `(chưa có)`.

- [ ] [SQL fundamentals — SELECT, WHERE, JOIN](../../06_Databases/sql-fundamentals/lessons/01_basic/01_select-where.md) (chưa có)
- [ ] [SQL — GROUP BY, aggregate](../../06_Databases/sql-fundamentals/lessons/01_basic/02_group-by.md) (chưa có)
- [ ] [Postgres là gì + khi nào pick Postgres](../../06_Databases/postgresql/lessons/01_basic/00_what-is-postgres.md) (chưa có)
- [ ] [Schema design — chuẩn hoá 1NF, 2NF, 3NF](../../06_Databases/sql-fundamentals/lessons/02_intermediate/01_normalization.md) (chưa có)
- [ ] [Index — vì sao truy vấn chậm, fix bằng index](../../06_Databases/postgresql/lessons/02_intermediate/01_index.md) (chưa có)
- [ ] [SQLAlchemy ORM cơ bản](../../03_Languages/python/lessons/03_advanced/05_sqlalchemy.md) (chưa có)
- [ ] [Alembic migration](../../07_Web/backend/python-fastapi/lessons/02_intermediate/01_alembic.md) (chưa có)

### 🛠️ Setup môi trường (chỉ tối thiểu cho stage)

> 💡 Setup TỐI THIỂU cho stage. Muốn cấu hình sâu, plugin, alternative — vào tool guide tương ứng.

- [ ] Cài Postgres local: chọn 1
  - Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=dev postgres:16`
  - Native: `brew install postgresql@16`
  - 🛠️ **Đào sâu**: [So sánh DB local — Postgres vs SQLite vs Docker DB](../../02_Tools/db-local/00_db-local-options.md) (chưa có)
- [ ] Cài DB client GUI: chọn 1
  - 🛠️ [DBeaver](../../02_Tools/db-clients/dbeaver.md) (chưa có) — free, đa DB
  - 🛠️ [TablePlus](../../02_Tools/db-clients/tableplus.md) (chưa có) — đẹp, Mac
  - 🛠️ [pgAdmin](../../02_Tools/db-clients/pgadmin.md) (chưa có) — official Postgres
  - 🛠️ [So sánh DB clients](../../02_Tools/db-clients/00_db-client-options.md) (chưa có)
- [ ] Install `sqlalchemy[asyncio]` + `alembic` qua pip

### 🧪 Bài tập (mỗi tuần 5-10 bài)

> 💡 Bài tập dùng dataset thật để khỏi nhàm. KHÔNG `SELECT 1+1`.

- [ ] **Tuần 1** — SQL thuần
  - [ ] [10 SQL basic queries trên Northwind dataset](../../06_Databases/sql-fundamentals/exercises/01_basic/) (chưa có)
  - [ ] [JOIN 3 bảng — orders + customers + products](../../06_Databases/sql-fundamentals/exercises/01_basic/) (chưa có)
- [ ] **Tuần 2** — Schema design
  - [ ] [Design schema cho blog 3 bảng (user/post/comment)](../../06_Databases/sql-fundamentals/exercises/02_intermediate/) (chưa có)
  - [ ] [Refactor schema không chuẩn 1NF → 3NF](../../06_Databases/sql-fundamentals/exercises/02_intermediate/) (chưa có)
- [ ] **Tuần 3** — ORM
  - [ ] [Convert API in-memory (Stage 2) → SQLAlchemy](../../07_Web/backend/python-fastapi/exercises/) (chưa có)
- [ ] **Tuần 4** — Migration + Index
  - [ ] [Alembic migration — thêm cột, đổi tên cột, xoá cột](../../07_Web/backend/python-fastapi/exercises/) (chưa có)
  - [ ] [Tìm 5 query chậm trong app + thêm index fix](../../06_Databases/postgresql/exercises/) (chưa có)

### 🎯 Project Stage 3

- [ ] **Blog API với Postgres + SQLAlchemy + Alembic** — CRUD posts/users/comments, full schema, migration
  - Spec đầy đủ → [Project mini — Blog API persistence](../../07_Web/backend/python-fastapi/projects/01_blog-api-postgres.md) (chưa có)

### ✅ Verify — sau Stage 3 bạn phải

- [ ] Đọc được EXPLAIN của 1 query, hiểu seq scan vs index scan
- [ ] Viết migration up/down không xoá data
- [ ] API survive khi DB restart (connection pool tự reconnect)
- [ ] Schema có ERD vẽ rõ ràng (dbdiagram.io hoặc tương tự)

### 🚨 Khi vấp

| Vấn đề | Đi đâu |
|---|---|
| Query chậm không hiểu vì sao | [Lesson — EXPLAIN + index](../../06_Databases/postgresql/lessons/02_intermediate/01_index.md) (chưa có) |
| Alembic migration broken | [Recipe — Recover broken migration](../../07_Web/backend/python-fastapi/recipes/01_alembic-recover.md) (chưa có) |
| Postgres không connect | [Recipe — Postgres connection refused](../../06_Databases/postgresql/recipes/01_connection-refused.md) (chưa có) |
| Stuck > 1 ngày | Reach out → [Tài nguyên cộng đồng](#tài-nguyên-cộng-đồng) |

### ⏭️ Next: Stage 4 — Authentication + Authorization

→ Dữ liệu đã lưu được. Giờ cần biết "ai" đang dùng — Stage 4 dạy JWT, OAuth, role-based access.

---

## 📌 Đặc trưng của roadmap (so với lesson/tool)

| | Lesson | Tool guide | **Roadmap** |
|---|---|---|---|
| Dạy concept? | ✅ | ❌ | ❌ (chỉ link sang lesson) |
| Step-by-step UI? | ❌ | ✅ | ❌ |
| Định hướng + navigation? | ❌ | ❌ | ✅ |
| Verify checklist? | Self-check | ❌ | ✅ (checklist sau mỗi stage) |
| Có bài tập? | ✅ | ❌ | Link sang exercise |
| Có project? | Link sang | ❌ | ✅ Stage project + capstone |

→ Roadmap là **layer điều hướng** — không bao giờ tự dạy. Đọc thấy roadmap dài 2000 dòng giải thích Postgres là gì → SAI, phải đẩy giải thích sang lesson.

---

## 📌 Changelog

- **v1.0.0 (19/05/2026)** — Sample 1 stage roadmap. Demonstrate: navigation-only, link sang lesson cho concept, link sang tool guide cho deep tool, verify checklist + recovery guide khi vấp.
