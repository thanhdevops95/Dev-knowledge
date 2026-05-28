# 🗄️ Module 3.3: Databases for DevOps

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Database Management** - RDS, NoSQL, Caching, and Migrations.
>
> *Quản lý Database - RDS, NoSQL, Caching, và Migrations.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Manage RDS (MySQL, PostgreSQL) (Quản lý RDS)
- ✅ Work with NoSQL databases - DynamoDB, MongoDB (Làm việc với NoSQL)
- ✅ Implement caching with Redis/ElastiCache (Triển khai caching)
- ✅ Perform database migrations (Thực hiện migrations)
- ✅ Configure backup and recovery (Cấu hình backup và recovery)
- ✅ Tune performance (Tối ưu hiệu suất)

---

## 📚 Content (Nội dung)

### 1. Why Database Knowledge Matters? (Tại sao DevOps cần hiểu về Database?)

As a DevOps Engineer, you don't need to write complex SQL like a DBA, but you need to understand:

*Là DevOps Engineer, bạn không cần viết SQL phức tạp như DBA, nhưng cần hiểu:*

- **Deployment**: Cách deploy database, quản lý migrations
- **Backup & Recovery**: Đảm bảo dữ liệu không bị mất
- **Monitoring**: Theo dõi performance, connections, query times
- **Scaling**: Khi nào cần scale, read replicas, sharding

---

### 2. SQL vs NoSQL - When to Use Which? (Khi nào dùng gì?)

This is an important question that DevOps often has to answer when designing systems.

*Đây là câu hỏi quan trọng mà DevOps thường phải trả lời khi thiết kế hệ thống.*

| Tiêu chí | SQL (PostgreSQL, MySQL) | NoSQL (MongoDB, DynamoDB) |
|----------|-------------------------|---------------------------|
| **Cấu trúc dữ liệu** | Schema cố định, bảng có quan hệ | Schema linh hoạt, document-based |
| **Tính nhất quán** | ACID - Đảm bảo chính xác 100% | Eventually consistent (có thể chấp nhận delay) |
| **Use case** | E-commerce, banking, CRM | Logging, IoT, real-time analytics |
| **Scale** | Vertical (máy mạnh hơn) | Horizontal (nhiều máy hơn) |

---

### 3. RDS - Relational Database Service

#### What is RDS? (RDS là gì?)

**RDS** is AWS's managed database service. AWS handles patching, backup, high availability - you just use it.

*RDS là dịch vụ managed database của AWS. AWS lo việc patching, backup, high availability - bạn chỉ cần dùng.*

#### When to Use RDS Instead of Self-hosting? (Khi nào dùng RDS thay vì tự host?)

| Tự host (EC2 + MySQL) | RDS |
|-----------------------|-----|
| Phải tự backup, patching | Tự động |
| Khó setup Multi-AZ | Bật 1 click |
| Tốn thời gian quản lý | Focus vào application |
| Rẻ hơn nếu bạn có expertise | Đắt hơn nhưng tiết kiệm thời gian |

#### Create RDS Instance (Tạo RDS Instance)

```bash
aws rds create-db-instance \
  --db-instance-identifier myapp-production-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password SuperSecretPassword123! \
  --allocated-storage 20 \
  --multi-az \
  --backup-retention-period 7
```

**Giải thích:**

- `--db-instance-identifier`: Tên định danh duy nhất cho database
- `--db-instance-class`: Cấu hình máy (t3.micro = nhỏ, cho dev/test)
- `--engine`: Loại database (postgres, mysql, mariadb...)
- `--multi-az`: Tạo bản sao ở Availability Zone khác để đảm bảo uptime
- `--backup-retention-period`: Giữ backup bao nhiêu ngày

---

### 4. Redis - In-Memory Caching

#### Redis là gì? (What is Redis?)

**Redis** is an in-memory database (stored in RAM), extremely fast, commonly used to cache frequently accessed data.

*Redis là cơ sở dữ liệu in-memory (lưu trong RAM), cực nhanh, thường dùng để cache dữ liệu thường xuyên truy cập.*

#### Why Do You Need Caching? (Tại sao cần caching?)

```
Không có cache:
User → App → Database (100ms) → App → User
                 ↑
          Mỗi request đều query DB = chậm, tốn resource

Có cache (Redis):
User → App → Redis (1ms) → App → User
                 ↑
          Cache hit = nhanh gấp 100 lần!
```

#### Basic Redis Commands (Các lệnh Redis cơ bản)

```bash
# Kết nối đến Redis
redis-cli -h my-redis-server.amazonaws.com -p 6379

# SET: Lưu một giá trị với key
SET user:123:profile '{"name": "John", "email": "john@example.com"}'

# GET: Lấy giá trị theo key
GET user:123:profile

# EXPIRE: Set thời gian sống (TTL) - sau 1 giờ tự động xóa
EXPIRE user:123:profile 3600

# SETEX: SET + EXPIRE trong 1 lệnh (lưu 1 giờ)
SETEX session:abc123 3600 '{"user_id": 123}'
```

---

### 5. Database Migrations

#### Migrations là gì? (What are Migrations?)

**Migrations** are a way to manage database schema changes with code. Instead of running SQL manually, you write migration files and run them automatically.

*Migrations là cách quản lý thay đổi schema database bằng code. Thay vì chạy SQL thủ công, bạn viết file migration và chạy tự động.*

#### Why Do You Need Migrations? (Tại sao cần Migrations?)

| Không dùng Migrations | Dùng Migrations |
|-----------------------|-----------------|
| Chạy SQL thủ công trên production 😱 | Chạy lệnh tự động, có version control |
| Không biết ai thay đổi gì | Mọi thay đổi đều được track trong Git |
| Khó rollback nếu có lỗi | Có thể rollback dễ dàng |

#### Flyway Example (Ví dụ với Flyway)

```sql
-- V1__Create_users_table.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- V2__Add_name_to_users.sql
ALTER TABLE users ADD COLUMN name VARCHAR(100);
```

```bash
# Chạy migration - Flyway tự detect file mới và chạy theo thứ tự
flyway -url=jdbc:postgresql://localhost:5432/mydb \
       -user=admin \
       -password=secret \
       migrate
```

**Lưu ý:** Tên file migration theo format `V{version}__{description}.sql`. Flyway tự track version nào đã chạy.

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [3.2 AWS Core](../3.2_AWS_Core_Services/) | **3.3 Databases** | [3.4 Ansible](../3.4_Config_Management_Ansible/) |

---

**Master database management! 🗄️**

*Thành thạo quản lý database!*

</div>
