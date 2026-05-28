# ✅ Solutions: Linux & Bash

> Solutions for Exercises and Project. **Try to solve it yourself first!**
>
> *Đáp án cho Exercises và Project. **Hãy thử tự làm trước khi xem!***

---

## 🗂️ Exercise 1: File System Navigation (Bài tập 1: Điều hướng File System)

```bash
# 1. Create directory structure (Tạo cấu trúc thư mục)
mkdir -p ~/devops-practice/{projects/{web-app/{src,tests,docs},api-server/{src,tests}},scripts,logs}

# 2. Create README.md in each src/ (Tạo README.md trong mỗi src/)
touch ~/devops-practice/projects/web-app/src/README.md
touch ~/devops-practice/projects/api-server/src/README.md

# 3. Create 5 dummy log files (Tạo 5 files log giả)
# Option 1: Using curly braces (Cách 1: Dùng ngoặc nhọn)
touch ~/devops-practice/logs/app-0{1,2,3,4,5}.log
# Option 2: Using for loop (Cách 2: Dùng vòng lặp for)
for i in {1..5}; do touch ~/devops-practice/logs/app-0$i.log; done

# 4. Move logs to archive (Di chuyển logs vào archive)
mkdir -p ~/devops-practice/logs/archive
mv ~/devops-practice/logs/*.log ~/devops-practice/logs/archive/

# 5. Delete empty directory (Xóa thư mục trống)
rmdir ~/devops-practice/projects/api-server/tests/
```

---

## 🔐 Exercise 2: Permissions Management (Bài tập 2: Quản lý quyền hạn)

```bash
# 1-3. Create files (Tạo files)
echo "This is confidential" > secret.txt
echo "This is public" > public.txt
cat << 'EOF' > deploy.sh
#!/bin/bash
echo "Deploying application..."
EOF

# 4. Set permissions (Thiết lập các quyền hạn)
chmod 400 secret.txt    # -r-------- (Owner Read only)
chmod 644 public.txt    # -rw-r--r-- (Standard text file)
chmod 711 deploy.sh     # -rwx--x--x (Owner full, Others execute)

# 5. Create group and add user (Tạo group và thêm user)
sudo groupadd devteam
sudo usermod -aG devteam $USER

# 6. Change group owner (Thay đổi nhóm sở hữu)
sudo chgrp devteam deploy.sh
```

---

## 🔍 Exercise 3: Text Processing (Bài tập 3: Xử lý văn bản)

```bash
# 1. Count ERROR lines (Đếm số dòng ERROR)
grep -c "ERROR" server.log
# Expected Output: 3

# 2. List unique users who logged in (Liệt kê unique users đã login)
grep "User login" server.log | awk '{print $NF}' | sort | uniq
# Output: admin, john

# 3. Display timestamp and message for WARNING (Hiển thị WARNING)
grep "WARNING" server.log | awk '{print $1, $2, $4, $5, $6, $7}'
# Or simply:
grep "WARNING" server.log

# 4. Find the last line containing "admin" (Tìm dòng cuối cùng chứa "admin")
grep "admin" server.log | tail -1

# 5. Replace INFO with [INFO] (Thay thế INFO thành [INFO])
sed 's/INFO/[INFO]/g' server.log > server_new.log

# 6. Display first 5 lines (Hiển thị 5 dòng đầu tiên)
head -5 server.log

# 7. Count "connection" occurrences (case-insensitive) (Đếm số lần xuất hiện "connection")
grep -i -c "connection" server.log
# To count ALL occurrences across lines:
grep -io "connection" server.log | wc -l
```

---

## 📊 Exercise 4: Process Management (Bài tập 4: Quản lý tiến trình)

```bash
# 1. Top 5 processes by CPU (Top 5 tiến trình dùng nhiều CPU nhất)
ps aux --sort=-%cpu | head -6

# 2. Top 5 processes by RAM (Top 5 tiến trình dùng nhiều RAM nhất)
ps aux --sort=-%mem | head -6

# 3. Processes of the current user (Các tiến trình của người dùng hiện tại)
ps -u $USER

# 4. Run sleep in the background (Chạy sleep trong background)
sleep 300 &

# 5. Find the PID of the sleep process (Tìm PID của tiến trình sleep)
pgrep sleep
# Or (Hoặc)
ps aux | grep sleep

# 6. Kill the process (Dừng tiến trình)
kill $(pgrep sleep)
# Or with a specific PID (Hoặc với PID cụ thể)
# kill 12345

# Bonus: Kill all processes with "sleep" in name (Dừng tất cả tiến trình tên "sleep")
pkill sleep
# Or (Hoặc)
killall sleep
```

---

## 🔧 Exercise 5: Bash Scripting Basics (Bài tập 5: Cơ bản về Bash Scripting)

### Task 1: sysinfo.sh (Báo cáo thông tin hệ thống)

```bash
#!/bin/bash
# System Information Script (Script lấy thông tin hệ thống)

echo "=========================================="
echo "         SYSTEM INFORMATION"
echo "=========================================="
echo ""
echo "Hostname    : $(hostname)"
echo "OS Version  : $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "Kernel      : $(uname -r)"
echo "CPU Model   : $(grep "model name" /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs)"
echo "Total RAM   : $(free -h | grep Mem | awk '{print $2}')"
echo "Disk Usage  : $(df -h / | tail -1 | awk '{print $5}')"
echo "Date/Time   : $(date)"
echo "Uptime      : $(uptime -p)"
echo ""
echo "=========================================="
```

### Task 2: greet.sh (Script gửi lời chào)

```bash
#!/bin/bash
# Greeting Script based on time (Script chào hỏi theo thời gian)

echo -n "Enter your name (Nhập tên bạn): "
read name

hour=$(date +%H)

if [ $hour -ge 5 ] && [ $hour -lt 12 ]; then
    greeting="Good morning"
elif [ $hour -ge 12 ] && [ $hour -lt 18 ]; then
    greeting="Good afternoon"
elif [ $hour -ge 18 ] && [ $hour -lt 22 ]; then
    greeting="Good evening"
else
    greeting="Good night"
fi

echo "$greeting, $name!"
```

### Task 3: counter.sh (Bộ đếm file)

```bash
#!/bin/bash
# File Counter Script (Script đếm tệp tin)

if [ -z "$1" ]; then
    echo "Usage (Cách dùng): $0 <directory>"
    exit 1
fi

dir="$1"

if [ ! -d "$dir" ]; then
    echo "Error: $dir is not a directory (Lỗi: $dir không phải thư mục)"
    exit 1
fi

# Count files, dirs, and hidden items (Đếm file, thư mục và các mục ẩn)
files=$(find "$dir" -maxdepth 1 -type f ! -name ".*" | wc -l)
dirs=$(find "$dir" -maxdepth 1 -type d ! -name ".*" ! -path "$dir" | wc -l)
hidden=$(ls -la "$dir" | grep "^\." | wc -l)

echo "Contents of: $dir"
echo "Files       : $files"
echo "Directories : $dirs"
echo "Hidden items: $hidden"
```

---

## 🔄 Exercise 6: Loops and Conditions (Bài tập 6: Vòng lặp và Điều kiện)

### Task 1: backup.sh (Tự động sao lưu)

```bash
#!/bin/bash
# Backup Script with validation (Script sao lưu có kiểm tra lỗi)

source_dir="$1"
backup_base="$2"

# Validate arguments (Kiểm tra đối số)
if [ -z "$source_dir" ] || [ -z "$backup_base" ]; then
    echo "Usage (Sử dụng): $0 <source_dir> <backup_dir>"
    exit 1
fi

# Check source exists (Kiểm tra nguồn tồn tại)
if [ ! -d "$source_dir" ]; then
    echo "Error: Source directory does not exist (Lỗi: Thư mục nguồn không tồn tại)"
    exit 1
fi

# Create backup directory with timestamp (Tạo thư mục backup với dấu thời gian)
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="${backup_base}/backup_${timestamp}"
mkdir -p "$backup_dir"

# Copy files (Sao chép tệp tin)
count=0
for file in "$source_dir"/*; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_dir/"
        ((count++))
    fi
done

echo "Backup completed! (Sao lưu hoàn tất!)"
echo "Location: $backup_dir"
echo "Files copied: $count"
```

### Task 2: rotate.sh (Script luân chuyển log)

```bash
#!/bin/bash
# Log Rotation Script (Script quản lý tập tin log)

log_dir="$1"

if [ -z "$log_dir" ] || [ ! -d "$log_dir" ]; then
    echo "Usage (Sử dụng): $0 <log_directory>"
    exit 1
fi

compressed=0
deleted=0

# Compress large log files (Nén các file log lớn)
for file in "$log_dir"/*.log; do
    [ -f "$file" ] || continue
    # Cross-platform way to get file size (Cách lấy size file trên nhiều OS)
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
    
    if [ $size -gt 1048576 ]; then  # > 1MB
        gzip "$file"
        echo "Compressed: $file"
        ((compressed++))
    fi
done

# Delete old compressed files (Xóa các file nén đã cũ)
find "$log_dir" -name "*.gz" -mtime +7 -delete -print | while read file; do
    echo "Deleted: $file"
    ((deleted++))
done

echo "Summary (Tổng kết):"
echo "  Compressed: $compressed files"
echo "  Deleted: $deleted files"
```

### Task 3: check_services.sh (Kiểm tra dịch vụ)

```bash
#!/bin/bash
# Service Status Checker with colors (Script kiểm tra dịch vụ kèm màu sắc)

services=("nginx" "docker" "ssh")
failed=0

echo "=================================="
echo "     SERVICE STATUS CHECK"
echo "=================================="
printf "%-15s %s\n" "SERVICE" "STATUS"
echo "----------------------------------"

for service in "${services[@]}"; do
    if systemctl is-active --quiet "$service" 2>/dev/null; then
        printf "%-15s \e[32m%s\e[0m\n" "$service" "RUNNING"
    else
        printf "%-15s \e[31m%s\e[0m\n" "$service" "STOPPED"
        ((failed++))
    fi
done

echo "=================================="

if [ $failed -gt 0 ]; then
    echo "Warning (Cảnh báo): $failed service(s) not running"
    exit 1
else
    echo "All services running (Tất cả dịch vụ đang hoạt động)"
    exit 0
fi
```

---

## 🌐 Exercise 7: Networking Commands (Bài tập 7: Các lệnh mạng)

```bash
# 1. IP addresses of all interfaces (Xem IP của tất cả interfaces)
ip addr show | grep "inet " | awk '{print $2}'
# Or (Hoặc)
hostname -I

# 2. Check if port 80 is listening (Kiểm tra port 80 đang mở)
ss -tuln | grep :80
# Or (Hoặc)
netstat -tuln | grep :80

# 3. Check connectivity to google.com (Kiểm tra kết nối)
ping -c 3 google.com

# 4. Trace route to 8.8.8.8 (Dò tìm đường truyền)
traceroute 8.8.8.8
# Or on Ubuntu (Hoặc trên Ubuntu)
tracepath 8.8.8.8

# 5. Established connections (Các kết nối đang hoạt động)
ss -t state established
# Or (Hoặc)
netstat -tn | grep ESTABLISHED

# 6. Process using port 22 (Process sử dụng port 22)
sudo ss -tulnp | grep :22
# Or (Hoặc)
sudo lsof -i :22

# Bonus: Connectivity checker script (Script kiểm tra kết nối hàng loạt)
#!/bin/bash
hosts=("google.com" "github.com" "8.8.8.8")

for host in "${hosts[@]}"; do
    if ping -c 1 -W 2 "$host" &>/dev/null; then
        echo "[OK] $host is reachable (Có thể kết nối)"
    else
        echo "[FAIL] $host is not reachable (Không thể kết nối)"
    fi
done
```

---

## 📦 Exercise 8: Package Management (Bài tập 8: Quản lý gói)

### Ubuntu/Debian

```bash
# 1. Update package list (Cập nhật danh sách gói)
sudo apt update

# 2. Search for nginx (Tìm kiếm nginx)
apt search nginx

# 3. Show info for curl (Xem thông tin gói curl)
apt show curl

# 4. List packages containing "python" (Liệt kê các gói có python)
dpkg -l | grep python

# 5. Check if git is installed (Kiểm tra git đã cài chưa)
dpkg -l | grep git
# Or (Hoặc)
which git && echo "Git is installed"
```

### RHEL/CentOS

```bash
# 1. Update (Cập nhật)
sudo yum update
# Or (Hoặc)
sudo dnf update

# 2. Search (Tìm kiếm)
yum search nginx

# 3. Information (Thông tin)
yum info curl

# 4. List (Liệt kê)
rpm -qa | grep python

# 5. Verify (Xác minh)
rpm -q git
```

---

## 🔐 Exercise 9: SSH & Remote Operations (Bài tập 9: SSH và Thao tác từ xa)

```bash
# 1. Generate SSH key (Tạo cặp khóa SSH)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. Copy public key to remote (Sao chép khóa tới server từ xa)
ssh-copy-id user@remote-server
# Or manual way (Hoặc làm thủ công)
# cat ~/.ssh/id_ed25519.pub | ssh user@remote-server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# 3. SSH and run remote command (SSH và chạy lệnh từ xa)
ssh user@remote-server "uptime"

# 4. Copy file local -> remote (Chép tệp local lên remote)
scp local-file.txt user@remote-server:/path/to/destination/

# 5. Copy directory remote -> local (Chép thư mục từ remote về local)
scp -r user@remote-server:/remote/path/ /local/path/

# 6. SSH config entry (Cấu hình SSH config để đăng nhập nhanh)
cat << 'EOF' >> ~/.ssh/config
Host myserver
    HostName 192.168.1.100
    User deploy
    IdentityFile ~/.ssh/id_ed25519
    Port 22
EOF

# Bonus: Simple deploy script (Script triển khai đơn giản)
#!/bin/bash
SERVER="user@remote-server"
APP_DIR="/opt/myapp"

ssh $SERVER << 'ENDSSH'
cd /opt/myapp
git pull origin main
sudo systemctl restart myapp
ENDSSH

echo "Deployment completed! (Triển khai hoàn tất!)"
```

---

## 🎯 Exercise 10: Comprehensive Challenge (Thử thách tổng hợp)

### server_setup.sh (Example Solution)

```bash
#!/bin/bash
#
# Server Setup Script
# Usage: sudo ./server_setup.sh [--dry-run] [-v]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Config
LOG_FILE="/var/log/setup.log"
DEPLOY_USER="deploy"
SSH_KEY="ssh-rsa AAAA... your-key-here"

# Flags
DRY_RUN=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Functions
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "$msg"
    echo "$msg" >> "$LOG_FILE"
}

run_cmd() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Would run: $*"
    else
        if [ "$VERBOSE" = true ]; then
            echo -e "${GREEN}[RUNNING]${NC} $*"
        fi
        "$@"
    fi
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}Error: This script must be run as root${NC}"
        exit 1
    fi
}

# Step 1: System Update
system_update() {
    log "Starting system update..."
    run_cmd apt update
    run_cmd apt upgrade -y
    log "System update completed"
}

# Step 2: User Setup
user_setup() {
    log "Setting up user $DEPLOY_USER..."
    
    if id "$DEPLOY_USER" &>/dev/null; then
        log "User $DEPLOY_USER already exists"
    else
        run_cmd useradd -m -s /bin/bash "$DEPLOY_USER"
        log "User $DEPLOY_USER created"
    fi
    
    run_cmd usermod -aG sudo "$DEPLOY_USER"
    
    # Setup SSH key
    local ssh_dir="/home/$DEPLOY_USER/.ssh"
    run_cmd mkdir -p "$ssh_dir"
    echo "$SSH_KEY" >> "$ssh_dir/authorized_keys"
    run_cmd chown -R "$DEPLOY_USER:$DEPLOY_USER" "$ssh_dir"
    run_cmd chmod 700 "$ssh_dir"
    run_cmd chmod 600 "$ssh_dir/authorized_keys"
    
    log "User setup completed"
}

# Step 3: Security (UFW)
security_setup() {
    log "Configuring firewall..."
    
    run_cmd apt install -y ufw
    run_cmd ufw default deny incoming
    run_cmd ufw default allow outgoing
    run_cmd ufw allow ssh
    run_cmd ufw allow http
    run_cmd ufw allow https
    run_cmd ufw --force enable
    
    log "Firewall configured"
}

# Step 4: Software Installation
install_software() {
    log "Installing software..."
    
    # Git
    run_cmd apt install -y git
    
    # Docker
    run_cmd apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    run_cmd apt update
    run_cmd apt install -y docker-ce
    run_cmd systemctl start docker
    run_cmd systemctl enable docker
    run_cmd usermod -aG docker "$DEPLOY_USER"
    
    # Nginx
    run_cmd apt install -y nginx
    run_cmd systemctl start nginx
    run_cmd systemctl enable nginx
    
    log "Software installation completed"
}

# Step 5: Directory Setup
directory_setup() {
    log "Setting up directories..."
    
    run_cmd mkdir -p /opt/apps
    run_cmd chown "$DEPLOY_USER:$DEPLOY_USER" /opt/apps
    
    run_cmd mkdir -p /var/log/apps
    run_cmd chmod 755 /var/log/apps
    
    log "Directory setup completed"
}

# Step 6: Verification
verify_setup() {
    log "Verifying setup..."
    
    echo ""
    echo "=========================================="
    echo "         SETUP VERIFICATION"
    echo "=========================================="
    
    # Check user
    if id "$DEPLOY_USER" &>/dev/null; then
        echo -e "[${GREEN}✓${NC}] User $DEPLOY_USER exists"
    else
        echo -e "[${RED}✗${NC}] User $DEPLOY_USER NOT found"
    fi
    
    # Check services
    for service in docker nginx; do
        if systemctl is-active --quiet "$service"; then
            echo -e "[${GREEN}✓${NC}] $service is running"
        else
            echo -e "[${RED}✗${NC}] $service is NOT running"
        fi
    done
    
    # Check UFW
    if ufw status | grep -q "active"; then
        echo -e "[${GREEN}✓${NC}] UFW is active"
    else
        echo -e "[${RED}✗${NC}] UFW is NOT active"
    fi
    
    # Check directories
    for dir in /opt/apps /var/log/apps; do
        if [ -d "$dir" ]; then
            echo -e "[${GREEN}✓${NC}] $dir exists"
        else
            echo -e "[${RED}✗${NC}] $dir NOT found"
        fi
    done
    
    echo "=========================================="
    echo ""
}

# Main
main() {
    check_root
    
    log "=========================================="
    log "Starting server setup..."
    log "=========================================="
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}Running in DRY-RUN mode${NC}"
    fi
    
    system_update
    user_setup
    security_setup
    install_software
    directory_setup
    verify_setup
    
    log "=========================================="
    log "Server setup completed successfully!"
    log "=========================================="
}

main
```

---

## 📝 Notes

- The above solutions are **one of many ways** to solve the problem (Các solutions trên là **một trong nhiều cách** để giải quyết vấn đề)
- Always possible to optimize or write differently (Luôn có thể optimize hoặc viết khác đi)
- Important to understand **logic** and **why** it works (Quan trọng là hiểu **logic** và **tại sao** nó hoạt động)

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
