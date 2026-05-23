# Bài 5: Git - Hệ thống Quản lý Phiên bản Phân tán

## 🎯 Mục tiêu bài học

-   Hiểu được tại sao cần phải quản lý phiên bản mã nguồn.
-   Thành thạo chu trình làm việc cơ bản với Git: `add`, `commit`, `push`, `pull` (kéo), `fetch` (tìm nạp).
-   Nắm vững cách làm việc với nhánh (branch) để phát triển tính năng mới một cách an toàn.
-   Biết cách xem lại lịch sử thay đổi và xử lý các xung đột khi hợp nhất (merge conflict).

## 📖 Nội dung chính

1.  **Giới thiệu Git:** Git là gì? Tại sao nó là công cụ bắt buộc?
2.  **Cài đặt và Cấu hình:** Thiết lập tên và email của bạn.
3.  **Kho chứa (Repository):** Khởi tạo (`git init`) và sao chép (`git clone`).
4.  **Chu trình làm việc cơ bản:** `git status`, `git add`, `git commit`.
5.  **Làm việc với Nhánh (Branching):** `git branch`, `git checkout`, `git merge`.
6.  **Làm việc với kho chứa từ xa:** `git remote`, `git push`, `git pull`.
7.  **Xem lịch sử và So sánh:** `git log`, `git diff`.
8.  **Hoàn tác thay đổi:** `git revert`, `git reset`.
9.  **Bỏ qua file với `.gitignore`**: Một file cấu hình quan trọng.
10. **Mô hình Git Flow:** Một chiến lược phân nhánh phổ biến.

## 🛠️ Công cụ & Lý thuyết

-   **Công cụ SCM (Source Code Management - Quản lý Mã nguồn):** <u>Git</u>, Subversion (SVN), Mercurial.
-   **Nền tảng SCM:** <u>GitHub</u>, GitLab, Bitbucket (các dịch vụ hosting cho kho chứa Git).
-   **Lý thuyết:** Version Control System (VCS - Hệ thống Quản lý Phiên bản), Distributed VCS (DVCS - Hệ thống Quản lý Phiên bản Phân tán), Branching Strategies (Chiến lược phân nhánh).

---

# Nội dung chi tiết - Bài 5: Git - Hệ thống Quản lý Phiên bản

Mã nguồn là tài sản quý giá nhất của một dự án phần mềm. Sẽ ra sao nếu bạn vô tình xóa mất một file quan trọng? Hoặc một tính năng mới làm hỏng toàn bộ ứng dụng và bạn không biết làm cách nào để quay lại phiên bản ổn định trước đó? Git ra đời để giải quyết những vấn đề này.

---

### 1. Giới thiệu Git

**Git** là một **Hệ thống Quản lý Phiên bản Phân tán (Distributed Version Control System - DVCS)** được tạo ra bởi Linus Torvalds.

-   **Quản lý phiên bản:** Nó theo dõi và lưu lại mọi sự thay đổi trong mã nguồn của bạn theo thời gian. Bạn có thể xem lại lịch sử, so sánh các phiên bản, và quay trở lại bất kỳ phiên bản nào trong quá khứ.
-   **Phân tán:** Mỗi lập trình viên có một bản sao đầy đủ của toàn bộ lịch sử dự án trên máy tính của mình. Điều này giúp làm việc offline và tăng tốc độ hoạt động.

Đối với DevOps, Git là nền tảng của CI/CD (Continuous Integration/Continuous Deployment - Tích hợp liên tục/Triển khai liên tục). Mọi thay đổi trong mã nguồn được đưa lên Git sẽ kích hoạt các quy trình tự động.

---

### 2. Cài đặt và Cấu hình

Sau khi cài đặt Git, điều đầu tiên bạn cần làm là cho Git biết bạn là ai. Thông tin này sẽ được gắn vào mỗi `commit` (bản ghi thay đổi) của bạn.

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

---

### 3. Kho chứa (Repository)

Một kho chứa (repository hay "repo") là nơi chứa toàn bộ mã nguồn và lịch sử thay đổi của dự án.

-   **Tạo một repo mới:**
    ```bash
    # Đi vào thư mục dự án của bạn
    cd my-project
    # Khởi tạo repo
    git init
    ```
-   **Lấy một repo đã có từ xa (ví dụ từ GitHub):**
    ```bash
    git clone https://github.com/user/project.git
    ```

---

### 4. Chu trình làm việc cơ bản

Đây là 3 bước bạn sẽ làm hàng ngày:

1.  **`git add <file>`:** Sau khi bạn thay đổi file, bạn cần cho Git biết rằng bạn muốn theo dõi sự thay đổi này. Hành động này đưa file vào một khu vực gọi là **Staging Area**.
    - `git add .` để thêm tất cả các file đã thay đổi.
2.  **`git commit -m "Your message"`:** Ghi lại các thay đổi trong Staging Area vào lịch sử của repo. Mỗi commit là một "ảnh chụp" (snapshot) của dự án tại một thời điểm.
    -   Tin nhắn commit (`commit message`) nên tuân theo một quy ước chung, ví dụ: `feat: Add user login functionality`. Điều này giúp lịch sử dự án trở nên dễ đọc hơn.
3.  **`git status`:** Luôn là bạn đồng hành. Lệnh này cho bạn biết trạng thái hiện tại của repo: file nào đã thay đổi, file nào đang ở Staging Area,...

---

### 5. Làm việc với Nhánh (Branching)

Nhánh (branch) cho phép bạn tạo ra một không gian làm việc riêng để phát triển một tính năng mới hoặc sửa lỗi mà không ảnh hưởng đến nhánh chính (thường là `main` hoặc `master`).

-   **`git branch`**: Liệt kê tất cả các nhánh.
-   **`git branch <tên-nhánh>`**: Tạo một nhánh mới.
-   **`git checkout <tên-nhánh>`** (hoặc `git switch <tên-nhánh>`): Chuyển sang làm việc trên nhánh đó.
    - `git checkout -b <tên-nhánh>`: Tạo và chuyển sang nhánh mới trong một lệnh.
-   **`git merge <tên-nhánh>`**: Sau khi hoàn thành công việc trên nhánh của bạn, bạn sẽ quay lại nhánh `main` và hợp nhất (merge) những thay đổi từ nhánh của bạn vào.

---

### 6. Làm việc với kho chứa từ xa (Remote)

Để cộng tác với người khác, bạn cần một kho chứa trung tâm (remote), thường được host trên GitHub, GitLab, hoặc Bitbucket.

-   **`git remote -v`**: Xem các remote đã được cấu hình. `origin` là tên mặc định cho remote mà bạn đã `clone`.
-   **`git push origin <tên-nhánh>`**: Đẩy (push) các commit từ nhánh trên máy của bạn lên remote.
-   **`git pull origin <tên-nhánh>`**: Kéo (pull) các thay đổi mới nhất từ remote về máy của bạn. Lệnh này thực chất là sự kết hợp của `git fetch` (lấy thông tin thay đổi) và `git merge` (trộn thay đổi đó vào nhánh hiện tại).

---

### 7. Xem lịch sử và So sánh

-   **`git log`**: Hiển thị lịch sử các commit.
    - `git log --oneline --graph`: Hiển thị log một cách gọn gàng và trực quan.
-   **`git diff`**: So sánh sự khác biệt giữa các phiên bản.
    - `git diff`: So sánh thay đổi trong thư mục làm việc với Staging Area.
    - `git diff --staged`: So sánh Staging Area với commit cuối cùng.
    - `git diff HEAD`: So sánh thư mục làm việc với commit cuối cùng.

---

### 8. Hoàn tác thay đổi (Undoing Things)

Sai lầm là điều không thể tránh khỏi. Git cung cấp các công cụ mạnh mẽ để bạn sửa sai.

-   **`git commit --amend`**: Sửa lại commit gần nhất (thay đổi tin nhắn hoặc thêm file mới).
-   **`git revert <commit-hash>`**: Tạo ra một commit mới để **đảo ngược** lại các thay đổi của một commit cũ. Cách này an toàn vì nó không thay đổi lịch sử đã có.
-   **`git reset <commit-hash>`**: Di chuyển con trỏ HEAD về một commit trong quá khứ, **xóa bỏ lịch sử** phía sau nó. Lệnh này rất mạnh và nguy hiểm, chỉ nên dùng trên nhánh cá nhân chưa được push lên remote.

---

### 9. Bỏ qua file với `.gitignore`

Dự án của bạn sẽ luôn có những file không cần đưa vào lịch sử Git, ví dụ: file log, thư mục chứa các thư viện (`node_modules`), file chứa thông tin nhạy cảm (`.env`).

Bạn có thể tạo một file tên là `.gitignore` ở thư mục gốc của dự án và liệt kê các file/thư mục bạn muốn Git bỏ qua.

*Ví dụ file `.gitignore`:*
```
# Bỏ qua thư mục chứa các gói phụ thuộc
node_modules/

# Bỏ qua các file log
*.log

# Bỏ qua file biến môi trường
.env
```

---

### 10. Mô hình Git Flow

Git Flow là một mô hình phân nhánh phổ biến, sử dụng các nhánh với vai trò cụ thể:
-   `main`: Luôn chứa code đã được release, ổn định.
-   `develop`: Nhánh tích hợp các tính năng đã hoàn thành.
-   `feature/*`: Nhánh để phát triển tính năng mới, được tạo từ `develop`.
-   `release/*`: Nhánh chuẩn bị cho một phiên bản release mới.
-   `hotfix/*`: Nhánh để sửa các lỗi nghiêm trọng trên production, được tạo từ `main`.

Hiểu về Git là kỹ năng nền tảng. Trong bài tiếp theo, chúng ta sẽ khám phá cách tự động hóa quy trình làm việc sau khi bạn `git push` - đó chính là CI/CD.

---

## ✍️ Bài tập thực hành (Exercises)

**Đề bài:** Xây dựng một trang web portfolio đơn giản và quản lý các phiên bản của nó bằng Git.

1.  **Bài tập 1: Khởi tạo dự án và Commit đầu tiên**
    -   Tạo một thư mục mới tên là `my-portfolio`.
    -   Bên trong thư mục, khởi tạo một kho chứa Git mới (`git init`).
    -   Tạo file `index.html` với nội dung cơ bản (ví dụ: một thẻ `<h1>` chứa tên của bạn).
    -   Kiểm tra trạng thái của kho chứa (`git status`).
    -   Đưa file `index.html` vào Staging Area và commit với tin nhắn: `feat: Add initial index.html`.

2.  **Bài tập 2: Phát triển tính năng trên nhánh mới**
    -   Tạo một nhánh mới tên là `feature/add-styling`.
    -   Chuyển sang nhánh vừa tạo.
    -   Tạo một file `style.css` và thêm một vài quy tắc CSS đơn giản (ví dụ: đổi màu nền, màu chữ).
    -   Trong file `index.html`, thêm thẻ `<link>` để nhúng file `style.css`.
    -   Commit các thay đổi trên nhánh `feature/add-styling` với tin nhắn: `feat: Add basic CSS styling`.
    -   Quay trở lại nhánh `main` và hợp nhất (merge) nhánh `feature/add-styling` vào.

3.  **Bài tập 3: Mô phỏng và giải quyết xung đột (Merge Conflict)**
    -   Từ nhánh `main`, tạo một nhánh mới tên là `feature/update-header`.
    -   Trên nhánh này, thay đổi nội dung thẻ `<h1>` trong `index.html` thành "My Awesome Portfolio". Commit thay đổi.
    -   Quay lại nhánh `main`. Cũng tại file `index.html`, thay đổi nội dung thẻ `<h1>` thành "Welcome to My Website". Commit thay đổi.
    -   Bây giờ, hãy thử hợp nhất nhánh `feature/update-header` vào `main`. Git sẽ báo lỗi xung đột.
    -   Mở file `index.html` trong editor, bạn sẽ thấy các dấu `<<<<<<<`, `=======`, `>>>>>>>`.
    -   Hãy giải quyết xung đột bằng cách xóa các dấu này và chọn nội dung cuối cùng bạn muốn giữ lại.
    -   Sau khi giải quyết xong, `git add index.html` và `git commit` để hoàn tất việc hợp nhất.

4.  **Bài tập 4: Sử dụng `.gitignore`**
    -   Tạo một thư mục `logs/` và một file `app.log` bên trong.
    -   Tạo một file `notes.txt` chứa các ghi chú cá nhân.
    -   Kiểm tra `git status`. Bạn sẽ thấy các file/thư mục mới này đang ở trạng thái "untracked".
    -   Tạo một file `.gitignore` ở thư mục gốc.
    -   Thêm các dòng sau vào `.gitignore`:
        ```
        # Ignore log files
        logs/
        *.log

        # Ignore personal notes
        notes.txt
        ```
    -   Kiểm tra lại `git status` để thấy rằng Git đã bỏ qua các file và thư mục này.

[Bài trước: Nhập môn Mạng máy tính](../../Lesson01-foundation/04-networking-concepts/) | [Quay lại Mục lục chính](../../README.md) | [Bài tiếp theo: Lý thuyết về CI/CD](../06-ci-cd-theory/)