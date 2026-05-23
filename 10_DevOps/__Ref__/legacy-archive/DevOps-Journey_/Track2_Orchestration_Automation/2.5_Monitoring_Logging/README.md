# 📊 Module 2.5: Monitoring & Logging

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Observability** - Monitor and debug distributed systems.
>
> *Khả năng quan sát - Giám sát và debug hệ thống phân tán.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand observability pillars - metrics, logs, traces (Hiểu các trụ cột observability)
- ✅ Setup Prometheus & Grafana (Thiết lập Prometheus & Grafana)
- ✅ Create dashboards and alerts (Tạo dashboard và cảnh báo)
- ✅ Implement centralized logging with ELK/Loki (Triển khai logging tập trung)
- ✅ Collect application metrics (Thu thập metrics ứng dụng)
- ✅ Configure alerting and oncall (Cấu hình cảnh báo và trực)

---

## 📚 Content (Nội dung)

### 1. What is Observability? (Khả năng quan sát là gì?)

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> It's Friday 5 PM. Users start complaining: "The app is slow!" You check the server - CPU is 30%, RAM is 50%. Everything looks fine. But WHERE is the problem? Without monitoring, you're blind. Is it the database? The API? The network? You spend 4 hours debugging instead of going home.
>
> *Thứ 6, 5h chiều. Người dùng bắt đầu phàn nàn: "App chậm quá!" Bạn kiểm tra server - CPU 30%, RAM 50%. Mọi thứ trông bình thường. Nhưng vấn đề Ở ĐÂU? Không có monitoring, bạn như mù. Là database? API? Network? Bạn mất 4 tiếng debug thay vì về nhà.*
>
> **With proper observability, you would see: "Database query latency spiked to 5 seconds at 4:55 PM" - problem found in 2 minutes!**
>
> *Với observability đúng cách, bạn sẽ thấy: "Database query latency tăng lên 5 giây lúc 4:55 PM" - tìm ra vấn đề trong 2 phút!*

**Observability** is the ability to understand the internal state of a system by examining its outputs. In DevOps, this is an extremely important skill to:

*Observability (Khả năng quan sát) là khả năng hiểu trạng thái bên trong của một hệ thống chỉ bằng cách xem các đầu ra của nó. Trong DevOps, đây là kỹ năng cực kỳ quan trọng để:*

- **Detect incidents quickly** *(Phát hiện sự cố nhanh chóng)*
- **Understand root causes** *(Hiểu nguyên nhân gốc rễ)*
- **Ensure performance and reliability** *(Đảm bảo hiệu năng và độ tin cậy)*

#### The Three Pillars of Observability (Ba trụ cột của Observability)

| Pillar (Trụ cột) | Description (Mô tả) | Example Tools (Công cụ ví dụ) |
|------------------|---------------------|-------------------------------|
| 📈 **Metrics (Số liệu)** | Quantitative data over time (CPU, RAM, request count) *(Dữ liệu định lượng theo thời gian)* | Prometheus, Datadog |
| 📜 **Logs (Nhật ký)** | Records of events in the system *(Bản ghi sự kiện xảy ra trong hệ thống)* | Loki, ELK Stack |
| 🔗 **Traces (Dấu vết)** | Track a request across multiple services *(Theo dõi một request đi qua nhiều services)* | Jaeger, Zipkin |

---

### 2. Prometheus - Metrics Collection (Thu thập Metrics)

#### Prometheus là gì? (What is Prometheus?)

**Prometheus** là hệ thống giám sát và cảnh báo mã nguồn mở, ban đầu được xây dựng tại SoundCloud. Nó thu thập và lưu trữ metrics dưới dạng **time series data** (dữ liệu chuỗi thời gian).

*Prometheus is an open-source monitoring and alerting system, originally built at SoundCloud. It collects and stores metrics as time series data.*

**Cách Prometheus hoạt động (How it works):**

1. Prometheus **pull** (kéo) metrics từ các ứng dụng thông qua HTTP endpoint (thường là `/metrics`).
2. Các ứng dụng **expose** metrics ở định dạng Prometheus.
3. Prometheus lưu trữ metrics và cho phép truy vấn bằng **PromQL**.

#### Prometheus Configuration (Cấu hình Prometheus)

The main Prometheus config file defines "jobs" - each job is a group of targets (applications) to collect metrics from.

*File cấu hình chính của Prometheus định nghĩa các "job" - mỗi job là một nhóm targets (ứng dụng) cần thu thập metrics.*

```yaml
# prometheus.yml
global:
  scrape_interval: 15s  # Thu thập metrics mỗi 15 giây

scrape_configs:
  # Job thu thập metrics của chính Prometheus
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  # Job thu thập metrics của Node Exporter (CPU, RAM, Disk của server)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
  
  # Job thu thập metrics của ứng dụng
  - job_name: 'app'
    static_configs:
      - targets: ['app:3000']
```

**Giải thích (Explanation):**

- `scrape_interval`: Tần suất Prometheus pull metrics.
- `job_name`: Tên nhóm targets, giúp phân loại metrics.
- `targets`: Danh sách địa chỉ `host:port` của các ứng dụng expose metrics.

### 2. Grafana Dashboard (Bảng điều khiển Grafana)

Grafana visualizes Prometheus metrics as beautiful, interactive dashboards. Here's a simple panel definition.

*Grafana biểu diễn metrics của Prometheus thành dashboards đẹp, tương tác. Dưới đây là định nghĩa panel đơn giản.*

```json
{
  "panels": [
    {
      "title": "CPU Usage",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(process_cpu_seconds_total[5m])"
        }
      ]
    }
  ]
}
```

### 3. PromQL Basics (PromQL cơ bản)

PromQL is Prometheus's query language. These are the most common queries you'll write.

*PromQL là ngôn ngữ truy vấn của Prometheus. Đây là các query phổ biến nhất bạn sẽ viết.*

```promql
# CPU usage (Sử dụng CPU)
rate(process_cpu_seconds_total[5m])

# Memory usage (Sử dụng bộ nhớ)
process_resident_memory_bytes / 1024 / 1024

# HTTP request rate (Tỷ lệ yêu cầu HTTP)
rate(http_requests_total[5m])

# Error rate (Tỷ lệ lỗi)
rate(http_requests_total{status="500"}[5m])

# 95th percentile latency (Độ trễ phân vị 95)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### 4. Alerting (Cảnh báo)

```yaml
# alerting.rules.yml
groups:
  - name: example
    rules:
      - alert: HighCPU
        expr: rate(process_cpu_seconds_total[5m]) > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
```

### 5. Loki Logging

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      replication_factor: 1

schema_config:
  configs:
    - from: 2020-01-01
      store: boltdb
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 168h
```

---

> ✅ **Checkpoint - Before continuing, make sure you can answer:**
> *(Trước khi tiếp tục, hãy chắc bạn có thể trả lời:)*
>
> - [ ] What are the three pillars of observability? *(Ba trụ cột của observability là gì?)*
> - [ ] How does Prometheus collect metrics? *(Prometheus thu thập metrics như thế nào?)*
> - [ ] What is PromQL used for? *(PromQL dùng để làm gì?)*
> - [ ] When would you use Loki vs ELK Stack? *(Khi nào dùng Loki vs ELK Stack?)*
>
> *If you can't answer, please re-read the sections above!*

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [2.4 Kubernetes](../2.4_Kubernetes_Core/) | **2.5 Monitoring** | [2.6 Capstone](../2.6_Capstone_Project/) |

---

**Master observability for production systems! 📊**

*Thành thạo khả năng quan sát cho hệ thống production!*

</div>
