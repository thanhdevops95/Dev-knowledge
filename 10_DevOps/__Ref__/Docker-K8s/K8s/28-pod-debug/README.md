# Bài 28 — Debug pod (logs, exec, describe, cp)

> **Tiên quyết:** pod `myapp-pod` đang chạy.

## Lệnh thủ công

```bash
# Logs — đọc stdout/stderr của container
kubectl logs myapp-pod -n myapp-dev
kubectl logs -f myapp-pod -n myapp-dev          # follow realtime (Ctrl+C để thoát)
kubectl logs --tail=20 myapp-pod -n myapp-dev
kubectl logs --previous myapp-pod -n myapp-dev  # log của container TRƯỚC khi restart (debug crash)

# Exec vào pod — chạy lệnh bên trong container
kubectl exec -it myapp-pod -n myapp-dev -- /bin/bash
# Nếu image không có bash (vd alpine, distroless):
# kubectl exec -it myapp-pod -n myapp-dev -- sh
# Lệnh 1-lần (non-interactive):
kubectl exec myapp-pod -n myapp-dev -- ls /app
kubectl exec myapp-pod -n myapp-dev -- env

# Describe — info chi tiết + Events (debug pod stuck)
kubectl describe pod myapp-pod -n myapp-dev

# Copy file giữa pod và local
kubectl cp myapp-dev/myapp-pod:/app/app.py ./pod-app.py     # pod → local
kubectl cp ./localfile.txt myapp-dev/myapp-pod:/tmp/        # local → pod
ls -la ./pod-app.py
```

> 💡 Warning `tar: Removing leading '/' from member names` khi `kubectl cp` là **bình thường** — đây là cách K8s stream file qua API: `tar` trong pod → untar ra local. Không phải lỗi.

## Cheat sheet so sánh

| Docker | Kubernetes |
|--------|------------|
| `docker logs` | `kubectl logs` |
| `docker exec` | `kubectl exec` |
| `docker inspect` | `kubectl describe` |
| `docker cp` | `kubectl cp` |
| `docker ps` | `kubectl get pods` |

## Bài kế tiếp

→ [Bài 29 — Deployment](../29-deployment/)
