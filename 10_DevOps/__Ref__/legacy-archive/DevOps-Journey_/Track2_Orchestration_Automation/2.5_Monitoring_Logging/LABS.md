# 🔬 Labs: Monitoring & Logging

> **Hands-on Labs for Prometheus, Grafana & Logging**
>
> *Bài thực hành Prometheus, Grafana và Logging.*

---

## 🔬 Lab 1: Prometheus Setup

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

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
```

```bash
docker compose up -d
# Access: http://localhost:9090
```

---

## 🔬 Lab 2: Grafana Dashboards

```yaml
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  grafana-data:
```

1. Access <http://localhost:3000> (admin/admin)
2. Add Prometheus data source
3. Import dashboard (ID: 1860 for Node Exporter)

---

## 🔬 Lab 3: Application Metrics

```javascript
// Express.js with prom-client
const client = require('prom-client');
const express = require('express');

const app = express();

// Metrics
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'path', 'status']
});

app.use((req, res, next) => {
  res.on('finish', () => {
    httpRequestsTotal.inc({
      method: req.method,
      path: req.path,
      status: res.statusCode
    });
  });
  next();
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```

---

## 🔬 Lab 4: Alerting

```yaml
# alertmanager.yml
global:
  slack_api_url: 'https://hooks.slack.com/services/xxx'

route:
  receiver: 'slack'

receivers:
  - name: 'slack'
    slack_configs:
      - channel: '#alerts'
        text: '{{ .CommonAnnotations.summary }}'
```

---

## 🔬 Lab 5: Loki Logging Stack

```yaml
version: '3.8'

services:
  loki:
    image: grafana/loki:2.9.0
    ports:
      - "3100:3100"

  promtail:
    image: grafana/promtail:2.9.0
    volumes:
      - /var/log:/var/log
      - ./promtail.yml:/etc/promtail/config.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

---

## ✅ Checklist

- [ ] Lab 1: Prometheus
- [ ] Lab 2: Grafana
- [ ] Lab 3: App Metrics
- [ ] Lab 4: Alerting
- [ ] Lab 5: Loki

---

## ✅ General Verification (Kiểm chứng tổng quát)

Verify monitoring stack is working:

*(Xác nhận monitoring stack hoạt động:)*

```bash
# Check services running (Kiểm tra services chạy)
docker compose ps

# Test Prometheus (Kiểm tra Prometheus)
curl http://localhost:9090/-/healthy

# Test Grafana (Kiểm tra Grafana)
curl -I http://localhost:3000

# Test Node Exporter metrics (Kiểm tra metrics Node Exporter)
curl http://localhost:9100/metrics | head -20

# Test Loki (Kiểm tra Loki)
curl http://localhost:3100/ready
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Solution |
|-------|----------|
| `Prometheus target down` | Check exporter running, firewall rules *(Kiểm tra exporter và firewall)* |
| `Grafana: no data` | Check data source URL, time range *(Kiểm tra URL và khoảng thời gian)* |
| `Alert not firing` | Check alert rules, Alertmanager config *(Kiểm tra rules và config)* |
| `Loki: no logs` | Check promtail config, log paths *(Kiểm tra cấu hình promtail)* |
| `Port conflict` | Change host ports in docker-compose *(Đổi port)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

```bash
# Stop monitoring stack (Dừng monitoring stack)
docker compose down

# Remove volumes (Xóa volumes)
docker compose down -v

# Remove config files (Xóa files cấu hình)
rm -f prometheus.yml alertmanager.yml promtail.yml

# Remove images (Xóa images)
docker rmi prom/prometheus prom/node-exporter grafana/grafana grafana/loki grafana/promtail
```

---

**[← Back to README](./README.md)**

