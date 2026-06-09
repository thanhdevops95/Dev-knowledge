# postgresql

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Cập nhật:** 25/05/2026\
> **Status:** ✅ Có bài — `01_basic` hoàn chỉnh (5 bài)

> 🎯 PostgreSQL — RDBMS mặc định cho backend hiện đại. Từ "Postgres là gì" và setup, đến psql, index/performance, JSONB/arrays/full-text, và backup/replication production.

## 📖 Bài đã có — `lessons/01_basic/`

| # | Bài | Nội dung chính |
|---|---|---|
| 00 | [PostgreSQL là gì?](lessons/01_basic/00_what-is-postgresql.md) | Postgres vs MySQL/SQLite, MVCC, install (Docker/native/cloud), connect từ FastAPI/Node |
| 01 | [psql & Meta-commands](lessons/01_basic/01_psql-and-meta-commands.md) | psql CLI, meta-commands, system catalog, `\copy`, scripting, pgcli |
| 02 | [Indexes & Performance](lessons/01_basic/02_indexes-and-performance.md) | 6 loại index, EXPLAIN ANALYZE, anti-pattern slow query, VACUUM/ANALYZE |
| 03 | [JSONB & Arrays](lessons/01_basic/03_jsonb-and-arrays.md) | JSON vs JSONB, query operators, GIN index, arrays native, full-text search, pgvector |
| 04 | [Backup & Replication](lessons/01_basic/04_backup-and-replication.md) | pg_dump/pg_restore, streaming replication, WAL + PITR, 3-2-1 rule |

## 🚀 Lộ trình đọc đề xuất

- **Mới với Postgres** → đọc tuần tự 00 → 04.
- **Đã dùng Postgres, cần tối ưu** → nhảy tới 02 (indexes) + 03 (JSONB).
- **Vận hành production** → 01 (psql/catalog) + 04 (backup/replication).
- **Chưa biết SQL** → học [sql-fundamentals](../sql-fundamentals/) trước.

## 📂 Cấu trúc cluster

```
postgresql/
├── README.md          ← (file này)
├── lessons/01_basic/  ← 5 bài đã có
├── exercises/         ← (chưa có)
├── recipes/           ← (chưa có)
└── setup/             ← (chưa có)
```

→ Sau `01_basic`, hướng học tiếp: advanced (partitioning, sharding với Citus, pgvector deep, advanced replication).
