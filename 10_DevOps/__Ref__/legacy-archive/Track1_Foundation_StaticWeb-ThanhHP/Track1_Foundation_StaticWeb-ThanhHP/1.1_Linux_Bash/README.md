# 🐧 Module 1.1: Linux & Bash

[![Duration](https://img.shields.io/badge/Duration-10--15%20hours-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Beginner-green?style=flat-square)](.)

> **Linux Fundamentals & Bash Scripting** - Foundation for every DevOps Engineer.
>
> *Nền tảng Linux & Bash Scripting - Nền tảng cho mọi DevOps Engineer.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand what Linux is and why DevOps engineers need it (Hiểu Linux là gì và tại sao cần)
- ✅ Navigate the file system proficiently (Điều hướng file system thành thạo)
- ✅ Manipulate files and directories (Thao tác files và thư mục)
- ✅ Manage users, permissions, processes (Quản lý users, permissions, processes)
- ✅ Write basic Bash scripts (Viết Bash script cơ bản)
- ✅ Use package managers - apt/yum (Sử dụng package manager)

---

## 📖 Content (Nội dung)

### 1. What is Linux? (Linux là gì?) - 30 min

#### 1.1 Introduction (Giới thiệu)

**Linux** is an open-source operating system, developed by Linus Torvalds in 1991. Unlike Windows or macOS, Linux is completely free and customizable.

*Linux là hệ điều hành mã nguồn mở, được phát triển bởi Linus Torvalds năm 1991. Khác với Windows hay macOS, Linux hoàn toàn miễn phí và có thể tùy chỉnh.*

#### 1.2 Why DevOps needs Linux? (Tại sao DevOps cần Linux?)

| Reason | Explanation |
|--------|-------------|
| **Servers run Linux** | 90%+ servers on the internet run Linux |
| **Containers** | Docker, Kubernetes are based on Linux |
| **Scripting** | Bash scripting is a powerful automation tool |
| **Free & Open Source** | No license cost, easy to customize |

#### 1.3 Popular Linux Distributions (Các Linux Distributions phổ biến)

```
┌─────────────────────────────────────────────────────────────┐
│                    LINUX DISTRIBUTIONS                       │
├────────────────┬────────────────┬────────────────────────────┤
│   Ubuntu/      │   RHEL/        │   Alpine                   │
│   Debian       │   CentOS       │   (Containers)             │
├────────────────┼────────────────┼────────────────────────────┤
│   apt install  │   yum install  │   apk add                  │
│   .deb         │   .rpm         │   Minimal size             │
└────────────────┴────────────────┴────────────────────────────┘
```

---

### 2. Linux File System (Hệ thống File Linux) - 1 hour

#### 2.1 Directory Structure (Cấu trúc thư mục)

```
/                    ← Root directory (thư mục gốc)
├── home/            ← User directories (thư mục người dùng)
│   └── user/        ← User's home (tương đương C:\Users\username)
├── etc/             ← System config files (file cấu hình)
├── var/             ← Logs, databases
│   └── log/         ← System logs
├── tmp/             ← Temporary files (files tạm - tự động xóa)
├── opt/             ← Third-party software (phần mềm bên thứ 3)
├── usr/             ← User programs (chương trình người dùng)
│   ├── bin/         ← User binaries
│   └── local/       ← Locally installed software
├── bin/             ← Essential binaries (binaries thiết yếu)
├── sbin/            ← System binaries (admin)
└── root/            ← Root user's home
```

#### 2.2 Absolute vs Relative Paths (Đường dẫn tuyệt đối vs tương đối)

```bash
# Absolute Path - Starts from / (Đường dẫn tuyệt đối - Bắt đầu từ /)
/home/user/documents/file.txt

# Relative Path - Relative to current location (Đường dẫn tương đối - Tương đối với vị trí hiện tại)
./documents/file.txt    # In current directory (trong thư mục hiện tại)
../documents/file.txt   # Go up one level then into documents (lùi 1 cấp)
```

#### 2.3 Important Directories (Những thư mục quan trọng)

| Directory | Purpose | Example |
|-----------|---------|---------|
| `/home/user` | Personal files (Files cá nhân) | Documents, Downloads |
| `/etc` | Config files (Cấu hình) | `/etc/nginx/nginx.conf` |
| `/var/log` | Logs (Nhật ký) | `/var/log/syslog` |
| `/tmp` | Temporary files (Tạm thời) | Auto-deleted on reboot |

---

### 3. Basic Navigation (Điều hướng cơ bản) - 1 hour

#### 3.1 pwd - Print Working Directory

```bash
$ pwd
/home/devops

# Shows where you are (Cho biết bạn đang ở đâu)
```

#### 3.2 ls - List Directory Contents (Liệt kê nội dung thư mục)

```bash
ls              # List files (Liệt kê files)
ls -l           # Long format (Chi tiết)
ls -a           # Show hidden files (Hiển thị hidden files)
ls -la          # Combine both (Kết hợp cả 2)
ls -lh          # Human readable (KB, MB, GB)
ls -lt          # Sort by time (Sắp xếp theo thời gian)
```

**Reading `ls -l` output (Đọc output của ls -l):**

```
-rw-r--r-- 1 user group 4096 Dec 29 10:00 file.txt
│          │ │    │     │    │            │
│          │ │    │     │    │            └── File name (Tên file)
│          │ │    │     │    └── Modification time (Thời gian sửa)
│          │ │    │     └── Size in bytes (Kích thước)
│          │ │    └── Group owner
│          │ └── User owner
│          └── Hard links count (Số hard links)
└── Permissions (rwxrwxrwx)
```

#### 3.3 cd - Change Directory (Thay đổi thư mục)

```bash
cd /path/to/directory    # Go to absolute path (Đi đến đường dẫn tuyệt đối)
cd folder                # Go into subfolder (Đi vào folder con)
cd ..                    # Go up one level (Lùi lên 1 cấp)
cd ../..                 # Go up two levels (Lùi lên 2 cấp)
cd ~                     # Go to home directory (Về home)
cd -                     # Go to previous directory (Quay lại thư mục trước)
```

---

### 4. File and Directory Operations (Thao tác Files và Thư mục) - 2 hours

#### 4.1 Creating Files and Directories (Tạo files và thư mục)

```bash
# Create empty file (Tạo file rỗng)
touch file.txt

# Create file with content (Tạo file với nội dung)
echo "Hello World" > file.txt

# Create directory (Tạo thư mục)
mkdir mydir

# Create nested directories (Tạo thư mục lồng nhau)
mkdir -p parent/child/grandchild
```

#### 4.2 Copy, Move, Rename (Sao chép, Di chuyển, Đổi tên)

```bash
# Copy file (Sao chép file)
cp source.txt destination.txt
cp source.txt /path/to/destination/

# Copy directory recursively (Sao chép thư mục đệ quy)
cp -r source_dir/ destination_dir/

# Move/Rename file (Di chuyển/Đổi tên file)
mv oldname.txt newname.txt
mv file.txt /path/to/destination/

# Move directory (Di chuyển thư mục)
mv source_dir/ destination/
```

#### 4.3 Deleting Files and Directories (Xóa files và thư mục)

```bash
# Delete file (Xóa file)
rm file.txt

# Delete multiple files (Xóa nhiều files)
rm file1.txt file2.txt file3.txt
rm *.txt                # Delete all .txt files (Xóa tất cả .txt)

# Delete empty directory (Xóa thư mục rỗng)
rmdir empty_dir/

# Delete directory and contents (Xóa thư mục và nội dung)
rm -r directory/

# Delete without confirmation (DANGEROUS!) (Xóa không hỏi - NGUY HIỂM!)
rm -rf directory/

# ⚠️ WARNING: Never run (CẢNH BÁO: Không bao giờ chạy): rm -rf /
```

#### 4.4 Reading File Contents (Đọc nội dung files)

```bash
# View entire file (Xem toàn bộ file)
cat file.txt

# View with paging - press q to quit (Xem với phân trang - nhấn q để thoát)
less file.txt

# View first/last lines (Xem dòng đầu/cuối)
head file.txt
head -n 20 file.txt     # First 20 lines (20 dòng đầu)
tail file.txt
tail -n 20 file.txt     # Last 20 lines (20 dòng cuối)

# Follow file in realtime - for logs (Theo dõi realtime - cho logs)
tail -f /var/log/syslog
```

---

### 5. Search (Tìm kiếm) - 1 hour

#### 5.1 find - Find Files (Tìm files)

```bash
# Find by name (Tìm theo tên)
find /home -name "*.txt"

# Find by type (f=file, d=directory) (Tìm theo loại)
find . -type f -name "*.log"
find . -type d -name "config"

# Find by modification time (Tìm theo thời gian sửa đổi)
find . -mtime -7        # Modified in last 7 days (Sửa trong 7 ngày qua)
find . -mtime +30       # Modified more than 30 days ago (Sửa hơn 30 ngày trước)

# Find by size (Tìm theo kích thước)
find . -size +100M      # Larger than 100MB (Lớn hơn 100MB)
find . -size -10K       # Smaller than 10KB (Nhỏ hơn 10KB)
```

#### 5.2 grep - Search in Content (Tìm kiếm trong nội dung)

```bash
# Find pattern in file (Tìm pattern trong file)
grep "error" logfile.txt

# Case insensitive (Không phân biệt hoa thường)
grep -i "Error" logfile.txt

# Show line numbers (Hiển thị số dòng)
grep -n "error" logfile.txt

# Search recursively in directory (Tìm đệ quy trong thư mục)
grep -r "TODO" ./src/

# Count occurrences (Đếm số lần xuất hiện)
grep -c "error" logfile.txt
```

#### 5.3 Combining find and grep (Kết hợp find và grep)

```bash
# Find .txt files containing "error" (Tìm files .txt chứa "error")
find . -name "*.txt" -exec grep -l "error" {} \;
```

---

### 6. Permissions (Quyền truy cập) - 2 hours

#### 6.1 Understanding Permissions (Hiểu về Permissions)

```
-rwxr-xr--
│└┬─┘└┬─┘└┬─┘
│ │   │   └── Others (o): r-- = read only (chỉ đọc)
│ │   └────── Group (g): r-x = read + execute (đọc + chạy)
│ └────────── User/Owner (u): rwx = full access (toàn quyền)
└──────────── File type (- = file, d = directory)
```

| Permission | Symbol | Number | Meaning |
|------------|--------|--------|---------|
| Read | r | 4 | Read file/list directory (Đọc file/liệt kê thư mục) |
| Write | w | 2 | Write file/create delete in dir (Ghi file/tạo xóa) |
| Execute | x | 1 | Run file/enter directory (Chạy file/vào thư mục) |

#### 6.2 chmod - Change Permissions (Thay đổi permissions)

**Numeric method (Cách numeric):**

```bash
chmod 755 script.sh     # rwxr-xr-x
chmod 644 file.txt      # rw-r--r--
chmod 600 secret.txt    # rw------- (owner only - chỉ owner)
chmod 777 folder/       # rwxrwxrwx (NOT RECOMMENDED! - KHÔNG NÊN!)
```

**Symbolic method (Cách symbolic):**

```bash
chmod +x script.sh      # Add execute for all (Thêm execute cho tất cả)
chmod u+x script.sh     # Add execute for owner (Thêm execute cho owner)
chmod g-w file.txt      # Remove write from group (Bỏ write của group)
chmod o-rwx secret.txt  # Remove all from others (Bỏ hết quyền của others)
```

#### 6.3 chown - Change Owner (Thay đổi owner)

```bash
sudo chown user:group file.txt
sudo chown -R user:group directory/  # Recursive (Đệ quy)
```

---

### 7. Process Management (Quản lý Processes) - 1.5 hours

#### 7.1 Viewing Processes (Xem processes)

```bash
# List all processes (Liệt kê tất cả processes)
ps aux

# Find specific process (Tìm process cụ thể)
ps aux | grep nginx

# View realtime - press q to quit (Xem realtime - nhấn q để thoát)
top
htop    # Better version - needs install (Phiên bản đẹp hơn - cần cài)
```

#### 7.2 Kill Processes (Dừng processes)

```bash
# Kill by PID (Kill bằng PID)
kill 1234
kill -9 1234    # Force kill (Buộc dừng)

# Kill by name (Kill bằng tên)
pkill nginx
killall nginx
```

#### 7.3 Background Processes (Processes chạy nền)

```bash
# Run in background (Chạy trong background)
./script.sh &

# View background jobs (Xem background jobs)
jobs

# Bring to foreground (Đưa về foreground)
fg %1

# Send to background (Đưa vào background)
bg %1

# Run process that persists after terminal closes (Chạy không bị ảnh hưởng khi đóng terminal)
nohup ./long_running_script.sh &
```

---

### 8. Package Manager (Quản lý Package) - 1 hour

#### 8.1 APT (Ubuntu/Debian)

```bash
# Update package list (Update danh sách packages)
sudo apt update

# Upgrade installed packages (Upgrade packages đã cài)
sudo apt upgrade

# Install package (Cài đặt package)
sudo apt install nginx

# Remove package (Gỡ cài đặt)
sudo apt remove nginx
sudo apt autoremove     # Remove unused dependencies (Xóa dependencies không dùng)

# Search package (Tìm package)
apt search nginx
```

#### 8.2 YUM/DNF (RHEL/CentOS)

```bash
sudo yum update
sudo yum install nginx
sudo yum remove nginx
yum search nginx
```

---

### 9. Bash Scripting (Viết Script Bash) - 3 hours

#### 9.1 First Script (Script đầu tiên)

```bash
#!/bin/bash
# File: hello.sh

echo "Hello, DevOps!"
```

Run script (Chạy script):

```bash
chmod +x hello.sh
./hello.sh
```

#### 9.2 Variables (Biến)

```bash
#!/bin/bash

# Assign variable - NO spaces around the "=" sign (Gán biến - KHÔNG có dấu cách quanh dấu "=")
NAME="DevOps"
AGE=25

# Use variable (Sử dụng biến)
echo "Hello, $NAME"
echo "You are $AGE years old"

# Input from user (Input từ người dùng)
echo "Enter your name:"
read USERNAME
echo "Hello, $USERNAME!"
```

#### 9.3 Conditionals (Điều kiện if/else)

```bash
#!/bin/bash

FILE="/etc/passwd"

if [ -f "$FILE" ]; then
    echo "$FILE exists."
else
    echo "$FILE does not exist."
fi

# Check numbers (Kiểm tra số)
NUMBER=10
if [ $NUMBER -gt 5 ]; then
    echo "Greater than 5"
elif [ $NUMBER -eq 5 ]; then
    echo "Equal to 5"
else
    echo "Less than 5"
fi
```

**Operators (Toán tử):**

| Operator | Meaning |
|----------|---------|
| `-f` | File exists (File tồn tại) |
| `-d` | Directory exists (Thư mục tồn tại) |
| `-eq` | Equal - numbers (Bằng - số) |
| `-ne` | Not equal (Không bằng) |
| `-gt` | Greater than (Lớn hơn) |
| `-lt` | Less than (Nhỏ hơn) |
| `=` | String equal (String bằng nhau) |
| `!=` | String not equal (String khác nhau) |

#### 9.4 Loops (Vòng lặp)

```bash
#!/bin/bash

# For loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# For loop with range (Với range)
for i in {1..10}; do
    echo "Count: $i"
done

# For loop with files (Với files)
for file in *.txt; do
    echo "Processing: $file"
done

# While loop
COUNT=0
while [ $COUNT -lt 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done
```

#### 9.5 Functions (Hàm)

```bash
#!/bin/bash

# Define function (Định nghĩa function)
greet() {
    echo "Hello, $1!"
}

# Call function (Gọi function)
greet "DevOps"
greet "World"

# Function with return value (Function với return value)
add_numbers() {
    local RESULT=$(( $1 + $2 ))
    echo $RESULT
}

SUM=$(add_numbers 5 3)
echo "Sum: $SUM"
```

---

### 10. Pipes and Redirect (Pipes và Redirect) - 1 hour

#### 10.1 Pipe (|)

Pass output of one command as input to another (Truyền output của command này làm input cho command khác):

```bash
# Count files in directory (Đếm số file trong thư mục)
ls -la | wc -l

# Find nginx process (Tìm process nginx)
ps aux | grep nginx

# Sort and get 10 largest files (Sắp xếp và lấy 10 file lớn nhất)
du -h * | sort -rh | head -10
```

#### 10.2 Redirect (Chuyển hướng)

```bash
# Write output to file - overwrite (Ghi output vào file - ghi đè)
echo "Hello" > file.txt

# Append to file (Nối vào file)
echo "World" >> file.txt

# Redirect stderr (Chuyển hướng lỗi)
command 2> error.log

# Redirect both stdout and stderr (Chuyển hướng cả output và lỗi)
command > output.txt 2>&1
command &> all_output.txt
```

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|-------------|
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [Setup Environment](../../Setup_Environment/) | **1.1 Linux & Bash** | [1.2 Python](../1.2_Python_Basics/) |

---

**Master Linux fundamentals! 🐧**

*Thành thạo nền tảng Linux!*

</div>
