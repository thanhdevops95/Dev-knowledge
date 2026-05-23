# 🚀 Quick Start - 5 Phút chạy Demo

## Prerequisites
- Minikube installed
- kubectl installed

## Bắt đầu ngay:

### 1. Start Minikube
```bash
minikube start --driver=docker
# Nếu docker không được, thử: minikube start --driver=virtualbox
```

### 2. Deploy tất cả
```bash
cd /Users/rom/K8S/Project_K8s_Test/FullDemo
./scripts/deploy-all.sh
```

### 3. Xem pods chạy thế nào
```bash
kubectl get pods
kubectl get pods -o wide  # Xem pod chạy trên node nào
```

### 4. Xem replicaset
```bash
kubectl get replicaset
```

### 5. Xem deployment
```bash
kubectl get deployment
kubectl describe deployment curl-app-deployment
```

### 6. Xem service
```bash
kubectl get svc
```

### 7. Test ứng dụng
```bash
./scripts/test-app.sh
```

### 8. Truy cập từ browser
```bash
# Lấy NodePort
kubectl get svc curl-app-service

# Lấy Minikube IP
minikube ip

# Truy cập: http://<minikube-ip>:30007
# Ví dụ: http://192.168.49.2:30007
```

## Troubleshooting

### Pod stuck trong Pending?
```bash
kubectl describe pod <pod-name>
# Kiểm tra: Insufficient resources, node selector, taints
```

### Pod crash?
```bash
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

### Service không hoạt động?
```bash
# Xem endpoints
kubectl get endpoints curl-app-service

# Nếu empty → selector không match với pod labels
# Kiểm tra pod labels:
kubectl get pods --show-labels

# Kiểm tra service selector:
kubectl get svc curl-app-service -o yaml
```

### NodePort không accessible?
```bash
# Kiểm tra firewall trên node (nếu có)
# Minikube: thường không có firewall

# Test từ trong minikube node:
minikube ssh
curl http://<node-ip>:30007

# Test từ localhost (trên host machine):
curl http://$(minikube ip):30007
```

## Cleanup
```bash
./scripts/cleanup.sh
# hoặc
kubectl delete -f yaml-manifests/
```

## Các lệnh quan trọng nhất

| Task | Command |
|------|---------|
| Xem tất cả | `kubectl get all` |
| Xem pods | `kubectl get pods` |
| Xem nodes | `kubectl get nodes` |
| Xem services | `kubectl get svc` |
| Xem replicaset | `kubectl get replicaset` |
| Xem deployment | `kubectl get deployment` |
| Xem chi tiết | `kubectl describe <resource> <name>` |
| Xem logs | `kubectl logs <pod-name>` |
| Vào pod shell | `kubectl exec -it <pod-name> -- sh` |
| Scale replicas | `kubectl scale deployment <name> --replicas=3` |
| Delete resource | `kubectl delete <resource> <name>` |

---

**Chạy demo và xem CONCEPTS.md để hiểu chi tiết từng khái niệm!** 🎓
