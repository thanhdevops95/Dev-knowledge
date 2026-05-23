# 📋 Python Cheatsheet — Tra cứu nhanh

> `[BEGINNER → ADVANCED]` — Bảng tổng hợp cú pháp và patterns Python thường dùng.

---

## Data Types & Structures

```python
# ── Strings ──
s = "Hello World"
s.upper(); s.lower(); s.strip(); s.split()
s.replace("World", "Python")
f"Name: {name}, Age: {age}"          # f-string ⭐
f"{price:.2f}"; f"{num:,}"; f"{pct:.1%}"  # Formatting

# ── Lists ──
lst = [1, 2, 3]
lst.append(4); lst.extend([5,6]); lst.insert(0, 0)
lst.pop(); lst.remove(3); lst.sort(reverse=True)
lst[1:3]; lst[::2]; lst[::-1]        # Slicing
[x**2 for x in range(10) if x%2==0]  # Comprehension ⭐

# ── Dicts ──
d = {"a": 1, "b": 2}
d.get("c", 0)                        # Default value
d.setdefault("c", 3)                 # Set if not exists
d | {"d": 4}                         # Merge (3.9+)
{k: v for k, v in items if v > 0}   # Dict comprehension

# ── Sets ──
s = {1, 2, 3}
s & {2, 3, 4}  # Intersection: {2, 3}
s | {4, 5}     # Union: {1, 2, 3, 4, 5}
s - {2, 3}     # Difference: {1}

# ── Tuples ── (immutable)
t = (1, 2, 3)
a, b, c = t    # Unpacking
a, *rest = t   # a=1, rest=[2,3]
```

## Functions

```python
# ── Args & Kwargs ──
def func(a, b=10, *args, **kwargs): ...
func(1, 2, 3, 4, key="val")

# ── Lambda ──
square = lambda x: x**2
sorted(users, key=lambda u: u.age)

# ── Decorators ──
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time()-start:.3f}s")
        return result
    return wrapper

@timer
def slow_func(): ...

# ── Generators ──
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# ── Type Hints (3.10+) ──
def greet(name: str, times: int = 1) -> str: ...
items: list[int] = [1, 2, 3]
data: dict[str, int | None] = {"a": 1, "b": None}
```

## Classes

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int = 0
    
    @property
    def is_adult(self) -> bool:
        return self.age >= 18

# ── Dunder methods ──
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return f"Vector({self.x}, {self.y})"
    def __add__(self, other): return Vector(self.x+other.x, self.y+other.y)
    def __eq__(self, other): return self.x==other.x and self.y==other.y
    def __len__(self): return int((self.x**2 + self.y**2)**0.5)
```

## File I/O

```python
# Read/Write
with open("file.txt", "r") as f:
    content = f.read()          # Entire file
    lines = f.readlines()       # List of lines

with open("file.txt", "w") as f:
    f.write("Hello\n")

# JSON
import json
data = json.loads(json_string)
json_string = json.dumps(data, indent=2, ensure_ascii=False)

# CSV
import csv
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"])

# Path (modern file handling)
from pathlib import Path
p = Path("data") / "file.txt"
p.read_text(); p.write_text("content")
p.exists(); p.is_file(); p.suffix; p.stem
list(Path(".").glob("**/*.py"))
```

## Error Handling

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except (TypeError, KeyError):
    logger.error("Type or key error")
except Exception as e:
    logger.exception("Unexpected error")
    raise
else:
    print("Success!")       # No exception
finally:
    cleanup()               # Always runs
```

## Common Patterns

```python
# ── Context Manager ──
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.time()
    yield
    print(f"{label}: {time.time()-start:.3f}s")

with timer("process"):
    heavy_work()

# ── Enum ──
from enum import Enum, auto
class Status(Enum):
    PENDING = auto()
    ACTIVE = auto()
    DELETED = auto()

# ── Counter, defaultdict ──
from collections import Counter, defaultdict
c = Counter("abracadabra")        # {'a': 5, 'b': 2, ...}
d = defaultdict(list)
d["key"].append("value")          # No KeyError!

# ── walrus operator (:=) ──
if (n := len(data)) > 100:
    print(f"Large dataset: {n} items")
```

## Useful One-liners

```python
# Flatten nested list
flat = [x for sublist in nested for x in sublist]

# Transpose matrix
transposed = list(zip(*matrix))

# Group by
from itertools import groupby
groups = {k: list(v) for k, v in groupby(sorted_data, key=func)}

# Chunk list
chunks = [lst[i:i+n] for i in range(0, len(lst), n)]

# Remove duplicates (preserve order)
unique = list(dict.fromkeys(lst))
```
