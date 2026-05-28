# ⚡ Python Performance — Tối ưu hiệu năng Python

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `02-python-advanced.md`

---

## 1. Profiling — Đo trước khi optimize

```python
# cProfile — CPU profiling
python -m cProfile -s cumulative my_script.py

# line_profiler — từng dòng
pip install line_profiler
@profile  # Decorator
def slow_function():
    ...
kernprof -l -v my_script.py

# memory_profiler
pip install memory-profiler
@profile
def memory_heavy():
    big_list = [i for i in range(10**7)]
python -m memory_profiler my_script.py

# timeit — micro-benchmarks
import timeit
timeit.timeit('sum(range(1000))', number=10000)
```

> **"Premature optimization is the root of all evil"** — Donald Knuth. Đo TRƯỚC, optimize SAU.

---

## 2. Common Optimizations

```python
# ── List comprehension > loop ──
# ❌ Slow
result = []
for i in range(1000000):
    result.append(i * 2)

# ✅ 2-3x faster
result = [i * 2 for i in range(1000000)]

# ── Generator for large data ──
# ❌ Load tất cả vào memory
data = [process(x) for x in huge_list]  # Memory: O(n)

# ✅ Lazy evaluation
data = (process(x) for x in huge_list)  # Memory: O(1)

# ── dict/set lookup > list ──
# ❌ O(n) per lookup
if item in large_list: ...

# ✅ O(1) per lookup
item_set = set(large_list)
if item in item_set: ...

# ── Use built-in functions ──
# ❌
total = 0
for x in numbers:
    total += x

# ✅ C-level implementation
total = sum(numbers)

# ── String concatenation ──
# ❌ O(n²) with += 
result = ""
for s in strings:
    result += s

# ✅ O(n) with join
result = "".join(strings)
```

---

## 3. Concurrency & Parallelism

```python
# ── asyncio — I/O-bound (network, disk) ──
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)

# ── ThreadPool — I/O-bound (legacy sync code) ──
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as pool:
    results = pool.map(fetch_url, urls)

# ── ProcessPool — CPU-bound ──
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as pool:
    results = pool.map(heavy_computation, data_chunks)

# ── GIL: chỉ 1 thread chạy Python code cùng lúc ──
# Threads: tốt cho I/O-bound (GIL released during I/O)
# Processes: tốt cho CPU-bound (separate GIL per process)
```

---

## 4. C Extensions & Cython

```python
# NumPy — vectorized operations (C-level)
import numpy as np
# ❌ Python loop: 10 seconds
result = [x**2 for x in range(10**7)]
# ✅ NumPy: 0.1 seconds (100x faster)
result = np.arange(10**7) ** 2

# Cython — compile Python to C
# my_module.pyx
def fast_sum(int n):
    cdef int i, total = 0
    for i in range(n):
        total += i
    return total
```

---

## 5. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n):
    # Only computed once per unique n
    return sum(i**2 for i in range(n))

# Redis caching for web apps
import redis
cache = redis.Redis()

def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = db.query(User).get(user_id)
    cache.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

---

## Gotchas

| ❌ Sai | ✅ Đúng |
|--------|---------|
| Optimize without profiling | Profile first, optimize bottlenecks |
| `for` loop with NumPy arrays | Use vectorized operations |
| Threads for CPU-bound | Use `ProcessPoolExecutor` |
| Cache without expiration | Set TTL for cached data |

---

## Tài nguyên

- [High Performance Python (Gorelick)](https://www.oreilly.com/library/view/high-performance-python/9781492055013/) — Best book
- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips) — Official wiki
- [Scalene (profiler)](https://github.com/plasma-umass/scalene) — Modern CPU+Memory profiler
