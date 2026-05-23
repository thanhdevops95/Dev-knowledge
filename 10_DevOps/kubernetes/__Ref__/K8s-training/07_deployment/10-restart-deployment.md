# Bài #29 — Restart Deployment

> 🎯 Restart toàn bộ Pod của Deployment — không cần đổi image.

---

## 📋 Metadata

- **Bài số:** #29
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~3 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Sử dụng `kubectl rollout restart`
- [ ] Hiểu cơ chế: tạo RS mới mặc dù không đổi template
- [ ] Use cases khi nên restart

---

## 📚 Nội Dung

### 1. Lệnh Restart

```bash
kubectl rollout restart deployment/<name>
```

**Cơ chế:**

- Tạo **RS mới** (cùng image, cùng config)
- RS mới scale up → RS cũ scale down
- Tuân theo `strategy` (RollingUpdate/Recreate)

---

### 2. Khi Nào Cần Restart?

✅ **Use cases hợp lý:**

- 🔄 Pod load **ConfigMap/Secret** mới (sau khi update ConfigMap)
- 🐛 Container bị "treo" mà không crash (memory leak)
- 🔑 Cần **rotate** credentials, certs trong env
- 🧪 Test resilience của hệ thống

❌ **Use cases nên tránh:**

- Không nên dùng `restart` để "force update" → nên dùng `set image` rõ ràng

---

### 3. Demo

```bash
# Setup
kubectl create deployment app1-deploy \
  --image=nginx:1.24-alpine --replicas=10

# Xem RS hiện tại
kubectl get rs
# NAME                    DESIRED  CURRENT  READY  AGE
# app1-deploy-7c5xxx      10       10       10     1m

# Restart
kubectl rollout restart deployment/app1-deploy
# deployment.apps/app1-deploy restarted

# Theo dõi
kubectl get pods -w
# Sẽ thấy Pod mới được tạo, Pod cũ bị terminate

kubectl get rs
# NAME                    DESIRED  CURRENT  READY  AGE
# app1-deploy-7c5xxx      0        0        0      2m   ← cũ
# app1-deploy-d5fxxx      10       10       10     30s  ← mới (RS mới!)

# Xem rollout history
kubectl rollout history deployment/app1-deploy
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>     ← do restart
```

---

### 4. Restart Tuân Theo Strategy

**RollingUpdate (default):**

```bash
kubectl rollout restart deployment/app1
# Pod mới tạo → Ready → xóa Pod cũ (no down-time)
```

**Recreate:**

```bash
# Sau khi đổi sang Recreate
kubectl rollout restart deployment/app1
# TẤT CẢ Pod cũ bị xóa → tạo mới (CÓ down-time)
```

---

### 5. So Sánh: Restart vs Set Image

| Tình huống | Restart | Set image |
|------------|---------|-----------|
| Image không đổi | ✅ Tạo RS mới (chỉ khác hash) | ❌ Không có thay đổi → không làm gì |
| Image đổi | — | ✅ Tạo RS mới với image mới |
| Audit/tracking | RS mới (revision) | RS mới (revision) |

> 💡 **Restart cũng tạo revision** — có thể rollback bằng `kubectl rollout undo`!

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo deployment
kubectl create deployment demo --image=nginx:1.24 --replicas=5

# 2. Giả lập update ConfigMap (mock)
kubectl rollout restart deployment/demo

# 3. Theo dõi
kubectl rollout status deployment/demo
kubectl get rs

# 4. Kiểm tra Pod đã có age mới
kubectl get pods

# 5. Cleanup
kubectl delete deployment demo
```

---

## ⚠️ Lưu Ý

- 🔥 **Restart KHÔNG đổi image** — image vẫn như cũ, chỉ thay đổi metadata trong template
- 💡 K8s thêm annotation `kubectl.kubernetes.io/restartedAt` vào template → trigger RS mới
- ⚠️ Nếu app không **graceful shutdown** → có thể mất request đang xử lý

---

## ✅ Self-Check

1. **`kubectl rollout restart` có đổi image không?**
   <details>
   <summary>Đáp án</summary>
   **Không**. Image giữ nguyên. K8s chỉ thêm annotation `restartedAt` vào template để trigger RS mới.
   </details>

2. **Khi nào nên dùng restart?**
   <details>
   <summary>Đáp án</summary>
   - Sau khi update ConfigMap/Secret để Pod load lại
   - Container bị treo
   - Cần rotate certs/credentials
   </details>

3. **Restart có thể rollback được không?**
   <details>
   <summary>Đáp án</summary>
   **Có**. Vì restart cũng tạo revision mới → `kubectl rollout undo` để quay về RS cũ.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #28 — Progress Deadline](09-progress-deadline.md)
- ➡️ [Module 08 — Services](../08-services/README.md)

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Restart Deployment vẫn tạo ReplicaSet mới và track lại cho chúng ta — Deployment là một technique rất hay để audit lại những thứ chúng ta đã làm."*

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
