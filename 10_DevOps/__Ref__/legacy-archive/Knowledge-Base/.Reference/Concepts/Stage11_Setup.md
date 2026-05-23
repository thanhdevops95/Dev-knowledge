# 🛠️ GIAI ĐOẠN 11: CHUẨN BỊ HELM

## 📌 MỤC TIÊU
Cài đặt phần mềm trên Kubernetes thủ công (viết hàng chục file YAML) rất mệt. **Helm** là "App Store" của K8s, giúp cài trọn gói Prometheus/Grafana chỉ với 1 lệnh.

---

## 1. CÀI ĐẶT HELM
- **macOS**: `brew install helm`
- **Windows**: `choco install kubernetes-helm`

## 2. THÊM REPO CẦN THIẾT
```bash
# Repo của Prometheus Community
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Repo của Grafana
helm repo add grafana https://grafana.github.io/helm-charts

# Update
helm repo update
```

## ✅ CHECKLIST
```bash
helm version
# Output: v3.x.x
```
Sẵn sàng cài đặt hệ thống giám sát khổng lồ!
