# Kubernetes — 17 bài thực hành thủ công + 9 bài Bonus

> **Series:** kubernetes-practice · [← Docker](../Docker/README.md) · [Mục lục tổng](../README.md) · [Tiếp: Advanced →](../Advanced/README.md)

## Tiên quyết

- Đã hoàn thành **Docker Bài 24** — image `<your-username>/myapp:6.0` push lên Docker Hub (Public).
- Cluster K8s: Minikube / Kind / Docker Desktop.
- `kubectl get nodes` → `Ready`.

## Cách dùng

Mỗi bài 1 thư mục chứa các file manifest YAML + `README.md` lệnh thủ công. Trước khi `apply`, **mở từng file** và thay `<YOUR_DOCKERHUB_USERNAME>` bằng tên thật.

## Lộ trình 17 bài chính

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 25 | [`25-cluster-setup/`](25-cluster-setup/) | Cài Minikube/Kind/Docker Desktop K8s |
| 26 | [`26-namespace/`](26-namespace/) | Namespace `myapp-dev`/`myapp-prod` |
| 27 | [`27-pod-first/`](27-pod-first/) | Pod đầu tiên + `imagePullPolicy` |
| 28 | [`28-pod-debug/`](28-pod-debug/) | logs/exec/describe/cp |
| 29 | [`29-deployment/`](29-deployment/) | 3 replicas, self-healing, scale |
| 30 | [`30-service/`](30-service/) | NodePort, load balance |
| 31 | [`31-rolling-update/`](31-rolling-update/) | Update image, rollback |
| 32 | [`32-configmap/`](32-configmap/) | ConfigMap → env |
| 33 | [`33-secret/`](33-secret/) | Secret (`stringData` + base64) |
| 34 | [`34-pv-pvc/`](34-pv-pvc/) | Persistent Volume (hostPath) |
| 35 | [`35-redis-on-k8s/`](35-redis-on-k8s/) | Redis trong cluster |
| 36 | [`36-probes/`](36-probes/) | Liveness + Readiness + **Startup** |
| 37 | [`37-hpa/`](37-hpa/) | Autoscale (`autoscaling/v2` + behavior) |
| 38 | [`38-ingress/`](38-ingress/) | HTTP routing host-based |
| 39 | [`39-statefulset/`](39-statefulset/) | StatefulSet + Headless Service |
| 40 | [`40-helm/`](40-helm/) | Helm chart cơ bản |
| 41 | [`41-full-stack/`](41-full-stack/) | **Dự án tổng hợp** |

## Bonus — 9 bài production-grade

> Học sau Bài 41. Mỗi bài là một mảng kiến thức **bắt buộc** cho cluster production thật. Kí hiệu 🔴 = critical.

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 56 🔴 | [`56-job-cronjob/`](56-job-cronjob/) | Job + CronJob (migration, backup, scheduled task) |
| 57 🔴 | [`57-daemonset/`](57-daemonset/) | DaemonSet — pod chạy trên MỌI node (log shipper) |
| 58 🔴 | [`58-init-sidecar/`](58-init-sidecar/) | Init Container + Sidecar Pattern |
| 59 🔴 | [`59-rbac/`](59-rbac/) | RBAC + ServiceAccount + Role/RoleBinding |
| 60 🔴 | [`60-networkpolicy/`](60-networkpolicy/) | NetworkPolicy — firewall ở tầng pod |
| 61 🔴 | [`61-affinity-taints/`](61-affinity-taints/) | Taints / Tolerations / NodeSelector / Affinity |
| 62 🔴 | [`62-quota-pdb/`](62-quota-pdb/) | ResourceQuota + LimitRange + PodDisruptionBudget |
| 63 | [`63-storageclass/`](63-storageclass/) | StorageClass + Dynamic Provisioning |
| 64 🔴 | [`64-kustomize/`](64-kustomize/) | Kustomize — base + overlays/dev/prod |

## ⚠️ Lưu ý

- **Namespace mặc định** từ Bài 27: `myapp-dev`. Set default: `kubectl config set-context --current --namespace=myapp-dev` (Bài 26).
- **`imagePullPolicy: IfNotPresent`** (Bài 27): với Minikube/Kind cần `minikube image load` hoặc `kind load docker-image` để load image local vào cluster.
- **Secret base64 ≠ encrypt** (Bài 33): chỉ encode. Production dùng Sealed Secrets / External Secrets (Bài 68 Bonus).
- **`hostPath` PV chỉ single-node** (Bài 34): cluster production phải dùng StorageClass (Bài 63 Bonus).
- **`REDIS_PORT` collision** (Bài 35): K8s tự inject biến `<SERVICE>_PORT=tcp://IP:PORT`. App nên dùng tên biến **khác** (`APP_REDIS_HOST`) hoặc parse `tcp://`.
- **3 probe** (Bài 36): Liveness restart, Readiness gỡ khỏi Service, Startup cho app boot chậm.
- **HPA `autoscaling/v2`** (Bài 37): hỗ trợ multi-metric + `behavior` chống flapping. Cần `metrics-server` và `resources.requests`.
- **Ingress** (Bài 38) cần controller — Minikube: `minikube addons enable ingress`.
- **NetworkPolicy** (Bài 60) cần CNI hỗ trợ (Calico/Cilium) — Minikube: `minikube start --cni=calico`.

→ Bắt đầu: [Bài 25](25-cluster-setup/)
