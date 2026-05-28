# 🔬 Labs: Databases for DevOps

---

## 🔬 Lab 1: RDS Setup

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password MyPassword123 \
  --allocated-storage 20

# Wait for available
aws rds wait db-instance-available --db-instance-identifier mydb

# Get endpoint
aws rds describe-db-instances --db-instance-identifier mydb \
  --query 'DBInstances[0].Endpoint.Address'
```

---

## 🔬 Lab 2: PostgreSQL Basics

```sql
-- Connect
psql -h mydb.xxx.rds.amazonaws.com -U admin -d postgres

-- Create database
CREATE DATABASE appdb;

-- Create table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert data
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');

-- Query
SELECT * FROM users;

-- Backup
pg_dump -h host -U admin appdb > backup.sql
```

---

## 🔬 Lab 3: Redis Caching

```bash
# Run Redis locally
docker run -d -p 6379:6379 --name redis redis:alpine

# Connect
redis-cli

# Basic operations
SET user:1 "John"
GET user:1
EXPIRE user:1 3600

# Hash
HSET user:1 name "John" email "john@example.com"
HGETALL user:1

# List
LPUSH queue job1 job2 job3
RPOP queue
```

---

## 🔬 Lab 4: Database Migrations

```bash
# Using Flyway
flyway -url=jdbc:postgresql://host:5432/db \
       -user=admin \
       -password=secret \
       migrate

# Migration file: V1__create_users.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

# V2__add_email.sql
ALTER TABLE users ADD COLUMN email VARCHAR(100);
```

---

## 🔬 Lab 5: Backup & Restore

```bash
# PostgreSQL backup
pg_dump -h host -U admin -d mydb > backup.sql
pg_dump -h host -U admin -d mydb -F c > backup.dump

# Restore
psql -h host -U admin -d mydb < backup.sql
pg_restore -h host -U admin -d mydb backup.dump

# AWS RDS snapshot
aws rds create-db-snapshot \
  --db-instance-identifier mydb \
  --db-snapshot-identifier mydb-snapshot
```

---

## ✅ Checklist

- [ ] Lab 1: RDS Setup
- [ ] Lab 2: PostgreSQL Basics
- [ ] Lab 3: Redis Caching
- [ ] Lab 4: Database Migrations
- [ ] Lab 5: Backup & Restore

---

**[← Back to README](./README.md)**
