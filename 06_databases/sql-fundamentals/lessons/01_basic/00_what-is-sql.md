# 🎓 SQL là gì? — Ngôn ngữ chung của database

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Không có — đây là bài intro mọi developer cần đọc

> 🎯 *Bài INTRO. Hiểu **SQL là gì**, **RDBMS** vs **NoSQL**, **table/row/column**, 5 nhóm câu lệnh (DDL/DML/DQL/DCL/TCL), 5 hệ phổ biến (PostgreSQL/MySQL/SQLite/SQL Server/Oracle), và **cài SQLite trong 1 phút** để chạy thử. KHÔNG dạy SELECT chi tiết (sẽ học từ bài 01 trở đi).*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **SQL là gì** + lịch sử ngắn (50 năm)
- [ ] Phân biệt **SQL (relational)** vs **NoSQL** + khi nào dùng gì
- [ ] Đọc được anatomy 1 **table** (rows + columns + schema)
- [ ] Biết **5 nhóm câu lệnh** SQL (DDL/DML/DQL/DCL/TCL)
- [ ] So sánh **PostgreSQL / MySQL / SQLite / SQL Server / Oracle**
- [ ] Cài được **SQLite** + chạy query đầu tiên
- [ ] Biết 3 cách query DB: CLI / GUI tool / từ code

---

## Tình huống — bạn quản lý 100 user trong Excel

Bạn làm sản phẩm có 100 user. Lưu trong **Excel** `users.xlsx`:

| id | name | email | created_at | status |
|----|------|-------|------------|--------|
| 1  | Nguyen Van A | nguyenvana@ex.com | 2025-01-15 | active |
| 2  | Le Van B  | levanb@ex.com | 2025-02-20 | active |
| ... | ... | ... | ... | ... |

Vài tháng sau, vấn đề bùng nổ:

- 🔢 **5 user mỗi ngày đăng ký mới** → cuối tháng 250 row, Excel chậm.
- 🚫 2 dev cùng edit Excel → **conflict** liên tục.
- 🔍 "Tìm user nào active trong tháng 5" → Excel filter chậm 2 giây.
- 🧮 "Đếm tổng user theo tháng" → phải tạo pivot table tay.
- 🐛 1 dev xóa nhầm 5 row → không có history, không undo được.
- 🌐 Site cần show user list **realtime** → Excel không phục vụ HTTP được.

Bạn ngơ:
- Làm sao **nhiều người** đọc/sửa data cùng lúc không conflict?
- Làm sao **query nhanh** trên hàng triệu dòng?
- Làm sao **tự động hóa** thay vì click pivot table?
- Làm sao đảm bảo **không mất data** khi server crash?

→ Tất cả là việc của **database** — và **SQL** là cách bạn "nói chuyện" với database. Bài này dạy bạn **SQL là gì**, vì sao thay Excel, **5 hệ phổ biến**, và cách chạy query đầu tiên.

---

## 1️⃣ Vậy SQL là gì?

**SQL** = **Structured Query Language** — ngôn ngữ truy vấn dữ liệu trong **relational database** (RDBMS).

- Phát minh tại **IBM năm 1974** (System R) bởi Donald Chamberlin & Raymond Boyce.
- Chuẩn hóa **ANSI/ISO SQL** từ 1986 (SQL-86) → SQL-92 → SQL:1999 → ... → **SQL:2023**.
- Đọc là **"sequel"** (gốc tên "SEQUEL") hoặc **"S-Q-L"** (đánh vần) — cả 2 đều OK.

> 🧠 **Ẩn dụ — SQL như tiếng Anh cho data:**
> - **Excel** = sổ tay cá nhân, lưu thông tin trong 1 cuốn.
> - **Database** = **thư viện công cộng** với hàng triệu cuốn, nhiều người mượn cùng lúc, có thủ thư đảm bảo không mất sách.
> - **SQL** = **ngôn ngữ chung** bạn nói với thủ thư: "tìm cho tôi sách của Donald Knuth in trước 1990".

### Sự khác biệt vs Excel

Beginner hay nghĩ "Excel cũng làm được" — đúng cho data cá nhân, nhưng bùng vỡ ngay khi quy mô lên hoặc nhiều người dùng. Bảng dưới so sánh 8 trục cốt lõi giải thích vì sao mọi web/app phải dùng DB chuyên nghiệp:

| Tiêu chí | Excel | SQL Database |
|---|---|---|
| Quy mô | 1M rows max | Hàng tỷ rows OK |
| Concurrent users | 1-2 (conflict ngay) | Hàng nghìn cùng lúc |
| Speed query | Filter chậm dần | Index → ms |
| Data integrity | Người dùng tự lo | Constraint tự enforce |
| Backup/recovery | Save-as file | Snapshot + WAL + replication |
| Realtime (web/app) | ❌ | ✅ Native |
| Audit trail | ❌ | ✅ (trigger, log) |
| Học khó | 1 giờ | 10-100 giờ |

→ Excel cho data **cá nhân, nhỏ, một mình**. SQL cho data **chung, lớn, nhiều người, phải tin được**.

---

## 2️⃣ Relational Database (RDBMS) — cấu trúc bảng

**RDBMS** = **Relational Database Management System** — lưu data trong **table** (bảng) với hàng + cột, các bảng **liên kết** với nhau qua **key**.

### Anatomy 1 table

1 table SQL gồm **3 thành phần cơ bản**: schema (định nghĩa cột + kiểu + ràng buộc), rows (data thực), columns (đặc tính). Sơ đồ minh hoạ table `users` với 3 row:

```
TABLE: users
┌────┬─────────────┬──────────────┬─────────────┬──────────┐
│ id │ name        │ email        │ created_at  │ status   │  ← Schema (cột + kiểu)
├────┼─────────────┼──────────────┼─────────────┼──────────┤
│ 1  │ Nguyen Van A│ nguyenvana@ex.com  │ 2025-01-15  │ active   │  ← Row (record)
│ 2  │ Le Van B    │ levanb@ex.com │ 2025-02-20  │ active   │
│ 3  │ Tran Van C  │ tranvanc@ex.com  │ 2025-03-10  │ inactive │
└────┴─────────────┴──────────────┴─────────────┴──────────┘
   ↑      ↑          ↑              ↑           ↑
   └─ PK  └─ name col, type VARCHAR, NOT NULL
```

| Khái niệm | Ý nghĩa |
|---|---|
| **Schema** | Định nghĩa cột + kiểu + ràng buộc (NOT NULL, UNIQUE...) |
| **Row / Record / Tuple** | 1 dòng = 1 entity (1 user) |
| **Column / Field / Attribute** | 1 cột = 1 đặc tính |
| **Primary Key (PK)** | Cột định danh duy nhất (`id`) |
| **Foreign Key (FK)** | Cột nối sang bảng khác (`user_id` ở `orders` → `users.id`) |

→ Chi tiết schema sẽ học ở [bài 05](05_schema-design-basics.md).

### Relational — "liên kết bảng"

Chữ **"Relational"** trong RDBMS = khả năng **link** bảng với bảng qua **FK** (foreign key). Đây là sức mạnh chính: data không lặp lại, query ghép linh hoạt. Sơ đồ minh hoạ users → orders qua `user_id`:

```
TABLE: users                       TABLE: orders
┌────┬─────────────┐               ┌──────┬─────────┬──────────┐
│ id │ name        │               │ id   │ user_id │ amount   │
├────┼─────────────┤               ├──────┼─────────┼──────────┤
│ 1  │ Nguyen Van A│ ◀──────┐     │ 100  │ 1       │ 250000   │
│ 2  │ Le Van B    │        └─FK──│ 101  │ 1       │ 380000   │
│ 3  │ Tran Van C  │               │ 102  │ 2       │ 150000   │
└────┴─────────────┘               └──────┴─────────┴──────────┘
                                          ↑
                                  FK trỏ về users.id
```

→ "Order #100 thuộc về user #1 (Nguyen Van A)". Khi cần "tất cả order của 1 user" → **JOIN** 2 bảng (xem [bài 03](03_joins.md)).

---

## 3️⃣ SQL vs NoSQL — khi nào dùng gì?

**NoSQL** = "Not Only SQL" — họ database **không-tabular** (key-value, document, graph, column-family).

| Loại | Ví dụ | Lưu data dạng |
|---|---|---|
| **Relational (SQL)** | PostgreSQL, MySQL | Bảng + row + cột |
| **Document** | MongoDB, CouchDB | JSON document tự do |
| **Key-Value** | Redis, DynamoDB | `key → value` |
| **Graph** | Neo4j | Node + edge (mạng quan hệ) |
| **Column-family** | Cassandra, ScyllaDB | Cột rộng, big-data |
| **Time-series** | InfluxDB, TimescaleDB | Tối ưu cho `(time, metric, value)` |

### Khi nào chọn gì?

Pick DB phù hợp với use case quan trọng hơn pick "DB nào hot nhất". Bảng dưới mapping 7 scenario phổ biến với DB tốt nhất — và lý do tại sao:

| Use case | Chọn | Lý do |
|---|---|---|
| App có **structured data + relation** (user/order/product) | **SQL** | Chuẩn, ACID, JOIN mạnh |
| **Catalog sản phẩm** với schema thay đổi liên tục | MongoDB | Document linh hoạt |
| **Cache, session** | Redis | Trong RAM, ms |
| **Mạng xã hội** "bạn của bạn" | Neo4j | Graph traversal natively |
| **IoT logs** (1M events/s) | InfluxDB | Time-series tối ưu |
| **Realtime analytics** big-data | Cassandra | Scale horizontal |
| **Search engine** | Elasticsearch | Full-text indexing |

→ **2026 reality**: 80% app vẫn dùng **SQL** (Postgres/MySQL) làm primary store. NoSQL bổ sung cho từng vấn đề cụ thể. Nhiều app dùng cả 2 (Postgres cho data chính + Redis cho cache + Elasticsearch cho search).

> 💡 **Quy tắc nhanh**: chưa biết chọn gì → dùng **PostgreSQL**. Nó là choice an toàn 90% case.

---

## 4️⃣ 5 nhóm câu lệnh SQL

SQL có ~30 từ khóa chính, chia 5 nhóm theo mục đích:

| Nhóm | Tên đầy đủ | Mục đích | Ví dụ |
|---|---|---|---|
| **DDL** | Data Definition Language | Định nghĩa cấu trúc | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** | Data Manipulation Language | Sửa data | `INSERT`, `UPDATE`, `DELETE` |
| **DQL** | Data Query Language | Đọc data | `SELECT` |
| **DCL** | Data Control Language | Phân quyền | `GRANT`, `REVOKE` |
| **TCL** | Transaction Control Language | Đảm bảo nguyên tử | `BEGIN`, `COMMIT`, `ROLLBACK` |

### Ví dụ flow đầy đủ

Để hình dung 5 nhóm SQL phối hợp ra sao, theo dõi flow đầy đủ dưới: tạo bảng (DDL) → thêm data (DML) → query (DQL) → đóng gói trong transaction (TCL). Đây là sequence điển hình của 1 backend app:

```sql
-- DDL: tạo bảng
CREATE TABLE users (
  id    SERIAL PRIMARY KEY,
  name  VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);

-- DML: thêm data
INSERT INTO users (name, email) VALUES ('Nguyen Van A', 'nguyenvana@ex.com');

-- DQL: đọc data
SELECT * FROM users WHERE id = 1;

-- DML: sửa data
UPDATE users SET name = 'Nguyen Van A' WHERE id = 1;

-- DCL: phân quyền
GRANT SELECT ON users TO analyst_role;

-- TCL: transaction
BEGIN;
  INSERT INTO orders (user_id, amount) VALUES (1, 100000);
  UPDATE users SET total_orders = total_orders + 1 WHERE id = 1;
COMMIT;  -- hoặc ROLLBACK; nếu lỗi
```

→ 6 cluster lessons dạy đúng các nhóm này. Bài 01-03 = **DQL** (SELECT). Bài 04 = **DML + TCL**. Bài 05 = **DDL**.

---

## 5️⃣ 5 hệ RDBMS phổ biến — so sánh

| RDBMS | License | Đặc điểm | Use case |
|---|---|---|---|
| **PostgreSQL** | Free (OSS) | Tính năng đầy đủ nhất, chuẩn SQL nghiêm | Default 2026, fintech, GIS, analytics |
| **MySQL** | Free (OSS, Oracle) | Phổ biến nhất, performance read-heavy | Web traditional, WordPress |
| **MariaDB** | Free (OSS, fork MySQL) | Drop-in MySQL replacement | Khi không muốn Oracle |
| **SQLite** | Free (public domain) | **Embedded**, file đơn, không cần server | Mobile, desktop app, test, embedded |
| **SQL Server** | Commercial (Microsoft) | Windows ecosystem, T-SQL | Enterprise .NET shop |
| **Oracle DB** | Commercial ($$$$) | Lớn nhất, enterprise, đầy đủ | Banking, telecom legacy |

### Cheat-sheet "chọn hệ nào"

| Bạn là | Dùng |
|---|---|
| Mới học SQL | **SQLite** — không cần cài server, 1 file |
| Backend dev 2026 | **PostgreSQL** (90% choice tốt) |
| Wordpress/PHP app | **MySQL** |
| Mobile app (offline storage) | **SQLite** |
| Microsoft .NET shop | **SQL Server** |
| Big enterprise legacy | **Oracle** (forced choice) |
| Analytics big-data | **PostgreSQL + columnar** (Timescale, Citus) hoặc Snowflake/BigQuery |

→ **PostgreSQL** là chuẩn vàng 2026. Chi tiết Postgres có cluster riêng `06_databases/postgresql/`.

---

## 6️⃣ Cài SQLite trong 1 phút — chạy query đầu tiên

**SQLite** = RDBMS nhẹ nhất, **không cần server**, data nằm trong 1 file `.db`. Có sẵn macOS/Linux.

### Mac/Linux — kiểm tra sẵn có

```bash
$ sqlite3 --version
3.43.0 2023-08-24 ...
```

→ Có sẵn macOS Monterey+ và đa số Linux distro.

### Windows

Tải [sqlite-tools-win32](https://www.sqlite.org/download.html) → giải nén → thêm vào PATH.

### Hoặc dùng container Docker (1 lệnh)

```bash
docker run -it --rm keinos/sqlite3
```

### Tạo DB + table + chạy query

```bash
$ sqlite3 myshop.db        # Tạo (hoặc mở) file myshop.db

sqlite> CREATE TABLE users (
  ...>     id    INTEGER PRIMARY KEY,
  ...>     name  TEXT NOT NULL,
  ...>     email TEXT UNIQUE
  ...> );

sqlite> INSERT INTO users (name, email) VALUES ('Nguyen Van A', 'nguyenvana@ex.com');
sqlite> INSERT INTO users (name, email) VALUES ('Le Van B',  'levanb@ex.com');
sqlite> INSERT INTO users (name, email) VALUES ('Tran Van C', 'tranvanc@ex.com');

sqlite> SELECT * FROM users;
1|Nguyen Van A|nguyenvana@ex.com
2|Le Van B|levanb@ex.com
3|Tran Van C|tranvanc@ex.com

sqlite> .mode column       -- Format đẹp
sqlite> .headers on
sqlite> SELECT * FROM users;
id  name  email
--  ----  ------------
1   Nguyen Van A  nguyenvana@ex.com
2   Le Van B   levanb@ex.com
3   Tran Van C  tranvanc@ex.com

sqlite> .exit
```

→ File `myshop.db` lưu trên disk. Mở lại bất kỳ lúc nào: `sqlite3 myshop.db`.

> 💡 **Cluster tip**: Mọi ví dụ SQL trong cluster bạn copy chạy ngay ở SQLite. PostgreSQL syntax 99% giống, vài chỗ khác sẽ chú thích riêng.

---

## 7️⃣ 3 cách query DB

### Cách 1 — CLI client

```bash
sqlite3 myshop.db          # SQLite
psql -d myshop             # PostgreSQL
mysql -u root -p myshop    # MySQL
```

→ Quick check, debug, automation script.

### Cách 2 — GUI tool

| Tool | Hệ hỗ trợ | Free |
|---|---|---|
| **DBeaver** | All (Postgres/MySQL/SQLite/Oracle/MSSQL/MongoDB...) | ✅ Free |
| **DataGrip** | All | ❌ $99/year (JetBrains) |
| **TablePlus** | All | ⚠️ Free (limited) / $89 |
| **pgAdmin** | PostgreSQL | ✅ Free |
| **MySQL Workbench** | MySQL | ✅ Free |
| **DB Browser for SQLite** | SQLite | ✅ Free |
| **Postico** | PostgreSQL (Mac) | ⚠️ Free trial / $40 |

→ **DBeaver Community** = recommendation #1 — free, mọi hệ.

### Cách 3 — Từ code (ORM hoặc raw)

**Python:**
```python
import sqlite3
conn = sqlite3.connect('myshop.db')
cur = conn.cursor()
cur.execute('SELECT * FROM users WHERE id = ?', (1,))
print(cur.fetchone())
```

**Node.js:**
```javascript
const Database = require('better-sqlite3');
const db = new Database('myshop.db');
const user = db.prepare('SELECT * FROM users WHERE id = ?').get(1);
console.log(user);
```

**Go:**
```go
db, _ := sql.Open("sqlite3", "myshop.db")
row := db.QueryRow("SELECT * FROM users WHERE id = ?", 1)
```

→ Hầu hết ngôn ngữ có **ORM** (Object-Relational Mapper): Prisma (Node), SQLAlchemy (Python), Hibernate (Java), GORM (Go). ORM tự generate SQL từ object. Nhưng **biết SQL raw vẫn bắt buộc** — ORM không cover mọi case.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Tưởng SQL = MySQL** → SQL là **chuẩn ngôn ngữ**, MySQL chỉ là 1 hệ. Postgres/SQLite/SQL Server đều "SQL" với 90% syntax chung + 10% phương ngữ riêng.
2. **Lưu password plaintext** → Nguy hiểm. Phải hash (bcrypt/argon2) trước khi `INSERT`.
3. **Dùng Excel cho production data** → 1 file `.xlsx`, 1 dev, 1 phút bị corrupt → mất hết. SQLite cũng tốt hơn Excel cho persistence.
4. **Không backup** → DB nào cũng có cách backup. Postgres: `pg_dump`. SQLite: copy file. Quên = mất hết.
5. **Học SQL qua "SQL tutorial 10 phút"** → Đủ để biết tồn tại, không đủ để vào job. SQL có hàng trăm thủ thuật, cần thực hành thật nhiều với dataset thật.

---

## 🧠 Tự kiểm tra (Self-check)

1. **SQL** đứng cho gì? Phát minh năm nào?
2. Phân biệt **DDL** vs **DML** vs **DQL**. Cho ví dụ mỗi loại.
3. Khi nào chọn **NoSQL** thay vì SQL?
4. **PostgreSQL** vs **MySQL** — chọn nào nếu mới bắt đầu 2026?
5. **SQLite** khác gì 4 hệ kia? Khi nào dùng?

<details>
<summary>Gợi ý đáp án</summary>

1. **Structured Query Language**. Phát minh tại **IBM 1974** (System R), chuẩn ANSI 1986.

2. **DDL** = Data Definition Language (cấu trúc): `CREATE TABLE`, `ALTER`, `DROP`. **DML** = Data Manipulation Language (sửa): `INSERT`, `UPDATE`, `DELETE`. **DQL** = Data Query Language (đọc): `SELECT`. *(Một số tài liệu gộp DQL vào DML — không sai.)*

3. **NoSQL** khi: (1) schema linh hoạt thay đổi liên tục (document MongoDB); (2) key-value đơn giản cần tốc độ ms (Redis); (3) graph traversal (Neo4j); (4) big-data scale ngang (Cassandra); (5) time-series (InfluxDB). Không thay SQL — thường dùng kèm.

4. **PostgreSQL** — tính năng đầy đủ hơn, chuẩn SQL nghiêm, JSON support tốt, extension nhiều (PostGIS, Timescale, pgvector). MySQL vẫn OK cho web traditional/Wordpress, nhưng Postgres là default 2026.

5. **SQLite** = embedded — không cần server riêng, data trong 1 file. Lý tưởng: học SQL, mobile app, desktop app, test integration. Không phù hợp web app nhiều user concurrent (single-writer lock).
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Cài SQLite quick

```bash
sqlite3 --version                  # Check có sẵn (Mac/Linux)
sqlite3 myshop.db                  # Mở/tạo DB
.mode column                       # Format output đẹp
.headers on                        # Show tên cột
.tables                            # List tables
.schema users                      # Show schema 1 table
.exit                              # Thoát
```

### 5 lệnh tối thiểu

```sql
CREATE TABLE t (id INT, name TEXT);          -- DDL
INSERT INTO t VALUES (1, 'Nguyen Van A');             -- DML
SELECT * FROM t;                              -- DQL
UPDATE t SET name = 'L' WHERE id = 1;         -- DML
DELETE FROM t WHERE id = 1;                   -- DML
```

### Chọn hệ DB

| Bạn cần | Chọn |
|---|---|
| Học SQL nhanh | SQLite |
| Default backend 2026 | **PostgreSQL** |
| Wordpress/PHP | MySQL |
| Mobile app | SQLite |
| .NET | SQL Server |
| Cache | Redis (NoSQL) |
| Search | Elasticsearch (NoSQL) |
| Real-time logs | InfluxDB (NoSQL) |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **SQL** | Structured Query Language — ngôn ngữ chuẩn truy vấn RDBMS |
| **RDBMS** | Relational Database Management System (Postgres, MySQL, ...) |
| **Table** | Bảng — đơn vị lưu data |
| **Row / Record** | 1 dòng = 1 entity |
| **Column / Field** | 1 cột = 1 đặc tính |
| **Schema** | Định nghĩa cột + kiểu + ràng buộc của table |
| **Primary Key (PK)** | Cột định danh duy nhất mỗi row |
| **Foreign Key (FK)** | Cột nối sang bảng khác |
| **Query** | Câu hỏi gửi DB (`SELECT ...`) |
| **DDL / DML / DQL / DCL / TCL** | 5 nhóm câu lệnh SQL |
| **NoSQL** | Database không-tabular (document, key-value, graph, column-family) |
| **ACID** | Atomicity / Consistency / Isolation / Durability — đảm bảo transaction |
| **ORM** | Object-Relational Mapper — code object ↔ table |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ➡️ **Bài tiếp theo:** [SELECT & WHERE — Câu lệnh SQL bạn dùng 90% thời gian](01_select-and-filter.md)
- ↑ **Về cụm:** [sql-fundamentals README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [HTTP là gì](../../../../05_networking/http-https/lessons/01_basic/00_what-is-http.md) — backend web nhận HTTP request, query SQL, trả response
- [REST API concepts](../../../../05_networking/http-https/lessons/01_basic/05_rest-api-concepts.md) — REST resource thường map 1:1 với SQL table

### 🌐 Tài nguyên tham khảo khác
- 📖 [SQLBolt](https://sqlbolt.com/) — tutorial interactive miễn phí (recommend #1 cho beginner)
- 📖 [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) — best Postgres tutorial
- 📖 [SQLite docs](https://www.sqlite.org/lang.html)
- 📖 [Use The Index, Luke!](https://use-the-index-luke.com/) — index/performance bible
- 📖 [Mode SQL Tutorial](https://mode.com/sql-tutorial/)

---

> 🎯 *Sau bài này bạn hiểu SQL là gì, RDBMS vs NoSQL, chọn được hệ phù hợp, và chạy được query đầu tiên với SQLite. Bài kế tiếp dạy **SELECT + WHERE + ORDER BY** — câu lệnh bạn dùng nhiều nhất trong đời SQL.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `sql-fundamentals/` lesson 1/6. Cover: SQL là gì + RDBMS vs Excel + relational concept (PK/FK) + SQL vs NoSQL (7 loại) + 5 nhóm câu lệnh (DDL/DML/DQL/DCL/TCL) + flow đầy đủ tạo bảng → insert → query → setup SQLite.
- **v1.1.0 (25/05/2026)** — Thêm lead-in 2-3 câu trước §1 Excel vs SQL + §2 Anatomy table + Relational diagram + §3 "Khi nào chọn gì" + §4 Ví dụ flow đầy đủ. Chuẩn hoá tên + email trong ví dụ. Thêm Changelog section.
