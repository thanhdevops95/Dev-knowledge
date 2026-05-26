# 🧪 Bài thực hành: Xây dựng & Đẩy Trang Portfolio Cá Nhân lên GitHub

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.1.0\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 26/05/2026\
> **Độ khó:** ⭐\
> **Thời gian ước tính:** ~30 phút\
> **Prerequisites:** Đã học xong bài học [02_remote-and-github-basic.md](../../lessons/01_basic/02_remote-and-github-basic.md) ✅

---

## 🎯 Mục tiêu của bài Lab
Trong bài thực hành thực chiến này, bạn sẽ tự tay xây dựng một dự án thực tế đầu tay: **Một website giới thiệu bản thân đơn giản (Portfolio)**. Bạn sẽ áp dụng trọn vẹn quy trình làm việc chuyên nghiệp với Git ở máy local và kết nối đồng bộ an toàn lên kho lưu trữ đám mây GitHub.

---

## 🔍 Kiểm tra môi trường (Environment Check)
Trước khi bắt tay vào gõ lệnh, hãy đảm bảo môi trường máy tính của bạn đã sẵn sàng bằng cách chạy các lệnh kiểm tra sau:

| Công cụ | Lệnh kiểm tra | Kết quả mong đợi |
|---|---|---|
| **Git đã cài đặt** | `git --version` | Hiển thị phiên bản Git (ví dụ: `git version 2.x.x`) |
| **Cấu hình Username** | `git config user.name` | Trả về tên hiển thị của bạn trên GitHub |
| **Cấu hình Email** | `git config user.email` | Trả về địa chỉ email đăng ký GitHub của bạn |

> ⚠️ **Nếu chưa cấu hình tên/email:** Hãy chạy ngay 2 lệnh sau:
> ```bash
> git config --global user.name "Tên Của Bạn"
> git config --global user.email "email@example.com"
> ```

---

## 🗺️ Quy trình 5 bước thực hiện
```
[Bước 1: Chuẩn bị code HTML] ──> [Bước 2: Init Git] ──> [Bước 3: Cấu hình .gitignore]
                                                                │
[Bước 5: Push lên GitHub] <── [Bước 4: Commit Atomic] <─────────┘
```

---

## 🛠️ Từng bước thực hành chi tiết

### 📂 Bước 1: Chuẩn bị thư mục dự án và viết code HTML mẫu
Mở Terminal của bạn lên và gõ các lệnh sau để tạo thư mục làm việc:

```bash
cd ~/Desktop
mkdir my-first-portfolio
cd my-first-portfolio
```

Tạo một trang web giới thiệu đơn giản bằng cách tạo file `index.html`:
```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My First Portfolio</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; text-align: center; padding: 50px; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
        h1 { color: #1a73e8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Xin chào! Mình là một Coder tương lai 🚀</h1>
        <p>Đây là website Portfolio đầu tay được quản lý bởi Git và lưu trữ trên GitHub.</p>
    </div>
</body>
</html>
EOF
```

Tạo thêm một file ghi chú cá nhân (chứa các ý tưởng nháp không muốn lưu trữ chính thức) và một file cấu hình giả lập chứa thông tin nhạy cảm:
```bash
echo "Ý tưởng thiết kế: Thêm ảnh đại diện, đổi tông màu tối" > draft-notes.txt
echo "SECRET_API_KEY=my-super-secret-key-12345" > .env
```

---

### 🚀 Bước 2: Khởi tạo Git và cấu hình danh tính cá nhân
Biến thư mục này thành một kho chứa Git chính thức:

```bash
git init
```
Output thực tế:
```
Initialized empty Git repository in /Users/user/Desktop/my-first-portfolio/.git/
```
*   **Giải thích output:** 
    *   Git đã khởi tạo thành công một kho chứa rỗng trên máy của bạn.
    *   Thư mục ẩn `.git/` đã được sinh ra ngầm bên trong dự án để ghi nhận mọi biến động thay đổi file từ lúc này trở đi.

---

### 🛡️ Bước 3: Cấu hình phòng thủ với `.gitignore`
Chúng ta có file `.env` (chứa API key nhạy cảm) và `draft-notes.txt` (file ghi chép nháp không muốn đồng nghiệp xem). Hãy cấu hình để Git bỏ qua chúng hoàn toàn.

Tạo tệp `.gitignore`:
```bash
cat > .gitignore << 'EOF'
.env
draft-notes.txt
EOF
```

Bây giờ hãy chạy lệnh kiểm tra trạng thái:
```bash
git status
```
Output thực tế hiển thị:
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        index.html

nothing added to commit but untracked files present (use "git add" to track)
```
*   **Giải thích output:** 
    *   Trạng thái `Untracked files:` màu đỏ báo hiệu các tệp mới xuất hiện và chưa được Git đưa vào lịch sử lưu vết.
    *   Git chỉ hiển thị `.gitignore` và `index.html`. Hai tệp nhạy cảm `.env` và `draft-notes.txt` hoàn toàn biến mất khỏi radar theo dõi của Git nhờ cấu hình loại trừ chuẩn xác!

---

### 📦 Bước 4: Chụp ảnh lịch sử (Commit) đầu tay
Đưa các file an toàn vào Staging Area:

```bash
git add .
```

Kiểm tra xem các file đã sẵn sàng trong khay đóng gói chưa:
```bash
git status
```
Output thực tế hiển thị:
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   index.html
```
*   **Giải thích output:** 
    *   Trạng thái `Changes to be committed:` chuyển sang màu xanh lá cây báo hiệu các tệp đã nằm sẵn sàng trong **Staging Area**.
    *   Lúc này, bạn có thể tự tin chạy lệnh commit để chụp ảnh lịch sử mà không sợ bị lẫn các file nháp.

Tạo commit đầu tiên tuân thủ Conventional Commits:
```bash
git commit -m "feat: init portfolio page structure"
```
Output thực tế hiển thị:
```
[main (root-commit) f1e2d3c] feat: init portfolio page structure
 2 files changed, 18 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 index.html
```
*   **Giải thích output:** 
    *   Mã commit gốc `f1e2d3c` (root-commit) đã được sinh ra đại diện cho trạng thái lưu trữ đầu tiên của dự án.
    *   Git thông báo ghi nhận thay đổi của 2 tệp tin và tạo thành công cơ sở dữ liệu lưu vết local.

---

### ☁️ Bước 5: Kết nối và đẩy code lên đám mây GitHub

1.  Truy cập vào tài khoản GitHub của bạn và tạo một Repository mới mang tên: `my-first-portfolio` (Đảm bảo **KHÔNG** tích chọn tạo sẵn README hay .gitignore).
2.  Copy đường dẫn HTTPS của Repository đó (có dạng: `https://github.com/your-username/my-first-portfolio.git`).
3.  Quay lại Terminal và chạy lệnh liên kết:

```bash
git remote add origin https://github.com/your-username/my-first-portfolio.git
```

Đảm bảo nhánh chính tên là `main`:
```bash
git branch -M main
```

Tiến hành đẩy code lên GitHub an toàn:
```bash
git push -u origin main
```
*Terminal có thể yêu cầu đăng nhập nếu bạn chưa cấu hình xác thực (Hãy áp dụng hướng dẫn GitHub CLI hoặc SSH Key ở bài học trước).*

Output thực tế khi thành công:
```
Writing objects: 100% (4/4), 450 bytes | 450.00 KiB/s, done.
Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/your-username/my-first-portfolio.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```
*   **Giải thích output:**
    *   Trạng thái `Writing objects: 100%` báo hiệu gói dữ liệu code đã được nén và đẩy thành công qua Internet lên server đám mây.
    *   Dòng cuối khẳng định nhánh `main` ở máy local đã được liên kết đồng bộ mặc định với nhánh `main` trên GitHub.

---

## ✅ Tiêu chí hoàn thành bài Lab (Exit Criteria)
Hãy tự kiểm tra xem mình đã hoàn tất bài Lab đạt tiêu chuẩn 5 sao chưa bằng cách kiểm chứng:

1.  **Kiểm tra local:** Gõ lệnh `git status` tại thư mục dự án. Output phải báo trạng thái sạch sẽ tuyệt đối:
    ```
    On branch main
    nothing to commit, working tree clean
    ```
2.  **Kiểm tra an toàn:** Mở file `.env` ra kiểm tra xem API key vẫn còn nguyên trên máy local của bạn.
3.  **Kiểm tra remote:** Truy cập vào link GitHub Repository của bạn trên trình duyệt web. Bạn phải thấy hiển thị file `index.html` và `.gitignore`. **Tuyệt đối không có sự xuất hiện của file `.env` và `draft-notes.txt` trên GitHub.**

---

## 🧹 Dọn dẹp tài nguyên (Cleanup)
Sau khi đã kiểm tra thành công code của bạn trên GitHub và hoàn thành bài học, hãy dọn dẹp thư mục nháp ở Desktop để giữ cho máy tính luôn sạch sẽ:

```bash
cd ~/Desktop
rm -rf my-first-portfolio
```
*Lưu ý: Lệnh `rm -rf` sẽ xóa vĩnh viễn thư mục nháp local. Vì code của bạn đã được đẩy lên GitHub an toàn nên việc dọn dẹp local này là cực kỳ an toàn và được khuyến nghị.*

---

## 🔗 Liên kết & Điều hướng
*   ➡️ Thử thách tiếp theo (Cấp độ Trung cấp): [00_branching-and-merging.md](../../lessons/02_intermediate/00_branching-and-merging.md) — Phân tách các nhánh tính năng song song an toàn.
