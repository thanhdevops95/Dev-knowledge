# 📝 Quiz & Self-Test - Kubernetes

Kiểm tra kiến thức Kubernetes của bạn với 20 câu hỏi từ cơ bản đến nâng cao.

**Hướng dẫn:** Trả lời câu hỏi trước, sau đó xem đáp án bên dưới.

---

## 🟢 Cơ bản (1-7)

### Q1: Pod là gì?

- [ ] A. Một container đơn lẻ
- [ ] B. Đơn vị nhỏ nhất có thể deploy trong K8s
- [ ] C. Một virtual machine
- [ ] D. Một node trong cluster

<details>
<summary>💡 Đáp án</summary>

**B đúng**

Pod là đơn vị nhỏ nhất trong Kubernetes:

- Có thể chứa 1 hoặc nhiều containers
- Containers trong Pod share network namespace
- Pod có 1 IP address

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: app
      image: nginx
    - name: sidecar  # Có thể có nhiều containers
      image: busybox
```

</details>

---

### Q2: Deployment vs Pod

Tại sao dùng Deployment thay vì tạo Pod trực tiếp?

- [ ] A. Deployment chạy nhanh hơn
- [ ] B. Deployment quản lý replicas và rolling updates
- [ ] C. Pod không thể tạo trực tiếp
- [ ] D. Deployment dùng ít resources hơn

<details>
<summary>💡 Đáp án</summary>

**B đúng**

Deployment cung cấp:

- **Replicas**: Chạy nhiều Pods giống nhau
- **Rolling updates**: Update không downtime
- **Rollback**: Quay lại version cũ
- **Self-healing**: Tự tạo Pod mới khi Pod chết

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3  # 3 Pods luôn running
  template:
    spec:
      containers:
        - name: app
          image: nginx:1.20
```

</details>

---

### Q3: Service Types

ClusterIP Service khác NodePort như thế nào?

<details>
<summary>💡 Đáp án</summary>

| Type | Accessible from | Use case |
|------|-----------------|----------|
| **ClusterIP** | Chỉ trong cluster | Internal services |
| **NodePort** | Bên ngoài qua NodeIP:Port | Testing, simple external |
| **LoadBalancer** | Internet qua cloud LB | Production public |

```yaml
# ClusterIP (default)
spec:
  type: ClusterIP
  ports:
    - port: 80
# Chỉ access: http://my-service:80 (trong cluster)

# NodePort
spec:
  type: NodePort
  ports:
    - port: 80
      nodePort: 30080
# Access: http://node-ip:30080 (từ ngoài)
```

</details>

---

### Q4: ConfigMap vs Secret

Khi nào dùng ConfigMap vs Secret?

<details>
<summary>💡 Đáp án</summary>

| ConfigMap | Secret |
|-----------|--------|
| Non-sensitive config | Sensitive data |
| Plain text | Base64 encoded |
| Database host, log level | Passwords, API keys |

```yaml
# ConfigMap - config thường
apiVersion: v1
kind: ConfigMap
data:
  LOG_LEVEL: "info"

# Secret - sensitive
apiVersion: v1
kind: Secret
type: Opaque
data:
  password: cGFzc3dvcmQxMjM=  # base64
```

**Lưu ý:** Secret chỉ base64 encoded, **KHÔNG encrypted** by default!

</details>

---

### Q5: kubectl Commands

Lệnh nào xem logs của Pod?

- [ ] A. kubectl describe pod
- [ ] B. kubectl get pod
- [ ] C. kubectl logs pod
- [ ] D. kubectl exec pod

<details>
<summary>💡 Đáp án</summary>

**C đúng**

```bash
kubectl logs mypod              # Logs của container chính
kubectl logs mypod -c sidecar   # Logs của container specific
kubectl logs mypod -f           # Follow logs
kubectl logs mypod --previous   # Logs trước khi crash
```

Các lệnh khác:

- `describe`: Chi tiết + events
- `get`: Status summary
- `exec`: Chạy command trong container

</details>

---

### Q6: Namespace

Namespace dùng để làm gì?

- [ ] A. Tăng performance
- [ ] B. Logical separation của resources
- [ ] C. Backup data
- [ ] D. Connect nhiều clusters

<details>
<summary>💡 Đáp án</summary>

**B đúng**

Namespace = Virtual cluster trong cluster:

- Tách biệt environments (dev, staging, prod)
- Resource quotas per namespace
- RBAC per namespace

```bash
# List namespaces
kubectl get ns
# default, kube-system, kube-public

# Create namespace
kubectl create ns staging

# Deploy to specific namespace
kubectl apply -f app.yaml -n staging
```

</details>

---

### Q7: Labels and Selectors

Labels dùng để làm gì?

<details>
<summary>💡 Đáp án</summary>

Labels = Key-value pairs để:

- **Organize** resources
- **Select** resources (Service → Pods, Deployment → Pods)
- **Filter** khi query

```yaml
# Pod with labels
metadata:
  labels:
    app: myapp
    env: production
    version: v1

# Service selector
spec:
  selector:
    app: myapp  # Chọn Pods có label app=myapp
```

```bash
# Filter by labels
kubectl get pods -l app=myapp
kubectl get pods -l 'env in (production, staging)'
```

</details>

---

## 🟡 Trung bình (8-14)

### Q8: Pod Lifecycle

Pod ở status "Pending" nghĩa là gì?

- [ ] A. Pod đang chạy
- [ ] B. Pod đang đợi được schedule
- [ ] C. Pod đã complete
- [ ] D. Pod bị lỗi

<details>
<summary>💡 Đáp án</summary>

**B đúng**

Pod statuses:

- **Pending**: Đợi được schedule lên node
- **Running**: Đang chạy
- **Succeeded**: Completed (Jobs)
- **Failed**: Container exited với error
- **Unknown**: Không thể get status

Pending thường do:

- Không đủ resources trên nodes
- Node selector không match
- PVC chưa bound

</details>

---

### Q9: Probes

Liveness vs Readiness probe khác nhau như thế nào?

<details>
<summary>💡 Đáp án</summary>

| Probe | Purpose | Failure action |
|-------|---------|----------------|
| **Liveness** | Container còn sống không? | Restart container |
| **Readiness** | Container sẵn sàng nhận traffic? | Remove từ Service endpoints |
| **Startup** | Container đã start xong chưa? | Disable liveness/readiness probe |

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
# Fail → Container restart

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5
# Fail → Không nhận traffic, nhưng không restart
```

</details>

---

### Q10: Resource Requests vs Limits

Requests và Limits khác nhau như thế nào?

<details>
<summary>💡 Đáp án</summary>

| | Requests | Limits |
|-|----------|--------|
| **Purpose** | Scheduling | Hard cap |
| **Guarantee** | Minimum guaranteed | Maximum allowed |
| **Exceed** | OK (if available) | CPU throttled, Memory OOM |

```yaml
resources:
  requests:
    memory: "256Mi"  # Scheduler đảm bảo ít nhất 256Mi
    cpu: "250m"
  limits:
    memory: "512Mi"  # Không được dùng quá 512Mi
    cpu: "500m"      # Throttle nếu vượt 500m
```

**Best practice:** requests = 70-80% của limits

</details>

---

### Q11: Horizontal Pod Autoscaler

HPA scale dựa trên gì?

<details>
<summary>💡 Đáp án</summary>

HPA scale Pods dựa trên:

- CPU utilization
- Memory utilization
- Custom metrics

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70  # Scale khi CPU > 70%
```

**Lưu ý:** Pod phải có resource requests để HPA hoạt động.

</details>

---

### Q12: Persistent Volumes

PV, PVC, StorageClass liên quan như thế nào?

<details>
<summary>💡 Đáp án</summary>

```
StorageClass → Định nghĩa HOW to provision storage
      ↓
PersistentVolume (PV) → Actual storage resource
      ↓
PersistentVolumeClaim (PVC) → Request for storage by Pod
      ↓
Pod → Uses PVC as volume
```

```yaml
# StorageClass (admin creates)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3

# PVC (developer creates)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  storageClassName: fast
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 10Gi

# Pod (developer creates)
spec:
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data
```

</details>

---

### Q13: Rolling Update Strategy

`maxSurge` và `maxUnavailable` là gì?

<details>
<summary>💡 Đáp án</summary>

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Có thể TẠO thêm 1 Pod quá replicas
      maxUnavailable: 0  # Không Pod nào được unavailable
```

Với replicas=3:

- **maxSurge: 1** → Có thể có 4 Pods cùng lúc
- **maxUnavailable: 0** → Luôn có 3 Pods ready

Update process:

```
[v1] [v1] [v1]       → Start
[v1] [v1] [v1] [v2]  → Tạo 1 v2 (surge)
[v1] [v1] [v2] [v2]  → Xóa 1 v1, tạo thêm v2
...
[v2] [v2] [v2]       → Done
```

</details>

---

### Q14: Network Policies

Network Policy dùng để làm gì?

<details>
<summary>💡 Đáp án</summary>

Network Policy = Firewall rules cho Pods:

- Ingress: Traffic **vào** Pod
- Egress: Traffic **ra** từ Pod

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - port: 8080
# Backend chỉ nhận traffic từ frontend Pods
```

**Lưu ý:** Cần CNI plugin hỗ trợ (Calico, Weave, Cilium).

</details>

---

## 🔴 Nâng cao (15-20)

### Q15: RBAC

Role vs ClusterRole khác nhau như thế nào?

<details>
<summary>💡 Đáp án</summary>

| | Role | ClusterRole |
|-|------|-------------|
| **Scope** | Namespace-specific | Cluster-wide |
| **Use case** | Namespace resources | Nodes, PVs, cluster resources |

```yaml
# Role (namespace-scoped)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]

# ClusterRole (cluster-wide)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list"]
```

</details>

---

### Q16: Pod Disruption Budget

PDB dùng để làm gì?

<details>
<summary>💡 Đáp án</summary>

PDB = Đảm bảo minimum availability khi có **voluntary disruption**:

- Node drain
- Cluster upgrade
- Deployment updates

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2  # Hoặc: maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

Với minAvailable=2:

- Nếu có 3 Pods, chỉ 1 có thể bị evict cùng lúc
- Node drain sẽ đợi cho đến khi có đủ Pods healthy

</details>

---

### Q17: Taints and Tolerations

Taints và Tolerations hoạt động như thế nào?

<details>
<summary>💡 Đáp án</summary>

- **Taint** = Node nói "Tôi không chấp nhận Pods"
- **Toleration** = Pod nói "Tôi chấp nhận taint đó"

```bash
# Taint node
kubectl taint nodes node1 dedicated=gpu:NoSchedule
```

```yaml
# Pod với toleration
spec:
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "gpu"
      effect: "NoSchedule"
```

Effects:

- **NoSchedule**: Không schedule Pods mới
- **PreferNoSchedule**: Try không schedule
- **NoExecute**: Evict existing Pods

</details>

---

### Q18: Init Containers

Init containers khác regular containers như thế nào?

<details>
<summary>💡 Đáp án</summary>

Init containers:

- Chạy **trước** regular containers
- Chạy **tuần tự** (không parallel)
- Phải **complete** trước khi app containers start
- **Dùng cho**: Setup, wait for dependencies

```yaml
spec:
  initContainers:
    - name: wait-for-db
      image: busybox
      command: ['sh', '-c', 'until nc -z db 5432; do sleep 1; done']
    - name: init-config
      image: busybox
      command: ['sh', '-c', 'cp /config/* /app/']
  containers:
    - name: app
      image: myapp
```

Order: wait-for-db → init-config → app

</details>

---

### Q19: StatefulSet vs Deployment

Khi nào dùng StatefulSet?

<details>
<summary>💡 Đáp án</summary>

| Deployment | StatefulSet |
|------------|-------------|
| Stateless apps | Stateful apps |
| Pods interchangeable | Pods có identity |
| Random Pod names | Ordered Pod names (app-0, app-1) |
| Shared storage OK | Per-Pod storage |

**Use StatefulSet for:**

- Databases (MySQL, PostgreSQL)
- Message queues (Kafka, RabbitMQ)
- Distributed systems (ZooKeeper, etcd)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql
spec:
  serviceName: mysql  # Required
  replicas: 3
  # Pods: mysql-0, mysql-1, mysql-2
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 10Gi
  # Mỗi Pod có PVC riêng
```

</details>

---

### Q20: CRD và Operators

Custom Resource Definitions dùng để làm gì?

<details>
<summary>💡 Đáp án</summary>

CRD = Extend Kubernetes API với custom resources:

```yaml
# CRD definition
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.mycompany.com
spec:
  group: mycompany.com
  names:
    kind: Database
    plural: databases
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
```

```yaml
# Custom Resource
apiVersion: mycompany.com/v1
kind: Database
metadata:
  name: my-postgres
spec:
  engine: postgresql
  version: "15"
  storage: 100Gi
```

**Operator** = Controller + CRD:

- Watches custom resources
- Automates complex operations
- Examples: Prometheus Operator, MongoDB Operator

</details>

---

## 📊 Đánh giá

| Score | Level |
|-------|-------|
| 0-7 | 🟢 Beginner - Cần học thêm basics |
| 8-14 | 🟡 Intermediate - Đang tiến bộ |
| 15-18 | 🔴 Advanced - Hiểu sâu |
| 19-20 | ⭐ Expert - Sẵn sàng interview |

---

[← Về README](README.md) | [LABS.md →](LABS.md) | [SCENARIOS.md →](SCENARIOS.md)
