# Bài #15 — Giới Thiệu ReplicaSet

> 🎯 **ReplicaSet** đảm bảo luôn có **đúng N Pod** chạy. Pod chết? Tự động tạo lại. Đây là nền tảng cho HA và scaling.

---

## 📋 Metadata

- **Bài số:** #15
- **Module:** 06-replicaset
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~10 phút
- **Prerequisites:** [Bài #14 — YAML Manifest 101](../05-imperative-vs-declarative/02-yaml-manifest-101.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **vấn đề** ReplicaSet giải quyết: HA + Self-healing
- [ ] Viết được manifest ReplicaSet đầy đủ
- [ ] Hiểu khái niệm **Label** và **Selector** (cốt lõi của ReplicaSet)
- [ ] Test self-healing: xóa Pod → ReplicaSet tự tạo lại

---

## 📚 Nội Dung

### 1. Vấn Đề Của Pod Đơn

```
   Trước khi có ReplicaSet:
   ┌── Node ────┐
   │  Pod app-1 │  ← chỉ 1 Pod
   └────────────┘
       │
       ▼ Pod chết!
   ┌── Node ────┐
   │  (empty)   │  ← Không ai tạo lại! ❌
   └────────────┘
```

→ Cần **cơ chế đảm bảo luôn có N Pod** đang chạy.

### 2. ReplicaSet Là Gì?

**ReplicaSet (RS)** = controller K8s đảm bảo:
- **Số lượng Pod = `replicas`** ở mọi thời điểm
- Pod bị xóa → **tự tạo lại**
- Pod thiếu → **tự bổ sung**

```
   ReplicaSet rs3 (replicas: 3)
   ┌── Node 1 ──┐  ┌── Node 2 ──┐
   │ Pod app-1  │  │  Pod app-3 │
   │ Pod app-2  │  │            │
   └────────────┘  └────────────┘
       3 Pod ✅

   Pod app-1 chết!
   ↓
   ┌── Node 1 ──┐  ┌── Node 2 ──┐
   │ Pod app-2  │  │  Pod app-3 │
   │ Pod app-X  │  │            │  ← Tự tạo Pod mới!
   └────────────┘  └────────────┘
       3 Pod ✅
```

> ⚠️ **ReplicaSet KHÔNG có Imperative way!** Phải dùng **YAML manifest** (Declarative) — đây là lý do bạn cần học YAML trước.

---

### 3. Cấu Trúc Manifest ReplicaSet

```yaml
apiVersion: apps/v1          # ← apps/v1 (KHÔNG phải v1)
kind: ReplicaSet             # ← Không thể đổi
metadata:
  name: rs3
  labels:
    app: rs3
spec:
  replicas: 3                # ← Số Pod mong muốn
  selector:                  # ← TÌM Pod theo label gì
    matchLabels:
      app: app3
  template:                  # ← TEMPLATE để TẠO Pod
    metadata:
      labels:
        app: app3            # ← LABEL phải MATCH selector
        project: demo
    spec:
      containers:
        - name: simple-app
          image: nginx:latest
          ports:
            - containerPort: 8080
```

> 🔑 **Quy tắc vàng:** `selector.matchLabels` PHẢI khớp với `template.metadata.labels`. Nếu không, ReplicaSet sẽ không "thấy" Pod nó tạo ra → tạo loop vô tận!

---

### 4. Label & Selector — Cơ Chế Group

```
┌───────────── Label ────────────┐
│  Là TAG gắn vào resource        │
│  Vd: app=app3, env=prod        │
└────────────────────────────────┘

┌──────────── Selector ──────────┐
│  Là QUERY tìm resource theo    │
│  label tương ứng                │
│  Vd: matchLabels: app=app3     │
└────────────────────────────────┘

   Selector "app=app3"
        │
        ▼ tìm thấy
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Pod      │  │Pod      │  │Pod      │
   │app=app3 │  │app=app3 │  │app=app3 │
   └─────────┘  └─────────┘  └─────────┘

   Pods khác (app=app2) → KHÔNG bị select
```

→ **Label/Selector** là pattern xuyên suốt K8s (Service cũng dùng).

---

## 💻 Hands-On / Demo

### Bước 1: Tạo file `rs3.yaml`

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs3
  labels:
    app: rs3
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app3
  template:
    metadata:
      labels:
        app: app3
        project: demo
    spec:
      containers:
        - name: simple-app
          image: nginx:1.25-alpine
          ports:
            - containerPort: 80
```

### Bước 2: Apply

```bash
# Trước khi apply
kubectl get rs
# No resources found

# Apply
kubectl apply -f rs3.yaml
# replicaset.apps/rs3 created

# Verify
kubectl get rs
# NAME   DESIRED   CURRENT   READY   AGE
# rs3    3         3         3       10s

kubectl get pods
# NAME        READY   STATUS    RESTARTS   AGE
# rs3-abc12   1/1     Running   0          10s
# rs3-def34   1/1     Running   0          10s
# rs3-ghi56   1/1     Running   0          10s
```

> 💡 Tên Pod = `<rs-name>-<hash-random>`. Đây là cách K8s đảm bảo Pod có tên unique.

### Bước 3: Test Self-Healing

```bash
# Xóa 1 Pod
kubectl delete pod rs3-abc12

# Watch ngay sau khi xóa
kubectl get pods -w

# NAME        READY   STATUS              RESTARTS   AGE
# rs3-def34   1/1     Running             0          1m
# rs3-ghi56   1/1     Running             0          1m
# rs3-XYZ99   0/1     ContainerCreating   0          2s   ← TỰ TẠO!
# rs3-XYZ99   1/1     Running             0          5s
```

→ ReplicaSet **tự tạo lại** Pod mới — bạn không cần làm gì!

### Bước 4: Inspect Pod Detail

```bash
# Xem 1 Pod chi tiết
kubectl describe pod rs3-def34

# Output (rút gọn):
# Labels:
#   app=app3
#   project=demo
# Controlled By:  ReplicaSet/rs3   ← Pod thuộc về rs3!
```

### Bước 5: Inspect ReplicaSet Detail

```bash
kubectl describe rs rs3

# Output (rút gọn):
# Replicas:       3 current / 3 desired
# Pods Status:    3 Running / 0 Waiting / 0 Succeeded / 0 Failed
# Pod Template:
#   Labels:  app=app3, project=demo
#   Containers:
#     simple-app:
#       Image:  nginx:1.25-alpine
```

### Cleanup

```bash
kubectl delete -f rs3.yaml
# replicaset.apps "rs3" deleted
# (Pod thuộc rs3 cũng tự xóa)
```

---

## ⚠️ Lưu Ý

- 🔥 ReplicaSet **không có Imperative way** — bắt buộc YAML
- 🔥 `selector.matchLabels` PHẢI khớp `template.metadata.labels`
- 🔥 Đặt `apiVersion: apps/v1` (KHÔNG phải `v1`)
- ⚠️ **Best practice 2026**: Hiếm dùng ReplicaSet trực tiếp — thường dùng **Deployment** (Module 07) bao bọc bên ngoài
- ⚠️ Nếu trong cluster **đã có Pod** với label match selector → ReplicaSet "đếm" cả Pod đó!

---

## ✅ Self-Check

1. **ReplicaSet đảm bảo điều gì?**
   <details>
   <summary>Đáp án</summary>
   Số lượng Pod luôn = `replicas`. Pod chết → tự tạo lại. Pod thừa → xóa.
   </details>

2. **`apiVersion` của ReplicaSet?**
   <details>
   <summary>Đáp án</summary>
   `apps/v1`
   </details>

3. **Pattern nào RS dùng để "biết" Pod nào thuộc về mình?**
   <details>
   <summary>Đáp án</summary>
   **Label & Selector** — `selector.matchLabels` match Pod's `labels`.
   </details>

4. **Có thể tạo ReplicaSet bằng `kubectl run` không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG** — ReplicaSet không có Imperative. Phải dùng YAML.
   </details>

5. **Xóa 1 Pod thuộc RS, hậu quả?**
   <details>
   <summary>Đáp án</summary>
   ReplicaSet tự động tạo Pod mới trong vài giây để duy trì replicas.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Module 05](../05-imperative-vs-declarative/README.md)
- ➡️ [Bài #16 — Cơ chế Label vs Selector](02-replicaset-labels-vs-selector.md)

### Tài Nguyên

- 📖 [ReplicaSet Concept](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- 📖 [Labels & Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
- 📺 Video gốc: `Decopy_✅ #15 _ Giới Thiệu ReplicaSet..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"ReplicaSet KHÔNG có Imperative — bắt buộc dùng YAML. Đây là lý do mình phải dạy YAML ở Bài #14 trước."*

> 💬 *"Tất cả tài nguyên K8s đều có label. Label chính là cơ chế để group/select các resource theo nhóm."*

> 💬 *"Bài tiếp theo mình sẽ demo: nếu trong cluster đã có Pod với label match → RS sẽ chỉ tạo thêm Pod còn thiếu, không tạo đủ replicas mới!"*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
