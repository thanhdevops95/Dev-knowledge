# 🧮 Dynamic Programming — Quy hoạch động

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `01-dsa-fundamentals.md`
> Kỹ thuật giải thuật mạnh mẽ nhất cho bài toán tối ưu hóa.

---

## Tại sao cần Dynamic Programming?

Hãy tưởng tượng bạn leo cầu thang 50 bậc, mỗi bước có thể leo 1 hoặc 2 bậc. Có bao nhiêu cách leo? Nếu dùng **đệ quy thuần**, bạn sẽ tính lại cùng một bài con **hàng tỷ lần**:

```
                    f(5)
                   /    \
               f(4)      f(3)
              /    \     /    \
          f(3)    f(2) f(2)   f(1)
         /    \
     f(2)    f(1)

f(2) được tính 3 lần! f(3) tính 2 lần!
Với f(50): khoảng 2^50 ≈ 10^15 phép tính — HÀNG NĂM!
```

**Dynamic Programming (DP)** giải quyết bằng cách **ghi nhớ kết quả** đã tính → mỗi bài con chỉ tính **1 lần**. Biến O(2ⁿ) thành O(n).

### 2 điều kiện để áp dụng DP

| Điều kiện | Ý nghĩa | Ví dụ |
|---|---|---|
| **Overlapping subproblems** | Bài toán con bị tính lại nhiều lần | Fibonacci: f(3) tính 2 lần |
| **Optimal substructure** | Lời giải tối ưu = tổ hợp lời giải tối ưu của bài con | Đường đi ngắn nhất: shortest(A→C) = shortest(A→B) + shortest(B→C) |

---

## 1. Memoization (Top-Down) — Đệ quy + Cache

**Ý tưởng:** Viết đệ quy bình thường, nhưng **lưu kết quả vào cache**. Trước khi tính, kiểm tra cache trước.

```python
# ❌ Naive recursion — O(2^n) 💥
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# ✅ Memoization — O(n) ⚡
def fib_memo(n, memo={}):
    if n <= 1:
        return n
    if n in memo:
        return memo[n]  # Already computed!
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# Python shortcut: @lru_cache
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(100))  # 354224848179261915075 — instant!
```

Memoization giữ nguyên cấu trúc đệ quy (dễ hiểu), chỉ thêm cache. Nhược điểm: recursion depth limit (Python mặc định 1000).

---

## 2. Tabulation (Bottom-Up) — Lặp + Bảng

**Ý tưởng:** Tính từ bài con **nhỏ nhất** lên lớn dần, lưu vào **bảng (array)**. Không cần đệ quy.

```python
# Bottom-Up Fibonacci — O(n) time, O(n) space
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]

# Space-optimized — O(1) space ⚡
def fib_optimal(n):
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
```

### So sánh Top-Down vs Bottom-Up

| | Memoization (Top-Down) | Tabulation (Bottom-Up) |
|---|---|---|
| **Cách tiếp cận** | Đệ quy + cache | Lặp + bảng |
| **Tính bài con nào?** | Chỉ bài con **cần thiết** | Tính **tất cả** bài con |
| **Stack overflow?** | Có (recursion depth) | Không |
| **Dễ viết?** | Dễ hơn (giữ cấu trúc đệ quy) | Khó hơn (cần xác định thứ tự) |
| **Tối ưu space?** | Khó | Dễ (chỉ giữ giá trị cần thiết) |

---

## 3. 1D DP — Climbing Stairs, House Robber

### Climbing Stairs

Bạn leo cầu thang n bậc. Mỗi bước leo 1 hoặc 2 bậc. Có bao nhiêu cách?

```python
def climb_stairs(n: int) -> int:
    """
    dp[i] = số cách leo đến bậc i
    dp[i] = dp[i-1] + dp[i-2]
    (đến bậc i: hoặc từ i-1 leo 1 bậc, hoặc từ i-2 leo 2 bậc)
    """
    if n <= 2:
        return n
    
    prev2, prev1 = 1, 2  # dp[1]=1, dp[2]=2
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1

# climb_stairs(5) = 8
# Cách: [1,1,1,1,1], [1,1,1,2], [1,1,2,1], [1,2,1,1], [2,1,1,1],
#        [1,2,2], [2,1,2], [2,2,1]
```

### House Robber

Dãy nhà có giá trị `[2, 7, 9, 3, 1]`. Không được cướp 2 nhà liên tiếp. Maximize tổng giá trị.

```python
def rob(nums: list[int]) -> int:
    """
    dp[i] = max money robbing houses 0..i
    dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    (hoặc bỏ qua nhà i, hoặc cướp nhà i + best từ i-2)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2, prev1 = 0, 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = curr
    return prev1

# rob([2, 7, 9, 3, 1]) = 12 (rob houses 0, 2, 4: 2+9+1=12)
```

---

## 4. 2D DP — Knapsack, LCS

### 0/1 Knapsack — Bài toán ba lô

Có N items, mỗi item có (weight, value). Ba lô chứa tối đa W kg. Chọn items để **maximize tổng value**.

```python
def knapsack(weights: list, values: list, capacity: int) -> int:
    """
    dp[i][w] = max value using items 0..i-1 with capacity w
    
    For each item i:
      - DON'T take: dp[i][w] = dp[i-1][w]
      - TAKE:       dp[i][w] = dp[i-1][w - weight_i] + value_i
      dp[i][w] = max of above two choices
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i - 1][w]
            
            # Take item i (if it fits)
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
    
    return dp[n][capacity]

# Items: weight=[2,3,4,5], value=[3,4,5,6], capacity=8
# Answer: 10 (items weight 3+5=8, value 4+6=10)
print(knapsack([2, 3, 4, 5], [3, 4, 5, 6], 8))
```

### Longest Common Subsequence (LCS)

Tìm subsequence chung dài nhất của 2 chuỗi.

```python
def lcs(text1: str, text2: str) -> int:
    """
    dp[i][j] = LCS length of text1[:i] and text2[:j]
    
    If text1[i-1] == text2[j-1]:
        dp[i][j] = dp[i-1][j-1] + 1     (extend LCS)
    Else:
        dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (skip one char)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

print(lcs("abcde", "ace"))  # 3 → "ace"
```

```
    ""  a  c  e
""   0  0  0  0
a    0  1  1  1
b    0  1  1  1
c    0  1  2  2
d    0  1  2  2
e    0  1  2  3  ← LCS = 3
```

---

## 5. String DP — Edit Distance, Palindrome

### Edit Distance (Levenshtein Distance)

Số thao tác tối thiểu (insert, delete, replace) để biến word1 thành word2.

```python
def min_distance(word1: str, word2: str) -> int:
    """
    dp[i][j] = min operations to convert word1[:i] → word2[:j]
    
    If word1[i-1] == word2[j-1]:
        dp[i][j] = dp[i-1][j-1]           (no operation needed)
    Else:
        dp[i][j] = 1 + min(
            dp[i-1][j],     # delete from word1
            dp[i][j-1],     # insert into word1
            dp[i-1][j-1]    # replace
        )
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: converting to/from empty string
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete
                    dp[i][j - 1],      # insert
                    dp[i - 1][j - 1]   # replace
                )
    
    return dp[m][n]

print(min_distance("kitten", "sitting"))  # 3
# kitten → sitten (replace k→s) → sittin (replace e→i) → sitting (insert g)
```

### Longest Palindromic Subsequence

```python
def longest_palindrome_subseq(s: str) -> int:
    """LPS = LCS(s, reverse(s))"""
    return lcs(s, s[::-1])

print(longest_palindrome_subseq("bbbab"))  # 4 → "bbbb"
```

---

## 6. Interval DP — Matrix Chain Multiplication

Tối ưu hóa thứ tự nhân ma trận để **giảm số phép nhân**.

```python
def matrix_chain(dims: list) -> int:
    """
    dims = [10, 20, 30, 40] → matrices: 10×20, 20×30, 30×40
    dp[i][j] = min multiplications for matrices i..j
    
    Try every split point k between i and j:
    dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1])
    """
    n = len(dims) - 1  # Number of matrices
    dp = [[0] * n for _ in range(n)]
    
    # l = chain length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            
            for k in range(i, j):
                cost = (dp[i][k] + dp[k + 1][j] +
                        dims[i] * dims[k + 1] * dims[j + 1])
                dp[i][j] = min(dp[i][j], cost)
    
    return dp[0][n - 1]

# Matrices: 10×20, 20×30, 30×40
print(matrix_chain([10, 20, 30, 40]))  # 18000
```

---

## 7. DP on Trees — Diameter, Path Sum

```python
def tree_diameter(root) -> int:
    """
    Diameter = longest path between any two nodes.
    For each node: diameter through it = left_depth + right_depth
    """
    diameter = 0
    
    def depth(node):
        nonlocal diameter
        if not node:
            return 0
        
        left = depth(node.left)
        right = depth(node.right)
        
        # Update diameter: path through this node
        diameter = max(diameter, left + right)
        
        # Return depth of this subtree
        return 1 + max(left, right)
    
    depth(root)
    return diameter
```

---

## 8. Nhận diện bài DP — Checklist

Khi gặp bài toán, hãy tự hỏi:

```
1. ✅ Có hỏi "tối ưu" (min/max) hoặc "đếm số cách"?
   → Khả năng cao là DP

2. ✅ Có overlapping subproblems?
   → Vẽ recursion tree, nếu thấy node lặp lại → DP

3. ✅ Có optimal substructure?
   → Lời giải tối ưu = tổ hợp lời giải tối ưu bài con?

4. 📝 Xác định STATE:
   → "dp[i] = gì?" hoặc "dp[i][j] = gì?"
   → State thường là: index, remaining capacity, position

5. 📝 Xác định TRANSITION:
   → dp[i] = f(dp[i-1], dp[i-2], ...)
   → Liệt kê tất cả lựa chọn tại state i

6. 📝 BASE CASE:
   → dp[0] = ?, dp[1] = ?

7. 📝 ANSWER:
   → dp[n]? max(dp)? dp[m][n]?
```

### DP Pattern Recognition

| Nếu bài toán... | Pattern | Ví dụ |
|---|---|---|
| 1D array, mỗi step chọn take/skip | **1D DP** | House Robber, Climbing Stairs |
| 2 sequences, tìm common/distance | **2D DP (grid)** | LCS, Edit Distance |
| Items + capacity | **Knapsack** | 0/1 Knapsack, Coin Change |
| String + palindrome/partition | **Interval DP** | Palindrome Partition, Matrix Chain |
| Tree + subtree optimization | **Tree DP** | Diameter, House Robber III |
| Graph + shortest path | **Graph DP** | Bellman-Ford, Floyd-Warshall |

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Mọi bài đệ quy đều là DP | DP cần **overlapping subproblems** | DFS/backtracking không phải DP nếu không lặp |
| 2 | Luôn dùng 2D table | Nhiều bài 2D optimize được thành 1D | LCS, Knapsack có thể O(n) space |
| 3 | Quên base case | Luôn xác định base case trước | dp[0], dp[1] quyết định correctness |
| 4 | DP = memorize recursion | Bottom-up thường nhanh hơn vì no stack overhead | Memoization dễ viết, tabulation hiệu quả hơn |
| 5 | Copy-paste DP solution không hiểu | Vẽ bảng DP bằng tay trước khi code | Hiểu transition = hiểu bài toán |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** LeetCode 70 — Climbing Stairs
- [ ] **Bài 2 (Dễ):** LeetCode 198 — House Robber
- [ ] **Bài 3 (Trung bình):** LeetCode 322 — Coin Change
- [ ] **Bài 4 (Trung bình):** LeetCode 1143 — Longest Common Subsequence
- [ ] **Bài 5 (Trung bình):** LeetCode 416 — Partition Equal Subset Sum (Knapsack variant)
- [ ] **Bài 6 (Khó):** LeetCode 72 — Edit Distance
- [ ] **Bài 7 (Khó):** LeetCode 312 — Burst Balloons (Interval DP)

---

## Tài nguyên thêm

- [NeetCode DP Roadmap](https://neetcode.io/roadmap) — Video giải từng dạng DP
- [Grokking Dynamic Programming (Educative)](https://www.educative.io/courses/grokking-dynamic-programming-a-deep-dive-using-python) — Course chuyên DP
- [CLRS Chapter 15 — Dynamic Programming](https://mitpress.mit.edu/9780262046305/) — Sách giáo khoa
- [Back To Back SWE — DP Playlist](https://www.youtube.com/@BackToBackSWE) — YouTube channel
- [Aditya Verma DP Playlist](https://www.youtube.com/playlist?list=PL_z_8CaSLPWekqhdCPmFohncHwz8TY2Go) — 50+ bài DP lectures
