# Bài #25 — Pause & Resume Deployment

> 🎯 Tạm dừng/tiếp tục rollout — **gom nhiều thay đổi thành 1 revision**.

---

## 📋 Metadata

- **Bài số:** #25
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~5 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Pause Deployment để dừng rollout
- [ ] Thay đổi nhiều thuộc tính trong khi pause
- [ ] Resume → áp dụng tất cả thay đổi 1 lần (1 revision)

---

## 📚 Nội Dung

### 1. Khi Nào Cần Pause?

**Vấn đề:** Mỗi `kubectl set image`, `kubectl set env`, `kubectl edit` đều **tạo 1 revision mới**.

```
Không pause:
set image v1 → v2  → revision 2
set env DB=...     → revision 3
set resources ...  → revision 4
                     (3 lần rollout!)
```

**Giải pháp: Pause → tất cả thay đổi → Resume**

```
pause
  set image v1 → v2
  set env DB=...
  set resources ...
resume                → revision 2 (1 lần rollout!)
```

---

### 2. Lệnh Pause / Resume

```bash
# Pause
kubectl rollout pause deployment/<name>

# Resume
kubectl rollout resume deployment/<name>
```

---

### 3. Demo Đầy Đủ

```bash
# Setup
kubectl create deployment app1 \
  --image=nginx:1.22-alpine --replicas=5

# Pause
kubectl rollout pause deployment/app1

# Đổi image — KHÔNG kích hoạt rollout
kubectl set image deployment/app1 \
  nginx=nginx:1.23-alpine

# Đổi resources — KHÔNG kích hoạt rollout
kubectl set resources deployment/app1 \
  -c=nginx --limits=cpu=200m,memory=128Mi

# Verify: pods vẫn chạy v1.22 (chưa rollout)
kubectl get pods
kubectl describe deployment app1 | grep Image:
# Image: nginx:1.23-alpine    ← spec đã đổi
# Nhưng pods vẫn chạy v1.22

# Resume → tất cả thay đổi áp dụng 1 lần
kubectl rollout resume deployment/app1
kubectl rollout status deployment/app1
# deployment "app1" successfully rolled out

# Xem history — chỉ 2 revision (1 ban đầu, 1 sau resume)
kubectl rollout history deployment/app1
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>
```

---

### 4. So Sánh: Pause vs Không Pause

| Hành động | Không Pause | Có Pause |
|-----------|-------------|----------|
| Đổi 3 thứ | **3 revisions** | **1 revision** |
| Số lần Pod restart | 3 lần | 1 lần |
| Down-time | Nhiều | Ít |
| History sạch | Không | ✅ |

---

## 💻 Hands-On / Demo

```bash
# 1. Pause
kubectl rollout pause deployment/app1

# 2. Thay đổi nhiều thứ
kubectl set image deployment/app1 nginx=nginx:1.24
kubectl set env deployment/app1 DB_HOST=db.example.com
kubectl scale deployment/app1 --replicas=10

# 3. Resume
kubectl rollout resume deployment/app1

# 4. Theo dõi
kubectl rollout status deployment/app1
```

---

## ⚠️ Lưu Ý

- 🔥 **Trong khi pause:** rollback **không hoạt động**
- 💡 **Use case:** chuẩn bị nhiều thay đổi rồi áp dụng cùng lúc
- ⚠️ Đừng quên `resume` — không thì Pod sẽ **kẹt** ở phiên bản cũ

---

## ✅ Self-Check

1. **Pause Deployment có nghĩa là gì?**
   <details>
   <summary>Đáp án</summary>
   Tạm dừng controller xử lý các thay đổi → các thay đổi không được rollout cho đến khi resume.
   </details>

2. **Tại sao nên pause khi update nhiều thuộc tính?**
   <details>
   <summary>Đáp án</summary>
   Để gom thành **1 rollout = 1 revision** thay vì N rollouts. Giảm restart Pod, sạch history.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #24 — Rollback Deployment](05-rollback-deployment.md)
- ➡️ [Bài #26 — Change Cause](07-change-cause.md)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
