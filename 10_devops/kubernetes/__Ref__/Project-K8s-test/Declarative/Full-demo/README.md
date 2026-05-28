# K8s Full Demo Project - Học Pod, Node, ReplicaSet, Service, Labels & Selectors

## 🎯 Mục tiêu
Hiểu rõ các khái niệm cơ bản của Kubernetes thông qua một project demo đơn giản với app có curl.

## 📋 Yêu cầu
- Minikube đã được cài đặt và chạy
- kubectl đã được cài đặt

## 🏗️ Cấu trúc Project

```
FullDemo/
├── yaml-manifests/          # Tất cả YAML files
│   ├── 01-pod.yaml
│   ├── 02-deployment.yaml
│   ├── 03-service-nodeport.yaml
│   └── 04-hpa.yaml (optional)
├── scripts/
│   ├── deploy-all.sh
│   ├── cleanup.sh
│   └── test-app.sh
└── README.md
```

## 📚 Khái niệm sẽ học

1. **Pod** - Đơn vị nhỏ nhất trong K8s
2. **Node** - Máy vật lý/VM chạy Pods
3. **ReplicaSet** - Đảm bảo số lượng Pod luôn được duy trì
4. **Deployment** - Quản lý ReplicaSet và rolling updates
5. **Service** - Expose Pods ra ngoài (NodePort, ClusterIP)
6. **Labels & Selectors** - Cơ chế grouping và targeting
7. **Ports** - Cách K8s quản lý networking

## 🚀 Các bước thực hiện

### Bước 1: Kiểm tra Minikube
```bash
minikube status
minikube start --driver=docker  # hoặc virtualbox, hyperkit
```

### Bước 2: Xem Nodes
```bash
kubectl get nodes
```

### Bước 3: Deploy ứng dụng
```bash
# Apply tất cả YAML files
kubectl apply -f yaml-manifests/
```

### Bước 4: Kiểm tra
```bash
kubectl get pods
kubectl get replicaset
kubectl get deployment
kubectl get service
kubectl get nodes -o wide
```

### Bước 5: Test ứng dụng
```bash
# Lấy NodePort của service
kubectl get svc curl-app

# Test từ trong cluster
kubectl exec -it <pod-name> -- curl http://curl-app:8080

# Test từ outside (dùng IP của node)
curl http://$(minikube ip):<NodePort>
```

## 🔍 Giải thích chi tiết

### 1. POD
- Pod là wrapper chứa 1 hoặc nhiều container
- Trong demo: mỗi pod chứa 1 container curl-app
- Xem pod chi tiết: `kubectl describe pod <pod-name>`
- Xem logs: `kubectl logs <pod-name>`

### 2. NODE
- Node là worker machine trong cluster
- Minikube tạo 1 node duy nhất
- Xem node info: `kubectl describe node <node-name>`
- Pods được schedule lên node nào: `kubectl get pod -o wide`

### 3. REPLICASET
- ReplicaSet đảm bảo luôn có đúng số Pods chạy
- Tự động tạo/xóa Pods nếu cần
- Quản lý bởi Deployment
- Xem: `kubectl describe replicaset <rs-name>`

### 4. DEPLOYMENT
- Quản lý ReplicaSet
- Hỗ trợ rolling updates, rollback
- Declarative: bạn nói MUỐN có gì, K8s làm
- Xem history: `kubectl rollout history deployment/curl-app`

### 5. SERVICE (NodePort)
- Service là load balancer cho Pods
- NodePort: mở port trên mọi Node (30000-32767)
- Selectors: tìm Pods có labels phù hợp
- Port mapping:
  - port: 8080 (service port)
  - targetPort: 80 (port của container)
  - nodePort: 30007 (port trên node)

### 6. LABELS & SELECTORS
- Labels: key-value pairs gắn vào resources
  - Pod có: app=curl-app
  - Service có selector: app=curl-app
- Selectors: dùng để tìm và kết nối resources
- Service dùng selector để tìm Pods để route traffic

## 🎮 Commands quan trọng

```bash
# Xem tất cả resources
kubectl get all

# Xem tất cả với labels
kubectl get pods --show-labels

# Xem deployment details
kubectl describe deployment curl-app

# Xem service details
kubectl describe service curl-app

# Scale replicas
kubectl scale deployment curl-app --replicas=3

# Xem events
kubectl get events --sort-by='.lastTimestamp'

# Vào shell của pod
kubectl exec -it <pod-name> -- /bin/bash

# Delete tất cả
kubectl delete -f yaml-manifests/
# hoặc
kubectl delete all --all
```

## 📊 Kiến trúc Flow

```
User Request → NodePort (30007) → Service (curl-app:8080)
                                    ↓
                            Selector match (app=curl-app)
                                    ↓
                            Pods (curl-app-xxxxx):80
                                    ↓
                            Container (curl-app)
```

## 🔄 Lifecycle

1. **Apply YAML**: K8s đọc và tạo resources
2. **Scheduler**: Chọn node để chạy pod
3. **Kubelet**: Node chạy pod
4. **Service**: Tạo endpoints và route traffic
5. **ReplicaSet**: Theo dõi và đảm bảo số lượng pod

## 🧪 Experiment Ideas

1. Scale deployment lên 3 replicas: `kubectl scale deployment curl-app --replicas=3`
2. Xem pod bị schedule lên node nào: `kubectl get pod -o wide`
3. Delete 1 pod xem ReplicaSet có tạo lại không
4. Thay đổi image và xem rolling update
5. Xem service endpoints: `kubectl get endpoints curl-app`

## 🧹 Cleanup

```bash
# Xong project, cleanup để tránh tốn resource
kubectl delete -f yaml-manifests/
# hoặc
./scripts/cleanup.sh

# Dừng minikube
minikube stop

# Xóa minikube cluster
minikube delete
```

## 📖 Tài liệu tham khảo
- Kubernetes Docs: https://kubernetes.io/docs/home/
- Minikube Docs: https://minikube.sigs.k8s.io/docs/

---

**Lưu ý**: Đây là project học tập, production cần thêm configmaps, secrets, ingress, persistent volumes, etc.
