# Bài #19 — Edit ReplicaSet & Giới Thiệu Deployment

> 🎯 **Bước ngoặt:** Hiểu **giới hạn của ReplicaSet** → vì sao production cần **Deployment** thay thế.

---

## 📋 Metadata

- **Bài số:** #19
- **Module:** 06-replicaset
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~4 phút
- **Prerequisites:** [Bài #18 — Expose RS Declarative](04-expose-replicaset-declarative.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Edit ReplicaSet bằng `kubectl edit`
- [ ] Hiểu **vấn đề:** RS không tự cập nhật Pod khi đổi image
- [ ] Biết **workaround thủ công** (xóa Pod cũ)
- [ ] Hiểu **vì sao cần Deployment** (rolling update, rollback...)

---

## 📚 Nội Dung

### 1. Edit ReplicaSet Bằng `kubectl edit`

```bash
kubectl edit rs <rs-name>
# Mở vim/nano editor với manifest đầy đủ
# Sửa replicas, image, label... rồi save
```

### 2. Test 1: Đổi Replicas

```bash
kubectl edit rs rs3
# Sửa: replicas: 3 → replicas: 4
# :wq save
```

→ RS tự **tạo thêm 1 Pod** để đạt 4. Hoạt động đúng! ✅

### 3. Test 2: Đổi Image — VẤN ĐỀ

```bash
kubectl edit rs rs3
# Sửa: image: nginx:1.24 → image: nginx:1.25
# :wq save
```

→ RS **KHÔNG tạo Pod mới với image mới!** Pod cũ vẫn chạy version cũ! ❌

```bash
kubectl get pods
# rs3-abc12   1/1   Running   (image: nginx:1.24 — CŨ)
# rs3-def34   1/1   Running   (image: nginx:1.24 — CŨ)
# rs3-ghi56   1/1   Running   (image: nginx:1.24 — CŨ)
```

#### Vì sao?

```
RS chỉ làm 2 việc:
1. Đếm Pod match selector
2. Nếu thiếu → tạo từ template

RS KHÔNG check: "Pod hiện tại có giống template không?"
   → Pod cũ vẫn match selector → vẫn được đếm → RS không làm gì
```

→ **Đây là điểm yếu nghiêm trọng của RS** cho production.

---

### 4. Workaround Thủ Công

```bash
# Xóa từng Pod cũ
kubectl delete pod rs3-abc12 rs3-def34 rs3-ghi56

# RS tự tạo Pod mới (với image mới từ template)
kubectl get pods -w
# rs3-XYZ99   ContainerCreating   ← image mới
# rs3-XYZ99   Running
# rs3-MNO88   Running
# rs3-PQR77   Running
```

→ Hơi vô lý, vì:
- Phải xóa thủ công → không tự động
- Tất cả Pod xóa cùng lúc → **DOWNTIME** ❌
- Không có rollback nếu image mới bị bug

---

### 5. Giải Pháp: Deployment (Module 07)

**Deployment** = wrapper cao cấp hơn ReplicaSet, có:

| Feature                            | ReplicaSet | Deployment |
| ---------------------------------- | ---------- | ---------- |
| Self-healing                       | ✅          | ✅          |
| Scaling                            | ✅          | ✅          |
| **Rolling Update** (zero-downtime) | ❌          | ✅          |
| **Rollback** (back về version cũ)  | ❌          | ✅          |
| **Pause/Resume**                   | ❌          | ✅          |
| **Revision History**               | ❌          | ✅          |

```
┌─────────── Deployment ─────────────┐
│  ┌────── ReplicaSet v1 ────────┐   │
│  │  Pod, Pod, Pod (image v1)   │   │
│  └─────────────────────────────┘   │
│                ↓                    │
│  ┌────── ReplicaSet v2 ────────┐   │
│  │  Pod, Pod, Pod (image v2)   │   │
│  └─────────────────────────────┘   │
└────────────────────────────────────┘

Deployment quản lý NHIỀU ReplicaSet
→ Rolling update: từ từ chuyển traffic v1 → v2
→ Rollback: switch về RS v1 ngay lập tức
```

> 🎓 **Production thực tế: 99% case dùng Deployment, không dùng RS trực tiếp.**

---

## 💻 Hands-On / Demo

```bash
# Setup
kubectl apply -f rs3.yaml

# Edit replicas (hoạt động tốt)
kubectl edit rs rs3
# Sửa replicas: 3 → 4

# Verify
kubectl get rs
# rs3   4 Desired   4 Current

# ===== VẤN ĐỀ: ĐỔI IMAGE =====
kubectl edit rs rs3
# Sửa image: nginx:1.24-alpine → nginx:1.25-alpine

# Watch
kubectl get pods -w
# Vẫn 4 Pod cũ chạy nginx:1.24!  ❌

# Workaround: xóa Pod cũ
kubectl delete pod rs3-abc12

# Verify Pod mới có image mới
kubectl describe pod $(kubectl get pods -l app=app3 -o name | head -n 1) | grep Image
# Image: nginx:1.25-alpine  ✅

# Cleanup
kubectl delete rs rs3
```

---

## ⚠️ Lưu Ý

- 🔥 RS chỉ self-heal về **số lượng**, không **đồng bộ** Pod hiện tại với template mới
- 🔥 Update image trên RS = **không có hiệu lực** ngay (Pod cũ vẫn chạy)
- 🔥 Workaround xóa thủ công → **DOWNTIME**, **không có rollback**
- ✅ **Production:** dùng Deployment thay RS — toàn bộ Module 07 sẽ học sâu

---

## ✅ Self-Check

1. **Edit `replicas` trên RS có hoạt động ngay không?**
   <details>
   <summary>Đáp án</summary>
   **Có** — RS tự scale lên/xuống.
   </details>

2. **Edit `image` trên RS có cập nhật Pod không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG** — Pod cũ vẫn chạy image cũ. Phải xóa Pod thủ công.
   </details>

3. **Vì sao RS không cập nhật Pod khi đổi template?**
   <details>
   <summary>Đáp án</summary>
   RS chỉ check **số lượng** Pod match selector, không check **template**. Pod cũ vẫn match selector → RS không làm gì.
   </details>

4. **Production nên dùng RS hay Deployment?**
   <details>
   <summary>Đáp án</summary>
   **Deployment** — có rolling update, rollback, revision history.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #18 — Expose RS Declarative](04-expose-replicaset-declarative.md)
- ➡️ [Bài #20 — Create Deployment](../07-deployment/01-create-deployment.md)

### Tài Nguyên

- 📖 [Why Deployment over ReplicaSet?](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- 📺 Video gốc: `Decopy_✅ #19 Edit ReplicaSet và Giới Thiệu Deployment..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Đối với hình thức này (RS), khi thay đổi image hay version mới, mình phải làm KHÁ THỦ CÔNG — không hỗ trợ tối ưu."*

> 💬 *"Vậy thì để rollout, rollback, pause, resume... chúng ta sẽ dùng object khác — gọi là **Deployment**."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
