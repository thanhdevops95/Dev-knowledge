# ✅ Solutions: Linux & Bash

> Đáp án cho Exercises và Project. **Hãy thử tự làm trước khi xem!**

---

## 🗂️ Exercise 1: File System Navigation

```bash
# 1. Tạo cấu trúc thư mục
mkdir -p ~/devops-practice/{projects/{web-app/{src,tests,docs},api-server/{src,tests}},scripts,logs}

# 2. Tạo README.md trong mỗi src/
touch ~/devops-practice/projects/web-app/src/README.md
touch ~/devops-practice/projects/api-server/src/README.md

# 3. Tạo 5 log files
touch ~/devops-practice/logs/app-0{1,2,3,4,5}.log
# hoặc
for i in {1..5}; do touch ~/devops-practice/logs/app-0$i.log; done

# 4. Di chuyển logs vào archive
mkdir ~/devops-practice/logs/archive
mv ~/devops-practice/logs/*.log ~/devops-practice/logs/archive/

# 5. Xóa thư mục trống
rmdir ~/devops-practice/projects/api-server/tests/
```

---

## 🔐 Exercise 2: Permissions Management

```bash
# 1-3. Tạo files
echo "This is confidential" > secret.txt
echo "This is public" > public.txt
cat << 'EOF' > deploy.sh
#!/bin/bash
echo "Deploying application..."
EOF

# 4. Thiết lập permissions
chmod 400 secret.txt    # -r--------
chmod 644 public.txt    # -rw-r--r--
chmod 711 deploy.sh     # -rwx--x--x

# 5. Tạo group và thêm user
sudo groupadd devteam
sudo usermod -aG devteam $USER

# 6. Thay đổi group owner
sudo chgrp devteam deploy.sh
```

---

## 🔍 Exercise 3: Text Processing

```bash
# Setup file đã có trong đề

# 1. Đếm số dòng ERROR
grep -c "ERROR" server.log
# Output: 3

# 2. Liệt kê unique users đã login
grep "User login" server.log | awk '{print $NF}' | sort | uniq
# Output: 
# admin
# john

# 3. Hiển thị timestamp và message của WARNING
grep "WARNING" server.log | awk '{print $1, $2, $4, $5, $6, $7}'
# Hoặc đơn giản hơn:
grep "WARNING" server.log

# 4. Tìm dòng cuối cùng chứa "admin"
grep "admin" server.log | tail -1
# Output: 2024-01-15 08:30:00 INFO User login: admin

# 5. Thay thế INFO thành [INFO]
sed 's/INFO/[INFO]/g' server.log > server_new.log

# 6. Hiển thị 5 dòng đầu tiên
head -5 server.log

# 7. Đếm số lần "connection" xuất hiện (case-insensitive)
grep -i -c "connection" server.log
# Output: 3
# Hoặc đếm tất cả occurrences:
grep -io "connection" server.log | wc -l
```

---

## 📊 Exercise 4: Process Management

```bash
# 1. Top 5 processes by CPU
ps aux --sort=-%cpu | head -6

# 2. Top 5 processes by RAM
ps aux --sort=-%mem | head -6

# 3. Processes của user hiện tại
ps -u $USER

# 4. Chạy sleep trong background
sleep 300 &

# 5. Tìm PID của sleep
pgrep sleep
# hoặc
ps aux | grep sleep

# 6. Kill process
kill $(pgrep sleep)
# hoặc với PID cụ thể
kill 12345

# Bonus: Kill tất cả processes tên chứa "sleep"
pkill sleep
# hoặc
killall sleep
```

---

## 🔧 Exercise 5: Bash Scripting Basics

### Task 1: sysinfo.sh

```bash
#!/bin/bash
# System Information Script

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

### Task 2: greet.sh

```bash
#!/bin/bash
# Greeting Script

echo -n "Enter your name: "
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

### Task 3: counter.sh

```bash
#!/bin/bash
# File Counter Script

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

dir="$1"

if [ ! -d "$dir" ]; then
    echo "Error: $dir is not a directory"
    exit 1
fi

files=$(find "$dir" -maxdepth 1 -type f ! -name ".*" | wc -l)
dirs=$(find "$dir" -maxdepth 1 -type d ! -name ".*" ! -path "$dir" | wc -l)
hidden=$(ls -la "$dir" | grep "^\." | wc -l)

echo "Contents of: $dir"
echo "Files       : $files"
echo "Directories : $dirs"
echo "Hidden items: $hidden"
```

---

## 🔄 Exercise 6: Loops and Conditions

### Task 1: backup.sh

```bash
#!/bin/bash
# Backup Script

source_dir="$1"
backup_base="$2"

# Validate arguments
if [ -z "$source_dir" ] || [ -z "$backup_base" ]; then
    echo "Usage: $0 <source_dir> <backup_dir>"
    exit 1
fi

# Check source exists
if [ ! -d "$source_dir" ]; then
    echo "Error: Source directory does not exist"
    exit 1
fi

# Create backup directory with timestamp
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="${backup_base}/backup_${timestamp}"
mkdir -p "$backup_dir"

# Copy files
count=0
for file in "$source_dir"/*; do
    if [ -f "$file" ]; then
        cp "$file" "$backup_dir/"
        ((count++))
    fi
done

echo "Backup completed!"
echo "Location: $backup_dir"
echo "Files copied: $count"
```

### Task 2: rotate.sh

```bash
#!/bin/bash
# Log Rotation Script

log_dir="$1"

if [ -z "$log_dir" ] || [ ! -d "$log_dir" ]; then
    echo "Usage: $0 <log_directory>"
    exit 1
fi

compressed=0
deleted=0

# Compress large log files
for file in "$log_dir"/*.log; do
    [ -f "$file" ] || continue
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file")
    
    if [ $size -gt 1048576 ]; then  # > 1MB
        gzip "$file"
        echo "Compressed: $file"
        ((compressed++))
    fi
done

# Delete old compressed files
find "$log_dir" -name "*.gz" -mtime +7 -delete -print | while read file; do
    echo "Deleted: $file"
    ((deleted++))
done

echo ""
echo "Summary:"
echo "  Compressed: $compressed files"
echo "  Deleted: $deleted files"
```

### Task 3: check_services.sh

```bash
#!/bin/bash
# Service Checker Script

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
    echo "Warning: $failed service(s) not running"
    exit 1
else
    echo "All services running"
    exit 0
fi
```

---

## 🌐 Exercise 7: Networking Commands

```bash
# 1. IP addresses của tất cả interfaces
ip addr show | grep "inet " | awk '{print $2}'
# hoặc
hostname -I

# 2. Kiểm tra port 80 đang listen
ss -tuln | grep :80
# hoặc
netstat -tuln | grep :80

# 3. Kiểm tra connectivity đến google.com
ping -c 3 google.com

# 4. Trace route đến 8.8.8.8
traceroute 8.8.8.8
# hoặc (Ubuntu)
tracepath 8.8.8.8

# 5. Connections đang ESTABLISHED
ss -t state established
# hoặc
netstat -tn | grep ESTABLISHED

# 6. Process sử dụng port 22
sudo ss -tulnp | grep :22
# hoặc
sudo lsof -i :22

# Bonus: Connectivity checker script
#!/bin/bash
hosts=("google.com" "github.com" "8.8.8.8")

for host in "${hosts[@]}"; do
    if ping -c 1 -W 2 "$host" &>/dev/null; then
        echo "[OK] $host is reachable"
    else
        echo "[FAIL] $host is not reachable"
    fi
done
```

---

## 📦 Exercise 8: Package Management

### Ubuntu/Debian

```bash
# 1. Update package list
sudo apt update

# 2. Tìm kiếm nginx
apt search nginx

# 3. Thông tin về curl
apt show curl

# 4. Liệt kê packages có "python"
dpkg -l | grep python

# 5. Kiểm tra git đã cài chưa
dpkg -l | grep git
# hoặc
which git && echo "Git is installed"
```

### RHEL/CentOS

```bash
# 1. Update
sudo yum update
# hoặc
sudo dnf update

# 2. Tìm kiếm
yum search nginx

# 3. Thông tin
yum info curl

# 4. Liệt kê
rpm -qa | grep python

# 5. Kiểm tra
rpm -q git
```

---

## 🔐 Exercise 9: SSH & Remote Operations

```bash
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. Copy public key
ssh-copy-id user@remote-server
# hoặc thủ công
cat ~/.ssh/id_ed25519.pub | ssh user@remote-server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# 3. SSH và chạy command
ssh user@remote-server "uptime"

# 4. Copy file local -> remote
scp local-file.txt user@remote-server:/path/to/destination/

# 5. Copy thư mục remote -> local
scp -r user@remote-server:/remote/path/ /local/path/

# 6. SSH config entry
cat << 'EOF' >> ~/.ssh/config
Host myserver
    HostName 192.168.1.100
    User deploy
    IdentityFile ~/.ssh/id_ed25519
    Port 22
EOF

# Bonus: Simple deploy script
#!/bin/bash
SERVER="user@remote-server"
APP_DIR="/opt/myapp"

ssh $SERVER << 'ENDSSH'
cd /opt/myapp
git pull origin main
sudo systemctl restart myapp
ENDSSH

echo "Deployment completed!"
```

---

## 🎯 Exercise 10: Comprehensive Challenge

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

- Các solutions trên là **một trong nhiều cách** để giải quyết vấn đề
- Luôn có thể optimize hoặc viết khác đi
- Quan trọng là hiểu **logic** và **tại sao** nó hoạt động

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
