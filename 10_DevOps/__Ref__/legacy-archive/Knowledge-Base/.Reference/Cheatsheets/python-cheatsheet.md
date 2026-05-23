# Python Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Python syntax and commands for quick reference -- Cú pháp và lệnh Python để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [Basics](#basics) -- Cơ bản
- [Data Types](#data-types) -- Kiểu Dữ liệu
- [Strings](#strings) -- Chuỗi
- [Lists](#lists) -- Danh sách
- [Dictionaries](#dictionaries) -- Từ điển
- [Control Flow](#control-flow) -- Luồng Điều khiển
- [Functions](#functions) -- Hàm
- [Classes](#classes) -- Lớp
- [File Operations](#file-operations) -- Thao tác File
- [Error Handling](#error-handling) -- Xử lý Lỗi
- [Modules & Packages](#modules--packages) -- Modules và Packages
- [Virtual Environments](#virtual-environments) -- Môi trường Ảo
- [Common Patterns](#common-patterns) -- Patterns Thường dùng

## <a id="basics"></a> Basics -- Cơ bản

```python
# Comments -- Chú thích
# Single line comment -- Chú thích một dòng

"""
Multi-line comment
or docstring
-- Chú thích nhiều dòng hoặc docstring
"""

# Variables -- Biến
name = "John"                 # String -- Chuỗi
age = 25                      # Integer -- Số nguyên
height = 1.75                 # Float -- Số thực
is_active = True              # Boolean -- Boolean
nothing = None                # None type -- Kiểu None

# Type checking -- Kiểm tra kiểu
type(name)                    # <class 'str'>
isinstance(age, int)          # True

# Type conversion -- Chuyển đổi kiểu
int("42")                     # String to int -- Chuỗi sang int
float("3.14")                 # String to float -- Chuỗi sang float
str(42)                       # Int to string -- Int sang chuỗi
list("hello")                 # String to list -- Chuỗi sang list
bool(1)                       # True

# Input/Output -- Input/Output
print("Hello")                # Print -- In
print(f"Name: {name}")        # f-string
print("Name:", name)          # Multiple args -- Nhiều tham số
name = input("Enter name: ")  # Input -- Nhập

# Operators -- Toán tử
5 + 3                         # Addition: 8 -- Cộng
5 - 3                         # Subtraction: 2 -- Trừ
5 * 3                         # Multiplication: 15 -- Nhân
5 / 3                         # Division: 1.666... -- Chia
5 // 3                        # Floor division: 1 -- Chia lấy phần nguyên
5 % 3                         # Modulo: 2 -- Chia lấy dư
5 ** 3                        # Power: 125 -- Lũy thừa

# Comparison -- So sánh
5 == 5                        # Equal -- Bằng
5 != 3                        # Not equal -- Không bằng
5 > 3                         # Greater than -- Lớn hơn
5 >= 5                        # Greater or equal -- Lớn hơn hoặc bằng
5 < 3                         # Less than -- Nhỏ hơn
5 <= 5                        # Less or equal -- Nhỏ hơn hoặc bằng

# Logical -- Logic
True and False                # AND
True or False                 # OR
not True                      # NOT
```

## <a id="data-types"></a> Data Types -- Kiểu Dữ liệu

```python
# Numbers -- Số
x = 10                        # int
y = 3.14                      # float
z = 3 + 4j                    # complex -- Số phức

# Strings -- Chuỗi
s = "Hello"
s = 'Hello'
s = """Multi-line
string"""

# Lists -- Danh sách (mutable -- có thể thay đổi)
my_list = [1, 2, 3, "four"]

# Tuples -- Tuple (immutable -- không thể thay đổi)
my_tuple = (1, 2, 3)

# Sets -- Tập hợp (unique values -- giá trị duy nhất)
my_set = {1, 2, 3}

# Dictionaries -- Từ điển (key-value pairs -- cặp key-value)
my_dict = {"name": "John", "age": 25}

# Frozenset -- Frozenset (immutable set -- set bất biến)
my_frozenset = frozenset([1, 2, 3])

# Bytes -- Bytes
my_bytes = b"Hello"

# Range -- Range
my_range = range(10)          # 0 to 9
```

## <a id="strings"></a> Strings -- Chuỗi

```python
s = "Hello World"

# Access -- Truy cập
s[0]                          # 'H' (first char -- ký tự đầu)
s[-1]                         # 'd' (last char -- ký tự cuối)
s[0:5]                        # 'Hello' (slice -- cắt)
s[6:]                         # 'World' (from index 6 -- từ chỉ số 6)
s[:5]                         # 'Hello' (first 5 -- 5 đầu tiên)
s[::2]                        # 'HloWrd' (every 2nd char -- mỗi ký tự thứ 2)
s[::-1]                       # 'dlroW olleH' (reverse -- đảo ngược)

# Methods -- Phương thức
s.lower()                     # 'hello world'
s.upper()                     # 'HELLO WORLD'
s.title()                     # 'Hello World'
s.capitalize()                # 'Hello world'
s.strip()                     # Remove whitespace -- Xóa khoảng trắng
s.lstrip()                    # Remove left whitespace -- Xóa khoảng trắng trái
s.rstrip()                    # Remove right whitespace -- Xóa khoảng trắng phải
s.split()                     # ['Hello', 'World']
s.split(',')                  # Split by comma -- Chia theo dấu phẩy
'-'.join(['a', 'b', 'c'])     # 'a-b-c'
s.replace('World', 'Python')  # 'Hello Python'
s.find('World')               # 6 (index or -1 -- chỉ số hoặc -1)
s.index('World')              # 6 (index or error -- chỉ số hoặc lỗi)
s.count('l')                  # 3
s.startswith('Hello')         # True
s.endswith('World')           # True
s.isalpha()                   # False (has space -- có khoảng trắng)
s.isdigit()                   # False
s.isalnum()                   # False

# Formatting -- Định dạng
name = "John"
age = 25
f"Name: {name}, Age: {age}"              # f-string
"Name: {}, Age: {}".format(name, age)    # format()
"Name: %s, Age: %d" % (name, age)        # % formatting
```

## <a id="lists"></a> Lists -- Danh sách

```python
lst = [1, 2, 3, 4, 5]

# Access -- Truy cập
lst[0]                        # 1 (first -- đầu tiên)
lst[-1]                       # 5 (last -- cuối cùng)
lst[1:3]                      # [2, 3] (slice -- cắt)
len(lst)                      # 5 (length -- độ dài)

# Modify -- Sửa đổi
lst[0] = 10                   # [10, 2, 3, 4, 5]
lst.append(6)                 # Add to end -- Thêm vào cuối
lst.insert(0, 0)              # Insert at index -- Chèn tại chỉ số
lst.extend([7, 8])            # Add multiple -- Thêm nhiều
lst += [9, 10]                # Concatenate -- Nối
lst.remove(3)                 # Remove by value -- Xóa theo giá trị
lst.pop()                     # Remove and return last -- Xóa và trả về cuối
lst.pop(0)                    # Remove and return at index -- Xóa và trả về tại chỉ số
del lst[0]                    # Delete by index -- Xóa theo chỉ số
lst.clear()                   # Remove all -- Xóa tất cả

# Other methods -- Các phương thức khác
lst = [3, 1, 4, 1, 5]
lst.sort()                    # Sort in place -- Sắp xếp tại chỗ
lst.sort(reverse=True)        # Sort descending -- Sắp xếp giảm dần
sorted(lst)                   # Return new sorted list -- Trả về list đã sắp xếp
lst.reverse()                 # Reverse in place -- Đảo ngược tại chỗ
lst.index(4)                  # Find index of value -- Tìm chỉ số của giá trị
lst.count(1)                  # Count occurrences -- Đếm số lần xuất hiện
lst.copy()                    # Shallow copy -- Sao chép nông

# List comprehension -- List comprehension
[x**2 for x in range(5)]                    # [0, 1, 4, 9, 16]
[x for x in range(10) if x % 2 == 0]        # [0, 2, 4, 6, 8]
[x.upper() for x in ['a', 'b', 'c']]        # ['A', 'B', 'C']
[[x*y for x in range(3)] for y in range(3)] # Nested -- Lồng nhau
```

## <a id="dictionaries"></a> Dictionaries -- Từ điển

```python
d = {"name": "John", "age": 25, "city": "NYC"}

# Access -- Truy cập
d["name"]                     # "John"
d.get("name")                 # "John"
d.get("country", "Unknown")   # "Unknown" (default -- mặc định)

# Modify -- Sửa đổi
d["age"] = 26                 # Update value -- Cập nhật giá trị
d["country"] = "USA"          # Add new key -- Thêm key mới
d.update({"age": 27, "job": "Developer"})  # Update multiple -- Cập nhật nhiều
del d["city"]                 # Delete key -- Xóa key
d.pop("age")                  # Remove and return -- Xóa và trả về
d.clear()                     # Remove all -- Xóa tất cả

# Methods -- Phương thức
d = {"name": "John", "age": 25}
d.keys()                      # dict_keys(['name', 'age'])
d.values()                    # dict_values(['John', 25])
d.items()                     # dict_items([('name', 'John'), ('age', 25)])
"name" in d                   # True (check key -- kiểm tra key)
len(d)                        # 2

# Dictionary comprehension -- Dictionary comprehension
{x: x**2 for x in range(5)}   # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
{k: v for k, v in d.items() if v}  # Filter -- Lọc

# Iterate -- Lặp
for key in d:                 # Iterate keys -- Lặp keys
    print(key)

for key, value in d.items():  # Iterate key-value -- Lặp key-value
    print(f"{key}: {value}")
```

## <a id="control-flow"></a> Control Flow -- Luồng Điều khiển

```python
# If-elif-else
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")

# Ternary operator -- Toán tử tam phân
result = "Yes" if condition else "No"

# For loop -- Vòng lặp for
for i in range(5):            # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 2):     # 2, 4, 6, 8 (start, stop, step -- bắt đầu, kết thúc, bước)
    print(i)

for item in my_list:          # Iterate list -- Lặp list
    print(item)

for i, item in enumerate(my_list):  # With index -- Với chỉ số
    print(f"{i}: {item}")

for key, value in my_dict.items():  # Iterate dict -- Lặp dict
    print(f"{key}: {value}")

# While loop -- Vòng lặp while
while condition:
    pass

# Loop control -- Điều khiển vòng lặp
break                         # Exit loop -- Thoát vòng lặp
continue                      # Skip iteration -- Bỏ qua vòng lặp
else:                         # After loop (if no break) -- Sau vòng lặp (nếu không break)
    pass

# Match-case (Python 3.10+)
match value:
    case 1:
        print("One")
    case 2 | 3:
        print("Two or Three")
    case _:
        print("Other")
```

## <a id="functions"></a> Functions -- Hàm

```python
# Define function -- Định nghĩa hàm
def greet(name):
    """Docstring -- Mô tả hàm"""
    return f"Hello, {name}!"

# Call function -- Gọi hàm
result = greet("World")

# Default parameters -- Tham số mặc định
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Keyword arguments -- Tham số keyword
greet(name="World", greeting="Hi")

# *args and **kwargs -- *args và **kwargs
def func(*args, **kwargs):
    print(args)               # Tuple of positional args -- Tuple các tham số vị trí
    print(kwargs)             # Dict of keyword args -- Dict các tham số keyword

func(1, 2, 3, name="John")    # args=(1, 2, 3), kwargs={'name': 'John'}

# Lambda function -- Hàm lambda
square = lambda x: x ** 2
add = lambda x, y: x + y

# Map, filter, reduce
list(map(lambda x: x**2, [1, 2, 3]))      # [1, 4, 9]
list(filter(lambda x: x > 0, [-1, 0, 1])) # [1]
from functools import reduce
reduce(lambda x, y: x + y, [1, 2, 3])     # 6

# Decorator -- Decorator
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Generator -- Generator
def count_up_to(n):
    i = 0
    while i < n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num)

# Generator expression -- Biểu thức generator
gen = (x**2 for x in range(10))
```

## <a id="classes"></a> Classes -- Lớp

```python
# Define class -- Định nghĩa lớp
class Person:
    # Class attribute -- Thuộc tính lớp
    species = "Human"
    
    # Constructor -- Hàm khởi tạo
    def __init__(self, name, age):
        self.name = name      # Instance attribute -- Thuộc tính instance
        self.age = age
    
    # Instance method -- Phương thức instance
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    # Class method -- Phương thức lớp
    @classmethod
    def from_birth_year(cls, name, birth_year):
        return cls(name, 2024 - birth_year)
    
    # Static method -- Phương thức tĩnh
    @staticmethod
    def is_adult(age):
        return age >= 18
    
    # Property -- Property
    @property
    def info(self):
        return f"{self.name}, {self.age} years old"
    
    # String representation -- Biểu diễn chuỗi
    def __str__(self):
        return f"Person({self.name})"
    
    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"

# Create instance -- Tạo instance
person = Person("John", 25)
print(person.greet())

# Inheritance -- Kế thừa
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
    
    def study(self):
        return f"{self.name} is studying"

# Multiple inheritance -- Kế thừa nhiều
class A:
    pass

class B:
    pass

class C(A, B):
    pass

# Dataclass (Python 3.7+)
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0
```

## <a id="file-operations"></a> File Operations -- Thao tác File

```python
# Read file -- Đọc file
with open("file.txt", "r") as f:
    content = f.read()        # Read all -- Đọc tất cả
    
with open("file.txt", "r") as f:
    lines = f.readlines()     # Read as list of lines -- Đọc như list dòng

with open("file.txt", "r") as f:
    for line in f:            # Read line by line -- Đọc từng dòng
        print(line.strip())

# Write file -- Ghi file
with open("file.txt", "w") as f:
    f.write("Hello World")    # Overwrite -- Ghi đè

with open("file.txt", "a") as f:
    f.write("New line\n")     # Append -- Thêm vào

with open("file.txt", "w") as f:
    f.writelines(["Line 1\n", "Line 2\n"])

# File modes -- Các chế độ file
# 'r'  - Read -- Đọc
# 'w'  - Write (overwrite) -- Ghi (ghi đè)
# 'a'  - Append -- Thêm vào
# 'x'  - Create (fail if exists) -- Tạo (lỗi nếu tồn tại)
# 'b'  - Binary mode -- Chế độ nhị phân
# '+'  - Read and write -- Đọc và ghi

# JSON
import json

data = {"name": "John", "age": 25}
json_str = json.dumps(data)           # Object to JSON string -- Object sang chuỗi JSON
data = json.loads(json_str)           # JSON string to object -- Chuỗi JSON sang object

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)      # Write to file -- Ghi vào file

with open("data.json", "r") as f:
    data = json.load(f)               # Read from file -- Đọc từ file

# CSV
import csv

with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    writer.writerows([["John", 25], ["Jane", 24]])
```

## <a id="error-handling"></a> Error Handling -- Xử lý Lỗi

```python
# Try-except -- Try-except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero -- Không thể chia cho 0")
except Exception as e:
    print(f"Error: {e}")
else:
    print("Success -- Thành công")
finally:
    print("Always executed -- Luôn thực thi")

# Raise exception -- Raise exception
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative -- Tuổi không thể âm")

# Custom exception -- Exception tùy chỉnh
class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# Assert
assert x > 0, "x must be positive -- x phải dương"
```

## <a id="modules--packages"></a> Modules & Packages -- Modules và Packages

```python
# Import -- Import
import os
import os as operating_system
from os import path
from os import path as p
from os import *              # Import all (avoid!) -- Import tất cả (tránh!)

# Common modules -- Các modules thường dùng
import os                     # OS interface
import sys                    # System
import datetime               # Date and time
import json                   # JSON
import re                     # Regular expressions
import random                 # Random numbers
import math                   # Math functions
import collections            # Collections
import itertools              # Iterators
import functools              # Functional tools
import subprocess             # Run commands
import pathlib                # Path operations
import logging                # Logging
import unittest               # Testing

# Module info -- Thông tin module
print(__name__)               # Current module name -- Tên module hiện tại
print(__file__)               # Current file path -- Đường dẫn file hiện tại

# Main check -- Kiểm tra main
if __name__ == "__main__":
    main()
```

## <a id="virtual-environments"></a> Virtual Environments -- Môi trường Ảo

```bash
# Create virtual environment -- Tạo môi trường ảo
python -m venv venv
python3 -m venv venv

# Activate -- Kích hoạt
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# Deactivate -- Hủy kích hoạt
deactivate

# Install packages -- Cài đặt packages
pip install package_name
pip install package_name==1.0.0
pip install -r requirements.txt

# List packages -- Liệt kê packages
pip list
pip freeze > requirements.txt

# Uninstall -- Gỡ cài đặt
pip uninstall package_name
```

## <a id="common-patterns"></a> Common Patterns -- Patterns Thường dùng

```python
# Context manager -- Context manager
class MyContext:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

with MyContext() as ctx:
    pass

# Singleton pattern -- Pattern Singleton
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Threading -- Threading
import threading

def task():
    print("Task running")

thread = threading.Thread(target=task)
thread.start()
thread.join()

# Async/await -- Async/await
import asyncio

async def main():
    await asyncio.sleep(1)
    return "Done"

asyncio.run(main())

# Type hints (Python 3.5+) -- Type hints
def greet(name: str) -> str:
    return f"Hello, {name}"

from typing import List, Dict, Optional, Union

def process(items: List[int]) -> Dict[str, int]:
    return {"sum": sum(items)}

def maybe_none(x: Optional[int]) -> int:
    return x if x else 0

def either(x: Union[int, str]) -> str:
    return str(x)
```

---
