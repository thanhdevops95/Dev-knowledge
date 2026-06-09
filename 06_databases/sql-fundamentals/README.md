# sql-fundamentals

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Cập nhật:** 25/05/2026\
> **Status:** ✅ Có bài — `01_basic` hoàn chỉnh (6 bài)

> 🎯 Nền tảng SQL cho mọi developer: từ "SQL là gì" đến SELECT, aggregation, JOIN, DML/transaction, và schema design. Ví dụ chạy được ngay trên SQLite/PostgreSQL.

## 📖 Bài đã có — `lessons/01_basic/`

| # | Bài | Nội dung chính |
|---|---|---|
| 00 | [SQL là gì?](lessons/01_basic/00_what-is-sql.md) | RDBMS vs NoSQL, table/row/column, 5 nhóm câu lệnh, cài SQLite chạy query đầu tiên |
| 01 | [SELECT & Filter](lessons/01_basic/01_select-and-filter.md) | SELECT, WHERE (8 operator), ORDER BY, LIMIT/OFFSET, DISTINCT |
| 02 | [Aggregations](lessons/01_basic/02_aggregations.md) | COUNT/SUM/AVG/MIN/MAX, GROUP BY, HAVING, WHERE vs HAVING |
| 03 | [JOINs](lessons/01_basic/03_joins.md) | 5 loại JOIN, alias bảng, self-join, JOIN 3+ bảng |
| 04 | [INSERT/UPDATE/DELETE](lessons/01_basic/04_insert-update-delete.md) | DML, UPSERT, RETURNING, transaction ACID, soft delete |
| 05 | [Schema Design Basics](lessons/01_basic/05_schema-design-basics.md) | Data types, PK/FK, constraints, indexes, normalization 1NF→3NF |

## 🚀 Lộ trình đọc đề xuất

- **Mới bắt đầu** → đọc tuần tự 00 → 05.
- **Đã biết SQL cơ bản, ôn lại** → nhảy tới 02 (aggregations) + 03 (JOINs) + 05 (schema design).
- **Tra cứu nhanh** → mỗi bài có section `⚡ Cheatsheet` + `📘 Glossary` ở cuối.

## 📂 Cấu trúc cluster

```
sql-fundamentals/
├── README.md          ← (file này)
├── lessons/01_basic/  ← 6 bài đã có
├── exercises/         ← (chưa có)
├── recipes/           ← (chưa có)
└── setup/             ← (chưa có)
```

→ Sau `01_basic`, hướng học tiếp: `postgresql/` (Postgres-specific) hoặc `02_intermediate` (subquery, CTE, window functions).
