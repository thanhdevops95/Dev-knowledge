# Hướng Dẫn Khóa Học DevOps

Chào mừng bạn đến với lộ trình học DevOps! Đây nơi bạn sẽ tìm thấy tất cả tài liệu, bài giảng, bài tập và nộp bài làm của mình.

## Dành cho Học viên

### Bước 1: Fork và Clone Kho chứa

1.  **Fork a Repository:** Nhấn nút "Fork" ở góc trên bên phải của trang này để tạo một bản sao của kho chứa này về tài khoản GitHub của bạn.
2.  **Clone a Repository:** Sao chép kho chứa bạn vừa fork về máy tính cá nhân:
    ```bash
    git clone https://github.com/TEN_CUA_BAN/devops-learning-path.git
    cd devops-learning-path
    ```
    Thay `TEN_CUA_BAN` bằng tên tài khoản GitHub của bạn.

3.  **Thêm Remote Upstream:** Để cập nhật các thay đổi mới nhất từ kho chứa gốc của giáo viên:
    ```bash
    git remote add upstream https://github.com/TEN_GIAO_VIEN/devops-learning-path.git
    ```
    Thay `TEN_GIAO_VIEN` bằng tên tài khoản GitHub của giáo viên.

### Bước 2: Quy trình làm và nộp bài tập
Khóa học này được thiết kế để bạn xây dựng một dự án duy nhất từ đầu đến cuối. Bạn sẽ làm tất cả các bài tập trên **một nhánh duy nhất** trong suốt khóa học.

1.  **Cập nhật nhánh `main` (Chỉ làm khi có thông báo từ giáo viên):**
    Nếu giáo viên có cập nhật đề bài hoặc tài liệu, bạn cần cập nhật nhánh `main` của mình.
    ```bash
    git checkout main
    git pull upstream main
    ```

2.  **Tạo nhánh làm bài của riêng bạn (Chỉ làm 1 lần duy nhất):**
    Tạo **một nhánh duy nhất** từ `main` để làm bài. Nhánh này sẽ là nơi bạn lưu trữ toàn bộ quá trình học của mình.
    Quy tắc đặt tên nhánh: `solution/ho-ten-cua-ban`
    ```bash
    git checkout -b solution/nguyen-van-a
    ```
    *Trong suốt phần còn lại của khóa học, bạn sẽ chỉ làm việc trên nhánh này.*

3.  **Làm bài tập theo từng giai đoạn:**
    *   Đọc file hướng dẫn trong thư mục bài học tương ứng.
    *   Thực hiện các yêu cầu (ví dụ: tạo `Dockerfile`, viết file YAML...).
    *   Sau khi hoàn thành một bài học/giai đoạn, hãy commit code của bạn với một thông điệp rõ ràng.
    ```bash
    # Ví dụ sau khi hoàn thành bài Docker
    git add Dockerfile
    git commit -m "feat: Complete Lesson 08 - Dockerize application"
    ```

4.  **Nộp bài để Review (Sau mỗi giai đoạn quan trọng):**
    *   Đẩy (push) nhánh làm bài của bạn lên kho chứa đã fork. Vì bạn làm việc trên cùng một nhánh, lệnh push luôn giống nhau.
    ```bash
    git push origin solution/nguyen-van-a
    ```
    *   **Tạo Pull Request (PR) để được review:**
        *   Truy cập kho chứa đã fork của bạn trên GitHub (`https://github.com/TEN_CUA_BAN/devops-learning-path`).
        *   Chuyển sang nhánh `solution/nguyen-van-a` của bạn.
        *   Nhấn vào nút "Contribute" và sau đó "Open pull request".
        *   **QUAN TRỌNG:** Đảm bảo PR được tạo để hợp nhất từ nhánh `solution/nguyen-van-a` của bạn vào nhánh `main` của kho chứa **GỐC** (kho của giáo viên).
        *   Đặt tiêu đề PR rõ ràng, ví dụ: `Review Submission for Lesson 09 - Kubernetes`.
        *   Nhấn "Create pull request".

### Bước 3: Nhận phản hồi

*   Giáo viên sẽ xem xét bài làm của bạn và để lại nhận xét trực tiếp trên Pull Request.
*   Bạn sẽ nhận được thông báo qua email. Hãy đọc kỹ phản hồi và thực hiện các thay đổi nếu được yêu cầu.
*   Bạn có thể push thêm các commit mới để sửa lỗi theo yêu cầu ngay trên nhánh đó. Các commit mới sẽ tự động cập nhật vào PR.
*   **Sau khi giáo viên đã chấm điểm và chấp thuận, PR sẽ được ĐÓNG (CLOSED) mà KHÔNG được hợp nhất (MERGED).**
*   Bạn tiếp tục làm bài học tiếp theo trên chính nhánh `solution/nguyen-van-a` của mình và lặp lại quy trình tạo PR mới khi cần review cho bài học đó.

## Dành cho Giáo viên

### Quy trình quản lý

1.  **Chuẩn bị nội dung:** Tất cả bài giảng và đề bài nên được hoàn thiện trên nhánh `main`. Nhánh `main` là phiên bản "sạch" mà học viên sẽ bắt đầu.
2.  **Review bài làm:**
    *   Học viên sẽ tạo các Pull Request (PR) từ nhánh `solution/ten-hoc-vien` của họ vào nhánh `main` của bạn.
    *   Mỗi PR là một điểm để bạn review một giai đoạn trong dự án của họ.
    *   Trong tab "Files changed" của PR, bạn có thể xem tất cả các thay đổi tích lũy của học viên cho đến thời điểm đó.
    *   Để lại nhận xét, yêu cầu thay đổi nếu cần.
    *   **Quan trọng:** Sau khi đã chấm điểm và hài lòng, hãy **Đóng Pull Request (Close Pull Request)** và **KHÔNG HỢP NHẤT (Do Not Merge)**. Việc này giữ cho nhánh `main` của bạn luôn là phiên bản đề bài gốc, không bị ảnh hưởng bởi bài làm của học viên.

### Cách tạo kho chứa mới cho khóa học sau

Khi bạn muốn bắt đầu một khóa học mới mà không có bài làm của học viên cũ, bạn có hai cách:

1.  **Cách đơn giản:** Sao chép toàn bộ thư mục dự án (không bao gồm thư mục `.git`), tạo một kho chứa mới trên GitHub và đẩy (push) mã nguồn lên.
2.  **Cách chuyên nghiệp (dùng template):**
    *   Trên kho chứa hiện tại, vào `Settings`.
    *   Chọn "Template repository".
    *   Sau này, khi muốn tạo kho chứa mới, bạn có thể chọn "Use this template" để tạo một bản sao sạch sẽ, không bao gồm lịch sử commit và các nhánh khác.

Chúc bạn và các học viên có một khóa học thành công!
