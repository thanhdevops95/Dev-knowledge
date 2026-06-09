# python-fastapi

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Cập nhật:** 01/06/2026\
> **Status:** ✅ Có bài — cluster Basic hoàn chỉnh (5/5)

> ⚙️ *Python + FastAPI — web framework hiện đại, async native, type-safe, auto OpenAPI docs. Cluster `01_basic` đã đủ để build một backend REST production-ready (routing, Pydantic, database, auth).*

## 📖 Bài học

### `lessons/01_basic/` — nền tảng (5 bài, đọc tuần tự)

| # | Bài | Nội dung chính |
|---|---|---|
| 00 | [FastAPI là gì](lessons/01_basic/00_what-is-fastapi.md) | So sánh FastAPI/Flask/Django, type hints + Pydantic, OpenAPI auto-docs, sync vs async, Hello World |
| 01 | [Routes & Parameters](lessons/01_basic/01_routes-and-parameters.md) | Path/query/body/header/cookie param, validate `Path()`/`Query()`, status code, `HTTPException`, `APIRouter` |
| 02 | [Pydantic Models](lessons/01_basic/02_pydantic-models.md) | Tách Request/Response model, `Field()`, validator custom, nested model, `response_model`, alias |
| 03 | [Database với SQLModel](lessons/01_basic/03_database-with-sqlmodel.md) | SQLModel, `Depends(get_session)`, CRUD đầy đủ, relationship 1-N, Alembic migration |
| 04 | [Auth & Middleware](lessons/01_basic/04_auth-and-middleware.md) | Hash password (bcrypt), JWT, OAuth2 Password Flow, `get_current_user`, CORS, custom middleware |

## 🚀 Lộ trình đọc

```
00 (intro + setup) → 01 (routing) → 02 (Pydantic) → 03 (database) → 04 (auth + middleware)
```

→ Sau 5 bài: có backend đầy đủ DB persistent + JWT auth + CORS + logging + auto docs.

## 🔗 Liên quan

- Nền tảng: [HTTP/HTTPS](../../../05_networking/http-https/) + [REST API concepts](../../../05_networking/http-https/lessons/01_basic/05_rest-api-concepts.md)
- Tích hợp DB: [SQL fundamentals](../../../06_databases/sql-fundamentals/)
- Deploy: [Docker](../../../10_devops/docker/)

## 🔜 Dự kiến mở rộng

- `lessons/02_intermediate/` — background tasks, WebSocket, file upload, testing.
- `setup/`, `exercises/`, `recipes/` — chưa có nội dung.
