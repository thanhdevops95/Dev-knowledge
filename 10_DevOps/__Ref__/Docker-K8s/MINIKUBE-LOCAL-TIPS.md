# 🧠 Mẹo dùng Minikube/Docker Desktop trên máy local

> **Author:** Mr.Rom
> **Mục đích:** Tổng hợp các "gotcha" khi chạy bộ đề 69 bài trên macOS + Minikube + Docker Desktop. Đề master viết theo chuẩn production K8s — chạy trên local cần một số mẹo nhỏ.
>
> File này là **bạn đồng hành** với `docker-k8s-practice.md`. Khi đề ghi "bị lỗi X", check ở đây trước.

---

## 📋 Mục lục theo bài

| Vấn đề | Bài liên quan | Mục |
|--------|--------------|-----|
| macOS `cp -i` alias làm `cp` không overwrite | Docker 05 | [§1](#1-macos-cp--i-alias) |
| Image build local KHÔNG vào được cluster | K8s 27+ | [§2](#2-minikube-image-load) |
| `<YOUR_DOCKERHUB_USERNAME>` xuất hiện trong nhiều file | K8s toàn phần | [§3](#3-thay-placeholder-bằng-image-local) |
| `docker stop` mất 10s vì Flask không catch SIGTERM | Docker 11 / Bonus 53 | [§4](#4-flask-app--signal-handling) |
| `docker inspect IP` ra rỗng | Docker 17 | [§5](#5-docker-inspect-ip-format-mới) |
| Tag image uppercase Docker reject | Bonus 53 | [§6](#6-docker-tag-phải-lowercase) |
| `pkill`, `curl`, `wget` thiếu trong image slim | Bonus 51, 52 | [§7](#7-image-slim-thiếu-tool-debug) |
| `docker compose` vs `docker-compose` | Docker 23 | [§8](#8-docker-compose-v2) |
| BuildKit khiến IMAGE ID khác | Docker 05 | [§9](#9-buildkit-imager-id) |
| Apple Silicon arm64 ≠ cloud amd64 | Docker 24, 55 | [§10](#10-multi-arch-buildx) |
| Minikube IP không reach từ Mac host | K8s 30, 38, 41 | [§11](#11-minikube-ip-không-reach-từ-host) |
| NetworkPolicy không enforce | K8s Bonus 60 | [§12](#12-networkpolicy-cần-calico-cni) |
| RAM cluster không đủ | K8s Advanced 45-50, 65-69 | [§13](#13-ram--cpu-tối-thiểu) |
| Kustomize `commonLabels` deprecated | K8s Bonus 64 | [§14](#14-kustomize-5x-syntax) |
| ArgoCD CRD "Too long" khi install | Advanced 45 | [§15](#15-argocd-crd-too-long) |
| Istio `profile=minimal` không có Gateway | Advanced 48 | [§16](#16-istio-minimal-vs-demo-profile) |
| NetworkPolicy chặn Istio sidecar inject | Advanced 48 | [§17](#17-istio-sidecar--networkpolicy-conflict) |
| cert-manager webhook fail ngay sau install | Advanced 65 | [§18](#18-cert-manager-đợi-cainjector) |
| Prometheus không scrape ServiceMonitor namespace khác | Advanced 66 | [§19](#19-prometheus-serviceMonitorNamespaceSelector) |
| K8s Secret base64 ≠ encryption | K8s 33, Bonus 68 | [§20](#20-secret-base64--encryption) |

---

## §1. macOS `cp -i` alias

**Triệu chứng:** Trong Bài 05, lệnh `cp app_v1_1.py.snapshot app.py` không overwrite file → build sai content mà không có error message.

**Lý do:** macOS shipping với `alias cp='cp -i'` (interactive) trong `/etc/zshrc` hoặc user `.zshrc`. Khi target tồn tại, `cp` hỏi `overwrite app.py? (y/n)`. Nếu copy-paste cả block lệnh, không gõ `y` → file không thay đổi.

**Fix:**
```bash
/bin/cp -f source.txt target.txt    # gọi cp gốc, không alias
# HOẶC
\cp -f source.txt target.txt          # \ đứng trước = bypass alias
```

---

## §2. `minikube image load`

**Triệu chứng:** Apply Pod với `image: myapp:6.0` → `ErrImagePull` / `ImagePullBackOff` dù `docker images` trên host thấy image.

**Lý do:** Minikube chạy K8s trong VM/container riêng, **không chia sẻ image cache với Docker daemon host**.

**Fix:**
```bash
# Build image local
docker build -t myapp:6.0 .

# Load vào cluster Minikube
minikube image load myapp:6.0

# Hoặc cho kind:
kind load docker-image myapp:6.0 --name myapp-cluster

# Trong manifest, dùng imagePullPolicy: IfNotPresent
# (mặc định "Always" với tag latest sẽ thử pull từ registry)
```

**Alternative cho dev nhanh:** dùng `eval $(minikube docker-env)` để build trực tiếp trong daemon Minikube (không khuyến nghị cho lab vì làm rối state).

---

## §3. Thay placeholder bằng image local

**Triệu chứng:** Mọi YAML K8s đều có `image: <YOUR_DOCKERHUB_USERNAME>/myapp:6.0` → `InvalidImageName` khi apply.

**Lý do:** Đề viết sẵn placeholder để học viên thay bằng username Docker Hub thật. Khi chạy hoàn toàn local (không push), thay placeholder bằng `myapp:6.0` rồi `minikube image load`.

**Fix script một lần cho toàn workspace:**
```bash
# Trong /Users/rom/Me/Docker-K8s/
find K8s Advanced -name "*.yaml" -exec sed -i.bak \
  's|<YOUR_DOCKERHUB_USERNAME>/myapp|myapp|g; s|<your-username>/myapp|myapp|g' {} \;

# Sau khi xong, restore:
find K8s Advanced -name "*.yaml" -exec sed -i.bak \
  's|image: myapp:|image: <YOUR_DOCKERHUB_USERNAME>/myapp:|g' {} \;
# Hoặc clean .bak: find . -name "*.bak" -delete
```

---

## §4. Flask app & signal handling

**Triệu chứng:** `docker stop myapp-web` mất **~10 giây** rồi exit code **137** (= SIGKILL), thay vì 0/143 (graceful).

**Lý do:** Flask `app.run()` (dev server) không cài signal handler → Docker gửi SIGTERM, app ignore → Docker chờ hết grace period (mặc định 10s) → SIGKILL.

**Verify:**
```bash
time docker stop myapp-web         # ≈ 10s
docker inspect --format='{{.State.ExitCode}}' myapp-web   # 137
```

**Fix trong production:**
```python
import signal, sys
signal.signal(signal.SIGTERM, lambda s,f: sys.exit(0))
signal.signal(signal.SIGINT, lambda s,f: sys.exit(0))
```

Hoặc dùng WSGI server thật (gunicorn, uvicorn — có sẵn signal handler).

→ Chi tiết signal/PID 1: **Bonus Bài 53**.

---

## §5. `docker inspect` IP format mới

**Triệu chứng:** `docker inspect --format='{{.NetworkSettings.IPAddress}}' myapp-web` → output **rỗng**.

**Lý do:** Trên Docker 20+, field `.NetworkSettings.IPAddress` (top-level) là **legacy** — chỉ có giá trị khi container chạy trên default bridge. Container modern (custom network, Compose) → IP nằm trong `.NetworkSettings.Networks.<network-name>.IPAddress`.

**Fix:**
```bash
# In IP của mọi network container join:
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myapp-web

# Hoặc cụ thể network:
docker inspect --format='{{.NetworkSettings.Networks.bridge.IPAddress}}' myapp-web
docker inspect --format='{{.NetworkSettings.Networks.myapp-net.IPAddress}}' myapp-web
```

---

## §6. Docker tag phải lowercase

**Triệu chứng:** `docker build -t demo-A .` → `invalid reference format: repository name (library/demo-A) must be lowercase`.

**Lý do:** Image reference format yêu cầu **repository name** (phần `demo-A`) chỉ chấp nhận `[a-z0-9._-]`. Tag (`:V1`) cho phép uppercase.

**Fix:**
```bash
# Loop với lowercase, dùng tr để uppercase filename
for f in a b c d; do
  UPPER=$(echo "$f" | tr a-z A-Z)
  docker build -t demo-$f -f Dockerfile.$UPPER .
done
```

---

## §7. Image slim thiếu tool debug

**Triệu chứng:** `docker exec myapp pkill python` → `pkill: command not found`. Tương tự `curl`, `wget`, `vim`, `htop`...

**Lý do:** `python:3.11-slim`, `alpine`, `debian:slim` cố tình lược bỏ tool để giảm size + attack surface.

**Fix:**
```bash
# Option 1: dùng cách khác sẵn có
docker exec myapp kill -9 1            # PID 1 = entrypoint (luôn có)
docker exec myapp python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000').read())"  # thay curl

# Option 2: cài thêm trong Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl procps net-tools \
  && rm -rf /var/lib/apt/lists/*

# Option 3: image debug riêng (nicolaka/netshoot)
docker run --rm -it --network container:myapp nicolaka/netshoot
```

---

## §8. Docker Compose V2

**Triệu chứng:** `docker-compose up` báo `command not found` hoặc `version: '3.8'` không có tác dụng.

**Lý do:** Docker Desktop modern dùng **Compose V2** binary built-in. Lệnh chính thức: `docker compose` (có space). `docker-compose` (gạch) là V1 legacy. Field `version:` trong compose file đã **deprecated** từ V2.

**Fix:**
```bash
# Dùng "docker compose" thay "docker-compose"
docker compose up -d
docker compose ps
docker compose down -v

# Compose file: bỏ dòng version (V2 không cần)
# services: ...

# depends_on chỉ đảm bảo THỨ TỰ start, không phải READY.
# Phải combo với healthcheck + condition:
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
  web:
    depends_on:
      db:
        condition: service_healthy
```

---

## §9. BuildKit IMAGE ID

**Triệu chứng:** Bài 05 đề kỳ vọng `myapp:1.2` và `myapp:latest` cùng IMAGE ID, nhưng `docker images` thấy ID **khác nhau** dù content `app.py` giống.

**Lý do:** Docker 23+ default BuildKit. Mỗi lần build, BuildKit sinh manifest có **metadata khác** (timestamps, build attestation) → IMAGE ID khác dù layer giống.

**Fix:** Đây là **bình thường, không phải bug**. Nếu cần ID giống thật:
```bash
# Disable BuildKit (về classic builder)
DOCKER_BUILDKIT=0 docker build -t myapp:1.2 .
DOCKER_BUILDKIT=0 docker build -t myapp .
```

---

## §10. Multi-arch buildx

**Triệu chứng:** Build image trên Mac M1 (arm64) → push lên Docker Hub → cloud K8s x86_64 pull về báo `exec format error`.

**Lý do:** Image bị "lock" vào arch của máy build.

**Fix:**
```bash
# Tạo builder hỗ trợ multi-platform
docker buildx create --name multi --use --bootstrap

# Build cho cả 2 arch và push (--push BẮT BUỘC với multi-arch)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t <user>/myapp:6.0 \
  --push .

# Cleanup: phải switch context TRƯỚC khi xóa builder
docker context use default
docker buildx rm multi
```

> 💡 `docker buildx use default` báo lỗi → đây là 2 khái niệm khác (builder vs context). Phải dùng `docker context use default`.

---

## §11. Minikube IP không reach từ host

**Triệu chứng:** `minikube ip` ra `192.168.49.2`, nhưng `curl 192.168.49.2:30080` từ Mac terminal → timeout.

**Lý do:** Minikube driver=docker chạy node trong Docker container; IP `192.168.49.2` là IP của docker network, **không route từ host macOS**.

**Fix — 3 cách reach service:**

```bash
# Cách 1: port-forward (đơn giản nhất)
kubectl port-forward -n myapp-dev service/myapp-service 8080:80
curl http://localhost:8080

# Cách 2: minikube service (mở tunnel + browser)
minikube service myapp-service -n myapp-dev --url

# Cách 3: minikube tunnel (cho LoadBalancer + Ingress)
sudo minikube tunnel    # chạy nền, không tắt
# Ingress sau đó truy cập qua localhost (CẦN sudo trên macOS)
```

**Ingress local pattern (host header trick):**
```bash
# Không sửa /etc/hosts, dùng curl --resolve:
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 18080:80 &
curl -H "Host: myapp.local" http://localhost:18080/
# HOẶC
curl --resolve myapp.local:18080:127.0.0.1 http://myapp.local:18080/
```

---

## §12. NetworkPolicy cần Calico CNI

**Triệu chứng:** Apply NetworkPolicy → resource tạo OK nhưng pod KHÔNG bị chặn.

**Lý do:** Minikube default dùng **kindnet CNI** không enforce NetworkPolicy.

**Fix:**
```bash
# Phải start cluster với --cni=calico (delete + recreate nếu cần)
minikube delete
minikube start --memory=6144 --cpus=4 --cni=calico

# Verify Calico chạy
kubectl wait --for=condition=ready pod -l k8s-app=calico-node -n kube-system --timeout=180s

# Apply NetworkPolicy như bình thường — giờ sẽ enforce
```

**Verify enforce:**
```bash
# Pod được phép → OK
kubectl exec tester-frontend -- curl --max-time 5 http://myapp/

# Pod không match rule → timeout (exit code 28)
kubectl exec tester-other -- curl --max-time 5 http://myapp/
```

---

## §13. RAM & CPU tối thiểu

| Stack | RAM tối thiểu | CPU |
|-------|---------------|-----|
| Minikube + core K8s (25-41) | 4GB | 2 |
| + Calico CNI | 4GB | 2 |
| + metrics-server + ingress | 4GB | 2 |
| + ArgoCD | 5GB | 3 |
| + Istio (profile=minimal) | 5GB | 3 |
| + cert-manager | 5GB | 3 |
| + kube-prometheus-stack (light) | 6GB | 4 |
| **TẤT CẢ** (Phase 2+3 full) | **6-8GB** | **4** |
| Istio profile=demo (full addons) | thêm 2GB | thêm 1 |

```bash
minikube start --memory=6144 --cpus=4 --cni=calico
# macOS Docker Desktop: vào Settings → Resources tăng total 10GB+
```

---

## §14. Kustomize 5.x syntax

**Triệu chứng:** `kubectl kustomize` warn `'commonLabels' is deprecated. Please use 'labels' instead.`

**Fix:**
```yaml
# CŨ (deprecated)
commonLabels:
  app: myapp

# MỚI
labels:
  - pairs:
      app: myapp
    includeSelectors: true   # khớp hành vi cũ
```

---

## §15. ArgoCD CRD "Too long"

**Triệu chứng:** `kubectl apply -n argocd -f https://...install.yaml` → `The CustomResourceDefinition "applicationsets.argoproj.io" is invalid: metadata.annotations: Too long: may not be more than 262144 bytes`.

**Lý do:** CRD ApplicationSet có schema rất lớn (>262KB). `kubectl apply` (client-side) lưu cả manifest vào annotation `kubectl.kubernetes.io/last-applied-configuration` → vượt limit etcd.

**Fix:**
```bash
# Cách 1: dùng server-side apply (không lưu vào annotation)
kubectl apply --server-side -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Cách 2: kubectl create (chỉ lần đầu, không update được)
kubectl create -n argocd -f https://...
```

---

## §16. Istio minimal vs demo profile

**Triệu chứng:** Cài `istioctl install --set profile=minimal` để tiết kiệm RAM, sau đó apply Gateway → không có pod ingressgateway nào nhận request.

**Lý do:** `profile=minimal` chỉ cài `istiod` (control plane). KHÔNG có:
- `istio-ingressgateway` (cần cho Gateway resource)
- Kiali, Jaeger, Grafana, Prometheus addons

**Fix:**
```bash
# Option 1: Cài profile=demo nếu đủ RAM (~4GB extra)
istioctl install --set profile=demo -y

# Option 2: Giữ minimal + cài thêm ingressgateway riêng
istioctl install --set profile=minimal \
  --set components.ingressGateways[0].enabled=true \
  --set components.ingressGateways[0].name=istio-ingressgateway -y
```

---

## §17. Istio sidecar & NetworkPolicy conflict

**Triệu chứng:** Sau khi `kubectl label namespace istio-injection=enabled` và restart deployment, pod stuck ở `Init:1/2` mãi.

**Lý do:** Sidecar inject thêm init container `istio-init` cần kết nối tới `istiod.istio-system.svc:15012` để download mTLS cert. NetworkPolicy `default-deny-ingress`/`egress` trong namespace chặn traffic này.

**Fix:**
```bash
# Cách 1: Gỡ default-deny tạm thời khi enable injection
kubectl delete networkpolicy default-deny-ingress -n myapp-dev
# Restart pod → sidecar inject xong → re-apply policy

# Cách 2: Add allow rule cho istio-system
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-istio-control
  namespace: myapp-dev
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: istio-system
      ports:
        - {protocol: TCP, port: 15012}
        - {protocol: TCP, port: 15014}
EOF
```

---

## §18. cert-manager đợi cainjector

**Triệu chứng:** Ngay sau `kubectl apply -f cert-manager.yaml`, apply ClusterIssuer → `failed calling webhook "webhook.cert-manager.io": x509: certificate signed by unknown authority`.

**Lý do:** Race condition: `cert-manager-webhook` cần CA bundle (do `cert-manager-cainjector` inject) trong `ValidatingWebhookConfiguration` để serve TLS. Apply Issuer ngay khi pod còn đang start → webhook reject.

**Fix:**
```bash
# Đợi tất cả 3 pod ready trước khi tạo Issuer
kubectl wait --for=condition=available --timeout=120s -n cert-manager deployment/cert-manager
kubectl wait --for=condition=available --timeout=120s -n cert-manager deployment/cert-manager-cainjector
kubectl wait --for=condition=available --timeout=120s -n cert-manager deployment/cert-manager-webhook
sleep 30    # đợi cainjector inject CA vào webhook config

# Bây giờ apply Issuer OK
kubectl apply -f cluster-issuer.yaml
```

---

## §19. Prometheus serviceMonitorNamespaceSelector

**Triệu chứng:** Apply ServiceMonitor ở namespace `myapp-dev`, Prometheus chạy ở `monitoring`, không thấy target.

**Lý do:** kube-prometheus-stack mặc định set `serviceMonitorNamespaceSelector` chỉ chọn namespace có release label, hoặc `{}` (tất cả) tùy version. ServiceMonitor selector cũng cần label `release: <helm-release-name>` để match.

**Fix:**
```bash
# Cách 1: Add label release=kps vào ServiceMonitor
metadata:
  labels:
    release: kps   # = tên helm release của kube-prometheus-stack

# Cách 2: Upgrade chart với selector mở rộng
helm upgrade kps prometheus-community/kube-prometheus-stack \
  -n monitoring --reuse-values \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.serviceMonitorNamespaceSelector=""
```

---

## §20. Secret base64 ≠ encryption

**Triệu chứng:** Tưởng K8s Secret an toàn vì "encoded".

**Lý do:** Field `data:` là **base64** — bất kỳ ai có quyền `get secret` đều decode được. `kubectl describe` ẩn value nhưng `kubectl get -o yaml` để lộ.

```bash
kubectl get secret myapp-secret -o jsonpath='{.data.DB_PASSWORD}' | base64 -d
# In ra plaintext password!
```

**Fix production:**
- **Sealed Secrets** (encrypt local bằng public key, decrypt server) — đơn giản, GitOps friendly → **Bonus Bài 68**
- **External Secrets Operator + Vault/AWS Secrets Manager** — sync từ store ngoài → **Bonus Bài 68**
- **etcd encryption at rest** — encrypt ở storage layer (admin K8s cluster)

---

## 📚 Tham khảo

- File master đề: [`docker-k8s-practice.md`](docker-k8s-practice.md)
- Log chạy thực: [`LAB-RUN-LOG.md`](LAB-RUN-LOG.md) (Phase 1-4)
- Audit chất lượng: [`DOCUMENT-AUDIT.md`](DOCUMENT-AUDIT.md)

> Tất cả mẹo ở đây đều xuất phát từ **lab run thật** trên macOS arm64 + Docker Desktop + Minikube v1.38.1, không phải lý thuyết. Khi gặp lỗi mới, ghi vào LAB-RUN-LOG.md + bổ sung vào file này.
