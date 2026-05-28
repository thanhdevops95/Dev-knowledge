# 🔗 Linked Lists — Danh sách liên kết

> `[BEGINNER → INTERMEDIATE]` — Cấu trúc dữ liệu nền tảng, hay gặp trong phỏng vấn

---

## Tại sao cần học Linked List?

**Array** lưu phần tử liên tiếp trong RAM → **chèn/xóa ở giữa tốn O(n)** vì phải dịch chuyển.

**Linked List** mỗi phần tử trỏ đến phần tử tiếp theo → **chèn/xóa O(1)** nếu có pointer.

```
Array:     [10][20][30][40][50]     ← Liên tiếp trong bộ nhớ
             ↓ chèn 25 ở giữa → phải dịch 30, 40, 50!

Linked List: 10 → 20 → 30 → 40 → 50
                   ↓ chèn 25
             10 → 20 → 25 → 30 → 40 → 50  ← Chỉ đổi 2 con trỏ!
```

---

## 1. Singly Linked List

Mỗi node chứa **data** + **con trỏ đến node tiếp theo**:

```
head
  │
  ▼
┌───┬───┐    ┌───┬───┐    ┌───┬───┐    ┌───┬──────┐
│ 10│ ●─┼──► │ 20│ ●─┼──► │ 30│ ●─┼──► │ 40│ null │
└───┴───┘    └───┴───┘    └───┴───┘    └───┴──────┘
 data next    data next    data next    data  next
```

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    # Thêm vào đầu: O(1)
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    # Thêm vào cuối: O(n) — phải duyệt đến cuối
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    # Xóa node theo giá trị: O(n)
    def delete(self, data):
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    # Tìm kiếm: O(n)
    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    # In danh sách
    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" → ".join(elements) + " → null")

# Sử dụng
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.prepend(5)
ll.display()    # 5 → 10 → 20 → 30 → null
ll.delete(20)
ll.display()    # 5 → 10 → 30 → null
```

---

## 2. Doubly Linked List

Mỗi node có **2 con trỏ**: prev (trước) + next (sau) → duyệt 2 chiều:

```
null ◄──┐          ┌──►  null
        │          │
      ┌─┴──┬───┬───┤  ┌───┬───┬───┐  ┌───┬───┬──┴┐
      │null│ 10│ ●─┼──►│ ◄─│ 20│ ●─┼──►│ ◄─│ 30│null│
      └────┴───┴───┘  └───┴───┴───┘  └───┴───┴────┘
       prev data next  prev data next  prev data next
```

```python
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = DoublyNode(data)
        if not self.tail:
            self.head = self.tail = new_node
            return
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    # Xóa node — dễ hơn singly (có prev pointer)
    def delete(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next  # Xóa head
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev  # Xóa tail
```

**Ứng dụng:** Browser history (back/forward), text editor cursor, LRU Cache.

---

## 3. Circular Linked List

Node cuối trỏ về head thay vì null:

```
     ┌──────────────────────────────┐
     │                              │
     ▼                              │
┌───┬───┐  ┌───┬───┐  ┌───┬───┐   │
│ 10│ ●─┼─►│ 20│ ●─┼─►│ 30│ ●─┼───┘
└───┴───┘  └───┴───┘  └───┴───┘
```

**Ứng dụng:** Round-robin scheduling, circular buffers, multiplayer game turn order.

---

## 4. Kỹ thuật phổ biến — Two Pointers

### Tìm node giữa

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # Nhảy 1
        fast = fast.next.next     # Nhảy 2
    return slow  # Khi fast đến cuối, slow ở giữa!

# 1 → 2 → 3 → 4 → 5
# slow:     3 (giữa!)
```

### Phát hiện vòng (cycle detection)

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True   # Có vòng!
    return False  # Không vòng (fast đến null)
```

### Đảo ngược Linked List

```python
def reverse(head):
    prev = None
    current = head
    while current:
        next_temp = current.next  # Lưu next
        current.next = prev       # Đổi hướng
        prev = current            # Tiến prev
        current = next_temp       # Tiến current
    return prev  # prev giờ là head mới

# Trước: 1 → 2 → 3 → null
# Sau:   3 → 2 → 1 → null
```

---

## 5. So sánh Array vs Linked List

| Thao tác | Array | Linked List |
|---|---|---|
| Truy cập index `[i]` | **O(1)** ⚡ | O(n) 🐌 |
| Tìm kiếm | O(n) | O(n) |
| Chèn đầu | O(n) 🐌 | **O(1)** ⚡ |
| Chèn cuối | O(1)* | O(1)** |
| Chèn giữa | O(n) | **O(1)*** |
| Xóa đầu | O(n) | **O(1)** |
| Bộ nhớ | Liên tiếp, cache-friendly | Phân tán, nhiều pointer overhead |

> *Amortized O(1) cho dynamic array  
> **O(1) nếu có tail pointer  
> ***O(1) nếu đã có pointer đến vị trí

**Khi nào dùng Linked List?**
- Chèn/xóa đầu thường xuyên
- Kích thước thay đổi liên tục
- Implement stack, queue, LRU cache

**Khi nào dùng Array?**
- Truy cập random index
- Cache performance quan trọng
- Dữ liệu ít thay đổi

---

## Các lỗi thường gặp

```
❌ Sai: Quên xử lý edge case — head = null, chỉ 1 node
✅ Đúng: LUÔN check null và single-node trước

❌ Sai: Mất pointer → memory leak hoặc mất dữ liệu
✅ Đúng: Lưu next_temp TRƯỚC khi đổi pointer

❌ Sai: Dùng linked list cho mọi thứ "vì O(1) insert"
✅ Đúng: Array thường nhanh hơn thực tế nhờ CPU cache locality
```

---

## Bài tập thực hành

- [ ] Implement Singly Linked List đầy đủ (insert, delete, search, reverse)
- [ ] Merge 2 sorted linked lists thành 1 sorted list
- [ ] Phát hiện vòng và tìm điểm bắt đầu vòng
- [ ] Implement LRU Cache dùng Doubly Linked List + HashMap

---

## Tài nguyên thêm

- [Visualgo — Linked List](https://visualgo.net/en/list) — Trực quan hóa thao tác
- [LeetCode Linked List Problems](https://leetcode.com/tag/linked-list/) — Luyện đề
