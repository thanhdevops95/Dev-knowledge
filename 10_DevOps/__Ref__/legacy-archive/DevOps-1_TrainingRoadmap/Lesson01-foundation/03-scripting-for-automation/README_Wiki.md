# Bài 3: Kỹ năng Viết Script (Scripting for Automation)

## 🎯 Mục tiêu bài học

- Hiểu được tại sao tự động hóa là một kỹ năng cốt lõi của DevOps.
- Nắm vững cú pháp cơ bản của Bash Scripting: biến, cấu trúc điều khiển, vòng lặp, và hàm.
- Viết được các script đơn giản để tự động hóa các tác vụ quản trị hệ thống Linux.
- Biết cách gỡ lỗi (debug) một bash script.

## 📖 Nội dung chính

1.  **Giới thiệu về Scripting:** Tại sao phải tự động hóa?
2.  **Bash Script 101:** Shebang, quyền thực thi, và cách chạy một script.
3.  **Biến và Tham số:** Cách khai báo biến, sử dụng biến hệ thống và tham số dòng lệnh (`$1`, `$2`, ...).
4.  **Cấu trúc điều khiển:** `if-else`, `elif`.
5.  **Vòng lặp:** Lặp qua danh sách với `for` và lặp theo điều kiện với `while`.
6.  **Hàm (Functions):** Tổ chức code thành các khối tái sử dụng.
7.  **Ví dụ thực tế:** Viết script tự động sao lưu một thư mục.

## 🛠️ Công cụ & Lý thuyết

-   **Ngôn ngữ Scripting:** <u>Bash Scripting</u>, Python, PowerShell.
-   **Công cụ:** `bash`, `chmod`.
-   **Lý thuyết:** Automation, Shell Scripting.

---

# Nội dung chi tiết - Bài 3: Kỹ năng Viết Script

Sau khi đã làm quen với dòng lệnh Linux, bước tiếp theo là kết hợp các lệnh đó lại thành một chuỗi tự động. Đây chính là lúc scripting phát huy sức mạnh. Đối với DevOps, "tự động hóa mọi thứ" là một tôn chỉ, và bash scripting là công cụ cơ bản nhất để làm điều đó trên môi trường Linux.

---

### 1. Giới thiệu về Scripting: Tại sao phải tự động hóa?

Hãy tưởng tượng bạn cần kiểm tra dung lượng ổ đĩa trên 100 máy chủ mỗi sáng. Việc đăng nhập vào từng máy và gõ lệnh `df -h` thật tẻ nhạt, tốn thời gian và dễ sai sót.

Scripting cho phép bạn viết một lần và chạy lại nhiều lần. Bạn có thể viết một script để:
-   Tự động sao lưu (backup) dữ liệu quan trọng.
-   Triển khai một phiên bản ứng dụng mới.
-   Dọn dọn các file log cũ.
-   Cài đặt và cấu hình một phần mềm.

-> Scripting giúp **tiết kiệm thời gian, giảm lỗi do con người, và đảm bảo tính nhất quán.**

---

### 2. Bash Script 101

Một bash script là một file văn bản chứa một chuỗi các lệnh shell.

-   **Shebang:** Dòng đầu tiên của script luôn phải là `#!/bin/bash`. Dòng này báo cho hệ điều hành biết rằng script này cần được thực thi bởi `bash`.
-   **Quyền thực thi:** Mặc định, file văn bản không có quyền chạy. Bạn cần cấp quyền cho nó:
    ```bash
    chmod +x your_script.sh
    ```
-   **Chạy script:**
    ```bash
    ./your_script.sh
    ```
-   **Comments:** Dùng dấu `#` để viết ghi chú. Mọi thứ sau dấu `#` trên cùng một dòng sẽ được bỏ qua.

```bash
#!/bin/bash

# Đây là script đầu tiên của tôi
echo "Hello, DevOps Journey!" # In ra một lời chào
```

---

### 3. Biến và Tham số

-   **Khai báo biến:** Viết liền, không có khoảng trắng quanh dấu `=`.n    ```bash
    NAME="Elsa"
    echo "Xin chào, $NAME"
    ```
-   **Biến hệ thống:** Bash có sẵn nhiều biến hữu ích, ví dụ:
    -   `$USER`: Tên người dùng hiện tại.
    -   `$HOME`: Thư mục nhà của người dùng.
    -   `$PWD`: Thư mục làm việc hiện tại.
-   **Tham số dòng lệnh:** Script có thể nhận tham số khi được gọi.
    -   `$0`: Tên của chính file script.
    -   `$1`: Tham số thứ nhất.
    -   `$2`: Tham số thứ hai.
    -   `$#`: Tổng số tham số được truyền vào.
    -   `$@`: Tất cả các tham số.

    *Ví dụ (save as `welcome.sh`):*
    ```bash
    #!/bin/bash
    echo "Chào bạn $1, chúc bạn một ngày tốt lành!"
    ```
    *Cách chạy:*
    `./welcome.sh Anh` -> Output: `Chào bạn Anh, chúc bạn một ngày tốt lành!`

---

### 4. Cấu trúc điều khiển: `if-else`

Cho phép script rẽ nhánh và thực hiện các hành động khác nhau dựa trên một điều kiện.

```bash
#!/bin/bash

# Kiểm tra xem có phải là người dùng root không
if [ $(whoami) == "root" ]; then
  echo "Bạn đang chạy với quyền root."
else
  echo "Bạn không phải là root. Một số lệnh có thể không hoạt động."
fi

# Các toán tử so sánh:
# -eq: bằng (số)
# -ne: không bằng (số)
# -gt: lớn hơn (số)
# ==: bằng (chuỗi)
# !=: không bằng (chuỗi)
# -z: chuỗi rỗng
```

---

### 5. Vòng lặp: `for` và `while`

-   **Vòng lặp `for`:** Dùng để lặp qua một danh sách các phần tử.
    ```bash
    # Lặp qua các số từ 1 đến 5
    for i in 1 2 3 4 5; do
      echo "Số: $i"
    done

    # Lặp qua các file trong thư mục
    for FILE in $(ls *.log); do
      echo "Đang xử lý file $FILE..."
    done
    ```
-   **Vòng lặp `while`:** Dùng khi bạn muốn lặp cho đến khi một điều kiện không còn đúng nữa.
    ```bash
    COUNTER=1
    while [ $COUNTER -le 5 ]; do
      echo "Đếm: $COUNTER"
      let COUNTER=COUNTER+1 # hoặc ((COUNTER++))
    done
    ```

---

### 6. Hàm (Functions)

Giúp bạn đóng gói một khối code để tái sử dụng.

```bash
#!/bin/bash

# Định nghĩa hàm
function say_hello() {
  echo "Xin chào từ bên trong hàm!"
}

# Gọi hàm
echo "Bắt đầu script..."
say_hello
echo "Script kết thúc."
```

---

### 7. Ví dụ thực tế: Script sao lưu tự động

Đây là một script đơn giản để nén một thư mục và lưu vào một thư mục backup với tên file có chứa ngày tháng hiện tại.

```bash
#!/bin/bash

# --- Cấu hình ---
SOURCE_DIR="/home/elsa/DevOps-Journey" # Thư mục cần backup
BACKUP_DIR="/mnt/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILENAME="backup-$DATE.tar.gz"
# ----------------

echo "Bắt đầu quá trình sao lưu thư mục $SOURCE_DIR..."

# Kiểm tra xem thư mục backup có tồn tại không, nếu không thì tạo ra
mkdir -p $BACKUP_DIR

# Nén thư mục nguồn và lưu vào thư mục backup
tar -czf "$BACKUP_DIR/$FILENAME" "$SOURCE_DIR"

echo "Sao lưu hoàn tất! File được lưu tại: $BACKUP_DIR/$FILENAME"
echo "Liệt kê các file trong thư mục backup:"
ls -lh $BACKUP_DIR
```

## ✍️ Bài tập thực hành (Exercises)

Hãy vận dụng kiến thức đã học để hoàn thành các kịch bản (script) tự động hóa sau đây.

**Bài 1: Script Chào hỏi (Biến và Tham số)**
1.  Viết một script tên `greeting.sh` nhận vào một tham số là tên của bạn.
2.  Script sẽ in ra câu chào: `Chào mừng [tên của bạn] đến với thế giới của Bash Scripting!`
3.  **Nâng cao:** Thêm logic kiểm tra. Nếu không có tham số nào được truyền vào (`$1` rỗng), script sẽ in ra thông báo: `Vui lòng cho tôi biết tên của bạn.` (Gợi ý: dùng `if [ -z "$1" ]`).

**Bài 2: Vòng lặp và Tạo File**
1.  Viết một script `file_creator.sh`.
2.  Script này sử dụng vòng lặp `for` để tạo ra 5 file văn bản có tên là `file1.txt`, `file2.txt`, ..., `file5.txt`.
3.  Bên trong mỗi file, ghi đúng dòng chữ `Đây là file thứ [số thứ tự]`. Ví dụ, `file3.txt` sẽ chứa dòng `Đây là file thứ 3`.

**Bài 3: Cải tiến Script Backup (Ví dụ thực tế)**
1.  Lấy lại script sao lưu tự động từ ví dụ trong bài học.
2.  **Hoàn thành thử thách:** Thêm chức năng vào script để nó tự động **tìm và xóa** các file backup (`.tar.gz`) trong thư mục `BACKUP_DIR` đã được tạo ra **cũ hơn 7 ngày**.
3.  Gợi ý: Sử dụng lệnh `find $BACKUP_DIR -name "backup-*.tar.gz" -mtime +7 -print -delete`. Tùy chọn `-print` sẽ in ra tên file trước khi xóa.
4.  Thêm một dòng `echo` để thông báo về việc dọn dẹp các bản backup cũ.

**Bài 4: Sử dụng Hàm (Functions)**
1.  Viết một script `system_check.sh` có các hàm sau:
    -   `show_uptime()`: Chạy và in ra kết quả của lệnh `uptime`.
    -   `show_disk_usage()`: Chạy và in ra kết quả của lệnh `df -h`.
    -   `show_memory_usage()`: Chạy và in ra kết quả của lệnh `free -h`.
2.  Sau khi định nghĩa các hàm, hãy gọi lần lượt cả 3 hàm trong script, kèm theo một dòng `echo` tiêu đề cho mỗi hàm. Ví dụ: `echo "--- Uptime ---"`, sau đó gọi `show_uptime`.

---

Trong bài tiếp theo, chúng ta sẽ tìm hiểu về các khái niệm mạng máy tính cơ bản, nền tảng để các dịch vụ và máy chủ giao tiếp với nhau.

[Bài trước: Làm chủ Dòng lệnh Linux](../02-linux-cli/) | [Quay lại Mục lục chính](../../README.md) | [Bài tiếp theo: Nhập môn Mạng máy tính](../04-networking-concepts/)