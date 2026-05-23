# 🏔️ Heaps & Priority Queues — Hàng đợi ưu tiên

> `[INTERMEDIATE]` — Prerequisite: `01-dsa-fundamentals.md`
> Cấu trúc dữ liệu quan trọng cho scheduling, shortest path, và Top-K problems.

---

## Tại sao cần Heap?

Hãy tưởng tượng phòng cấp cứu bệnh viện: bệnh nhân **không xếp hàng theo thứ tự đến** — ai nặng nhất được khám **trước**. Đây chính là **Priority Queue** (hàng đợi ưu tiên), và **Heap** là cấu trúc dữ liệu tối ưu nhất để implement nó.

| Thao tác | Sorted Array | Unsorted Array | **Binary Heap** |
|---|---|---|---|
| Insert | O(n) | O(1) | **O(log n)** |
| Get min/max | O(1) | O(n) | **O(1)** |
| Extract min/max | O(1)* → O(n) shift | O(n) | **O(log n)** |

> Heap cho phép **insert nhanh** (O(log n)) VÀ **lấy min/max nhanh** (O(1)) — best of both worlds.

---

## 1. Heap là gì?

**Binary Heap** là **complete binary tree** (cây nhị phân hoàn chỉnh) thỏa mãn **heap property**:

- **Min-Heap:** Parent ≤ Children (gốc là phần tử **nhỏ nhất**)
- **Max-Heap:** Parent ≥ Children (gốc là phần tử **lớn nhất**)

```
Min-Heap:                    Max-Heap:
      1                           9
     / \                         / \
    3   5                       7   6
   / \ / \                    / \ / \
  7  8 9  6                  3  5 1  4

Parent luôn ≤ children       Parent luôn ≥ children
Root = min = 1                Root = max = 9
```

### Lưu trữ bằng Array

Heap được lưu trữ hiệu quả bằng **array** (không cần pointers):

```
Index:    0  1  2  3  4  5  6
Array:  [ 1, 3, 5, 7, 8, 9, 6 ]

Parent(i)      = (i - 1) // 2
Left child(i)  = 2 * i + 1
Right child(i) = 2 * i + 2

Ví dụ: node ở index 1 (value=3)
  Parent:      (1-1)//2 = 0 (value=1) ✅ 1 ≤ 3
  Left child:  2*1+1 = 3 (value=7)    ✅ 3 ≤ 7
  Right child: 2*1+2 = 4 (value=8)    ✅ 3 ≤ 8
```

---

## 2. Heapify — Xây dựng và duy trì Heap

### Sift-Up (Bubble Up) — Khi insert phần tử mới

Thêm phần tử vào cuối array → "nổi lên" nếu nhỏ hơn parent (min-heap).

```python
class MinHeap:
    def __init__(self):
        self.heap = []
    
    def insert(self, val):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)
    
    def _sift_up(self, i):
        """Move element UP until heap property restored."""
        parent = (i - 1) // 2
        while i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent
            parent = (i - 1) // 2
```

```
Insert 2 vào Min-Heap [1, 3, 5, 7, 8, 9, 6]:

Step 1: Append → [1, 3, 5, 7, 8, 9, 6, 2]
                                         ^
Step 2: 2 < parent(7)? Yes → swap
         → [1, 3, 5, 2, 8, 9, 6, 7]
                      ^
Step 3: 2 < parent(3)? Yes → swap
         → [1, 2, 5, 3, 8, 9, 6, 7]
               ^
Step 4: 2 < parent(1)? No → done!
```

### Sift-Down (Bubble Down) — Khi extract phần tử gốc

Lấy gốc ra → đưa phần tử cuối lên gốc → "chìm xuống" nếu lớn hơn children.

```python
    def extract_min(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        
        min_val = self.heap[0]
        
        # Move last element to root
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        if self.heap:
            self._sift_down(0)
        
        return min_val
    
    def _sift_down(self, i):
        """Move element DOWN until heap property restored."""
        n = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            
            if smallest == i:
                break  # Heap property satisfied
            
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest
    
    def peek(self):
        """Get min without removing — O(1)."""
        return self.heap[0] if self.heap else None
```

### Build Heap from Array — O(n)

```python
def heapify(arr):
    """Convert array to min-heap IN-PLACE — O(n)."""
    n = len(arr)
    # Start from last non-leaf node, sift down each
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)

def sift_down(arr, n, i):
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        sift_down(arr, n, smallest)

# Build heap: O(n) — KHÔNG phải O(n log n)!
# Bởi vì đa số nodes ở gần lá, sift_down rất ngắn
data = [9, 3, 7, 1, 5, 8, 2]
heapify(data)
print(data)  # [1, 3, 2, 9, 5, 8, 7] — min-heap!
```

---

## 3. Heap Sort — O(n log n) guaranteed

**Heap Sort** dùng heap để sort: build max-heap → extract max lặp lại → array sorted tăng dần.

```python
def heap_sort(arr):
    n = len(arr)
    
    # 1. Build max-heap — O(n)
    for i in range(n // 2 - 1, -1, -1):
        max_sift_down(arr, n, i)
    
    # 2. Extract max one by one — O(n log n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move max to end
        max_sift_down(arr, i, 0)         # Restore heap (size shrinks)

def max_sift_down(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_sift_down(arr, n, largest)

data = [12, 11, 13, 5, 6, 7]
heap_sort(data)
print(data)  # [5, 6, 7, 11, 12, 13]
```

| So sánh | Heap Sort | Quick Sort | Merge Sort |
|---|---|---|---|
| **Worst case** | O(n log n) ✅ | O(n²) ❌ | O(n log n) ✅ |
| **Space** | O(1) in-place ✅ | O(log n) | O(n) ❌ |
| **Stable?** | ❌ | ❌ | ✅ |
| **Cache-friendly?** | ❌ (random access) | ✅ (sequential) | ✅ |

Heap Sort có worst case tốt và space O(1), nhưng **cache-unfriendly** nên thực tế thường chậm hơn Quick Sort.

---

## 4. Priority Queue — Interface trừu tượng

**Priority Queue** là abstract data type — Heap là implementation phổ biến nhất.

### Python `heapq` — Min-Heap built-in

```python
import heapq

# Min-heap operations
pq = []
heapq.heappush(pq, 5)
heapq.heappush(pq, 1)
heapq.heappush(pq, 3)

print(heapq.heappop(pq))  # 1 (smallest)
print(heapq.heappop(pq))  # 3
print(heapq.heappop(pq))  # 5

# Max-heap trick: negate values
max_pq = []
heapq.heappush(max_pq, -10)
heapq.heappush(max_pq, -20)
heapq.heappush(max_pq, -5)
print(-heapq.heappop(max_pq))  # 20 (largest)

# Priority Queue with custom objects
tasks = []
heapq.heappush(tasks, (1, "Critical bug"))   # (priority, task)
heapq.heappush(tasks, (3, "Nice-to-have"))
heapq.heappush(tasks, (2, "Feature request"))

while tasks:
    priority, task = heapq.heappop(tasks)
    print(f"[P{priority}] {task}")
# [P1] Critical bug
# [P2] Feature request
# [P3] Nice-to-have
```

### Ứng dụng Priority Queue

```
1. Task Scheduling:    OS scheduler — process có priority cao chạy trước
2. Dijkstra:           Shortest path — luôn explore node gần nhất
3. Huffman Coding:     Compression — merge 2 nodes tần suất thấp nhất
4. Event Simulation:   Game loop — process event có timestamp sớm nhất
5. Merge K sorted:     Merge K sorted lists bằng min-heap size K
```

---

## 5. Top-K Problems — Min-Heap cho Top-K largest

### Bài toán: Tìm K phần tử lớn nhất

```python
import heapq

def top_k_largest(nums: list, k: int) -> list:
    """
    Find K largest elements using min-heap of size K.
    Time: O(n log k), Space: O(k)
    """
    # Dùng min-heap size K
    # Gốc heap = phần tử nhỏ nhất trong K lớn nhất
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    
    for num in nums[k:]:
        if num > min_heap[0]:  # Lớn hơn phần tử nhỏ nhất?
            heapq.heapreplace(min_heap, num)  # Pop min + push new
    
    return sorted(min_heap, reverse=True)

print(top_k_largest([3, 1, 4, 1, 5, 9, 2, 6], k=3))
# [9, 6, 5]
```

Tại sao dùng **min-heap** cho **top-K largest**? Vì gốc min-heap là "ngưỡng" — bất kỳ phần tử nào nhỏ hơn ngưỡng sẽ bị loại. Giữ heap size = K → O(n log K) thay vì sort toàn bộ O(n log n).

---

## 6. Kth Largest Element — Quickselect vs Heap

```python
# Cách 1: Heap — O(n log k)
def kth_largest_heap(nums, k):
    return heapq.nlargest(k, nums)[-1]

# Cách 2: Quickselect — O(n) average, O(n²) worst
import random

def kth_largest_quickselect(nums, k):
    """Find kth largest — average O(n)."""
    k = len(nums) - k  # Convert to kth smallest
    
    def quickselect(left, right):
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]
        
        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]
        
        if store == k:
            return nums[store]
        elif store < k:
            return quickselect(store + 1, right)
        else:
            return quickselect(left, store - 1)
    
    return quickselect(0, len(nums) - 1)

# So sánh:
# Heap:        O(n log k) — stable, predictable
# Quickselect: O(n) avg   — faster nhưng worst case O(n²)
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Python `heapq` là max-heap | Python `heapq` là **min-heap** | Dùng negate (-x) cho max-heap |
| 2 | Heap là sorted array | Heap chỉ đảm bảo parent ≤ children | [1, 3, 2] là valid min-heap (3 > 2 OK vì khác nhánh) |
| 3 | Build heap = N lần insert = O(n log n) | Build heap bằng `heapify` = O(n) | Heapify bottom-up nhanh hơn N inserts |
| 4 | Dùng heap cho range queries | Heap không hỗ trợ range queries | Dùng BST hoặc sorted array cho range |
| 5 | Quên handle duplicate priorities | Thêm tiebreaker (counter) | `(priority, counter, task)` tránh compare error |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Implement MinHeap class từ đầu (insert, extract_min, peek)
- [ ] **Bài 2 (Trung bình):** LeetCode 703 — Kth Largest Element in a Stream
- [ ] **Bài 3 (Trung bình):** LeetCode 347 — Top K Frequent Elements (dùng heap)
- [ ] **Bài 4 (Khó):** LeetCode 23 — Merge K Sorted Lists (dùng min-heap size K)
- [ ] **Bài 5 (Khó):** LeetCode 295 — Find Median from Data Stream (2 heaps: max-heap + min-heap)

---

## Tài nguyên thêm

- [Visualgo — Heap](https://visualgo.net/en/heap) — Trực quan hóa heap operations
- [Python heapq Documentation](https://docs.python.org/3/library/heapq.html) — Official docs
- [NeetCode — Heap/Priority Queue](https://neetcode.io/roadmap) — Video giải LeetCode
- [CLRS Chapter 6 — Heapsort](https://mitpress.mit.edu/9780262046305/) — Sách giáo khoa algorithms
