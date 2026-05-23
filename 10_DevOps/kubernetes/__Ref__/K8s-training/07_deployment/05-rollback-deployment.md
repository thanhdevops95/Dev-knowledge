# Bài #24 — Rollback Deployment (Quay Về Phiên Bản Cũ)

> 🎯 Một trong những **siêu năng lực** lớn nhất của K8s Deployment.

---

## 📋 Metadata

- **Bài số:** #24
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~5 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu cơ chế rollback của K8s
- [ ] Rollback về **revision trước** bằng `kubectl rollout undo`
- [ ] Rollback về **revision cụ thể**
- [ ] Hiểu rollback cũng tạo **revision mới**

---

## 📚 Nội Dung

### 1. Tại Sao K8s Có Thể Rollback?

```
Deployment giữ nhiều ReplicaSet (mặc định 10)
├─ RS hash=abc (image: v1)   ← revision 1
├─ RS hash=def (image: v2)   ← revision 2
└─ RS hash=ghi (image: v3)   ← revision 3 (CURRENT)
```

→ Khi rollback: K8s **scale RS cũ lên** + **scale RS hiện tại xuống 0**.

---

### 2. Lệnh Rollback

**Rollback về revision trước (revision N-1):**

```bash
kubectl rollout undo deployment/<name>
```

**Rollback về revision cụ thể:**

```bash
kubectl rollout undo deployment/<name> --to-revision=2
```

---

### 3. Demo Đầy Đủ

```bash
# Setup: tạo deployment v1
kubectl create deployment app1-deploy \
  --image=hieuvu/simple-app:v1 --replicas=5

# Update lên v2
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v2
kubectl rollout status deployment/app1-deploy

# Update lên v3
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v3
kubectl rollout status deployment/app1-deploy

# Xem lịch sử
kubectl rollout history deployment/app1-deploy
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>
# 3         <none>

# 🔥 Rollback về revision trước (= revision 2)
kubectl rollout undo deployment/app1-deploy

kubectl rollout history deployment/app1-deploy
# REVISION  CHANGE-CAUSE
# 1         <none>
# 3         <none>     ← bị "đẩy" sang revision mới
# 4         <none>     ← rollback tạo revision mới = template của revision 2

# Rollback về revision 1 (về v1 ban đầu)
kubectl rollout undo deployment/app1-deploy --to-revision=1

kubectl rollout history deployment/app1-deploy
# REVISION  CHANGE-CAUSE
# 3         <none>
# 4         <none>
# 5         <none>     ← rollback tạo revision 5 = template của revision 1
```

---

### 4. Quan Trọng: Rollback **Tạo Revision Mới**

```
Trạng thái:                 History:
v1 → v2 → v3                rev1, rev2, rev3
↓ rollback to rev2
v1 → v2 → v3 → v2'          rev1, rev3, rev4 (rev2 thành rev4)
                            (rev2 cũ bị xóa, thay bằng rev4)
```

→ **Revision không bao giờ bị "ghi đè"** — chỉ thêm mới vào lịch sử.

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo + update 2 lần
kubectl create deployment demo --image=nginx:1.22-alpine --replicas=3
kubectl set image deployment/demo nginx=nginx:1.23-alpine
kubectl set image deployment/demo nginx=nginx:1.24-alpine

# 2. Xem history
kubectl rollout history deployment/demo

# 3. Rollback
kubectl rollout undo deployment/demo

# 4. Verify image hiện tại
kubectl describe deployment demo | grep Image:

# 5. Cleanup
kubectl delete deployment demo
```

---

## ⚠️ Lưu Ý

- 🔥 Rollback chỉ hoạt động khi RS cũ **vẫn còn trong history**
- ⚠️ `revisionHistoryLimit` (default 10) — nếu rollback về quá xa → KHÔNG được
- 💡 **Best practice:** rollback chỉ là biện pháp tạm thời. Sau đó, sửa code → deploy version mới
- 🔥 Rollback **không thể** quay về version chưa từng deploy

---

## ✅ Self-Check

1. **Lệnh rollback về revision trước?**
   <details>
   <summary>Đáp án</summary>
   `kubectl rollout undo deployment/<name>`
   </details>

2. **Rollback có làm mất các revision sau không?**
   <details>
   <summary>Đáp án</summary>
   **Không**. Rollback **tạo revision mới** với template của revision đích, các revision khác vẫn giữ nguyên.
   </details>

3. **Có thể rollback về revision đã bị "đẩy" ra khỏi history không?**
   <details>
   <summary>Đáp án</summary>
   **Không**. Chỉ rollback được revision còn trong `revisionHistoryLimit`.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #23 — Rollout Deployment](04-rollout-deployment.md)
- ➡️ [Bài #25 — Pause & Resume Deployment](06-pause-resume.md)

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Đây là một trong những lý do chính khiến mọi người thích Kubernetes — rollback chỉ 1 lệnh."*

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
