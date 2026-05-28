# Caching Strategies

> **Tags:** `caching` `redis` `cache-aside` `write-through` `distributed-cache` `ttl` `cdn`
> **Level:** Intermediate | **Prerequisite:** `nosql/02-redis.md`

---

## 1. Why Cache?

```
Latency by layer (2024 numbers):
  L1 cache    ~0.5 ns
  L2 cache    ~7 ns
  RAM         ~100 ns
  Redis (LAN) ~0.1-1 ms
  DB query    ~5-20 ms    ← Cache here!
  Disk I/O    ~10 ms
  Network API ~100-500 ms ← Cache here too!

Cache goal: serve from fast layer, avoid slow layer
```

---

## 2. Cache Patterns

### Cache-Aside (Lazy Loading) — Most Common
```python
async def get_user(user_id: int) -> User:
    cache_key = f"user:{user_id}"
    
    # 1. Check cache
    cached = await redis.get(cache_key)
    if cached:
        return User.model_validate_json(cached)
    
    # 2. Cache MISS — fetch from DB
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    if not user:
        return None
    
    # 3. Populate cache
    await redis.setex(cache_key, 3600, user.model_dump_json())  # TTL 1 hour
    
    return user

async def update_user(user_id: int, data: dict) -> User:
    user = await db.update_user(user_id, data)
    
    # Invalidate cache (not update — avoids cache/DB races)
    await redis.delete(f"user:{user_id}")
    
    return user

# Pros: only cache what's needed, resilient to cache failure
# Cons: cache miss penalty, data can be stale (up to TTL)
```

### Read-Through
```python
# Cache handles loading automatically — app always reads from cache
class UserCache:
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis
    
    async def get(self, user_id: int) -> User | None:
        key = f"user:{user_id}"
        
        if data := await self.redis.get(key):
            return User.model_validate_json(data)
        
        # Auto-load from source
        user = await self.db.find_user(user_id)
        if user:
            await self.redis.setex(key, 3600, user.model_dump_json())
        
        return user

# Pros: consistent pattern, app code simpler
# Cons: cache must be warm, first request always misses
```

### Write-Through
```python
async def save_user(user: User) -> User:
    # Write to DB
    saved = await db.save_user(user)
    
    # Write to cache SIMULTANEOUSLY
    await redis.setex(f"user:{saved.id}", 3600, saved.model_dump_json())
    
    return saved

# Pros: cache always consistent, no stale reads
# Cons: write latency increases (must wait for both DB + cache)
#       wastes cache space for rarely-read data
```

### Write-Behind (Write-Back) — Risky!
```python
async def save_user(user: User):
    # Write to cache ONLY
    await redis.setex(f"user:{user.id}", 300, user.model_dump_json())
    
    # Queue for async DB write
    await queue.enqueue('sync_user_to_db', user.id)

# Celery/BullMQ worker flushes to DB eventually:
@celery_app.task
def sync_user_to_db(user_id: int):
    user_data = redis.get(f"user:{user_id}")
    db.save_user(User.model_validate_json(user_data))

# Pros: fastest writes (write to fast cache, not slow DB)
# Cons: data loss risk if cache fails before DB sync!
#       complex recovery, hard to debug
```

---

## 3. Redis Caching Patterns

```python
from redis.asyncio import Redis
import json
from functools import wraps

redis = Redis(host='localhost', port=6379, decode_responses=True)

# Decorator-based caching
def cached(key_fn, ttl=3600):
    """Cache decorator — key_fn builds cache key from args"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = key_fn(*args, **kwargs)
            
            if cached_data := await redis.get(cache_key):
                return json.loads(cached_data)
            
            result = await func(*args, **kwargs)
            
            if result is not None:
                await redis.setex(cache_key, ttl, json.dumps(result, default=str))
            
            return result
        
        # Expose cache invalidation
        wrapper.invalidate = lambda *args, **kwargs: redis.delete(key_fn(*args, **kwargs))
        return wrapper
    return decorator

@cached(key_fn=lambda user_id: f"user:{user_id}", ttl=1800)
async def get_user(user_id: int) -> dict:
    return await db.fetch_one("SELECT * FROM users WHERE id = $1", user_id)

# Invalidate
await get_user.invalidate(123)

# Cache stampede prevention (only one request refreshes)
import asyncio

refresh_locks = {}

async def get_with_lock(cache_key: str, fetch_fn, ttl: int):
    """Prevent cache stampede: only 1 coroutine refreshes at a time"""
    if data := await redis.get(cache_key):
        return json.loads(data)
    
    # Already being refreshed?
    if cache_key in refresh_locks:
        await asyncio.wait_for(refresh_locks[cache_key].wait(), timeout=5)
        return json.loads(await redis.get(cache_key))
    
    # Acquire refresh lock
    event = asyncio.Event()
    refresh_locks[cache_key] = event
    
    try:
        result = await fetch_fn()
        await redis.setex(cache_key, ttl, json.dumps(result, default=str))
        return result
    finally:
        event.set()
        del refresh_locks[cache_key]
```

### Distributed Lock (Redlock)
```python
import time
import uuid

class DistributedLock:
    def __init__(self, redis: Redis, key: str, ttl_seconds: int = 30):
        self.redis = redis
        self.key = f"lock:{key}"
        self.ttl = ttl_seconds
        self.lock_id = str(uuid.uuid4())
    
    async def acquire(self, timeout: int = 10) -> bool:
        deadline = time.time() + timeout
        
        while time.time() < deadline:
            # SET key value NX EX ttl — atomic acquire
            acquired = await self.redis.set(
                self.key, self.lock_id,
                nx=True,      # Only set if not exists
                ex=self.ttl,  # Auto-expire to prevent deadlocks
            )
            if acquired:
                return True
            
            await asyncio.sleep(0.05)
        
        return False
    
    async def release(self):
        # Lua script ensures we only delete OUR lock (atomic)
        lua_script = """
        if redis.call('GET', KEYS[1]) == ARGV[1] then
            return redis.call('DEL', KEYS[1])
        else
            return 0
        end
        """
        await self.redis.eval(lua_script, 1, self.key, self.lock_id)
    
    async def __aenter__(self):
        if not await self.acquire():
            raise TimeoutError(f"Could not acquire lock: {self.key}")
        return self
    
    async def __aexit__(self, *args):
        await self.release()

# Usage
async def process_order(order_id: str):
    async with DistributedLock(redis, f"order:{order_id}", ttl_seconds=60):
        # Critical section — only one instance can run this
        order = await fetch_order(order_id)
        await process(order)
        await save(order)
```

### Rate Limiting with Redis
```python
async def is_rate_limited(identifier: str, limit: int, window_seconds: int) -> tuple[bool, dict]:
    """Sliding window rate limiter"""
    now = time.time()
    window_start = now - window_seconds
    key = f"rate:{identifier}"
    
    # Remove old timestamps
    await redis.zremrangebyscore(key, '-inf', window_start)
    
    # Count requests in window
    request_count = await redis.zcard(key)
    
    if request_count >= limit:
        oldest = await redis.zrange(key, 0, 0, withscores=True)
        retry_after = int(oldest[0][1] + window_seconds - now) if oldest else window_seconds
        return True, {'limit': limit, 'remaining': 0, 'retry_after': retry_after}
    
    # Record this request
    await redis.zadd(key, {str(uuid.uuid4()): now})
    await redis.expire(key, window_seconds + 1)
    
    return False, {'limit': limit, 'remaining': limit - request_count - 1, 'retry_after': 0}

# FastAPI middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    identifier = f"{request.client.host}:{request.url.path}"
    
    limited, info = await is_rate_limited(identifier, limit=100, window_seconds=60)
    
    if limited:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
            headers={
                "X-RateLimit-Limit": str(info['limit']),
                "X-RateLimit-Remaining": str(info['remaining']),
                "Retry-After": str(info['retry_after']),
            }
        )
    
    response = await call_next(request)
    response.headers["X-RateLimit-Remaining"] = str(info['remaining'])
    return response
```

---

## 4. Cache Invalidation Strategies

```python
# Strategy 1: TTL-based (simplest, some staleness acceptable)
await redis.setex("product:123", ttl=300, value=product_json)

# Strategy 2: Event-driven invalidation (on writes)
async def update_product(product_id: int, data: dict):
    product = await db.update_product(product_id, data)
    
    # Invalidate all related cache keys
    await redis.delete(
        f"product:{product_id}",
        f"category:{product.category_id}:products",
        f"search:*",    # Pattern delete (expensive!)
    )
    
    # Or use Redis SCAN for pattern delete (safe for production)
    async for key in redis.scan_iter(f"search:*"):
        await redis.delete(key)
    
    return product

# Strategy 3: Cache tags (group related keys)
class TaggedCache:
    async def set(self, key: str, value, tags: list[str], ttl: int = 3600):
        await redis.setex(key, ttl, value)
        
        # Store key in each tag set
        for tag in tags:
            await redis.sadd(f"tag:{tag}", key)
            await redis.expire(f"tag:{tag}", ttl)
    
    async def invalidate_by_tag(self, tag: str):
        tag_key = f"tag:{tag}"
        keys = await redis.smembers(tag_key)
        
        if keys:
            # Delete all keys with this tag
            await redis.delete(*keys)
        
        # Delete tag set itself
        await redis.delete(tag_key)

cache = TaggedCache()

# Cache product with tags
await cache.set(
    key=f"product:{product_id}",
    value=product_json,
    tags=[f"category:{product.category_id}", f"brand:{product.brand_id}"],
    ttl=3600
)

# Invalidate all products in category 5:
await cache.invalidate_by_tag("category:5")

# Strategy 4: Versioning (cache key includes version)
async def get_product_v(product_id: int) -> dict:
    version = await redis.get(f"product:{product_id}:version") or "0"
    cache_key = f"product:{product_id}:v{version}"
    
    if data := await redis.get(cache_key):
        return json.loads(data)
    
    product = await db.get_product(product_id)
    await redis.setex(cache_key, 3600, json.dumps(product))
    return product

async def invalidate_product_version(product_id: int):
    # Increment version — old cached keys become stale and expire naturally
    await redis.incr(f"product:{product_id}:version")
```

---

## 5. CDN Caching

```nginx
# Nginx cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g;

server {
  location /api/products {
    proxy_pass http://backend;
    proxy_cache api_cache;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    proxy_cache_valid 200 5m;     # Cache 200 responses for 5 minutes
    proxy_cache_valid 404 1m;     # Cache 404 for 1 minute
    
    # Stale while revalidate
    proxy_cache_use_stale error timeout updating http_500;
    proxy_cache_background_update on;
    
    add_header X-Cache-Status $upstream_cache_status;  # HIT/MISS/BYPASS
  }
  
  location /api/user {
    # Don't cache authenticated endpoints
    proxy_no_cache $http_authorization;
    proxy_cache_bypass $http_authorization;
  }
}
```

```python
# Cache-Control headers (browser + CDN)
from fastapi import Response

@app.get("/api/products")
async def get_products(response: Response):
    products = await product_service.get_all()
    
    response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=60"
    # max-age: cache for 5 minutes
    # stale-while-revalidate: serve stale for 1 min while fetching fresh
    
    return products

@app.get("/api/user/profile")
async def get_profile(response: Response, current_user = Depends(get_current_user)):
    response.headers["Cache-Control"] = "private, no-store"  # Never cache!
    return current_user

# Cache busting via ETag
@app.get("/api/products/{product_id}")
async def get_product(product_id: int, request: Request, response: Response):
    product = await db.get_product(product_id)
    
    etag = f'"{hashlib.md5(str(product.updated_at).encode()).hexdigest()}"'
    
    if request.headers.get("If-None-Match") == etag:
        return Response(status_code=304)  # Not Modified
    
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=60"
    return product
```

---

## 6. Cache Metrics to Monitor

```python
# Track cache performance
class CacheStats:
    def __init__(self, redis: Redis):
        self.redis = redis
    
    async def record_hit(self, cache_type: str):
        await self.redis.incr(f"cache:hits:{cache_type}")
    
    async def record_miss(self, cache_type: str):
        await self.redis.incr(f"cache:misses:{cache_type}")
    
    async def get_hit_rate(self, cache_type: str) -> float:
        hits = int(await self.redis.get(f"cache:hits:{cache_type}") or 0)
        misses = int(await self.redis.get(f"cache:misses:{cache_type}") or 0)
        total = hits + misses
        return hits / total if total else 0

# Redis INFO stats
redis_info = await redis.info('stats')
keyspace_hits = redis_info['keyspace_hits']
keyspace_misses = redis_info['keyspace_misses']
hit_rate = keyspace_hits / (keyspace_hits + keyspace_misses) * 100
print(f"Cache hit rate: {hit_rate:.1f}%")

# Target hit rates:
# > 90% — excellent
# 80-90% — good
# < 80% — investigate why so many misses
# Memory usage + eviction rate
memory_info = await redis.info('memory')
used_memory = memory_info['used_memory_human']
evicted_keys = (await redis.info('stats'))['evicted_keys']
```

---

*Tài liệu liên quan: `nosql/02-redis.md` | `nosql/02-redis-deep-dive.md` | `system-design/01-system-design.md`*
