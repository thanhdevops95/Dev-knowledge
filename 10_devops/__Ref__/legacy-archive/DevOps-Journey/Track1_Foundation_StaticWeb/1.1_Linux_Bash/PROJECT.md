# 🎯 Project: Linux & Bash

> **Mini project to apply Linux and Bash scripting knowledge.**
>
> *Mini project để áp dụng kiến thức Linux và Bash scripting.*

---

## 📋 Project Overview (Tổng quan dự án)

### Project Name: **Server Monitoring Dashboard Script**

*(Tên dự án: Script Dashboard Giám sát Máy chủ)*

Build a set of scripts to monitor and report server status.
*(Xây dựng một bộ scripts để monitor và report trạng thái server.)*

### Objectives (Mục tiêu)

- Apply Bash scripting knowledge. *(Áp dụng kiến thức Bash scripting.)*
- Work with system commands. *(Làm việc với system commands.)*
- Process text and create reports. *(Xử lý text và tạo reports.)*
- Automation with cron jobs. *(Automation với cron jobs.)*

### Duration (Thời gian): 2-3 days *(2-3 ngày)*

---

## 🎯 Requirements (Yêu cầu)

### Core Features (Tính năng cốt lõi)

#### 1. System Information Collector (`collect_info.sh`)

Script to collect system information:
*(Script thu thập thông tin hệ thống:)*

```
Output format:
=====================================
SYSTEM REPORT - 2024-01-15 10:30:00
=====================================

HOSTNAME: my-server
OS: Ubuntu 22.04 LTS
KERNEL: 5.15.0-91-generic
UPTIME: 5 days, 3 hours, 25 minutes

CPU:
  Model: Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
  Cores: 8
  Usage: 15%

MEMORY:
  Total: 16 GB
  Used: 8 GB (50%)
  Free: 8 GB

DISK:
  /       : 45% used (45GB / 100GB)
  /home   : 60% used (120GB / 200GB)

NETWORK:
  eth0: 192.168.1.100
  
TOP 5 PROCESSES (by CPU):
  PID    CPU%   MEM%   COMMAND
  1234   25.0   5.0    nginx
  ...
=====================================
```

#### 2. Health Checker (`health_check.sh`)

Script to check server "health":
*(Script kiểm tra "sức khỏe" server:)*

- [ ] CPU usage < 80%
- [ ] Memory usage < 90%
- [ ] Disk usage < 85%
- [ ] Required services running (nginx, docker)
- [ ] Network connectivity (ping 8.8.8.8)
- [ ] DNS resolution working

```
Output:
[✓] CPU Usage: 15% (OK)
[✓] Memory Usage: 50% (OK)
[✓] Disk Usage: 45% (OK)
[✓] Service nginx: running
[✗] Service docker: stopped  ← ALERT!
[✓] Network: OK
[✓] DNS: OK

Status: WARNING - 1 issue found
```

#### 3. Log Analyzer (`analyze_logs.sh`)

Script to analyze log files:
*(Script phân tích log files:)*

Input: Log file path
Output:

- Total entries. *(Tổng số entries.)*
- Breakdown by log level (INFO, WARNING, ERROR).
- Top 5 error messages.
- Timeline (entries per hour).

#### 4. Alert System (`alert.sh`)

Script to send alerts when issues occur:
*(Script gửi alerts khi có vấn đề:)*

- Write alerts to `/var/log/server_alerts.log`. *(Ghi alerts vào file `/var/log/server_alerts.log`.)*
- (Optional) Send email notification. *(Gửi email notification.)*
- Include timestamp and severity level. *(Include timestamp và severity level.)*

#### 5. Main Dashboard (`dashboard.sh`)

Main script integrating all modules:
*(Script chính tích hợp tất cả:)*

```bash
./dashboard.sh [options]

Options:
  -i, --info      Show system information
  -h, --health    Run health check
  -l, --logs      Analyze logs
  -a, --all       Run all checks
  -w, --watch     Continuous monitoring (refresh every 5s)
  --help          Show help
```

---

## 📁 Project Structure (Cấu trúc dự án)

```
server-monitor/
├── scripts/
│   ├── collect_info.sh
│   ├── health_check.sh
│   ├── analyze_logs.sh
│   ├── alert.sh
│   └── dashboard.sh
├── config/
│   ├── thresholds.conf    # CPU_THRESHOLD=80, etc.
│   └── services.conf      # List of services to monitor (Danh sách dịch vụ cần giám sát)
├── logs/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── install.sh             # Installation script (Script cài đặt)
├── uninstall.sh          # Cleanup script (Script dọn dẹp)
└── README.md
```

---

## 📝 Detailed Specifications (Đặc tả chi tiết)

### `thresholds.conf`

```bash
# Alert thresholds (Ngưỡng cảnh báo)
CPU_THRESHOLD=80
MEMORY_THRESHOLD=90
DISK_THRESHOLD=85

# Services to monitor (Dịch vụ cần giám sát)
SERVICES="nginx docker ssh"

# Log paths (Đường dẫn log)
SYSTEM_LOG=/var/log/syslog
APP_LOG=/var/log/app.log

# Alert settings (Cài đặt cảnh báo)
ALERT_LOG=/var/log/server_alerts.log
```

### `collect_info.sh` Specifications (Đặc tả)

```bash
#!/bin/bash

# Functions needed (Các hàm cần thiết):
# - get_hostname()
# - get_os_info()
# - get_kernel_version()
# - get_uptime()
# - get_cpu_info()
# - get_memory_info()
# - get_disk_info()
# - get_network_info()
# - get_top_processes()
# - generate_report()

# Output options (Tùy chọn đầu ra):
# - Terminal (colored)
# - File (plain text)
# - JSON format (optional bonus)
```

### `health_check.sh` Specifications (Đặc tả)

```bash
#!/bin/bash

# Exit codes (Mã thoát):
# 0 = All checks passed (Tất cả kiểm tra đạt)
# 1 = Warning (non-critical issues) (Cảnh báo - vấn đề không nghiêm trọng)
# 2 = Critical (immediate attention needed) (Nghiêm trọng - cần xử lý ngay)

# Check functions (Các hàm kiểm tra):
# - check_cpu()
# - check_memory()
# - check_disk()
# - check_services()
# - check_network()
# - check_dns()

# Each function returns (Mỗi hàm trả về):
# 0 = OK
# 1 = Warning
# 2 = Critical
```

---

## ✅ Acceptance Criteria (Tiêu chí chấp nhận)

### Must Have (Bắt buộc)

- [ ] All 5 scripts working correctly. *(Cả 5 scripts hoạt động đúng.)*
- [ ] Proper error handling. *(Xử lý lỗi đúng cách.)*
- [ ] Colored terminal output. *(Đầu ra terminal có màu.)*
- [ ] Help messages for all scripts. *(Thông báo trợ giúp cho tất cả scripts.)*
- [ ] Configuration file support. *(Hỗ trợ file cấu hình.)*
- [ ] Appropriate exit codes. *(Exit codes phù hợp.)*

### Should Have (Nên có)

- [ ] Logging of script activities. *(Ghi log hoạt động script.)*
- [ ] Report generation (text files). *(Tạo báo cáo (text files).)*
- [ ] Watch mode with refresh. *(Chế độ watch với refresh.)*
- [ ] Installation script. *(Script cài đặt.)*

### Nice to Have (Có thì tốt)

- [ ] JSON output option. *(Tùy chọn xuất JSON.)*
- [ ] Email alerts. *(Cảnh báo qua email.)*
- [ ] Historical data storage. *(Lưu trữ dữ liệu lịch sử.)*
- [ ] Simple web dashboard (bonus). *(Dashboard web đơn giản.)*

---

## 🔧 Technical Requirements (Yêu cầu kỹ thuật)

### Bash Version (Phiên bản Bash)

- Bash 4.0+ required. *(Yêu cầu Bash 4.0+.)*

### Permissions (Quyền hạn)

- Some commands need sudo (e.g., reading system logs).
  *(Một số lệnh cần sudo (ví dụ: đọc log hệ thống).)*
- Handle permission errors gracefully.
  *(Xử lý lỗi quyền hạn một cách êm ái.)*

### Portability (Tính di động)

- Should work on Ubuntu 20.04+. *(Nên hoạt động trên Ubuntu 20.04+.)*
- Handle missing commands (check if command exists).
  *(Xử lý lệnh bị thiếu (kiểm tra lệnh có tồn tại không).)*

### Code Quality (Chất lượng code)

- Use functions for modularity. *(Sử dụng hàm để module hóa.)*
- Include comments. *(Bao gồm comments.)*
- Consistent coding style. *(Phong cách code nhất quán.)*
- No hardcoded values (use config). *(Không hardcode giá trị (dùng config).)*

---

## 📊 Evaluation Rubric (Thang điểm đánh giá)

| Criteria (Tiêu chí) | Points (Điểm) |
|---------------------|---------------|
| **Functionality** (scripts work correctly) *(Scripts hoạt động đúng)* | 40 |
| **Code Quality** (clean, readable, documented) *(Code sạch, dễ đọc, có tài liệu)* | 20 |
| **Error Handling** (graceful failures) *(Xử lý lỗi êm ái)* | 15 |
| **Configuration** (flexible, no hardcoding) *(Linh hoạt, không hardcode)* | 10 |
| **User Experience** (helpful messages, colors) *(Thông báo hữu ích, có màu)* | 10 |
| **Bonus Features** *(Tính năng bổ sung)* | 5 |
| **Total** *(Tổng)* | **100** |

### Grading (Xếp loại)

- 90-100: Excellent *(Xuất sắc)*
- 80-89: Good *(Tốt)*
- 70-79: Satisfactory *(Đạt yêu cầu)*
- Below 70: Needs improvement *(Cần cải thiện)*

---

## 🚀 Getting Started (Bắt đầu)

### Step 1: Setup (Bước 1: Thiết lập)

```bash
# Create project directory (Tạo thư mục dự án)
mkdir -p ~/server-monitor/{scripts,config,logs,reports}
cd ~/server-monitor

# Create config file (Tạo file cấu hình)
cat << 'EOF' > config/thresholds.conf
CPU_THRESHOLD=80
MEMORY_THRESHOLD=90
DISK_THRESHOLD=85
SERVICES="nginx ssh"
EOF
```

### Step 2: Start Simple (Bước 2: Bắt đầu đơn giản)

```bash
# Begin with collect_info.sh (Bắt đầu với collect_info.sh)
touch scripts/collect_info.sh
chmod +x scripts/collect_info.sh

# Start with basic structure (Bắt đầu với cấu trúc cơ bản)
cat << 'EOF' > scripts/collect_info.sh
#!/bin/bash
# System Information Collector (Bộ thu thập thông tin hệ thống)

echo "Starting system info collection..."
# Your code here (Code của bạn ở đây)
EOF
```

### Step 3: Iterate (Bước 3: Phát triển dần)

- Implement one function at a time. *(Triển khai từng hàm một.)*
- Test frequently. *(Test thường xuyên.)*
- Commit progress to git. *(Commit tiến độ vào git.)*

---

## 💡 Hints (Gợi ý)

### Getting System Info (Lấy thông tin hệ thống)

```bash
# Hostname
hostname

# OS info (Thông tin OS)
cat /etc/os-release

# CPU usage (Sử dụng CPU)
top -bn1 | grep "Cpu(s)"

# Memory (Bộ nhớ)
free -h

# Disk (Đĩa)
df -h
```

### Colored Output (Đầu ra có màu)

```bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[✓]${NC} Check passed"
echo -e "${RED}[✗]${NC} Check failed"
```

### Service Check (Kiểm tra dịch vụ)

```bash
systemctl is-active --quiet nginx && echo "running" || echo "stopped"
```

---

## 📥 Submission (Nộp bài)

### Required Files (Files bắt buộc)

1. All script files. *(Tất cả script files.)*
2. Config files. *(Các file cấu hình.)*
3. README.md with instructions. *(README.md với hướng dẫn.)*
4. Sample output/screenshots. *(Mẫu output/screenshots.)*

### Submission Format (Định dạng nộp bài)

```bash
# Create archive (Tạo file nén)
tar -czvf server-monitor-yourname.tar.gz server-monitor/
```

---

## 🔗 Resources (Tài nguyên)

- [CHEATSHEET.md](./CHEATSHEET.md) - Command reference *(Tra cứu lệnh)*
- [LABS.md](./LABS.md) - Review labs *(Xem lại labs)*
- [SOLUTIONS.md](./SOLUTIONS.md) - Example solutions *(Đáp án mẫu)*

---

## 🔗 Navigation (Điều hướng)

[⬅️ README](./README.md) | [LABS](./LABS.md) | [QUIZ ➡️](./QUIZ.md)

---

**Good luck! 🚀** *(Chúc may mắn! 🚀)*
