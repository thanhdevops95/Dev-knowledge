# Redis Deep Dive

> **Tags:** `redis` `caching` `pub-sub` `streams` `sorted-sets` `lua` `cluster`
> **Level:** Intermediate | **Prerequisite:** `nosql/01-nosql-basics.md`

---

## 1. Data Structures

### Strings
```bash
# SET với options
SET user:1:name "Alice" EX 3600 NX   # EX=seconds TTL, NX=only if not exists
SET counter 0
INCR counter         # Atomic increment → 1
INCRBY counter 10    # → 11
DECR counter         # → 10
INCRBYFLOAT price 2.5

# Get/Set multiple
MSET user:1:name "Alice" user:1:email "alice@example.com"
MGET user:1:name user:1:email

# String as bit array (space-efficient flags)
SETBIT feature_flags:user:1 0 1   # Enable feature 0
GETBIT feature_flags:user:1 0     # → 1
BITCOUNT feature_flags:user:1     # Count enabled features
```

### Hash — Object-like Storage
```bash
# Hash = map within a key
HSET user:1 name "Alice" email "alice@example.com" age 30
HGET user:1 name            # "Alice"
HMGET user:1 name email     # Multiple fields
HGETALL user:1              # All fields + values
HKEYS user:1               # ["name", "email", "age"]
HLEN user:1                # 3
HEXISTS user:1 name         # 1 (true)
HDEL user:1 age
HINCRBY user:1 score 10    # Increment numeric field

# Memory: small hashes (<=128 fields, <=64 bytes/value) stored as listpack (very efficient)
```

### List — Ordered, Allows Duplicates
```bash
LPUSH queue job1 job2 job3   # Push to left: [job3, job2, job1]
RPUSH queue job4             # Push to right: [job3, job2, job1, job4]
LPOP queue                   # Pop from left: job3
RPOP queue                   # Pop from right: job4
LRANGE queue 0 -1            # Get all elements
LLEN queue
LINDEX queue 0               # First element

# Blocking pop — message queue pattern!
BLPOP queue1 queue2 0        # Wait indefinitely for element
BRPOP queue 30               # Wait max 30 seconds

# Fixed-size list
LPUSH notifications:user:1 "New message"
LTRIM notifications:user:1 0 99   # Keep only last 100

# Useful: activity feed, job queue, recent items
```

### Set — Unique, Unordered
```bash
SADD online_users user:1 user:2 user:3
SMEMBERS online_users
SISMEMBER online_users user:1   # 1 (exists)
SCARD online_users              # 3 (count)
SREM online_users user:2

# Set operations — very powerful!
SUNION set1 set2        # All elements from both
SINTER set1 set2        # Only elements in BOTH
SDIFF set1 set2         # Elements in set1 but NOT set2

# Example: Common friends
SADD user:1:friends user:3 user:4 user:5
SADD user:2:friends user:4 user:5 user:6
SINTER user:1:friends user:2:friends   # [user:4, user:5]

# Store result
SINTERSTORE common_friends user:1:friends user:2:friends
```

### Sorted Set (ZSet) — Score-based Ranking
```bash
# Add with score
ZADD leaderboard 1500 "Alice"
ZADD leaderboard 2300 "Bob"
ZADD leaderboard 1800 "Carol"

# Get rankings (ascending by score)
ZRANGE leaderboard 0 -1 WITHSCORES     # All, lowest first
ZREVRANGE leaderboard 0 2 WITHSCORES   # Top 3, highest first
ZRANK leaderboard "Alice"              # Rank (0-indexed): 0
ZREVRANK leaderboard "Alice"           # Reverse rank: 2
ZSCORE leaderboard "Alice"             # 1500

# Range by score
ZRANGEBYSCORE leaderboard 1000 2000    # Scores 1000-2000
ZRANGEBYSCORE leaderboard -inf +inf LIMIT 0 10  # Pagination!

# Update score (atomic)
ZINCRBY leaderboard 100 "Alice"   # Alice now: 1600

# Remove lowest N elements
ZPOPMIN leaderboard 5

# Use cases: leaderboards, rate limiting, delayed queues, priority queues
```

---

## 2. Advanced Data Structures

### Bitmap — Compact Boolean Flags
```bash
# Each bit = 1 day of user activity (365 days = 46 bytes!)
SETBIT user:123:activity:2024 0 1    # Active on day 0 (Jan 1)
SETBIT user:123:activity:2024 15 1   # Active on day 15
SETBIT user:123:activity:2024 16 1

BITCOUNT user:123:activity:2024       # Total active days
BITCOUNT user:123:activity:2024 0 6   # Active days in first week (bytes 0-6)

# Bitfield operations
BITPOS user:123:activity:2024 1       # First active day

# Count active users (bitwise AND/OR across all users)
BITOP AND active_both user:1:activity user:2:activity  # Both active on same days
BITOP OR any_active user:1:activity user:2:activity    # Either active
```

### HyperLogLog — Approximate Count
```bash
# Count unique visitors without storing all user IDs
# Memory: ~12KB regardless of unique count.  Error: ~0.81%

PFADD visitors:2024-01-15 user:1 user:2 user:3
PFADD visitors:2024-01-15 user:1  # Duplicate - ignored
PFCOUNT visitors:2024-01-15       # ~3

# Merge multiple HLLs
PFMERGE visitors:week visitors:2024-01-13 visitors:2024-01-14 visitors:2024-01-15
PFCOUNT visitors:week   # Approximate unique visitors in week
```

### Streams — Persistent Message Log
```bash
# Add messages (like Kafka)
XADD events * action "purchase" userId "123" amount "99.99"
# Returns: "1704067200000-0" (timestamp-sequence ID)

XADD events 1704067200000-1 action "view" productId "456"

# Read messages
XRANGE events - +           # All messages
XRANGE events - + COUNT 10  # First 10
XREVRANGE events + -        # Reverse order
XREAD COUNT 10 STREAMS events 0    # From beginning

# Consumer groups (parallel processing like Kafka consumer groups)
XGROUP CREATE events consumer-group $ MKSTREAM
XREADGROUP GROUP consumer-group worker-1 COUNT 10 STREAMS events >  # > = only new messages

# Acknowledge processed
XACK events consumer-group 1704067200000-0

# Pending messages (not acknowledged)
XPENDING events consumer-group - + 10
```

---

## 3. Persistence

```
No persistence:    Pure cache. Data lost on restart.
                   appendonly no, save ""

RDB (Snapshots):   Fork process, write full snapshot to disk periodically.
                   Fast restart, but may lose minutes of data.
                   save 900 1 (every 900s if ≥1 change)
                   save 300 10
                   save 60 10000

AOF (Append Only): Write every command to log. Most durable.
                   appendonly yes
                   appendfsync everysec  (balance performance/durability)
                   appendfsync always    (safest, slowest)
                   appendfsync no        (fastest, OS decides)

RDB + AOF:         Best of both. Use for production.
                   On restart: use AOF (more data), use RDB if AOF missing.
```

```bash
# Manual save
SAVE     # Blocking — blocks Redis until done
BGSAVE   # Background — fork and save asynchronously

# Check last save time
LASTSAVE

# AOF rewrite (compact AOF file)
BGREWRITEAOF
```

---

## 4. Pub/Sub

```bash
# Subscribe to channels
SUBSCRIBE news:tech news:sports
PSUBSCRIBE news:*    # Pattern subscribe (all news channels)

# Publish
PUBLISH news:tech "Redis 8.0 released"
# → All subscribers of news:tech receive this

# List subscriptions
PUBSUB CHANNELS         # All active channels
PUBSUB NUMSUB news:tech  # Number of subscribers for channel
```

```python
import redis
import threading

r = redis.Redis()

def subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe('events')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received: {message['data']}")

def publisher():
    import time
    for i in range(10):
        r.publish('events', f'event-{i}')
        time.sleep(0.5)

threading.Thread(target=subscriber).start()
publisher()

# Note: Pub/Sub is fire-and-forget
# If subscriber is offline, messages are LOST
# Use Streams for persistent/reliable messaging
```

---

## 5. Transactions with MULTI/EXEC

```bash
# MULTI...EXEC = atomic execution of queued commands
MULTI
DECRBY inventory:product:1 1    # Decrement inventory
INCR order_count                 # Increment orders
EXEC    # Execute all atomically

# DISCARD — cancel queued commands
MULTI
INCR counter
DISCARD  # Clear queue, exit transaction mode

# WATCH — optimistic locking (CAS)
WATCH inventory:product:1

current = GET inventory:product:1  # Read outside MULTI

MULTI
DECRBY inventory:product:1 1
EXEC  # Returns nil if inventory changed after WATCH (conflict!)
# If nil: retry the whole thing
```

```python
# Python: retry pattern with WATCH
def buy_item(product_id: str, quantity: int):
    with r.pipeline() as pipe:
        while True:
            try:
                pipe.watch(f'inventory:{product_id}')
                
                current = int(pipe.get(f'inventory:{product_id}') or 0)
                if current < quantity:
                    pipe.unwatch()
                    raise ValueError("Insufficient inventory")
                
                pipe.multi()
                pipe.decrby(f'inventory:{product_id}', quantity)
                pipe.execute()   # Fails if watched key changed
                break            # Success!
            except redis.WatchError:
                continue         # Retry
```

---

## 6. Lua Scripting

Lua scripts run **atomically** — no other commands execute in between:

```python
import redis

r = redis.Redis()

# Rate limiter (atomic: no race condition)
RATE_LIMITER = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

-- Current count
local current = redis.call('INCR', key)

-- Set TTL on first request
if current == 1 then
    redis.call('EXPIRE', key, window)
end

-- Check limit
if current <= limit then
    return 1   -- Allowed
else
    return 0   -- Rate limited
end
"""

def is_allowed(user_id: str, limit: int = 100, window: int = 60) -> bool:
    key = f"rate:{user_id}:{int(time.time() // window)}"
    result = r.eval(RATE_LIMITER, 1, key, limit, window)
    return bool(result)

# Distributed lock
ACQUIRE_LOCK = """
if redis.call('SET', KEYS[1], ARGV[1], 'NX', 'PX', ARGV[2]) then
    return 1
else
    return 0
end
"""

RELEASE_LOCK = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    redis.call('DEL', KEYS[1])
    return 1
else
    return 0
end
"""

import uuid

def with_lock(name: str, ttl_ms: int = 30000):
    lock_key = f"lock:{name}"
    lock_value = str(uuid.uuid4())   # Unique value to prevent releasing others' locks
    
    acquired = r.eval(ACQUIRE_LOCK, 1, lock_key, lock_value, ttl_ms)
    if not acquired:
        raise LockError(f"Could not acquire lock: {name}")
    
    try:
        yield
    finally:
        r.eval(RELEASE_LOCK, 1, lock_key, lock_value)
```

---

## 7. Cluster & High Availability

### Redis Cluster (Sharding)
```
16384 hash slots distributed across nodes:
  Node 1: slots 0-5460
  Node 2: slots 5461-10922
  Node 3: slots 10923-16383

Data placement:
  HASH_SLOT = CRC16(key) % 16384

{user}.name and {user}.age share same slot (hash tag {user})
```

```bash
# Create cluster
redis-cli --cluster create \
  node1:6379 node2:6379 node3:6379 \
  node1:6380 node2:6380 node3:6380 \   # 3 replicas
  --cluster-replicas 1

redis-cli --cluster info localhost:6379
redis-cli --cluster check localhost:6379

# Add node
redis-cli --cluster add-node new_node:6379 existing_node:6379

# Rebalance
redis-cli --cluster rebalance localhost:6379
```

### Redis Sentinel (High Availability)
```
Master ─── 3 Sentinels monitoring ─── Replica 1
                                     Replica 2

On master failure:
  1. Sentinels detect master down
  2. Quorum agrees (majority vote)
  3. New master elected from replicas
  4. Clients redirected to new master
```

```python
from redis.sentinel import Sentinel

sentinel = Sentinel([
    ('sentinel1', 26379),
    ('sentinel2', 26379),
    ('sentinel3', 26379),
], socket_timeout=0.1)

master = sentinel.master_for('mymaster', socket_timeout=0.1)
replica = sentinel.slave_for('mymaster', socket_timeout=0.1)

master.set('key', 'value')   # Write to master
replica.get('key')           # Read from replica
```

---

## 8. Memory Optimization

```bash
# Memory usage
INFO memory
MEMORY USAGE key              # Memory for specific key (in bytes)
MEMORY DOCTOR                 # Recommendations
DEBUG JMAP                    # Detailed memory breakdown

# Eviction policies (when maxmemory reached)
maxmemory 2gb
maxmemory-policy allkeys-lru  # Evict least recently used

# Policies:
# noeviction       — return error (default)
# allkeys-lru      — evict any key by LRU
# volatile-lru     — evict keys with TTL by LRU
# allkeys-lfu      — evict by least frequently used
# volatile-ttl     — evict keys with shortest TTL
# allkeys-random   — evict random key
```

### Compression Tips
```
# Small hashes/lists use ziplist/listpack (compact)
# Default thresholds (per redis.conf):
hash-max-listpack-entries 128   # Use ziplist if ≤128 fields
hash-max-listpack-value 64      # Use ziplist if field value ≤64 bytes

zset-max-listpack-entries 128
zset-max-listpack-value 64

# If your data is < these thresholds, Redis automatically uses compact encoding!

# Key naming: short keys save memory
# Bad:  session:user:12345 (23 bytes)
# Good: s:u:12345 (8 bytes)
# At millions of keys, this matters!
```

---

## 9. Monitoring Queries

```bash
# Real-time command monitoring
MONITOR   # Shows all commands (HIGH overhead — don't use in production!)

# Slow log
CONFIG SET slowlog-log-slower-than 10000  # Log commands >10ms
SLOWLOG GET 10                             # Last 10 slow commands
SLOWLOG LEN                                # Total count

# Stats
INFO server       # Server info
INFO stats        # Hit rates, connections
INFO replication  # Master/replica status
INFO keyspace     # Databases + key counts
INFO clients      # Connected clients

# Important metrics to monitor:
# - hit_rate = keyspace_hits / (keyspace_hits + keyspace_misses)
# - memory_used vs maxmemory
# - evicted_keys (should be near 0)
# - connected_clients
# - blocked_clients
# - rdb_last_bgsave_status
```

---

## 10. Useful Patterns

```python
import redis
from functools import wraps
import json
import hashlib

r = redis.Redis(decode_responses=True)

# Cache-aside decorator
def cache(ttl: int = 300, key_prefix: str = ""):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function + args
            cache_key = f"{key_prefix or func.__name__}:{hashlib.md5(str((args, kwargs)).encode()).hexdigest()}"
            
            # Check cache
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            r.setex(cache_key, ttl, json.dumps(result, default=str))
            
            return result
        return wrapper
    return decorator

@cache(ttl=60)
async def get_user_profile(user_id: int) -> dict:
    return await db.fetch_user(user_id)

# Leaderboard
def update_score(user_id: str, delta: float, leaderboard: str = "global"):
    r.zincrby(leaderboard, delta, user_id)

def get_top_users(n: int = 10, leaderboard: str = "global"):
    return r.zrevrange(leaderboard, 0, n-1, withscores=True)

def get_user_rank(user_id: str, leaderboard: str = "global"):
    rank = r.zrevrank(leaderboard, user_id)
    score = r.zscore(leaderboard, user_id)
    return {"rank": rank + 1 if rank is not None else None, "score": score}
```

---

*Tài liệu liên quan: `nosql/01-nosql-basics.md` | `caching/01-caching-strategies.md` | `backend/realtime/02-redis-pubsub.md`*
