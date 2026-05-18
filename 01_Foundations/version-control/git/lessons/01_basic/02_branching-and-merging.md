# 🎓 Long thử Google login an toàn — Branching + Merging

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 19/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~25 phút\
> **Prerequisites:** [01_init-and-first-commit.md](./01_init-and-first-commit.md)

> 🎯 *Tiếp Long story: Long đã có repo với feature login. Giờ sếp lại bảo "thêm Google login". Lần này Long không liều sửa thẳng `main` — học cách tạo nhánh riêng, code thoải mái, merge khi xong.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **branch** là gì (mô hình mental)
- [ ] Tạo, switch, xóa branch (`git branch`, `git checkout`, `git switch`)
- [ ] Merge 2 branch (`git merge`)
- [ ] Phân biệt **fast-forward** vs **three-way merge**
- [ ] Resolve **merge conflict** khi gặp

---

## Tình huống — Long không muốn lặp lại bi kịch cuối tuần

Tuần trước Long mất 1 ngày code vì sửa Google login phá login cũ ([nhớ lại bài intro](./00_what-is-git.md)). Giờ có Git rồi, sếp lại bảo:

> *"Thêm tính năng dark mode. Nếu OK thì merge production. Không OK thì hủy luôn, KHÔNG ảnh hưởng login."*

Long suy nghĩ:
- **Cách cũ** (chưa biết Git tốt): sửa thẳng `main`. Dark mode buggy → ảnh hưởng login → repeat bi kịch cũ.
- **Cách Long mới hiểu**: dùng `git branch` để tạo **nhánh thời gian song song** — code dark mode trong nhánh riêng, `main` không bị động. Tốt thì merge, không thì xóa nhánh.

Đây chính là **killer feature** của Git, làm nó vượt xa các VCS cũ (SVN, CVS).

> 💡 **Quy tắc team chuyên nghiệp**: KHÔNG ai code thẳng vào `main`. Mọi thay đổi đều qua feature branch + Pull Request (xem bài 03). Long đang học chuẩn từ đầu — tốt.

---

## 1️⃣ Vậy branch thực sự là gì?

**Định nghĩa chính thức**: Branch là 1 **con trỏ di động** trỏ tới 1 commit. Khi commit mới, con trỏ tự dịch theo. Mỗi branch là 1 "dòng thời gian" độc lập.

**🪞 Ẩn dụ**: *Branch giống như **nhánh sông** — nước (commit) chảy theo nhánh, có thể tách ra (branching), gặp lại nhau (merging). `main` là dòng chính. `feature/X` là nhánh nhỏ tạm.*

### Mô hình mental — Linear history vs Branching

**Không có branch** (linear):

```
main: A → B → C → D → E
```

**Có branch** (parallel timelines):

```
main:    A → B → C ─────────── F ← merge
                    \         /
feature:             D → E ──/
```

→ `main` đi 1 hướng. `feature` tách ra ở C, làm 2 commits D-E, rồi gộp lại tại F.

### HEAD là gì

`HEAD` = "Bạn đang đứng ở đâu" — con trỏ tới branch + commit hiện tại.

```
main:    A → B → C (HEAD ở đây)
```

Khi `checkout feature`:

```
main:    A → B → C
              \
feature:       D → E (HEAD ở đây)
```

→ `git status` show `On branch feature` = HEAD ở `feature`.

> 💡 *Đa số confusion với Git xảy ra khi không biết HEAD đang ở đâu. Luôn `git status` đầu tiên khi bí.*

---

## 2️⃣ Long tạo nhánh đầu tiên — Hands-on

### Setup project mới

```bash
cd ~/Desktop
mkdir branching-demo
cd branching-demo
git init
echo "# Branching Demo" > README.md
echo "print('main version')" > app.py
git add .
git commit -m "Initial commit"
git log --oneline
```

```
a1b2c3d (HEAD -> main) Initial commit
```

### 🛠️ 3.1 Xem branch — `git branch`

```bash
git branch
```

```
* main
```

→ Chỉ có 1 branch `main`. Dấu `*` = branch hiện tại (HEAD đang ở đây).

### 🛠️ 3.2 Tạo branch mới — `git branch <name>`

```bash
git branch feature/say-hi
git branch
```

```
  feature/say-hi
* main
```

→ Đã tạo branch `feature/say-hi`, nhưng `*` vẫn ở `main` — branch mới được tạo nhưng chưa switch.

> 💡 *Quy ước tên branch*: `feature/<name>`, `fix/<name>`, `chore/<name>`. Dùng `/` để group.

### 🛠️ 3.3 Switch branch — `git checkout` hoặc `git switch`

2 cách (đều OK):

```bash
git checkout feature/say-hi
# hoặc (Git 2.23+, modern):
git switch feature/say-hi
```

```
Switched to branch 'feature/say-hi'
```

`git branch`:

```
* feature/say-hi
  main
```

→ `*` chuyển sang `feature/say-hi`.

### 🛠️ 3.4 Shortcut: tạo + switch 1 lệnh

```bash
git checkout -b feature/new-feature
# hoặc:
git switch -c feature/new-feature
```

→ `-b` (branch) / `-c` (create) tạo + switch luôn. **Lệnh dùng nhiều nhất**.

### 🛠️ 3.5 Commit trong branch

Quay lại `feature/say-hi`:

```bash
git checkout feature/say-hi
echo "print('Hello from feature!')" >> app.py
git add app.py
git commit -m "Add hello message"
```

```bash
git log --oneline
```

```
b4c5d6e (HEAD -> feature/say-hi) Add hello message
a1b2c3d (main) Initial commit
```

→ Branch `feature/say-hi` giờ có 2 commits. `main` vẫn chỉ 1 commit.

Verify `main` không bị động:

```bash
git checkout main
cat app.py
```

```
print('main version')
```

→ `main` vẫn nguyên `main version`! 1 commit duy nhất.

```bash
git checkout feature/say-hi
cat app.py
```

```
print('main version')
print('Hello from feature!')
```

→ Quay lại `feature/say-hi`, file lại có 2 dòng.

> 💡 *Đây là magic của branching: 2 phiên bản code song song trên cùng 1 disk. Git tự swap khi `checkout`.*

---

## 3️⃣ Hợp 2 nhánh thành 1 — `git merge`

Giờ `feature/say-hi` đã xong, merge về `main`:

```bash
git checkout main          # phải về branch ĐÍCH trước
git merge feature/say-hi   # merge branch SOURCE vào
```

```
Updating a1b2c3d..b4c5d6e
Fast-forward
 app.py | 1 +
 1 file changed, 1 insertion(+)
```

`git log --oneline`:

```
b4c5d6e (HEAD -> main, feature/say-hi) Add hello message
a1b2c3d Initial commit
```

→ `main` giờ tới commit `b4c5d6e`. **Fast-forward merge**.

### Xóa branch sau khi merge

```bash
git branch -d feature/say-hi
```

```
Deleted branch feature/say-hi (was b4c5d6e).
```

→ Branch không còn, nhưng **commit b4c5d6e vẫn ở `main`** (đã merge). Xóa branch chỉ xóa cái "tag", không xóa lịch sử.

### Fast-forward vs Three-way merge

**Fast-forward**: branch ĐÍCH (`main`) không có commit mới sau khi tách branch SOURCE. Git chỉ "dịch con trỏ" tới commit cuối của SOURCE.

```
TRƯỚC merge:
main:        A → B
                  \
feature:           C → D

SAU merge (fast-forward):
main:        A → B → C → D
feature:             C → D (vẫn còn nếu chưa xóa)
```

**Three-way merge**: cả `main` và `feature` đều có commit mới sau tách. Git tạo **merge commit mới** (M) gộp 2 nhánh.

```
TRƯỚC merge:
main:        A → B → E (có commit mới)
                  \
feature:           C → D

SAU merge (three-way):
main:        A → B → E → M (merge commit)
                  \     /
feature:           C → D
```

→ Three-way tạo "shape diamond" trong git log.

### Demo three-way merge

Tạo conflict scenario:

```bash
# Trên main, sửa app.py
echo "print('main update')" >> app.py
git add app.py
git commit -m "Update main"

# Tạo branch + sửa cùng file
git checkout -b feature/say-bye
echo "print('Goodbye!')" >> app.py
git add app.py
git commit -m "Add goodbye"

# Merge về main
git checkout main
git merge feature/say-bye
```

Git tự động merge nếu thay đổi KHÔNG đụng nhau. Tạo merge commit:

```
Merge branch 'feature/say-bye'
```

`git log --oneline --graph`:

```
*   c7d8e9f (HEAD -> main) Merge branch 'feature/say-bye'
|\
| * f6g7h8i (feature/say-bye) Add goodbye
* | d4e5f6g Update main
|/
* b4c5d6e Add hello message
* a1b2c3d Initial commit
```

→ Thấy hình "diamond" — đó là three-way merge.

---

## 4️⃣ Khi 2 nhánh đụng cùng dòng — Conflict

Conflict xảy ra khi 2 branch sửa **cùng dòng** trong **cùng file**.

### Demo conflict

```bash
# Reset cho gọn (nếu cần)
git checkout main

# Tạo 2 branch sửa cùng dòng
git checkout -b feature/version-a
echo "print('Version A')" > greeting.py
git add greeting.py
git commit -m "Version A"

git checkout main
git checkout -b feature/version-b
echo "print('Version B')" > greeting.py
git add greeting.py
git commit -m "Version B"

# Merge cả 2 → cái thứ 2 sẽ conflict
git checkout main
git merge feature/version-a    # OK — fast-forward
git merge feature/version-b    # CONFLICT
```

```
Auto-merging greeting.py
CONFLICT (add/add): Merge conflict in greeting.py
Automatic merge failed; fix conflicts and then commit the result.
```

`git status`:

```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both added:      greeting.py
```

### Mở file conflict

```bash
cat greeting.py
```

```
<<<<<<< HEAD
print('Version A')
=======
print('Version B')
>>>>>>> feature/version-b
```

| Phần | Ý nghĩa |
|---|---|
| `<<<<<<< HEAD` | Bắt đầu phần của branch hiện tại (đã merge `version-a`) |
| `=======` | Phân cách |
| `>>>>>>> feature/version-b` | Kết thúc phần của branch đang merge |

→ Git đánh dấu, để bạn TỰ quyết định giữ phần nào.

### Resolve manually

Mở file (vd VS Code), edit để chỉ giữ phần đúng. Có 3 lựa chọn:

**Option 1**: giữ HEAD (Version A):

```python
print('Version A')
```

**Option 2**: giữ feature/version-b (Version B):

```python
print('Version B')
```

**Option 3**: kết hợp cả 2:

```python
print('Version A')
print('Version B')
```

### Commit để hoàn tất merge

```bash
git add greeting.py
git status
```

```
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)
```

```bash
git commit -m "Resolve conflict: keep both versions"
```

```
[main g1h2i3j] Resolve conflict: keep both versions
```

→ Conflict resolved!

### Hủy merge nếu hoảng

```bash
git merge --abort
```

→ Quay về trạng thái trước merge. **An toàn nếu bạn không biết phải làm gì**.

### VS Code làm conflict resolution dễ hơn

Mở file conflict trong VS Code → có UI:
- **Accept Current Change** (HEAD) — giữ HEAD
- **Accept Incoming Change** — giữ branch merge
- **Accept Both Changes** — gộp cả 2
- **Compare Changes** — xem diff

→ Click 1 button thay phải edit thủ công. Khuyên beginner.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Quên `git checkout <branch>` trước merge

```bash
git merge feature/x    # Đang ở main? Hay branch khác?
```

- **Triệu chứng**: merge nhầm vào branch khác, hỗn loạn
- **Cách tránh**: luôn `git status` trước merge để biết HEAD ở đâu

### ❌ Pitfall: Code thẳng vào `main`

- **Triệu chứng**: `main` lúc xanh lúc đỏ, deploy gãy, không revert được dễ
- **Cách tránh**: **Quy tắc team**: KHÔNG commit thẳng `main`. Luôn qua feature branch + merge. Setup [branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) trên GitHub.

### ❌ Pitfall: Branch sống quá lâu

- **Triệu chứng**: branch `feature/x` sống 2 tháng → khi merge conflict hàng chục file
- **Cách tránh**: branch ngắn 1-3 ngày là tốt nhất. Lâu hơn → rebase định kỳ từ `main`.

### ❌ Pitfall: Resolve conflict bằng cách "xóa hết"

```python
# Conflict markers
<<<<<<< HEAD
print('A')
=======
print('B')
>>>>>>> branch
```

→ Có người xóa luôn cả 3 dòng `<<<`, `===`, `>>>` mà không suy nghĩ → mất code.

- **Cách tránh**: hiểu **mỗi marker** trước khi xóa. Dùng VS Code UI giúp tránh sai.

### ✅ Best practice: Naming convention cho branch

| Prefix | Use case |
|---|---|
| `feature/<name>` | Tính năng mới |
| `fix/<name>` | Bug fix |
| `chore/<name>` | Refactor, doc, test |
| `release/<version>` | Release branch |
| `hotfix/<name>` | Fix khẩn cấp production |

Ví dụ:
```
feature/user-authentication
fix/login-redirect-loop
chore/update-eslint-config
```

### ✅ Best practice: Pull main thường xuyên về feature branch

```bash
git checkout feature/x
git fetch origin
git merge origin/main      # hoặc rebase
```

→ Giữ branch up-to-date với `main` để giảm conflict khi merge cuối.

### ✅ Best practice: Delete branch sau merge

```bash
git branch -d feature/done
git push origin --delete feature/done    # nếu đã push lên remote
```

→ Repo gọn gàng. Github cũng có nút "Delete branch" sau khi PR merged.

---

## 🧠 Self-check

**Q1.** Sự khác nhau giữa `git branch new-branch` và `git checkout -b new-branch`?

<details>
<summary>💡 Đáp án</summary>

- `git branch new-branch` — TẠO branch mới, nhưng KHÔNG switch sang. HEAD vẫn ở branch hiện tại.
- `git checkout -b new-branch` — TẠO + SWITCH luôn sang branch mới. HEAD chuyển sang `new-branch`.

→ Dùng `-b` khi muốn bắt đầu code ngay trong branch mới (case phổ biến).

</details>

**Q2.** Khi nào fast-forward, khi nào three-way merge?

<details>
<summary>💡 Đáp án</summary>

- **Fast-forward**: branch ĐÍCH (vd `main`) KHÔNG có commit mới sau khi tách branch SOURCE. Git chỉ "dịch con trỏ", không tạo merge commit.

- **Three-way**: cả ĐÍCH và SOURCE đều có commit mới sau khi tách. Git phải tạo **merge commit** gộp 2 nhánh — có hình "diamond" trong log.

Force three-way ngay cả khi có thể fast-forward: `git merge --no-ff feature/x` — để giữ history rõ "có branch ở đây".

</details>

**Q3.** Khi gặp merge conflict trong `app.py`, đoạn `<<<<<<< HEAD` đến `=======` là phần của branch nào?

<details>
<summary>💡 Đáp án</summary>

Phần đó là **HEAD** — branch hiện tại bạn đang đứng (branch ĐÍCH, vd `main` khi bạn `git merge feature/x` từ `main`).

Phần từ `=======` đến `>>>>>>> feature/x` là branch ĐANG ĐƯỢC MERGE VÀO (`feature/x`).

Bạn quyết định giữ phần nào (hoặc cả 2, hoặc viết lại) → xóa các marker → `git add` → `git commit`.

</details>

---

## ⚡ Cheatsheet

| Lệnh | Mục đích |
|---|---|
| `git branch` | List branch |
| `git branch -a` | List cả remote branch |
| `git branch <name>` | Tạo branch (không switch) |
| `git checkout <name>` | Switch branch |
| `git switch <name>` | Switch branch (modern Git 2.23+) |
| `git checkout -b <name>` | Tạo + switch (cũ) |
| `git switch -c <name>` | Tạo + switch (modern) |
| `git branch -d <name>` | Xóa branch (chỉ khi đã merge) |
| `git branch -D <name>` | Force xóa branch (cẩn thận!) |
| `git branch -m <new-name>` | Rename branch hiện tại |
| `git merge <branch>` | Merge `<branch>` vào branch hiện tại |
| `git merge --no-ff <branch>` | Force three-way (không fast-forward) |
| `git merge --abort` | Hủy merge đang dở (rollback) |
| `git log --oneline --graph --decorate` | Xem graph branch + merge |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Branch | Nhánh | 1 dòng thời gian phát triển song song |
| HEAD | (giữ nguyên) | Con trỏ tới branch + commit hiện tại |
| Checkout | (giữ nguyên) | Switch branch hoặc khôi phục file |
| Switch | (giữ nguyên) | Lệnh modern thay checkout cho switch branch |
| Merge | Gộp | Gộp commits từ branch này vào branch khác |
| Fast-forward | Tiến nhanh | Merge bằng cách dịch con trỏ (không tạo commit mới) |
| Three-way merge | Merge 3 chiều | Merge tạo commit mới gộp 2 nhánh |
| Merge commit | (giữ nguyên) | Commit đặc biệt có 2 parent (từ 2 branch) |
| Conflict | Xung đột | Khi 2 branch sửa cùng dòng |
| Resolve | Giải quyết | Sửa conflict thủ công + commit |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [01_init-and-first-commit.md](./01_init-and-first-commit.md) |
| ➡️ Bài tiếp | [03_remote-and-github.md](./03_remote-and-github.md) — push lên GitHub, collab |
| 🧭 Roadmap | [Zero to Coder — Stage 1](../../../../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-cơ-bản-2-3-tuần) |

### Tài nguyên ngoài

- [Pro Git Ch.3 — Git Branching](https://git-scm.com/book/vi/v2/Phân-nhánh-trong-Git-Sơ-Lược-Về-Phân-Nhánh-Trong-Git) — Pro Git tiếng Việt
- [Learn Git Branching (interactive)](https://learngitbranching.js.org/) — game học branching, **cực hay**
- [Atlassian — Git Branching](https://www.atlassian.com/git/tutorials/using-branches) — tutorial chi tiết

---

## 📌 Changelog

- **v2.0.0 (19/05/2026)** — Restructure theo writing-style v0.5.1:
  - Title đổi: "Long thử Google login an toàn — Branching + Merging" (gắn vào story)
  - Mở bằng **tình huống Long tuần trước mất 1 ngày code** + cách cũ vs cách mới với Git branch
  - Headers đổi: `1️⃣ Vì sao cần branch (WHY)` / `2️⃣ Branch là gì (WHAT)` / `3️⃣ Hands-on (HOW)` / `4️⃣ Merge` / `5️⃣ Conflict` → câu hỏi tự nhiên ("Vậy branch thực sự là gì?", "Long tạo nhánh đầu tiên", "Hợp 2 nhánh thành 1", "Khi 2 nhánh đụng cùng dòng")
  - Move folder từ `02_Tools/git/` → `01_Foundations/version-control/git/`
  - Fix relative path depth
- **v1.0.0 (16/05/2026)** — Bản đầu tiên — branching/merging + fast-forward vs three-way + conflict resolution + 5 pitfall + naming convention.
