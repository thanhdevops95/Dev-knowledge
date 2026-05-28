# 📋 Databases for DevOps - Cheatsheet

> **Quick Reference for Database Commands**
>
> *Tra cứu nhanh lệnh cơ sở dữ liệu*

---

## 🐘 PostgreSQL

```bash
# Connect (Kết nối)
psql -h localhost -U postgres -d mydb

# Common commands in psql
\l                              # List databases (Liệt kê databases)
\c mydb                         # Connect to database (Kết nối)
\dt                             # List tables (Liệt kê tables)
\d tablename                    # Describe table (Mô tả table)
\q                              # Quit (Thoát)
```

```sql
-- Basic SQL
SELECT * FROM users LIMIT 10;
CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'pass';
GRANT ALL ON DATABASE mydb TO myuser;
```

---

## 🐬 MySQL

```bash
# Connect (Kết nối)
mysql -h localhost -u root -p

# Common commands
SHOW DATABASES;
USE mydb;
SHOW TABLES;
DESCRIBE tablename;
```

```sql
-- User management (Quản lý user)
CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON mydb.* TO 'user'@'%';
FLUSH PRIVILEGES;
```

---

## 🔴 Redis

```bash
# Connect (Kết nối)
redis-cli
redis-cli -h localhost -p 6379

# Common commands (Lệnh phổ biến)
SET key "value"                 # Set key
GET key                        # Get key
DEL key                        # Delete key
KEYS *                         # List all keys
TTL key                        # Time to live
EXPIRE key 3600                # Set expiry (seconds)
FLUSHDB                        # Clear database
INFO                           # Server info
```

---

## 🍃 MongoDB

```bash
# Connect (Kết nối)
mongosh
mongosh "mongodb://localhost:27017"

# Common commands (Lệnh phổ biến)
show dbs                       # List databases
use mydb                       # Switch database
show collections               # List collections
db.users.find()               # Find all
db.users.find({name: "John"}) # Find with filter
db.users.insertOne({...})     # Insert one
db.users.deleteOne({...})     # Delete one
```

---

## 🐳 Docker Commands

```bash
# PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 postgres:15

# MySQL
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -p 3306:3306 mysql:8

# Redis
docker run -d --name redis \
  -p 6379:6379 redis:alpine

# MongoDB
docker run -d --name mongo \
  -p 27017:27017 mongo:6
```

---

## 📊 Common Ports (Cổng phổ biến)

| Database | Port |
|----------|------|
| PostgreSQL | 5432 |
| MySQL | 3306 |
| Redis | 6379 |
| MongoDB | 27017 |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
