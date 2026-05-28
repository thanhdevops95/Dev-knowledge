# 🌳 Trees & Graphs — Cây và Đồ thị

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Cấu trúc dữ liệu xuất hiện mọi nơi: file system, DOM, mạng xã hội

---

## Tại sao cần học Trees & Graphs?

**Cây** có ở khắp nơi:
- **File system:** thư mục chứa thư mục con
- **HTML DOM:** `<html>` chứa `<body>` chứa `<div>`
- **Database index:** B-Tree giúp query nhanh

**Đồ thị** mô hình hóa quan hệ:
- **Mạng xã hội:** ai kết bạn với ai?
- **Google Maps:** đường ngắn nhất từ A đến B?
- **Internet:** các router kết nối thế nào?

---

## Phần 1: Trees (Cây)

### Khái niệm cơ bản

```
          Root (gốc)
         /    \
       A        B         ← Children (con) của Root
      / \       |
    C    D      E         ← Leaf nodes (lá — không có con)

Thuật ngữ:
• Root:   Node trên cùng (không có cha)
• Parent: Node cha
• Child:  Node con
• Leaf:   Node không có con
• Depth:  Khoảng cách từ root → node (root = 0)
• Height: Khoảng cách từ node → leaf xa nhất
```

---

### Binary Tree — Cây nhị phân

Mỗi node tối đa **2 con** (left, right):

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
```

### Binary Search Tree (BST) — Cây tìm kiếm nhị phân

**Quy tắc:** Left < Node < Right

```
        8
       / \
      3    10
     / \     \
    1    6    14
        / \   /
       4   7 13
```

```python
class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if not node:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        return node

    def search(self, val):
        return self._search(self.root, val)

    def _search(self, node, val):
        if not node:
            return False
        if val == node.val:
            return True
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)
```

**Độ phức tạp BST:**

| Thao tác | Average | Worst (mất cân bằng) |
|---|---|---|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

> ⚠️ BST có thể bị "suy thoái" thành linked list nếu insert theo thứ tự → dùng **Self-balancing BST** (AVL, Red-Black Tree).

---

### Duyệt cây (Tree Traversal)

```
        1
       / \
      2    3
     / \
    4    5
```

```python
# Inorder (Left → Root → Right) — BST cho thứ tự tăng dần!
def inorder(node):
    if not node: return
    inorder(node.left)
    print(node.val, end=" ")  # 4 2 5 1 3
    inorder(node.right)

# Preorder (Root → Left → Right) — Copy cây, serialize
def preorder(node):
    if not node: return
    print(node.val, end=" ")  # 1 2 4 5 3
    preorder(node.left)
    preorder(node.right)

# Postorder (Left → Right → Root) — Xóa cây, tính biểu thức
def postorder(node):
    if not node: return
    postorder(node.left)
    postorder(node.right)
    print(node.val, end=" ")  # 4 5 2 3 1

# BFS — Level Order (theo từng tầng)
from collections import deque

def level_order(root):
    if not root: return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.val, end=" ")  # 1 2 3 4 5
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
```

**Mẹo nhớ:**
```
In-order:   Left  ROOT Right  → "ROOT ở IN giữa"
Pre-order:  ROOT  Left Right  → "ROOT ở PRE trước"
Post-order: Left  Right ROOT  → "ROOT ở POST sau"
```

---

### Heap — Cây ưu tiên

**Min-Heap:** Node cha luôn ≤ node con (gốc là giá trị nhỏ nhất).

```
Min-Heap:        Max-Heap:
     1                9
    / \              / \
   3    5           7    8
  / \              / \
 7    9           3    5
```

```python
import heapq

# Min-heap trong Python
nums = [5, 3, 8, 1, 9]
heapq.heapify(nums)          # [1, 3, 8, 5, 9]
heapq.heappush(nums, 2)      # [1, 2, 8, 5, 9, 3]
smallest = heapq.heappop(nums)  # 1, heap: [2, 3, 8, 5, 9]

# Top K largest — O(n log k) thay vì sort O(n log n)
top_3 = heapq.nlargest(3, [5, 3, 8, 1, 9, 7])  # [9, 8, 7]
```

**Ứng dụng:** Priority queue, Dijkstra, K-th largest element, task scheduling.

---

## Phần 2: Graphs (Đồ thị)

### Khái niệm cơ bản

```
Undirected (Vô hướng):        Directed (Có hướng):
   A ── B                        A ──► B
   |  / |                        │     │
   | /  |                        ▼     ▼
   C ── D                        C ──► D

Weighted (Có trọng số):
   A ─5─ B
   |     |
   3     2
   |     |
   C ─1─ D
```

### Biểu diễn đồ thị

```python
# 1. Adjacency List (phổ biến nhất) — tốn ít bộ nhớ
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C'],
}

# Weighted graph
weighted_graph = {
    'A': [('B', 5), ('C', 3)],
    'B': [('A', 5), ('D', 2)],
    'C': [('A', 3), ('D', 1)],
    'D': [('B', 2), ('C', 1)],
}

# 2. Adjacency Matrix — truy cập O(1) nhưng tốn bộ nhớ O(V²)
#      A  B  C  D
# A  [ 0, 1, 1, 0 ]
# B  [ 1, 0, 1, 1 ]
# C  [ 1, 1, 0, 1 ]
# D  [ 0, 1, 1, 0 ]
```

---

### BFS — Breadth-First Search (Tìm kiếm theo chiều rộng)

Duyệt theo **từng tầng** — giống lan sóng:

```
Bắt đầu từ A:
Tầng 0: A
Tầng 1: B, C
Tầng 2: D, E
```

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

bfs(graph, 'A')  # A B C D
```

**Ứng dụng:** Đường đi ngắn nhất (unweighted), level-order traversal, social network "bạn bè chung".

---

### DFS — Depth-First Search (Tìm kiếm theo chiều sâu)

Đi **sâu nhất có thể** trước, rồi quay lại:

```python
# Đệ quy
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    print(node, end=" ")

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

dfs(graph, 'A')  # A B C D (thứ tự có thể khác)

# Dùng stack (iterative)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(node, end=" ")
            for neighbor in graph[node]:
                stack.append(neighbor)
```

**Ứng dụng:** Phát hiện cycle, topological sort, maze solving, connected components.

---

### Dijkstra — Đường đi ngắn nhất

Tìm đường đi ngắn nhất từ 1 đỉnh đến tất cả đỉnh khác (weighted graph):

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)

    while pq:
        dist, node = heapq.heappop(pq)

        if dist > distances[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return distances

# A ─5─ B
# |     |
# 3     2
# |     |
# C ─1─ D
result = dijkstra(weighted_graph, 'A')
# {'A': 0, 'B': 5, 'C': 3, 'D': 4}
# A→D ngắn nhất: A→C(3) + C→D(1) = 4, không phải A→B(5) + B→D(2) = 7
```

---

## Bảng tra nhanh

| Cấu trúc | Ưu điểm | Use case |
|---|---|---|
| **BST** | Tìm O(log n) | Search, sorted data |
| **Heap** | Min/Max O(1), Insert O(log n) | Priority queue, Top-K |
| **Trie** | Prefix search O(length) | Autocomplete, dictionary |
| **B-Tree** | Disk-friendly, balanced | Database index |
| **Graph + BFS** | Đường ngắn nhất (unweighted) | Social network, maze |
| **Graph + DFS** | Duyệt sâu, cycle detect | Topological sort, puzzle |
| **Dijkstra** | Đường ngắn nhất (weighted) | GPS, routing |

---

## Bài tập thực hành

- [ ] Implement BST đầy đủ (insert, search, delete, inorder)
- [ ] Tìm chiều cao của cây nhị phân (đệ quy)
- [ ] BFS tìm đường ngắn nhất trong mê cung (2D grid)
- [ ] Implement Dijkstra cho weighted graph
- [ ] Phát hiện cycle trong directed graph (DFS)

---

## Tài nguyên thêm

- [Visualgo — Binary Heap, BST, Graph](https://visualgo.net/) — Trực quan hóa tuyệt vời
- [LeetCode Tree Problems](https://leetcode.com/tag/tree/) — Luyện đề
- [Graph Theory Playlist (William Fiset)](https://www.youtube.com/playlist?list=PLDV1Zeh2NRsDGO4--qE8yH72HFL1Km93Y) — YouTube
