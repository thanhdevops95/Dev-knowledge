# 📋 Overview — 06_databases

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 25/05/2026

> 🌟 Tổng quan mảng cơ sở dữ liệu: vì sao cần database, các họ DB chính, và lộ trình học.

## 🧠 06_databases là gì

**Database** = nơi lưu trữ dữ liệu có tổ chức, cho phép nhiều người đọc/ghi đồng thời, query nhanh, đảm bảo toàn vẹn và không mất dữ liệu khi sự cố. Đây là "bộ nhớ dài hạn" của hầu hết mọi ứng dụng web/mobile/backend.

## ⚙️ Các họ database chính

| Họ | Ví dụ | Lưu data dạng | Dùng khi |
|---|---|---|---|
| Relational (SQL) | PostgreSQL, MySQL, SQLite | Bảng + hàng + cột | Structured data + quan hệ (mặc định 90% app) |
| Document | MongoDB | JSON document linh hoạt | Schema thay đổi liên tục |
| Key-Value | Redis | `key → value` (trong RAM) | Cache, session, tốc độ ms |
| Search | Elasticsearch | Inverted index | Full-text search |
| Vector | pgvector, Pinecone | Vector embedding | AI/ML similarity search |
| Time-series | InfluxDB, TimescaleDB | `(time, metric, value)` | IoT, monitoring metrics |

## 📚 Các khái niệm cốt lõi

- **Table / Row / Column** — đơn vị lưu trữ cơ bản của SQL.
- **Primary Key / Foreign Key** — định danh duy nhất + liên kết bảng.
- **Index** — cấu trúc giúp query nhanh hơn nhiều lần.
- **Transaction (ACID)** — đảm bảo "tất cả hoặc không gì", không mất dữ liệu.
- **Normalization** — tách bảng để giảm trùng lặp.

## 🔜 Lộ trình học đề xuất

1. **Nền tảng** → [sql-fundamentals](sql-fundamentals/) — SQL chung cho mọi RDBMS.
2. **DB cho backend** → [postgresql](postgresql/) — RDBMS mặc định 2026.
3. **Thiết kế** → [database-design](database-design/) — schema, quan hệ, ràng buộc.
4. **NoSQL / chuyên biệt** → redis, mongodb, elasticsearch, vector-databases, time-series (đang bổ sung).

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Khung ban đầu.
- **v1.0.0 (25/05/2026)** — Viết overview thật: định nghĩa, các họ DB, khái niệm cốt lõi, lộ trình học.
