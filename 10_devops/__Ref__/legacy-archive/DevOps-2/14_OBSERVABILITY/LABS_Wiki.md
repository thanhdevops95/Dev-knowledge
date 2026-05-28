# Module 14: Observability Labs

---

## 🔧 Lab 1: Setup Prometheus

```yaml
# docker-compose.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

```bash
docker-compose up -d
# Access http://localhost:9090
```

---

## 🔧 Lab 2: Setup Grafana

```yaml
# Add to docker-compose.yml
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

```bash
docker-compose up -d
# Access http://localhost:3000
# Login: admin/admin
# Add Prometheus as data source
```

---

## 🔧 Lab 3: Create Dashboard

1. Grafana → Create → Dashboard
2. Add panel
3. Query: `rate(http_requests_total[5m])`
4. Visualization: Graph
5. Save

---

## 🔧 Lab 4: Setup Alerts

```yaml
# alerting-rules.yml
groups:
  - name: alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

---

## 📋 Tổng kết

| Lab | Skill |
|-----|-------|
| 1 | Prometheus setup |
| 2 | Grafana setup |
| 3 | Dashboards |
| 4 | Alerting |

👉 **[SCENARIOS.md](SCENARIOS.md)**
