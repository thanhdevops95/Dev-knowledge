# Bài #26 — Change Cause (Mô Tả Cho Mỗi Revision)

> 🎯 Thêm "ghi chú" cho mỗi revision để biết **TẠI SAO** thay đổi.

---

## 📋 Metadata

- **Bài số:** #26
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~4 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu khái niệm `kubernetes.io/change-cause` annotation
- [ ] Thêm change-cause khi rollout (imperative)
- [ ] Thêm change-cause vào YAML (declarative)

---

## 📚 Nội Dung

### 1. Vấn Đề: History Không Có Mô Tả

```bash
kubectl rollout history deployment/app1
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>
# 3         <none>
# 4         <none>
```

→ **Không biết** revision nào làm gì! Phải `--revision=N` xem từng cái.

---

### 2. Giải Pháp: Annotation `kubernetes.io/change-cause`

Annotation này được K8s **tự động** đọc và hiển thị trong `rollout history`.

---

### 3. Cách 1: Imperative — `kubectl annotate`

```bash
kubectl annotate deployment/<name> \
  kubernetes.io/change-cause="<mô tả>" \
  --overwrite
```

**Ví dụ:**

```bash
# Update image
kubectl set image deployment/app1 nginx=nginx:1.23

# Annotate ngay sau đó
kubectl annotate deployment/app1 \
  kubernetes.io/change-cause="Update nginx to v1.23 — security fix CVE-2026-1234" \
  --overwrite

kubectl rollout history deployment/app1
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         Update nginx to v1.23 — security fix CVE-2026-1234
```

> 💡 `--overwrite` để ghi đè annotation cũ.

---

### 4. Cách 2: Declarative — YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-deploy
  annotations:
    kubernetes.io/change-cause: "Update nginx to v1.24 — performance improvement"
spec:
  replicas: 5
  # ...
```

```bash
kubectl apply -f deployment.yaml
```

---

### 5. Demo Đầy Đủ

```bash
# Tạo deployment v1
kubectl create deployment app1 \
  --image=nginx:1.22 --replicas=3
kubectl annotate deployment/app1 \
  kubernetes.io/change-cause="Initial deployment v1.22"

# Update v2
kubectl set image deployment/app1 nginx=nginx:1.23
kubectl annotate deployment/app1 \
  kubernetes.io/change-cause="Bump to v1.23 - bugfix #1234" \
  --overwrite

# Update v3
kubectl set image deployment/app1 nginx=nginx:1.24
kubectl annotate deployment/app1 \
  kubernetes.io/change-cause="Bump to v1.24 - new feature XYZ" \
  --overwrite

# Xem history với mô tả đầy đủ
kubectl rollout history deployment/app1
# REVISION  CHANGE-CAUSE
# 1         Initial deployment v1.22
# 2         Bump to v1.23 - bugfix #1234
# 3         Bump to v1.24 - new feature XYZ
```

---

## 💻 Hands-On / Demo

Như mục 5 ở trên — copy/paste để chạy.

---

## ⚠️ Lưu Ý

- 🔥 Phải có `--overwrite` nếu annotation đã tồn tại
- 💡 **Best practice:** mỗi PR/release → 1 change-cause với link Jira/PR
- ⚠️ Annotation **không tự động cập nhật** — phải `annotate` thủ công sau mỗi update
- ✅ Trong CI/CD: tự động set change-cause = commit message hoặc PR title

---

## ✅ Self-Check

1. **Annotation nào dùng cho change-cause?**
   <details>
   <summary>Đáp án</summary>
   `kubernetes.io/change-cause`
   </details>

2. **Tại sao cần `--overwrite`?**
   <details>
   <summary>Đáp án</summary>
   Vì annotation đã tồn tại từ lần trước, mặc định `kubectl annotate` không ghi đè.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #25 — Pause & Resume](06-pause-resume.md)
- ➡️ [Bài #27 — Recreate vs RollingUpdate](08-deployment-strategies.md)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
