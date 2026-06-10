# 🎓 Schema Design — CREATE TABLE, PK/FK, Indexes & Normalization

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [JOINs](03_joins.md), [INSERT/UPDATE/DELETE](04_insert-update-delete.md)

> 🎯 *Học thiết kế schema từ A-Z: chọn **data types** đúng, **PRIMARY KEY** + **FOREIGN KEY**, **constraints** (NOT NULL/UNIQUE/CHECK), **indexes** (when + how), **normalization** 1NF→3NF, và 5 anti-pattern beginner. Sau bài này bạn không sợ "schema sai sau 1 năm vứt cả app".*

## 🎯 Sau bài này bạn sẽ

- [ ] Chọn đúng **data type** cho cột (INT vs BIGINT, TEXT vs VARCHAR, DATETIME)
- [ ] Đặt **PRIMARY KEY** đúng — biết khi nào dùng `SERIAL` vs `UUID`
- [ ] Dùng **FOREIGN KEY** + biết `ON DELETE CASCADE` / `RESTRICT` / `SET NULL`
- [ ] Apply 4 constraint: `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`
- [ ] Tạo **INDEX** đúng chỗ (và biết tradeoff)
- [ ] Hiểu **normalization** 1NF / 2NF / 3NF (intro level)
- [ ] Khi nào **denormalize** (cho performance)
- [ ] Tránh 5 anti-pattern: God table, no PK, store JSON-blob in TEXT, varchar(255) reflex, no index on FK

---

## Tình huống — bạn thiết kế bảng `users` cho app đầu tiên

Bạn quyết định "tự design schema":

```sql
CREATE TABLE users (
  id        TEXT,                      -- không PK
  user_data VARCHAR(255),                -- json blob trong text
  phone     VARCHAR(255),                -- mọi varchar đều 255
  email     VARCHAR(255),                -- không UNIQUE
  age       VARCHAR(20),                 -- tuổi mà text
  created   TEXT,                        -- date là text
  status    TEXT                         -- 'active' / 'a' / 'Active' tùy dev
);
```

3 tháng sau, vấn đề bùng nổ:
- 🐛 2 user cùng `email = nguyenvana@ex.com` (không UNIQUE) → login bug.
- 🐛 `age = "thirty"` (validation app rỉ) → query `WHERE age > 25` lỗi.
- 🐌 Query 100k user → 5 giây (không index).
- 💔 Delete user → order vẫn còn `user_id = 1` orphan (không FK).
- 🔥 1 dev edit `user_data` JSON → corrupt format → app crash 1 giờ.

Bạn ngơ:
- Tại sao **PK** quan trọng?
- **Indexes** đặt ở đâu?
- Sao có `VARCHAR(50)` mà mình dùng 255 không sai?
- **Normalization** là gì, nghe đáng sợ?

→ Bài này dạy bạn **schema design** đúng từ đầu — tránh dependency hell sau này.

---

## 1️⃣ Data types — chọn đúng từ đầu

### Số (numeric)

SQL có **8 dạng kiểu số** chính — từ `SMALLINT` (16-bit) đến `BIGINT` (64-bit) cho integer, `DECIMAL/NUMERIC` cho chính xác (tiền tệ), `FLOAT/REAL` cho khoa học. Chọn đúng từ đầu để tránh migrate cột sau này:

| Type | Range | Khi nào dùng |
|---|---|---|
| `SMALLINT` / `INT2` | -32k → 32k | Age, count nhỏ |
| `INTEGER` / `INT` / `INT4` | -2.1B → 2.1B | **Default cho ID**, count |
| `BIGINT` / `INT8` | -9.2 × 10^18 | ID khi expect >2B records (Twitter, IoT) |
| `DECIMAL(p,s)` / `NUMERIC` | Chính xác | **Tiền tệ** (không bao giờ FLOAT) |
| `REAL` / `FLOAT4` | ~7 digit precision | Scientific (không tiền) |
| `DOUBLE PRECISION` / `FLOAT8` | ~15 digit precision | Scientific |
| `SERIAL` (Postgres) / `AUTO_INCREMENT` (MySQL) | INT + auto | Default PK |
| `BIGSERIAL` | BIGINT + auto | PK cho table sẽ rất lớn |

> ⚠️ **TIỀN không dùng FLOAT!** `0.1 + 0.2 = 0.30000000000000004` — sai 1 cent → kiện. Dùng `DECIMAL(10, 2)` (10 digit, 2 decimal).

### Chuỗi (text)

3 dạng text chính — fixed-length, variable-length max-N, unlimited. Postgres modern thường default `TEXT`, MySQL/SQLite có sự khác biệt nhỏ. Bảng so sánh khi nào dùng cái nào:

| Type | Postgres | MySQL | Use case |
|---|---|---|---|
| `CHAR(n)` | Fixed n | Fixed n | Mã quốc gia "VN", "US" (đúng 2 ký tự) |
| `VARCHAR(n)` | Variable, max n | Variable, max n | Name, email, slug |
| `TEXT` | Unlimited | Unlimited (TEXT) / 64KB (TEXT cũ) | Bio, content blog, JSON |

> 💡 **Postgres**: `VARCHAR(n)` và `TEXT` performance **bằng nhau**. `VARCHAR(n)` chỉ thêm constraint length. Default → `TEXT`.

> 💡 **MySQL**: `VARCHAR(255)` historical limit (1 byte length prefix). Hiện đại không còn issue, nhưng "varchar 255" trở thành cargo cult.

### Boolean

Chỉ có Postgres support `BOOLEAN` native — MySQL và SQLite phải dùng INTEGER 0/1 workaround. Nắm để viết SQL cross-DB cho đúng:

| Type | Postgres | MySQL | SQLite |
|---|---|---|---|
| `BOOLEAN` | ✅ `TRUE/FALSE` | ❌ Dùng `TINYINT(1)` | ❌ Dùng `INTEGER` 0/1 |

### Date / Time

Time zone là **nguồn bug khó debug nhất** trong app — user ở `+07`, server ở UTC, log ở `+00`. Postgres có `TIMESTAMPTZ` xử lý đúng từ đầu; MySQL phải lưu UTC + convert ở app layer. 5 dạng date/time cốt lõi:

| Type | Ý nghĩa | Ví dụ |
|---|---|---|
| `DATE` | Ngày | `2025-05-23` |
| `TIME` | Giờ trong ngày | `14:30:00` |
| `TIMESTAMP` | Ngày + giờ (KHÔNG timezone) | `2025-05-23 14:30:00` |
| `TIMESTAMPTZ` | Ngày + giờ + timezone | `2025-05-23 14:30:00+07` |
| `INTERVAL` (Postgres) | Khoảng thời gian | `2 hours` |

> 🌍 **2026 best practice**: luôn dùng `TIMESTAMPTZ` (Postgres). MySQL `DATETIME` (UTC-store + convert app-level).

### JSON / JSONB (Postgres)

Khi schema flexible — vd lưu event payload, user preferences, config động — `JSONB` của Postgres là "best of both worlds": vẫn relational DB nhưng có thể lưu structure tùy ý + query/index được:

```sql
CREATE TABLE events (
  id         SERIAL PRIMARY KEY,
  payload    JSONB NOT NULL          -- binary JSON, query được
);

-- Query field JSON
SELECT payload->>'user_email' FROM events WHERE payload->'type' = '"login"';
```

→ `JSONB` faster than `JSON` (parsed once). Index được. Nhưng schema-less = trade-off với constraints.

### Khác (Postgres exclusive)

| Type | Use case |
|---|---|
| `UUID` | Distributed system, không-conflict ID across DB |
| `INET` | IP address (IPv4/v6) |
| `CIDR` | IP range |
| `MONEY` | Tiền (nhưng vẫn nên `DECIMAL`) |
| `ARRAY` | `INTEGER[]`, `TEXT[]` |
| `tsvector` | Full-text search |
| `point/polygon` | Geometry (kết hợp PostGIS) |

---

## 2️⃣ PRIMARY KEY (PK)

**PK** = cột (hoặc combo) định danh **duy nhất** mỗi row.

```sql
CREATE TABLE users (
  id     SERIAL PRIMARY KEY,        -- Postgres auto-increment INT
  email  TEXT UNIQUE NOT NULL
);
```

### Quy tắc PK

- ✅ **Bắt buộc** mỗi bảng có 1 PK.
- ✅ **Unique** + **NOT NULL** tự động.
- ✅ Tự build index dưới cùng.
- ✅ **Không đổi** giá trị PK sau khi tạo row (vì FK trỏ vào).

### Surrogate vs Natural PK

| Loại | Ví dụ | Pros | Cons |
|---|---|---|---|
| **Surrogate** | `id SERIAL` (auto) | Stable, đơn giản, ngắn | Không "mean" gì |
| **Natural** | `email`, `ssn` | Có nghĩa, đỡ JOIN | Đổi value = sửa FK khắp nơi |

→ **2026 best practice**: **Surrogate PK** (`id SERIAL` hoặc `UUID`). Để Natural như `email` là `UNIQUE` constraint, không phải PK.

### `SERIAL` vs `UUID`

| Lựa chọn | Khi nào |
|---|---|
| **`SERIAL` / `BIGSERIAL`** | Single DB, monolithic app, default |
| **`UUID`** | Distributed system, microservice, sharded, public-facing ID không lộ count |

```sql
-- UUID (Postgres)
CREATE TABLE users (
  id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- pg14+
  ...
);
```

→ UUID nặng hơn (16 bytes vs 4 INT), random insert kém hơn (B-tree index fragmenting). Dùng khi thật sự cần. Postgres 17+ có `UUID v7` (time-ordered) khắc phục fragment.

### Composite PK — nhiều cột

```sql
CREATE TABLE order_items (
  order_id   INTEGER,
  product_id INTEGER,
  qty        INTEGER,
  PRIMARY KEY (order_id, product_id)        -- cặp (order, product) unique
);
```

→ Hữu ích cho junction table M-N (xem §3).

---

## 3️⃣ FOREIGN KEY (FK) + Relationship

**FK** = cột trỏ về PK của bảng khác. Đảm bảo **referential integrity**.

```sql
CREATE TABLE orders (
  id       SERIAL PRIMARY KEY,
  user_id  INTEGER NOT NULL REFERENCES users(id),
  amount   INTEGER
);
```

### 3 loại relationship

#### 1-1 (one-to-one)

```sql
-- user và profile 1-1
CREATE TABLE profiles (
  user_id  INTEGER PRIMARY KEY REFERENCES users(id),
  bio      TEXT,
  avatar   TEXT
);
```

→ Hiếm — thường gộp vào `users`. Tách khi: profile rất lớn (BLOB), security (PII riêng).

#### 1-N (one-to-many) — phổ biến nhất

```sql
-- 1 user nhiều order
CREATE TABLE orders (
  id       SERIAL PRIMARY KEY,
  user_id  INTEGER NOT NULL REFERENCES users(id),
  ...
);
```

→ FK ở bên "many" trỏ về "one".

#### M-N (many-to-many) — cần junction table

```sql
-- 1 student học nhiều course, 1 course có nhiều student
CREATE TABLE students  (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE courses   (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE enrollments (                      -- junction
  student_id INTEGER REFERENCES students(id),
  course_id  INTEGER REFERENCES courses(id),
  enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (student_id, course_id)
);
```

→ Junction table có composite PK + 2 FK.

### ON DELETE / ON UPDATE — referential action

Khi parent row bị xóa, child rows làm gì?

| Action | Hành vi |
|---|---|
| `CASCADE` | Xóa child theo |
| `RESTRICT` (default Postgres) | Cấm xóa parent nếu có child |
| `SET NULL` | Child `user_id` thành NULL |
| `SET DEFAULT` | Child về DEFAULT value |
| `NO ACTION` | Như RESTRICT, check ở COMMIT |

```sql
CREATE TABLE orders (
  id       SERIAL PRIMARY KEY,
  user_id  INTEGER NOT NULL REFERENCES users(id)
                     ON DELETE CASCADE              -- user xóa → order xóa theo
                     ON UPDATE CASCADE              -- user.id đổi → order.user_id đổi theo
);
```

### Chọn action nào?

| Use case | Action |
|---|---|
| Comment trên post, post bị xóa | `CASCADE` (comment xóa theo) |
| User xóa nhưng order giữ lại (analytics) | `SET NULL` hoặc soft delete |
| User có order, không cho xóa user | `RESTRICT` |

> ⚠️ `CASCADE` mạnh — xóa user → xóa orders → xóa order_items → ... Đôi khi vô ý xóa cả terabyte. Cân nhắc kỹ.

---

## 4️⃣ Constraints — Validation ở DB layer

### `NOT NULL`

```sql
name TEXT NOT NULL
```

→ Cấm INSERT NULL. App có bug vẫn không lưu được NULL.

### `UNIQUE`

```sql
email TEXT UNIQUE NOT NULL
```

→ 2 user không thể trùng email.

**Unique composite** (2+ cột):

```sql
CREATE TABLE products (
  id    SERIAL PRIMARY KEY,
  sku   TEXT,
  store_id INTEGER,
  UNIQUE (sku, store_id)                -- 1 sku unique per store
);
```

### `CHECK`

```sql
age INTEGER CHECK (age >= 0 AND age < 150)
amount INTEGER CHECK (amount > 0)
status TEXT CHECK (status IN ('active', 'inactive', 'pending'))
```

→ Logic validation ở DB. App có bug, DB vẫn từ chối.

> 💡 **Enum** vs **CHECK IN**: Postgres có `CREATE TYPE status AS ENUM(...)` — type-safe hơn. Nhưng thêm enum value khó (DDL change). `CHECK IN` linh hoạt hơn.

### `DEFAULT`

```sql
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
status      TEXT      DEFAULT 'active'
view_count  INTEGER   DEFAULT 0
```

→ INSERT không cần truyền → tự fill.

### Combo

```sql
CREATE TABLE users (
  id         SERIAL PRIMARY KEY,
  email      TEXT NOT NULL UNIQUE CHECK (email LIKE '%@%'),
  age        INTEGER CHECK (age >= 0 AND age < 150),
  status     TEXT NOT NULL DEFAULT 'active'
             CHECK (status IN ('active', 'inactive', 'banned')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

→ Schema này từ chối: missing email, email không format, age âm, status sai value.

---

## 5️⃣ Indexes — Query nhanh hơn 100-1000x

**Index** = data structure (thường B-tree) giúp DB tìm row nhanh hơn full scan.

### Tự có

- PK → tự index.
- UNIQUE → tự index.

### Tạo thêm

```sql
CREATE INDEX idx_orders_user_id  ON orders(user_id);
CREATE INDEX idx_users_status    ON users(status);

-- Composite index (cột thứ tự quan trọng!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### Khi nào tạo index?

| Tạo index trên | Ví dụ |
|---|---|
| **FK** | `orders.user_id` — JOIN nhanh |
| **Cột hay filter WHERE** | `users.status`, `orders.created_at` |
| **Cột hay sort** | `created_at DESC` |
| **Cột UNIQUE** | (tự có) |

### Khi nào KHÔNG tạo index?

- Bảng nhỏ (<1000 rows) — full scan nhanh hơn.
- Cột write-heavy, ít read — index chậm INSERT/UPDATE.
- Cột low-cardinality (vd `gender` có 2 value) — index không giúp.

### Index types

| Type | Use case |
|---|---|
| **B-tree** | Default — `=`, `<`, `>`, `BETWEEN`, sort, prefix `LIKE 'abc%'` |
| **Hash** | Chỉ `=`, không sort. Hiếm dùng. |
| **GIN** (Postgres) | Full-text search, JSONB, array |
| **GiST** (Postgres) | Geometry, range |
| **BRIN** (Postgres) | Big table ordered (logs by time) — index nhẹ |

### Partial index

```sql
-- Chỉ index user active (90% query filter này)
CREATE INDEX idx_users_active ON users(email) WHERE status = 'active';
```

→ Nhỏ hơn, nhanh hơn full index.

### Tradeoff

```
+ Read: 100-1000x nhanh hơn (đặc biệt JOIN, ORDER BY)
- Write: 10-30% chậm hơn (INSERT/UPDATE phải update index)
- Disk: tốn thêm 10-30% storage
- Maintenance: VACUUM, REINDEX định kỳ (Postgres)
```

→ **Quy tắc**: read-heavy → nhiều index. Write-heavy → ít index. Mỗi index phải có **lý do**.

### `EXPLAIN` — kiểm tra query có dùng index không

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'nguyenvana@ex.com';
```

→ Output cho biết: `Index Scan` (✅) hay `Seq Scan` (❌ full scan). Học sâu ở `02_intermediate/`.

---

## 6️⃣ Normalization — 1NF / 2NF / 3NF

Normalization = quá trình **tách bảng** để giảm trùng lặp + bug data.

### Bảng chưa normalize (denormalized)

```
orders
┌────┬─────────┬─────────────┬───────────┬──────────┬────────────────────────────────┐
│ id │ user_id │ user_name   │ user_city │ product  │ product_category │ amount │
├────┼─────────┼─────────────┼───────────┼──────────┼────────────────────────────────┤
│ 1  │ 1       │ Nguyen Van A│ Hanoi     │ iPhone   │ Phone            │ 25M    │
│ 2  │ 1       │ Nguyen Van A│ Hanoi     │ AirPods  │ Audio            │ 5M     │
│ 3  │ 2       │ Le Van B    │ Hanoi     │ iPhone   │ Phone            │ 25M    │
└────┴─────────┴─────────────┴───────────┴──────────┴──────────────────┴────────┘
```

**Vấn đề:**
- Đổi tên user 1 từ `Nguyen Van A` thành tên mới → update **mọi row** của user 1 (anomaly).
- User 1 đổi city Hanoi → Saigon → update mọi row.
- Lưu trùng `Phone`, `Audio` cho product → tốn disk.

### 1NF (First Normal Form)

**Quy tắc**: mỗi cell chứa **1 giá trị atomic** (không list, không object).

```
❌ Vi phạm 1NF:
phones: "0901,0902,0903"

✅ 1NF:
phone1: "0901"
phone2: "0902"
-- Hoặc tách table user_phones (id, user_id, phone)
```

### 2NF (Second Normal Form)

**Quy tắc**: 1NF + mọi non-PK cột phụ thuộc **toàn bộ PK** (không chỉ 1 phần).

Bảng `orders` ở trên không 2NF vì `user_name`, `user_city` chỉ phụ thuộc `user_id` (1 phần). Tách:

```
orders                     users
┌────┬─────────┬────────┐  ┌─────┬──────┬──────┐
│ id │ user_id │ amount │  │ id  │ name │ city │
├────┼─────────┼────────┤  ├─────┼──────┼──────┤
│ 1  │ 1       │ 25M    │  │ 1   │ Nguyen Van A │ Hanoi│
│ 2  │ 1       │ 5M     │  │ 2   │ Le Van B     │ Hanoi│
└────┴─────────┴────────┘  └─────┴──────┴──────┘
```

### 3NF (Third Normal Form)

**Quy tắc**: 2NF + mọi non-PK cột phụ thuộc **trực tiếp** vào PK (không transitive).

Bảng nếu có `(product_id, product_name, product_category)` — `category` phụ thuộc `product_id` qua `product_name` (transitive). Tách:

```
order_items                products
┌────┬─────────┬───────────┐  ┌────┬─────────┬──────────┐
│ id │ order_id│ product_id│  │ id │ name    │ category │
├────┼─────────┼───────────┤  ├────┼─────────┼──────────┤
│ 1  │ 1       │ 1         │  │ 1  │ iPhone  │ Phone    │
│ 2  │ 2       │ 2         │  │ 2  │ AirPods │ Audio    │
└────┴─────────┴───────────┘  └────┴─────────┴──────────┘
```

### Quy tắc thực hành

→ **3NF là "đủ" cho 99% app**. 4NF/5NF lý thuyết hơn.

### Denormalize — khi nào break rule?

**Performance**. JOIN 5 bảng cho 1 query → chậm. Đôi khi **copy** data sang đích để đỡ JOIN:

```sql
-- Đường tắt: lưu user_name trong order
ALTER TABLE orders ADD COLUMN user_name_cache TEXT;

-- Trigger keep sync (hoặc app responsibility)
```

→ Trade-off: nhanh đọc, chậm write (cập nhật cả 2 nơi).

> 💡 **Quy tắc 2026**: normalize bằng 3NF từ đầu. Khi gặp bottleneck performance thực sự (đo bằng EXPLAIN + production load), mới denormalize có chọn lọc.

---

## 7️⃣ Bạn viết lại schema đúng

### Trước (bạn sai)

```sql
CREATE TABLE users (
  id        TEXT,
  user_data VARCHAR(255),
  phone     VARCHAR(255),
  email     VARCHAR(255),
  age       VARCHAR(20),
  created   TEXT,
  status    TEXT
);
```

### Sau (chuẩn)

```sql
-- USERS
CREATE TABLE users (
  id          SERIAL PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE
                CHECK (email LIKE '%_@__%.__%'),
  name        TEXT NOT NULL,
  phone       TEXT,
  age         SMALLINT CHECK (age >= 0 AND age < 150),
  status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'inactive', 'banned')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at  TIMESTAMPTZ                             -- soft delete
);

-- Index cho query phổ thông
CREATE INDEX idx_users_status_created ON users(status, created_at DESC)
  WHERE deleted_at IS NULL;

-- ORDERS — 1 user nhiều order
CREATE TABLE orders (
  id          SERIAL PRIMARY KEY,
  user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  amount      DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
  status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id  ON orders(user_id);
CREATE INDEX idx_orders_status   ON orders(status);
CREATE INDEX idx_orders_created  ON orders(created_at DESC);

-- PRODUCTS
CREATE TABLE products (
  id       SERIAL PRIMARY KEY,
  sku      TEXT NOT NULL UNIQUE,
  name     TEXT NOT NULL,
  price    DECIMAL(12, 2) NOT NULL CHECK (price >= 0),
  category TEXT
);

-- ORDER_ITEMS — junction M-N order × product
CREATE TABLE order_items (
  order_id    INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  qty         INTEGER NOT NULL CHECK (qty > 0),
  unit_price  DECIMAL(12, 2) NOT NULL CHECK (unit_price >= 0),
  PRIMARY KEY (order_id, product_id)
);
```

→ Schema này: 3NF, đầy đủ constraint, indexes hợp lý, FK chuẩn, soft delete-ready.

---

## ⚠️ 5 anti-pattern beginner

### Anti-pattern 1 — "God table"

```sql
-- ❌ 1 bảng 80 cột chứa mọi thứ
CREATE TABLE users (
  id, name, email, address, phone, billing_address, shipping_address,
  order_1, order_2, ..., order_50, last_login, ...
);
```

→ Tách bảng theo concept. 3NF.

### Anti-pattern 2 — Không có PK

```sql
-- ❌
CREATE TABLE logs (event TEXT, ts TEXT);
```

→ Mọi bảng phải có PK. `id SERIAL PRIMARY KEY` là default.

### Anti-pattern 3 — JSON blob trong TEXT/VARCHAR

```sql
-- ❌
metadata VARCHAR(255)  -- "{\"key\":\"val\",...}"
```

→ Dùng `JSONB` (Postgres) — query được, index được. Hoặc tách thành cột riêng.

### Anti-pattern 4 — `VARCHAR(255)` reflex

```sql
-- ❌ Mọi cột đều VARCHAR(255)
name      VARCHAR(255)
phone     VARCHAR(255)
age       VARCHAR(255)  -- tuổi mà text
country   VARCHAR(255)  -- chỉ cần 2 ký tự
```

→ Chọn type đúng: `SMALLINT` cho age, `CHAR(2)` cho country, `VARCHAR(20)` cho phone.

### Anti-pattern 5 — Không index FK

```sql
-- ❌ FK không có index → JOIN chậm O(n × m)
CREATE TABLE orders (
  id      SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id)
);

-- ✅ Postgres KHÔNG tự index FK (MySQL có). Tự tạo:
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

---

## 🧠 Tự kiểm tra (Self-check)

1. Tại sao không lưu tiền dùng `FLOAT`?
2. Khi nào chọn `UUID` thay vì `SERIAL` cho PK?
3. `ON DELETE CASCADE` vs `ON DELETE SET NULL` — khác biệt + use case?
4. Schema sau 1 năm có 10M user, query `WHERE status = 'active' ORDER BY created_at DESC LIMIT 20` chậm. Index nào sửa?
5. Bảng `(student_id, course_id, grade)` là 1NF, 2NF, 3NF chưa?

<details>
<summary>Gợi ý đáp án</summary>

1. FLOAT/DOUBLE có **floating point precision** — `0.1 + 0.2 = 0.30000000000000004`. Sai 1 cent qua nhiều phép tính = sai bill. Tiền **luôn** dùng `DECIMAL(10, 2)` hoặc `NUMERIC`.

2. **UUID** khi: (a) microservices/distributed system, không share ID generator; (b) public-facing ID không lộ count (ID 100 = thứ 100); (c) merge data từ nhiều DB.

3. `CASCADE` xóa child theo (comment xóa khi post xóa). `SET NULL` giữ child, set FK = NULL (order giữ lại, user_id = NULL khi user xóa — cho analytics).

4. Composite index `(status, created_at DESC)` hoặc partial index `(created_at DESC) WHERE status = 'active'`. Cả 2 đều giúp.

5. Giả sử PK = `(student_id, course_id)`. **1NF** ✅ (cell atomic). **2NF** ✅ (`grade` phụ thuộc cả PK). **3NF** ✅ (không transitive). Schema này đẹp.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Type tốt cho mỗi cột

| Mục đích | Type |
|---|---|
| ID auto | `SERIAL` / `BIGSERIAL` / `UUID` |
| Tiền | `DECIMAL(12, 2)` |
| Tuổi | `SMALLINT` |
| Email/name | `TEXT` (Postgres) hoặc `VARCHAR(255)` (MySQL) |
| Country code | `CHAR(2)` |
| Boolean | `BOOLEAN` (Postgres), `TINYINT(1)` (MySQL) |
| Date+time | `TIMESTAMPTZ` (Postgres), `DATETIME` (MySQL) |
| JSON | `JSONB` (Postgres), `JSON` (MySQL 5.7+) |
| Status enum | `TEXT CHECK (status IN (...))` |

### Template bảng chuẩn (Postgres)

```sql
CREATE TABLE entity (
  id          SERIAL PRIMARY KEY,
  ...
  created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at  TIMESTAMPTZ
);

CREATE INDEX idx_entity_active ON entity(created_at DESC) WHERE deleted_at IS NULL;
```

### FK pattern

```sql
user_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
```

### Constraint combo

```sql
status TEXT NOT NULL DEFAULT 'active'
       CHECK (status IN ('active', 'inactive', 'banned'))
```

### Index cheat

```sql
-- Single col
CREATE INDEX idx_t_col ON t(col);

-- Composite (cột phổ biến nhất trước)
CREATE INDEX idx_t_a_b ON t(a, b);

-- Partial
CREATE INDEX idx_t_active ON t(col) WHERE status = 'active';

-- Sort order
CREATE INDEX idx_t_created_desc ON t(created_at DESC);

-- Unique constraint
ALTER TABLE t ADD CONSTRAINT uq_t_email UNIQUE (email);

-- Drop
DROP INDEX idx_t_col;

-- Check usage
EXPLAIN ANALYZE SELECT * FROM t WHERE col = 'x';
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Schema** | Định nghĩa cấu trúc table (cột + type + constraint) |
| **Data type** | Loại data của cột (INT, TEXT, DATE...) |
| **PRIMARY KEY (PK)** | Cột định danh duy nhất mỗi row |
| **FOREIGN KEY (FK)** | Cột trỏ về PK bảng khác |
| **Surrogate / Natural PK** | Auto-gen ID vs business value (email) |
| **Constraint** | Ràng buộc: NOT NULL / UNIQUE / CHECK / DEFAULT |
| **Index** | Data structure giúp query nhanh (B-tree, hash, GIN, GiST) |
| **B-tree** | Default index — balanced tree, hỗ trợ `=`, `<`, `>`, sort, prefix LIKE |
| **Composite index** | Index trên nhiều cột (thứ tự quan trọng) |
| **Partial index** | Index chỉ trên subset rows (WHERE clause) |
| **Normalization** | Quá trình tách bảng giảm trùng (1NF/2NF/3NF) |
| **Denormalize** | Copy data về bảng khác cho performance |
| **Referential integrity** | FK đảm bảo "không có orphan row" |
| **Junction table** | Bảng nối M-N relationship |
| **EXPLAIN** | Lệnh xem query plan |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [INSERT / UPDATE / DELETE & Transactions](04_insert-update-delete.md)
- ↑ **Về cụm:** [sql-fundamentals README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [REST API concepts](../../../../05_networking/http-https/lessons/01_basic/05_rest-api-concepts.md) — REST resource thường map 1:1 với SQL table

### 🌐 Tài nguyên tham khảo khác
- 📖 [Use The Index, Luke!](https://use-the-index-luke.com/) — bible về index/performance
- 📖 [Postgres docs: CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- 📖 [Database normalization explained — Vertabelo](https://vertabelo.com/blog/normalization-1nf-2nf-3nf/)
- 📖 [SQL Antipatterns — Bill Karwin](https://pragprog.com/titles/bksqla/sql-antipatterns/) — sách dày, đáng đọc
- 📖 [Postgres EXPLAIN visualizer](https://explain.dalibo.com/)

---

> 🎯 *Cluster SQL fundamentals basic 6/6 đóng. Bạn giờ có đủ kiến thức để **viết query 90% use case** + **thiết kế schema đúng từ đầu**. Bài kế tiếp có thể vào **02_intermediate** (subquery, CTE, window functions, indexes nâng cao) hoặc nhảy sang `06_databases/postgresql/` cụ thể.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `sql-fundamentals/` lesson 6/6. Cover: data types (numeric, text, boolean, date/time, JSON, ARRAY) + PK + FK + constraints (NOT NULL, UNIQUE, CHECK, DEFAULT) + 3 normalization form (1NF/2NF/3NF) + denormalization khi nào + indexes vai trò + ERD design + naming convention.
- **v1.1.0 (25/05/2026)** — Thêm lead-in 2-3 câu trước §1 Data types — Số numeric + Chuỗi text + Boolean + Date/Time + JSON/JSONB sections. Chuẩn hoá tên trong ví dụ normalization. Thêm Changelog section.
