# Bài 13: Quản lý Log tập trung với EFK Stack

## 🎯 Mục tiêu bài học

-   Hiểu được sự khác biệt giữa Metrics và Logs, và tại sao cần cả hai.
-   Nắm được vai trò của từng thành phần trong EFK Stack: Elasticsearch, Fluentd, và Kibana.
-   Hiểu được luồng di chuyển của một dòng log: từ ứng dụng -> Fluentd -> Elasticsearch -> Kibana.
-   Thực hành cấu hình Fluentd để thu thập log từ một ứng dụng container và đẩy về Elasticsearch.
-   Sử dụng Kibana để tìm kiếm, lọc và trực quan hóa dữ liệu log.

## 📖 Nội dung chính

1.  **Logging là gì?** Metrics cho bạn biết "cái gì" đang xảy ra, Logs cho bạn biết "tại sao".
2.  **Vấn đề của logging truyền thống:** `ssh` vào từng máy để xem log.
3.  **Giới thiệu EFK Stack:**
    -   **Elasticsearch:** "Trái tim" của stack, một công cụ tìm kiếm và phân tích mạnh mẽ.
    -   **Fluentd:** Công cụ thu thập, xử lý và chuyển tiếp log.
    -   **Kibana:** Giao diện web để khám phá và trực quan hóa log.
4.  **Luồng hoạt động của EFK.**
5.  **Thực hành:**
    -   Chạy EFK stack bằng Docker Compose.
    -   Cấu hình một ứng dụng để ghi log ra `stdout`.
    -   Cấu hình Fluentd để bắt log từ Docker driver.
    -   Sử dụng Kibana Discover để xem và tìm kiếm log.

## 🛠️ Công cụ & Lý thuyết

-   **Hệ thống Log:** <u>EFK Stack</u>, ELK Stack (Logstash), Grafana Loki, Splunk.
-   **Thành phần:** <u>Elasticsearch</u> (lưu trữ), <u>Fluentd</u> (thu thập), <u>Kibana</u> (trực quan hóa).
-   **Lý thuyết:** Centralized Logging, Log Aggregation, Structured Logging.

---

# Nội dung chi tiết - Bài 13: Quản lý Log tập trung với EFK Stack

Ở bài trước, chúng ta đã học cách dùng Prometheus để thu thập metrics. Metrics cho chúng ta biết "cái gì" đang xảy ra với hệ thống (ví dụ: CPU đang ở mức 90%). Nhưng để biết "tại sao" CPU lại cao như vậy, chúng ta cần xem xét logs. Logs là các bản ghi sự kiện được tạo ra bởi ứng dụng hoặc hệ thống, chứa thông tin chi tiết về các hoạt động đã diễn ra.

---

### 1. Logging là gì? Metrics vs. Logs

| Tiêu chí   | Metrics (Số liệu)                                     | Logs (Nhật ký)                                           |
|-----------|-------------------------------------------------------|----------------------------------------------------------|
| **Bản chất** | Dữ liệu dạng số, có thể tổng hợp được (aggregatable). | Dữ liệu dạng văn bản, không cấu trúc hoặc có cấu trúc.     |
| **Mục đích**  | Đo lường tình trạng tổng quan của hệ thống.          | Cung cấp thông tin chi tiết về một sự kiện cụ thể.      |
| **Ví dụ**   | `cpu_usage = 90%`, `http_requests_total = 1M`         | `[ERROR] User 'elsa' failed to login: invalid password`  |
| **Câu hỏi** | "Cái gì?", "Bao nhiêu?"                               | "Tại sao?", "Ai?", "Khi nào?"                             |

Một hệ thống quan sát (observability) hoàn chỉnh cần cả hai: dùng metrics để cảnh báo và phát hiện vấn đề, sau đó dùng logs để điều tra và tìm ra nguyên nhân gốc rễ.

---

### 2. Vấn đề của logging truyền thống

Khi chỉ có một vài máy chủ, việc `ssh` vào từng máy và dùng các lệnh như `tail -f app.log` hoặc `grep "ERROR" app.log` có vẻ khả thi. Nhưng khi hệ thống của bạn có hàng chục, hàng trăm microservices chạy trên các container liên tục được tạo ra và xóa đi, cách làm này trở nên bất khả thi.

**Quản lý log tập trung** ra đời để giải quyết vấn đề này. Ý tưởng là thu thập tất cả logs từ mọi nguồn (ứng dụng, máy chủ, database...) và đưa chúng về một nơi duy nhất để lưu trữ, tìm kiếm và phân tích.

---

### 3. Giới thiệu EFK Stack

EFK là một bộ ba công cụ mã nguồn mở rất phổ biến để xây dựng hệ thống log tập trung.
*(Lưu ý: Một biến thể phổ biến khác là ELK Stack, sử dụng Logstash thay cho Fluentd. Cả hai đều có chức năng tương tự.)*

-   **E - Elasticsearch:**
    -   Là "trái tim" và "bộ não" của stack.
    -   Về bản chất, nó là một công cụ tìm kiếm và phân tích dữ liệu phân tán, được xây dựng dựa trên Apache Lucene.
    -   Nó lưu trữ dữ liệu log (thường ở định dạng JSON) và cho phép bạn thực hiện các truy vấn tìm kiếm phức tạp với tốc độ cực nhanh.

-   **F - Fluentd:**
    -   Là một **công cụ thu thập và chuyển tiếp log (log collector/forwarder)**.
    -   Nó được cài đặt trên các máy chủ ứng dụng hoặc chạy như một agent, có nhiệm vụ thu thập log từ nhiều nguồn khác nhau (file, `stdout` của container, syslog,...).
    -   Điểm mạnh của Fluentd là khả năng xử lý log trước khi chuyển tiếp: nó có thể lọc, thêm bớt trường thông tin, và chuyển đổi log từ dạng không cấu trúc sang dạng có cấu trúc (structured logging).
    -   Sau khi xử lý, Fluentd sẽ đẩy log đến các đích khác nhau, trong trường hợp này là Elasticsearch.

-   **K - Kibana:**
    -   Là giao diện web để tương tác với dữ liệu trong Elasticsearch.
    -   Cho phép bạn **khám phá, tìm kiếm, và lọc** dữ liệu log một cách trực quan.
    -   Cung cấp các công cụ để **trực quan hóa** dữ liệu và tạo ra các dashboard (tương tự Grafana, nhưng chuyên cho việc phân tích log).

---

### 4. Luồng hoạt động của EFK

1.  Ứng dụng của bạn ghi log (ví dụ: ghi ra `stdout`).
2.  Docker Engine bắt lấy log từ `stdout` của container.
3.  **Fluentd** (được cấu hình làm logging driver cho Docker hoặc chạy như một container riêng) thu thập log từ Docker.
4.  Fluentd xử lý log (ví dụ: thêm thông tin về tên container, image_id) và chuyển đổi nó thành định dạng JSON.
5.  Fluentd đẩy log đã được xử lý vào **Elasticsearch**.
6.  Elasticsearch lập chỉ mục (index) log để tối ưu cho việc tìm kiếm.
7.  Người dùng truy cập **Kibana**, gửi truy vấn đến Elasticsearch.
8.  Elasticsearch trả về kết quả và Kibana hiển thị chúng cho người dùng.

---

### 5. Thực hành với Docker Compose

Cách dễ nhất để trải nghiệm EFK là chạy chúng bằng Docker Compose.

**1. Tạo file `docker-compose.yml`:**
(Đây là một ví dụ đơn giản, cấu hình thực tế có thể phức tạp hơn)
```yaml
version: '3' 
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node

  kibana:
    image: docker.elastic.co/kibana/kibana:7.15.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  fluentd:
    image: fluent/fluentd:v1.14-1
    volumes:
      - ./fluentd/conf:/fluentd/etc
    ports:
      - "24224:24224"
    depends_on:
      - elasticsearch

  my-app: # Một ứng dụng ví dụ ghi log ra stdout
    image: alpine
    command: >
      sh -c "while true; do echo \`date\` Hello from my-app; sleep 5; done"
    logging:
      driver: "fluentd" # Gửi log của container này đến fluentd
      options:
        fluentd-address: localhost:24224
        tag: docker.my-app
```
**2. Tạo file cấu hình cho Fluentd (`fluentd/conf/fluent.conf`):**
```conf
<source>
  @type forward
  port 24224
</source>

<match docker.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  logstash_prefix docker_logs
</match>
```
**3. Chạy stack:** `docker-compose up`

**4. Khám phá:**
-   Truy cập Kibana tại `http://localhost:5601`.
-   Vào mục "Stack Management" -> "Index Patterns" và tạo một index pattern tên là `docker_logs-*`.
-   Vào mục "Discover", bạn sẽ thấy các dòng log từ `my-app` được hiển thị. Hãy thử tìm kiếm và lọc chúng!

## ✍️ Bài tập thực hành (Exercises)

Phần thực hành này sẽ hướng dẫn bạn dựng một hệ thống logging EFK hoàn chỉnh tại local để thu thập log từ một container khác.

**Yêu cầu:**
-   Đã cài đặt Docker và Docker Compose.
-   Phân bổ đủ tài nguyên cho Docker (ít nhất 4GB RAM) vì Elasticsearch khá tốn bộ nhớ.

**Bài 1: Chuẩn bị Cấu hình cho EFK Stack**
1.  Tạo một thư mục chính cho dự án, ví dụ `efk-practice`.
2.  Bên trong `efk-practice`, tạo một thư mục con tên là `fluentd`, và bên trong `fluentd` lại tạo một thư mục con `conf`. Cấu trúc sẽ là: `efk-practice/fluentd/conf/`.
3.  Trong thư mục `efk-practice/fluentd/conf/`, tạo file `fluent.conf` với nội dung sau. File này cấu hình Fluentd lắng nghe log và chuyển tiếp đến Elasticsearch.
    ```conf
    # Lắng nghe log được forward đến port 24224
    <source>
      @type forward
      port 24224
      bind 0.0.0.0
    </source>

    # Bất kỳ log nào có tag khớp với 'docker.**' sẽ được xử lý bởi khối này
    <match docker.**>
      @type copy
      <store>
        @type elasticsearch
        host elasticsearch # Tên service của elasticsearch trong docker-compose
        port 9200
        logstash_format true
        logstash_prefix docker_logs # Tên index sẽ có dạng docker_logs-YYYY.MM.DD
        logstash_dateformat %Y%m%d
        include_tag_key true
        type_name _doc
        tag_key @log_name
        flush_interval 1s # Gửi log đến elasticsearch mỗi 1 giây
      </store>
      # In log ra stdout của container fluentd để tiện debug
      <store>
        @type stdout
      </store>
    </match>
    ```
4.  Trong thư mục gốc `efk-practice`, tạo file `docker-compose.yml` với nội dung như trong phần hướng dẫn số 5.

**Bài 2: Khởi chạy Stack và Kiểm tra**
1.  Mở terminal trong thư mục `efk-practice`.
2.  Chạy lệnh `docker-compose up -d`. Chờ vài phút để tất cả các container khởi động. Elasticsearch có thể mất nhiều thời gian nhất.
3.  Dùng lệnh `docker-compose ps` để xem trạng thái các container. Đảm bảo tất cả đều `Up`.
4.  Kiểm tra log của ứng dụng `my-app` để thấy nó đang ghi log: `docker-compose logs my-app`.
5.  Kiểm tra log của `fluentd` để xem nó có nhận được log không: `docker-compose logs fluentd`. Bạn sẽ thấy các dòng log JSON được in ra.

**Bài 3: Khám phá Logs trên Kibana**
1.  Truy cập Kibana tại `http://localhost:5601`.
2.  Từ menu bên trái (biểu tượng hamburger ☰), đi đến `Management > Stack Management`.
3.  Trong mục `Kibana`, click vào `Index Patterns`.
4.  Click `Create index pattern`.
5.  Trong ô `Index pattern name`, gõ `docker_logs*` và click `Next step`.
6.  Ở bước tiếp theo, chọn `@timestamp` từ dropdown `Time field` và click `Create index pattern`.
7.  Click vào menu hamburger ☰ một lần nữa và chọn `Discover`.
8.  **Kết quả:** Bạn sẽ thấy một biểu đồ và danh sách các dòng log từ container `my-app` đang liên tục đổ về.

**Bài 4: Tìm kiếm và Lọc**
1.  Trong thanh tìm kiếm của `Discover` (có chữ "KQL"), gõ `Hello` và nhấn Enter. Kibana sẽ chỉ hiển thị các dòng log chứa từ "Hello".
2.  Click vào một dòng log bất kỳ để mở rộng. Xem các trường thông tin (fields) đã được Fluentd thêm vào, ví dụ như `container_id` và `container_name`.
3.  Thử lọc theo một trường, ví dụ click vào trường `container_name`, nhấn vào dấu `+` để chỉ hiển thị log từ container đó.

Để dừng và xóa toàn bộ stack, quay lại terminal và chạy `docker-compose down`.

---

Trong bài học tiếp theo, chúng ta sẽ bắt đầu làm quen với nền tảng đám mây, nơi mà hầu hết các hệ thống DevOps hiện đại được xây dựng và vận hành.

[Bài trước: Giám sát hệ thống với Prometheus & Grafana](../12-prometheus-and-grafana/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Nhập môn AWS](../../Lesson06-cloud-platforms/14-aws-core-services/)