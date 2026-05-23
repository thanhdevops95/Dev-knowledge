# Bài #14 — YAML K8s Manifest 101

> 🎯 Học **YAML syntax** đủ dùng cho K8s — không cần thành expert YAML, chỉ cần biết viết manifest đúng.

---

## 📋 Metadata

- **Bài số:** #14
- **Module:** 05-imperative-vs-declarative
- **Cấp độ:** `BEGINNER → INTERMEDIATE`
- **Thời lượng video gốc:** ~6 phút
- **Prerequisites:** [Bài #13 — Imperative vs Declarative](01-imperative-vs-declarative.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Hiểu **luật indentation** quan trọng nhất của YAML
- [ ] Phân biệt **4 kiểu dữ liệu**: scalar, dictionary, list, multi-line string
- [ ] Viết được manifest Pod đầy đủ
- [ ] Xử lý multi-line string (`|` literal vs `>` folded)

---

## 📚 Nội Dung

### 1. YAML là gì?

**YAML** = "**Y**AML **A**in't **M**arkup **L**anguage" — định dạng văn bản dễ đọc cho con người.

K8s chấp nhận cả **YAML** và **JSON**, nhưng **gần 100% người dùng chọn YAML** vì:
- Không cần `{}`, `[]`
- Không cần dấu `,`
- Có comment (`#`)
- Đọc tự nhiên

#### Quy tắc indentation (CỰC KỲ QUAN TRỌNG)

```yaml
# ✅ ĐÚNG — thường dùng 2 space
metadata:
  name: my-pod          # 2 space
  labels:               # 2 space
    app: web            # 4 space (1 cấp con của labels)
```

```yaml
# ❌ SAI — trộn tab và space, sai indent
metadata:
   name: my-pod         # 3 space (sai!)
  labels:               # 2 space
    app: web
```

> ⚠️ **Quy tắc:** Đã chọn 2 space → **mọi cấp đều 2 space**, KHÔNG dùng TAB.

---

### 2. Bốn Kiểu Dữ Liệu YAML

#### 2.1. Scalar (Key-Value Pair)

```yaml
name: Mr.Rom
age: 18
isHappy: true
salary: 50000.5
```

#### 2.2. Dictionary / Map (Object)

Một object lồng nhau:

```yaml
person:
  name: Mr.Rom
  age: 18
  address:
    city: Hanoi
    country: Vietnam
```

> 💡 Trong K8s: `metadata`, `spec`, `labels` — đều là **dictionary**.

#### 2.3. List / Array (Mảng)

Dùng dấu `-` cho mỗi phần tử:

```yaml
person:
  name: Mr.Rom
  albums:
    - name: Album 1
      pictures: 60
    - name: Album 2
      pictures: 30
    - name: Album 3
      pictures: 20
```

> 💡 Trong K8s: `containers`, `ports`, `env` — đều là **list**.

#### 2.4. Multi-line String

##### Literal Block (`|`) — GIỮ xuống dòng

```yaml
description: |
  This is line 1.
  This is line 2.
  This is line 3.
```

Khi parse → giữ nguyên xuống dòng:
```
This is line 1.
This is line 2.
This is line 3.
```

> 💡 Dùng cho: shell script dài, config file embedded.

##### Folded Block (`>`) — Gộp thành 1 dòng

```yaml
description: >
  This is a very long
  description that should
  be folded into one line.
```

Khi parse → bỏ xuống dòng:
```
This is a very long description that should be folded into one line.
```

> 💡 Dùng cho: văn bản dài, nhưng thực tế là 1 dòng.

---

### 3. Cấu Trúc Manifest K8s — 4 Phần Cơ Bản

```yaml
apiVersion: v1          # ← [1] API version (vd: v1, apps/v1, networking.k8s.io/v1)
kind: Pod               # ← [2] Loại resource (Pod, Deployment, Service, ConfigMap...)
metadata:               # ← [3] Metadata (tên, label, annotation, namespace)
  name: my-pod
  labels:
    app: simple-app
    environment: dev
spec:                   # ← [4] Specification (config thực tế của resource)
  containers:
    - name: app
      image: nginx:latest
      ports:
        - containerPort: 80
```

#### Mapping Resource → apiVersion + kind

| Resource          | `apiVersion`           | `kind`                 |
| ----------------- | ---------------------- | ---------------------- |
| Pod               | `v1`                   | `Pod`                  |
| Service           | `v1`                   | `Service`              |
| ConfigMap, Secret | `v1`                   | `ConfigMap` / `Secret` |
| Deployment        | `apps/v1`              | `Deployment`           |
| ReplicaSet        | `apps/v1`              | `ReplicaSet`           |
| Ingress           | `networking.k8s.io/v1` | `Ingress`              |
| NetworkPolicy     | `networking.k8s.io/v1` | `NetworkPolicy`        |

> 💡 **Quy tắc đặt tên:** dùng **camelCase** (vd: `apiVersion`, `containerPort`).

---

### 4. Ví Dụ: Pod với Multi-Container

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
    - name: simple-app
      image: nginx
      ports:
        - containerPort: 80
    - name: helper
      image: busybox
      command: ["sleep", "3600"]
```

> ⚠️ **Multi-container Pod**: các container phải dùng **port khác nhau** (vì share network namespace).

---

## 💻 Hands-On / Demo

### Tạo file `demo.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-app
  labels:
    app: simple-app
    env: dev
spec:
  containers:
    - name: simple-app
      image: nginx:latest
      ports:
        - containerPort: 80
      env:
        - name: APP_VERSION
          value: "1.0"
        - name: LOG_LEVEL
          value: "debug"
```

### Apply & Verify

```bash
# Apply
kubectl apply -f demo.yaml
# pod/simple-app created

# Verify
kubectl get pods
kubectl describe pod simple-app
kubectl logs simple-app

# Vào trong pod
kubectl exec -it simple-app -- sh
# Bên trong:
~ $ env | grep APP
APP_VERSION=1.0
LOG_LEVEL=debug
```

### Validate YAML trước khi apply (rất hữu ích)

```bash
# Dry-run (test syntax, không tạo thực sự)
kubectl apply -f demo.yaml --dry-run=client

# Validate online: yamllint.com hoặc YAML extension trong VS Code
```

### Cleanup

```bash
kubectl delete -f demo.yaml
```

---

## 🛠️ Mẹo Hay

### Mẹo 1: Generate YAML tự động từ Imperative

```bash
# Tạo Pod imperative, NHƯNG chỉ in YAML (không thực sự tạo)
kubectl run my-pod --image=nginx --port=80 \
  --dry-run=client -o yaml > my-pod.yaml

# Mở my-pod.yaml ra sửa, rồi apply
```

→ Cách **nhanh nhất** để có YAML mẫu mà không phải nhớ cú pháp.

### Mẹo 2: VS Code Extension

Cài `YAML` extension của Red Hat → có:
- IntelliSense cho K8s manifest
- Validation tự động
- Format on save

### Mẹo 3: Comment trong YAML

```yaml
# Đây là comment toàn dòng
apiVersion: v1
kind: Pod
metadata:
  name: my-pod  # Comment cuối dòng
```

---

## ⚠️ Lưu Ý

- 🚨 **KHÔNG dùng TAB** — chỉ space (mặc định 2)
- 🚨 **Indentation phải nhất quán** — mọi cấp cùng số space
- 🚨 String chứa số (`"1.0"`, `"100"`) phải có **dấu nháy**, nếu không K8s parse thành number
- 🔥 Multi-container trong 1 Pod → các port phải khác nhau
- 🔥 Tên resource phải **lowercase + hyphens**: `my-pod` ✅, `MyPod` ❌
- 💡 Lưu YAML vào Git (kèm app code) — track thay đổi

---

## ✅ Self-Check

1. **YAML chỉ chấp nhận TAB hay SPACE?**
   <details>
   <summary>Đáp án</summary>
   **Chỉ SPACE** (thường 2). Tuyệt đối không TAB.
   </details>

2. **4 phần cơ bản của manifest K8s?**
   <details>
   <summary>Đáp án</summary>
   `apiVersion`, `kind`, `metadata`, `spec`
   </details>

3. **`apiVersion` của Deployment là gì?**
   <details>
   <summary>Đáp án</summary>
   `apps/v1`
   </details>

4. **`|` và `>` khác nhau ở điểm nào?**
   <details>
   <summary>Đáp án</summary>
   - `|` (Literal): GIỮ xuống dòng
   - `>` (Folded): GỘP các dòng thành 1 (xuống dòng = space)
   </details>

5. **Lệnh nào generate YAML từ imperative command?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl run pod --image=nginx --dry-run=client -o yaml
   kubectl create deployment app --image=nginx --dry-run=client -o yaml
   ```

   </details>

6. **Có 2 container trong 1 Pod, có thể đặt cùng `containerPort: 80` không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG** — vì share network namespace nên port phải khác nhau.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #13 — Imperative vs Declarative](01-imperative-vs-declarative.md)
- ➡️ [Module 06 — ReplicaSet](../06-replicaset/README.md)

### Tài Nguyên

- 📖 [YAML Spec](https://yaml.org/spec/)
- 📖 [K8s API Reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- 📖 [yamllint](https://yamllint.com/)
- 📺 Video gốc: `Decopy_✅ #14 _ YAML K8s Manifest 101..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"YAML rất kỵ TAB. Bỏ lệch 1 space thôi là `kubectl apply` không chạy ngay."*

> 💬 *"Khi viết YAML, các bạn nên dùng VS Code thay vì terminal — có syntax highlight, IntelliSense, dễ phát hiện lỗi sớm hơn."*

> 💬 *"Sau này có thể tạo cả 1 tenant chạy với 1 lệnh `kubectl apply -f tenants/` — đó là sức mạnh của Declarative + YAML."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
