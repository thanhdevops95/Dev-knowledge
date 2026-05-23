# Module 06: DATABASES

> **"Data là vàng - biết quản lý database là kỹ năng sống còn"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu SQL vs NoSQL - khi nào dùng gì
- ✅ PostgreSQL/MySQL operations cơ bản
- ✅ MongoDB operations cơ bản
- ✅ Redis cache và use cases
- ✅ Database backup và restore
- ✅ Replication và High Availability concepts
- ✅ Connection pooling
- ✅ Database trong Docker

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| RDBMS | Relational Database Management System | Hệ quản trị CSDL quan hệ |
| SQL | Structured Query Language | Ngôn ngữ truy vấn |
| NoSQL | Not Only SQL | CSDL phi quan hệ |
| Schema | Database Schema | Cấu trúc database |
| Table | Table | Bảng data |
| Row | Row/Record | Dòng/Bản ghi |
| Column | Column/Field | Cột/Trường |
| Primary Key | Primary Key | Khóa chính |
| Foreign Key | Foreign Key | Khóa ngoại |
| Index | Index | Chỉ mục tăng tốc query |
| Query | Query | Câu truy vấn |
| Transaction | Transaction | Giao dịch |
| ACID | Atomicity, Consistency, Isolation, Durability | Tính chất transaction |
| Replication | Replication | Sao chép database |
| Primary/Master | Primary/Master | Server chính |
| Replica/Slave | Replica/Slave | Server sao chép |
| Backup | Backup | Sao lưu |
| Restore | Restore | Khôi phục |
| Connection Pool | Connection Pool | Pool kết nối |
| ORM | Object-Relational Mapping | Ánh xạ object-database |

---

## ✅ Checklist Labs

### Labs PostgreSQL cơ bản

- [ ] Lab 1: Install PostgreSQL
- [ ] Lab 2: Connect với psql client
- [ ] Lab 3: Create database và users
- [ ] Lab 4: Grant permissions
- [ ] Lab 5: CRUD operations (INSERT, SELECT, UPDATE, DELETE)
- [ ] Lab 6: Joins và relationships
- [ ] Lab 7: Indexes creation
- [ ] Lab 8: Explain analyze query

### Labs PostgreSQL operations

- [ ] Lab 9: pg_dump backup
- [ ] Lab 10: pg_restore
- [ ] Lab 11: Point-in-time recovery concepts
- [ ] Lab 12: PostgreSQL logs
- [ ] Lab 13: Connection limits configuration
- [ ] Lab 14: PostgreSQL trong Docker

### Labs MySQL

- [ ] Lab 15: Install MySQL
- [ ] Lab 16: MySQL client và basic operations
- [ ] Lab 17: mysqldump backup
- [ ] Lab 18: MySQL restore
- [ ] Lab 19: MySQL trong Docker

### Labs MongoDB

- [ ] Lab 20: Install MongoDB
- [ ] Lab 21: mongosh client
- [ ] Lab 22: CRUD operations (insertOne, find, updateOne, deleteOne)
- [ ] Lab 23: Query operators
- [ ] Lab 24: Indexes trong MongoDB
- [ ] Lab 25: mongodump và mongorestore
- [ ] Lab 26: MongoDB trong Docker

### Labs Redis

- [ ] Lab 27: Install Redis
- [ ] Lab 28: redis-cli basics
- [ ] Lab 29: String operations (SET, GET, INCR)
- [ ] Lab 30: Hash operations
- [ ] Lab 31: List operations
- [ ] Lab 32: Set operations
- [ ] Lab 33: Key expiration (TTL)
- [ ] Lab 34: Redis pub/sub
- [ ] Lab 35: Redis persistence (RDB, AOF)
- [ ] Lab 36: Redis trong Docker

### Labs cho Counter App

- [ ] Lab 37: Connect Counter App to PostgreSQL
- [ ] Lab 38: Counter App với Redis (existing)
- [ ] Lab 39: Database connection pooling

### Labs Replication (Concepts)

- [ ] Lab 40: PostgreSQL streaming replication concept
- [ ] Lab 41: MongoDB ReplicaSet concept
- [ ] Lab 42: Redis Sentinel concept

---

## 🚨 Checklist Scenarios

### Scenarios về Connection

- [ ] Scenario 1: Connection refused
- [ ] Scenario 2: Authentication failed
- [ ] Scenario 3: Too many connections
- [ ] Scenario 4: Connection timeout
- [ ] Scenario 5: Database không accept remote connections

### Scenarios về Performance

- [ ] Scenario 6: Query chạy cực chậm
- [ ] Scenario 7: Missing index
- [ ] Scenario 8: Full table scan
- [ ] Scenario 9: Lock contention
- [ ] Scenario 10: Database memory usage cao

### Scenarios về Data

- [ ] Scenario 11: Data corruption
- [ ] Scenario 12: Xóa nhầm data
- [ ] Scenario 13: Disk full
- [ ] Scenario 14: Restore từ backup failed

### Scenarios về Availability

- [ ] Scenario 15: Primary database down
- [ ] Scenario 16: Replication lag
- [ ] Scenario 17: Split brain scenario
- [ ] Scenario 18: Failover manual vs automatic

### Scenarios về Redis

- [ ] Scenario 19: Redis memory full
- [ ] Scenario 20: Cache miss rate cao
- [ ] Scenario 21: Redis eviction unexpected
- [ ] Scenario 22: Key expiration issues

### Scenarios về Docker

- [ ] Scenario 23: Database data lost sau container restart
- [ ] Scenario 24: Volume permissions issues
- [ ] Scenario 25: Network connectivity trong Docker

---

## ⏱️ Thời lượng

**Ước tính:** 4-6 giờ

| Phần | Thời gian |
|------|-----------|
| PostgreSQL (Labs 1-14) | 2 giờ |
| MySQL (Labs 15-19) | 0.5 giờ |
| MongoDB (Labs 20-26) | 1 giờ |
| Redis (Labs 27-36) | 1.5 giờ |
| Integration & Replication | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [MongoDB Manual](https://docs.mongodb.com/manual/)
- [Redis Documentation](https://redis.io/documentation)
- [Use The Index, Luke!](https://use-the-index-luke.com/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
