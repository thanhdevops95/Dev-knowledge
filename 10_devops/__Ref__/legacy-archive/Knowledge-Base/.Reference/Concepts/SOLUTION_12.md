# Lời giải và Hướng dẫn - Bài 13: EFK Stack

Chào mừng bạn đến với bài thực hành về ghi log tập trung. Tôi đã chuẩn bị các file cấu hình để bạn có thể khởi chạy một hệ thống EFK (Elasticsearch, Fluentd, Kibana) hoàn chỉnh bằng Docker Compose.

**Yêu cầu:**
-   Máy tính của bạn đã được cài đặt Docker và Docker Compose.
-   **Quan trọng:** Elasticsearch khá tốn tài nguyên. Hãy đảm bảo bạn đã cấp phát đủ bộ nhớ cho Docker (khuyến nghị ít nhất 4GB RAM) trong phần cài đặt của Docker Desktop.

Hãy mở terminal, di chuyển vào thư mục của bài tập này (`workspare/.../13-efk-stack-logging`) và làm theo các bước dưới đây.

---

### Bài 1: Chuẩn bị Cấu hình (Đã hoàn thành)

Tôi đã tạo sẵn cấu trúc thư mục và 2 file cấu hình quan trọng.

**1. File `fluentd/conf/fluent.conf`:**
Đây là file "luật chơi" cho Fluentd.
```conf
<source>
  @type forward
  port 24224
  bind 0.0.0.0
</source>
<match docker.**>
  @type copy
  <store>
    @type elasticsearch
    # ... cấu hình đẩy đến Elasticsearch
  </store>
  <store>
    @type stdout 
  </store>
</match>
```
-   **`<source>`**: Lắng nghe log được gửi đến cổng 24224.
-   **`<match docker.**>`**: Bất kỳ log nào có tag bắt đầu bằng `docker.` sẽ được xử lý.
-   **`@type copy`**: Gửi log đến nhiều đích cùng lúc.
-   **`<store> @type elasticsearch`**: Đích thứ nhất là Elasticsearch.
-   **`<store> @type stdout`**: Đích thứ hai là in ra màn hình console của chính Fluentd, rất hữu ích cho việc debug.

**2. File `docker-compose.yml`:**
File này định nghĩa 4 services sẽ chạy.
-   `elasticsearch`: Nơi lưu trữ log.
-   `kibana`: Giao diện web để xem log.
-   `fluentd`: Nhận log và chuyển tiếp cho `elasticsearch`.
-   `my-app`: Một container đơn giản chỉ để tạo ra log, được cấu hình để gửi tất cả log của nó đến `fluentd` thông qua `logging driver`.

---

### Bài 2: Khởi chạy Stack và Kiểm tra

**1. Khởi chạy Stack:**
Chạy lệnh sau. Docker Compose sẽ đọc file `docker-compose.yml` và khởi chạy 4 container. **Lưu ý:** Lần đầu khởi động, Elasticsearch có thể mất vài phút để sẵn sàng.
```bash
docker-compose up -d
```

**2. Kiểm tra trạng thái:**
Sau khoảng 1-2 phút, chạy lệnh sau để đảm bảo cả 4 container đều đang ở trạng thái `Up`.
```bash
docker-compose ps
```

**3. Kiểm tra luồng log:**
-   Xem log của ứng dụng mẫu để thấy nó đang hoạt động:
    ```bash
    docker-compose logs my-app
    ```
    *Kết quả mong đợi: Bạn sẽ thấy các dòng `INFO: Hello from my-app...` được in ra mỗi 5 giây.*

-   Xem log của Fluentd để xác nhận nó đang nhận được log:
    ```bash
    docker-compose logs fluentd
    ```
    *Kết quả mong đợi: Bạn sẽ thấy các dòng log ở định dạng JSON được in ra. Đây là các log mà Fluentd nhận được từ `my-app` và chuẩn bị gửi đi.*

---

### Bài 3 & 4: Khám phá và Tìm kiếm Logs trên Kibana

**1. Truy cập Kibana:**
Mở trình duyệt và truy cập `http://localhost:5601`. Chờ một lúc để Kibana khởi động hoàn tất.

**2. Tạo Index Pattern:**
Lần đầu tiên sử dụng, bạn cần cho Kibana biết nó nên tìm log ở đâu trong Elasticsearch.
-   Click vào biểu tượng menu hamburger (☰) ở góc trên bên trái, đi đến **Management > Stack Management**.
-   Trong mục **Kibana**, click vào **Index Patterns**.
-   Click vào nút **Create index pattern**.
-   Trong ô **Index pattern name**, gõ chính xác `docker_logs*`. Tên này khớp với `logstash_prefix` chúng ta đã định nghĩa trong file `fluent.conf`. Bạn sẽ thấy thông báo "Success! Your index pattern matches 1 index."
-   Click **Next step**.
-   Ở bước tiếp theo, trong dropdown **Time field**, chọn `@timestamp`.
-   Click **Create index pattern**.

**3. Khám phá Logs (Discover):**
-   Click vào biểu tượng menu hamburger (☰) một lần nữa và chọn **Discover**.
-   **Kết quả:** Một thế giới mới mở ra! Bạn sẽ thấy một biểu đồ cột hiển thị số lượng log theo thời gian và ở dưới là danh sách các dòng log từ `my-app` liên tục được cập nhật. Mỗi dòng log là một văn bản có cấu trúc (JSON) mà bạn có thể mở rộng để xem chi tiết.

**4. Tìm kiếm và Lọc:**
-   Trong thanh tìm kiếm **KQL** ở trên cùng, gõ `INFO` và nhấn Enter. Kibana sẽ lọc và chỉ hiển thị các dòng log chứa từ khóa đó.
-   Click vào một dòng log bất kỳ để mở rộng. Bạn sẽ thấy các trường thông tin rất hữu ích đã được Fluentd tự động thêm vào như `container_id` và `container_name`.
-   Trỏ chuột vào trường `container_name`, bạn sẽ thấy một icon `+` và `-`. Click vào dấu `+` để thêm một bộ lọc, chỉ hiển thị log từ container `my-app`.

---

### Dọn dẹp

Khi đã thực hành xong, quay lại terminal và chạy lệnh sau để dừng và xóa toàn bộ stack (containers, networks).
```bash
docker-compose down
```
Nếu bạn muốn xóa cả dữ liệu của Elasticsearch (được lưu trong volume), dùng thêm cờ `-v`:
```bash
docker-compose down -v
```

Chúc mừng bạn đã hoàn thành việc xây dựng một hệ thống logging tập trung mạnh mẽ!