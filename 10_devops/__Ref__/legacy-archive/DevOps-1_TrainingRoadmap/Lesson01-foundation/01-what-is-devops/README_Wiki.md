# Bài 1: DevOps là gì?

## 🎯 Mục tiêu bài học

-   Hiểu rõ định nghĩa, triết lý và văn hóa của DevOps.
-   Nắm được mô hình CALMS (Culture, Automation, Lean, Measurement, Sharing).
-   Phân biệt được DevOps với các mô hình phát triển truyền thống như Waterfall và Agile.
-   Hiểu được lợi ích mà DevOps mang lại cho tổ chức.

## 📖 Nội dung chính

1.  **Bối cảnh ra đời:** Tại sao DevOps lại xuất hiện?
2.  **Định nghĩa DevOps:** Không chỉ là công cụ, mà là văn hóa và tư duy.
3.  **5 Trụ cột của DevOps (CALMS):** Phân tích chi tiết từng thành phần.
4.  **Vòng đời DevOps:** Plan -> Code -> Build -> Test -> Release -> Deploy -> Operate -> Monitor.
5.  **Lợi ích kinh doanh:** Tăng tốc độ, cải thiện chất lượng, giảm rủi ro.

## 🛠️ Công cụ & Lý thuyết

-   **Phương pháp luận:** <u>DevOps</u>, Agile, Scrum, Waterfall.
-   **Mô hình văn hóa:** <u>CALMS</u>, The Three Ways.

## ✍️ Bài tập thực hành (Exercises)

Đây là các câu hỏi lý thuyết giúp bạn củng cố lại những kiến thức đã học trong bài. Hãy thử tự trả lời trước khi tìm kiếm lại trong tài liệu.

-   **Câu 1:** "Bức tường của sự nhầm lẫn" (The Wall of Confusion) là gì? Giải thích bằng một ví dụ thực tế mà bạn có thể tưởng tượng ra trong một công ty phần mềm.
-   **Câu 2:** Tại sao nói DevOps là một "văn hóa" chứ không chỉ là một chức danh hay một bộ công cụ?
-   **Câu 3:** Trong 5 trụ cột của mô hình CALMS, bạn cho rằng trụ cột nào là khó áp dụng nhất khi một tổ chức bắt đầu chuyển đổi sang DevOps? Tại sao?
-   **Câu 4:** Lấy một ví dụ về một công việc lặp đi lặp lại trong quá trình phát triển phần mềm mà có thể được "Tự động hóa" (Automation) để cải thiện quy trình.

---

# Nội dung chi tiết - Bài 1: DevOps là gì?

Chào mừng bạn đến với bài học đầu tiên trên hành trình trở thành Kỹ sư DevOps. Trước khi đi sâu vào các công cụ phức tạp, điều quan trọng nhất là phải hiểu đúng về triết lý và văn hóa đằng sau DevOps.

---

### 1. Bối cảnh ra đời: "Bức tường của sự nhầm lẫn" (The Wall of Confusion)

Trong các mô hình phát triển phần mềm truyền thống, thường tồn tại một "bức tường" vô hình giữa hai đội:

-   **Development (Dev):** Đội ngũ phát triển, mục tiêu của họ là xây dựng và cho ra mắt các tính năng mới càng nhanh càng tốt.
-   **Operations (Ops):** Đội ngũ vận hành, mục tiêu của họ là giữ cho hệ thống ổn định, an toàn và hoạt động 24/7.

Sự xung đột về mục tiêu này tạo ra một "Bức tường của sự nhầm lẫn":
-   Dev "ném code qua tường" cho Ops và không quan tâm đến việc triển khai hay vận hành sau đó.
-   Ops gặp khó khăn khi triển khai code mới, thường xuyên phải đối mặt với các lỗi phát sinh trên môi trường production mà họ không hiểu rõ.
-   Kết quả: Tốc độ ra mắt sản phẩm chậm, chất lượng thấp, và văn hóa đổ lỗi lẫn nhau.

**DevOps ra đời như một giải pháp để phá vỡ bức tường này.**

---

### 2. Định nghĩa DevOps: Không chỉ là Công cụ hay Chức danh

Nhiều người lầm tưởng DevOps là một công cụ, một chức danh công việc, hay một đội riêng biệt. Thực tế, DevOps là một **VĂN HÓA (CULTURE)**, một **TƯ DUY (MINDSET)**, và một tập hợp các **PHƯƠNG PHÁP THỰC HÀNH (PRACTICES)**.

> **DevOps là sự kết hợp giữa triết lý văn hóa, phương pháp thực hành và công cụ nhằm tăng khả năng cung cấp ứng dụng và dịch vụ của một tổ chức với tốc độ cao.**

Mục tiêu cốt lõi là tạo ra sự **hợp tác** và **chia sẻ trách nhiệm** giữa các nhóm Dev, Ops, QA (Kiểm thử chất lượng), và Security trong toàn bộ vòng đời của sản phẩm, từ lúc lên ý tưởng cho đến khi vận hành và nhận phản hồi từ người dùng.

---

### 3. Năm Trụ cột của DevOps (Mô hình CALMS)

Mô hình CALMS là một cách tuyệt vời để tóm tắt các khía cạnh chính của DevOps.

-   **C - Culture (Văn hóa):** Đây là trụ cột quan trọng nhất. Nó nói về việc phá vỡ các "silo" (làm việc độc lập), xây dựng lòng tin, khuyến khích thử nghiệm, và xem thất bại như một cơ hội để học hỏi.
-   **A - Automation (Tự động hóa):** Tự động hóa mọi thứ có thể trong quy trình phát triển và triển khai: từ việc build code, chạy kiểm thử, đến việc cấp phát hạ tầng. Mục đích là để giảm thiểu lỗi do con người và tăng tốc độ.
-   **L - Lean (Tinh gọn):** Áp dụng các nguyên tắc sản xuất tinh gọn vào phát triển phần mềm. Tập trung vào việc loại bỏ lãng phí, giao hàng theo từng phần nhỏ, và nhận phản hồi nhanh chóng.
-   **M - Measurement (Đo lường):** "Bạn không thể cải thiện những gì bạn không thể đo lường". Thu thập dữ liệu (metrics) về mọi thứ, từ thời gian build, tỷ lệ lỗi, đến hiệu năng ứng dụng. Dữ liệu này giúp đưa ra quyết định chính xác.
-   **S - Sharing (Chia sẻ):** Khuyến khích việc chia sẻ kiến thức, công cụ, và trách nhiệm giữa các đội. Khi Dev hiểu về vận hành và Ops hiểu về code, sản phẩm cuối cùng sẽ tốt hơn.

---

### 4. Vòng đời DevOps (DevOps Lifecycle)

Vòng đời DevOps là một vòng lặp vô tận, thể hiện tính liên tục của quy trình.

![DevOps Lifecycle](https://www.simform.com/wp-content/uploads/2022/01/what-is-devops-lifecycle-1024x628.png)

1.  **Plan (Kế hoạch):** Lên kế hoạch và định nghĩa các tính năng.
2.  **Code (Viết mã):** Phát triển và quản lý mã nguồn (ví dụ: dùng Git).
3.  **Build (Xây dựng):** Tích hợp mã nguồn và xây dựng thành sản phẩm có thể chạy được (Tích hợp liên tục - CI).
4.  **Test (Kiểm thử):** Tự động chạy các bài kiểm thử để đảm bảo chất lượng.
5.  **Release (Phát hành):** Chuẩn bị phiên bản để triển khai.
6.  **Deploy (Triển khai):** Tự động triển khai ứng dụng lên môi trường production (Triển khai liên tục - CD).
7.  **Operate (Vận hành):** Quản lý và duy trì hạ tầng cho ứng dụng.
8.  **Monitor (Giám sát):** Thu thập dữ liệu, log và giám sát hiệu năng của ứng dụng để nhận phản hồi và quay trở lại bước **Plan**.

---

### 5. Lợi ích của DevOps

-   **Tốc độ:** Ra mắt sản phẩm và tính năng mới nhanh hơn, giúp tăng lợi thế cạnh tranh.
-   **Chất lượng và Độ tin cậy:** Giảm tỷ lệ lỗi trên production nhờ tự động hóa kiểm thử và quy trình triển khai nhất quán.
-   **Bảo mật:** Tích hợp bảo mật vào sớm trong vòng đời phát triển (DevSecOps).
-   **Khả năng mở rộng:** Quản lý hạ tầng phức tạp và mở rộng một cách hiệu quả.
-   **Cải thiện văn hóa làm việc:** Giảm căng thẳng, tăng sự hài lòng và hiệu suất của nhân viên.

Trong bài học tiếp theo, chúng ta sẽ bắt đầu với công cụ nền tảng và thiết yếu nhất đối với mọi Kỹ sư DevOps: **Dòng lệnh Linux**.

---

[Quay lại Mục lục chính](../../README.md) | [Bài tiếp theo: Làm chủ Dòng lệnh Linux](../02-linux-cli/)