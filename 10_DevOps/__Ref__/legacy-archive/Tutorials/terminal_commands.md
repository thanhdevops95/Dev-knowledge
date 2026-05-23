# Hướng dẫn Terminal Commands

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tổng hợp lệnh terminal thường dùng cho PowerShell (Windows) và Bash (Linux/macOS).

---

## 📁**THAO TÁC VỚI THƯ MỤC**

### Xem thư mục hiện tại

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `pwd` | `pwd` | In đường dẫn hiện tại |
| `Get-Location` | `pwd` | Tương tự pwd |

**Giải thích:**
- `pwd` (print working directory): Hiển thị đường dẫn đầy đủ của thư mục hiện tại bạn đang làm việc
- Rất hữu ích khi bạn mất hướng trong cây thư mục hoặc muốn xác nhận vị trí

**Kết quả:**
```
/Users/username/projects/my-app
```

**Ứng dụng:**
- Kiểm tra thư mục hiện tại trước khi chạy lệnh
- Xác nhận đúng vị trí trước khi xóa file quan trọng
- Sử dụng trong script để biết vị trí tuyệt đối

**Lưu ý:**
- Không cần tham số, chỉ cần gõ `pwd` là được

### Di chuyển thư mục

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `cd folder` | `cd folder` | Vào thư mục |
| `cd ..` | `cd ..` | Lên thư mục cha |
| `cd ~` | `cd ~` | Về thư mục home |
| `cd \` | `cd /` | Về thư mục gốc |
| `cd -` | `cd -` | Quay lại thư mục trước |

**Giải thích:**
- `cd` (change directory): Thay đổi thư mục làm việc hiện tại
- `..` = thư mục cha (mẹ) của thư mục hiện tại
- `~` = thư mục home của user (thường là /Users/username trên Mac hoặc C:\Users\username trên Windows)
- `/` hoặc `\` = thư mục gốc hệ thống
- `-` = quay về thư mục vừa sử dụng trước đó

**Ví dụ:**
```bash
# Từ /Users/john/projects/my-app
cd src          # → /Users/john/projects/my-app/src
cd ..           # → /Users/john/projects/my-app (quay lại)
cd ../..        # → /Users/john
cd ~            # → /Users/john (home)
cd /            # → / (root trên Mac/Linux)
cd -            # → /Users/john/projects/my-app (thư mục trước)
```

**Ứng dụng:**
- Điều hướng trong hệ thống file
- Vào thư mục dự án trước khi chạy lệnh
- Lệnh cơ bản nhất, sử dụng hàng chục lần mỗi ngày

**Lưu ý:**
- `cd` không có tham số sẽ về home: `cd` = `cd ~`
- Đường dẫn tương đối (relative): `cd src` - từ vị trí hiện tại
- Đường dẫn tuyệt đối (absolute): `cd /Users/john/projects`

### Liệt kê nội dung

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `ls` | `ls` | Liệt kê file/folder |
| `dir` | `ls -la` | Chi tiết hơn |
| `ls -Force` | `ls -a` | Hiện file ẩn |
| `Get-ChildItem -Recurse` | `ls -R` | Liệt kê đệ quy |
| `tree` | `tree` | Hiện dạng cây |

**Giải thích:**
- `ls` (list): Liệt kê các file và thư mục trong thư mục hiện tại
- `-a` (all): Hiển thị cả file ẩn (bắt đầu bằng dấu chấm .)
- `-l` (long): Hiển thị chi tiết (quyền, chủ sở hữu, kích thước, ngày tháng)
- `-h` (human-readable): Hiển thị kích thước dễ đọc (KB, MB, GB)
- `-R` (recursive): Liệt kê tất cả file trong thư mục con
- `tree`: Hiển thị cấu trúc cây thư mục (cần cài đặt trước)

**Ví dụ:**
```bash
ls              # Liệt kê đơn giản
ls -la          # Liệt kê chi tiết cả file ẩn
ls -lh          # Kích thước dễ đọc (1.2M, 34K)
ls -R           # Hiệt tất cả thư mục con
ls -1           # Mỗi file 1 dòng
tree -L 2       # Hiển thị 2 cấp thư mục
```

**Ứng dụng:**
- Xem có gì trong thư mục trước khi làm việc
- Tìm file bị ẩn (dotfiles như .git, .env)
- Kiểm tra cấu trúc dự án
- Xem quyền file (r=read, w=write, x=execute)

**Lưu ý:**
- File ẩn trên Unix/Mac bắt đầu bằng `.`
- PowerShell: `ls` là alias của `Get-ChildItem`
- Để sử dụng `tree`, có thể cần cài: `brew install tree` (Mac) hoặc `apt install tree` (Linux)

### Tạo thư mục

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `mkdir folder` | `mkdir folder` | Tạo thư mục |
| `mkdir -p a/b/c` | `mkdir -p a/b/c` | Tạo nhiều cấp |
| `New-Item -ItemType Directory folder` | `mkdir folder` | Cách khác |

**Giải thích:**
- `mkdir` (make directory): Tạo thư mục mới
- `-p` (parents): Tạo thư mục cha nếu chưa tồn tại (không báo lỗi)
- Mặc định: nếu thư mục cha không tồn tại sẽ báo lỗi

**Ví dụ:**
```bash
mkdir project                    # Tạo 1 thư mục
mkdir -p src/components/header   # Tạo cấu trúc nhiều cấp
mkdir project1 project2 project3 # Tạo nhiều thư mục cùng lúc
```

**Kết quả:**
```
project/ được tạo
src/components/header/ được tạo với các thư mục cha
```

**Ứng dụng:**
- Tạo cấu trúc thư mục cho dự án mới
- Chuẩn bị folder lưu trữ file
- Thiết lập layout cho website, ứng dụng

**Lưu ý:**
- Tên thư mục không được chứa ký tự đặc biệt
- Trên Windows và Mac phân biệt cách gõ nhưng không phân biệt in hoa/thường
- Linux phân biệt in hoa/thường: `Folder` ≠ `folder`

### Xóa thư mục

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `rmdir folder` | `rmdir folder` | Xóa thư mục rỗng |
| `Remove-Item -Recurse folder` | `rm -r folder` | Xóa thư mục có nội dung |
| `rm -r -Force folder` | `rm -rf folder` | Xóa bắt buộc |

**Giải thích:**
- `rmdir`: Xóa thư mục rỗng (an toàn, lỗi nếu có nội dung)
- `rm -r` (recursive): Xóa thư mục và tất cả nội dung bên trong
- `-f` (force): Xóa không cần xác nhận, bỏ qua các lỗi
- **CẢNH BÁO: `rm -rf` CÓ THỂ XÓA VIỄN VŨ - hãy cẩn thận!**

**Ví dụ:**
```bash
rmdir empty-folder           # Xóa folder rỗng
rm -r project                # Xóa folder + nội dung, hỏi xác nhận
rm -rf .git                  # Xóa ngay không hỏi
rm -rf node_modules/         # Xóa dependencies (thường an toàn)
```

**Ứng dụng:**
- Dọn dẹp các thư mục không dùng
- Xóa thư mục build, cache, node_modules
- Giải phóng dung lượng ổ đĩa

**Lưu ý - RẤT QUAN TRỌNG:**
- `rm -rf /` sẽ xóa TOÀN BỘ hệ thống (đừng chạy!)
- `rm -rf *` trong thư mục sai có thể xóa toàn bộ dự án
- Kiểm tra kỹ đường dẫn trước khi xóa
- Không có "Undo" trong terminal - đã xóa là mất
- Tốt nhất là sử dụng `rm -r` (có xác nhận) thay vì `rm -rf`

---

## 📄**THAO TÁC VỚI FILE**

### Tạo file

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `New-Item file.txt` | `touch file.txt` | Tạo file rỗng |
| `echo "nội dung" > file.txt` | `echo "nội dung" > file.txt` | Tạo + ghi nội dung |
| `echo "thêm" >> file.txt` | `echo "thêm" >> file.txt` | Thêm nội dung |

**Giải thích:**
- `touch`: Tạo file rỗng hoặc cập nhật timestamp nếu tồn tại
- `>` (redirect - ghi đè): Ghi nội dung vào file, nếu file tồn tại sẽ xóa nội dung cũ
- `>>` (append - thêm vào): Thêm nội dung vào cuối file, giữ nội dung cũ
- `echo`: Hiển thị text (nếu kết hợp `>` hoặc `>>` sẽ ghi vào file)

**Ví dụ:**
```bash
touch README.md               # Tạo file rỗng
echo "Hello" > file.txt       # Tạo file với nội dung "Hello"
echo "World" >> file.txt      # File giờ có "Hello\nWorld"
echo "Test" > file.txt        # Ghi đè: file chỉ còn "Test"
```

**Ứng dụng:**
- Tạo file .gitignore, README.md, config
- Ghi log từ lệnh: `command > output.log`
- Tạo template file nhanh

**Lưu ý:**
- `touch file` nếu file tồn tại sẽ cập nhật thời gian, không xóa nội dung
- `>` sẽ xóa nội dung cũ - cẩn thận!
- `>>` an toàn hơn vì giữ nội dung cũ

### Xem nội dung file

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `cat file.txt` | `cat file.txt` | Xem toàn bộ file |
| `Get-Content file.txt` | `cat file.txt` | Tương tự |
| `head file.txt` | `head file.txt` | Xem 10 dòng đầu |
| `tail file.txt` | `tail file.txt` | Xem 10 dòng cuối |
| `tail -f file.txt` | `tail -f file.txt` | Theo dõi file realtime |
| `more file.txt` | `less file.txt` | Xem từng trang |

**Giải thích:**
- `cat` (concatenate): Hiển thị toàn bộ nội dung file (dùng cho file nhỏ)
- `head`: Hiển thị 10 dòng đầu (mặc định), `-n 20` để xem 20 dòng
- `tail`: Hiển thị 10 dòng cuối (dùng để xem log cuối cùng)
- `tail -f` (follow): Theo dõi file realtime, tự động hiển thị dòng mới (Ctrl+C để thoát)
- `less` hoặc `more`: Xem từng trang, dùng Space để next, q để thoát

**Ví dụ:**
```bash
cat file.txt                # Xem toàn bộ
head -n 5 file.txt         # Xem 5 dòng đầu
tail -n 20 file.txt        # Xem 20 dòng cuối
tail -f /var/log/syslog    # Theo dõi log realtime (Ctrl+C thoát)
less file.txt              # Xem từng trang (Space next, q exit)
```

**Ứng dụng:**
- Xem nội dung file config, README, source code
- Kiểm tra log lỗi (thường dùng `tail -f`)
- Kiểm tra dòng đầu file (header của CSV, SQL dump)
- Debug khi chương trình chạy

**Lưu ý:**
- `cat` không tốt cho file lớn (sẽ spam màn hình) → dùng `less` hoặc `head/tail`
- `tail -f` rất hữu ích để xem log server/app realtime
- `less` có nhiều lệnh: `/text` tìm, `G` cuối file, `g` đầu file

### Copy file

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `copy file1 file2` | `cp file1 file2` | Copy file |
| `Copy-Item -Recurse folder1 folder2` | `cp -r folder1 folder2` | Copy thư mục |

**Giải thích:**
- `cp` (copy): Copy file hoặc thư mục
- `-r` (recursive): Copy thư mục và toàn bộ nội dung bên trong
- `-i` (interactive): Hỏi xác nhận nếu file đích tồn tại
- `-v` (verbose): Hiển thị chi tiết quá trình copy

**Ví dụ:**
```bash
cp file.txt backup.txt           # Copy file
cp file.txt folder/              # Copy vào folder
cp -r src/ src_backup/           # Copy cả thư mục
cp -r src/* dest/                # Copy nội dung thư mục (không copy thư mục con)
cp -v *.py backup/               # Copy tất cả .py file với chi tiết
```

**Ứng dụng:**
- Backup file quan trọng
- Copy template/boilerplate code
- Duplicate thư mục dự án
- Migrate file từ nơi này sang nơi khác

**Lưu ý:**
- Nếu file đích tồn tại sẽ bị ghi đè (không cảnh báo)
- `cp -i` an toàn hơn (hỏi xác nhận)
- Copy thư mục phải dùng `-r`, nếu không sẽ báo lỗi
- `cp -r folder1 folder2/` sẽ tạo `folder2/folder1/`

### Di chuyển/Đổi tên

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `move file1 file2` | `mv file1 file2` | Di chuyển hoặc đổi tên |
| `ren old.txt new.txt` | `mv old.txt new.txt` | Đổi tên |
| `Move-Item` | `mv` | Tương tự |

**Giải thích:**
- `mv` (move): Di chuyển file/folder hoặc đổi tên
- Nếu đích là thư mục: file sẽ được di chuyển vào (giữ nguyên tên)
- Nếu đích là tên khác: file sẽ đổi tên hoặc di chuyển
- `-i` (interactive): Hỏi xác nhận nếu file đích tồn tại

**Ví dụ:**
```bash
mv old.txt new.txt           # Đổi tên
mv file.txt folder/          # Di chuyển vào folder (giữ tên)
mv folder/ new_folder/       # Đổi tên thư mục
mv file.txt folder/new.txt   # Di chuyển + đổi tên
mv -i *.py src/              # Di chuyển tất cả .py với xác nhận
```

**Ứng dụng:**
- Đổi tên file (nhanh hơn rename bằng chu chuột)
- Organize file vào folder
- Sắp xếp lại cấu trúc dự án
- Di chuyển backup/archive

**Lưu ý:**
- `mv` không xóa file - nó chỉ "move" metadata
- Kết hợp với các thư mục con: `mv src/file.txt dest/`
- Có thể dùng pattern: `mv *.log logs/`
- `mv -i` an toàn (hỏi trước khi ghi đè)

### Xóa file

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `del file.txt` | `rm file.txt` | Xóa file |
| `Remove-Item file.txt` | `rm file.txt` | Tương tự |
| `rm *.log` | `rm *.log` | Xóa theo pattern |

**Giải thích:**
- `rm` (remove): Xóa file
- `-f` (force): Xóa bắt buộc không hỏi
- `-i` (interactive): Hỏi xác nhận trước xóa
- `*` (wildcard): Đại diện cho bất kỳ ký tự
- Không thể undo - file bị xóa VIỄN VIỄN

**Ví dụ:**
```bash
rm file.txt                  # Xóa file
rm -i file.txt              # Hỏi xác nhận
rm *.log                    # Xóa tất cả file .log
rm -v *.tmp                 # Xóa và hiển thị chi tiết
rm file1.txt file2.txt      # Xóa nhiều file
```

**Ứng dụng:**
- Xóa file không dùng
- Dọn dẹp log cũ, cache, temp file
- Xóa file debug khi release
- Giải phóng dung lượng

**Lưu ý - RẤT QUAN TRỌNG:**
- Không có "Undo" - kiểm tra kỹ trước khi xóa
- `rm *` cẩn thận - có thể xóa hết thư mục
- `rm -i` an toàn hơn (hỏi xác nhận từng file)
- Tốt nhất backup trước khi xóa các file quan trọng
- Trên Mac/Linux file xóa KHÔNG vào Trash, xóa là mất

---

## 🔍**TÌM KIẾM**

### Tìm file

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `Get-ChildItem -Recurse -Filter "*.py"` | `find . -name "*.py"` | Tìm file theo tên |
| `dir -Recurse *.txt` | `find . -type f -name "*.txt"` | Tìm file .txt |
| `where python` | `which python` | Tìm vị trí command |

**Giải thích:**
- `find`: Tìm kiếm file/folder theo nhiều tiêu chí
- `-name "pattern"`: Tìm theo tên (hỗ trợ wildcard *)
- `-type f`: Chỉ tìm file (f=file, d=directory)
- `-type d`: Chỉ tìm thư mục
- `which`: Tìm vị trí của command (để biết command từ đâu)
- `.` = thư mục hiện tại

**Ví dụ:**
```bash
find . -name "*.py"              # Tìm tất cả file .py
find . -name "test_*.py"         # Tìm file bắt đầu bằng test_
find . -type f -name "*.txt"     # Chỉ tìm file .txt
find . -type d -name "node_*"    # Chỉ tìm thư mục
find /home -name "config.json"   # Tìm từ /home
which python                     # Tìm python executable (đầu tiên trong PATH)
```

**Ứng dụng:**
- Tìm file cần xóa (log, cache, build)
- Tìm source code file
- Định vị file config
- Tìm command cài đặt

**Lưu ý:**
- `find . -name "*.py"` tìm đệ quy (tất cả subfolder)
- `find` mạnh nhưng chậm với thư mục lớn
- `-name` phân biệt hoa/thường (dùng `-iname` để không phân biệt)
- `which` dùng để tìm cmd, không dùng để tìm file thông thường

### Tìm nội dung trong file

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `Select-String "text" file.txt` | `grep "text" file.txt` | Tìm text trong file |
| `Select-String "text" *.py` | `grep "text" *.py` | Tìm trong nhiều file |
| `Select-String -Recurse "text"` | `grep -r "text" .` | Tìm đệ quy |

**Giải thích:**
- `grep` (global regular expression print): Tìm dòng chứa text/pattern
- `-r` (recursive): Tìm trong tất cả file của thư mục con
- `-i` (ignore-case): Bỏ qua hoa/thường
- `-v` (invert-match): Hiển thị dòng KHÔNG chứa text
- `-n` (line number): Hiển thị số dòng
- `-l` (list files): Chỉ hiển thị tên file (không hiển thị nội dung)

**Ví dụ:**
```bash
grep "error" log.txt            # Tìm dòng chứa "error"
grep "error" *.log              # Tìm trong tất cả .log file
grep -r "TODO" .                # Tìm "TODO" trong tất cả file
grep -i "warning" log.txt       # Không phân biệt hoa/thường
grep -n "function" code.py      # Hiển thị số dòng
grep -v "#" config.ini          # Dòng không chứa comment (#)
grep -l "console.log" *.js      # Chỉ show file có console.log
```

**Ứng dụng:**
- Tìm lỗi trong log
- Tìm TODO/FIXME trong code
- Tìm function/class định nghĩa
- Tìm config settings
- Debug bằng cách tìm debug statement

**Lưu ý:**
- `grep` hỗ trợ regex (regular expression) - rất mạnh
- `grep "^text"` - dòng bắt đầu bằng text
- `grep "text$"` - dòng kết thúc bằng text
- `grep -r "pattern" --include="*.py"` - chỉ tìm .py files

---

## 💻**HỆ THỐNG**

### Thông tin hệ thống

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `$env:USERNAME` | `whoami` | User hiện tại |
| `hostname` | `hostname` | Tên máy |
| `Get-ComputerInfo` | `uname -a` | Thông tin hệ thống |
| `$PSVersionTable` | `bash --version` | Version shell |

**Giải thích:**
- `whoami`: Hiển thị tên user đang đăng nhập
- `hostname`: Hiển thị tên máy tính trên mạng
- `uname` (unix name): Hiển thị thông tin OS
- `-a` (all): Hiển thị tất cả thông tin

**Ví dụ:**
```bash
whoami                       # → john
hostname                     # → MacBook-Pro.local
uname -a                     # → Darwin MacBook-Pro ... 14.0 ...
```

**Kết quả:**
```
uname -a output:
Darwin MacBook-Pro.local 23.1.0 Darwin Kernel Version 23.1.0
```

**Ứng dụng:**
- Kiểm tra user hiện tại trước khi chạy lệnh (quyền)
- Xác định OS (Linux, Mac, Windows)
- Biết version Bash/Shell
- Kiểm tra tên server

**Lưu ý:**
- `whoami` hữu ích khi làm việc với quyền (sudo)
- `uname -s` chỉ OS: Darwin (Mac), Linux, etc.
- `uname -m` kiến trúc: arm64, x86_64

### Quản lý tiến trình

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `Get-Process` | `ps aux` | Liệt kê tiến trình |
| `Stop-Process -Name "name"` | `kill <PID>` | Dừng tiến trình |
| `taskkill /IM name.exe /F` | `killall name` | Dừng theo tên |
| `Start-Process notepad` | `open app` (Mac) | Mở ứng dụng |

**Giải thích:**
- `ps` (process status): Liệt kê tiến trình đang chạy
- `-aux` (all users, extended): Hiển thị chi tiết của tất cả user
- `kill <PID>`: Dừng tiến trình theo Process ID
- `-9`: Force kill (SIGKILL - không thể bỏ qua)
- `killall`: Dừng tiến trình theo tên
- `PID` = Process ID (số định danh tiến trình)

**Ví dụ:**
```bash
ps aux                           # Liệt kê tất cả tiến trình
ps aux | grep python             # Tìm python process
kill 1234                        # Dừng process ID 1234
kill -9 1234                     # Force kill process 1234
killall python                   # Dừng tất cả python
killall -9 chrome                # Force kill chrome
```

**Kết quả:**
```
ps aux output:
USER    PID  %CPU %MEM    VSZ   RSS TTY  STAT START  TIME COMMAND
root      1  0.0  0.0  19992  1544 ?    Ss   10:00  0:01 /sbin/init
john   1234  0.5  2.3 1234567 45678 ?   Sl   10:05  0:15 python app.py
```

**Ứng dụng:**
- Tìm tiến trình chiếm tài nguyên
- Dừng chương trình bị hang
- Kill server/app sau khi test
- Monitor hệ thống

**Lưu ý:**
- `kill` gửi SIGTERM (yêu cầu dừng nhẹ nhàng)
- `kill -9` là SIGKILL (dừng bắt buộc, không cho cơ hội cleanup)
- `killall` nguy hiểm - có thể kill tiến trình khác cùng tên
- `ps aux | grep python` hữu ích để tìm PID
- CẢNH BÁO: kill process sai có thể làm hỏng hệ thống

### Dung lượng ổ đĩa

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `Get-PSDrive` | `df -h` | Xem dung lượng ổ đĩa |
| `(Get-Item file).Length` | `du -sh folder` | Dung lượng folder |

**Giải thích:**
- `df` (disk free): Hiển thị dung lượng ổ đĩa
- `-h` (human-readable): Hiển thị dạng KB, MB, GB
- `du` (disk usage): Hiển thị dung lượng thư mục
- `-s` (summary): Chỉ tổng (không hiển thị chi tiết từng file)
- `-h` (human-readable): Dễ đọc

**Ví dụ:**
```bash
df -h                            # Xem tất cả ổ đĩa
du -sh /Users/john               # Dung lượng home folder
du -sh *                         # Dung lượng từng item hiện tại
du -sh . | sort -h               # Sắp xếp theo size
du -h --max-depth=1              # Dung lượng cấp 1
```

**Kết quả:**
```
df -h:
Filesystem     Size   Used  Avail Use% Mounted on
/dev/disk1s1   500GB  250GB  250GB  50% /

du -sh /Users/john:
45G     /Users/john
```

**Ứng dụng:**
- Kiểm tra ổ đĩa full
- Tìm folder lớn (node_modules, .git)
- Dọn dẹp dung lượng trước khi backup
- Theo dõi sử dụng ổ đĩa

**Lưu ý:**
- `df -h` xem toàn bộ ổ đĩa (mounted filesystems)
- `du -sh` xem từng thư mục
- `du -sh .` xem thư mục hiện tại
- `du -h --max-depth=1` xem sơ đồ cấp 1 (tốt để tìm folder lớn)

---

## 🌐**MẠNG**

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `ping google.com` | `ping google.com` | Kiểm tra kết nối |
| `ipconfig` | `ifconfig` hoặc `ip addr` | Xem IP |
| `netstat -an` | `netstat -an` | Xem ports đang mở |
| `curl url` | `curl url` | Gọi HTTP request |
| `Invoke-WebRequest url` | `wget url` | Tải file từ URL |
**Giải thích:**
- `ping`: Gửi ICMP request để kiểm tra kết nối mạng
- `ifconfig` (interface config): Hiển thị thông tin card mạng
- `netstat`: Hiển thị kết nối mạng, port đang listen
- `curl`: Gửi HTTP request (GET, POST, etc.)
- `wget`: Tải file từ HTTP/FTP

**Ví dụ:**
```bash
ping google.com                  # Kiểm tra mạng
ping -c 4 8.8.8.8               # Ping 4 lần
ifconfig                        # Xem IP, MAC address
netstat -an | grep LISTEN       # Ports đang mở
curl https://api.example.com    # GET request
curl -X POST -d "data" url      # POST request
wget https://example.com/file.zip # Tải file
```

**Kết quả:**
```
ping google.com:
PING google.com (142.251.32.14): 56 data bytes
64 bytes from 142.251.32.14: icmp_seq=0 ttl=119 time=25.3 ms
```

**Ứng dụng:**
- Kiểm tra internet connection
- Test API
- Tìm IP server
- Tải file từ internet
- Check ports mở (security)

**Lưu ý:**
- `ping` không được phép với một số server (firewall)
- `curl` rất mạnh (GET, POST, headers, auth, etc.)
- `wget` tương tự curl nhưng khác syntax
- `netstat` có thể chậm với nhiều kết nối (dùng `ss` thay thế)
---

## 📦**NÉNZIP**

### Windows PowerShell

```powershell
# Nén
Compress-Archive -Path folder -DestinationPath archive.zip

# Giải nén
Expand-Archive -Path archive.zip -DestinationPath folder
```

**Giải thích:**
- `Compress-Archive`: Nén thư mục thành .zip
- `Expand-Archive`: Giải nén .zip

**Ứng dụng:**
- Backup dự án
- Gửi file qua email
- Share code

### Bash

```bash
# Nén
zip -r archive.zip folder
tar -czvf archive.tar.gz folder

# Giải nén
unzip archive.zip
tar -xzvf archive.tar.gz
```

**Giải thích:**
- `zip`: Tạo file .zip
- `-r` (recursive): Nén cả thư mục con
- `tar`: Tạo tar archive
- `-c` (create): Tạo archive
- `-z` (gzip): Nén bằng gzip (.tar.gz)
- `-v` (verbose): Hiển thị chi tiết
- `-f` (file): Tên file output
- `unzip`: Giải nén .zip
- `tar -x`: Giải nén tar

**Ví dụ:**
```bash
zip -r project.zip project/          # Nén folder
zip -r backup.zip *.py *.json        # Nén file lựa chọn
tar -czvf backup.tar.gz project/     # Nén tar.gz
unzip project.zip                    # Giải nén
tar -xzvf backup.tar.gz              # Giải nén tar.gz
unzip -l archive.zip                 # Xem nội dung (không giải)
tar -tzf archive.tar.gz              # Xem nội dung tar.gz
```

**Ứng dụng:**
- Backup dự án, database
- Tải source code
- Chia sẻ folder lớn
- Archive log cũ

**Lưu ý:**
- `.zip` tương thích Windows/Mac/Linux
- `.tar.gz` compress tốt hơn, thường dùng Linux
- `zip -r` cẩn thận node_modules (rất lớn)
- Có thể exclude: `zip -r -x "node_modules/*" archive.zip folder/`

---

## 🔧**BIẾN MÔI TRƯỜNG**

### Xem biến

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `$env:PATH` | `echo $PATH` | Xem PATH |
| `Get-ChildItem Env:` | `env` | Xem tất cả biến |
| `$env:VARIABLE` | `echo $VARIABLE` | Xem 1 biến |

**Giải thích:**
- Biến môi trường: Config toàn cục cho shell
- `PATH`: Danh sách thư mục chứa executable (tìm kiếm command)
- `HOME`: Thư mục home user
- `USER`: Tên user
- `SHELL`: Loại shell đang dùng
- `echo`: In giá trị
- `env`: Hiển thị tất cả biến

**Ví dụ:**
```bash
echo $PATH                       # Xem PATH
echo $HOME                       # Xem home
echo $USER                       # Xem user
env | grep PATH                  # Tìm PATH trong env
env | sort                       # Xem tất cả biến sắp xếp
```

### Đặt biến (tạm thời)

```powershell
# PowerShell
$env:MY_VAR = "value"
echo $env:MY_VAR
```

```bash
# Bash
export MY_VAR="value"
echo $MY_VAR
```

**Giải thích:**
- `export`: Làm biến có sẵn cho child process
- Tạm thời: Chỉ tồn tại trong session hiện tại
- Vĩnh viễn: Thêm vào ~/.bashrc hoặc ~/.bash_profile

**Ví dụ:**
```bash
# Tạm thời
export DEBUG=1
export DATABASE_URL="postgresql://localhost/mydb"

# Kiểm tra
echo $DEBUG

# Vĩnh viễn (thêm vào ~/.bashrc)
echo 'export DEBUG=1' >> ~/.bashrc
source ~/.bashrc
```

**Ứng dụng:**
- Config ứng dụng (API key, database URL)
- Đặt ngôn ngữ (LANG, LC_ALL)
- Python path, Node path
- Debug mode

**Lưu ý:**
- `export` để biến có sẵn cho child process
- Không `export` thì chỉ shell hiện tại dùng được
- `$VARIABLE` để sử dụng biến
- File `.bashrc` sửa lâu dài (thêm vào profile)

---

## 🔗**PIPE & REDIRECT**

### Pipe (|) - Chuyển output sang lệnh khác

```bash
# Đếm số file .py
ls *.py | wc -l

# Tìm và lọc
cat file.txt | grep "error"

# Sắp xếp
ls | sort
```

**Giải thích:**
- `|` (pipe): Chuyển output của lệnh này sang input của lệnh khác
- `wc` (word count): Đếm dòng, từ, ký tự
- `-l`: Đếm dòng
- Rất mạnh: Kết hợp nhiều lệnh đơn giản

**Ví dụ:**
```bash
ls | wc -l                       # Đếm file trong folder
ps aux | grep python             # Tìm python process
cat file.txt | head -5           # 5 dòng đầu
cat file.txt | tail -5           # 5 dòng cuối
cat file.txt | grep "error" | wc -l # Đếm lỗi
```

**Ứng dụng:**
- Xử lý dữ liệu từ lệnh này sang lệnh khác
- Filter, count, sort output
- Tạo pipeline xử lý phức tạp

### Redirect - Chuyển output ra file

```bash
# Ghi đè (>)
echo "hello" > file.txt

# Thêm vào (>>)
echo "world" >> file.txt

# Redirect stderr (2>)
command 2> error.log

# Redirect cả stdout và stderr
command > output.log 2>&1
```

**Giải thích:**
- `>` (redirect stdout): Ghi output vào file, ghi đè
- `>>` (append): Thêm output vào cuối file
- `2>` (redirect stderr): Ghi error vào file
- `2>&1`: Ghi cả error và output vào file
- stdout = standard output (output bình thường)
- stderr = standard error (error messages)

**Ví dụ:**
```bash
ls > files.txt                   # Liệt kê vào file
command >> log.txt               # Thêm vào log
python script.py > output.txt 2> error.txt  # Tách output và error
command > output.txt 2>&1        # Cả hai vào cùng file
python script.py 2>/dev/null     # Bỏ qua error
```

**Ứng dụng:**
- Lưu output command vào file
- Tạo log file
- Chuyển hướng error
- Tự động hóa (script chạy unattended)

**Lưu ý:**
- `>` sẽ xóa nội dung cũ - cẩn thận!
- `>>` an toàn hơn (append)
- `/dev/null` là "trash" - `2>/dev/null` bỏ qua error
- `2>&1` chuyển stderr sang stdout (thường dùng)

---

## 📜**HISTORY & ALIAS**

### Xem lịch sử lệnh

| PowerShell | Bash | Mô tả |
|------------|------|-------|
| `history` | `history` | Xem lịch sử |
| `h` | `!123` | Chạy lệnh số 123 |
| `r` | `!!` | Chạy lại lệnh cuối |
| `Ctrl + R` | `Ctrl + R` | Tìm trong history |

**Giải thích:**
- `history`: Xem các lệnh đã chạy (lưu trong ~/.bash_history)
- `!123`: Chạy lệnh số 123 từ history
- `!!`: Chạy lệnh cuối (rất hữu ích)
- `Ctrl+R`: Reverse search (tìm lệnh cũ)

**Ví dụ:**
```bash
history                          # Xem 30 lệnh gần đây
history | grep python            # Tìm lệnh chứa python
history 20                       # Xem 20 lệnh gần đây
!!                               # Chạy lại lệnh cuối
!-2                              # Chạy lệnh cách đây 2 vị trí
!python                          # Chạy lệnh bắt đầu bằng python
Ctrl+R python                    # Tìm lệnh chứa python
```

**Ứng dụng:**
- Tìm lệnh dài đã chạy
- Chạy lại lệnh phức tạp
- Debug bằng cách xem lệnh đã chạy
- Học từ các lệnh trước đó

### Tạo Alias

```powershell
# PowerShell (tạm thời)
Set-Alias ll Get-ChildItem

# PowerShell (vĩnh viễn) - thêm vào $PROFILE
notepad $PROFILE
# Thêm: Set-Alias ll Get-ChildItem
```

```bash
# Bash (tạm thời)
alias ll='ls -la'

# Bash (vĩnh viễn) - thêm vào ~/.bashrc
echo "alias ll='ls -la'" >> ~/.bashrc
source ~/.bashrc
```

**Giải thích:**
- `alias`: Tạo tên gọi tắt cho lệnh dài
- Tạm thời: Chỉ tồn tại session hiện tại
- Vĩnh viễn: Thêm vào ~/.bashrc
- `source`: Tải lại config file

**Ví dụ:**
```bash
alias ll='ls -la'                # Tắt cho ls -la
alias la='ls -A'                 # Tắt cho ls -A
alias l='ls -CF'                 # Tắt cho ls -CF
alias gc='git commit'            # Tắt git command
alias gs='git status'            # Tắt git status
alias ..='cd ..'                 # Tắt cd ..

# Vĩnh viễn (thêm vào ~/.bashrc hoặc ~/.bash_profile)
echo "alias ll='ls -la'" >> ~/.bashrc
echo "alias gc='git commit'" >> ~/.bashrc
source ~/.bashrc
```

**Ứng dụng:**
- Viết tắt các lệnh dùng thường xuyên
- Giảm lỗi gõ
- Tăng tốc độ làm việc
- Chuẩn hóa workflow team

**Lưu ý:**
- Alias chỉ shortcut - không thay thế learning
- Quá nhiều alias dễ quên lệnh gốc
- `alias` xem tất cả alias hiện tại
- `unalias ll` xóa alias
- Cẩn thận: `alias rm='rm -i'` (hỏi xác nhận) - an toàn hơn

---

## ⌨️**PHÍM TẮT TERMINAL**

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + C` | Dừng lệnh đang chạy |
| `Ctrl + Z` | Tạm dừng lệnh (background) |
| `Ctrl + D` | Đóng terminal |
| `Ctrl + L` | Xóa màn hình (clear) |
| `Ctrl + R` | Tìm trong history |
| `Tab` | Auto-complete |
| `↑ / ↓` | Duyệt history |

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
