# 📐 Thuật toán & Cấu trúc Dữ liệu (DSA)

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Nền tảng tư duy lập trình

---

## Tại sao cần học DSA?

- **Phỏng vấn** — FAANG và nhiều công ty lớn test DSA
- **Hiệu năng** — Chọn đúng cấu trúc dữ liệu → code nhanh hơn 100-1000x
- **Tư duy** — Rèn luyện khả năng chia nhỏ và giải quyết vấn đề
- **Code tốt hơn** — Biết lúc nào dùng Map thay vì List, Queue thay vì Stack

---

## Big O Notation — Đánh giá độ phức tạp

```
O(1)       Constant    — Truy cập phần tử theo index
O(log n)   Logarithmic — Binary search
O(n)       Linear      — Duyệt qua mảng
O(n log n) Log-linear  — Merge sort, Quick sort
O(n²)      Quadratic   — Bubble sort, vòng lặp lồng nhau
O(2ⁿ)      Exponential — Brute force subset
O(n!)      Factorial   — Permutations
```

```
Nhanh                                                    Chậm
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)
```

**Quy tắc tính Big O:**
```python
def example(arr):
    x = arr[0]          # O(1)
    
    for item in arr:    # O(n)
        print(item)
    
    for i in arr:       # O(n²) — vòng lặp lồng
        for j in arr:
            print(i, j)
    
    # Tổng = O(1) + O(n) + O(n²) → loại bỏ bậc nhỏ → O(n²)
```

---

## Cấu trúc dữ liệu cơ bản

### Array / List — Mảng

```python
# Time complexity:
# Access by index: O(1)
# Search:          O(n)
# Insert/Delete cuối: O(1) amortized
# Insert/Delete giữa: O(n)

arr = [1, 2, 3, 4, 5]
arr[2]          # O(1) — truy cập trực tiếp
arr.append(6)   # O(1) — thêm cuối
arr.insert(0, 0)  # O(n) — chèn giữa (phải dịch chuyển)

# Khi dùng: Cần truy cập nhanh theo index, dữ liệu liên tục
```

### Hash Map / Dictionary

```python
# Time complexity:
# Insert: O(1) average
# Lookup: O(1) average
# Delete: O(1) average
# → Tốt nhất cho tìm kiếm nhanh theo key

phone_book = {}
phone_book["Alice"] = "0901234567"   # O(1)
phone_book["Bob"]   = "0987654321"   # O(1)

number = phone_book.get("Alice")     # O(1) — nhanh hơn rất nhiều so với list!

# Use cases:
# - Đếm tần suất (frequency counter)
# - Cache kết quả (memoization)
# - Group data theo key
# - Tìm kiếm O(1)

# Ví dụ: Đếm ký tự
def char_frequency(s: str) -> dict:
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return freq
```

### Stack — Ngăn xếp (LIFO)

```python
# Last In, First Out — Vào sau ra trước
# Time: push O(1), pop O(1), peek O(1)

stack = []
stack.append("a")   # push
stack.append("b")
stack.append("c")

top = stack[-1]     # peek: "c"
item = stack.pop()  # pop: "c"

# Use cases:
# - Undo/Redo functionality
# - Kiểm tra brackets/parentheses
# - Call stack trong function calls
# - DFS (Depth First Search)
# - Evaluate expressions

def is_valid_brackets(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
    
    return len(stack) == 0

print(is_valid_brackets("({[]})"))  # True
print(is_valid_brackets("({[})"))   # False
```

### Queue — Hàng đợi (FIFO)

```python
from collections import deque

# First In, First Out — Vào trước ra trước
# deque: enqueue O(1), dequeue O(1)

queue = deque()
queue.append("task1")    # enqueue
queue.append("task2")
queue.append("task3")

item = queue.popleft()   # dequeue: "task1"

# Use cases:
# - Job queues / task scheduling
# - BFS (Breadth First Search)
# - Buffer cho luồng dữ liệu
# - Printer queue
```

### Linked List — Danh sách liên kết

```python
# Time complexity:
# Access: O(n)
# Search: O(n)
# Insert đầu/cuối: O(1)
# Insert giữa: O(n) để tìm vị trí
# Delete: O(n) để tìm, O(1) để xóa

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def prepend(self, value):           # O(1)
        node = Node(value)
        node.next = self.head
        self.head = node
    
    def append(self, value):            # O(n)
        node = Node(value)
        if not self.head:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node
    
    def delete(self, value):            # O(n)
        if not self.head:
            return
        if self.head.value == value:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return
            current = current.next
```

### Tree — Cây

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# Binary Search Tree (BST):
# - Trái < Root < Phải
# - Search, Insert, Delete: O(log n) average, O(n) worst

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        def _insert(node, val):
            if not node:
                return TreeNode(val)
            if val < node.val:
                node.left = _insert(node.left, val)
            else:
                node.right = _insert(node.right, val)
            return node
        self.root = _insert(self.root, val)
    
    def search(self, val) -> bool:
        def _search(node, val):
            if not node:
                return False
            if node.val == val:
                return True
            if val < node.val:
                return _search(node.left, val)
            return _search(node.right, val)
        return _search(self.root, val)

# Tree Traversals
def inorder(node):     # Left → Root → Right (cho BST: tăng dần)
    if node:
        inorder(node.left)
        print(node.val)
        inorder(node.right)

def preorder(node):    # Root → Left → Right (copy tree)
    if node:
        print(node.val)
        preorder(node.left)
        preorder(node.right)

def postorder(node):   # Left → Right → Root (delete tree)
    if node:
        postorder(node.left)
        postorder(node.right)
        print(node.val)
```

---

## Thuật toán Sắp xếp

| Thuật toán | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| **Tim Sort** (Python default) | O(n) | O(n log n) | O(n log n) | O(n) | ✅ |

```python
# Merge Sort — Chia để trị
def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    return result + left[i:] + right[j:]
```

---

## Thuật toán Tìm kiếm

```python
# Linear Search — O(n)
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

# Binary Search — O(log n) — Mảng phải được sắp xếp!
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# BFS — Duyệt theo chiều rộng (Breadth First Search)
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

# DFS — Duyệt theo chiều sâu (Depth First Search)
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    result = [node]
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    
    return result
```

---

## Kỹ thuật giải bài

### Two Pointers

```python
# Tìm 2 số có tổng = target trong mảng đã sort
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
```

### Sliding Window

```python
# Tổng lớn nhất của subarray độ dài k
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### Dynamic Programming

```python
# Fibonacci — Memoization (Top-down)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Fibonacci — Tabulation (Bottom-up)
def fib_dp(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

---

## Bài tập thực hành (LeetCode)

### Beginner
- [ ] Two Sum (LeetCode #1)
- [ ] Valid Parentheses (LeetCode #20)
- [ ] Reverse Linked List (LeetCode #206)
- [ ] Maximum Subarray (LeetCode #53)

### Intermediate
- [ ] Binary Search (LeetCode #704)
- [ ] Merge Intervals (LeetCode #56)
- [ ] Climbing Stairs (LeetCode #70) — DP
- [ ] Number of Islands (LeetCode #200) — BFS/DFS

### Advanced
- [ ] Longest Palindromic Substring (LeetCode #5)
- [ ] LRU Cache (LeetCode #146)
- [ ] Word Ladder (LeetCode #127)

---

## Tài nguyên thêm

- [NeetCode.io](https://neetcode.io/) — Roadmap + 150 bài thiết yếu có giải thích
- [LeetCode](https://leetcode.com/) — Luyện tập
- [Visualgo](https://visualgo.net/) — Trực quan hóa thuật toán
- [The Algorithm Design Manual (book)](https://www.amazon.com/Algorithm-Design-Manual-Steven-Skiena/dp/1848000693)
