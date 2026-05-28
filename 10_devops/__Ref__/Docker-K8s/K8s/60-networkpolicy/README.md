# Bài 60 — NetworkPolicy 🔴

> **Tiên quyết:** Hoàn thành Bài 59; cluster có **CNI hỗ trợ NetworkPolicy** (Calico/Cilium/Weave). Minikube: `minikube start --cni=calico`.
> **File:** `default-deny.yaml`, `allow-frontend.yaml`, `egress.yaml`.

> ⚠️ **CNI không support → apply không lỗi nhưng KHÔNG hoạt động.** Luôn test verify bằng `kubectl exec ... -- nc -zv target port`.

## Lệnh thủ công

### Phần A: Default Deny — chặn hết ingress

```bash
kubectl apply -f default-deny.yaml

# Test: pod khác curl vào myapp → timeout
kubectl run probe --image=busybox:1.36 -n myapp-dev --rm -it --restart=Never -- \
  sh -c "nc -zv myapp-service 80"
# → bị block
```

### Phần B: Allow theo label

```bash
kubectl apply -f allow-frontend.yaml

# Test: pod KHÔNG có label `role=frontend` → vẫn block
kubectl run probe-other --image=busybox:1.36 -n myapp-dev --rm -it --restart=Never -- \
  sh -c "nc -zv myapp-service 80"

# Pod CÓ label `role=frontend` → pass
kubectl run probe-fe --image=busybox:1.36 -n myapp-dev --rm -it --restart=Never \
  --labels="role=frontend" -- \
  sh -c "nc -zv myapp-service 80"
```

### Phần C: Egress — chặn outbound

```bash
kubectl apply -f egress.yaml

# Test: pod myapp curl ra ngoài internet → bị block
kubectl exec -n myapp-dev <myapp-pod> -- wget -T 3 https://google.com
# → timeout

# Curl tới redis → pass
kubectl exec -n myapp-dev <myapp-pod> -- nc -zv redis 6379
```

## Kết quả mong đợi

- Sau `default-deny`: mọi traffic ingress bị chặn.
- Sau `allow-frontend`: chỉ pod có label `role=frontend` gọi được myapp.
- Sau `egress`: myapp chỉ gọi được Redis và DNS, không gọi được internet.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| Apply không lỗi nhưng traffic vẫn pass | CNI không hỗ trợ NetworkPolicy — đổi sang Calico/Cilium |
| Pod fail DNS sau khi apply egress | Quên allow `kube-dns` (UDP/53) — thêm rule egress (đã có trong `egress.yaml`) |
| `Forbidden` khi apply | API server có thể chưa enable `networking.k8s.io/v1` — kiểm tra version |

## Câu hỏi

- NetworkPolicy là **whitelist** hay **blacklist**?
  *(Whitelist. Khi pod match policy nào → mọi traffic KHÔNG explicitly allow đều bị block. Pod không match policy nào → traffic free.)*
- Nếu CNI không hỗ trợ NetworkPolicy, áp dụng có lỗi không?
  *(Không lỗi nhưng cũng không hoạt động — bẫy thường gặp.)*

## Bài kế tiếp

```bash
cd ../61-affinity-taints
```
