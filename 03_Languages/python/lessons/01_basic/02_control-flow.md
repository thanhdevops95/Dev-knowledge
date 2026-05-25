# 🎓 Python Control Flow — `if`, `for`, `while`

> **Tác giả:** Mr.Nguyen Van A\
> **Phiên bản:** v2.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 21/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~20 phút\
> **Prerequisites:** [01_variables-and-types.md](./01_variables-and-types.md)

> 🎯 *Sau khi có dữ liệu (variables + types), bạn cần **logic** để chương trình "ra quyết định" và "lặp lại task". `if`/`for`/`while` là 3 cấu trúc cốt lõi.*

## 🎯 Sau bài này bạn sẽ

- [ ] Viết `if` / `elif` / `else` để rẽ nhánh
- [ ] Dùng `for` lặp qua list, dict, range, string
- [ ] Dùng `while` lặp dựa trên điều kiện
- [ ] Dùng `break` / `continue` điều khiển vòng lặp
- [ ] Hiểu **indentation** (thụt dòng) — đặc trưng Python
- [ ] Viết list/dict comprehension cơ bản

---

## Tình huống — script tính lương bài trước chưa "thông minh"

Bài trước bạn viết được script tính lương đơn giản:

```python
salary = hours * rate
tax = salary * 0.1
print(salary - tax)
```

Sếp xem qua: *"Lương thấp dưới 5 triệu thì khỏi tính thuế. Trên 10 triệu thì 15%. Trên 20 triệu thì 20%. Và làm cho 30 nhân viên cùng lúc — đừng gõ 30 lần."*

Bạn cần:
- **`if`/`elif`/`else`** — quyết định mức thuế theo lương
- **`for`** — lặp qua 30 nhân viên
- **`while`** — loop đến khi user nhập đúng password

Đây là 3 cấu trúc **control flow** — cốt lõi để chương trình "ra quyết định" và "lặp lại". Không có chúng, code chạy thẳng 1 lần xong là dừng — vô dụng.

---

## 1️⃣ Vì sao Control Flow là phần KHÔNG THỂ THIẾU?

Code không có control flow = chạy 1 dòng → 2 → 3 → ... đến hết. Không "ra quyết định", không "lặp lại". Vô dụng.

Có control flow:

| Tình huống thực tế | Lệnh |
|---|---|
| "Nếu user đã đăng nhập, hiện dashboard; nếu chưa, redirect" | `if/else` |
| "In số 1, 2, 3, ..., 100" | `for` |
| "Đọc file dòng-dòng đến hết" | `for` |
| "Cho user input password đến khi đúng" | `while` |
| "Lặp qua mỗi user trong DB → gửi email" | `for` |
| "Trong 100 lần thử, dừng ngay khi gặp lỗi đầu" | `for` + `break` |

→ Mọi chương trình thực tế đều dùng 3 cấu trúc này hàng chục lần.

---

## 2️⃣ Trước hết — Indentation là gì? (đặc trưng quan trọng nhất Python)

🪞 **Ẩn dụ**: *Indentation (thụt dòng) như **lề lùi vào của 1 đoạn văn** — đoạn nào lùi vào cùng mức = cùng "thuộc về" 1 phần. Python ép viết lề rõ ràng để code dễ đọc; ngôn ngữ khác cho phép viết loạn, Python bắt phải có trật tự.*

Khác với hầu hết ngôn ngữ (Java/C/JS dùng `{}`), Python dùng **thụt dòng** (indentation) để định nghĩa "block":

### Java
```java
if (age >= 18) {
    System.out.println("Adult");
    System.out.println("Can vote");
}
```

### Python
```python
if age >= 18:
    print("Adult")
    print("Can vote")
```

| Yếu tố | Java | Python |
|---|---|---|
| Mở block | `{` | `:` |
| Đóng block | `}` | Dedent (giảm indent) |
| Indent | Optional (cosmetic) | **BẮT BUỘC** |

### Quy tắc indent

3 quy tắc bắt buộc khi indent Python — vi phạm 1 trong 3 = lỗi `IndentationError`:

| Quy tắc | Chi tiết |
|---|---|
| **4 spaces** chuẩn PEP 8 | Không phải 2, không phải Tab |
| Nhất quán trong file | Không trộn tab + space |
| Mỗi level lùi vào 1 đơn vị | 4 → 8 → 12 spaces |

> 💡 VS Code mặc định: Python dùng 4 spaces. Khi gõ Tab, VS Code tự thành 4 spaces. KHÔNG bị "Tab vs Space hell".

### IndentationError — Lỗi đặc trưng Python

Đây là lỗi 99% người mới Python gặp ít nhất 1 lần. Trông như code đúng nhưng Python từ chối chạy:

```python
if age >= 18:
print("Adult")    # ❌ Không indent — phải có 4 spaces đầu dòng
```

```
IndentationError: expected an indented block
```

→ Nhớ **luôn indent sau dấu `:`**.

---

## 3️⃣ `if / elif / else` — Cách Python "ra quyết định"

### 🛠️ 3.1 `if` đơn giản

```python
age = 20

if age >= 18:
    print("Bạn đủ tuổi.")
```

### 🛠️ 3.2 `if / else`

```python
age = 15

if age >= 18:
    print("Đủ tuổi.")
else:
    print("Chưa đủ tuổi.")
```

### 🛠️ 3.3 `if / elif / else` — nhiều nhánh

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Điểm: {score}, Hạng: {grade}")
# Điểm: 85, Hạng: B
```

> 💡 `elif` = "else if" rút gọn. Python KHÔNG có `switch/case` truyền thống (có `match` từ 3.10+ nhưng không bắt buộc học).

### 🛠️ 3.4 Toán tử so sánh + logic

| Toán tử | Ý nghĩa | Ví dụ |
|---|---|---|
| `==` | Bằng (so sánh giá trị) | `5 == 5` → True |
| `!=` | Khác | `5 != 3` → True |
| `<`, `>`, `<=`, `>=` | So sánh | `5 < 10` → True |
| `and` | AND | `age >= 18 and is_active` |
| `or` | OR | `is_admin or is_owner` |
| `not` | NOT | `not is_blocked` |
| `in` | Membership | `"x" in [1, "x", 3]` → True |
| `not in` | Không thuộc | `"y" not in [1, "x", 3]` → True |
| `is` | Same object | `x is None` |
| `is not` | Khác object | `x is not None` |

⚠️ **Phân biệt `==` vs `is`**:

```python
>>> a = [1, 2, 3]
>>> b = [1, 2, 3]
>>> a == b
True            # giá trị bằng nhau
>>> a is b
False           # KHÁC object trong memory

>>> c = a
>>> a is c
True            # cùng reference
```

→ Dùng `==` cho so sánh giá trị. `is` chỉ dùng với `None`, `True`, `False`.

### 🛠️ 3.5 Chained comparison — Pythonic

```python
# Java/C style
if x > 0 and x < 10:
    ...

# ✅ Python style (đẹp hơn)
if 0 < x < 10:
    ...
```

### 🛠️ 3.6 Ternary operator — `if` 1 dòng

```python
age = 20
status = "adult" if age >= 18 else "minor"
print(status)    # adult
```

→ Format: `<value_if_true> if <condition> else <value_if_false>`.

---

## 4️⃣ `for` — Lặp qua iterable

### 🛠️ 4.1 Lặp qua list

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```

```
apple
banana
cherry
```

### 🛠️ 4.2 Lặp qua range — đếm số

```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)
```

```python
for i in range(1, 6):    # 1, 2, 3, 4, 5
    print(i)
```

```python
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8 (step 2)
    print(i)
```

```python
for i in range(10, 0, -1):  # 10, 9, 8, ..., 1 (đếm ngược)
    print(i)
```

> 💡 `range(start, end, step)` — `end` KHÔNG inclusive.

### 🛠️ 4.3 Lặp qua string

```python
for char in "Python":
    print(char)
```

```
P
y
t
h
o
n
```

### 🛠️ 4.4 Lặp qua dict

```python
user = {"name": "Nguyen Van A", "age": 28, "email": "dev@example.com"}

# Lặp qua keys (mặc định)
for key in user:
    print(key, user[key])

# Lặp qua items (key + value) — recommend
for key, value in user.items():
    print(f"{key}: {value}")

# Lặp qua values
for value in user.values():
    print(value)
```

### 🛠️ 4.5 `enumerate` — Lấy cả index và value

```python
fruits = ["apple", "banana", "cherry"]

# ❌ Không Pythonic
for i in range(len(fruits)):
    print(i, fruits[i])

# ✅ Pythonic
for i, fruit in enumerate(fruits):
    print(i, fruit)
```

```
0 apple
1 banana
2 cherry
```

→ `enumerate` start từ 0. Muốn start từ 1: `enumerate(fruits, start=1)`.

### 🛠️ 4.6 `zip` — Lặp song song nhiều list

```python
names = ["Nguyen Van A", "Le Van B", "Tran Van C"]
ages = [28, 25, 30]

for name, age in zip(names, ages):
    print(f"{name}: {age}")
```

```
Nguyen Van A: 28
Le Van B: 25
Tran Van C: 30
```

### 🛠️ 4.7 Nested loops

```python
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})")
```

```
(0, 0)
(0, 1)
(0, 2)
(1, 0)
...
(2, 2)
```

---

## 5️⃣ `while` — Lặp dựa điều kiện

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

```
0
1
2
3
4
```

### Khi nào dùng `while` vs `for`

| Dùng `for` khi | Dùng `while` khi |
|---|---|
| Biết trước số lần lặp | Lặp đến khi điều kiện đổi |
| Lặp qua collection | Đợi event (vd user nhập đúng password) |
| `range(N)` | Game loop, server loop |

### Use case `while`: input loop

```python
password = ""
while password != "admin123":
    password = input("Nhập password: ")

print("Đăng nhập thành công!")
```

### Infinite loop — `while True`

```python
while True:
    user_input = input("> ")
    if user_input == "quit":
        break
    print(f"Bạn nhập: {user_input}")
```

→ `while True` + `break` là pattern phổ biến cho REPL, server loop.

---

## 6️⃣ `break` và `continue`

### `break` — Thoát vòng lặp

```python
for num in range(10):
    if num == 5:
        break
    print(num)
```

```
0
1
2
3
4
```

→ Khi `num == 5`, thoát luôn.

### `continue` — Skip iteration hiện tại

```python
for num in range(10):
    if num % 2 == 0:    # số chẵn
        continue
    print(num)          # chỉ in số lẻ
```

```
1
3
5
7
9
```

### `else` trên vòng lặp — đặc trưng Python

Python có cú pháp lạ: `for/else` và `while/else`. `else` chạy nếu vòng lặp KHÔNG bị `break`.

```python
for num in range(10):
    if num == 100:
        print("Tìm thấy!")
        break
else:
    print("Không tìm thấy")    # chạy đây
```

→ Use case: search trong loop, biết "đã thử hết chưa".

---

## 7️⃣ Comprehension — Pythonic shortcut

### List comprehension

```python
# Cách thường
squares = []
for n in range(10):
    squares.append(n ** 2)

# ✅ List comprehension
squares = [n ** 2 for n in range(10)]
```

Có điều kiện:

```python
even_squares = [n ** 2 for n in range(10) if n % 2 == 0]
# [0, 4, 16, 36, 64]
```

If/else trong comprehension:

```python
labels = ["even" if n % 2 == 0 else "odd" for n in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']
```

### Dict comprehension

```python
squares = {n: n ** 2 for n in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Set comprehension

```python
unique_lengths = {len(name) for name in ["Nguyen Van A", "Le Van B", "Tran Van C", "Tom"]}
# {3} — Nguyen Van A, Le Van B, Tran Van C, Tom đều 3 ký tự
```

> 💡 **Quy tắc**: comprehension đẹp khi đơn giản. Nếu nested 2+ for hoặc logic phức tạp → quay về for loop thường (đọc dễ hơn).

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Modify list khi đang lặp

```python
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)    # ❌ Lỗi logic!
print(numbers)    # [1, 3, 5] hoặc [1, 3, 4, 5] tùy phiên bản
```

- **Fix**: tạo list mới
  ```python
  numbers = [num for num in numbers if num % 2 != 0]
  ```

### ❌ Pitfall: Quên `:` sau `if`/`for`/`while`

```python
if age >= 18      # ❌ thiếu :
    print("OK")
```

```
SyntaxError: expected ':'
```

→ Bạn sẽ gặp lỗi này 50 lần khi mới học. Quen dần.

### ❌ Pitfall: Mix tab + space trong indent

```python
def func():
    if True:
\t  print("a")    # ❌ Tab thay 4 spaces
        print("b")
```

```
IndentationError: unindent does not match any outer indentation level
```

- **Fix**: cấu hình editor "convert Tab to Spaces". VS Code mặc định.

### ❌ Pitfall: Infinite loop không break

```python
i = 0
while i < 10:
    print(i)
    # quên i += 1 → infinite loop, terminal đứng hình
```

- **Fix**: `Ctrl + C` để stop. Đảm bảo có cập nhật biến trong loop.

### ✅ Best practice: Dùng `in` thay nhiều `==`

```python
# ❌
if name == "Nguyen Van A" or name == "Le Van B" or name == "Tran Van C":
    ...

# ✅
if name in ("Nguyen Van A", "Le Van B", "Tran Van C"):
    ...
```

### ✅ Best practice: Early return / early continue

```python
# ❌ Nested if
for user in users:
    if user.is_active:
        if user.has_permission:
            if user.email_verified:
                send_email(user)

# ✅ Early continue (gọn hơn, ít indent)
for user in users:
    if not user.is_active:
        continue
    if not user.has_permission:
        continue
    if not user.email_verified:
        continue
    send_email(user)
```

### ✅ Best practice: Truthy/Falsy cho check rỗng

```python
fruits = []

# ❌
if len(fruits) == 0:
    print("Empty")

# ✅ Pythonic
if not fruits:
    print("Empty")
```

---

## 🧠 Self-check

**Q1.** Khi nào dùng `for` vs `while`?

<details>
<summary>💡 Đáp án</summary>

- **`for`**: biết trước số lần lặp HOẶC lặp qua collection (list, dict, string, ...). Đa số case dùng `for`.
- **`while`**: lặp đến khi điều kiện đổi, không biết trước số lần (user input loop, server loop, retry với backoff).

Rule of thumb: 90% case dùng `for`. Chỉ dùng `while` khi `for` không phù hợp.

</details>

**Q2.** Tại sao Python dùng indent thay `{}` như Java?

<details>
<summary>💡 Đáp án</summary>

Triết lý: **Readability counts**. Indent đẹp = code dễ đọc. Trong Java, người mới có thể quên `{}` hoặc indent sai làm code khó đọc.

Python "ép" coder indent đúng — code Python nào cũng có format đẹp.

Downside: copy/paste code có thể vỡ indent. Mix tab/space gây bug. → VS Code tự xử lý.

</details>

**Q3.** Sự khác nhau giữa `break`, `continue`, `return`?

<details>
<summary>💡 Đáp án</summary>

- **`break`**: thoát ngay khỏi vòng lặp HIỆN TẠI. Code sau loop vẫn chạy.
- **`continue`**: skip iteration HIỆN TẠI, đi tiếp iteration tiếp theo.
- **`return`**: thoát khỏi **function** (kể cả đang trong loop). Code sau function call mới chạy.

```python
def example():
    for i in range(10):
        if i == 3:
            continue    # skip i==3
        if i == 7:
            break       # dừng loop, in "Done"
        if i == 5:
            return      # thoát luôn function, không in "Done"
        print(i)
    print("Done")
```

</details>

---

## ⚡ Cheatsheet

```python
# IF
if cond:
    ...
elif cond:
    ...
else:
    ...

# Ternary
value = "yes" if cond else "no"

# FOR
for item in collection:
    ...

for i in range(10):           # 0..9
for i in range(1, 11):        # 1..10
for i in range(0, 10, 2):     # 0, 2, 4, 6, 8

for i, item in enumerate(list):
for k, v in dict.items():
for a, b in zip(list_a, list_b):

# WHILE
while cond:
    ...

while True:
    ...
    if exit_cond:
        break

# Control
break       # thoát loop
continue    # skip iteration
else:       # chạy nếu loop không break

# Comprehension
[x for x in iter]
[x for x in iter if cond]
[expr1 if cond else expr2 for x in iter]
{k: v for k, v in items}
{x for x in iter}      # set

# Comparison
==  !=  <  >  <=  >=
and  or  not
in  not in
is  is not       # chỉ dùng với None, True, False

# Chained
0 < x < 10
```

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Control flow | Điều khiển luồng | Logic điều khiển code chạy theo thứ tự nào |
| Conditional | Điều kiện | `if/elif/else` |
| Loop | Vòng lặp | `for`, `while` |
| Iterable | Có thể lặp | Object lặp được: list, str, dict, range, ... |
| Iteration | Lần lặp | 1 lượt chạy của loop |
| Indentation | Thụt dòng | Whitespace ở đầu dòng — Python dùng để định block |
| `break` | (giữ nguyên) | Thoát loop |
| `continue` | (giữ nguyên) | Skip iteration |
| Truthy / Falsy | (giữ nguyên) | Value coi như True/False trong context boolean |
| Comprehension | Cú pháp tổng hợp | `[expr for x in iter]` |
| Ternary | Toán tử 3 ngôi | `a if cond else b` |
| `range()` | (giữ nguyên) | Sinh chuỗi số |
| `enumerate()` | (giữ nguyên) | Tra số thứ tự + giá trị |
| `zip()` | (giữ nguyên) | Lặp song song nhiều iterable |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [01_variables-and-types.md](./01_variables-and-types.md) |
| ➡️ Bài tiếp | [03_functions.md](./03_functions.md) |
| 🧭 Roadmap | [Zero to Coder — Stage 2](../../../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-2--python-từ-đầu-6-8-tuần) |

### Tài nguyên ngoài

- [Python Tutorial Ch.4 — Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Real Python — Conditional Statements](https://realpython.com/python-conditional-statements/)
- [Real Python — `for` Loops](https://realpython.com/python-for-loop/)

---

## 📌 Changelog

- **v2.1.0 (24/05/2026)** — Apply Blueprint v0.5.4. Thêm ẩn dụ "lề lùi đoạn văn" cho indentation, 2 lead-in trước bảng quy tắc indent + IndentationError example.


- **v2.0.0 (21/05/2026)** — Restructure theo writing-style v0.5.1:
  - Mở bằng **tình huống script tính lương cần tax theo bậc + lặp 30 nhân viên**
  - Headers đổi: `1️⃣ (WHY)` / `2️⃣ Indentation (WHAT)` / `3️⃣ if/elif/else (HOW)` → câu hỏi/mô tả tự nhiên
  - Content kỹ thuật KHÔNG đổi
- **v1.0.0 (16/05/2026)** — Bản đầu tiên — if/elif/else + for/while + break/continue + comprehension + 5 pitfall/best-practice.
