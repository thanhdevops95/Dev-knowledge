# Module 06: Database Scenarios

---

## 🚨 Scenario 1: "Database connection refused"

### 📍 Bối cảnh

App startup báo lỗi:

```
Error: Connection refused to localhost:5432
```

### 🔍 Điều tra

**Bước 1: Service có chạy không?**

```bash
sudo systemctl status postgresql
```

**Bước 2: Đúng port không?**

```bash
ss -tuln | grep 5432
```

**Bước 3: Firewall?**

```bash
sudo ufw status
```

### 💡 Giải quyết

```bash
# Start service
sudo systemctl start postgresql

# Check config
sudo cat /etc/postgresql/*/main/postgresql.conf | grep listen_addresses
# listen_addresses = 'localhost'  # Chỉ local
# listen_addresses = '*'  # Tất cả interfaces
```

---

## 🚨 Scenario 2: "Database quá chậm"

### 📍 Bối cảnh

Query mất 30 giây thay vì milliseconds.

### 🔍 Điều tra

**Bước 1: Xem slow queries**

```sql
-- PostgreSQL
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds';
```

**Bước 2: Explain query**

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

**Output xấu:**

```
Seq Scan on orders  (cost=0.00..100000.00 rows=1000000 ...)
```

→ Đang scan toàn bộ table!

### 💡 Giải quyết

**Thêm index:**

```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Verify
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
-- Index Scan... (much faster)
```

---

## 🚨 Scenario 3: "Disk full - Database crash"

### 📍 Bối cảnh

```
FATAL: could not write to file: No space left on device
```

### 🔍 Điều tra

```bash
df -h
# /dev/sda1  100G  100G  0   100%  /
```

### 💡 Giải quyết

**Bước 1: Tìm files lớn**

```bash
sudo du -sh /var/lib/postgresql/* | sort -h
```

**Bước 2: Clean WAL logs**

```sql
-- PostgreSQL
CHECKPOINT;
SELECT pg_switch_wal();
```

**Bước 3: Vacuum**

```sql
VACUUM FULL;
```

**Bước 4: Clean old backups**

```bash
find /backup -name "*.sql.gz" -mtime +30 -delete
```

---

## 🚨 Scenario 4: "Redis memory full"

### 📍 Bối cảnh

```
OOM command not allowed when used memory > 'maxmemory'
```

### 🔍 Kiểm tra

```bash
redis-cli INFO memory
# used_memory_human:4.00G
# maxmemory_human:4.00G
```

### 💡 Giải quyết

**Option 1: Tăng maxmemory**

```bash
redis-cli CONFIG SET maxmemory 8gb
```

**Option 2: Eviction policy**

```bash
# Xóa keys ít dùng nhất
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

**Option 3: Clean unused keys**

```bash
redis-cli
> SCAN 0 MATCH "cache:*" COUNT 1000
> DEL cache:old_key
```

---

## 🚨 Scenario 5: "Lost data after container restart"

### 📍 Bối cảnh

Restart Docker container, data biến mất!

### 🔍 Nguyên nhân

Không mount volume → data lưu trong container layer → mất khi container die.

### 💡 Giải quyết

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data  # <-- Thêm dòng này

volumes:
  postgres_data:  # <-- Và dòng này
```

**Backup before fix:**

```bash
docker exec container_name pg_dump -U user dbname > backup.sql
```

---

## 📋 Database Troubleshooting Cheatsheet

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| Connection refused | Service down | Start service |
| Authentication failed | Wrong credentials | Check user/password |
| Slow queries | Missing index | Add index |
| Disk full | Too many logs | Clean up, vacuum |
| OOM | Memory limit | Increase memory, eviction |
| Data loss | No volumes | Add persistent volumes |
| Corrupted data | Crash | Restore from backup |

---

## ⏭️ Module tiếp theo

👉 **[Module 07: Docker](../07_DOCKER/README.md)**
