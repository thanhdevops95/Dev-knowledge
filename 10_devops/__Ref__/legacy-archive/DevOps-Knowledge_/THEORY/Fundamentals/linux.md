# Linux Fundamentals

> Kiến thức nền tảng về hệ điều hành Linux

## 📋 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Kiến trúc Linux](#kiến-trúc-linux)
- [File System](#file-system)
- [Quản lý Process](#quản-lý-process)
- [User & Permission](#user--permission)
- [Networking](#networking)
- [Package Management](#package-management)
- [Shell & Scripting](#shell--scripting)
- [Best Practices](#best-practices)

## Giới thiệu

### Linux là gì?

Linux là một hệ điều hành mã nguồn mở (open-source operating system) dựa trên Unix, được phát triển bởi Linus Torvalds năm 1991.

**Đặc điểm chính:**
- **Open Source**: Mã nguồn mở, miễn phí
- **Stable**: Ổn định, hiếm khi crash
- **Secure**: Bảo mật cao
- **Multi-user**: Hỗ trợ nhiều người dùng
- **Multi-tasking**: Đa nhiệm

### Tại sao DevOps cần Linux?

1. **Servers chạy Linux**: 90% servers production chạy Linux
2. **Container & Cloud**: Docker, Kubernetes đều dựa trên Linux
3. **Automation**: Shell scripting mạnh mẽ
4. **Cost-effective**: Miễn phí, tiết kiệm chi phí

## Kiến trúc Linux

### Các thành phần chính

```
┌─────────────────────────────────────┐
│      Applications & Programs        │
├─────────────────────────────────────┤
│         System Libraries            │
├─────────────────────────────────────┤
│            Shell                    │
├─────────────────────────────────────┤
│            Kernel                   │
├─────────────────────────────────────┤
│           Hardware                  │
└─────────────────────────────────────┘
```

**1. Kernel (Nhân)**
- Core của hệ điều hành
- Quản lý hardware resources
- Process management, memory management

**2. Shell**
- Giao diện giữa user và kernel
- Bash, Zsh, Fish

**3. System Libraries**
- Các thư viện hệ thống
- glibc, systemd

**4. Applications**
- Các ứng dụng người dùng

## File System

### Cấu trúc thư mục

```
/                   # Root directory
├── bin/           # Essential binaries
├── boot/          # Boot loader files
├── dev/           # Device files
├── etc/           # Configuration files
├── home/          # User home directories
├── lib/           # System libraries
├── opt/           # Optional software
├── root/          # Root user home
├── tmp/           # Temporary files
├── usr/           # User programs
└── var/           # Variable data (logs)
```

### File Types

- **Regular file** (`-`): File thông thường
- **Directory** (`d`): Thư mục
- **Link** (`l`): Symbolic link
- **Character device** (`c`): Character device file
- **Block device** (`b`): Block device file

### File Permissions

```bash
-rwxr-xr--

- rwx r-x r--
│ │││ │││ │││ 
│ │││ │││ └┴┴─ Others (r--)
│ │││ └┴┴──── Group (r-x)
│ └┴┴───── Owner (rwx)
└──────── File type (-)

# Ý nghĩa của "-rwxr-xr--" là tệp tin này cho phép chủ sở hữu có toàn quyền (đọc, ghi, thực thi), thành viên trong nhóm được phép đọc và thực thi (nhưng không được ghi), còn người khác chỉ được phép đọc nội dung.
```

**Permission values:**
- `r` (read) = 4
- `w` (write) = 2
- `x` (execute) = 1
ß
## Quản lý Process

### Process là gì?

Process là một chương trình đang chạy trong hệ thống.

### Các lệnh quản lý process

```bash
# Xem processes
ps aux
top
htop

# Kill process
kill <PID>
kill -9 <PID>  # Force kill
killall <process_name>

# Background & Foreground
command &      # Chạy background
fg            # Đưa lên foreground
bg            # Tiếp tục chạy background
```

### Process States

- **Running (R)**: Đang chạy
- **Sleeping (S)**: Đang chờ
- **Stopped (T)**: Đã dừng
- **Zombie (Z)**: Process đã kết thúc nhưng chưa được clean up

## User & Permission

### User Management

```bash
# Tạo user
useradd username
useradd -m -s /bin/bash username

# Đổi password
passwd username

# Xóa user
userdel username
userdel -r username  # Xóa cả home directory

# Thêm user vào group
usermod -aG groupname username
```

### Permission Management

```bash
# Thay đổi permission
chmod 755 file.txt
chmod u+x file.sh
chmod g-w file.txt

# Thay đổi owner
chown user:group file.txt
chown -R user:group directory/

# Thay đổi group
chgrp group file.txt
```

## Networking

### Network Commands

```bash
# Xem IP address
ip addr
ifconfig

# Test connectivity
ping google.com
ping -c 4 8.8.8.8

# DNS lookup
nslookup google.com
dig google.com

# Port scanning
netstat -tulpn
ss -tulpn

# Download files
wget https://example.com/file.zip
curl -O https://example.com/file.zip
```

### Network Configuration

```bash
# Xem routing table
ip route
route -n

# Xem DNS servers
cat /etc/resolv.conf

# Xem hostname
hostname
hostnamectl
```

## Package Management

### Debian/Ubuntu (APT)

```bash
# Update package list
apt update

# Upgrade packages
apt upgrade

# Install package
apt install package_name

# Remove package
apt remove package_name
apt purge package_name  # Remove with config

# Search package
apt search keyword
```

### RHEL/CentOS (YUM/DNF)

```bash
# Install package
yum install package_name
dnf install package_name

# Update packages
yum update
dnf update

# Remove package
yum remove package_name
```

## Shell & Scripting

### Basic Shell Commands

```bash
# Navigation
cd /path/to/directory
pwd
ls -la

# File operations
cp source dest
mv source dest
rm file
mkdir directory
touch file

# Text processing
cat file.txt
less file.txt
head -n 10 file.txt
tail -f /var/log/syslog
grep "pattern" file.txt
```

### Basic Bash Script

```bash
#!/bin/bash

# Variables
NAME="DevOps"
echo "Hello, $NAME"

# Conditionals
if [ -f "/etc/passwd" ]; then
    echo "File exists"
fi

# Loops
for i in {1..5}; do
    echo "Number: $i"
done

# Functions
function greet() {
    echo "Hello, $1"
}

greet "World"
```

## Best Practices

### 1. Security

- ✅ Luôn update hệ thống
- ✅ Sử dụng SSH keys thay vì password
- ✅ Disable root login qua SSH
- ✅ Sử dụng firewall (ufw, firewalld)
- ✅ Principle of least privilege

### 2. System Management

- ✅ Regular backups
- ✅ Monitor system resources
- ✅ Log rotation
- ✅ Document changes

### 3. Performance

- ✅ Optimize boot time
- ✅ Clean up unused packages
- ✅ Monitor disk space
- ✅ Use appropriate file systems

## Tài liệu tham khảo

- [Linux Documentation Project](https://tldp.org/)
- [Arch Linux Wiki](https://wiki.archlinux.org/)
- [Ubuntu Documentation](https://help.ubuntu.com/)

---

