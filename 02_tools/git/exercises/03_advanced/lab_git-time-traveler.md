# 🧪 Bài thực hành: Du hành thời gian gỡ rối mã nguồn — Git Time Traveler

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 10/06/2026\
> **Độ khó:** 🔴\
> **Yêu cầu trước:** Đã học xong bài [Quy tắc undo và sửa sai](../../lessons/03_advanced/00_undo-and-recovery.md) và [Rebase & Cherry-pick](../../lessons/03_advanced/02_rebase-and-cherry-pick.md) ✅

---

## 🎯 Mục tiêu của bài Lab
Trong quá trình phát triển dự án thực tế, bạn sẽ liên tục gặp phải các tình huống "lỡ tay": Gõ nhầm dòng lệnh, commit sai file nhạy cảm, hay code viết ra bị lỗi nát bét và muốn quay về quá khứ an toàn.

Bài Lab thực chiến này sẽ đưa bạn qua **4 kịch bản thảm họa kinh điển** và hướng dẫn bạn cách sử dụng các cỗ máy du hành thời gian (`amend`, `reset --soft`, `revert`, `reset --hard`) để giải cứu mã nguồn một cách điêu luyện nhất!

---

## 🛠️ Từng bước thực hành chi tiết

### 📂 Khởi động: Tạo sân chơi du hành thời gian
Mở Terminal của bạn lên và gõ các lệnh sau để chuẩn bị môi trường:

```bash
cd ~/Desktop
mkdir git-time-traveler-playground
cd git-time-traveler-playground
git init
echo "Phên bản gốc của hệ thống" > app.log
git add app.log
git commit -m "chore: initial production baseline"
```

---

### 🚨 Kịch bản 1: Sửa nhanh sai sót gõ nhầm (Commit Amend)
Bạn vừa code xong tính năng A, nhưng vội vàng commit và gõ sai chính tả message:

```bash
echo "print('Feature A')" > app.py
git add app.py
git commit -m "faet: add feature A"   # <-- ❌ Gõ nhầm "feat" thành "faet"
```

#### 🛠️ Phương pháp giải cứu:
Không cần tạo commit mới để đè lỗi. Hãy sử dụng bùa hộ mệnh **`--amend`** để sửa chữa ngay tại chỗ:
```bash
git commit --amend -m "feat: add feature A"
```
Output thực tế hiển thị:
```
[main e7d8c9b] feat: add feature A
 Date: ...
 1 file changed, 1 insertion(+)
 create mode 100644 app.py
```
-   **Giải thích output:** Commit sai chính tả cũ đã bị Git xóa bỏ vật lý và ghi đè bằng commit mới `e7d8c9b` với tin nhắn đã được chuẩn hóa đẹp đẽ.

---

### 🚨 Kịch bản 2: Hủy commit lỗi nhưng giữ lại code để sửa (Reset Soft)
Bạn tiến hành phát triển tiếp file `app.py`. Bạn tạo một commit mới:

```bash
echo "print('Feature B lỗi')" >> app.py
git commit -am "feat: implement feature B"
```

Ngay sau khi commit, bạn giật mình nhận ra code của `Feature B` đang bị viết sai logic trầm trọng. Bạn muốn **hủy bỏ commit này ngay lập tức**, nhưng **không muốn mất đi những dòng code đã cất công gõ**. Bạn muốn giữ lại code ở Staging Area để sửa lại cho đúng.

#### 🛠️ Phương pháp giải cứu:
Hãy dùng cỗ máy du hành thời gian **`reset --soft`** lùi lại đúng 1 bước:
```bash
git reset --soft HEAD~1
```

Kiểm tra trạng thái hệ thống:
```bash
git status
```
Output thực tế hiển thị:
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   app.py
```
-   **Giải thích output:** Commit chứa lỗi đã bị bốc hơi khỏi lịch sử, nhưng dòng code bạn viết vẫn nằm nguyên vẹn, an toàn trong **Staging Area** (màu xanh). Bạn có thể mở file sửa lại code lỗi và thực hiện commit lại!

---

### 🚨 Kịch bản 3: Đảo ngược sai lầm đã push lên remote (Git Revert)
Hãy commit lại file `app.py` sau khi đã giả vờ sửa đổi:
```bash
git commit -m "feat: implement correct feature B"
```

Bây giờ, bạn đẩy code này lên GitHub. Một ngày sau, khách hàng báo lỗi: *"Feature B bị lỗi logic nghiệp vụ nghiêm trọng, hãy gỡ bỏ nó khỏi production ngay lập tức!"*. Vì commit này đã nằm trên server chung của team, bạn **tuyệt đối không được dùng reset** (vì sẽ làm vỡ lịch sử của người khác).

#### 🛠️ Phương pháp giải cứu:
Hãy tạo một commit mới mang tính chất **đảo ngược hoàn toàn** những gì `Feature B` đã gây ra bằng lệnh **`revert`**:

1.  Gõ `git log --oneline` để lấy mã hash của commit chứa `Feature B` (ví dụ mã hash tìm được là `c7d8e9f`).
2.  Chạy lệnh đảo ngược:
    ```bash
    git revert --no-edit c7d8e9f
    ```
    *(Tham số `--no-edit` để Git tự động lưu tin nhắn revert mặc định mà không bắt bạn mở editor)*.

Output thực tế hiển thị:
```
[main a2b3c4d] Revert "feat: implement correct feature B"
 1 file changed, 1 deletion(-)
```
Gõ `git log --oneline` để kiểm chứng → Lịch sử của bạn vẫn thẳng tắp, an toàn tuyệt đối và tính năng lỗi đã được gỡ bỏ hoàn toàn khỏi code!

---

### 🚨 Kịch bản 4: Vứt bỏ toàn bộ đống code nát (Reset Hard)
Bạn nổi hứng thử nghiệm một ý tưởng điên rồ:
```bash
echo "Ý tưởng điên rồ phá hủy mọi thứ" >> app.py
echo "File rác sinh ra" > trash.txt
```
Sau 10 phút, bạn nhận ra ý tưởng này hoàn toàn thất bại. Code bị lỗi tùm lum và bạn muốn **vứt bỏ sạch sẽ mọi thay đổi nháp** này để đưa thư mục làm việc quay lại trạng thái hoàn toàn sạch sẽ như lúc chưa sửa.

#### 🛠️ Phương pháp giải cứu:
Dùng quả bom nguyên tử nguy hiểm nhất của Git: **`reset --hard`**:
```bash
git reset --hard HEAD
```
Output thực tế hiển thị:
```
HEAD is now at a2b3c4d Revert "feat: implement correct feature B"
```

Hãy gõ lệnh kiểm tra thư mục:
```bash
git status
```
Output hiển thị sạch sẽ tuyệt đối:
```
On branch main
nothing to commit, working tree clean
```
-   **Giải thích output:** Toàn bộ đống code lỗi bừa bộn đã bị dọn sạch bong kin kít. Dự án của bạn đã quay trở về trạng thái an toàn tuyệt đối của commit gần nhất!

---

## ✅ Tiêu chí hoàn thành bài Lab (Exit Criteria)
Hãy tự kiểm tra kết quả du hành vũ trụ của bạn:
1.  Gõ `git status` báo `working tree clean`.
2.  Gõ `git log --oneline`. Bạn phải thấy lịch sử commit được ghi nhận rõ ràng, sạch sẽ và chứa commit Revert an toàn.
3.  Mở file `app.py` ra kiểm tra → File hoàn toàn sạch sẽ, không còn chứa dòng chữ *"Ý tưởng điên rồ"* lỗi lầm nào nữa.

---

## 🧹 Dọn dẹp tài nguyên (Cleanup)
Sau khi đã hoàn thành các kịch bản du hành thời gian và tự tin kiểm soát Git, hãy dọn dẹp sạch sẽ thư mục thực hành trên Desktop để máy tính luôn ngăn nắp:

```bash
cd ~/Desktop
rm -rf git-time-traveler-playground
```

---

Chúc mừng bạn! Bạn đã hoàn thành xuất sắc khóa huấn luyện phi hành gia du hành thời gian của Git! 🚀

---

## 🔗 Liên kết & Tài nguyên

-   ➡️ Thử thách cuối cùng: [Lab — Cứu hộ dữ liệu khẩn cấp qua Reflog](./lab_emergency-reflog-rescue.md) — Cứu hộ dữ liệu khẩn cấp qua Reflog.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v2.0.0 (26/05/2026)** — Lab thực hành nâng cao: các kịch bản "du hành thời gian" gỡ rối mã nguồn với reset/reflog/rebase.
- **v2.0.1 (10/06/2026)** — Bỏ field "Thời gian ước tính"; đổi `Prerequisites` → `Yêu cầu trước`; bổ sung heading "Liên kết & Tài nguyên"; bullet `*` → `-`; link text theo tiêu đề.
