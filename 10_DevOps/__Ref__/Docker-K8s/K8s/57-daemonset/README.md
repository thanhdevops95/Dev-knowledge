# Bài 57 — DaemonSet 🔴

> **Tiên quyết:** Hoàn thành Bài 56; cluster có ít nhất 2 node để thấy DaemonSet rõ ràng (single-node vẫn làm được, chỉ thấy 1 pod).
> **File:** `daemonset-fluent-bit.yaml`.

## Lệnh thủ công

```bash
# 1. Apply DaemonSet
kubectl apply -f daemonset-fluent-bit.yaml

# 2. Verify mỗi node có đúng 1 pod
kubectl get ds -n kube-system
kubectl get pods -n kube-system -o wide -l app=fluent-bit
kubectl get nodes
# Số pod fluent-bit = số node

# 3. Mô phỏng add node mới (Kind)
# kind create cluster --config kind-multi-node.yaml   # nếu cluster mới
# Sau khi node mới Ready → DaemonSet tự deploy pod lên (không cần làm gì)

# 4. Xoá khi xong
kubectl delete -f daemonset-fluent-bit.yaml
```

## Kết quả mong đợi

- `kubectl get ds -n kube-system` — `DESIRED == CURRENT == NUMBER-READY` = số node.
- Mỗi node có 1 pod `fluent-bit-*` ở STATUS `Running`.
- Pod schedule được cả trên node control-plane nhờ `tolerations`.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| Số pod ít hơn số node | Node có taint mà DS thiếu `tolerations` — thêm vào |
| `MountVolume.SetUp failed` | hostPath không tồn tại trên node; kiểm tra distro |
| Pod `CrashLoopBackOff` | Image `fluent/fluent-bit:2.2` chưa có config — bài này demo schedule, không cấu hình config |

## So sánh DaemonSet vs Deployment

| Tiêu chí | Deployment | DaemonSet |
|---------|-----------|-----------|
| Số pod | `replicas` quyết định | bằng số node match |
| Auto thêm khi add node mới | ❌ | ✅ |
| Use case | App business | System agent (log shipper, node exporter, CNI) |

## Câu hỏi

- Khi nào dùng DaemonSet thay vì Deployment + nodeSelector?
  *(Khi cần CHẮC CHẮN mỗi node có 1 pod, kể cả node mới add.)*
- DaemonSet có cần Service không?
  *(Thường không — vì agent thường ghi log/metric ra ngoài, không nhận traffic. Trừ khi cần expose endpoint local.)*

## Bài kế tiếp

```bash
cd ../58-init-sidecar
```
