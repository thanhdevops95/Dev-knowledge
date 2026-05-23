# Quiz: Module 01 - LINUX BASICS

> **30 câu trắc nghiệm kiểm tra kiến thức**

---

## 📋 INSTRUCTIONS

- **30 questions** - Multiple choice
- **Time limit:** 45 minutes (recommended)
- **Passing score:** 24/30 (80%)
- **Check answers:** [SOLUTIONS.md](SOLUTIONS.md)

---

## SECTION 1: FILE SYSTEM & NAVIGATION (10 questions)

### Q1: Root directory trong Linux là

A) `C:\`  
B) `/root`  
C) `/`  
D) `/home`

---

### Q2: Lệnh nào hiển thị đường dẫn thư mục hiện tại?

A) `cd`  
B) `dir`  
C) `pwd`  
D) `path`

---

### Q3: Hidden files trong Linux bắt đầu với

A) `~`  
B) `.`  
C) `_`  
D) `#`

---

### Q4: `/etc` directory chứa

A) User home directories  
B) System configuration files  
C) Log files  
D) Temporary files

---

### Q5: Symbol `~` đại diện cho

A) Root directory  
B) Parent directory  
C) Home directory  
D) Current directory

---

### Q6: Lệnh `cd ..` làm gì?

A) Go to root  
B) Go to home  
C) Go up one level  
D) Go to previous directory

---

### Q7: Để list cả hidden files, dùng

A) `ls`  
B) `ls -a`  
C) `ls -h`  
D) `ls -all`

---

### Q8: `/var/log` directory chứa

A) User logs  
B) System and application logs  
C) Boot logs only  
D) Database logs only

---

### Q9: Tạo directory với parent directories

A) `mkdir -p path/to/deep`  
B) `mkdir -r path/to/deep`  
C) `mkdir --all path/to/deep`  
D) `mkpath path/to/deep`

---

### Q10: `/tmp` directory đặc biệt vì

A) Files永久 lưu trữ  
B) Files bị xóa sau restart  
C) Chỉ root write được  
D) Không ai xóa được files

---

## SECTION 2: FILE OPERATIONS (5 questions)

### Q11: Copy file và rename cùng lúc

A) `cp file1 file2 rename`  
B) `cp file1 file2`  
C) `copy file1 to file2`  
D) `mv file1 file2`

---

### Q12: Lệnh nào xóa directory và contents

A) `rmdir folder`  
B) `rm folder`  
C) `rm -r folder`  
D) `delete folder`

---

### Q13: Append text vào file

A) `echo "text" > file`  
B) `echo "text" >> file`  
C) `echo "text" >>> file`  
D) `add "text" file`

---

### Q14: View file real-time khi nó thay đổi

A) `cat -f file.log`  
B) `tail -f file.log`  
C) `watch file.log`  
D) `less -f file.log`

---

### Q15: `touch` command làm gì khi file đã tồn tại?

A) Delete file  
B) Create duplicate  
C) Update timestamp  
D) Error

---

## SECTION 3: PERMISSIONS (7 questions)

### Q16: Permission `-rw-r--r--` nghĩa là

A) Owner: read+write, Group: read, Others: read  
B) Everyone can write  
C) Only owner can access  
D) Everyone can execute

---

### Q17: Octal permission `755` tương đương

A) `rwxr-xr-x`  
B) `rwxrwxrwx`  
C) `rw-r--r--`  
D) `r-xr-xr-x`

---

### Q18: Make file executable

A) `chmod +x file`  
B) `chmod 777 file`  
C) `execute file`  
D) `chmod x file`

---

### Q19: Change file owner

A) `chmod user:group file`  
B) `chown user:group file`  
C) `owner user file`  
D) `change-owner user file`

---

### Q20: Permission `600` best cho

A) Web files  
B) SSH private keys  
C) Executable scripts  
D) Public documents

---

### Q21: `chmod 777 file` means

A) Everyone full access (DANGEROUS!)  
B) Only owner full access  
C) Read-only for everyone  
D) Secure permission

---

### Q22: Recursive permission change

A) `chmod -r 755 folder`  
B) `chmod -R 755 folder`  
C) `chmod -recursive 755 folder`  
D) `chmod 755 folder/*`

---

## SECTION 4: PROCESSES (5 questions)

### Q23: View all processes

A) `ps`  
B) `ps -u`  
C) `ps aux`  
D) `process --all`

---

### Q24: Force kill process

A) `kill PID`  
B) `kill -1 PID`  
C) `kill -9 PID`  
D) `kill -15 PID`

---

### Q25: Restart a service

A) `service restart nginx`  
B) `systemctl restart nginx`  
C) `restart nginx`  
D) Both A and B

---

### Q26: Process state 'Z' means

A) Running  
B) Zombie  
C) Sleeping  
D) Stopped

---

### Q27: Run command in background

A) `command &`  
B) `command -bg`  
C) `bg command`  
D) `background command`

---

## SECTION 5: SEARCH & TEXT (5 questions)

### Q28: Search case-insensitive

A) `grep "error" file`  
B) `grep -i "error" file`  
C) `grep -case "error" file`  
D) `grep --ignore "error" file`

---

### Q29: Count lines matching pattern

A) `grep -n "error" file`  
B) `grep -count "error" file`  
C) `grep -c "error" file`  
D) `grep "error" file | wc`

---

### Q30: Find files modified in last 7 days

A) `find /path -mtime 7`  
B) `find /path -mtime -7`  
C) `find /path -days 7`  
D) `find /path -modified 7`

---

## 📊 SCORING

| Score | Grade | Level |
|-------|-------|-------|
| 27-30 | A | Excellent ⭐⭐⭐ |
| 24-26 | B | Good ⭐⭐ |
| 21-23 | C | Pass ⭐ |
| <21 | F | Review module 📚 |

---

## ✅ AFTER QUIZ

1. Check answers in [SOLUTIONS.md](SOLUTIONS.md)
2. Review questions you got wrong
3. Re-read relevant sections in [README.md](README.md)
4. Retake quiz if score < 24

---

<div align="center">

**Good luck! 🍀**

**Time starts NOW! ⏱️**

</div>
