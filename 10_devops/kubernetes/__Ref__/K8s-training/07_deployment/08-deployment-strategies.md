# Bài #27 — Recreate vs RollingUpdate (Deployment Strategies)

> 🎯 2 chiến lược triển khai chính trong K8s — chọn cái nào cho production?

---

## 📋 Metadata

- **Bài số:** #27
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~10 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu cơ chế **RollingUpdate** (default)
- [ ] Hiểu cơ chế **Recreate**
- [ ] Cấu hình `maxSurge` và `maxUnavailable`
- [ ] Chọn chiến lược phù hợp cho từng môi trường

---

## 📚 Nội Dung

### 1. Recreate Strategy

```yaml
spec:
  strategy:
    type: Recreate
```

**Cơ chế:**

```
[Kill ALL old Pods]  →  [Create ALL new Pods]
   v1 v1 v1 v1 v1            v2 v2 v2 v2 v2
   ❌❌❌❌❌                  ✅✅✅✅✅
   ↑                          ↑
   Down-time                  Service available
```

**Đặc điểm:**

- ⚠️ **CÓ down-time** (tất cả Pod cũ bị xóa trước khi tạo mới)
- ✅ Tiết kiệm tài nguyên (không cần Pod dự phòng)
- 💡 Phù hợp: **dev/staging**, **DB migration**, **app không cho phép 2 version chạy song song**

---

### 2. RollingUpdate Strategy (Default)

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # tối đa thêm Pod (vượt replicas)
      maxUnavailable: 25%  # tối đa Pod thiếu (so với replicas)
```

**Cơ chế:**

```
Bước 1: [Tạo Pod mới] → [Đợi Ready] → [Xóa Pod cũ]
Bước 2: Lặp lại đến khi tất cả Pod = v2

  v1 v1 v1 v1 v1 v1 v1 v1 v1 v1
            ↓ tạo 2 Pod mới (maxSurge=2)
  v1 v1 v1 v1 v1 v1 v1 v1 v1 v1 + v2 v2
            ↓ Pod v2 ready, xóa 2 v1
  v1 v1 v1 v1 v1 v1 v1 v1 + v2 v2
            ↓ tiếp tục
  ...
  v2 v2 v2 v2 v2 v2 v2 v2 v2 v2
```

**Đặc điểm:**

- ✅ **KHÔNG** down-time
- ⚠️ Cần **tài nguyên dư** (để tạo Pod mới song song)
- 💡 Phù hợp: **production**

---

### 3. `maxSurge` và `maxUnavailable`

| Tham số | Ý nghĩa | Default |
|---------|---------|---------|
| `maxSurge` | Số Pod **THÊM** vượt `replicas` | 25% |
| `maxUnavailable` | Số Pod **THIẾU** so với `replicas` | 25% |

**Ví dụ với `replicas=10`:**

| Cấu hình | Tối đa cùng lúc | Tối thiểu running |
|----------|-----------------|---------------------|
| `maxSurge=2`, `maxUnavailable=1` | 12 Pod | 9 Pod |
| `maxSurge=25%`, `maxUnavailable=25%` | 13 Pod | 8 Pod (làm tròn) |
| `maxSurge=0`, `maxUnavailable=1` | 10 Pod | 9 Pod |

---

### 4. Trade-off Tốc Độ vs Tài Nguyên

```
maxSurge cao   → roll-out nhanh + tốn tài nguyên hơn
maxSurge thấp  → roll-out chậm + tiết kiệm tài nguyên
```

**Production lớn (1000+ Pod):**

- `maxSurge=10%`, `maxUnavailable=0` → an toàn nhưng chậm (có thể 30 phút)
- `maxSurge=20%`, `maxUnavailable=5%` → cân bằng

---

### 5. YAML Đầy Đủ

**Recreate:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-deploy
spec:
  replicas: 10
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
        - name: simple-app
          image: hieuvu/simple-app:v1
```

**RollingUpdate:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-deploy
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
        - name: simple-app
          image: hieuvu/simple-app:v1
```

---

## 💻 Hands-On / Demo

```bash
# Recreate strategy
kubectl edit deployment app1-deploy
# Sửa: strategy.type: Recreate

# Update image — Pod cũ bị TERMINATE TRƯỚC, sau đó tạo mới
kubectl set image deployment/app1-deploy nginx=nginx:1.23
kubectl get pods -w
# Sẽ thấy: 10 Pod cũ Terminating → 0 Pod → 10 Pod mới Pending → Running

# Rolling update strategy
kubectl edit deployment app1-deploy
# Sửa: strategy.type: RollingUpdate, maxSurge: 2, maxUnavailable: 1

kubectl set image deployment/app1-deploy nginx=nginx:1.24
kubectl get pods -w
# Sẽ thấy: 10 Pod cũ + 2 Pod mới = 12 Pod cùng lúc
# Pod mới Ready → xóa 2 Pod cũ
```

---

## ⚠️ Lưu Ý

- 🔥 **Recreate** = down-time → KHÔNG dùng cho production critical
- ✅ **RollingUpdate** mặc định + an toàn
- 💡 Các strategy nâng cao: **Blue/Green**, **Canary**, **A/B testing** — cần thêm tool (Argo Rollouts, Flagger)
- ⚠️ Service phải có **readiness probe** để RollingUpdate hoạt động đúng

---

## ✅ Self-Check

1. **Strategy mặc định của Deployment?**
   <details>
   <summary>Đáp án</summary>
   `RollingUpdate` với `maxSurge: 25%`, `maxUnavailable: 25%`.
   </details>

2. **Khi nào dùng Recreate?**
   <details>
   <summary>Đáp án</summary>
   - Dev/staging (tiết kiệm tài nguyên)
   - App không cho 2 version chạy song song (DB migration không tương thích)
   - Hệ thống critical về tài nguyên
   </details>

3. **`maxSurge=0`, `maxUnavailable=1` ý nghĩa?**
   <details>
   <summary>Đáp án</summary>
   Không thêm Pod mới (giữ tổng = `replicas`), chấp nhận 1 Pod bị thiếu trong lúc rollout.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #26 — Change Cause](07-change-cause.md)
- ➡️ [Bài #28 — Progress Deadline](09-progress-deadline.md)

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Hệ thống production nên dùng RollingUpdate. Hệ thống dev/test ít quan trọng có thể dùng Recreate để tiết kiệm tài nguyên."*

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
