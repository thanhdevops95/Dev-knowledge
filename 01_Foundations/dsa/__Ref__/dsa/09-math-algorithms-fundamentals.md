# 🔢 Math Algorithms — Thuật toán Toán học

> `[INTERMEDIATE]` — Prerequisite: `01-dsa-fundamentals.md`
> Các thuật toán toán học cơ bản mọi developer nên biết — GCD, modular arithmetic, primes, combinatorics.

---

## Tại sao developer cần biết Math Algorithms?

Bạn không cần giỏi toán cao cấp để code, nhưng một số thuật toán toán cơ bản xuất hiện **rất thường xuyên**:
- **Cryptography:** RSA dùng modular exponentiation, primes
- **Hashing:** Modular arithmetic cho hash functions
- **Game dev:** Vector math, trigonometry
- **Competitive programming:** Hầu hết bài medium-hard cần number theory

---

## 1. GCD & LCM — Ước chung lớn nhất

### Euclid's Algorithm — O(log(min(a,b)))

```python
def gcd(a: int, b: int) -> int:
    """
    Greatest Common Divisor — Euclid's Algorithm.
    Key insight: gcd(a, b) = gcd(b, a % b)
    
    gcd(48, 18):
    48 % 18 = 12 → gcd(18, 12)
    18 % 12 = 6  → gcd(12, 6)
    12 % 6  = 0  → gcd(6, 0) = 6 ✅
    """
    while b:
        a, b = b, a % b
    return a

def lcm(a: int, b: int) -> int:
    """Least Common Multiple: lcm = a * b / gcd(a, b)"""
    return a * b // gcd(a, b)

print(gcd(48, 18))  # 6
print(lcm(4, 6))    # 12

# Python 3.9+: math.gcd, math.lcm built-in
from math import gcd, lcm
```

### Extended Euclidean — Tìm x, y sao cho ax + by = gcd(a, b)

```python
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Returns (gcd, x, y) where ax + by = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

# 35x + 15y = gcd(35, 15) = 5
g, x, y = extended_gcd(35, 15)
print(f"{g} = 35×{x} + 15×{y}")  # 5 = 35×1 + 15×(-2)
```

---

## 2. Modular Arithmetic — Tính toán với mod

### Tính chất cơ bản

```
(a + b) mod m = ((a mod m) + (b mod m)) mod m
(a - b) mod m = ((a mod m) - (b mod m) + m) mod m
(a × b) mod m = ((a mod m) × (b mod m)) mod m

⚠️ (a / b) mod m ≠ ((a mod m) / (b mod m)) mod m
    → Cần dùng modular inverse!
```

### Modular Exponentiation — Fast Power

```python
def power_mod(base: int, exp: int, mod: int) -> int:
    """
    Calculate base^exp % mod efficiently — O(log exp).
    
    Ý tưởng: 2^10 = 2^5 × 2^5 = (2^2 × 2^2 × 2)^2
    Chia exp cho 2 mỗi bước → O(log n)
    """
    result = 1
    base %= mod
    
    while exp > 0:
        if exp & 1:  # exp is odd
            result = (result * base) % mod
        exp >>= 1    # exp = exp / 2
        base = (base * base) % mod
    
    return result

# 2^100 mod 1000000007
print(power_mod(2, 100, 10**9 + 7))  # 976371285
# Python built-in: pow(2, 100, 10**9 + 7)
```

### Modular Inverse — Chia trong mod

```python
def mod_inverse(a: int, mod: int) -> int:
    """
    Find x such that (a × x) % mod = 1.
    Uses Fermat's little theorem: a^(p-1) ≡ 1 (mod p) if p is prime.
    → a^(-1) ≡ a^(p-2) (mod p)
    """
    return pow(a, mod - 2, mod)

MOD = 10**9 + 7
# (10 / 2) mod MOD
# = 10 × mod_inverse(2, MOD) mod MOD
print((10 * mod_inverse(2, MOD)) % MOD)  # 5
```

---

## 3. Số nguyên tố — Primes

### Kiểm tra số nguyên tố — O(√n)

```python
def is_prime(n: int) -> bool:
    """Check if n is prime — O(√n)."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6  # Optimization: primes > 3 have form 6k±1
    
    return True
```

### Sieve of Eratosthenes — Tìm tất cả primes ≤ n

```python
def sieve(n: int) -> list[int]:
    """
    Find all primes up to n — O(n log log n).
    
    Đánh dấu các bội số: 2→4,6,8... 3→6,9,12... 5→10,15...
    Số chưa bị đánh dấu = prime!
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, n + 1) if is_prime[i]]

primes = sieve(50)
print(primes)
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

### Phân tích thừa số nguyên tố

```python
def prime_factors(n: int) -> list[int]:
    """Prime factorization — O(√n)."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

print(prime_factors(60))   # [2, 2, 3, 5] → 60 = 2² × 3 × 5
print(prime_factors(97))   # [97] → prime!
```

---

## 4. Combinatorics — Tổ hợp

### nCr — Tổ hợp chập r từ n

```python
def nCr(n: int, r: int, mod: int = 10**9 + 7) -> int:
    """
    C(n, r) = n! / (r! × (n-r)!)
    Sử dụng modular inverse cho mod operations.
    """
    if r > n:
        return 0
    if r == 0 or r == n:
        return 1
    
    # Precompute factorials
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    
    # nCr = fact[n] × inverse(fact[r]) × inverse(fact[n-r])
    return (fact[n] * pow(fact[r], mod - 2, mod) % mod * 
            pow(fact[n - r], mod - 2, mod) % mod)

print(nCr(10, 3))   # 120
print(nCr(52, 5))   # 2598960 (poker hands)
```

### Pascal's Triangle — Tam giác Pascal

```python
def pascal(n: int) -> list[list[int]]:
    """
    Pascal's triangle: C(n,r) = C(n-1,r-1) + C(n-1,r)
    
    Row 0:     1
    Row 1:    1 1
    Row 2:   1 2 1
    Row 3:  1 3 3 1
    Row 4: 1 4 6 4 1
    """
    triangle = [[1]]
    for i in range(1, n + 1):
        row = [1]
        for j in range(1, i):
            row.append(triangle[i-1][j-1] + triangle[i-1][j])
        row.append(1)
        triangle.append(row)
    return triangle
```

---

## 5. Matrix Exponentiation — Fibonacci nhanh O(log n)

```python
import numpy as np

def matrix_power(matrix, n):
    """Matrix exponentiation — O(log n)."""
    result = np.eye(len(matrix), dtype=int)
    base = np.array(matrix, dtype=int)
    
    while n > 0:
        if n & 1:
            result = result @ base
        base = base @ base
        n >>= 1
    
    return result

def fibonacci_fast(n: int) -> int:
    """
    Fibonacci using matrix exponentiation — O(log n).
    
    [F(n+1)]   [1, 1]^n   [1]
    [F(n)  ] = [1, 0]   × [0]
    """
    if n <= 1:
        return n
    M = matrix_power([[1, 1], [1, 0]], n)
    return int(M[0][1])

print(fibonacci_fast(50))  # 12586269025
```

---

## 6. Geometry Basics — Hình học tính toán

```python
import math

def distance(p1: tuple, p2: tuple) -> float:
    """Euclidean distance between 2 points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def cross_product(o, a, b):
    """
    Cross product of vectors OA and OB.
    > 0: counter-clockwise (B is left of OA)
    = 0: collinear
    < 0: clockwise (B is right of OA)
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def on_segment(p, q, r):
    """Check if point q lies on segment pr."""
    return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | `a / b % mod` | `a * mod_inverse(b, mod) % mod` | Phép chia KHÔNG commute với mod |
| 2 | Sieve tới n → check `i*i <= n` | Sieve tới √n đủ | Bội đã bị đánh dấu bởi prime nhỏ hơn |
| 3 | `is_prime(1)` = True | 1 KHÔNG phải prime | Prime phải > 1 |
| 4 | Integer overflow khi tính nCr | Dùng mod trong mỗi bước nhân | C(100, 50) cực lớn → overflow nếu không mod |
| 5 | Float comparison: `a == b` | `abs(a - b) < 1e-9` | Floating point precision errors |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** LeetCode 204 — Count Primes (Sieve)
- [ ] **Bài 2 (Trung bình):** LeetCode 50 — Pow(x, n) (fast exponentiation)
- [ ] **Bài 3 (Trung bình):** LeetCode 372 — Super Pow (modular exp)
- [ ] **Bài 4 (Trung bình):** Tính C(10^9, 10^5) mod 10^9+7
- [ ] **Bài 5 (Khó):** LeetCode 1175 — Prime Arrangements (combinatorics)

---

## Tài nguyên thêm

- [CP-Algorithms — Number Theory](https://cp-algorithms.com/algebra/) — Toàn diện nhất
- [Project Euler](https://projecteuler.net/) — Math + Programming problems
- [CLRS Chapter 31 — Number Theory](https://mitpress.mit.edu/9780262046305/) — Sách giáo khoa
- [3Blue1Brown — Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) — Visual math
