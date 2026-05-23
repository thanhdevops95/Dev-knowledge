# Lời giải - Bài 2: Làm chủ Dòng lệnh Linux

Chào mừng bạn đến với bài thực hành về dòng lệnh Linux. Trong file này, chúng ta sẽ đi qua từng bước để hoàn thành các yêu cầu của bài học.

Các lệnh dưới đây được thực hiện từ bên trong thư mục `workspare/Exercises01-foundation/02-linux-cli/`.

---

### Bài 1: Điều hướng và Quản lý File

**Mục tiêu:** Tạo ra một cấu trúc thư mục dự án, làm quen với việc tạo, di chuyển, sao chép, và xóa file.

**1. Tạo một thư mục tên là `devops_practice`:**

```bash
mkdir devops_practice
```

-   **Giải thích:** Lệnh `mkdir` (make directory) được dùng để tạo một thư mục mới.

**2. Di chuyển vào bên trong thư mục `devops_practice`:**

```bash
cd devops_practice
```

-   **Giải thích:** Lệnh `cd` (change directory) giúp chúng ta thay đổi thư mục làm việc hiện tại. Từ bây giờ, các lệnh tiếp theo sẽ được thực thi từ bên trong `devops_practice`.

**3. Tạo cây thư mục `project/src`, `project/docs`, `project/tests` chỉ bằng một lệnh:**

```bash
mkdir -p project/{src,docs,tests}
```

-   **Giải thích:**
    -   `-p` (parents): Cờ này cho phép `mkdir` tạo cả thư mục cha (`project`) nếu nó chưa tồn tại.
    -   `{src,docs,tests}`: Đây là một tính năng của shell gọi là "brace expansion", nó sẽ tạo ra 3 thư mục cùng lúc bên trong `project`.

**4. Trong thư mục `project/src`, tạo một file rỗng tên là `main.py`:**

```bash
touch project/src/main.py
```

-   **Giải thích:** `touch` là lệnh dùng để tạo một file trống hoặc cập nhật thời gian sửa đổi của file đã có.

**5. Sao chép file `main.py` vào thư mục `project/tests` với tên mới là `test_main.py`:**

```bash
cp project/src/main.py project/tests/test_main.py
```

-   **Giải thích:** `cp` (copy) sao chép nội dung của file nguồn (`project/src/main.py`) đến một file đích (`project/tests/test_main.py`).

**6. Xóa file `main.py` ở thư mục `src` ban đầu:**

```bash
rm project/src/main.py
```

-   **Giải thích:** `rm` (remove) dùng để xóa file.

**7. Liệt kê toàn bộ các file và thư mục bên trong `project` một cách đệ quy:**

```bash
ls -R project
```

-   **Giải thích:** `ls` là lệnh liệt kê file. Cờ `-R` (recursive) sẽ liệt kê toàn bộ nội dung của các thư mục con bên trong.
-   **Kết quả mong đợi:**
    ```
    project:
    docs	src	tests

    project/docs:

    project/src:

    project/tests:
    test_main.py
    ```

---

### Bài 2: Quyền và Ghi Nội dung File

**Mục tiêu:** Học cách ghi nội dung vào file và quản lý quyền truy cập.

**1. Ghi dòng chữ `print("Hello DevOps")` vào file `project/src/main.py`:**

```bash
echo 'print("Hello DevOps")' > project/src/main.py
```

-   **Giải thích:**
    -   `echo` là lệnh in một chuỗi văn bản ra màn hình.
    -   Toán tử `>` (redirection) chuyển hướng đầu ra của lệnh `echo` và ghi nó vào file `project/src/main.py`. Nếu file đã có nội dung, nó sẽ bị **ghi đè**. Nếu file chưa tồn tại, nó sẽ được tạo mới.

**2. Nối thêm dòng `print("This is my first Python script")` vào cuối file `main.py`:**

```bash
echo 'print("This is my first Python script")' >> project/src/main.py
```

-   **Giải thích:** Toán tử `>>` (append) cũng chuyển hướng đầu ra, nhưng nó sẽ **nối thêm** vào cuối file thay vì ghi đè.

**3. Hiển thị nội dung của file `main.py`:**

```bash
cat project/src/main.py
```

-   **Giải thích:** Lệnh `cat` (concatenate) đọc và hiển thị toàn bộ nội dung của một file ra màn hình.
-   **Kết quả mong đợi:**
    ```
    print("Hello DevOps")
    print("This is my first Python script")
    ```

**4. Cấp quyền thực thi (`x`) cho file `main.py` chỉ cho người sở hữu file:**

```bash
chmod u+x project/src/main.py
```

-   **Giải thích:** `chmod` (change mode) thay đổi quyền của file.
    -   `u` (user): Áp dụng cho người sở hữu.
    -   `+` (add): Thêm quyền.
    -   `x` (execute): Quyền thực thi.

**5. Chạy lệnh `ls -l project/src` để xác nhận quyền:**

```bash
ls -l project/src
```

-   **Giải thích:** `ls -l` hiển thị danh sách file ở định dạng dài, bao gồm cả thông tin về quyền.
-   **Kết quả mong đợi:** Bạn sẽ thấy chuỗi quyền bắt đầu bằng `-rwx------` hoặc tương tự, cho thấy chủ sở hữu đã có quyền `x`.

---

### Bài 3: Tìm kiếm và Lọc

**Mục tiêu:** Sử dụng các công cụ mạnh mẽ để tìm kiếm file và nội dung bên trong file.

**1. Tìm tất cả các file có đuôi `.py` bên trong thư mục `project`:**

```bash
find project -name "*.py"
```

-   **Giải thích:**
    -   `find`: Lệnh tìm kiếm file/thư mục.
    -   `project`: Đường dẫn bắt đầu tìm kiếm.
    -   `-name "*.py"`: Điều kiện tìm kiếm. `-name` là tìm theo tên, và `*.py` là mẫu (pattern) cho tất cả các file kết thúc bằng `.py`.

**2. Tạo file log giả `app.log` và ghi nội dung:
(File này đã tồn tại, nhưng đây là lệnh để tạo ra nó)**

```bash
echo -e "INFO: Application started\nDEBUG: Connecting to database\nERROR: Failed to connect to database\nINFO: Shutting down" > app.log
```
- **Giải thích:** Cờ `-e` cho phép `echo` diễn giải các ký tự đặc biệt như `\n` (xuống dòng).

**3. Sử dụng `grep` để tìm dòng chứa từ `ERROR` trong file `app.log`:**

```bash
grep "ERROR" app.log
```

-   **Giải thích:** `grep` là công cụ tìm kiếm văn bản cực kỳ mạnh mẽ. Nó sẽ quét qua file `app.log` và in ra mọi dòng có chứa chuỗi "ERROR".
-   **Kết quả mong đợi:**
    ```
    ERROR: Failed to connect to database
    ```

---

### Bài 4: Kết hợp Lệnh (Pipes)

**Mục tiêu:** Hiểu sức mạnh của ống dẫn `|` để kết hợp các lệnh nhỏ thành một quy trình xử lý mạnh mẽ.

**1. Liệt kê tất cả tiến trình và lọc ra các tiến trình `bash`:**

```bash
ps aux | grep 'bash'
```

-   **Giải thích:**
    -   `ps aux`: Lệnh này liệt kê tất cả (`a`) các tiến trình đang chạy trên hệ thống, bao gồm cả của người dùng khác (`x`) và hiển thị thông tin chi tiết (`u`).
    -   `|` (pipe): Ống dẫn này lấy toàn bộ đầu ra (output) của lệnh `ps aux` và chuyển nó làm đầu vào (input) cho lệnh tiếp theo.
    -   `grep 'bash'`: `grep` nhận đầu vào từ `ps aux` và chỉ lọc ra những dòng có chứa từ `bash`.

**2. Liệt kê các file cấu hình `.conf` trong thư mục `/etc`:**

```bash
ls -l /etc | grep ".conf"
```

-   **Giải thích:** Tương tự như trên, lệnh này lấy danh sách tất cả các file/thư mục trong `/etc` và chỉ hiển thị những dòng có chứa chuỗi `.conf`. Đây là một cách nhanh để lọc ra các file cấu hình.

Chúc mừng bạn đã hoàn thành bài thực hành! Hãy thử tự mình gõ lại các lệnh này để ghi nhớ chúng tốt hơn.