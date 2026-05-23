# 🎓 Linux Navigation — `pwd`, `ls`, `cd`

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 21/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút (chưa tính thực hành)\
> **Prerequisites:** [Terminal là gì](../../../../01_Foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md)\
> **Áp dụng cho:** Linux • macOS (BSD Unix, lệnh giống Linux) • WSL trên Windows • Git Bash trên Windows

> 🎯 *Học 3 lệnh nền tảng của Linux/Unix — `pwd`, `ls`, `cd`. Đây là **lệnh POSIX**, dùng được trên Linux, Mac, WSL, Git Bash. Windows native (CMD/PowerShell) có lệnh khác — xem [windows-shell-commands](../../../windows/) (chưa có).*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng `pwd` xem đang đứng ở đâu
- [ ] Dùng `ls` (+ flag `-l`, `-a`, `-la`) liệt kê file/folder
- [ ] Dùng `cd` di chuyển — kể cả các shortcut `..`, `~`, `-`
- [ ] Hiểu **absolute path** (`/Users/rom`) vs **relative path** (`./Desktop`)
- [ ] Navigate folder bất kỳ trong < 5 giây

---

## Tình huống — terminal mới mở, bạn không biết đang ở đâu

Bạn mở terminal lần đầu. Prompt hiện:

```
rom@MacBook ~ %
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
│   └── rom/               ← home folder của user "rom" (= ~)
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
| **Absolute** (tuyệt đối) | Bắt đầu bằng `/` | `/Users/rom/Desktop` | Hoạt động ở mọi nơi — không phụ thuộc đang đứng đâu |
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
/Users/rom
```

→ Bạn đang ở folder `/Users/rom` (home folder trên Mac). Trên Linux có thể là `/home/rom`. Trên Windows Git Bash: `/c/Users/rom`.

> 💡 **Path trên Mac/Linux dùng `/` (forward slash)**. Windows native dùng `\` nhưng Git Bash convert thành `/`.

### 🛠️ 3.2 `ls` — Folder này có gì?

`ls` = **List**.

#### Cơ bản

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
drwxr-xr-x  5 rom  staff   160 May 16 10:00 Desktop
drwxr-xr-x  8 rom  staff   256 May 15 14:30 Documents
-rw-r--r--  1 rom  staff   542 May 16 09:00 my-note.txt
```

| Ký hiệu đầu | Ý nghĩa |
|---|---|
| `d` | Folder (directory) |
| `-` | File thường |
| `l` | Symbolic link |

> 💡 Phần `drwxr-xr-x` là **permissions** — sẽ học chi tiết ở bài [02_file-permissions.md](./02_file-operations.md) (sắp có).

#### Show file ẩn — `ls -a`

File bắt đầu bằng `.` (vd `.git`, `.env`) là **ẩn** — `ls` mặc định không hiển thị.

```bash
ls -a
```

```
.  ..  .bashrc  .git  .ssh  Desktop  Documents
```

#### Kết hợp — `ls -la`

```bash
ls -la
```

→ Vừa chi tiết, vừa show file ẩn. **Lệnh `ls` dùng nhiều nhất**.

#### Sort theo size — `ls -lhS`

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
/Users/rom/Desktop
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
pwd                          # /Users/rom
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

## 💡 Pitfall & Best practice

### ❌ Pitfall: Case-sensitive trên Mac/Linux

```bash
cd desktop   # ❌ KHÔNG vào được (folder tên "Desktop", D viết hoa)
cd Desktop   # ✅
```

- **Lý do**: Linux + Mac (filesystem mặc định) case-sensitive. Windows case-insensitive.
- **Cách tránh**: dùng **Tab autocomplete** — gõ `cd De<Tab>` shell tự complete đúng case.

### ❌ Pitfall: Path có khoảng trắng

```bash
cd My Folder/   # ❌ thực ra cd "My" rồi báo lỗi
```

- **Cách tránh**: bọc trong ngoặc kép hoặc escape:
  ```bash
  cd "My Folder/"
  cd My\ Folder/
  ```
- **Tốt hơn**: đặt tên folder không có space (`my-folder/`).

### ❌ Pitfall: Quên `cd` ra → chạy lệnh sai chỗ

```bash
# Tưởng đang ở /Users/rom/projects, thực ra ở /
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

## 🧠 Self-check

**Q1.** `cd ../../etc` đi đâu (giả sử đang ở `/Users/rom/projects/my-app`)?

<details>
<summary>💡 Đáp án</summary>

`/etc`.

Đường đi:
- `..` → `/Users/rom/projects`
- `..` → `/Users/rom`
- `etc` (relative) → `/Users/rom/etc`?

❌ Sai! `etc` ở root, không phải trong home. Đáp án đúng:

- `..` → `/Users/rom/projects`
- `..` → `/Users/rom`
- `etc` → `/Users/rom/etc` (path TƯƠNG ĐỐI, không có `/`)

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

**Q3.** Đang ở `/Users/rom`, sau khi chạy chuỗi sau, đứng ở đâu?
```bash
cd ~/Desktop
cd ../Documents
cd ../../etc
cd -
```

<details>
<summary>💡 Đáp án</summary>

Bước 1: `cd ~/Desktop` → `/Users/rom/Desktop`\
Bước 2: `cd ../Documents` → `/Users/rom/Documents` (../ lùi từ Desktop về rom)\
Bước 3: `cd ../../etc` → `/etc`? 

❌ Phân tích kỹ: `../..` từ `/Users/rom/Documents`:
- `..` → `/Users/rom`
- `..` → `/Users`
- `etc` → `/Users/etc` ❌

Đáp án đúng: `/Users/etc` (relative path, không phải `/etc`).

Bước 4: `cd -` → quay lại folder trước = `/Users/rom/Documents`.

</details>

---

## ⚡ Cheatsheet

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

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Filesystem | Hệ thống file | Cấu trúc cây folder/file của OS |
| Path | Đường dẫn | Vị trí 1 file/folder, vd `/Users/rom` |
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
| ⬅️ Bài trước | [What is Terminal](../../../../01_Foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md) (intro về terminal-as-tool ở 02_Tools) |
| ➡️ Bài tiếp | [02_file-operations.md](./02_file-operations.md) — mkdir, touch, cp, mv, rm |
| 🔗 Liên quan | (sẽ có) `04_text-search-and-pipes.md` — `find`, `grep` |
| 🧭 Roadmap | [Zero to Coder — Stage 1](../../../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-tối-thiểu-2-3-tuần) |

### Tài nguyên ngoài

- [Linux Path tutorial](https://www.redhat.com/sysadmin/linux-path-absolute-relative) — RedHat
- [`ls` man page](https://man7.org/linux/man-pages/man1/ls.1.html) — tất cả flag

---

## 📌 Changelog

- **v2.0.0 (21/05/2026)** — Restructure theo writing-style v0.5.1:
  - Mở bằng **tình huống beginner mở terminal lần đầu** với 3 câu hỏi cụ thể (đang ở đâu, có gì, đi đâu)
  - Headers đổi: `1️⃣ (WHY)` / `2️⃣ Filesystem (WHAT)` / `3️⃣ Hands-on (HOW)` → câu hỏi/mô tả tự nhiên ("Vì sao 3 lệnh này CỰC KỲ quan trọng?", "Trước hết — Filesystem Linux trông như thế nào?", "Bắt tay làm — 3 lệnh cốt lõi")
  - Content kỹ thuật KHÔNG đổi
- **v1.1.0 (16/05/2026)** — Move từ `02_Tools/shell/lessons/01_basic/` sang `04_OS/linux/lessons/01_basic/` theo quy ước Blueprint v0.5 §3.2ter (02_Tools KHÔNG chứa lệnh OS). Title đổi "Navigation" → "Linux Navigation". Thêm note cross-OS (Mac/WSL/Git Bash dùng được, Windows native khác).
- **v1.0.0 (16/05/2026)** — Bản đầu tiên — lesson dạy navigation `pwd`/`ls`/`cd`. Tách từ `00_terminal-fundamentals.md` cũ theo quy ước Blueprint v0.4 §3.0 (Intro vs Lesson).
