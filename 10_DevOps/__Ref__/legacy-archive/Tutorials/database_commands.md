# Hướng dẫn Database Commands

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tổng hợp các lệnh SQL cơ bản và cách sử dụng các database phổ biến.

---

## 📊**SQL CƠ BẢN**

### SELECT - Truy vấn dữ liệu

```sql
-- Lấy tất cả cột
SELECT * FROM users;

-- Lấy cột cụ thể
SELECT name, email FROM users;

-- Với điều kiện
SELECT * FROM users WHERE age > 18;

-- Sắp xếp
SELECT * FROM users ORDER BY created_at DESC;

-- Giới hạn
SELECT * FROM users LIMIT 10;
SELECT * FROM users LIMIT 10 OFFSET 20;

-- Đếm
SELECT COUNT(*) FROM users;

-- Group by
SELECT country, COUNT(*) as count
FROM users
GROUP BY country;

-- Distinct (loại trùng)
SELECT DISTINCT country FROM users;
```

### WHERE - Điều kiện

```sql
-- So sánh
SELECT * FROM users WHERE age = 25;
SELECT * FROM users WHERE age > 18;
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE age != 25;

-- AND, OR
SELECT * FROM users WHERE age > 18 AND country = 'VN';
SELECT * FROM users WHERE age > 18 OR country = 'VN';

-- IN
SELECT * FROM users WHERE country IN ('VN', 'US', 'UK');

-- BETWEEN
SELECT * FROM users WHERE age BETWEEN 18 AND 30;

-- LIKE (pattern matching)
SELECT * FROM users WHERE name LIKE 'John%';     -- Bắt đầu bằng John
SELECT * FROM users WHERE name LIKE '%son';      -- Kết thúc bằng son
SELECT * FROM users WHERE name LIKE '%hn%';      -- Chứa hn
SELECT * FROM users WHERE name LIKE 'J_hn';      -- J + 1 ký tự + hn

-- NULL
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;
```

### INSERT - Thêm dữ liệu

```sql
-- Insert 1 row
INSERT INTO users (name, email, age)
VALUES ('John', 'john@example.com', 25);

-- Insert nhiều rows
INSERT INTO users (name, email, age)
VALUES
    ('John', 'john@example.com', 25),
    ('Jane', 'jane@example.com', 30),
    ('Bob', 'bob@example.com', 22);
```

### UPDATE - Cập nhật dữ liệu

```sql
-- Update với điều kiện
UPDATE users
SET email = 'newemail@example.com'
WHERE id = 1;

-- Update nhiều cột
UPDATE users
SET name = 'John Doe', age = 26
WHERE id = 1;

-- Update tất cả (NGUY HIỂM!)
UPDATE users SET status = 'active';
```

### DELETE - Xóa dữ liệu

```sql
-- Delete với điều kiện
DELETE FROM users WHERE id = 1;

-- Delete tất cả (NGUY HIỂM!)
DELETE FROM users;

-- Xóa bảng và reset ID
TRUNCATE TABLE users;
```

---

## 🔗**JOIN - Kết hợp bảng**

### INNER JOIN

Chỉ lấy records có match ở cả 2 bảng.

```sql
SELECT users.name, orders.total
FROM users
INNER JOIN orders ON users.id = orders.user_id;
```

### LEFT JOIN

Lấy tất cả từ bảng trái, match với bảng phải.

```sql
SELECT users.name, orders.total
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

### RIGHT JOIN

Lấy tất cả từ bảng phải, match với bảng trái.

```sql
SELECT users.name, orders.total
FROM users
RIGHT JOIN orders ON users.id = orders.user_id;
```

### Ví dụ thực tế

```sql
-- Lấy user kèm số đơn hàng
SELECT
    users.name,
    COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id;
```

---

## 🏗️**QUẢN LÝ BẢNG**

### CREATE TABLE

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Với foreign key
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    total DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### ALTER TABLE

```sql
-- Thêm cột
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Xóa cột
ALTER TABLE users DROP COLUMN phone;

-- Đổi kiểu dữ liệu
ALTER TABLE users MODIFY COLUMN age SMALLINT;

-- Đổi tên cột
ALTER TABLE users RENAME COLUMN name TO full_name;

-- Thêm index
ALTER TABLE users ADD INDEX idx_email (email);
```

### DROP TABLE

```sql
DROP TABLE users;

-- Xóa nếu tồn tại
DROP TABLE IF EXISTS users;
```

---

## 🔢**KIỂU DỮ LIỆU**

### Số

| Kiểu | Mô tả |
|------|-------|
| `INT` | Số nguyên |
| `BIGINT` | Số nguyên lớn |
| `DECIMAL(10,2)` | Số thập phân chính xác |
| `FLOAT` | Số thập phân |
| `BOOLEAN` | True/False |

### Văn bản

| Kiểu | Mô tả |
|------|-------|
| `VARCHAR(255)` | Chuỗi độ dài thay đổi |
| `CHAR(10)` | Chuỗi độ dài cố định |
| `TEXT` | Văn bản dài |
| `JSON` | Dữ liệu JSON |

### Thời gian

| Kiểu | Mô tả |
|------|-------|
| `DATE` | Ngày (YYYY-MM-DD) |
| `TIME` | Giờ (HH:MM:SS) |
| `DATETIME` | Ngày và giờ |
| `TIMESTAMP` | Unix timestamp |

---

## 🗄️**SQLITE**

SQLite là database file-based, nhẹ, không cần server.

### Python với SQLite

```python
import sqlite3

# Kết nối (tạo file nếu chưa có)
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Tạo bảng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
''')

# Insert
cursor.execute(
    'INSERT INTO users (name, email) VALUES (?, ?)',
    ('John', 'john@example.com')
)

# Select
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Commit và đóng
conn.commit()
conn.close()
```

### SQLite CLI

```bash
# Mở database
sqlite3 my_database.db

# Commands
.tables           # Liệt kê tables
.schema users     # Xem schema của table
.headers on       # Hiện headers
.mode column      # Format output
.quit             # Thoát
```

---

## 🐘**POSTGRESQL**

### Kết nối

```bash
# CLI
psql -U username -d database_name

# Với host
psql -h localhost -U username -d database_name
```

### PostgreSQL CLI Commands

```sql
-- Liệt kê databases
\l

-- Kết nối database
\c database_name

-- Liệt kê tables
\dt

-- Mô tả table
\d table_name

-- Thoát
\q
```

### Python với PostgreSQL

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="user",
    password="password"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

conn.close()
```

---

## 🐬**MYSQL**

### Kết nối

```bash
mysql -u root -p
mysql -u root -p database_name
```

### MySQL CLI Commands

```sql
-- Liệt kê databases
SHOW DATABASES;

-- Sử dụng database
USE database_name;

-- Liệt kê tables
SHOW TABLES;

-- Mô tả table
DESCRIBE table_name;
```

### Python với MySQL

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="mydb"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

conn.close()
```

---

## 🔧**INDEX**

Index giúp query nhanh hơn.

```sql
-- Tạo index
CREATE INDEX idx_email ON users(email);

-- Index unique
CREATE UNIQUE INDEX idx_email ON users(email);

-- Index nhiều cột
CREATE INDEX idx_name_email ON users(name, email);

-- Xóa index
DROP INDEX idx_email ON users;
```

### Khi nào dùng Index?

| Nên dùng | Không nên dùng |
|----------|----------------|
| Cột hay dùng trong WHERE | Bảng nhỏ |
| Cột dùng trong JOIN | Cột ít giá trị unique |
| Cột dùng trong ORDER BY | Cột hay UPDATE |
| Primary key, Foreign key | INSERT nhiều |

---

## 🔐**TRANSACTIONS**

```sql
-- Bắt đầu transaction
BEGIN;
-- hoặc
START TRANSACTION;

-- Thực hiện queries
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Commit (lưu)
COMMIT;

-- Hoặc Rollback (hủy)
ROLLBACK;
```

### Python với Transaction

```python
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

try:
    cursor.execute('UPDATE accounts SET balance = balance - 100 WHERE id = 1')
    cursor.execute('UPDATE accounts SET balance = balance + 100 WHERE id = 2')
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
finally:
    conn.close()
```

---

## 📊**HÀM TỔNG HỢP**

```sql
-- Đếm
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT country) FROM users;

-- Tổng
SELECT SUM(amount) FROM orders;

-- Trung bình
SELECT AVG(age) FROM users;

-- Min/Max
SELECT MIN(price), MAX(price) FROM products;

-- Với GROUP BY
SELECT country, COUNT(*), AVG(age)
FROM users
GROUP BY country
HAVING COUNT(*) > 10;
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
