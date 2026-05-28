# Bài #23 — Rollout Deployment (Theo Dõi Triển Khai)

> 🎯 Theo dõi quá trình rollout (cập nhật) của Deployment.

---

## 📋 Metadata

- **Bài số:** #23
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~6 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Sử dụng `kubectl rollout status` để theo dõi
- [ ] Sử dụng `kubectl rollout history` để xem lịch sử
- [ ] Hiểu khái niệm **Revision**

---

## 📚 Nội Dung

### 1. Mỗi Rollout Tạo 1 Revision

Mỗi lần update Deployment (đổi image, đổi env, đổi labels...) → tạo **revision mới**.

```
Deployment app1-deploy
├─ Revision 1   → ReplicaSet abc (image: v1)
├─ Revision 2   → ReplicaSet def (image: v2)  ← UPDATE
├─ Revision 3   → ReplicaSet ghi (image: v3)  ← UPDATE
└─ Revision 4   → ReplicaSet jkl (image: v4)  ← CURRENT
```

---

### 2. Lệnh Rollout Quan Trọng

```bash
# Theo dõi rollout đang chạy (block đến khi xong)
kubectl rollout status deployment/<name>

# Xem lịch sử rollout
kubectl rollout history deployment/<name>

# Xem chi tiết 1 revision
kubectl rollout history deployment/<name> --revision=2

# Restart deployment (terminate và tạo lại Pod)
kubectl rollout restart deployment/<name>

# Pause rollout
kubectl rollout pause deployment/<name>

# Resume rollout
kubectl rollout resume deployment/<name>

# Undo (rollback) về revision trước
kubectl rollout undo deployment/<name>

# Undo về revision cụ thể
kubectl rollout undo deployment/<name> --to-revision=2
```

---

### 3. Demo: Theo Dõi Rollout

```bash
# Setup
kubectl create deployment app1-deploy \
  --image=hieuvu/simple-app:v1 --replicas=10

kubectl scale deployment app1-deploy --replicas=10

# Cập nhật image
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v2

# Theo dõi
kubectl rollout status deployment/app1-deploy

# Output:
# Waiting for deployment "app1-deploy" rollout to finish: 2 of 10 updated replicas...
# Waiting for deployment "app1-deploy" rollout to finish: 5 of 10 updated replicas...
# Waiting for deployment "app1-deploy" rollout to finish: 8 of 10 updated replicas...
# deployment "app1-deploy" successfully rolled out
```

---

### 4. Xem Lịch Sử

```bash
kubectl rollout history deployment/app1-deploy

# Output:
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>
# 3         <none>
```

> ⚠️ `CHANGE-CAUSE` mặc định là `<none>`. Bài #26 sẽ chỉ cách thêm mô tả.

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo deployment
kubectl create deployment app1-deploy \
  --image=hieuvu/simple-app:v1 --replicas=10

# 2. Update + theo dõi
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v2
kubectl rollout status deployment/app1-deploy

# 3. Update lần 2
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v3
kubectl rollout status deployment/app1-deploy

# 4. Xem lịch sử
kubectl rollout history deployment/app1-deploy

# 5. Xem chi tiết 1 revision
kubectl rollout history deployment/app1-deploy --revision=2

# 6. Xem RS tương ứng
kubectl get rs
```

---

## ⚠️ Lưu Ý

- 💡 Số revision lưu giữ kiểm soát bởi `revisionHistoryLimit` (mặc định 10)
- 🔥 `kubectl rollout status` rất hữu ích trong **CI/CD** để chờ deployment xong
- ⚠️ Không nhầm `rollout` (theo dõi) với `rollback` (quay về cũ)

---

## ✅ Self-Check

1. **Lệnh nào để theo dõi rollout đang chạy?**
   <details>
   <summary>Đáp án</summary>
   `kubectl rollout status deployment/<name>`
   </details>

2. **Mỗi update tạo bao nhiêu revision?**
   <details>
   <summary>Đáp án</summary>
   Mỗi update làm thay đổi Pod template → 1 revision mới.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #22 — Set Image](03-set-image.md)
- ➡️ [Bài #24 — Rollback Deployment](05-rollback-deployment.md)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
