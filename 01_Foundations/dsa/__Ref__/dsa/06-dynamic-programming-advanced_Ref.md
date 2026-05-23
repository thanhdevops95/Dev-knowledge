# 🧮 Dynamic Programming & Advanced DSA

> `[INTERMEDIATE → ADVANCED]` — Thuật toán cho phỏng vấn Senior

---

## Dynamic Programming là gì?

**DP = chia bài toán lớn → bài toán con + ghi nhớ kết quả** (không tính lại).

```
Fibonacci naive:
fib(5) = fib(4) + fib(3)
       = (fib(3) + fib(2)) + (fib(2) + fib(1))
       = ((fib(2) + fib(1)) + fib(2)) + (fib(2) + fib(1))
  → Tính fib(2) NHIỀU LẦN! O(2^n) 😱

DP: ghi nhớ kết quả
fib(1) = 1, fib(2) = 1
fib(3) = fib(2) + fib(1) = 2   ← ghi nhớ
fib(4) = fib(3) + fib(2) = 3   ← dùng kết quả đã tính
fib(5) = fib(4) + fib(3) = 5   ← O(n) ⚡
```

---

## 1. Top-Down (Memoization) vs Bottom-Up (Tabulation)

```python
# Top-Down: Recursive + cache
def fib_memo(n, memo={}):
    if n <= 2:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# Bottom-Up: Iterative + table
def fib_tab(n):
    if n <= 2:
        return 1
    dp = [0] * (n + 1)
    dp[1] = dp[2] = 1
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Space-optimized: chỉ cần 2 biến
def fib_opt(n):
    if n <= 2:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
```

---

## 2. Classic DP Problems

### Climbing Stairs

```python
# Bạn có thể leo 1 hoặc 2 bậc. Có bao nhiêu cách leo n bậc?
def climb_stairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]  # Đến bậc i: từ i-1 hoặc i-2
    return dp[n]
```

### 0/1 Knapsack

```python
# Có N items (weight, value). Túi chứa W kg. Maximize tổng value.
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],                              # Không lấy item i
                    dp[i-1][w - weights[i-1]] + values[i-1]  # Lấy item i
                )
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]

# items: weight=[2,3,4,5], value=[3,4,5,6], capacity=8
# Answer: 10 (items 2+3=5kg, value=4+6=10)
```

### Longest Common Subsequence (LCS)

```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

lcs("abcde", "ace")  # 3 ("ace")
```

### Coin Change

```python
# Có coins = [1, 5, 10, 25]. Đổi amount = 30. Cần ít nhất bao nhiêu xu?
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1

    return dp[amount] if dp[amount] != float('inf') else -1

coin_change([1, 5, 10, 25], 30)  # 2 (25 + 5)
```

---

## 3. Graph Algorithms nâng cao

### Dijkstra — Shortest Path (weighted)

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_dist > distances[curr_node]:
            continue

        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('D', 3), ('C', 1)],
    'C': [('B', 1), ('D', 5)],
    'D': [],
}
dijkstra(graph, 'A')  # {'A': 0, 'B': 3, 'C': 2, 'D': 6}
```

### Topological Sort — DAG ordering

```python
def topological_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = [node for node in in_degree if in_degree[node] == 0]
    result = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(graph) else []  # [] = cycle!

# Use case: build systems, task scheduling, course prerequisites
```

---

## 4. Advanced Data Structures

### Trie — Prefix Tree

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find(prefix) is not None

    def _find(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

# Use case: autocomplete, spell checker, IP routing
trie = Trie()
trie.insert("apple")
trie.insert("app")
trie.search("app")       # True
trie.starts_with("ap")   # True
```

### Union-Find (Disjoint Set)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

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
        return True

# Use case: connected components, Kruskal's MST, cycle detection
```

---

## 5. DP Framework — Cách tiếp cận

```
Bước 1: Xác định subproblem
  "dp[i] = gì?" hoặc "dp[i][j] = gì?"

Bước 2: Xác định recurrence relation
  dp[i] = f(dp[i-1], dp[i-2], ...)

Bước 3: Base cases
  dp[0] = ?, dp[1] = ?

Bước 4: Thứ tự tính toán
  Bottom-up: i từ nhỏ → lớn

Bước 5: Trả kết quả
  dp[n] hoặc max(dp)
```

---

## Big O Cheat Sheet

| Algorithm | Time | Space |
|---|---|---|
| Binary Search | O(log n) | O(1) |
| BFS/DFS | O(V + E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Merge Sort | O(n log n) | O(n) |
| Quick Sort | O(n log n) avg | O(log n) |
| DP (1D) | O(n) | O(n) |
| DP (2D) | O(n × m) | O(n × m) |
| Trie insert/search | O(L) | O(Σ L) |

---

## Bài tập thực hành

- [ ] LeetCode: Climbing Stairs (70), Coin Change (322)
- [ ] LeetCode: Longest Common Subsequence (1143)
- [ ] LeetCode: 0/1 Knapsack variant — Partition Equal Subset Sum (416)
- [ ] Implement Trie + autocomplete feature

---

## Tài nguyên thêm

- [NeetCode.io](https://neetcode.io/) — Roadmap & video giải
- [LeetCode Patterns](https://seanprashad.com/leetcode-patterns/) — Nhóm theo pattern
- [Grokking Algorithms](https://www.manning.com/books/grokking-algorithms) — Visual book
