# 🍃 MongoDB — NoSQL Document Database

> `[INTERMEDIATE]` — Dữ liệu linh hoạt, scale dễ dàng

---

## MongoDB là gì?

MongoDB lưu dữ liệu dưới dạng **documents** (JSON/BSON), thay vì rows và columns như SQL.

**Khi nào dùng MongoDB:**
- Dữ liệu không có cấu trúc cố định (schema-less)
- Content management, catalog, user profiles
- Real-time analytics, event logging
- Cần scale horizontal dễ dàng

**Khi nào KHÔNG dùng MongoDB:**
- Dữ liệu có quan hệ phức tạp
- Cần ACID transaction mạnh (dùng PostgreSQL)
- Financial transactions

---

## So sánh SQL vs MongoDB

| SQL | MongoDB |
|---|---|
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| JOIN | $lookup |
| Primary Key | `_id` |
| Index | Index |

---

## Cài đặt (Docker)

```bash
docker run -d \
  --name my-mongo \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -p 27017:27017 \
  mongo:7

# Kết nối
docker exec -it my-mongo mongosh -u root -p secret
# GUI: MongoDB Compass, Studio 3T
```

---

## CRUD cơ bản

```javascript
// Chọn database
use mydb

// ── CREATE ─────────────────────────────────────
db.users.insertOne({
    name: "Jesse",
    email: "jesse@example.com",
    age: 25,
    tags: ["developer", "blogger"],
    address: {
        city: "Hà Nội",
        country: "VN"
    },
    createdAt: new Date()
})

db.users.insertMany([
    { name: "Alice", age: 30 },
    { name: "Bob", age: 25 }
])

// ── READ ───────────────────────────────────────
db.users.findOne({ email: "jesse@example.com" })

db.users.find({ age: { $gte: 18 } })               // age >= 18
db.users.find({ "address.city": "Hà Nội" })        // Nested field
db.users.find({ tags: "developer" })               // Trong array
db.users.find({
    age: { $gte: 18, $lte: 30 },
    "address.country": "VN"
})

// Projection — chỉ lấy một số fields
db.users.find({}, { name: 1, email: 1, _id: 0 })

// Sort, Limit, Skip
db.users.find().sort({ age: -1 }).limit(10).skip(20)

// ── UPDATE ─────────────────────────────────────
// $set — Cập nhật field cụ thể
db.users.updateOne(
    { email: "jesse@example.com" },
    {
        $set: { age: 26, "address.city": "HCM" },
        $currentDate: { updatedAt: true }
    }
)

// $push — Thêm vào array
db.users.updateOne(
    { _id: ObjectId("...") },
    { $push: { tags: "devops" } }
)

// $pull — Xóa khỏi array
db.users.updateOne(
    { _id: ObjectId("...") },
    { $pull: { tags: "blogger" } }
)

// $inc — Tăng/giảm số
db.posts.updateOne(
    { _id: ObjectId("...") },
    { $inc: { viewCount: 1 } }
)

// upsert — update nếu có, insert nếu chưa có
db.users.updateOne(
    { email: "new@example.com" },
    { $set: { name: "New User" } },
    { upsert: true }
)

// ── DELETE ─────────────────────────────────────
db.users.deleteOne({ email: "jesse@example.com" })
db.users.deleteMany({ age: { $lt: 18 } })
```

---

## Query Operators

```javascript
// Comparison
$eq, $ne        // equal, not equal
$gt, $gte       // greater than, >=
$lt, $lte       // less than, <=
$in             // trong mảng
$nin            // không trong mảng

// Logical
$and, $or, $not, $nor

db.users.find({
    $or: [
        { age: { $lt: 18 } },
        { age: { $gt: 65 } }
    ]
})

// Element
$exists         // Field có tồn tại không
$type           // Kiểm tra type

// Array
$all            // Chứa tất cả giá trị
$elemMatch      // Ít nhất 1 phần tử khớp
$size           // Kích thước array

db.posts.find({
    tags: { $all: ["javascript", "react"] }
})

// Text search
db.posts.createIndex({ content: "text" })
db.posts.find({ $text: { $search: "machine learning" } })
```

---

## Aggregation Pipeline ⭐

```javascript
db.orders.aggregate([
    // Stage 1: Match
    { $match: { status: "completed", createdAt: { $gte: new Date("2026-01-01") } } },

    // Stage 2: Group
    { $group: {
        _id: "$userId",
        totalOrders: { $sum: 1 },
        totalAmount: { $sum: "$amount" },
        avgAmount: { $avg: "$amount" }
    }},

    // Stage 3: Lookup (JOIN)
    { $lookup: {
        from: "users",
        localField: "_id",
        foreignField: "_id",
        as: "userInfo"
    }},

    // Stage 4: Unwind array
    { $unwind: "$userInfo" },

    // Stage 5: Project — định nghĩa output
    { $project: {
        userName: "$userInfo.name",
        totalOrders: 1,
        totalAmount: { $round: ["$totalAmount", 2] }
    }},

    // Stage 6: Sort
    { $sort: { totalAmount: -1 } },

    // Stage 7: Limit
    { $limit: 10 }
])
```

---

## Indexes

```javascript
// Single field
db.users.createIndex({ email: 1 })           // 1 = ascending, -1 = descending

// Unique index
db.users.createIndex({ email: 1 }, { unique: true })

// Compound index
db.posts.createIndex({ status: 1, createdAt: -1 })

// Text index
db.posts.createIndex({ title: "text", content: "text" })

// TTL index — Tự động xóa documents sau X giây
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 })

// Liệt kê indexes
db.users.getIndexes()

// Xem query plan
db.users.find({ email: "test@example.com" }).explain("executionStats")
```

---

## Schema Design Patterns

```javascript
// ── Embedding (One-to-few) ──────────────────────
// Tốt khi data con được access cùng lúc với parent
const user = {
    _id: ObjectId(),
    name: "Jesse",
    addresses: [           // Embed addresses vào user
        { type: "home", city: "Hà Nội" },
        { type: "work", city: "HCM" }
    ]
}

// ── Referencing (One-to-many) ──────────────────
// Tốt khi data con rất lớn hoặc được access độc lập
const post = {
    _id: ObjectId(),
    title: "My Post",
    authorId: ObjectId("user_id")  // Reference đến users collection
}

// ── Hybrid ─────────────────────────────────────
// Bucket pattern: group time-series data
const hourlyStats = {
    date: new Date("2026-02-19T13:00:00"),
    deviceId: "sensor-001",
    measurements: [         // 60 readings trong 1 document
        { minute: 0, value: 23.5 },
        { minute: 1, value: 23.6 },
        // ...
    ],
    summary: { min: 23.0, max: 24.1, avg: 23.5 }
}
```

---

## Với Node.js (Mongoose)

```javascript
import mongoose from 'mongoose';

// Schema
const userSchema = new mongoose.Schema({
    name: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true },
    age: { type: Number, min: 0, max: 150 },
    role: { type: String, enum: ['user', 'admin'], default: 'user' },
    tags: [String],
    createdAt: { type: Date, default: Date.now }
});

// Virtual
userSchema.virtual('displayName').get(function() {
    return `${this.name} (${this.role})`;
});

// Method
userSchema.methods.isAdmin = function() {
    return this.role === 'admin';
};

const User = mongoose.model('User', userSchema);

// CRUD
const user = await User.create({ name: "Jesse", email: "j@example.com" });
const users = await User.find({ role: 'admin' }).select('name email').lean();
await User.findByIdAndUpdate(id, { $set: { age: 26 } }, { new: true });
await User.findByIdAndDelete(id);
```

---

## Bài tập thực hành

- [ ] Thiết kế schema cho Blog (posts, comments, tags)
- [ ] Viết aggregation pipeline tính thống kê bài viết theo tháng
- [ ] Tạo TTL index cho session management
- [ ] So sánh hiệu năng với/không có index bằng `explain()`

---

## Tài nguyên thêm

- [MongoDB Docs](https://www.mongodb.com/docs/) — Tài liệu chính thức
- [MongoDB University (free)](https://learn.mongodb.com/) — Khóa học miễn phí
- [Mongoose Docs](https://mongoosejs.com/docs/) — ODM cho Node.js
