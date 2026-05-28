# 🧪 Bài thực hành: Quy trình làm việc nhóm chuyên nghiệp với Pull Request

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.1.0\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 26/05/2026\
> **Độ khó:** 🟡\
> **Thời gian ước tính:** ~30 phút\
> **Prerequisites:** Đã học xong bài học [02_collaborative-workflows.md](../../lessons/02_intermediate/02_collaborative-workflows.md) ✅

---

## 🎯 Mục tiêu của bài Lab
Trong thế giới công nghệ chuyên nghiệp, **không một ai được phép push code thẳng vào nhánh `main`**. Mọi dòng code trước khi được đưa vào sản phẩm chính thức đều phải trải qua quy trình **Pull Request (PR) & Code Review** cực kỳ nghiêm ngặt. 

Trong bài Lab này, bạn sẽ tự mình đóng cả hai vai: **Lập trình viên junior** (tạo nhánh, viết code và gửi yêu cầu PR) và **Lập trình viên senior** (đánh giá code, phê duyệt và merge PR trên GitHub) để nắm lòng 100% quy trình collab thực tế tại các tập đoàn công nghệ lớn.

---

## 🔍 Kiểm tra môi trường (Environment Check)
Hãy kiểm tra xem các thiết lập và tài khoản của bạn đã sẵn sàng để làm việc nhóm trên mây hay chưa:

| Công cụ / Tài khoản | Cách kiểm tra | Kết quả mong đợi |
|---|---|---|
| **Tài khoản GitHub** | Truy cập [github.com](https://github.com) | Đảm bảo bạn đã đăng nhập và sẵn sàng tạo Repo mới |
| **Xác thực kết nối** | Chạy `gh auth status` hoặc `ssh -T git@github.com` | Xác nhận quyền truy cập đẩy code an toàn lên GitHub |

---

## 🗺️ Sơ đồ quy trình Pull Request
```
[Local: main] ──> [Tạo nhánh feature] ──> [Commit code] ──> [Push lên GitHub]
                                                                  │
[GitHub: Trình duyệt] <── [Merge PR] <── [Tạo Pull Request] <─────┘
```

---

## 🛠️ Từng bước thực hành chi tiết

### 📂 Bước 1: Khởi tạo thư mục và liên kết lên GitHub
1.  **Tại máy local:** Tạo thư mục và khởi tạo Git:
    ```bash
    cd ~/Desktop
    mkdir pull-request-lab
    cd pull-request-lab
    git init
    ```
2.  Tạo file `README.md` làm nền tảng ban đầu và commit:
    ```bash
    echo "# Pull Request Practice Lab" > README.md
    git add README.md
    git commit -m "chore: initial repository structure"
    ```
    Output thực tế hiển thị:
    ```
    [main (root-commit) a1b2c3d] chore: initial repository structure
     1 file changed, 1 insertion(+)
     create mode 100644 README.md
    ```
    *   **Giải thích output:**
        *   Mã commit gốc `a1b2c3d` đã được sinh ra ghi nhận cấu trúc nền móng ban đầu của dự án.
        *   Git báo hiệu 1 file mới đã được theo dõi và tạo thành công cơ sở dữ liệu local.

3.  **Tại GitHub:** Tạo một repository trống mang tên `pull-request-lab` (Visibility chọn **Public**).
4.  **Liên kết local với GitHub và push nhánh main lên trước:**
    ```bash
    git remote add origin https://github.com/your-username/pull-request-lab.git
    git branch -M main
    git push -u origin main
    ```
    Output thực tế:
    ```
    branch 'main' set up to track 'origin/main'.
    ```
    *   **Giải thích output:** Nhánh `main` của local đã được liên kết đồng bộ bền vững với server từ xa. Từ nay về sau, bạn chỉ cần gõ `git push` để đẩy thay đổi trên nhánh main.

---

### 🌿 Bước 2: Tạo nhánh tính năng `feature/add-profile`
Bắt đầu một nhiệm vụ mới, dứt khoát không sửa code trên `main`. Hãy tách ra một nhánh tính năng riêng:

```bash
git checkout -b feature/add-profile
```
Output thực tế hiển thị:
```
Switched to a new branch 'feature/add-profile'
```
*   **Giải thích output:** Con trỏ làm việc HEAD đã nhảy từ `main` sang nhánh phụ song song mang tên `feature/add-profile` an toàn.

---

### 📝 Bước 3: Viết code hồ sơ cá nhân và commit
Tạo file `profile.md` chứa thông tin giới thiệu của bạn:
```bash
cat > profile.md << 'EOF'
# 👤 Hồ Sơ Lập Trình Viên

- **Họ và tên:** [Tên của bạn]
- **Vị trí:** Coder tương lai thực chiến
- **Công cụ yêu thích:** Git, VS Code, Python, JavaScript
- **Châm ngôn:** "Measure twice, cut once" — Mr.Rom
EOF
```

Stage và commit thay đổi tuân thủ Conventional Commits:
```bash
git add profile.md
git commit -m "feat: add developer profile documentation"
```
Output thực tế:
```
[feature/add-profile e5f6g7h] feat: add developer profile documentation
 1 file changed, 6 insertions(+)
 create mode 100644 profile.md
```
*   **Giải thích output:** 
    *   Mã commit `e5f6g7h` đã được tạo ra ghi nhận sự mọc thêm cành cành mới trên nhánh tính năng.
    *   Nhánh chính `main` hoàn toàn không bị ảnh hưởng bởi thay đổi này.

---

### ☁️ Bước 4: Đẩy nhánh tính năng lên đám mây GitHub
Đẩy nhánh phụ lên remote GitHub:

```bash
git push -u origin feature/add-profile
```
Output thực tế hiển thị:
```
Writing objects: 100% (3/3), 320 bytes | 320.00 KiB/s, done.
To https://github.com/your-username/pull-request-lab.git
 * [new branch]      feature/add-profile -> feature/add-profile
branch 'feature/add-profile' set up to track 'origin/feature/add-profile'.
```
*   **Giải thích output:**
    *   Nhánh phụ của bạn đã được đóng gói và truyền tải qua Internet thành công lên server.
    *   Đường dẫn tracking được thiết lập giúp bạn dễ dàng đồng bộ nhánh phụ sau này.

---

### 📋 Bước 5: Khởi tạo Pull Request trên giao diện GitHub
1.  Truy cập vào repository `pull-request-lab` của bạn trên GitHub bằng trình duyệt.
2.  Bạn sẽ thấy một bảng thông báo màu vàng hiện ra ghi: *"feature/add-profile had recent pushes less than a minute ago"*. Click ngay vào nút **`Compare & pull request`**.
3.  Biên soạn thông tin PR chuyên nghiệp theo chuẩn 5 sao:
    *   **Title:** `feat: add developer profile documentation`
    *   **Description:**
        ```markdown
        ## Summary
        Thêm tài liệu hồ sơ cá nhân giới thiệu lập trình viên.

        ## Changes
        - Tạo mới file `profile.md` chứa thông tin kỹ năng và châm ngôn làm việc.

        ## Test Plan
        - [x] Kiểm tra hiển thị Markdown chuẩn xác trên GitHub.
        ```
4.  Click nút xanh **`Create pull request`**.

---

### 🧐 Bước 6: Đóng vai Senior Developer — Đánh giá & Merge PR
Trang web sẽ hiển thị giao diện Pull Request đang mở. Lúc này bạn hãy hóa thân thành người chấm bài khó tính:
1.  Click vào tab **`Files changed`** ở phía trên để xem sự khác biệt. Bạn sẽ thấy dòng code thêm mới màu xanh lá cây cực kỳ trực quan.
2.  Nếu mọi thứ hoàn hảo, hãy click quay lại tab **`Conversation`**.
3.  Nhìn xuống ô màu xanh ở cuối trang, click vào mũi tên nhỏ cạnh nút `Merge pull request` → Chọn **`Squash and merge`** (Đây là kỹ thuật gộp toàn bộ các commit vụn vặt của nhánh phụ thành 1 commit duy nhất siêu sạch trước khi nạp vào nhánh chính).
4.  Click **`Confirm squash and merge`**.
5.  Click nút **`Delete branch`** ngay trên màn hình để xóa sạch nhánh phụ trên server GitHub nhằm giữ sạch tài nguyên kho lưu trữ.

---

## ✅ Tiêu chí hoàn thành bài Lab (Exit Criteria)
Hãy tiến hành đồng bộ hóa ngược lại về máy local của bạn để nghiệm thu thành quả:

1.  **Đồng bộ local:** Tại Terminal local, switch về `main` và kéo code mới nhất từ GitHub về:
    ```bash
    git checkout main
    git pull
    ```
    Output thực tế hiển thị:
    ```
    Updating a1b2c3d..e5f6g7h
    Fast-forward
     profile.md | 6 ++++++
     1 file changed, 6 insertions(+)
     create mode 100644 profile.md
    ```
    *   **Giải thích output:** Lệnh `git pull` kéo thành công file `profile.md` được merge từ GitHub về local của bạn, đồng thời tiến hành gộp nhanh Fast-forward hoàn hảo.

2.  **Xóa nhánh local thừa:** Sau khi đã gộp thành công trên GitHub, hãy xóa nhánh phụ ở local đi để giữ sạch máy tính:
    ```bash
    git branch -d feature/add-profile
    ```
3.  **Kiểm chứng lịch sử:** Chạy lệnh `git log --oneline`. Bạn phải thấy lịch sử Git local của bạn chỉ có đúng 2 commit siêu sạch sẽ như thế này:
    ```
    e5f6g7h (HEAD -> main, origin/main) feat: add developer profile documentation
    a1b2c3d chore: initial repository structure
    ```

---

## 🧹 Dọn dẹp tài nguyên (Cleanup)
Sau khi hoàn tất bài thực hành và đồng bộ thành công nhánh chính, hãy dọn dẹp thư mục làm việc trên Desktop của bạn để giữ gìn vệ sinh cho ổ cứng máy tính:

```bash
cd ~/Desktop
rm -rf pull-request-lab
```
*Vì code của bạn đã được đẩy lên GitHub và merge an toàn vào nhánh main trên đám mây, việc xóa thư mục local này hoàn toàn không làm mất code mà giúp bạn rèn luyện thói quen giữ sạch không gian làm việc.*

---

## 🔗 Liên kết & Điều hướng
*   ➡️ Thử thách tiếp theo (Cấp độ Nâng cao): [00_undo-and-recovery.md](../../lessons/03_advanced/00_undo-and-recovery.md) — Sửa chữa các sai lầm nguy hiểm.
