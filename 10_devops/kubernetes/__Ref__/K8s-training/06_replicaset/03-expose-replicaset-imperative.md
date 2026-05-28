# Bài #17 — Expose ReplicaSet Bằng Imperative Way

> 🎯 Hands-on nhanh: dùng `kubectl expose` để expose 3 Pod của RS thành 1 NodePort Service.

---

## 📋 Metadata

- **Bài số:** #17
- **Module:** 06-replicaset
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~2 phút
- **Prerequisites:** [Bài #16 — RS Labels & Selector](02-replicaset-labels-vs-selector.md), [Bài #10 — NodePort hands-on](../04-expose-pod-nodeport/02-nodeport-service-expose-pod.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Expose ReplicaSet thành NodePort Service bằng `kubectl expose`
- [ ] Thấy Service tự load-balance giữa 3 Pod backend
- [ ] Nhớ cú pháp expose cho **rs** (không phải `pod`)

---

## 📚 Nội Dung

### 1. So Sánh: Expose Pod vs Expose ReplicaSet

```bash
# Expose 1 Pod
kubectl expose pod app-1 --type=NodePort --port=80

# Expose tất cả Pod của RS
kubectl expose rs rs3 --type=NodePort --port=80
```

→ Cú pháp giống nhau, chỉ khác `pod` → `rs`.

> 💡 Service không quan tâm bạn expose Pod hay RS — nó vẫn chỉ dùng **selector** match Pod backend.

---

## 💻 Hands-On / Demo

### Setup: Tạo RS Trước

```yaml
# rs3.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs3
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app3
  template:
    metadata:
      labels:
        app: app3
    spec:
      containers:
        - name: app
          image: nginx:alpine
          ports:
            - containerPort: 80
```

```bash
kubectl apply -f rs3.yaml

# Verify 3 Pod đang chạy
kubectl get pods
# NAME        READY   STATUS    RESTARTS   AGE
# rs3-abc12   1/1     Running   0          10s
# rs3-def34   1/1     Running   0          10s
# rs3-ghi56   1/1     Running   0          10s
```

### Bước 1: Expose RS

```bash
kubectl expose rs rs3 \
  --name=service-3 \
  --type=NodePort \
  --port=80

# Output:
# service/service-3 exposed
```

### Bước 2: Kiểm Tra Service

```bash
kubectl get svc
# NAME         TYPE        CLUSTER-IP      PORT(S)        AGE
# service-3    NodePort    10.97.105.55    80:30256/TCP   5s
#                                              │
#                                              └─ NodePort random

kubectl describe svc service-3
# Selector:    app=app3       ← TỰ LẤY từ RS template label
# Endpoints:   10.99.9.9:80, 10.99.9.10:80, 10.99.9.11:80   ← 3 Pod IP!
```

### Bước 3: Truy Cập

```bash
# Trên Minikube
minikube service service-3 --url
# http://192.168.49.2:30256

# Curl nhiều lần — Service load-balance giữa 3 Pod
for i in {1..6}; do curl http://192.168.49.2:30256; echo; done
```

> 💡 Mỗi request có thể đi đến 1 Pod khác nhau (round-robin mặc định).

### Cleanup

```bash
kubectl delete svc service-3
kubectl delete rs rs3
```

---

## ⚠️ Lưu Ý

- 🔥 NodePort tạo bằng Imperative là **random** — production nên dùng YAML
- 🔥 `kubectl expose rs` tự lấy `selector` từ RS template label
- ⚠️ Khi xóa RS, **Service KHÔNG bị xóa theo** — phải xóa thủ công

---

## ✅ Self-Check

1. **Lệnh expose ReplicaSet?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl expose rs <rs-name> --name=<svc-name> --type=NodePort --port=<p>
   ```

   </details>

2. **Service biết Pod backend nào dựa vào đâu?**
   <details>
   <summary>Đáp án</summary>
   Dựa vào **selector** (match Pod label).
   </details>

3. **NodePort tạo bằng Imperative có cố định không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG** — random trong 30000-32767. Muốn cố định → YAML (Bài #18).
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #16 — RS Labels vs Selector](02-replicaset-labels-vs-selector.md)
- ➡️ [Bài #18 — Expose RS Declarative](04-expose-replicaset-declarative.md)

### Tài Nguyên

- 📺 Video gốc: `Decopy_✅ #17 _ Expose ReplicaSet Imperative..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Câu lệnh imperative này — đôi khi các bạn sẽ phải nhớ. Lâu lâu làm có khả năng quên. Để chắc cái việc quên đấy, mình sẽ dùng phương thức Declarative ở bài tiếp theo."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
