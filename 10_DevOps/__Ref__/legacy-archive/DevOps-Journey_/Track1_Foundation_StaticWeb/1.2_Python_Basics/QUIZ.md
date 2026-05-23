# ❓ Quiz: Python Basics

> **Knowledge Check for Python in DevOps**
>
> *Kiểm tra kiến thức Python cho DevOps. Chọn đáp án đúng nhất.*

---

## 📋 Instructions

- Tổng cộng: **20 câu hỏi**
- Thời gian đề xuất: **20 phút**
- Passing score: **70% (14/20)**
- Đáp án ở cuối file

---

## Questions

### Q1: Data Types

```python
x = "100"
y = 100
```

`x` và `y` có kiểu dữ liệu gì?

- a) Cả hai đều là `int`
- b) Cả hai đều là `str`
- c) `x` là `str`, `y` là `int`
- d) `x` là `int`, `y` là `str`  

---

### Q2: String Formatting

Cách nào để format string trong Python 3.6+?

- a) `"Hello %s" % name`
- b) `"Hello {}".format(name)`
- c) `f"Hello {name}"`
- d) Tất cả đều đúng  

---

### Q3: List Operations

```python
servers = ["web1", "web2", "db1"]
servers.append("db2")
servers.pop(0)
```

Kết quả của `servers` là gì?

- a) `["web1", "web2", "db1", "db2"]`
- b) `["web2", "db1", "db2"]`
- c) `["web1", "web2", "db1"]`
- d) `["db2", "web2", "db1"]`  

---

### Q4: Dictionary Access

```python
config = {"host": "localhost", "port": 8080}
value = config.get("timeout", 30)
```

`value` bằng bao nhiêu?

- a) `None`
- b) `8080`
- c) `30`
- d) Error  

---

### Q5: List Comprehension

```python
numbers = [1, 2, 3, 4, 5]
result = [n * 2 for n in numbers if n > 2]
```

`result` là gì?

- a) `[2, 4, 6, 8, 10]`
- b) `[6, 8, 10]`
- c) `[3, 4, 5]`
- d) `[1, 2, 3, 4, 5]`  

---

### Q6: File Handling

Cách đúng để đọc file và tự động đóng sau khi xong?

- a) `f = open("file.txt"); data = f.read(); f.close()`
- b) `with open("file.txt") as f: data = f.read()`
- c) `data = open("file.txt").read()`
- d) Cả a và b đều đúng, nhưng b tốt hơn  

---

### Q7: Function Parameters

```python
def connect(host, port=22, timeout=30):
    pass
```

Cách gọi nào SAI?

- a) `connect("192.168.1.1")`
- b) `connect("192.168.1.1", 8080)`
- c) `connect("192.168.1.1", timeout=60)`
- d) `connect(port=22, "192.168.1.1")`  

---

### Q8: Error Handling

```python
try:
    result = 10 / 0
except ValueError:
    print("Value Error")
except ZeroDivisionError:
    print("Zero Division")
except:
    print("Unknown Error")
```

Output là gì?

- a) `Value Error`
- b) `Zero Division`
- c) `Unknown Error`
- d) Error, program crashes  

---

### Q9: Import Statement

Cách import đúng để sử dụng `os.path.exists()`?

- a) `from os import path`
- b) `import os`
- c) `import os.path`
- d) Cả a, b, c đều đúng  

---

### Q10: Subprocess

```python
import subprocess
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
```

`result.stdout` chứa gì?

- a) Return code của command
- b) Output text của command
- c) Error messages
- d) Process ID  

---

### Q11: JSON Handling

```python
import json
data = '{"name": "server1", "port": 80}'
```

Cách chuyển `data` thành Python dictionary?

- a) `json.loads(data)`
- b) `json.load(data)`
- c) `json.dumps(data)`
- d) `json.parse(data)`  

---

### Q12: Environment Variables

Cách lấy environment variable `API_KEY` với default value?

- a) `os.environ["API_KEY"]`
- b) `os.getenv("API_KEY", "default")`
- c) `os.environ.get("API_KEY")`
- d) Cả b và c đều đúng  

---

### Q13: String Methods

```python
path = "/etc/nginx/nginx.conf"
```

Cách lấy filename `nginx.conf` từ path?

- a) `path.split("/")[-1]`
- b) `os.path.basename(path)`
- c) `path.rsplit("/", 1)[1]`
- d) Tất cả đều đúng  

---

### Q14: Boolean Logic

```python
x = True
y = False
result = x and not y
```

`result` là gì?

- a) `True`
- b) `False`
- c) `None`
- d) Error  

---

### Q15: Lambda Functions

```python
multiply = lambda x, y: x * y
```

Tương đương với function nào?

a)

```python
def multiply(x, y):
    return x + y
```

b)

```python
def multiply(x, y):
    return x * y
```

c)

```python
def multiply(x, y):
    x * y
```

d)

```python
def multiply():
    return x * y
```

---

### Q16: Requests Library

```python
import requests
response = requests.get("https://api.example.com/data")
```

Cách kiểm tra request thành công (status 200-299)?

- a) `if response.status_code == 200`
- b) `if response.ok`
- c) `if response.success`
- d) Cả a và b đều đúng  

---

### Q17: Working with Paths

```python
import os
path = os.path.join("/var", "log", "app.log")
```

`path` trên Linux sẽ là gì?

- a) `/var\log\app.log`
- b) `/var/log/app.log`
- c) `var/log/app.log`
- d) `/var//log//app.log`  

---

### Q18: Exception Types

Lỗi nào xảy ra khi truy cập key không tồn tại trong dictionary?

- a) `IndexError`
- b) `ValueError`
- c) `KeyError`
- d) `AttributeError`  

---

### Q19: *args và **kwargs

```python
def func(*args, **kwargs):
    print(args, kwargs)

func(1, 2, name="test")
```

Output là gì?

- a) `(1, 2) {'name': 'test'}`
- b) `[1, 2] {'name': 'test'}`
- c) `1, 2, name=test`
- d) Error  

---

### Q20: YAML Parsing

```python
import yaml
yaml_content = """
server:
  host: localhost
  port: 8080
"""
data = yaml.safe_load(yaml_content)
```

Cách lấy giá trị `8080`?

- a) `data["server.port"]`
- b) `data["server"]["port"]`
- c) `data.server.port`
- d) `data["port"]`  

---

## 📝 Answers

<details>
<summary><strong>Click để xem đáp án</strong></summary>

| Question | Answer | Explanation |
|----------|--------|-------------|
| Q1 | **c** | String trong quotes là `str`, số không có quotes là `int` |
| Q2 | **d** | Python hỗ trợ cả 3 cách, f-string là recommended từ 3.6+ |
| Q3 | **b** | append thêm "db2" vào cuối, pop(0) xóa phần tử đầu tiên |
| Q4 | **c** | get() trả về default value 30 vì key "timeout" không tồn tại |
| Q5 | **b** | Chỉ số > 2 (3,4,5) được nhân 2 = [6,8,10] |
| Q6 | **d** | Cả hai đều đúng, nhưng `with` đảm bảo file được đóng |
| Q7 | **d** | Positional argument không thể sau keyword argument |
| Q8 | **b** | ZeroDivisionError được catch bởi except tương ứng |
| Q9 | **d** | Cả 3 cách đều cho phép sử dụng os.path.exists() |
| Q10 | **b** | stdout chứa output text khi capture_output=True, text=True |
| Q11 | **a** | loads() parse JSON string, load() đọc từ file object |
| Q12 | **d** | Cả getenv() và environ.get() đều hỗ trợ default |
| Q13 | **d** | Tất cả đều trả về "nginx.conf" |
| Q14 | **a** | True and (not False) = True and True = True |
| Q15 | **b** | Lambda trả về x * y |
| Q16 | **d** | ok là True khi status_code trong range 200-299 |
| Q17 | **b** | os.path.join sử dụng separator phù hợp với OS |
| Q18 | **c** | KeyError cho missing dictionary key |
| Q19 | **a** | *args thu thập positional args thành tuple |
| Q20 | **b** | YAML load thành nested dict |

### Scoring

- 18-20: Excellent! 🌟
- 14-17: Good job! ✅
- 10-13: Need review 📚
- Below 10: Study more! 📖

</details>

---

**[← Back to README](./README.md)** | **[Go to Exercises →](./EXERCISES.md)**
