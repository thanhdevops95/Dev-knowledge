# Module 14: OBSERVABILITY (Monitoring, Logging, Tracing)

> **"Bạn không thể sửa cái bạn không nhìn thấy - Observability là mắt của hệ thống"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu 3 pillars of observability (Metrics, Logs, Traces)
- ✅ Prometheus setup và PromQL
- ✅ Grafana dashboards
- ✅ Alerting với Alertmanager
- ✅ Logging stack (EFK/Loki)
- ✅ Distributed tracing basics
- ✅ APM concepts

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| Observability | Observability | Khả năng quan sát hệ thống |
| Metrics | Metrics | Số liệu đo lường |
| Logs | Logs | Nhật ký sự kiện |
| Traces | Traces | Theo dõi request xuyên suốt |
| Prometheus | Prometheus | Metrics collection system |
| Grafana | Grafana | Visualization tool |
| PromQL | PromQL | Prometheus Query Language |
| Exporter | Exporter | Thu thập metrics từ service |
| Alert | Alert | Cảnh báo |
| Alertmanager | Alertmanager | Quản lý alerts |
| Target | Scrape Target | Endpoint để scrape metrics |
| Label | Label | Nhãn phân loại metrics |
| Cardinality | Cardinality | Số unique label combinations |
| Dashboard | Dashboard | Bảng điều khiển trực quan |
| Panel | Panel | Ô hiển thị trong dashboard |
| EFK | Elasticsearch, Fluentd, Kibana | Stack logging |
| Loki | Grafana Loki | Log aggregation system |
| Jaeger | Jaeger | Distributed tracing |
| Span | Span | Một đoạn trong trace |
| APM | Application Performance Monitoring | Giám sát performance |

---

## ✅ Checklist Labs

### Labs Observability Concepts

- [ ] Lab 1: 3 pillars of observability
- [ ] Lab 2: Metrics vs Logs vs Traces
- [ ] Lab 3: USE method (Utilization, Saturation, Errors)
- [ ] Lab 4: RED method (Rate, Errors, Duration)
- [ ] Lab 5: Golden signals

### Labs Prometheus Basics

- [ ] Lab 6: Install Prometheus (Docker)
- [ ] Lab 7: Prometheus configuration
- [ ] Lab 8: Prometheus targets
- [ ] Lab 9: Prometheus UI
- [ ] Lab 10: Metric types (Counter, Gauge, Histogram, Summary)
- [ ] Lab 11: Node Exporter
- [ ] Lab 12: Scrape configuration

### Labs PromQL

- [ ] Lab 13: PromQL basics - instant vectors
- [ ] Lab 14: PromQL - range vectors
- [ ] Lab 15: PromQL - operators
- [ ] Lab 16: PromQL - aggregation (sum, avg, max, min)
- [ ] Lab 17: PromQL - rate và irate
- [ ] Lab 18: PromQL - histogram_quantile
- [ ] Lab 19: PromQL - label matching
- [ ] Lab 20: Recording rules

### Labs Grafana

- [ ] Lab 21: Install Grafana
- [ ] Lab 22: Add Prometheus datasource
- [ ] Lab 23: First dashboard
- [ ] Lab 24: Panel types (Graph, Stat, Table, Gauge)
- [ ] Lab 25: Variables trong dashboard
- [ ] Lab 26: Templating
- [ ] Lab 27: Dashboard annotations
- [ ] Lab 28: Dashboard provisioning
- [ ] Lab 29: Dashboard permissions
- [ ] Lab 30: Grafana alerting

### Labs Alerting

- [ ] Lab 31: Prometheus alerting rules
- [ ] Lab 32: Alertmanager installation
- [ ] Lab 33: Alertmanager configuration
- [ ] Lab 34: Alert routing
- [ ] Lab 35: Alert grouping
- [ ] Lab 36: Alert silencing
- [ ] Lab 37: Alert inhibition
- [ ] Lab 38: Slack notifications
- [ ] Lab 39: Email notifications
- [ ] Lab 40: PagerDuty integration

### Labs Application Metrics

- [ ] Lab 41: Python app with prometheus_client
- [ ] Lab 42: Custom metrics (counters, gauges)
- [ ] Lab 43: Histogram cho latency
- [ ] Lab 44: /metrics endpoint

### Labs Prometheus on Kubernetes

- [ ] Lab 45: kube-prometheus-stack
- [ ] Lab 46: ServiceMonitor
- [ ] Lab 47: PodMonitor
- [ ] Lab 48: PrometheusRule
- [ ] Lab 49: Kubernetes dashboards

### Labs Logging - EFK

- [ ] Lab 50: Elasticsearch basics
- [ ] Lab 51: Fluentd installation
- [ ] Lab 52: Fluentd configuration
- [ ] Lab 53: Kibana setup
- [ ] Lab 54: Kibana queries
- [ ] Lab 55: Index patterns

### Labs Logging - Loki

- [ ] Lab 56: Loki installation
- [ ] Lab 57: Promtail configuration
- [ ] Lab 58: LogQL basics
- [ ] Lab 59: Loki trong Grafana
- [ ] Lab 60: Log filtering và parsing

### Labs Logging Best Practices

- [ ] Lab 61: Structured logging (JSON)
- [ ] Lab 62: Log levels
- [ ] Lab 63: Correlation IDs
- [ ] Lab 64: Log retention policies

### Labs Tracing

- [ ] Lab 65: Jaeger installation
- [ ] Lab 66: Jaeger UI
- [ ] Lab 67: OpenTelemetry basics
- [ ] Lab 68: Instrument Python app
- [ ] Lab 69: Trace visualization
- [ ] Lab 70: Tracing trong Grafana

### Labs Counter App Observability

- [ ] Lab 71: Add metrics to Counter App
- [ ] Lab 72: Counter App dashboard
- [ ] Lab 73: Counter App alerts
- [ ] Lab 74: Counter App logging
- [ ] Lab 75: Full observability stack

---

## 🚨 Checklist Scenarios

### Scenarios về Metrics

- [ ] Scenario 1: Prometheus target down
- [ ] Scenario 2: High cardinality causing OOM
- [ ] Scenario 3: Metrics missing
- [ ] Scenario 4: Scrape timeout
- [ ] Scenario 5: Storage full

### Scenarios về PromQL

- [ ] Scenario 6: Query returns no data
- [ ] Scenario 7: Wrong rate calculation
- [ ] Scenario 8: Query too slow
- [ ] Scenario 9: Unexpected results from aggregation

### Scenarios về Dashboards

- [ ] Scenario 10: Dashboard load slow
- [ ] Scenario 11: Panel shows "No data"
- [ ] Scenario 12: Variable không work
- [ ] Scenario 13: Dashboard visualization confusing

### Scenarios về Alerting

- [ ] Scenario 14: Alert không fire khi nên fire
- [ ] Scenario 15: Alert firing sai (false positive)
- [ ] Scenario 16: Alert storm (quá nhiều alerts)
- [ ] Scenario 17: Notification không đến
- [ ] Scenario 18: Alert fatigue
- [ ] Scenario 19: On-call missed alert

### Scenarios về Logging

- [ ] Scenario 20: Logs không appear trong Kibana/Loki
- [ ] Scenario 21: Log parsing failed
- [ ] Scenario 22: Log volume quá lớn
- [ ] Scenario 23: Sensitive data in logs
- [ ] Scenario 24: Cannot find specific log entry

### Scenarios về Tracing

- [ ] Scenario 25: Traces incomplete
- [ ] Scenario 26: High latency không biết ở đâu
- [ ] Scenario 27: Span missing

### Scenarios về Production

- [ ] Scenario 28: Incident detection too slow
- [ ] Scenario 29: Root cause analysis khó
- [ ] Scenario 30: Capacity planning data needed
- [ ] Scenario 31: SLO breach not detected
- [ ] Scenario 32: Post-mortem data collection

---

## ⏱️ Thời lượng

**Ước tính:** 6-8 giờ

| Phần | Thời gian |
|------|-----------|
| Concepts (Labs 1-5) | 0.5 giờ |
| Prometheus (Labs 6-20) | 2 giờ |
| Grafana (Labs 21-30) | 1.5 giờ |
| Alerting (Labs 31-40) | 1 giờ |
| App metrics & K8s (Labs 41-49) | 1 giờ |
| Logging (Labs 50-64) | 1.5 giờ |
| Tracing & Counter App | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Cheatsheet](https://promlabs.com/promql-cheat-sheet/)
- [OpenTelemetry](https://opentelemetry.io/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
