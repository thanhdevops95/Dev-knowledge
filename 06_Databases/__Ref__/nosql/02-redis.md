# ⚡ Redis — In-memory Data Store

> `[INTERMEDIATE]` — Cache, Session, Queue — nhanh nhất thế giới

---

## Redis là gì?

Redis (Remote Dictionary Server) là **in-memory data store** — lưu dữ liệu trong RAM nên cực nhanh (thường < 1ms latency).

**Dùng Redis khi:**
- **Caching** — Cache kết quả DB, API, HTML
- **Session storage** — Lưu user sessions
- **Rate limiting** — Giới hạn số request
- **Pub/Sub** — Message broker đơn giản
- **Queues** — Background jobs (với Bull/BullMQ)
- **Leaderboard** — Real-time rankings với Sorted Sets
- **Distributed locks** — Tránh race conditions

---

## Cài đặt

```bash
docker run -d --name my-redis -p 6379:6379 redis:7-alpine

# Kết nối
docker exec -it my-redis redis-cli
```

---

## Data Structures

### String — Kiểu cơ bản nhất

```bash
SET user:1:name "Jesse"
GET user:1:name              # "Jesse"

# Với expiry (TTL)
SET session:abc123 "user_id:1" EX 3600    # Expire sau 1 giờ
TTL session:abc123                         # Xem còn bao nhiêu giây

# Counter
SET page:views 0
INCR page:views              # 1
INCRBY page:views 10         # 11
DECR page:views              # 10

# Atomic get-and-set
GETSET user:1:token "new_token"

# Nhiều keys cùng lúc
MSET user:1:name "Jesse" user:1:email "j@example.com"
MGET user:1:name user:1:email
```

### Hash — Object/Dictionary

```bash
HSET user:1 name "Jesse" email "jesse@example.com" age 25
HGET user:1 name             # "Jesse"
HGETALL user:1               # Tất cả fields
HMGET user:1 name email      # Nhiều fields
HDEL user:1 age              # Xóa field
HEXISTS user:1 email         # Kiểm tra tồn tại
HKEYS user:1                 # Tất cả keys
HLEN user:1                  # Số fields
HINCRBY user:1 age 1         # Tăng số
```

### List — Queue / Stack

```bash
# RPUSH = push right, LPUSH = push left
RPUSH tasks "task1" "task2" "task3"
LPUSH tasks "urgent-task"

LRANGE tasks 0 -1            # Lấy tất cả: [urgent-task, task1, task2, task3]
LLEN tasks                   # Độ dài

# Pop
LPOP tasks                   # Lấy và xóa từ trái
RPOP tasks                   # Lấy và xóa từ phải
BLPOP tasks 5                # Blocking pop (chờ tối đa 5s)

# Dùng như Queue: RPUSH (enqueue) + BLPOP (dequeue)
# Dùng như Stack: RPUSH (push) + RPOP (pop)
```

### Set — Tập hợp không trùng lặp

```bash
SADD tags "python" "backend" "python"  # {"python", "backend"}
SCARD tags                              # 2
SISMEMBER tags "python"                # 1 (true)
SMEMBERS tags                          # Tất cả thành viên
SREM tags "backend"                    # Xóa

# Set operations
SUNION set1 set2             # Hợp
SINTER set1 set2             # Giao
SDIFF set1 set2              # Hiệu
```

### Sorted Set — Leaderboard / Priority Queue

```bash
ZADD leaderboard 1000 "Alice" 850 "Bob" 1200 "Charlie"

ZRANK leaderboard "Alice"            # Index (0-based, tăng dần)
ZREVRANK leaderboard "Alice"         # Reverse rank
ZSCORE leaderboard "Alice"           # Score
ZINCRBY leaderboard 50 "Bob"         # Tăng score

ZRANGE leaderboard 0 -1 WITHSCORES REV  # Top scores
ZRANGEBYSCORE leaderboard 900 1300      # Theo score range
```

---

## Patterns phổ biến

### Cache Aside Pattern

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user(user_id: int):
    cache_key = f"user:{user_id}"
    
    # 1. Kiểm tra cache
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)  # Cache HIT
    
    # 2. Cache MISS → lấy từ DB
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    
    # 3. Lưu vào cache 1 giờ
    r.setex(cache_key, 3600, json.dumps(user))
    
    return user

def update_user(user_id: int, data: dict):
    db.update("UPDATE users SET ... WHERE id = %s", user_id)
    # Xóa cache để lần sau lấy lại từ DB
    r.delete(f"user:{user_id}")
```

### Session Storage

```python
import secrets

def create_session(user_id: int) -> str:
    session_id = secrets.token_urlsafe(32)
    r.setex(
        f"session:{session_id}",
        3600,  # 1 giờ
        json.dumps({"user_id": user_id, "role": "user"})
    )
    return session_id

def get_session(session_id: str) -> dict | None:
    data = r.get(f"session:{session_id}")
    if data:
        # Refresh TTL mỗi lần dùng (sliding expiration)
        r.expire(f"session:{session_id}", 3600)
        return json.loads(data)
    return None

def delete_session(session_id: str):
    r.delete(f"session:{session_id}")
```

### Rate Limiting

```python
def is_rate_limited(user_id: int, limit: int = 100, window: int = 60) -> bool:
    key = f"rate_limit:{user_id}:{int(time.time() // window)}"
    
    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    results = pipe.execute()
    
    request_count = results[0]
    return request_count > limit
```

### Pub/Sub

```python
# Publisher
r.publish("notifications", json.dumps({
    "type": "new_message",
    "from": "Alice",
    "to": "Bob"
}))

# Subscriber
pubsub = r.pubsub()
pubsub.subscribe("notifications")

for message in pubsub.listen():
    if message["type"] == "message":
        data = json.loads(message["data"])
        print(f"Nhận: {data}")
```

---

## Với Node.js

```javascript
import { createClient } from 'redis';

const client = createClient({ url: 'redis://localhost:6379' });
await client.connect();

// String với expiry
await client.setEx('session:abc', 3600, JSON.stringify({ userId: 1 }));
const session = JSON.parse(await client.get('session:abc'));

// Hash
await client.hSet('user:1', { name: 'Jesse', email: 'j@example.com' });
const user = await client.hGetAll('user:1');

// Pipeline (batch commands)
const pipeline = client.multi();
pipeline.incr('counter');
pipeline.expire('counter', 60);
await pipeline.exec();
```

---

## Best Practices

```bash
# 1. Đặt tên key có namespace
user:1:profile       # ✅
user_1_profile       # ❌

# 2. Luôn đặt TTL cho data tạm
SET key value EX 3600    # Không để eternal keys

# 3. Dùng SCAN thay vì KEYS (production)
KEYS pattern          # ❌ Block server!
SCAN 0 MATCH user:* COUNT 100  # ✅

# 4. Monitor
INFO stats
MONITOR              # Real-time commands (debug only!)
SLOWLOG GET 10       # Xem slow commands

# 5. Memory
MEMORY USAGE user:1
CONFIG GET maxmemory
CONFIG SET maxmemory-policy allkeys-lru
```

---

## Bài tập thực hành

- [ ] Implement cache layer cho một API endpoint
- [ ] Xây dựng rate limiter đơn giản
- [ ] Tạo real-time leaderboard với Sorted Set
- [ ] Implement session management với sliding expiration

---

## Tài nguyên thêm

- [Redis Docs](https://redis.io/docs/) — Tài liệu chính thức
- [Redis University (free)](https://university.redis.com/) — Khóa học miễn phí
- [Try Redis](https://try.redis.io/) — Thử Redis trực tuyến
