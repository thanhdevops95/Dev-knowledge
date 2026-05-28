# Bài 2: Làm chủ Dòng lệnh Linux

## 🎯 Mục tiêu bài học

-   Thành thạo các lệnh cơ bản để điều hướng và quản lý hệ thống file Linux.
-   Hiểu và sử dụng được các lệnh để quản lý quyền, tiến trình, và người dùng.
-   Nắm vững các công cụ dòng lệnh để tìm kiếm, lọc văn bản và kiểm tra mạng.
-   Hiểu được sức mạnh của `pipe` (|) trong việc kết hợp các lệnh.

## 📖 Nội dung chính

1.  **Cấu trúc Hệ thống File:** `pwd`, `ls`, `cd`.
2.  **Quản lý File và Thư mục:** `touch`, `mkdir`, `cp`, `mv`, `rm`, `cat`, `less`.
3.  **Quản lý Quyền:** `chmod`, `chown`, và ý nghĩa của các quyền `rwx`.
4.  **Tìm kiếm và Lọc văn bản:** `grep`, `find`, và ống dẫn `|`.
5.  **Quản lý Tiến trình:** `ps`, `top`, `htop`, `kill`.
6.  **Các lệnh Mạng cơ bản:** `ping`, `curl`, `wget`, `netstat`, `ip addr`.
7.  **Quản lý Người dùng và Đặc quyền:** `whoami`, `sudo`.

## 🛠️ Công cụ & Lý thuyết

-   **Shells:** <u>Bash</u>, Zsh, Fish.
-   **Terminal Multiplexers:** tmux, screen.
-   **Công cụ dòng lệnh:** `grep`, `awk`, `sed`, `find`.

---

# Nội dung chi tiết - Bài 2: Làm chủ Dòng lệnh Linux

Đối với một Kỹ sư DevOps, dòng lệnh Linux (Command Line Interface - CLI) không chỉ là một công cụ, mà là môi trường làm việc chính. Hầu hết các máy chủ trên thế giới đều chạy Linux, và việc thành thạo CLI sẽ giúp bạn quản lý, tự động hóa và gỡ lỗi hệ thống một cách hiệu quả.

---

### 1. Cấu trúc Hệ thống File và Điều hướng

Hệ thống file của Linux được tổ chức theo một cây thư mục bắt đầu từ gốc (`/`).

-   `pwd` (Print Working Directory): Hiển thị thư mục hiện tại bạn đang đứng.
-   `ls` (List): Liệt kê các file và thư mục trong thư mục hiện tại.
    -   `ls -l`: Hiển thị chi tiết (quyền, chủ sở hữu, kích thước...).
    -   `ls -a`: Hiển thị cả các file/thư mục ẩn (bắt đầu bằng dấu `.`).
-   `cd` (Change Directory): Thay đổi thư mục làm việc.
    -   `cd /home/user/documents`: Đi đến một đường dẫn tuyệt đối.
    -   `cd ../project`: Đi lên một cấp và vào thư mục `project`.
    -   `cd ~` hoặc `cd`: Quay về thư mục nhà của người dùng.

---

### 2. Quản lý File và Thư mục

-   `touch <tên_file>`: Tạo một file rỗng.
-   `mkdir <tên_thư_mục>`: Tạo một thư mục mới.
-   `cp <nguồn> <đích>` (Copy): Sao chép file hoặc thư mục.
    -   `cp file1.txt file2.txt`
    -   `cp -r dir1/ dir2/` (sao chép đệ quy cả thư mục).
-   `mv <nguồn> <đích>` (Move): Di chuyển hoặc đổi tên file/thư mục.
    -   `mv old_name.txt new_name.txt` (đổi tên).
    -   `mv file.txt /tmp/` (di chuyển).
-   `rm <tên_file>` (Remove): Xóa file. **Cẩn thận, lệnh này không có thùng rác!**
    -   `rm -r <tên_thư_mục>`: Xóa thư mục và toàn bộ nội dung bên trong.
    -   `rm -rf <tên_thư_mục>`: Xóa mà không cần hỏi xác nhận (cực kỳ nguy hiểm).
-   `cat <tên_file>`: Đọc và hiển thị toàn bộ nội dung của file.
-   `less <tên_file>`: Đọc nội dung file theo từng trang (nhấn `q` để thoát).

---

### 3. Quản lý Quyền (Permissions)

Khi chạy `ls -l`, bạn sẽ thấy một chuỗi như `-rwxr-xr--`. Đây là quyền truy cập, gồm 3 nhóm (chủ sở hữu, nhóm, những người khác), mỗi nhóm có 3 quyền: `r` (read), `w` (write), `x` (execute).

-   `chmod` (Change Mode): Thay đổi quyền của file/thư mục.
    -   `chmod u+x script.sh`: Thêm (`+`) quyền thực thi (`x`) cho người dùng (`u`).
    -   `chmod 755 script.sh`: Gán quyền bằng số (octal). `7` là `rwx`, `5` là `r-x`. Đây là quyền phổ biến cho các file script.
-   `chown` (Change Owner): Thay đổi chủ sở hữu và nhóm sở hữu của file/thư mục.
    -   `chown new_user:new_group file.txt`

---

### 4. Tìm kiếm và Lọc văn bản

-   `grep <chuỗi> <tên_file>` (Global regular expression print): Tìm kiếm một chuỗi văn bản bên trong file.
    -   `grep "error" /var/log/app.log`
-   `find <đường_dẫn> -name "<tên_file>"`: Tìm kiếm file/thư mục.
    -   `find /etc -name "*.conf"`
-   **Ống dẫn `|` (Pipe):** Đây là một khái niệm cực kỳ mạnh mẽ, cho phép bạn lấy đầu ra của lệnh này làm đầu vào cho lệnh khác.
    -   `cat app.log | grep "ERROR"`: Lọc các dòng có chữ "ERROR" từ file log.

---

### 5. Quản lý Tiến trình (Process Management)

-   `ps aux`: Liệt kê tất cả các tiến trình đang chạy trên hệ thống.
-   `top` hoặc `htop` (cần cài thêm): Hiển thị các tiến trình đang chạy một cách trực quan và cập nhật liên tục, sắp xếp theo CPU hoặc RAM sử dụng.
-   `kill <PID>`: Gửi tín hiệu để dừng một tiến trình.
    -   `kill 1234` (gửi tín hiệu mặc định TERM).
    -   `kill -9 1234` (gửi tín hiệu KILL, buộc dừng tiến trình ngay lập tức).

---

### 6. Các lệnh Mạng cơ bản

-   `ping <host>`: Kiểm tra kết nối mạng tới một máy chủ.
-   `curl <URL>`: Lấy nội dung từ một URL. Rất hữu ích để kiểm tra API.
    -   `curl https://api.github.com`
-   `wget <URL>`: Tải file từ một URL.
-   `netstat -tuln` hoặc `ss -tuln`: Liệt kê các cổng (port) đang mở và lắng nghe trên máy chủ.
-   `ip addr` hoặc `ifconfig`: Hiển thị thông tin cấu hình mạng của máy chủ (địa chỉ IP, ...).

---

### 7. Quản lý Người dùng và Đặc quyền

-   `whoami`: Cho biết bạn đang đăng nhập với tư cách người dùng nào.
-   `sudo <lệnh>` (Superuser Do): Thực thi một lệnh với quyền của người dùng `root` (quản trị viên cao nhất). Đây là lệnh bạn sẽ dùng rất thường xuyên.
-   `useradd <tên_người_dùng>`: Tạo một người dùng mới.
-   `passwd <tên_người_dùng>`: Đặt hoặc thay đổi mật khẩu cho người dùng.

---

## ✍️ Bài tập thực hành (Exercises)

Cách duy nhất để làm chủ dòng lệnh là thực hành. Hãy thử kết nối vào một máy chủ Linux (hoặc sử dụng terminal trên máy Mac/Linux của bạn) và hoàn thành các bài tập sau.

**Bài 1: Điều hướng và Quản lý File**
1.  Tạo một thư mục tên là `devops_practice`.
2.  Di chuyển vào bên trong thư mục `devops_practice`.
3.  Tạo cây thư mục sau chỉ bằng một lệnh: `project/src`, `project/docs`, `project/tests`.
4.  Trong thư mục `project/src`, tạo một file rỗng tên là `main.py`.
5.  Sao chép file `main.py` vào thư mục `project/tests` với tên mới là `test_main.py`.
6.  Xóa file `main.py` ở thư mục `src` ban đầu.
7.  Liệt kê toàn bộ các file và thư mục bên trong `project` một cách đệ quy (hiển thị cả các thư mục con).

**Bài 2: Quyền và Ghi Nội dung File**
1.  Sử dụng lệnh `echo` và toán tử chuyển hướng `>` để ghi dòng chữ `print("Hello DevOps")` vào file `project/src/main.py`.
2.  Nối thêm (append) dòng `print("This is my first Python script")` vào cuối file `main.py` mà không xóa nội dung cũ (sử dụng `>>`).
3.  Hiển thị nội dung của file `main.py` để kiểm tra kết quả.
4.  Cấp quyền thực thi (`x`) cho file `main.py` chỉ cho người sở hữu file.
5.  Chạy lệnh `ls -l project/src` để xác nhận lại quyền của file đã được thay đổi đúng hay chưa.

**Bài 3: Tìm kiếm và Lọc**
1.  Sử dụng lệnh `find` để tìm tất cả các file có đuôi `.py` bên trong thư mục `project`.
2.  Tạo một file log giả `app.log` trong thư mục `devops_practice` và ghi vào đó vài dòng, trong đó có một dòng chứa từ `ERROR`.
3.  Sử dụng `grep` để tìm và hiển thị dòng chứa từ `ERROR` trong file `app.log`.

**Bài 4: Kết hợp Lệnh (Pipes)**
1.  Chạy lệnh `ps aux` để liệt kê tất cả tiến trình.
2.  Sử dụng ống dẫn `|` và lệnh `grep` để lọc kết quả từ `ps aux` và chỉ hiển thị các tiến trình liên quan đến `bash` (hoặc `zsh` nếu bạn đang dùng Z-shell).
3.  Sử dụng `ls -l /etc | grep ".conf"` để liệt kê tất cả các file cấu hình (đuôi `.conf`) trong thư mục `/etc`.

Trong bài học tiếp theo, chúng ta sẽ học cách tự động hóa các chuỗi lệnh như thế này bằng **Bash Scripting**.

[Quay lại Mục lục chính](../../README.md) | [Bài tiếp theo: Kỹ năng Viết Script](../03-scripting-for-automation/)
