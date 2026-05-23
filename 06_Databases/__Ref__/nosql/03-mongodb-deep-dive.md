# MongoDB Deep Dive

> **Tags:** `mongodb` `nosql` `aggregation` `indexes` `transactions` `sharding` `atlas`
> **Level:** Intermediate | **Prerequisite:** `nosql/01-nosql-basics.md`

---

## 1. Document Model

```javascript
// MongoDB stores BSON documents (Binary JSON)
// Flexible schema = no fixed columns like SQL

// Example document
{
  _id: ObjectId("64a1e3f2b9d5c8e1234abc01"),  // Auto-generated unique ID
  name: "Alice Johnson",
  email: "alice@example.com",
  age: 30,
  address: {                          // Embedded document (denormalized)
    street: "123 Main St",
    city: "Hanoi",
    country: "VN",
    location: {                       // GeoJSON
      type: "Point",
      coordinates: [105.8412, 21.0278]
    }
  },
  tags: ["premium", "verified"],     // Array
  orders: [                           // Embedded array of documents
    { orderId: "ORD-001", amount: 150.0, date: ISODate("2024-01-15") },
    { orderId: "ORD-002", amount: 89.99, date: ISODate("2024-02-01") },
  ],
  createdAt: ISODate("2024-01-10T10:30:00Z"),
  metadata: {
    source: "web",
    campaign: "winter-2024",
  }
}
```

### Embedding vs Referencing
```javascript
// EMBED when:
// - Data is always read together (one-to-few relationship)
// - Nested data doesn't grow unboundedly
// - Need atomic updates

// REFERENCE when:
// - Data is large and seldom read
// - One-to-many (many side could be huge)
// - Many-to-many relationships

// REFERENCE example
// users collection
{ _id: ObjectId("user1"), name: "Alice" }

// posts collection
{ 
  _id: ObjectId("post1"), 
  title: "My Post",
  authorId: ObjectId("user1"),   // Reference — not embedded!
  commentCount: 42
}

// To load post with author:
db.posts.aggregate([
  { $lookup: {
    from: "users",
    localField: "authorId",
    foreignField: "_id",
    as: "author"
  }},
  { $unwind: "$author" }
]);
```

---

## 2. CRUD Operations

```javascript
// INSERT
db.users.insertOne({ name: "Alice", email: "alice@example.com" });
db.users.insertMany([
  { name: "Bob" },
  { name: "Carol" },
], { ordered: false });  // Continue on duplicate key errors

// FIND
db.users.findOne({ email: "alice@example.com" });    // Returns first match
db.users.find({ city: "Hanoi" }).toArray();          // Returns all matches

// Query operators
db.users.find({
  age: { $gte: 18, $lte: 65 },               // Range
  status: { $in: ["active", "premium"] },     // In list
  email: { $exists: true, $ne: null },        // Field exists and not null
  "address.city": "Hanoi",                    // Dot notation for nested
  tags: "premium",                             // Match in array
  tags: { $all: ["premium", "verified"] },    // Match ALL elements
  tags: { $elemMatch: { $gt: "a", $lt: "z" } },  // Array element conditions
  name: { $regex: /^Alice/i },               // Regex
});

// Projection (select fields)
db.users.find(
  { active: true },
  { name: 1, email: 1, _id: 0 }  // 1=include, 0=exclude
);

// Sorting, limit, skip
db.users.find()
  .sort({ createdAt: -1 })   // -1 = descending
  .limit(10)
  .skip(20);  // Page 3 (0-indexed, 10 per page)

// UPDATE
db.users.updateOne(
  { _id: ObjectId("...") },    // Filter
  { $set: { name: "Alice Updated", updatedAt: new Date() } }  // Update
);

// Update operators
db.users.updateMany(
  { status: "trial" },
  {
    $set: { status: "active" },
    $inc: { loginCount: 1 },          // Increment
    $push: { tags: "verified" },      // Append to array
    $pull: { tags: "trial" },         // Remove from array
    $addToSet: { tags: "premium" },   // Add if not exists
    $unset: { tempField: "" },        // Delete field
    $currentDate: { updatedAt: true },  // Set to current date
  }
);

// Upsert (insert if not found)
db.users.updateOne(
  { email: "newuser@example.com" },
  { $setOnInsert: { createdAt: new Date() }, $set: { name: "New User" } },
  { upsert: true }
);

// Find and update (returns document)
const updated = db.users.findOneAndUpdate(
  { _id: id },
  { $inc: { views: 1 } },
  { returnDocument: 'after' }  // Return updated doc
);

// DELETE
db.users.deleteOne({ _id: id });
db.users.deleteMany({ status: "inactive", lastLogin: { $lt: twoYearsAgo } });
```

---

## 3. Aggregation Pipeline

```javascript
// Pipeline = series of stages that transform documents

// Example: Sales report by category
db.orders.aggregate([
  // Stage 1: Filter (like WHERE)
  { $match: {
    status: "completed",
    createdAt: { $gte: ISODate("2024-01-01") }
  }},
  
  // Stage 2: Lookup (like JOIN)
  { $lookup: {
    from: "products",
    localField: "productId",
    foreignField: "_id",
    as: "product"
  }},
  
  // Stage 3: Deconstruct array
  { $unwind: "$product" },
  
  // Stage 4: Add computed fields
  { $addFields: {
    revenue: { $multiply: ["$quantity", "$product.price"] },
    month: { $dateToString: { format: "%Y-%m", date: "$createdAt" } }
  }},
  
  // Stage 5: Group (like GROUP BY + aggregate)
  { $group: {
    _id: { category: "$product.category", month: "$month" },
    totalRevenue: { $sum: "$revenue" },
    orderCount: { $sum: 1 },
    avgOrderValue: { $avg: "$revenue" },
    uniqueCustomers: { $addToSet: "$customerId" }
  }},
  
  // Stage 6: Project (reshape)
  { $project: {
    _id: 0,
    category: "$_id.category",
    month: "$_id.month",
    totalRevenue: { $round: ["$totalRevenue", 2] },
    orderCount: 1,
    avgOrderValue: { $round: ["$avgOrderValue", 2] },
    uniqueCustomers: { $size: "$uniqueCustomers" }
  }},
  
  // Stage 7: Sort
  { $sort: { totalRevenue: -1 } },
  
  // Stage 8: Limit
  { $limit: 20 }
]);

// facet — multiple aggregations in one pass
db.products.aggregate([
  { $facet: {
    priceRanges: [
      { $bucket: {
        groupBy: "$price",
        boundaries: [0, 50, 100, 200, 500],
        default: "500+",
        output: { count: { $sum: 1 } }
      }}
    ],
    categories: [
      { $group: { _id: "$category", count: { $sum: 1 } } },
      { $sort: { count: -1 } },
      { $limit: 10 }
    ],
    stats: [
      { $group: {
        _id: null,
        avgPrice: { $avg: "$price" },
        maxPrice: { $max: "$price" },
        totalProducts: { $sum: 1 }
      }}
    ]
  }}
]);
```

---

## 4. Indexes — Performance

```javascript
// Check query performance
db.users.find({ email: "alice@example.com" }).explain("executionStats");
// Look for: COLLSCAN (bad) vs IXSCAN (good)

// Single field index
db.users.createIndex({ email: 1 });       // 1 = ascending, -1 = descending
db.users.createIndex({ email: 1 }, { unique: true });

// Compound index (order matters!)
db.orders.createIndex({ userId: 1, status: 1, createdAt: -1 });
// Supports queries: { userId } | { userId, status } | { userId, status, createdAt }
// NOT: { status } | { createdAt } alone

// Text index (full-text search)
db.articles.createIndex({ title: "text", content: "text" }, {
  weights: { title: 10, content: 1 }  // Title more important
});
db.articles.find({ $text: { $search: "mongodb performance" } });

// Geospatial index
db.places.createIndex({ location: "2dsphere" });
db.places.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [105.84, 21.02] },
      $maxDistance: 1000  // 1km radius
    }
  }
});

// Partial index (only index subset)
db.users.createIndex(
  { email: 1 },
  { partialFilterExpression: { status: "active" } }  // Only active users
);

// TTL index (auto-delete documents)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 86400 }  // Delete after 24 hours
);

// Sparse index (don't index documents missing the field)
db.users.createIndex({ phone: 1 }, { sparse: true });

// List and analyze indexes
db.users.getIndexes();
db.users.totalIndexSize();
db.users.explain().find({ email: "alice@example.com" });
```

---

## 5. Transactions (ACID)

```javascript
// Multi-document ACID transactions (requires replica set)
const session = client.startSession();

try {
  session.startTransaction({
    readConcern: { level: "snapshot" },
    writeConcern: { w: "majority" }
  });
  
  // All operations use the same session
  await orders.insertOne({ 
    userId, 
    items, 
    total 
  }, { session });
  
  await inventory.updateMany(
    { productId: { $in: productIds } },
    { $inc: { stock: -1 } },
    { session }
  );
  
  await users.updateOne(
    { _id: userId },
    { $inc: { totalSpent: total } },
    { session }
  );
  
  await session.commitTransaction();
  
} catch (error) {
  await session.abortTransaction();
  throw error;
} finally {
  await session.endSession();
}

// With callback API (auto-retry on transient errors)
const result = await client.withSession(session =>
  session.withTransaction(async () => {
    // ... operations
  })
);
```

---

## 6. Change Streams — Real-time

```javascript
// Watch for changes to a collection
const changeStream = db.orders.watch([
  { $match: { "fullDocument.status": "completed" } }
], {
  fullDocument: "updateLookup"  // Include full document on updates
});

changeStream.on('change', (change) => {
  const { operationType, fullDocument, documentKey } = change;
  
  switch (operationType) {
    case 'insert':
      notifyNewOrder(fullDocument);
      break;
    case 'update':
      updateDashboard(fullDocument);
      break;
    case 'delete':
      removeFromCache(documentKey._id);
      break;
  }
});

// Resume from a specific position (after restart)
const { resumeToken } = changeStream;
// Store resumeToken, use on reconnect:
const stream = db.orders.watch([], { resumeAfter: resumeToken });
```

---

## 7. Schema Validation

```javascript
// Enforce schema with JSON Schema validation
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email", "createdAt"],
      properties: {
        name: {
          bsonType: "string",
          minLength: 2,
          maxLength: 100,
          description: "Name is required and must be 2-100 chars"
        },
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
          description: "Must be valid email format"
        },
        age: {
          bsonType: "int",
          minimum: 0,
          maximum: 120,
        },
        role: {
          enum: ["admin", "user", "guest"],
          description: "Must be one of: admin, user, guest"
        },
        address: {
          bsonType: "object",
          required: ["city", "country"],
          properties: {
            city: { bsonType: "string" },
            country: { bsonType: "string", minLength: 2, maxLength: 2 }
          }
        }
      }
    }
  },
  validationLevel: "strict",    // "strict" or "moderate"
  validationAction: "error"     // "error" or "warn"
});
```

---

## 8. Sharding — Horizontal Scaling

```javascript
// Enable sharding on database
sh.enableSharding("myapp");

// Shard collection by field
sh.shardCollection("myapp.orders", { userId: "hashed" });  // Hashed = even distribution
sh.shardCollection("myapp.events", { date: 1, region: 1 });  // Range = query efficiency

// Sharding strategies:
// Hashed sharding: even data distribution, no range queries
// Range sharding: efficient range queries, may cause hotspots

// Check sharding status
sh.status();
db.orders.getShardDistribution();

// Zones (pin certain data to specific shards)
sh.addTagRange(
  "myapp.users",
  { region: "US" },       // Min
  { region: "US\uffff" }, // Max
  "us-east-shard"         // Tag name
);

// Tag shards
sh.addShardTag("shard01", "us-east-shard");
```

---

## 9. Mongoose — ODM

```typescript
import mongoose, { Schema, Document, Model } from 'mongoose';

// Schema definition
const userSchema = new Schema<IUser>({
  name: {
    type: String,
    required: [true, 'Name is required'],
    trim: true,
    minlength: 2,
    maxlength: 100,
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    validate: {
      validator: (v: string) => /\S+@\S+\.\S+/.test(v),
      message: 'Invalid email format',
    },
  },
  password: { type: String, select: false },  // Exclude from queries by default
  role: { type: String, enum: ['admin', 'user'], default: 'user' },
  tags: [{ type: String }],
  address: {
    city: String,
    country: String,
    location: {
      type: { type: String, default: 'Point' },
      coordinates: [Number],
    },
  },
}, {
  timestamps: true,  // Auto-add createdAt, updatedAt
  versionKey: false,
});

// Indexes
userSchema.index({ email: 1 }, { unique: true });
userSchema.index({ 'address.location': '2dsphere' });

// Virtual (not stored in DB)
userSchema.virtual('displayName').get(function (this: IUser) {
  return `${this.name} <${this.email}>`;
});

// Pre-save hook (e.g., hash password)
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password!, 12);
  next();
});

// Instance method
userSchema.methods.comparePassword = async function (password: string) {
  return bcrypt.compare(password, this.password);
};

// Static method
userSchema.statics.findByEmail = function (email: string) {
  return this.findOne({ email: email.toLowerCase() });
};

const User = mongoose.model<IUser, UserModel>('User', userSchema);

// Queries
const users = await User.find({ role: 'admin' })
  .select('name email role')
  .populate('orders')      // Populate referenced documents
  .sort({ createdAt: -1 })
  .limit(10)
  .lean();                 // Return plain JS objects (faster, no mongoose overhead)

// Transactions with Mongoose
const session = await mongoose.startSession();
session.startTransaction();
try {
  await Order.create([{ userId, items }], { session });
  await User.updateOne({ _id: userId }, { $inc: { orderCount: 1 } }, { session });
  await session.commitTransaction();
} catch (e) {
  await session.abortTransaction();
  throw e;
} finally {
  session.endSession();
}
```

---

## 10. Performance Tips

```javascript
// 1. Use projections to limit data returned
db.users.find({}, { password: 0, __v: 0 });

// 2. Avoid $where and JavaScript expressions
// Bad: db.users.find({ $where: "this.age > 18" })  →slow: no index
// Good: db.users.find({ age: { $gt: 18 } })

// 3. Use covered queries (all fields in index)
db.users.createIndex({ email: 1, name: 1 });
db.users.find({ email: "..." }, { email: 1, name: 1, _id: 0 });
// → No document fetch needed!

// 4. Limit results always
db.users.find({}).limit(1000);  // Never return unbounded results

// 5. Use $inc instead of read-modify-write
// Bad: user.views++; user.save()  (race condition!)
// Good: db.users.updateOne({ _id: id }, { $inc: { views: 1 } })  (atomic)

// 6. Aggregation: $match and $project early
db.orders.aggregate([
  { $match: { status: "active" } },   // ← Filter FIRST reduces docs
  { $project: { total: 1 } },         // ← Project EARLY reduces size
  { $group: { ... } },
  { $sort: { ... } },
]);

// 7. allowDiskUse for large aggregations
db.orders.aggregate([...], { allowDiskUse: true });

// 8. Monitor slow queries
db.setProfilingLevel(1, { slowms: 100 });  // Log queries >100ms
db.system.profile.find().limit(10).sort({ ts: -1 });
```

---

*Tài liệu liên quan: `nosql/01-nosql-basics.md` | `nosql/02-redis-deep-dive.md` | `sql/02-postgresql-advanced.md`*
