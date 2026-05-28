# Bài #20 — Create Deployment (Imperative & Declarative)

> 🎯 **Khái niệm quan trọng nhất Module 07** — Deployment là tài nguyên dùng nhiều nhất trong K8s production.

---

## 📋 Metadata

- **Bài số:** #20
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~7 phút
- **Prerequisites:** [Module 06 — ReplicaSet](../06-replicaset/README.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **mối quan hệ:** Deployment → ReplicaSet → Pod
- [ ] Tạo Deployment bằng cả Imperative + Declarative
- [ ] Hiểu cấu trúc YAML Deployment
- [ ] Phân biệt phần **Deployment spec** vs **Pod template**

---

## 📚 Nội Dung

### 1. Quan Hệ: Deployment ⊃ ReplicaSet ⊃ Pod

```
┌─────────────── Deployment "app1-deploy" ────────────────┐
│                                                          │
│  ┌─────── ReplicaSet "app1-deploy-9d5..." ────┐         │
│  │                                              │         │
│  │   ┌──── Pod ────┐  ┌──── Pod ────┐           │         │
│  │   │ image: v1   │  │ image: v1   │           │         │
│  │   └─────────────┘  └─────────────┘           │         │
│  │   ┌──── Pod ────┐                            │         │
│  │   │ image: v1   │                            │         │
│  │   └─────────────┘                            │         │
│  │   replicas: 3                                │         │
│  └──────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────┘
```

**Khi update image v1 → v2:**

```
┌─────────────── Deployment "app1-deploy" ────────────────┐
│                                                          │
│  ┌─────── ReplicaSet "9d5..." (v1) ───┐                  │
│  │   replicas: 0  ← scale xuống 0    │   (giữ lại)       │
│  └────────────────────────────────────┘                  │
│                                                          │
│  ┌─────── ReplicaSet "8b7..." (v2) ───┐  ← TẠO MỚI       │
│  │   ┌── Pod ──┐ ┌── Pod ──┐ ┌── Pod ──┐                 │
│  │   │ v2      │ │ v2      │ │ v2      │                 │
│  │   └─────────┘ └─────────┘ └─────────┘                 │
│  │   replicas: 3                       │                 │
│  └────────────────────────────────────┘                  │
└──────────────────────────────────────────────────────────┘
```

→ **Deployment quản lý nhiều RS** → có thể **rollback** về RS cũ.

---

### 2. Imperative — Tạo Deployment Nhanh

```bash
kubectl create deployment <name> \
  --image=<image> \
  --replicas=<n> \
  --port=<port>
```

**Ví dụ:**

```bash
kubectl create deployment app1-deploy \
  --image=nginx:1.24-alpine \
  --replicas=3 \
  --port=80

# Output:
# deployment.apps/app1-deploy created

kubectl get deploy
# NAME           READY   UP-TO-DATE   AVAILABLE   AGE
# app1-deploy    3/3     3            3           10s

kubectl get rs
# NAME                       DESIRED   CURRENT   READY   AGE
# app1-deploy-9d5xxx         3         3         3       10s

kubectl get pods
# NAME                              READY   STATUS    AGE
# app1-deploy-9d5xxx-aaa             1/1     Running   10s
# app1-deploy-9d5xxx-bbb             1/1     Running   10s
# app1-deploy-9d5xxx-ccc             1/1     Running   10s
```

> 💡 Naming: `<deployment>-<rs-hash>-<pod-hash>`

---

### 3. Declarative — Manifest Đầy Đủ

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2-deploy
  labels:
    app: app2
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app2          # ← Phải khớp template.metadata.labels
  template:              # ← TEMPLATE Pod
    metadata:
      labels:
        app: app2        # ← Match selector!
    spec:
      containers:
        - name: simple-app
          image: nginx:1.24-alpine
          ports:
            - containerPort: 80
```

**Phân chia thành 2 phần:**

```
┌───── PHẦN DEPLOYMENT ──────┐    ┌────── PHẦN POD TEMPLATE ──────┐
│  apiVersion, kind, name    │    │  template:                     │
│  spec.replicas             │    │    metadata.labels             │
│  spec.selector             │    │    spec.containers             │
│  spec.strategy             │    │    spec.volumes                │
└────────────────────────────┘    └────────────────────────────────┘
   ↑                                  ↑
   Cấu hình của Deployment            Cấu hình của Pod sẽ tạo
```

---

## 💻 Hands-On / Demo

### Imperative

```bash
kubectl create deployment app1-deploy \
  --image=nginx:1.24-alpine \
  --replicas=2 \
  --port=80

# Kiểm tra cả 3 cấp
kubectl get deploy
kubectl get rs
kubectl get pods
```

### Declarative

**File `deployment.yaml`:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app2
  template:
    metadata:
      labels:
        app: app2
    spec:
      containers:
        - name: simple-app
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
```

```bash
kubectl apply -f deployment.yaml
kubectl get deploy
kubectl get rs
```

### Generate YAML từ Imperative (mẹo hay)

```bash
kubectl create deployment app3 \
  --image=nginx \
  --dry-run=client -o yaml > app3.yaml
# Mở file ra sửa, rồi apply
```

### Cleanup

```bash
kubectl delete deploy app1-deploy app2-deploy
```

---

## ⚠️ Lưu Ý

- 🔥 `apiVersion: apps/v1` (KHÔNG `v1`)
- 🔥 `selector.matchLabels` PHẢI khớp `template.metadata.labels`
- 🔥 Deployment **tự động tạo RS** — không cần tự tạo RS
- ✅ **Production:** dùng Deployment, KHÔNG dùng RS trực tiếp
- ⚠️ Trừ **CronJob** hoặc **Job** thì có thể dùng các kind khác

---

## ✅ Self-Check

1. **Mối quan hệ Deployment → RS → Pod là gì?**
   <details>
   <summary>Đáp án</summary>
   Deployment **quản lý nhiều** ReplicaSet (1 RS active + N RS cũ). Mỗi RS quản lý nhiều Pod.
   </details>

2. **`apiVersion` của Deployment?**
   <details>
   <summary>Đáp án</summary>
   `apps/v1`
   </details>

3. **Tạo Deployment Imperative bằng lệnh gì?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl create deployment <name> --image=<image> --replicas=<n>
   ```

   </details>

4. **Khi đổi image trên Deployment, hệ thống làm gì?**
   <details>
   <summary>Đáp án</summary>
   - Tạo **RS mới** với image mới
   - Scale RS mới lên
   - Scale RS cũ xuống 0 (vẫn giữ để rollback)
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Module 06 — ReplicaSet](../06-replicaset/README.md)
- ➡️ [Bài #21 — Scale & Expose Deployment](02-scale-expose-deployment.md)

### Tài Nguyên

- 📖 [Deployment Concept](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- 📺 Video gốc: `Decopy_✅ #20 Create Deployment..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Deployment dựa trên ReplicaSet. Hiểu RS rồi học Deployment rất dễ chịu."*

> 💬 *"Hầu hết tình huống production các bạn dùng Deployment. Trừ khi làm CronJob hay Job thì mới dùng RS only."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
