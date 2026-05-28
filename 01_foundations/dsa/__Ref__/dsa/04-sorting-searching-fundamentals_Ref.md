# 📊 Sorting & Searching — Sắp xếp và Tìm kiếm

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Thuật toán nền tảng mọi developer đều cần biết

---

## Tại sao cần học Sorting & Searching?

- Database sắp xếp hàng triệu bản ghi mỗi giây
- Google tìm kiếm trong hàng tỷ trang web chỉ 0.3 giây
- Bất kỳ app nào cũng có: *sort danh sách, tìm kiếm item*

Biết thuật toán đúng = **hiệu năng gấp 1000 lần** so với brute force.

---

## Phần 1: Sorting (Sắp xếp)

### Big O — Đánh giá hiệu năng

| Thuật toán | Best | Average | Worst | Space | Stable? |
|---|---|---|---|---|---|
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| **Selection Sort** | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | ❌ |

> **Stable** = giữ nguyên thứ tự các phần tử bằng nhau

---

### Bubble Sort — Đơn giản nhất (chỉ để hiểu, KHÔNG dùng thực tế)

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:   # Đã sorted → dừng sớm
            break
    return arr

# [5, 3, 8, 1] → [3, 5, 1, 8] → [3, 1, 5, 8] → [1, 3, 5, 8]
```

---

### Merge Sort — Chia để trị, ổn định

**Ý tưởng:** Chia mảng thành 2 nửa → sort từng nửa → merge.

```
[38, 27, 43, 3, 9, 82, 10]
        /              \
[38, 27, 43]      [3, 9, 82, 10]
   /     \           /        \
[38]  [27, 43]    [3, 9]   [82, 10]
       /   \       /  \      /    \
     [27] [43]   [3]  [9] [82]  [10]
       \   /       \  /      \    /
     [27, 43]    [3, 9]   [10, 82]
        \          /          /
   [27, 38, 43] [3, 9]  [10, 82]
         \         \       /
    [3, 9, 10, 27, 38, 43, 82]  ← Merge!
```

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

---

### Quick Sort — Nhanh nhất trung bình

**Ý tưởng:** Chọn pivot → phần tử nhỏ hơn qua trái, lớn hơn qua phải → đệ quy.

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# In-place version (tối ưu bộ nhớ)
def quick_sort_inplace(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

---

### Khi nào dùng thuật toán nào?

```
Dữ liệu nhỏ (< 50 phần tử)?
  → Insertion Sort (đơn giản, ít overhead)

Cần stable sort?
  → Merge Sort

Cần nhanh nhất trung bình, in-place?
  → Quick Sort

Đã gần sorted?
  → Insertion Sort (best case O(n)!)

Production code?
  → Dùng built-in sort (TimSort = Merge + Insertion)
    Python: sorted(), list.sort()
    JS: Array.sort()
    Java: Arrays.sort()
```

---

## Phần 2: Searching (Tìm kiếm)

### Linear Search — O(n)

```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

---

### Binary Search — O(log n) ⚡

**Yêu cầu:** Mảng đã được **sorted**.

```
Tìm 7 trong [1, 3, 5, 7, 9, 11, 13]:

Bước 1: mid = 7 → FOUND!

Tìm 3 trong [1, 3, 5, 7, 9, 11, 13]:

Bước 1: mid = 7, 3 < 7 → tìm bên trái [1, 3, 5]
Bước 2: mid = 3 → FOUND!

Mỗi bước loại bỏ NỬA mảng → log₂(n) bước
1 triệu phần tử → chỉ cần ~20 bước!
```

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1   # Tìm bên phải
        else:
            right = mid - 1  # Tìm bên trái

    return -1  # Không tìm thấy

# Đệ quy version
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1

    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

### Biến thể Binary Search

```python
# Tìm phần tử đầu tiên >= target (Lower Bound)
import bisect
arr = [1, 3, 5, 5, 5, 7, 9]
bisect.bisect_left(arr, 5)   # 2 (index đầu tiên = 5)
bisect.bisect_right(arr, 5)  # 5 (index sau phần tử cuối = 5)

# Tìm peak element
def find_peak(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        mid = (left + right) // 2
        if arr[mid] < arr[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left
```

---

## So sánh tốc độ thực tế

```
n = 1,000,000 phần tử:

Linear Search:   ~1,000,000 thao tác  → ~10ms
Binary Search:   ~20 thao tác         → ~0.001ms  (nhanh hơn 10,000x!)

Bubble Sort:     ~1,000,000,000,000   → ~vài giờ 😵
Quick Sort:      ~20,000,000          → ~0.5 giây
Merge Sort:      ~20,000,000          → ~0.7 giây
Python sorted(): ~20,000,000          → ~0.3 giây (TimSort optimized)
```

---

## Các lỗi thường gặp

```
❌ Sai: Binary search trên mảng chưa sorted → kết quả sai
✅ Đúng: LUÔN sort trước hoặc dùng sorted data structure (BST, B-Tree)

❌ Sai: mid = (left + right) / 2 → integer overflow khi left + right lớn
✅ Đúng: mid = left + (right - left) // 2

❌ Sai: Tự implement sort trong production
✅ Đúng: Dùng built-in sort (TimSort đã tối ưu sẵn)
```

---

## Bài tập thực hành

- [ ] Implement Merge Sort và Quick Sort từ đầu
- [ ] Binary Search: tìm căn bậc 2 của số nguyên (không dùng sqrt)
- [ ] Đếm số lần xuất hiện của target trong sorted array (dùng binary search)
- [ ] Sort mảng 1 triệu phần tử — so sánh thời gian bubble vs quick vs built-in

---

## Tài nguyên thêm

- [Sorting Algorithm Animations](https://www.toptal.com/developers/sorting-algorithms) — So sánh trực quan
- [Visualgo — Sorting](https://visualgo.net/en/sorting) — Từng bước animation
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/) — Tra cứu nhanh
