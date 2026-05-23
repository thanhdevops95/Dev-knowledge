# 🔢 Bit Manipulation — Thao tác trên bit

> `[INTERMEDIATE]` — Prerequisite: `01-dsa-fundamentals.md`
> Kỹ thuật xử lý trực tiếp trên bit — nhanh, tiết kiệm bộ nhớ, hay gặp trong interviews.

---

## Tại sao cần Bit Manipulation?

Mọi dữ liệu trong máy tính đều là **chuỗi bit** (0 và 1). Thao tác trực tiếp trên bit cho phép:
- **Tốc độ cực nhanh** — CPU xử lý bitwise operations trong 1 clock cycle
- **Tiết kiệm bộ nhớ** — 1 int 32-bit lưu được 32 flags (thay vì 32 booleans)
- **Giải thuật thông minh** — Nhiều bài LeetCode dùng bit tricks để O(1) space

| Phép toán | Ký hiệu | Python | Ý nghĩa |
|---|---|---|---|
| AND | `&` | `5 & 3` = 1 | Cả 2 bit đều 1 → 1 |
| OR | `\|` | `5 \| 3` = 7 | Ít nhất 1 bit là 1 → 1 |
| XOR | `^` | `5 ^ 3` = 6 | Khác nhau → 1, giống nhau → 0 |
| NOT | `~` | `~5` = -6 | Đảo tất cả bit |
| Left shift | `<<` | `1 << 3` = 8 | Nhân 2^n |
| Right shift | `>>` | `8 >> 2` = 2 | Chia 2^n |

---

## 1. Bitwise Operators — Truth Tables

```
AND (&):  OR (|):   XOR (^):  NOT (~):
0 & 0 = 0   0 | 0 = 0   0 ^ 0 = 0   ~0 = 1
0 & 1 = 0   0 | 1 = 1   0 ^ 1 = 1   ~1 = 0
1 & 0 = 0   1 | 0 = 1   1 ^ 0 = 1
1 & 1 = 1   1 | 1 = 1   1 ^ 1 = 0

Ví dụ:   5 = 101
         3 = 011
─────────────────
5 & 3  = 001 = 1   (chỉ bit cuối cùng 1)
5 | 3  = 111 = 7   (tất cả bit có ít nhất 1 cái 1)
5 ^ 3  = 110 = 6   (bit khác nhau)
```

### Shifts — Nhân và chia nhanh

```python
# Left shift: nhân 2^n
1 << 0  # 1    (2^0)
1 << 1  # 2    (2^1)
1 << 3  # 8    (2^3)
5 << 2  # 20   (5 × 4)

# Right shift: chia 2^n (bỏ phần dư)
8 >> 1   # 4    (8 / 2)
8 >> 2   # 2    (8 / 4)
7 >> 1   # 3    (7 / 2, bỏ dư)
```

---

## 2. Two's Complement — Biểu diễn số âm

Máy tính dùng **two's complement** để biểu diễn số âm. Công thức: `-n = ~n + 1`

```
Với 8-bit:
 5  = 00000101
-5  = 11111011  (đảo bit + cộng 1)

Verify: 5 + (-5) = 00000101 + 11111011 = 100000000 (overflow→ 0) ✅

Trick kiểm tra dấu:
- Bit cao nhất = 0 → số dương
- Bit cao nhất = 1 → số âm
```

---

## 3. Brian Kernighan's Algorithm — Đếm bit 1

**Bài toán:** Đếm số bit 1 trong biểu diễn nhị phân của n.

```python
# ❌ Naive: duyệt từng bit — O(32) hoặc O(64)
def count_bits_naive(n):
    count = 0
    while n:
        count += n & 1  # Check last bit
        n >>= 1
    return count

# ✅ Brian Kernighan: chỉ duyệt số bit 1 — O(number of set bits)
def count_bits(n: int) -> int:
    """
    Trick: n & (n-1) XÓA bit 1 thấp nhất.
    
    n     = 12 = 1100
    n-1   = 11 = 1011
    n&(n-1) =   1000 = 8  (xóa bit 1 ở vị trí 2)
    
    Lặp lại cho đến khi n = 0.
    """
    count = 0
    while n:
        n &= (n - 1)  # Clear lowest set bit
        count += 1
    return count

print(count_bits(12))   # 2 (1100 → 2 bit 1)
print(count_bits(255))  # 8 (11111111)
```

---

## 4. Power of 2 Check — `n & (n-1) == 0`

```python
def is_power_of_two(n: int) -> bool:
    """
    Power of 2 chỉ có ĐÚNG 1 bit 1:
    1  = 0001, 2  = 0010, 4  = 0100, 8  = 1000
    
    n & (n-1) xóa bit 1 thấp nhất.
    Nếu chỉ có 1 bit 1 → kết quả = 0.
    """
    return n > 0 and (n & (n - 1)) == 0

print(is_power_of_two(16))  # True  (10000)
print(is_power_of_two(18))  # False (10010)
```

---

## 5. Subset Enumeration — Bitmask

Dùng **bitmask** để biểu diễn tập con: bit thứ i = 1 → phần tử i **có mặt**.

```python
def all_subsets(items: list) -> list[list]:
    """
    Generate all subsets using bitmask.
    
    items = ['a', 'b', 'c'] (n=3)
    Bitmasks 000 to 111 (0 to 7):
      000 = []
      001 = ['a']
      010 = ['b']
      011 = ['a', 'b']
      100 = ['c']
      101 = ['a', 'c']
      110 = ['b', 'c']
      111 = ['a', 'b', 'c']
    """
    n = len(items)
    subsets = []
    
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):  # Check if bit i is set
                subset.append(items[i])
        subsets.append(subset)
    
    return subsets

print(all_subsets(['a', 'b', 'c']))
# [[], ['a'], ['b'], ['a', 'b'], ['c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
```

### Bitmask DP — Traveling Salesman

```python
def tsp(dist: list[list[int]]) -> int:
    """
    Traveling Salesman Problem using bitmask DP.
    dp[mask][i] = min cost to visit cities in mask, ending at i.
    """
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at city 0
    
    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue  # Already visited
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(
                    dp[new_mask][v],
                    dp[mask][u] + dist[u][v]
                )
    
    full_mask = (1 << n) - 1
    return min(dp[full_mask][i] + dist[i][0] for i in range(n))
```

---

## 6. XOR Tricks — Phép toán ma thuật

XOR có tính chất đặc biệt: `a ^ a = 0`, `a ^ 0 = a`, giao hoán và kết hợp.

### Tìm số xuất hiện 1 lần (Single Number)

```python
def single_number(nums: list[int]) -> int:
    """
    Every number appears twice EXCEPT one. Find it.
    XOR: a ^ a = 0, a ^ 0 = a
    
    [2, 1, 4, 5, 2, 4, 1]
    2^1^4^5^2^4^1 = (2^2)^(1^1)^(4^4)^5 = 0^0^0^5 = 5
    """
    result = 0
    for num in nums:
        result ^= num
    return result

print(single_number([2, 1, 4, 5, 2, 4, 1]))  # 5
```

### Swap không cần biến tạm

```python
def swap_xor(a, b):
    """
    Swap without temp variable using XOR.
    a = 5 (101), b = 3 (011)
    
    a = a ^ b  → 110 (6)
    b = a ^ b  → 110 ^ 011 = 101 (5) ← b = original a!
    a = a ^ b  → 110 ^ 101 = 011 (3) ← a = original b!
    """
    a = a ^ b
    b = a ^ b  # b = original a
    a = a ^ b  # a = original b
    return a, b
```

### Tìm missing number

```python
def missing_number(nums: list[int]) -> int:
    """
    Array [0, 1, ..., n] missing one number.
    XOR all nums with [0..n] — duplicates cancel out.
    """
    n = len(nums)
    result = n  # Start with n
    for i in range(n):
        result ^= i ^ nums[i]
    return result

print(missing_number([3, 0, 1]))  # 2
```

---

## 7. Common Bit Operations Cheatsheet

| Operation | Code | Ví dụ |
|---|---|---|
| Set bit i | `n \| (1 << i)` | `5 \| (1<<1)` = 7 (101→111) |
| Clear bit i | `n & ~(1 << i)` | `7 & ~(1<<1)` = 5 (111→101) |
| Toggle bit i | `n ^ (1 << i)` | `5 ^ (1<<0)` = 4 (101→100) |
| Check bit i | `(n >> i) & 1` | `(5 >> 2) & 1` = 1 (bit 2 is set) |
| Lowest set bit | `n & (-n)` | `12 & (-12)` = 4 (1100→0100) |
| Clear lowest bit | `n & (n - 1)` | `12 & 11` = 8 (1100→1000) |
| Is power of 2 | `n & (n-1) == 0` | `8 & 7` = 0 → True |
| Count set bits | Brian Kernighan | See above |

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | `~0 = 1` (NOT) | `~0 = -1` (two's complement) | NOT đảo TẤT CẢ bits, kể cả sign bit |
| 2 | XOR swap khi a và b cùng reference | Chỉ dùng XOR swap khi a, b khác nhau | `a ^ a = 0` → cả 2 biến mất! |
| 3 | Shift negative numbers | Behavior undefined trong C/C++ | Python OK (arbitrary precision ints) |
| 4 | Quên operator precedence | `(n & 1) == 0` KHÔNG phải `n & 1 == 0` | `==` có precedence cao hơn `&` |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** LeetCode 136 — Single Number (XOR)
- [ ] **Bài 2 (Dễ):** LeetCode 191 — Number of 1 Bits (Brian Kernighan)
- [ ] **Bài 3 (Trung bình):** LeetCode 268 — Missing Number (XOR)
- [ ] **Bài 4 (Trung bình):** LeetCode 78 — Subsets (bitmask enumeration)
- [ ] **Bài 5 (Khó):** LeetCode 137 — Single Number II (bit counting)

---

## Tài nguyên thêm

- [Bit Twiddling Hacks (Stanford)](https://graphics.stanford.edu/~seander/bithacks.html) — 100+ bit tricks
- [Binary Representations (Khan Academy)](https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:digital-information/xcae6f4a7ff015e7d:binary-numbers/a/bits-and-binary) — Cơ bản binary
- [LeetCode Bit Manipulation Tag](https://leetcode.com/tag/bit-manipulation/) — Bài tập theo tag
