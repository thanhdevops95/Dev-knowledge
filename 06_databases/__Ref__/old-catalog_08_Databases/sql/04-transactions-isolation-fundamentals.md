# 🔒 Database Transactions & Isolation Levels

> `[INTERMEDIATE → ADVANCED]` — Đảm bảo data consistency trong concurrent systems

---

## Tại sao cần Transactions?

Hãy tưởng tượng chuyển tiền từ tài khoản A sang B:

```
Bước 1: Trừ A 1.000.000đ    ← Thành công
Bước 2: Cộng B 1.000.000đ   ← Server crash! ❌

Kết quả: A mất tiền, B không nhận được.
→ Data inconsistent. Tiền "biến mất"!
```

**Transaction** đảm bảo: hoặc **TẤT CẢ** các bước thành công, hoặc **KHÔNG bước nào** xảy ra. Đây là nguyên tắc **ACID**:

```
A — Atomicity  (Nguyên tử):    Tất cả hoặc không gì cả
C — Consistency (Nhất quán):    Data luôn valid sau transaction
I — Isolation   (Cô lập):      Transactions không ảnh hưởng nhau
D — Durability  (Bền vững):    Commit xong → data tồn tại vĩnh viễn (kể cả crash)
```

---

## 1. Transaction cơ bản

### SQL

```sql
-- Transfer money: atomic operation
BEGIN TRANSACTION;

UPDATE accounts 
SET balance = balance - 1000000 
WHERE id = 'A' AND balance >= 1000000;  -- Check đủ tiền!

UPDATE accounts 
SET balance = balance + 1000000 
WHERE id = 'B';

-- Kiểm tra cả 2 updates thành công
-- Nếu bất kỳ lỗi nào → ROLLBACK tất cả
COMMIT;

-- Nếu lỗi:
-- ROLLBACK;  ← Hoàn tác TẤT CẢ changes
```

### Prisma (TypeScript ORM)

```typescript
// Prisma interactive transaction
async function transferMoney(fromId: string, toId: string, amount: number) {
    return prisma.$transaction(async (tx) => {
        // Bước 1: Trừ tiền sender
        const sender = await tx.account.update({
            where: { id: fromId },
            data: { balance: { decrement: amount } },
        });

        // Validate: không cho âm
        if (sender.balance < 0) {
            throw new Error('Insufficient balance');
            // → Prisma tự ROLLBACK toàn bộ transaction!
        }

        // Bước 2: Cộng tiền receiver
        await tx.account.update({
            where: { id: toId },
            data: { balance: { increment: amount } },
        });

        // Bước 3: Tạo record chuyển tiền
        await tx.transfer.create({
            data: { fromId, toId, amount, status: 'completed' },
        });

        return sender;
    });
    // Tất cả 3 operations COMMIT cùng lúc, hoặc ROLLBACK tất cả
}
```

---

## 2. Concurrency Problems — Vấn đề khi nhiều users cùng truy cập

Khi 2 transactions chạy đồng thời trên cùng data, có thể xảy ra:

### Dirty Read — Đọc data chưa commit

```
Transaction A (chuyển tiền):        Transaction B (xem số dư):
BEGIN                               BEGIN
UPDATE balance = balance - 100
                                    SELECT balance → thấy đã trừ 100!
ROLLBACK                           
                                    → B đọc sai! Data đã bị rollback.
```

### Non-repeatable Read — Đọc 2 lần khác nhau

```
Transaction A (báo cáo):           Transaction B (cập nhật):
BEGIN
SELECT price → 100
                                    UPDATE price = 200
                                    COMMIT
SELECT price → 200  ❌
→ Cùng 1 transaction, đọc 2 lần khác nhau!
```

### Phantom Read — Data "ma" xuất hiện

```
Transaction A (thống kê):          Transaction B (thêm mới):
BEGIN
SELECT COUNT(*) WHERE age > 25 → 5
                                    INSERT (name='C', age=30)
                                    COMMIT
SELECT COUNT(*) WHERE age > 25 → 6  ❌
→ Row mới "ma" xuất hiện!
```

---

## 3. Isolation Levels — Chọn mức cô lập

Mỗi level là **trade-off giữa consistency và performance**. Level cao hơn = an toàn hơn nhưng chậm hơn:

| Level | Dirty Read | Non-repeatable | Phantom | Performance |
|---|---|---|---|---|
| READ UNCOMMITTED | ❌ Có thể | ❌ Có thể | ❌ Có thể | Nhanh nhất |
| READ COMMITTED | ✅ Ngăn | ❌ Có thể | ❌ Có thể | Nhanh |
| REPEATABLE READ | ✅ Ngăn | ✅ Ngăn | ❌ Có thể | Trung bình |
| SERIALIZABLE | ✅ Ngăn | ✅ Ngăn | ✅ Ngăn | Chậm nhất |

**Thực tế:**
- **PostgreSQL default**: READ COMMITTED (đủ cho 90% cases)
- **MySQL/InnoDB default**: REPEATABLE READ
- **Cần financial accuracy**: SERIALIZABLE

```sql
-- Set isolation level cho transaction
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- ... queries ...
COMMIT;

-- PostgreSQL: set cho session
SET default_transaction_isolation = 'read committed';
```

### Khi nào dùng level nào?

| Use Case | Level | Lý do |
|---|---|---|
| Dashboard analytics | READ COMMITTED | Chấp nhận data hơi cũ, cần nhanh |
| Order processing | READ COMMITTED | Balance check + update đủ an toàn |
| Financial transfer | SERIALIZABLE | PHẢI chính xác tuyệt đối |
| Inventory check | REPEATABLE READ | Tránh phantom reads khi đếm stock |
| Reporting | READ COMMITTED + Snapshot | Đọc consistent point-in-time data |

---

## 4. Locking Strategies

### Optimistic Locking — "Hy vọng không có conflict"

Không lock row khi đọc. Khi update, kiểm tra version number:

```typescript
// Version field trong schema
// prisma: @@map("version") Int @default(0)

async function updateProduct(id: string, newPrice: number) {
    const product = await prisma.product.findUnique({ where: { id } });

    try {
        await prisma.product.update({
            where: {
                id,
                version: product.version,  // Check version chưa đổi!
            },
            data: {
                price: newPrice,
                version: { increment: 1 },  // Tăng version
            },
        });
    } catch (e) {
        // StaleObjectError: ai đó đã update trước!
        // → Retry hoặc thông báo user
        throw new ConflictError('Product was modified by another user');
    }
}
```

**Khi nào dùng:** Low contention (ít conflict). Web apps thông thường.

### Pessimistic Locking — "Chắc chắn lock trước"

Lock row ngay khi đọc, không ai sửa được cho đến khi unlock:

```sql
-- SELECT ... FOR UPDATE: lock rows cho đến COMMIT/ROLLBACK
BEGIN;
SELECT * FROM accounts WHERE id = 'A' FOR UPDATE;
-- Row 'A' bị LOCK! Transaction khác phải chờ.
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
COMMIT;
-- Unlock!
```

```typescript
// Prisma raw query for pessimistic locking
await prisma.$transaction(async (tx) => {
    // Lock row
    const [account] = await tx.$queryRaw`
        SELECT * FROM accounts WHERE id = ${id} FOR UPDATE
    `;

    if (account.balance < amount) {
        throw new Error('Insufficient balance');
    }

    await tx.account.update({
        where: { id },
        data: { balance: { decrement: amount } },
    });
});
```

**Khi nào dùng:** High contention (nhiều conflict). Financial systems, inventory.

---

## 5. Deadlocks — Bế tắc

```
Deadlock: 2 transactions chờ nhau mãi mãi

Transaction A:           Transaction B:
LOCK row 1               LOCK row 2
→ Muốn LOCK row 2        → Muốn LOCK row 1
→ Chờ B release row 2    → Chờ A release row 1
→ DEADLOCK! ☠️

DB tự phát hiện → abort 1 transaction → transaction đó phải retry.
```

**Phòng tránh deadlock:**
1. **Lock cùng thứ tự**: Luôn lock row ID nhỏ trước, lớn sau
2. **Giữ lock ngắn**: Transaction càng ngắn càng tốt
3. **Set timeout**: `SET lock_timeout = '5s'`
4. **Retry logic**: Catch deadlock error → retry with backoff

---

## Bài tập thực hành

- [ ] Implement money transfer với transaction (SQL hoặc Prisma)
- [ ] Simulate dirty read: 2 connections, READ UNCOMMITTED vs READ COMMITTED
- [ ] Optimistic locking: concurrent product updates → handle conflict
- [ ] Deadlock: tạo deadlock scenario → fix bằng consistent lock ordering

---

## Tài nguyên thêm

- [PostgreSQL Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html) — Official
- [Designing Data-Intensive Applications (Ch.7)](https://dataintensive.net/) — Martin Kleppmann
- [Prisma Transactions](https://www.prisma.io/docs/concepts/components/prisma-client/transactions)
