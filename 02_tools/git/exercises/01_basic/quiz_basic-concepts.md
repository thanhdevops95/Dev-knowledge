# 🧠 Trắc nghiệm tự đánh giá: Nền tảng Git & 3 Vùng cốt lõi

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 26/05/2026\
> **Độ khó:** ⭐\
> **Mục tiêu:** Giúp người học tự kiểm tra và khắc sâu các khái niệm cơ bản về Git, 3 vùng dữ liệu, và quy trình commit trước khi chuyển sang các chủ đề nâng cao hơn.

---

## 🎯 Hướng dẫn làm bài
Đọc kỹ từng câu hỏi dưới đây, tự suy nghĩ câu trả lời trong đầu hoặc viết ra giấy, sau đó nhấn vào phần **💡 Xem giải thích của Mr.Rom** để đối chiếu kết quả và lĩnh hội những đúc kết tri thức sâu sắc nhất.

---

## 🧠 Các câu hỏi tự đánh giá

### Q1. Staging Area (vùng đệm) thực sự đóng vai trò gì trong Git? Tại sao không commit trực tiếp từ Working Directory cho nhanh?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

Việc thiết kế thêm **Staging Area** (vùng đệm) chính là một trong những điểm tinh tế nhất biến Git thành một công cụ quản lý phiên bản chuyên nghiệp và linh hoạt, thay vì chỉ là một công cụ copy-paste tự động.

#### 1. Ẩn dụ thực tế:
Hãy tưởng tượng bạn đang dọn nhà và đóng gói đồ đạc vào các thùng giấy để gửi đi.
*   **Working Directory** chính là **bàn làm việc** đang bừa bộn của bạn (chứa đầy sách vở, bút thước, cốc uống nước).
*   **Staging Area** chính là **khay gỗ nhỏ** đặt cạnh bàn. Bạn chủ động chọn cuốn sách A và cái bút B đặt vào khay gỗ để chuẩn bị đóng gói. Những chiếc cốc chưa dùng tới bạn vẫn để lại trên bàn.
*   **Repository (Commit)** chính là **chiếc thùng carton** sau khi bạn đã dán băng keo niêm phong và gửi vào kho lưu trữ.

Nếu không có khay gỗ (Staging Area), mỗi khi bạn muốn đóng gói (commit), Git sẽ buộc phải đóng gói toàn bộ đống bừa bộn trên bàn làm việc của bạn.

#### 2. Vai trò kỹ thuật tối thượng của Staging Area:
*   **Commit có tính chọn lọc (Selective Commits):** Bạn sửa đổi 5 file để tối ưu code, nhưng trong đó có 1 file nhạy cảm `.env` hoặc file nháp `temp.txt`. Staging Area giúp bạn chỉ chọn đúng 4 file có giá trị để commit, bỏ lại file nháp ở Working Directory.
*   **Tạo ra các Commit Nguyên Tử (Atomic Commits):** Trong khi làm việc, bạn lỡ tay sửa cả tính năng Đăng nhập và sửa một lỗi chính tả ở phần Footer. Thay vì gộp chung hai thay đổi không liên quan này vào một commit hỗn tạp, bạn có thể:
    1.  `git add login.js` → Commit với tin nhắn: `"feat: add login authentication"`.
    2.  `git add footer.html` → Commit với tin nhắn: `"fix: correct typo in footer contact info"`.
*   **Lập kế hoạch trước khi chụp ảnh:** Giúp bạn có một khoảng dừng để chạy `git diff --staged`, tự rà soát lại xem mình có lỡ tay thêm dòng code thừa nào vào "khay đóng gói" trước khi bấm nút lưu trữ vĩnh viễn hay không.

</details>

---

### Q2. Sự khác nhau giữa trạng thái "Untracked" và "Unstaged" (Modified) của một tệp tin là gì?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

Đây là hai trạng thái cực kỳ dễ gây nhầm lẫn cho người mới học khi đọc kết quả từ lệnh `git status`. Để phân biệt chúng, bạn cần nhìn vào mối quan hệ trong quá khứ giữa Git và tệp tin đó.

```
                  ┌─── Chưa từng được commit ───> [Untracked] (Tệp mới tinh)
                  │
[Tệp tin trong Git]
                  │
                  └─── Đã từng được commit ─────> Chỉnh sửa tiếp ───> [Modified / Unstaged]
```

#### 1. Trạng thái Untracked (Chưa theo dõi):
*   **Bản chất:** Là một tệp tin **hoàn toàn mới tinh** vừa được tạo ra trong thư mục dự án của bạn. Git chưa từng biết đến sự tồn tại của tệp này trong lịch sử các commit trước đây.
*   **Hành vi của Git:** Git đứng ngoài cuộc và nói: *"Tôi thấy tệp này xuất hiện trong folder, nhưng tôi sẽ bỏ qua nó hoàn toàn cho đến khi bạn chạy lệnh `git add` để yêu cầu tôi theo dõi!"*.
*   **Hiển thị:** Nằm ở mục `Untracked files:` (thường có màu đỏ).

#### 2. Trạng thái Unstaged / Modified (Đã sửa đổi nhưng chưa staged):
*   **Bản chất:** Là tệp tin **đã từng được commit ít nhất một lần** trong quá khứ (Git đã theo dõi và lưu trữ nó trong database). Tuy nhiên, gần đây bạn đã mở tệp ra và chỉnh sửa thêm bớt dòng code mới, nhưng chưa chạy lệnh `git add` để đưa các thay đổi mới đó vào Staging Area.
*   **Hành vi của Git:** Git chủ động giám sát và nói: *"Tệp này tôi đã quản lý từ trước rồi nhé, nay tôi phát hiện bạn vừa sửa đổi nội dung của nó. Hãy `git add` để cập nhật trạng thái mới nhất đi!"*.
*   **Hiển thị:** Nằm ở mục `Changes not staged for commit:` (thường ghi trạng thái `modified:` màu đỏ).

#### 🪞 Phép so sánh nhanh:
*   **Untracked** giống như một **người khách lạ** vừa bước vào công ty, chưa có thẻ nhân viên, chưa có thông tin trong phòng nhân sự.
*   **Unstaged / Modified** giống như một **nhân viên cũ** của công ty vừa thay đổi kiểu tóc mới, mọi người đều nhận ra họ nhưng sự thay đổi này chưa được cập nhật vào ảnh thẻ hồ sơ.

</details>

---

### Q3. Tại sao commit message (tin nhắn commit) lại cực kỳ quan trọng? Một commit message chuẩn cần tuân thủ những quy tắc nào?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

Lập trình viên chuyên nghiệp không chỉ viết code cho máy chạy, họ viết tài liệu để con người (và chính họ trong tương lai) đọc hiểu. **Commit Message chính là cuốn nhật ký hành trình của dự án.**

#### 1. Tại sao commit message cẩu thả là một tai họa?
Hãy tưởng tượng 6 tháng sau, hệ thống gặp lỗi nghiêm trọng ở tính năng thanh toán. Bạn mở lịch sử Git (`git log`) để tìm xem lỗi phát sinh từ đâu và đập vào mắt bạn là một chuỗi commit như thế này:
*   `fix`
*   `sửa lỗi`
*   `update code`
*   `chạy đi mà`
*   `asdffgasd`

Bạn hoàn toàn bất lực và buộc phải mở từng commit ra đọc hàng ngàn dòng code diff để mò lỗi. Bạn đã lãng phí hàng giờ đồng hồ chỉ vì sự lười biếng viết vài từ tử tế trong quá khứ.

#### 2. Quy chuẩn Conventional Commits (Chuẩn hóa quốc tế):
Cộng đồng công nghệ thế giới sử dụng quy chuẩn Conventional Commits để tự động hóa và làm sạch lịch sử Git. Cấu trúc tiêu chuẩn:

```
<type>: <mô tả ngắn gọn bằng thể chủ động>
```

Các **`<type>`** phổ biến nhất:
*   `feat`: Thêm một tính năng mới hoàn chỉnh (ví dụ: `feat: add Google login`).
*   `fix`: Sửa một lỗi (bug) trong chương trình (ví dụ: `fix: resolve crash on database reconnection`).
*   `docs`: Chỉ thay đổi tài liệu, hướng dẫn, README (ví dụ: `docs: update setup instructions`).
*   `style`: Thay đổi định dạng code (khoảng trắng, dấu chấm phẩy, format) không làm thay đổi logic chạy của code.
*   `refactor`: Cơ cấu lại cấu trúc code (tối ưu, chia nhỏ hàm) mà không thêm tính năng hay sửa bug.
*   `chore`: Các thay đổi lặt vặt về cấu hình tool, cài đặt thư viện dependency (ví dụ: `chore: add eslint dependencies`).

#### 💡 Quy tắc vàng viết commit message:
1.  **Sử dụng thể chủ động, ngắn gọn (dưới 50 ký tự).**
2.  **Giải thích TẠI SAO làm điều này, chứ không nhắc lại CODE LÀM GÌ** (vì code thay đổi gì thì Git diff đã hiển thị rõ rồi).
3.  **Tuyệt đối không commit khi chưa viết message rõ ràng.**

</details>

---

### Q4. Remote Repository trên GitHub có đồng bộ thời gian thực (Real-time sync) với Local Repository trên máy của bạn hay không?

<details>
<summary>💡 Xem Giải thích của Mr.Rom</summary>

**Trả lời:**

**Hoàn toàn không đồng bộ thời gian thực.** Đây là một đặc điểm cốt lõi vô cùng quan trọng phân biệt Git (VCS phân tán) với các dịch vụ đồng bộ file tự động như Dropbox, Google Drive hay OneDrive.

#### 1. Bản chất phân tán (Distributed Architecture):
*   Khi bạn sửa code, `git add` hay thậm chí `git commit` liên tục 100 lần ở máy cá nhân, **GitHub hoàn toàn không biết gì về những thay đổi này**. Mọi hành động chụp ảnh lịch sử đều diễn ra khép kín và an toàn bên trong thư mục ẩn `.git/` trên ổ cứng máy bạn.
*   Để đưa các thay đổi này lên GitHub, bạn phải **chủ động ra lệnh** bằng cách gõ:
    ```bash
    git push origin <tên-nhánh>
    ```
*   Ngược lại, khi đồng nghiệp của bạn đẩy code mới lên GitHub, máy local của bạn cũng không tự động cập nhật. Bạn phải chủ động kéo về bằng lệnh:
    ```bash
    git pull origin <tên-nhánh>
    ```

#### 2. Tại sao thiết kế "không đồng bộ" này lại vô cùng thông thái?
*   **Làm việc offline hoàn toàn:** Bạn có thể ngồi trên máy bay, ngoài bãi biển không có Internet để code và commit bình thường. Khi nào có mạng, bạn chỉ cần push một cú duy nhất để đồng bộ toàn bộ lịch sử 10 ngày code.
*   **Tránh phá hỏng dự án của người khác:** Hãy tưởng tượng nếu tự động sync thời gian thực giống Google Drive, khi bạn đang viết dở một đoạn code lỗi (chưa chạy được), code lỗi đó sẽ lập tức đồng bộ sang máy đồng nghiệp và làm sập toàn bộ hệ thống của họ. Việc đồng bộ chủ động qua `commit` + `push`/`pull` giúp bạn kiểm soát hoàn toàn chất lượng code trước khi chia sẻ với tập thể.

</details>

---

## 🔗 Liên kết & Tài nguyên
*   ⬅️ Quay lại bài học: [02_remote-and-github-basic.md](../../lessons/01_basic/02_remote-and-github-basic.md)
*   ➡️ Thử thách thực hành: [lab_my-first-portfolio.md](../01_basic/lab_my-first-portfolio.md)
