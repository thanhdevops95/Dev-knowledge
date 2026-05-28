# 🗄️ PostgreSQL nâng cao — Performance, Indexing & Patterns

> `[INTERMEDIATE → ADVANCED]` — Khai thác PostgreSQL hiệu quả

---

## 1. Advanced Indexing

### Index Types

```sql
-- B-tree (default): equality, range, sorting
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_date ON orders (created_at DESC);

-- Partial index: chỉ index rows matching condition
CREATE INDEX idx_active_users ON users (email) WHERE active = true;
-- Tiết kiệm space + nhanh hơn. Chỉ 10% users active → index nhỏ 10x!

-- Composite index (thứ tự QUAN TRỌNG!)
CREATE INDEX idx_orders_user_date ON orders (user_id, created_at DESC);
-- ✅ WHERE user_id = 1 ORDER BY created_at DESC
-- ✅ WHERE user_id = 1
-- ❌ WHERE created_at > '2026-01-01' (cần user_id trước!)

-- GIN index: full-text search, JSONB, arrays
CREATE INDEX idx_products_tags ON products USING GIN (tags);
CREATE INDEX idx_products_search ON products USING GIN (to_tsvector('english', name || ' ' || description));

-- SELECT * FROM products WHERE to_tsvector('english', name || ' ' || description) @@ to_tsquery('english', 'laptop & gaming');

-- BRIN index: data tự nhiên ordered (timestamps, sequential IDs)
CREATE INDEX idx_events_time ON events USING BRIN (created_at);
-- Nhỏ 100x so với B-tree! Tốt cho time-series data.
```

### EXPLAIN ANALYZE — Hiểu query plan

```sql
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.active = true
GROUP BY u.name
ORDER BY order_count DESC
LIMIT 10;

-- Output:
-- Limit (cost=100..105 rows=10) (actual time=15.2..15.3 rows=10)
--   → Sort (cost=100..102 rows=500) (actual time=15.1..15.2 rows=500)
--     → HashAggregate (cost=80..90 rows=500) (actual time=12.0..12.5 rows=500)
--       → Hash Join (cost=20..70 rows=5000) (actual time=2.0..10.0 rows=5000)
--         → Seq Scan on users (cost=0..10 rows=500) (actual time=0.1..1.0 rows=500)
--              Filter: (active = true)
--         → Hash (cost=0..5 rows=10000) (actual time=0.5..0.5 rows=10000)
--           → Seq Scan on orders ← ❌ Cần index!

-- Fix: CREATE INDEX idx_orders_user_id ON orders (user_id);
-- Sau khi tạo index: Seq Scan → Index Scan!
```

---

## 2. Window Functions — SQL nâng cao

```sql
-- ROW_NUMBER: xếp hạng
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
-- Rank nhân viên TRONG MỖI department

-- LAG/LEAD: so sánh với row trước/sau
SELECT
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) as prev_day_revenue,
    revenue - LAG(revenue) OVER (ORDER BY date) as daily_change,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY date))::numeric
        / LAG(revenue) OVER (ORDER BY date) * 100, 2
    ) as change_pct
FROM daily_revenue;

-- Running total
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) as running_total
FROM transactions;

-- Moving average (7 ngày)
SELECT
    date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d
FROM daily_revenue;
```

---

## 3. CTEs & Recursive Queries

```sql
-- CTE (Common Table Expression): đặt tên cho subquery
WITH monthly_stats AS (
    SELECT
        DATE_TRUNC('month', created_at) as month,
        COUNT(*) as order_count,
        SUM(total) as revenue
    FROM orders
    WHERE created_at >= '2026-01-01'
    GROUP BY DATE_TRUNC('month', created_at)
),
growth AS (
    SELECT
        month,
        order_count,
        revenue,
        LAG(revenue) OVER (ORDER BY month) as prev_revenue
    FROM monthly_stats
)
SELECT
    month,
    order_count,
    revenue,
    ROUND((revenue - prev_revenue) / prev_revenue * 100, 1) as growth_pct
FROM growth;

-- Recursive CTE: hierarchical data (org chart, categories)
WITH RECURSIVE category_tree AS (
    -- Base case: root categories
    SELECT id, name, parent_id, 0 as depth, name::text as path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive step
    SELECT c.id, c.name, c.parent_id, ct.depth + 1, ct.path || ' > ' || c.name
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY path;

-- Output:
-- Electronics
-- Electronics > Laptops
-- Electronics > Laptops > Gaming Laptops
-- Electronics > Phones
```

---

## 4. JSONB — NoSQL trong PostgreSQL

```sql
-- Tạo table với JSONB column
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'
);

-- Insert
INSERT INTO products (name, metadata) VALUES
('MacBook Pro', '{
    "brand": "Apple",
    "specs": {"ram": 16, "storage": 512},
    "tags": ["laptop", "premium"],
    "reviews": [{"score": 5, "text": "Great!"}]
}');

-- Query JSONB
SELECT name, metadata->>'brand' as brand              -- Text
FROM products WHERE metadata->>'brand' = 'Apple';

SELECT name, (metadata->'specs'->>'ram')::int as ram   -- Nested + cast
FROM products WHERE (metadata->'specs'->>'ram')::int >= 16;

SELECT name FROM products
WHERE metadata->'tags' ? 'premium';                    -- Array contains

-- Update JSONB
UPDATE products
SET metadata = jsonb_set(metadata, '{specs,ram}', '32')
WHERE id = 1;

-- GIN index cho JSONB queries
CREATE INDEX idx_products_metadata ON products USING GIN (metadata);
```

---

## 5. Performance Tuning

```sql
-- Connection pooling: PgBouncer
-- pgbouncer.ini
-- [databases]
-- mydb = host=localhost port=5432 dbname=mydb
-- [pgbouncer]
-- pool_mode = transaction     -- Share connections between transactions
-- max_client_conn = 1000
-- default_pool_size = 25

-- Vacuum: dọn dead tuples
-- PostgreSQL MVCC → UPDATE/DELETE tạo dead tuples
VACUUM ANALYZE orders;          -- Dọn + update statistics
VACUUM (VERBOSE) orders;        -- Xem chi tiết

-- Cấu hình quan trọng (postgresql.conf)
-- shared_buffers = 25% RAM (4GB cho server 16GB)
-- effective_cache_size = 75% RAM
-- work_mem = 64MB (per sort operation)
-- maintenance_work_mem = 512MB (for VACUUM, CREATE INDEX)
-- random_page_cost = 1.1 (SSD) hoặc 4 (HDD)

-- Monitoring queries chậm
-- log_min_duration_statement = 1000  -- Log queries > 1 giây

-- pg_stat_statements: top slow queries
SELECT
    query,
    calls,
    mean_exec_time::numeric(10,2) as avg_ms,
    total_exec_time::numeric(10,2) as total_ms
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## 6. Partitioning — Tables lớn

```sql
-- Range partitioning: chia theo thời gian
CREATE TABLE events (
    id BIGSERIAL,
    event_type TEXT,
    payload JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE events_2026_02 PARTITION OF events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE events_2026_03 PARTITION OF events
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- Query chỉ scan partition liên quan
SELECT * FROM events WHERE created_at >= '2026-03-01';
-- → Chỉ scan events_2026_03, skip tất cả partitions khác!

-- Auto-create partitions: pg_partman extension
```

---

## Các lỗi thường gặp

```
❌ Sai: SELECT * everywhere
✅ Đúng: Chỉ SELECT columns cần thiết → giảm I/O

❌ Sai: N+1 queries (loop query trong app code)
✅ Đúng: JOIN hoặc WHERE id IN (...) batch query

❌ Sai: Index mỗi column → write chậm
✅ Đúng: Index theo query patterns thực tế. Review pg_stat_user_indexes.
```

---

## Bài tập thực hành

- [ ] EXPLAIN ANALYZE: tìm slow query → tạo index fix
- [ ] Window functions: monthly growth report
- [ ] Recursive CTE: category tree / org chart
- [ ] JSONB: product catalog với flexible attributes

---

## Tài nguyên thêm

- [PostgreSQL Docs](https://www.postgresql.org/docs/) — Official
- [Use The Index, Luke](https://use-the-index-luke.com/) — Indexing guide
- [pganalyze](https://pganalyze.com/docs) — Performance monitoring
