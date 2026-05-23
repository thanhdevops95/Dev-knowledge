# 📋 Linux & Bash - Cheatsheet

> **Quick Reference for Linux Commands**
>
> *Tra cứu nhanh các lệnh Linux*

---

## 📂 File System Navigation (Điều hướng hệ thống file)

```bash
pwd                 # Print working directory (In thư mục hiện tại)
ls                  # List files (Liệt kê files)
ls -la              # List all files with details (Chi tiết tất cả files)
cd /path            # Change directory (Chuyển thư mục)
cd ..               # Go up one level (Lên một cấp)
cd ~                # Go to home directory (Về thư mục home)
```

---

## 📄 File Operations (Thao tác với file)

```bash
touch file.txt      # Create empty file (Tạo file rỗng)
mkdir dir           # Create directory (Tạo thư mục)
mkdir -p a/b/c      # Create nested directories (Tạo thư mục lồng nhau)
cp src dst          # Copy file (Sao chép file)
mv src dst          # Move/rename file (Di chuyển/đổi tên file)
rm file             # Delete file (Xóa file)
rm -rf dir          # Delete directory recursively (Xóa thư mục đệ quy)
```

---

## 👀 File Viewing (Xem file)

```bash
cat file            # View entire file (Xem toàn bộ file)
less file           # View with pagination (Xem với phân trang)
head -n 10 file     # View first 10 lines (Xem 10 dòng đầu)
tail -n 10 file     # View last 10 lines (Xem 10 dòng cuối)
tail -f file        # Follow file changes (Theo dõi thay đổi file)
```

---

## 🔐 Permissions (Phân quyền)

```bash
chmod 755 file      # rwxr-xr-x
chmod +x file       # Add execute permission (Thêm quyền thực thi)
chown user:group file  # Change owner (Đổi chủ sở hữu)
```

### Permission Numbers (Số phân quyền)

| # | Permission |
|---|------------|
| 7 | rwx (read + write + execute) |
| 6 | rw- (read + write) |
| 5 | r-x (read + execute) |
| 4 | r-- (read only) |
| 0 | --- (no permission) |

---

## ⚙️ Process Management (Quản lý tiến trình)

```bash
ps aux              # List all processes (Liệt kê tất cả tiến trình)
top                 # Interactive process viewer (Xem tiến trình tương tác)
htop                # Better process viewer (Xem tiến trình tốt hơn)
kill PID            # Kill process by ID (Dừng tiến trình theo ID)
kill -9 PID         # Force kill (Dừng cưỡng bức)
```

---

## 🔎 Text Search (Tìm kiếm văn bản)

```bash
grep "text" file    # Search text in file (Tìm text trong file)
grep -r "text" dir  # Search recursively (Tìm đệ quy)
grep -i "text" file # Case insensitive (Không phân biệt chữ hoa/thường)
find /path -name "*.txt"  # Find files (Tìm files)
```

---

## 📜 Bash Scripting

```bash
#!/bin/bash

# Variables (Biến)
NAME="DevOps"
echo "Hello $NAME"

# Conditionals (Điều kiện)
if [ -f file.txt ]; then
    echo "File exists"
fi

# Loops (Vòng lặp)
for i in 1 2 3; do
    echo $i
done

# While loop
while [ $COUNT -lt 10 ]; do
    echo $COUNT
    ((COUNT++))
done
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
