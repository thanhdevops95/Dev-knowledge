# Linux File Operations — Tạo, đổi, xóa file & folder với `mkdir`, `touch`, `cp`, `mv`, `rm`

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [01_navigation.md](./01_navigation.md)\
> **Áp dụng cho:** Linux • macOS • WSL • Git Bash

> 🎯 *Sau bài navigation, bạn biết "đi đâu". Bài này dạy "làm gì khi đến" — tạo, copy, đổi tên, xóa file/folder. Đặc biệt cảnh báo `rm` vì không có Undo.*

## 🎯 Sau bài này bạn sẽ

- [ ] Tạo folder (`mkdir`) — kể cả nhiều cấp lồng nhau (`mkdir -p`)
- [ ] Tạo file rỗng (`touch`)
- [ ] Copy file/folder (`cp`)
- [ ] Đổi tên / di chuyển (`mv`)
- [ ] Xóa AN TOÀN (`rm`) — biết khi nào cần `-r`, khi nào KHÔNG dùng `-rf`

---

## 1️⃣ Vì sao 5 lệnh này quan trọng (WHY)

Sau khi navigate (`cd`, `ls`, `pwd`), bạn cần **TƯƠNG TÁC** với file/folder. 5 lệnh trong bài là **bộ CRUD cơ bản** cho filesystem:

| CRUD | Lệnh |
|---|---|
| **C**reate | `mkdir` (folder), `touch` (file rỗng) |
| **R**ead | `cat`, `less` (xem [bài 03](./03_view-file-content.md)) |
| **U**pdate | `mv` (đổi tên/di chuyển), text editor (vim, code, ...) |
| **D**elete | `rm` |
| **Copy** | `cp` |

→ Mọi script automation, CI/CD pipeline, tutorial — đều dùng 5 lệnh này.

---

## 2️⃣ Mô hình tinh thần (WHAT)

**🪞 Ẩn dụ**: *5 lệnh này như **5 công cụ trong xưởng**: `mkdir` = đào hố (tạo folder), `touch` = đặt thùng rỗng (file rỗng), `cp` = nhân bản, `mv` = chuyển/dán nhãn lại, `rm` = đốt (không có thùng rác recovery).*

**Quy tắc chung**:
- Lệnh có thể nhận **1 hoặc nhiều** file/folder cùng lúc
- Flag `-r` (recursive) = áp dụng cho cả folder con
- Flag `-i` (interactive) = hỏi xác nhận trước khi làm
- Flag `-v` (verbose) = in ra việc đang làm

> 💡 Tinh thần chung rồi, giờ học từng lệnh chi tiết.

---

## 3️⃣ Hands-on (HOW)

### 🛠️ 3.1 `mkdir` — Tạo folder

`mkdir` = **Make Directory**.

#### Tạo 1 folder

```bash
cd ~/Desktop
mkdir my-first-project
ls
```

```
my-first-project
```

#### Tạo nhiều folder cùng lúc

```bash
mkdir docs src tests
ls
```

```
docs  my-first-project  src  tests
```

#### Tạo folder lồng nhau — `-p`

```bash
mkdir -p projects/python/learning/week-01
```

→ `-p` (parents) bảo `mkdir` tạo cả folder cha nếu chưa có. **Không có `-p`** sẽ báo lỗi nếu folder cha chưa tồn tại.

Verify cấu trúc:

```bash
ls -R projects
```

```
projects:
python

projects/python:
learning

projects/python/learning:
week-01

projects/python/learning/week-01:
```

#### Brace expansion — tạo nhiều folder pattern

```bash
mkdir module-{1..5}
ls
```

```
module-1  module-2  module-3  module-4  module-5
```

→ Cực kỳ hữu ích khi setup project có structure cố định.

### 🛠️ 3.2 `touch` — Tạo file rỗng (hoặc cập nhật timestamp)

```bash
touch hello.txt
ls -la hello.txt
```

```
-rw-r--r--  1 rom  staff  0 May 16 10:30 hello.txt
```

→ File rỗng (0 byte) được tạo. Giờ bạn có thể mở `hello.txt` trong VS Code (`code hello.txt`) để viết nội dung.

#### Tạo nhiều file

```bash
touch a.txt b.txt c.txt
ls
```

#### `touch` trên file đã có = cập nhật timestamp

```bash
touch hello.txt   # file đã có
ls -la hello.txt
```

```
-rw-r--r--  1 rom  staff  0 May 16 10:35 hello.txt
                                    ↑
                              (timestamp mới)
```

→ Sometimes dùng để "force" Make/build system rebuild file đó.

### 🛠️ 3.3 `cp` — Copy

`cp` = **Copy**.

#### Copy file

```bash
cp hello.txt hello-backup.txt
ls
```

```
hello-backup.txt  hello.txt
```

#### Copy vào folder

```bash
mkdir backups
cp hello.txt backups/
ls backups/
```

```
hello.txt
```

#### Copy folder — `-r`

```bash
cp -r projects projects-copy
ls
```

```
projects  projects-copy
```

→ **Bắt buộc `-r`** khi copy folder (cùng tất cả file con). Không có `-r` sẽ báo lỗi.

#### Preserve metadata — `-p`

```bash
cp -p hello.txt hello-archive.txt
```

→ Giữ nguyên timestamp, permissions của file gốc. Hữu ích khi backup.

### 🛠️ 3.4 `mv` — Move / Rename

`mv` = **Move**. **2 chức năng**: chuyển vị trí, hoặc đổi tên (trên Unix, rename = move tại chỗ).

#### Đổi tên

```bash
mv hello.txt greeting.txt
ls
```

```
greeting.txt
```

#### Chuyển vào folder

```bash
mv greeting.txt backups/
ls backups/
```

```
greeting.txt  hello.txt
```

#### Chuyển + đổi tên cùng lúc

```bash
mv backups/greeting.txt archive/welcome.txt
```

→ Vừa di chuyển vừa rename trong 1 lệnh.

> 💡 *Trên Linux/Mac, không có lệnh `rename` riêng cho file thường — dùng `mv`.*

### 🛠️ 3.5 `rm` — Xóa (CỰC KỲ CẨN THẬN)

`rm` = **Remove**. **KHÔNG vào Trash** — xóa vĩnh viễn.

#### Xóa file

```bash
rm hello-backup.txt
ls
```

→ Mất.

#### Xóa nhiều file

```bash
rm a.txt b.txt c.txt
```

#### Xóa folder — phải có `-r`

```bash
rm -r my-first-project
```

→ Xóa folder + tất cả file/folder con bên trong.

#### Interactive — `-i` (an toàn cho beginner)

```bash
rm -i hello.txt
```

```
remove hello.txt? y
```

→ Hỏi xác nhận trước khi xóa. **Khuyên beginner dùng** trong tháng đầu.

#### `-rf` — Lực ép xóa folder (NGUY HIỂM)

```bash
rm -rf old-stuff/
```

- `-r` recursive
- `-f` force (không hỏi gì, không báo lỗi nếu file không tồn tại)

> ⚠️ **CẢNH BÁO**:
> - KHÔNG BAO GIỜ chạy `rm -rf /` — xóa **TOÀN BỘ** ổ cứng
> - KHÔNG BAO GIỜ chạy `rm -rf ~` — xóa toàn bộ home folder (cũng mất tất cả code, photo, document)
> - Trước `rm -rf <path>`, **luôn `ls <path>` đầu** để chắc chắn đang xóa đúng cái
> - Cân nhắc dùng `trash` (cài qua `brew install trash` trên Mac) thay `rm` — có Undo

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: `mkdir` không có `-p` → báo lỗi khi folder cha chưa có

```bash
mkdir a/b/c
# mkdir: a: No such file or directory
```

- **Cách tránh**: dùng `mkdir -p a/b/c` — tạo cả `a` và `b` nếu chưa có.

### ❌ Pitfall: `cp` đè file đích không hỏi (silent overwrite)

```bash
cp source.txt dest.txt    # dest.txt đã có → bị đè không cảnh báo
```

- **Cách tránh**: dùng `cp -i` (interactive) → hỏi trước khi đè:
  ```bash
  cp -i source.txt dest.txt
  # overwrite dest.txt? y/n
  ```
- **Best**: alias trong `.zshrc`/`.bashrc`:
  ```bash
  alias cp='cp -i'
  alias mv='mv -i'
  alias rm='rm -i'
  ```

### ❌ Pitfall: `rm *` trong folder lớn (đặc biệt nguy hiểm)

```bash
rm *   # xóa MỌI file trong folder hiện tại
```

- **Triệu chứng**: xóa nhầm file quan trọng, không undo
- **Cách tránh**:
  - Luôn `ls` trước để biết `*` match gì
  - Dùng `rm -i *` để hỏi từng file
  - Tốt nhất: `rm` từng file rõ ràng

### ❌ Pitfall: `rm -rf` với biến chưa định nghĩa

Đây là 1 trong những **bug huyền thoại** đã xóa server thật:

```bash
TARGET=""
rm -rf $TARGET/*   # khi TARGET rỗng → rm -rf /* — XÓA CẢ ROOT
```

- **Cách tránh**:
  - Trong script: `set -u` để báo lỗi khi dùng biến chưa định nghĩa
  - Quote biến: `rm -rf "${TARGET:?}"/*` — `${VAR:?}` báo lỗi nếu rỗng

### ✅ Best practice: Cài `trash` thay `rm`

Trên Mac:

```bash
brew install trash
trash hello.txt   # vào Trash, có thể restore
```

Trên Linux:

```bash
sudo apt install trash-cli
trash hello.txt
```

→ An toàn hơn, đặc biệt khi đang học.

### ✅ Best practice: Dry-run trước `rm -rf`

Trước khi xóa nhiều file:

```bash
ls -la old-stuff/    # XEM trước có gì
rm -rf old-stuff/    # XÓA sau khi chắc
```

### ✅ Best practice: Brace expansion trong tạo file/folder

```bash
mkdir -p projects/{frontend,backend,database}/{src,tests,docs}
```

→ Tạo 9 folder lồng nhau trong 1 lệnh. Cực nhanh khi setup project.

---

## 🧠 Self-check

**Q1.** Sự khác nhau giữa `cp file.txt copy.txt` và `cp -r folder copy-folder`?

<details>
<summary>💡 Đáp án</summary>

- `cp file.txt copy.txt` — copy 1 file. KHÔNG cần `-r`.
- `cp -r folder copy-folder` — copy folder + toàn bộ nội dung bên trong. **BẮT BUỘC `-r`** (recursive).

Không có `-r` khi copy folder → báo lỗi: `cp: folder is a directory (not copied)`.

</details>

**Q2.** Bạn cần tạo cấu trúc folder sau, trong 1 lệnh duy nhất:
```
project/
├── src/
├── tests/
└── docs/
    └── api/
```

<details>
<summary>💡 Đáp án</summary>

```bash
mkdir -p project/{src,tests,docs/api}
```

Phân tích:
- `-p` để tạo cả `project` folder cha
- `{src,tests,docs/api}` = brace expansion → 3 folder: `src`, `tests`, `docs/api`
- `docs/api` tự tạo cả `docs` lẫn `api` con

</details>

**Q3.** Tại sao `rm -rf /` cực kỳ nguy hiểm? Và bạn sẽ dùng cờ gì để an toàn hơn?

<details>
<summary>💡 Đáp án</summary>

- `rm -rf /` xóa **toàn bộ filesystem** từ root xuống — mọi file/folder/OS/app/data. Không có Undo. Một số distro chặn bằng cờ `--preserve-root` nhưng không nên dựa vào.

- An toàn hơn:
  - `rm -i` — hỏi xác nhận từng file
  - Cài `trash` → file vào Trash, restore được
  - Trong script: `set -u` + quote biến `"${VAR:?}"` để báo lỗi khi biến rỗng

</details>

---

## ⚡ Cheatsheet

| Lệnh | Mục đích |
|---|---|
| `mkdir <name>` | Tạo folder |
| `mkdir -p a/b/c` | Tạo nhiều cấp lồng |
| `mkdir mod-{1..5}` | Tạo 5 folder dùng brace expansion |
| `touch <file>` | Tạo file rỗng / update timestamp |
| `cp <src> <dst>` | Copy file |
| `cp -r <src> <dst>` | Copy folder (recursive) |
| `cp -i <src> <dst>` | Copy + hỏi trước khi đè |
| `mv <src> <dst>` | Move / rename |
| `rm <file>` | Xóa file |
| `rm -i <file>` | Xóa file + hỏi (an toàn beginner) |
| `rm -r <folder>` | Xóa folder |
| `rm -rf <folder>` | Force xóa folder (KHÔNG hỏi) |
| `trash <file>` | Xóa vào Trash (cần cài) |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Recursive | Đệ quy | Áp dụng cho cả folder con (cờ `-r`) |
| Interactive | Tương tác | Hỏi xác nhận trước khi làm (cờ `-i`) |
| Force | Cưỡng chế | Không hỏi, bỏ qua lỗi (cờ `-f`) |
| Brace expansion | Mở rộng dấu ngoặc | Cú pháp `{a,b,c}` hoặc `{1..5}` shell tự sinh nhiều phiên bản |
| Glob | Wildcard | `*` match tên file, `?` match 1 ký tự, `[abc]` match a/b/c |
| Timestamp | Dấu thời gian | Thời điểm file được tạo/sửa/access |
| In-place | Tại chỗ | Sửa file trực tiếp không tạo bản sao |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [01_navigation.md](./01_navigation.md) |
| ➡️ Bài tiếp | [03_view-file-content.md](./03_view-file-content.md) — cat, less, head, tail |
| 🔗 Liên quan | (sẽ có) `06_file-permissions.md` — chmod, chown |
| 🧭 Roadmap | [Zero to Coder — Stage 1](../../../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-cơ-bản-2-3-tuần) |

### Tài nguyên ngoài

- [Linux File Operations](https://linuxize.com/post/basic-linux-commands/) — tutorial chi tiết
- [Brace Expansion Tutorial](https://www.linuxjournal.com/content/bash-brace-expansion) — patterns nâng cao

---

## 📌 Changelog

- **v1.1.0 (16/05/2026)** — Move từ `02_Tools/shell/` sang `04_OS/linux/` theo Blueprint v0.5 §3.2ter. Title đổi "File Operations" → "Linux File Operations".
- **v1.0.0 (16/05/2026)** — Bản đầu tiên — lesson `mkdir`/`touch`/`cp`/`mv`/`rm` với hands-on + 4 pitfall + 4 best practice.
