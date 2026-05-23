# 📋 Monitoring & Logging - Cheatsheet

> **Quick Reference for Prometheus, Grafana & ELK**
>
> *Tra cứu nhanh Prometheus, Grafana & ELK*

---

## 📊 Prometheus

### Configuration (Cấu hình)

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['localhost:8080']
  
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
```

### PromQL Queries

```promql
# Basic queries (Truy vấn cơ bản)
up                                  # Check targets
http_requests_total                 # Total requests

# Rate & increase (Tốc độ & tăng)
rate(http_requests_total[5m])       # Requests per second
increase(http_requests_total[1h])   # Increase in 1 hour

# Aggregation (Tổng hợp)
sum(rate(http_requests_total[5m])) by (status_code)
avg(node_cpu_seconds_total)

# Filtering (Lọc)
http_requests_total{status="200"}
http_requests_total{job=~"app.*"}
```

---

## 📈 Grafana

### Dashboard Query Examples

```promql
# CPU Usage (Sử dụng CPU)
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Usage (Sử dụng bộ nhớ)
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Disk Usage (Sử dụng đĩa)
100 - ((node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100)
```

---

## 🔔 Alertmanager

```yaml
# alertmanager.yml
route:
  receiver: 'slack'
  group_wait: 30s
  
receivers:
  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/...'
        channel: '#alerts'
```

### Alert Rules

```yaml
# rules.yml
groups:
  - name: example
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status="500"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

---

## 📝 ELK Stack

### Logstash Pipeline

```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

### Filebeat Config

```yaml
filebeat.inputs:
  - type: log
    paths:
      - /var/log/*.log

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
