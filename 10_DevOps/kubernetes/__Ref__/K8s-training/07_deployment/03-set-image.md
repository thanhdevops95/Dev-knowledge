# Bài #22 — Set Container Image (Cập Nhật Image)

> 🎯 Cập nhật image của Deployment — bước đầu của **Rolling Update**.

---

## 📋 Metadata

- **Bài số:** #22
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~5 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Cập nhật image bằng `kubectl set image`
- [ ] So sánh: `set image`, `edit deployment`, `apply -f`
- [ ] Hiểu cơ chế Deployment tạo RS mới khi đổi image

---

## 📚 Nội Dung

### 1. Cú Pháp `kubectl set image`

```bash
kubectl set image deployment/<name> \
  <container-name>=<new-image>:<tag>
```

**Ví dụ:**

```bash
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v2

# Kiểm tra
kubectl rollout status deployment/app1-deploy
# Waiting for deployment "app1-deploy" rollout to finish: 2 of 5 updated...
# deployment "app1-deploy" successfully rolled out
```

---

### 2. Tại Sao Đổi Image Lại Tạo RS Mới?

```
TRƯỚC khi đổi image:
┌─ Deployment app1-deploy ────────────┐
│  ┌─ RS hash=abc (image: v1) ────┐    │
│  │  Pod1, Pod2, Pod3            │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘

SAU khi đổi image v1 → v2:
┌─ Deployment app1-deploy ────────────┐
│  ┌─ RS hash=abc (image: v1) ────┐    │
│  │  replicas: 0  ← scale xuống  │    │
│  └──────────────────────────────┘    │
│  ┌─ RS hash=xyz (image: v2) ────┐    │ ← TẠO MỚI
│  │  Pod4, Pod5, Pod6            │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

→ **Hash của RS được tính từ Pod template.** Đổi image = đổi template = RS mới.

> 💡 RS cũ **không bị xóa** → có thể rollback.

---

### 3. So Sánh 3 Cách Cập Nhật Image

| Cách | Lệnh | Ưu | Nhược |
|------|------|----|----|
| **set image** | `kubectl set image deploy/app c=img:v2` | Nhanh, 1 dòng | Imperative, không lưu lại |
| **edit deployment** | `kubectl edit deploy app` | Trực quan | Dễ sai cú pháp YAML |
| **apply -f** | Sửa YAML rồi `kubectl apply -f` | Declarative ✅ | Nhiều bước hơn |

> ✅ **Production:** dùng cách 3 (Declarative) + commit Git.

---

## 💻 Hands-On / Demo

```bash
# Setup
kubectl create deployment app1-deploy \
  --image=hieuvu/simple-app:v1 --replicas=3

# Cách 1: set image
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v2

kubectl rollout status deployment/app1-deploy

# Cách 2: edit
kubectl edit deployment/app1-deploy
# Sửa image: ...:v3

# Cách 3: apply
# Sửa file deployment.yaml → kubectl apply -f deployment.yaml

# Kiểm tra lịch sử RS
kubectl get rs
# Sẽ thấy nhiều RS với hash khác nhau

kubectl rollout history deployment/app1-deploy
```

---

## ⚠️ Lưu Ý

- 🔥 `<container-name>` PHẢI khớp tên container trong template (xem `kubectl describe deploy`)
- ⚠️ `set image` không lưu lại change → Git không có dấu vết
- 💡 RS cũ **mặc định giữ 10 cái** (`revisionHistoryLimit: 10`)

---

## ✅ Self-Check

1. **Tại sao `kubectl set image` lại tạo RS mới?**
   <details>
   <summary>Đáp án</summary>
   Vì Deployment tính hash dựa trên Pod template. Đổi image = đổi template = hash mới = RS mới.
   </details>

2. **`<container-name>` lấy ở đâu?**
   <details>
   <summary>Đáp án</summary>
   `kubectl describe deployment <name>` → mục `Containers` → tên container.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #21 — Scale & Expose](02-scale-expose-deployment.md)
- ➡️ [Bài #23 — Rollout Deployment](04-rollout-deployment.md)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
