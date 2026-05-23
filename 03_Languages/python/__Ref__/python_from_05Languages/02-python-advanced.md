# Python Advanced

> **Tags:** `python` `decorators` `generators` `asyncio` `metaclasses` `type-hints`
> **Level:** Advanced | **Prerequisite:** `python/01-python-basics.md`

---

## 1. Decorators

Decorator = function nhận function, trả về function (higher-order function).

```python
from functools import wraps
import time

# Basic decorator
def timer(func):
    @wraps(func)  # Giữ nguyên __name__, __doc__ của func gốc
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function(n: int) -> int:
    return sum(range(n))

# Equivalent to: slow_function = timer(slow_function)
```

### Decorator với arguments (Decorator factory)
```python
def retry(max_attempts: int = 3, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying...")
        return wrapper
    return decorator

@retry(max_attempts=3, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url: str) -> dict:
    return requests.get(url).json()
```

### Class-based decorator
```python
class cache:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        wraps(func)(self)  # Copy metadata

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Common built-in decorators
```python
class MyClass:
    class_var = 0

    @classmethod
    def create_from_string(cls, data: str) -> 'MyClass':
        # Nhận class thay vì instance — factory method
        instance = cls()
        return instance

    @staticmethod
    def validate(data: str) -> bool:
        # Không nhận self hay cls — utility function
        return bool(data.strip())

    @property
    def computed(self) -> int:
        return self.class_var * 2

    @computed.setter
    def computed(self, value: int):
        self.class_var = value // 2
```

---

## 2. Generators & yield

Generator = lazy sequence, tính từng giá trị khi cần (không load tất cả vào memory):

```python
# Generator function
def fibonacci():
    a, b = 0, 1
    while True:
        yield a     # Pause, return a, save state
        a, b = b, a + b

# Usage
fib = fibonacci()
print([next(fib) for _ in range(10)])  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Generator expression (lazy list comprehension)
squares = (x**2 for x in range(1_000_000))  # Không tính ngay, chỉ tạo generator
first_ten = list(itertools.islice(squares, 10))

# Đọc file lớn mà không load hết vào memory
def read_chunks(filename: str, chunk_size: int = 8192):
    with open(filename, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk

for chunk in read_chunks('bigfile.bin'):
    process(chunk)
```

### yield from — delegate to sub-generator
```python
def chain(*iterables):
    for iterable in iterables:
        yield from iterable   # yield from delegates iteration

result = list(chain([1, 2], [3, 4], [5, 6]))  # [1, 2, 3, 4, 5, 6]

# Recursive generator
def flatten(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4], 5], 6]))  # [1, 2, 3, 4, 5, 6]
```

### send() — two-way communication với generator
```python
def accumulator():
    total = 0
    while True:
        value = yield total    # yield vừa gửi vừa nhận
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)          # Prime the generator (advance to first yield)
acc.send(10)       # 10
acc.send(20)       # 30
acc.send(5)        # 35
```

---

## 3. Context Managers

```python
from contextlib import contextmanager, asynccontextmanager

# Class-based
class DatabaseConnection:
    def __enter__(self):
        self.conn = create_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        # Return True để suppress exception, False để re-raise
        return False

with DatabaseConnection() as conn:
    conn.execute("SELECT 1")

# Decorator-based (simpler!)
@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield   # Code trong `with` block chạy ở đây
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.3f}s")

with timer("database query"):
    results = db.execute(complex_query)

# Async context manager
@asynccontextmanager
async def managed_client(url: str):
    client = aiohttp.ClientSession()
    try:
        yield client
    finally:
        await client.close()

async def fetch():
    async with managed_client("https://api.example.com") as client:
        response = await client.get("/data")
```

---

## 4. Metaclasses

Metaclass = "class của class". Mọi class trong Python là instance của `type`.

```python
# type() là metaclass mặc định
MyClass = type('MyClass', (BaseClass,), {'attr': 42, 'method': lambda self: None})

# Tạo metaclass custom
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabasePool(metaclass=Singleton):
    def __init__(self):
        self.connections = []

pool1 = DatabasePool()
pool2 = DatabasePool()
assert pool1 is pool2  # True — same instance

# Practical: Auto-register subclasses
class PluginMeta(type):
    registry = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if bases:  # Not the base class itself
            PluginMeta.registry[name] = cls

class Plugin(metaclass=PluginMeta):
    pass

class JSONPlugin(Plugin):
    def parse(self, data): ...

class XMLPlugin(Plugin):
    def parse(self, data): ...

# Plugins auto-registered:
PluginMeta.registry  # {'JSONPlugin': JSONPlugin, 'XMLPlugin': XMLPlugin}
```

---

## 5. Type Hints & Annotations

```python
from typing import Optional, Union, Any, TypeVar, Generic, Protocol
from typing import Sequence, Mapping, Callable, Iterator, Generator
from collections.abc import Awaitable

# Basic
def greet(name: str) -> str:
    return f"Hello, {name}"

# Optional — có thể None
def find_user(user_id: int) -> Optional[User]:
    return db.get(user_id)  # Could be None

# Union — nhiều types
def process(data: Union[str, bytes, dict]) -> None: ...
def process(data: str | bytes | dict) -> None: ...  # Python 3.10+

# TypeVar — generic
T = TypeVar('T')

def first(lst: list[T]) -> T:
    return lst[0]

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

stack: Stack[int] = Stack()
stack.push(1)   # OK
stack.push("x") # Type error!

# Protocol — structural typing (duck typing với types)
class Drawable(Protocol):
    def draw(self) -> None: ...
    def resize(self, scale: float) -> None: ...

class Circle:
    def draw(self) -> None: print("Drawing circle")
    def resize(self, scale: float) -> None: self.radius *= scale

def render(shape: Drawable) -> None:  # Circle satisfies Drawable without inheriting!
    shape.draw()

# Callable
def apply(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)

# TypedDict
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    age: int
    email: str | None

def create_user(data: UserDict) -> User: ...
```

### Dataclasses
```python
from dataclasses import dataclass, field, KW_ONLY

@dataclass(frozen=True)   # Immutable (hashable)
class Point:
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

@dataclass
class User:
    name: str
    email: str
    _: KW_ONLY               # Following fields are keyword-only
    age: int = 0
    tags: list[str] = field(default_factory=list)  # Mutable default!

    def __post_init__(self):
        self.email = self.email.lower()
```

---

## 6. asyncio Deep Dive

```python
import asyncio
from typing import AsyncIterator

# Async generator
async def paginate(url: str, page_size: int = 100) -> AsyncIterator[list[dict]]:
    page = 1
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url, params={"page": page, "size": page_size}) as resp:
                data = await resp.json()
                if not data:
                    return
                yield data
                page += 1

async def main():
    async for page in paginate("https://api.example.com/users"):
        for user in page:
            process(user)

# Task management
async def fetch_all(urls: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch(session, url), name=url)
            for url in urls
        ]

        # gather: run all, return all results
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Xử lý cả successes và failures
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                print(f"Error for {url}: {result}")
            else:
                print(f"Success for {url}: {len(result)} bytes")
        
        return [r for r in results if not isinstance(r, Exception)]

# Timeout
async def with_timeout(coro, seconds: float):
    try:
        return await asyncio.wait_for(coro, timeout=seconds)
    except asyncio.TimeoutError:
        print("Operation timed out")
        raise

# Semaphore — limit concurrent requests
async def rate_limited_fetch(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_limit(url: str) -> str:
        async with semaphore:  # Only max_concurrent at a time
            return await fetch(url)
    
    return await asyncio.gather(*[fetch_with_limit(url) for url in urls])
```

---

## 7. Python Memory Model & GIL

### Global Interpreter Lock (GIL)
```
CPython GIL: chỉ 1 thread Python chạy bytecode tại 1 thời điểm

Implications:
  - CPU-bound threading: NO speedup (GIL prevents true parallelism)
  - I/O-bound threading: OK (GIL released during I/O)
  - asyncio (single-threaded): OK for I/O
  - multiprocessing: OK for CPU (separate Python interpreters)

Python 3.12: "no-GIL" build (experimental, per-interpreter GIL)
Python 3.13+: free-threaded mode (--disable-gil)
```

### Memory model
```python
# Everything is an object
x = 42          # x is just a name pointing to int object 42
y = x           # y also points to SAME object
y = 43          # y now points to new object 43, x still 42

# Mutable vs Immutable
a = [1, 2, 3]   # list is mutable
b = a            # b points to SAME list
b.append(4)      # Modifies the list — a is also [1, 2, 3, 4]!
b = [5, 6]       # b now points to NEW list — a unchanged

# id() reveals object identity
print(id(a) == id(b))   # False after b = [5, 6]
```

---

## 8. Advanced Patterns

### Descriptor Protocol
```python
class Validated:
    """Descriptor that validates value on set"""
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be numeric")
        if value < 0:
            raise ValueError(f"{self.name} must be non-negative")
        setattr(obj, self.private_name, value)

class Circle:
    radius = Validated()
    
    def __init__(self, radius: float):
        self.radius = radius  # Triggers __set__

c = Circle(5)    # OK
c = Circle(-1)   # ValueError!
c = Circle("x")  # TypeError!
```

### `__slots__`
```python
# Thay dict bằng fixed set of attributes → tiết kiệm memory ~40%
class Point:
    __slots__ = ('x', 'y')    # No __dict__!
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Cannot add new attributes:
p = Point(1, 2)
p.z = 3   # AttributeError!
```

---

## 9. Useful Standard Library

```python
# itertools — lazy iteration
from itertools import (
    chain,           # chain([1,2], [3,4]) → [1,2,3,4]
    islice,          # Take first N from any iterable
    groupby,         # Group consecutive elements
    combinations,    # Combinations without replacement
    permutations,    # All permutations
    product,         # Cartesian product
    accumulate,      # Running totals
    cycle,           # Infinite cycle
    repeat,          # Repeat element N times
)

# functools
from functools import (
    lru_cache,       # Memoization with LRU eviction
    cache,           # Unbounded memoization (Python 3.9+)
    partial,         # Partial function application
    reduce,          # fold left
    singledispatch,  # Function overloading by type
)

@lru_cache(maxsize=128)
def expensive(n: int) -> int:
    return n * n

# collections
from collections import (
    defaultdict,   # dict with default factory
    Counter,       # Counting hashables
    deque,         # O(1) append/pop from both ends
    namedtuple,    # Tuple with names
    OrderedDict,   # Dict that remembers insertion order (less needed in 3.7+)
    ChainMap,      # Multiple dicts as one view
)

word_count = Counter("hello world hello".split())
# Counter({'hello': 2, 'world': 1})
word_count.most_common(1)  # [('hello', 2)]
```

---

## 10. Bài tập

1. **Decorator chain**: Viết `@retry(3)` + `@timeout(5)` + `@log_calls` decorators, stack chúng lại.
2. **Infinite generator**: Viết generator trả về số nguyên tố vô hạn (prime sieve).
3. **Async pipeline**: Tạo async pipeline: producer tạo URLs → fetcher lấy HTML → parser extract links → saver ghi vào file.
4. **Metaclass registry**: Tạo plugin system với metaclass auto-registration.
5. **Memory comparison**: Tạo 1 triệu Point objects với và không có `__slots__`. So sánh memory dùng `tracemalloc`.

---

*Tài liệu liên quan: `python/01-python-basics.md` | `python/05-python-performance.md` | `programming/03-async-programming.md`*
