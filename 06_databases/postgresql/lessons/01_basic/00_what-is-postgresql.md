# 🎓 PostgreSQL là gì? — RDBMS #1 cho backend 2026

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~16 phút\
> **Prerequisites:** [SQL fundamentals](../../../sql-fundamentals/lessons/01_basic/00_what-is-sql.md)

> 🎯 *Bài INTRO. Hiểu **PostgreSQL là gì**, **vs MySQL/MariaDB**, **history** (35 năm), **MVCC architecture**, **psql** CLI, **install local** + **Docker**, kết nối từ FastAPI/Node. KHÔNG dạy `SELECT` chi tiết (xem [SQL fundamentals](../../../sql-fundamentals/)).*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **PostgreSQL** + history (1986 Berkeley → 2026)
- [ ] So sánh **Postgres vs MySQL vs SQLite vs MariaDB**
- [ ] Hiểu **MVCC** (Multi-Version Concurrency Control)
- [ ] **Install** Postgres trên Mac/Linux/Docker
- [ ] Connect bằng **psql** + **pgcli**
- [ ] **role + database** — concepts cơ bản
- [ ] Connection từ FastAPI/Node — DATABASE_URL
- [ ] Biết **extensions** ecosystem (PostGIS, pgvector, Timescale)

---

## Tình huống — Bạn chọn DB cho production

Bạn có FastAPI backend ([cluster trước](../../../../07_web/backend/python-fastapi/)). Bây giờ deploy production cần DB thật.

Chọn lựa:
- **SQLite** — dev OK nhưng single-writer lock, không scale.
- **MySQL** — phổ thông, OK cho Wordpress nhưng feature ít hơn.
- **MariaDB** — fork MySQL, drop-in replacement.
- **Postgres** — nghe nhiều "modern default" nhưng setup hơi phức tạp.
- **SQL Server / Oracle** — đắt commercial.

Bạn ngơ:
- Sao **Postgres** = default 2026 dù MySQL còn phổ biến hơn?
- **MVCC** là gì mà nghe rần rộ?
- **JSONB, GIN index, full-text search** — feature nào Postgres độc quyền?
- Cài thế nào — `brew install`? Docker? Cloud (Supabase, Neon)?

→ Bài này dạy Postgres overview + setup. Bài 01-04 đi sâu psql/index/JSONB/backup.

---

## 1️⃣ Vậy PostgreSQL là gì?

**PostgreSQL** (= "Postgres") = RDBMS open-source, được phát triển ~35 năm. Reputation: **mature, feature-rich, standards-compliant**.

### Lịch sử — Các mốc quan trọng

Postgres không phải sản phẩm "hot mới ra" — nó đã trải qua **40 năm tiến hoá** từ project đại học (Berkeley) thành DB enterprise. Timeline 10 mốc giải thích vì sao Postgres năm 2026 ổn định + giàu tính năng:

| Năm | Sự kiện |
|---|---|
| 1986 | **Ingres** → **Postgres** tại UC Berkeley (Michael Stonebraker) |
| 1996 | Thêm SQL support → đổi tên **PostgreSQL** |
| 2000s | Mature production-ready (Yahoo!, Skype dùng) |
| 2010 | Postgres 9.0 — streaming replication |
| 2017 | Postgres 10 — logical replication, parallel query |
| 2019 | Postgres 12 — improved partitioning |
| 2022 | Postgres 15 — MERGE statement |
| 2023 | Postgres 16 — logical replication enhancements |
| 2024 | Postgres 17 — incremental backup, faster vacuum |
| **2026** | Postgres 18 (latest) — async I/O, virtual columns |

### Mức độ phổ biến

Sau 35 năm phát triển, Postgres đã trở thành **lựa chọn mặc định** cho backend mới + được mọi cloud provider lớn support. 3 số liệu cho thấy độ trưởng thành:

- **#1** "most loved" DB trong Stack Overflow Survey 2024 (lần thứ 7).
- Dùng bởi: **Apple, Instagram, Reddit, Spotify, Twitch, Robinhood, Stripe (legacy), Notion**.
- Cloud managed: **AWS RDS Postgres, Supabase, Neon, Crunchy Data, Render**.

> 🧠 **Ẩn dụ — Postgres như Toyota Corolla:**
> - Không sexy nhất.
> - Không fastest nhất.
> - Nhưng **reliable + feature đầy đủ + ecosystem to** → dùng 20 năm vẫn ổn.
> - MySQL = Honda Civic (popular, easier). MongoDB = Tesla (hot 2015, nhưng JSON đã thua Postgres JSONB).

---

## 2️⃣ Postgres vs MySQL vs SQLite — Bảng so sánh

4 SQL DB phổ biến nhất 2026 — mỗi cái có "sweet spot" riêng. Bảng so sánh 13 trục giúp pick đúng cho project mới. Postgres mạnh nhất tổng thể nhưng không phải lúc nào cũng là đáp án đúng:

| Tiêu chí | **PostgreSQL** | **MySQL** | **SQLite** | **MariaDB** |
|---|---|---|---|---|
| Năm | 1986 → 1996 SQL | 1995 | 2000 | 2009 (fork MySQL) |
| License | Open (PostgreSQL License) | Dual (GPL + Oracle commercial) | Public domain | GPL |
| Owner | PostgreSQL Global Dev Group | **Oracle** | D. Richard Hipp | MariaDB Foundation |
| Standards compliance | **Excellent** | OK | Good | OK |
| Concurrency | **MVCC** (best) | InnoDB MVCC | Single writer | InnoDB MVCC |
| ACID | Full | InnoDB only | Full | Full |
| JSON | **JSONB (binary indexed)** | JSON (no binary) | JSON | JSON |
| Full-text search | **Built-in** (tsvector) | Built-in (limited) | FTS5 | Built-in |
| Replication | Streaming + logical | Async + group | None native | Async + Galera |
| Extensions | **Rich ecosystem** (PostGIS, pgvector, Timescale, Citus) | Plugins | Loadable extensions | Plugins |
| Performance | Strong all-around | **Faster read-heavy** | Insanely fast for small | Like MySQL |
| Embedded | No | No | **Yes (single file)** | No |
| Best for | **Backend default 2026** | Wordpress, traditional LAMP | Mobile, embedded, dev | Drop-in MySQL replacement |

### Khi nào chọn Postgres?

Postgres mạnh nhất khi gặp **7 use case** dưới đây — extension ecosystem (PostGIS, pgvector, Timescale) là điểm khác biệt lớn nhất so với MySQL/SQLite:

| Use case | Lý do |
|---|---|
| **Backend mới 2026** | Default — feature đầy đủ, MVCC tốt nhất |
| **Geospatial** (Uber, Foursquare) | PostGIS extension #1 thế giới |
| **AI/ML embedding search** | **pgvector** extension |
| **Time-series** | Timescale extension |
| **Multi-tenant SaaS** | Row-level security (RLS) native |
| **Complex query** (analytics) | Query planner mạnh, parallel query |
| **JSON-heavy app** | JSONB nhanh hơn MongoDB nhiều case |

### Khi không cần Postgres

Không phải project nào cũng phù hợp Postgres — 4 trường hợp dưới đây có lựa chọn tốt hơn vì lý do ecosystem hoặc đặc thù workload:

- Wordpress / PHP CMS — MySQL ecosystem.
- Mobile app embedded — SQLite.
- Pure cache key-value — Redis.
- Document store khổng lồ + flexible schema — MongoDB.

→ **2026 default**: Postgres. Khi nào cần khác, có lý do rõ.

---

## 3️⃣ MVCC — Bí mật concurrency

**MVCC** = **Multi-Version Concurrency Control** — Postgres allow **reads + writes đồng thời không lock**.

### Vấn đề traditional DB

```
Transaction A: SELECT * FROM users WHERE id = 1   → ⏳ đợi
Transaction B: UPDATE users SET name = 'X' WHERE id = 1   (lock row)
```

→ A đợi B commit. Slow under load.

### Postgres MVCC

```
Transaction A: SELECT * FROM users WHERE id = 1
   → Đọc snapshot tại thời điểm A start
   → Không lock, không đợi
Transaction B: UPDATE users SET name = 'X' WHERE id = 1
   → Tạo NEW VERSION của row
   → Commit
A: vẫn thấy old version (consistency)
```

→ **Readers don't block writers, writers don't block readers**.

### Trade-off

| Pros | Cons |
|---|---|
| ✅ High concurrency | ❌ "Dead rows" tích lũy → cần VACUUM định kỳ |
| ✅ Snapshot isolation native | ❌ DB size grow until VACUUM |
| ✅ bạn transactions OK | ❌ Configuration để tune VACUUM |

→ Modern Postgres có **autovacuum** chạy ngầm. Beginner không phải lo, advanced ops tune theo workload.

---

## 4️⃣ Install Postgres — 3 cách

### Cách 1 — Docker (recommended cho dev)

```bash
docker run --name pg-dev \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_USER=myapp \
  -e POSTGRES_DB=myapp \
  -p 5432:5432 \
  -v pg-data:/var/lib/postgresql/data \
  -d postgres:18
```

→ Pros: clean, isolated, dễ remove. **2026 default cho dev**.

### Cách 2 — Native install

**Mac (Homebrew):**
```bash
brew install postgresql@18
brew services start postgresql@18

# Tạo user + db
createdb myapp
psql myapp
```

**Ubuntu:**
```bash
sudo apt install postgresql-18 postgresql-client-18
sudo systemctl enable --now postgresql
sudo -u postgres createuser -P myapp
sudo -u postgres createdb -O myapp myapp
```

### Cách 3 — Cloud managed (production)

| Provider | Pros | Pricing |
|---|---|---|
| **Supabase** | Postgres + Auth + Realtime + Storage | Free tier 500MB |
| **Neon** | Serverless Postgres, branches | Free tier 0.5GB |
| **Render** | Simple Postgres hosting | Free tier 256MB |
| **AWS RDS Postgres** | Enterprise scale | Pay-as-go |
| **Crunchy Data** | Postgres specialists | $$$ |

→ **2026 startup default**: Supabase / Neon (Postgres + tooling). Production enterprise: RDS.

---

## 5️⃣ psql — CLI client cốt lõi

```bash
psql                            # Connect mặc định (Mac/Linux)
psql -d myapp                   # Connect database
psql -U myuser -d myapp          # Specific user
psql -h localhost -p 5432 -U myapp myapp    # Full
psql postgresql://user:pass@host:5432/db    # URL
```

### Khi đã trong psql

```
myapp=# SELECT 1+1;
 ?column?
----------
        2
(1 row)

myapp=# \q                       # Quit
```

### Meta-commands quan trọng (chi tiết [bài 01](01_psql-and-meta-commands.md))

```
\l                  list databases
\c dbname            connect to database
\d                   list tables
\d tablename         describe table
\du                  list users/roles
\dn                  list schemas
\dx                  list extensions
\timing on           show query time
\x                   expanded display
\?                   help (meta-commands)
\h SELECT            SQL help
```

### Alternative — pgcli (recommended)

```bash
pip install pgcli
pgcli -d myapp
```

→ **pgcli** = psql + autocomplete + syntax highlight. **Default 2026 cho dev**.

### GUI tools

| Tool | Free | Note |
|---|---|---|
| **DBeaver** | ✅ | Universal (Postgres + MySQL + ...) |
| **pgAdmin** | ✅ | Official Postgres GUI |
| **TablePlus** | ⚠️ Trial / $89 | Mac đẹp, light |
| **DataGrip** | ❌ $99/y JetBrains | Best DX |
| **Postico** | ⚠️ $40 | Mac native |

→ Recommendation: **DBeaver** (free, universal) hoặc **TablePlus** (Mac đẹp).

---

## 6️⃣ Role + Database — Concept cơ bản

### Role = user/group/permission

```sql
CREATE ROLE alice LOGIN PASSWORD 'secret';      -- = user
CREATE ROLE devs;                                  -- = group, không LOGIN
GRANT devs TO alice, bob;                          -- alice + bob thuộc devs
```

→ **Postgres unified**: user = role có LOGIN, group = role không LOGIN.

### Database = container schema + tables

```sql
CREATE DATABASE myapp OWNER alice;
\c myapp
CREATE SCHEMA inventory;
CREATE TABLE inventory.products (...);
```

→ **Database** > **Schema** > **Table**. Default schema = `public`.

### Permission

```sql
GRANT SELECT, INSERT ON products TO devs;
GRANT ALL ON ALL TABLES IN SCHEMA inventory TO devs;
REVOKE INSERT ON products FROM devs;
```

→ Granular permission per table/column/role.

### Default user `postgres`

Sau install, có user **`postgres`** = superuser. Best practice:
- KHÔNG dùng `postgres` cho app. Tạo user riêng `myapp` chỉ access database `myapp`.
- Set strong password cho `postgres`.

---

## 7️⃣ Connect từ FastAPI / Node

### FastAPI (SQLModel/SQLAlchemy)

```python
# .env
DATABASE_URL=postgresql+psycopg2://myapp:secret@localhost:5432/myapp
```

```python
import os
from sqlmodel import create_engine

engine = create_engine(
    os.getenv("DATABASE_URL"),
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,    # Reconnect nếu connection chết
)
```

→ Driver: `psycopg2` (sync) hoặc `asyncpg` (async).

### Node.js (Prisma/Drizzle/pg)

```javascript
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
});

const { rows } = await pool.query('SELECT * FROM users WHERE id = $1', [1]);
```

### Connection pooling

| Library | Pool built-in |
|---|---|
| `psycopg2` / SQLAlchemy | ✅ |
| `asyncpg` | ✅ |
| Prisma | ✅ |
| Drizzle | ✅ |
| Raw `pg` | ✅ |

→ Always use pool (10-50 connections), không tạo connection mới mỗi request.

### `DATABASE_URL` format

```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE?option=value

postgresql://myapp:secret@localhost:5432/myapp
postgresql://myapp:secret@db.supabase.co:5432/postgres?sslmode=require
```

---

## 8️⃣ Extensions ecosystem — Postgres killer feature

### Cài extension

```sql
-- List available
SELECT * FROM pg_available_extensions;

-- Install
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgvector;
```

### Famous extensions

| Extension | Mục đích | Use case |
|---|---|---|
| **PostGIS** | Geospatial — point, polygon, distance | Uber, Foursquare, mapping |
| **pgvector** | Vector embeddings — AI/ML similarity search | RAG, recommendation |
| **TimescaleDB** | Time-series optimized | IoT, monitoring metrics |
| **Citus** | Distributed sharding | Multi-tenant SaaS scale |
| **pg_partman** | Auto table partitioning | Big logs/events |
| **pg_cron** | Job scheduling trong DB | Cleanup, refresh views |
| **pg_trgm** | Trigram search (fuzzy match) | Autocomplete, "did you mean" |
| **uuid-ossp** | UUID generators | PK UUID instead of serial |
| **hstore** | Key-value store (predecessor JSONB) | Legacy — JSONB tốt hơn |

→ **AI 2026 boom**: **pgvector** đưa Postgres thành DB chính cho RAG (Retrieval Augmented Generation). Cạnh tranh Pinecone, Weaviate, Chroma.

---

## 9️⃣ Bạn setup Postgres + connect FastAPI

```bash
# 1. Run Postgres
docker run --name pg-acmeshop \
  -e POSTGRES_USER=acmeshop \
  -e POSTGRES_PASSWORD=devsecret \
  -e POSTGRES_DB=acmeshop \
  -p 5432:5432 \
  -d postgres:18

# 2. Verify
docker exec -it pg-acmeshop psql -U acmeshop
acmeshop=# SELECT version();
acmeshop=# \q

# 3. FastAPI .env
cat > .env <<EOF
DATABASE_URL=postgresql+psycopg2://acmeshop:devsecret@localhost:5432/acmeshop
EOF

# 4. FastAPI app
fastapi dev main.py
# → Auto create tables via SQLModel
```

→ Backend bạn now backed by **real Postgres**. Bài kế tiếp dạy psql deep + production patterns.

---

## ⚠️ 5 pitfall hay vướng

1. **Dùng user `postgres` cho app** → if compromised = toàn DB. Tạo user riêng per app, GRANT chỉ cần thiết.
2. **Không pool connection** → mỗi request = new connection (~50ms overhead, 100 connection limit default). Always use pool.
3. **Tin password trong DATABASE_URL** → leak vào git. **`.env`** + `.gitignore`.
4. **Postgres ≠ MySQL syntax 100%** → vài difference (limit/offset, on conflict, JSON). Check docs khi migrate.
5. **Quên enable extension** trước CREATE TABLE dùng feature → "type postgis.geometry does not exist". Always `CREATE EXTENSION` trước.

---

## ✅ Self-check

1. **MVCC** — khác lock-based traditional thế nào?
2. **Postgres vs MySQL** — 3 điểm khác biệt chính 2026?
3. Lệnh **connect psql** với DATABASE_URL?
4. Khác **role + user** trong Postgres?
5. **pgvector** + **PostGIS** dùng cho gì?

<details>
<summary>Gợi ý đáp án</summary>

1. **MVCC** = mỗi transaction thấy **snapshot** tại thời điểm start. Reads không lock writes, writes tạo new version (not update in place). **Lock-based**: reads/writes block nhau → low concurrency. MVCC enable Postgres high concurrency + snapshot isolation native.

2. (a) **JSONB** binary indexed — Postgres. MySQL JSON cũ chậm hơn. (b) **MVCC** + **autovacuum** Postgres. MySQL InnoDB cũng MVCC nhưng implementation khác. (c) **Extensions ecosystem** — Postgres giàu nhất (PostGIS, pgvector, Timescale). MySQL plugins ít hơn. Bonus: standards compliance, query planner, full-text search built-in.

3. ```bash
   psql "postgresql://user:pass@host:5432/db"
   # Hoặc set env:
   export DATABASE_URL="..."
   psql $DATABASE_URL
   ```

4. **Postgres unified**: cả 2 là **role** trong system. **User** = role có `LOGIN` (đăng nhập được). **Group** (role) không có `LOGIN`, dùng để grant permission cho nhiều user (`GRANT devs TO alice, bob`).

5. **pgvector** = vector embeddings cho AI/ML — similarity search (cosine, L2 distance). Use case: RAG, semantic search, recommendation. **PostGIS** = geospatial — point/polygon/distance. Use case: ride-sharing Uber, mapping, "shops within 5km".
</details>

---

## ⚡ Cheatsheet

### Install Docker

```bash
docker run --name pg-dev \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_USER=myapp \
  -e POSTGRES_DB=myapp \
  -p 5432:5432 \
  -v pg-data:/var/lib/postgresql/data \
  -d postgres:18
```

### Connect

```bash
psql "postgresql://user:pass@host:5432/db"
psql -h localhost -U myapp -d myapp
pgcli -d myapp                          # better than psql
```

### psql essentials

```
\l    list dbs       \c db   connect
\d    list tables    \d tbl  describe
\du   list roles     \dx     list extensions
\timing on            \x       expanded display
\q    quit            \?       meta-help
```

### Compare DB

```
Backend default 2026  → PostgreSQL
Geospatial            → Postgres + PostGIS
AI embedding          → Postgres + pgvector
Time-series           → Postgres + TimescaleDB
Mobile/embedded       → SQLite
Wordpress             → MySQL
Drop-in MySQL alt     → MariaDB
```

### Driver

```python
# Python
postgresql+psycopg2://...        # Sync (FastAPI default)
postgresql+asyncpg://...          # Async
```

```javascript
// Node
import { Pool } from 'pg';        // Raw
import { PrismaClient } from '@prisma/client';   // ORM
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **PostgreSQL / Postgres** | RDBMS open-source mature (1986+) |
| **MVCC** | Multi-Version Concurrency Control — readers don't block writers |
| **VACUUM** | Cleanup dead tuples — autovacuum chạy ngầm |
| **psql** | Official CLI client |
| **pgcli** | psql + autocomplete + highlight (community) |
| **Role** | User/group unified concept (LOGIN = user) |
| **Database** | Container schemas + tables |
| **Schema** | Namespace cho tables (default `public`) |
| **Extension** | Plugin (PostGIS, pgvector, ...) |
| **PostGIS** | Geospatial extension #1 |
| **pgvector** | AI embedding vector extension |
| **TimescaleDB** | Time-series extension |
| **JSONB** | Binary JSON (indexed, fast) |
| **Connection pool** | Reuse DB connections cho many requests |
| **DATABASE_URL** | Standard connection string |

---

## 🔗 Links

### Trong cluster
- → Tiếp: [psql & Meta-commands](01_psql-and-meta-commands.md)
- ↑ Cluster: [postgresql README](../../README.md)

### Cross-reference
- [SQL fundamentals](../../../sql-fundamentals/) — SQL syntax trước Postgres-specific
- [FastAPI database](../../../../07_web/backend/python-fastapi/lessons/01_basic/03_database-with-sqlmodel.md) — FastAPI + Postgres

### External
- 📖 [PostgreSQL official docs](https://www.postgresql.org/docs/) — best reference
- 📖 [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) — beginner-friendly
- 📖 [Crunchy Data: Postgres learning](https://www.crunchydata.com/developers/playground)
- 📖 [Use The Index, Luke!](https://use-the-index-luke.com/) — performance bible
- 📖 [Postgres weekly newsletter](https://postgresweekly.com/)
- 📖 [PostgreSQL Wiki](https://wiki.postgresql.org/)

---

> 🎯 *Sau bài này bạn install + connect Postgres. Bài kế tiếp đi sâu **psql client** — meta-commands, useful queries, EXPLAIN intro.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 Lịch sử (đổi tên "History — Years that matter" → "Lịch sử — Các mốc quan trọng" theo §3.7 Vietnamese-first) + §1 Mức độ phổ biến (đổi "Adoption") + §2 So sánh Postgres vs others + Khi nào chọn Postgres + Khi không cần Postgres. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `postgresql/` lesson 1/5. Cover: Postgres là gì + history 40 năm + adoption + so sánh Postgres/MySQL/SQLite/MariaDB + MVCC concurrency + when to pick + install path 3 OS (macOS Homebrew, Linux apt, Docker) + first connection.
