# GIẢI THÍCH CHI TIẾT CÁC KHÁI NIỆM KUBERNETES

## 1. POD
**Pod là smallest deployable unit trong Kubernetes**

### Pod là gì?
- Pod là nhóm một hoặc nhiều containers (thường là 1)
- Cùng share: network namespace, storage volumes
- Cùng lifecycle: cùng start/stop/restart
- Cùng IP address và port space

### Trong project này:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: curl-pod
  labels:
    app: curl-app
    tier: frontend
spec:
  containers:
  - name: curl-container
    image: curlimages/curl:latest
```
- `metadata.name`: Tên của Pod
- `metadata.labels`: Tags để identify và select
- `spec.containers`: Định nghĩa container trong Pod

### Kiểm tra:
```bash
kubectl get pods                    # List tất cả Pods
kubectl get pods -o wide           # Thêm node và IP
kubectl describe pod curl-pod      # Chi tiết
kubectl logs curl-pod              # Logs
kubectl exec -it curl-pod -- sh    # Vào inside Pod
```

## 2. NODE
**Node là worker machine chạy Pods**

### Node là gì?
- Physical server hoặc Virtual Machine
- Chạy: Kubelet, container runtime (Docker/containerd), kube-proxy
- Có:
  - Internal IP (cluster network)
  - External IP (internet-facing)
  - Tài nguyên: CPU, Memory, Storage

### Trong K8s:
```bash
kubectl get nodes                 # List nodes
kubectl describe node <node-name> # Chi tiết node
kubectl top node                  # Resource usage
```

### Output ví dụ:
```
NAME       STATUS   ROLES           AGE   VERSION
node-1     Ready    control-plane   10d   v1.28.0
node-2     Ready    <none>          10d   v1.28.0
```

### Cách Pod được schedule lên Node:
1. Scheduler chọn Node phù hợp (resources, taints, etc.)
2. Kubelet trên Node đó tạo và quản lý Pod
3. Pod được gán IP từ cluster network

## 3. LABELS & SELECTORS
**Labels và Selectors là cách grouping và discovering resources**

### Labels (Nhãn)
- Key-value pairs đánh dấu resources
- Flexible, user-defined
- Có thể thêm/sửa/xóa sau khi tạo

```yaml
metadata:
  labels:
    app: curl-app        # Ứng dụng nào
    tier: backend        # Layer nào (frontend/backend/db)
    environment: dev     # Môi trường
    version: v1          # Version
    team: platform       # Team sở hữu
```

### Selectors (Bộ chọn)
- Dùng labels để chọn/match resources
- Dùng trong:
  - Service → Selects Pods để route traffic
  - ReplicaSet/Deployment → Selects Pods để quản lý
  - kubectl commands → Filter resources

```yaml
# Deployment selector
selector:
  matchLabels:
    app: curl-app
    tier: backend

# Service selector
selector:
  app: curl-app
  tier: backend
```

### Cách hoạt động:
1. Deployment có selector `app=curl-app, tier=backend`
2. Deployment tạo Pod với labels giống selector
3. Service có selector giống nhau
4. Service tự động kết nối đến các Pods có labels phù hợp

### Best practices cho labels:
```
app.kubernetes.io/name: curl-app
app.kubernetes.io/instance: prod-1
app.kubernetes.io/version: v1.2.3
app.kubernetes.io/component: backend
app.kubernetes.io/part-of: fullstack-app
```

### Query với labels:
```bash
kubectl get pods -l app=curl-app
kubectl get pods -l tier=backend
kubectl get pods -l 'environment in (dev,staging)'
kubectl get pods -l 'app=curl-app,tier=backend'
```

## 4. REPLICASET
**ReplicaSet đảm bảo số lượng Pods luôn chạy**

### ReplicaSet là gì?
- Đảm bảo số lượng Pods (`replicas`) luôn chạy
- Theo dõi Pods bằng labels/selector
- Tạo mới Pod nếu có Pod fail/terminate
- Scale up/down số Pods

### Trong project:
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: curl-app
      tier: backend
```

### Cách hoạt động:
1. `replicas: 3` → ReplicaSet tạo 3 Pods
2. Mỗi Pod có labels `app=curl-app, tier=backend`
3. Nếu 1 Pod fail → ReplicaSet tạo Pod mới
4. Nếu có 4 Pods (thủ công) → ReplicaSet xóa 1 để giữ 3

### Commands:
```bash
kubectl scale deployment curl-deployment --replicas=5   # Scale to 5
kubectl get rs                                     # List ReplicaSets
kubectl describe rs curl-deployment-xxxxx          # Chi tiết
```

### ReplicaSet vs Deployment:
- **ReplicaSet**: Chỉ quản lý số lượng Pods
- **Deployment**: Quản lý ReplicaSet + rolling updates + rollback
- **LUÔN dùng Deployment** thay vì ReplicaSet trực tiếp

## 5. DEPLOYMENT
**Deployment quản lý ReplicaSet và cung cấp updates/rollback**

### Deployment là gì?
- Declarative updates cho Pods và ReplicaSets
- Rolling updates: update từng Pod, không downtime
- Rollback: quay về version cũ nếu có lỗi
- Scale: thay đổi số replicas

### Trong project:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: curl-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: curl-app
      tier: backend
  template:
    metadata:
      labels:
        app: curl-app
        tier: backend
    spec:
      containers:
      - name: curl-container
        image: curlimages/curl:latest
```

### Workflow:
1. `kubectl apply -f curl-deployment.yaml`
2. Deployment tạo ReplicaSet
3. ReplicaSet tạo 3 Pods từ `spec.template`
4. Pods running với labels khớp selector
5. Update image: `kubectl set image deployment/curl-deployment curl-container=curlimages/curl:8.5.0`
6. Deployment tạo ReplicaSet mới, update từng Pod

### Commands:
```bash
kubectl get deployments
kubectl describe deployment curl-deployment
kubectl rollout status deployment/curl-deployment  # Xem rollout status
kubectl rollout history deployment/curl-deployment # Xem history
kubectl rollout undo deployment/curl-deployment    # Rollback
kubectl set image deployment/curl-deployment curl-container=curlimages/curl:8.5.0
```

## 6. PORTS TRONG KUBERNETES
**Các loại port khác nhau trong K8s**

### Container Port
- Port chạy bên trong container
- Định nghĩa trong container spec
- Chỉ để document, không tự động mở firewall

```yaml
containers:
- name: curl-container
  ports:
  - containerPort: 8080  # Container lắng nghe port này
    name: http
```

### Service Ports
Service có 3 loại port:

#### 1. port (Service port)
- Port của Service trong cluster
- Pods khác trong cluster access qua port này
- Virtual IP (ClusterIP)

```yaml
ports:
- port: 80           # Service port trong cluster
```

#### 2. targetPort
- Port của Pod/Pod container mà Service forward tới
- Phải khớp với `containerPort` của Pod

```yaml
ports:
- targetPort: 8080   # Pod containerPort
```

#### 3. nodePort (chỉ với NodePort service)
- Port mở trên mỗi Node trong cluster
- Range: 30000-32767 (default)
- External traffic access qua: `<NodeIP>:<nodePort>`

```yaml
ports:
- nodePort: 30080    # Port trên mỗi Node
```

### Ví dụ hoàn chỉnh:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: curl-service
spec:
  selector:
    app: curl-app
  ports:
  - name: http
    port: 80          # Service port (cluster)
    targetPort: 8080  # Pod port
    nodePort: 30080   # Node port (external)
  type: NodePort
```

### Flow traffic:
```
External: http://<NodeIP>:30080
    ↓ (NodePort)
Service (ClusterIP: 10.96.x.x:80)
    ↓ (kube-proxy iptables/ipvs)
Pod (10.244.x.x:8080)
    ↓
Container (localhost:8080)
```

## 7. NODEPORT SERVICE
**NodePort expose service ra external network**

### NodePort là gì?
- Mở một port trên MỌI Node trong cluster
- Port range: 30000-32767 (có thể thay đổi)
- External clients access qua `<NodeIP>:<nodePort>`

### Trong project:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: curl-service
spec:
  type: NodePort
  selector:
    app: curl-app
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080
```

### Cách hoạt động:
1. Tạo Service với `type: NodePort`
2. K8s tự động allocate nodePort (30000-32767) nếu không chỉ định
3. Kube-proxy config iptables/ipvs rules trên mỗi Node
4. Traffic đến `<NodeIP>:30080` được forward tới Service
5. Service load balance đến các Pods khớp selector

### Access methods:

#### Method 1: Direct Node IP
```bash
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
curl http://$NODE_IP:30080
```

#### Method 2: Minikube
```bash
minikube service curl-service
# Mở browser tự động
```

#### Method 3: Port-forward (không cần NodePort)
```bash
kubectl port-forward service/curl-service 8080:80
# Access http://localhost:8080
```

#### Method 4: NodePort với External IP
Nếu Node có External IP:
```bash
EXTERNAL_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}')
curl http://$EXTERNAL_IP:30080
```

### Limitations của NodePort:
- Chỉ 1 service có thể dùng 1 nodePort cụ thể
- Port range giới hạn (có thể clash)
- Không có load balancing thông minh
- Không có TLS termination
- Không có path-based routing

### Khi nào dùng NodePort:
- Development/Testing
- Simple setup không có LoadBalancer
- On-premises clusters

### Alternatives:
- **LoadBalancer**: Tạo cloud load balancer (AWS ELB, GCP LB, Azure LB)
- **Ingress**: HTTP routing, SSL termination, name-based virtual hosting
- **HostPort**: Direct port trên host (không recommended)

## 8. YAML TRONG KUBERNETES
**YAML format để define K8s resources**

### YAML basics:
```yaml
# Comment
key: value                  # Key-value pair
object:                    # Dictionary/Map
  key1: value1
  key2: value2
  nested:
    key3: value3
list:                      # Array/List
  - item1
  - item2
  - item3
```

### YAML trong K8s:
```yaml
apiVersion: v1              # API version của resource
kind: Pod                   # Loại resource (Pod, Service, Deployment...)
metadata:                   # Metadata của resource
  name: my-pod              # Tên
  labels:                   # Labels
    app: my-app
  namespace: default        # Namespace (default nếu không có)
spec:                       # Specification của resource
  containers:
  - name: my-container
    image: nginx:latest
    ports:
    - containerPort: 80
```

### Required fields:
1. `apiVersion`: Group/Version (v1, apps/v1, batch/v1...)
2. `kind`: Type của resource
3. `metadata.name`: Tên resource
4. `spec`: Configuration cụ thể của resource

### YAML syntax rules:
- Indentation với spaces (KHÔNG dùng tabs)
- 2 spaces per level (convention)
- No trailing spaces
- Use quotes for special characters: `"value: with: colons"`
- Boolean: `true`/`false` (không quotes)
- Null: `null` hoặc `~`

### Multi-line strings:
```yaml
# Literal block scalar (|
description: |
  This is line 1
  This is line 2
  Empty lines preserved

# Folded block scalar (>)
description: >
  This is line 1
  This is line 2
  Newlines folded to spaces
```

### Arrays:
```yaml
ports:
- name: http
  port: 80
- name: https
  port: 443
```

### Anchors & Aliases (reuse):
```yaml
labels: &default-labels
  app: my-app
  version: v1

deployment:
  metadata:
    labels: *default-labels
```

### Validate YAML:
```bash
# Syntax check
kubectl apply -f pod.yaml --dry-run=client

# Validate against schema
kubectl create --dry-run=client -f pod.yaml

# Online validator
# https://www.yamllint.com/
```

### Tips:
- Keep YAML minimal, only necessary fields
- Use comments to explain WHY
- Use consistent indentation
- Validate YAML before apply
- Version control all YAML files

## TỔNG KẾT FLOW

### Tạo và deploy ứng dụng:
```
1. Viết YAML files:
   - Pod/Deployment: Định nghĩa containers
   - Service: Expose Pods
   - ConfigMap/Secret: Configuration

2. Apply to cluster:
   kubectl apply -f <file>

3. Kiểm tra:
   kubectl get pods,svc,deploy

4. Test:
   kubectl port-forward svc/name 8080:80
   curl http://localhost:8080

5. Debug:
   kubectl logs <pod>
   kubectl describe <resource>
   kubectl exec -it <pod> -- sh
```

### Cách Pods chạy:
```
Node (máy vật lý/VM)
  ├── Kubelet (quản lý Pods)
  ├── Container Runtime (Docker/containerd)
  └── Kube-proxy (network proxy)
       ↓
    Pod (IP: 10.244.x.x)
       ├── Container 1 (curl)
       │    └── Port 8080
       └── [More containers...]
       ↓
    Service (ClusterIP: 10.96.x.x:80)
       ↓ (Selector: app=curl-app)
    ReplicaSet (3 replicas)
       ↓
    Deployment (manages ReplicaSet)
```

### Cách traffic flow với NodePort:
```
Internet/Your Laptop
    ↓ http://<NodeIP>:30080
Node (any node in cluster)
    ↓ (iptables/ipvs rules by kube-proxy)
Service ClusterIP (10.96.x.x:80)
    ↓ (kube-proxy load balancing)
Pod 1 (10.244.1.5:8080)
    OR
Pod 2 (10.244.2.7:8080)
    OR
Pod 3 (10.244.3.2:8080)
    ↓
Container (localhost:8080)
```

## CÁC COMMANDS QUAN TRỌNG

### Resources:
```bash
kubectl get pods,svc,deploy,rs,pvc,cm,secret,nodes
kubectl get all --all-namespaces
kubectl get pods -o wide
kubectl describe <type> <name>
kubectl logs <pod-name>
```

### Apply/Delete:
```bash
kubectl apply -f <file-or-dir>
kubectl delete -f <file-or-dir>
kubectl delete pod <pod-name>
kubectl scale deploy <name> --replicas=5
```

### Exec/Port-forward:
```bash
kubectl exec -it <pod> -- /bin/sh
kubectl port-forward svc/<service> <local-port>:<remote-port>
kubectl port-forward pod/<pod> <local-port>:<container-port>
```

### Update/Replace:
```bash
kubectl set image deployment/<name> <container>=<new-image>
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout history deployment/<name>
```

### Labels:
```bash
kubectl get pods -l app=curl-app
kubectl label pods <pod> version=v2
kubectl get pods --show-labels
```

## TROUBLESHOOTING CHECKLIST

1. Pod not running?
   ```bash
   kubectl describe pod <pod>
   kubectl logs <pod>
   Check image name, resource limits, node capacity
   ```

2. Service not working?
   ```bash
   kubectl get endpoints <service>  # Phải có endpoints
   kubectl describe service <service>
   Check selector labels match pod labels
   ```

3. Cannot access from outside?
   ```bash
   kubectl get svc  # Check NodePort assigned (30000-32767)
   Firewall: allow NodePort range
   Check Node IP: kubectl get nodes -o wide
   ```

4. Pods keep restarting?
   ```bash
   kubectl logs <pod> --previous  # Logs của container cũ
   Check livenessProbe/readinessProbe
   Check resource limits/requests
   ```

5. Node has no resources?
   ```bash
   kubectl top nodes
   kubectl describe node <node>
   Check allocatable resources
   ```

## NEXT LEARNING STEPS

1. **Namespace**: Phân tách environments (dev/staging/prod)
2. **Ingress**: HTTP routing, SSL, multiple domains
3. **ConfigMap & Secret**: Manage configuration and secrets
4. **PersistentVolume & PVC**: Storage cho stateful apps
5. **StatefulSet**: Cho databases (MySQL, PostgreSQL, MongoDB)
6. **DaemonSet**: Chạy Pod trên mọi Node (logging, monitoring)
7. **HorizontalPodAutoscaler**: Auto-scale based on CPU/memory
8. **Jobs & CronJob**: Tasks chạy một lần hoặc định kỳ
9. **Service Mesh**: Istio, Linkerd (advanced networking)
10. **Helm**: Package manager cho K8s

## RESOURCES
- Official Docs: https://kubernetes.io/docs/home/
- Interactive Tutorial: https://kubernetes.io/docs/tutorials/kubernetes-basics/
- Katacoda: https://www.katacoda.com/courses/kubernetes
- K8s Concepts: https://kubernetes.io/docs/concepts/
