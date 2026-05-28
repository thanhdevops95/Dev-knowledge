# GIAI ĐOẠN 11: OBSERVABILITY - MẮT THẦN GIÁM SÁT

## 📌 MỤC TIÊU GIAI ĐOẠN 11
Khi hệ thống chạy trên K8s, bạn không thể SSH vào từng node xem log. Bạn cần Dashboard tập trung.
Chúng ta sẽ cài đặt bộ 3 quyền lực:
1. **Prometheus**: Thu thập số liệu (CPU, RAM, Request/s).
2. **Grafana**: Vẽ biểu đồ đẹp mắt.
3. **Loki**: Gom log từ tất cả các Pod về một chỗ.

---

## 🏗️ PHẦN 1: CÀI ĐẶT PROMETHEUS STACK (KUBE-PROMETHEUS-STACK)

Gói này bao gồm Prometheus + Grafana + AlertManager.

```bash
# Tạo namespace riêng cho gọn
kubectl create ns monitoring

# Cài đặt qua Helm
helm install my-kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring
```

## 🏗️ PHẦN 2: CÀI ĐẶT LOKI STACK (LOGGING)

Để xem log (thay vì gõ `kubectl logs` từng cái).

```bash
helm install my-loki grafana/loki-stack \
  --namespace monitoring \
  --set grafana.enabled=false \
  --set prometheus.enabled=false \
  --set promtail.enabled=true
```
*(Ta tắt grafana/prometheus tích hợp sẵn của loki-stack để dùng cái chung ở Phần 1)*

---

## 🔭 PHẦN 3: TRUY CẬP GRAFANA DASHBOARD

Mặc định Grafana không lộ ra ngoài Internet. Ta dùng `port-forward` để vào từ máy cá nhân.

### 1. Lấy mật khẩu Admin
```bash
kubectl get secret --namespace monitoring my-kube-prometheus-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
*(Copy chuỗi mật khẩu hiện ra)*

### 2. Port-forward
```bash
kubectl port-forward --namespace monitoring svc/my-kube-prometheus-stack-grafana 3000:80
```
*(Giữ terminal này chạy)*

### 3. Đăng nhập
- Mở trình duyệt: `http://localhost:3000`
- User: `admin`
- Pass: (Chuỗi vừa copy)

---

## 📊 PHẦN 4: KHÁM PHÁ DASHBOARD

### 1. Xem Metrics (K8s Cluster)
- Vào Menu -> Dashboards -> Manage.
- Chọn **Kubernetes / Compute Resources / Namespace (Pods)**.
- Bạn sẽ thấy biểu đồ CPU/RAM của từng Pod nhảy múa. Thử chạy Load Test (Giai đoạn 10) và quay lại đây xem biểu đồ dựng đứng!

### 2. Xem Logs (Loki)
- Vào Explore (hình la bàn).
- Ở dropdown Source, chọn **Loki**.
- Gõ query: `{app="backend"}` (hoặc chọn trong Log Browser).
- Bấm "Run query".
- Toàn bộ log của backend (dù có 10 pod) đều hiện ra ở đây. Bạn có thể filter theo từ khóa "Error" để tìm lỗi.

---

## 📝 TỔNG KẾT
Giờ đây bạn nắm rõ sức khỏe hệ thống trong lòng bàn tay.
- App chậm? -> Xem Grafana CPU.
- App lỗi 500? -> Xem Loki Log.

👉 **Bước tiếp theo:** Hệ thống khỏe nhưng có an toàn không? Giai đoạn 12: **DevSecOps**.
