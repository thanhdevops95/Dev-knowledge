# Module 03: Scripting (Bash & Python)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Script** | - | File chứa các lệnh được thực thi tuần tự |
| **Bash** | /bæʃ/ | Bourne Again Shell - Ngôn ngữ scripting trên Linux |
| **Python** | /ˈpaɪθɑːn/ | Ngôn ngữ lập trình phổ biến cho automation |
| **Automation** | - | Tự động hóa - Máy làm thay công việc lặp lại |
| **Shebang** | - | `#!/bin/bash` - Dòng đầu chỉ định interpreter |
| **Variable** | - | Biến - Nơi lưu trữ giá trị |
| **Function** | - | Hàm - Khối code có thể gọi lại |
| **Loop** | - | Vòng lặp - Thực thi code nhiều lần (for, while) |
| **Conditional** | - | Điều kiện - Rẽ nhánh logic (if/else) |
| **Cron** | /krɒn/ | Công cụ lập lịch chạy script tự động |
| **Argument** | - | Tham số truyền vào script ($1, $2...) |
| **Exit Code** | - | Mã trả về (0 = thành công, >0 = lỗi) |
| **Pipe** | - | `|` - Chuyển output của lệnh này làm input lệnh kia |
| **Regex** | - | Regular Expression - Biểu thức tìm kiếm pattern |

---

## 🎬 Câu chuyện mở đầu

Ngày đầu tiên làm DevOps, bạn được giao task:

> "Backup database mỗi ngày lúc 3h sáng, nén lại, upload lên S3, xóa backups cũ hơn 7 ngày."

Bạn có thể làm thủ công. Nhưng bạn phải **thức dậy lúc 3h sáng mỗi ngày**.

Hoặc - bạn viết **script** và để máy tự làm.

**Đây là lý do bạn cần học scripting.**

---

## 📖 Scripting là gì?

### Automation = Viết code để máy làm thay mình

```
Công việc lặp lại                Script tự động
─────────────────               ─────────────────
Mỗi ngày SSH vào server    →    Cron job chạy tự động
Copy file bằng tay         →    Script copy + verify
Check logs thủ công        →    Script alert khi có lỗi
Deploy bằng 10 lệnh        →    1 script, 1 lệnh
```

### Tại sao DevOps cần scripting?

| Lý do | Giải thích |
|-------|------------|
| **Tiết kiệm thời gian** | Làm 1 lần, chạy 1000 lần |
| **Tránh lỗi** | Máy không quên bước, không gõ nhầm |
| **Reproducible** | Ai chạy cũng cùng kết quả |
| **Documentable** | Script chính là documentation |
| **Testable** | Có thể test trước khi production |

---

## 🐚 Bash Scripting

### Bash là gì?

**Bash** = Bourne Again SHell - Shell mặc định của hầu hết Linux.

Khi bạn gõ lệnh trong terminal, bạn đang dùng Bash.

### Script đầu tiên

**Tạo file:**

```bash
nano hello.sh
```

**Nội dung:**

```bash
#!/bin/bash
# Script đầu tiên của tôi

echo "Hello, DevOps!"
echo "Today is $(date)"
echo "You are: $(whoami)"
```

**Giải thích:**

- `#!/bin/bash` = Shebang, khai báo interpreter
- `#` = Comment
- `$(command)` = Chạy command và lấy output

**Chạy:**

```bash
chmod +x hello.sh
./hello.sh
```

**Output:**

```
Hello, DevOps!
Today is Mon Jan 15 10:00:00 UTC 2024
You are: youruser
```

---

## 📦 Biến (Variables)

### Khai báo và sử dụng

```bash
#!/bin/bash

# Khai báo biến (KHÔNG có space quanh dấu =)
NAME="DevOps Engineer"
AGE=25
CURRENT_DATE=$(date +%Y-%m-%d)

# Sử dụng biến (dùng $)
echo "Hello, $NAME"
echo "You are $AGE years old"
echo "Today is $CURRENT_DATE"
```

### ⚠️ Lỗi phổ biến

```bash
# SAI - có space
NAME = "John"

# ĐÚNG - không space
NAME="John"
```

### Biến đặc biệt

```bash
#!/bin/bash

echo "Script name: $0"        # Tên script
echo "First argument: $1"     # Tham số thứ 1
echo "Second argument: $2"    # Tham số thứ 2
echo "All arguments: $@"      # Tất cả tham số
echo "Number of args: $#"     # Số lượng tham số
echo "Last exit code: $?"     # Exit code của lệnh trước
echo "Process ID: $$"         # PID của script
```

**Chạy:**

```bash
./script.sh hello world
```

**Output:**

```
Script name: ./script.sh
First argument: hello
Second argument: world
All arguments: hello world
Number of args: 2
```

---

## 🔀 Điều kiện (Conditionals)

### if-else cơ bản

```bash
#!/bin/bash

AGE=25

if [ $AGE -ge 18 ]; then
    echo "You are an adult"
else
    echo "You are a minor"
fi
```

### Operators so sánh số

| Operator | Nghĩa | Ví dụ |
|----------|-------|-------|
| `-eq` | Equal | `[ $a -eq $b ]` |
| `-ne` | Not equal | `[ $a -ne $b ]` |
| `-gt` | Greater than | `[ $a -gt $b ]` |
| `-ge` | Greater or equal | `[ $a -ge $b ]` |
| `-lt` | Less than | `[ $a -lt $b ]` |
| `-le` | Less or equal | `[ $a -le $b ]` |

### Operators so sánh string

```bash
if [ "$NAME" == "John" ]; then
    echo "Hello John"
fi

if [ -z "$NAME" ]; then
    echo "NAME is empty"
fi

if [ -n "$NAME" ]; then
    echo "NAME is not empty"
fi
```

### Kiểm tra file

```bash
FILE="/etc/hosts"

if [ -e "$FILE" ]; then
    echo "File exists"
fi

if [ -f "$FILE" ]; then
    echo "It's a regular file"
fi

if [ -d "/var/log" ]; then
    echo "It's a directory"
fi

if [ -r "$FILE" ]; then
    echo "File is readable"
fi

if [ -w "$FILE" ]; then
    echo "File is writable"
fi

if [ -x "/bin/bash" ]; then
    echo "File is executable"
fi
```

### Kết hợp điều kiện

```bash
# AND
if [ $AGE -ge 18 ] && [ $AGE -lt 65 ]; then
    echo "Working age"
fi

# OR
if [ "$COUNTRY" == "VN" ] || [ "$COUNTRY" == "Vietnam" ]; then
    echo "Hello Vietnamese"
fi
```

---

## 🔄 Vòng lặp (Loops)

### for loop

```bash
#!/bin/bash

# Loop qua list
for NAME in Alice Bob Charlie; do
    echo "Hello, $NAME"
done

# Loop qua files
for FILE in /var/log/*.log; do
    echo "Processing: $FILE"
    wc -l "$FILE"
done

# Loop qua range
for i in {1..5}; do
    echo "Number: $i"
done

# C-style for loop
for ((i=0; i<5; i++)); do
    echo "Index: $i"
done
```

### while loop

```bash
#!/bin/bash

COUNT=0

while [ $COUNT -lt 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done
```

### Đọc file từng dòng

```bash
#!/bin/bash

while IFS= read -r LINE; do
    echo "Line: $LINE"
done < /etc/hosts
```

---

## 📝 Functions

### Định nghĩa function

```bash
#!/bin/bash

# Cách 1
function greet() {
    echo "Hello, $1!"
}

# Cách 2 (POSIX compatible)
goodbye() {
    echo "Goodbye, $1!"
}

# Gọi function
greet "John"
goodbye "Jane"
```

### Return values

```bash
#!/bin/bash

add_numbers() {
    local RESULT=$(($1 + $2))
    echo $RESULT  # "Return" bằng echo
}

calculate() {
    if [ $1 -gt 100 ]; then
        return 0  # Success
    else
        return 1  # Failure
    fi
}

# Lấy output từ function
SUM=$(add_numbers 5 3)
echo "Sum: $SUM"

# Check return code
if calculate 150; then
    echo "Number is large"
fi
```

---

## 🛠️ Script thực tế: Backup Database

### Yêu cầu

- Backup MySQL database
- Nén file
- Upload lên S3
- Xóa backups local > 7 ngày

### Script hoàn chỉnh

```bash
#!/bin/bash
#
# backup_database.sh
# Backup MySQL và upload lên S3
#
# Usage: ./backup_database.sh

set -e  # Exit on error

# ============================================
# CONFIGURATION
# ============================================

DB_HOST="localhost"
DB_USER="backup_user"
DB_PASS="your_password"
DB_NAME="production_db"

BACKUP_DIR="/backup/mysql"
S3_BUCKET="s3://my-backups/mysql"
RETENTION_DAYS=7

# ============================================
# FUNCTIONS
# ============================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error() {
    log "ERROR: $1"
    exit 1
}

# ============================================
# MAIN SCRIPT
# ============================================

log "Starting backup process..."

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Generate filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"

# Backup database
log "Backing up database: $DB_NAME"
mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -ne 0 ]; then
    error "Backup failed!"
fi

log "Backup created: $BACKUP_FILE"
log "Size: $(du -h $BACKUP_FILE | cut -f1)"

# Upload to S3
log "Uploading to S3..."
aws s3 cp "$BACKUP_FILE" "$S3_BUCKET/"

if [ $? -ne 0 ]; then
    error "S3 upload failed!"
fi

log "Upload complete"

# Clean old backups
log "Cleaning backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

log "Backup process completed successfully!"
```

### Chạy với cron

```bash
# Edit crontab
crontab -e

# Thêm dòng (chạy lúc 3h sáng mỗi ngày)
0 3 * * * /home/scripts/backup_database.sh >> /var/log/backup.log 2>&1
```

---

## 🐍 Python cho DevOps

### Tại sao Python?

| Bash | Python |
|------|--------|
| Tốt cho tasks đơn giản | Tốt cho logic phức tạp |
| Chạy commands dễ | Xử lý data dễ |
| Syntax khó đọc | Syntax clean |
| Error handling yếu | Error handling mạnh |
| Không có thư viện | Hàng nghìn libraries |

### Script Python đầu tiên

```python
#!/usr/bin/env python3
"""
hello.py - Script đầu tiên
"""

import os
from datetime import datetime

def main():
    print("Hello, DevOps!")
    print(f"Today is {datetime.now().strftime('%Y-%m-%d')}")
    print(f"You are: {os.getenv('USER')}")
    print(f"Current dir: {os.getcwd()}")

if __name__ == "__main__":
    main()
```

### Chạy shell commands từ Python

```python
#!/usr/bin/env python3
"""
Chạy commands và xử lý output
"""

import subprocess

def run_command(cmd):
    """Run command and return output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode

# Ví dụ
stdout, stderr, code = run_command("ls -la /var/log")

if code == 0:
    print("Command succeeded!")
    print(stdout)
else:
    print(f"Command failed: {stderr}")
```

### Làm việc với files

```python
#!/usr/bin/env python3
"""
File operations
"""

from pathlib import Path

# Đọc file
content = Path("/etc/hosts").read_text()
print(content)

# Ghi file
Path("/tmp/test.txt").write_text("Hello World!")

# Đọc từng dòng
with open("/etc/hosts") as f:
    for line in f:
        if not line.startswith("#"):
            print(line.strip())

# Tìm files
for log_file in Path("/var/log").glob("*.log"):
    size = log_file.stat().st_size
    print(f"{log_file.name}: {size} bytes")
```

### HTTP requests

```python
#!/usr/bin/env python3
"""
API requests với requests library
"""

import requests

def check_website(url):
    """Check if website is up"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {url} is UP")
            return True
        else:
            print(f"⚠️ {url} returned {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ {url} is DOWN: {e}")
        return False

# Check multiple sites
sites = [
    "https://google.com",
    "https://github.com",
    "https://nonexistent.example.com"
]

for site in sites:
    check_website(site)
```

### JSON handling

```python
#!/usr/bin/env python3
"""
Parse JSON data
"""

import json

# Parse JSON string
data = '{"name": "John", "age": 30}'
obj = json.loads(data)
print(obj["name"])  # John

# Read JSON file
with open("config.json") as f:
    config = json.load(f)

# Write JSON file
data = {"server": "localhost", "port": 8080}
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## 📝 Tổng kết Module 03

### Bash Skills

✅ Shebang và execution  
✅ Variables và special variables  
✅ Conditionals (if/else, operators)  
✅ Loops (for, while)  
✅ Functions  
✅ Real-world scripts  

### Python Skills

✅ Basic syntax  
✅ Running shell commands  
✅ File operations  
✅ HTTP requests  
✅ JSON handling  

### Khi nào dùng gì?

```
Bash when:
├── Chạy vài commands
├── Task đơn giản
├── Pipe commands
└── Không cần logic phức tạp

Python when:
├── Xử lý data phức tạp
├── API calls
├── Error handling cần tốt
└── Code cần maintain lâu dài
```

---

## ⏭️ Tiếp theo

👉 **[LABS.md - Thực hành Scripting](LABS.md)**
