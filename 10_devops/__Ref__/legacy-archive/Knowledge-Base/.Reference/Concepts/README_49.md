# Bài 12: Giám sát hệ thống với Prometheus & Grafana

## 🎯 Mục tiêu bài học

-   Hiểu được tầm quan trọng của việc giám sát (monitoring) trong DevOps.
-   Nắm được kiến trúc và mô hình hoạt động của Prometheus (pull-based).
-   Viết được cấu hình cơ bản để Prometheus thu thập (scrape) số liệu (metrics) từ một ứng dụng.
-   Sử dụng ngôn ngữ truy vấn PromQL để truy vấn và phân tích metrics.
-   Xây dựng được một Dashboard trên Grafana để trực quan hóa các metrics từ Prometheus.

## 📖 Nội dung chính

1.  **Tại sao phải giám sát?** "Bạn không thể cải thiện thứ bạn không thể đo lường."
2.  **Giới thiệu Prometheus:** Một hệ thống giám sát và cảnh báo mã nguồn mở.
3.  **Kiến trúc Prometheus:** Server, Targets, Exporters, Alertmanager.
4.  **Metrics và Các kiểu dữ liệu:** Counter, Gauge, Histogram, Summary.
5.  **PromQL:** Ngôn ngữ truy vấn mạnh mẽ của Prometheus.
6.  **Giới thiệu Grafana:** Công cụ trực quan hóa dữ liệu hàng đầu.
7.  **Thực hành:**
    -   Cài đặt Prometheus và cấu hình để scrape chính nó.
    -   Cài đặt Grafana, kết nối đến Prometheus làm Data Source.
    -   Tạo một Dashboard đơn giản để hiển thị CPU/RAM usage của Prometheus.

## 🛠️ Công cụ & Lý thuyết

-   **Giám sát Metrics:** <u>Prometheus</u>, Datadog, InfluxDB, Zabbix.
-   **Trực quan hóa:** <u>Grafana</u>, Kibana, Datadog Dashboards.
-   **Công cụ:** `prometheus`, `grafana`, `node_exporter`, `alertmanager`.
-   **Lý thuyết:** Monitoring, Metrics, Time Series Data, Pull vs. Push model, Visualization.

---

# Nội dung chi tiết - Bài 12: Giám sát với Prometheus & Grafana

Việc triển khai được ứng dụng chỉ là một nửa câu chuyện. Làm thế nào bạn biết được ứng dụng đang hoạt động tốt? Người dùng có đang gặp lỗi không? Hệ thống có sắp hết tài nguyên không? Giám sát (Monitoring) là quá trình thu thập, phân tích và hiển thị dữ liệu về tình trạng hệ thống để trả lời những câu hỏi này.

---

### 1. Tại sao phải giám sát?

-   **Phát hiện sự cố sớm:** Nhận biết các vấn đề (CPU cao, bộ nhớ đầy, tỷ lệ lỗi tăng...) trước khi chúng ảnh hưởng nghiêm trọng đến người dùng.
-   **Gỡ lỗi và Phân tích nguyên nhân gốc rễ (Root Cause Analysis):** Khi có sự cố, dữ liệu lịch sử giúp bạn tìm ra nguyên nhân.
-   **Hoạch định dung lượng (Capacity Planning):** Dự đoán khi nào cần nâng cấp hoặc bổ sung tài nguyên dựa trên xu hướng tăng trưởng.
-   **Tối ưu hóa hiệu năng:** Xác định các điểm nghẽn cổ chai trong hệ thống.
-   **Đo lường mục tiêu kinh doanh:** Theo dõi các chỉ số quan trọng như số lượng người dùng đăng ký, số lượng giao dịch...

---

### 2. Giới thiệu Prometheus

Prometheus là một dự án mã nguồn mở của Cloud Native Computing Foundation (CNCF), đã trở thành tiêu chuẩn de facto cho việc giám sát các hệ thống hiện đại, đặc biệt là Kubernetes.

**Đặc điểm chính:**
-   **Mô hình Pull-based:** Prometheus chủ động "kéo" (pull) hoặc "cạo" (scrape) dữ liệu số liệu (metrics) từ các điểm cuối HTTP (HTTP endpoints) của ứng dụng hoặc máy chủ.
-   **Lưu trữ dạng Time Series:** Dữ liệu được lưu dưới dạng chuỗi thời gian, tức là một giá trị được gắn với một dấu thời gian (timestamp).
-   **Ngôn ngữ truy vấn mạnh mẽ (PromQL):** Cho phép bạn cắt, lọc, và tổng hợp dữ liệu time series một cách linh hoạt.
-   **Tích hợp với cơ chế cảnh báo (Alerting):** Có thể định nghĩa các quy tắc cảnh báo và đẩy chúng đến Alertmanager.

---

### 3. Kiến trúc Prometheus

-   **Prometheus Server:** Trung tâm của hệ thống, chịu trách nhiệm scrape và lưu trữ dữ liệu.
-   **Targets:** Là các dịch vụ mà Prometheus sẽ scrape metrics. Chúng phải cung cấp một endpoint HTTP (thường là `/metrics`) trả về dữ liệu theo định dạng của Prometheus.
-   **Exporters:** Nhiều ứng dụng (như database, message queue) không có sẵn endpoint `/metrics`. Exporter là một công cụ "phụ trợ" chạy bên cạnh ứng dụng đó, thu thập dữ liệu từ ứng dụng và "phơi" ra endpoint `/metrics` cho Prometheus. Ví dụ: `node_exporter` để lấy metrics của máy chủ (CPU, RAM, disk).
-   **Alertmanager:** Xử lý các cảnh báo được gửi từ Prometheus. Nó có thể nhóm, khử nhiễu, và gửi thông báo đến các kênh như Email, Slack, PagerDuty.

---

### 4. Metrics và Các kiểu dữ liệu

Prometheus định nghĩa 4 kiểu metrics chính:
-   **Counter:** Một giá trị chỉ có thể tăng, không bao giờ giảm (ví dụ: số lượng request đã phục vụ, số lượng lỗi đã xảy ra). Dùng để tính tốc độ thay đổi (rate).
-   **Gauge:** Một giá trị có thể tăng hoặc giảm (ví dụ: nhiệt độ CPU hiện tại, số lượng request đang xử lý).
-   **Histogram:** Thống kê và phân loại các quan sát (ví dụ: thời gian phản hồi request) vào các "thùng" (bucket) có thể cấu hình. Giúp trả lời câu hỏi như "Có bao nhiêu request có thời gian phản hồi dưới 100ms?".
-   **Summary:** Tương tự Histogram, nhưng nó tính toán các phân vị (quantile) có thể cấu hình (ví dụ: phân vị thứ 99 của thời gian phản hồi là 200ms).

---

### 5. PromQL (Prometheus Query Language)

Đây là tính năng mạnh mẽ nhất của Prometheus.

*Ví dụ một số truy vấn:*
-   `node_memory_MemAvailable_bytes`: Lấy giá trị hiện tại của bộ nhớ còn trống.
-   `rate(http_requests_total[5m])`: Tính tốc độ trung bình (số request mỗi giây) của các request HTTP trong 5 phút vừa qua.
-   `sum(rate(http_requests_total{job="my-app"}[5m])) by (status_code)`: Tính tổng tốc độ request cho ứng dụng "my-app", nhóm theo mã trạng thái HTTP (200, 404, 500...).

---

### 6. Giới thiệu Grafana

Trong khi Prometheus rất giỏi trong việc thu thập và lưu trữ dữ liệu, giao diện web của nó khá cơ bản. Grafana là một công cụ trực quan hóa mã nguồn mở cho phép bạn tạo ra các dashboard đẹp và linh hoạt từ nhiều nguồn dữ liệu khác nhau, trong đó có Prometheus.

Với Grafana, bạn có thể:
-   Tạo các biểu đồ đường, biểu đồ cột, đồng hồ đo...
-   Tổ chức các biểu đồ vào một dashboard.
-   Sử dụng các biến để tạo dashboard động (ví dụ: chọn xem metrics cho server A hoặc server B từ một dropdown).

---

### 7. Thực hành

1.  **Cài đặt `node_exporter`** trên một máy chủ để lấy metrics hệ thống.
2.  **Cài đặt Prometheus Server.**
3.  **Cấu hình file `prometheus.yml`** để Prometheus có thể tìm và scrape metrics từ `node_exporter`.
    ```yaml
    scrape_configs:
      - job_name: 'node'
        static_configs:
          - targets: ['<IP_cua_may_chu_chay_node_exporter>:9100']
    ```
4.  **Khởi động Prometheus** và truy cập vào giao diện web của nó. Thử một vài truy vấn PromQL.
5.  **Cài đặt Grafana.**
6.  **Trên Grafana UI:**
    -   Thêm Prometheus làm một Data Source mới.
    -   Tạo một Dashboard mới.
    -   Thêm một Panel (biểu đồ) và sử dụng PromQL để vẽ đồ thị CPU usage.
    -   Hoặc, import một dashboard có sẵn cho Node Exporter từ Grafana.com.

## ✍️ Bài tập thực hành (Exercises)

Cách tốt nhất để học Prometheus và Grafana là chạy chúng cùng nhau. Chúng ta sẽ sử dụng `docker-compose` để khởi chạy toàn bộ stack giám sát một cách nhanh chóng.

**Yêu cầu:**
-   Đã cài đặt Docker và Docker Compose.

**Bài 1: Chuẩn bị môi trường**
1.  Tạo một thư mục mới cho bài thực hành, ví dụ `monitoring-stack`.
2.  Bên trong thư mục đó, tạo file `prometheus.yml`. Đây là file cấu hình đểบอก Prometheus biết cần scrape metrics từ đâu.
    ```yaml
    global:
      scrape_interval: 15s # Tần suất scrape mặc định

    scrape_configs:
      # Scrape metrics của chính Prometheus
      - job_name: 'prometheus'
        static_configs:
          - targets: ['localhost:9090']

      # Scrape metrics của Node Exporter (sẽ chạy trong container)
      - job_name: 'node_exporter'
        static_configs:
          # Dùng tên service trong docker-compose làm hostname
          - targets: ['node_exporter:9100']
    ```
3.  Trong cùng thư mục, tạo file `docker-compose.yml`. File này định nghĩa 3 services: Prometheus, Grafana, và Node Exporter.
    ```yaml
    version: '3.8'
    services:
      prometheus:
        image: prom/prometheus:latest
        container_name: prometheus
        volumes:
          - ./prometheus.yml:/etc/prometheus/prometheus.yml
        ports:
          - "9090:9090"

      node_exporter:
        image: prom/node-exporter:latest
        container_name: node_exporter
        ports:
          - "9100:9100"

      grafana:
        image: grafana/grafana:latest
        container_name: grafana
        ports:
          - "3000:3000"
        depends_on:
          - prometheus
    ```

**Bài 2: Khởi chạy và Kiểm tra Stack**
1.  Mở terminal trong thư mục `monitoring-stack`.
2.  Chạy lệnh: `docker-compose up -d`. Docker sẽ tải về và khởi chạy 3 container.
3.  **Kiểm tra Prometheus:**
    -   Mở trình duyệt và truy cập `http://localhost:9090`.
    -   Đi đến menu `Status -> Targets`.
    -   Bạn sẽ thấy 2 target là `prometheus` và `node_exporter` đều ở trạng thái `UP` (màu xanh). Điều này xác nhận Prometheus đã scrape metrics thành công.
4.  **Kiểm tra Node Exporter:**
    -   Truy cập `http://localhost:9100/metrics`. Bạn sẽ thấy một trang đầy chữ, đó chính là các metrics về hệ thống (CPU, RAM, Disk...) mà Node Exporter đang "phơi" ra.

**Bài 3: Cấu hình Grafana và Trực quan hóa**
1.  **Truy cập Grafana:** Mở trình duyệt, đi đến `http://localhost:3000`.
2.  Đăng nhập với username `admin` và password `admin`. Grafana sẽ yêu cầu bạn đổi mật khẩu.
3.  **Thêm Data Source:**
    -   Click vào biểu tượng bánh răng (Configuration) ở menu bên trái, chọn `Data Sources`.
    -   Click `Add data source`, chọn `Prometheus`.
    -   Trong ô `HTTP URL`, nhập `http://prometheus:9090` (chúng ta dùng tên service `prometheus` vì Grafana và Prometheus đang chạy chung một mạng Docker).
    -   Cuộn xuống dưới và click `Save & test`. Bạn sẽ thấy thông báo "Data source is working".
4.  **Import Dashboard có sẵn:**
    -   Cách nhanh nhất để có một dashboard đẹp là import từ cộng đồng. Dashboard phổ biến nhất cho Node Exporter có ID là `1860`.
    -   Click vào biểu tượng dấu `+` (Create) ở menu trái, chọn `Import`.
    -   Trong ô "Import via grafana.com", nhập ID `1860` và click `Load`.
    -   Ở bước tiếp theo, ở dưới cùng, hãy chắc chắn rằng bạn đã chọn Data Source là `Prometheus` mà bạn vừa tạo.
    -   Click `Import`.
5.  **Chiêm ngưỡng kết quả:** Ngay lập tức, bạn sẽ có một dashboard đầy đủ thông tin về CPU, RAM, Disk, Network... của máy tính bạn, được thu thập bởi Node Exporter, lưu trữ bởi Prometheus, và vẽ lên bởi Grafana.

Để dừng toàn bộ stack, quay lại terminal và chạy `docker-compose down`.

---

Trong bài học tiếp theo, chúng ta sẽ tìm hiểu về phần còn lại của bộ ba "Observability": Logging (Ghi log).

[Bài trước: Terraform - Hạ tầng dưới dạng Mã](../11-terraform-iac/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Quản lý Log tập trung với EFK Stack](../13-efk-stack-logging/)