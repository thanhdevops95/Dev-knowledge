# Bài 4: Nhập môn Mạng máy tính (Networking Concepts)

## 🎯 Mục tiêu bài học

- Hiểu được cách các máy tính và dịch vụ giao tiếp với nhau qua mạng.
- Nắm được các khái niệm cốt lõi: địa chỉ IP, TCP/IP, DNS, và các cổng (ports).
- Phân biệt được vai trò của các thành phần mạng quan trọng như Firewall và Load Balancer.
- Hiểu khái niệm về Mạng riêng ảo (VPC) trên môi trường cloud.

## 📖 Nội dung chính

1.  **Mô hình TCP/IP:** Các lớp (layer) và vai trò của chúng.
2.  **Địa chỉ IP và Ports:** "Địa chỉ nhà" và "số căn hộ" của một dịch vụ.
3.  **DNS (Domain Name System):** "Danh bạ" của Internet.
4.  **HTTP/HTTPS:** Giao thức web và tại sao HTTPS lại quan trọng.
5.  **Firewall (Tường lửa):** "Bảo vệ" của hệ thống mạng.
6.  **Load Balancer (Bộ cân bằng tải):** Phân phối traffic để tránh quá tải.
7.  **VPC (Virtual Private Cloud):** Mạng riêng của bạn trên đám mây.

## 🛠️ Công cụ & Lý thuyết

-   **Lý thuyết:** TCP/IP Model, OSI Model, DNS Resolution, Load Balancing.
-   **Công cụ:** `ping`, `curl`, `netstat`, `ss`, `nslookup`, `dig`, `traceroute`.

---

# Nội dung chi tiết - Bài 4: Nhập môn Mạng máy tính

Trong thế giới DevOps, các ứng dụng không tồn tại một cách cô lập. Chúng là một phần của một hệ thống phân tán, bao gồm nhiều máy chủ, dịch vụ, và database giao tiếp với nhau qua mạng. Hiểu được các khái niệm mạng cơ bản là điều bắt buộc để bạn có thể xây dựng, triển khai và gỡ lỗi các hệ thống phức tạp.

---

### 1. Mô hình TCP/IP

Hãy tưởng tượng việc gửi một gói hàng. Bạn cần địa chỉ người nhận, người gửi, gói hàng được đóng gói, và phương tiện vận chuyển. Mạng máy tính cũng tương tự và được mô tả qua mô hình TCP/IP.

-   **Application Layer:** Lớp ứng dụng (HTTP, FTP, SMTP) - nơi dữ liệu của bạn được tạo ra.
-   **Transport Layer:** Lớp vận chuyển (TCP, UDP) - đảm bảo dữ liệu được gửi đi một cách tin cậy (TCP) hoặc nhanh nhất có thể (UDP). Nó giống như việc bạn chọn gửi bảo đảm hay gửi thường.
-   **Internet Layer:** Lớp Internet (IP) - chịu trách nhiệm định tuyến, tìm đường đi cho gói tin trên mạng.
-   **Link Layer:** Lớp liên kết (Ethernet, Wi-Fi) - xử lý việc truyền dữ liệu vật lý qua dây cáp hoặc sóng vô tuyến.

---

### 2. Địa chỉ IP và Ports

-   **Địa chỉ IP (Internet Protocol):** Là một địa chỉ duy nhất định danh một thiết bị trên mạng, ví dụ `172.217.22.14` (IPv4). Nó giống như địa chỉ nhà của bạn.
-   **Port (Cổng):** Một máy chủ có thể chạy nhiều dịch vụ cùng lúc (web, email, database). Port là một con số (từ 0 đến 65535) để phân biệt các dịch vụ đó. Nó giống như số căn hộ trong một tòa chung cư.
    -   Port 80: HTTP (web server)
    -   Port 443: HTTPS (web server bảo mật)
    -   Port 22: SSH (đăng nhập từ xa)
    -   Port 5432: PostgreSQL (database)

Khi bạn truy cập `google.com:443`, bạn đang nói: "Hãy kết nối đến máy chủ có địa chỉ IP của google.com, và nói chuyện với dịch vụ đang chạy ở cổng 443".

---

### 3. DNS (Domain Name System)

Con người dễ nhớ tên (`google.com`) hơn là địa chỉ IP (`172.217.22.14`). DNS là hệ thống giúp dịch từ tên miền sang địa chỉ IP.

> DNS là "Danh bạ điện thoại của Internet".

Khi bạn gõ `google.com` vào trình duyệt, máy tính của bạn sẽ hỏi một máy chủ DNS: "Địa chỉ IP của `google.com` là gì?". Máy chủ DNS trả về `172.217.22.14`, và trình duyệt của bạn bắt đầu kết nối đến địa chỉ đó.
-   Lệnh `nslookup google.com` hoặc `dig google.com` giúp bạn tự tra cứu DNS.

---

### 4. HTTP/HTTPS

-   **HTTP (HyperText Transfer Protocol):** Là giao thức chính được sử dụng để tải các trang web. Tuy nhiên, dữ liệu HTTP được truyền đi dưới dạng văn bản thuần, không mã hóa, do đó có thể bị nghe lén.
-   **HTTPS (HTTP Secure):** Là phiên bản an toàn của HTTP. Nó sử dụng mã hóa SSL/TLS để bảo vệ dữ liệu giữa trình duyệt của bạn và máy chủ web. Mọi trang web hiện đại đều phải sử dụng HTTPS. Dấu hiệu là ổ khóa trên thanh địa chỉ trình duyệt.

---

### 5. Firewall (Tường lửa)

Firewall hoạt động như một người bảo vệ cho hệ thống mạng của bạn. Nó kiểm soát traffic đi vào và đi ra dựa trên một bộ quy tắc (rules).

-   Ví dụ, bạn có thể tạo một rule: "Chỉ cho phép traffic đến từ cổng 443 (HTTPS). Chặn tất cả các cổng khác."
-   Firewall giúp ngăn chặn các truy cập trái phép và các cuộc tấn công từ bên ngoài.

---

### 6. Load Balancer (Bộ cân bằng tải)

Khi một trang web có hàng triệu người truy cập, một máy chủ web duy nhất sẽ bị quá tải. Load Balancer là một thiết bị (phần cứng hoặc phần mềm) đứng trước nhiều máy chủ web và phân phối các yêu cầu (requests) của người dùng đến các máy chủ đó.

-   **Lợi ích:**
    -   **Tăng khả năng chịu tải:** Phục vụ được nhiều người dùng hơn.
    -   **Tăng độ tin cậy (High Availability):** Nếu một máy chủ web bị lỗi, Load Balancer sẽ tự động chuyển traffic sang các máy chủ còn lại.
    -   **Dễ dàng bảo trì:** Bạn có thể gỡ một máy chủ ra để nâng cấp mà không làm gián đoạn dịch vụ.

---

### 7. VPC (Virtual Private Cloud)

Trên các nền tảng đám mây như AWS, Azure, hay GCP, VPC cho phép bạn tạo ra một không gian mạng riêng tư, hoàn toàn cô lập.

Trong VPC, bạn có toàn quyền kiểm soát:
-   Dải địa chỉ IP riêng.
-   Tạo các mạng con (subnets).
-   Cấu hình bảng định tuyến (route tables).
-   Thiết lập các Firewall (Security Groups, Network ACLs).

VPC giống như việc bạn xây dựng một mạng LAN của riêng mình, nhưng trên nền tảng ảo hóa của nhà cung cấp đám mây.

## ✍️ Bài tập thực hành (Exercises)

Các khái niệm về mạng có thể hơi trừu tượng. Hãy dùng các câu hỏi và lệnh sau để kiểm tra lại hiểu biết của bạn.

**Câu 1: Lý thuyết TCP/IP và DNS**
1.  Trình bày vai trò của DNS trong một yêu cầu truy cập web. Ví dụ, khi bạn gõ `https://google.com` vào trình duyệt, luồng đi của yêu cầu sẽ như thế nào **trước khi** trình duyệt của bạn thực sự bắt đầu tải trang web?
2.  TCP và UDP khác nhau ở điểm nào là cơ bản nhất? Tại sao các dịch vụ đòi hỏi độ tin cậy cao (như chuyển tiền, tải file) lại dùng TCP, trong khi các dịch vụ ưu tiên tốc độ (như game online, gọi video) có thể dùng UDP?

**Bài 2: Sử dụng Công cụ Dòng lệnh (Thực hành)**
1.  Mở terminal và chạy lệnh `ping 8.8.8.8` (đây là địa chỉ DNS server của Google). Lệnh này cho bạn biết thông tin gì về kết nối mạng của bạn?
2.  Dùng lệnh `nslookup github.com` (hoặc `dig github.com`). Lệnh này trả về (các) địa chỉ IP nào cho tên miền `github.com`?
3.  Chạy lệnh `curl -I https://www.vietnamnet.vn` (cờ `-I` là để lấy phần header của phản hồi HTTP). Trong kết quả trả về, bạn có thấy thông tin về `server` họ đang dùng là gì không?
4.  Trên máy Linux hoặc Mac, chạy lệnh `ss -tuln` hoặc `netstat -tuln`. Lệnh này liệt kê các cổng đang "lắng nghe" (LISTENING) trên máy của bạn. Bạn có thấy cổng nào quen thuộc không?

**Câu 3: Firewall và Ports**
1.  Giả sử bạn có một máy chủ ứng dụng (Application Server). Dịch vụ của bạn cần giao tiếp với một máy chủ cơ sở dữ liệu (Database Server). Để đảm bảo an toàn, bạn cấu hình Firewall cho Database Server.
2.  Hãy viết ra một quy tắc Firewall (diễn giải bằng lời) mà bạn sẽ đặt cho Database Server, liên quan đến Application Server. (Gợi ý: Cần cho phép kết nối từ đâu, đến cổng nào, và hành động là gì?).

**Câu 4: Load Balancer**
1.  Giải thích tại sao việc chỉ tăng cấu hình (CPU, RAM) cho một máy chủ duy nhất (còn gọi là "scale-up" hay "mở rộng theo chiều dọc") không phải lúc nào cũng là giải pháp tốt bằng việc thêm nhiều máy chủ và dùng Load Balancer ("scale-out" hay "mở rộng theo chiều ngang")? Nêu ít nhất 2 lợi ích của việc scale-out.

---

Trong phần tiếp theo, chúng ta sẽ tìm hiểu về Git, công cụ không thể thiếu để quản lý mã nguồn - tài sản quan trọng nhất của mọi dự án phần mềm.

[Bài trước: Kỹ năng Viết Script (Bash Scripting)](../03-scripting-for-automation/) | [Quay lại Mục lục chính](../../README.md) | [Bài tiếp theo: Git - Hệ thống Quản lý Phiên bản](../../Lesson02-scm-and-ci/05-git-version-control/)