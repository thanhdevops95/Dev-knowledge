# Kubernetes Full Learning Project

## Tổng quan
Project này giúp bạn hiểu rõ các khái niệm Kubernetes cơ bản thông qua một ứng dụng **nginx** đơn giản (web server).

## Cấu trúc thư mục
```
k8s-full-project/
├── pods/
│   └── curl-pod.yaml          # Pod đơn lẻ
├── deployments/
│   └── curl-deployment.yaml   # Deployment với ReplicaSet
├── services/
│   └── curl-service.yaml      # Service với NodePort
└── configmaps/
    └── curl-config.yaml       # ConfigMap cho configuration
```

## Các khái niệm được học

### 1. Pod
- **Pod**: Smallest deployable unit trong K8s
- Một Pod chứa 1 hoặc nhiều containers
- Pods được schedule trên Nodes
- Có unique IP address trong cluster

### 2. Node
- **Node**: Worker machine (VM hoặc physical server)
- Chạy Kubelet, container runtime (Docker/containerd)
- Chứa Pods
- Có Internal/External IP

### 3. Label & Selector
- **Label**: Key-value pairs đánh dấu resources (Pods, Services, etc.)
- **Selector**: Dùng labels để chọn resources
- Ví dụ: `selector.matchLabels.app: curl-app`

### 4. ReplicaSet
- **ReplicaSet**: Đảm bảo số lượng Pods chạy đúng theo `replicas`
- Được quản lý bởi Deployment
- Tự động scale, replace Pods failed

### 5. Deployment
- **Deployment**: Quản lý ReplicaSet
- Cung cấp rolling updates, rollback
- Declarative updates

### 6. Port
- **containerPort**: Port trong container (80 cho nginx)
- **port**: Port của Service trong cluster (80)
- **targetPort**: Port của Pod/Pod container (80)
- **nodePort**: Port trên Node (30080)

### 7. Service
- **Service**: Network abstraction để expose Pods
- **NodePort**: Mở port trên mọi Node (30000-32767)
- Access qua: `<NodeIP>:<nodePort>`

### 8. ConfigMap
- **ConfigMap**: Lưu configuration dưới dạng key-value
- Tách biệt config từ image container
- Không dùng cho sensitive data (dùng Secret)

## Cài đặt & Chạy

### Prerequisites
```bash
# Kiểm tra K8s cluster
kubectl cluster-info

# Kiểm tra nodes
kubectl get nodes

# Kiểm tra kubectl config
kubectl config view
```

### Apply configurations
```bash
# Navigate vào thư mục
cd k8s-full-project

# Apply tất cả theo thứ tự
kubectl apply -f configmaps/
kubectl apply -f pods/
kubectl apply -f deployments/
kubectl apply -f services/
```

### Hoặc apply tất cả cùng lúc:
```bash
kubectl apply -f .
```

### Kiểm tra trạng thái
```bash
# Xem tất cả resources
kubectl get all

# Xem Pods
kubectl get pods
kubectl get pods -o wide  # Xem thêm node và IP

# Xem Deployments
kubectl get deployments

# Xem Services
kubectl get services

# Xem Nodes
kubectl get nodes
kubectl describe nodes

# Xem ConfigMaps
kubectl get configmaps
```

### Test ứng dụng
```bash
# Lấy NodePort của service
kubectl get service curl-service

# Output ví dụ:
# NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
# curl-service   NodePort   10.96.123.456   <none>        80:30080/TCP   5s

# Test từ trong cluster (từ một Pod)
kubectl run curl-test --image=curlimages/curl:latest --rm -i --tty -- \
  curl http://curl-service

# Test từ localhost (nếu có Minikube/Docker Desktop)
# Với Minikube:
minikube service curl-service

# Hoặc lấy Node IP và test trực tiếp:
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
curl http://$NODE_IP:30080

# Test với port-forward (không cần NodePort)
kubectl port-forward service/curl-service 8080:80
# Mở http://localhost:8080 trong browser
```

### Delete resources
```bash
# Xóa theo thứ tự ngược
kubectl delete -f services/
kubectl delete -f deployments/
kubectl delete -f pods/
kubectl delete -f configmaps/

# Hoặc xóa tất cả
kubectl delete -f .
```

### Xem logs
```bash
# Xem logs của Pod
kubectl logs curl-pod
kubectl logs -l app=curl-app  # Logs của tất cả Pods có label này

# Xem logs với follow
kubectl logs -f curl-deployment-xxxxx
```

### Exec vào Pod
```bash
# Exec vào Pod đang chạy
kubectl exec -it curl-pod -- /bin/sh

# Trong Pod, test curl:
# curl http://curl-service:80
# curl http://google.com
```

## Troubleshooting
```bash
# Xem chi tiết Pod
kubectl describe pod curl-pod

# Xem events
kubectl get events --sort-by='.lastTimestamp'

# Xem logs của Deployment
kubectl logs deployment/curl-deployment

# Kiểm tra Service endpoints
kubectl get endpoints curl-service
```

## Cleanup hoàn toàn
```bash
# Xóa tất cả
kubectl delete -f .

# Xóa pods còn sót lại (nếu có)
kubectl delete pods --all

# Xóa services
kubectl delete services --all

# Xóa deployments
kubectl delete deployments --all
```

## Chi tiết từng file

### curl-pod.yaml
- Tạo một Pod đơn lẻ với container curl
- Labels: `app=curl-app`, `tier=frontend`, `environment=learning`
- Container port: 80, 443
- Resource limits/requests

### curl-deployment.yaml
- Deployment với 3 replicas
- ReplicaSet tự động đảm bảo 3 Pods luôn chạy
- Selector match labels: `app=curl-app`, `tier=backend`
- Pod template có labels trùng với selector
- Liveness/Readiness probes

### curl-service.yaml
- Service type: NodePort
- Selector: `app=curl-app`, `tier=backend`
- Port mapping:
  - Service port: 80
  - Target port: 8080 (Pod containerPort)
  - NodePort: 30080
- Accessible từ outside cluster qua NodeIP:30080

### curl-config.yaml
- ConfigMap với các config keys
- File config.json tronglined
- Có thể mount vào Pod làm environment variables hoặc volume

## Best Practices
1. Luôn đặt labels cho resources
2. Sử dụng Namespaces để phân tách environments
3. Đặt resource limits/requests
4. Dùng ConfigMap/Secret cho configuration
5. Không hardcode sensitive data trong YAML
6. Sử dụng kubectl apply thay vì kubectl create
7. Version control tất cả YAML files

## Next Steps
- Tạo Namespace
- Tạo Ingress thay vì NodePort
- Tạo PersistentVolume và PersistentVolumeClaim
- Tìm hiểu HorizontalPodAutoscaler
- Thêm liveness/readiness probes thực tế
- Tạo StatefulSet cho stateful apps
