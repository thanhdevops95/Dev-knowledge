# Hướng dẫn và Giải thích - Bài 14: Tour dạo quanh AWS Console

Chào mừng bạn đến với chuyến tham quan các dịch vụ cốt lõi của AWS. File này sẽ là người bạn đồng hành, giải thích những gì bạn đang thấy và tại sao chúng lại quan trọng.

**⚠️ Cảnh báo:** Hãy luôn nhớ bạn đang sử dụng một tài khoản AWS thật. Luôn tuân thủ các hướng dẫn, đặc biệt là việc **dọn dẹp tài nguyên** ở cuối bài để tránh phát sinh chi phí không mong muốn.

---

### Bài 1: Làm quen với Console và IAM

**Mục tiêu:** Hiểu được giao diện tổng quan và cách AWS quản lý quyền truy cập.

**Các bước:** Làm theo hướng dẫn trong `README.md`.

**Những điều cần quan sát và ý nghĩa:**

1.  **AWS Region:** Khi bạn thấy danh sách các Region (`us-east-1`, `ap-southeast-1`,...), hãy nhận ra rằng hạ tầng của bạn có vị trí địa lý thực tế. Việc chọn Region gần người dùng giúp giảm độ trễ. Các tài nguyên bạn tạo (như EC2) thường chỉ tồn tại trong Region bạn đã chọn.

2.  **Dịch vụ IAM (Identity and Access Management):**
    -   **Tại sao nó quan trọng?** Đây là trung tâm an ninh của tài khoản AWS. Mọi quyền truy cập đều được quản lý tại đây.
    -   **Khi bạn xem `Users`:** Nếu là tài khoản mới, bạn sẽ không thấy user nào ngoài `root user` (là tài khoản bạn dùng để đăng nhập). Trong thực tế, **không bao giờ** dùng `root user` cho công việc hàng ngày. Nguyên tắc là tạo các IAM user riêng với quyền hạn giới hạn.
    -   **Khi bạn xem `Roles`:** Bạn có thể thấy một vài role có sẵn với tên như `AWSServiceRoleFor...`. Đây là các role được AWS tự tạo ra để các dịch vụ của AWS có thể "nói chuyện" và tác động lẫn nhau một cách an toàn (ví dụ: cho phép EC2 truy cập S3). Điều này thể hiện cơ chế cấp quyền tạm thời, an toàn hơn so với việc lưu trữ key truy cập cứng.

---

### Bài 2: Khám phá Mạng với VPC

**Mục tiêu:** Hiểu rằng các tài nguyên của bạn chạy trong một mạng ảo cô lập mà bạn có thể kiểm soát.

**Các bước:** Làm theo hướng dẫn trong `README.md`.

**Những điều cần quan sát và ý nghĩa:**

1.  **Default VPC (VPC Mặc định):** AWS tạo sẵn cho bạn một VPC ở mỗi Region để bạn có thể bắt đầu một cách nhanh chóng mà không cần phải là chuyên gia về mạng.
2.  **Subnets (Mạng con):** Bạn sẽ thấy VPC mặc định có nhiều Subnet, mỗi Subnet nằm trong một Availability Zone (AZ) khác nhau. Đây chính là cách AWS cho phép bạn xây dựng ứng dụng có tính sẵn sàng cao (High Availability). Bằng cách đặt các máy chủ ở các Subnet thuộc các AZ khác nhau, nếu một AZ gặp sự cố, ứng dụng của bạn vẫn sống.
3.  **Route Tables (Bảng định tuyến):** Mỗi Subnet được liên kết với một Route Table. Nó hoạt động như một biển chỉ dẫn giao thông, quy định traffic từ Subnet đó có thể đi đến đâu (ví dụ: đi ra Internet, đi đến Subnet khác...).
4.  **Internet Gateway (Cổng Internet):** Đây là thành phần cho phép traffic từ VPC của bạn đi ra Internet và ngược lại. Một Route Table trỏ đến Internet Gateway sẽ làm cho Subnet đó trở thành "public subnet".

---

### Bài 3: "Chạy thử" một máy chủ EC2

**Mục tiêu:** Làm quen với các lựa chọn khi tạo một máy chủ ảo, "xương sống" của nhiều ứng dụng.

**Các bước:** Làm theo hướng dẫn trong `README.md`, và **nhớ click `Cancel` ở cuối**.

**Những điều cần quan sát và ý nghĩa:**

1.  **AMI (Amazon Machine Image):** Đây là template cho máy chủ của bạn. Nó chứa hệ điều hành (Amazon Linux, Ubuntu, Windows,...) và các phần mềm được cài sẵn. Việc chọn đúng AMI là bước đầu tiên để xây dựng môi trường.
2.  **Instance Type:** `t2.micro` là một máy chủ rất nhỏ, phù hợp cho việc học và thử nghiệm (và nằm trong Free Tier). Trong thực tế, bạn sẽ thấy hàng trăm loại instance type khác nhau, được tối ưu cho các mục đích khác nhau: tính toán cao (C-series), nhiều RAM (R-series), có GPU (G-series),...
3.  **Key pair (Cặp khóa):** Đây là cơ chế bảo mật để bạn có thể đăng nhập vào máy chủ Linux của mình qua SSH. Bạn sẽ tải về một file `.pem` (private key), và AWS sẽ giữ lại public key trên máy chủ EC2. Bạn **không thể** tải lại private key sau này, nên phải giữ nó cẩn thận.
4.  **Network settings:** Ở đây bạn sẽ thấy EC2 được đặt trong VPC mặc định và một Subnet nào đó. Bạn cũng có thể thấy mục `Security Group`. Security Group hoạt động như một firewall cho từng máy chủ, quy định cổng nào (ví dụ cổng 22 cho SSH, cổng 80 cho HTTP) được phép truy cập từ những địa chỉ IP nào.

**HÃY NHỚ CLICK `CANCEL` ĐỂ KHÔNG TẠO MÁY CHỦ.**

---

### Bài 4: Tạo và sử dụng S3 Bucket

**Mục tiêu:** Trải nghiệm dịch vụ lưu trữ đối tượng, một dịch vụ cực kỳ linh hoạt và phổ biến của AWS.

**Các bước:** Làm theo hướng dẫn trong `README.md` để tạo bucket, upload file, xóa file, và **xóa bucket**.

**Những điều cần quan sát và ý nghĩa:**

1.  **Tên Bucket Duy nhất Toàn cầu:** Khi bạn tạo bucket, AWS yêu cầu tên phải là duy nhất trên toàn bộ hệ thống S3 toàn cầu. Điều này là vì tên bucket có thể được dùng như một phần của địa chỉ web (`http://<bucket-name>.s3.amazonaws.com/...`).
2.  **`Block all public access`**: Mặc định, tùy chọn này luôn được bật. Đây là một biện pháp an ninh quan trọng mà AWS đã thêm vào để ngăn chặn việc vô tình làm lộ dữ liệu nhạy cảm ra ngoài Internet.
3.  **Upload/Delete file:** Quá trình này rất đơn giản. Hãy tưởng tượng S3 như một "Google Drive/Dropbox vô hạn". Bạn có thể lưu trữ mọi thứ từ file log, ảnh người dùng, cho đến các bản backup database.
4.  **Dọn dẹp:** Việc hướng dẫn bạn xóa file và sau đó xóa bucket là để tập cho bạn một thói quen quan trọng nhất khi làm việc với cloud: **Luôn dọn dẹp những gì bạn không còn dùng đến.** Đây là cách tốt nhất để kiểm soát chi phí.

Chúc mừng bạn đã hoàn thành chuyến tham quan đầu tiên. Giờ bạn đã có một cái nhìn tổng quan về cách các dịch vụ AWS cốt lõi hoạt động và tương tác với nhau.