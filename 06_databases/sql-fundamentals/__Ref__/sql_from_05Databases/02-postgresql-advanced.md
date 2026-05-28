# PostgreSQL Advanced

> **Tags:** `postgresql` `jsonb` `indexing` `partitioning` `performance` `rls`
> **Level:** Advanced | **Prerequisite:** `sql/01-sql-basics.md`

---

## 1. JSONB — Semi-structured Data

PostgreSQL `JSONB` lưu JSON dưới dạng binary — **indexable, queryable, efficient**:

```sql
-- JSONB vs JSON
-- JSON: stores as-is, preserves whitespace, duplicate keys OK
-- JSONB: binary, removes whitespace, deduplicates keys, faster queries

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'
);

INSERT INTO products (name, metadata) VALUES
('Widget Pro', '{"price": 29.99, "tags": ["sale", "featured"], "specs": {"weight": 1.5, "color": "red"}}');

-- JSONB operators
SELECT metadata -> 'price'           -- Returns JSONB: 29.99
SELECT metadata ->> 'price'          -- Returns TEXT: "29.99"  
SELECT metadata -> 'specs' -> 'color' -- Navigate nested: "red"
SELECT metadata #> '{specs,color}'    -- Same but with path array
SELECT metadata #>> '{specs,color}'   -- Returns TEXT

-- Filter using JSONB
SELECT * FROM products WHERE metadata ->> 'price' = '29.99';
SELECT * FROM products WHERE (metadata ->> 'price')::numeric > 20;
SELECT * FROM products WHERE metadata @> '{"tags": ["sale"]}';  -- Contains
SELECT * FROM products WHERE metadata ? 'price';                 -- Has key
SELECT * FROM products WHERE metadata ?& ARRAY['price', 'tags']; -- All keys exist
SELECT * FROM products WHERE metadata ?| ARRAY['sale', 'featured']; -- Any key

-- Update JSONB
UPDATE products SET metadata = metadata || '{"featured": true}'  -- Merge top-level
WHERE id = 1;

UPDATE products SET metadata = jsonb_set(metadata, '{specs,weight}', '2.0')
WHERE id = 1;

UPDATE products SET metadata = metadata - 'featured'   -- Remove key
WHERE id = 1;

-- Extract array elements
SELECT jsonb_array_elements(metadata -> 'tags') AS tag FROM products;
SELECT jsonb_object_keys(metadata) AS key FROM products;
```

### GIN Index on JSONB
```sql
-- GIN index: accelerates @>, ?, ?&, ?| operators
CREATE INDEX idx_products_metadata ON products USING GIN (metadata);

-- Specific path index (more selective)
CREATE INDEX idx_products_price ON products ((metadata ->> 'price'));
CREATE INDEX idx_products_tags ON products USING GIN ((metadata -> 'tags'));
```

---

## 2. Table Partitioning

Chia table lớn thành nhiều partitions để tăng hiệu suất query và maintenance:

### Range Partitioning (theo thời gian)
```sql
-- Create partitioned table
CREATE TABLE orders (
    id BIGSERIAL,
    user_id INT NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)  -- Partition key must be in PK
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Catch-all partition
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- Each partition can have its own indexes
CREATE INDEX ON orders_2024_q1 (user_id);
CREATE INDEX ON orders_2024_q2 (user_id);

-- Queries automatically route to correct partition (partition pruning)
EXPLAIN SELECT * FROM orders WHERE created_at >= '2024-07-01' AND created_at < '2024-10-01';
-- Shows: Seq Scan on orders_2024_q3 (only scans 1 partition!)
```

### List Partitioning
```sql
CREATE TABLE users (
    id SERIAL,
    country_code CHAR(2) NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id, country_code)
) PARTITION BY LIST (country_code);

CREATE TABLE users_us PARTITION OF users FOR VALUES IN ('US');
CREATE TABLE users_eu PARTITION OF users FOR VALUES IN ('DE', 'FR', 'IT', 'ES');
CREATE TABLE users_asia PARTITION OF users FOR VALUES IN ('JP', 'CN', 'KR', 'SG');
CREATE TABLE users_other PARTITION OF users DEFAULT;
```

### Hash Partitioning (distribute evenly)
```sql
CREATE TABLE events (
    id BIGSERIAL,
    session_id BIGINT NOT NULL,
    event_type TEXT,
    PRIMARY KEY (id, session_id)
) PARTITION BY HASH (session_id);

CREATE TABLE events_p0 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE events_p1 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE events_p2 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE events_p3 PARTITION OF events FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

### Partition Management
```sql
-- Drop old partition (vs deleting rows — much faster!)
DROP TABLE orders_2024_q1;

-- Detach partition (make it a standalone table)
ALTER TABLE orders DETACH PARTITION orders_2024_q1;

-- Attach existing table as partition
ALTER TABLE orders ATTACH PARTITION orders_2025_q1
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
```

---

## 3. Materialized Views

```sql
-- Create materialized view (stores computed result physically)
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS total_orders,
    SUM(total) AS revenue,
    AVG(total)::NUMERIC(10,2) AS avg_order_value
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;

-- Index on materialized view
CREATE UNIQUE INDEX ON monthly_sales (month);
CREATE INDEX ON monthly_sales (revenue);

-- Query (fast — reads from materialized data)
SELECT * FROM monthly_sales WHERE month >= '2024-01-01';

-- Refresh (full or concurrent)
REFRESH MATERIALIZED VIEW monthly_sales;                -- Takes LOCK (blocks reads briefly)
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;   -- No locks on reads (needs unique index)

-- Automate refresh
-- Option 1: pg_cron extension
SELECT cron.schedule('refresh-monthly-sales', '0 * * * *', 
    'REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales');

-- Option 2: Application-level on data change
```

---

## 4. LISTEN/NOTIFY

Real-time notifications within PostgreSQL:

```sql
-- Session 1 (listener)
LISTEN user_events;  -- Subscribe to channel

-- Session 2 (notifier)
NOTIFY user_events, '{"action": "created", "userId": 123}';
-- Session 1 receives notification immediately

-- In stored procedure/trigger
CREATE OR REPLACE FUNCTION notify_user_created()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('user_events', 
        json_build_object(
            'action', 'created',
            'userId', NEW.id,
            'email', NEW.email
        )::TEXT
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_user_insert
AFTER INSERT ON users
FOR EACH ROW EXECUTE FUNCTION notify_user_created();
```

```python
# Python async LISTEN
import asyncpg

async def main():
    conn = await asyncpg.connect("postgresql://localhost/mydb")
    
    async def handle_notification(conn, pid, channel, payload):
        import json
        data = json.loads(payload)
        print(f"Received: {data}")
        # Trigger WebSocket push, cache invalidation, etc.
    
    await conn.add_listener('user_events', handle_notification)
    await asyncio.sleep(float('inf'))  # Keep listening
```

---

## 5. Row Level Security (RLS)

Enforce data access policies at database level:

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts FORCE ROW LEVEL SECURITY;  -- Apply to table owners too

-- Policy: users can only see their own posts
CREATE POLICY user_isolation ON posts
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::INT)
    WITH CHECK (user_id = current_setting('app.current_user_id')::INT);

-- Admin can see all
CREATE POLICY admin_all ON posts
    FOR ALL
    TO app_admin  -- Role
    USING (true);

-- Set the context per request (from application)
SET LOCAL app.current_user_id = '123';  -- Transaction-local setting
SELECT * FROM posts;  -- Automatically filtered!

-- In application (e.g., FastAPI)
async def get_db_with_user(user_id: int):
    async with db.transaction():
        await db.execute(f"SET LOCAL app.current_user_id = '{user_id}'")
        yield db
```

---

## 6. pgBouncer — Connection Pooling

PostgreSQL nặng về connections — mỗi connection là 1 process:

```ini
; pgbouncer.ini

[databases]
myapp = host=127.0.0.1 port=5432 dbname=myapp

[pgbouncer]
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/users.txt

; Pool mode:
; transaction: connection returned after each transaction (BEST for most apps)
; session: connection held for entire session (DEFAULT, worst pooling)
; statement: connection returned after each statement (needs autocommit)
pool_mode = transaction

; Per-pool connection limits
default_pool_size = 20
max_client_conn = 1000
reserve_pool_size = 5

; Stats (useful for monitoring)
stats_period = 60
```

```bash
# Connect via pgBouncer (port 6432 instead of 5432)
psql -h localhost -p 6432 -U myuser myapp

# Monitoring
psql -h localhost -p 6432 -U pgbouncer pgbouncer
SHOW POOLS;
SHOW STATS;
SHOW CLIENTS;
```

### Pool sizing formula
```
Optimal pool size = (core_count * 2) + effective_spindle_count
# For 4-core, SSD server: 4 * 2 + 1 = ~9-10
# But test with your actual workload!

# Connection count monitoring
SELECT count(*) FROM pg_stat_activity;
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
```

---

## 7. VACUUM & Table Maintenance

PostgreSQL dùng MVCC — không xóa rows ngay khi DELETE/UPDATE, cần VACUUM để cleanup:

```sql
-- Check table bloat
SELECT
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    round(n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 2) AS dead_pct,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Manual VACUUM
VACUUM orders;                    -- Clean dead tuples, doesn't return to OS
VACUUM FULL orders;               -- Complete rewrite, returns space to OS (LOCKS table!)
VACUUM ANALYZE orders;            -- VACUUM + update statistics

-- Check autovacuum settings
SHOW autovacuum_vacuum_threshold;    -- 50 dead rows trigger
SHOW autovacuum_vacuum_scale_factor; -- 20% of table trigger

-- Per-table autovacuum tuning (high-update tables)
ALTER TABLE orders SET (
    autovacuum_vacuum_scale_factor = 0.05,  -- 5% threshold (more frequent)
    autovacuum_vacuum_cost_delay = 2,       -- Less throttling
    autovacuum_vacuum_threshold = 25
);
```

---

## 8. Advanced Indexing

```sql
-- Partial index — index only subset of rows
CREATE INDEX idx_orders_pending ON orders (created_at)
WHERE status = 'pending';  -- Only indexes pending orders!

-- Index on expression
CREATE INDEX idx_users_lower_email ON users (LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';  -- Uses index!

-- Covering index (include columns to avoid table lookup)
CREATE INDEX idx_orders_user_total ON orders (user_id) INCLUDE (total, status);
-- Query can be answered entirely from index:
SELECT total, status FROM orders WHERE user_id = 123;

-- GiST index (geometric types, full-text)
CREATE INDEX idx_products_name_gist ON products USING GIST (name gist_trgm_ops);
SELECT * FROM products WHERE name % 'wiget';  -- Fuzzy match!

-- BRIN index (Block Range INdex — for naturally ordered data)
CREATE INDEX idx_orders_created_brin ON orders USING BRIN (created_at);
-- Much smaller than B-tree, good for time-series append-only tables

-- Check index usage
SELECT
    schemaname, tablename, indexname,
    idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0   -- Unused indexes!
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## 9. Performance Monitoring Queries

```sql
-- Slow queries (requires pg_stat_statements extension)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT
    LEFT(query, 100) AS query,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms,
    round(mean_exec_time::numeric, 2) AS avg_ms,
    round(stddev_exec_time::numeric, 2) AS stddev_ms,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Blocking queries
SELECT
    activity.pid,
    activity.usename,
    activity.query,
    blocking.pid AS blocking_id,
    blocking.query AS blocking_query
FROM pg_stat_activity AS activity
JOIN pg_stat_activity AS blocking
    ON blocking.pid = ANY(pg_blocking_pids(activity.pid));

-- Table sizes
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS total_size,
    pg_size_pretty(pg_relation_size(tablename::regclass)) AS table_size,
    pg_size_pretty(pg_indexes_size(tablename::regclass)) AS indexes_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;

-- Cache hit ratio (should be > 99%)
SELECT
    sum(heap_blks_read) AS heap_read,
    sum(heap_blks_hit) AS heap_hit,
    round(sum(heap_blks_hit)::numeric / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0) * 100, 2) AS ratio
FROM pg_statio_user_tables;
```

---

## 10. Bài tập

1. **JSONB schema design**: Lưu product catalog với dynamic attributes dùng JSONB. Tạo GIN indexes phù hợp.
2. **Partitioning**: Tạo `events` table với monthly range partitions. Implement trigger để auto-create next month's partition.
3. **Materialized view**: Tạo daily sales summary materialized view với CONCURRENT refresh.
4. **RLS**: Implement multi-tenant system với RLS — mỗi tenant chỉ thấy data của mình.
5. **Performance tuning**: Dùng `pg_stat_statements` tìm 5 slowest queries trong database, analyze với EXPLAIN ANALYZE và add appropriate indexes.

---

*Tài liệu liên quan: `sql/01-sql-basics.md` | `sql/03-query-optimization.md` | `sql/04-transactions-isolation.md`*
