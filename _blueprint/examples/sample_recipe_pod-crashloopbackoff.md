# Pod ở trạng thái `CrashLoopBackOff`

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 01/06/2026\
> **Loại:** Troubleshooting\
> **Áp dụng cho:** Kubernetes 1.20+

> 🎯 *Pod liên tục restart, status `CrashLoopBackOff` — debug nhanh nguyên nhân và fix.*

---

## 🐛 Problem

`kubectl get pods` show:

```
NAME         READY   STATUS             RESTARTS      AGE
my-pod       0/1     CrashLoopBackOff   5 (45s ago)   2m
```

Pod khởi động → chạy được vài giây → exit → K8s restart → lại exit → vòng lặp. Số `RESTARTS` tăng dần. `READY` luôn 0/1.

→ Người search Google: `CrashLoopBackOff`, `pod keeps restarting`, `pod restart loop kubernetes`.

## 🔍 Cause

| Nguyên nhân | Khả năng | Cách xác định |
|---|---|---|
| Container exit code != 0 (app crash) | 🔥 Cao | `kubectl logs <pod>` xem stack trace |
| CMD/ENTRYPOINT sai trong image | 🔥 Cao | `kubectl describe pod <pod>` → field `Last State: Terminated, Reason` |
| Thiếu config (ENV, volume mount) | 🟡 TB | Xem log + so YAML với spec |
| OOMKilled (vượt memory limit) | 🟡 TB | `kubectl describe` → `Last State: Terminated, Reason: OOMKilled` |
| Liveness probe fail liên tục | 🟢 Thấp | `kubectl describe` → Events có `Liveness probe failed` |
| Image không tồn tại | 🟢 Thấp (sẽ là `ImagePullBackOff` thay vì CrashLoop) | — |

## ✅ Solution

### Bước 1: Xem log container

```bash
kubectl logs my-pod
```

Nếu Pod đã restart, xem log lần restart trước (quan trọng — log hiện tại có thể rỗng):

```bash
kubectl logs my-pod --previous
```

→ Đọc log tìm error message. Đa số case fix ở đây.

### Bước 2: Describe để xem chi tiết

```bash
kubectl describe pod my-pod
```

Quan tâm 3 chỗ:

```
Containers:
  my-container:
    State:          Waiting
    Reason:         CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error     ← Error / OOMKilled / Completed
      Exit Code:    1         ← != 0 là crash
      Started:      ...
      Finished:     ...

Events:
  Type     Reason     Message
  Warning  BackOff    Back-off restarting failed container
```

- `Last State.Reason` = `OOMKilled` → tăng memory limit
- `Exit Code` = 1 / 137 → app crash, đọc log
- Events có `Liveness probe failed` → probe quá khắt khe

### Bước 3: Fix theo cause

#### Nếu app crash (đa số case)

Đọc log → fix code → rebuild image → push → update Pod:

```bash
docker build -t myapp:1.1 .
docker push myapp:1.1
kubectl set image pod/my-pod my-container=myapp:1.1
```

#### Nếu OOMKilled

Tăng memory limit trong YAML:

```yaml
resources:
  limits:
    memory: "512Mi"     # tăng lên
  requests:
    memory: "256Mi"
```

Apply lại.

#### Nếu Liveness probe fail

Nới `initialDelaySeconds` hoặc tăng `failureThreshold`:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30   # tăng lên cho app khởi động chậm
  failureThreshold: 5       # tăng lên trước khi K8s kill
```

## 🔎 Verify

```bash
kubectl get pod my-pod -w
```

Sau 30s — 1 phút:

```
NAME         READY   STATUS    RESTARTS   AGE
my-pod       1/1     Running   0          1m
```

`RESTARTS` không tăng nữa và `STATUS: Running` ổn định = đã fix.

## 🛡️ Prevention

- ✅ **Test image local trước**: `docker run myapp:1.0` chạy được mới push lên cluster
- ✅ **Set resources hợp lý**: không để default — phải có `requests` + `limits` cho cả cpu + memory
- ✅ **Liveness probe sau Readiness**: app cần thời gian khởi động, dùng `startupProbe` để bảo vệ slow start
- ✅ **Log structured**: app log JSON dễ search trong K8s
- ✅ **Monitor restart count**: alert khi `kube_pod_container_status_restarts_total` > 3 trong 5 phút

---

## 💡 Biến thể

### Biến thể A: Pod thuộc Deployment

Pod sinh từ Deployment → fix bằng cách edit Deployment, không edit Pod trực tiếp (Deployment sẽ tạo Pod mới đúng spec):

```bash
kubectl edit deployment my-deployment
# Sửa image hoặc resources trong editor
```

K8s sẽ tự rolling update.

### Biến thể B: Init container fail

Nếu init container fail thay vì main container:

```
Init Containers:
  init-db:
    State:          Terminated
    Reason:         Error
```

Debug init container riêng:

```bash
kubectl logs my-pod -c init-db
```

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [Kubernetes Pod — README cụm](../sample_kubernetes-pod/README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- [Pod — Đơn vị deploy nhỏ nhất của Kubernetes](../sample_kubernetes-pod/lessons/01_basic/01_pod.md) — vòng đời Pod
- ImagePullBackOff — Pod không pull được image (recipe khác)
- Pending Pod — Pod không schedule được (recipe khác)

### 🌐 Tài nguyên tham khảo khác

- [Official K8s troubleshooting docs](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/) — debug Pod chính chủ

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (15/05/2026)** — Bản đầu tiên — recipe debug CrashLoopBackOff (Problem → Cause → Solution → Verify → Prevention).
- **v1.1.0 (01/06/2026)** — Chuẩn hoá section Liên kết sang 3-sub + nav bullet (link text = tiêu đề thật); heading changelog chuẩn + tăng dần. Lý do: đồng bộ 3 quyết định governance + quy ước nền.
