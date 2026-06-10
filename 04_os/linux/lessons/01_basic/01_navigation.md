# 🎓 Linux Navigation — `pwd`, `ls`, `cd`

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 21/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Terminal là gì](../../../../01_foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md)\
> **Áp dụng cho:** Linux • macOS (BSD Unix, lệnh giống Linux) • WSL trên Windows • Git Bash trên Windows

> 🎯 *Học 3 lệnh nền tảng của Linux/Unix — `pwd`, `ls`, `cd`. Đây là **lệnh POSIX**, dùng được trên Linux, Mac, WSL, Git Bash. Windows native (CMD/PowerShell) có lệnh khác — xem [windows-shell-commands](../../../windows/) (chưa có).*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng `pwd` xem đang đứng ở đâu
- [ ] Dùng `ls` (+ flag `-l`, `-a`, `-la`) liệt kê file/folder
- [ ] Dùng `cd` di chuyển — kể cả các shortcut `..`, `~`, `-`
- [ ] Hiểu **absolute path** (`/Users/user`) vs **relative path** (`./Desktop`)
- [ ] Navigate folder bất kỳ trong < 5 giây

---

## Tình huống — terminal mới mở, bạn không biết đang ở đâu

Bạn mở terminal lần đầu. Prompt hiện:

```
user@laptop ~ %
```

Câu hỏi đầu tiên:
1. **Đang ở folder nào?** — `~` là cái gì? File project của bạn ở đâu?
2. **Folder này có gì?** — File `requirements.txt` có ở đây không? `.env` thì sao?
3. **Làm sao di chuyển sang folder khác?** — vd vào `Desktop/myapp/`

3 câu hỏi này được trả lời bằng đúng **3 lệnh**: `pwd`, `ls`, `cd`. Đây là **bộ 3 cốt lõi** của Linux/Unix — chưa thành thạo thì chưa nói được biết terminal.

---

## 1️⃣ Vì sao 3 lệnh này CỰC KỲ quan trọng?

`pwd` + `ls` + `cd` là **bộ 3 cốt lõi** của terminal. Mọi lệnh khác (tạo file, chạy script, install package...) đều dùng filesystem → bạn phải biết:

1. **Đang ở đâu** (`pwd`) — không biết → chạy lệnh có thể xóa nhầm folder
2. **Có gì xung quanh** (`ls`) — không biết → không biết file nào tồn tại
3. **Đi đến đâu khác** (`cd`) — không biết → kẹt 1 chỗ, không làm được gì

→ Học terminal mà chưa thành thạo 3 lệnh này = chưa biết terminal.

---

## 2️⃣ Trước hết — Filesystem Linux trông như thế nào?

Trước khi học lệnh, hiểu cấu trúc filesystem.

**🪞 Ẩn dụ**: *Filesystem giống như **cây thư mục lồng nhau** — gốc là `/` (root), các nhánh là folder, lá là file. Bạn luôn "đứng ở 1 nhánh" và di chuyển lên/xuống/ngang.*

```
/                          ← root (Mac/Linux)
├── Users/
│   └── user/               ← home folder của user (= ~)
│       ├── Desktop/
│       ├── Documents/
│       └── projects/
│           └── my-app/    ← giả sử bạn đang đứng ở đây
└── etc/                   ← config files hệ thống
```

### Path — đường dẫn tới 1 vị trí

2 loại path:

| Loại | Format | Ví dụ | Đặc điểm |
|---|---|---|---|
| **Absolute** (tuyệt đối) | Bắt đầu bằng `/` | `/Users/user/Desktop` | Hoạt động ở mọi nơi — không phụ thuộc đang đứng đâu |
| **Relative** (tương đối) | Không bắt đầu bằng `/` | `./Desktop` hoặc `../etc` | Phụ thuộc folder hiện tại |

**Ký hiệu đặc biệt**:

| Ký hiệu | Ý nghĩa |
|---|---|
| `/` | Root (cao nhất) |
| `~` | Home folder của user hiện tại (Mac: `/Users/<user>`, Linux: `/home/<user>`) |
| `.` | Folder hiện tại |
| `..` | Folder cha (lùi 1 cấp) |
| `-` | Folder vừa rời đi (dùng với `cd`) |

> 💡 Diagram filesystem đã rõ, giờ ta thử 3 lệnh thực tế.

---

## 3️⃣ Bắt tay làm — 3 lệnh cốt lõi

### 🛠️ 3.1 `pwd` — Tôi đang ở đâu?

`pwd` = **Print Working Directory**.

```bash
pwd
```

Output mẫu:

```
/Users/user
```

→ Bạn đang ở folder `/Users/user` (home folder trên Mac). Trên Linux có thể là `/home/user`. Trên Windows Git Bash: `/c/Users/user`.

> 💡 **Path trên Mac/Linux dùng `/` (forward slash)**. Windows native dùng `\` nhưng Git Bash convert thành `/`.

### 🛠️ 3.2 `ls` — Folder này có gì?

`ls` = **List**.

#### Cơ bản

Gõ `ls` không tham số → liệt kê tên file/folder ngay trong folder hiện tại:

```bash
ls
```

```
Desktop  Documents  Downloads  Pictures  projects
```

#### Chi tiết hơn — `ls -l`

Hiển thị: quyền truy cập, kích thước, ngày sửa, owner.

```bash
ls -l
```

```
drwxr-xr-x  5 user  staff   160 May 16 10:00 Desktop
drwxr-xr-x  8 user  staff   256 May 15 14:30 Documents
-rw-r--r--  1 user  staff   542 May 16 09:00 my-note.txt
```

| Ký hiệu đầu | Ý nghĩa |
|---|---|
| `d` | Folder (directory) |
| `-` | File thường |
| `l` | Symbolic link |

> 💡 Phần `drwxr-xr-x` là **permissions** — sẽ học chi tiết ở bài [Users & Permissions](../02_intermediate/00_users-and-permissions.md).

#### Show file ẩn — `ls -a`

File bắt đầu bằng `.` (vd `.git`, `.env`) là **ẩn** — `ls` mặc định không hiển thị.

```bash
ls -a
```

```
.  ..  .bashrc  .git  .ssh  Desktop  Documents
```

#### Kết hợp — `ls -la`

Gộp `-l` (chi tiết) + `-a` (cả file ẩn) — đây là **lệnh `ls` dùng nhiều nhất hàng ngày**:

```bash
ls -la
```

→ Vừa chi tiết, vừa show file ẩn. **Lệnh `ls` dùng nhiều nhất**.

#### Sort theo size — `ls -lhS`

Khi muốn tìm file/folder chiếm disk nhiều nhất, thêm `-h` (human-readable: KB/MB thay byte) + `-S` (sort theo size giảm dần):

```bash
ls -lhS
```

- `-l` chi tiết
- `-h` human-readable (KB, MB thay byte)
- `-S` sort theo size giảm dần

### 🛠️ 3.3 `cd` — Đi đến folder khác

`cd` = **Change Directory**.

#### Đi thẳng

```bash
cd Desktop
pwd
```

```
/Users/user/Desktop
```

→ Đã chuyển vào `Desktop`. Giờ `ls` sẽ liệt kê thứ trong Desktop, không phải home folder.

#### Shortcut quan trọng

| Lệnh | Đi đâu |
|---|---|
| `cd ~` hoặc `cd` (không gì) | Về home folder |
| `cd ..` | Lên 1 cấp (folder cha) |
| `cd ../..` | Lên 2 cấp |
| `cd ../../..` | Lên 3 cấp |
| `cd /` | Về root (cao nhất) |
| `cd -` | Về folder trước đó (toggle như "Back" của browser) |
| `cd ~/Desktop` | Tuyệt đối — đi thẳng tới Desktop |
| `cd ./projects` | Tương đối — `./projects` từ folder hiện tại |

> 💡 *`..` và `~` là chìa khoá navigate nhanh. `..` = "lùi", `~` = "về nhà".*

#### Ví dụ chuỗi điều hướng

```bash
pwd                          # /Users/user
cd Desktop                   # vào Desktop
cd ../Documents              # ra Desktop → vào Documents (qua home)
cd ../../etc                 # ra Documents → ra home → vào /etc (system folder)
cd ~                         # về home
cd -                         # toggle về /etc (chỗ vừa rời)
cd -                         # toggle về home (chỗ vừa rời lần nữa)
```

### 🛠️ 3.4 Combine: tìm file Python trong project

Đây là 1 use case thực tế:

```bash
cd ~/projects/my-app         # vào project
pwd                          # verify đang đúng chỗ
ls -la                       # xem có gì
ls -la src/                  # xem chi tiết folder src
cd src
ls *.py                      # chỉ liệt kê file .py trong src
```

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Case-sensitive trên Mac/Linux

```bash
cd desktop   # ❌ KHÔNG vào được (folder tên "Desktop", D viết hoa)
cd Desktop   # ✅
```

- **Lý do**: Linux + Mac (filesystem mặc định) case-sensitive. Windows case-insensitive.
- **Cách tránh**: dùng **Tab autocomplete** — gõ `cd De<Tab>` shell tự complete đúng case.

### ❌ Cạm bẫy: Path có khoảng trắng

```bash
cd My Folder/   # ❌ thực ra cd "My" rồi báo lỗi
```

- **Cách tránh**: bọc trong ngoặc kép hoặc escape:
  ```bash
  cd "My Folder/"
  cd My\ Folder/
  ```
- **Tốt hơn**: đặt tên folder không có space (`my-folder/`).

### ❌ Cạm bẫy: Quên `cd` ra → chạy lệnh sai chỗ

```bash
# Tưởng đang ở /Users/user/projects, thực ra ở /
ls          # output toàn folder hệ thống — KHÔNG phải projects
rm -r tmp   # xóa /tmp — có thể thảm họa!
```

- **Cách tránh**: **luôn `pwd` trước** khi chạy lệnh phá hoại (`rm`, `mv` lớn).

### ✅ Best practice: Tab autocomplete

Khi gõ tên file/folder dài, gõ vài ký tự đầu rồi nhấn `Tab` — shell tự complete.

```bash
cd Doc<Tab>
```

→ Tự thành `cd Documents/`. Nếu nhiều match, `Tab Tab` để xem list.

### ✅ Best practice: Lịch sử lệnh

- `↑` (up arrow) — gọi lại lệnh trước
- `↓` (down arrow) — lệnh sau
- `Ctrl + R` — search lịch sử (gõ keyword, Enter)

### ✅ Best practice: `ls` ngay sau `cd`

```bash
cd ~/projects
ls          # luôn ls sau cd để biết folder có gì
```

→ Habit này giúp tránh nhầm folder + nhanh biết next action.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** `cd ../../etc` đi đâu (giả sử đang ở `/Users/user/projects/my-app`)?

<details>
<summary>💡 Đáp án</summary>

`/etc`.

Đường đi:
- `..` → `/Users/user/projects`
- `..` → `/Users/user`
- `etc` (relative) → `/Users/user/etc`?

❌ Sai! `etc` ở root, không phải trong home. Đáp án đúng:

- `..` → `/Users/user/projects`
- `..` → `/Users/user`
- `etc` → `/Users/user/etc` (path TƯƠNG ĐỐI, không có `/`)

Nếu muốn đến `/etc` (system folder), phải dùng absolute: `cd /etc`.

→ Bài học: chú ý absolute (bắt đầu `/`) vs relative.

</details>

**Q2.** Khác nhau giữa `ls`, `ls -l`, `ls -a`, `ls -la`?

<details>
<summary>💡 Đáp án</summary>

- `ls` — chỉ tên, không file ẩn
- `ls -l` — chi tiết (permissions, size, date), không file ẩn
- `ls -a` — chỉ tên, có file ẩn
- `ls -la` — chi tiết + có file ẩn (dùng nhiều nhất)

`-l` = long format. `-a` = all (gồm ẩn).

</details>

**Q3.** Đang ở `/Users/user`, sau khi chạy chuỗi sau, đứng ở đâu?
```bash
cd ~/Desktop
cd ../Documents
cd ../../etc
cd -
```

<details>
<summary>💡 Đáp án</summary>

Bước 1: `cd ~/Desktop` → `/Users/user/Desktop`\
Bước 2: `cd ../Documents` → `/Users/user/Documents` (../ lùi từ Desktop về home)\
Bước 3: `cd ../../etc` → `/etc`? 

❌ Phân tích kỹ: `../..` từ `/Users/user/Documents`:
- `..` → `/Users/user`
- `..` → `/Users`
- `etc` → `/Users/etc` ❌

Đáp án đúng: `/Users/etc` (relative path, không phải `/etc`).

Bước 4: `cd -` → quay lại folder trước = `/Users/user/Documents`.

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Lệnh | Mục đích |
|---|---|
| `pwd` | In folder hiện tại |
| `ls` | List file/folder (không ẩn) |
| `ls -l` | List chi tiết |
| `ls -a` | List + file ẩn |
| `ls -la` | List chi tiết + ẩn (dùng nhiều) |
| `ls -lhS` | List sort theo size, human-readable |
| `cd <path>` | Đi tới folder |
| `cd ~` | Về home |
| `cd ..` | Lên 1 cấp |
| `cd ../..` | Lên 2 cấp |
| `cd /` | Về root |
| `cd -` | Toggle folder vừa rời |
| `Tab` | Autocomplete |
| `Tab Tab` | Xem list match |
| `↑ / ↓` | Lịch sử lệnh |
| `Ctrl + R` | Search lịch sử |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| EN | VN | Giải thích |
|---|---|---|
| Filesystem | Hệ thống file | Cấu trúc cây folder/file của OS |
| Path | Đường dẫn | Vị trí 1 file/folder, vd `/Users/user` |
| Absolute path | Đường dẫn tuyệt đối | Bắt đầu bằng `/`, không phụ thuộc folder hiện tại |
| Relative path | Đường dẫn tương đối | Không bắt đầu bằng `/`, phụ thuộc folder hiện tại |
| Working directory | Thư mục đang làm việc | Folder bạn đang đứng (xem bằng `pwd`) |
| Parent directory | Thư mục cha | Folder chứa folder hiện tại, ký hiệu `..` |
| Home directory | Thư mục home | Folder cá nhân của user, ký hiệu `~` |
| Root | Gốc | Folder cao nhất hệ thống, ký hiệu `/` |
| Hidden file | File ẩn | File bắt đầu bằng `.`, không hiện trong `ls` mặc định |
| Tab completion | Tự hoàn thành | Nhấn Tab để shell tự gợi ý phần còn lại |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [What is Terminal](../../../../01_foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md) (intro về terminal-as-tool ở 02_tools) |
| ➡️ Bài tiếp | [02_file-operations.md](./02_file-operations.md) — mkdir, touch, cp, mv, rm |
| 🔗 Liên quan | [Text Processing Advanced](../02_intermediate/04_text-processing-advanced.md) — `grep`, `sed`, `awk` |
| 🧭 Roadmap | [Zero to Coder — Stage 1](../../../../00_roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-tối-thiểu-2-3-tuần) |

### 🌐 Tài nguyên tham khảo khác

- [Linux Path tutorial](https://www.redhat.com/sysadmin/linux-path-absolute-relative) — RedHat
- [`ls` man page](https://man7.org/linux/man-pages/man1/ls.1.html) — tất cả flag

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (16/05/2026)** — Bản đầu tiên — lesson dạy navigation `pwd`/`ls`/`cd`.
- **v1.1.0 (16/05/2026)** — Đặt vào `04_os/linux/lessons/01_basic/` (lệnh OS). Đổi tiêu đề "Navigation" → "Linux Navigation". Thêm ghi chú cross-OS (Mac/WSL/Git Bash dùng được, Windows native khác).
- **v2.0.0 (21/05/2026)** — Mở bài bằng tình huống mở terminal lần đầu với 3 câu hỏi cụ thể (đang ở đâu, có gì, đi đâu). Đặt lại tiêu đề các phần cho tự nhiên hơn. Nội dung kỹ thuật không đổi.
- **v2.1.0 (24/05/2026)** — Thêm 3 lời dẫn trước ví dụ (ls cơ bản, ls -la, ls -lhS).
