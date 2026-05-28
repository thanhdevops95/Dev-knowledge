# 💻 Terminal & Command Line

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Công cụ mạnh nhất của mọi lập trình viên

---

## Tại sao phải học Terminal?

- **Nhanh hơn GUI** — Nhiều tác vụ hoàn thành trong vài giây thay vì hàng chục click
- **Tự động hóa** — Viết script để chạy hàng chục lệnh một lúc
- **Server không có giao diện** — Linux server chỉ có CLI
- **Công cụ Dev yêu cầu** — Git, Docker, npm, pip... đều dùng terminal

---

## Điều hướng hệ thống file

```bash
pwd                     # Print Working Directory — xem đang ở đâu
ls                      # List — liệt kê file/folder
ls -la                  # Liệt kê chi tiết (gồm file ẩn)
cd folder               # Change Directory
cd ..                   # Lên thư mục cha
cd ~                    # Về home directory
cd -                    # Quay lại thư mục trước
```

---

## Quản lý file & thư mục

```bash
mkdir my-folder             # Tạo thư mục
mkdir -p a/b/c              # Tạo nhiều cấp thư mục
touch file.txt              # Tạo file rỗng
cp file.txt copy.txt        # Copy file
cp -r folder/ new-folder/   # Copy thư mục (recursive)
mv file.txt new-name.txt    # Đổi tên / Di chuyển
rm file.txt                 # Xóa file
rm -rf folder/              # Xóa thư mục (⚠️ không có thùng rác!)
```

---

## Xem nội dung file

```bash
cat file.txt                # In toàn bộ nội dung
less file.txt               # Xem từng trang (q để thoát)
head -n 20 file.txt         # Xem 20 dòng đầu
tail -n 20 file.txt         # Xem 20 dòng cuối
tail -f app.log             # Theo dõi log realtime
```

---

## Tìm kiếm

```bash
# Tìm file
find . -name "*.js"                     # Tìm file .js
find . -type d -name "node_modules"     # Tìm thư mục

# Tìm nội dung trong file
grep "error" app.log                    # Tìm text trong file
grep -r "TODO" ./src                    # Tìm đệ quy trong thư mục
grep -n "function" main.py              # Hiển thị số dòng
grep -i "ERROR" app.log                 # Không phân biệt hoa thường
```

---

## Pipes & Redirect

```bash
# Pipe: truyền output của lệnh này vào lệnh khác
ls -la | grep ".js"         # Lọc file .js từ kết quả ls
cat log.txt | grep "ERROR" | wc -l  # Đếm số dòng lỗi

# Redirect output vào file
echo "Hello" > file.txt     # Ghi vào file (ghi đè)
echo "World" >> file.txt    # Append vào file
command 2> errors.log       # Redirect stderr
command > out.txt 2>&1      # Redirect cả stdout và stderr
```

---

## Quản lý process

```bash
ps aux                      # Liệt kê tất cả process
ps aux | grep "node"        # Tìm process node
kill 1234                   # Dừng process theo PID
kill -9 1234                # Force kill
pkill node                  # Kill process theo tên
top                         # Monitor process realtime
htop                        # Monitor đẹp hơn (cần cài)
Ctrl + C                    # Dừng lệnh đang chạy
Ctrl + Z                    # Tạm dừng (background)
bg                          # Tiếp tục ở background
fg                          # Đưa về foreground
```

---

## Biến môi trường

```bash
echo $HOME                  # Xem giá trị biến
echo $PATH                  # Xem PATH
export MY_VAR="hello"       # Đặt biến (trong session hiện tại)
printenv                    # Liệt kê tất cả biến môi trường

# Thêm vào ~/.zshrc hoặc ~/.bashrc để lưu vĩnh viễn
export DATABASE_URL="postgres://..."
```

---

## Shell Scripting cơ bản

```bash
#!/bin/bash
# deploy.sh — Script deploy đơn giản

# Biến
APP_NAME="my-app"
DEPLOY_DIR="/var/www/$APP_NAME"

# Điều kiện
if [ -d "$DEPLOY_DIR" ]; then
    echo "Thư mục tồn tại"
else
    mkdir -p "$DEPLOY_DIR"
fi

# Vòng lặp
for file in *.txt; do
    echo "Đang xử lý: $file"
done

# Hàm
deploy() {
    echo "Deploying $APP_NAME..."
    git pull origin main
    npm install
    npm run build
    echo "Done!"
}

deploy
```

Chạy script:
```bash
chmod +x deploy.sh      # Cấp quyền thực thi
./deploy.sh             # Chạy script
```

---

## Các phím tắt hữu ích

| Phím tắt | Tác dụng |
|---|---|
| `Ctrl + C` | Dừng lệnh |
| `Ctrl + L` | Clear terminal |
| `Ctrl + R` | Tìm lệnh trong history |
| `↑ / ↓` | Duyệt history lệnh |
| `Tab` | Auto-complete |
| `Tab Tab` | Gợi ý completion |
| `Ctrl + A` | Nhảy về đầu dòng |
| `Ctrl + E` | Nhảy về cuối dòng |
| `Ctrl + W` | Xóa 1 từ phía sau |

---

## Bài tập thực hành

- [ ] Tạo cấu trúc thư mục dự án bằng terminal (không dùng GUI)
- [ ] Viết script bash tạo file backup tự động
- [ ] Dùng `grep` + `pipe` để phân tích log file
- [ ] Tự cấu hình `~/.zshrc` với alias tiện dụng

---

## Tài nguyên thêm

- [The Missing Semester of CS Education](https://missing.csail.mit.edu/) — MIT course về shell tools
- [Explain Shell](https://explainshell.com/) — Giải thích từng phần của lệnh shell
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/) — Tài liệu chính thức
