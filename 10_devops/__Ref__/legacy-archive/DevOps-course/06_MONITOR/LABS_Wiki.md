# 🧪 MODULE 06: LABS - Prometheus & Grafana

## LAB 1: Cài đặt Prometheus

### docker-compose.yml

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

volumes:
  prometheus-data:
```

### prometheus.yml

```yaml
scrape_configs:
  - job_name: 'counter-app'
    static_configs:
      - targets: ['host.docker.internal:5000']
```

### Start

```bash
docker-compose up -d
# Access: http://localhost:9090
```

---

## LAB 2: Đo lường Counter App

### Update app.py

```python
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

request_count = Counter('counter_requests_total', 'Total requests')
increment_count = Counter('counter_increments_total', 'Total increments')

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)

@app.route('/')
def index():
    request_count.inc()
    # ... rest of code

@app.route('/increment')
def increment():
    increment_count.inc()
    # ... rest of code
```

### Test

```bash
curl http://localhost:5000/metrics
# counter_requests_total 42
# counter_increments_total 10
```

---

## LAB 3: Thiết lập Grafana

### Add to docker-compose.yml

```yaml
grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Configure

1. Login: <http://localhost:3000> (admin/admin)
2. Add Data Source → Prometheus → <http://prometheus:9090>
3. Create Dashboard → Add Panel
4. Query: `rate(counter_requests_total[5m])`
5. Save dashboard

---

## LAB 4: Cấu hình Cảnh báo

### alert.rules.yml

```yaml
groups:
  - name: counter-app
    rules:
      - alert: HighRequestRate
        expr: rate(counter_requests_total[1m]) > 100
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High request rate"
```

### Update prometheus.yml

```yaml
rule_files:
  - "/etc/prometheus/alert.rules.yml"

alerting:
  alertmanagers:
    - static_configs:
      - targets: ['alertmanager:9093']
```

✅ **Checklist**

- [ ] Prometheus running
- [ ] Metrics endpoint working
- [ ] Grafana dashboard created
- [ ] Alerts configured
