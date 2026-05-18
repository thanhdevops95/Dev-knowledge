# Python Variables + Data Types — Biến và 7 kiểu dữ liệu cốt lõi

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~25 phút\
> **Prerequisites:** [00_what-is-python.md](./00_what-is-python.md), đã có Python REPL chạy được

> 🎯 *Học **biến** + **7 kiểu dữ liệu cốt lõi**: int, float, str, bool, list, dict, tuple, set. Đây là viên gạch xây mọi thứ khác trong Python.*

## 🎯 Sau bài này bạn sẽ

- [ ] Tạo + dùng **biến** (variable)
- [ ] Hiểu **dynamic typing** của Python
- [ ] Dùng thành thạo 4 kiểu primitive: `int`, `float`, `str`, `bool`
- [ ] Dùng thành thạo 4 kiểu collection: `list`, `dict`, `tuple`, `set`
- [ ] Chuyển đổi kiểu (type casting)
- [ ] Phân biệt **mutable** vs **immutable**

---

## 1️⃣ Vì sao học biến + kiểu dữ liệu trước (WHY)

Mọi chương trình = **dữ liệu** + **logic**. Trước khi viết logic (if/for), bạn phải hiểu **lưu dữ liệu thế nào**:

| Bạn muốn lưu | Kiểu dữ liệu |
|---|---|
| Tuổi (28) | `int` |
| Lương (1.5 triệu) | `float` |
| Tên ("Rom") | `str` |
| Đăng nhập rồi (Yes/No) | `bool` |
| Danh sách bạn bè (5 người, có thể thêm/bớt) | `list` |
| Thông tin user (tên + tuổi + email) | `dict` |
| Ngày sinh (3 phần: năm, tháng, ngày — KHÔNG đổi) | `tuple` |
| Tag duy nhất (không trùng) | `set` |

→ Hiểu 7 kiểu trên = hiểu **70% việc xử lý dữ liệu** trong Python.

---

## 2️⃣ Biến (Variable) là gì (WHAT)

**Định nghĩa**: Biến là **tên** trỏ tới 1 **giá trị** trong memory. Đặt tên = "dán nhãn" lên giá trị.

**🪞 Ẩn dụ**: *Biến giống như **nhãn dán trên hộp**. `name = "Rom"` = "dán nhãn 'name' lên hộp chứa chữ Rom". Khi gọi `name`, Python tìm hộp có nhãn đó và lấy nội dung.*

### Cú pháp gán biến

```python
<tên_biến> = <giá_trị>
```

Ví dụ:

```python
age = 28
name = "Rom"
is_logged_in = True
```

### Dynamic typing — Python tự đoán type

Khác với Java/C (phải khai báo `int age = 28;`), Python tự detect:

```python
>>> age = 28
>>> type(age)
<class 'int'>

>>> age = "twenty-eight"   # đổi sang str được luôn
>>> type(age)
<class 'str'>
```

→ Cùng biến `age` lúc là `int`, lúc là `str`. Python không cấm. **Nhưng** code maintain khó vì biến không "ổn định" type.

> 💡 **Best practice**: 1 biến nên giữ 1 type xuyên suốt. Cần đổi type → tạo biến mới (`age_str = str(age)`).

### Quy tắc đặt tên biến

| ✅ Đúng | ❌ Sai | Lý do |
|---|---|---|
| `age` | `Age` | Convention: snake_case, không Pascal |
| `user_name` | `userName` | Convention: snake_case, không camel |
| `_private` | `1user` | Tên không bắt đầu bằng số |
| `email` | `e-mail` | Không có `-` |
| `is_active` | `is active` | Không có space |
| `count_v2` | `class` | Không trùng keyword (`class`, `def`, `if`, ...) |

### PEP 8 — Python style guide

[PEP 8](https://peps.python.org/pep-0008/) là chuẩn naming Python:

- **Variable / function**: `snake_case` — `user_name`, `calculate_total`
- **Class**: `PascalCase` — `UserAccount`, `HttpClient`
- **Constant**: `UPPER_CASE` — `MAX_RETRY`, `API_KEY`
- **Private**: prefix `_` — `_internal_helper`

---

## 3️⃣ 4 kiểu primitive (HOW)

### 🛠️ 3.1 `int` — Số nguyên

```python
age = 28
year = 2026
negative = -42
big_number = 1_000_000   # _ là dấu phân cách (Python 3.6+) — đọc dễ hơn 1000000
```

Phép toán:

```python
>>> 5 + 3
8
>>> 10 - 4
6
>>> 6 * 7
42
>>> 17 / 5      # chia thường — trả về float
3.4
>>> 17 // 5     # chia nguyên — trả về int
3
>>> 17 % 5      # phần dư (modulo)
2
>>> 2 ** 10     # lũy thừa
1024
```

> 💡 *Python tự xử lý số nguyên cực lớn — không bị overflow như Java/C*:
> ```python
> >>> 2 ** 100
> 1267650600228229401496703205376
> ```

### 🛠️ 3.2 `float` — Số thực

```python
price = 19.99
pi = 3.14159
scientific = 1.5e3     # 1500.0
```

> ⚠️ **Pitfall**: float không chính xác tuyệt đối (do binary representation):
> ```python
> >>> 0.1 + 0.2
> 0.30000000000000004    # KHÔNG bằng 0.3 chính xác!
> ```
> → Khi cần chính xác (tiền tệ, khoa học), dùng `decimal.Decimal` thay `float`.

### 🛠️ 3.3 `str` — Chuỗi

3 cách viết:

```python
single = 'Hello'
double = "World"
multi = """Multi-line
string"""
```

Phép toán:

```python
>>> "Hello" + " " + "World"      # concat
'Hello World'

>>> "ab" * 3                      # repeat
'ababab'

>>> len("Python")                 # độ dài
6

>>> "Python"[0]                   # char đầu (index từ 0)
'P'

>>> "Python"[-1]                  # char cuối
'n'

>>> "Python"[0:3]                 # slice [start:end)
'Pyt'

>>> "Python".upper()
'PYTHON'

>>> "Python".lower()
'python'

>>> "Python".replace("y", "Y")
'PYthon'

>>> "Hello, World".split(", ")    # split thành list
['Hello', 'World']

>>> "-".join(["2026", "05", "16"])
'2026-05-16'
```

#### f-string — Format string (Python 3.6+, RECOMMEND)

```python
name = "Rom"
age = 28
print(f"Tên: {name}, Tuổi: {age}")
# Tên: Rom, Tuổi: 28
```

Tính trong f-string:

```python
price = 99
print(f"Giá: {price * 1000:,} VND")
# Giá: 99,000 VND
```

> 💡 f-string thay 3 cú pháp cũ (`%` format, `.format()`, concat). **Luôn dùng f-string** trong Python 3.6+.

### 🛠️ 3.4 `bool` — Boolean (True/False)

```python
is_active = True
is_admin = False
```

⚠️ Viết hoa `T` và `F` — Python case-sensitive. `true` (lowercase) sẽ báo lỗi.

Phép toán logic:

```python
>>> True and False
False

>>> True or False
True

>>> not True
False
```

Phép so sánh trả `bool`:

```python
>>> 5 > 3
True

>>> "abc" == "abc"
True

>>> "abc" != "ABC"
True
```

#### Truthy / Falsy values

Python có "values đánh giá như False" khi cast sang bool:

```python
>>> bool(0)        # False
>>> bool(0.0)      # False
>>> bool("")       # False (empty string)
>>> bool([])       # False (empty list)
>>> bool({})       # False (empty dict)
>>> bool(None)     # False
>>> bool(42)       # True
>>> bool("hello")  # True
```

→ Hữu ích trong `if`:

```python
name = ""
if name:
    print(f"Hello {name}")
else:
    print("Tên trống!")   # ← chạy đây vì "" là Falsy
```

---

## 4️⃣ 4 kiểu collection

### 🛠️ 4.1 `list` — Danh sách thứ tự, có thể đổi

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = ["Rom", 28, True, 3.14]    # list mix nhiều type được
empty = []
```

Truy cập:

```python
>>> fruits[0]           # phần tử đầu
'apple'
>>> fruits[-1]          # phần tử cuối
'cherry'
>>> fruits[1:3]         # slice
['banana', 'cherry']
```

Thay đổi:

```python
>>> fruits.append("orange")        # thêm cuối
>>> fruits
['apple', 'banana', 'cherry', 'orange']

>>> fruits.insert(0, "mango")      # thêm vào vị trí
>>> fruits
['mango', 'apple', 'banana', 'cherry', 'orange']

>>> fruits.remove("apple")          # xóa theo value
>>> fruits
['mango', 'banana', 'cherry', 'orange']

>>> fruits.pop()                    # xóa cuối + trả về
'orange'

>>> fruits[0] = "kiwi"              # thay vị trí
>>> fruits
['kiwi', 'banana', 'cherry']

>>> len(fruits)
3
```

#### List comprehension — đặc trưng Pythonic

```python
>>> numbers = [1, 2, 3, 4, 5]
>>> squares = [n ** 2 for n in numbers]
>>> squares
[1, 4, 9, 16, 25]

>>> even_squares = [n ** 2 for n in numbers if n % 2 == 0]
>>> even_squares
[4, 16]
```

→ Cú pháp `[expr for item in iterable if condition]` — gọn + Pythonic.

### 🛠️ 4.2 `dict` — Key-value (như JSON object)

```python
user = {
    "name": "Rom",
    "age": 28,
    "email": "rom@example.com",
    "is_active": True
}
```

Truy cập:

```python
>>> user["name"]
'Rom'

>>> user.get("name")            # an toàn — None nếu không có key
'Rom'

>>> user.get("phone", "N/A")    # default value
'N/A'
```

Thay đổi:

```python
>>> user["age"] = 29              # update value
>>> user["phone"] = "0123456789"  # thêm key mới
>>> user
{'name': 'Rom', 'age': 29, 'email': '...', 'is_active': True, 'phone': '0123456789'}

>>> del user["phone"]              # xóa key
>>> user.pop("is_active")          # xóa + trả value
True
```

Lặp:

```python
>>> for key in user:
...     print(key, user[key])
name Rom
age 29
email rom@example.com

>>> for key, value in user.items():
...     print(f"{key}: {value}")
name: Rom
age: 29
email: rom@example.com

>>> user.keys()
dict_keys(['name', 'age', 'email'])

>>> user.values()
dict_values(['Rom', 29, 'rom@example.com'])
```

### 🛠️ 4.3 `tuple` — List immutable

```python
birthday = (1996, 5, 20)        # (year, month, day)
coordinates = (10.5, 20.3)
single = (42,)                  # ⚠️ phải có dấu phẩy cho tuple 1 phần tử
```

Truy cập giống list:

```python
>>> birthday[0]
1996
>>> birthday[-1]
20
>>> len(birthday)
3
```

**KHÔNG đổi được** (immutable):

```python
>>> birthday[0] = 1997
TypeError: 'tuple' object does not support item assignment
```

#### Unpacking — đặc trưng tuple

```python
>>> birthday = (1996, 5, 20)
>>> year, month, day = birthday   # unpack
>>> year
1996
>>> day
20
```

#### Khi nào dùng tuple?

| Dùng `tuple` khi | Dùng `list` khi |
|---|---|
| Dữ liệu KHÔNG đổi (ngày sinh, color RGB) | Dữ liệu sẽ thêm/bớt |
| Return nhiều giá trị từ function | Lưu collection variable |
| Dùng làm key của dict (list không được) | — |

### 🛠️ 4.4 `set` — Tập hợp không trùng lặp

```python
tags = {"python", "tutorial", "beginner"}
unique_numbers = {1, 2, 3, 2, 1}    # tự loại trùng
print(unique_numbers)                # {1, 2, 3}

empty_set = set()                    # ⚠️ {} là dict rỗng, không phải set rỗng
```

Phép toán tập hợp:

```python
>>> a = {1, 2, 3}
>>> b = {2, 3, 4}

>>> a | b           # union
{1, 2, 3, 4}

>>> a & b           # intersection
{2, 3}

>>> a - b           # difference
{1}

>>> a ^ b           # symmetric difference
{1, 4}
```

Thêm / xóa:

```python
>>> tags.add("advanced")
>>> tags.remove("beginner")
>>> "python" in tags    # check membership
True
```

#### Khi nào dùng set?

| Use case | Ví dụ |
|---|---|
| Loại duplicate khỏi list | `unique = list(set([1, 2, 2, 3]))` |
| Check membership nhanh | `if user_id in admin_set` (O(1) vs list O(n)) |
| Math set operations | Union, intersection |

---

## 5️⃣ Type casting — Chuyển đổi type

```python
>>> int("42")        # str → int
42
>>> int(3.7)         # float → int (cắt phần thập phân)
3
>>> int("3.7")       # ❌ ValueError — str có dấu chấm không convert được
ValueError: invalid literal for int() with base 10: '3.7'
>>> int(float("3.7"))  # ✅ qua float trước
3

>>> str(42)          # int → str
'42'
>>> str(3.14)
'3.14'

>>> float("3.14")    # str → float
3.14
>>> float(5)
5.0

>>> bool(1)          # int → bool
True
>>> bool(0)
False

>>> list("Python")           # str → list
['P', 'y', 't', 'h', 'o', 'n']
>>> list((1, 2, 3))          # tuple → list
[1, 2, 3]
>>> tuple([1, 2, 3])         # list → tuple
(1, 2, 3)
>>> set([1, 2, 2, 3])        # list → set (loại duplicate)
{1, 2, 3}
```

---

## 6️⃣ Mutable vs Immutable — quan trọng

| Mutable (có thể đổi) | Immutable (không thể đổi) |
|---|---|
| `list` | `int` |
| `dict` | `float` |
| `set` | `str` |
| | `bool` |
| | `tuple` |

**Implication**: khi gán biến, mutable share reference, immutable không.

```python
# Immutable — không sao
>>> a = 5
>>> b = a       # b copy giá trị
>>> b = 10
>>> a
5               # a không đổi

# Mutable — CẨN THẬN
>>> list1 = [1, 2, 3]
>>> list2 = list1     # list2 trỏ tới CÙNG list (không phải copy)
>>> list2.append(4)
>>> list1
[1, 2, 3, 4]    # list1 cũng đổi!
```

Muốn copy thực sự:

```python
>>> list2 = list1.copy()        # shallow copy
>>> list2 = list1[:]            # cũng OK
>>> import copy
>>> list2 = copy.deepcopy(list1) # deep copy (nested list/dict)
```

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: float comparison

```python
>>> 0.1 + 0.2 == 0.3
False                # ❌ 0.30000000000000004 != 0.3
```

- **Fix**: dùng `math.isclose()`:
  ```python
  >>> import math
  >>> math.isclose(0.1 + 0.2, 0.3)
  True
  ```

### ❌ Pitfall: Default mutable argument

```python
def add_item(item, items=[]):    # ❌ MẶC ĐỊNH list rỗng
    items.append(item)
    return items
```

```python
>>> add_item("a")
['a']
>>> add_item("b")
['a', 'b']         # ❌ Không phải ['b'] !
```

- **Lý do**: default `[]` tạo 1 LẦN khi def, các call sau share cùng list
- **Fix**:
  ```python
  def add_item(item, items=None):
      if items is None:
          items = []
      items.append(item)
      return items
  ```

### ❌ Pitfall: KeyError khi truy cập dict

```python
>>> user = {"name": "Rom"}
>>> user["email"]
KeyError: 'email'
```

- **Fix**: dùng `.get()`:
  ```python
  >>> user.get("email")            # None nếu không có
  >>> user.get("email", "default@example.com")
  ```

### ✅ Best practice: f-string > old format

```python
# ❌ Cũ
"Hello %s, age %d" % (name, age)
"Hello {}, age {}".format(name, age)

# ✅ Modern (Python 3.6+)
f"Hello {name}, age {age}"
```

### ✅ Best practice: snake_case naming

```python
# ❌ Không Pythonic
userName = "Rom"
isActive = True

# ✅ Pythonic
user_name = "Rom"
is_active = True
```

### ✅ Best practice: type hints (Python 3.5+)

```python
# Optional nhưng giúp đọc code + IDE autocomplete
name: str = "Rom"
age: int = 28
fruits: list[str] = ["apple", "banana"]
user: dict[str, str] = {"name": "Rom"}

def greet(name: str) -> str:
    return f"Hello, {name}!"
```

→ Type hints không enforce runtime — chỉ giúp IDE + `mypy` static check.

---

## 🧠 Self-check

**Q1.** Tại sao `0.1 + 0.2 != 0.3` trong Python?

<details>
<summary>💡 Đáp án</summary>

Vì float là binary representation — `0.1`, `0.2`, `0.3` không có representation chính xác trong binary. `0.1 + 0.2` thực ra là `0.30000000000000004`.

Đây là vấn đề **của mọi ngôn ngữ** dùng IEEE 754 (Java, JS, C++...) — không riêng Python.

Fix: dùng `math.isclose()` hoặc `decimal.Decimal` cho tiền tệ.

</details>

**Q2.** Khi nào dùng `tuple` thay `list`?

<details>
<summary>💡 Đáp án</summary>

Dùng `tuple` khi:
- Dữ liệu **KHÔNG đổi** (ngày sinh, color RGB, coordinate)
- Return nhiều giá trị từ function (`return name, age, email`)
- Cần dùng làm **key của dict** (list không hashable, tuple được)

Dùng `list` khi data sẽ thêm/bớt/đổi.

</details>

**Q3.** Sự khác nhau giữa shallow copy vs deep copy của list?

<details>
<summary>💡 Đáp án</summary>

```python
import copy
original = [[1, 2], [3, 4]]

# Shallow copy — copy outer list, nhưng nested list vẫn share
shallow = original.copy()
shallow[0][0] = 99
print(original)    # [[99, 2], [3, 4]] — nested cũng đổi!

# Deep copy — copy đệ quy mọi level
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original)    # [[1, 2], [3, 4]] — không ảnh hưởng
```

→ Có nested mutable → cần `deepcopy`.

</details>

---

## ⚡ Cheatsheet

```python
# Primitive
age: int = 28
price: float = 9.99
name: str = "Rom"
is_active: bool = True

# Collection
fruits: list = ["apple", "banana"]            # mutable, ordered
user: dict = {"name": "Rom", "age": 28}       # mutable, key-value
birthday: tuple = (1996, 5, 20)               # immutable, ordered
tags: set = {"python", "tutorial"}            # mutable, no duplicate, unordered

# String methods
"abc".upper(), "ABC".lower(), "abc".capitalize()
"a b c".split(), "-".join(["a","b","c"])
"abc".replace("a", "A"), "abc".strip()
f"name={name}, age={age}"

# List methods
fruits.append("x"), fruits.insert(0, "x"), fruits.pop()
fruits.remove("x"), fruits.sort(), fruits.reverse()
sorted(fruits), len(fruits)
[x ** 2 for x in fruits if x]    # comprehension

# Dict methods
user.get("name"), user.get("phone", "N/A")
user.keys(), user.values(), user.items()
"name" in user

# Type casting
int("42"), float("3.14"), str(42)
list("abc"), tuple([1,2,3]), set([1,1,2])

# Logic
True and False, True or False, not True
0.1 == 0.2, "a" == "a", 5 > 3
```

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Variable | Biến | Tên trỏ tới 1 giá trị |
| Data type | Kiểu dữ liệu | Loại của giá trị (int/str/list/...) |
| Primitive | Sơ cấp | Type cơ bản: int, float, str, bool |
| Collection | Tập hợp | Type chứa nhiều giá trị: list, dict, tuple, set |
| Mutable | Có thể đổi | Có thể sửa sau khi tạo (list, dict, set) |
| Immutable | Bất biến | Không sửa được (int, float, str, bool, tuple) |
| Index | Chỉ số | Vị trí phần tử (bắt đầu từ 0) |
| Slice | Lát cắt | Lấy phần con: `[start:end:step]` |
| Comprehension | Cú pháp tổng hợp | `[expr for x in iter if cond]` — đặc trưng Python |
| Unpacking | Bóc tách | `a, b, c = tuple` — gán nhiều biến 1 lúc |
| Type hint | Gợi ý kiểu | `name: str = "Rom"` — annotation cho IDE |
| Truthy / Falsy | Có-thật / Sai-mặc-định | Value coi như True/False trong `if` |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [00_what-is-python.md](./00_what-is-python.md) |
| ➡️ Bài tiếp | [02_control-flow.md](./02_control-flow.md) — if, for, while |
| 🧭 Roadmap | [Zero to Coder — Stage 2](../../../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-2--python-từ-đầu-6-8-tuần) |

### Tài nguyên ngoài

- [Python Tutorial Ch.3 — Data structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Real Python — Variables](https://realpython.com/python-variables/)
- [PEP 8 — Style Guide](https://peps.python.org/pep-0008/)

---

## 📌 Changelog

- **v1.0.0 (16/05/2026)** — Bản đầu tiên — variables + 7 type chính (4 primitive + 4 collection) + casting + mutable/immutable + 5 pitfall/best-practice.
