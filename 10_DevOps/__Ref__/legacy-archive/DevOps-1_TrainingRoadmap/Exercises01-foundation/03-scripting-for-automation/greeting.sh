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
