# 🏃 Greedy Algorithms — Thuật toán Tham lam

> `[INTERMEDIATE]` — Prerequisite: `01-dsa-fundamentals.md`
> Kỹ thuật chọn lựa **tối ưu cục bộ** tại mỗi bước, hy vọng đạt **tối ưu toàn cục**.

---

## Tại sao cần Greedy?

Hãy tưởng tượng bạn đi siêu thị có 50.000đ, muốn mua **nhiều loại trái cây nhất** có thể. Chiến lược tham lam: **luôn chọn loại rẻ nhất** trước → mua được nhiều loại nhất. Đơn giản, nhanh, và trong trường hợp này **chính xác tối ưu**.

Greedy algorithm chọn **quyết định tốt nhất tại mỗi bước** mà **không quay lại** (no backtracking). Mỗi quyết định là **final**.

| | Greedy | DP | Brute Force |
|---|---|---|---|
| **Cách hoạt động** | Chọn best tại mỗi bước | Thử mọi bài con, ghi nhớ | Thử mọi tổ hợp |
| **Time** | Thường O(n log n) | O(n²) hoặc O(n × W) | O(2ⁿ) |
| **Tối ưu?** | Chỉ khi có greedy property | Luôn tối ưu | Luôn tối ưu |
| **Dễ code?** | ✅ Rất dễ | Trung bình | Dễ nhưng chậm |

---

## 1. Greedy Choice Property — Khi nào Greedy đúng?

Greedy chỉ cho kết quả tối ưu khi bài toán có **2 tính chất**:

1. **Greedy Choice Property:** Chọn lựa tối ưu cục bộ → dẫn đến tối ưu toàn cục
2. **Optimal Substructure:** Lời giải tối ưu chứa lời giải tối ưu của bài con

Nếu thiếu greedy choice property → **greedy cho kết quả sai**, phải dùng DP.

```
✅ Greedy ĐÚNG:
  Đổi tiền (coins = [1, 5, 10, 25]): chọn đồng lớn nhất trước
  25 + 25 + 10 + 5 + 1 + 1 + 1 + 1 + 1 = 70¢ ← tối ưu!

❌ Greedy SAI:
  Đổi tiền (coins = [1, 3, 4]): đổi 6
  Greedy: 4 + 1 + 1 = 3 đồng
  Optimal: 3 + 3 = 2 đồng ← greedy không tìm được!
```

---

## 2. Activity Selection — Bài toán kinh điển

**Bài toán:** Có N hoạt động, mỗi hoạt động có (start, end). Chọn **nhiều hoạt động nhất** mà không overlap.

**Greedy strategy:** Luôn chọn hoạt động **kết thúc sớm nhất** (earliest finish time).

```python
def activity_selection(activities: list[tuple[int, int]]) -> list:
    """
    Select maximum non-overlapping activities.
    Greedy: always pick activity that finishes earliest.
    
    Proof: Nếu có optimal solution KHÔNG chọn activity finish sớm nhất,
    ta có thể THAY activity đầu tiên bằng activity finish sớm nhất
    mà vẫn giữ nguyên số lượng (vì nó finish sớm hơn, không block nhiều hơn).
    """
    # Sort by finish time
    sorted_acts = sorted(activities, key=lambda x: x[1])
    
    selected = [sorted_acts[0]]
    last_end = sorted_acts[0][1]
    
    for start, end in sorted_acts[1:]:
        if start >= last_end:  # No overlap
            selected.append((start, end))
            last_end = end
    
    return selected

activities = [(1, 3), (2, 5), (4, 7), (1, 8), (5, 9), (8, 10)]
print(activity_selection(activities))
# [(1, 3), (4, 7), (8, 10)] — 3 activities (maximum!)
```

```
Timeline:
|---A1---|
  |------A2------|
     |-------A3-------|
|------------A4------------|
        |--------A5--------|
                  |---A6---|

Greedy picks: A1(1-3), A3(4-7), A6(8-10) ← maximum 3
```

---

## 3. Huffman Coding — Nén dữ liệu

**Bài toán:** Gán mã nhị phân cho ký tự sao cho **tổng số bit nhỏ nhất**. Ký tự xuất hiện nhiều → mã ngắn.

**Greedy strategy:** Luôn merge **2 nodes tần suất thấp nhất** trước (dùng min-heap).

```python
import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding(text: str) -> dict:
    # Count frequency
    freq = Counter(text)
    
    # Build priority queue
    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)
    
    # Greedy: merge 2 lowest frequency nodes
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)
    
    # Generate codes by traversing tree
    codes = {}
    def generate(node, code=""):
        if node.char:
            codes[node.char] = code
            return
        generate(node.left, code + "0")
        generate(node.right, code + "1")
    
    generate(heap[0])
    return codes

text = "aaaaabbbccde"
codes = huffman_coding(text)
print(codes)
# Possible: {'a': '0', 'b': '10', 'c': '110', 'd': '1110', 'e': '1111'}
# a (5x) = 1 bit, b (3x) = 2 bits — ký tự phổ biến = mã ngắn!
```

Huffman coding được dùng trong **ZIP, GZIP, PNG, JPEG, MP3** — nền tảng của data compression.

---

## 4. Interval Scheduling — Non-overlapping Intervals

**Bài toán:** Xóa ít interval nhất để không còn overlap.

```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """
    LeetCode 435 — Minimum removals for non-overlapping.
    Greedy: keep interval with earliest end time.
    """
    intervals.sort(key=lambda x: x[1])
    
    removals = 0
    prev_end = float('-inf')
    
    for start, end in intervals:
        if start >= prev_end:
            prev_end = end  # Keep this interval
        else:
            removals += 1   # Remove (overlap with previous)
    
    return removals

print(erase_overlap_intervals([[1,2],[2,3],[3,4],[1,3]]))
# 1 — remove [1,3], keep [1,2],[2,3],[3,4]
```

---

## 5. Dijkstra as Greedy — Shortest Path

Dijkstra's algorithm là **greedy**: luôn explore node có **khoảng cách ngắn nhất** hiện tại.

```python
import heapq

def dijkstra(graph: dict, start: str) -> dict:
    """
    Greedy: always process nearest unvisited node.
    Works for non-negative edge weights only.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        curr_dist, curr = heapq.heappop(pq)
        
        if curr_dist > distances[curr]:
            continue  # Already found shorter path
        
        for neighbor, weight in graph[curr]:
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    
    return distances

graph = {
    'A': [('B', 4), ('C', 1)],
    'B': [('D', 1)],
    'C': [('B', 2), ('D', 5)],
    'D': [],
}
print(dijkstra(graph, 'A'))
# {'A': 0, 'B': 3, 'C': 1, 'D': 4}
# Path A→D: A→C(1)→B(3)→D(4) thay vì A→B(4)→D(5)
```

**Tại sao Dijkstra work?** Vì edge weights **non-negative** → node đã processed sẽ KHÔNG bao giờ tìm được đường ngắn hơn → greedy choice safe.

**Nếu có negative edges?** Dijkstra **SAI** → dùng Bellman-Ford (DP-based).

---

## 6. Greedy vs DP — Khi nào dùng gì?

| Tiêu chí | Greedy | DP |
|---|---|---|
| **Khi nào đúng** | Bài toán có greedy choice property | Luôn đúng (nếu có optimal substructure) |
| **Tốc độ** | Thường nhanh hơn (O(n log n)) | Chậm hơn (O(n²), O(n × W)) |
| **Dễ chứng minh** | Khó — phải prove greedy works | Dễ — transition formula |
| **Khi không chắc** | Thử greedy → verify | Fallback sang DP |

```
Fractional Knapsack (cắt được item)?
  → Greedy: lấy ratio value/weight cao nhất trước

0/1 Knapsack (không cắt được)?
  → DP: greedy KHÔNG tối ưu

Coin Change (coins = [1, 5, 10, 25])?
  → Greedy: chọn đồng lớn nhất trước

Coin Change (coins = [1, 3, 4])?
  → DP: greedy KHÔNG tối ưu
```

### Các bài Greedy kinh điển

| Bài toán | Greedy Strategy | Complexity |
|---|---|---|
| Activity Selection | Earliest finish time | O(n log n) |
| Huffman Coding | Merge lowest frequencies | O(n log n) |
| Fractional Knapsack | Highest value/weight ratio | O(n log n) |
| Dijkstra | Process nearest node | O((V+E) log V) |
| Prim's MST | Add cheapest edge | O(E log V) |
| Kruskal's MST | Add cheapest edge (no cycle) | O(E log E) |
| Task Scheduling | Earliest deadline | O(n log n) |

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | "Greedy luôn tối ưu" | Greedy chỉ tối ưu khi có greedy property | Phải chứng minh hoặc verify |
| 2 | Dijkstra với negative edges | Dùng Bellman-Ford cho negative edges | Negative edges phá greedy assumption |
| 3 | Quên sort trước khi greedy | Sort là bước đầu tiên của hầu hết greedy | Activity selection cần sort by end time |
| 4 | Greedy cho 0/1 Knapsack | 0/1 Knapsack cần DP | Greedy chỉ đúng cho Fractional Knapsack |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** LeetCode 455 — Assign Cookies (greedy matching)
- [ ] **Bài 2 (Trung bình):** LeetCode 435 — Non-overlapping Intervals
- [ ] **Bài 3 (Trung bình):** LeetCode 621 — Task Scheduler
- [ ] **Bài 4 (Trung bình):** Implement Huffman Coding + Decoding
- [ ] **Bài 5 (Khó):** LeetCode 45 — Jump Game II (greedy BFS)

---

## Tài nguyên thêm

- [CLRS Chapter 16 — Greedy Algorithms](https://mitpress.mit.edu/9780262046305/) — Sách giáo khoa
- [NeetCode Greedy Playlist](https://neetcode.io/) — Video giải LeetCode
- [Visualgo — Greedy](https://visualgo.net/) — Trực quan hóa thuật toán
- [Greedy Algorithms (GeeksforGeeks)](https://www.geeksforgeeks.org/greedy-algorithms/) — Bài tập + lý thuyết
