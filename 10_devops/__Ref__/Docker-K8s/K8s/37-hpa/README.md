# Bài 37 — HPA (Horizontal Pod Autoscaler)

> 📌 **HPA cần `resources.requests` trong Deployment** để tính %CPU. Không có `requests` → metrics-server không tính được tỉ lệ → HPA vĩnh viễn không scale (giá trị `<unknown>`).

## Lệnh thủ công

```bash
# 1. Bật metrics-server (cần để HPA đọc CPU/MEM)
# Minikube:
minikube addons enable metrics-server
# Kind/khác — cài thủ công:
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Đợi vài phút metrics có dữ liệu, verify:
kubectl top nodes
kubectl top pods -n myapp-dev

# 2. Cách nhanh — autoscaling/v1 (chỉ CPU)
kubectl autoscale deployment myapp-deployment \
  --cpu-percent=50 --min=2 --max=10 \
  -n myapp-dev

# 3. KHUYẾN NGHỊ — autoscaling/v2 YAML (CPU + Memory + behavior)
kubectl apply -f hpa-v2.yaml

# 4. Xem HPA
kubectl get hpa -n myapp-dev
kubectl describe hpa myapp-hpa -n myapp-dev

# 5. Tạo tải để test scale
kubectl run load-gen --image=busybox:1.36 -n myapp-dev --rm -it --restart=Never -- /bin/sh
# Trong shell load-gen:
#   while true; do wget -q -O- http://myapp-service.myapp-dev/; done
# Ctrl+C để thoát

# 6. Quan sát scale (terminal khác)
kubectl get hpa -w -n myapp-dev
kubectl top pods -n myapp-dev
kubectl get pods -n myapp-dev
```

## So sánh `autoscaling/v1` vs `autoscaling/v2`

| Tiêu chí | `v1` (`kubectl autoscale`) | `v2` (file `hpa-v2.yaml`) |
|---------|--------------------------|---------------------------|
| Metric | Chỉ CPU | CPU + Memory + Custom |
| Multi-metric | ❌ | ✅ |
| `behavior` (stabilization, policies) | ❌ | ✅ — chống flapping |
| Phù hợp | Dev/demo nhanh | Production |

## Kết quả mong đợi

- Khi tải tăng → HPA tăng replicas đến gần max=10.
- Khi dừng tải → sau `scaleDown.stabilizationWindowSeconds` (5 phút) replicas giảm về 2.
- `kubectl get hpa` không có `<unknown>` — bằng cách Deployment khai `resources.requests`.

## Câu hỏi

- Nếu Deployment KHÔNG có `resources.requests.cpu`, HPA hiển thị `<unknown>` — tại sao?
  *(Vì HPA tính % so với requests, không có requests = không có mẫu số.)*
- `stabilizationWindowSeconds` giúp gì? Đặt 0 sẽ ra sao?
  *(Chống flapping — pod scale up/down liên tục khi metric dao động. 0 = phản ứng tức thì, dễ thrashing.)*
- HPA scale theo RPS thì làm thế nào?
  *(Custom metrics adapter + Prometheus — học ở Bài 66 Bonus.)*

## Bài kế tiếp

```bash
cp -r ../37-hpa ../38-ingress
cd ../38-ingress
```
