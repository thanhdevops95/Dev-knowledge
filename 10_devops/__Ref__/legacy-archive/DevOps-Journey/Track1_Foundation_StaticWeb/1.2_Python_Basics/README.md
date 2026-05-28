# 🐍 Module 1.2: Python Basics

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Beginner-green?style=flat-square)](.)

> **Python for DevOps** - Scripting and automation with Python.
>
> *Python cho DevOps - Viết script và tự động hóa với Python.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand Python syntax and data types (Hiểu cú pháp Python và các kiểu dữ liệu)
- ✅ Work with files and directories (Làm việc với files và thư mục)
- ✅ Process JSON and YAML configs (Xử lý cấu hình JSON và YAML)
- ✅ Call APIs with requests library (Gọi APIs với thư viện requests)
- ✅ Execute system commands (Thực thi lệnh hệ thống)
- ✅ Write automation scripts (Viết script tự động hóa)

---

## 📋 Prerequisites (Điều kiện tiên quyết)

- Complete Module 1.1 Linux & Bash (Hoàn thành Module 1.1 Linux & Bash)
- Python 3.8+ installed (Đã cài Python 3.8+)
- VS Code with Python extension (VS Code với extension Python)

---

## 📚 Content (Nội dung)

### 1. What is Python? (Python là gì?)

**Python** is a high-level, interpreted programming language known for its simplicity and readability. It is the most popular language for DevOps automation, data science, and AI.

*Python là ngôn ngữ lập trình bậc cao, thông dịch, nổi tiếng với sự đơn giản và dễ đọc. Đây là ngôn ngữ phổ biến nhất cho tự động hóa DevOps, khoa học dữ liệu và AI.*

**Key features for DevOps (Tính năng chính cho DevOps):**

- **Readable (Dễ đọc)**: Code looks like English pseudo-code (Code nhìn giống mã giả tiếng Anh).
- **Batteries Included (Đầy đủ tiện ích)**: Huge standard library for file I/O, networking, etc. (Thư viện chuẩn khổng lồ).
- **Cross-platform**: Runs on Windows, Linux, macOS (Chạy trên mọi nền tảng).

### 2. Python Basics (Cơ bản Python)

#### Data Types (Kiểu dữ liệu)

```python
# Strings (Chuỗi)
name = "DevOps"
path = '/etc/nginx/nginx.conf'

# Numbers (Số)
port = 8080
percentage = 99.5

# Boolean (Luận lý)
enabled = True
running = False

# Lists (Danh sách)
servers = ["web1", "web2", "db1"]
ports = [80, 443, 3306]

# Dictionaries (Từ điển)
config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

```

#### Control Flow (Luồng điều khiển)

```python
# If/Else (Điều kiện)
if status == 200:
    print("OK")
elif status == 404:
    print("Not Found")
else:
    print("Error")

# For loops (Vòng lặp for)
for server in servers:
    print(f"Checking {server}")

# While loops (Vòng lặp while)
while retries < 3:
    try_connect()
    retries += 1

```

---

### 3. Functions (Hàm)

```python
def deploy_app(app_name, environment="staging"):
    """Deploy application to specified environment.
    Triển khai ứng dụng đến môi trường được chỉ định."""
    print(f"Deploying {app_name} to {environment}")
    # Deployment logic (Logic triển khai)
    return True

# Usage (Sử dụng)
deploy_app("my-app")
deploy_app("my-app", environment="production")

```

---

### 4. File Operations (Thao tác với File)

```python
# Read file (Đọc file)
with open("/etc/hosts", "r") as f:
    content = f.read()
    print(content)

# Write file (Ghi file)
with open("output.txt", "w") as f:
    f.write("Hello DevOps!")

# JSON (Xử lý JSON)
import json

with open("config.json", "r") as f:
    config = json.load(f)

with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

# YAML (Xử lý YAML)
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

```

---

### 5. Working with OS (Làm việc với Hệ điều hành)

```python
import os
import subprocess

# Environment variables (Biến môi trường)
home = os.environ.get("HOME")
api_key = os.getenv("API_KEY", "default")

# File system (Hệ thống tệp)
os.path.exists("/etc/nginx")
os.listdir("/var/log")
os.makedirs("new/nested/dir", exist_ok=True)

# Run commands (Chạy lệnh)
result = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    text=True
)
print(result.stdout)

```

---

---

---

### 6. HTTP Requests (Yêu cầu HTTP)

```python
import requests

# GET request (Yêu cầu GET)
response = requests.get("https://api.github.com")
data = response.json()

# POST request (Yêu cầu POST)
payload = {"name": "new-server"}
response = requests.post(
    "https://api.example.com/servers",
    json=payload,
    headers={"Authorization": "Bearer token"}
)

# Error handling (Xử lý lỗi)
response.raise_for_status()

```

---

### 7. Error Handling (Xử lý lỗi)

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    cleanup()

```

---

---

---

### 8. Classes - OOP (Lớp - Lập trình hướng đối tượng)

```python
class Server:
    def __init__(self, hostname, ip):
        self.hostname = hostname
        self.ip = ip
        self.status = "stopped"
    
    def start(self):
        self.status = "running"
        print(f"{self.hostname} started")
    
    def stop(self):
        self.status = "stopped"
        print(f"{self.hostname} stopped")

# Usage (Sử dụng)
web1 = Server("web1", "192.168.1.10")
web1.start()

```

---

## 🛠️ Common DevOps Patterns (Các mẫu DevOps phổ biến)

### Config Parser (Trình phân tích cấu hình)

```python
import yaml
import os

def load_config(config_file):
    """Load config with environment variable override.
    Tải cấu hình với ghi đè từ biến môi trường."""
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Override with env vars (Ghi đè bằng biến môi trường)
    if os.getenv("DB_HOST"):
        config["database"]["host"] = os.getenv("DB_HOST")
    
    return config

```

### Log Parser (Trình phân tích log)

```python
def parse_logs(log_file):
    """Parse log file and count errors.
    Phân tích file log và đếm lỗi."""
    errors = []
    
    with open(log_file) as f:
        for line in f:
            if "ERROR" in line:
                errors.append(line.strip())
    
    return errors

```

### Health Checker (Kiểm tra sức khỏe)

```python
import requests

def check_health(urls):
    """Check health of multiple endpoints.
    Kiểm tra sức khỏe của nhiều endpoints."""
    results = {}
    
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            results[url] = r.status_code == 200
        except:
            results[url] = False
    
    return results

```

---

## 📖 Resources (Tài liệu tham khảo)

### Documentation (Tài liệu)

- [Python Official Docs](https://docs.python.org/3/)
- [Requests Library](https://requests.readthedocs.io/)
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

### Books (Sách)

- "Automate the Boring Stuff with Python"
- "Python for DevOps" by Noah Gift

---

## Module Files (Các file trong Module)

| File | Description |
|------|-------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Practice exercises (Bài tập thực hành) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Exercise solutions (Đáp án bài tập) |
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [1.1 Linux & Bash](../1.1_Linux_Bash/) | **1.2 Python** | [1.3 Network](../1.3_Network_Basics/) |

---

**Ready to automate with Python! 🐍**

*Sẵn sàng tự động hóa với Python!*

</div>
