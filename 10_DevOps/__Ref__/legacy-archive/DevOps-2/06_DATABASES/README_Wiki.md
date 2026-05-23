# Module 06: Databases

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Database** | - | Cơ sở dữ liệu - Nơi lưu trữ dữ liệu có cấu trúc |
| **SQL** | - | Structured Query Language - Ngôn ngữ truy vấn database |
| **NoSQL** | - | Không dùng SQL - Database linh hoạt (MongoDB, Redis) |
| **RDBMS** | - | Relational Database Management System - PostgreSQL, MySQL |
| **Table** | - | Bảng - Nơi lưu dữ liệu trong SQL database |
| **Schema** | - | Cấu trúc định nghĩa các bảng và quan hệ |
| **ACID** | - | Atomicity, Consistency, Isolation, Durability - Tính chất transaction |
| **Query** | - | Truy vấn - Câu lệnh lấy/sửa dữ liệu |
| **Index** | - | Chỉ mục - Tăng tốc tìm kiếm |
| **Replication** | - | Sao chép dữ liệu sang server backup |
| **Backup** | - | Sao lưu dữ liệu để phục hồi khi cần |
| **PostgreSQL** | - | Database SQL mạnh mẽ, open source |
| **Redis** | /ˈredɪs/ | In-memory database cực nhanh, dùng cho caching |
| **TTL** | - | Time To Live - Thời gian data tồn tại trong Redis |

---

## 📖 Database là gì? (Định nghĩa từ gốc)

### Trước hết: Tại sao cần lưu trữ dữ liệu?

Khi bạn chạy một chương trình:

- **Biến trong RAM** → Mất khi tắt chương trình
- **File text** → Chậm khi tìm kiếm, khó query phức tạp

**Vấn đề thực tế:**

| Yêu cầu | File text | Database |
|---------|-----------|----------|
| Lưu 1 triệu users | ✓ (chậm) | ✓ (nhanh) |
| Tìm user theo email | Phải đọc hết file | Index, micro-giây |
| 100 người ghi cùng lúc | Conflict! | Transaction, ACID |
| Backup và recovery | Thủ công | Tự động |

### Database = Hệ thống lưu trữ có cấu trúc

> **Database = Phần mềm chuyên dụng để lưu trữ, tổ chức, và truy xuất dữ liệu hiệu quả**

Cụ thể, database cung cấp:

- **Cấu trúc dữ liệu** → Bảng, cột, quan hệ
- **Query language** → SQL để tìm kiếm phức tạp
- **Indexing** → Tìm kiếm nhanh trong triệu records
- **Transactions** → Đảm bảo dữ liệu consistent
- **Concurrency** → Nhiều người đọc/ghi cùng lúc
- **Backup/Recovery** → Không mất dữ liệu

### DevOps cần biết gì về Database?

DevOps không cần viết complex queries, nhưng cần:

| Kỹ năng | Tại sao |
|---------|---------|
| **Backup & Restore** | Khôi phục dữ liệu khi có sự cố |
| **Replication** | Setup master-slave, high availability |
| **Monitoring** | Phát hiện slow queries, disk đầy |
| **Connection pooling** | Tối ưu kết nối từ app đến DB |
| **Migration** | Di chuyển DB giữa các servers |

---

## 🎬 Câu chuyện thực tế

Mỗi ứng dụng cần **lưu trữ dữ liệu** persistent:

- User accounts và passwords
- Orders và transactions  
- Products và inventory
- Sessions và cache

Câu hỏi: **Dùng Database nào?**

Không có câu trả lời "tốt nhất". Mỗi loại database phù hợp với use case khác nhau.

---

## 📖 Database Types

### SQL vs NoSQL

```
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE TYPES                          │
├────────────────────────────┬────────────────────────────────┤
│          SQL               │           NoSQL                │
│    (Relational)            │       (Non-relational)         │
├────────────────────────────┼────────────────────────────────┤
│ • Tables, rows, columns    │ • Documents, key-value, graphs │
│ • Fixed schema             │ • Flexible schema              │
│ • ACID transactions        │ • Eventually consistent        │
│ • Complex queries (JOIN)   │ • Simple queries, fast reads   │
├────────────────────────────┼────────────────────────────────┤
│ PostgreSQL, MySQL          │ MongoDB, Redis, DynamoDB       │
│ MariaDB, SQLite            │ Cassandra, Elasticsearch       │
└────────────────────────────┴────────────────────────────────┘
```

### Khi nào dùng gì?

| Use Case | Database | Lý do |
|----------|----------|-------|
| E-commerce (orders, users) | PostgreSQL | ACID, complex queries |
| Blog, CMS | MySQL | Simple, widely supported |
| Session storage | Redis | Fast, in-memory |
| Real-time analytics | MongoDB | Flexible schema |
| Caching | Redis, Memcached | Microsecond latency |
| Full-text search | Elasticsearch | Search optimized |

---

## 🐘 PostgreSQL

### Tại sao PostgreSQL?

- **Open source** và miễn phí
- **Feature-rich**: JSON, full-text search, GIS
- **ACID compliant**: Transactions đáng tin cậy
- **Extensible**: Plugins và custom types
- **Cloud support**: AWS RDS, GCP Cloud SQL, Azure

### Cài đặt

```bash
# Ubuntu
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql
```

### Basic Operations

```bash
# Connect as postgres user
sudo -u postgres psql

# Trong psql shell:
```

```sql
-- Tạo database
CREATE DATABASE myapp;

-- Tạo user
CREATE USER myuser WITH PASSWORD 'mypassword';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE myapp TO myuser;

-- Connect to database
\c myapp

-- Tạo table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data
INSERT INTO users (email, name) VALUES ('john@example.com', 'John Doe');

-- Query
SELECT * FROM users;

-- Exit
\q
```

### Connection String

```
postgresql://myuser:mypassword@localhost:5432/myapp
```

### Backup & Restore

```bash
# Backup
pg_dump myapp > backup.sql

# Backup với compression
pg_dump myapp | gzip > backup.sql.gz

# Restore
psql myapp < backup.sql

# Restore from gzip
gunzip -c backup.sql.gz | psql myapp
```

---

## 🔴 Redis

### Redis là gì?

**Redis** = **Re**mote **Di**ctionary **S**erver

In-memory data store, cực kỳ nhanh (microseconds).

### Use Cases

| Use Case | Ví dụ |
|----------|-------|
| **Caching** | Cache API responses |
| **Sessions** | Store user sessions |
| **Rate Limiting** | Limit API calls per IP |
| **Pub/Sub** | Real-time notifications |
| **Queues** | Job queues |
| **Leaderboards** | Gaming scores |

### Cài đặt

```bash
# Ubuntu
sudo apt install redis-server -y

# Start
sudo systemctl start redis
sudo systemctl enable redis

# Test
redis-cli ping
# PONG
```

### Basic Operations

```bash
# Connect
redis-cli

# Trong redis-cli:
```

```redis
# Set key-value
SET name "John"

# Get value
GET name
# "John"

# Set with expiration (60 seconds)
SET session:123 "user_data" EX 60

# Check TTL
TTL session:123
# 58

# Delete
DEL name

# Check exists
EXISTS name
# 0

# Increment counter
SET counter 0
INCR counter
# 1
INCR counter
# 2

# Hash (object-like)
HSET user:1 name "John" email "john@example.com"
HGET user:1 name
HGETALL user:1

# List (queue)
LPUSH queue "task1"
LPUSH queue "task2"
RPOP queue
# "task1"

# Exit
QUIT
```

### Python với Redis

```python
import redis

# Connect
r = redis.Redis(host='localhost', port=6379, db=0)

# Set/Get
r.set('name', 'John')
print(r.get('name'))  # b'John'

# With expiration
r.setex('session', 3600, 'session_data')  # 1 hour

# Increment
r.incr('counter')
print(r.get('counter'))  # b'1'
```

---

## 💾 Database trong DevOps

### Backup Strategy

```
┌─────────────────────────────────────────────────────┐
│                 BACKUP STRATEGY                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Full Backup ────────────────────────────── Weekly   │
│       │                                              │
│       │   Incremental ──────────────────── Daily    │
│       │        │                                     │
│       │        │   Transaction Logs ───── Hourly    │
│       │        │          │                          │
│       ▼        ▼          ▼                          │
│   ┌──────┐ ┌──────┐ ┌──────┐                        │
│   │ S3   │ │ S3   │ │ S3   │                        │
│   └──────┘ └──────┘ └──────┘                        │
│                                                      │
│   Retention: 30 days                                 │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Database trong Docker

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  redis_data:
```

---

## 📝 Tổng kết Module 06

### Bạn đã học

✅ SQL vs NoSQL và khi nào dùng  
✅ PostgreSQL basics  
✅ Redis caching  
✅ Backup strategies  
✅ Database trong Docker  

---

## ⏭️ Tiếp theo

👉 **[LABS.md - Thực hành Database](LABS.md)**
