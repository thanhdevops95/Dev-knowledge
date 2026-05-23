# Bài 66 — Prometheus + Grafana Stack

> **Mục tiêu:** observability với RED metrics (Rate, Errors, Duration), Alert và Grafana dashboard.

## Tiên quyết

- Cluster còn ≥2 GB RAM trống.
- `myapp` đang chạy ở namespace `myapp-dev`; image đã expose endpoint `/metrics` (xem `myapp-metrics-deployment.yaml`).
- Helm 3 đã cài.

## File trong thư mục

- `myapp-metrics-deployment.yaml` — Deployment + Service đã expose `/metrics` qua port `http`.
- `servicemonitor.yaml` — Cho Prometheus Operator biết phải scrape myapp.
- `prometheusrule.yaml` — Alert HighErrorRate (rate 5xx > 5% trong 5 phút).
- `dashboards/myapp.json` — Skeleton Grafana dashboard (Import → JSON).

## Lệnh thủ công

```bash
# 1. Cài kube-prometheus-stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring
helm install kps prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --set grafana.adminPassword='admin' \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false

kubectl get pods -n monitoring

# 2. Deploy app có /metrics (giả định image bạn đã build và push)
kubectl apply -f myapp-metrics-deployment.yaml

# 3. Khai báo ServiceMonitor + PrometheusRule
kubectl apply -f servicemonitor.yaml
kubectl apply -f prometheusrule.yaml

# 4. Port-forward Prometheus + Grafana
kubectl port-forward -n monitoring svc/kps-grafana 3000:80 &
kubectl port-forward -n monitoring svc/kps-kube-prometheus-stack-prometheus 9090:9090 &

# 5. Mở Grafana http://localhost:3000 (admin/admin) → Dashboards → Import → JSON
#    paste nội dung dashboards/myapp.json
```

## Kết quả mong đợi

- Tại Prometheus UI (`:9090`) → Status → Targets: thấy job `myapp-monitor` UP.
- Query `myapp_request_total` ra kết quả > 0 sau khi `curl` app vài lần.
- Grafana hiển thị panel RPS + P95 latency.

## Câu hỏi

- RED metrics gồm những gì? Vì sao là chuẩn?
- ServiceMonitor cần ở cùng namespace với Prometheus không? (gợi ý: tùy `serviceMonitorNamespaceSelector`).

## Bài kế tiếp

```bash
cd ../67-velero-backup
```
