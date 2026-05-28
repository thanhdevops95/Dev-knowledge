# ✅ Solutions: Databases

---

## Exercise 1: RDS Setup

```bash
# Create subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name mydb-subnet \
  --db-subnet-group-description "DB Subnet" \
  --subnet-ids subnet-a subnet-b

# Create RDS
aws rds create-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username admin \
  --master-user-password MySecurePass123 \
  --allocated-storage 20 \
  --multi-az \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name mydb-subnet \
  --backup-retention-period 7
```

---

## Exercise 3: Flyway Migration

```sql
-- V1__create_users.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- V2__add_name.sql
ALTER TABLE users ADD COLUMN name VARCHAR(100);

-- V3__create_orders.sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```bash
# Run migrations
flyway -url=jdbc:postgresql://host:5432/db \
       -user=admin -password=secret migrate
```

---

**[← Back to Exercises](./EXERCISES.md)**
