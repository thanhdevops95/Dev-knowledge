# Bài 48 — Cài Istio & Sidecar Injection

## Tiên quyết

- Cluster đủ RAM (≥4GB free).
- `minikube start --memory=8192 --cpus=4` nếu chưa.

> ⚠️ **Tài nguyên cần thiết — chọn profile theo máy:**
>
> | Profile | Component | RAM tối thiểu | Dùng khi |
> |---------|-----------|---------------|----------|
> | `demo` | istiod + ingress + Kiali/Jaeger/Grafana/Prometheus | **≥ 4GB RAM, 2 vCPU** | Học đầy đủ (đề mặc định) |
> | `minimal` | chỉ istiod + ingress gateway | ~1GB RAM | Máy yếu, học traffic management |
>
> **Máy yếu:** `minikube start --memory=6144 --cpus=4` rồi mới cài Istio. Pod hay bị `Pending` / `OOMKilled` chính là dấu hiệu RAM không đủ.

## Phần A — Cài đặt

```bash
# 1. Download istioctl
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# 2. Install Istio
#    Demo full-stack (mặc định cho bài này):
istioctl install --set profile=demo -y
#    Hoặc minimal nếu máy yếu:
# istioctl install --set profile=minimal -y

# 3. Cài addons (Kiali, Jaeger, Grafana, Prometheus)
kubectl apply -f samples/addons/
kubectl rollout status deployment/kiali -n istio-system

# 4. Enable automatic sidecar injection cho namespace
kubectl label namespace myapp-dev istio-injection=enabled
```

## Phần B — Redeploy & quan sát sidecar

```bash
# Restart deployment để inject sidecar
kubectl rollout restart deployment/myapp-deployment -n myapp-dev
kubectl rollout status deployment/myapp-deployment -n myapp-dev

# Pod giờ có 2 container: app + istio-proxy
kubectl get pods -n myapp-dev
# READY: 2/2 (thay vì 1/1 trước đây)

kubectl describe pod <pod-name> -n myapp-dev | grep -A 5 istio-proxy
```

## Phần C — Truy cập qua Istio Gateway

Apply `gateway.yaml`:
```bash
kubectl apply -f gateway.yaml

# Lấy IP của istio-ingressgateway
kubectl get svc istio-ingressgateway -n istio-system
# Với Minikube:
minikube tunnel   # chạy ở terminal riêng
```

## Câu hỏi

- Sidecar proxy = container `istio-proxy` (Envoy) chạy chung pod với app
- Data plane = sidecar; Control plane = istiod

## Bài kế tiếp

```bash
cp -r ../48-istio-setup ../49-traffic-management
cd ../49-traffic-management
```
