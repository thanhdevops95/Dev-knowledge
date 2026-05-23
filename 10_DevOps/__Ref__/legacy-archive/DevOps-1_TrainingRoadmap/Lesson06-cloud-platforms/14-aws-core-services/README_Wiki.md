# Bài 14: Nhập môn AWS (Amazon Web Services)

## 🎯 Mục tiêu bài học

-   Hiểu được Cloud Computing là gì và các mô hình dịch vụ (IaaS, PaaS, SaaS).
-   Nắm được các khái niệm toàn cầu của AWS: Regions, Availability Zones (AZs).
-   Làm quen với vai trò và chức năng của các dịch vụ AWS cốt lõi mà mọi Kỹ sư DevOps cần biết.
-   Thực hành tạo và tương tác với các dịch vụ này thông qua AWS Management Console.

## 📖 Nội dung chính

1.  **Tổng quan về Cloud Computing và AWS.**
2.  **Kiến trúc toàn cầu của AWS:** Regions, Availability Zones, Edge Locations.
3.  **Quản lý danh tính và truy cập (Identity and Access Management - IAM):**
    -   `User`: Người dùng.
    -   `Group`: Nhóm người dùng.
    -   `Role`: Vai trò, dùng để cấp quyền cho dịch vụ AWS.
    -   `Policy`: Các quy tắc cấp quyền.
4.  **Dịch vụ Compute cốt lõi:**
    -   **EC2 (Elastic Compute Cloud):** Máy chủ ảo.
5.  **Dịch vụ Storage cốt lõi:**
    -   **S3 (Simple Storage Service):** Lưu trữ đối tượng (files, images, backups).
6.  **Dịch vụ Networking cốt lõi:**
    -   **VPC (Virtual Private Cloud):** Mạng riêng ảo của bạn trên AWS.
7.  **Dịch vụ Database cốt lõi:**
    -   **RDS (Relational Database Service):** Dịch vụ cơ sở dữ liệu quan hệ được quản lý (MySQL, PostgreSQL...).

## 🛠️ Công cụ & Lý thuyết

-   **Nhà cung cấp Cloud:** <u>AWS</u>, Google Cloud (GCP), Microsoft Azure.
-   **Công cụ tương tác:** AWS Management Console, AWS CLI.
-   **Lý thuyết:** Cloud Computing (IaaS, PaaS, SaaS), High Availability, Scalability.

---

# Nội dung chi tiết - Bài 14: Nhập môn AWS (Amazon Web Services)

Hầu hết các công ty hiện nay đều xây dựng và vận hành hạ tầng của họ trên các nền tảng điện toán đám mây (Cloud Computing) thay vì tự xây dựng trung tâm dữ liệu riêng. AWS là nhà cung cấp đám mây lớn nhất và phổ biến nhất thế giới, do đó, việc thành thạo các dịch vụ cốt lõi của AWS là một kỹ năng không thể thiếu của Kỹ sư DevOps.

---

### 1. Tổng quan về Cloud Computing và AWS

**Cloud Computing** là việc cung cấp các tài nguyên máy tính (máy chủ, lưu trữ, database, mạng, phần mềm...) qua Internet theo mô hình "trả tiền theo dung lượng sử dụng" (pay-as-you-go).

**Các mô hình dịch vụ:**
-   **IaaS (Infrastructure as a Service):** Bạn thuê hạ tầng cơ bản (máy chủ ảo, mạng, lưu trữ). Bạn chịu trách nhiệm quản lý hệ điều hành và mọi thứ bên trên nó. (Ví dụ: AWS EC2).
-   **PaaS (Platform as a Service):** Bạn chỉ cần tập trung vào việc viết code. Nhà cung cấp đám mây sẽ lo về hệ điều hành, runtime, scaling... (Ví dụ: Heroku, AWS Elastic Beanstalk).
-   **SaaS (Software as a Service):** Bạn sử dụng một phần mềm hoàn chỉnh qua Internet. (Ví dụ: Gmail, Salesforce).

---

### 2. Kiến trúc toàn cầu của AWS

-   **Regions (Vùng):** Là các khu vực địa lý riêng biệt trên toàn thế giới nơi AWS đặt các trung tâm dữ liệu (ví dụ: `us-east-1` ở Bắc Virginia, `ap-southeast-1` ở Singapore). Bạn nên chọn Region gần với người dùng của mình nhất để giảm độ trễ.
-   **Availability Zones (AZs - Vùng sẵn sàng):** Mỗi Region bao gồm nhiều AZ. Mỗi AZ là một hoặc nhiều trung tâm dữ liệu riêng biệt với nguồn điện, hệ thống làm mát, và mạng riêng. Các AZ được kết nối với nhau bằng đường truyền tốc độ cao, độ trễ thấp.
    -   **Mục đích:** Để xây dựng các ứng dụng có **tính sẵn sàng cao (High Availability)**. Bằng cách triển khai ứng dụng trên nhiều AZ, nếu một AZ gặp sự cố (mất điện, thiên tai), ứng dụng của bạn vẫn có thể hoạt động ở các AZ còn lại.

---

### 3. Quản lý danh tính và truy cập (IAM)

IAM là dịch vụ cho phép bạn quản lý quyền truy cập vào các tài nguyên AWS một cách an toàn. Đây là dịch vụ bạn nên tìm hiểu đầu tiên.

-   **Users:** Một thực thể đại diện cho một người hoặc một ứng dụng cần tương tác với AWS.
-   **Groups:** Một tập hợp các user. Thay vì gán quyền cho từng user, bạn có thể gán quyền cho group, và mọi user trong group sẽ có quyền đó.
-   **Policies:** Là một tài liệu JSON định nghĩa các quyền (cho phép hoặc từ chối) đối với một hành động trên một tài nguyên. Ví dụ: "Cho phép đọc tất cả các đối tượng trong S3 bucket `my-bucket`".
-   **Roles:** Một vai trò (role) tương tự như user, nhưng nó được thiết kế để các dịch vụ AWS có thể "đảm nhận" (assume) và có được các quyền tạm thời để thực hiện một hành động. Ví dụ, bạn tạo một Role cho phép EC2 có quyền ghi file vào S3.

**Nguyên tắc cốt lõi:** Nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege). Chỉ cấp cho user hoặc service những quyền tối thiểu cần thiết để thực hiện công việc của họ.

---

### 4. Dịch vụ Compute cốt lõi: EC2

**EC2 (Elastic Compute Cloud)** là dịch vụ cho phép bạn thuê các máy chủ ảo trên đám mây.
-   Bạn có thể chọn loại máy (instance type) với cấu hình CPU, RAM khác nhau.
-   Bạn có thể chọn hệ điều hành (Amazon Machine Image - AMI).
-   Bạn toàn quyền kiểm soát máy chủ đó, có thể SSH vào và cài đặt bất cứ thứ gì bạn muốn (mô hình IaaS).

---

### 5. Dịch vụ Storage cốt lõi: S3

**S3 (Simple Storage Service)** là dịch vụ lưu trữ đối tượng (object storage) với độ bền, tính sẵn sàng và khả năng mở rộng gần như vô hạn.
-   Bạn không lưu trữ hệ điều hành hay chạy ứng dụng trên S3. Bạn lưu trữ **files**: hình ảnh, video, file backup, file log, các file tĩnh cho trang web...
-   Dữ liệu được tổ chức trong các **buckets** (tên bucket phải là duy nhất trên toàn cầu).

---

### 6. Dịch vụ Networking cốt lõi: VPC

**VPC (Virtual Private Cloud)** cho phép bạn tạo ra một không gian mạng logic hoàn toàn cô lập trên AWS, nơi bạn có thể triển khai các tài nguyên AWS của mình.
-   Bạn có toàn quyền kiểm soát môi trường mạng ảo của mình, bao gồm việc chọn dải địa chỉ IP riêng, tạo các mạng con (subnets), cấu hình bảng định tuyến (route tables) và cổng mạng (gateways).
-   **Security Group:** Hoạt động như một tường lửa ảo cho các máy chủ EC2 để kiểm soát traffic vào và ra.

---

### 7. Dịch vụ Database cốt lõi: RDS

**RDS (Relational Database Service)** giúp bạn dễ dàng thiết lập, vận hành và mở rộng một cơ sở dữ liệu quan hệ trên đám mây.
-   Hỗ trợ các hệ quản trị CSDL phổ biến như MySQL, PostgreSQL, MariaDB, Oracle, SQL Server.
-   AWS sẽ quản lý các tác vụ quản trị tốn thời gian như cài đặt, vá lỗi, sao lưu, và chuyển đổi dự phòng (failover), giúp bạn tập trung vào ứng dụng của mình.

## ✍️ Bài tập thực hành (Tour dạo quanh AWS Console)

Cách tốt nhất để làm quen với AWS là tự mình khám phá giao diện quản lý của nó. Bài thực hành này là một "tour" hướng dẫn bạn các bước an toàn để tương tác với các dịch vụ cốt lõi.

**Yêu cầu:**
-   Bạn cần có một tài khoản AWS. Nếu chưa có, hãy đăng ký một tài khoản.
-   **CẢNH BÁO QUAN TRỌNG:** Hầu hết các dịch vụ AWS đều tính phí. Tuy nhiên, AWS cung cấp một **Free Tier (Gói miễn phí)** cho tài khoản mới trong 12 tháng, cho phép bạn sử dụng một lượng tài nguyên nhất định mà không tốn tiền. Các bài tập dưới đây được thiết kế để nằm trong giới hạn của Free Tier, nhưng hãy **luôn cẩn thận** và **nhớ dọn dẹp (xóa) các tài nguyên sau khi thực hành xong** để tránh phát sinh chi phí không mong muốn.

**Bài 1: Làm quen với Console và IAM**
1.  Đăng nhập vào [AWS Management Console](https://aws.amazon.com/console/).
2.  Ở góc trên bên phải, bạn sẽ thấy tên một Region (ví dụ: `N. Virginia` hoặc `us-east-1`). Click vào đó để xem danh sách tất cả các Region mà AWS cung cấp.
3.  Trong thanh tìm kiếm ở giữa trang, gõ `IAM` và truy cập vào dịch vụ IAM.
4.  Khám phá các mục bên trái: `Users`, `Groups`, `Roles`. Xem các user và role có sẵn. Đừng tạo mới vội, chỉ xem để làm quen.

**Bài 2: Khám phá Mạng với VPC**
1.  Trong thanh tìm kiếm, gõ `VPC` và truy cập dịch vụ VPC.
2.  Từ menu trái, vào mục `Your VPCs`. Bạn sẽ thấy một VPC mặc định (Default VPC) đã được AWS tạo sẵn cho bạn trong Region hiện tại.
3.  Khám phá các thành phần liên quan của VPC mặc định này: `Subnets`, `Route Tables`, `Internet Gateways`.

**Bài 3: "Chạy thử" một máy chủ EC2**
1.  Tìm và truy cập dịch vụ `EC2`.
2.  Click vào nút `Launch instance`. Bạn sẽ được đưa đến một trình hướng dẫn gồm nhiều bước.
3.  **Bước 1 (Name and tags):** Đặt tên cho máy chủ, ví dụ `my-first-server`.
4.  **Bước 2 (Application and OS Images):** Đây là nơi chọn AMI. Hãy tìm một AMI có nhãn "Free tier eligible", ví dụ Amazon Linux 2.
5.  **Bước 3 (Instance type):** Chọn loại máy. Hãy đảm bảo bạn chọn loại có nhãn "Free tier eligible", ví dụ `t2.micro`.
6.  **Bước 4 (Key pair):** Đây là bước tạo cặp khóa để SSH vào máy chủ.
7.  **Bước 5 (Network settings):** Xem các cấu hình mạng. Mặc định nó sẽ được chạy trong Default VPC của bạn.
8.  **DỪNG LẠI Ở ĐÂY!** Chúng ta chỉ xem các bước để làm quen. **KHÔNG** click `Launch instance` để tránh phát sinh tài nguyên. Hãy click `Cancel` để thoát ra.

**Bài 4: Tạo và sử dụng S3 Bucket (An toàn và Miễn phí)**
1.  Tìm và truy cập dịch vụ `S3`.
2.  Click `Create bucket`.
3.  **Bucket name:** Đặt một cái tên **duy nhất trên toàn cầu** (ví dụ: `my-unique-devops-journey-bucket-` cộng với một chuỗi số ngẫu nhiên).
4.  **AWS Region:** Chọn Region gần bạn.
5.  Để các cài đặt còn lại là mặc định (đặc biệt là `Block all public access` vẫn được chọn để đảm bảo an toàn). Cuộn xuống và click `Create bucket`.
6.  Click vào tên bucket bạn vừa tạo.
7.  Click `Upload`, chọn một file bất kỳ trên máy tính của bạn và upload nó lên.
8.  Sau khi upload thành công, hãy chọn file đó và click `Delete`. Gõ `permanently delete` để xác nhận và xóa file.
9.  Cuối cùng, quay ra danh sách các bucket, chọn bucket bạn đã tạo và click `Delete`. Gõ tên bucket để xác nhận và xóa nó đi. **Đây là bước dọn dẹp quan trọng.**

---

Trong bài học cuối cùng, chúng ta sẽ kết hợp tất cả các kiến thức đã học để thực hiện một dự án hoàn chỉnh.

[Bài trước: Quản lý Log tập trung với EFK Stack](../13-efk-stack-logging/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Dự án Tốt nghiệp](../../Lesson07-final-project-and-career/15-final-project/)