#!/bin/bash

# Bài 2: Vòng lặp và Tạo File
# Script này sử dụng vòng lặp `for` để tạo ra 5 file văn bản.
# Cú pháp `{1..5}` tạo ra một chuỗi số từ 1 đến 5.

echo "Bắt đầu tạo files..."

for i in {1..5}; do
  echo "Đây là file thứ $i" > "file$i.txt"
done

echo "Đã tạo 5 files: file1.txt, file2.txt, file3.txt, file4.txt, file5.txt."
ls -l file*.txt
