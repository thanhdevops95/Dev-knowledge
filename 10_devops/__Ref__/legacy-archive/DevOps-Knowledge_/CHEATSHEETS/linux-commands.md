# Linux Commands Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Commonly used Linux commands for quick reference -- Các lệnh Linux thường dùng để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [File & Directory](#file--directory) -- File và Thư mục
- [File Permissions](#file-permissions) -- Quyền File
- [Process Management](#process-management) -- Quản lý Tiến trình
- [System Information](#system-information) -- Thông tin Hệ thống
- [Networking](#networking) -- Mạng
- [Package Management](#package-management) -- Quản lý Gói
- [User Management](#user-management) -- Quản lý Người dùng
- [Disk & Storage](#disk--storage) -- Đĩa và Lưu trữ
- [Search & Find](#search--find) -- Tìm kiếm
- [Text Processing](#text-processing) -- Xử lý Văn bản
- [Compression & Archives](#compression--archives) -- Nén và Lưu trữ
- [Keyboard Shortcuts](#keyboard-shortcuts) -- Phím tắt

## <a id="file--directory"></a> File & Directory -- File và Thư mục

```bash
# Navigation -- Điều hướng
pwd                          # Print working directory -- In thư mục hiện tại
cd /path/to/dir             # Change directory -- Chuyển thư mục
cd ~                        # Go to home -- Về thư mục home
cd -                        # Go to previous directory -- Về thư mục trước
ls                          # List files -- Liệt kê files
ls -l                       # List with details -- Liệt kê với chi tiết
ls -a                       # List all -- Liệt kê tất cả
ls -la                      # List all with details -- Liệt kê tất cả với chi tiết
ls -lh                      # List with human-readable sizes -- Liệt kê với kích thước dễ đọc

# Create -- Tạo
mkdir dirname               # Create directory -- Tạo thư mục
mkdir -p path/to/dir       # Create nested directories -- Tạo thư mục lồng nhau
touch filename             # Create empty file -- Tạo file rỗng

# Copy -- Sao chép
cp source dest             # Copy file -- Sao chép file
cp -r source dest          # Copy directory recursively -- Sao chép thư mục đệ quy
cp -p source dest          # Preserve attributes -- Giữ nguyên thuộc tính

# Move/Rename -- Di chuyển/Đổi tên
mv source dest             # Move or rename -- Di chuyển hoặc đổi tên
mv file1 file2 dir/        # Move multiple files -- Di chuyển nhiều files

# Delete -- Xóa
rm file                    # Remove file -- Xóa file
rm -r directory            # Remove directory recursively -- Xóa thư mục đệ quy
rm -rf directory           # Force remove (be careful!) -- Xóa cưỡng chế (cẩn thận!)
rmdir empty_dir            # Remove empty directory -- Xóa thư mục rỗng

# View -- Xem
cat file                   # Display file content -- Hiển thị nội dung file
less file                  # View file (paginated) -- Xem file (phân trang)
head file                  # First 10 lines -- 10 dòng đầu
head -n 20 file           # First 20 lines -- 20 dòng đầu
tail file                  # Last 10 lines -- 10 dòng cuối
tail -f file              # Follow file updates (logs) -- Theo dõi cập nhật file (logs)
tail -n 50 file           # Last 50 lines -- 50 dòng cuối
```

## <a id="file-permissions"></a> File Permissions -- Quyền File

```bash
# View permissions -- Xem quyền
ls -l file                 # View file permissions -- Xem quyền file
stat file                  # Detailed file info -- Thông tin file chi tiết

# Change permissions (numeric) -- Thay đổi quyền (số)
chmod 755 file             # rwxr-xr-x  ==> owner (read, write, execute), group (read, execute), others (read, execute) -- chủ sở hữu (đọc, ghi, thực thi), nhóm (đọc, thực thi), người khác (đọc, thực thi)
chmod 644 file             # rw-r--r--  ==> owner (read, write), group (read), others (read) -- chủ sở hữu (đọc, ghi), nhóm (đọc), người khác (đọc)
chmod 600 file             # rw-------  ==> owner (read, write), group (none), others (none) -- chủ sở hữu (đọc, ghi), nhóm (không có quyền), người khác (không có quyền)
chmod 751 file             # rwxr-x--x  ==> owner (read, write, execute), group (read, execute), others (execute) -- chủ sở hữu (đọc, ghi, thực thi), nhóm (đọc, thực thi), người khác (thực thi)
chmod 777 file             # rwxrwxrwx (avoid! -- tránh!) ==> all have full permissions -- tất cả có đầy đủ quyền

# Change permissions (symbolic) -- Thay đổi quyền (ký hiệu)
chmod u+x file             # Add execute for user -- Thêm quyền thực thi cho user
chmod g-w file             # Remove write for group -- Xóa quyền ghi cho group
chmod o+r file             # Add read for others -- Thêm quyền đọc cho others
chmod a+x file             # Add execute for all -- Thêm quyền thực thi cho tất cả

# Change ownership -- Thay đổi quyền sở hữu
chown user file            # Change owner -- Đổi chủ sở hữu
chown user:group file      # Change owner and group -- Đổi chủ sở hữu và group
chown -R user:group dir/   # Recursive -- Đệ quy

# Change group -- Thay đổi group
chgrp group file           # Change group only -- Chỉ đổi group
```

## <a id="process-management"></a> Process Management -- Quản lý Tiến trình

```bash
# View processes -- Xem tiến trình
ps                         # Current shell processes -- Tiến trình shell hiện tại
ps aux                     # All processes -- Tất cả tiến trình
ps aux | grep nginx        # Find specific process -- Tìm tiến trình cụ thể
top                        # Real-time process monitor -- Giám sát tiến trình real-time
htop                       # Better top (if installed) -- Top tốt hơn (nếu đã cài)

# Process control -- Điều khiển tiến trình
kill PID                   # Terminate process -- Kết thúc tiến trình
kill -9 PID               # Force kill -- Buộc kết thúc
killall process_name       # Kill by name -- Kết thúc theo tên
pkill pattern             # Kill by pattern -- Kết thúc theo pattern

# Background & Foreground -- Nền và Tiền cảnh
command &                  # Run in background -- Chạy nền
jobs                       # List background jobs -- Liệt kê jobs nền
fg %1                     # Bring job 1 to foreground -- Đưa job 1 lên tiền cảnh
bg %1                     # Continue job 1 in background -- Tiếp tục job 1 ở nền
Ctrl+Z                    # Suspend current process -- Tạm dừng tiến trình
Ctrl+C                    # Kill current process -- Kết thúc tiến trình

# Process priority -- Ưu tiên tiến trình
nice -n 10 command        # Start with priority 10 -- Bắt đầu với ưu tiên 10
renice -n 5 -p PID        # Change priority of running process -- Đổi ưu tiên tiến trình đang chạy
```

## <a id="system-information"></a> System Information -- Thông tin Hệ thống

```bash
# System -- Hệ thống
uname -a                   # System information -- Thông tin hệ thống
hostname                   # System hostname -- Tên máy chủ
uptime                     # System uptime -- Thời gian hoạt động
date                       # Current date/time -- Ngày/giờ hiện tại
cal                        # Calendar -- Lịch
whoami                     # Current user -- Người dùng hiện tại
w                          # Who is logged in -- Ai đang đăng nhập

# Hardware -- Phần cứng
lscpu                      # CPU information -- Thông tin CPU
free -h                    # Memory usage -- Sử dụng bộ nhớ
df -h                      # Disk usage -- Sử dụng đĩa
du -sh directory           # Directory size -- Kích thước thư mục
du -h --max-depth=1        # Size of subdirectories -- Kích thước thư mục con
lsblk                      # Block devices -- Thiết bị khối
lspci                      # PCI devices -- Thiết bị PCI
lsusb                      # USB devices -- Thiết bị USB

# OS Information -- Thông tin HĐH
cat /etc/os-release        # OS details -- Chi tiết HĐH
cat /proc/cpuinfo          # CPU details -- Chi tiết CPU
cat /proc/meminfo          # Memory details -- Chi tiết bộ nhớ
```

## <a id="networking"></a> Networking -- Mạng

```bash
# Network interfaces -- Giao diện mạng
ip addr                    # Show IP addresses -- Hiển thị địa chỉ IP
ip addr show eth0          # Show specific interface -- Hiển thị giao diện cụ thể
ifconfig                   # Network interfaces (older) -- Giao diện mạng (cũ)

# Connectivity -- Kết nối
ping google.com            # Test connectivity -- Kiểm tra kết nối
ping -c 4 8.8.8.8         # Ping 4 times -- Ping 4 lần
traceroute google.com      # Trace route -- Theo dõi đường đi
mtr google.com            # Better traceroute -- Traceroute tốt hơn

# DNS
nslookup google.com        # DNS lookup -- Tra cứu DNS
dig google.com            # Detailed DNS query -- Truy vấn DNS chi tiết
host google.com           # Simple DNS lookup -- Tra cứu DNS đơn giản

# Ports & Connections -- Cổng và Kết nối
netstat -tulpn            # Listening ports -- Cổng đang lắng nghe
ss -tulpn                 # Socket statistics (better) -- Thống kê socket (tốt hơn)
lsof -i :80               # What's using port 80 -- Cái gì đang dùng cổng 80
nc -zv host 22            # Test port connectivity -- Kiểm tra kết nối cổng

# Download -- Tải xuống
wget URL                   # Download file -- Tải file
wget -O filename URL       # Download with custom name -- Tải với tên tùy chỉnh
curl -O URL               # Download with curl -- Tải với curl
curl -L URL               # Follow redirects -- Theo dõi chuyển hướng
```

## <a id="package-management"></a> Package Management -- Quản lý Gói

### Debian/Ubuntu (APT)
```bash
# Update -- Cập nhật
apt update                 # Update package list -- Cập nhật danh sách gói
apt upgrade               # Upgrade packages -- Nâng cấp gói
apt full-upgrade          # Upgrade with dependencies -- Nâng cấp với dependencies

# Install/Remove -- Cài đặt/Gỡ bỏ
apt install package        # Install package -- Cài đặt gói
apt remove package         # Remove package -- Gỡ bỏ gói
apt purge package         # Remove with config -- Gỡ bỏ kèm cấu hình
apt autoremove            # Remove unused dependencies -- Gỡ bỏ dependencies không dùng

# Search -- Tìm kiếm
apt search keyword         # Search packages -- Tìm kiếm gói
apt show package          # Package details -- Chi tiết gói
apt list --installed      # List installed packages -- Liệt kê gói đã cài
```

### RHEL/CentOS (YUM/DNF)
```bash
# Update -- Cập nhật
yum update                # Update packages -- Cập nhật gói
dnf update                # DNF version -- Phiên bản DNF

# Install/Remove -- Cài đặt/Gỡ bỏ
yum install package       # Install -- Cài đặt
yum remove package        # Remove -- Gỡ bỏ

# Search -- Tìm kiếm
yum search keyword        # Search -- Tìm kiếm
yum info package         # Package info -- Thông tin gói
```

## <a id="user-management"></a> User Management -- Quản lý Người dùng

```bash
# Users -- Người dùng
useradd username          # Create user -- Tạo người dùng
useradd -m -s /bin/bash user  # Create with home & shell -- Tạo với home và shell
passwd username           # Set password -- Đặt mật khẩu
userdel username          # Delete user -- Xóa người dùng
userdel -r username       # Delete with home directory -- Xóa kèm thư mục home
usermod -aG group user    # Add user to group -- Thêm người dùng vào group

# Groups -- Nhóm
groupadd groupname        # Create group -- Tạo nhóm
groupdel groupname        # Delete group -- Xóa nhóm
groups username           # Show user's groups -- Hiển thị nhóm của người dùng
id username              # User ID and groups -- ID người dùng và nhóm

# Switch user -- Chuyển người dùng
su username              # Switch user -- Chuyển người dùng
su -                     # Switch to root -- Chuyển sang root
sudo command             # Run as root -- Chạy với quyền root
sudo -i                  # Root shell -- Shell root
```

## <a id="disk--storage"></a> Disk & Storage -- Đĩa và Lưu trữ

```bash
# Disk usage -- Sử dụng đĩa
df -h                     # Disk space -- Không gian đĩa
df -i                     # Inode usage -- Sử dụng inode
du -sh directory          # Directory size -- Kích thước thư mục
du -h --max-depth=1       # Subdirectory sizes -- Kích thước thư mục con
ncdu                      # Interactive disk usage -- Sử dụng đĩa tương tác

# Mount -- Gắn kết
mount                     # Show mounted filesystems -- Hiển thị hệ thống file đã gắn
mount /dev/sdb1 /mnt     # Mount device -- Gắn thiết bị
umount /mnt              # Unmount -- Tháo gắn
lsblk                    # List block devices -- Liệt kê thiết bị khối

# Disk operations -- Thao tác đĩa
fdisk -l                 # List disks -- Liệt kê đĩa
parted -l                # Partition info -- Thông tin phân vùng
mkfs.ext4 /dev/sdb1      # Format as ext4 -- Định dạng ext4
```

## <a id="search--find"></a> Search & Find -- Tìm kiếm

```bash
# Find files -- Tìm files
find /path -name "*.txt"           # Find by name -- Tìm theo tên
find /path -type f                 # Find files only -- Chỉ tìm files
find /path -type d                 # Find directories only -- Chỉ tìm thư mục
find /path -mtime -7               # Modified in last 7 days -- Sửa đổi trong 7 ngày qua
find /path -size +100M             # Larger than 100MB -- Lớn hơn 100MB
find /path -name "*.log" -delete   # Find and delete -- Tìm và xóa

# Locate (faster, uses database) -- Locate (nhanh hơn, dùng database)
locate filename                    # Find file -- Tìm file
updatedb                          # Update locate database -- Cập nhật database locate

# Which -- Lệnh nào
which command                     # Find command location -- Tìm vị trí lệnh
whereis command                   # Find binary, source, manual -- Tìm binary, source, manual
```

## <a id="text-processing"></a> Text Processing -- Xử lý Văn bản

```bash
# View/Edit -- Xem/Sửa
cat file                  # Display file -- Hiển thị file
tac file                  # Display reversed -- Hiển thị ngược
more file                 # Page through file -- Xem file theo trang
less file                 # Better pager -- Pager tốt hơn
head -n 20 file          # First 20 lines -- 20 dòng đầu
tail -n 20 file          # Last 20 lines -- 20 dòng cuối
tail -f file             # Follow file -- Theo dõi file

# Search -- Tìm kiếm
grep "pattern" file       # Search in file -- Tìm trong file
grep -r "pattern" dir/    # Recursive search -- Tìm đệ quy
grep -i "pattern" file    # Case-insensitive -- Không phân biệt hoa thường
grep -v "pattern" file    # Invert match -- Đảo ngược kết quả
grep -n "pattern" file    # Show line numbers -- Hiển thị số dòng

# Text manipulation -- Thao tác văn bản
sed 's/old/new/g' file    # Replace text -- Thay thế văn bản
awk '{print $1}' file     # Print first column -- In cột đầu tiên
cut -d: -f1 /etc/passwd   # Cut by delimiter -- Cắt theo delimiter
sort file                 # Sort lines -- Sắp xếp dòng
uniq file                 # Remove duplicates -- Xóa trùng lặp
wc -l file               # Count lines -- Đếm dòng
wc -w file               # Count words -- Đếm từ

# Compare -- So sánh
diff file1 file2          # Show differences -- Hiển thị khác biệt
comm file1 file2          # Compare sorted files -- So sánh files đã sắp xếp
```

## <a id="compression--archives"></a> Compression & Archives -- Nén và Lưu trữ

```bash
# tar
tar -czf archive.tar.gz dir/      # Create compressed archive -- Tạo archive nén
tar -xzf archive.tar.gz           # Extract -- Giải nén
tar -tzf archive.tar.gz           # List contents -- Liệt kê nội dung
tar -xzf archive.tar.gz -C /path  # Extract to path -- Giải nén đến đường dẫn

# gzip
gzip file                         # Compress file -- Nén file
gunzip file.gz                    # Decompress -- Giải nén
gzip -k file                      # Keep original -- Giữ file gốc

# zip
zip -r archive.zip dir/           # Create zip -- Tạo zip
unzip archive.zip                 # Extract -- Giải nén
unzip -l archive.zip              # List contents -- Liệt kê nội dung
```

## <a id="keyboard-shortcuts"></a> Keyboard Shortcuts -- Phím tắt

```bash
Ctrl+C          # Kill current process -- Kết thúc tiến trình hiện tại
Ctrl+Z          # Suspend current process -- Tạm dừng tiến trình hiện tại
Ctrl+D          # Exit shell / EOF -- Thoát shell / EOF
Ctrl+L          # Clear screen -- Xóa màn hình
Ctrl+A          # Go to line start -- Đến đầu dòng
Ctrl+E          # Go to line end -- Đến cuối dòng
Ctrl+U          # Delete to line start -- Xóa đến đầu dòng
Ctrl+K          # Delete to line end -- Xóa đến cuối dòng
Ctrl+R          # Search command history -- Tìm kiếm lịch sử lệnh
!!              # Repeat last command -- Lặp lại lệnh cuối
!$              # Last argument of previous command -- Tham số cuối của lệnh trước
```

---
