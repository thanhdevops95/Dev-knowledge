# Hướng dẫn Git cơ bản

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tài liệu này tổng hợp các thao tác Git thường gặp khi làm việc với dự án phần mềm.

**Áp dụng cho:** Python, Node.js, Java, C#, và các ngôn ngữ khác.

---

## 🔗**CÁC LỆNH GIT THƯỜNG DÙNG**

| Lệnh | Mô tả |
|------|-------|
| `git status` | Xem trạng thái hiện tại |
| `git add .` | Thêm tất cả file vào staging |
| `git commit -m "msg"` | Commit với message |
| `git push` | Push lên remote |
| `git pull` | Pull code mới từ remote |
| `git log --oneline` | Xem lịch sử commit |
| `git diff` | Xem thay đổi |
| `git branch` | Xem danh sách branch |
| `git checkout <branch>` | Chuyển branch |
| `git remote -v` | Xem remote URL |

---

## 🔧**TÌNH HUỐNG 1: GỠ BỎ GIT KHỎI DỰ ÁN**

### Khi nào cần dùng?
- Khi muốn tách dự án ra khỏi repo cũ
- Khi muốn upload lên repo mới
- Khi clone dự án về và muốn xóa lịch sử git

### Các bước thực hiện

#### Windows (PowerShell):
```powershell
# Kiểm tra có git không
git status
# ==> Lệnh này kiểm tra xem thư mục hiện tại có phải là một Git repository không.
# Kết quả nếu là Git repository:
# On branch main (hoặc master)
# Your branch is up to date with 'origin/main'.
# nothing to commit, working tree clean
# Ý nghĩa: Repo đang ở branch main, không có thay đổi chưa commit.

# Nếu KHÔNG phải Git repository:
# fatal: not a git repository (or any of the parent directories): .git
# Ý nghĩa: Thư mục hiện tại không phải là Git repository.

# Xóa thư mục .git (xóa hoàn toàn lịch sử git)
Remove-Item -Recurse -Force ".git"
# ==> Lệnh này xóa thư mục .git và tất cả nội dung bên trong.
# -Recurse: Xóa thư mục và tất cả thư mục con
# -Force: Bỏ qua xác nhận, xóa ngay lập tức
# ".git": Tên thư mục cần xóa (thư mục ẩn chứa lịch sử commit)
# Kết quả: Không có output nếu xóa thành công (im lặng là tốt!)
# Ý nghĩa: Toàn bộ lịch sử commit, branch, tag được xóa vĩnh viễn.

# Xác nhận đã xóa
git status
# ==> Lệnh này kiểm tra lại xem có còn repo không.
# Kết quả nếu xóa thành công:
# fatal: not a git repository (or any of the parent directories): .git
# Ý nghĩa: Git không tìm thấy thư mục .git, cho biết repo đã bị xóa hoàn toàn.
# Bây giờ thư mục này trở lại thư mục bình thường, không còn theo dõi bởi Git.
```

#### Linux/macOS:
```bash
# Xóa thư mục .git
rm -rf .git
# ==> Lệnh này xóa thư mục .git và tất cả nội dung bên trong.
# rm: Lệnh remove (xóa) file/thư mục
# -r: Recursive - xóa thư mục và tất cả thư mục/file con bên trong
# -f: Force - bỏ qua xác nhận, xóa ngay lập tức
# ".git": Tên thư mục cần xóa (thư mục ẩn chứa lịch sử commit)
# Kết quả: Không có output nếu xóa thành công (im lặng = thành công)
# Ý nghĩa: Toàn bộ lịch sử commit, branch, remote URL bị xóa vĩnh viễn.

# Xác nhận đã xóa
git status
# ==> Kiểm tra lại xem repo có còn không.
# Kết quả nếu xóa thành công:
# fatal: not a git repository (or any of the parent directories): .git
# Ý nghĩa: Git báo lỗi vì không tìm thấy thư mục .git.
# Điều này chứng tỏ Git đã hoàn toàn bị gỡ bỏ khỏi dự án này.
# Thư mục bây giờ trở lại thư mục bình thường, không còn là Git repository.
```

> ⚠️ **Lưu ý:** Sau khi xóa `.git`, toàn bộ lịch sử commit sẽ mất vĩnh viễn!

---

## 🚀**TÌNH HUỐNG 2: TẠO MỚI GIT CHO DỰ ÁN**

### Khi nào cần dùng?
- Khi bắt đầu dự án mới
- Sau khi gỡ git cũ và muốn tạo mới
- Khi muốn upload dự án lên GitHub/GitLab

### Các bước thực hiện

#### Bước 1: Khởi tạo git
```bash
cd <thư-mục-dự-án>
# ==> Lệnh này thay đổi thư mục làm việc (change directory).
# <thư-mục-dự-án>: Tên thư mục chứa dự án (ví dụ: cd my-project)
# Kết quả: Không có output nếu thành công, shell prompt sẽ thay đổi.
# Ý nghĩa: Bây giờ bạn đang ở trong thư mục dự án, sẵn sàng khởi tạo git.

git init
# ==> Lệnh này khởi tạo một Git repository mới trong thư mục hiện tại.
# Kết quả:
# Initialized empty Git repository in /path/to/my-project/.git/
# Ý nghĩa: Git đã tạo thư mục .git ẩn chứa tất cả cấu hình Git.
# Từ đây trở đi, Git sẽ theo dõi mọi thay đổi file trong dự án.
```

#### Bước 2: Thêm file vào staging
```bash
# Thêm tất cả file
git add .
# ==> Lệnh này thêm tất cả file và thư mục con vào staging area (area chờ commit).
# ".": Biểu thị thư mục hiện tại và tất cả nội dung bên trong.
# Kết quả: Không có output nếu thành công.
# Ý nghĩa: Git sẽ theo dõi tất cả file hiện tại, chuẩn bị để commit.
# Lưu ý: File trong .gitignore sẽ KHÔNG được thêm vào staging.

# Hoặc thêm từng file
git add main.py README.md
# ==> Thêm chỉ những file cụ thể vào staging area.
# main.py README.md: Tên file cần thêm (có thể thêm nhiều file cách nhau bằng space).
# Kết quả: Không có output nếu thành công.
# Ý nghĩa: Chỉ hai file này sẽ được commit, file khác sẽ bị bỏ qua.
```

#### Bước 3: Commit đầu tiên
```bash
git commit -m "v1.0.0 - Initial release"
# ==> Lệnh này lưu các thay đổi đã staging vào lịch sử Git.
# -m: Tùy chọn chỉ định commit message (dòng mô tả)
# "v1.0.0 - Initial release": Nội dung message (nên mô tả rõ ràng thay đổi gì)
# Kết quả:
# [main (root-commit) abc1234] v1.0.0 - Initial release
#  3 files changed, 45 insertions(+)
#  create mode 100644 main.py
#  create mode 100644 README.md
#  create mode 100644 requirements.txt
# Ý nghĩa: 
# - [main]: Commit này ở branch main
# - (root-commit): Đây là commit đầu tiên trong repo
# - abc1234: Hash ID duy nhất của commit này (dùng để tham chiếu sau)
# - 3 files changed: 3 file được thêm vào
# - 45 insertions: 45 dòng code được thêm
```

#### Bước 4: Kết nối với remote repository
```bash
# Thêm remote (GitHub/GitLab)
git remote add origin https://github.com/username/repo-name.git
# ==> Lệnh này kết nối repo local với một server repository (remote).
# remote add: Thêm một kết nối remote mới
# origin: Tên mặc định cho remote chính (có thể đặt tên khác)
# https://github.com/username/repo-name.git: URL của repo trên GitHub
# Kết quả: Không có output nếu thành công.
# Ý nghĩa: Git bây giờ biết rằng repo local này liên kết với repo trên GitHub.
# Thay username và repo-name bằng thông tin thực tế của bạn.

# Kiểm tra remote
git remote -v
# ==> Lệnh này hiển thị danh sách tất cả remote connections.
# -v: Verbose - hiển thị chi tiết (URL)
# Kết quả:
# origin  https://github.com/username/repo-name.git (fetch)
# origin  https://github.com/username/repo-name.git (push)
# Ý nghĩa:
# - origin: Tên remote connection
# - (fetch): URL dùng để tải code từ remote
# - (push): URL dùng để gửi code lên remote
# Nếu chỉ có 1 dòng, nghĩa là fetch và push dùng chung URL.
```

#### Bước 5: Push lên remote
```bash
# Push lần đầu
git push -u origin main
# ==> Lệnh này đẩy (push) các commit từ repo local lên server (remote).
# -u: Upstream - thiết lập branch local để theo dõi branch remote
# origin: Tên remote connection
# main: Tên branch cần push
# Kết quả:
# Enumerating objects: 3, done.
# Counting objects: 100% (3/3), done.
# Delta compression using up to 8 threads
# Compressing objects: 100% (2/2), done.
# Writing objects: 100% (3/3), 256 bytes | 256.00 KiB/s, done.
# Total 3 (delta 0), reused 0 (delta 0)
# remote: 
# remote: Create a pull request for 'main' on GitHub by visiting:
# remote: https://github.com/username/repo-name/pull/new/main
# remote: 
# To https://github.com/username/repo-name.git
#  * [new branch] main -> main
# Branch 'main' set up to track remote tracking branch 'main' from 'origin'.
# Ý nghĩa:
# - [new branch]: Branch 'main' được tạo lần đầu trên GitHub
# - Enumerating objects: Git đang chuẩn bị dữ liệu để gửi
# - Writing objects: Đang gửi file lên server
# - "set up to track": Branch local 'main' sẽ tự động theo dõi remote 'origin/main'

# Hoặc nếu branch là master
git push -u origin master
# ==> Giống như trên, nhưng dùng branch 'master' thay vì 'main'.
# Ý nghĩa: Phiên bản cũ của Git dùng 'master', phiên bản mới dùng 'main'.
```

---

## 📝**TÌNH HUỐNG 3: CLONE DỰ ÁN VỀ MÁY**

### Các bước thực hiện

```bash
# Clone repo
git clone https://github.com/username/repo-name.git
# ==> Lệnh này tải một bản sao hoàn chỉnh của repo từ GitHub về máy local.
# https://github.com/username/repo-name.git: URL của repo trên GitHub
# Kết quả: Thư mục 'repo-name' được tạo với tất cả code + lịch sử git.
# Ý nghĩa: Bạn có một bản sao đầy đủ, có thể làm việc offline và commit.

# Hoặc clone vào thư mục cụ thể
git clone https://github.com/username/repo-name.git my-folder
# ==> Giống như trên, nhưng repo sẽ được clone vào thư mục 'my-folder' tùy chỉnh.
# Hữu ích khi bạn muốn đặt tên khác hoặc clone cùng repo nhiều lần.
```

---

## 🔄**TÌNH HUỐNG 4: CẬP NHẬT CODE (WORKFLOW HÀNG NGÀY)**

### Quy trình làm việc

```bash
# 1. Kiểm tra trạng thái
git status
# ==> Xem trạng thái hiện tại của repo (file đã thay đổi, staging area, v.v.).
# Kết quả nếu clean: On branch main, nothing to commit, working tree clean
# Ý nghĩa: Bạn ở branch main, không có file nào thay đổi, mọi thứ đều sạch sẽ.

# 2. Pull code mới từ remote
git pull
# ==> Tải code mới từ GitHub về và tự động merge vào branch hiện tại.
# Kết quả: Already up to date (nếu không có update) hoặc hiển thị số file thay đổi.
# Ý nghĩa: Đảm bảo bạn có code mới nhất trước khi bắt đầu làm việc.

# 3. Chỉnh sửa code...
# (Bạn sửa file bằng editor như VS Code)

# 4. Xem những gì đã thay đổi
git diff
# ==> Hiển thị chi tiết các dòng code được thêm/xóa.
# Kết quả: Dòng cũ bắt đầu bằng -, dòng mới bắt đầu bằng +
# Ý nghĩa: Xem lại thay đổi trước khi commit.

# 5. Thêm file đã sửa
git add .
# ==> Thêm tất cả file đã thay đổi vào staging area (chuẩn bị commit).
# Ý nghĩa: File sẽ được bao gồm trong commit tiếp theo.

# 6. Commit với message mô tả
git commit -m "Thêm tính năng XYZ"
# ==> Lưu các thay đổi vào lịch sử git với message mô tả rõ ràng.
# Ý nghĩa: Tạo 1 điểm lưu trữ (snapshot) có thể quay lại sau.

# 7. Push lên remote
git push
# ==> Đẩy commit mới lên GitHub để cập nhật code trên server.
# Kết quả: Everything up-to-date (nếu không có commit mới) hoặc [main ...] main -> main
# Ý nghĩa: Các thành viên khác có thể pull code mới của bạn.
```

---

## 🌿**TÌNH HUỐNG 5: LÀM VIỆC VỚI BRANCH**

### Tạo và chuyển branch

```bash
# Xem danh sách branch
git branch
# ==> Hiển thị tất cả branch trong repo local.
# Kết quả: * main (branch hiện tại được đánh dấu *)
#          feature-new
#          develop
# Ý nghĩa: Bạn có 3 branch, đang ở branch main.

# Tạo branch mới
git branch feature-new
# ==> Tạo 1 branch mới từ commit hiện tại.
# Ý nghĩa: Branch mới sẽ chứa tất cả code từ commit hiện tại.

# Chuyển sang branch mới
git checkout feature-new
# ==> Chuyển từ branch main sang feature-new.
# Kết quả: Switched to branch 'feature-new'
# Ý nghĩa: Bây giờ các commit sẽ tạo ở branch feature-new.

# Hoặc tạo + chuyển cùng lúc
git checkout -b feature-new
# ==> Tạo branch và chuyển sang nó trong 1 lệnh.
# Ý nghĩa: Tiết kiệm thời gian so với tạo + chuyển riêng.
```

### Merge branch

```bash
# Chuyển về main
git checkout main
# ==> Chuyển sang branch main để chuẩn bị nhận merge.
# Ý nghĩa: Merge sẽ kết hợp feature-new vào branch hiện tại (main).

# Merge feature-new vào main
git merge feature-new
# ==> Kết hợp các thay đổi từ feature-new vào main.
# Kết quả: Merge made by the 'recursive' strategy + số file/dòng thay đổi
# Ý nghĩa: Code mới từ feature-new giờ có ở main.

# Xóa branch sau khi merge
git branch -d feature-new
# ==> Xóa branch feature-new (chỉ xóa sau khi merge thành công).
# Ý nghĩa: Dọn dẹp branch không cần thiết, giữ repo gọn gàng.
```

---

## ⏪**TÌNH HUỐNG 6: HOÀN TÁC (UNDO)**

### Hoàn tác file chưa commit

```bash
# Hoàn tác 1 file về trạng thái commit cuối
git checkout -- <filename>
# ==> Loại bỏ tất cả thay đổi trong file và khôi phục về commit cuối cùng.
# --: Phân tách option từ filename (tránh nhầm với branch name)
# <filename>: Tên file cần hoàn tác (ví dụ: main.py)
# Kết quả: Không có output nếu thành công.
# Ý nghĩa: File được khôi phục, mọi thay đổi chưa commit đều mất (cẩn thận!).

# Hoàn tác tất cả file
git checkout -- .
# ==> Loại bỏ thay đổi TẤT CẢ file về commit cuối.
# Kết quả: Không có output.
# Ý nghĩa: Tất cả file sẽ quay lại trạng thái lần commit cuối.
# ⚠️ CẢNH BÁO: Điều này sẽ XÓA các thay đổi chưa commit. Dùng git stash để lưu trước.
```

### Hoàn tác commit

```bash
# Hoàn tác commit cuối, giữ lại changes
git reset --soft HEAD~1
# ==> Quay lại commit trước đó nhưng giữ lại các thay đổi trong working directory.
# --soft: Chế độ "mềm" - giữ changes ở working directory
# HEAD~1: Commit trước commit hiện tại (HEAD là commit hiện tại)
# Kết quả: Unstaged changes after reset: M main.py
# Ý nghĩa: Bạn có thể sửa lại v commit với message khác.

# Hoàn tác commit cuối, xóa changes
git reset --hard HEAD~1
# ==> Quay lại commit trước đó và HUỶ TẤT CẢ thay đổi không cần lưu.
# --hard: Chế độ "cứng" - xóa tất cả changes
# HEAD~1: Commit trước đó
# Kết quả: HEAD is now at abc1234 Previous commit message
# Ý nghĩa: Code quay lại trước đó, commit mới bị xóa vĩnh viễn.
# ⚠️ CẢNH BÁO: Điều này sẽ XÓA commit và code! Không thể khôi phục được!
```

### Xem lịch sử commit

```bash
git log --oneline -10
# ==> Hiển thị danh sách 10 commit gần nhất dưới dạng tóm tắt (1 dòng/commit).
# --oneline: Tóm tắt (1 dòng thay vì nhiều dòng)
# -10: Số commit muốn xem (10 commit gần nhất)
# Kết quả:
# abc5678 (HEAD -> main) Thêm tính năng XYZ
# def4567 Sửa bug trong main.py
# ghi3456 Thêm database connection
# jkl2345 (tag: v1.0.0) Initial release
# Ý nghĩa:
# - abc5678: Hash commit (ID duy nhất của commit)
# - HEAD -> main: Commit hiện tại ở branch main
# - (tag: v1.0.0): Commit này được đánh tag v1.0.0
```

---

## 🏷️**TÌNH HUỐNG 7: TẠO TAG (VERSION)**

### Tạo tag cho version release

```bash
# Tạo tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
# ==> Tạo một tag (nhãn) cho commit hiện tại để đánh dấu version release.
# -a: Annotated tag (tag có metadata như tác giả, ngày, message)
# v1.0.0: Tên tag (theo semantic versioning: v[Major].[Minor].[Patch])
# -m: Tùy chọn chỉ định message cho tag
# Kết quả: Không có output nếu thành công.
# Ý nghĩa: Tag v1.0.0 được tạo, đánh dấu điểm version 1.0.0 của dự án.

# Xem danh sách tag
git tag
# ==> Hiển thị danh sách tất cả tag trong repo.
# Kết quả: v0.1.0
#          v0.2.0
#          v1.0.0
# Ý nghĩa: Mỗi dòng là 1 tag, dễ dàng quay lại version cũ khi cần.

# Push tag lên remote
git push origin v1.0.0
# ==> Đẩy 1 tag cụ thể lên GitHub.
# origin: Tên remote (thường là GitHub)
# v1.0.0: Tên tag cần push
# Kết quả: * [new tag]         v1.0.0 -> v1.0.0
# Ý nghĩa: GitHub bây giờ có tag này, có thể tạo release từ tag.

# Hoặc push tất cả tag
git push --tags
# ==> Đẩy TẤT CẢ tag lên GitHub cùng lúc.
# Kết quả: * [new tag]         v0.1.0 -> v0.1.0
#          * [new tag]         v0.2.0 -> v0.2.0
#          * [new tag]         v1.0.0 -> v1.0.0
# Ý nghĩa: Tiết kiệm thời gian so với push từng tag.
```

---

## 📄**TÌNH HUỐNG 8: TẠO FILE .gitignore**

### .gitignore là gì?

**`.gitignore`** là một file đặc biệt mà Git sử dụng để biết những file/thư mục nào **KHÔNG CẦN** theo dõi (track) và commit lên repository.

### Tại sao cần .gitignore?

| Lý do | Ví dụ |
|-------|-------|
| **File tạm thời** | `__pycache__/`, `*.pyc` - Python tự tạo khi chạy |
| **Thư viện cài đặt** | `venv/`, `node_modules/` - Quá nặng, ai cũng tự cài được |
| **File cài đặt IDE** | `.vscode/`, `.idea/` - Mỗi người dùng IDE khác nhau |
| **File nhạy cảm** | `.env`, `config.local.json` - Chứa mật khẩu, API key |
| **File hệ thống** | `.DS_Store` (Mac), `Thumbs.db` (Windows) |
| **Log và cache** | `*.log`, `.cache/` - Không cần lưu |

### Cách tạo file .gitignore

#### Bước 1: Tạo file
```bash
# Windows (PowerShell)
New-Item .gitignore -ItemType File

# Linux/macOS
touch .gitignore
```

#### Bước 2: Thêm nội dung
Mở file `.gitignore` bằng text editor và thêm các pattern.

### Cú pháp .gitignore

| Pattern | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| `filename` | Bỏ qua file cụ thể | `secret.txt` |
| `*.ext` | Bỏ qua tất cả file có đuôi `.ext` | `*.log`, `*.pyc` |
| `folder/` | Bỏ qua toàn bộ thư mục | `venv/`, `__pycache__/` |
| `!filename` | KHÔNG bỏ qua (ngoại lệ) | `!important.log` |
| `#` | Comment (ghi chú) | `# Đây là ghi chú` |
| `**/folder` | Bỏ qua folder ở bất kỳ đâu | `**/__pycache__` |
| `folder/**` | Bỏ qua mọi thứ trong folder | `logs/**` |

### File .gitignore mẫu cho Python 🐍

```gitignore
# =============================================
# .gitignore cho dự án Python
# =============================================

# ----- FILE TẠM THỜI CỦA PYTHON -----
# Khi Python chạy, nó tạo các file .pyc để tăng tốc
# Không cần commit vì Python sẽ tự tạo lại
__pycache__/
*.py[cod]
*$py.class
*.pyo

# ----- MÔI TRƯỜNG ẢO (VIRTUAL ENVIRONMENT) -----
# Thư mục chứa các thư viện đã cài đặt
# Không commit vì quá nặng và ai cũng tự cài được từ requirements.txt
venv/
env/
.venv/
ENV/

# ----- THƯ MỤC IDE/EDITOR -----
# Mỗi người dùng IDE khác nhau, không cần đồng bộ
.vscode/
.idea/
*.swp
*.swo
*~

# ----- FILE LOG -----
# Log được tạo khi chạy ứng dụng, không cần lưu
*.log
logs/
*.log.*

# ----- FILE CACHE -----
# Cache tạm thời, sẽ được tạo lại khi cần
.cache/
*.cache
*.json.cache
.pytest_cache/

# ----- FILE HỆ ĐIỀU HÀNH -----
# Windows tạo Thumbs.db, Mac tạo .DS_Store
.DS_Store
Thumbs.db
ehthumbs.db
Desktop.ini

# ----- FILE NHẠY CẢM -----
# QUAN TRỌNG: Không bao giờ commit file chứa mật khẩu!
.env
.env.local
*.env
config.local.json
secrets.json

# ----- FILE BUILD/DISTRIBUTION -----
# Được tạo khi đóng gói ứng dụng
build/
dist/
*.egg-info/
*.egg

# ----- FILE DATABASE -----
# Database local không cần commit
*.db
*.sqlite3

# ----- JUPYTER NOTEBOOK -----
.ipynb_checkpoints/
```

---

### File .gitignore mẫu cho Node.js/JavaScript 

```gitignore
# =============================================
# .gitignore cho dự án Node.js/JavaScript
# =============================================

# ----- THƯ MỤC NODE_MODULES -----
# Chứa tất cả thư viện cài đặt từ npm/yarn
# Rất nặng (hàng trăm MB), ai cũng tự cài được từ package.json
node_modules/

# ----- FILE LOCK -----
# Chỉ giữ 1 trong 2: package-lock.json HOẶC yarn.lock
# Không ignore file này nếu muốn đồng bộ version
# yarn.lock
# package-lock.json

# ----- THƯ MỤC BUILD -----
# File được tạo khi build dự án
dist/
build/
.next/
out/

# ----- FILE MÔI TRƯỜNG -----
# Chứa biến môi trường, API key, mật khẩu
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# ----- THƯ MỤC IDE/EDITOR -----
.vscode/
.idea/
*.swp

# ----- FILE LOG -----
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# ----- FILE HỆ ĐIỀU HÀNH -----
.DS_Store
Thumbs.db

# ----- FILE TEST/COVERAGE -----
coverage/
.nyc_output/

# ----- FILE CACHE -----
.cache/
.parcel-cache/
.eslintcache
```

---

### File .gitignore mẫu cho C#/.NET 

```gitignore
# =============================================
# .gitignore cho dự án C#/.NET
# =============================================

# ----- THƯ MỤC BUILD -----
# File được tạo khi compile
bin/
obj/

# ----- NUGET PACKAGES -----
# Thư viện cài đặt từ NuGet
packages/
*.nupkg

# ----- FILE VISUAL STUDIO -----
.vs/
*.user
*.suo
*.userosscache
*.sln.docstates

# ----- FILE RIDER/JETBRAINS -----
.idea/
*.DotSettings.user

# ----- FILE PUBLISH -----
publish/

# ----- FILE LOG -----
*.log
logs/

# ----- FILE HỆ ĐIỀU HÀNH -----
.DS_Store
Thumbs.db
```

---

### File .gitignore mẫu cho Java ☕

```gitignore
# =============================================
# .gitignore cho dự án Java
# =============================================

# ----- FILE COMPILED -----
# File .class được tạo khi compile
*.class

# ----- THƯ MỤC BUILD -----
target/
build/
out/

# ----- FILE MAVEN/GRADLE -----
.mvn/
!.mvn/wrapper/maven-wrapper.jar
.gradle/

# ----- FILE IDE -----
# Eclipse
.classpath
.project
.settings/

# IntelliJ IDEA
.idea/
*.iml
*.ipr
*.iws

# NetBeans
nbproject/private/
nbbuild/
nbdist/

# ----- FILE LOG -----
*.log
logs/

# ----- FILE HỆ ĐIỀU HÀNH -----
.DS_Store
Thumbs.db
```

---

### File .gitignore CHUNG (dùng cho mọi dự án) 📦

```gitignore
# =============================================
# .gitignore CHUNG - DÙNG CHO MỌI NGÔN NGỮ
# =============================================

# ----- FILE HỆ ĐIỀU HÀNH -----
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Desktop.ini

# ----- THƯ MỤC IDE/EDITOR -----
.vscode/
.idea/
*.swp
*.swo
*~
*.bak

# ----- FILE LOG -----
*.log
logs/

# ----- FILE NHẠY CẢM -----
# QUAN TRỌNG: Không BAO GIờ commit!
.env
.env.*
*.env
config.local.*
secrets.*
*_secret.*
*.key
*.pem

# ----- FILE TẠM THỜI -----
*.tmp
*.temp
*.bak
*.backup
```


### Kiểm tra file nào bị ignore

```bash
# Xem file nào đang bị ignore
git status --ignored
# ==> Hiển thị danh sách tất cả file/thư mục đang bị ignore (không được tracked).
# --ignored: Tùy chọn chỉ hiển thị những file bị ignore theo .gitignore
# Kết quả:
# On branch main
# Your branch is up to date with 'origin/main'.
# 
# Ignored files:
#   (use "git add -f <file>..." to include in what will be committed)
#         __pycache__/
#         *.log
#         .env
#         node_modules/
# \u00dd ngh\u0129a:
# - Ignored files: Section liệt kê các file được ignore
# - __pycache__/: Thư mục Python cache đang bị ignore
# - *.log: Tất cả file .log đang bị ignore
# - .env: File biến môi trường đang bị ignore
# - node_modules/: Thư mục npm đang bị ignore
# Hữu ích để xác nhận .gitignore hoạt động đúng.

# Kiểm tra 1 file cụ thể có bị ignore không
git check-ignore -v <filename>
# ==> Kiểm tra xem 1 file cụ thể có bị ignore không v vì sao (bị quy tắc nào ignore).
# -v: Verbose - hiển thị chi tiết (thông báo rule nào ignore file)
# <filename>: Tên file cần kiểm tra (ví dụ: config.local.json)
# Kết quả nếu file bị ignore:
# .gitignore:15:config.local.*     config.local.json
# \u00dd ngh\u0129a:
# - .gitignore: File quy tắc
# - 15: Dòng 15 trong .gitignore (nơi viết quy tắc)
# - config.local.*: Quy tắc (pattern) ignore file này
# - config.local.json: Tên file bị ignore
# K\u1ebft qu\u1ea3 nếu file KHÔNG bị ignore:
# (kh\u00f4ng c\u00f3 output)
# \u00dd ngh\u0129a: File không bị ignore, sẽ được tracked bình thường.
# V\u00ed dụ: git check-ignore -v main.py (check xem main.py c\u00f3 bị ignore không)
```

### Lưu ý quan trọng

> ⚠️ **File đã commit trước khi thêm vào .gitignore sẽ KHÔNG tự động bị bỏ qua!**

Để bỏ theo dõi file đã commit:
```bash
# Bước 1: Thêm pattern vào .gitignore
echo "*.log" >> .gitignore
# ==> Thêm pattern "*.log" vào cuối file .gitignore.
# echo: Lệnh in text ra màn hình (hoặc vào file nếu có >>)
# "*.log": Pattern - bỏ qua tất cả file có đuôi .log
# >>: Toán tử append (thêm vào cuối file mà không xóa nội dung cũ)
# .gitignore: Tên file đích
# Kết quả: Không có output nếu thành công.
# Ý nghĩa: Pattern "*.log" được thêm vào .gitignore, những file .log mới sẽ bị ignore.
# Lưu ý: File .log ĐÃ commit trước đó sẽ VẪN ĐƯỢC TRACKED (vẫn ở Git)!

# Bước 2: Xóa file khỏi git (nhưng giữ file trên máy)
git rm --cached <filename>
# ==> Xóa file khỏi Git tracking (staging area) nhưng giữ lại file trên đĩa cứng.
# --cached: Chỉ xóa khỏi Git, KHÔNG xóa file trên máy
# <filename>: Tên file cần xóa khỏi tracking (ví dụ: config.local.json)
# Kết quả:
# rm 'config.local.json'
# Ý nghĩa:
# - Git sẽ không còn theo dõi file này
# - File vẫn tồn tại trên máy (không bị xóa)
# - Lần commit tiếp theo sẽ ghi nhận "file bị xóa khỏi repo"
# Hữu ích khi bạn muốn bỏ file nhạy cảm ra khỏi Git nhưng vẫn giữ nó locally.

# Hoặc xóa cả thư mục
git rm -r --cached <folder>/
# ==> Xóa toàn bộ thư mục và nội dung khỏi Git tracking (nhưng giữ trên máy).
# -r: Recursive - xóa thư mục và tất cả file con bên trong
# --cached: Chỉ xóa khỏi Git, không xóa file trên máy
# <folder>/: Tên thư mục (ví dụ: node_modules/)
# Kết quả:
# rm 'node_modules/package1/index.js'
# rm 'node_modules/package2/helper.js'
# ...
# Ý nghĩa:
# - Tất cả file trong node_modules/ sẽ bị xóa khỏi Git
# - Thư mục vẫn tồn tại trên máy v có thể dùng bình thường
# - Git sẽ không còn theo dõi file trong thư mục
# Rất hữu ích khi vô tình commit node_modules (rất nặng).

# Bước 3: Commit thay đổi
git commit -m "Remove tracked files that should be ignored"
# ==> Commit để ghi nhận việc xóa file khỏi Git.
# -m: Tùy chọn chỉ định message
# "Remove tracked files that should be ignored": Message mô tả rõ hành động
# Kết quả:
# [main 1a2b3c4] Remove tracked files that should be ignored
#  1 file changed, 0 insertions(+), 1 deletion(-)
#  delete mode 100644 config.local.json
# Ý nghĩa:
# - 1 file changed: 1 file được thay đổi (xóa khỏi repo)
# - delete mode: File bị xóa khỏi Git
# - config.local.json: File cụ thể bị xóa
# Sau commit này, file config.local.json sẽ không còn ở lịch sử commit mới.
# Lưu ý: Lịch sử cũ vẫn còn file này (Git lưu tất cả), nhưng các commit mới sẽ không có.

# ========== QUY TRÌNH HOÀN CHỈNH ==========
# 1. echo "*.log" >> .gitignore          # Thêm pattern ignore
# 2. git status                          # Xem file cần xóa
# 3. git rm --cached debug.log           # Xóa khỏi Git
# 4. git commit -m "Stop tracking logs"  # Commit thay đổi
# 5. git push                            # Đẩy lên GitHub
# Sau 5 bước này, file .log sẽ không còn ở repo nhưng vẫn ở máy local.
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
