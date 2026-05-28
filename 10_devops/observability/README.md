# 📊 Observability — System Monitoring, Logging & Tracing

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 26/05/2026

> 🎯 *Observability (Khả năng quan sát) là giác quan của hệ thống. Khác với giám sát thụ động (Monitoring - báo hệ thống sống hay chết), Observability giúp bạn hiểu SỰ CỐ XẢY RA VÌ SAO nhờ sự liên kết chặt chẽ của 3 cột trụ: Metrics (Thông số), Logs (Nhật ký), và Traces (Dấu vết).*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu rõ bản chất 3 cột trụ của Observability, phân biệt Monitoring vs Observability và chuẩn OpenTelemetry
- [x] Làm chủ **Prometheus** & **PromQL** từ thu thập metrics (Counters, Gauges, Histograms) đến viết câu truy vấn phức tạp
- [x] Xây dựng hệ thống quản lý log tập trung sử dụng **Grafana Loki** và Logstash/ELK, truy vấn sâu với **LogQL**
- [x] Triển khai Distributed Tracing (Dấu vết phân tán) bằng **OpenTelemetry**, theo dõi vết request xuyên suốt các microservices
- [x] Thiết kế dashboards chuyên nghiệp trên **Grafana**, kết nối chéo dữ liệu Metrics ↔ Logs ↔ Traces
- [x] Xây dựng chiến lược cảnh báo thông minh qua Alertmanager, phân biệt SLI, SLO, SLA và quản lý Error Budget
- [x] Thấu hiểu và áp dụng các quy trình SRE (Site Reliability Engineering) trong thực tế vận hành

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Nền tảng 3 Cột trụ (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`What is Observability`](./lessons/01_basic/00_what-is-observability.md) | 🌱 Intro | ✅ 🌟 | Giới thiệu 3 cột trụ (Metrics, Logs, Traces), phân biệt vs Monitoring, tổng quan hệ sinh thái OTel, SLI/SLO. |
| **01** | [`Metrics & Prometheus`](./lessons/01_basic/01_metrics-prometheus.md) | 🌳 Lesson | ✅ 🌟 | Kiến trúc Prometheus (pull-based), 4 loại metric chính, viết các câu truy vấn PromQL cơ bản, cài exporters. |
| **02** | [`Logs with Loki & ELK`](./lessons/01_basic/02_logs-loki-elk.md) | 🌳 Lesson | ✅ 🌟 | Quản lý log tập trung, so sánh Loki (cardinality-based) vs ELK (full-text index), Promtail, cấu trúc JSON log. |
| **03** | [`Traces & OpenTelemetry`](./lessons/01_basic/03_traces-opentelemetry.md) | 🌳 Lesson | ✅ 🌟 | Khái niệm distributed tracing, spans, trace context propagation, setup OpenTelemetry cho ứng dụng FastAPI. |
| **04** | [`Grafana & Alerting`](./lessons/01_basic/04_grafana-and-alerting.md) | 🌳 Lesson | ✅ 🌟 | Tạo dashboard Grafana, cài đặt luật cảnh báo, Alertmanager, kết nối alert sang Slack/Telegram. |

### 📖 Lộ trình Intermediate — Đi sâu Vận hành Chuyên sâu (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | ✅ 🌟 | Tổng quan về các bài toán hóc búa khi vận hành hệ thống giám sát ở quy mô lớn (High Cardinality, Cost, SRE). |
| **01** | [`PromQL Deep & Alerting`](./lessons/02_intermediate/01_promql-deep-and-alerting.md) | 🌳 Lesson | ✅ 🌟 | Viết PromQL nâng cao (histogram quantile, recording rules), thiết lập cảnh báo dựa trên tỷ lệ cạn kiệt (burn rate). |
| **02** | [`Loki & LogQL Deep`](./lessons/02_intermediate/02_loki-logql-deep.md) | 🌳 Lesson | ✅ 🌟 | Làm chủ LogQL (parser, filter, metric queries), quản lý nhãn nhạy cảm (label cardinality) để tránh làm nghẽn Loki. |
| **03** | [`OTel Instrumentation`](./lessons/02_intermediate/03_opentelemetry-instrumentation.md) | 🌳 Lesson | ✅ 🌟 | Manual instrument tạo custom spans, truyền context qua hàng đợi (queues), cấu hình OTel Collector pipeline. |
| **04** | [`SRE Practices`](./lessons/02_intermediate/04_sre-practices.md) | 🌳 Lesson | ✅ 🌟 | Ứng dụng SRE: tính toán số liệu SLI/SLO thực tế, quản lý Error Budget, quy trình On-call và họp rút kinh nghiệm (Postmortem). |

---

## 🚀 Lộ trình đề xuất

*   **Beginner:** Bắt đầu với **Bài 00 (Intro)** để hiểu vì sao ta cần quan sát hệ thống. Sau đó học thực hành song song **Metrics (Bài 01)** và **Logs (Bài 02)** vì đây là hai công cụ dùng nhiều nhất hàng ngày.
*   **Intermediate:** Khi hệ thống bắt đầu phát triển thành nhiều microservices, hãy chuyển sang học **Distributed Tracing (Bài 03 của cả basic và intermediate)** để liên kết các request lại với nhau, tránh việc mò kim đáy bể khi xảy ra lỗi.

---

## 💡 Các bộ công cụ chính (Toolstack)

*   **Prometheus:** Hệ thống lưu trữ dữ liệu dạng time-series chuyên dụng cho metrics.
*   **Grafana Loki:** Giải pháp thu thập log hiệu quả, chi phí rẻ do không đánh chỉ mục toàn văn (full-text index).
*   **OpenTelemetry (OTel):** Bộ chuẩn hóa API và SDK nguồn mở thu thập dữ liệu viễn thông từ ứng dụng.
*   **Grafana:** Bảng điều khiển trung tâm để hiển thị mọi dữ liệu giám sát.

---

## 📌 Changelog

- **v1.0.0 (26/05/2026)** — Cập nhật mục lục hoàn chỉnh, tích hợp đầy đủ lộ trình Basic và các bài học nâng cao Intermediate.
- **v0.1.0 (20/05/2026)** — Khởi tạo file README khung (skeleton).
