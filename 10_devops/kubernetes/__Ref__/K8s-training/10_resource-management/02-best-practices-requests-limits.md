# Bài #36 — Best Practices: Requests & Limits

> 🎯 Recommendation từ thực tế production để cấu hình đúng CPU/Memory.

---

## 📋 Metadata

- **Bài số:** #36
- **Module:** 10-resource-management
- **Cấp độ:** `ADVANCED`
- **Thời lượng video gốc:** ~10 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **3 rule vàng** cho CPU/Memory
- [ ] Phân tích trade-off của 2 cách giải quyết
- [ ] Hiểu cơ chế CPU compressible vs Memory non-compressible
- [ ] Áp dụng best practices vào YAML

---

## 📚 Nội Dung

### 1. Tình Huống Thực Tế

**Cấu hình:** Node có 1 CPU (1000m), 4 GB RAM. 2 Pod chạy:

```yaml
# Pod A
resources:
  requests:
    cpu: "500m"
  # KHÔNG có limit

# Pod B
resources:
  requests:
    cpu: "50m"      # ← Quá thấp!
  # KHÔNG có limit
```

**Vấn đề:** Pod A có bug → ăn dần CPU lên 800m. Pod B chỉ request 50m → khi Pod B cần 700m → bị throttle nghiêm trọng.

---

### 2. Hai Cách Giải Quyết

**Cách 1 (SAI):** Đặt CPU Limit cho Pod A.

```yaml
# Pod A
resources:
  requests:
    cpu: "500m"
  limits:
    cpu: "700m"   # ← Limit
```

**Vấn đề:** Pod B vẫn bị thiếu CPU nếu Pod A "ăn" 700m. Không giải quyết gốc.

**Cách 2 (ĐÚNG):** Tăng Requests cho Pod B.

```yaml
# Pod B
resources:
  requests:
    cpu: "700m"   # ← Tăng request
  # KHÔNG có limit
```

→ Scheduler **đảm bảo** Pod B luôn có 700m CPU.

---

### 3. Tại Sao CPU KHÔNG Nên Set Limit?

**CPU = Compressible Resource** — có thể "lấy lại":

```
Pod ăn CPU lên 800m
Sau khi xong việc → trả về 300m
                  → trả về 100m   ← OS tự lấy lại
```

→ Pod **trả CPU** khi không dùng. **Không cần Limit để bảo vệ**.

**Đặt CPU Limit có hại:**

- ❌ Lãng phí CPU dư của Node
- ❌ Bị throttle vô lý
- ❌ Slow ứng dụng không cần thiết

> 🔥 **Rule #1: KHÔNG set CPU Limit (hoặc set rất cao).**

---

### 4. Tại Sao Memory NÊN Set Limit = Request?

**Memory = Non-compressible Resource** — không trả lại:

```
Pod ăn RAM lên 500Mi
Ứng dụng không dùng nữa → Pod VẪN giữ 500Mi (không trả về)
```

→ Cần **Limit** để chặn Pod ăn vô tận.

**Best practice:** `requests.memory == limits.memory`

```yaml
resources:
  requests:
    memory: "256Mi"
  limits:
    memory: "256Mi"   # ← Bằng nhau
```

**Lý do:**

- ✅ Đảm bảo predictable behavior
- ✅ Pod được Guaranteed QoS class (priority cao nhất)
- ✅ Tránh OOM bất ngờ khi Node thiếu RAM

> 🔥 **Rule #2: Memory request = Memory limit.**

---

### 5. Rule Tổng Hợp (3 Quy Tắc)

| # | Rule | Lý do |
|---|------|-------|
| 1 | **KHÔNG set CPU Limit** | CPU compressible — auto-recover |
| 2 | **LUÔN set CPU Request** | Đảm bảo Pod có CPU tối thiểu |
| 3 | **Memory: Request = Limit** | Tránh OOM bất ngờ + Guaranteed QoS |

---

### 6. Bonus: QoS Classes

K8s phân loại Pod thành 3 QoS dựa trên resources:

| QoS | Điều kiện | Ưu tiên khi Node hết RAM |
|-----|-----------|--------------------------|
| **Guaranteed** | Mọi container có request = limit cho cả CPU + RAM | Cao nhất — không bị evict |
| **Burstable** | Có request hoặc limit nhưng không bằng nhau | Trung bình |
| **BestEffort** | KHÔNG có request lẫn limit | Thấp nhất — bị evict trước |

> 💡 Production critical → **Guaranteed**.

---

### 7. YAML Mẫu Theo Best Practice

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: production-app
spec:
  containers:
    - name: app
      image: my-app:v1
      resources:
        requests:
          cpu: "250m"      # Set CPU request
          memory: "256Mi"
        limits:
          # cpu: KHÔNG SET (hoặc set rất cao)
          memory: "256Mi"  # Memory limit = request
```

---

## ⚠️ Lưu Ý

- 🔥 Đừng set CPU/Memory **quá thấp** → Scheduler có thể evict Pod khi Node thiếu
- 💡 Monitor thực tế (Metrics Server, Prometheus) → tinh chỉnh số liệu
- ⚠️ Mỗi **microservice cần tinh chỉnh riêng** — không có "one size fits all"
- ✅ Bắt đầu với **estimate** + **monitor** + **adjust**

---

## ✅ Self-Check

1. **Tại sao KHÔNG nên set CPU Limit?**
   <details>
   <summary>Đáp án</summary>
   CPU là compressible — Pod tự trả CPU khi không dùng. Set Limit chỉ làm Pod bị throttle vô lý mà không bảo vệ gì.
   </details>

2. **Tại sao Memory request = limit?**
   <details>
   <summary>Đáp án</summary>
   - Memory không trả lại sau khi cấp
   - Set bằng nhau → Pod được QoS Guaranteed
   - Tránh OOM bất ngờ
   </details>

3. **3 QoS class của Pod là gì?**
   <details>
   <summary>Đáp án</summary>
   - **Guaranteed** (request = limit cho cả CPU + RAM)
   - **Burstable** (có set nhưng không bằng nhau)
   - **BestEffort** (không set gì)
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #35 — Requests & Limits](01-requests-limits.md)
- ➡️ [Bài #37 — Command & Args](03-command-args.md)

### Tài Nguyên

- 📖 [QoS Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)
- 📖 [Resource Best Practices](https://kubernetes.io/docs/setup/best-practices/cluster-large/)

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Rule số 1 cho tất cả các hệ thống: ĐỪNG set CPU Limit. CPU có tính chất giãn nở, Pod cần nhiều thì nó lấy, không dùng nữa thì trả lại."*

> 💬 *"Memory thì lại không có tính chất đó — đã ăn là không trả. Cho nên memory phải set cẩn thận."*

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
