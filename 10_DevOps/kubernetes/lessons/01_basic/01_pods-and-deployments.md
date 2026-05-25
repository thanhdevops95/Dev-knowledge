# 🎓 Pods & Deployments — Building blocks K8s app

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [What is K8s](00_what-is-kubernetes.md)

> 🎯 *Master **Pod** (smallest unit), **Deployment** (production way), **ReplicaSet**, **labels + selectors**, **rolling update + rollback**, **resource requests/limits**, **liveness/readiness probes**, **init containers**, **HPA basics**. Sau bài này deploy app production-grade trên K8s.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Pod** = smallest deployable unit
- [ ] Write **Deployment** YAML đầy đủ
- [ ] Master **kubectl** commands cho Pod/Deployment
- [ ] **Labels + selectors** cho pod discovery
- [ ] **Rolling update + rollback**
- [ ] **Resource requests + limits** (CPU, RAM)
- [ ] **Liveness + readiness probes** — health check
- [ ] **HPA** (Horizontal Pod Autoscaler) intro

---

## Tình huống — Bạn deploy FastAPI lần đầu lên K8s

Bạn create kind cluster, viết YAML đầu tiên:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fastapi
spec:
  containers:
  - name: fastapi
    image: acmeshop/fastapi:latest
```

```bash
kubectl apply -f pod.yaml
kubectl get pods
# fastapi 1/1 Running

kubectl delete pod fastapi
kubectl get pods
# (no pods)   ← KHÔNG tự restart!
```

Bạn ngơ: Pod chết = chết luôn. Sao K8s không **self-heal**?

Senior:
> *"**Pod naked** không có controller — không self-heal. Production luôn dùng **Deployment** wrap Pod. Plus health check, resource limits, rolling update."*

→ Bài này dạy Pod → Deployment → production-grade.

---

## 1️⃣ Pod — Smallest unit

**Pod** = nhóm 1+ containers chia **network + storage + lifecycle**.

### Why Pod, not Container?

K8s không deploy **container đơn lẻ** — luôn wrap trong Pod. **Lý do**: nhiều workload cần 2+ container chạy chung (app + log shipper, app + proxy), và chúng phải chia chung **network namespace** + **volume mount** mới giao tiếp được. Pod là **đơn vị nhỏ nhất** đảm bảo điều đó:

```
┌────────────────────────────────────┐
│         Pod (shared net + IPC)      │
│  ┌──────────────┐  ┌──────────────┐│
│  │  Container 1  │  │  Container 2 ││
│  │  (main app)   │  │  (sidecar)   ││
│  └──────────────┘  └──────────────┘│
│  Shared: localhost, volumes        │
└────────────────────────────────────┘
```

→ **2 container trong 1 pod** = share localhost network + volumes. Use case:
- **Sidecar pattern** — main app + logging agent / proxy / TLS.
- **Init container** — setup runs trước main container.

**99% pods chỉ 1 container**. Sidecar advanced.

### YAML đơn giản

Pod khai báo bằng YAML 4 phần chính: `apiVersion` (v1 cho Pod), `kind` (loại object), `metadata` (tên + labels), `spec` (mô tả container). Đây là **manifest tối giản** chạy 1 container Nginx:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: myapp
spec:
  containers:
  - name: app
    image: nginx:latest
    ports:
    - containerPort: 80
```

```bash
kubectl apply -f pod.yaml
kubectl get pods
# my-pod   1/1   Running   0   10s
```

### Pod lifecycle phases

Pod đi qua **5 phase** trong vòng đời. Khi `kubectl apply` xong, Pod vào `Pending` (chờ scheduler chọn node), rồi `ContainerCreating` (pull image + chạy), rồi `Running`. Nếu crash liên tục, Pod rơi vào `CrashLoopBackOff` — K8s restart với delay tăng dần:

```
Pending → ContainerCreating → Running → Succeeded/Failed
                                  ↓
                              CrashLoopBackOff (restart loop)
```

### Pitfall — Pod chết = chết luôn

Đây là cái bẫy lớn nhất khi mới học K8s. Beginner nghĩ K8s tự động restart mọi thứ — sai. **Raw Pod không có controller** đứng sau, nên xoá là mất luôn, không hồi sinh:

```bash
kubectl delete pod my-pod
kubectl get pods           # Empty
```

→ **Pod no controller** = K8s không restart. Production luôn dùng **Deployment**.

### Khi nào dùng raw Pod?

Vì Pod naked không self-heal, **production tuyệt đối không dùng**. Raw Pod chỉ phục vụ 2 mục đích: debug nhanh (chạy 1 container test trong vài phút) và workload **đặc biệt** chạy 1 lần (Job, CronJob — sẽ học sau):

- ❌ Production app — never.
- ✅ Quick debug/test — `kubectl run nginx --image=nginx`.
- ✅ Job/CronJob (background task).

---

## 2️⃣ Deployment — Production way

**Deployment** = manage Pods với:
- ✅ **Replicas** — N copies.
- ✅ **Self-heal** — crash → restart.
- ✅ **Rolling update** — zero downtime.
- ✅ **Rollback** — undo bad deploy.

### YAML đầy đủ

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
  labels:
    app: fastapi
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
        image: acmeshop/fastapi:v1.0
        ports:
        - containerPort: 8000
```

### Architecture

```
   Deployment
      │
      └── manages ──► ReplicaSet
                          │
                          └── manages ──► Pod 1
                                       ──► Pod 2
                                       ──► Pod 3
```

→ Deployment **không trực tiếp** manage Pod. Đi qua **ReplicaSet** (handle replica count).

### Apply + verify

```bash
kubectl apply -f deployment.yaml

kubectl get deployments
# NAME      READY   UP-TO-DATE   AVAILABLE   AGE
# fastapi   3/3     3            3           30s

kubectl get pods
# fastapi-7f9c-abc   1/1   Running
# fastapi-7f9c-def   1/1   Running
# fastapi-7f9c-ghi   1/1   Running

kubectl get replicasets
# fastapi-7f9c   3   3   3   30s
```

### Self-heal test

```bash
kubectl delete pod fastapi-7f9c-abc

kubectl get pods
# fastapi-7f9c-def   1/1   Running
# fastapi-7f9c-ghi   1/1   Running
# fastapi-7f9c-NEW   0/1   ContainerCreating   ← Auto recreated!
```

→ Deployment **detect** pod missing → ReplicaSet create new. Self-heal ✓.

---

## 3️⃣ Labels + Selectors

**Labels** = key-value tag trên objects. **Selectors** = filter by label.

### Use case

```yaml
metadata:
  labels:
    app: fastapi
    env: production
    version: v1.0
    tier: backend
```

```bash
# Get by label
kubectl get pods -l app=fastapi
kubectl get pods -l env=production
kubectl get pods -l 'app=fastapi,env=production'
kubectl get pods -l 'app in (fastapi, nginx)'
kubectl get pods -l 'env!=test'

# Show labels
kubectl get pods --show-labels
```

### How Deployment finds Pods

```yaml
spec:
  selector:
    matchLabels:
      app: fastapi           # ← Deployment finds Pods với label này
  template:
    metadata:
      labels:
        app: fastapi          # ← Pod labels (must match selector)
```

→ **Selector + template labels phải match**. Sai = Deployment không "see" Pods.

### Add/remove label

```bash
kubectl label pod fastapi-7f9c-abc env=production
kubectl label pod fastapi-7f9c-abc env-          # remove (note trailing -)
```

---

## 4️⃣ Rolling update — Zero downtime deploy

### Trigger

```bash
# Method 1: Edit YAML + apply
# (change image: v1.0 → v2.0)
kubectl apply -f deployment.yaml

# Method 2: Imperative
kubectl set image deployment/fastapi fastapi=acmeshop/fastapi:v2.0

# Method 3: Edit live
kubectl edit deployment/fastapi
# (vim mở, edit, save)
```

### Watch progress

```bash
kubectl rollout status deployment/fastapi
# Waiting for deployment "fastapi" rollout to finish: 1 of 3 updated replicas...
# Waiting for deployment "fastapi" rollout to finish: 2 of 3 updated replicas...
# deployment "fastapi" successfully rolled out

kubectl rollout history deployment/fastapi
# REVISION  CHANGE-CAUSE
# 1         (image v1.0)
# 2         (image v2.0)
```

### Mechanics — Rolling strategy default

```
Initial: 3 Pods v1.0 running

Step 1: Create 1 Pod v2.0 (4 total, 1 unavailable allowed)
Step 2: Wait pod v2.0 ready (readiness probe)
Step 3: Delete 1 Pod v1.0 (3 total: 2 v1.0 + 1 v2.0)
Step 4: Create 1 Pod v2.0 (4 total: 2 v1.0 + 2 v2.0)
Step 5: Delete 1 Pod v1.0 (3 total: 1 v1.0 + 2 v2.0)
... continue until all v2.0
```

→ **maxSurge** = số pod extra cho phép (default 25%). **maxUnavailable** = số pod down chấp nhận (default 25%).

### Customize strategy

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1            # 1 pod extra
      maxUnavailable: 0       # KHÔNG cho down — zero disruption
  # Other type:
  # type: Recreate           # Kill all old → create new (downtime!)
```

### Rollback

```bash
# Undo last
kubectl rollout undo deployment/fastapi

# Undo to specific revision
kubectl rollout undo deployment/fastapi --to-revision=1

# Pause / resume rollout
kubectl rollout pause deployment/fastapi
kubectl rollout resume deployment/fastapi
```

→ **Saved revision** mặc định 10. Production: bug → rollback trong 30s.

---

## 5️⃣ Resource requests + limits

Mỗi container declare CPU/RAM needed + max:

```yaml
spec:
  containers:
  - name: fastapi
    image: acmeshop/fastapi:v1.0
    resources:
      requests:
        memory: "256Mi"           # Minimum guaranteed
        cpu: "250m"               # 0.25 CPU
      limits:
        memory: "512Mi"           # Max — exceed = OOMKilled
        cpu: "500m"               # Max — throttled
```

### Vai trò

| Setting | Tác dụng |
|---|---|
| **requests** | Scheduler dùng để **place pod** trên node có đủ resource |
| **limits** | Kernel enforce — pod **không thể vượt** |

### Memory limit exceed → OOMKilled

```bash
kubectl get pods
# fastapi-xxx   0/1   CrashLoopBackOff

kubectl describe pod fastapi-xxx
# Last State: Terminated
#   Reason: OOMKilled
#   Exit Code: 137
```

→ Pod bị **OOM** (Out Of Memory) → restart loop. Tăng `limits.memory` hoặc fix memory leak.

### CPU limit exceed → throttled

→ Container không bị kill, nhưng CPU bị **throttle** (chạy slower). App response time tăng.

### Best practice

| Pattern | Strategy |
|---|---|
| Burstable | `requests < limits` (most apps) |
| Guaranteed (QoS) | `requests = limits` (databases, critical) |
| BestEffort | Không set (test only, avoid prod) |

### Units

```
CPU:    1   = 1 full core
        1000m = 1 core (millicpu)
        500m = 0.5 core
        100m = 0.1 core (small service)

Memory: 1Gi = 1024^3 bytes (binary)
        1G  = 1000^3 bytes (decimal)
        Use Mi/Gi for K8s (binary)
```

---

## 6️⃣ Health checks — Liveness + Readiness

### Liveness — Restart if dead

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
```

→ K8s gọi `GET /healthz` mỗi 10s. Fail 3 lần liên tiếp → **restart pod**.

### Readiness — Add to Service only when ready

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

→ Pod chưa ready → **không nhận traffic** (loại khỏi Service endpoints). Nhưng KHÔNG restart.

### Startup probe — App start chậm (Java)

```yaml
startupProbe:
  httpGet:
    path: /startup
    port: 8000
  failureThreshold: 30
  periodSeconds: 10
  # → cho phép 300s để startup (30 × 10)
```

→ App Java/Rails startup 60-90s. Startup probe cho phép time, liveness chỉ fire **sau khi** startup OK.

### Endpoint trong FastAPI

```python
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    if not db.is_connected():
        raise HTTPException(503, "DB not ready")
    return {"status": "ready"}
```

→ **Distinguish**:
- **Liveness** = "process còn alive?" → simple check.
- **Readiness** = "ready serve traffic?" → check DB, cache, dependency.

### 3 probe types

| Probe | Mechanism |
|---|---|
| `httpGet` | HTTP request — most common |
| `tcpSocket` | TCP port open? |
| `exec` | Run command inside container |

```yaml
livenessProbe:
  exec:
    command: ["cat", "/tmp/healthy"]
```

---

## 7️⃣ Init containers — Pre-start setup

```yaml
spec:
  initContainers:
  - name: wait-for-db
    image: busybox
    command: ['sh', '-c', 'until nc -z postgres 5432; do sleep 1; done']
  containers:
  - name: app
    image: myapp:latest
```

→ **Init containers** chạy **trước** main containers. Đảm bảo dependency ready (DB up, migration done, secrets fetched).

### Use cases

```yaml
initContainers:
  # 1. Wait for service
  - name: wait-db
    command: ['sh', '-c', 'until nc -z postgres 5432; do sleep 1; done']

  # 2. Run migration
  - name: migrate
    image: myapp:latest
    command: ['alembic', 'upgrade', 'head']

  # 3. Fetch secret/config
  - name: fetch-config
    command: ['curl', '-o', '/config/app.json', 'http://config-server/app']
```

---

## 8️⃣ HPA — Horizontal Pod Autoscaler

Auto-scale Pods theo CPU/memory/custom metric.

### Setup

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70    # Scale up khi CPU > 70%
```

```bash
kubectl apply -f hpa.yaml
kubectl get hpa
# NAME      TARGETS   MINPODS   MAXPODS   REPLICAS
# fastapi   45%/70%   3         10        3

# Stress test
kubectl run -it stress --image=busybox --rm -- sh
$ while true; do wget -q -O- http://fastapi/; done

kubectl get hpa --watch
# fastapi   89%/70%   3   10   5      ← Auto scaled up!
```

### Prerequisites

```bash
# metrics-server cần
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

→ Custom metrics (HTTP requests/s, queue depth) cần **Prometheus Adapter**.

---

## 9️⃣ Hands-on — Deploy FastAPI production-grade

### `deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
  labels:
    app: fastapi
    env: production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  selector:
    matchLabels:
      app: fastapi

  template:
    metadata:
      labels:
        app: fastapi
        env: production
    spec:
      initContainers:
      - name: wait-for-db
        image: busybox
        command: ['sh', '-c', 'until nc -z postgres 5432; do sleep 1; done']

      containers:
      - name: fastapi
        image: acmeshop/fastapi:v1.0
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8000

        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        livenessProbe:
          httpGet:
            path: /healthz
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5

        env:
        - name: DATABASE_URL
          value: postgresql://user:pass@postgres:5432/myapp
        # Better: use ConfigMap + Secret (bài 03)

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Deploy + verify

```bash
kubectl apply -f deployment.yaml

kubectl get all
# NAME             TYPE      READY   AGE
# deployment/fastapi  3/3   30s
# replicaset/...     3/3   30s
# pod/fastapi-xxx-1  1/1   30s
# pod/fastapi-xxx-2  1/1   30s
# pod/fastapi-xxx-3  1/1   30s
# hpa/fastapi        3/3   30s

kubectl rollout status deployment/fastapi
kubectl logs -l app=fastapi --tail=20

# Update
kubectl set image deployment/fastapi fastapi=acmeshop/fastapi:v1.1
kubectl rollout status deployment/fastapi
```

→ Production-grade: 3 replicas, rolling update, health check, resource limit, auto-scale. **Real K8s app**.

→ Bài kế tiếp dạy **Service + Ingress** để expose ra ngoài.

---

## ⚠️ 5 pitfall hay vướng

1. **Pod naked production** → no self-heal. Always Deployment.
2. **Selector mismatch template labels** → Deployment không see pods, replicas = 0 forever.
3. **No resource limits** → 1 pod hog cả node → other pods evicted. Always set limits.
4. **Liveness probe = readiness probe** → init slow restart loop. Use **startup probe** cho app startup chậm.
5. **`maxUnavailable: 25%`** mặc định + 4 replicas → 1 pod down OK. Production critical: `maxUnavailable: 0` + `maxSurge: 1`.

---

## ✅ Self-check

1. **Pod** vs **Deployment** — production dùng cái nào, vì sao?
2. Cách K8s **self-heal** Deployment?
3. Khác **liveness** và **readiness** probe?
4. **Resource limits** không set → vấn đề gì?
5. **HPA** scale dựa vào gì?

<details>
<summary>Gợi ý đáp án</summary>

1. **Production = Deployment**. Pod naked không có controller — crash = chết. Deployment manage replicas via ReplicaSet, self-heal, rolling update, rollback. Raw Pod chỉ cho quick test.

2. K8s **reconciliation loop**: Deployment declare `replicas: 3` → ReplicaSet enforce 3 pods alive → controller detect missing pod → schedule new pod. Continuous reconcile.

3. **Liveness**: "process còn alive?" — fail → **restart pod**. **Readiness**: "ready serve traffic?" — fail → **loại khỏi Service endpoints** (no restart). DB connection check fits readiness. App alive check fits liveness.

4. (a) 1 pod hog cả node CPU/RAM → other pods slow/evicted. (b) Scheduler không biết place pod đúng node. (c) Bug memory leak → cả node OOM. Always set requests + limits — minimum guarantee + hard cap.

5. **Resource metrics** (CPU/memory utilization vs request) — default. Plus **custom metrics** (HTTP RPS, queue length) via Prometheus Adapter. Plus **external metrics** (cloud LB queue). HPA scale Pods based on metric average across replicas.
</details>

---

## ⚡ Cheatsheet

### Deployment template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels: { app: app }
  template:
    metadata:
      labels: { app: app }
    spec:
      containers:
      - name: app
        image: myapp:v1
        ports: [{ containerPort: 8000 }]
        resources:
          requests: { memory: "256Mi", cpu: "250m" }
          limits:   { memory: "512Mi", cpu: "500m" }
        livenessProbe:
          httpGet: { path: /healthz, port: 8000 }
        readinessProbe:
          httpGet: { path: /ready, port: 8000 }
```

### kubectl Deployment

```bash
kubectl apply -f deploy.yaml
kubectl get deployments
kubectl rollout status deployment/app
kubectl rollout history deployment/app
kubectl rollout undo deployment/app
kubectl set image deployment/app app=myapp:v2
kubectl scale deployment/app --replicas=5
kubectl describe deployment app
```

### Labels

```bash
kubectl get pods -l app=fastapi
kubectl label pod x env=prod
kubectl label pod x env-                          # remove
```

### Probes

```yaml
livenessProbe:
  httpGet:    { path: /healthz, port: 8000 }
readinessProbe:
  httpGet:    { path: /ready, port: 8000 }
startupProbe:
  httpGet:    { path: /startup, port: 8000 }
  failureThreshold: 30
```

### HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: app }
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Pod** | 1+ containers share network + storage |
| **Deployment** | Manage Pods via ReplicaSet — production way |
| **ReplicaSet** | Maintain N replicas of Pod |
| **Labels** | Key-value tags |
| **Selectors** | Filter by label |
| **Rolling update** | Replace pods gradually (zero downtime) |
| **`maxSurge` / `maxUnavailable`** | Update strategy parameters |
| **Liveness probe** | Health check → restart if fail |
| **Readiness probe** | Ready check → remove from Service if fail |
| **Startup probe** | Initial check for slow-start apps |
| **Init container** | Run before main containers |
| **Resource requests** | Minimum guaranteed |
| **Resource limits** | Maximum allowed (kernel enforce) |
| **OOMKilled** | Pod killed exceed memory limit |
| **HPA** | Horizontal Pod Autoscaler |

---

## 🔗 Links

### Trong cluster
- ← Trước: [What is Kubernetes](00_what-is-kubernetes.md)
- → Tiếp: [Services & Networking](02_services-and-networking.md)
- ↑ Cluster: [kubernetes README](../../README.md)

### External
- 📖 [K8s docs — Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- 📖 [K8s docs — Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- 📖 [K8s docs — Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- 📖 [HPA walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)

---

> 🎯 *Sau bài này deploy app production-grade. Bài kế tiếp dạy **Service + Ingress** — expose ra ngoài + load balance.*

---

## 📜 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Why Pod + YAML đơn giản + Pod lifecycle + Pitfall + Khi nào dùng raw Pod.
- **v1.0.0 (23/05/2026)** — Bản đầu tiên. K8s sprint #1.
