# Hướng dẫn thực hành - Bài 5: Git

Git là một công cụ thực hành. Cách tốt nhất để học là làm theo một quy trình làm việc thực tế. Bài hướng dẫn này sẽ mô phỏng việc tạo một dự án nhỏ, phát triển một tính năng mới trên một nhánh riêng, và sau đó hợp nhất nó lại.

**Lưu ý:** Hãy mở terminal của bạn và gõ theo từng lệnh để cảm nhận cách Git hoạt động.

---

### Phần 1: Khởi tạo dự án và Commit đầu tiên

**1. Tạo thư mục dự án và khởi tạo Git:**

Đầu tiên, chúng ta tạo một thư mục riêng cho dự án này và biến nó thành một kho chứa Git (repository).

```bash
# Tạo một thư mục mới và di chuyển vào đó
mkdir my-git-project
cd my-git-project

# Khởi tạo một kho chứa Git trống
git init
```

-   **Giải thích:** `git init` tạo ra một thư mục con ẩn tên là `.git`. Đây là nơi Git lưu trữ toàn bộ lịch sử và cấu hình của dự án.
-   **Kết quả mong đợi:** `Initialized empty Git repository in /path/to/my-git-project/.git/`

**2. Cấu hình thông tin cá nhân (Nếu bạn chưa từng làm):**

Git cần biết bạn là ai để ghi vào lịch sử. Lệnh này chỉ cần chạy một lần trên máy.

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

**3. Tạo file đầu tiên và kiểm tra trạng thái:**

Bây giờ, hãy tạo một file `README.md` và xem Git phản ứng như thế nào.

```bash
# Tạo file README.md với một ít nội dung
echo "# My Awesome Project" > README.md

# Kiểm tra trạng thái của kho chứa
git status
```

-   **Giải thích:** `git status` là người bạn thân nhất của bạn. Nó cho biết những gì đang xảy ra.
-   **Kết quả mong đợi:** Git sẽ báo rằng có một file chưa được theo dõi (`Untracked files`).
    ```
    On branch master
    No commits yet
    Untracked files:
      (use "git add <file>..." to include in what will be committed)
            README.md
    nothing added to commit but untracked files present (use "git add" to track)
    ```

**4. Đưa file vào Staging Area:**

Chúng ta cần cho Git biết rằng chúng ta muốn theo dõi và chuẩn bị file này cho lần commit tới.

```bash
git add README.md
```

-   **Giải thích:** `git add` đưa file vào một khu vực gọi là "Staging Area". Đây là nơi bạn gom góp các thay đổi trước khi tạo một commit.
-   Hãy chạy lại `git status` để xem sự khác biệt. Git sẽ báo rằng có "Changes to be committed".

**5. Thực hiện Commit:**

Bây giờ, hãy lưu "ảnh chụp" này vào lịch sử của dự án.

```bash
git commit -m "Initial commit: Add README.md"
```

-   **Giải thích:** `git commit` tạo một bản ghi mới trong lịch sử. Cờ `-m` cho phép bạn ghi một tin nhắn mô tả ngắn gọn về thay đổi này.
-   Hãy chạy `git status` một lần nữa. Nó sẽ báo `nothing to commit, working tree clean`.
-   Chạy `git log --oneline` để xem commit đầu tiên của bạn trong lịch sử.

---

### Phần 2: Làm việc với Nhánh (Branching)

Giả sử chúng ta muốn phát triển một tính năng mới. Cách làm an toàn là tạo một nhánh riêng để không ảnh hưởng đến nhánh chính (`master` hoặc `main`).

**1. Tạo và chuyển sang nhánh mới:**

```bash
git checkout -b feature/add-license
```

-   **Giải thích:** `git checkout -b` là lệnh gộp của hai lệnh: `git branch feature/add-license` (tạo nhánh) và `git checkout feature/add-license` (chuyển sang nhánh đó).
-   **Kết quả mong đợi:** `Switched to a new branch 'feature/add-license'`

**2. Phát triển tính năng mới:**

Trên nhánh mới này, chúng ta sẽ tạo một file `LICENSE`.

```bash
# Tạo file LICENSE
echo "MIT License" > LICENSE

# Kiểm tra trạng thái
git status

# Add và commit file mới
git add LICENSE
git commit -m "Feat: Add LICENSE file"
```

-   **Giải thích:** Bây giờ, commit này chỉ tồn tại trên nhánh `feature/add-license`. Nhánh `master` vẫn chưa hề biết đến sự tồn tại của file `LICENSE`.
-   Chạy `git log --oneline` để xem lịch sử trên nhánh này. Bạn sẽ thấy 2 commit.

**3. Hợp nhất (Merge) nhánh tính năng:**

Sau khi hoàn thành tính năng, chúng ta sẽ hợp nhất nó trở lại nhánh chính.

```bash
# 1. Quay trở về nhánh chính
git checkout master

# 2. Hợp nhất những thay đổi từ nhánh feature
git merge feature/add-license
```

-   **Giải thích:**
    -   `git checkout master` đưa chúng ta trở lại nhánh `master`. Nếu bạn chạy `ls` bây giờ, bạn sẽ không thấy file `LICENSE`.
    -   `git merge` lấy các commit từ nhánh `feature/add-license` và áp dụng chúng vào nhánh `master`.
-   **Kết quả mong đợi:** Sau khi merge, bạn chạy `ls` sẽ thấy cả `README.md` và `LICENSE`.

**4. Xem lại lịch sử sau khi hợp nhất:**

```bash
git log --oneline --graph --all
```

-   **Giải thích:** Lệnh này cho bạn một cái nhìn trực quan (`--graph`) về lịch sử của tất cả (`--all`) các nhánh, cho thấy commit đã được tạo trên một nhánh riêng và sau đó được hợp nhất vào.

---

### Phần 3: Tương tác với Kho chứa từ xa (Remote)

Phần này mang tính lý thuyết vì chúng ta không có một remote thật. Các lệnh này được dùng để đồng bộ code của bạn với một kho chứa trung tâm như GitHub.

-   **`git remote add origin <URL>`**: Kết nối kho chứa cục bộ của bạn với một kho chứa từ xa. `origin` là tên mặc định cho remote đó.
-   **`git push -u origin master`**: Đẩy (push) các commit từ nhánh `master` ở máy bạn lên remote `origin`. Cờ `-u` thiết lập liên kết để lần sau bạn chỉ cần gõ `git push`.
-   **`git pull`**: Kéo (pull) các thay đổi mới nhất từ remote về máy (nếu có người khác đã push lên).

Chúc mừng! Bạn đã hoàn thành một quy trình làm việc cơ bản nhưng đầy đủ với Git. Hãy lặp lại các bước này để chúng trở thành thói quen.