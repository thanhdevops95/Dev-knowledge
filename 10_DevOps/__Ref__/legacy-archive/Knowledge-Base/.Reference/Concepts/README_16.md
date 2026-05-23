# 🎯 GIAI ĐOẠN 11: OBSERVABILITY - MONITORING & LOGGING

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-11**.
- **Giai đoạn 11: Prometheus + Grafana + Loki** - Giám sát toàn diện!

Hệ thống chạy mà không biết sức khỏe thế nào là mù quáng. Observability giúp "nhìn thấy" mọi thứ.

## 🚀 CÁCH CHẠY

### Bước 1: Add Helm Repos
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Bước 2: Cài Prometheus Stack
```bash
kubectl create ns monitoring

helm install my-kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring
```

### Bước 3: Cài Loki (Logging)
```bash
helm install my-loki grafana/loki-stack \
  --namespace monitoring \
  --set grafana.enabled=false \
  --set prometheus.enabled=false \
  --set promtail.enabled=true
```

### Bước 4: Truy cập Grafana
```bash
# Lấy password
kubectl get secret --namespace monitoring my-kube-prometheus-stack-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# Port forward
kubectl port-forward --namespace monitoring \
  svc/my-kube-prometheus-stack-grafana 3000:80
```

Mở: http://localhost:3000
- User: `admin`
- Pass: (từ lệnh trên)

## 🧪 TESTING

### Test 1: Xem Metrics
1. Vào Grafana
2. Dashboards → Kubernetes / Compute Resources / Namespace (Pods)
3. Thấy biểu đồ CPU/RAM của từng Pod

### Test 2: Xem Logs
1. Explore → Chọn Loki
2. Query: `{app="backend"}`
3. Thấy tất cả logs của backend pods

### Test 3: Alert (Nâng cao)
1. Alerting → Alert rules
2. Tạo rule: "CPU > 80%"
3. Test bằng load test

## ✅ CHECKLIST

- [ ] Cài được Prometheus Stack
- [ ] Cài được Loki
- [ ] Truy cập được Grafana
- [ ] Xem được metrics
- [ ] Xem được logs
- [ ] Hiểu được Observability

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **Prometheus:** Thu thập metrics
2. ✅ **Grafana:** Visualization
3. ✅ **Loki:** Log aggregation
4. ✅ **Promtail:** Log shipper
5. ✅ **Dashboards:** Theo dõi real-time

## 🚧 TIẾP THEO

Giai đoạn 12: **DevSecOps** - Bảo mật!
