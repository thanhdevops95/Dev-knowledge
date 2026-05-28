# Bài 6: Lý thuyết về CI/CD

## 🎯 Mục tiêu bài học

-   Hiểu rõ định nghĩa và mục đích của Tích hợp liên tục (CI), Giao hàng liên tục (CD), và Triển khai liên tục (CD).
-   Phân biệt được sự khác nhau giữa Continuous Delivery và Continuous Deployment.
-   Nắm được các lợi ích mà một quy trình CI/CD hoàn chỉnh mang lại.
-   Hiểu được các giai đoạn chính trong một đường ống (pipeline) CI/CD.

## 📖 Nội dung chính

1.  **Vấn đề của quy trình thủ công:** Tại sao chúng ta cần CI/CD?
2.  **Tích hợp liên tục (Continuous Integration - CI):** Hợp nhất và kiểm thử code thường xuyên.
3.  **Giao hàng liên tục (Continuous Delivery - CD):** Luôn sẵn sàng để triển khai.
4.  **Triển khai liên tục (Continuous Deployment - CD):** Tự động triển khai lên production.
5.  **So sánh Continuous Delivery vs. Continuous Deployment.**
6.  **Đường ống CI/CD (CI/CD Pipeline):** Các bước tự động hóa.
7.  **Lợi ích của CI/CD.**

## 🛠️ Công cụ & Lý thuyết

-   **Lý thuyết:** CI/CD Principles, Build Automation, Test Automation, Deployment Strategies.
-   **Công cụ (sẽ học):** <u>GitLab CI</u>, Jenkins, GitHub Actions, Docker, Kubernetes.

---

# Nội dung chi tiết - Bài 6: Lý thuyết về CI/CD

Sau khi đã có mã nguồn được quản lý bằng Git, câu hỏi tiếp theo là: "Làm thế nào để đưa những thay đổi trong code đến tay người dùng một cách nhanh chóng và an toàn?". Câu trả lời nằm ở CI/CD, trái tim của DevOps hiện đại.

---

### 1. Vấn đề của quy trình thủ công

Trong quá khứ, quy trình diễn ra như sau:
-   Nhiều lập trình viên làm việc trên các nhánh riêng trong nhiều tuần, nhiều tháng.
-   Đến "ngày tích hợp", mọi người cố gắng hợp nhất code lại với nhau -> "Địa ngục hợp nhất" (Merge Hell) với vô số xung đột.
-   Sau khi hợp nhất, một đội QA riêng sẽ kiểm thử thủ công trong vài ngày.
-   Cuối cùng, đội Ops sẽ triển khai thủ công, thường là vào ban đêm hoặc cuối tuần để giảm ảnh hưởng nếu có lỗi.

Quy trình này **chậm chạp, rủi ro cao, và đầy căng thẳng**. CI/CD ra đời để giải quyết triệt để các vấn đề này.

---

### 2. Tích hợp liên tục (Continuous Integration - CI)

**CI là phương pháp thực hành mà các lập trình viên hợp nhất (merge) code của họ vào một kho chứa chung nhiều lần trong một ngày.**

Mỗi khi code được hợp nhất (thường là sau một `git push` lên nhánh `develop`), một quy trình tự động sẽ được kích hoạt:
1.  **Build:** Biên dịch mã nguồn và đóng gói thành một sản phẩm có thể chạy được (ví dụ: file `.jar`, `.exe`, hoặc một Docker image).
2.  **Test:** Tự động chạy một bộ các bài kiểm thử (unit tests, integration tests) để xác minh rằng thay đổi mới không làm hỏng các tính năng hiện có.

**Mục tiêu của CI:** **Phát hiện và sửa lỗi sớm.** Nếu quá trình build hoặc test thất bại, cả đội sẽ được thông báo ngay lập tức. Họ phải ưu tiên sửa lỗi này trước khi làm bất cứ việc gì khác. Điều này đảm bảo rằng kho chứa chung luôn ở trạng thái ổn định.

---

### 3. Giao hàng liên tục (Continuous Delivery - CD)

**Continuous Delivery là bước phát triển tiếp theo của CI. Nó đảm bảo rằng sau mỗi lần CI thành công, sản phẩm đã build và test sẽ được tự động triển khai đến một môi trường giống-như-production (ví dụ: Staging, UAT).**

Ở giai đoạn này, sản phẩm đã vượt qua tất cả các kiểm thử tự động và **về mặt kỹ thuật là sẵn sàng để được triển khai cho người dùng.**

Tuy nhiên, việc triển khai lên môi trường Production **cần một bước phê duyệt thủ công**. Đây có thể là một cú click chuột của Product Manager, QA Lead, hoặc một người có thẩm quyền sau khi họ đã kiểm tra sản phẩm trên môi trường Staging.

**Mục tiêu của Continuous Delivery:** **Giảm rủi ro khi release.** Bằng cách luôn có một phiên bản sẵn sàng, việc quyết định "khi nào" release trở thành một quyết định kinh doanh, không phải là một vấn đề kỹ thuật.

---

### 4. Triển khai liên tục (Continuous Deployment - CD)

**Continuous Deployment là mức độ tự động hóa cao nhất. Nó tự động triển khai mọi thay đổi vượt qua tất cả các giai đoạn kiểm thử thẳng lên môi trường Production mà không cần bất kỳ sự can thiệp nào của con người.**

Chỉ có những công ty có văn hóa kiểm thử rất mạnh và các cơ chế giám sát, rollback tự động tinh vi mới dám áp dụng hình thức này (ví dụ: Facebook, Amazon, Netflix).

---

### 5. So sánh Continuous Delivery vs. Continuous Deployment

| Tiêu chí             | Continuous Delivery (Giao hàng liên tục)              | Continuous Deployment (Triển khai liên tục)           |
| --------------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| **Triển khai lên Production** | Cần một bước phê duyệt **thủ công**.                  | Hoàn toàn **tự động**.                               |
| **Tần suất triển khai** | Vài lần một ngày hoặc vài lần một tuần.               | Có thể lên đến hàng trăm, hàng ngàn lần một ngày.      |
| **Mức độ rủi ro**     | Thấp. Có bước kiểm tra cuối cùng của con người.       | Cao hơn. Phụ thuộc hoàn toàn vào kiểm thử tự động. |
| **Phù hợp với**       | Hầu hết các công ty.                                  | Các công ty công nghệ hàng đầu với văn hóa DevOps chín muồi. |

**Lưu ý:** Cả hai đều bắt đầu bằng "CD", dễ gây nhầm lẫn. Trong ngữ cảnh chung, khi nói "CI/CD", "CD" thường ám chỉ Continuous Delivery.

---

### 6. Đường ống CI/CD (CI/CD Pipeline)

Pipeline là hiện thực hóa của quy trình CI/CD. Nó là một chuỗi các giai đoạn (stages) được thực thi một cách tuần tự hoặc song song. Một pipeline điển hình bao gồm:

1.  **Source Stage:** Kích hoạt khi có commit mới.
2.  **Build Stage:** Biên dịch code, tạo package.
3.  **Test Stage:** Chạy unit test, integration test, static code analysis.
4.  **Deploy to Staging Stage:** Triển khai lên môi trường Staging.
5.  **Approval Stage (trong Continuous Delivery):** Chờ phê duyệt thủ công.
6.  **Deploy to Production Stage:** Triển khai lên môi trường Production.

---

### 7. Lợi ích của CI/CD

-   **Giảm rủi ro:** Phát hiện lỗi sớm, triển khai các thay đổi nhỏ giúp dễ dàng xác định và sửa lỗi hơn.
-   **Tăng tốc độ phát hành:** Tự động hóa giúp loại bỏ các nút thắt cổ chai thủ công.
-   **Tăng năng suất lập trình viên:** Họ có thể tập trung vào việc viết code thay vì các công việc triển khai lặp đi lặp lại.
-   **Tăng độ tin cậy:** Quy trình nhất quán đảm bảo chất lượng.
-   **Tăng sự tự tin:** Cả đội tự tin hơn khi thực hiện các thay đổi.

## ✍️ Bài tập thực hành (Exercises)

Hãy suy ngẫm và trả lời các câu hỏi tình huống sau để củng cố sự hiểu biết của bạn về CI/CD.

**Câu 1: CI - Tích hợp liên tục**
-   Một lập trình viên trong đội của bạn nói: "Tôi không cần một pipeline tự động. Tôi vẫn merge code của mình vào nhánh `develop` mỗi cuối ngày."
-   Theo bạn, cách làm này có thực sự được coi là Continuous Integration (CI) không? Tại sao? Yếu tố **tự động** nào là then chốt và không thể thiếu của một quy trình CI đúng nghĩa?

**Câu 2: Continuous Delivery vs. Continuous Deployment**
-   Công ty của bạn đang phát triển một ứng dụng ngân hàng trực tuyến, nơi mà các lỗi nhỏ cũng có thể gây ra thiệt hại tài chính lớn.
-   Theo bạn, mô hình **Continuous Delivery** hay **Continuous Deployment** sẽ phù hợp hơn cho việc triển khai ứng dụng này lên môi trường Production? Hãy giải thích lý do tại sao bạn chọn mô hình đó, xét đến yếu tố rủi ro và các quy định có thể có của ngành tài chính.

**Câu 3: Thiết kế Pipeline**
-   Hãy phác thảo (bằng các gạch đầu dòng) các giai đoạn (stages) cơ bản nhất cho một CI/CD pipeline của một dự án website tĩnh (ví dụ: HTML, CSS, aJavaScript).
-   Bắt đầu từ lúc lập trình viên `git push` lên kho chứa và kết thúc ở việc website được triển khai lên một môi trường Staging để kiểm thử.

**Câu 4: Lợi ích của CI/CD**
-   Trong các lợi ích được liệt kê của CI/CD, hãy chọn ra 2 lợi ích mà bạn cho là quan trọng nhất đối với một **lập trình viên**.
-   Giải thích tại sao chúng lại quan trọng và chúng trực tiếp giải quyết vấn đề gì trong công việc hàng ngày của một lập trình viên so với quy trình làm việc thủ công?

---

Trong bài học tiếp theo, chúng ta sẽ bắt tay vào thực hành, xây dựng một pipeline CI/CD đơn giản bằng GitLab CI.

[Bài trước: Git - Hệ thống Quản lý Phiên bản](../05-git-version-control/) | [Quay lại Mục lục chính](../../README.md) | [Bài tiếp theo: Xây dựng CI/CD Pipeline với GitLab CI](../07-gitlab-ci-pipeline/)