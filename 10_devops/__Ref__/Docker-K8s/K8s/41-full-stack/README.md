# Bài 41 — Dự án tổng hợp: Full Stack trên K8s

> **Đề tổng hợp** — kết hợp tất cả kiến thức Bài 25-40.

## Yêu cầu bắt buộc

1. **Frontend nginx** — Deployment 2 replicas, serve static HTML "Welcome"
2. **Backend API** — `<your-username>/myapp:7.0`, Deployment 3 replicas + HPA min=2 max=10
3. **Redis cache** — StatefulSet
4. **PostgreSQL** — StatefulSet với PVC
5. **ConfigMap** chia sẻ + **Secret** cho passwords
6. **Ingress** với 2 path: `/` → frontend, `/api` → backend
7. **Liveness/Readiness probes** đầy đủ
8. **Resource requests/limits** mọi container
9. Đóng gói thành **Helm chart**

## Cấu trúc thư mục đã chuẩn bị

```
41-full-stack/
├── README.md                ← bạn đang đọc
├── manifests/               ← raw YAML (Phần 1)
│   ├── 00-namespace.yaml
│   ├── 01-configmap.yaml
│   ├── 02-secret.yaml
│   ├── 03-frontend.yaml
│   ├── 04-backend.yaml
│   ├── 05-redis-statefulset.yaml
│   ├── 06-postgres-statefulset.yaml
│   ├── 07-services.yaml
│   ├── 08-ingress.yaml
│   └── 09-hpa.yaml
└── helm-chart/              ← phiên bản Helm (Phần 2 — tuỳ chọn)
```

## Lệnh thủ công

### Phần 1 — Apply raw YAML

```bash
# Sửa <YOUR_DOCKERHUB_USERNAME> trong các file trước!
cd manifests
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-configmap.yaml
kubectl apply -f 02-secret.yaml
kubectl apply -f 05-redis-statefulset.yaml
kubectl apply -f 06-postgres-statefulset.yaml
kubectl apply -f 03-frontend.yaml
kubectl apply -f 04-backend.yaml
kubectl apply -f 07-services.yaml
kubectl apply -f 08-ingress.yaml
kubectl apply -f 09-hpa.yaml

# Đợi mọi resource ready
kubectl get all -n myapp-dev
kubectl wait --for=condition=ready pod --all -n myapp-dev --timeout=180s
```

### Phần 2 — Truy cập

```bash
# Lấy minikube IP, thêm /etc/hosts
echo "$(minikube ip) myapp.local" | sudo tee -a /etc/hosts

# Test
curl http://myapp.local/              # frontend nginx
curl http://myapp.local/api/health    # backend API
```

## Tiêu chí đánh giá

- [ ] Tất cả pod Running, READY 1/1 hoặc 2/2
- [ ] Frontend & Backend routing đúng qua Ingress
- [ ] Backend kết nối được Redis (đếm visitor tăng)
- [ ] HPA hiển thị `kubectl get hpa`
- [ ] PVC `Bound`
- [ ] Secret base64 (không hardcode plaintext trong Deployment YAML)

## Phần 2 (tuỳ chọn) — Helm

Dùng `helm create myapp-fullstack` rồi gộp tất cả manifests trên thành templates. Có thể tham khảo chart Helm chuẩn (Bitnami, etc.).

## Hoàn thành Phần K8s

**Tiếp:** [Advanced/](../../Advanced/) — Helm template chuyên sâu, ArgoCD, Istio.
