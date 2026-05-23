# 📋 Competitive Coding Cheatsheet — Tra cứu nhanh cho DSA & Interviews

> `[INTERMEDIATE → ADVANCED]` — Bảng tổng hợp thuật toán, độ phức tạp, và patterns.

---

## 1. Big-O Complexity — Tra cứu nhanh

### Data Structures

| Cấu trúc | Access | Search | Insert | Delete | Space |
|---|---|---|---|---|---|
| **Array** | O(1) | O(n) | O(n) | O(n) | O(n) |
| **Linked List** | O(n) | O(n) | O(1) | O(1) | O(n) |
| **Stack / Queue** | O(n) | O(n) | O(1) | O(1) | O(n) |
| **Hash Table** | — | O(1)* | O(1)* | O(1)* | O(n) |
| **BST (balanced)** | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| **Min/Max Heap** | O(1) top | O(n) | O(log n) | O(log n) | O(n) |
| **Trie** | — | O(L) | O(L) | O(L) | O(Σ L) |

_*Amortized / average case_

### Sorting

| Algorithm | Best | Average | Worst | Space | Stable? |
|---|---|---|---|---|---|
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |
| **Counting Sort** | O(n + k) | O(n + k) | O(n + k) | O(k) | ✅ |
| **Radix Sort** | O(d × n) | O(d × n) | O(d × n) | O(n + k) | ✅ |

### Graph

| Algorithm | Time | Space | Use case |
|---|---|---|---|
| **BFS** | O(V + E) | O(V) | Shortest path (unweighted) |
| **DFS** | O(V + E) | O(V) | Connectivity, cycle detection |
| **Dijkstra** | O((V+E) log V) | O(V) | Shortest path (non-negative) |
| **Bellman-Ford** | O(V × E) | O(V) | Shortest path (negative edges) |
| **Floyd-Warshall** | O(V³) | O(V²) | All-pairs shortest path |
| **Topological Sort** | O(V + E) | O(V) | DAG ordering |
| **Kruskal MST** | O(E log E) | O(V) | Minimum spanning tree |
| **Prim MST** | O(E log V) | O(V) | Minimum spanning tree |

---

## 2. Problem-Solving Patterns

### Two Pointers

```python
# Sorted array: find pair with target sum
def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

# Remove duplicates from sorted array (in-place)
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

### Sliding Window

```python
# Max sum subarray of size k
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Slide window
        max_sum = max(max_sum, window_sum)
    return max_sum

# Longest substring without repeating characters
def length_of_longest_substring(s):
    seen = {}
    left = max_len = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

### Binary Search

```python
# Standard binary search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Lower bound: first index where arr[i] >= target
def lower_bound(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

### DFS / BFS

```python
from collections import deque

# BFS — shortest path in unweighted graph
def bfs(graph, start, target):
    queue = deque([(start, 0)])  # (node, distance)
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1

# DFS — recursive
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

### Backtracking

```python
# Generate all permutations
def permutations(nums):
    result = []
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i, num in enumerate(remaining):
            path.append(num)
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()  # Undo choice
    backtrack([], nums)
    return result

# N-Queens: place N queens on N×N board
def solve_n_queens(n):
    result = []
    def backtrack(row, cols, diag1, diag2, board):
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue
            board[row][col] = 'Q'
            backtrack(row+1, cols|{col}, diag1|{row-col}, diag2|{row+col}, board)
            board[row][col] = '.'
    backtrack(0, set(), set(), set(), [['.']*n for _ in range(n)])
    return result
```

### Union-Find

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Number of components
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.count -= 1
        return True
```

### Monotonic Stack

```python
# Next Greater Element
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # decreasing stack of indices
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(i)
    return result

# next_greater([2, 1, 2, 4, 3]) → [4, 2, 4, -1, -1]
```

---

## 3. Python Tricks for Competitive Programming

```python
# ── Input ──
import sys
input = sys.stdin.readline  # Faster input

n = int(input())
arr = list(map(int, input().split()))

# ── Common imports ──
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right
from functools import lru_cache
from itertools import combinations, permutations, product
from math import gcd, lcm, comb, inf, ceil, floor, log2

# ── Useful snippets ──
# Infinity
INF = float('inf')

# Frequency count
freq = Counter(arr)

# Adjacency list
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# Grid directions (4-directional)
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Grid directions (8-directional)
DIRS8 = [(dx, dy) for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy]

# Recursion limit (for deep DFS)
sys.setrecursionlimit(10**6)

# Sort by custom key
intervals.sort(key=lambda x: x[1])  # Sort by end time

# Default MOD for competitive programming
MOD = 10**9 + 7
```

---

## 4. Common DP States

```
1D:   dp[i]        → Linear sequence
2D:   dp[i][j]     → Two sequences, grid, intervals
DP + bitmask:       → Subset enumeration (TSP, assignment)

Common states:
- dp[i] = answer for first i elements
- dp[i][j] = answer for subarray/substring [i..j]
- dp[i][w] = answer for items 0..i with capacity w (knapsack)
- dp[mask] = answer for subset represented by bitmask
- dp[i][j][k] = 3D state (rare, try to reduce)
```

---

## 5. Interview Framework — UMPIRE

```
U — Understand the problem
    Ask clarifying questions
    Identify edge cases
    Confirm input/output format

M — Match to known patterns
    Two Pointers? Sliding Window? BFS/DFS?
    Binary Search? DP? Greedy?

P — Plan approach
    Write pseudocode
    Identify data structures
    Estimate time/space complexity

I — Implement
    Write clean code
    Use meaningful variable names

R — Review
    Walk through with example
    Check edge cases
    Verify correctness

E — Evaluate
    State time/space complexity
    Discuss trade-offs
    Propose optimizations
```

---

## 6. Pattern Recognition Cheatsheet

| Nếu bài toán có... | Thử pattern này |
|---|---|
| Sorted array | Binary Search, Two Pointers |
| Linked list | Fast/Slow pointers, Reverse |
| Tree | DFS, BFS, Recursion |
| Graph | BFS, DFS, Union-Find, Dijkstra |
| "All combinations/permutations" | Backtracking |
| "Maximum/Minimum" | DP, Greedy, Binary Search on answer |
| "K-th element" | Heap (size K), Quickselect |
| "Subarray/Substring" | Sliding Window, Prefix Sum |
| "Parentheses/Brackets" | Stack |
| "Intervals" | Sort + Greedy/Sweep line |
| "Matrix" | BFS/DFS (grid), DP |
| "String pattern" | KMP, Trie, Rabin-Karp |
| O(1) space constraint | Bit manipulation, in-place |

---

## 7. Time Complexity Hints — Nhận biết expected complexity

```
n ≤ 10:        O(n!) — Brute force / permutations
n ≤ 20:        O(2^n) — Bitmask DP / subsets
n ≤ 500:       O(n³) — 3 nested loops
n ≤ 5,000:     O(n²) — 2 nested loops
n ≤ 10^6:      O(n log n) — Sorting / binary search
n ≤ 10^8:      O(n) — Linear scan
n ≤ 10^18:     O(log n) — Binary search / math
```

---

## Tài nguyên thêm

- [NeetCode 150](https://neetcode.io/practice) — Curated LeetCode list
- [Blind 75](https://www.teamblind.com/post/New-Year-Gift---Curated-List-of-Top-75-LeetCode-Questions-to-Save-Your-Time-OaM1orEU) — Must-do interview problems
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/) — Tra cứu complexity
- [CP-Algorithms](https://cp-algorithms.com/) — Encyclopedia thuật toán
- [Codeforces](https://codeforces.com/) — Competitive programming platform
- [LeetCode Patterns](https://seanprashad.com/leetcode-patterns/) — Nhóm bài theo pattern
