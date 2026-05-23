# 📦 MongoDB nâng cao — Aggregation, Indexing & Patterns

> `[INTERMEDIATE → ADVANCED]` — Khai thác MongoDB hiệu quả

---

## 1. Aggregation Pipeline — Xử lý dữ liệu phức tạp

```javascript
// Pipeline = chuỗi stages xử lý documents tuần tự
// $match → $group → $sort → $project → $limit

// Ví dụ: Doanh thu mỗi category trong tháng 3
db.orders.aggregate([
    // Stage 1: Lọc đơn hàng tháng 3
    {
        $match: {
            status: 'completed',
            createdAt: {
                $gte: ISODate('2026-03-01'),
                $lt: ISODate('2026-04-01'),
            },
        },
    },
    // Stage 2: Tách mảng items (1 order → N documents)
    { $unwind: '$items' },

    // Stage 3: Nhóm theo category, tính tổng
    {
        $group: {
            _id: '$items.category',
            totalRevenue: { $sum: '$items.price' },
            totalQuantity: { $sum: '$items.quantity' },
            orderCount: { $sum: 1 },
            avgOrderValue: { $avg: '$items.price' },
        },
    },
    // Stage 4: Sắp xếp theo doanh thu giảm dần
    { $sort: { totalRevenue: -1 } },

    // Stage 5: Format output
    {
        $project: {
            category: '$_id',
            totalRevenue: 1,
            totalQuantity: 1,
            avgOrderValue: { $round: ['$avgOrderValue', 0] },
            _id: 0,
        },
    },
]);
// Output:
// { category: "Electronics", totalRevenue: 50000000, totalQuantity: 120, avgOrderValue: 416667 }
// { category: "Clothing",    totalRevenue: 20000000, totalQuantity: 500, avgOrderValue: 40000 }
```

### $lookup — JOIN giữa collections

```javascript
// Giống SQL LEFT JOIN
db.orders.aggregate([
    {
        $lookup: {
            from: 'users',               // Collection cần join
            localField: 'customerId',     // Field ở orders
            foreignField: '_id',          // Field ở users
            as: 'customer',              // Tên field output (array)
        },
    },
    { $unwind: '$customer' },            // Array → single object
    {
        $project: {
            orderId: '$_id',
            'customer.name': 1,
            'customer.email': 1,
            total: 1,
            status: 1,
        },
    },
]);
```

---

## 2. Indexing — Tăng tốc queries

```javascript
// Không index: O(N) — scan TOÀN BỘ collection
// Có index:    O(log N) — B-tree lookup

// Single field index
db.users.createIndex({ email: 1 });          // 1 = ascending

// Compound index (thứ tự QUAN TRỌNG!)
db.orders.createIndex({ customerId: 1, createdAt: -1 });
// Hỗ trợ queries:
//   find({ customerId: 123 })                        ✅
//   find({ customerId: 123 }).sort({ createdAt: -1 })  ✅
//   find({ createdAt: ... })                         ❌ (phải có customerId trước!)

// Text index (full-text search)
db.products.createIndex({ name: 'text', description: 'text' });
db.products.find({ $text: { $search: 'laptop gaming' } });

// TTL index (tự xóa sau N giây — sessions, logs)
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 });

// Unique index
db.users.createIndex({ email: 1 }, { unique: true });

// Analyze query performance
db.orders.find({ status: 'pending' }).explain('executionStats');
// Xem: totalDocsExamined, executionTimeMillis, indexUsed
```

### Index Strategy

```
ESR Rule (Equality → Sort → Range):
  Query: find({ status: 'active', age: { $gt: 18 } }).sort({ name: 1 })

  ✅ Index: { status: 1, name: 1, age: 1 }
            (Equality)  (Sort)   (Range)

  ❌ Index: { age: 1, status: 1, name: 1 }
            (Range đầu tiên → không tối ưu!)
```

---

## 3. Schema Design Patterns

### Embedding vs Referencing

```javascript
// Embedding: data luôn đọc cùng nhau → nhúng vào
// ✅ 1 query lấy hết. Nhanh!
{
    _id: ObjectId("..."),
    name: "An",
    addresses: [                     // Embed!
        { street: "123 Lê Lợi", city: "HCM" },
        { street: "456 Hoàng Diệu", city: "HN" },
    ],
}

// Referencing: data độc lập, many-to-many → reference
// ✅ Không duplicate data. Flexible.
// Order document
{
    _id: ObjectId("..."),
    customerId: ObjectId("user_123"),  // Reference!
    items: [
        { productId: ObjectId("prod_1"), quantity: 2 },
    ],
}
```

### Bucket Pattern — Time-series data

```javascript
// ❌ 1 document per measurement = triệu documents!
{ sensorId: "s1", temp: 22.5, timestamp: "2026-03-04T10:00:00" }
{ sensorId: "s1", temp: 22.6, timestamp: "2026-03-04T10:01:00" }

// ✅ Bucket: gom 1 giờ vào 1 document
{
    sensorId: "s1",
    date: "2026-03-04",
    hour: 10,
    measurements: [
        { temp: 22.5, minute: 0 },
        { temp: 22.6, minute: 1 },
        // ... 60 entries
    ],
    stats: { min: 22.0, max: 23.5, avg: 22.7, count: 60 },
}
// Giảm document count 60x. Query nhanh hơn!
```

### Computed Pattern — Pre-calculate aggregations

```javascript
// ❌ Tính mỗi lần query (chậm)
db.products.aggregate([
    { $group: { _id: null, avgRating: { $avg: '$rating' } } },
]);

// ✅ Pre-compute khi write
// Mỗi khi có review mới:
db.products.updateOne(
    { _id: productId },
    {
        $inc: { ratingCount: 1, ratingSum: newRating },
        $set: { avgRating: (ratingSum + newRating) / (ratingCount + 1) },
    },
);
// Read chỉ cần: db.products.find({ _id: productId }, { avgRating: 1 })
```

---

## 4. Transactions (Multi-document)

```javascript
const session = client.startSession();

try {
    session.startTransaction();

    // Trừ tiền account A
    await accounts.updateOne(
        { _id: 'A' },
        { $inc: { balance: -100000 } },
        { session },
    );

    // Cộng tiền account B
    await accounts.updateOne(
        { _id: 'B' },
        { $inc: { balance: 100000 } },
        { session },
    );

    await session.commitTransaction();
} catch {
    await session.abortTransaction();  // Rollback!
} finally {
    session.endSession();
}
```

---

## 5. Change Streams — Real-time

```javascript
// Lắng nghe thay đổi real-time (giống CDC)
const changeStream = db.collection('orders').watch([
    { $match: { 'fullDocument.status': 'confirmed' } },
]);

changeStream.on('change', (change) => {
    console.log('Order confirmed:', change.fullDocument);
    // Gửi notification, update dashboard...
});
```

---

## Các lỗi thường gặp

```
❌ Sai: Embed mọi thứ → document > 16MB limit!
✅ Đúng: Embed nếu data nhỏ + đọc cùng nhau. Reference nếu data lớn/độc lập.

❌ Sai: Không tạo index → full collection scan
✅ Đúng: Tạo index cho MỌI field dùng trong find/sort. Dùng explain() kiểm tra.

❌ Sai: Index quá nhiều → write chậm (mỗi write phải update N indexes)
✅ Đúng: Chỉ index fields thực sự query. Review index usage định kỳ.
```

---

## Bài tập thực hành

- [ ] Aggregation: top 10 sản phẩm bán chạy nhất theo tháng
- [ ] Design schema: social media (users, posts, comments, likes) — embed vs ref
- [ ] Index: optimize slow query với explain()
- [ ] Change streams: real-time notification khi order status thay đổi

---

## Tài nguyên thêm

- [MongoDB University](https://university.mongodb.com/) — Free courses
- [MongoDB Schema Design Patterns](https://www.mongodb.com/blog/post/building-with-patterns-a-summary)
- [The Little MongoDB Book](https://www.openmymind.net/2011/3/28/The-Little-MongoDB-Book/) — Free
