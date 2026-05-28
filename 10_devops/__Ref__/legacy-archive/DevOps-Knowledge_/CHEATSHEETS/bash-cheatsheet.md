# Bash Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Bash scripting syntax and commands for quick reference -- Cú pháp và lệnh Bash scripting để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [Script Basics](#script-basics) -- Script Cơ bản
- [Variables](#variables) -- Biến
- [Strings](#strings) -- Chuỗi
- [Arrays](#arrays) -- Mảng
- [Conditionals](#conditionals) -- Điều kiện
- [Loops](#loops) -- Vòng lặp
- [Functions](#functions) -- Hàm
- [Input/Output](#inputoutput) -- Input/Output
- [File Operations](#file-operations) -- Thao tác File
- [Common Patterns](#common-patterns) -- Patterns Thường dùng

## <a id="script-basics"></a> Script Basics -- Script Cơ bản

```bash
#!/bin/bash
# Shebang line - specifies interpreter -- Dòng shebang - chỉ định interpreter

# Comments -- Chú thích
# This is a single line comment -- Đây là chú thích một dòng

: '
This is a
multi-line comment
-- Đây là chú thích nhiều dòng
'

# Make script executable -- Làm script có thể thực thi
chmod +x script.sh

# Run script -- Chạy script
./script.sh
bash script.sh
source script.sh              # Run in current shell -- Chạy trong shell hiện tại

# Exit codes -- Mã thoát
exit 0                        # Success -- Thành công
exit 1                        # General error -- Lỗi chung
echo $?                       # Last exit code -- Mã thoát cuối

# Set options -- Đặt options
set -e                        # Exit on error -- Thoát khi lỗi
set -x                        # Debug mode -- Chế độ debug
set -u                        # Error on undefined variable -- Lỗi khi biến chưa định nghĩa
set -o pipefail               # Pipe fail on first error -- Pipe fail ở lỗi đầu tiên
```

## <a id="variables"></a> Variables -- Biến

```bash
# Variable assignment -- Gán biến
name="John"                   # String (no spaces around =) -- Chuỗi (không có khoảng trắng quanh =)
age=25                        # Number -- Số
readonly PI=3.14              # Constant -- Hằng số

# Using variables -- Sử dụng biến
echo $name                    # Simple usage -- Sử dụng đơn giản
echo ${name}                  # Explicit form -- Dạng tường minh
echo "${name} is ${age}"      # In string -- Trong chuỗi

# Special variables -- Biến đặc biệt
$0                            # Script name -- Tên script
$1, $2, ...                   # Positional parameters -- Tham số vị trí
$#                            # Number of arguments -- Số lượng tham số
$@                            # All arguments (separate) -- Tất cả tham số (riêng biệt)
$*                            # All arguments (single string) -- Tất cả tham số (một chuỗi)
$$                            # Current PID -- PID hiện tại
$!                            # Last background PID -- PID nền cuối
$?                            # Last exit code -- Mã thoát cuối

# Default values -- Giá trị mặc định
${var:-default}               # Use default if unset -- Dùng mặc định nếu chưa đặt
${var:=default}               # Assign default if unset -- Gán mặc định nếu chưa đặt
${var:+value}                 # Use value if set -- Dùng value nếu đã đặt
${var:?error}                 # Error if unset -- Lỗi nếu chưa đặt

# Command substitution -- Thay thế lệnh
date=$(date +%Y-%m-%d)        # Modern syntax -- Cú pháp hiện đại
date=`date +%Y-%m-%d`         # Legacy syntax -- Cú pháp cũ

# Arithmetic -- Số học
result=$((5 + 3))             # Addition -- Cộng
result=$((10 - 2))            # Subtraction -- Trừ
result=$((4 * 3))             # Multiplication -- Nhân
result=$((20 / 4))            # Division -- Chia
result=$((10 % 3))            # Modulo -- Chia lấy dư
((count++))                   # Increment -- Tăng
((count--))                   # Decrement -- Giảm
```

## <a id="strings"></a> Strings -- Chuỗi

```bash
# String operations -- Thao tác chuỗi
str="Hello World"

${#str}                       # Length: 11 -- Độ dài: 11
${str:0:5}                    # Substring: "Hello" -- Chuỗi con: "Hello"
${str:6}                      # From position 6: "World" -- Từ vị trí 6: "World"
${str: -5}                    # Last 5 chars: "World" -- 5 ký tự cuối: "World"

# String replacement -- Thay thế chuỗi
${str/World/Everyone}         # Replace first: "Hello Everyone" -- Thay thế đầu tiên
${str//o/0}                   # Replace all: "Hell0 W0rld" -- Thay thế tất cả
${str/#Hello/Hi}              # Replace at start -- Thay thế ở đầu
${str/%World/Universe}        # Replace at end -- Thay thế ở cuối

# Case conversion -- Chuyển đổi chữ hoa/thường
${str^^}                      # Uppercase: "HELLO WORLD" -- Chữ hoa
${str,,}                      # Lowercase: "hello world" -- Chữ thường
${str^}                       # First char uppercase -- Ký tự đầu viết hoa

# Remove pattern -- Xóa pattern
file="/path/to/file.txt"
${file#*/}                    # Remove shortest from start: "path/to/file.txt" -- Xóa ngắn nhất từ đầu
${file##*/}                   # Remove longest from start: "file.txt" -- Xóa dài nhất từ đầu
${file%.*}                    # Remove shortest from end: "/path/to/file" -- Xóa ngắn nhất từ cuối
${file%%/*}                   # Remove longest from end: "" -- Xóa dài nhất từ cuối
```

## <a id="arrays"></a> Arrays -- Mảng

```bash
# Indexed arrays -- Mảng indexed
arr=(one two three)           # Declare array -- Khai báo mảng
arr[3]="four"                 # Add element -- Thêm phần tử

${arr[0]}                     # First element: "one" -- Phần tử đầu: "one"
${arr[@]}                     # All elements -- Tất cả phần tử
${arr[*]}                     # All as single string -- Tất cả như một chuỗi
${#arr[@]}                    # Array length: 4 -- Độ dài mảng: 4
${!arr[@]}                    # All indices: 0 1 2 3 -- Tất cả chỉ số

# Array operations -- Thao tác mảng
arr+=(five)                   # Append -- Thêm vào cuối
unset arr[2]                  # Remove element -- Xóa phần tử
arr=("${arr[@]}" "new")       # Append to end -- Thêm vào cuối

# Loop through array -- Lặp qua mảng
for item in "${arr[@]}"; do
    echo "$item"
done

# Associative arrays (bash 4+) -- Mảng kết hợp (bash 4+)
declare -A assoc              # Declare associative array -- Khai báo mảng kết hợp
assoc[name]="John"
assoc[age]=25
echo ${assoc[name]}           # Access by key -- Truy cập theo key
echo ${!assoc[@]}             # All keys -- Tất cả keys
```

## <a id="conditionals"></a> Conditionals -- Điều kiện

```bash
# If statement -- Câu lệnh if
if [ condition ]; then
    commands
elif [ condition ]; then
    commands
else
    commands
fi

# Test operators -- Các toán tử kiểm tra
# String comparison -- So sánh chuỗi
[ "$a" = "$b" ]               # Equal -- Bằng
[ "$a" != "$b" ]              # Not equal -- Không bằng
[ -z "$a" ]                   # Empty -- Rỗng
[ -n "$a" ]                   # Not empty -- Không rỗng

# Numeric comparison -- So sánh số
[ "$a" -eq "$b" ]             # Equal -- Bằng
[ "$a" -ne "$b" ]             # Not equal -- Không bằng
[ "$a" -lt "$b" ]             # Less than -- Nhỏ hơn
[ "$a" -le "$b" ]             # Less than or equal -- Nhỏ hơn hoặc bằng
[ "$a" -gt "$b" ]             # Greater than -- Lớn hơn
[ "$a" -ge "$b" ]             # Greater than or equal -- Lớn hơn hoặc bằng

# File tests -- Kiểm tra file
[ -e "$file" ]                # Exists -- Tồn tại
[ -f "$file" ]                # Is file -- Là file
[ -d "$file" ]                # Is directory -- Là thư mục
[ -r "$file" ]                # Is readable -- Có thể đọc
[ -w "$file" ]                # Is writable -- Có thể ghi
[ -x "$file" ]                # Is executable -- Có thể thực thi
[ -s "$file" ]                # Not empty -- Không rỗng

# Logical operators -- Toán tử logic
[ condition1 ] && [ condition2 ]  # AND
[ condition1 ] || [ condition2 ]  # OR
[ ! condition ]                   # NOT

# Extended test [[ ]] -- Test mở rộng [[ ]]
[[ "$str" =~ regex ]]         # Regex match -- Khớp regex
[[ "$str" == pattern* ]]      # Pattern match -- Khớp pattern

# Case statement -- Câu lệnh case
case "$var" in
    pattern1)
        commands
        ;;
    pattern2|pattern3)
        commands
        ;;
    *)
        default commands
        ;;
esac
```

## <a id="loops"></a> Loops -- Vòng lặp

```bash
# For loop -- Vòng lặp for
for i in 1 2 3 4 5; do
    echo "$i"
done

for i in {1..10}; do          # Range -- Phạm vi
    echo "$i"
done

for i in {0..20..2}; do       # Range with step -- Phạm vi với bước
    echo "$i"
done

for file in *.txt; do         # Glob pattern -- Pattern glob
    echo "$file"
done

for ((i=0; i<10; i++)); do    # C-style loop -- Vòng lặp kiểu C
    echo "$i"
done

# While loop -- Vòng lặp while
while [ condition ]; do
    commands
done

while read line; do           # Read file line by line -- Đọc file từng dòng
    echo "$line"
done < file.txt

# Until loop -- Vòng lặp until
until [ condition ]; do
    commands
done

# Loop control -- Điều khiển vòng lặp
break                         # Exit loop -- Thoát vòng lặp
continue                      # Skip iteration -- Bỏ qua vòng lặp
break 2                       # Break outer loop -- Thoát vòng lặp ngoài
```

## <a id="functions"></a> Functions -- Hàm

```bash
# Function definition -- Định nghĩa hàm
function greet() {
    echo "Hello, $1!"
}

# Alternative syntax -- Cú pháp thay thế
greet() {
    echo "Hello, $1!"
}

# Call function -- Gọi hàm
greet "World"                 # Output: Hello, World! -- Xuất: Hello, World!

# Function with return -- Hàm với return
add() {
    local result=$(($1 + $2)) # Local variable -- Biến local
    echo $result              # Return via stdout -- Trả về qua stdout
}
sum=$(add 5 3)                # Capture output -- Bắt output

# Return status -- Trạng thái return
check_file() {
    if [ -f "$1" ]; then
        return 0              # Success -- Thành công
    else
        return 1              # Failure -- Thất bại
    fi
}

if check_file "file.txt"; then
    echo "File exists -- File tồn tại"
fi

# Function arguments -- Tham số hàm
my_func() {
    echo "Function name: $0"  # Script name -- Tên script
    echo "First arg: $1"      # First argument -- Tham số đầu
    echo "All args: $@"       # All arguments -- Tất cả tham số
    echo "Arg count: $#"      # Number of arguments -- Số lượng tham số
}
```

## <a id="inputoutput"></a> Input/Output -- Input/Output

```bash
# Read input -- Đọc input
read name                     # Read into variable -- Đọc vào biến
read -p "Enter name: " name   # With prompt -- Với prompt
read -s password              # Silent (for passwords) -- Im lặng (cho mật khẩu)
read -t 5 answer              # Timeout 5 seconds -- Timeout 5 giây
read -n 1 char                # Read single character -- Đọc một ký tự
read -a array                 # Read into array -- Đọc vào mảng

# Output -- Xuất
echo "Hello"                  # Print with newline -- In có xuống dòng
echo -n "Hello"               # No newline -- Không xuống dòng
echo -e "Hello\tWorld"        # Enable escape sequences -- Bật escape sequences
printf "Name: %s\n" "$name"   # Formatted output -- Xuất có định dạng
printf "Number: %05d\n" 42    # Padded number: 00042 -- Số đệm: 00042

# Redirection -- Chuyển hướng
command > file                # Stdout to file (overwrite) -- Stdout đến file (ghi đè)
command >> file               # Stdout to file (append) -- Stdout đến file (thêm vào)
command 2> file               # Stderr to file -- Stderr đến file
command &> file               # Both stdout and stderr -- Cả stdout và stderr
command 2>&1                  # Stderr to stdout -- Stderr đến stdout
command < file                # File to stdin -- File đến stdin
command1 | command2           # Pipe stdout -- Pipe stdout

# Here document -- Here document
cat << EOF
This is a
multi-line
text
EOF

# Here string -- Here string
cat <<< "single line"
```

## <a id="file-operations"></a> File Operations -- Thao tác File

```bash
# Check file -- Kiểm tra file
if [ -f "$file" ]; then
    echo "File exists -- File tồn tại"
fi

# Read file -- Đọc file
content=$(cat file.txt)       # Read entire file -- Đọc toàn bộ file

while IFS= read -r line; do   # Read line by line -- Đọc từng dòng
    echo "$line"
done < file.txt

# Write file -- Ghi file
echo "text" > file.txt        # Overwrite -- Ghi đè
echo "text" >> file.txt       # Append -- Thêm vào

# File info -- Thông tin file
basename "/path/to/file.txt"  # Get filename: file.txt -- Lấy tên file
dirname "/path/to/file.txt"   # Get directory: /path/to -- Lấy thư mục
realpath "file.txt"           # Get absolute path -- Lấy đường dẫn tuyệt đối

# Temporary files -- Files tạm thời
tmpfile=$(mktemp)             # Create temp file -- Tạo file tạm
tmpdir=$(mktemp -d)           # Create temp directory -- Tạo thư mục tạm
```

## <a id="common-patterns"></a> Common Patterns -- Patterns Thường dùng

```bash
# Script template -- Template script
#!/bin/bash
set -euo pipefail             # Strict mode -- Chế độ nghiêm ngặt

# Colors for output -- Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'                  # No Color -- Không màu
echo -e "${RED}Error${NC}"
echo -e "${GREEN}Success${NC}"

# Error handling -- Xử lý lỗi
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

command || error_exit "Command failed"

# Trap signals -- Bắt tín hiệu
cleanup() {
    rm -f "$tmpfile"
}
trap cleanup EXIT INT TERM

# Check if command exists -- Kiểm tra lệnh tồn tại
if command -v docker &> /dev/null; then
    echo "Docker is installed -- Docker đã cài đặt"
fi

# Parse arguments -- Phân tích tham số
while getopts ":hv" opt; do
    case $opt in
        h) echo "Help" ;;
        v) echo "Verbose" ;;
        \?) echo "Invalid option" ;;
    esac
done

# Confirm action -- Xác nhận hành động
read -p "Continue? (y/n) " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Proceeding..."
fi
```

---
