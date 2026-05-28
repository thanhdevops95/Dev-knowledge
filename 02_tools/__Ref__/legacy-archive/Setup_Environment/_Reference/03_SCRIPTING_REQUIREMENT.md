# Module 03: SHELL & PYTHON SCRIPTING

> **"Automation begins with scripting - đây là siêu năng lực của DevOps"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Viết Bash scripts từ cơ bản đến nâng cao
- ✅ Thành thạo variables, loops, conditions trong Bash
- ✅ Xử lý arguments và user input
- ✅ Text processing với sed, awk, grep
- ✅ Python scripting cơ bản cho DevOps
- ✅ Làm việc với files, JSON, YAML trong Python
- ✅ Tạo automation scripts thực tế
- ✅ Schedule scripts với cron

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| Shell | Shell | Trình thông dịch lệnh |
| Bash | Bourne Again Shell | Shell phổ biến nhất |
| Shebang | Shebang (#!) | Dòng đầu chỉ định interpreter |
| Variable | Variable | Biến lưu trữ giá trị |
| Array | Array | Mảng |
| Loop | Loop | Vòng lặp (for, while) |
| Condition | Conditional | Điều kiện (if, else) |
| Function | Function | Hàm |
| Exit Code | Exit Code | Mã trả về (0=success) |
| Pipe | Pipe (\|) | Nối output → input |
| Redirect | Redirect (\>, \>\>) | Chuyển hướng output |
| Regex | Regular Expression | Biểu thức chính quy |
| Cron | Cron | Scheduler chạy lệnh định kỳ |
| Crontab | Crontab | File cấu hình cron |

---

## ✅ Checklist Labs

### Labs Bash cơ bản

- [ ] Lab 1: Script đầu tiên - Hello World
- [ ] Lab 2: Variables và Environment Variables
- [ ] Lab 3: User input với read
- [ ] Lab 4: Command line arguments ($1, $2, $@, $#)
- [ ] Lab 5: Exit codes và error handling

### Labs Bash control flow

- [ ] Lab 6: If-else conditions
- [ ] Lab 7: Case statements
- [ ] Lab 8: For loops
- [ ] Lab 9: While loops
- [ ] Lab 10: Until loops
- [ ] Lab 11: Break và Continue

### Labs Bash functions & advanced

- [ ] Lab 12: Functions với parameters
- [ ] Lab 13: Local vs Global variables
- [ ] Lab 14: Return values từ functions
- [ ] Lab 15: Arrays trong Bash
- [ ] Lab 16: String manipulation
- [ ] Lab 17: Arithmetic operations
- [ ] Lab 18: Here documents (heredoc)

### Labs Text Processing

- [ ] Lab 19: grep patterns và regex
- [ ] Lab 20: sed - find và replace
- [ ] Lab 21: sed - delete và insert lines
- [ ] Lab 22: awk - column extraction
- [ ] Lab 23: awk - calculations và formatting
- [ ] Lab 24: Combining grep, sed, awk

### Labs Python cho DevOps

- [ ] Lab 25: Python script đầu tiên
- [ ] Lab 26: Làm việc với files
- [ ] Lab 27: JSON parsing và manipulation
- [ ] Lab 28: YAML parsing với PyYAML
- [ ] Lab 29: HTTP requests với requests library
- [ ] Lab 30: subprocess - chạy shell commands từ Python
- [ ] Lab 31: argparse - command line arguments
- [ ] Lab 32: os và shutil - file operations
- [ ] Lab 33: Logging trong Python

### Labs Automation thực tế

- [ ] Lab 34: Script backup files tự động
- [ ] Lab 35: Script health check services
- [ ] Lab 36: Script cleanup old logs
- [ ] Lab 37: Script monitor disk usage
- [ ] Lab 38: Cron job scheduling
- [ ] Lab 39: Script gửi notification (Slack/Email)
- [ ] Lab 40: Script deploy đơn giản

---

## 🚨 Checklist Scenarios

### Scenarios về Bash Scripts

- [ ] Scenario 1: Script chạy manual nhưng fail trong cron
- [ ] Scenario 2: Script fails với "command not found"
- [ ] Scenario 3: Permission denied khi run script
- [ ] Scenario 4: Script chạy sai khi có space trong filename
- [ ] Scenario 5: Script infinite loop - không dừng được
- [ ] Scenario 6: Script fails với special characters in input

### Scenarios về Variables & Environment

- [ ] Scenario 7: Environment variable không set trong script
- [ ] Scenario 8: Variable scope issue trong subshell
- [ ] Scenario 9: Unset variable gây crash

### Scenarios về File Processing

- [ ] Scenario 10: Script xử lý file lớn bị out of memory
- [ ] Scenario 11: Script fails với Unicode characters
- [ ] Scenario 12: Regex quá greedy match sai

### Scenarios về Cron

- [ ] Scenario 13: Cron job không chạy
- [ ] Scenario 14: Cron job chạy nhiều lần
- [ ] Scenario 15: Cron job output không thấy đâu

### Scenarios về Python

- [ ] Scenario 16: ImportError - module not found
- [ ] Scenario 17: JSON decode error
- [ ] Scenario 18: API request timeout
- [ ] Scenario 19: File encoding issues (UTF-8)
- [ ] Scenario 20: Python version mismatch

### Scenarios về Production

- [ ] Scenario 21: Script chạy quá lâu block deployment
- [ ] Scenario 22: Script fail silently không báo lỗi
- [ ] Scenario 23: Race condition khi nhiều script chạy song song
- [ ] Scenario 24: Script modify wrong files do path issue

---

## ⏱️ Thời lượng

**Ước tính:** 6-8 giờ

| Phần | Thời gian |
|------|-----------|
| Bash cơ bản (Labs 1-11) | 2 giờ |
| Bash nâng cao (Labs 12-18) | 1.5 giờ |
| Text processing (Labs 19-24) | 1 giờ |
| Python (Labs 25-33) | 2 giờ |
| Automation (Labs 34-40) | 1.5 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [Bash Scripting Tutorial](https://linuxconfig.org/bash-scripting-tutorial)
- [ShellCheck - Script Linter](https://www.shellcheck.net/)
- [Python for DevOps (Book)](https://www.oreilly.com/library/view/python-for-devops/9781492057680/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
