# Bài #38 — Metrics Server (Monitor CPU/Memory)

> 🎯 Add-on cho phép `kubectl top` xem usage thực tế.

---

## 📋 Metadata

- **Bài số:** #38
- **Module:** 10-resource-management
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~7 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu Metrics Server là gì
- [ ] Enable trên Minikube
- [ ] Sử dụng `kubectl top pod` và `kubectl top node`
- [ ] Hiểu nó là **prerequisite** cho HPA (Horizontal Pod Autoscaler)

---

## 📚 Nội Dung

### 1. Metrics Server Là Gì?

**Metrics Server** = Add-on **thu thập** CPU/Memory usage **thực tế** của Pod và Node.

```
┌─── Cluster ──────────────────────────────────┐
│                                               │
│  ┌─ Metrics Server ─┐    ┌── kubelet ──┐      │
│  │ Aggregator       │ ←──│ (mỗi Node)  │      │
│  │                  │    │             │      │
│  └──────────────────┘    └─────────────┘      │
│           │                                   │
│           ▼                                   │
│   kubectl top pod                             │
│   kubectl top node                            │
│   HPA (auto-scale)                            │
└───────────────────────────────────────────────┘
```

> 💡 Mỗi `kubelet` (chạy trên Node) đã đo metrics. Metrics Server **gom lại** thành API.

---

### 2. Khác Biệt: Resources Cấp Phát vs Thực Tế

```bash
# Resources cấp phát (request/limit)
kubectl describe pod my-pod | grep -A 5 Limits
# Limits:
#   cpu: 1
#   memory: 2Gi
# Requests:
#   cpu: 500m
#   memory: 1Gi

# Resources thực tế đang dùng (CẦN Metrics Server!)
kubectl top pod my-pod
# NAME     CPU(cores)   MEMORY(bytes)
# my-pod   35m          40Mi
```

→ Pod request **1 CPU, 2 GB** nhưng thực tế dùng **35m, 40Mi** → có thể giảm request!

---

### 3. Enable Trên Minikube

```bash
# Liệt kê add-ons
minikube addons list

# Enable Metrics Server
minikube addons enable metrics-server
# ✅  metrics-server was successfully enabled

# Verify Pod đang chạy
kubectl get pods -n kube-system | grep metrics-server
# metrics-server-xxx     1/1     Running
```

> ⚠️ Mất ~15-30 giây để Metrics Server "warm up" và bắt đầu thu data.

---

### 4. Enable Trên Cluster Khác (kubeadm, EKS, GKE...)

```bash
# Cài qua YAML chính thức
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Trên EKS (AWS)
# Phải enable thêm trong EKS console hoặc dùng Helm
```

---

### 5. Sử Dụng `kubectl top`

```bash
# Top Pod toàn cluster
kubectl top pod -A

# Top Pod theo namespace
kubectl top pod -n default

# Sort theo CPU
kubectl top pod --sort-by=cpu

# Sort theo Memory
kubectl top pod --sort-by=memory

# Top Node
kubectl top node
# NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
# minikube   123m         6%     1234Mi          15%
```

---

### 6. Tại Sao Metrics Server Quan Trọng?

✅ **Prerequisites** cho:

- 🔥 **HPA (Horizontal Pod Autoscaler)** — auto scale theo CPU/Memory
- 🔥 **VPA (Vertical Pod Autoscaler)** — auto adjust resources
- 🔥 **`kubectl top`** command
- 🔥 **Dashboard** (Lens, K9s) hiển thị usage

---

## 💻 Hands-On / Demo

```bash
# 1. Enable
minikube addons enable metrics-server

# Chờ ~30 giây rồi check
sleep 30
kubectl get pod -n kube-system | grep metrics-server

# 2. Tạo test Pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: stress-test
spec:
  containers:
    - name: stress
      image: nginx:1.24
      resources:
        requests:
          cpu: "500m"
          memory: "256Mi"
        limits:
          cpu: "1000m"
          memory: "512Mi"
EOF

# 3. Xem usage
kubectl top pod stress-test
# NAME          CPU(cores)   MEMORY(bytes)
# stress-test   1m           5Mi

# 4. Cleanup
kubectl delete pod stress-test
```

---

### Bonus: Stress Test với `polinux/stress`

> ⚠️ Image này chỉ chạy trên **AMD64** (không chạy trên Apple M1/M2).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: stress
spec:
  containers:
    - name: stress
      image: polinux/stress
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "1000m"
          memory: "1Gi"
      command: ["stress"]
      args: ["--vm", "1", "--vm-bytes", "1G", "--vm-hang", "1"]
```

```bash
kubectl apply -f stress.yaml
# Đợi 1 phút rồi kiểm tra
kubectl top pod stress
# Sẽ thấy CPU/Memory tăng lên gần limit
```

---

## ⚠️ Lưu Ý

- 🔥 Metrics Server **không có sẵn** — phải cài addon
- ⚠️ Lưu trữ metrics **trong RAM** (không persist) — ngắn hạn (1-2 phút)
- 💡 Cho long-term metrics → cần **Prometheus + Grafana**
- ⚠️ EKS không enable mặc định — phải cài thủ công

---

## ✅ Self-Check

1. **Lệnh xem usage thực tế của Pod?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl top pod
   ```

   </details>

2. **Tại sao cần Metrics Server cho HPA?**
   <details>
   <summary>Đáp án</summary>
   HPA cần biết Pod đang dùng bao nhiêu CPU/Memory để quyết định scale.
   </details>

3. **Enable trên Minikube bằng lệnh gì?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   minikube addons enable metrics-server
   ```

   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #37 — Command & Args](03-command-args.md)
- ➡️ [Bài #39 — Resource Quotas](05-resource-quotas.md)

### Tài Nguyên

- 📖 [Metrics Server GitHub](https://github.com/kubernetes-sigs/metrics-server)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
