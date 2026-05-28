# Bài #16 — Cơ Chế Làm Việc của ReplicaSet (Labels vs Selector)

> 🎯 Hiểu **DEEP** cách ReplicaSet "đếm" Pod để tránh lỗi nguy hiểm: **RS có thể "ăn" Pod khác** nếu label match!

---

## 📋 Metadata

- **Bài số:** #16
- **Module:** 06-replicaset
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~3 phút
- **Prerequisites:** [Bài #15 — Giới thiệu ReplicaSet](01-gioi-thieu-replicaset.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu RS dùng **selector + label** để **đếm** Pod (không quan tâm Pod do ai tạo)
- [ ] Test scenario: tạo Pod thủ công trước → RS chỉ tạo thêm để bù
- [ ] Hiểu **rủi ro thiết kế label**: label đơn giản quá → bug khó debug
- [ ] Áp dụng best practice đặt label

---

## 📚 Nội Dung

### 1. Cơ Chế Đếm Của ReplicaSet

```
RS "rs3" với selector: app=app3, replicas=3

Trước khi RS chạy:
   ┌──────────────────────────────────┐
   │  Pod thủ công có label app=app3  │  ← Pod đã có sẵn!
   └──────────────────────────────────┘

Sau khi RS apply:
   "Tôi cần 3 Pod với label app=app3"
   "Đếm sẵn... có 1 Pod rồi → chỉ tạo thêm 2"

   ┌──────────────────────────────────┐
   │  Pod thủ công (app=app3) ✓       │  ← Vẫn được giữ!
   │  Pod RS-tạo-1 (app=app3) ✓       │
   │  Pod RS-tạo-2 (app=app3) ✓       │
   └──────────────────────────────────┘
   = 3 Pod → đủ replicas ✅
```

→ **RS không phân biệt** Pod là do nó tạo hay do ai đó tạo. Miễn match label là **đếm**.

---

### 2. Vấn Đề: Pod "Ăn Ké" RS

#### Scenario nguy hiểm

```
Bạn có 1 Pod thủ công:
   - label: app=app3
   - image: my-app:v2 (CŨ!)

Bạn deploy RS với:
   - selector: app=app3
   - replicas: 3
   - template: image my-app:v3 (MỚI!)

→ RS đếm: đã có 1 Pod (cũ), tạo thêm 2 (mới)
→ Kết quả:
   1 Pod chạy v2 (CŨ) ❌
   2 Pod chạy v3 (MỚI)

→ User bị routing đến cả 2 version → bug crazy!
```

> 🚨 **Đây là lý do label phải UNIQUE và có TÍNH PHÂN BIỆT cao.**

---

### 3. Best Practice Đặt Label

#### ❌ Tránh

```yaml
labels:
  app: backend           # quá generic
  type: api              # quá rộng
```

#### ✅ Nên

```yaml
labels:
  app.kubernetes.io/name: my-app
  app.kubernetes.io/instance: production
  app.kubernetes.io/version: "v3.2.1"
  app.kubernetes.io/component: api
  app.kubernetes.io/part-of: my-product
  app.kubernetes.io/managed-by: helm
  environment: production
  release: stable
```

> 📚 Đây là **K8s recommended labels** — nên áp dụng từ đầu.

---

## 💻 Hands-On / Demo

### Bước 1: Tạo 1 Pod Thủ Công Trước

```bash
# Tạo Pod thủ công với label app=app3 (cùng selector RS sẽ tạo)
kubectl run app3-manual \
  --image=nginx:1.24-alpine \
  --labels="app=app3,environment=production" \
  --port=80

# Verify
kubectl get pods --show-labels
# NAME          READY   STATUS    LABELS
# app3-manual   1/1     Running   app=app3,environment=production
```

### Bước 2: Apply ReplicaSet

```bash
# Sử dụng rs3.yaml từ Bài #15
kubectl apply -f rs3.yaml

# Watch
kubectl get pods -w

# Output bất ngờ:
# NAME          READY   STATUS              RESTARTS   AGE
# app3-manual   1/1     Running             0          2m   ← Pod thủ công VẪN còn!
# rs3-abc12     0/1     ContainerCreating   0          1s   ← chỉ tạo 2 mới
# rs3-def34     0/1     ContainerCreating   0          1s
```

→ RS chỉ tạo **2 Pod** (không phải 3)! Vì đã đếm Pod thủ công có sẵn.

### Bước 3: Verify

```bash
kubectl get rs
# NAME   DESIRED   CURRENT   READY   AGE
# rs3    3         3         3       30s   ← 3 Pod (1 cũ + 2 mới)

# Xem version của từng Pod
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].image}{"\n"}{end}'
# app3-manual   nginx:1.24-alpine    ← KHÁC version!
# rs3-abc12     nginx:1.25-alpine
# rs3-def34     nginx:1.25-alpine
```

→ **Bug visible:** 1 Pod chạy version 1.24, 2 Pod chạy version 1.25!

### Bước 4: "Sửa" Bằng Cách Xóa Pod Thủ Công

```bash
kubectl delete pod app3-manual

# RS tự nhận biết, tạo Pod thay thế
kubectl get pods -w
# rs3-XYZ99   1/1   Running   ← cùng image với RS template
```

→ Bây giờ tất cả 3 Pod cùng version!

### Cleanup

```bash
kubectl delete rs rs3
```

---

## ⚠️ Lưu Ý

- 🔥 RS **đếm tất cả** Pod match label, không quan tâm ai tạo
- 🔥 Pod thủ công + RS cùng label → bug **rất khó phát hiện**
- 🔥 Đặt label **CỤ THỂ + UNIQUE** (vd: thêm `version`, `instance`)
- ✅ Áp dụng [K8s recommended labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/)
- ✅ Trong production, ít khi dùng RS trực tiếp — dùng Deployment (Module 07)

---

## ✅ Self-Check

1. **RS đếm Pod theo cơ chế gì?**
   <details>
   <summary>Đáp án</summary>
   Đếm tất cả Pod match `selector` (theo label), bất kể Pod do ai tạo.
   </details>

2. **Có 1 Pod thủ công `app=app3`. Apply RS với `replicas=3, selector: app=app3`. RS sẽ tạo bao nhiêu Pod mới?**
   <details>
   <summary>Đáp án</summary>
   **Chỉ 2 Pod mới** — vì đã đếm 1 Pod sẵn có.
   </details>

3. **Vì sao đặt label đơn giản (`app: backend`) là nguy hiểm?**
   <details>
   <summary>Đáp án</summary>
   Có thể **trùng** với resource khác → RS "ăn ké" Pod khác → bug routing, version mismatch.
   </details>

4. **Best practice tối thiểu cho label là gì?**
   <details>
   <summary>Đáp án</summary>
   Dùng **K8s recommended labels**:
   - `app.kubernetes.io/name`
   - `app.kubernetes.io/instance`
   - `app.kubernetes.io/version`
   - `environment`
   - `release`
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #15 — Giới thiệu ReplicaSet](01-gioi-thieu-replicaset.md)
- ➡️ [Bài #17 — Expose RS Imperative](03-expose-replicaset-imperative.md)

### Tài Nguyên

- 📖 [Recommended Labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/)
- 📖 [Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
- 📺 Video gốc: `Decopy_✅ #16 _ Cơ Chế Làm Việc của ReplicaSet..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Cực kỳ lưu ý: nếu các bạn tạo label đơn giản quá, RS có thể ghép nhiều version Pod không mong muốn. User truy xuất qua Service sẽ random ra cả version cũ + mới — bug crazy!"*

> 💬 *"Sau này khi hệ thống ngày càng phức tạp, các bạn cần phải xem ứng dụng đặt label như thế nào — đó là KỸ NĂNG QUAN TRỌNG khi thiết kế K8s."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
