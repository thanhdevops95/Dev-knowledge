# 🗃️ SQL cơ bản — Ngôn ngữ truy vấn cơ sở dữ liệu

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Mọi developer đều cần biết SQL

---

## Tại sao cần học SQL?

- **90%+ ứng dụng** lưu dữ liệu trong relational database (PostgreSQL, MySQL, SQLite)
- Backend, Data Engineering, AI/ML — đều cần SQL
- Ngôn ngữ **50 năm tuổi** nhưng vẫn là **#1** cho truy vấn dữ liệu

---

## 1. Database & Table — Nền tảng

```sql
-- Tạo database
CREATE DATABASE shop_db;

-- Tạo bảng
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,           -- Tự tăng
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255) UNIQUE NOT NULL,
    age         INTEGER CHECK (age >= 0),
    role        VARCHAR(20) DEFAULT 'user',
    is_active   BOOLEAN DEFAULT true,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users(id), -- Foreign Key
    total       DECIMAL(10, 2) NOT NULL,
    status      VARCHAR(20) DEFAULT 'pending',
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    price       DECIMAL(10, 2) NOT NULL,
    category    VARCHAR(50),
    stock       INTEGER DEFAULT 0
);

CREATE TABLE order_items (
    id          SERIAL PRIMARY KEY,
    order_id    INTEGER REFERENCES orders(id),
    product_id  INTEGER REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    price       DECIMAL(10, 2) NOT NULL
);
```

---

## 2. CRUD — Thao tác cơ bản

### INSERT — Thêm dữ liệu

```sql
-- Thêm 1 dòng
INSERT INTO users (name, email, age, role)
VALUES ('Nguyễn Văn An', 'an@mail.com', 25, 'admin');

-- Thêm nhiều dòng
INSERT INTO users (name, email, age) VALUES
    ('Trần Thị Bình', 'binh@mail.com', 30),
    ('Lê Văn Cường', 'cuong@mail.com', 22),
    ('Phạm Thị Dung', 'dung@mail.com', 28);
```

### SELECT — Đọc dữ liệu

```sql
-- Lấy tất cả
SELECT * FROM users;

-- Chọn cột cụ thể
SELECT name, email, age FROM users;

-- Lọc với WHERE
SELECT * FROM users WHERE age >= 25 AND role = 'admin';

-- Pattern matching
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM users WHERE name LIKE 'Nguyễn%';

-- Sắp xếp
SELECT * FROM users ORDER BY age DESC;         -- Giảm dần
SELECT * FROM users ORDER BY name ASC, age DESC; -- Nhiều cột

-- Giới hạn (pagination)
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;  -- Page 3

-- Distinct — loại bỏ trùng
SELECT DISTINCT role FROM users;
```

### UPDATE — Cập nhật

```sql
-- Cập nhật 1 dòng
UPDATE users SET age = 26, role = 'admin' WHERE id = 1;

-- Cập nhật nhiều dòng
UPDATE users SET is_active = false WHERE age < 18;

-- ⚠️ LUÔN có WHERE! Không có = cập nhật TẤT CẢ!
UPDATE users SET role = 'admin';  -- 💥 Tất cả users thành admin!
```

### DELETE — Xóa

```sql
-- Xóa cụ thể
DELETE FROM users WHERE id = 5;

-- ⚠️ LUÔN có WHERE!
DELETE FROM users;  -- 💥 Xóa TẤT CẢ users!
```

---

## 3. JOIN — Kết hợp bảng

```
users:                     orders:
┌────┬──────┬────────┐    ┌────┬─────────┬────────┐
│ id │ name │ email  │    │ id │ user_id │ total  │
├────┼──────┼────────┤    ├────┼─────────┼────────┤
│  1 │ An   │ an@... │    │  1 │    1    │ 150.00 │
│  2 │ Bình │ binh.. │    │  2 │    1    │  75.50 │
│  3 │ Cường│ cuong..│    │  3 │    2    │ 200.00 │
└────┴──────┴────────┘    └────┴─────────┴────────┘
```

```sql
-- INNER JOIN — Chỉ lấy dòng khớp ở CẢ HAI bảng
SELECT u.name, o.total, o.status
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
-- An: 150.00, An: 75.50, Bình: 200.00
-- Cường KHÔNG xuất hiện (không có order)

-- LEFT JOIN — Tất cả từ bảng trái + khớp bảng phải
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
-- An: 150.00, An: 75.50, Bình: 200.00, Cường: NULL

-- Nhiều bảng
SELECT u.name, o.total, p.name AS product, oi.quantity
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.status = 'completed';
```

```
     INNER JOIN          LEFT JOIN           RIGHT JOIN          FULL OUTER JOIN
    ┌───┬───┐           ┌───┬───┐           ┌───┬───┐           ┌───┬───┐
    │ A │ B │           │ A │ B │           │ A │ B │           │ A │ B │
    │   │███│           │███│███│           │███│███│           │███│███│
    │   │███│           │███│███│           │   │███│           │███│███│
    │   │   │           │███│   │           │   │███│           │███│███│
    └───┴───┘           └───┴───┘           └───┴───┘           └───┴───┘
  Chỉ phần chung      Tất cả A + chung    Chung + tất cả B    Tất cả A + B
```

---

## 4. Aggregate Functions — Hàm tổng hợp

```sql
SELECT
    COUNT(*) AS total_users,          -- Đếm
    AVG(age) AS avg_age,              -- Trung bình
    MIN(age) AS youngest,             -- Nhỏ nhất
    MAX(age) AS oldest,               -- Lớn nhất
    SUM(age) AS total_age             -- Tổng
FROM users;

-- GROUP BY — Nhóm theo cột
SELECT role, COUNT(*) AS count, AVG(age) AS avg_age
FROM users
GROUP BY role;
-- admin: 2, avg_age: 27.5
-- user:  3, avg_age: 24.0

-- HAVING — Lọc sau khi GROUP BY (WHERE lọc TRƯỚC)
SELECT role, COUNT(*) AS count
FROM users
GROUP BY role
HAVING COUNT(*) > 1;  -- Chỉ roles có > 1 user
```

**Thứ tự thực thi SQL:**

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
  1       2        3          4        5          6         7
```

---

## 5. Subqueries — Query lồng

```sql
-- Tìm users có order lớn hơn trung bình
SELECT name, email
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
    WHERE total > (SELECT AVG(total) FROM orders)
);

-- EXISTS — kiểm tra tồn tại
SELECT name
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

---

## 6. Index — Tăng tốc truy vấn

```sql
-- Không có index: Full Table Scan → O(n)
-- Có index: B-Tree lookup → O(log n)

-- Tạo index
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- Khi nào tạo index?
-- ✅ Cột trong WHERE, JOIN, ORDER BY thường xuyên
-- ✅ Foreign keys
-- ❌ Bảng nhỏ (< 1000 rows)
-- ❌ Cột ít giá trị unique (gender: M/F)
-- ❌ Cột thường xuyên UPDATE

-- Kiểm tra query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'an@mail.com';
```

---

## 7. Transaction — Đảm bảo toàn vẹn

```sql
-- Chuyển tiền: A trừ 100, B cộng 100
-- Phải xảy ra ĐỒNG THỜI hoặc KHÔNG xảy ra!

BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- Cả 2 thành công

-- Nếu lỗi ở giữa:
BEGIN;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    -- 💥 Lỗi xảy ra ở đây!
ROLLBACK;  -- Quay lại trạng thái ban đầu, A không mất tiền
```

**ACID:**
- **A**tomicity: Tất cả hoặc không gì cả
- **C**onsistency: Dữ liệu luôn hợp lệ
- **I**solation: Transaction không ảnh hưởng lẫn nhau
- **D**urability: Commit xong = lưu vĩnh viễn (kể cả mất điện)

---

## Các lỗi thường gặp

```
❌ Sai: SELECT * trong production → lấy thừa dữ liệu
✅ Đúng: SELECT chỉ cột cần: SELECT name, email FROM users

❌ Sai: String concatenation trong query → SQL Injection!
   query = f"SELECT * FROM users WHERE name = '{input}'"
✅ Đúng: Parameterized query
   cursor.execute("SELECT * FROM users WHERE name = %s", (input,))

❌ Sai: Quên index cho foreign key → JOIN cực chậm
✅ Đúng: Index mọi foreign key + cột WHERE thường dùng
```

---

## Bài tập thực hành

- [ ] Tạo schema cho e-commerce (users, products, orders, order_items)
- [ ] Viết query: Top 5 sản phẩm bán chạy nhất (JOIN + GROUP BY + ORDER BY)
- [ ] Viết query: Doanh thu theo tháng (DATE functions + GROUP BY)
- [ ] Thêm index + dùng EXPLAIN ANALYZE so sánh tốc độ

---

## Tài nguyên thêm

- [SQLBolt](https://sqlbolt.com/) — Học SQL tương tác, miễn phí
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) — Đầy đủ nhất
- [Use The Index, Luke](https://use-the-index-luke.com/) — Hiểu sâu về indexing
