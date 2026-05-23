#!/bin/bash

# Bài 3: Cải tiến Script Backup

# --- Cấu hình ---
# Lấy đường dẫn của thư mục project một cách an toàn
SOURCE_DIR="$(dirname "$0")/../../.." 
# Tạo thư mục backup ngay trong thư mục exercises
BACKUP_DIR="$(dirname "$0")/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILENAME="backup-$DATE.tar.gz"
# ----------------

echo "Bắt đầu quá trình sao lưu thư mục $SOURCE_DIR..."

# Kiểm tra xem thư mục backup có tồn tại không, nếu không thì tạo ra
mkdir -p "$BACKUP_DIR"

# Nén thư mục nguồn và lưu vào thư mục backup
# Dùng tar để nén. c: create, z: gzip, f: file
tar -czf "$BACKUP_DIR/$FILENAME" "$SOURCE_DIR"

echo "Sao lưu hoàn tất! File được lưu tại: $BACKUP_DIR/$FILENAME"
echo "---"

echo "Bắt đầu dọn dẹp các bản sao lưu cũ hơn 7 ngày..."
# Gợi ý: Lệnh `find` rất mạnh mẽ để tìm kiếm file.
# -mtime +7: tìm các file có thời gian sửa đổi cũ hơn 7*24 giờ.
# -print: In ra tên file tìm được.
# -delete: Xóa file tìm được. (Được comment lại để đảm bảo an toàn)
# Để kích hoạt tính năng xóa, hãy bỏ comment ở `-delete`.
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +7 -print # -delete
echo "Dọn dẹp hoàn tất."
