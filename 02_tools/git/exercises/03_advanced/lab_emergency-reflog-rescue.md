# 🧪 Bài thực hành: Cứu hộ dữ liệu khẩn cấp — Reflog Rescue Hero

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.1.1\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 10/06/2026\
> **Độ khó:** 🔴\
> **Yêu cầu trước:** Đã học xong bài [Cứu hộ thảm họa mã nguồn với Git Reflog](../../lessons/03_advanced/01_advanced-recovery-reflog.md) ✅

---

## 🎯 Mục tiêu của bài Lab
Hãy tưởng tượng một ngày đi làm thực tế, bạn lỡ tay xóa mất một nhánh tính năng chứa 2 tuần code ròng rã của đồng nghiệp hoặc chính mình mà chưa kịp push lên GitHub. Bạn cảm thấy như bầu trời sụp đổ và nhịp tim tăng lên 150 bpm.

Bài Lab thực chiến này sẽ mô phỏng **chính xác thảm họa kinh hoàng đó** và hướng dẫn bạn cách từng bước truy quét chiếc hộp đen **`reflog`** để tìm lại dấu vết, lấy lại mã SHA-1 của commit mồ côi (dangling commit) và thực hiện phép hồi sinh nhánh đã mất một cách ngoạn mục!

---

## 🔍 Kiểm tra môi trường (Environment Check)
Hãy đảm bảo môi trường Git của bạn đã sẵn sàng để thực thi các lệnh truy vết nâng cao:

| Công cụ | Lệnh kiểm tra | Kết quả mong đợi |
|---|---|---|
| **Git đã cài** | `git --version` | Phiên bản Git hiện tại |

---

## 🗺️ Sơ đồ quy trình cứu hộ
```
[Tách nhánh shopping-cart] ──> [Commit code quan trọng] ──> [Switch về main]
                                                                  │
[Hồi sinh nhánh thành công!] <── [Branch lại từ SHA] <── [Reflog tìm SHA] <── [Xóa nhánh -D]
```

---

## 🛠️ Từng bước thực hành chi tiết

### 📂 Bước 1: Khởi tạo sân chơi cứu hộ
Mở Terminal của bạn lên và gõ các lệnh sau để tạo một thư mục trống:

```bash
cd ~/Desktop
mkdir emergency-rescue-playground
cd emergency-rescue-playground
git init
```
Output thực tế hiển thị:
```
Initialized empty Git repository in /Users/user/Desktop/emergency-rescue-playground/.git/
```
-   **Giải thích output:** Thư mục ẩn `.git/` đã được sinh ra để sẵn sàng làm chiếc hộp đen ghi nhận mọi tọa độ bay của con trỏ HEAD.

Tạo một tệp nền tảng `core.py` trên nhánh `main` và commit gốc:
```bash
echo "print('Hệ thống lõi khởi chạy')" > core.py
git add core.py
git commit -m "chore: init core system"
```
Output thực tế:
```
[main (root-commit) z9y8x7w] chore: init core system
```

---

### 🛒 Bước 2: Tách nhánh `feature/shopping-cart` và phát triển tính năng
Tách sang nhánh phụ để phát triển tính năng giỏ hàng:
```bash
git checkout -b feature/shopping-cart
```
Output thực tế:
```
Switched to a new branch 'feature/shopping-cart'
```
-   **Giải thích output:** Trạng thái switch thành công sang cành mọc mới `feature/shopping-cart`.

Giả lập viết code giỏ hàng cực kỳ phức tạp qua 2 commit liên tục:

**Commit 1: Thêm khung giỏ hàng**
```bash
echo "class Cart: pass" >> core.py
git commit -am "feat: implement basic cart class structure"
```

**Commit 2: Thêm logic tính tiền (Đây là báu vật cực kỳ quan trọng)**
```bash
echo "    def checkout(self): print('Thanh toán thành công!')" >> core.py
git commit -am "feat: add checkout logic and pricing calculation"
```

Hãy gõ `git log --oneline` để kiểm chứng lịch sử hiện tại của nhánh phụ:
```bash
git log --oneline
```
Output thực tế hiển thị:
```
a1b2c3d (HEAD -> feature/shopping-cart) feat: add checkout logic and pricing calculation
e4f5g6h feat: implement basic cart class structure
z9y8x7w chore: init core system
```
-   **Giải thích output:** Nhánh shopping-cart đang sở hữu 3 commit, với commit mới nhất trên đỉnh là `a1b2c3d`.

---

### 💥 Bước 3: Thảm họa xảy ra — Xóa cưỡng bức nhánh phụ!
Quay trở lại nhánh chính `main`:
```bash
git checkout main
```
Output thực tế:
```
Switched to branch 'main'
```

Bây giờ, hãy nhắm mắt lại và gõ lệnh xóa cưỡng bức nhánh phụ (giả lập hành động lỡ tay tai hại lúc ngái ngủ):
```bash
git branch -D feature/shopping-cart
```
Output thực tế hiển thị lạnh lùng:
```
Deleted branch feature/shopping-cart (was a1b2c3d).
```
-   **Giải thích output:** Git thông báo đã xóa sổ con trỏ nhánh `feature/shopping-cart`. Toàn bộ lịch sử các commit giỏ hàng đã bốc hơi khỏi lệnh `git log` thông thường.

---

### 🔍 Bước 4: Truy tìm hộp đen cứu hộ — `git reflog`
Hãy hít một hơi thật sâu. Đừng xóa thư mục, đừng reset máy. Hãy gọi bùa cứu mạng **`reflog`**:

```bash
git reflog
```

Output thực tế sẽ in ra danh sách lịch sử dịch chuyển HEAD đầy đủ:
```
z9y8x7w (HEAD -> main) HEAD@{0}: checkout: moving from feature/shopping-cart to main
a1b2c3d HEAD@{1}: commit: feat: add checkout logic and pricing calculation     <-- BÁU VẬT ĐÂY RỒI!
e4f5g6h HEAD@{2}: commit: feat: implement basic cart class structure
z9y8x7w (HEAD -> main) HEAD@{3}: checkout: moving from main to feature/shopping-cart
```
-   **Phân tích nhật ký cứu hộ:**
    -   Dòng `HEAD@{0}` ghi nhận bạn vừa switch từ nhánh `feature/shopping-cart` về `main`.
    -   Dòng `HEAD@{1}` ghi nhận commit cuối cùng của bạn trên nhánh phụ mang mã SHA-1 **`a1b2c3d`** chứa nội dung *"add checkout logic"*. Đây chính là tọa độ vàng để cứu hộ!

---

### 🌟 Bước 5: Hồi sinh nhánh đã mất từ cõi chết!
Bạn đã có mã SHA-1 `a1b2c3d` của commit mồ côi. Hãy yêu cầu Git tạo dựng lại một con trỏ nhánh mới mang tên `feature/shopping-cart` trỏ thẳng vào commit đó:

```bash
git branch feature/shopping-cart a1b2c3d
```

Hãy kiểm tra lại danh sách nhánh:
```bash
git branch
```
Output thực tế hiển thị:
```
  feature/shopping-cart    <-- ĐÃ HỒI SINH KỲ DIỆU!
* main
```
-   **Giải thích output:** Nhánh phụ `feature/shopping-cart` đã được phục sinh tuyệt đối trên bản đồ phân nhánh, chấm dứt thảm họa mất code!

---

## ✅ Tiêu chí hoàn thành bài Lab (Exit Criteria)
Hãy tiến hành nghiệm thu thành quả cứu hộ vĩ đại của bạn:

1.  **Kiểm tra nhánh:** Chuyển sang nhánh vừa được hồi sinh:
    ```bash
    git checkout feature/shopping-cart
    ```
2.  **Kiểm tra lịch sử:** Gõ `git log --oneline`. Bạn phải thấy hiển thị đầy đủ và nguyên vẹn 2 commit giỏ hàng đã từng bị xóa:
    ```
    a1b2c3d (HEAD -> feature/shopping-cart) feat: add checkout logic and pricing calculation
    e4f5g6h feat: implement basic cart class structure
    z9y8x7w chore: init core system
    ```
3.  **Kiểm tra code:** Mở file `core.py` ra kiểm tra → Toàn bộ logic class `Cart` và hàm `checkout` vẫn còn nguyên vẹn 100%, không mất mát một chữ nào!

---

## 🧹 Dọn dẹp tài nguyên (Cleanup)
Sau khi đã hoàn thành thử thách cứu hộ xuất sắc và nắm giữ tấm bùa hộ mệnh Reflog, hãy dọn dẹp sạch sẽ thư mục thực hành trên Desktop để máy tính luôn gọn gàng:

```bash
cd ~/Desktop
rm -rf emergency-rescue-playground
```
*Việc dọn dẹp này giúp giải phóng tài nguyên cục bộ trên máy của bạn một cách gọn gàng.*

---

Chúc mừng bạn! Bạn đã hoàn thành xuất sắc thử thách khó khăn nhất của một chuyên gia Git thực chiến. Từ nay về sau, bạn chính là "người hùng giải cứu code" của bất kỳ đội ngũ công nghệ nào bạn tham gia! 🚀

---

## 📌 Nhật ký thay đổi (Changelog)

- **v2.1.0 (26/05/2026)** — Lab thực hành cứu hộ dữ liệu khẩn cấp bằng `git reflog` (commit và nhánh bị xoá).
- **v2.1.1 (10/06/2026)** — Bỏ field "Thời gian ước tính"; đổi `Prerequisites` → `Yêu cầu trước`; bullet `*` → `-`; link text theo tiêu đề bài.
