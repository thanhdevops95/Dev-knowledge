# 📜 Design by Contract — Thiết kế theo Hợp đồng

> `[INTERMEDIATE]` — Không phụ thuộc ngôn ngữ cụ thể
> **Prerequisite:** `01-how-computers-work-fundamentals.md`, hiểu biết cơ bản về hàm và OOP

---

## Tại sao cần Design by Contract?

Hãy tưởng tượng bạn thuê thợ sửa ống nước. Trước khi bắt tay vào việc, cả hai bên **thỏa thuận rõ ràng**:
- **Bạn (caller):** Cung cấp nước sạch, mở van chính, trả tiền
- **Thợ (function):** Sửa xong ống không rò rỉ, hoàn thành trong 2 giờ
- **Bất biến:** Hệ thống ống không thay đổi cấu trúc tổng thể

Nếu bạn không mở van → thợ **không có nghĩa vụ** sửa. Nếu thợ sửa xong mà vẫn rò → thợ **vi phạm hợp đồng**.

**Design by Contract (DbC)** áp dụng ý tưởng này vào lập trình: mỗi function/module có **hợp đồng rõ ràng** gồm 3 thành phần:

| Thành phần | Ý nghĩa | Ai chịu trách nhiệm? |
|---|---|---|
| **Precondition** | Điều kiện phải đúng **trước khi** gọi function | Caller (người gọi) |
| **Postcondition** | Điều kiện phải đúng **sau khi** function trả về | Function (người được gọi) |
| **Invariant** | Điều kiện phải đúng **luôn luôn** (trước và sau mỗi method) | Class/Module |

> **Tại sao quan trọng?** DbC giúp phát hiện bug **sớm hơn** (fail fast), code **tự tài liệu** (self-documenting), và phân rõ **trách nhiệm** giữa caller và callee. Bertrand Meyer (người tạo ngôn ngữ Eiffel) phát triển khái niệm này năm 1986.

```
┌────────────────────────────────────────┐
│              CONTRACT                  │
│                                        │
│  Precondition:   "Input phải hợp lệ"  │
│         ↓                              │
│  ┌──────────────┐                      │
│  │   Function   │                      │
│  │  (thực thi)  │                      │
│  └──────────────┘                      │
│         ↓                              │
│  Postcondition: "Output đảm bảo đúng" │
│                                        │
│  Invariant: "Trạng thái luôn nhất quán"│
└────────────────────────────────────────┘
```

---

## 1. Preconditions — Điều kiện tiên quyết

**Precondition (tiền điều kiện)** là điều kiện mà **caller phải đảm bảo** trước khi gọi function. Nếu precondition bị vi phạm, function **không chịu trách nhiệm** cho kết quả sai.

Hãy nghĩ về precondition như **bảng hướng dẫn tại cửa vào**: "Vui lòng có vé trước khi vào rạp". Nếu bạn không có vé, rạp không có trách nhiệm cho bạn xem phim.

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """
    Calculate discounted price.
    
    Preconditions:
        - price > 0
        - 0 <= discount_percent <= 100
    """
    # Kiểm tra precondition — fail fast nếu caller vi phạm
    assert price > 0, f"Price must be positive, got {price}"
    assert 0 <= discount_percent <= 100, (
        f"Discount must be 0-100, got {discount_percent}"
    )
    
    return price * (1 - discount_percent / 100)
```

Ở đây, nếu caller gọi `calculate_discount(-50, 110)`, function sẽ **crash ngay lập tức** với thông báo rõ ràng, thay vì trả về kết quả vô nghĩa mà phải debug hàng giờ sau đó.

### Precondition trong các ngôn ngữ

```java
// Java — kiểm tra precondition bằng IllegalArgumentException
public double calculateDiscount(double price, double discountPercent) {
    if (price <= 0) {
        throw new IllegalArgumentException("Price must be positive: " + price);
    }
    if (discountPercent < 0 || discountPercent > 100) {
        throw new IllegalArgumentException("Discount must be 0-100: " + discountPercent);
    }
    return price * (1 - discountPercent / 100);
}
```

```go
// Go — return error thay vì panic
func CalculateDiscount(price, discountPercent float64) (float64, error) {
    if price <= 0 {
        return 0, fmt.Errorf("price must be positive, got %f", price)
    }
    if discountPercent < 0 || discountPercent > 100 {
        return 0, fmt.Errorf("discount must be 0-100, got %f", discountPercent)
    }
    return price * (1 - discountPercent/100), nil
}
```

---

## 2. Postconditions — Đảm bảo kết quả

**Postcondition (hậu điều kiện)** là điều kiện mà **function phải đảm bảo** khi trả về kết quả. Nếu postcondition bị vi phạm, đó là **bug trong function**.

Quay lại ví dụ thợ sửa ống nước: postcondition là "ống không rò rỉ sau khi sửa". Nếu vẫn rò → lỗi của thợ, không phải của bạn.

```python
def sort_list(items: list) -> list:
    """
    Sort a list of comparable items in ascending order.
    
    Precondition:  items is not None
    Postcondition: 
        - result is sorted (result[i] <= result[i+1] for all i)
        - result has same elements as items (same length, same content)
    """
    assert items is not None, "Input list must not be None"
    
    result = sorted(items)
    
    # Kiểm tra postcondition — đảm bảo function làm đúng
    assert len(result) == len(items), "Sort must preserve all elements"
    assert all(
        result[i] <= result[i + 1] for i in range(len(result) - 1)
    ), "Result must be sorted"
    
    return result
```

Postcondition giúp phát hiện bug **ngay trong function**, không đợi đến khi caller nhận kết quả sai rồi mới biết. Ví dụ, nếu ai đó viết thuật toán sort sai mà quên 1 phần tử, postcondition sẽ bắt ngay.

### Postcondition thực tế cho API

```python
def transfer_money(from_account: Account, to_account: Account, amount: float):
    """
    Transfer money between accounts.
    
    Precondition:  amount > 0, from_account.balance >= amount
    Postcondition: 
        - from_account.balance == old_from_balance - amount
        - to_account.balance == old_to_balance + amount
        - Total money in system unchanged (conservation)
    """
    assert amount > 0, "Transfer amount must be positive"
    assert from_account.balance >= amount, "Insufficient funds"
    
    old_total = from_account.balance + to_account.balance
    
    from_account.balance -= amount
    to_account.balance += amount
    
    # Postcondition: tiền không "biến mất" hoặc "sinh ra"
    new_total = from_account.balance + to_account.balance
    assert new_total == old_total, (
        f"Money conservation violated! Old: {old_total}, New: {new_total}"
    )
```

Postcondition `new_total == old_total` đảm bảo không có lỗi arithmetic hay race condition khiến tiền "bốc hơi". Đây là một **invariant kinh doanh** cực kỳ quan trọng trong fintech.

---

## 3. Class Invariants — Bất biến của đối tượng

**Invariant (bất biến)** là điều kiện phải đúng **mọi lúc** trên object/module — trước và sau mỗi public method. Nếu invariant bị phá vỡ, object ở trạng thái **không hợp lệ**.

Ví dụ đời thường: "Số dư tài khoản ngân hàng không bao giờ âm" — bất kể bạn nạp tiền, rút tiền, hay chuyển khoản, điều này **luôn đúng**.

```python
class BankAccount:
    """
    Invariant: balance >= 0 at all times
    """
    def __init__(self, owner: str, initial_balance: float = 0):
        assert initial_balance >= 0, "Initial balance must be non-negative"
        self.owner = owner
        self.balance = initial_balance
        self._check_invariant()
    
    def _check_invariant(self):
        """Verify class invariant holds"""
        assert self.balance >= 0, (
            f"INVARIANT VIOLATED: {self.owner}'s balance is {self.balance}"
        )
    
    def deposit(self, amount: float):
        # Precondition
        assert amount > 0, "Deposit amount must be positive"
        
        self.balance += amount
        
        # Check invariant sau mỗi operation
        self._check_invariant()
    
    def withdraw(self, amount: float):
        # Precondition
        assert amount > 0, "Withdraw amount must be positive"
        assert amount <= self.balance, "Insufficient funds"
        
        self.balance -= amount
        
        # Check invariant — nếu logic sai, bắt ngay
        self._check_invariant()
```

Mỗi method public **kết thúc bằng `_check_invariant()`**. Nếu bất kỳ method nào để balance âm, invariant sẽ fail ngay — không đợi đến khi hệ thống thanh toán xử lý sai tiền.

### Invariant cho data structure

```python
class SortedList:
    """
    A list that always maintains sorted order.
    
    Invariant: self._items[i] <= self._items[i+1] for all valid i
    """
    def __init__(self):
        self._items = []
    
    def _check_invariant(self):
        for i in range(len(self._items) - 1):
            assert self._items[i] <= self._items[i + 1], (
                f"Sort invariant violated at index {i}: "
                f"{self._items[i]} > {self._items[i+1]}"
            )
    
    def insert(self, value):
        # Binary search to find insertion point
        import bisect
        bisect.insort(self._items, value)
        self._check_invariant()
    
    def remove(self, value):
        self._items.remove(value)
        self._check_invariant()
```

---

## 4. Assertions trong thực tế

### Python `assert`

```python
# assert expression, "error message"
assert len(users) > 0, "User list cannot be empty"

# CẢNH BÁO: assert bị TẮT khi chạy python -O (optimize mode)
# → Không dùng assert cho validation input từ user/API
# → Chỉ dùng cho internal contract checking

# ❌ SAI: dùng assert cho user input
def login(username, password):
    assert username, "Username required"  # Bị tắt khi -O !

# ✅ ĐÚNG: dùng exception cho user input
def login(username, password):
    if not username:
        raise ValueError("Username is required")
```

Điểm quan trọng: `assert` dùng cho **contract (nội bộ)**, `raise` dùng cho **validation (bên ngoài)**. Contract là thỏa thuận giữa developer với developer, validation là kiểm tra input từ người dùng.

### Java `assert`

```java
// Java assert — phải bật bằng -ea flag khi chạy
public void processOrder(Order order) {
    assert order != null : "Order must not be null";
    assert order.getItems().size() > 0 : "Order must have items";
    
    // Process logic...
    
    assert order.getTotal() >= 0 : "Total cannot be negative";
}

// Chạy: java -ea MyApp
// Production thường TẮT assert để performance
```

### Go — Không có assert, dùng error + panic

```go
// Go philosophy: explicit error handling
func Withdraw(account *Account, amount float64) error {
    // Precondition — return error (expected failure)
    if amount <= 0 {
        return fmt.Errorf("amount must be positive: %f", amount)
    }
    if account.Balance < amount {
        return fmt.Errorf("insufficient funds: have %f, need %f",
            account.Balance, amount)
    }
    
    account.Balance -= amount
    
    // Invariant — panic (programming error, should never happen)
    if account.Balance < 0 {
        panic(fmt.Sprintf("INVARIANT VIOLATED: negative balance %f",
            account.Balance))
    }
    
    return nil
}
```

Go phân biệt rõ: `error` cho lỗi **dự đoán được** (precondition vi phạm bởi caller), `panic` cho **invariant violations** (bug thật sự trong code).

### Thư viện DbC chuyên dụng

```python
# Python: icontract (runtime contract checking)
# pip install icontract
import icontract

@icontract.require(lambda price: price > 0, "Price must be positive")
@icontract.require(lambda discount: 0 <= discount <= 100)
@icontract.ensure(lambda result: result >= 0, "Result must be non-negative")
def calculate_discount(price: float, discount: float) -> float:
    return price * (1 - discount / 100)
```

---

## 5. So sánh: Design by Contract vs Defensive Programming

| Tiêu chí | Design by Contract | Defensive Programming |
|---|---|---|
| **Triết lý** | "Nếu caller sai, crash ngay — đó là lỗi của caller" | "Không tin tưởng ai cả, kiểm tra mọi thứ" |
| **Precondition fail** | Crash (AssertionError) — lỗi caller | Return error code, giá trị mặc định, hoặc throw |
| **Khi nào dùng** | Internal APIs, library code, team agreements | Public APIs, user input, data từ bên ngoài |
| **Ưu điểm** | Code gọn, bug phát hiện nhanh, trách nhiệm rõ | An toàn, robust, không crash production |
| **Nhược điểm** | Crash production nếu không tắt assert | Code dài, che giấu bug |
| **Ngôn ngữ tiêu biểu** | Eiffel (built-in), Ada (SPARK) | Hầu hết ngôn ngữ |

### Khi nào dùng cách nào?

```
User input / External API data?
  → Defensive Programming (validate, return error)
  
Internal function contract?
  → Design by Contract (assert, fail fast)

Library public API?
  → Kết hợp: validate input (throw) + assert invariants

Production?
  → Tắt assert cho performance, giữ defensive checks
  
Testing / Development?
  → Bật assert tối đa để phát hiện bug sớm
```

### Ví dụ kết hợp

```python
class OrderService:
    def create_order(self, user_id: str, items: list[dict]) -> Order:
        # DEFENSIVE: validate external input
        if not user_id:
            raise ValueError("user_id is required")
        if not items:
            raise ValueError("Order must have at least one item")
        for item in items:
            if item.get("quantity", 0) <= 0:
                raise ValueError(f"Invalid quantity for {item.get('name')}")
        
        # Business logic
        order = Order(user_id=user_id)
        total = 0
        for item in items:
            total += item["price"] * item["quantity"]
            order.add_item(item)
        order.total = total
        
        # CONTRACT: internal invariant — bug nếu fail
        assert order.total >= 0, f"Order total cannot be negative: {order.total}"
        assert len(order.items) == len(items), "All items must be added"
        
        return order
```

---

## 6. DbC trong thiết kế API và Microservices

Trong kiến trúc hiện đại, DbC được mở rộng thành **API contracts**:

| Level | Contract | Tool |
|---|---|---|
| Function | Pre/Post/Invariant | assert, icontract |
| API | Request/Response schema | OpenAPI/Swagger, JSON Schema |
| Service | SLA, error codes | gRPC proto, API versioning |
| Team | Interface agreements | Consumer-driven contracts (Pact) |

```
API Contract ví dụ:

POST /api/orders
  Precondition:  Authorization header present, body has items[]
  Postcondition: 201 Created with order_id, Location header
  Invariant:     order_id is globally unique, total > 0
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Dùng `assert` để validate user input | Dùng `raise ValueError` | Assert bị tắt ở production (`python -O`) |
| 2 | Không check invariant sau mutation | Luôn check invariant sau mỗi public method | Bug có thể để object ở trạng thái invalid |
| 3 | Precondition quá strict | Chỉ check những gì function thực sự cần | Over-constraining giảm tính tái sử dụng |
| 4 | Postcondition có side effect | Postcondition chỉ nên **kiểm tra**, không **thay đổi** state | Check phải idempotent |
| 5 | Bỏ qua contract khi refactor | Giữ contract, cập nhật nếu behavior thay đổi | Contract là documentation sống |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Viết function `divide(a, b)` với precondition `b != 0`, postcondition `result * b ≈ a`. Dùng assert.
- [ ] **Bài 2 (Trung bình):** Tạo class `Stack` với invariant: `size >= 0` và `size <= max_capacity`. Implement push/pop/peek với contract checking.
- [ ] **Bài 3 (Khó):** Tạo class `CircularBuffer` với invariant checking. Đảm bảo: buffer size không vượt capacity, read pointer và write pointer luôn valid.
- [ ] **Bài 4 (Nâng cao):** Dùng thư viện `icontract` (Python) để viết contract cho một OrderService đơn giản. So sánh code với và không có DbC.

---

## Tài nguyên thêm

- [Design by Contract — Bertrand Meyer (Original Paper)](https://www.eiffel.com/values/design-by-contract/) — Nguồn gốc DbC
- [icontract — Python DbC Library](https://github.com/Parquery/icontract) — Runtime contract checking
- [Programming by Contract in Java (Cofoja)](https://github.com/nhatminhle/cofoja) — Java contracts
- [SPARK/Ada Formal Verification](https://www.adacore.com/about-spark) — DbC ở mức chứng minh toán học
- [Clean Code (Robert C. Martin)](https://www.oreilly.com/library/view/clean-code/9780136083238/) — Chương về hàm và trách nhiệm
