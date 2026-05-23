# Module 03: Scripting Labs

---

## 🎯 Mục tiêu

Sau labs này, bạn sẽ:
- Viết được Bash scripts thực tế
- Tự động hóa các tasks lặp lại
- Viết Python scripts cho DevOps
- Debug và xử lý lỗi trong scripts

---

## 🔧 Lab 1: Script đầu tiên

### 🎬 Bối cảnh

Mỗi sáng bạn phải check: server có chạy không, disk còn trống không, có process nào chiếm CPU không. Hãy viết script làm việc này!

### Bước 1: Tạo script

```bash
cd ~/devops-workspace/scripts
nano morning_check.sh
```

### Bước 2: Viết nội dung

```bash
#!/bin/bash
#
# morning_check.sh
# Script kiểm tra hệ thống mỗi sáng
#

echo "=========================================="
echo "   MORNING SYSTEM CHECK"
echo "   $(date)"
echo "=========================================="
echo

# 1. System uptime
echo "📊 UPTIME:"
uptime
echo

# 2. Disk usage
echo "💾 DISK USAGE:"
df -h | grep -E "^/dev|Filesystem"
echo

# 3. Memory usage
echo "🧠 MEMORY:"
free -h
echo

# 4. Top 5 CPU processes
echo "⚙️ TOP 5 CPU PROCESSES:"
ps aux --sort=-%cpu | head -6
echo

# 5. Check important services
echo "🔧 SERVICES STATUS:"
for SERVICE in ssh nginx docker; do
    if systemctl is-active --quiet $SERVICE 2>/dev/null; then
        echo "  ✅ $SERVICE: running"
    else
        echo "  ❌ $SERVICE: not running"
    fi
done
echo

echo "=========================================="
echo "   CHECK COMPLETE"
echo "=========================================="
```

### Bước 3: Chạy script

```bash
chmod +x morning_check.sh
./morning_check.sh
```

### ✅ Checkpoint Lab 1

- [ ] Script chạy không lỗi
- [ ] Hiểu từng phần của script
- [ ] Biết cách thêm checks mới

---

## 📦 Lab 2: Xử lý Arguments

### 🎬 Bối cảnh

Viết script nhận tham số từ command line.

### Script: greet.sh

```bash
#!/bin/bash
#
# greet.sh - Chào người dùng
# Usage: ./greet.sh <name> [greeting]
#

# Check số arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <name> [greeting]"
    echo "Example: $0 John 'Good morning'"
    exit 1
fi

NAME=$1
GREETING=${2:-"Hello"}  # Default là "Hello" nếu không truyền

echo "$GREETING, $NAME!"
echo "Today is $(date +%A)"
```

### Test script

```bash
chmod +x greet.sh

./greet.sh
# Output: Usage: ./greet.sh <name> [greeting]

./greet.sh John
# Output: Hello, John!

./greet.sh John "Good morning"
# Output: Good morning, John!
```

### ✅ Checkpoint Lab 2

- [ ] Hiểu $1, $2, $#
- [ ] Biết set default value với ${var:-default}
- [ ] Validate arguments trước khi dùng

---

## 🔀 Lab 3: Conditionals thực tế

### 🎬 Bối cảnh

Viết script kiểm tra disk usage và alert nếu sắp đầy.

### Script: check_disk.sh

```bash
#!/bin/bash
#
# check_disk.sh - Kiểm tra disk và alert
#

THRESHOLD=80
ALERT_EMAIL="admin@example.com"

echo "Checking disk usage..."
echo

# Lấy disk usage của partition root
USAGE=$(df / | grep / | awk '{print $5}' | sed 's/%//')

echo "Current usage: ${USAGE}%"
echo "Threshold: ${THRESHOLD}%"
echo

if [ "$USAGE" -ge "$THRESHOLD" ]; then
    echo "⚠️ WARNING: Disk usage is above threshold!"
    echo
    echo "Top 10 largest directories:"
    du -sh /* 2>/dev/null | sort -h | tail -10
    echo
    echo "Consider cleaning:"
    echo "  - /var/log (log files)"
    echo "  - /tmp (temp files)"
    echo "  - Old docker images: docker system prune"
else
    echo "✅ Disk usage is OK"
fi
```

### Test

```bash
chmod +x check_disk.sh
./check_disk.sh
```

---

## 🔄 Lab 4: Loops thực tế

### 🎬 Bối cảnh

Kiểm tra nhiều servers cùng lúc.

### Script: check_servers.sh

```bash
#!/bin/bash
#
# check_servers.sh - Ping nhiều servers
#

# List of servers to check
SERVERS=(
    "8.8.8.8"          # Google DNS
    "1.1.1.1"          # Cloudflare DNS
    "github.com"
    "google.com"
)

echo "=========================================="
echo "   SERVER CONNECTIVITY CHECK"
echo "=========================================="
echo

# Counter
UP=0
DOWN=0

for SERVER in "${SERVERS[@]}"; do
    # Ping 1 lần, timeout 2 giây
    if ping -c 1 -W 2 "$SERVER" &> /dev/null; then
        echo "✅ $SERVER - UP"
        ((UP++))
    else
        echo "❌ $SERVER - DOWN"
        ((DOWN++))
    fi
done

echo
echo "=========================================="
echo "Summary: $UP up, $DOWN down"
echo "=========================================="

# Exit code based on result
if [ $DOWN -gt 0 ]; then
    exit 1
else
    exit 0
fi
```

---

## 📝 Lab 5: Functions

### 🎬 Bối cảnh

Tổ chức code thành functions để dễ maintain.

### Script: utils.sh (Library)

```bash
#!/bin/bash
#
# utils.sh - Common utility functions
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if running as root
is_root() {
    [ "$EUID" -eq 0 ]
}

# Require root
require_root() {
    if ! is_root; then
        log_error "This script must be run as root"
        exit 1
    fi
}

# Confirm action
confirm() {
    read -p "$1 [y/N] " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}
```

### Script sử dụng utils.sh

```bash
#!/bin/bash
#
# deploy.sh - Uses utils.sh
#

# Import utils
source ./utils.sh

log_info "Starting deployment..."

# Check requirements
if ! command_exists docker; then
    log_error "Docker is not installed"
    exit 1
fi

log_info "Docker found: $(docker --version)"

# Confirm before proceeding
if ! confirm "Continue with deployment?"; then
    log_warn "Deployment cancelled"
    exit 0
fi

log_info "Deploying..."
# ... deployment logic ...

log_info "Deployment complete!"
```

---

## 🛠️ Lab 6: Script thực tế - Log Analyzer

### 🎬 Bối cảnh

Phân tích access log và tìm các patterns.

### Script: analyze_logs.sh

```bash
#!/bin/bash
#
# analyze_logs.sh - Phân tích Nginx access log
#
# Usage: ./analyze_logs.sh <logfile>
#

LOG_FILE=${1:-"/var/log/nginx/access.log"}

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file not found: $LOG_FILE"
    exit 1
fi

echo "=========================================="
echo "   LOG ANALYSIS: $LOG_FILE"
echo "=========================================="
echo

# Total requests
TOTAL=$(wc -l < "$LOG_FILE")
echo "📊 Total requests: $TOTAL"
echo

# Top 10 IPs
echo "🔝 Top 10 IP addresses:"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10
echo

# Top 10 URLs
echo "🔝 Top 10 URLs:"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10
echo

# Status codes distribution
echo "📈 Status codes:"
awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -rn
echo

# Errors (4xx, 5xx)
ERRORS=$(awk '$9 ~ /^[45]/' "$LOG_FILE" | wc -l)
ERROR_PCT=$(echo "scale=2; $ERRORS * 100 / $TOTAL" | bc)
echo "❌ Error rate: $ERRORS/$TOTAL ($ERROR_PCT%)"
echo

# Recent 5 errors
echo "🔍 Recent 5 errors:"
awk '$9 ~ /^[45]/' "$LOG_FILE" | tail -5
```

---

## 🐍 Lab 7: Python Script cơ bản

### 🎬 Bối cảnh

Viết Python script kiểm tra health của websites.

### Script: health_check.py

```python
#!/usr/bin/env python3
"""
health_check.py - Check website health
"""

import requests
import sys
from datetime import datetime

def check_url(url, timeout=5):
    """Check if URL is accessible"""
    try:
        response = requests.get(url, timeout=timeout)
        return {
            'url': url,
            'status': 'UP',
            'code': response.status_code,
            'time_ms': int(response.elapsed.total_seconds() * 1000)
        }
    except requests.RequestException as e:
        return {
            'url': url,
            'status': 'DOWN',
            'error': str(e)
        }

def main():
    urls = [
        'https://google.com',
        'https://github.com',
        'https://httpbin.org/status/200',
        'https://httpbin.org/status/500',
    ]
    
    print(f"\n{'='*50}")
    print(f"  HEALTH CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    results = []
    for url in urls:
        result = check_url(url)
        results.append(result)
        
        if result['status'] == 'UP':
            status_icon = '✅'
            details = f"HTTP {result['code']} - {result['time_ms']}ms"
        else:
            status_icon = '❌'
            details = result.get('error', 'Unknown error')
        
        print(f"{status_icon} {url}")
        print(f"   {details}\n")
    
    # Summary
    up_count = sum(1 for r in results if r['status'] == 'UP')
    print(f"{'='*50}")
    print(f"  Summary: {up_count}/{len(results)} sites UP")
    print(f"{'='*50}\n")
    
    # Exit code
    sys.exit(0 if up_count == len(results) else 1)

if __name__ == '__main__':
    main()
```

### Chạy

```bash
pip3 install requests
chmod +x health_check.py
./health_check.py
```

---

## 📊 Lab 8: Python xử lý JSON

### Script: parse_config.py

```python
#!/usr/bin/env python3
"""
parse_config.py - Đọc và validate config JSON
"""

import json
import sys
from pathlib import Path

def load_config(filepath):
    """Load config from JSON file"""
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)

def validate_config(config):
    """Validate required fields"""
    required = ['app_name', 'port', 'database']
    missing = [field for field in required if field not in config]
    
    if missing:
        print(f"Error: Missing fields: {missing}")
        return False
    
    if not isinstance(config['port'], int):
        print("Error: 'port' must be an integer")
        return False
    
    if config['port'] < 1 or config['port'] > 65535:
        print("Error: 'port' must be between 1-65535")
        return False
    
    return True

def main():
    # Create sample config
    sample_config = {
        "app_name": "MyApp",
        "port": 8080,
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp_db"
        },
        "features": {
            "cache": True,
            "logging": True
        }
    }
    
    # Save sample
    config_file = Path("config.json")
    config_file.write_text(json.dumps(sample_config, indent=2))
    print(f"Created sample config: {config_file}")
    
    # Load and validate
    config = load_config(config_file)
    
    print("\nConfig contents:")
    print(json.dumps(config, indent=2))
    
    print("\nValidating...")
    if validate_config(config):
        print("✅ Config is valid!")
    else:
        print("❌ Config is invalid!")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## 🎓 Tổng kết Labs

| Lab | Skill | Output |
|-----|-------|--------|
| 1 | Basic script | morning_check.sh |
| 2 | Arguments | greet.sh |
| 3 | Conditionals | check_disk.sh |
| 4 | Loops | check_servers.sh |
| 5 | Functions | utils.sh |
| 6 | Real-world | analyze_logs.sh |
| 7 | Python basics | health_check.py |
| 8 | Python JSON | parse_config.py |

---

## ⏭️ Tiếp theo

👉 **[SCENARIOS.md - Tình huống Scripting](SCENARIOS.md)**
