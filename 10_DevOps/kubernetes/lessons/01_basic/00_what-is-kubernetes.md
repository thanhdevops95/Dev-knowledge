# 🎓 Kubernetes là gì? — Container orchestration de-facto

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [Docker basics](../../../docker/lessons/01_basic/00_what-is-docker.md), [Linux intermediate](../../../../04_OS/linux/lessons/02_intermediate/00_users-and-permissions.md)

> 🎯 *Bài INTRO. Hiểu **K8s là gì**, **vs Docker Compose** (khi nào dùng cái nào), **architecture** (control plane + nodes), **3 distro local** (minikube/kind/k3s), **kubectl** intro, **declarative YAML**, **landscape 2026** (managed K8s, alternatives). KHÔNG dạy Pod/Deployment chi tiết (bài 01 trở đi).*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **K8s** + history (2014 Google → de-facto standard 2026)
- [ ] So sánh **Docker Compose** vs **K8s** — khi nào dùng cái nào
- [ ] Vẽ được **architecture** (control plane: API server / etcd / scheduler / controller; nodes: kubelet / kube-proxy / container runtime)
- [ ] Install local: **minikube / kind / k3s / Docker Desktop K8s**
- [ ] Dùng **`kubectl`** + autocomplete + context switching
- [ ] Hiểu **declarative** (YAML manifest) vs **imperative** (`kubectl create`)
- [ ] Biết **managed K8s** (EKS/GKE/AKS/DOKS) + alternatives (Nomad, ECS, Cloud Run)
- [ ] **Lộ trình** học K8s 0 → 1

---

## Tình huống — Bạn deploy FastAPI scale 1000 user

Bạn deploy FastAPI ([cluster trước](../../../../07_Web/backend/python-fastapi/)) lên VPS. 1 container, chạy systemd. OK cho dev. Production:

- 😱 1 VPS → 1 instance, fail = downtime.
- 😱 Traffic tăng 10x → CPU 100%, không scale ngang được.
- 😱 Deploy = manual SSH + rebuild + restart → 10 phút downtime.
- 😱 Database, Redis, frontend — 3 service, mỗi cái chạy riêng, monitor riêng.
- 😱 Cần TLS cert renewal, log aggregation, secrets management.

Bạn search "container orchestration" → gặp **Kubernetes**. Người ta nói:
- K8s = "operating system" cho cluster server.
- Auto-scale + self-heal + rolling update.
- De-facto standard cho cloud-native.
- Khó học — "learn K8s" là meme.

Bạn ngơ:
- K8s khác **Docker Compose** thế nào?
- **Pod**, **Deployment**, **Service** — vocab quá nhiều?
- Local test K8s thế nào?
- Production: **DIY** hay **managed** (EKS, GKE)?

→ Bài này tổng quan. Bài 01-04 đi sâu Pod/Service/Config/Namespace.

---

## 1️⃣ Vậy Kubernetes là gì?

**Kubernetes** (= "K8s", "kube") = container orchestration platform — quản lý **cluster** servers chạy **hàng nghìn container** tự động.

- 2014 — Google open-source K8s (kế thừa Borg internal system).
- 2015 — donate to **CNCF** (Cloud Native Computing Foundation).
- 2026 — **de-facto standard**. Mọi cloud provider có managed K8s.

> 🧠 **Ẩn dụ — K8s như HĐH cho cluster:**
> - **1 server** — OS Linux quản process.
> - **N servers** — K8s quản containers across servers.
> - K8s decide: "container này chạy trên server nào, restart khi crash, scale lên 5 replicas khi CPU cao".

### K8s không phải...

Trước khi học K8s, cần **dispel 5 misconception** phổ biến. K8s focus narrow: schedule containers across cluster. Mọi thứ khác (monitoring, CI/CD, service mesh, database) cần thêm tool riêng:

- ❌ K8s **không phải** monitoring (cần Prometheus).
- ❌ K8s **không phải** CI/CD (cần GitHub Actions, ArgoCD).
- ❌ K8s **không phải** service mesh (cần Istio/Linkerd).
- ❌ K8s **không phải** database (cần Operator hoặc external).
- ❌ K8s **không phải** "easier than Docker Compose" — **harder!**

### K8s là...

8 capabilities K8s **làm rất tốt** — orchestration container ở scale. Auto-scale + self-heal + rolling update là 3 thứ làm K8s không thể thiếu cho production lớn:

- ✅ Schedule + run containers on cluster.
- ✅ Auto-scale (HPA based on CPU/RAM/custom metric).
- ✅ Self-heal (restart crashed containers).
- ✅ Rolling update (0 downtime deploy).
- ✅ Service discovery + internal DNS.
- ✅ Secrets + config management.
- ✅ Storage abstraction (PV/PVC).
- ✅ Network policy.

---

## 2️⃣ Docker Compose vs Kubernetes — Khi nào dùng cái nào?

### Docker Compose

Docker Compose là alternative đơn giản cho single-host deployment. 1 file YAML, 1 lệnh `docker compose up`. Đủ cho dev local + single VPS production (~5K users):

```yaml
# docker-compose.yml
services:
  api:
    image: myapp:latest
    ports: ["8000:8000"]
  db:
    image: postgres:18
```

→ Run với `docker compose up`. 1 host, đơn giản.

| Aspect | Docker Compose | Kubernetes |
|---|---|---|
| Cluster size | **1 host** | N hosts |
| Auto-scale | ❌ | ✅ HPA |
| Self-heal | Limited (`restart: always`) | ✅ Full |
| Rolling update | ❌ (manual restart) | ✅ |
| Load balancing | Manual (Nginx) | ✅ Built-in Service |
| Service discovery | DNS via Compose network | ✅ Native (CoreDNS) |
| Learning curve | 1 ngày | **1-3 tháng** |
| Best for | Dev, single host, small prod | Production scale, multi-host |
| Cost | $0 setup | $$$ infra + ops |

### Khi nào chọn gì?

Quy tắc 2026: **đừng vội K8s**. 99% startup years 1-2 dùng Compose là đủ. Pick K8s khi có 3 signals: team 5+ người, microservices > 5, multi-region. Decision matrix:

| Use case | Choose |
|---|---|
| Local dev | **Docker Compose** |
| Single VPS prod (~5K users) | **Docker Compose** + systemd OK |
| Medium scale (~50K users), 1-3 services | **Docker Compose** + Caddy reverse proxy |
| Multi-host, auto-scale, 10+ services | **K8s** |
| Cloud-native team (microservices) | **K8s** |
| Solo dev, MVP startup | **Docker Compose** |
| Series A startup, enterprise | **K8s** managed (EKS/GKE) |

> 💡 **Quy tắc 2026**: **đừng vội** K8s. Compose / systemd / Caddy đủ cho 99% startup years 1-2. K8s khi: team 5+, microservices, multi-region.

---

## 3️⃣ Architecture — Control plane + nodes

K8s cluster chia 2 phần: **Control plane** (API server + etcd + scheduler + controller manager — "brain") và **Worker nodes** (kubelet + container runtime — chạy actual workload). Diagram architecture:

```
                   ┌─────────────────────────────┐
                   │      CONTROL PLANE           │
                   │  ┌────────┐  ┌───────────┐   │
                   │  │  API   │  │   etcd    │   │
                   │  │ Server │  │  (state)  │   │
                   │  └────┬───┘  └───────────┘   │
                   │       │                        │
                   │  ┌────┴────┐  ┌──────────┐   │
                   │  │Scheduler│  │Controller│   │
                   │  │         │  │  Manager │   │
                   │  └─────────┘  └──────────┘   │
                   └──────────────┬───────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                ▼                 ▼                 ▼
        ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
        │   NODE 1    │   │   NODE 2    │   │   NODE 3    │
        │             │   │             │   │             │
        │ ┌─────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │
        │ │ kubelet │ │   │ │ kubelet │ │   │ │ kubelet │ │
        │ └─────────┘ │   │ └─────────┘ │   │ └─────────┘ │
        │ ┌─────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │
        │ │kube-prxy│ │   │ │kube-prxy│ │   │ │kube-prxy│ │
        │ └─────────┘ │   │ └─────────┘ │   │ └─────────┘ │
        │ ┌─────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │
        │ │container│ │   │ │container│ │   │ │container│ │
        │ │ runtime │ │   │ │ runtime │ │   │ │ runtime │ │
        │ └─────────┘ │   │ └─────────┘ │   │ └─────────┘ │
        │ [Pods]      │   │ [Pods]      │   │ [Pods]      │
        └─────────────┘   └─────────────┘   └─────────────┘
```

### Control plane components

| Component | Vai trò |
|---|---|
| **API server** | Single source of truth — kubectl + everything go through it (REST API) |
| **etcd** | Key-value store — lưu cluster state (config, secrets, ...) |
| **Scheduler** | Decide pod nào chạy node nào (resource available, affinity) |
| **Controller Manager** | Reconcile actual vs desired state (replica count, node health, ...) |
| **Cloud Controller** | Integrate cloud provider (LoadBalancer creation, persistent disks) |

### Node components

| Component | Vai trò |
|---|---|
| **kubelet** | Agent trên node — talk với API server, run containers |
| **kube-proxy** | Network rules — implement Services (iptables/IPVS) |
| **Container runtime** | Run containers (containerd default; before: Docker) |

### Reconciliation loop — Core idea

```
Desired state (YAML manifest):  "10 replicas of nginx"
              │
              ▼
        API server
              │
              ▼
        etcd (save desired)
              │
              ▼
   Controller Manager constantly:
     1. Get desired (from etcd)
     2. Get actual (count running pods)
     3. Diff
     4. Take action (start/stop pods)
              │
              ▼
        Actual = Desired ✓
```

→ K8s **continuously reconcile**. Crash 1 pod → controller detect → restart. Node die → reschedule pods elsewhere.

---

## 4️⃣ Install local — 4 cách

### 1. minikube — Classic

```bash
brew install minikube
minikube start --driver=docker
kubectl get nodes
```

→ Pros: mature, default tutorial. Cons: slow, heavy (1 VM).

### 2. kind (Kubernetes IN Docker) — Recommended

```bash
brew install kind
kind create cluster
kubectl get nodes
```

→ Pros: fast, lightweight (Docker container), multi-node testing. **Recommended 2026 cho test/CI**.

### 3. k3s / k3d — Lightweight production

```bash
# k3d (k3s in Docker)
brew install k3d
k3d cluster create mycluster --servers 1 --agents 2
```

→ Pros: **production-ready** lightweight K8s (Rancher). Used by edge/IoT/small prod. Plus great for laptop.

### 4. Docker Desktop K8s

Mac/Win Docker Desktop có toggle "Enable Kubernetes" trong Settings → install in 1 click. Slow startup.

### Compare

| Distro | Speed | Multi-node | Production-ready | Best for |
|---|---|---|---|---|
| **minikube** | Slow | Yes | No | Tutorials |
| **kind** | Fast | Yes | No | **CI/CD test**, dev |
| **k3s/k3d** | Fast | Yes | **Yes** | Edge, IoT, small prod, dev |
| **Docker Desktop** | Slow | No (single node) | No | Simplicity |

### Test với kind

```bash
kind create cluster --name acme-shop

kubectl cluster-info
# Kubernetes control plane is running at https://127.0.0.1:42323

kubectl get nodes
# NAME                       STATUS   ROLES           AGE   VERSION
# acme-shop-control-plane     Ready    control-plane   30s   v1.31

kind delete cluster --name acme-shop
```

---

## 5️⃣ `kubectl` — CLI master

### Install

```bash
brew install kubectl
# Hoặc tải binary từ kubernetes.io
```

### Concepts cơ bản

```bash
# Get resources
kubectl get nodes                    # List nodes
kubectl get pods                      # Pods (current namespace)
kubectl get pods -A                   # All namespaces
kubectl get pods -n kube-system       # Specific namespace
kubectl get pods -o wide              # More columns
kubectl get pods -o yaml              # YAML
kubectl get pods -l app=myapp         # Label filter

# Describe (detail + events)
kubectl describe pod my-pod
kubectl describe node my-node

# Logs
kubectl logs my-pod
kubectl logs my-pod -f                # Follow
kubectl logs my-pod -c my-container   # Specific container
kubectl logs -l app=myapp --tail=100  # By label

# Exec into pod
kubectl exec -it my-pod -- bash
kubectl exec my-pod -- ls /app

# Port forward (test locally)
kubectl port-forward pod/my-pod 8000:80
# Now localhost:8000 → pod:80

# Apply manifest
kubectl apply -f manifest.yaml
kubectl apply -f directory/

# Delete
kubectl delete pod my-pod
kubectl delete -f manifest.yaml
kubectl delete deployment my-deploy

# Diff before apply
kubectl diff -f manifest.yaml
```

### Context — Switch clusters

```bash
kubectl config get-contexts
kubectl config use-context kind-acme-shop
kubectl config current-context

# Switch namespace
kubectl config set-context --current --namespace=production
```

### Tools improve UX

| Tool | Purpose |
|---|---|
| **kubectx + kubens** | Quick switch context + namespace |
| **k9s** | TUI for K8s — best DX |
| **stern** | Multi-pod log tail |
| **kubectl-aliases** | `k` shortcut |
| **Lens** | GUI desktop app |

```bash
brew install kubectx k9s stern
```

→ **k9s** = "vim for K8s" — fly through cluster.

### Autocomplete

```bash
# Bash
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'alias k=kubectl' >> ~/.bashrc
echo 'complete -F __start_kubectl k' >> ~/.bashrc

# Zsh
echo 'source <(kubectl completion zsh)' >> ~/.zshrc
echo 'alias k=kubectl' >> ~/.zshrc
```

---

## 6️⃣ Declarative YAML vs Imperative

### Imperative — Tell HOW

```bash
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
kubectl expose deployment nginx --port=80
```

→ Quick for testing. KHÔNG track trong git.

### Declarative — Tell WHAT (default 2026)

```yaml
# nginx-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```

```bash
kubectl apply -f nginx-deploy.yaml
```

→ Declarative = git-track YAML. K8s reconcile actual → desired. **Default 2026**.

### Why declarative?

- ✅ **Git track** — version control, code review, rollback.
- ✅ **Idempotent** — apply 10 lần = apply 1 lần.
- ✅ **GitOps** — git push = deploy (ArgoCD/Flux).
- ✅ **Diff** — `kubectl diff -f file.yaml` show changes.

---

## 7️⃣ Managed K8s — Production reality

Self-hosted K8s **rất khó** (upgrade, etcd backup, control plane HA). **2026 reality**: 90% prod K8s = managed.

| Cloud | Service | Pros |
|---|---|---|
| **AWS** | **EKS** | Most mature, expensive |
| **GCP** | **GKE** | Best UX, K8s creators |
| **Azure** | **AKS** | Tight Azure integration |
| **DigitalOcean** | **DOKS** | Simple, cheap (~$12 + nodes) |
| **Linode** | **LKE** | Affordable |
| **Civo** | Managed K3s | Fast cluster create |
| **OVH** | Managed K8s | EU |

### Cost ballpark 2026

| Cluster size | Monthly |
|---|---|
| 1 node (1 cpu, 2GB) | $20-40 |
| 3 nodes (2 cpu, 4GB each) | $80-150 |
| 10 nodes prod | $500-2000 |
| Control plane | Free (EKS $73/mo) |

→ Managed K8s không rẻ. Cân nhắc kỹ ROI vs Docker Compose.

### Alternatives — Not K8s

| Alternative | Notes |
|---|---|
| **AWS ECS / Fargate** | Easier, Amazon-only |
| **GCP Cloud Run** | Serverless containers, autoscale to 0 |
| **Hetzner / Hashicorp Nomad** | Simpler orchestration |
| **Fly.io** | Easier deploy, global |
| **Railway / Render** | Heroku-like, PaaS |
| **Docker Swarm** | Built into Docker, simpler (dying) |

→ **Quy tắc**: cần thật sự K8s? Hay ECS/Cloud Run/Fly đủ?

---

## 8️⃣ Lộ trình học K8s 0 → 1

```
Week 1 — Basics
  ☐ Install kind/k3d local
  ☐ Pod, Deployment, Service (this cluster bài 01-02)
  ☐ kubectl 20 commands
  ☐ Deploy nginx, port-forward

Week 2 — App
  ☐ ConfigMap, Secret (bài 03)
  ☐ Namespace, RBAC (bài 04)
  ☐ Deploy FastAPI + Postgres
  ☐ Ingress + cert-manager

Week 3 — Production
  ☐ Health checks (liveness/readiness)
  ☐ Resource limits + requests
  ☐ HPA (auto-scale)
  ☐ Backup etcd

Week 4 — Ops
  ☐ Monitoring (Prometheus + Grafana)
  ☐ Logging (Loki)
  ☐ CI/CD with ArgoCD
  ☐ Service mesh (Linkerd, optional)
```

→ Sau 4 tuần đủ deploy app simple production. Master cần 6 tháng+.

### Certification

- **CKAD** (Certified Kubernetes Application Developer) — focus dev. **Recommended dev**.
- **CKA** (Certified Kubernetes Administrator) — focus ops.
- **CKS** (Certified Kubernetes Security Specialist) — advanced.

→ Linux Foundation issues. ~$395/exam. Online proctored. Hands-on tasks.

---

## 9️⃣ Hands-on — Deploy FastAPI lên kind

### `app.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: acmeshop/fastapi:latest
        ports:
        - containerPort: 8000

---
apiVersion: v1
kind: Service
metadata:
  name: fastapi
spec:
  selector:
    app: fastapi
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### Deploy

```bash
kind create cluster
docker build -t acmeshop/fastapi:latest .
kind load docker-image acmeshop/fastapi:latest

kubectl apply -f app.yaml
kubectl get pods
# NAME                       READY   STATUS    AGE
# fastapi-xxx-aaa            1/1     Running   30s
# fastapi-xxx-bbb            1/1     Running   30s
# fastapi-xxx-ccc            1/1     Running   30s

kubectl port-forward svc/fastapi 8000:80
curl http://localhost:8000/products
# {"products": [...]}

# Scale up
kubectl scale deployment fastapi --replicas=5

# Rolling update
kubectl set image deployment/fastapi fastapi=acmeshop/fastapi:v2

# Cleanup
kind delete cluster
```

→ **K8s working** với 3 replicas + Service + rolling update. Production needs more (Ingress, ConfigMap, Secrets, ...) — bài 02-04.

---

## ⚠️ 5 pitfall hay vướng

1. **Học K8s ngay khi 1 service** → overkill. Docker Compose + systemd đủ. K8s khi 5+ services.
2. **Self-host control plane** → complex (etcd backup, HA, upgrade). Use managed (EKS/GKE/DOKS).
3. **Quên `--context`** sau khi switch cluster → apply nhầm production. Dùng kubectx + prompt show context.
4. **Stateful workload (DB) trong K8s** → khó (PV, StatefulSet, backup). Managed RDS/Cloud SQL dễ hơn nhiều.
5. **Imperative trong production** → không git-track. Always YAML + `kubectl apply -f`.

---

## ✅ Self-check

1. **K8s** vs **Docker Compose** — khi nào dùng cái nào?
2. **Control plane** có những component nào? Vai trò mỗi cái?
3. Khác **imperative** và **declarative** K8s?
4. Tại sao **kind** hoặc **k3d** tốt hơn **minikube** cho dev 2026?
5. **Managed K8s** (EKS) so với **self-hosted** — pros vs cons?

<details>
<summary>Gợi ý đáp án</summary>

1. **Docker Compose**: 1 host, dev hoặc small prod, simple. **K8s**: multi-host, auto-scale, self-heal, complex micro-services, production scale. Đừng vội K8s — startup years 1-2 thường Compose đủ. K8s khi team 5+, 5+ services, multi-region.

2. **API Server** (REST entry point), **etcd** (key-value store cluster state), **Scheduler** (assign pod to node), **Controller Manager** (reconcile desired vs actual), **Cloud Controller** (integrate cloud provider). Plus nodes có kubelet + kube-proxy + container runtime.

3. **Imperative**: `kubectl create deployment ...` — tell HOW, không track git. **Declarative**: write YAML manifest + `kubectl apply -f` — tell WHAT, git-track, idempotent, GitOps-ready. **Default 2026**: declarative.

4. **kind/k3d** Docker-based — fast start (~30s), low resource, multi-node testing. **minikube** dùng VM — slow start (~2min), heavy. kind đặc biệt tốt cho CI/CD test K8s manifests.

5. **Managed**: control plane HA done (Google/AWS lo), auto-upgrade, integrate cloud (LB, disks), but $$$ + vendor lock. **Self-hosted**: cheaper, control hoàn toàn, but devops nightmare (etcd backup, HA control plane, upgrade chain). 90% prod 2026 = managed.
</details>

---

## ⚡ Cheatsheet

### Install local

```bash
brew install kubectl kind k9s kubectx
kind create cluster
```

### kubectl essentials

```bash
kubectl get pods                  kubectl get pods -A
kubectl get pods -o wide          kubectl describe pod <name>
kubectl logs <pod> -f             kubectl exec -it <pod> -- bash
kubectl apply -f file.yaml        kubectl delete -f file.yaml
kubectl port-forward pod/x 8000:80
kubectl scale deployment x --replicas=5
kubectl rollout status deployment/x
kubectl rollout undo deployment/x
```

### Context

```bash
kubectl config get-contexts
kubectl config use-context <ctx>
kubectx                            # quick switch
kubens                             # quick switch namespace
```

### Distros

```
kind        # Fast, dev/CI
k3d / k3s    # Lightweight, edge/small prod
minikube    # Classic, tutorials
Docker Desktop K8s  # 1-click Mac/Win
```

### Compose vs K8s

```
Compose      K8s
1 host       N hosts
1 day learn   1-3 months
$0           $$$ ops
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Kubernetes / K8s** | Container orchestration platform (Google 2014 → CNCF) |
| **Cluster** | Collection of nodes |
| **Control plane** | "Brain" — API server + etcd + scheduler + controllers |
| **Node** | Worker server chạy containers |
| **Pod** | Smallest unit — 1+ containers chia network/storage |
| **kubectl** | CLI client |
| **kubelet** | Agent trên node, talk control plane |
| **kube-proxy** | Network rules implementation |
| **containerd** | Container runtime (replaces Docker) |
| **etcd** | Key-value store for cluster state |
| **Declarative** | YAML manifest — tell WHAT |
| **Reconciliation loop** | Controllers ensure actual = desired |
| **minikube / kind / k3s / k3d** | Local K8s distros |
| **EKS / GKE / AKS / DOKS** | Managed K8s (AWS/GCP/Azure/DO) |
| **CNCF** | Cloud Native Computing Foundation |
| **CKAD / CKA / CKS** | K8s certifications |
| **k9s** | TUI for K8s |

---

## 🔗 Links

### Trong cluster
- → Tiếp: [Pods & Deployments](01_pods-and-deployments.md)
- ↑ Cluster: [kubernetes README](../../README.md)

### Cross-reference
- [Docker basics](../../../docker/) — K8s build trên Docker concepts
- [Linux intermediate](../../../../04_OS/linux/lessons/02_intermediate/) — server admin foundation
- [TCP/IP](../../../../05_Networking/tcp-ip-fundamentals/) — networking K8s

### External
- 📖 [Kubernetes docs](https://kubernetes.io/docs/) — official
- 📖 [Kubernetes the Hard Way — Kelsey Hightower](https://github.com/kelseyhightower/kubernetes-the-hard-way) — learn by building
- 📖 [Killer Shell — CKAD prep](https://killer.sh/)
- 📖 [Learnk8s](https://learnk8s.io/) — courses
- 📖 [k9s docs](https://k9scli.io/)
- 📖 [CNCF landscape](https://landscape.cncf.io/) — ecosystem 2026

---

> 🎯 *Sau bài này bạn install K8s local + chạy first Pod. Bài kế tiếp đi sâu **Pod + Deployment** — building blocks của K8s app.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước K8s không phải + K8s là + Docker Compose + Khi nào chọn gì + §3 Architecture diagram.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster K8s basic lesson 1/5. Cover: K8s concept + Docker Compose comparison + when to pick + control plane + workers + 7 core resources (Pod/ReplicaSet/Deployment/Service/Ingress/ConfigMap/Secret) + kubectl basics + setup minikube/kind.
