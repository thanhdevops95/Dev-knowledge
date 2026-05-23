# 📋 Linux & Bash - Cheatsheet

> **Quick Reference for Linux Commands and Bash Scripting**
>
> *Tra cứu nhanh các lệnh Linux và Bash scripting*

---

## 📂 File System Navigation (Điều hướng hệ thống file)

| Command (Lệnh) | Description (Mô tả) |
|----------------|---------------------|
| `pwd` | Print working directory (In thư mục hiện tại) |
| `ls` | List files (Liệt kê files) |
| `ls -la` | List all files with details (Chi tiết tất cả files, bao gồm cả file ẩn) |
| `cd /path` | Change directory (Chuyển thư mục) |
| `cd ..` | Go up one level (Lên một cấp) |
| `cd -` | Go to previous directory (Về thư mục vừa đứng trước đó) |
| `cd ~` | Go to home directory (Về thư mục home) |

---

## 📄 File & Directory Operations (Thao tác File & Thư mục)

| Command (Lệnh) | Description (Mô tả) |
|----------------|---------------------|
| `touch file.txt` | Create empty file (Tạo file rỗng) |
| `mkdir dir` | Create directory (Tạo thư mục) |
| `mkdir -p a/b/c` | Create nested directories (Tạo thư mục lồng nhau) |
| `cp src dst` | Copy file (Sao chép file) |
| `cp -r dir1 dir2`| Copy directory recursively (Sao chép thư mục) |
| `mv src dst` | Move/rename file (Di chuyển hoặc đổi tên file) |
| `rm file` | Delete file (Xóa file) |
| `rm -rf dir` | Delete directory recursively (Xóa thư mục cưỡng bức) |

---

## 👀 File Viewing & Searching (Xem & Tìm kiếm)

| Command (Lệnh) | Description (Mô tả) |
|----------------|---------------------|
| `cat file` | View entire file (Xem toàn bộ file) |
| `less file` | View with pagination (Xem phân trang - `q` để thoát) |
| `head -n 10 file`| View first 10 lines (Xem 10 dòng đầu) |
| `tail -n 10 file`| View last 10 lines (Xem 10 dòng cuối) |
| `tail -f file` | Follow file changes (Theo dõi thay đổi theo thời gian thực) |
| `grep "text" file`| Search text in file (Tìm văn bản trong file) |
| `grep -ri "text" .`| Recursive case-insensitive search (Tìm đệ quy, ko phân biệt hoa thường) |
| `find . -name "f*"`| Find files by name (Tìm file theo tên) |

---

## 🔐 Permissions & Ownership (Quyền hạn & Sở hữu)

| Command (Lệnh) | Description (Mô tả) |
|----------------|---------------------|
| `chmod +x file` | Add execute permission (Thêm quyền thực thi) |
| `chmod 755 file`| Owner: rwx, Group/Others: r-x (Quyền phổ biến cho script) |
| `chmod 600 file`| Owner: rw-, others: --- (Quyền cho file bí mật/key) |
| `chown user:group`| Change owner and group (Đổi chủ sở hữu và nhóm) |
| `sudo command` | Run as superuser (Chạy với quyền root) |

---

## ⚙️ Process & System (Tiến trình & Hệ thống)

| Command (Lệnh) | Description (Mô tả) |
|----------------|---------------------|
| `ps aux` | List all processes (Liệt kê toàn bộ tiến trình) |
| `top` / `htop` | Interactive process viewer (Xem tiến trình tương tác) |
| `kill -9 PID` | Force kill process (Dừng tiến trình cưỡng bức) |
| `df -h` | Check disk space (Kiểm tra dung lượng đĩa) |
| `free -h` | Check memory usage (Kiểm tra dung lượng RAM) |
| `uptime` | System run time (Thời gian hệ thống đã chạy) |

---

## 🌐 Networking (Mạng)

| Command (Lệnh) | Description (Mô tả) |
|----------------|---------------------|
| `ip addr` | Show IP addresses (Xem các địa chỉ IP) |
| `ping host` | Check connectivity (Kiểm tra kết nối đến host) |
| `curl -I URL` | Fetch HTTP headers (Lấy thông tin header của URL) |
| `wget URL` | Download file from Web (Tải file từ web) |
| `netstat -tunlp` | List listening ports (Xem các port đang mở - cần cài net-tools) |

---

## 📦 Archiving & Compression (Nén & Lưu trữ)

| Command (Lệnh) | Description (Mô tả) |
|----------------|---------------------|
| `tar -cvf a.tar dir`| Create tarball (Nén thư mục thành file .tar) |
| `tar -xvf a.tar` | Extract tarball (Giải nén file .tar) |
| `tar -czvf a.tar.gz dir`| Create compressed gzip (Nén thành .tar.gz) |
| `zip -r a.zip dir` | Create zip file (Nén thành file .zip) |
| `unzip a.zip` | Extract zip file (Giải nén file .zip) |

---

## ➡️ Redirection & Pipes (Chuyển hướng & Đường ống)

| Operator | Description (Mô tả) |
|----------|---------------------|
| `>` | Overwrite to file (Ghi đè vào file) |
| `>>` | Append to file (Ghi nối tiếp vào cuối file) |
| `2>` | Redirect error only (Chỉ chuyển hướng thông báo lỗi) |
| `&>` | Redirect both stdout & stderr (Chuyển cả output và lỗi) |
| `|` | Pipe output to next command (Truyền output làm input cho lệnh sau) |

---

## 📜 Bash Scripting Basics (Cơ bản về Bash Scripting)

```bash
#!/bin/bash

# 1. Variables (Biến)
NAME="DevOps"
COUNT=1

# 2. Command Substitution (Thay thế lệnh)
# Gán kết quả của lệnh vào một biến
CURRENT_DATE=$(date)
echo "Today is $CURRENT_DATE"

# 3. Conditionals (Điều kiện)
if [ "$NAME" == "DevOps" ]; then
    echo "Welcome, $NAME!"
fi

# 4. For Loop (Vòng lặp For)
for i in {1..3}; do
    echo "Counter: $i"
done

# 5. While Loop (Vòng lặp While)
while [ $COUNT -le 3 ]; do
    echo "Count is $COUNT"
    ((COUNT++))
done

# 6. Functions (Hàm)
my_func() {
    echo "Hello from function"
}
my_func
```

---

## 🔗 Navigation (Điều hướng)

[⬅️ README](./README.md) | [LABS](./LABS.md) | [QUIZ ➡️](./QUIZ.md)

---

*Last Updated: 2026-01-16*
