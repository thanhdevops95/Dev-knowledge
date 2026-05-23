# 🧪 Labs - Linux & Bash

> **Hands-on Labs to Strengthen Your Knowledge**
>
> *Bài thực hành hands-on để củng cố kiến thức*

---

## 📋 Instructions (Hướng dẫn thực hiện)

1. **Environment (Môi trường)**: Use WSL2 (Windows), Terminal (macOS), or a Linux VM.
   *(Sử dụng WSL2 (Windows), Terminal (macOS), hoặc Linux VM.)*
2. **Duration (Thời gian)**: Each lab takes ~15-30 minutes.
   *(Mỗi lab ~15-30 phút.)*
3. **Notes (Ghi chú)**: Document the commands you use for future review.
   *(Ghi lại các lệnh đã dùng để review sau.)*

---

## Lab 1: Explore File System (Khám phá File System) 🗂️

**Goal**: Familiarize with the Linux directory structure.
*(Làm quen với cấu trúc thư mục Linux.)*

### Step 1: Check Current Location (Bước 1: Kiểm tra vị trí hiện tại)

Use the `pwd` (print working directory) command to see where you are.
*(Sử dụng lệnh `pwd` để xem bạn đang đứng ở đâu.)*

```bash
pwd
```

**Expected Result (Kết quả mong đợi)**: `/home/username` or similar.

### Step 2: List Root Directory (Bước 2: Liệt kê thư mục gốc)

View the top-level directory of the Linux system.
*(Xem thư mục cấp cao nhất của hệ thống Linux.)*

```bash
ls /
```

**Observation (Quan sát)**: What directories do you see? (e.g., `bin`, `etc`, `home`, `var`).

### Step 3: Explore Important Directories (Bước 3: Khám phá các thư mục quan trọng)

Check contents of system configuration and log directories.
*(Kiểm tra nội dung các thư mục cấu hình hệ thống và nhật ký.)*

```bash
# Configuration files (Thư mục cấu hình)
ls /etc | head -20

# Log files (Thư mục logs)
ls /var/log

# Temporary files (Thư mục tạm)
ls /tmp
```

### Step 4: Navigate Between Directories (Bước 4: Di chuyển qua các thư mục)

Practice moving around the file system using `cd`.
*(Thực hành di chuyển trong file system bằng lệnh `cd`.)*

```bash
cd /var/log
pwd
ls -la

# Move to configuration directory
cd /etc
pwd
ls nginx/    # Will show error if Nginx is not installed (Sẽ báo lỗi nếu chưa cài nginx)

# Return home
cd ~
pwd
```

### ✅ Checklist

- [ ] Identify current location with `pwd`
- [ ] List contents with `ls`
- [ ] Navigate with `cd`
- [ ] Understand the purpose of `/`, `/home`, `/etc`, `/var`

### ✅ Verification (Kiểm chứng)

Confirm you've completed this lab successfully:

*(Xác nhận bạn đã hoàn thành lab thành công:)*

```bash
# Verify you can navigate (Xác nhận bạn có thể điều hướng)
cd / && pwd && cd ~ && pwd

# Expected: First shows /, then /home/username
```

### 🔧 Troubleshooting (Xử lý sự cố)

| Error | Solution |
|-------|----------|
| `bash: cd: /var/log: Permission denied` | Use `sudo ls /var/log` or switch to root *(Dùng sudo hoặc chuyển sang root)* |
| `-bash: ls: command not found` | PATH issue, try `/bin/ls` *(Lỗi PATH, thử /bin/ls)* |
| `No such file or directory` | Check spelling and path *(Kiểm tra chính tả và đường dẫn)* |

### 🧹 Cleanup (Dọn dẹp)

No cleanup needed for this lab - we only explored the filesystem.

*(Không cần dọn dẹp cho lab này - chúng ta chỉ khám phá hệ thống file.)*

---

## Lab 2: File and Directory Operations (Thao tác Files và Directories) 📁

**Goal**: Create, copy, move, and delete files and directories.
*(Tạo, copy, move, xóa files và directories.)*

### Step 1: Create Project Structure (Bước 1: Tạo cấu trúc project)

Create nested directories for a sample project.
*(Tạo các thư mục lồng nhau cho một project mẫu.)*

```bash
cd ~
mkdir -p devops-lab/project1/src
mkdir -p devops-lab/project1/docs
mkdir -p devops-lab/project1/tests
```

### Step 2: Verify Structure (Bước 2: Kiểm tra cấu trúc)

Use the recursive list command to see the hierarchy.
*(Sử dụng lệnh liệt kê đệ quy để xem cấu trúc phân cấp.)*

```bash
ls -R devops-lab/
```

### Step 3: Create Files (Bước 3: Tạo files)

Create empty files and files with initial content.
*(Tạo các file rỗng và các file có nội dung ban đầu.)*

```bash
cd devops-lab/project1

# Create an empty file (Tạo file rỗng)
touch README.md

# Create file with content (Tạo file với nội dung)
echo "# My DevOps Project" > README.md
echo "Version: 1.0" >> README.md

# Create utility scripts in src (Tạo script trong src)
echo 'echo "Hello World"' > src/main.sh
echo '# utility functions' > src/utils.sh
```

### Step 4: View File Content (Bước 4: Xem nội dung files)

Use `cat` to display file contents in the terminal.
*(Sử dụng `cat` để hiển thị nội dung file.)*

```bash
cat README.md
cat src/main.sh
```

### Step 5: Copy and Move Files (Bước 5: Copy và Move files)

Organize files by copying for backup and renaming.
*(Sắp xếp files bằng cách copy dự phòng và đổi tên.)*

```bash
# Copy file to docs
cp README.md docs/README_backup.md

# Rename/Move file
mv src/utils.sh src/helpers.sh

# Verify changes (Kiểm tra)
ls -la docs/
ls -la src/
```

### Step 6: Delete Files and Directories (Bước 6: Xóa files và thư mục)

Clean up temporary files. Be careful with these commands!
*(Dọn dẹp các file tạm. Hãy cẩn thận với các lệnh này!)*

```bash
# Create and delete a file (Tạo và xóa file)
touch temp_file.txt
rm temp_file.txt

# Create and delete a directory recursively (Xóa thư mục đệ quy)
mkdir to_delete
rm -r to_delete
```

### ✅ Checklist

- [ ] Create nested directories with `mkdir -p`
- [ ] Manage files with `touch` and `echo`
- [ ] Use `cp` and `mv` correctly
- [ ] Safely delete with `rm` and `rm -r`

### ✅ Verification (Kiểm chứng)

Confirm your project structure exists:

*(Xác nhận cấu trúc project tồn tại:)*

```bash
# Verify structure (Xác nhận cấu trúc)
ls -la ~/devops-lab/project1/
ls -la ~/devops-lab/project1/src/

# Expected: See README.md, src/, docs/, tests/ directories
```

### 🔧 Troubleshooting (Xử lý sự cố)

| Error | Solution |
|-------|----------|
| `mkdir: cannot create directory: File exists` | Directory already exists - this is OK *(Thư mục đã tồn tại - OK)* |
| `rm: cannot remove: Is a directory` | Use `rm -r` for directories *(Dùng rm -r cho thư mục)* |
| `cp: missing destination file operand` | Check syntax: `cp source destination` *(Kiểm tra cú pháp)* |

### 🧹 Cleanup (Dọn dẹp)

```bash
# Remove lab directory if needed (Xóa thư mục lab nếu cần)
rm -rf ~/devops-lab/project1

# Or keep for next labs (Hoặc giữ lại cho labs tiếp theo)
```

---

## Lab 3: Find and Filter (Tìm kiếm và Lọc) 🔍

**Goal**: Master `find` for files and `grep` for content.
*(Làm chủ lệnh `find` cho files và `grep` cho nội dung.)*

### Setup (Chuẩn bị)

Generate sample logs for searching.
*(Tạo dữ liệu log mẫu để thực hành tìm kiếm.)*

```bash
cd ~/devops-lab/project1
mkdir -p logs
echo "INFO: Application started" > logs/error.log
echo "ERROR: Connection failed" >> logs/error.log
echo "INFO: Retrying..." >> logs/error.log
echo "ERROR: Timeout exceeded" >> logs/error.log
```

### Step 1: Find Files (Bước 1: Tìm files với find)

Locate files based on their names or types.
*(Tìm vị trí file dựa trên tên hoặc loại.)*

```bash
# Find all shell scripts (Tìm tất cả .sh files)
find . -name "*.sh"

# Find documentation files (Tìm tất cả .md files)
find . -name "*.md"

# List only directories (Liệt kê thư mục)
find . -type d
```

### Step 2: Search Content (Bước 2: Tìm trong nội dung với grep)

Extract specific information from log files.
*(Trích xuất thông tin cụ thể từ các file log.)*

```bash
# Find lines containing ERROR (Tìm dòng chứa ERROR)
grep "ERROR" logs/error.log

# Show line numbers (Hiển thị số dòng)
grep -n "ERROR" logs/error.log

# Case-insensitive search (Tìm không phân biệt hoa thường)
grep -i "error" logs/error.log

# Count occurrences (Đếm số lần xuất hiện)
grep -c "ERROR" logs/error.log
```

### Step 3: Combine Operations (Bước 3: Kết hợp tìm kiếm)

Search for text across multiple files recursively.
*(Tìm kiếm văn bản trong nhiều file một cách đệ quy.)*

```bash
# Find "echo" in all files (Tìm "echo" trong mọi file)
grep -r "echo" .

# Show only filenames (Chỉ hiển thị tên file)
grep -rl "echo" .
```

---

## Lab 4: Permissions (Phân quyền) 🔐

**Goal**: Understand and modify Linux file security.
*(Hiểu và thay đổi bảo mật file trong Linux.)*

### Step 1: Inspect Permissions (Bước 1: Xem permissions hiện tại)

Use `ls -la` to see who owns what and what access they have.
*(Xem ai sở hữu gì và họ có quyền truy cập nào.)*

```bash
cd ~/devops-lab/project1
ls -la src/
```

### Step 2: Script Execution Test (Bước 2: Thử nghiệm chạy script)

Observe "Permission denied" when a script isn't executable.
*(Quan sát lỗi "Permission denied" khi script chưa có quyền thực thi.)*

```bash
# Create a simple script (Tạo script)
echo '#!/bin/bash
echo "Hello from script!"' > src/myscript.sh

# Check default permissions (Xem permission mặc định)
ls -l src/myscript.sh

# Try to run (it will fail) (Thử chạy - sẽ lỗi)
./src/myscript.sh
```

### Step 3: Grant Execute Rights (Bước 3: Thêm quyền thực thi)

Make the script runnable using `chmod`.
*(Làm cho script có thể chạy được bằng lệnh `chmod`.)*

```bash
# Add execute for owner (Thêm execute cho owner)
chmod u+x src/myscript.sh

# Run again (it works!) (Chạy lại)
./src/myscript.sh
```

### Step 4: Numeric Permissions (Bước 4: Thực hành với chế độ số)

Use the 3-digit octal system to set exact permissions.
*(Sử dụng hệ thống số 3 chữ số để thiết lập quyền chính xác.)*

```bash
touch src/secret.txt
# 600: Owner Read/Write only (Chỉ owner đọc ghi)
chmod 600 src/secret.txt

# 644: Owner Read/Write, Others Read (Mọi người đọc, owner ghi)
chmod 644 src/secret.txt

# 755: Common for scripts (Quyền phổ biến cho script)
chmod 755 src/myscript.sh
```

---

## Lab 5: Write Your First Bash Script (Viết Bash Script đầu tiên) 📝

**Goal**: Automate simple tasks with shell scripting.
*(Tự động hóa các nhiệm vụ đơn giản bằng shell scripting.)*

### Step 1: Base Script with Variables (Bước 1: Script cơ bản với biến)

Create a script that uses environment variables.
*(Tạo script sử dụng các biến môi trường.)*

```bash
mkdir -p scripts
cat > scripts/hello.sh << 'EOF'
#!/bin/bash
echo "🚀 Welcome to DevOps Journey!"
echo "📅 Today is: $(date)"
echo "👤 Current User: $USER"
echo "📂 Current Dir: $(pwd)"
EOF

chmod +x scripts/hello.sh
./scripts/hello.sh
```

### Step 2: Interactive Script (Bước 2: Script tương tác)

Use the `read` command to get user input.
*(Sử dụng lệnh `read` để lấy thông tin từ người dùng.)*

```bash
cat > scripts/greet.sh << 'EOF'
#!/bin/bash
echo "What is your name?"
read NAME
echo "Hello, $NAME! 👋 Welcome to DevOps Journey"
EOF

chmod +x scripts/greet.sh
./scripts/greet.sh
```

### Step 3: Conditional Logic (Bước 3: Script với điều kiện)

Use `if/else` to check for software installation.
*(Sử dụng `if/else` để kiểm tra phần mềm đã cài đặt chưa.)*

```bash
cat > scripts/check_docker.sh << 'EOF'
#!/bin/bash
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    docker --version
else
    echo "❌ Docker is NOT installed"
fi
EOF

chmod +x scripts/check_docker.sh
./scripts/check_docker.sh
```

---

## Lab 6: System Health Check (Script kiểm tra sức khỏe hệ thống) 💊

**Goal**: Create a professional monitoring script.
*(Tạo một script giám sát chuyên nghiệp.)*

### Create the Final Script (Tạo script hoàn chỉnh)

This script combines various Linux commands into a report.
*(Script này kết hợp nhiều lệnh Linux để tạo thành một báo cáo.)*

```bash
cat > scripts/system_health.sh << 'EOF'
#!/bin/bash
echo "========================================"
echo "    🏥 SYSTEM HEALTH CHECK REPORT"
echo "========================================"
echo "📋 SYSTEM INFO: $(hostname) | $(uname -r)"
echo "💻 CPU CORES: $(nproc)"
echo "📟 MEMORY:"
free -h | grep "Mem"
echo "💾 DISK USAGE:"
df -h | grep "/$"
echo "🐳 DOCKER STATUS:"
if command -v docker &> /dev/null; then echo "Running ✅"; else echo "Not installed ❌"; fi
echo "========================================"
EOF

chmod +x scripts/system_health.sh
./scripts/system_health.sh
```

---

## 🎯 Bonus Challenges (Thử thách bổ sung)

1. **Logging**: Modify `system_health.sh` to save output to a file.
   *(Sửa `system_health.sh` để lưu kết quả vào file log.)*
2. **Big Files**: Create a script to find all files >10MB in your home dir.
   *(Tạo script tìm tất cả các file lớn hơn 10MB trong thư mục home.)*
3. **Backup**: Write a script to backup `devops-lab` to a folder named `backups_YYYYMMDD`.
   *(Viết script backup thư mục lab vào một folder có gắn ngày tháng.)*

---

## ✅ General Verification (Kiểm chứng tổng quát)

After completing all labs, verify:

*(Sau khi hoàn thành tất cả labs, xác nhận:)*

```bash
# 1. Check devops-lab structure exists (Kiểm tra cấu trúc devops-lab)
ls -la ~/devops-lab/project1/

# 2. Check scripts are executable (Kiểm tra scripts có thể chạy)
ls -la ~/devops-lab/project1/scripts/

# 3. Run health check script (Chạy script kiểm tra sức khỏe)
~/devops-lab/project1/scripts/system_health.sh

# Expected: All commands work, scripts run successfully
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Permission Denied** | Cannot execute script | `chmod +x script.sh` *(Thêm quyền thực thi)* |
| **Command Not Found** | bash: command not found | Check PATH, install package *(Kiểm tra PATH, cài package)* |
| **No Such File** | File/directory doesn't exist | Verify path with `ls`, create with `mkdir -p` *(Xác nhận đường dẫn)* |
| **Syntax Error** | Script fails on line X | Check for typos, missing quotes *(Kiểm tra lỗi chính tả)* |
| **WSL Issues** | Windows-specific errors | Use forward slashes `/`, check file encoding *(Dùng / thay \)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

Remove all lab files when done:

*(Xóa tất cả files lab khi hoàn thành:)*

```bash
# Remove entire lab directory (Xóa toàn bộ thư mục lab)
rm -rf ~/devops-lab

# Or archive for future reference (Hoặc lưu trữ để tham khảo sau)
cd ~
tar -czvf devops-lab-backup.tar.gz devops-lab/
rm -rf devops-lab
```

> ⚠️ **Warning:** `rm -rf` is permanent! Double-check the path before running.
>
> *Cảnh báo: `rm -rf` xóa vĩnh viễn! Kiểm tra kỹ đường dẫn trước khi chạy.*

---

## 🔗 Navigation (Điều hướng)

[⬅️ README](./README.md) | [CHEATSHEET](./CHEATSHEET.md) | [QUIZ ➡️](./QUIZ.md)

---

*Last Updated: 2026-01-16*

