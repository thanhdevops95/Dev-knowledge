# Module 03 — Pod & kubectl Cơ Bản

> **Mục đích:** Làm quen **Pod** (đơn vị triển khai cơ bản) + 3 command `kubectl` quan trọng nhất: `run`, `logs`, `exec`.

---

## 📋 Metadata Module

- **Số bài:** 4
- **Tổng thời lượng video:** ~17 phút
- **Cấp độ:** `BEGINNER → INTERMEDIATE`
- **Prerequisites:** [Module 02 — Setup](../02-environment-setup/README.md) (Minikube đang chạy)

---

## 🗺️ Danh Sách Bài Học

| # | Bài Học | Mô Tả | Thời Lượng |
|---|---------|-------|------------|
| 01 | [Pod là gì? Demo kubectl run](01-pod-la-gi.md) | Khái niệm Pod, scaling, image policy | ~7 phút |
| 02 | [kubectl logs](02-kubectl-logs.md) | Xem & stream log, multi-container, --previous | ~3 phút |
| 03 | [kubectl exec](03-kubectl-exec.md) | Chui vào container, debug | ~2 phút |
| 04 | [Curl Pod (cross-namespace)](04-curl-pod.md) | DNS naming, networking giữa namespace | ~5 phút |

> ⚠️ **Bài #04 (Curl Pod)** thực ra dùng kiến thức Service & Namespace — bạn có thể skip và quay lại sau khi học xong Module 08, 09.

---

## 🎯 Sau Module Này, Bạn Sẽ:

- ✅ Tạo / xem / xóa **Pod** thành thạo
- ✅ Debug app bằng `kubectl logs` (kể cả streaming)
- ✅ Chui vào container bằng `kubectl exec`
- ✅ Hiểu DNS naming convention của K8s services

---

## 🛠️ Cheat Sheet

```bash
# CRUD Pod
kubectl run <name> --image=<image> --port=<port>   # Tạo
kubectl get pods                                    # Liệt kê
kubectl get pods -A                                 # Tất cả namespace
kubectl describe pod <name>                          # Chi tiết
kubectl delete pod <name>                            # Xóa

# Debug
kubectl logs <pod>                                   # Xem log
kubectl logs -f <pod>                                # Stream log
kubectl logs <pod> -c <container>                    # Multi-container
kubectl logs <pod> -p                                # Log lần crash trước
kubectl exec -it <pod> -- sh                         # Chui vào shell
kubectl exec <pod> -- <command>                      # Chạy 1 command
```

---

## 🔗 Tiếp Theo

➡️ **[Module 04 — Expose Pod (NodePort)](../04-expose-pod-nodeport/README.md)** (Mở Pod ra Internet)
