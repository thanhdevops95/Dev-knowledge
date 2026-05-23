# 🗄️ SQL & Cơ sở dữ liệu quan hệ

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Kỹ năng bắt buộc với mọi backend developer

---

## SQL là gì?

**SQL (Structured Query Language)** là ngôn ngữ để tương tác với cơ sở dữ liệu quan hệ. Học 1 lần, dùng được hầu hết: PostgreSQL, MySQL, SQLite, SQL Server...

**Cơ sở dữ liệu khuyên dùng: PostgreSQL** — Mạnh nhất, open source, dùng rộng rãi nhất.

---

## Cài đặt (Local với Docker)

```bash
docker run -d \
  --name my-postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  postgres:16-alpine

# Kết nối
docker exec -it my-postgres psql -U postgres -d mydb
# Hoặc dùng GUI: TablePlus, DBeaver, DataGrip
```

---

## Data Types phổ biến

| Type | Mô tả | Ví dụ |
|---|---|---|
| `INT`, `BIGINT` | Số nguyên | id, tuổi |
| `DECIMAL(p,s)` | Số thập phân chính xác | giá tiền |
| `FLOAT`, `DOUBLE` | Số thực | tọa độ |
| `VARCHAR(n)` | Chuỗi độ dài biến | name, email |
| `TEXT` | Chuỗi không giới hạn | nội dung bài viết |
| `BOOLEAN` | True/False | is_active |
| `DATE` | Ngày | 2026-02-19 |
| `TIMESTAMP` | Ngày + giờ | 2026-02-19 13:00:00 |
| `TIMESTAMPTZ` | Có timezone (PostgreSQL) | |
| `UUID` | ID duy nhất | primary key |
| `JSONB` | JSON (PostgreSQL) | metadata |
| `ARRAY` | Mảng (PostgreSQL) | tags |

---

## DDL — Định nghĩa cấu trúc

```sql
-- Tạo bảng
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    name        VARCHAR(100) NOT NULL,
    age         INT CHECK (age >= 0 AND age <= 150),
    role        VARCHAR(20) DEFAULT 'user',
    bio         TEXT,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE posts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       VARCHAR(500) NOT NULL,
    content     TEXT,
    author_id   UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status      VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    tags        TEXT[],                      -- PostgreSQL array
    metadata    JSONB DEFAULT '{}',          -- PostgreSQL JSONB
    view_count  INT DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Sửa bảng
ALTER TABLE users ADD COLUMN avatar_url TEXT;
ALTER TABLE users ALTER COLUMN name SET NOT NULL;
ALTER TABLE users DROP COLUMN bio;
ALTER TABLE posts RENAME COLUMN title TO heading;

-- Xóa bảng
DROP TABLE IF EXISTS posts;
TRUNCATE TABLE posts;                        -- Xóa data, giữ cấu trúc
```

---

## DML — Thao tác dữ liệu

```sql
-- INSERT
INSERT INTO users (email, name, role) VALUES
    ('alice@example.com', 'Alice', 'admin'),
    ('bob@example.com', 'Bob', 'user'),
    ('charlie@example.com', 'Charlie', 'user');

-- INSERT ... RETURNING (PostgreSQL)
INSERT INTO users (email, name)
VALUES ('dave@example.com', 'Dave')
RETURNING id, created_at;

-- SELECT
SELECT * FROM users;
SELECT id, name, email FROM users;
SELECT DISTINCT role FROM users;

-- WHERE
SELECT * FROM users WHERE is_active = TRUE;
SELECT * FROM users WHERE age BETWEEN 18 AND 30;
SELECT * FROM users WHERE name LIKE 'A%';        -- Bắt đầu bằng A
SELECT * FROM users WHERE name ILIKE '%alice%';  -- Case-insensitive
SELECT * FROM users WHERE role IN ('admin', 'moderator');
SELECT * FROM users WHERE avatar_url IS NULL;

-- UPDATE
UPDATE users SET is_active = FALSE WHERE role = 'user' AND age < 18;
UPDATE users SET updated_at = NOW() WHERE id = '...';

-- DELETE
DELETE FROM users WHERE is_active = FALSE AND created_at < NOW() - INTERVAL '1 year';

-- UPSERT (PostgreSQL)
INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice Updated')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name, updated_at = NOW();
```

---

## Queries nâng cao

```sql
-- ORDER BY
SELECT * FROM users ORDER BY name ASC, created_at DESC;

-- LIMIT & OFFSET (Pagination)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 10 OFFSET 20;

-- Aggregate Functions
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FILTER (WHERE is_active) AS active_count FROM users;
SELECT AVG(age), MAX(age), MIN(age) FROM users;
SELECT role, COUNT(*) AS total FROM users GROUP BY role;
SELECT role, COUNT(*) AS total FROM users 
GROUP BY role HAVING COUNT(*) > 10
ORDER BY total DESC;

-- Subquery
SELECT * FROM users
WHERE id IN (
    SELECT DISTINCT author_id FROM posts WHERE status = 'published'
);

-- EXISTS
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM posts p WHERE p.author_id = u.id
);
```

---

## JOINs ⭐

```sql
-- INNER JOIN — Chỉ lấy records khớp cả 2 bảng
SELECT u.name, p.title
FROM users u
INNER JOIN posts p ON u.id = p.author_id;

-- LEFT JOIN — Tất cả users, kể cả chưa có bài viết
SELECT u.name, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
GROUP BY u.id, u.name;

-- RIGHT JOIN — Tất cả posts, kể cả không có author
SELECT u.name, p.title
FROM users u
RIGHT JOIN posts p ON u.id = p.author_id;

-- FULL OUTER JOIN
SELECT u.name, p.title
FROM users u
FULL OUTER JOIN posts p ON u.id = p.author_id;

-- SELF JOIN
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

---

## Window Functions (PostgreSQL)

```sql
-- ROW_NUMBER — Đánh số dòng trong mỗi nhóm
SELECT
    name,
    role,
    ROW_NUMBER() OVER (PARTITION BY role ORDER BY created_at) AS rank_in_role
FROM users;

-- RANK, DENSE_RANK
SELECT
    name,
    view_count,
    RANK() OVER (ORDER BY view_count DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY view_count DESC) AS dense_rank
FROM posts;

-- LAG, LEAD — Giá trị dòng trước/sau
SELECT
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) AS prev_revenue,
    revenue - LAG(revenue) OVER (ORDER BY date) AS growth
FROM daily_revenue;

-- SUM với OVER — Running total
SELECT
    date,
    revenue,
    SUM(revenue) OVER (ORDER BY date) AS cumulative_revenue
FROM daily_revenue;
```

---

## Indexes ⭐

```sql
-- Index tăng tốc SELECT nhưng làm chậm INSERT/UPDATE/DELETE
-- Tạo index cho các cột thường WHERE, JOIN, ORDER BY

-- B-tree index (mặc định)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_status_created ON posts(status, created_at DESC);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index — chỉ index một phần dữ liệu
CREATE INDEX idx_posts_published ON posts(created_at)
WHERE status = 'published';

-- Full-text search index
CREATE INDEX idx_posts_content_fts ON posts USING GIN(to_tsvector('english', content));

-- Xem query plan
EXPLAIN ANALYZE SELECT * FROM posts WHERE author_id = '...';

-- Liệt kê indexes
SELECT indexname, tablename FROM pg_indexes WHERE tablename = 'posts';
```

---

## Transactions

```sql
BEGIN;

    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;

    -- Nếu có lỗi:
    -- ROLLBACK;

COMMIT;

-- Savepoint
BEGIN;
    INSERT INTO orders (user_id) VALUES (1) RETURNING id INTO order_id;
    SAVEPOINT after_order;
    
    INSERT INTO order_items (order_id, product_id) VALUES (order_id, 5);
    
    -- Rollback về savepoint nếu lỗi items
    ROLLBACK TO after_order;
    
COMMIT;
```

---

## CTEs (Common Table Expressions)

```sql
-- WITH clause — Readable subqueries
WITH active_users AS (
    SELECT id, name FROM users WHERE is_active = TRUE
),
published_posts AS (
    SELECT id, title, author_id FROM posts WHERE status = 'published'
)
SELECT u.name, COUNT(p.id) AS post_count
FROM active_users u
LEFT JOIN published_posts p ON u.id = p.author_id
GROUP BY u.id, u.name
ORDER BY post_count DESC;

-- Recursive CTE
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 0 AS level
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive: employees
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;
```

---

## Bài tập thực hành

- [ ] Thiết kế schema cho E-commerce (users, products, orders, order_items)
- [ ] Viết query lấy top 10 sản phẩm bán chạy nhất (dùng JOIN + GROUP BY)
- [ ] Tạo indexes hợp lý và dùng EXPLAIN ANALYZE để so sánh
- [ ] Viết transaction cho quá trình đặt hàng

---

## Tài nguyên thêm

- [PostgreSQL Docs](https://www.postgresql.org/docs/) — Tài liệu chính thức
- [SQLZoo](https://sqlzoo.net/) — Luyện tập SQL interactive
- [Use The Index, Luke](https://use-the-index-luke.com/) — Indexing chuyên sâu
- [pgexercises.com](https://pgexercises.com/) — Bài tập PostgreSQL
