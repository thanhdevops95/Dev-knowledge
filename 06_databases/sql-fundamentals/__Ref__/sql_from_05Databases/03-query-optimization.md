# SQL Query Optimization

> **Tags:** `sql` `performance` `indexes` `query-plan` `explain` `optimization`
> **Level:** Intermediate | **Prerequisite:** `sql/01-sql-basics.md`

---

## 1. EXPLAIN và EXPLAIN ANALYZE

```sql
-- EXPLAIN: shows query plan WITHOUT executing
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';

-- EXPLAIN ANALYZE: executes AND shows actual vs estimated stats
EXPLAIN ANALYZE SELECT u.*, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id;

-- EXPLAIN (FORMAT JSON, ANALYZE, BUFFERS) — most detailed
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT ...;

-- Good tools to visualize EXPLAIN output:
-- https://explain.dalibo.com/
-- https://explain.depesz.com/
```

### Reading EXPLAIN output
```
Seq Scan on users  (cost=0.00..25000.00 rows=1000000 width=100) (actual time=0.05..420.32 rows=987654 loops=1)
   Filter: (active = true)
   Rows Removed by Filter: 12346

Hash Join  (cost=100.00..5500.00 rows=5000 width=200)
  Hash Cond: (orders.user_id = users.id)
  ->  Seq Scan on orders  ...
  ->  Hash  ...
      Buckets: 1024  Batches: 1  Memory Usage: 64kB

Index Scan using users_email_idx on users
  Index Cond: (email = 'alice@example.com')
```

**Key metrics:**
- `cost=0.00..25000.00` — startup cost .. total cost (arbitrary units)
- `rows=1000000` — **estimated** rows (từ statistics)
- `actual rows=987654` — **actual** rows
- `loops=1` — how many times node executed
- Node types: `Seq Scan` (slow on large), `Index Scan` (fast), `Index Only Scan` (fastest)

---

## 2. Index Types và Khi Nào Dùng

### B-Tree Index (default)
```sql
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_user_created ON orders (user_id, created_at);  -- Composite

-- Supports: =, <, >, <=, >=, BETWEEN, IN, LIKE 'prefix%'
-- Cannot use: LIKE '%suffix', functions on column (without functional index)
```

### Hash Index
```sql
CREATE INDEX idx_users_email_hash ON users USING HASH (email);
-- ONLY supports: = (equality)
-- Faster for equality, smaller than B-tree
-- Not WAL-logged before PG10 (risky)
```

### GIN Index (Generalized Inverted Index)
```sql
-- For arrays, JSONB, full-text search
CREATE INDEX idx_products_tags ON products USING GIN (tags);
CREATE INDEX idx_docs_content ON docs USING GIN (to_tsvector('english', content));
CREATE INDEX idx_meta ON items USING GIN (metadata jsonb_path_ops);

-- jsonb_path_ops: smaller, faster @> but no ?, ?&, ?|
```

### GiST Index
```sql
-- For geometric types, range types, fuzzy text (pg_trgm)
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_products_name_trgm ON products USING GIST (name gist_trgm_ops);

-- Now supports LIKE '%anywhere%' and similarity queries!
SELECT * FROM products WHERE name % 'widgt';  -- Fuzzy match, >0.3 similarity
SELECT * FROM products WHERE name LIKE '%widget%';  -- Uses GiST!
```

### BRIN Index (Block Range INdex)
```sql
-- For large tables with natural ordering (timestamps, auto-increment IDs)
-- Very small size (~1% of B-tree) but less precise
CREATE INDEX idx_events_created_brin ON events USING BRIN (created_at);

-- Good for: append-only time-series, logs, events
-- Bad for: random inserts, high-cardinality data
```

---

## 3. Index Strategies

### Composite Index Column Order
```sql
-- Index (a, b, c) helps queries:
-- WHERE a = ?                   ✅
-- WHERE a = ? AND b = ?         ✅
-- WHERE a = ? AND b = ? AND c = ?  ✅
-- WHERE b = ?                   ❌ (cannot skip a)
-- WHERE a = ? AND c = ?         ✅ for a, ❌ for c

-- Selectivity rule: put most selective (high cardinality) column FIRST
-- Unless you have both equality and range:
-- WHERE status = 'active' AND created_at > '2024-01-01'
-- Good: CREATE INDEX ON orders (status, created_at)  -- equality first!
```

### Partial Index
```sql
-- Index only rows matching condition — smaller, faster
CREATE INDEX idx_orders_pending ON orders (created_at)
WHERE status = 'pending';

-- Very useful when you mostly query a subset
SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at;  -- Fast!
SELECT * FROM orders WHERE status = 'completed';  -- Uses full scan (no partial index)

-- Another example: soft-deleted records
CREATE INDEX idx_users_active ON users (email)
WHERE deleted_at IS NULL;
```

### Functional Index
```sql
-- Index on expression result
CREATE INDEX idx_users_lower_email ON users (LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';  -- Uses index!

-- Without functional index, this would NOT use idx_users_email:
-- SELECT * FROM users WHERE LOWER(email) = ...
-- Because the expression changes the column value

-- Date truncation
CREATE INDEX idx_orders_month ON orders (DATE_TRUNC('month', created_at));
```

### Covering Index (Index-Only Scan)
```sql
-- INCLUDE columns so query can be answered from index alone
CREATE INDEX idx_orders_covering ON orders (user_id, status) INCLUDE (total, created_at);

-- This query needs NO table access:
SELECT user_id, status, total, created_at FROM orders WHERE user_id = 123;
-- (Index Only Scan — much faster!)

-- Without INCLUDE, above query would need:
-- Index Scan (index lookup) → Heap Fetch (table access) per row
```

---

## 4. Query Optimization Techniques

### SELECT specific columns (avoid SELECT *)
```sql
-- BAD: transfers and processes all columns
SELECT * FROM orders WHERE user_id = 123;

-- GOOD: only what you need
SELECT id, total, status FROM orders WHERE user_id = 123;
```

### LIMIT early in CTEs
```sql
-- BAD: compute full CTE then limit
WITH all_orders AS (
    SELECT * FROM orders
    WHERE user_id = 123
    ORDER BY created_at DESC
)
SELECT * FROM all_orders LIMIT 10;

-- GOOD: push limit into CTE
WITH recent_orders AS (
    SELECT * FROM orders
    WHERE user_id = 123
    ORDER BY created_at DESC
    LIMIT 10
)
SELECT * FROM recent_orders;
```

### EXISTS vs IN vs JOIN
```sql
-- For "does related row exist?" — EXISTS is often fastest
-- BAD (may scan all):
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

-- GOOD (short-circuits):
SELECT * FROM users u WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 1000
);

-- For counting/selecting related data, JOIN is usually best
SELECT u.id, u.name, COUNT(o.id) AS order_count
FROM users u
JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;
```

### Avoid Functions on Indexed Columns in WHERE
```sql
-- BAD: prevents index use on created_at
WHERE DATE(created_at) = '2024-01-15'
WHERE YEAR(created_at) = 2024

-- GOOD: range query on indexed column
WHERE created_at >= '2024-01-15' AND created_at < '2024-01-16'
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
```

### N+1 Queries (most common ORM mistake)
```sql
-- N+1: 1 query for users + N queries for their orders
-- BAD (ORM generates this):
SELECT * FROM users WHERE active = true;  -- Returns 1000 users
-- Then for each user:
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
-- ... 999 more queries!

-- GOOD: single JOIN query
SELECT u.id, u.name, o.id AS order_id, o.total
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.active = true;

-- Or: two queries total with IN clause
SELECT * FROM users WHERE active = true;
-- Get user IDs: [1, 2, ..., 1000]
SELECT * FROM orders WHERE user_id = ANY(ARRAY[1, 2, ..., 1000]);
```

---

## 5. Window Functions

```sql
-- ROW_NUMBER, RANK, DENSE_RANK
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank,    -- gaps in rank
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rank  -- no gaps
FROM employees;

-- Running totals
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS running_total,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM daily_sales;

-- LAG/LEAD — access previous/next rows
SELECT
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) AS prev_day_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) AS day_over_day_change,
    LEAD(revenue, 7) OVER (ORDER BY date) AS revenue_7_days_later
FROM daily_metrics;

-- FIRST_VALUE, LAST_VALUE, NTH_VALUE
SELECT
    id,
    amount,
    FIRST_VALUE(amount) OVER (ORDER BY date) AS first_day_amount,
    LAST_VALUE(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_day_amount
FROM sales;

-- NTILE — divide into N equal groups
SELECT
    id, salary,
    NTILE(4) OVER (ORDER BY salary) AS quartile   -- 1=bottom 25%, 4=top 25%
FROM employees;
```

---

## 6. CTEs — Common Table Expressions

```sql
-- Basic CTE
WITH active_users AS (
    SELECT id, name, email
    FROM users
    WHERE active = true AND last_login > NOW() - INTERVAL '30 days'
),
user_stats AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(total) AS lifetime_value
    FROM orders
    GROUP BY user_id
)
SELECT
    u.id, u.name, u.email,
    COALESCE(s.order_count, 0) AS orders,
    COALESCE(s.lifetime_value, 0) AS ltv
FROM active_users u
LEFT JOIN user_stats s ON s.user_id = u.id
ORDER BY s.lifetime_value DESC NULLS LAST;

-- Recursive CTE — for hierarchical data (categories, org charts, graphs)
WITH RECURSIVE category_tree AS (
    -- Base case: root categories
    SELECT id, name, parent_id, 0 AS depth, ARRAY[name] AS path
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    -- Recursive case: children
    SELECT c.id, c.name, c.parent_id, ct.depth + 1, ct.path || c.name
    FROM categories c
    JOIN category_tree ct ON ct.id = c.parent_id
)
SELECT * FROM category_tree ORDER BY path;

-- Materialized CTE (force materialization, prevent multiple executions)
WITH MATERIALIZED expensive_calc AS (
    SELECT id, expensive_function(data) AS result
    FROM large_table
)
SELECT * FROM expensive_calc WHERE result > 100
UNION ALL
SELECT * FROM expensive_calc WHERE result < 0;  -- Uses materialized result, not re-executed
```

---

## 7. Transactions & Locking

```sql
-- Transaction isolation levels
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;   -- Default in PostgreSQL
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;  -- Consistent snapshot
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;     -- Strictest, prevents phantom reads

-- Explicit locking
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;          -- Exclusive lock on rows
SELECT * FROM accounts WHERE id = 1 FOR SHARE;           -- Shared lock (allows other readers)
SELECT * FROM accounts WHERE id = 1 FOR UPDATE SKIP LOCKED;  -- Skip locked rows (queue pattern)
SELECT * FROM accounts WHERE id = 1 FOR UPDATE NOWAIT;   -- Fail immediately if locked

-- Advisory locks (application-level mutex)
SELECT pg_try_advisory_lock(12345);      -- Returns true if acquired
SELECT pg_advisory_lock(12345);          -- Blocks until acquired
SELECT pg_advisory_unlock(12345);        -- Release
-- Session-level: persist until end of session
-- Transaction-level: auto-released at end of transaction
SELECT pg_try_advisory_xact_lock(12345);
```

---

## 8. Common Performance Anti-patterns

```sql
-- ❌ OFFSET pagination at scale (reads and discards N rows)
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;  -- Reads 100020 rows!

-- ✅ Cursor/keyset pagination
SELECT * FROM orders WHERE id > 100000 ORDER BY id LIMIT 20;  -- Fast!

-- ❌ COUNT(*) on large tables
SELECT COUNT(*) FROM orders;   -- Full scan

-- ✅ Estimate (milliseconds vs seconds)
SELECT reltuples::BIGINT FROM pg_class WHERE relname = 'orders';

-- ❌ SELECT ... ORDER BY RANDOM() for small sample
SELECT * FROM large_table ORDER BY RANDOM() LIMIT 10;  -- Full scan + sort!

-- ✅ TABLESAMPLE for approximate random sample
SELECT * FROM large_table TABLESAMPLE BERNOULLI (1) LIMIT 10;  -- 1% sample

-- ❌ OR on multiple indexed columns (can't use indexes efficiently)
SELECT * FROM users WHERE email = 'a@b.com' OR phone = '555-1234';

-- ✅ UNION (each branch can use its own index)
SELECT * FROM users WHERE email = 'a@b.com'
UNION
SELECT * FROM users WHERE phone = '555-1234';
```

---

## 9. Statistics & Query Planner

```sql
-- Update statistics (runs automatically but can force)
ANALYZE orders;
ANALYZE;  -- All tables

-- View table statistics
SELECT * FROM pg_stats WHERE tablename = 'orders' AND attname = 'user_id';
-- Shows: null_frac, n_distinct, most_common_vals, histogram_bounds

-- Increase statistics target for skewed data
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;  -- default is 100
ANALYZE orders;

-- Check if planner is making good choices
SET enable_seqscan = off;  -- Force index usage for testing
EXPLAIN SELECT ...;         -- If plan changes, index will help but planner chose not to

-- Auto-explain slow queries
LOAD 'auto_explain';
SET auto_explain.log_min_duration = '1s';  -- Log plans for queries > 1s
SET auto_explain.log_analyze = true;
```

---

## 10. Cheatsheet

```sql
-- Find missing indexes (high seq scan + many rows)
SELECT schemaname, tablename, seq_scan, n_live_tup
FROM pg_stat_user_tables
WHERE seq_scan > 100 AND n_live_tup > 10000
ORDER BY seq_scan DESC;

-- Unused indexes
SELECT tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Long-running queries
SELECT pid, duration, query
FROM (
    SELECT pid, now() - pg_stat_activity.query_start AS duration, query
    FROM pg_stat_activity
    WHERE state = 'active'
) t
WHERE duration > interval '5 minutes'
ORDER BY duration DESC;

-- Kill long query
SELECT pg_cancel_backend(pid);   -- Graceful cancel
SELECT pg_terminate_backend(pid); -- Force kill
```

---

*Tài liệu liên quan: `sql/01-sql-basics.md` | `sql/02-postgresql-advanced.md` | `sql/04-transactions-isolation.md`*
