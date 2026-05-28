# #️⃣ Hash Tables — Bảng băm

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Cấu trúc dữ liệu nhanh nhất cho lookup

---

## Tại sao Hash Table quan trọng?

| Thao tác | Array | Linked List | BST | **Hash Table** |
|---|---|---|---|---|
| Search | O(n) | O(n) | O(log n) | **O(1)** ⚡ |
| Insert | O(n) | O(1) | O(log n) | **O(1)** ⚡ |
| Delete | O(n) | O(n) | O(log n) | **O(1)** ⚡ |

> Hash Table = **Cấu trúc dữ liệu nhanh nhất** cho thao tác CRUD.  
> Python `dict`, JavaScript `Object`/`Map`, Java `HashMap` — đều là hash table.

---

## 1. Cách hoạt động

```
Key "name" ──► [Hash Function] ──► Index 3 ──► Lưu vào bucket[3]

            Hash Function
"name"  →  hash("name") % 8  →  3   →  bucket[3] = "An"
"age"   →  hash("age") % 8   →  7   →  bucket[7] = 25
"email" →  hash("email") % 8 →  1   →  bucket[1] = "an@mail.com"

Buckets:
[0] → empty
[1] → ("email", "an@mail.com")
[2] → empty
[3] → ("name", "An")
[4] → empty
[5] → empty
[6] → empty
[7] → ("age", 25)
```

**Hash Function:** Chuyển key (bất kỳ kiểu) thành số nguyên (index):
- Cùng key → **luôn cùng hash** (deterministic)
- Khác key → **nên khác hash** (ít collision)
- Tính toán **nhanh** — O(1)

---

## 2. Xử lý Collision — Khi 2 key cùng hash

### Chaining (Chuỗi liên kết)

```
Hash("cat") = 2
Hash("dog") = 2   ← Collision!

Bucket[2] → ("cat", "meo") → ("dog", "gâu") → null
              Linked List xử lý collision
```

```python
class HashTable:
    def __init__(self, size=8):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update
                return
        bucket.append((key, value))       # Insert

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
        raise KeyError(key)

# Sử dụng
ht = HashTable()
ht.put("name", "An")
ht.put("age", 25)
print(ht.get("name"))  # "An"
```

### Open Addressing (Địa chỉ mở)

Khi collision → tìm slot trống tiếp theo:

```
Hash("cat") = 2 → bucket[2] đã có → thử bucket[3] → trống → lưu!

Linear Probing:    index + 1, +2, +3...
Quadratic Probing: index + 1², +2², +3²...
Double Hashing:    index + i × hash2(key)
```

---

## 3. Load Factor & Resizing

```
Load Factor = Số phần tử / Số buckets

Load Factor < 0.75 → OK, ít collision
Load Factor ≥ 0.75 → RESIZE! (thường gấp đôi)

Resize: Tạo bảng mới lớn hơn → rehash tất cả phần tử
→ O(n) nhưng hiếm khi xảy ra → Amortized O(1)
```

---

## 4. Ứng dụng thực tế

### Đếm tần suất

```python
def count_frequency(text):
    freq = {}
    for word in text.split():
        freq[word] = freq.get(word, 0) + 1
    return freq

count_frequency("hello world hello python hello")
# {'hello': 3, 'world': 1, 'python': 1}
```

### Two Sum (Bài kinh điển)

```python
def two_sum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

two_sum([2, 7, 11, 15], 9)  # [0, 1] → 2 + 7 = 9
```

### Kiểm tra anagram

```python
from collections import Counter

def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)

is_anagram("listen", "silent")  # True
is_anagram("hello", "world")    # False
```

### Cache / Memoization

```python
def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(100)  # Instant! (không memo: hàng tỷ năm)
```

---

## 5. Set — Hash Table chỉ có key

```python
# Set = Hash Table không có value
colors = {"red", "green", "blue"}

"red" in colors      # O(1) ⚡ — so với list O(n)!
colors.add("yellow")
colors.remove("red")

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a & b    # {3, 4}     — Intersection (giao)
a | b    # {1,2,3,4,5,6} — Union (hợp)
a - b    # {1, 2}     — Difference (hiệu)
a ^ b    # {1, 2, 5, 6} — Symmetric Difference
```

**Ứng dụng Set:** Loại bỏ duplicate, kiểm tra membership, tìm phần tử chung.

---

## So sánh implementations

| Ngôn ngữ | Hash Table | Ordered Map |
|---|---|---|
| **Python** | `dict` (ordered 3.7+) | — |
| **JavaScript** | `Map`, `Object` | `Map` (insertion order) |
| **Java** | `HashMap` | `TreeMap` (sorted) |
| **Go** | `map` | — |
| **C++** | `unordered_map` | `map` (Red-Black Tree) |

---

## Các lỗi thường gặp

```
❌ Sai: Dùng mutable object làm key (list, dict)
✅ Đúng: Key phải immutable (string, number, tuple)

❌ Sai: Assume dict luôn ordered
✅ Đúng: Python 3.7+ ordered, nhưng Java HashMap thì KHÔNG

❌ Sai: "Hash Table luôn O(1)"
✅ Đúng: Worst case O(n) khi tất cả key collision → dùng good hash function
```

---

## Bài tập thực hành

- [ ] Implement Hash Table từ đầu (put, get, delete, resize)
- [ ] Two Sum, Three Sum dùng hash table
- [ ] Tìm ký tự xuất hiện đầu tiên không lặp lại trong string
- [ ] Group Anagrams: ["eat","tea","tan","ate","nat","bat"] → [["eat","tea","ate"],["tan","nat"],["bat"]]

---

## Tài nguyên thêm

- [Visualgo — Hash Table](https://visualgo.net/en/hashtable) — Trực quan hóa
- [Hash Table Wikipedia](https://en.wikipedia.org/wiki/Hash_table) — Chi tiết kỹ thuật
