# Lời giải - Bài 3: Kỹ năng Viết Script

Dưới đây là lời giải chi tiết và giải thích cho các bài tập trong bài học 03. Mỗi bài tập đi kèm với code hoàn chỉnh và hướng dẫn thực thi.

---

### Bài 1: Script Chào hỏi (`greeting.sh`)

**Mục tiêu:** Viết script nhận tham số dòng lệnh và sử dụng câu lệnh `if` để xử lý các trường hợp khác nhau.

**Code hoàn chỉnh:**
(File `greeting.sh` đã có sẵn với nội dung chính xác)
```bash
#!/bin/bash

# Mục tiêu: In ra câu chào với tên được truyền vào từ tham số dòng lệnh.
# Nếu không có tham số nào, in ra thông báo hướng dẫn.

# Kiểm tra xem tham số đầu tiên ($1) có rỗng hay không.
# Cú pháp `if [ -z "$1" ]` có nghĩa là "if the string $1 is zero-length".
# Luôn đặt biến trong dấu ngoặc kép ("$1") để xử lý đúng các trường hợp tên có chứa khoảng trắng.
if [ -z "$1" ]; then
  # Nếu không có tham số, in ra thông báo lỗi/hướng dẫn.
  echo "Vui lòng cho tôi biết tên của bạn."
  # Thoát script với mã lỗi 1 (biểu thị có lỗi xảy ra).
  exit 1
else
  # Nếu có tham số, in ra câu chào.
  echo "Chào mừng $1 đến với thế giới của Bash Scripting!"
fi
```

**Cách thực thi:**
1.  **Cấp quyền thực thi:**
    ```bash
    chmod +x greeting.sh
    ```
2.  **Chạy script với một tham số:**
    ```bash
    ./greeting.sh Elsa
    ```
    *Kết quả mong đợi:*
    ```
    Chào mừng Elsa đến với thế giới của Bash Scripting!
    ```
3.  **Chạy script mà không có tham số:**
    ```bash
    ./greeting.sh
    ```
    *Kết quả mong đợi:*
    ```
    Vui lòng cho tôi biết tên của bạn.
    ```

---

### Bài 2: Vòng lặp và Tạo File (`file_creator.sh`)

**Mục tiêu:** Sử dụng vòng lặp `for` để tự động hóa một tác vụ lặp đi lặp lại.

**Code hoàn chỉnh:**
(`file_creator.sh` đã được tạo)
```bash
#!/bin/bash

echo "Bắt đầu tạo files..."

for i in {1..5}; do
  echo "Đây là file thứ $i" > "file$i.txt"
done

echo "Đã tạo 5 files: file1.txt, file2.txt, file3.txt, file4.txt, file5.txt."
ls -l file*.txt
```

**Cách thực thi:**
1.  **Cấp quyền thực thi:**
    ```bash
    chmod +x file_creator.sh
    ```
2.  **Chạy script:**
    ```bash
    ./file_creator.sh
    ```
    *Kết quả mong đợi:* Script sẽ tạo ra 5 file, sau đó `ls -l` sẽ liệt kê chúng.
3.  **Kiểm tra nội dung một file:**
    ```bash
    cat file3.txt
    ```
    *Kết quả mong đợi:*
    ```
    Đây là file thứ 3
    ```

---

### Bài 3: Cải tiến Script Backup (`backup_improved.sh`)

**Mục tiêu:** Chỉnh sửa một script có sẵn, thêm vào logic nghiệp vụ phức tạp hơn bằng cách sử dụng `find`.

**Code hoàn chỉnh:**
(`backup_improved.sh` đã được tạo)
```bash
#!/bin/bash

# --- Cấu hình ---
SOURCE_DIR="$(dirname "$0")/../../.."
BACKUP_DIR="$(dirname "$0")/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILENAME="backup-$DATE.tar.gz"

echo "Bắt đầu quá trình sao lưu thư mục $SOURCE_DIR..."
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/$FILENAME" "$SOURCE_DIR"
echo "Sao lưu hoàn tất! File được lưu tại: $BACKUP_DIR/$FILENAME"
echo "---"

echo "Bắt đầu dọn dẹp các bản sao lưu cũ hơn 7 ngày..."
# -mtime +7: tìm file cũ hơn 7 ngày.
# -print: In tên file ra màn hình.
# -delete: Xóa file (được comment lại để an toàn).
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +7 -print
echo "Dọn dẹp hoàn tất."
```

**Cách thực thi:**
1.  **Cấp quyền thực thi:**
    ```bash
    chmod +x backup_improved.sh
    ```
2.  **Chạy script:**
    ```bash
    ./backup_improved.sh
    ```
    *Kết quả mong đợi:* Script sẽ tạo một file nén `.tar.gz` của toàn bộ project vào thư mục `backups`. Phần dọn dẹp sẽ chạy nhưng có thể không tìm thấy file nào cũ hơn 7 ngày ở lần chạy đầu tiên.

---

### Bài 4: Sử dụng Hàm (`system_check.sh`)

**Mục tiêu:** Học cách tổ chức code bằng các hàm (functions) để dễ đọc và tái sử dụng.

**Code hoàn chỉnh:**
(`system_check.sh` đã được tạo)
```bash
#!/bin/bash

show_uptime() {
  echo "--- Uptime của hệ thống ---"
  uptime
  echo ""
}

show_disk_usage() {
  echo "--- Dung lượng ổ đĩa sử dụng ---"
  df -h
  echo ""
}

show_memory_usage() {
  echo "--- Dung lượng bộ nhớ (RAM) sử dụng ---"
  if command -v free &> /dev/null; then
    free -h
  else
    # Lệnh thay thế cho macOS
    sysctl -n hw.memsize | awk '{printf "Total Memory: %.2f GB\n", $1/1024/1024/1024}'
    vm_stat | grep -E "Pages free|Pages active|Pages inactive|Pages speculative|Pages wired down"
  fi
  echo ""
}

# --- Thân script chính ---
show_uptime
show_disk_usage
show_memory_usage
echo "Kiểm tra hệ thống hoàn tất."
```

**Cách thực thi:**
1.  **Cấp quyền thực thi:**
    ```bash
    chmod +x system_check.sh
    ```
2.  **Chạy script:**
    ```bash
    ./system_check.sh
    ```
    *Kết quả mong đợi:* Script sẽ in ra lần lượt các thông tin về uptime, dung lượng ổ đĩa và dung lượng bộ nhớ của máy bạn, mỗi phần có một tiêu đề rõ ràng. Script này tương thích với cả Linux và macOS.
