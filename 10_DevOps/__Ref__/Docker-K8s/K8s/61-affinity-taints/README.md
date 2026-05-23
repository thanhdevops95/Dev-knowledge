# Bài 61 — Taints, Tolerations, NodeSelector, Affinity 🔴

> **Tiên quyết:** Hoàn thành Bài 60; cluster có nhiều node (Kind multi-node hoặc minikube với nhiều node) để thấy rõ. Single-node vẫn làm được taint/toleration.
> **File:** `nodeselector-pod.yaml`, `toleration-pod.yaml`, `affinity-deployment.yaml`, `anti-affinity-deployment.yaml`.

## Trước khi apply

Xem danh sách node và label hiện có:
```bash
kubectl get nodes
kubectl get nodes --show-labels
```

Thay `<YOUR_DOCKERHUB_USERNAME>` trong các file YAML cần image myapp.

## Lệnh thủ công

### Phần A: NodeSelector

```bash
# 1. Label node
kubectl label nodes <node-name> disktype=ssd tier=production

# 2. Apply pod với nodeSelector
kubectl apply -f nodeselector-pod.yaml

# 3. Verify pod schedule lên đúng node
kubectl get pod nodeselector-demo -n myapp-dev -o wide
```

### Phần B: Taints & Tolerations

```bash
# 1. Taint node để chặn pod thường
kubectl taint nodes <node-name> dedicated=gpu:NoSchedule

# 2. Pod thường sẽ Pending nếu cluster còn 1 node bị taint duy nhất
# 3. Apply pod có tolerations
kubectl apply -f toleration-pod.yaml
kubectl get pod toleration-demo -n myapp-dev -o wide

# 4. Untaint khi xong
kubectl taint nodes <node-name> dedicated=gpu:NoSchedule-
```

### Phần C: Affinity

```bash
kubectl apply -f affinity-deployment.yaml
kubectl get pods -n myapp-dev -l app=affinity-demo -o wide
```

### Phần D: PodAntiAffinity (HA spread)

```bash
kubectl apply -f anti-affinity-deployment.yaml
kubectl get pods -n myapp-dev -l app=myapp -o wide
# 3 replica phải nằm trên 3 node khác nhau (nếu cluster đủ node)
```

## Kết quả mong đợi

- Pod có `nodeSelector` chỉ schedule lên node có label đúng.
- Sau taint, pod thường `Pending`; pod có toleration schedule được.
- `podAntiAffinity` đảm bảo replicas trải đều trên các node.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| Pod `Pending` mãi | Không có node match — `kubectl describe pod` xem Events |
| AntiAffinity không spread | `topologyKey` sai; phải dùng `kubernetes.io/hostname` |
| Taint quên untaint | Khi xong demo nhớ `kubectl taint nodes <node> dedicated:NoSchedule-` |

## 3 effect của taint

- `NoSchedule`: chặn schedule mới (pod đang chạy vẫn ở lại)
- `PreferNoSchedule`: cố tránh
- `NoExecute`: đẩy pod đang chạy đi (cần `tolerationSeconds`)

## Câu hỏi

- Taint vs NodeSelector — ai chủ động?
  *(Taint: node đuổi pod. NodeSelector: pod chọn node.)*
- Khi nào dùng `requiredDuring...` vs `preferredDuring...`?
  *(Required: bắt buộc, không match = pending. Preferred: ưu tiên, không match = vẫn schedule chỗ khác.)*

## Bài kế tiếp

```bash
cd ../62-quota-pdb
```
