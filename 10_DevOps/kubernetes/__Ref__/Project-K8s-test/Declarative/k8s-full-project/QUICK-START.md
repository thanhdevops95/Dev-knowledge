# 🚀 QUICK START GUIDE
## Hướng dẫn từng bước để chạy Kubernetes project

---

## 📋 PREREQUISITES

### 1. Cài đặt kubectl
```bash
# Mac với Homebrew
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
kubectl version --client
```

### 2. Cài đặt Kubernetes Cluster

**Option A: Minikube (Recommended for learning)**
```bash
# Mac
brew install minikube
minikube start --memory=4096 --cpus=2

# Verify
kubectl cluster-info
kubectl get nodes
```

**Option B: Docker Desktop**
- Mở Docker Desktop
- Settings → Kubernetes → Enable Kubernetes
- Wait for cluster to start

**Option C: Kind (Kubernetes in Docker)**
```bash
brew install kind
kind create cluster --name learning
kubectl cluster-info
```

### 3. Verify Installation
```bash
kubectl version --client
kubectl cluster-info
kubectl get nodes
```

---

## 📁 PROJECT STRUCTURE

```
k8s-full-project/
├── pods/
│   └── curl-pod.yaml          # Pod đơn lẻ
├── deployments/
│   └── curl-deployment.yaml   # Deployment với 3 replicas
├── services/
│   └── curl-service.yaml      # NodePort Service
├── configmaps/
│   └── curl-config.yaml       # Configuration
├── deploy.sh                  # Script deploy tự động
├── README.md                  # Tài liệu đầy đủ
├── KUBERNETES-EXPLAINED.md    # Giải thích chi tiết từng khái niệm
└── QUICK-START.md            # File này
```

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### Bước 1: Navigate vào thư mục project
```bash
cd /Users/rom/K8S/Project_K8s_Test/Declarative/k8s-full-project
```

### Bước 2: Chạy script deploy tự động (Recommended)
```bash
./deploy.sh
```

**OR** chạy thủ công từng bước:

### Bước 2a: Apply ConfigMap
```bash
kubectl apply -f configmaps/
```
Expected output:
```
configmap/curl-config created
```

### Bước 2b: Apply Pod (optional - để xem Pod đơn lẻ)
```bash
kubectl apply -f pods/
```
Expected:
```
pod/curl-pod created
```

### Bước 2c: Apply Deployment
```bash
kubectl apply -f deployments/
```
Expected:
```
deployment.apps/curl-deployment created
```

### Bước 2d: Apply Service
```bash
kubectl apply -f services/
```
Expected:
```
service/curl-service created
```

### Bước 3: Wait for Pods to be Ready
```bash
# Xem status
kubectl get pods --watch

# Hoặc chờ khoảng 30 giây rồi check:
sleep 30
kubectl get pods
```

Expected output:
```
NAME                                READY   STATUS    RESTARTS   AGE
curl-deployment-74f59d59bf-abc12   1/1     Running   0          30s
curl-deployment-74f59d59bf-def34   1/1     Running   0          30s
curl-deployment-74f59d59bf-ghi56   1/1     Running   0          30s
curl-pod                            1/1     Running   0          2m
```

### Bước 4: Kiểm tra tất cả resources
```bash
kubectl get all
```

Expected output:
```
NAME                                    READY   STATUS    RESTARTS   AGE
pod/curl-deployment-74f59d59bf-abc12   1/1     Running   0          1m
pod/curl-deployment-74f59d59bf-def34   1/1     Running   0          1m
pod/curl-deployment-74f59d59bf-ghi56   1/1     Running   0          1m
pod/curl-pod                            1/1     Running   0          2m

NAME                               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/curl-service               NodePort    10.96.123.456   <none>        80:30080/TCP   1m
service/kubernetes                 ClusterIP   10.96.0.1       <none>        443/TCP        10d

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/curl-deployment   3/3     3            3           1m

NAME                                          DESIRED   CURRENT   READY   AGE
replicaset.apps/curl-deployment-74f59d59bf   3         3         3       1m

NAME                         DATA   AGE
configmap/curl-config        4      1m
```

---

## 🧪 TESTING & ACCESS

### Method 1: Port-Forward (Simplest - NO NodePort needed)
```bash
# Terminal 1: Start port-forward
kubectl port-forward service/curl-service 8080:80

# Terminal 2: Test
curl http://localhost:8080
# Hoặc mở browser: http://localhost:8080
```

**Advantages:**
- Không cần mở firewall port
- Simple, secure
- Tốt cho development

### Method 2: Using NodePort
```bash
# Get Node IP
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
echo "Node IP: $NODE_IP"

# Get NodePort
NODE_PORT=$(kubectl get service curl-service -o jsonpath='{.spec.ports[0].nodePort}')
echo "NodePort: $NODE_PORT"

# Test
curl http://$NODE_IP:$NODE_PORT
```

**Or direct:**
```bash
# Minikube users
minikube service curl-service

# Output: | http://127.0.0.1:XXXXX |
# Mở browser với URL đó
```

### Method 3: Exec vào Pod và test từ trong cluster
```bash
# Get pod name
POD_NAME=$(kubectl get pods -l app=curl-app -o jsonpath='{.items[0].metadata.name}')

# Exec vào pod
kubectl exec -it $POD_NAME -- sh

# Trong pod, test:
# curl http://curl-service:80
# curl http://curl-service:80/health (nếu có endpoint)
# ps aux (xem processes)

# Thoát: exit
```

### Method 4: Test từ another Pod
```bash
# Tạo temp pod để test
kubectl run curl-test --image=curlimages/curl:latest --rm -i --tty -- \
  curl http://curl-service

# Output:
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
```

---

## 🔍 EXPLORING & DEBUGGING

### Xem Pods với details
```bash
# List pods với IP và node
kubectl get pods -o wide

# Output:
# NAME                                READY   STATUS    IP           NODE
# curl-deployment-74f59d59bf-abc12   1/1     Running   10.244.1.5   node-1
# curl-deployment-74f59d59bf-def34   1/1     Running   10.244.2.7   node-2
```

### Describe Pod (chi tiết configuration)
```bash
kubectl describe pod curl-deployment-74f59d59bf-abc12
```

Look for:
- **Node**: Node nào chạy Pod này
- **IP**: Pod IP (10.244.x.x)
- **Containers**: Image, ports, probes
- **Events**: Lịch sử events (scheduling, pulling, starting)

### Xem Logs
```bash
# Logs của một pod
kubectl logs curl-deployment-74f59d59bf-abc12

# Logs của tất cả pods với label
kubectl logs -l app=curl-app

# Logs với follow
kubectl logs -f curl-deployment-74f59d59bf-abc12

# Logs của container trong multi-container pod
kubectl logs curl-pod -c container-name
```

### Xem Events (rất quan trọng cho debugging)
```bash
# Events gần đây
kubectl get events --sort-by='.lastTimestamp'

# Events của một resource
kubectl describe pod curl-deployment-74f59d59bf-abc12 | grep -A 20 Events

# Events của namespace
kubectl get events -n default --sort-by='.metadata.creationTimestamp'
```

### Xem Labels
```bash
# Show labels của pods
kubectl get pods --show-labels

# Output:
# NAME                                LABELS
# curl-deployment-74f59d59bf-abc12   app=curl-app,environment=learning,pod-template-hash=74f59d59bf,tier=backend,version=v1

# Filter by label
kubectl get pods -l app=curl-app
kubectl get pods -l tier=backend
kubectl get pods -l 'environment=learning'
kubectl get pods -l 'app=curl-app,tier=backend'
```

### Xem ConfigMap
```bash
kubectl get configmap curl-config -o yaml
kubectl describe configmap curl-config
```

### Xem Service Details
```bash
kubectl describe service curl-service

# Look for:
# - Selector: labels để chọn pods
# - Port: 80 (Service port)
# - TargetPort: 8080 (Pod port)
# - NodePort: 30080 (Node port)
# - Endpoints: IPs của các pods
```

### Kiểm tra Endpoints
```bash
kubectl get endpoints curl-service

# Output:
# NAME            ENDPOINTS                         AGE
# curl-service    10.244.1.5:8080,10.244.2.7:8080   1m

# Nếu endpoints = <none> → Selector không match pod labels!
```

---

## 🎨 LABELS & SELECTORS DEMO

### Thêm label mới vào pod
```bash
kubectl label pod curl-deployment-74f59d59bf-abc12 version=v2
```

### Xem pods với label cụ thể
```bash
kubectl get pods -l version=v2
kubectl get pods -l version  # Tất cả pods có label 'version'
```

### Update selector của service (nếu cần)
```bash
# Edit service
kubectl edit service curl-service

# Thay đổi spec.selector.matchLabels.version thành v2
# Sau đó, pods mới với version=v2 sẽ được load-balance
```

---

## 📊 SCALING

### Scale deployment lên 5 replicas
```bash
kubectl scale deployment curl-deployment --replicas=5

# Verify
kubectl get deployment curl-deployment
kubectl get pods -l app=curl-app

# Output: 5 pods thay vì 3
```

### Scale xuống 1 replica
```bash
kubectl scale deployment curl-deployment --replicas=1

# ReplicaSet sẽ terminate 2 pods giữ lại 1
```

### Auto-scaling với HPA (Horizontal Pod Autoscaler)
```bash
# Tạo HPA: scale từ 1-10 based trên CPU (target 50%)
kubectl autoscale deployment curl-deployment --cpu-percent=50 --min=1 --max=10

# Xem HPA
kubectl get hpa

# Test: Tạo load để xem scale
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://curl-service; done"
```

---

## 🔄 ROLLING UPDATE & ROLLBACK

### Update image version
```bash
# Update deployment với image mới
kubectl set image deployment/curl-deployment curl-container=curlimages/curl:8.5.0

# Xem rollout status
kubectl rollout status deployment/curl-deployment

# Output:
# deployment "curl-deployment" successfully rolled out
```

### Rollback nếu có vấn đề
```bash
# Xem rollout history
kubectl rollout history deployment/curl-deployment

# Rollback về revision trước
kubectl rollout undo deployment/curl-deployment

# Rollback về revision cụ thể
kubectl rollout undo deployment/curl-deployment --to-revision=2
```

---

## 🗑️ DELETE & CLEANUP

### Xóa theo từng loại
```bash
# Xóa service trước
kubectl delete -f services/

# Xóa deployment
kubectl delete -f deployments/

# Xóa pod (nếu có)
kubectl delete -f pods/

# Xóa configmap
kubectl delete -f configmaps/
```

### Xóa tất cả cùng lúc
```bash
cd /Users/rom/K8S/Project_K8s_Test/Declarative/k8s-full-project
kubectl delete -f .
```

### Xóa thủ công nếu còn sót lại
```bash
kubectl delete pods --all
kubectl delete deployments --all
kubectl delete services --all
kubectl delete replicasets --all
kubectl delete configmaps --all
```

### Xóa cả cluster (nếu dùng Minikube)
```bash
# Minikube
minikube stop
minikube delete

# Kind
kind delete cluster --name learning

# Docker Desktop: Turn off Kubernetes in Settings
```

---

## 📊 MONITORING

### Xem resource usage
```bash
# Install metrics-server nếu chưa có
# Minikube: minikube addons enable metrics-server

# Xem CPU/Memory của nodes
kubectl top nodes

# Xem CPU/Memory của pods
kubectl top pods
kubectl top pods -l app=curl-app
```

### Xem logs của tất cả pods
```bash
kubectl logs -l app=curl-app --tail=50
kubectl logs -l app=curl-app --tail=50 -f  # Follow
```

### Xem events
```bash
kubectl get events --sort-by='.lastTimestamp' | head -20
kubectl get events -w  # Watch events
```

---

## 🎓 LEARNING CHECKLIST

Sau khi deploy, hãy trả lời các câu hỏi sau:

- [ ] **Pods**: Có bao nhiêu pods đang chạy? Làm sao xem IP của từng pod?
- [ ] **Nodes**: Có bao nhiêu nodes? Pods được phân bổ ra sao trên các nodes?
- [ ] **Labels**: Labels của deployment là gì? Labels của pod là gì?
- [ ] **Selectors**: Service selector khớp với labels của pods không?
- [ ] **ReplicaSet**: Có bao nhiêu replicas? Làm sao để thay đổi số lượng?
- [ ] **Service**: Service port là gì? TargetPort? NodePort? Làm sao access từ outside?
- [ ] **NodePort**: Port range là多少? NodePort của service là bao nhiêu?
- [ ] **Deployment**: Làm sao update image? Làm sao rollback?
- [ ] **ConfigMap**: ConfigMap chứa gì? Làm sao sử dụng trong pods?

---

## 🔑 KEY CONCEPTS SUMMARY

| Concept | Definition | Example từ project |
|---------|------------|-------------------|
| **Pod** | Smallest deployable unit | `curl-pod` với container curl |
| **Node** | Worker machine | `node-1`, `node-2` từ `kubectl get nodes` |
| **Label** | Key-value tags | `app=curl-app`, `tier=backend` |
| **Selector** | Filter resources bằng labels | Service selector `app=curl-app` |
| **ReplicaSet** | Đảm bảo số lượng Pods | `replicas: 3` trong Deployment |
| **Deployment** | Quản lý ReplicaSet | `curl-deployment` |
| **Port** | Communication endpoint | `containerPort: 8080`, `port: 80` |
| **NodePort** | External access port | `nodePort: 30080` |
| **Service** | Network abstraction | `curl-service` expose pods |

---

## ❓ TROUBLESHOOTING

### Pods đang `Pending`
```bash
kubectl describe pod <pod-name>
# Check: Insufficient resources? Taints on node?
```

### Pods đang `CrashLoopBackOff`
```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
# Check: Image name? Command? Resource limits?
```

### Service không có endpoints
```bash
kubectl get endpoints <service-name>
kubectl describe service <service-name>
# Check: Selector labels khớp với pod labels?
kubectl get pods --show-labels
```

### Cannot access từ outside
```bash
# Check NodePort range
kubectl get svc <service>
# Check firewall: allow port 30000-32767
# Check Node IP: kubectl get nodes -o wide
# Try port-forward: kubectl port-forward svc/<service> 8080:80
```

### kubectl commands failing
```bash
# Check kubectl config
kubectl config view
kubectl config current-context

# Reset context nếu cần
kubectl config use-context <context-name>
```

---

## 📚 NEXT STEPS

1. **Đọc file `KUBERNETES-EXPLAINED.md`** - Giải thích chi tiết từng khái niệm
2. **Đọc file `README.md`** - Tổng quan project
3. **Thử các commands trong checklist trên**
4. **Tạo namespace mới và deploy lại**
5. **Thử Ingress thay vì NodePort**
6. **Thêm PersistentVolume cho storage**
7. **Tìm hiểu ConfigMap và Secret sâu hơn**
8. **Tìm hiểu StatefulSet cho databases**

---

## 🆘 HELP RESOURCES

```bash
# Help cho resource type
kubectl explain pod
kubectl explain deployment
kubectl explain service
kubectl explain deployment.spec.replicas

# API resources
kubectl api-resources

# kubectl cheatsheet
kubectl --help

# Online:
# - Kubernetes docs: https://kubernetes.io/docs/
# - Kubectl cheatsheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
```

---

**Chúc bạn học Kubernetes vui vẻ! 🎉**

**Questions?** Đọc KUBERNETES-EXPLAINED.md hoặc tìm kiếm trên Google với từ khóa "kubernetes <concept>".

**Need more hands-on?** Thử https://kubernetes.io/docs/tutorials/kubernetes-basics/
