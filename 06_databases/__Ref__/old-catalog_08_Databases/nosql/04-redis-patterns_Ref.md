# 🗃️ Redis Patterns nâng cao — Caching, Pub/Sub & Data Structures

> `[INTERMEDIATE → ADVANCED]` — Khai thác Redis hiệu quả

---

## 1. Caching Patterns

### Cache-Aside (Lazy Loading)

```javascript
import Redis from 'ioredis';
const redis = new Redis();

async function getCachedUser(userId) {
    const cacheKey = `user:${userId}`;

    // 1. Check cache
    const cached = await redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // 2. Cache miss → query DB
    const user = await db.users.findById(userId);
    if (!user) return null;

    // 3. Set cache with TTL
    await redis.set(cacheKey, JSON.stringify(user), 'EX', 3600);  // 1 hour
    return user;
}

// Invalidate on update
async function updateUser(userId, data) {
    await db.users.update(userId, data);
    await redis.del(`user:${userId}`);  // Xóa cache → lần sau query lại
}
```

### Cache Stampede Prevention

```javascript
// Problem: Cache expire → 1000 requests cùng lúc query DB!
// Solution: Distributed lock

async function getCachedWithLock(key, fetchFn, ttl = 3600) {
    const cached = await redis.get(key);
    if (cached) return JSON.parse(cached);

    // Chỉ 1 request được fetch, còn lại chờ
    const lockKey = `lock:${key}`;
    const acquired = await redis.set(lockKey, '1', 'EX', 10, 'NX');

    if (acquired) {
        try {
            const data = await fetchFn();
            await redis.set(key, JSON.stringify(data), 'EX', ttl);
            return data;
        } finally {
            await redis.del(lockKey);
        }
    }

    // Không lấy được lock → chờ rồi đọc cache
    await new Promise(r => setTimeout(r, 100));
    return getCachedWithLock(key, fetchFn, ttl);
}
```

---

## 2. Data Structures nâng cao

### Sorted Sets — Leaderboard / Ranking

```bash
# Thêm scores
ZADD leaderboard 1500 "player:1"
ZADD leaderboard 2300 "player:2"
ZADD leaderboard 1800 "player:3"

# Top 10 (điểm cao → thấp)
ZREVRANGE leaderboard 0 9 WITHSCORES

# Rank của 1 player
ZREVRANK leaderboard "player:1"  # → 2 (top 3)

# Cập nhật điểm
ZINCRBY leaderboard 500 "player:1"  # +500 điểm
```

```javascript
// Leaderboard API
async function addScore(userId, score) {
    await redis.zadd('leaderboard', score, `user:${userId}`);
}

async function getTopPlayers(limit = 10) {
    const results = await redis.zrevrange('leaderboard', 0, limit - 1, 'WITHSCORES');
    const players = [];
    for (let i = 0; i < results.length; i += 2) {
        players.push({ userId: results[i], score: parseInt(results[i + 1]) });
    }
    return players;
}

async function getPlayerRank(userId) {
    const rank = await redis.zrevrank('leaderboard', `user:${userId}`);
    return rank !== null ? rank + 1 : null;  // 0-indexed → 1-indexed
}
```

### Hash — Object storage

```bash
# User profile
HSET user:1 name "An" email "an@mail.com" age 25 role "admin"
HGET user:1 name         # "An"
HGETALL user:1           # { name: "An", email: "an@mail.com", ... }
HINCRBY user:1 age 1     # 26 (tăng tuổi!)

# Tiết kiệm RAM hơn nhiều key riêng lẻ!
```

### Bitmaps — Track user activity

```javascript
// User daily login tracking
async function trackLogin(userId) {
    const today = new Date().toISOString().split('T')[0];  // 2026-03-04
    await redis.setbit(`logins:${today}`, userId, 1);
}

async function countDailyLogins(date) {
    return await redis.bitcount(`logins:${date}`);
}

// Users logged in cả 3 ngày gần đây
await redis.bitop('AND', 'active:3days', 'logins:2026-03-02', 'logins:2026-03-03', 'logins:2026-03-04');
const activeUsers = await redis.bitcount('active:3days');
```

---

## 3. Pub/Sub — Real-time messaging

```javascript
// Publisher
const pub = new Redis();
pub.publish('notifications', JSON.stringify({
    userId: 123,
    type: 'order_shipped',
    message: 'Đơn hàng đã gửi!',
}));

// Subscriber (server khác!)
const sub = new Redis();
sub.subscribe('notifications', 'chat:room:1');

sub.on('message', (channel, message) => {
    const data = JSON.parse(message);
    console.log(`[${channel}]`, data);
    // Gửi WebSocket tới client
    io.to(data.userId).emit('notification', data);
});
```

---

## 4. Rate Limiting — Sliding Window

```javascript
// Token bucket rate limiter
async function isRateLimited(userId, limit = 100, windowSec = 60) {
    const key = `rate:${userId}`;
    const now = Date.now();
    const windowStart = now - windowSec * 1000;

    const multi = redis.multi();
    multi.zremrangebyscore(key, 0, windowStart);   // Xóa requests cũ
    multi.zadd(key, now, `${now}`);                 // Thêm request hiện tại
    multi.zcard(key);                                // Đếm requests trong window
    multi.expire(key, windowSec);                    // TTL
    const results = await multi.exec();

    const requestCount = results[2][1];
    return requestCount > limit;
}

// Middleware
app.use(async (req, res, next) => {
    if (await isRateLimited(req.ip, 100, 60)) {
        return res.status(429).json({ error: 'Too many requests' });
    }
    next();
});
```

---

## 5. Session Storage

```javascript
import session from 'express-session';
import RedisStore from 'connect-redis';

app.use(session({
    store: new RedisStore({ client: redis }),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: true,
        httpOnly: true,
        maxAge: 24 * 60 * 60 * 1000,  // 1 day
    },
}));
// Session data tự động lưu Redis → hỗ trợ multiple servers!
```

---

## 6. Redis Best Practices

```
Key naming:
✅ user:123:profile       (object:id:field)
✅ cache:users:page:1     (namespace:resource:param)
✅ rate:192.168.1.1       (feature:identifier)
❌ myKey, data, temp      (vô nghĩa!)

TTL:
✅ LUÔN set TTL cho cache keys → tránh memory leak
✅ Cache hot data: 5-60 min
✅ Session: 24h
✅ Rate limit: 1-60 min

Memory:
✅ Dùng Hash thay vì nhiều String keys (tiết kiệm 10x RAM)
✅ Monitor: redis-cli INFO memory
✅ Set maxmemory + eviction policy (allkeys-lru)
```

---

## Bài tập thực hành

- [ ] Cache-aside pattern cho user profiles
- [ ] Leaderboard API với Sorted Sets
- [ ] Rate limiter middleware (sliding window)
- [ ] Pub/Sub: real-time notifications

---

## Tài nguyên thêm

- [Redis Docs](https://redis.io/docs/) — Official
- [Redis University](https://university.redis.com/) — Free courses
- [Redis Best Practices](https://redis.io/docs/management/optimization/)
