# Exercise 01: Tạo Pod đầu tiên

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026\
> **Độ khó:** ⭐ Easy\
> **Thời gian ước tính:** ~10 phút\
> **Prerequisites:** [Pod basic](../sample_kubernetes-pod/lessons/01_basic/01_pod.md)

> 🎯 *Luyện kỹ năng tạo Pod cơ bản bằng cả 2 cách imperative và declarative. Bài tập đầu tiên cho người mới học K8s.*

---

## 🎯 Mục tiêu

Sau khi làm xong, bạn sẽ:

- [ ] Tạo được Pod bằng `kubectl run`
- [ ] Tạo được Pod bằng YAML manifest + `kubectl apply`
- [ ] Verify Pod đang chạy với labels đúng

## 📋 Đề bài

Tạo 1 Pod chạy nginx, có 2 label:
- `app=my-web`
- `tier=frontend`

Bằng **cả 2 cách** — imperative trước, sau đó xóa và làm lại bằng declarative.

### Input

- 1 cluster K8s đang chạy (Minikube/Kind/Docker Desktop)
- `kubectl` đã configure trỏ vào cluster

### Output mong đợi

- 1 Pod tên `my-web-pod` đang ở trạng thái `Running`
- Có 2 label như yêu cầu
- Tạo được bằng cả 2 cách (xóa giữa 2 lần)

## 🧪 Yêu cầu cụ thể

1. **Phần A — Imperative**: dùng `kubectl run` để tạo Pod với label
2. **Phần B — Declarative**: viết file `pod.yaml`, apply
3. Verify bằng `kubectl get pods --show-labels` thấy đúng labels

## 💡 Gợi ý

<details>
<summary>Gợi ý 1: kubectl run có flag `--labels` không?</summary>

Có. Dùng `--labels=key1=value1,key2=value2` (chú ý dấu `=`, không phải `:`).

</details>

<details>
<summary>Gợi ý 2: YAML manifest cấu trúc thế nào?</summary>

3 phần chính: `apiVersion`, `kind`, `metadata` (gồm `labels`), `spec` (gồm `containers`).

</details>

## ✅ Đáp án

<details>
<summary>💡 Mở đáp án</summary>

### Phần A — Imperative

```bash
kubectl run my-web-pod \
  --image=nginx:1.25 \
  --labels="app=my-web,tier=frontend"
```

Verify:

```bash
kubectl get pods --show-labels
```

```
NAME         READY   STATUS    LABELS
my-web-pod   1/1     Running   app=my-web,tier=frontend
```

Xóa để làm phần B:

```bash
kubectl delete pod my-web-pod
```

### Phần B — Declarative

Tạo `pod.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-web-pod
  labels:
    app: my-web
    tier: frontend
spec:
  containers:
    - name: nginx
      image: nginx:1.25
```

Apply:

```bash
kubectl apply -f pod.yaml
```

Verify giống phần A.

### Cách khác

Có thể dùng `kubectl run --dry-run=client -o yaml` để generate YAML từ imperative — cách lai 2 phương pháp:

```bash
kubectl run my-web-pod --image=nginx:1.25 \
  --labels="app=my-web,tier=frontend" \
  --dry-run=client -o yaml > pod.yaml
```

</details>

## 🔍 Verify bạn làm đúng

| Check | Lệnh | Kết quả mong đợi |
|---|---|---|
| Pod tồn tại | `kubectl get pod my-web-pod` | `Running` |
| Labels đúng | `kubectl get pod my-web-pod --show-labels` | Cột LABELS show 2 label |
| YAML valid | `kubectl apply -f pod.yaml --dry-run=client` | `pod/my-web-pod created (dry run)` |

## 🚀 Mở rộng

- 🔥 **Hard mode**: thêm 1 label `version=v1` mà KHÔNG xóa pod (gợi ý: `kubectl label`)
- 🎨 **Variation**: tạo Pod chạy image khác (vd: `httpd:2.4`) với cùng cấu trúc YAML

---

## 🔗 Liên kết

- ⬅️ Bài tập trước: (chưa có — đây là bài đầu)
- ➡️ Bài tập tiếp: Exercise 02 — Scale Deployment (chưa có)
- 📖 Bài học liên quan: [Pod basic](../sample_kubernetes-pod/lessons/01_basic/01_pod.md)

---

## 📌 Changelog

- **v1.0.0 (15/05/2026)** — Bản đầu tiên — sample dogfood exercise template.
