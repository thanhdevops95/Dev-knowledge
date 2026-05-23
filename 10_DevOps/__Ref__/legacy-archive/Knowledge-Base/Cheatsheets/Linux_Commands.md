# Linux Commands Cheatsheet -- Bảng Tra Cứu Lệnh Linux

> A comprehensive guide to Linux commands for DevOps Engineers. -- Hướng dẫn đầy đủ về các lệnh Linux dành cho kỹ sư DevOps.

## Table of Contents -- Mục Lục

1. [File & Directory Operations -- Thao Tác File & Thư Mục](#1-file--directory-operations----thao-tác-file--thư-mục)
2. [File Permissions -- Quyền Truy Cập File](#2-file-permissions----quyền-truy-cập-file)
3. [Process Management -- Quản Lý Tiến Trình](#3-process-management----quản-lý-tiến-trình)
4. [System Information -- Thông Tin Hệ Thống](#4-system-information----thông-tin-hệ-thống)
5. [Networking -- Mạng](#5-networking----mạng)
6. [Package Management -- Quản Lý Gói Phần Mềm](#6-package-management----quản-lý-gói-phần-mềm)
7. [User Management -- Quản Lý Người Dùng](#7-user-management----quản-lý-người-dùng)
8. [Disk & Storage -- Ổ Đĩa & Lưu Trữ](#8-disk--storage----ổ-đĩa--lưu-trữ)
9. [Search & Find -- Tìm Kiếm](#9-search--find----tìm-kiếm)
10. [Text Processing -- Xử Lý Văn Bản](#10-text-processing----xử-lý-văn-bản)
11. [Compression & Archives -- Nén & Giải Nén](#11-compression--archives----nén--giải-nén)

---

## 1. File & Directory Operations -- Thao Tác File & Thư Mục

Essential commands for navigating the filesystem and managing files/directories. -- Các lệnh cơ bản để điều hướng hệ thống tệp và quản lý tập tin/thư mục.

```bash
# Navigation -- Điều hướng
pwd                          # Print working directory -- In ra đường dẫn thư mục hiện tại
cd /path/to/dir              # Change directory -- Chuyển đến thư mục chỉ định
cd ~                         # Go to home directory -- Về thư mục gốc của user
cd -                         # Go to previous directory -- Quay lại thư mục trước đó
ls                           # List files -- Liệt kê danh sách file
ls -la                       # List all files including hidden ones with details -- Liệt kê tất cả file gồm cả file ẩn và chi tiết
ls -lh                       # List with human-readable sizes (e.g., 1K, 234M, 2G) -- Liệt kê với kích thước dễ đọc

# Creation -- Tạo mới
mkdir dirname                # Make directory -- Tạo thư mục mới
mkdir -p a/b/c               # Create nested directories -- Tạo thư mục lồng nhau
touch filename               # Create an empty file or update timestamp -- Tạo file rỗng hoặc cập nhật thời gian

# Manipulation -- Thao tác
cp source dest               # Copy file -- Sao chép file
cp -r source_dir dest_dir    # Copy directory recursively -- Sao chép thư mục đệ quy
mv old_path new_path         # Move or Rename file/directory -- Di chuyển hoặc đổi tên
rm file                      # Remove file -- Xóa file
rm -r dir                    # Remove directory recursively -- Xóa thư mục và nội dung bên trong
rm -rf dir                   # Force remove directory (Caution!) -- Xóa cưỡng chế thư mục (Cẩn thận!)

# Viewing Content -- Xem nội dung
cat file                     # Display file content -- Hiển thị toàn bộ nội dung file
less file                    # View file page-by-page -- Xem file từng trang (hữu ích cho file lớn)
head -n 10 file              # Show first 10 lines -- Xem 10 dòng đầu tiên
tail -n 10 file              # Show last 10 lines -- Xem 10 dòng cuối cùng
tail -f file.log             # Follow file output continuously -- Theo dõi log liên tục theo thời gian thực
```

---

## 2. File Permissions -- Quyền Truy Cập File

Understanding and modifying file permissions is crucial for security. Linux uses a user-group-others model. -- Hiểu và điều chỉnh quyền truy cập file là rất quan trọng để bảo mật. Linux sử dụng mô hình user-group-others.

| Permission -- Quyền | Code -- Mã | Description -- Mô tả |
|---------------------|------------|------------------------|
| Read (r)            | 4          | View content -- Xem nội dung |
| Write (w)           | 2          | Edit content -- Sửa nội dung |
| Execute (x)         | 1          | Run file -- Chạy file |

```bash
# Viewing Permissions -- Xem quyền
ls -l filename               # View permissions (e.g., -rwxr-xr--) -- Xem chi tiết quyền
stat filename                # Detailed file status -- Xem trạng thái chi tiết của file

# Changing Permissions (Numeric) -- Thay đổi quyền (Dạng số)
chmod 755 file               # rwxr-xr-x: User(RWX), Group(RX), Others(RX) -- Chuẩn cho scripts
chmod 644 file               # rw-r--r--: User(RW), Group(R), Others(R) -- Chuẩn cho tài liệu
chmod 600 file               # rw-------: User(RW) only -- Chuẩn cho private keys (SSH)
chmod 777 file               # rwxrwxrwx: All permissions for everyone (DANGEROUS) -- Quyền đầy đủ cho tất cả (NGUY HIỂM)

# Changing Permissions (Symbolic) -- Thay đổi quyền (Dạng ký hiệu)
chmod +x script.sh           # Add execute permission for all -- Thêm quyền thực thi cho tất cả
chmod u+x script.sh          # Add execute permission for User only -- Thêm quyền thực thi cho chủ sở hữu
chmod g-w file               # Remove write permission from Group -- Gỡ bỏ quyền ghi của nhóm

# Ownership -- Quyền sở hữu
chown user:group file        # Change owner and group -- Đổi người sở hữu và nhóm sở hữu
chown -R user:group dir      # Change recursively for directory -- Đổi đệ quy cho cả thư mục
chgrp group_name file        # Change group only -- Chỉ đổi nhóm
```

---

## 3. Process Management -- Quản Lý Tiến Trình

Monitor and control running applications using process identifiers (PIDs). -- Giám sát và điều khiển các ứng dụng đang chạy thông qua ID tiến trình (PID).

```bash
# Monitoring -- Giám sát
ps aux                       # List all running processes -- Liệt kê tất cả tiến trình đang chạy
ps aux | grep nginx          # Find specific process -- Tìm tiến trình cụ thể (ví dụ: nginx)
top                          # Real-time process monitoring -- Xem tiến trình theo thời gian thực
htop                         # Interactive process viewer -- Giao diện trực quan hơn top (cần cài đặt)

# Control -- Điều khiển
kill PID                     # Terminate process by ID -- Kết thúc tiến trình theo ID
kill -9 PID                  # Force kill process -- Buộc dừng tiến trình (dùng khi bị treo)
killall process_name         # Kill all processes by name -- Kết thúc tất cả tiến trình có tên này
pkill -f pattern             # Kill process based on command line pattern -- Kết thúc dựa trên tên mẫu

# Background Jobs -- Tác vụ nền
command &                    # Run command in background -- Chạy lệnh dưới nền
jobs                         # List background jobs -- Liệt kê các tác vụ nền
fg %1                        # Bring job 1 to foreground -- Đưa tác vụ 1 ra chạy trực tiếp
bg %1                        # Resume job 1 in background -- Tiếp tục chạy tác vụ 1 dưới nền
```

---

## 4. System Information -- Thông Tin Hệ Thống

Gather details about the hardware and operating system. -- Thu thập thông tin chi tiết về phần cứng và hệ điều hành.

```bash
# OS & Kernel -- Hệ điều hành & Kernel
uname -a                     # Check kernel version -- Kiểm tra phiên bản kernel
cat /etc/os-release          # Check OS distribution details -- Xem thông tin phiên bản OS
uptime                       # System runtime & load average -- Thời gian chạy & tải hệ thống

# Hardware -- Phần cứng
lscpu                        # CPU information -- Thông tin CPU
free -h                      # Memory (RAM) usage -- Kiểm tra dung lượng RAM
lsblk                        # List block devices -- Liệt kê ổ cứng/phân vùng
lsusb                        # List USB devices -- Liệt kê thiết bị USB
lspci                        # List PCI devices -- Liệt kê thiết bị PCI
df -h                        # Disk space usage -- Kiểm tra dung lượng ổ đĩa
du -sh directory             # Check size of specific directory -- Kiểm tra dung lượng thư mục
```

---

## 5. Networking -- Mạng

Troubleshoot network connectivity and manage interfaces. -- Khắc phục sự cố kết nối mạng và quản lý các giao diện mạng.

```bash
# Basics -- Cơ bản
ip addr                      # Show IP addresses -- Hiển thị địa chỉ IP
ifconfig                     # Old command for IP -- Lệnh cũ xem IP (có thể cần cài net-tools)
ping -c 4 google.com         # Check connectivity -- Kiểm tra kết nối đến máy chủ

# Diagnostics -- Chẩn đoán
traceroute google.com        # Trace path to destination -- Theo dõi đường đi gói tin
mtr google.com               # Real-time network diagnostic -- Kết hợp ping & traceroute
nslookup google.com          # DNS Lookup -- Tra cứu DNS
dig google.com               # Detailed DNS Lookup -- Tra cứu DNS chi tiết hơn

# Connections & Ports -- Kết nối & Cổng
netstat -tulpn               # List listening ports -- Liệt kê các cổng đang mở
ss -tulpn                    # Modern alternative to netstat -- Thay thế hiện đại cho netstat
lsof -i :80                  # Check what process is using port 80 -- Xem tiến trình nào đang chiếm cổng 80
nc -zv 127.0.0.1 22          # Test TCP connection to specific port -- Test kết nối đến cổng cụ thể

# Downloads -- Tải dữ liệu
curl -O URL                  # Download file -- Tải file về máy
wget URL                     # Download file -- Tải file (mạnh hơn curl cho việc tải file)
```

---

## 6. Package Management -- Quản Lý Gói Phần Mềm

Managing software varies by distribution. Here are the two most common. -- Quản lý phần mềm khác nhau tùy bản phân phối. Dưới đây là 2 loại phổ biến nhất.

### Debian/Ubuntu (APT)
```bash
apt update                   # Update package list -- Cập nhật danh sách gói
apt upgrade                  # Upgrade installed packages -- Nâng cấp các gói đã cài
apt install package_name     # Install a package -- Cài đặt gói mới
apt remove package_name      # Remove a package -- Gỡ bỏ gói
apt search keyword           # Search for a package -- Tìm kiếm gói
```

### RHEL/CentOS/Fedora (YUM/DNF)
```bash
yum update                   # Update packages -- Cập nhật và nâng cấp
yum install package_name     # Install package -- Cài đặt
yum remove package_name      # Remove package -- Gỡ bỏ
# dnf uses the same commands as yum -- dnf dùng lệnh tương tự yum
```

---

## 7. User Management -- Quản Lý Người Dùng

Create and manage user accounts and groups. -- Tạo và quản lý tài khoản người dùng và nhóm.

```bash
useradd -m username          # Create user with home directory -- Tạo user kèm thư mục home
passwd username              # Set/Change password -- Đặt/Đổi mật khẩu
usermod -aG group user       # Add user to a group -- Thêm user vào nhóm
userdel -r username          # Delete user and home directory -- Xóa user và dữ liệu của họ
su - username                # Switch to another user -- Chuyển sang tài khoản khác
sudo command                 # Run command as root -- Chạy lệnh với quyền quản trị
id username                  # Show user ID and groups -- Xem ID và nhóm của user
```

---

## 8. Disk & Storage -- Ổ Đĩa & Lưu Trữ

Managing disk usage and filesystems. -- Quản lý dung lượng đĩa và hệ thống tệp.

```bash
df -h                        # View disk space utilization -- Xem dung lượng ổ đĩa
du -sh /var/log              # View size of a directory -- Xem kích thước thư mục /var/log
fdisk -l                     # List partitions -- Liệt kê phân vùng
mount /dev/sdb1 /mnt         # Mount a filesystem -- Gắn phân vùng vào hệ thống
umount /mnt                  # Unmount -- Gỡ phân vùng
```

---

## 9. Search & Find -- Tìm Kiếm

Powerful tools to find files and patterns inside files. -- Công cụ mạnh mẽ để tìm file và tìm nội dung trong file.

```bash
# Finding Files -- Tìm File
find /path -name "*.log"     # Find files by name -- Tìm file theo tên
find /path -type f -size +100M # Find files larger than 100MB -- Tìm file lớn hơn 100MB
find /path -mtime -7         # Find files modified in last 7 days -- Tìm file sửa trong 7 ngày qua

# Finding Content (Grep) -- Tìm Nội Dung
grep "error" file.log        # Search for string in file -- Tìm chuỗi trong file
grep -r "config" /etc/       # Recursive search in directory -- Tìm đệ quy trong thư mục
grep -i "error" file.log     # Case insensitive search -- Tìm không phân biệt hoa thường
grep -v "ok" file.log        # Invert match (Show lines NOT containing "ok") -- Hiện dòng KHÔNG chứa "ok"
```

---

## 10. Text Processing -- Xử Lý Văn Bản

Manipulate output and text streams. -- Thao tác trên luồng dữ liệu văn bản.

```bash
sort file.txt                # Sort lines alphabetically -- Sắp xếp dòng theo alphabet
uniq file.txt                # Remove consecutive duplicates -- Xóa dòng trùng lặp liên tiếp
wc -l file.txt               # Count lines -- Đếm số dòng
cut -d: -f1 /etc/passwd      # Extract first column (delimiter :) -- Cắt lấy cột đầu tiên
sed 's/foo/bar/g' file.txt   # Replace 'foo' with 'bar' -- Thay thế 'foo' bằng 'bar'
awk '{print $1}' file.txt    # Print first column (advanced processing) -- In cột đầu tiên (xử lý nâng cao)
```

---

## 11. Compression & Archives -- Nén & Giải Nén

Compress files to save space or bundle them for transfer. -- Nén file để tiết kiệm dung lượng hoặc đóng gói để chuyển dữ liệu.

```bash
# Tar (Tape Archive)
tar -czf archive.tar.gz dir  # Create compressed archive -- Tạo file nén .tar.gz
tar -xzf archive.tar.gz      # Extract archive -- Giải nén file .tar.gz
tar -tvf archive.tar.gz      # List content of archive -- Xem nội dung file nén

# Gzip
gzip file.txt                # Compression file -- Nén file thành file.txt.gz
gunzip file.txt.gz           # Decompress file -- Giải nén file

# Zip
zip -r archive.zip dir       # Create zip file -- Tạo file zip
unzip archive.zip            # Extract zip file -- Giải nén zip
```

---

## 12. Useful Aliases -- Alias Hữu Ích

Shorten long commands to save time. Add these to your `~/.bashrc` or `~/.zshrc`. -- Rút gọn các lệnh dài để tiết kiệm thời gian. Thêm vào file `~/.bashrc` hoặc `~/.zshrc` của bạn.

```bash
alias ll='ls -lah'           # List all files detailed -- Liệt kê chi tiết tất cả file
alias ..='cd ..'             # Go back one directory -- Quay lại 1 thư mục
alias ...='cd ../..'         # Go back two directories -- Quay lại 2 thư mục
alias update='sudo apt update && sudo apt upgrade -y'  # Update system -- Cập nhật hệ thống
alias ports='netstat -tulpn' # Show open ports -- Xem các cổng đang mở
alias myip='curl ifconfig.me' # Show public IP -- Xem IP công khai
```
