# Python Functions — `def`, args, return

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~25 phút\
> **Prerequisites:** [02_control-flow.md](./02_control-flow.md)

> 🎯 *Function giúp gom code lặp lại thành 1 "viên gạch" tái sử dụng. Sau bài này bạn viết được function nhận tham số, trả về kết quả, dùng `*args`/`**kwargs`.*

## 🎯 Sau bài này bạn sẽ

- [ ] Define function với `def`
- [ ] Truyền **positional** + **keyword** arguments
- [ ] Set **default values** cho parameters
- [ ] Dùng `*args` (tuple) và `**kwargs` (dict)
- [ ] Hiểu **scope** (local vs global)
- [ ] Viết **docstring** + **type hints**
- [ ] Hiểu **lambda** function

---

## 1️⃣ Vì sao cần Function (WHY)

Code không có function:

```python
# In ra "Hello" 3 lần với 3 tên khác nhau
print(f"Hello Rom! Welcome to Python.")
print(f"Hello Lan! Welcome to Python.")
print(f"Hello Hoa! Welcome to Python.")
```

Vấn đề:
- Lặp lại 3 lần — DRY violation
- Sửa câu chào → phải sửa 3 chỗ
- Logic phức tạp hơn → copy/paste cả block

Có function:

```python
def greet(name):
    print(f"Hello {name}! Welcome to Python.")

greet("Rom")
greet("Lan")
greet("Hoa")
```

→ **Function = đóng gói logic + tái sử dụng**. 

3 lợi ích chính:
1. **DRY** (Don't Repeat Yourself) — viết 1 lần, gọi nhiều lần
2. **Abstraction** — caller chỉ cần biết function làm gì, không quan tâm cách
3. **Testable** — function rời rạc dễ test (qua `pytest`)

---

## 2️⃣ Function là gì (WHAT)

**Định nghĩa**: Function = block code có **tên**, nhận **input** (parameters), thực hiện task, trả về **output** (return value).

**🪞 Ẩn dụ**: *Function như **máy xay sinh tố** — bỏ trái cây (input) → xay (logic) → ra ly sinh tố (output). Cùng 1 máy dùng cho nhiều loại trái cây khác nhau.*

### Anatomy của function

```python
def calculate_total(price, quantity):    # tên + parameters
    """Tính tổng tiền."""                 # docstring
    total = price * quantity              # body
    return total                          # return value
```

| Phần | Vai trò |
|---|---|
| `def` | Keyword khai báo function |
| `calculate_total` | **Tên** function (snake_case) |
| `(price, quantity)` | **Parameters** — input |
| `:` | Mở block |
| `"""..."""` | **Docstring** — mô tả function |
| Body | Logic |
| `return` | Trả về kết quả (optional) |

### Gọi function

```python
result = calculate_total(100, 3)
print(result)    # 300
```

---

## 3️⃣ Hands-on chi tiết (HOW)

### 🛠️ 3.1 Function đơn giản — không argument, không return

```python
def say_hello():
    print("Hello!")
    print("Welcome to Python.")

say_hello()    # gọi
say_hello()    # gọi lại
```

### 🛠️ 3.2 Function nhận parameter

```python
def greet(name):
    print(f"Hello {name}!")

greet("Rom")    # Hello Rom!
greet("Lan")    # Hello Lan!
```

→ `name` = parameter. `"Rom"` = argument truyền vào.

### 🛠️ 3.3 Function nhiều parameter

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)    # 8
```

### 🛠️ 3.4 Positional vs Keyword arguments

```python
def divide(numerator, denominator):
    return numerator / denominator

# Positional — đúng thứ tự
print(divide(10, 2))    # 5.0

# Keyword — đặt tên rõ ràng
print(divide(numerator=10, denominator=2))    # 5.0

# Mix — positional trước, keyword sau
print(divide(10, denominator=2))    # 5.0

# ❌ Sai — keyword trước positional
print(divide(numerator=10, 2))      # SyntaxError
```

→ **Best practice**: dùng keyword arguments khi function có >2 parameters — code đọc rõ hơn:

```python
# ❌ Khó hiểu
create_user("Rom", 28, True, False, "vi")

# ✅ Rõ ràng
create_user(
    name="Rom",
    age=28,
    is_active=True,
    is_admin=False,
    locale="vi"
)
```

### 🛠️ 3.5 Default values

```python
def greet(name, greeting="Hello"):
    print(f"{greeting} {name}!")

greet("Rom")                     # Hello Rom!
greet("Lan", "Hi")               # Hi Lan!
greet("Hoa", greeting="Chào")    # Chào Hoa!
```

⚠️ **Pitfall**: Default value mutable

```python
def add_item(item, items=[]):    # ❌ default list rỗng
    items.append(item)
    return items

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['a', 'b']   ❌ KHÔNG phải ['b']!
```

→ Default `[]` chỉ tạo 1 lần khi def. Các call sau share cùng list.

**Fix**:

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 🛠️ 3.6 `*args` — Variable positional arguments

Khi không biết trước có bao nhiêu argument:

```python
def sum_all(*numbers):
    """Cộng tất cả số truyền vào."""
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3))           # 6
print(sum_all(1, 2, 3, 4, 5))     # 15
print(sum_all())                   # 0
```

`*numbers` thu thập mọi positional argument thành **tuple**.

### 🛠️ 3.7 `**kwargs` — Variable keyword arguments

```python
def create_user(**fields):
    """Tạo user với fields tuỳ ý."""
    for key, value in fields.items():
        print(f"{key}: {value}")

create_user(name="Rom", age=28, email="rom@example.com")
```

```
name: Rom
age: 28
email: rom@example.com
```

`**fields` thu thập mọi keyword argument thành **dict**.

### 🛠️ 3.8 Combine `*args` + `**kwargs`

```python
def log(level, *messages, **metadata):
    print(f"[{level}]")
    for msg in messages:
        print(f"  Message: {msg}")
    for k, v in metadata.items():
        print(f"  {k}: {v}")

log("INFO", "App started", "Listening on port 8080", user="rom", env="prod")
```

```
[INFO]
  Message: App started
  Message: Listening on port 8080
  user: rom
  env: prod
```

> 💡 Thứ tự bắt buộc: `def func(positional, *args, **kwargs)`.

### 🛠️ 3.9 `return` — Trả về kết quả

```python
def square(x):
    return x ** 2

result = square(5)
print(result)    # 25
```

#### Return nhiều giá trị (tuple)

```python
def divmod_(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder    # tuple

q, r = divmod_(17, 5)
print(q, r)    # 3 2
```

→ Python tự pack thành tuple. Caller unpack thành 2 biến.

#### Function không có `return`

```python
def greet(name):
    print(f"Hello {name}!")

result = greet("Rom")    # Hello Rom!
print(result)             # None
```

→ Function không có `return` → tự trả về `None`.

#### Early return

```python
def divide(a, b):
    if b == 0:
        return None        # early return — tránh chia 0
    return a / b
```

→ Pattern phổ biến: check edge case → early return → tránh nested if.

---

## 4️⃣ Scope — Local vs Global

```python
x = 10    # global

def my_function():
    y = 20    # local
    print(x)  # đọc được global
    print(y)

my_function()
print(y)    # ❌ NameError: y không tồn tại ngoài function
```

### Modify global trong function

```python
counter = 0

def increment():
    counter = counter + 1    # ❌ UnboundLocalError

increment()
```

→ Python coi `counter = ...` là tạo biến **local** mới, nhưng `+1` cần đọc `counter` chưa định nghĩa local → lỗi.

**Fix**: dùng `global`:

```python
counter = 0

def increment():
    global counter
    counter = counter + 1

increment()
print(counter)    # 1
```

> ⚠️ **Tránh dùng `global`** trong code thực tế — gây side effect khó debug. Best: function nhận parameter + return value.

```python
# ✅ Pure function
def increment(c):
    return c + 1

counter = 0
counter = increment(counter)
```

### `nonlocal` — modify biến của outer function (nested function)

```python
def outer():
    count = 0
    
    def inner():
        nonlocal count
        count += 1
    
    inner()
    inner()
    print(count)    # 2

outer()
```

---

## 5️⃣ Docstring + Type hints (Best practice)

### Docstring — Mô tả function

```python
def calculate_bmi(weight, height):
    """
    Tính chỉ số BMI (Body Mass Index).
    
    Args:
        weight: Cân nặng (kg)
        height: Chiều cao (m)
    
    Returns:
        BMI (float) — phân loại: <18.5 thiếu cân, 18.5-25 bình thường, >25 thừa cân
    
    Example:
        >>> calculate_bmi(60, 1.7)
        20.76
    """
    return weight / (height ** 2)
```

Truy cập docstring:

```python
>>> help(calculate_bmi)
>>> print(calculate_bmi.__doc__)
```

→ IDE (VS Code) hover function thấy docstring.

### Type hints (Python 3.5+)

```python
def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)
```

→ Khai báo type giúp:
- IDE autocomplete tốt hơn
- `mypy` check static
- Người đọc hiểu nhanh

Type hints phức tạp hơn:

```python
def get_users(filter_active: bool = True) -> list[dict]:
    ...

def find_user(user_id: int) -> dict | None:    # có thể None
    ...

from typing import Optional
def find_user(user_id: int) -> Optional[dict]:  # cũ hơn — same nghĩa
    ...
```

> 💡 Type hints **không enforce runtime** — chỉ giúp tooling. Mới chuyển từ Java/TS quen, dùng nhiều — tốt cho project lớn.

---

## 6️⃣ Lambda — Function 1 dòng (anonymous)

```python
# Function thường
def square(x):
    return x ** 2

# Lambda tương đương
square = lambda x: x ** 2

print(square(5))    # 25
```

Format: `lambda <params>: <expression>` — KHÔNG có `return` keyword.

### Use case chính: argument cho function khác

```python
numbers = [1, 2, 3, 4, 5]

# Sort theo bình phương
sorted_numbers = sorted(numbers, key=lambda x: x ** 2)

# Filter số chẵn
even = list(filter(lambda x: x % 2 == 0, numbers))

# Map x^2
squares = list(map(lambda x: x ** 2, numbers))
```

> 💡 **Đa số trường hợp**: dùng list comprehension thay map/filter (đọc dễ hơn):
> ```python
> even = [x for x in numbers if x % 2 == 0]
> squares = [x ** 2 for x in numbers]
> ```

→ Lambda chỉ nên dùng khi function 1 dòng + dùng inline ngắn. Lambda dài → dùng `def` thường.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Default mutable argument (lặp lại §3.5)

```python
# ❌
def add(item, lst=[]):
    lst.append(item)
    return lst
```

→ Fix: `lst=None` + check.

### ❌ Pitfall: Function quá dài

Function 100+ dòng = khó test, khó hiểu.

- **Cách tránh**: 1 function = 1 task. Nếu dài → tách thành nhiều function nhỏ hơn.

### ❌ Pitfall: Side effect thầm lặng

```python
total = 0

def add_to_total(n):
    global total
    total += n
```

→ Caller không biết `add_to_total(5)` thay đổi `total`. Hard to debug.

- **Cách tránh**: **Pure function** — nhận input, return output, không touch state ngoài.

### ❌ Pitfall: Return nhiều type khác nhau

```python
def find(items, target):
    for item in items:
        if item == target:
            return item     # trả str
    return -1               # trả int
```

→ Caller không biết type return → bug.

- **Cách tránh**: nhất quán — return `None` khi không tìm thấy:
  ```python
  def find(items, target):
      for item in items:
          if item == target:
              return item
      return None
  ```

### ✅ Best practice: Tên function = verb phrase

```python
# ❌
def user(id): ...      # noun
def email(): ...

# ✅
def get_user(id): ...
def send_email(): ...
def validate_input(): ...
```

### ✅ Best practice: 1 function = 1 responsibility

```python
# ❌
def process_user(user):
    # validate
    if not user.email:
        raise ValueError("Email required")
    # save
    db.save(user)
    # send email
    smtp.send(user.email, "Welcome")
    # log
    logger.info(f"Created user {user.id}")
```

→ 4 việc trong 1 function. Khó test.

- **Fix**: tách
  ```python
  def validate_user(user): ...
  def save_user(user): ...
  def send_welcome_email(user): ...
  def log_user_created(user): ...

  def process_user(user):
      validate_user(user)
      save_user(user)
      send_welcome_email(user)
      log_user_created(user)
  ```

### ✅ Best practice: Docstring + type hints cho function public

```python
def calculate_discount(price: float, percent: int) -> float:
    """
    Tính giá sau khi discount.
    
    Args:
        price: Giá gốc
        percent: % discount (0-100)
    
    Returns:
        Giá sau discount
    """
    return price * (1 - percent / 100)
```

---

## 🧠 Self-check

**Q1.** Tại sao `def add(item, lst=[])` là pitfall?

<details>
<summary>💡 Đáp án</summary>

Default value `[]` được tạo **1 LẦN** khi function được define. Mọi call sau đó share cùng list đó:

```python
def add(item, lst=[]):
    lst.append(item)
    return lst

print(add("a"))    # ['a']
print(add("b"))    # ['a', 'b']   ❌
```

Fix: dùng `None` làm default, check trong body:

```python
def add(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

</details>

**Q2.** Sự khác nhau giữa `*args` và `**kwargs`?

<details>
<summary>💡 Đáp án</summary>

- `*args` — thu thập **positional arguments** thành **tuple**:
  ```python
  def f(*args):
      print(args)
  f(1, 2, 3)    # (1, 2, 3)
  ```

- `**kwargs` — thu thập **keyword arguments** thành **dict**:
  ```python
  def f(**kwargs):
      print(kwargs)
  f(name="Rom", age=28)    # {'name': 'Rom', 'age': 28}
  ```

Dùng combo: `def f(positional, *args, **kwargs):` — accept mọi kiểu input.

</details>

**Q3.** Function không có `return` trả về gì?

<details>
<summary>💡 Đáp án</summary>

Tự động trả về **`None`** (Python's null).

```python
def greet(name):
    print(f"Hi {name}")
    # không có return

result = greet("Rom")    # in "Hi Rom"
print(result)             # None
print(type(result))       # <class 'NoneType'>
```

→ Function side-effect (print, save DB, ...) thường không cần return. Function tính toán → luôn có return.

</details>

---

## ⚡ Cheatsheet

```python
# Define
def name(params):
    """Docstring."""
    ...
    return value

# Type hints
def name(x: int, y: str = "default") -> bool:
    ...

# Positional + keyword
def f(a, b, c=10):
    ...

f(1, 2)              # positional
f(1, 2, c=20)        # mix
f(a=1, b=2, c=3)     # all keyword

# *args (tuple)
def f(*args):
    for arg in args: ...
f(1, 2, 3)

# **kwargs (dict)
def f(**kwargs):
    for k, v in kwargs.items(): ...
f(name="Rom", age=28)

# Combine
def f(a, *args, b=10, **kwargs):
    ...

# Return
return value           # 1 giá trị
return a, b            # tuple
return None            # rỗng / sentinel
                       # không có return → None

# Lambda
square = lambda x: x ** 2

# Scope
global x       # đổi global var
nonlocal x     # đổi outer function var

# Higher-order (function as argument)
sorted(items, key=lambda x: x.age)
list(filter(lambda x: x > 0, nums))
list(map(lambda x: x * 2, nums))
```

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Function | Hàm | Block code có tên, nhận input, trả output |
| Parameter | Tham số | Biến trong định nghĩa function |
| Argument | Đối số | Giá trị truyền khi gọi |
| Positional argument | Đối số vị trí | Truyền theo thứ tự |
| Keyword argument | Đối số từ khóa | Truyền theo tên (`name=value`) |
| Default value | Giá trị mặc định | Tham số có sẵn nếu không truyền |
| `*args` | (giữ nguyên) | Thu thập positional args thành tuple |
| `**kwargs` | (giữ nguyên) | Thu thập keyword args thành dict |
| Return value | Giá trị trả về | Output của function |
| Scope | Phạm vi | Vùng biến tồn tại (local/global) |
| Local | Cục bộ | Biến trong function |
| Global | Toàn cục | Biến ngoài mọi function |
| Docstring | Chuỗi mô tả | `"""..."""` đầu function |
| Type hint | Gợi ý kiểu | `param: type` annotation |
| Lambda | (giữ nguyên) | Function 1 dòng (anonymous) |
| Pure function | Hàm thuần | Cùng input → cùng output, không side effect |
| Higher-order function | Hàm bậc cao | Function nhận function khác làm argument |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [02_control-flow.md](./02_control-flow.md) |
| ➡️ Bài tiếp | (sắp có) `04_io-and-files.md` — input, print, file IO |
| 🧭 Roadmap | [Zero to Coder — Stage 2](../../../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-2--python-từ-đầu-6-8-tuần) |

### Tài nguyên ngoài

- [Python Tutorial Ch.4.7 — Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Real Python — Functions](https://realpython.com/defining-your-own-python-function/)
- [PEP 257 — Docstring Convention](https://peps.python.org/pep-0257/)

---

## 📌 Changelog

- **v1.0.0 (16/05/2026)** — Bản đầu tiên — `def` + params + return + default + `*args`/`**kwargs` + scope + docstring + type hints + lambda + 6 pitfall/best-practice.
