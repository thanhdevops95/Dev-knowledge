# Bài #35 — Requests & Limits (Cấp Phát Tài Nguyên)

> 🎯 Cấu hình **CPU/Memory** cho mỗi Pod — bảo vệ cluster khỏi pods "ăn hết" tài nguyên.

---

## 📋 Metadata

- **Bài số:** #35
- **Module:** 10-resource-management
- **Cấp độ:** `INTERMEDIATE` → `ADVANCED`
- **Thời lượng video gốc:** ~12 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **Requests** vs **Limits**
- [ ] Cấu hình `resources` cho container trong Pod
- [ ] Hành vi khi vượt giới hạn (CPU vs Memory)
- [ ] Đơn vị: `m` (millicores), `Mi`/`Gi` (memory)

---

## 📚 Nội Dung

### 1. Vấn Đề: Pod "Ăn Hết" Tài Nguyên

```
Node: 2 CPU, 4 GB RAM

Pod-A bị bug (vòng lặp vô hạn) →  Ăn hết 100% CPU
                                  Pod-B, Pod-C bị thiếu CPU → Slow
                                  Toàn bộ Node bị ảnh hưởng
```

→ **Cần giới hạn** mỗi Pod được dùng tối đa bao nhiêu.

---

### 2. Requests vs Limits

```yaml
resources:
  requests:                # ← Cấp phát ban đầu (đảm bảo)
    cpu: "200m"
    memory: "64Mi"
  limits:                  # ← Tối đa được dùng (chặn)
    cpu: "500m"
    memory: "128Mi"
```

| Field | Ý nghĩa | Use case |
|-------|---------|----------|
| **Requests** | Tối thiểu Pod cần để chạy. Scheduler dùng để chọn Node. | Cấp phát |
| **Limits** | Tối đa Pod được phép dùng. K8s chặn vượt qua. | Bảo vệ |

---

### 3. Đơn Vị

**CPU:**

```
1 CPU = 1 vCPU/Core (vật lý hoặc ảo)
1 CPU = 1000m (millicores)
0.5 CPU = 500m
0.1 CPU = 100m   (thấp nhất phổ biến)
```

**Memory:**

```
Mi (Mebibyte)  = 1024 KiB    ← K8s "thật"
Gi (Gibibyte)  = 1024 MiB    ← Dùng phổ biến

M (Megabyte)   = 1000 KB     ← SI standard
G (Gigabyte)   = 1000 MB
```

> 💡 Trong K8s nên dùng `Mi`, `Gi` để đúng với cách OS đo memory.

---

### 4. Hành Vi Khi Vượt Limit

| Resource | Khi vượt Limit | Hành vi |
|----------|----------------|---------|
| **CPU** | Ứng dụng chạy chậm | **Throttle** — KHÔNG chết, chỉ chậm |
| **Memory** | OOM (Out Of Memory) | **Pod bị Kill + Restart** |

**CPU Throttle:**

```
Đường (CPU) có 1000m
Quá nhiều xe (request) → Slow, không tắc, không sập
```

**Memory OOM:**

```
RAM cấp phát: 128Mi
App dùng: 130Mi (vượt!)
→ Linux kernel KILL container
→ K8s restart container (CrashLoopBackOff nếu lặp lại)
```

---

### 5. YAML Đầy Đủ

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: log
      image: busybox
      # Container này không có resources
    - name: app
      image: hieuvu/simple-app:v1
      resources:
        requests:
          cpu: "200m"        # 0.2 CPU
          memory: "64Mi"     # 64 MiB
        limits:
          cpu: "500m"        # 0.5 CPU
          memory: "128Mi"    # 128 MiB
```

> 💡 Mỗi **container trong Pod** có resources riêng.

---

### 6. Verify Resource Trên Node

```bash
kubectl describe node minikube
# Output:
# Allocated resources:
#   Resource           Requests      Limits
#   --------           --------      ------
#   cpu                950m (47%)    1500m (75%)
#   memory             234Mi (12%)   298Mi (15%)
```

→ Hiển thị **tổng request/limit** của tất cả Pod đang chạy trên Node.

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo Pod KHÔNG có resources
kubectl run pod-no-limit --image=nginx:1.24

# Kiểm tra Node
kubectl describe node minikube | grep -A 8 "Allocated resources"

# 2. Tạo Pod CÓ resources
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-limit
spec:
  containers:
    - name: nginx
      image: nginx:1.24
      resources:
        requests:
          cpu: "200m"
          memory: "64Mi"
        limits:
          cpu: "500m"
          memory: "128Mi"
EOF

# 3. Kiểm tra lại Node — sẽ thấy số tăng lên
kubectl describe node minikube | grep -A 8 "Allocated resources"

# 4. Cleanup
kubectl delete pod pod-no-limit pod-with-limit
```

---

## ⚠️ Lưu Ý

- 🔥 **Memory vượt limit = chết** (OOM). Cẩn thận!
- 🔥 **CPU vượt limit = chậm** (throttle), không chết
- 💡 Nếu **chỉ định Limit mà không có Requests** → Requests = Limits
- ⚠️ Requests **quá thấp** → Scheduler đặt nhiều Pod lên 1 Node → bottleneck
- ⚠️ Requests **quá cao** → Lãng phí, ít Pod fit được vào cluster

---

## ✅ Self-Check

1. **Khác biệt giữa Requests và Limits?**
   <details>
   <summary>Đáp án</summary>
   - **Requests:** Tối thiểu để chạy, dùng cho Scheduler
   - **Limits:** Tối đa, dùng để chặn
   </details>

2. **Pod vượt Memory limit thì sao?**
   <details>
   <summary>Đáp án</summary>
   **OOMKilled** — container bị Linux kernel kill, K8s restart Pod.
   </details>

3. **Pod vượt CPU limit thì sao?**
   <details>
   <summary>Đáp án</summary>
   **Throttle** — chậm, nhưng vẫn chạy. Không bị kill.
   </details>

4. **`200m` CPU là gì?**
   <details>
   <summary>Đáp án</summary>
   200 millicores = 0.2 CPU = 1/5 của 1 core.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Module 09 — Namespace](../09-namespace/README.md)
- ➡️ [Bài #36 — Best Practices Requests & Limits](02-best-practices-requests-limits.md)

### Tài Nguyên

- 📖 [Resource Management for Pods](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
