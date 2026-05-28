# Bài #37 — Command & Args (Override Docker ENTRYPOINT/CMD)

> 🎯 Override câu lệnh chạy của container ngay tại K8s manifest.

---

## 📋 Metadata

- **Bài số:** #37
- **Module:** 10-resource-management
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~7 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu mối quan hệ Docker `ENTRYPOINT/CMD` ↔ K8s `command/args`
- [ ] Override `command` (ENTRYPOINT)
- [ ] Override `args` (CMD)
- [ ] Hiểu khi nào container chạy "complete"

---

## 📚 Nội Dung

### 1. Mapping: Docker ↔ Kubernetes

| Docker | Kubernetes | Ý nghĩa |
|--------|------------|---------|
| `ENTRYPOINT` | `command` | Câu lệnh chạy chính |
| `CMD` | `args` | Đối số (arguments) |

**Ví dụ Dockerfile:**

```dockerfile
FROM ubuntu:22.04
ENTRYPOINT ["sleep"]
CMD ["1000"]
```

→ Container chạy: `sleep 1000`

---

### 2. Override Trong K8s

**Pod 1: Không override** → chạy `sleep 1000` (mặc định Dockerfile):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
spec:
  containers:
    - name: app
      image: hieuvu/ubuntu-sleep
      # KHÔNG override
```

**Pod 2: Override cả `command` lẫn `args`** → chạy `sleep 2000`:

```yaml
spec:
  containers:
    - name: app
      image: hieuvu/ubuntu-sleep
      command: ["sleep"]      # ← Override ENTRYPOINT
      args: ["2000"]          # ← Override CMD
```

**Pod 3: Chỉ override `args`** → chạy `sleep 3000`:

```yaml
spec:
  containers:
    - name: app
      image: hieuvu/ubuntu-sleep
      args: ["3000"]         # ← Override CMD only
      # ENTRYPOINT (sleep) giữ nguyên
```

**Pod 4: Override `command` không phải sleep** → container chạy xong → `Completed`:

```yaml
spec:
  containers:
    - name: app
      image: hieuvu/ubuntu-sleep
      command: ["ls"]        # ← Chỉ liệt kê file rồi thoát
```

→ `kubectl get pod` → `STATUS: Completed`

---

### 3. Hai Cách Viết Args (Mảng)

**Cách 1 (inline):**

```yaml
args: ["3000", "--verbose", "--debug"]
```

**Cách 2 (block):**

```yaml
args:
  - "3000"
  - "--verbose"
  - "--debug"
```

→ Tương đương nhau.

---

### 4. Khi Container Chạy "Complete"

Container hoàn thành công việc → tự động dừng:

```bash
kubectl get pod
# NAME    READY   STATUS      RESTARTS   AGE
# pod-4   0/1     Completed   0          5s

kubectl describe pod pod-4
# Events:
#   Successfully pulled image
#   Created container
#   Started container
#   <Then exited>
```

**Để chạy mãi mãi** → ENTRYPOINT phải là long-running:

- Web server (`nginx`, `gunicorn`)
- Polling loop
- `sleep infinity`

---

### 5. Use Case Phổ Biến

**1. Init script:**

```yaml
command: ["/bin/sh", "-c"]
args: ["./migrate.sh && exec ./server"]
```

**2. Pass config:**

```yaml
command: ["./app"]
args: ["--config=/etc/config.yaml", "--port=8080"]
```

**3. Probes / Health checks:**

```yaml
livenessProbe:
  exec:
    command: ["curl", "-f", "http://localhost:8080/health"]
```

---

## 💻 Hands-On / Demo

```bash
# 1. Pod mặc định
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-default
spec:
  containers:
    - name: app
      image: ubuntu:22.04
      command: ["sleep", "infinity"]
EOF

# 2. Override args
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-args
spec:
  containers:
    - name: app
      image: ubuntu:22.04
      command: ["sleep"]
      args: ["3000"]
EOF

# 3. Container "Completed"
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-ls
spec:
  containers:
    - name: app
      image: ubuntu:22.04
      command: ["ls", "/"]
EOF

# 4. Check
kubectl get pods
# pod-default   1/1   Running
# pod-args      1/1   Running
# pod-ls        0/1   Completed   ← chạy xong rồi

# 5. Cleanup
kubectl delete pod pod-default pod-args pod-ls
```

---

## ⚠️ Lưu Ý

- 🔥 `command` override **ENTRYPOINT** (KHÔNG phải `CMD`!)
- 🔥 `args` override **CMD**
- ⚠️ Nếu image có `ENTRYPOINT ["sh", "-c"]` thì `args` cần truyền cả command
- 💡 Thường dùng `["/bin/sh", "-c", "<full-command>"]` cho linh hoạt
- ⚠️ Container "Completed" sẽ KHÔNG restart trong Pod thường, nhưng sẽ restart trong Deployment/Job

---

## ✅ Self-Check

1. **`command` map vào gì trong Dockerfile?**
   <details>
   <summary>Đáp án</summary>
   `ENTRYPOINT`
   </details>

2. **Override `args` mà không override `command` thì sao?**
   <details>
   <summary>Đáp án</summary>
   ENTRYPOINT của Dockerfile vẫn được dùng. Chỉ args bị override.
   </details>

3. **Khi nào container "Completed"?**
   <details>
   <summary>Đáp án</summary>
   Khi process chính (ENTRYPOINT/CMD) thoát với exit code 0.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #36 — Best Practices](02-best-practices-requests-limits.md)
- ➡️ [Bài #38 — Metrics Server](04-metrics-server.md)

### Tài Nguyên

- 📖 [Define a Command and Arguments for a Container](https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
