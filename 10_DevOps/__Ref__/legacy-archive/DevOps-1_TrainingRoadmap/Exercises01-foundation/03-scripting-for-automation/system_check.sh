#!/bin/bash

# Bài 4: Sử dụng Hàm (Functions)
# Script này kiểm tra một vài thông số của hệ thống bằng cách sử dụng các hàm.

# Định nghĩa hàm để hiển thị uptime
show_uptime() {
  echo "--- Uptime của hệ thống ---"
  uptime
  echo "" # Thêm một dòng trống cho dễ đọc
}

# Định nghĩa hàm để hiển thị dung lượng ổ đĩa
show_disk_usage() {
  echo "--- Dung lượng ổ đĩa sử dụng ---"
  df -h
  echo ""
}

# Định nghĩa hàm để hiển thị dung lượng bộ nhớ
show_memory_usage() {
  echo "--- Dung lượng bộ nhớ (RAM) sử dụng ---"
  # Lệnh `free` không có sẵn trên macOS.
  # Chúng ta sẽ kiểm tra sự tồn tại của lệnh `free`.
  # Nếu có, dùng `free -h`. Nếu không, dùng lệnh cho macOS.
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
# Gọi lần lượt các hàm đã định nghĩa.
show_uptime
show_disk_usage
show_memory_usage

echo "Kiểm tra hệ thống hoàn tất."

