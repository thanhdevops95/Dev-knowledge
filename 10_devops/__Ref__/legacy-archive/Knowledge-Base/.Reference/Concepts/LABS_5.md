# Module 06: Database Labs

---

## 🎯 Mục tiêu

Sau labs này, bạn sẽ:

- Setup PostgreSQL và Redis
- CRUD operations
- Backup và restore
- Chạy databases trong Docker

---

## 🔧 Lab 1: PostgreSQL Setup

### Bước 1: Cài đặt

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Bước 2: Tạo database và user

```bash
# Connect as postgres
sudo -u postgres psql
```

```sql
-- Tạo database cho Counter App
CREATE DATABASE counter_app;

-- Tạo user
CREATE USER counter_user WITH PASSWORD 'counter_pass';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE counter_app TO counter_user;

\q
```

### Bước 3: Test connection

```bash
# Connect as new user
psql -h localhost -U counter_user -d counter_app

# Nếu báo lỗi authentication, edit pg_hba.conf:
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Đổi "peer" thành "md5" cho local connections
sudo systemctl reload postgresql
```

### ✅ Checkpoint Lab 1

- [ ] PostgreSQL running
- [ ] Database và user created
- [ ] Connect thành công

---

## 📝 Lab 2: CRUD với PostgreSQL

### Bước 1: Tạo table

```bash
psql -h localhost -U counter_user -d counter_app
```

```sql
-- Counter table
CREATE TABLE counters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    value INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verify
\dt
```

### Bước 2: Insert data

```sql
INSERT INTO counters (name, value) VALUES ('main', 0);
INSERT INTO counters (name, value) VALUES ('visits', 100);
INSERT INTO counters (name, value) VALUES ('clicks', 50);

-- Verify
SELECT * FROM counters;
```

### Bước 3: Update data

```sql
-- Increment counter
UPDATE counters SET value = value + 1, updated_at = NOW() WHERE name = 'main';

-- Verify
SELECT * FROM counters WHERE name = 'main';
```

### Bước 4: Query data

```sql
-- All counters
SELECT * FROM counters;

-- Specific counter
SELECT value FROM counters WHERE name = 'main';

-- Counters > 10
SELECT name, value FROM counters WHERE value > 10;

-- Count records
SELECT COUNT(*) FROM counters;
```

### Bước 5: Delete data

```sql
-- Delete specific
DELETE FROM counters WHERE name = 'clicks';

-- Verify
SELECT * FROM counters;
```

### ✅ Checkpoint Lab 2

- [ ] Create table
- [ ] Insert, Update, Delete
- [ ] Query với WHERE

---

## 💾 Lab 3: Backup và Restore

### Bước 1: Backup database

```bash
# Simple backup
pg_dump -U counter_user -h localhost counter_app > backup.sql

# With compression
pg_dump -U counter_user -h localhost counter_app | gzip > backup.sql.gz

# Check backup
head backup.sql
ls -lh backup.sql*
```

### Bước 2: Create test data

```bash
psql -U counter_user -h localhost counter_app
```

```sql
-- Add more data
INSERT INTO counters (name, value) VALUES ('test1', 100);
INSERT INTO counters (name, value) VALUES ('test2', 200);

SELECT * FROM counters;
\q
```

### Bước 3: Restore backup

```bash
# Drop and recreate database
sudo -u postgres psql -c "DROP DATABASE counter_app;"
sudo -u postgres psql -c "CREATE DATABASE counter_app OWNER counter_user;"

# Restore
psql -U counter_user -h localhost counter_app < backup.sql

# Or from gzip
gunzip -c backup.sql.gz | psql -U counter_user -h localhost counter_app

# Verify - test1, test2 should be gone
psql -U counter_user -h localhost counter_app -c "SELECT * FROM counters;"
```

### ✅ Checkpoint Lab 3

- [ ] Backup với pg_dump
- [ ] Restore database
- [ ] Verify data

---

## 🔴 Lab 4: Redis Setup và Operations

### Bước 1: Cài đặt

```bash
sudo apt install redis-server -y
sudo systemctl start redis
sudo systemctl enable redis

# Test
redis-cli ping
# PONG
```

### Bước 2: Basic operations

```bash
redis-cli
```

```redis
# String
SET counter 0
INCR counter
INCR counter
GET counter
# "2"

# With expiration (TTL)
SET session:abc123 "user_data" EX 300
TTL session:abc123
# 299

# Hash (object)
HSET user:1 name "John" email "john@test.com" visits 10
HGET user:1 name
HGETALL user:1
HINCRBY user:1 visits 1

# List (queue)
RPUSH tasks "task1"
RPUSH tasks "task2"
RPUSH tasks "task3"
LRANGE tasks 0 -1
LPOP tasks

# Set
SADD online_users "user1"
SADD online_users "user2"
SMEMBERS online_users
SCARD online_users
# 2

QUIT
```

### Bước 3: Python với Redis

```bash
pip3 install redis
```

```python
# test_redis.py
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Counter operations
r.set('page_views', 0)
for _ in range(10):
    r.incr('page_views')

print(f"Page views: {r.get('page_views').decode()}")

# Cache example
def get_user(user_id):
    cached = r.get(f'user:{user_id}')
    if cached:
        print("Cache hit!")
        return cached.decode()
    
    print("Cache miss - fetching from DB...")
    user = f"User {user_id} data"
    r.setex(f'user:{user_id}', 3600, user)  # Cache for 1 hour
    return user

print(get_user(1))  # Cache miss
print(get_user(1))  # Cache hit
```

```bash
python3 test_redis.py
```

### ✅ Checkpoint Lab 4

- [ ] Redis commands cơ bản
- [ ] Python Redis client

---

## 🐳 Lab 5: Databases với Docker

### Bước 1: Tạo docker-compose.yml

```bash
mkdir ~/db-docker
cd ~/db-docker
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: pg_container
    environment:
      POSTGRES_USER: devops
      POSTGRES_PASSWORD: devops123
      POSTGRES_DB: app_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"  # 5433 to avoid conflict with local postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devops"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: redis_container
    volumes:
      - redis_data:/data
    ports:
      - "6380:6379"  # 6380 to avoid conflict
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  redis_data:
```

### Bước 2: Start containers

```bash
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs
```

### Bước 3: Connect to databases

```bash
# PostgreSQL
docker exec -it pg_container psql -U devops -d app_db

# Redis
docker exec -it redis_container redis-cli
```

### Bước 4: Test persistence

```bash
# Add data
docker exec pg_container psql -U devops -d app_db -c "CREATE TABLE test (id INT);"
docker exec pg_container psql -U devops -d app_db -c "INSERT INTO test VALUES (1);"

# Restart containers
docker-compose down
docker-compose up -d

# Data should persist
docker exec pg_container psql -U devops -d app_db -c "SELECT * FROM test;"
```

### Bước 5: Cleanup

```bash
docker-compose down

# Remove volumes too
docker-compose down -v
```

### ✅ Checkpoint Lab 5

- [ ] Docker Compose cho databases
- [ ] Data persistence với volumes
- [ ] Connect từ host

---

## 🎓 Tổng kết Labs

| Lab | Skill | Output |
|-----|-------|--------|
| 1 | PostgreSQL setup | Database running |
| 2 | CRUD operations | Table với data |
| 3 | Backup/Restore | Protected data |
| 4 | Redis operations | Caching working |
| 5 | Docker databases | Containerized DBs |

---

## ⏭️ Tiếp theo

👉 **[SCENARIOS.md - Tình huống Database](SCENARIOS.md)**
