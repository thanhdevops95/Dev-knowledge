# 🎓 bạn bắt tay với Git — Tạo repo đầu tiên

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~20 phút\
> **Prerequisites:** [What is Git](./00_what-is-git.md), đã [cài Git](../../setup/git.md) + config xong

> 🎯 *Tiếp nối bài intro — bạn đọc xong, mở terminal lần đầu. Bài này dạy 4 lệnh cốt lõi (`init`, `add`, `commit`, `log`) qua project thực tế của bạn. Cuối bài bạn có repo local đầu tiên với 2-3 commit lịch sử.*

## 🎯 Sau bài này bạn sẽ

- [ ] Tạo repo Git với `git init`
- [ ] Đọc output của `git status` (3 trạng thái: untracked / modified / staged)
- [ ] Stage file bằng `git add`
- [ ] Tạo commit với `git commit -m "msg"`
- [ ] Xem lịch sử bằng `git log`
- [ ] Hiểu file `.gitignore` — và tránh push nhầm `.env` lên GitHub

---

## Tình huống — bạn mở terminal lần đầu

Bạn vừa đọc xong [bài intro về Git](./00_what-is-git.md). Sếp dặn *"sáng mai phải có Git tracking project."* Bạn ngồi xuống bàn, thấy folder `myapp/` đã code 1 tuần — có 5 file Python + 1 file `.env` chứa API key.

Bạn có 3 câu hỏi:
1. **Bắt đầu từ đâu?** Folder `myapp/` chưa phải Git repo. Phải làm gì để Git "biết" project này?
2. **Phải commit MỌI file cũ không?** Hay chỉ commit từ giờ trở đi?
3. **File `.env` có bí mật** — commit lên là leak. Làm sao loại?

Bài này trả lời cả 3 câu — qua đúng các lệnh bạn sẽ gõ.

> 💡 4 lệnh trong bài (`init`, `status`, `add`, `commit`) là **80% Git daily**. Bạn sẽ gõ lặp lại hàng chục lần mỗi ngày suốt sự nghiệp.

---

## 1️⃣ Vậy mỗi file trong Git ở trạng thái nào?

Trước hands-on, hiểu **4 trạng thái** mà 1 file có thể ở trong Git:

```mermaid
stateDiagram-v2
    [*] --> Untracked: file mới
    Untracked --> Staged: git add
    Staged --> Committed: git commit
    Committed --> Modified: edit file
    Modified --> Staged: git add
    Modified --> Committed: git commit -a
    Staged --> Unmodified: (đã commit, không sửa)
    Unmodified --> Modified: edit file
```

| Trạng thái | Ý nghĩa | `git status` show |
|---|---|---|
| **Untracked** | File mới, git chưa biết | `Untracked files:` |
| **Staged** | Đã `git add`, sẵn sàng commit | `Changes to be committed:` |
| **Modified** | File đã track, có sửa, chưa staged | `Changes not staged for commit:` |
| **Unmodified** | Đã commit, không có thay đổi | (không hiển thị) |

> 💡 *Hiểu 4 trạng thái này = đọc `git status` được = không bị lạc khi học Git.*

---

## 2️⃣ Bắt tay làm cùng bạn — Tạo repo + commit đầu tiên

> 💡 Mình làm cùng bạn. Mở terminal, gõ theo từng lệnh dưới đây. Không skip — mỗi lệnh dạy 1 ý.

### 🛠️ 2.1 Tạo project + init Git

```bash
cd ~/Desktop
mkdir my-first-git-project
cd my-first-git-project
```

Khởi tạo Git repo:

```bash
git init
```

Output:

```
Initialized empty Git repository in /Users/user/Desktop/my-first-git-project/.git/
```

→ Git tạo folder ẩn `.git/` chứa toàn bộ database. **Đây là folder duy nhất biến project thành "Git repo"**.

Verify:

```bash
ls -la
```

```
.git    ← folder ẩn, chứa database Git
```

> ⚠️ **KHÔNG xóa `.git/`** — xóa = mất toàn bộ lịch sử commits!

### 🛠️ 2.2 `git status` lần đầu

```bash
git status
```

Output:

```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

→ Repo trống, chưa có file. Branch mặc định = `main` (do config `init.defaultBranch main` ở [setup §5](../../setup/git.md#5️⃣-cấu-hình-ban-đầu-bắt-buộc-trước-khi-commit)).

### 🛠️ 2.3 Tạo file đầu tiên

```bash
echo "# My First Git Project" > README.md
echo "print('Hello Git!')" > hello.py
ls
```

```
README.md  hello.py
```

`git status` lại:

```bash
git status
```

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md
        hello.py

nothing added to commit but untracked files present
```

→ 2 file **untracked** — git chưa theo dõi.

### 🛠️ 2.4 Stage file — `git add`

Stage 1 file:

```bash
git add README.md
git status
```

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        hello.py
```

→ `README.md` giờ **staged**. `hello.py` vẫn untracked.

Stage tất cả file còn lại:

```bash
git add .       # . = mọi file trong folder hiện tại
git status
```

```
Changes to be committed:
        new file:   README.md
        new file:   hello.py
```

→ Cả 2 file đều staged.

> 💡 *`git add .` rất tiện nhưng ⚠️ stage MỌI file (kể cả file nhạy cảm như `.env`). Dùng `git add <file>` cụ thể khi muốn chính xác. Xem **§3 `.gitignore`** bên dưới để bảo vệ.*

### 🛠️ 2.5 Commit đầu tiên — `git commit`

```bash
git commit -m "Initial commit"
```

Output:

```
[main (root-commit) a1b2c3d] Initial commit
 2 files changed, 2 insertions(+)
 create mode 100644 README.md
 create mode 100644 hello.py
```

→ Commit `a1b2c3d` đã tạo. `(root-commit)` = commit đầu tiên (không có parent).

Verify:

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

→ **`working tree clean`** = không có thay đổi nào staged hay modified. Mọi thứ đã commit. Đây là trạng thái "sạch sẽ" đẹp nhất khi làm việc với Git.

### 🛠️ 2.6 Xem lịch sử — `git log`

```bash
git log
```

```
commit a1b2c3d4e5f6789abc123 (HEAD -> main)
Author: Dev <dev@example.com>
Date:   Thu May 16 11:30:00 2026

    Initial commit
```

| Phần | Ý nghĩa |
|---|---|
| `commit a1b2c3d...` | SHA hash 40 ký tự — ID duy nhất của commit |
| `(HEAD -> main)` | Branch hiện tại + commit mới nhất |
| `Author` | Tên + email (từ `git config`) |
| `Date` | Thời điểm commit |
| `Initial commit` | Message (từ `-m`) |

#### Format gọn — `--oneline`

```bash
git log --oneline
```

```
a1b2c3d (HEAD -> main) Initial commit
```

→ Mỗi commit 1 dòng. Dùng nhiều khi xem nhanh.

#### Có graph — đẹp khi có nhiều branch sau này

```bash
git log --oneline --graph --decorate
```

### 🛠️ 2.7 Commit thứ 2 — modify file đã track

Sửa `hello.py`:

```bash
echo "print('Welcome to Git')" >> hello.py
cat hello.py
```

```
print('Hello Git!')
print('Welcome to Git')
```

`git status`:

```bash
git status
```

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   hello.py
```

→ `hello.py` giờ **modified** (đã track + sửa, chưa staged).

Xem chính xác sửa gì:

```bash
git diff
```

```
diff --git a/hello.py b/hello.py
index abc..def 100644
--- a/hello.py
+++ b/hello.py
@@ -1 +1,2 @@
 print('Hello Git!')
+print('Welcome to Git')
```

→ `+` = dòng thêm. `-` = dòng bớt. Đây là cách so sánh chuẩn của Git.

Stage + commit:

```bash
git add hello.py
git commit -m "Add welcome message"
```

```
[main b4c5d6e] Add welcome message
 1 file changed, 1 insertion(+)
```

Verify:

```bash
git log --oneline
```

```
b4c5d6e (HEAD -> main) Add welcome message
a1b2c3d Initial commit
```

→ Có 2 commit rồi.

### 🛠️ 2.8 Shortcut — `git commit -am`

Khi sửa file ĐÃ track (không phải file mới), có thể gộp `add` + `commit`:

```bash
echo "print('Day 1')" >> hello.py
git commit -am "Add day 1 log"
```

→ `-a` (all) = stage mọi file modified + tracked. `-m` = message.

> ⚠️ `-a` **KHÔNG** stage file untracked (file mới). File mới phải `git add` riêng.

---

## 3️⃣ Quay lại câu hỏi 3 của bạn — Làm sao tránh commit `.env`?

### Tình huống `.env` của bạn

Bạn có file `.env`:

```
OPENAI_API_KEY=sk-proj-abc123xyz...
DATABASE_URL=postgres://user:password@host:5432/db
```

Nếu bạn làm `git add .` — `.env` sẽ vào staging, rồi commit, rồi `git push` lên GitHub public — **bị hack trong vài phút**. Bots quét GitHub tìm API key 24/7. 

→ Giải pháp: file `.gitignore` — bảo Git **bỏ qua** các file/folder không nên track.

### Vì sao cần `.gitignore`

Có file bạn KHÔNG muốn commit:
- `.env` — credentials (API keys, passwords)
- `node_modules/`, `venv/` — dependencies (cài lại từ `package.json`)
- `*.log` — log files
- `.DS_Store` (macOS), `Thumbs.db` (Windows) — system files
- `__pycache__/` (Python), `.idea/` (JetBrains)
- `dist/`, `build/` — output build (sinh lại từ source)

Nếu KHÔNG có `.gitignore`, `git add .` sẽ lỡ stage credentials → push lên GitHub → bị leak. Cực kỳ phổ biến.

### Tạo `.gitignore`

```bash
cat > .gitignore << 'EOF'
# Credentials
.env
.env.local
*.key

# Dependencies
node_modules/
venv/
__pycache__/
*.pyc

# Build output
dist/
build/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
EOF
```

`git status`:

```bash
git status
```

```
Untracked files:
        .gitignore
```

→ `.gitignore` ITSELF được track (chính nó cần commit). Nhưng các file pattern bên trong sẽ bị Git **bỏ qua**.

Commit:

```bash
git add .gitignore
git commit -m "Add .gitignore"
```

### Template `.gitignore` sẵn

Không cần tự viết — dùng template ở:

- [github.com/github/gitignore](https://github.com/github/gitignore) — official templates cho 100+ ngôn ngữ
- `gitignore.io` (web) — generate combo (vd: "Python + macOS + VS Code")

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Quên config `user.name` / `user.email` trước commit

- **Triệu chứng**: `git commit` báo lỗi `Please tell me who you are`
- **Fix**: chạy 2 lệnh ở [setup §5](../../setup/git.md#5️⃣-cấu-hình-ban-đầu-bắt-buộc-trước-khi-commit)

### ❌ Pitfall: `git add .` commit nhầm file nhạy cảm (`.env`)

- **Triệu chứng**: push lên GitHub → bị leak API key → bị hacker dùng
- **Cách tránh**:
  - Tạo `.gitignore` **NGAY khi `git init`** — trước bất kỳ `git add` nào
  - Dùng `git status` trước `git add .` để xem sẽ stage gì
- **Khắc phục nếu đã lỡ**: phải **rewrite history** (xem bài "Undo" sau) + **rotate key ngay** vì đã leak

### ❌ Pitfall: Commit message vô nghĩa

```
git commit -m "fix"
git commit -m "update"
git commit -m "asdf"
```

- **Triệu chứng**: 6 tháng sau xem `git log` không hiểu commit nào làm gì
- **Cách tránh**: dùng [Conventional Commits](https://www.conventionalcommits.org/):
  ```
  feat: add user authentication
  fix: handle null response from API
  docs: update README installation steps
  refactor: simplify error handling in main()
  ```
- Format: `<type>: <description>` — `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`

### ❌ Pitfall: Commit file quá lớn

- **Triệu chứng**: commit file > 100 MB → GitHub reject push
- **Cách tránh**: không commit binary lớn (video, dataset). Dùng:
  - [Git LFS](https://git-lfs.com/) — Large File Storage cho asset >100 MB
  - `.gitignore` exclude folder data

### ✅ Best practice: Commit thường xuyên, message ngắn gọn

```
✅ feat: add login endpoint
✅ fix: validate email format in signup
✅ test: add unit tests for password hashing
```

→ Commit nhỏ (1-3 file mỗi lần) dễ review + rollback. Tránh commit "bull bull" 50 file 1 lúc.

### ✅ Best practice: Atomic commit (1 commit = 1 thay đổi logic)

Sai:
```
commit: "fix bug + refactor + add tests"
```

Đúng (3 commits):
```
commit 1: "fix: null pointer in login handler"
commit 2: "refactor: extract validation logic"
commit 3: "test: add coverage for login flow"
```

→ Nếu lỡ commit nào sai → revert 1 commit không ảnh hưởng 2 cái còn lại.

### ✅ Best practice: `git status` trước mọi `git add` / `commit`

Habit: trước khi `git add` → `git status` xem có gì. Tránh commit nhầm.

---

## 🧠 Self-check

**Q1.** Sự khác nhau giữa "untracked" và "modified"?

<details>
<summary>💡 Đáp án</summary>

- **Untracked**: file MỚI, chưa từng được `git add` lần nào. Git không biết file này tồn tại.
- **Modified**: file ĐÃ track (đã commit ít nhất 1 lần trước), giờ bạn sửa nó nhưng chưa staged sửa đó.

Test: `git status` show:
- "Untracked files:" → untracked
- "Changes not staged for commit:" → modified

</details>

**Q2.** `git add file.txt` xong, file đó còn ở trong working directory không?

<details>
<summary>💡 Đáp án</summary>

**Có**. `git add` chỉ thêm 1 "bản sao" vào staging area, **không xóa file khỏi working directory**. Bạn vẫn có thể edit `file.txt` tiếp — sau khi `git add` lần nữa, bản mới sẽ thay bản cũ trong staging.

Cụ thể: nếu sau `git add file.txt` bạn sửa `file.txt` tiếp, `git status` sẽ show:
```
Changes to be committed:
   modified: file.txt   ← bản đã add
Changes not staged for commit:
   modified: file.txt   ← bản đang sửa
```

→ Cùng 1 file ở 2 trạng thái khác nhau (Staging + Modified).

</details>

**Q3.** Tại sao cần `.gitignore`? Hậu quả nếu không có?

<details>
<summary>💡 Đáp án</summary>

`.gitignore` bảo Git **bỏ qua** các file/folder không nên track: credentials, dependencies, build output, IDE config, OS files...

**Hậu quả không có:**
- 🔥 `git add .` commit nhầm `.env` chứa API key → push GitHub → **bị leak** → hacker dùng → công ty mất tiền / data
- 🐢 Repo bloat với `node_modules/` (có thể GB) → clone chậm
- 💔 Conflict liên tục vì IDE config cá nhân (`.idea/`) khác nhau giữa các dev

→ **Luôn tạo `.gitignore` NGAY sau `git init`**, trước bất kỳ `git add` nào.

</details>

**Q4.** Tại sao SHA hash của 2 commit luôn khác nhau, dù bạn commit cùng 1 file với cùng message?

<details>
<summary>💡 Đáp án</summary>

Vì SHA hash tính từ:
- Nội dung file
- Tree (cấu trúc folder)
- Author, committer, **timestamp**
- Parent commit hash

Timestamp khác nhau giữa 2 lần commit → SHA hash khác nhau. Đây là tính chất quan trọng: mỗi commit có ID DUY NHẤT trong vũ trụ, không trùng lặp.

</details>

---

## ⚡ Cheatsheet

| Lệnh | Mục đích |
|---|---|
| `git init` | Tạo repo trong folder hiện tại |
| `git status` | Xem trạng thái file (untracked/modified/staged) |
| `git status -sb` | Status ngắn + branch |
| `git add <file>` | Stage 1 file |
| `git add .` | Stage mọi file (cẩn thận!) |
| `git add -p` | Stage interactively (chọn từng hunk) |
| `git diff` | Xem thay đổi chưa staged |
| `git diff --staged` | Xem thay đổi đã staged |
| `git commit -m "msg"` | Commit với message |
| `git commit -am "msg"` | Add + commit file đã track (skip file mới) |
| `git log` | Lịch sử commit đầy đủ |
| `git log --oneline` | Mỗi commit 1 dòng |
| `git log --graph --oneline --decorate` | Graph view (đẹp khi nhiều branch) |
| `git show <hash>` | Xem chi tiết 1 commit |
| `cat > .gitignore` | Tạo .gitignore |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Init | Khởi tạo | `git init` — tạo repo mới trong folder |
| Untracked | Chưa theo dõi | File mới, Git chưa biết tới |
| Tracked | Đã theo dõi | File đã commit ít nhất 1 lần |
| Modified | Đã sửa | File đã track, có thay đổi chưa staged |
| Staged | Đã staged | File đã `git add`, chờ commit |
| Committed | Đã commit | Đã đóng gói vào repo |
| HEAD | (giữ nguyên) | Con trỏ tới commit hiện tại |
| SHA hash | (giữ nguyên) | ID duy nhất 40 ký tự của commit |
| Root commit | Commit gốc | Commit đầu tiên, không có parent |
| Working tree clean | Cây làm việc sạch | Không có thay đổi nào chưa commit |
| `.gitignore` | (giữ nguyên) | File khai báo pattern bỏ qua |
| Atomic commit | Commit nguyên tử | 1 commit = 1 thay đổi logic độc lập |
| Conventional Commits | (giữ nguyên) | Quy ước message: `<type>: <desc>` |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [00_what-is-git.md](./00_what-is-git.md) |
| ➡️ Bài tiếp | [02_remote-and-github-basic.md](./02_remote-and-github-basic.md) — Kết nối GitHub |
| 🧠 Trắc nghiệm | [quiz_basic-concepts.md](../../exercises/01_basic/quiz_basic-concepts.md) — Tự kiểm tra nền tảng Git |
| 🛠️ Setup | [Setup Git](../../setup/git.md) |
| 🗺️ Sitemap Git | [Lộ trình chinh phục Git (README)](../../README.md) |

### Tài nguyên ngoài

- [Pro Git Ch.2 — Git Basics](https://git-scm.com/book/vi/v2/Git-cơ-bản-Tạo-một-kho-Git) — Pro Git tiếng Việt
- [Conventional Commits](https://www.conventionalcommits.org/vi/v1.0.0/) — quy ước message
- [github.com/github/gitignore](https://github.com/github/gitignore) — templates `.gitignore`

---

## 📌 Changelog

- **v2.1.0 (24/05/2026)** — Apply Blueprint v0.5.4 §3.5. Bulk replace fictional character "bạn" → "bạn"/"Bạn"/"Mình" theo context (generic role thay tên riêng tự bịa). Nội dung kỹ thuật giữ nguyên.

- **v2.0.0 (19/05/2026)** — Restructure theo writing-style v0.5.1:
  - Mở bằng **tình huống bạn với folder `myapp/` + file `.env`** — 3 câu hỏi cụ thể
  - Headers đổi: `1️⃣ Vì sao học workflow này (WHY)` / `2️⃣ Lifecycle (WHAT)` / `3️⃣ Hands-on (HOW)` → câu hỏi tự nhiên ("Vậy mỗi file trong Git ở trạng thái nào?", "Bắt tay làm cùng bạn")
  - §3 `.gitignore` thêm tình huống `.env` của bạn với API key thật
  - Thống nhất giữ Git ở `02_tools/git/` làm Central Setup Hub và cross-cutting tool
  - Fix relative path depth (5 dots cho `../../../../../00_roadmaps/`)
- **v1.0.0 (16/05/2026)** — Bản đầu tiên — `git init` → `add` → `commit` workflow đầy đủ + 4 trạng thái file + `.gitignore` + 5 pitfall/best-practice.
