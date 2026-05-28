# Bài #40 — Limit Ranges (Giá Trị Mặc Định + Min/Max)

> 🎯 Cấu hình **default + min/max** cho resources trong namespace.

---

## 📋 Metadata

- **Bài số:** #40 (cuối cùng!)
- **Module:** 10-resource-management
- **Cấp độ:** `ADVANCED`
- **Thời lượng video gốc:** ~9 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **LimitRange** vs **ResourceQuota**
- [ ] Đặt giá trị **mặc định** request/limit cho Pod
- [ ] Đặt **min/max** cho mỗi container
- [ ] Combo LimitRange + ResourceQuota = Best practice

---

## 📚 Nội Dung

### 1. Vấn Đề Của ResourceQuota

ResourceQuota **bắt buộc** Pod phải khai báo request/limit. Mỗi Pod, mỗi container đều phải khai báo → **mệt!**

→ **LimitRange** giải quyết: tự động đặt **giá trị mặc định**.

---

### 2. So Sánh: LimitRange vs ResourceQuota

| | ResourceQuota | LimitRange |
|--|---------------|------------|
| **Scope** | Namespace tổng | Mỗi container/Pod |
| **Action** | Giới hạn tổng | Default + min/max |
| **Mục đích** | Giới hạn cluster usage | Đảm bảo từng Pod hợp lý |

> 💡 **Best practice: dùng cả 2.**

---

### 3. LimitRange YAML

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-resource-constraint
  namespace: demo
spec:
  limits:
    - type: Container        # Áp dụng cho mỗi container
      max:
        cpu: "1"             # Tối đa 1 CPU
      min:
        cpu: "100m"          # Tối thiểu 100m
      default:               # Mặc định limit (nếu không khai)
        cpu: "800m"
      defaultRequest:        # Mặc định request (nếu không khai)
        cpu: "500m"
```

---

### 4. Hành Vi Của LimitRange

**Khi tạo Pod KHÔNG khai báo resources:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
  namespace: demo
spec:
  containers:
    - name: app
      image: nginx
      # KHÔNG có resources!
```

→ Sau khi apply, Pod tự có:

```yaml
resources:
  requests:
    cpu: "500m"      # ← Lấy từ defaultRequest
  limits:
    cpu: "800m"      # ← Lấy từ default
```

→ **Tự động** áp dụng!

---

### 5. Demo: 4 Trường Hợp

**LimitRange:**

```yaml
limits:
  - type: Container
    min:    {cpu: "100m"}
    max:    {cpu: "1"}     # 1000m
    default:        {cpu: "800m"}
    defaultRequest: {cpu: "500m"}
```

| Pod | Request | Limit | Kết quả |
|-----|---------|-------|---------|
| **TH1** | (không khai) | (không khai) | ✅ Default: req=500m, lim=800m |
| **TH2** | 300m | 900m | ✅ OK (nằm trong [100m, 1000m]) |
| **TH3** | 1000m | (không khai) | ❌ Lỗi: req=1000m > defaultLimit (800m) |
| **TH4** | 1100m | 1100m | ❌ Lỗi: > max (1000m) |

> 💡 TH3 thú vị: vì không khai limit → lấy default 800m, nhưng request 1000m > limit 800m → conflict.

---

### 6. Demo Đầy Đủ

```bash
# 1. Tạo namespace + LimitRange
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: demo
---
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-constraint
  namespace: demo
spec:
  limits:
    - type: Container
      min: {cpu: "100m"}
      max: {cpu: "1"}
      default: {cpu: "800m"}
      defaultRequest: {cpu: "500m"}
EOF

# 2. Verify
kubectl describe limitrange cpu-constraint -n demo
# Type        Resource  Min   Max  Default Request  Default Limit
# ----        --------  ---   ---  ---------------  -------------
# Container   cpu       100m  1    500m             800m

# 3. TH1: Pod không khai báo
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-no-resources
  namespace: demo
spec:
  containers:
    - name: app
      image: nginx
EOF

# Verify
kubectl describe pod pod-no-resources -n demo | grep -A 5 Limits
# Limits:
#   cpu: 800m    ← lấy từ default
# Requests:
#   cpu: 500m    ← lấy từ defaultRequest

# 4. TH4: Vượt max
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-too-big
  namespace: demo
spec:
  containers:
    - name: app
      image: nginx
      resources:
        limits:
          cpu: "1100m"
EOF
# Error: maximum cpu usage per Container is 1, but limit is 1100m

# 5. Cleanup
kubectl delete ns demo
```

---

### 7. Combo Best Practice: LimitRange + ResourceQuota

```yaml
# 1. ResourceQuota: giới hạn TỔNG namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tier-gold-quota
  namespace: customer-gold
spec:
  hard:
    requests.cpu: "10"
    limits.cpu: "20"
    requests.memory: 20Gi
    limits.memory: 40Gi
    pods: "50"

---
# 2. LimitRange: giới hạn TỪNG Pod
apiVersion: v1
kind: LimitRange
metadata:
  name: tier-gold-limits
  namespace: customer-gold
spec:
  limits:
    - type: Container
      max:
        cpu: "2"          # Pod max 2 CPU
        memory: 4Gi
      min:
        cpu: "100m"
        memory: 64Mi
      default:
        cpu: "500m"       # Auto-fill nếu không khai
        memory: 512Mi
      defaultRequest:
        cpu: "200m"
        memory: 256Mi
```

→ Customer Gold:

- ✅ Không thể vượt 10 CPU tổng
- ✅ Mỗi Pod tối đa 2 CPU
- ✅ Pod không khai báo → auto-fill 200m/500m

---

## ⚠️ Lưu Ý

- 🔥 LimitRange áp dụng **chỉ khi tạo mới Pod** (không retroactive)
- 🔥 Có thể có **nhiều LimitRange** trong 1 namespace (CPU, Memory, PVC...)
- ⚠️ `default` < `min` hoặc `default` > `max` → **Lỗi cấu hình**
- 💡 LimitRange cũng support **PersistentVolumeClaim** (PVC storage)

---

## ✅ Self-Check

1. **LimitRange dùng cho gì?**
   <details>
   <summary>Đáp án</summary>
   - Đặt **default** request/limit (cho Pod không khai báo)
   - Đặt **min/max** cho mỗi container
   </details>

2. **ResourceQuota khác gì LimitRange?**
   <details>
   <summary>Đáp án</summary>
   - **ResourceQuota:** giới hạn TỔNG namespace
   - **LimitRange:** giới hạn TỪNG container/Pod
   </details>

3. **Pod khai request 1000m nhưng không khai limit, LimitRange có default 800m. Tạo được không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG**. Vì limit auto-fill = 800m < request 1000m → conflict.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #39 — Resource Quotas](05-resource-quotas.md)
- ➡️ [Quay về Module 10 README](README.md)
- 🏠 [Quay về trang chính](../README.md)

### Tài Nguyên

- 📖 [LimitRange](https://kubernetes.io/docs/concepts/policy/limit-range/)

---

## 🎉 Hoàn Thành Series!

🎓 **Bạn đã học xong 40 bài về Kubernetes cơ bản!** Bước tiếp theo:

1. ✅ Xem lại [README chính](../README.md) để ôn tổng kết
2. 🚀 Học chuyên sâu: **EKS, Helm, Ingress, ConfigMap/Secret, Probes, StatefulSet**
3. 🎯 Lấy chứng chỉ: **CKAD** (Bài #5)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
