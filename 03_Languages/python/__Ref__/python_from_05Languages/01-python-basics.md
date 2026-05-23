# 🐍 Python — Ngôn ngữ lập trình đa dụng

> `[BEGINNER]` — Ngôn ngữ tuyệt vời nhất để bắt đầu học lập trình

---

## Tại sao Python?

- **Cú pháp đơn giản** — gần với tiếng Anh tự nhiên
- **Đa dụng** — Web, AI/ML, Automation, Data Science, Scripting
- **Cộng đồng lớn** — Hàng triệu thư viện open source
- **Thị trường việc làm** — Nhu cầu rất cao

---

## Cài đặt

```bash
# Kiểm tra Python có sẵn chưa
python3 --version

# macOS (dùng pyenv để quản lý phiên bản)
brew install pyenv
pyenv install 3.12.0
pyenv global 3.12.0

# Ubuntu
sudo apt install python3 python3-pip

# Virtual Environment (BẮT BUỘC cho mỗi project)
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

---

## Kiểu dữ liệu cơ bản

```python
# Số
x = 10          # int
y = 3.14        # float
z = 2 + 3j      # complex

# Chuỗi
name = "Việt Nam"
multi = """
Nhiều dòng
"""
f_string = f"Xin chào, {name}!"   # f-string (Python 3.6+)

# Boolean
is_active = True
is_empty = False

# None (giống null ở ngôn ngữ khác)
result = None

# Kiểm tra kiểu
type(x)         # <class 'int'>
isinstance(x, int)  # True
```

---

## Cấu trúc dữ liệu

```python
# List — Có thứ tự, có thể thay đổi
fruits = ["apple", "banana", "cherry"]
fruits.append("mango")
fruits[0]           # "apple"
fruits[-1]          # "cherry"
fruits[1:3]         # ["banana", "cherry"]

# Tuple — Có thứ tự, KHÔNG thể thay đổi
point = (10, 20)
x, y = point        # Unpacking

# Dictionary — Key-value
user = {
    "name": "Jesse",
    "age": 25,
    "skills": ["Python", "JS"]
}
user["name"]            # "Jesse"
user.get("email", "N/A")  # "N/A" nếu không có key
user["email"] = "jesse@example.com"

# Set — Không trùng lặp, không thứ tự
tags = {"python", "backend", "python"}  # {"python", "backend"}
tags.add("devops")
```

---

## Điều kiện & Vòng lặp

```python
# If / elif / else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# Ternary (one-liner)
status = "pass" if score >= 60 else "fail"

# For loop
for fruit in fruits:
    print(fruit)

for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# While loop
count = 0
while count < 5:
    count += 1

# List Comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

---

## Hàm (Functions)

```python
# Hàm cơ bản
def greet(name: str, greeting: str = "Xin chào") -> str:
    return f"{greeting}, {name}!"

greet("Jesse")              # "Xin chào, Jesse!"
greet("Jesse", "Hello")    # "Hello, Jesse!"

# *args và **kwargs
def sum_all(*args):
    return sum(args)

def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Lambda (hàm ngắn gọn)
square = lambda x: x ** 2
sorted_users = sorted(users_list, key=lambda u: u["age"])

# Decorator
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done {func.__name__}")
        return result
    return wrapper

@log_call
def process_data(data):
    return data
```

---

## Class & OOP

```python
class Animal:
    # Class variable
    count = 0

    def __init__(self, name: str, age: int):
        self.name = name    # Instance variable
        self.age = age
        Animal.count += 1

    def __str__(self):      # Dùng cho print()
        return f"{self.name} ({self.age} tuổi)"

    def __repr__(self):     # Dùng cho debug
        return f"Animal(name={self.name!r}, age={self.age})"

    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):          # Kế thừa
    def speak(self) -> str:
        return f"{self.name} sủa: Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} kêu: Meow!"

dog = Dog("Buddy", 3)
print(dog)          # Buddy (3 tuổi)
print(dog.speak())  # Buddy sủa: Woof!
```

---

## Xử lý lỗi (Exceptions)

```python
try:
    result = 10 / 0
    data = json.loads("invalid json")
except ZeroDivisionError:
    print("Không thể chia cho 0")
except json.JSONDecodeError as e:
    print(f"JSON không hợp lệ: {e}")
except Exception as e:
    print(f"Lỗi không xác định: {e}")
else:
    print("Thành công!")    # Chạy khi không có lỗi
finally:
    print("Luôn chạy")      # Dùng để đóng file/connection

# Custom Exception
class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")

raise ValidationError("email", "Không hợp lệ")
```

---

## File I/O

```python
# Đọc file
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # Đọc toàn bộ
    lines = f.readlines()       # Đọc từng dòng

# Ghi file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")

# JSON
import json

data = {"name": "Jesse", "age": 25}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
parsed = json.loads(json_str)

with open("data.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## Module & Package

```python
# Import
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Thư viện hay dùng (cài bằng pip)
# pip install requests pandas numpy

import requests
response = requests.get("https://api.github.com/users/octocat")
data = response.json()
print(data["name"])
```

---

## Công cụ Python

```bash
pip install package-name       # Cài thư viện
pip list                        # Liệt kê thư viện đã cài
pip freeze > requirements.txt   # Export dependencies
pip install -r requirements.txt # Install từ file

# Linting & Formatting
pip install ruff                # Linting + formatting nhanh nhất
ruff check .
ruff format .

# Type checking
pip install mypy
mypy main.py
```

---

## Bài tập thực hành

- [ ] Viết script đọc file CSV và tính tổng/trung bình một cột
- [ ] Tạo class `BankAccount` với deposit, withdraw, balance
- [ ] Gọi API thời tiết và in kết quả ra terminal
- [ ] Web scraper đơn giản với `requests` + `BeautifulSoup`

---

## Tài nguyên thêm

- [Python.org Tutorial](https://docs.python.org/3/tutorial/) — Chính thức
- [Real Python](https://realpython.com/) — Tutorials chất lượng cao
- [Python Crash Course (book)](https://nostarch.com/python-crash-course-3rd-edition)
- [Automate the Boring Stuff (free)](https://automatetheboringstuff.com/) — Ứng dụng thực tế
