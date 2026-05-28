# Bài #31 — Demo Services (ClusterIP, NodePort, LoadBalancer)

> 🎯 Hands-on tạo cả 3 loại Service phổ biến.

---

## 📋 Metadata

- **Bài số:** #31
- **Module:** 08-services
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~12 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Viết YAML manifest cho Service
- [ ] Tạo và test ClusterIP
- [ ] Tạo và test NodePort
- [ ] Tạo và test LoadBalancer (trên Minikube)
- [ ] Sử dụng `kubectl api-resources`

---

## 📚 Nội Dung

### 1. `kubectl api-resources` — Xem Tất Cả Resource

```bash
kubectl api-resources

# NAME           SHORTNAMES   APIVERSION   NAMESPACED   KIND
# pods           po           v1           true         Pod
# services       svc          v1           true         Service
# deployments    deploy       apps/v1      true         Deployment
# ...
```

**Mẹo dùng shortnames:**

```bash
kubectl get pods       →   kubectl get po
kubectl get services   →   kubectl get svc
kubectl get deployment →   kubectl get deploy
```

---

### 2. ClusterIP Service — YAML

**`cluster-ip-svc.yaml`:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cluster-ip-svc
spec:
  # type: ClusterIP    # ← Mặc định, không cần ghi
  selector:
    app: app1          # ← Match Pod có label này
  ports:
    - protocol: TCP
      port: 8081       # ← Service port (truy cập qua đây)
      targetPort: 8080 # ← Container port (port của ứng dụng)
```

**Triển khai:**

```bash
kubectl apply -f cluster-ip-svc.yaml

kubectl get svc
# NAME             TYPE        CLUSTER-IP      PORT(S)    AGE
# cluster-ip-svc   ClusterIP   10.96.135.14    8081/TCP   10s
```

---

### 3. Tạo Pod Khớp Label

```bash
kubectl run pod-1 \
  --image=hieuvu/simple-app:v1 \
  --port=8080 \
  --labels="app=app1,environment=demo"

# Verify Pod chạy
kubectl get po
# NAME    READY   STATUS    AGE
# pod-1   1/1     Running   10s

# Service tự động phát hiện Pod
kubectl describe svc cluster-ip-svc
# Endpoints: 10.244.1.22:8080   ← Pod IP + container port
```

---

### 4. Test Load-balancing (Tạo Thêm Pod)

```bash
kubectl run pod-2 \
  --image=hieuvu/simple-app:v1 \
  --port=8080 \
  --labels="app=app1,environment=demo"

kubectl describe svc cluster-ip-svc
# Endpoints: 10.244.1.22:8080,10.244.1.23:8080
# ↑ Service tự động cộng thêm Pod-2 vào endpoint!
```

> 💡 Service rất "thông minh": Pod nào có label khớp selector đều được tự động thêm.

---

### 5. Test Truy Cập Service Từ Trong Cluster

```bash
# Vào trong Pod để test
kubectl exec -it pod-1 -- sh

# Trong Pod:
nslookup cluster-ip-svc
# Server:    10.96.0.10
# Address:   10.96.0.10#53
# Name:      cluster-ip-svc.default.svc.cluster.local
# Address:   10.96.135.14

# Gọi qua DNS
curl http://cluster-ip-svc:8081
# (response từ pod-1 hoặc pod-2)
```

> 🔥 **Form đầy đủ DNS:** `<service>.<namespace>.svc.cluster.local`

---

### 6. NodePort Service — YAML

**`nodeport-svc.yaml`:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nodeport-svc
spec:
  type: NodePort
  selector:
    app: app1
  ports:
    - protocol: TCP
      port: 8081         # Service port (in-cluster)
      targetPort: 8080   # Container port
      nodePort: 31238    # Node port (30000-32767)
```

**Triển khai + Test:**

```bash
kubectl apply -f nodeport-svc.yaml

kubectl get svc
# NAME           TYPE       CLUSTER-IP      PORT(S)          AGE
# nodeport-svc   NodePort   10.96.10.20    8081:31238/TCP   5s

# Truy cập qua Minikube
minikube service nodeport-svc --url
# http://192.168.49.2:31238

curl http://192.168.49.2:31238
```

---

### 7. LoadBalancer Service — YAML

**`lb-svc.yaml`:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: lb-svc
spec:
  type: LoadBalancer
  selector:
    app: app1
  ports:
    - protocol: TCP
      port: 8085       # External port (qua LB)
      targetPort: 8080 # Container port
```

**Triển khai:**

```bash
kubectl apply -f lb-svc.yaml

kubectl get svc
# NAME     TYPE          CLUSTER-IP    EXTERNAL-IP   PORT(S)         AGE
# lb-svc   LoadBalancer  10.96.50.10   <pending>     8085:30552/TCP  10s
```

> ⚠️ Trên **Minikube**: `EXTERNAL-IP` sẽ mãi `<pending>` vì không có cloud provider. Cần `minikube tunnel`.

```bash
minikube tunnel    # mở terminal khác
kubectl get svc lb-svc
# EXTERNAL-IP: 127.0.0.1
```

---

## 💻 Hands-On / Demo

```bash
# Setup Pods
kubectl run pod-1 --image=nginx:1.24 --port=80 -l app=app1
kubectl run pod-2 --image=nginx:1.24 --port=80 -l app=app1

# 1. ClusterIP
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: my-clusterip
spec:
  selector:
    app: app1
  ports:
  - port: 80
    targetPort: 80
EOF

# Test trong cluster
kubectl run -it --rm test --image=busybox --restart=Never -- \
  wget -qO- my-clusterip

# 2. NodePort
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport
spec:
  type: NodePort
  selector:
    app: app1
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
EOF

curl $(minikube ip):30080

# 3. Cleanup
kubectl delete svc my-clusterip my-nodeport
kubectl delete pod pod-1 pod-2
```

---

## ⚠️ Lưu Ý

- 🔥 `targetPort` = **port trong container**
- 🔥 `port` = **Service port** (nội bộ)
- 🔥 `nodePort` = **port trên Node** (30000-32767)
- ⚠️ Mỗi `nodePort` chỉ dùng 1 lần trong cluster — collision sẽ fail
- 💡 Nếu **không chỉ định** `nodePort` → K8s tự cấp port ngẫu nhiên
- ⚠️ ClusterIP → KHÔNG truy cập được từ bên ngoài cluster

---

## ✅ Self-Check

1. **Lệnh nào xem tất cả resource hỗ trợ?**
   <details>
   <summary>Đáp án</summary>
   `kubectl api-resources`
   </details>

2. **DNS đầy đủ của Service `app1` ở namespace `default`?**
   <details>
   <summary>Đáp án</summary>
   `app1.default.svc.cluster.local`
   </details>

3. **Service tự cập nhật endpoint khi nào?**
   <details>
   <summary>Đáp án</summary>
   Khi Pod được tạo/xóa với label khớp selector. Hoàn toàn tự động!
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #30 — Service Types](01-services-types-overview.md)
- ➡️ [Module 09 — Namespace](../09-namespace/README.md)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
