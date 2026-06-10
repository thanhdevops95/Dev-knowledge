# 🎓 psql & Meta-commands — Master CLI client

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [What is PostgreSQL](00_what-is-postgresql.md)

> 🎯 *Master **psql** CLI — kết nối, **meta-commands** (`\d`, `\du`, `\timing`), **system catalog** queries (size table, locks, active queries), **\\copy** import/export CSV, **pgcli** alternative, scripting `psql -c` + `-f`, **DevOps queries** (slow queries, table bloat). Sau bài này dùng Postgres CLI thuần thục như Linux power user.*

## 🎯 Sau bài này bạn sẽ

- [ ] Kết nối psql 5 cách + history file
- [ ] Master 20+ **meta-commands** `\d`, `\l`, `\du`, ...
- [ ] **System catalog** queries (`pg_stat_*`, `information_schema`)
- [ ] **Format output** với `\x`, `\timing`, `\pset`
- [ ] **Import / export** CSV với `\copy`
- [ ] **Script** với `psql -c "SQL"` + `-f script.sql`
- [ ] Tìm **slow queries**, **table size**, **active connections**
- [ ] Setup **pgcli** + **.psqlrc** config

---

## Tình huống — Bạn debug Postgres production lần đầu

Bạn deploy app, sau 1 tuần nhận alert "DB chậm". SSH vào server, gõ `psql`:

```
acmeshop=# 
```

Cursor đứng đó. Bạn không biết:
- Database này có bảng nào?
- Table users nặng bao nhiêu?
- Query nào đang slow?
- Connection từ app nào?

Bạn thử `SHOW TABLES;` (MySQL syntax) → lỗi. Hỏi senior:
> *"Postgres có **meta-commands** bắt đầu `\`. Plus **system catalog** (`pg_stat_activity`, `pg_stat_user_tables`...) cho mọi thông tin DB. Học là productive hơn 10x."*

→ Bài này dạy psql từ A-Z.

---

## 1️⃣ Kết nối — 5 cách

Postgres hỗ trợ **5 cách kết nối** khác nhau — từ connection string URL hiện đại, flags truyền thống, Unix socket (local default), env variables (cho script CI/CD), đến Docker exec. Chọn theo context dùng:

```bash
# 1. URL (modern)
psql "postgresql://user:pass@host:5432/dbname"

# 2. Flags
psql -h localhost -p 5432 -U myapp -d myapp
#     ↑host        ↑port    ↑user   ↑database

# 3. Default (Mac/Linux local — Unix socket)
psql -d myapp                    # OS user = DB user
psql myapp                        # Same

# 4. Environment variables
export PGHOST=localhost
export PGUSER=myapp
export PGDATABASE=myapp
psql

# 5. Docker exec
docker exec -it pg-container psql -U myapp
```

### Password — `.pgpass`

Gõ password mỗi lần connect rất phiền. File `~/.pgpass` lưu password cho các connection thường dùng — psql tự đọc, không hỏi nữa. **Bắt buộc `chmod 600`** để OS chỉ cho phép user owner đọc:

```
# ~/.pgpass — chmod 600
hostname:port:database:username:password

localhost:5432:myapp:myapp:secret
*:5432:*:myapp:secret
```

→ psql tự đọc, không hỏi password. Giảm gõ.

### `~/.psqlrc` — Config persistent

`~/.psqlrc` là init file của psql — mỗi session tự load. Thêm vài cấu hình thông minh sẽ nâng productivity lên đáng kể: hiển thị query time, alias query thường dùng, format đẹp hơn. Đây là setup recommended cho daily work:

```sql
-- ~/.psqlrc
\set QUIET 1               -- ít noise startup
\timing on                  -- show query time
\set HISTSIZE 5000
\set PROMPT1 '%n@%/%R%# '   -- user@db%# format

\pset null '∅'              -- show NULL như ∅
\pset linestyle unicode
\pset border 2

-- Useful queries as aliases
\set tables 'SELECT relname AS table, n_live_tup AS rows FROM pg_stat_user_tables ORDER BY n_live_tup DESC;'
-- Use: :tables

\unset QUIET
\echo 'psql ready'
```

→ Sau setup, mỗi `psql` session tự có timing + alias.

---

## 2️⃣ Meta-commands — Phải thuộc

Meta = lệnh psql bắt đầu `\` (không phải SQL).

### Database + Schema

Meta-commands cho database/schema/table — đây là tập lệnh **gõ nhiều nhất** khi explore DB lạ. Học thuộc 10 lệnh dưới sẽ tiết kiệm cực nhiều thời gian so với query trực tiếp `pg_catalog`:

```
\l               list databases (sizes, encoding)
\l+               same + chi tiết hơn
\c dbname         connect database khác
\c               show current connection

\dn              list schemas
\dn+              + permissions

\dt               list tables (current schema)
\dt *.*           list tables ALL schemas
\dt+ public.*     tables in public + size
\d table           describe table (columns + indexes + constraints)
\d+ table          describe + storage info
```

### Roles + Permissions

Để check role và permission (ai có quyền gì với table nào), dùng 4 lệnh meta dưới đây. Hữu ích nhất khi debug "tại sao user X không SELECT được":

```
\du               list users/roles
\du+              + descriptions
\dp tablename     show table permissions (privileges)
\z                same as \dp
```

### Other objects

```
\di               indexes
\dv               views
\dm               materialized views
\df               functions
\dx               installed extensions
\ds               sequences
\dy               triggers
```

### Output format

```
\x                toggle expanded display (vertical, dễ đọc khi nhiều cột)
\x auto            tự expanded nếu cần
\timing on         show query time
\pset null '∅'     change NULL display
\pset format aligned | unaligned | csv | json
\pset border 0|1|2
\pset pager off    disable paging (less)
\watch 2           re-run last query mỗi 2s (top-like)
```

### History + Edit

```
\h SELECT          help for SQL command
\?                meta-command help
\e                open last query in $EDITOR
\e filename        edit file in editor
\i filename        execute file (script.sql)
\s                show history
\s historyfile     save history
\g                execute query (same as ;)
\gset              execute + save to psql variables
```

### Output to file

```
\o output.txt       redirect output to file
\o                  back to stdout
\o | grep ...        pipe to command

\copy table TO 'file.csv' CSV HEADER     -- export
\copy table FROM 'file.csv' CSV HEADER    -- import
```

→ Quan trọng: `\copy` (client-side) vs `COPY` SQL (server-side). `\copy` dùng path local của user; `COPY` cần path server-side + permission.

### Variables

```
\set name 'Nguyen Van A'
\echo :name           -- prints "Nguyen Van A"

\set verbose true
\set ROW_COUNT          -- show số row affect after each query
```

### Quit + Save

```
\q                  quit
\! ls               run shell command
\!                  enter shell, exit lại psql
```

---

## 3️⃣ System catalog — Bộ não Postgres

Postgres lưu metadata trong **system tables/views**: `pg_*` (catalog) và `information_schema.*` (SQL standard).

### Useful catalog queries

#### Size of tables (biggest first)

```sql
SELECT
  schemaname || '.' || tablename AS table,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
  pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) AS data_size,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename) - pg_relation_size(schemaname || '.' || tablename)) AS index_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
LIMIT 20;
```

#### Database sizes

```sql
SELECT
  datname,
  pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

#### Active connections

```sql
SELECT
  pid,
  usename,
  application_name,
  client_addr,
  state,
  query_start,
  state_change,
  query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
```

#### Slow queries (cần extension `pg_stat_statements`)

```sql
-- Enable trong postgresql.conf: shared_preload_libraries = 'pg_stat_statements'
CREATE EXTENSION pg_stat_statements;

SELECT
  substring(query, 1, 80) AS query,
  calls,
  round(mean_exec_time::numeric, 2) AS mean_ms,
  round(total_exec_time::numeric, 2) AS total_ms,
  rows
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

#### Locks (debug blocking)

```sql
SELECT
  pid,
  usename,
  query,
  state,
  wait_event_type,
  wait_event
FROM pg_stat_activity
WHERE wait_event IS NOT NULL;
```

#### Index usage

```sql
SELECT
  schemaname || '.' || relname AS table,
  indexrelname AS index,
  idx_scan AS scans,
  pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

→ `idx_scan = 0` = index không bao giờ dùng → cân nhắc drop.

#### Table bloat (dead tuples)

```sql
SELECT
  schemaname || '.' || relname AS table,
  n_live_tup AS live,
  n_dead_tup AS dead,
  round(n_dead_tup * 100.0 / NULLIF(n_live_tup, 0), 1) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

→ Bloat cao → cần VACUUM manual (`VACUUM (VERBOSE, ANALYZE) tablename`).

### Kill stuck query

```sql
-- Find PID
SELECT pid, query FROM pg_stat_activity WHERE state != 'idle';

-- Cancel query (gentle)
SELECT pg_cancel_backend(12345);

-- Force terminate connection (harsh)
SELECT pg_terminate_backend(12345);
```

---

## 4️⃣ Useful daily queries

### Show schema + columns

```sql
\d+ users
-- Hoặc query:
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;
```

### Show indexes of a table

```sql
\d users
-- Or:
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'users';
```

### Show foreign keys

```sql
SELECT
  tc.table_name,
  kcu.column_name,
  ccu.table_name AS foreign_table,
  ccu.column_name AS foreign_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu USING (constraint_name)
JOIN information_schema.constraint_column_usage AS ccu USING (constraint_name)
WHERE tc.constraint_type = 'FOREIGN KEY';
```

### Row count exact (large table — count slow)

```sql
-- Estimate (fast, approximate)
SELECT reltuples::bigint AS estimate FROM pg_class WHERE relname = 'users';

-- Exact (slow on big table)
SELECT count(*) FROM users;
```

→ Postgres `count(*)` không có cache — luôn full scan trong MVCC. Estimate đủ 99%.

---

## 5️⃣ Import / Export với `\copy`

### Export CSV

```sql
-- Client-side (recommended)
\copy users TO 'users.csv' CSV HEADER

-- With filter
\copy (SELECT id, name, email FROM users WHERE created_at > '2025-01-01') TO 'recent.csv' CSV HEADER

-- All to stdout (pipe)
\copy users TO STDOUT CSV HEADER | gzip > users.csv.gz
```

### Import CSV

```sql
\copy users FROM 'users.csv' CSV HEADER

-- Skip duplicate via temp table
CREATE TEMP TABLE temp_users AS TABLE users WITH NO DATA;
\copy temp_users FROM 'users.csv' CSV HEADER
INSERT INTO users SELECT * FROM temp_users ON CONFLICT (id) DO NOTHING;
```

### Server-side `COPY` (cần superuser + server path)

```sql
COPY users TO '/var/lib/postgresql/users.csv' CSV HEADER;
COPY users FROM '/var/lib/postgresql/users.csv' CSV HEADER;
```

→ Faster (no network), nhưng file path **server**, không local. Hiếm dùng — `\copy` đủ 99%.

---

## 6️⃣ Scripting — `psql -c` + `-f`

### Run 1 lệnh

```bash
psql -d myapp -c "SELECT count(*) FROM users;"
psql -d myapp -c "VACUUM ANALYZE users;"
```

### Run file

```bash
psql -d myapp -f script.sql
psql -d myapp -f migration.sql -v ON_ERROR_STOP=1     # Stop nếu lỗi
```

### Stdin

```bash
echo "SELECT now();" | psql -d myapp
cat script.sql | psql -d myapp
```

### Backup + restore basic (chi tiết [bài 04](04_backup-and-replication.md))

```bash
pg_dump myapp > backup.sql
psql myapp < backup.sql

# Compressed format (recommended)
pg_dump -Fc myapp > backup.dump
pg_restore -d myapp_restored backup.dump
```

### Variables trong script

```sql
-- migrate.sql
\set userid 42

UPDATE users SET status = 'active' WHERE id = :userid;
```

```bash
psql -d myapp -f migrate.sql -v userid=42
```

---

## 7️⃣ pgcli — Modern alternative

### Install

```bash
pip install pgcli
brew install pgcli
```

### Pros vs psql

| Feature | psql | **pgcli** |
|---|---|---|
| Autocomplete | ❌ | ✅ Smart (table names, columns) |
| Syntax highlight | ❌ | ✅ |
| Multi-line edit | Basic | ✅ Vi/Emacs binding |
| Smart help | Basic | ✅ Inline doc |
| History | File | ✅ + DB-aware |

### Use

```bash
pgcli "postgresql://user:pass@host/db"
```

→ **2026 default cho dev**. Production scripts vẫn `psql` (always installed).

---

## 8️⃣ Bạn debug production lần đầu

```sql
-- 1. Connection check
SELECT version();
SELECT current_database(), current_user, now();

-- 2. List databases
\l+
-- Confirm có acmeshop database.

-- 3. List tables
\c acmeshop
\dt+
-- Thấy 15 tables, total size 2.3GB.

-- 4. Active connections
SELECT pid, usename, state, query
FROM pg_stat_activity
WHERE datname = current_database();
-- → 47 connections active, 3 đang chạy query, 1 idle in transaction 5 phút.

-- 5. Slowest queries (cần pg_stat_statements)
SELECT substring(query, 1, 80), calls, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;
-- → Query "SELECT * FROM orders ORDER BY ..." 8s mean. Cần index!

-- 6. Biggest tables
SELECT relname, pg_size_pretty(pg_total_relation_size(oid))
FROM pg_class WHERE relkind = 'r' ORDER BY pg_total_relation_size(oid) DESC LIMIT 10;
-- → orders 1.2GB, logs 600MB. Cân nhắc partition.

-- 7. Index usage
SELECT indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
-- → 3 indexes never used → drop tiết kiệm 200MB.

-- 8. Kill idle-in-transaction connection
SELECT pg_terminate_backend(12345);
-- (After confirming PID)
```

→ Bạn từ "ngơ" sang debug được trong 1 giờ. **psql + system catalog** = sysadmin Postgres.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Chạy `count(*)` trên bảng 100M rows** → full scan, slow. Dùng estimate từ `pg_class.reltuples` cho approximate.
2. **Quên `\timing on`** → không biết query nhanh/chậm. Set trong `.psqlrc`.
3. **Edit `~/.pgpass` permission ≠ 600** → psql refuse vì lo leak. `chmod 600 ~/.pgpass`.
4. **`COPY` vs `\copy`** — `COPY` cần file path **server**, `\copy` dùng path **client**. 99% dùng `\copy`.
5. **Forget `ON_ERROR_STOP=1`** trong script migration → 1 statement fail, các statement sau vẫn chạy → state inconsistent. Always `psql -v ON_ERROR_STOP=1`.

---

## 🧠 Tự kiểm tra (Self-check)

1. 5 meta-commands quan trọng nhất?
2. Tìm bảng nào nặng nhất trong DB?
3. **`\copy`** vs **`COPY`** — khác sao?
4. Lệnh kill query stuck (PID 12345)?
5. **`pg_stat_statements`** extension dùng cho gì?

<details>
<summary>Gợi ý đáp án</summary>

1. **`\l`** (list databases), **`\dt`** (list tables), **`\d table`** (describe), **`\du`** (list users), **`\timing on`** (show query time). Bonus: **`\x`** (expanded), **`\copy`** (CSV).

2. ```sql
   SELECT relname, pg_size_pretty(pg_total_relation_size(oid))
   FROM pg_class WHERE relkind = 'r'
   ORDER BY pg_total_relation_size(oid) DESC LIMIT 10;
   ```
   Hoặc meta: `\dt+` (less detail).

3. **`\copy`** = psql client-side, file path **của user** (laptop/server SSH vào). Không cần superuser. **`COPY`** = SQL server-side, file path **trên server Postgres**, cần superuser hoặc `pg_write_server_files` role. 99% dùng `\copy` — tránh permission headache.

4. ```sql
   SELECT pg_cancel_backend(12345);    -- gentle, cancel current query
   SELECT pg_terminate_backend(12345); -- harsh, kill connection
   ```
   Cancel trước, terminate nếu cancel không work.

5. **`pg_stat_statements`** = extension tracking **mọi query** chạy: count, mean time, total time, rows. **Bible debug slow query**. Cần enable trong `postgresql.conf` (`shared_preload_libraries = 'pg_stat_statements'`) + `CREATE EXTENSION`.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Connect

```bash
psql "postgresql://user:pass@host:5432/db"
psql -d mydb                          # local
pgcli -d mydb                         # better
```

### Meta essential

```
\l \dt \d \du \dn \dx \df \di
\timing on    \x    \pset null '∅'
\copy table TO 'f.csv' CSV HEADER
\copy table FROM 'f.csv' CSV HEADER
\e (edit)    \i file (run)    \q (quit)
\h SELECT (SQL help)
\?    (meta help)
```

### Catalog queries

```sql
-- Sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(oid))
FROM pg_class WHERE relkind = 'r'
ORDER BY pg_total_relation_size(oid) DESC LIMIT 10;

-- Active
SELECT pid, usename, state, query FROM pg_stat_activity;

-- Slow (pg_stat_statements)
SELECT query, calls, mean_exec_time FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Unused indexes
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

### Kill query

```sql
SELECT pg_cancel_backend(pid);
SELECT pg_terminate_backend(pid);
```

### Script

```bash
psql -d db -c "SQL"
psql -d db -f file.sql -v ON_ERROR_STOP=1
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **psql** | Official Postgres CLI client |
| **pgcli** | Community CLI with autocomplete |
| **Meta-command** | psql command bắt đầu `\` |
| **System catalog** | `pg_*` tables/views chứa metadata |
| **`information_schema`** | SQL-standard metadata views |
| **`pg_stat_*`** | Statistics views (activity, indexes, tables) |
| **`pg_stat_statements`** | Extension track query stats — bible debug |
| **`\copy` vs `COPY`** | Client-side vs server-side CSV |
| **`.pgpass`** | File lưu password (chmod 600) |
| **`.psqlrc`** | psql config startup |
| **`pg_cancel_backend` / `pg_terminate_backend`** | Cancel/kill query |
| **VACUUM** | Cleanup dead tuples |
| **Bloat** | Dead tuples không vacuum tích lũy |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [PostgreSQL là gì? — RDBMS #1 cho backend 2026](00_what-is-postgresql.md)
- ➡️ **Bài tiếp theo:** [Indexes & Performance — EXPLAIN ANALYZE, B-tree, GIN, BRIN](02_indexes-and-performance.md)
- ↑ **Về cụm:** [postgresql README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [psql docs](https://www.postgresql.org/docs/current/app-psql.html) — official reference
- 📖 [pgcli docs](https://www.pgcli.com/)
- 📖 [pg_stat_statements docs](https://www.postgresql.org/docs/current/pgstatstatements.html)
- 📖 [Crunchy: Postgres query observability](https://www.crunchydata.com/blog/postgres-query-observability)
- 📖 [PostgreSQL Cheatsheet — postgrescheatsheet.com](https://postgrescheatsheet.com/)

---

> 🎯 *Sau bài này psql là bạn đồng hành thân thiết. Bài kế tiếp dạy **indexes + EXPLAIN ANALYZE** — perf optimization Postgres production.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `postgresql/` lesson 2/5. Cover: psql connection 5 cách + .pgpass + .psqlrc config + 20+ meta-commands (\l \dt \d \du \dp \dx \df \timing \watch) + system catalog (pg_stat_activity, pg_stat_user_tables, pg_locks) + EXPLAIN intro + COPY import/export.
- **v1.1.0 (25/05/2026)** — Thêm lead-in 2-3 câu trước §1 Kết nối 5 cách + Password `.pgpass` + `~/.psqlrc` config + §2 Database/Schema meta-commands + Roles/Permissions meta. Chuẩn hoá ví dụ `\set` + diễn đạt mượt hơn. Thêm Changelog section.
