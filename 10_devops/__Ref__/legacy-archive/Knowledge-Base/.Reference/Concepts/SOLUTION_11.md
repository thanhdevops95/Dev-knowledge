# Lời giải và Hướng dẫn - Bài 12: Prometheus & Grafana

Chào mừng bạn đến với bài thực hành về giám sát. Tôi đã chuẩn bị sẵn các file cấu hình để bạn có thể khởi chạy một hệ thống giám sát đầy đủ bao gồm Prometheus, Grafana, và Node Exporter chỉ bằng một lệnh duy nhất.

**Yêu cầu:** Máy tính của bạn phải được cài đặt Docker và Docker Compose.

Hãy mở terminal, di chuyển vào thư mục của bài tập này (`workspare/.../12-prometheus-and-grafana`) và làm theo các bước dưới đây.

---

### Bài 1: Chuẩn bị môi trường (Đã hoàn thành)

Tôi đã tạo sẵn 2 file cấu hình quan trọng trong thư mục này. Hãy cùng phân tích chúng.

**1. File `prometheus.yml`:**
File này ra lệnh cho Prometheus biết nó cần "cào" (scrape) dữ liệu từ đâu.
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node_exporter:9100']
```
-   `job_name: 'prometheus'`: Prometheus sẽ tự giám sát chính nó.
-   `job_name: 'node_exporter'`: Prometheus sẽ giám sát `node_exporter`. Ở đây, `node_exporter:9100` là địa chỉ mà Prometheus sẽ kết nối đến. Docker Compose sẽ đảm bảo rằng hostname `node_exporter` được phân giải thành địa chỉ IP nội bộ của container Node Exporter.

**2. File `docker-compose.yml`:**
File này giống như một "bản thiết kế" cho toàn bộ ứng dụng đa container của chúng ta.
```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  node_exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    depends_on:
      - prometheus
```
-   Nó định nghĩa 3 "dịch vụ": `prometheus`, `node_exporter`, và `grafana`.
-   `volumes`: Phần quan trọng nhất ở đây là `volumes` của service `prometheus`. Nó ánh xạ file `prometheus.yml` từ máy của bạn vào đường dẫn cấu hình bên trong container, cho phép Prometheus đọc được chỉ dẫn của chúng ta.
-   `ports`: Ánh xạ các cổng từ container ra máy thật của bạn để chúng ta có thể truy cập qua trình duyệt.
-   `depends_on`: Đảm bảo rằng Grafana chỉ khởi động sau khi Prometheus đã sẵn sàng.

---

### Bài 2: Khởi chạy và Kiểm tra Stack

**1. Khởi chạy Stack:**
Chạy lệnh duy nhất sau. Docker Compose sẽ đọc file `docker-compose.yml` và tự động tải về các image, tạo và khởi chạy 3 container.
```bash
docker-compose up -d
```
-   `-d`: Chạy ở chế độ nền (detached).

**2. Kiểm tra Prometheus:**
-   Mở trình duyệt và truy cập `http://localhost:9090`.
-   Click vào menu **Status** ở trên cùng, chọn **Targets**.
-   **Kết quả mong đợi:** Bạn phải thấy cả hai `job` là `node_exporter` và `prometheus` đều có trạng thái **UP** màu xanh lá. Điều này xác nhận Prometheus đã kết nối và thu thập dữ liệu thành công.

**3. Kiểm tra Node Exporter:**
-   Mở một tab mới và truy cập `http://localhost:9100/metrics`.
-   **Kết quả mong đợi:** Bạn sẽ thấy một trang văn bản trắng với rất nhiều dòng chữ. Đây chính là "kho báu" metrics (CPU, RAM, network,...) mà Node Exporter đang cung cấp cho Prometheus.

---

### Bài 3: Cấu hình Grafana và Trực quan hóa

**1. Đăng nhập Grafana:**
-   Mở một tab mới và truy cập `http://localhost:3000`.
-   Đăng nhập với username: `admin` và password: `admin`.
-   Grafana sẽ yêu cầu bạn tạo một mật khẩu mới.

**2. Thêm Prometheus làm Nguồn dữ liệu (Data Source):**
-   Sau khi đăng nhập, ở menu bên trái, click vào biểu tượng bánh răng (⚙️ **Configuration**).
-   Chọn **Data Sources**.
-   Click vào nút **Add data source**.
-   Chọn **Prometheus** từ danh sách.
-   Trong phần **HTTP**, ở ô **URL**, nhập chính xác: `http://prometheus:9090`
    -   *Giải thích: Vì Grafana và Prometheus cùng nằm trong một mạng Docker do Compose tạo ra, chúng có thể "nói chuyện" với nhau qua tên service.*
-   Cuộn xuống cuối trang và click **Save & test**. Bạn sẽ thấy một thông báo màu xanh "Data source is working".

**3. Import Dashboard có sẵn:**
Cách nhanh nhất để có một dashboard giám sát hệ thống đẹp mắt là sử dụng lại dashboard do cộng đồng tạo sẵn.
-   Ở menu bên trái, click vào biểu tượng dấu cộng (➕ **Create**).
-   Chọn **Import**.
-   Trong ô "Import via grafana.com", nhập ID `1860` và click **Load**. (Đây là ID của dashboard "Node Exporter Full" rất phổ biến).
-   Ở màn hình tiếp theo, kéo xuống dưới cùng, ở phần "Prometheus", hãy chắc chắn rằng bạn đã chọn data source là `Prometheus` mà bạn vừa tạo ở bước trên.
-   Click **Import**.

**4. Chiêm ngưỡng kết quả:**
Ngay lập tức, bạn sẽ được chuyển đến một dashboard chuyên nghiệp, đầy đủ các biểu đồ về CPU, RAM, Disk I/O, Network Traffic,... của chính máy tính bạn. Dữ liệu này được `node_exporter` thu thập, `prometheus` lưu trữ, và `grafana` vẽ lên.

---

### Dọn dẹp

Khi đã thực hành xong, quay lại terminal và chạy lệnh sau để dừng và xóa toàn bộ stack:
```bash
docker-compose down
```

Chúc mừng bạn đã tự tay khởi chạy thành công một hệ thống giám sát hoàn chỉnh!