# ❓ Quiz: Git & GitLab

> **Knowledge Check for Git (20 Questions)**
>
> *Kiểm tra kiến thức Git (20 câu hỏi).*

---

### Q1: Git Init

What does `git init` do?

*(`git init` làm gì?)*

- a) Clone repository
- b) Create new repository *(Tạo mới repository)*
- c) Delete repository
- d) Update repository  

---

### Q2: Staging Area

Which command adds file to staging area?

*(Lệnh nào add file vào staging area?)*

- a) `git commit`
- b) `git add`
- c) `git push`
- d) `git stage`  

---

### Q3: Commit

Which command creates a commit?

*(Lệnh nào tạo commit?)*

- a) `git add -m "message"`
- b) `git commit -m "message"`
- c) `git push -m "message"`
- d) `git save -m "message"`  

---

### Q4: Branching

Which command creates and switches to a branch?

*(Lệnh nào tạo và switch branch?)*

- a) `git branch new-branch`
- b) `git checkout new-branch`
- c) `git checkout -b new-branch`
- d) `git switch new-branch`  

---

### Q5: Merge

To merge branch `feature` into `main`:

*(Để merge branch `feature` vào `main`:)*

- a) `git checkout feature && git merge main`
- b) `git checkout main && git merge feature`
- c) `git merge main feature`
- d) `git merge feature main`  

---

### Q6: Remote

Which command shows remote repositories?

*(Lệnh xem remote repositories?)*

- a) `git remote -v`
- b) `git remote list`
- c) `git show remote`
- d) `git list remote`  

---

### Q7: Pull vs Fetch

How is `git pull` different from `git fetch`?

*(`git pull` khác `git fetch` như thế nào?)*

- a) Pull only downloads, fetch also merges *(Pull chỉ download, fetch còn merge)*
- b) Fetch only downloads, pull also merges *(Fetch chỉ download, pull còn merge)*
- c) No difference *(Không khác nhau)*
- d) Fetch is for tags *(Fetch dùng cho tags)*  

---

### Q8: Revert

Which command creates a new commit to undo the previous commit?

*(Lệnh nào tạo commit mới để undo commit trước?)*

- a) `git reset`
- b) `git revert`
- c) `git undo`
- d) `git checkout`  

---

### Q9: Stash

What is `git stash` used for?

*(`git stash` dùng để làm gì?)*

- a) Delete changes *(Xóa thay đổi)*
- b) Commit changes *(Commit thay đổi)*
- c) Temporarily save changes *(Lưu tạm thời thay đổi)*
- d) Push changes *(Đẩy thay đổi)*  

---

### Q10: Log

Which command shows commit history in short format?

*(Lệnh xem commit history ngắn gọn?)*

- a) `git log -1`
- b) `git log --oneline`
- c) `git log --short`
- d) `git history`  

---

### Q11: Reset

What does `git reset --hard HEAD~1` do?

*(`git reset --hard HEAD~1` làm gì?)*

- a) Delete last commit, keep changes *(Xóa commit cuối, giữ changes)*
- b) Delete last commit, delete changes *(Xóa commit cuối, xóa changes)*
- c) Delete last 2 commits *(Xóa 2 commits cuối)*
- d) Does nothing *(Không làm gì)*  

---

### Q12: Cherry-pick

What is `git cherry-pick` used for?

*(`git cherry-pick` dùng để?)*

- a) Delete commit *(Xóa commit)*
- b) Apply specific commit from another branch *(Áp dụng commit cụ thể từ branch khác)*
- c) Create branch
- d) Merge branches  

---

### Q13: Rebase

How is `git rebase` different from `git merge`?

*(`git rebase` khác `git merge` như thế nào?)*

- a) Rebase creates merge commit *(Rebase tạo merge commit)*
- b) Rebase rewrites history, merge doesn't *(Rebase viết lại lịch sử, merge thì không)*
- c) No difference *(Không khác nhau)*
- d) Merge rewrites history  

---

### Q14: .gitignore

Which file will NOT be tracked if `.gitignore` contains `*.log`?

*(File nào không bị track nếu có `.gitignore` chứa `*.log`?)*

- a) debug.log
- b) app.log
- c) logs/error.log
- d) All of the above *(Tất cả)*  

---

### Q15: Tag

Which command creates an annotated tag?

*(Lệnh tạo annotated tag?)*

- a) `git tag v1.0`
- b) `git tag -a v1.0 -m "Release"`
- c) `git tag --annotated v1.0`
- d) `git create-tag v1.0`  

---

### Q16: Diff

What does `git diff --staged` show?

*(`git diff --staged` hiển thị gì?)*

- a) Changes not staged *(Các thay đổi chưa stage)*
- b) Changes staged but not committed *(Các thay đổi đã stage nhưng chưa commit)*
- c) All changes *(Tất cả thay đổi)*
- d) Committed changes *(Các thay đổi đã commit)*  

---

### Q17: Clone

What does `git clone --depth 1` do?

*(`git clone --depth 1` làm gì?)*

- a) Clone all history *(Clone tất cả history)*
- b) Clone only latest commit (shallow) *(Clone chỉ latest commit)*
- c) Clone specific branch *(Clone branch specific)*
- d) Clone without files  

---

### Q18: Blame

What does `git blame file.txt` show?

*(`git blame file.txt` hiển thị gì?)*

- a) Who modified each line *(Ai đã sửa từng dòng)*
- b) File history *(Lịch sử file)*
- c) Diff
- d) Errors *(Lỗi)*  

---

### Q19: Submodule

What is Git submodule used for?

*(Git submodule dùng để?)*

- a) Delete repositories
- b) Include other repos as subdirectory *(Bao gồm repo khác như thư mục con)*
- c) Create branches
- d) Merge repos  

---

### Q20: Hook

When does pre-commit hook run?

*(Pre-commit hook chạy khi nào?)*

- a) Before push *(Trước khi push)*
- b) Before commit is created *(Trước khi commit được tạo)*
- c) After commit *(Sau khi commit)*
- d) After push *(Sau khi push)*  

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | A | Q | A |
|---|---|---|---|
| 1 | b | 11 | b |
| 2 | b | 12 | b |
| 3 | b | 13 | b |
| 4 | c | 14 | d |
| 5 | b | 15 | b |
| 6 | a | 16 | b |
| 7 | b | 17 | b |
| 8 | b | 18 | a |
| 9 | c | 19 | b |
| 10 | b | 20 | b |

</details>

---

**[← Back to README](./README.md)**
