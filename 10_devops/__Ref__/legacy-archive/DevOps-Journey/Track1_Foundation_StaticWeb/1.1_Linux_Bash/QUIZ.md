# 📝 Quiz - Linux & Bash

> **Knowledge Check for Linux and Bash Scripting**
>
> *Kiểm tra kiến thức về Linux và Bash scripting*

---

## Instructions (Hướng dẫn)

- **Total Questions (Tổng số câu hỏi)**: 20
- **Duration (Thời gian)**: 15-20 mins (15-20 phút)
- **Answers (Đáp án)**: At the bottom of the page (Cuối trang)

---

## Part 1: Linux Basics (Phần 1: Linux Cơ bản) - 10 questions

### Question 1: Root Directory (Câu 1: Thư mục gốc)

In Linux, what symbol represents the root directory?
*(Trong Linux, thư mục gốc (root directory) được ký hiệu là gì?)*

- A) `~`
- B) `/`
- C) `\`
- D) `$`

---

### Question 2: Home Directory (Câu 2: Thư mục cá nhân)

Which command takes you to the current user's home directory?
*(Lệnh nào đưa bạn về home directory của user hiện tại?)*

- A) `cd home`
- B) `cd /`
- C) `cd ~`
- D) `cd ..`

---

### Question 3: Listing Hidden Files (Câu 3: Liệt kê files ẩn)

Which command displays all files including hidden files (starting with a dot)?
*(Lệnh nào hiển thị tất cả files kể cả hidden files (bắt đầu bằng dấu chấm)?)*

- A) `ls -l`
- B) `ls -h`
- C) `ls -a`
- D) `ls -r`

---

### Question 4: Recursive Directory Creation (Câu 4: Tạo thư mục lồng nhau)

To create a directory structure `parent/child/grandchild` when parent directories don't exist, which command is used?
*(Để tạo cấu trúc thư mục `parent/child/grandchild` khi các thư mục cha chưa tồn tại, dùng lệnh gì?)*

- A) `mkdir parent/child/grandchild`
- B) `mkdir -r parent/child/grandchild`
- C) `mkdir -p parent/child/grandchild`
- D) `mkdir --recursive parent/child/grandchild`

---

### Question 5: Viewing File Endings (Câu 5: Xem cuối file)

Which command displays the last 10 lines of a file?
*(Lệnh nào hiển thị 10 dòng cuối cùng của một file?)*

- A) `head file.txt`
- B) `tail file.txt`
- C) `cat file.txt`
- D) `less file.txt`

---

### Question 6: Searching in Files (Câu 6: Tìm kiếm trong file)

Which command finds all lines containing the word "error" in `log.txt`, case-insensitively?
*(Lệnh nào tìm tất cả các dòng chứa từ "error" trong file `log.txt`, không phân biệt hoa thường?)*

- A) `grep error log.txt`
- B) `grep -i error log.txt`
- C) `find error log.txt`
- D) `search -i error log.txt`

---

### Question 7: Permission Numbers (Câu 7: Chỉ số quyền hạn)

The permission `rwxr-xr--` is equivalent to which octal number?
*(Permission `rwxr-xr--` tương đương với số octal nào?)*

- A) 644
- B) 755
- C) 754
- D) 777

---

### Question 8: Adding Execute Permission (Câu 8: Thêm quyền thực thi)

Which command adds execute permission for the owner of `script.sh`?
*(Lệnh nào thêm quyền execute cho owner của file `script.sh`?)*

- A) `chmod +x script.sh`
- B) `chmod u+x script.sh`
- C) `chmod 755 script.sh`
- D) All of the above (Tất cả đều đúng)

---

### Question 9: Process Management (Câu 9: Quản lý tiến trình)

Which command stops (force kill) a process with PID 1234?
*(Lệnh nào dừng (force kill) process có PID 1234?)*

- A) `kill 1234`
- B) `kill -9 1234`
- C) `stop 1234`
- D) `terminate 1234`

---

### Question 10: Package management (Câu 10: Quản lý gói)

On Ubuntu/Debian, which command installs the `nginx` package?
*(Trên Ubuntu/Debian, lệnh nào cài đặt package `nginx`?)*

- A) `apt nginx install`
- B) `install apt nginx`
- C) `sudo apt install nginx`
- D) `sudo yum install nginx`

---

## Part 2: Bash Scripting (Phần 2: Bash Scripting) - 10 questions

### Question 11: Shebang (Câu 11: Dòng Shebang)

What should be the first line of a bash script?
*(Dòng đầu tiên của bash script nên là gì?)*

- A) `#/bin/bash`
- B) `#!/bin/bash`
- C) `//bin/bash`
- D) `@!/bin/bash`

---

### Question 12: Bash Variables (Câu 12: Biến trong Bash)

What is the correct way to assign a value to a variable in Bash?
*(Cách nào đúng để gán giá trị cho biến trong Bash?)*

- A) `NAME = "DevOps"`
- B) `NAME="DevOps"`
- C) `$NAME="DevOps"`
- D) `set NAME="DevOps"`

---

### Question 13: Using Variables (Câu 13: Sử dụng biến)

To print the value of the variable `NAME`, which syntax is used?
*(Để in giá trị của biến `NAME`, dùng cú pháp nào?)*

- A) `echo NAME`
- B) `echo $NAME`
- C) `echo %NAME%`
- D) `echo ${NAME}`
- E) B and D are correct (B và D đều đúng)

---

### Question 14: Numeric Comparison (Câu 14: So sánh số)

In Bash, which operator is used to check if number A is greater than number B?
*(Trong Bash, operator nào dùng để kiểm tra số A lớn hơn số B?)*

- A) `$A > $B`
- B) `$A -gt $B`
- C) `$A -greater $B`
- D) `$A == $B`

---

### Question 15: File Existence Check (Câu 15: Kiểm tra file tồn tại)

In an `if` condition, which flag checks if a file exists?
*(Trong điều kiện if, flag nào kiểm tra file có tồn tại không?)*

- A) `[ -e file.txt ]`
- B) `[ -f file.txt ]`
- C) `[ -d file.txt ]`
- D) A and B are correct (A và B đều đúng)

---

### Question 16: For Loop (Câu 16: Vòng lặp For)

What does the following loop print?
*(Vòng lặp sau in ra gì?)*

```bash
for i in 1 2 3; do
    echo $i
done
```

- A) `1 2 3` (on one line)
- B) `123`
- C) Each number on a new line (Mỗi số trên 1 dòng)
- D) Syntax Error (Lỗi cú pháp)

---

### Question 17: Command Substitution (Câu 17: Thay thế lệnh)

What is the CORRECT syntax to assign a command's output to a variable?
*(Cú pháp nào ĐÚNG để gán output của lệnh vào biến?)*

- A) `DATE=date`
- B) `DATE=$(date)`
- C) `DATE=${date}`
- D) `DATE=$[date]`

---

### Question 18: Pipes (Câu 18: Đường ống)

What does the command `ps aux | grep nginx` do?
*(Lệnh `ps aux | grep nginx` làm gì?)*

- A) Lists all processes named nginx (Liệt kê processes tên nginx)
- B) Runs ps and grep concurrently (Chạy ps và grep đồng thời)
- C) Takes `ps aux` output and finds lines containing "nginx" (Lấy output của `ps aux` và tìm "nginx")
- D) Deletes nginx process (Xóa process nginx)

---

### Question 19: Output Redirection (Câu 19: Chuyển hướng đầu ra)

How does `echo "Hello" >> file.txt` differ from `echo "Hello" > file.txt`?
*(Lệnh `echo "Hello" >> file.txt` khác với `echo "Hello" > file.txt` như thế nào?)*

- A) No difference (Không khác gì)
- B) `>>` appends, `>` overwrites (`>>` ghi thêm, `>` ghi đè)
- C) `>>` writes to stderr, `>` to stdout
- D) `>>` creates new file, `>` overwrites

---

### Question 20: Exit Code (Câu 20: Mã thoát)

In Bash, which exit code typically signifies a successful command?
*(Trong Bash, exit code nào thường báo hiệu command thành công?)*

- A) 1
- B) -1
- C) 0
- D) 255

---

## 📋 Answers (Đáp án)

<details>
<summary>Click to view answers (Click để xem đáp án)</summary>

### Part 1: Linux Basics (Phần 1: Linux Cơ bản)

| Question | Answer | Explanation (Giải thích) |
|----------|--------|--------------------------|
| 1 | **B** | `/` is the root directory in Linux (`/` là thư mục gốc) |
| 2 | **C** | `~` is a shortcut for the home directory (`~` là phím tắt cho thư mục home) |
| 3 | **C** | `-a` (all) shows hidden files (`-a` hiển thị tất cả files ẩn) |
| 4 | **C** | `-p` (parents) creates parent directories if missing (`-p` tạo thư mục cha nếu chưa có) |
| 5 | **B** | `tail` shows the end of a file (`tail` hiển thị phần cuối file) |
| 6 | **B** | `-i` (ignore case) is for case-insensitive search (`-i` tìm kiếm không phân biệt hoa thường) |
| 7 | **C** | rwx=7, r-x=5, r--=4 → 754 |
| 8 | **D** | All 3 ways are valid to add execute permission (Cả 3 cách đều đúng) |
| 9 | **B** | `-9` is the SIGKILL signal (force) (`-9` là tín hiệu SIGKILL để cưỡng ép dừng) |
| 10 | **C** | Ubuntu/Debian uses `apt` (Ubuntu/Debian sử dụng `apt`) |

### Part 2: Bash Scripting (Phần 2: Bash Scripting)

| Question | Answer | Explanation (Giải thích) |
|----------|--------|--------------------------|
| 11 | **B** | `#!` (shebang) + interpreter path (Shebang + đường dẫn script) |
| 12 | **B** | NO spaces around `=` (KHÔNG có khoảng cách quanh dấu `=`) |
| 13 | **E** | Both `$NAME` and `${NAME}` are valid (Cả 2 cách đều đúng) |
| 14 | **B** | `-gt` (greater than) for numeric comparison (`-gt` dùng cho so sánh số) |
| 15 | **D** | `-e` (exist) and `-f` (regular file) both check existence (Cả 2 đều check tồn tại) |
| 16 | **C** | `echo` adds a newline by default (`echo` mặc định xuống dòng) |
| 17 | **B** | `$()` is for command substitution (`$()` dùng để thay thế lệnh) |
| 18 | **C** | Pipe (`|`) passes output as input (Pipe truyền output làm input cho lệnh sau) |
| 19 | **B** | `>>` appends, `>` overwrites (`>>` ghi thêm, `>` ghi đè) |
| 20 | **C** | 0 = success, non-zero = error (0 là thành công, khác 0 là lỗi) |

### Scoring (Điểm số)

- **18-20 correct**: Excellent! ⭐⭐⭐ (Xuất sắc!)
- **14-17 correct**: Good! Keep it up ⭐⭐ (Tốt!)
- **10-13 correct**: Needs more review ⭐ (Cần ôn tập thêm)
- **< 10 correct**: Please re-read README.md (Hãy đọc lại file hướng dẫn)

</details>

---

## 🔗 Navigation (Điều hướng)

[⬅️ LABS](./LABS.md) | [README](./README.md) | [EXERCISES ➡️](./EXERCISES.md)

---

*Last Updated: 2026-01-16*
