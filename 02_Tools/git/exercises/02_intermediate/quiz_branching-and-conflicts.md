# 🧠 Trắc nghiệm tự đánh giá: Phân nhánh & Giải quyết Xung đột (Git Intermediate)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 26/05/2026\
> **Độ khó:** 🟡\
> **Mục tiêu:** Giúp người học củng cố sâu sắc các kiến thức trung cấp về cơ chế phân nhánh song song, bản chất con trỏ HEAD, nguyên lý gộp code (merge) và cách ứng phó chuyên nghiệp trước xung đột thực tế.

---

## 🎯 Hướng dẫn làm bài
Đọc kỹ từng câu hỏi tình huống dưới đây, tự suy nghĩ đưa ra phương án giải quyết của riêng mình, sau đó click vào phần **💡 Xem giải thích của Mr.Rom** để so sánh và mở rộng tư duy lập trình chuyên nghiệp.

---

## 🧠 Các câu hỏi tự đánh giá

### Q1. Sự khác biệt cốt lõi giữa cơ chế Fast-forward Merge và Three-way Merge (Merge Commit) là gì? Khi nào Git sử dụng cơ chế nào?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

Hiểu rõ hai cơ chế này sẽ giúp bạn làm chủ hoàn toàn lịch sử sơ đồ nhánh (Git Graph) của dự án.

#### 1. Fast-forward Merge (Tiến nhanh):
*   **Điều kiện xảy ra:** Nhánh đích (ví dụ `main`) **không hề có bất kỳ commit mới nào** kể từ thời điểm bạn tách nhánh phụ (ví dụ `feature/login`).
*   **Cơ chế hoạt động:** Git cực kỳ lười biếng. Nó nhận thấy lịch sử là một đường thẳng tuyến tính. Git không tạo ra bất kỳ commit gộp nào cả. Nó chỉ đơn giản là **cầm con trỏ `main` và di chuyển tiến nhanh về phía trước**, đặt trùng vào vị trí commit cuối cùng của nhánh `feature/login`.
*   **Lịch sử Git:** Sạch sẽ, là một đường thẳng tắp như thể bạn chưa từng tách nhánh.

```
(Trước merge)  main:      [A] ──> [B] (HEAD)
                                    └─── feature: [C] ──> [D]

(Sau merge)    main/feat: [A] ──> [B] ──> [C] ──> [D] (HEAD di chuyển tới đây)
```

#### 2. Three-way Merge (Gộp 3 chiều):
*   **Điều kiện xảy ra:** Cả hai nhánh `main` và `feature/login` **đều có các commit mới độc lập** phát sinh sau thời điểm tách nhánh.
*   **Cơ chế hoạt động:** Git không thể di chuyển con trỏ thẳng được nữa vì lịch sử đã bị rẽ lối. Git sẽ lấy 3 điểm dữ liệu:
    1.  Commit chung gần nhất (Common Ancestor - điểm gốc tách nhánh).
    2.  Commit mới nhất của nhánh đích (`main`).
    3.  Commit mới nhất của nhánh nguồn (`feature/login`).
    Git tự động gộp các thay đổi lại và **tạo ra một Commit gộp đặc biệt mới tinh (Merge Commit)**. Commit này đặc biệt vì nó có tới 2 commit cha (parents).
*   **Lịch sử Git:** Xuất hiện hình quả trám (diamond shape) rất đẹp mắt trên Git Graph.

```
(Trước merge)  main:      [A] ──> [B] ──> [E] (Có commit E mới)
                                    └─── feature: [C] ──> [D]

(Sau merge)    main:      [A] ──> [B] ──> [E] ──> [M] (Merge Commit mới)
                                    \             /
                       feature:      └──> [C] ──> [D] ───┘
```

> 💡 **Mẹo chuyên nghiệp:** Đôi khi bạn muốn giữ lại vết tích phân nhánh dù có đủ điều kiện Fast-forward để sau này dễ rollback. Bạn có thể ép Git dùng Three-way merge bằng lệnh: `git merge --no-ff <tên-nhánh>`.

</details>

---

### Q2. Con trỏ HEAD thực chất hoạt động như thế nào khi bạn chuyển nhánh (`git checkout/switch`) hoặc tạo ra một commit mới?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

Con trỏ **`HEAD`** chính là câu trả lời của Git cho câu hỏi: *"Tôi đang đứng ở đâu trong vũ trụ lịch sử dự án này?"*.

#### 1. Cơ chế hoạt động của HEAD:
*   Trong điều kiện bình thường, **HEAD không trỏ trực tiếp vào commit**.
*   **HEAD trỏ vào con trỏ Nhánh hiện tại (Branch Pointer)**, và con trỏ Nhánh mới là thực thể trỏ vào commit mới nhất của nhánh đó.

```
[HEAD] ───trỏ vào───> [main branch pointer] ───trỏ vào───> [Commit A (mới nhất)]
```

#### 2. Khi bạn tạo một commit mới:
1.  Git tạo ra object commit mới (ví dụ `Commit B`).
2.  Git tự động cập nhật con trỏ nhánh hiện tại (ví dụ `main`) tiến lên trỏ vào `Commit B`.
3.  Vì HEAD đang trỏ vào `main`, HEAD tự động được cập nhật gián tiếp để trỏ vào `Commit B`.

#### 3. Khi bạn switch nhánh (`git switch feature`):
Git chỉ đơn giản là nhổ con trỏ HEAD ra khỏi nhánh cũ và cắm nó vào nhánh mới:

```
[HEAD] ───trỏ vào───> [feature branch pointer] ───trỏ vào───> [Commit C]
```
Ngay lập tức, Git đọc cấu trúc dữ liệu của `Commit C` và cập nhật toàn bộ file trên ổ cứng thật (Working Directory) của bạn trùng khớp với trạng thái của nhánh mới.

> ⚠️ **Trạng thái nguy hiểm (Detached HEAD):** Nếu bạn gõ lệnh checkout thẳng đến một mã SHA commit cụ thể (`git checkout a1b2c3d`) thay vì tên nhánh, HEAD sẽ bị ngắt kết nối khỏi con trỏ nhánh và trỏ trực tiếp vào commit đó. Mọi commit bạn tạo ra ở trạng thái này sẽ bị "mất tích" khi bạn chuyển nhánh khác vì không có con trỏ nhánh nào giữ chúng lại!

</details>

---

### Q3. Tôi đang code một mình ở máy local, chạy lệnh kéo code `git pull origin main` thì đột ngột gặp Merge Conflict. Tại sao lại thế? Tôi phải xử lý thế nào cho an toàn?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

Đây là một tình huống kinh điển khi làm việc nhóm (hoặc khi bạn tự code trên 2 máy tính khác nhau).

#### 1. Tại sao lại xảy ra xung đột khi pull?
Bản chất của lệnh **`git pull`** là sự kết hợp của hai hành động chạy liên tiếp:
```bash
git pull = git fetch + git merge origin/main
```
1.  **`git fetch`:** Tải toàn bộ các commit mới từ GitHub về máy bạn (lúc này chưa có gì đụng chạm cả).
2.  **`git merge origin/main`:** Gộp nhánh từ xa (`origin/main`) vào nhánh local hiện tại của bạn (`main`).

Nếu một đồng nghiệp đã sửa dòng số 10 của file `index.html` và push lên GitHub trước, sau đó bạn (ở dưới máy local) cũng sửa dòng số 10 của file `index.html` đó. Khi bạn chạy `git pull`, Git tiến hành merge và phát hiện hai thay đổi đụng nhau chan chát. Xung đột nổ ra!

#### 2. Quy trình xử lý an toàn:
Bạn xử lý **hoàn toàn giống hệt như một Merge Conflict cục bộ** (local merge):
1.  Gõ `git status` để tìm file bị kẹt.
2.  Mở file bị xung đột lên, trao đổi với đồng nghiệp để quyết định xem giữ code của ai hoặc kết hợp cả hai.
3.  Xóa các ký tự marker (`<<<<<<<`, `=======`, `>>>>>>>`) rác.
4.  Chạy lệnh `git add <tên-file>` để xác nhận đã hòa giải.
5.  Chạy lệnh `git commit` để tạo Merge Commit hoàn tất đồng bộ.

</details>

---

### Q4. Tại sao các đội ngũ công nghệ chuyên nghiệp lại cực kỳ khắt khe trong việc quy định quy tắc đặt tên nhánh (Branch Naming Convention)? Đặt tên tùy tiện có tác hại gì?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

Trong các dự án thực tế lớn với hàng chục lập trình viên hoạt động cùng lúc, việc đặt tên nhánh tùy tiện (ví dụ: `code-moi`, `fixed`, `feature-1`, `test-nha`) sẽ biến kho chứa Git thành một bãi rác thông tin hỗn độn.

#### 1. Lợi ích tối thượng của Branch Naming Convention:
*   **Phân loại mục đích rõ ràng:** Nhìn vào tên nhánh biết ngay nhánh đó được sinh ra để làm gì nhờ các tiền tố (prefix) chuẩn hóa:
    *   `feature/`: Phát triển tính năng mới (ví dụ: `feature/user-profile`).
    *   `bugfix/` hoặc `fix/`: Sửa một lỗi code thông thường (ví dụ: `fix/login-session-timeout`).
    *   `hotfix/`: Sửa lỗi cực kỳ khẩn cấp trực tiếp trên môi trường Production đang chạy.
    *   `chore/`: Thay đổi nâng cấp cấu hình hệ thống, cài đặt thư viện nháp.
*   **Tích hợp tự động hóa (CI/CD Pipelines):** Các công cụ tự động hóa sẽ đọc tên nhánh để kích hoạt các kịch bản chạy thử nghiệm tương ứng. Ví dụ: Chỉ kích hoạt deploy tự động lên máy chủ thử nghiệm (Staging) khi phát hiện nhánh có tiền tố `feature/*` được merge.
*   **Dọn dẹp hệ thống siêu tốc:** Cho phép lập trình viên dùng các lệnh lọc bằng ký tự đại diện để xóa hàng loạt các nhánh tính năng đã hoàn thành (ví dụ: xóa sạch các nhánh bắt đầu bằng `feature/*` sau khi kết thúc một chặng nước rút Sprint).

#### 🪞 Ẩn dụ thực tế:
Nó giống như việc bạn dán nhãn phân loại hồ sơ vào các ngăn tủ tài liệu màu khác nhau (Đỏ cho việc khẩn cấp, Xanh cho tính năng mới). Chỉ cần nhìn lướt qua là bạn biết phải tìm tài liệu ở đâu, thay vì phải mở từng ngăn tủ ra bới móc.

</details>

---

## 🔗 Liên kết học tập tiếp theo
*   ⬅️ Quay lại bài học: [01_resolving-conflicts.md](../../lessons/02_intermediate/01_resolving-conflicts.md)
*   ➡️ Thử thách thực hành: [lab_conflict-hero.md](../02_intermediate/lab_conflict-hero.md)
