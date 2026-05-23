# Module 03: Scripting Scenarios

---

## 🎯 Mục đích

Các tình huống thực tế liên quan đến scripting mà bạn sẽ gặp khi làm DevOps.

---

## 🚨 Scenario 1: "Script chạy OK trên máy tôi, nhưng fail trên server"

### 📍 Bối cảnh

Bạn viết script trên laptop, test OK. Deploy lên server, chạy nhận lỗi:

```bash
./deploy.sh
```

**Output:**

```
./deploy.sh: line 1: syntax error near unexpected token `$'\r''
```

### 🔍 Điều tra

**Lỗi `$'\r'` là dấu hiệu file có Windows line endings (CRLF).**

```bash
# Kiểm tra file format
file deploy.sh
```

**Output xấu:**

```
deploy.sh: Bash script text executable, ASCII text, with CRLF line terminators
```

### 💡 Giải quyết

```bash
# Chuyển từ CRLF sang LF
sed -i 's/\r$//' deploy.sh

# Hoặc dùng dos2unix
dos2unix deploy.sh

# Kiểm tra lại
file deploy.sh
# deploy.sh: Bash script text executable, ASCII text
```

### 📚 Bài học

1. **Luôn dùng LF line endings** cho scripts
2. **Configure editor** để save với Unix line endings
3. **Thêm vào .gitattributes:**

   ```
   *.sh text eol=lf
   ```

---

## 🚨 Scenario 2: "Variable rỗng gây xóa nhầm"

### 📍 Bối cảnh

Script cleanup:

```bash
#!/bin/bash
BACKUP_DIR="/backup/old"
rm -rf $BACKUP_DIR/*
```

Một ngày, `BACKUP_DIR` không được set (có bug), script chạy thành:

```bash
rm -rf /*    # XÓA TOÀN BỘ HỆ THỐNG!
```

### 🔍 Vấn đề

Variable rỗng + không có quotes = thảm họa

### 💡 Giải quyết

**Cách 1: Luôn dùng quotes**

```bash
rm -rf "$BACKUP_DIR"/*
```

**Cách 2: Kiểm tra trước khi dùng**

```bash
if [ -z "$BACKUP_DIR" ]; then
    echo "ERROR: BACKUP_DIR is not set"
    exit 1
fi

rm -rf "$BACKUP_DIR"/*
```

**Cách 3: Dùng set -u**

```bash
#!/bin/bash
set -u  # Exit if variable is unset

rm -rf "$BACKUP_DIR"/*
# Script tự exit nếu BACKUP_DIR chưa được set
```

**Cách 4: Default value**

```bash
BACKUP_DIR="${BACKUP_DIR:-/tmp/default_backup}"
```

### 📚 Bài học

**Best practices cho safe scripts:**

```bash
#!/bin/bash
set -euo pipefail

# -e: Exit on error
# -u: Exit on unset variable
# -o pipefail: Exit on pipe fail
```

---

## 🚨 Scenario 3: "Cron job không chạy"

### 📍 Bối cảnh

Bạn setup cron job:

```bash
crontab -e
# Thêm:
0 3 * * * /home/user/backup.sh
```

Nhưng sáng dậy không thấy backup.

### 🔍 Điều tra

**Bước 1: Xem cron logs**

```bash
grep CRON /var/log/syslog | tail -20
```

**Bước 2: Các nguyên nhân phổ biến**

**Nguyên nhân 1: Script không có execute permission**

```bash
chmod +x /home/user/backup.sh
```

**Nguyên nhân 2: Path không đầy đủ**

Cron chạy với PATH minimal. Script dùng `docker`, `aws` sẽ fail.

```bash
# SAI
docker ps

# ĐÚNG
/usr/bin/docker ps
```

**Nguyên nhân 3: Environment variables missing**

```bash
# Cron không có env của user
# Thêm vào đầu script:
source /home/user/.bashrc
```

### 💡 Giải quyết

**Script chuẩn cho cron:**

```bash
#!/bin/bash

# Full path cho commands
PATH=/usr/local/bin:/usr/bin:/bin

# Log output
LOGFILE="/var/log/backup.log"

echo "=== Backup started at $(date) ===" >> "$LOGFILE"

# ... backup logic ...

echo "=== Backup completed at $(date) ===" >> "$LOGFILE"
```

**Crontab với logging:**

```bash
0 3 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1
```

---

## 🚨 Scenario 4: "Script chạy quá lâu"

### 📍 Bối cảnh

Script xử lý 10,000 files, mỗi file gọi `curl`. Chạy mất 5 tiếng!

```bash
for file in /data/*.json; do
    curl -X POST -d @"$file" https://api.example.com/upload
done
```

### 🔍 Vấn đề

Chạy tuần tự, mỗi request đợi response mới chạy tiếp.

### 💡 Giải quyết

**Cách 1: Parallel với xargs**

```bash
ls /data/*.json | xargs -P 10 -I {} curl -X POST -d @{} https://api.example.com/upload
```

`-P 10` = Chạy 10 processes song song

**Cách 2: GNU Parallel**

```bash
parallel -j 10 curl -X POST -d @{} https://api.example.com/upload ::: /data/*.json
```

**Cách 3: Background processes**

```bash
for file in /data/*.json; do
    curl -X POST -d @"$file" https://api.example.com/upload &
    
    # Limit concurrent jobs
    if (( $(jobs -r -p | wc -l) >= 10 )); then
        wait -n
    fi
done
wait
```

### 📚 Kết quả

| Cách | Thời gian |
|------|-----------|
| Tuần tự | 5 giờ |
| Parallel (10 jobs) | 30 phút |

---

## 🚨 Scenario 5: "Python script thiếu dependencies"

### 📍 Bối cảnh

Deploy Python script lên server mới:

```bash
python3 health_check.py
```

**Output:**

```
ModuleNotFoundError: No module named 'requests'
```

### 💡 Giải quyết

**Cách 1: requirements.txt**

```bash
# Tạo requirements.txt
pip freeze > requirements.txt

# Cài trên server mới
pip install -r requirements.txt
```

**Cách 2: Virtual environment**

```bash
# Tạo venv
python3 -m venv venv
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Chạy
python health_check.py
```

**Cách 3: Shebang với venv**

```python
#!/home/user/project/venv/bin/python3
"""Script sử dụng venv cụ thể"""
```

**Cách 4: Docker (best practice)**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "health_check.py"]
```

---

## 🚨 Scenario 6: "Script bị treo không thoát"

### 📍 Bối cảnh

Script chờ input nhưng chạy trong cron (không có TTY):

```bash
read -p "Continue? " answer
```

**Script treo vô hạn!**

### 💡 Giải quyết

**Cách 1: Timeout**

```bash
# Timeout sau 5 giây
read -t 5 -p "Continue? " answer || answer="yes"
```

**Cách 2: Default khi không interactive**

```bash
if [ -t 0 ]; then
    # Running interactively
    read -p "Continue? " answer
else
    # Running non-interactively (cron, pipe)
    answer="yes"
fi
```

**Cách 3: Force non-interactive**

```bash
export DEBIAN_FRONTEND=noninteractive
apt-get install -y nginx
```

---

## 📚 Best Practices Tổng kết

### Script Template

```bash
#!/bin/bash
#
# script_name.sh
# Description: What this script does
# Usage: ./script_name.sh [options]
#

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

error() {
    log "ERROR: $*" >&2
    exit 1
}

# Cleanup on exit
cleanup() {
    # Remove temp files, etc.
    log "Cleaning up..."
}
trap cleanup EXIT

# Main function
main() {
    log "Starting $SCRIPT_NAME..."
    # ... main logic ...
    log "Completed successfully"
}

# Run main
main "$@"
```

---

## ⏭️ Module tiếp theo

👉 **[Module 04: Git](../04_GIT/README.md)**
