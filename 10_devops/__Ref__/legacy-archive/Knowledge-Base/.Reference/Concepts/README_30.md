# 🎯 GIAI ĐOẠN 9: KUBERNETES - ORCHESTRATION

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-9**.
- **Giai đoạn 9: Kubernetes** - Quản lý containers quy mô lớn!

Docker Compose chỉ chạy 1 máy. Kubernetes chạy hàng trăm máy, tự phục hồi, tự scale.

## 🏗️ CẤU TRÚC

```
Stage09_Complete/
├── k8s/                  # ← MỚI: Kubernetes manifests
│   ├── mysql.yaml
│   ├── backend.yaml
│   └── gateway.yaml
├── (files cũ)
└── README.md
```

## 🚀 CÁCH CHẠY

### Bước 1: Start Minikube
```bash
minikube start --driver=docker
```

### Bước 2: Deploy
```bash
kubectl apply -f k8s/
```

### Bước 3: Xem Pods
```bash
kubectl get pods
# Đợi tất cả STATUS = Running
```

### Bước 4: Truy cập
```bash
# Lấy URL
minikube service gateway --url

# Hoặc port-forward
kubectl port-forward svc/gateway 8080:80
# Truy cập: http://localhost:8080
```

## 🧪 TESTING

### Test 1: Self-Healing
```bash
# Xem pods
kubectl get pods

# Xóa 1 pod backend
kubectl delete pod backend-xxx-xxx

# Xem lại ngay lập tức
kubectl get pods
# → Pod mới tự động được tạo!
```

### Test 2: Scaling
```bash
# Scale lên 5 replicas
kubectl scale deployment backend --replicas=5

kubectl get pods
# → Thấy 5 pods backend
```

### Test 3: Rolling Update
```bash
# Update image
kubectl set image deployment/backend backend=YOUR_USER/todo-go:v2

# Xem quá trình
kubectl rollout status deployment/backend
```

## ✅ CHECKLIST

- [ ] Minikube chạy thành công
- [ ] Deploy manifests thành công
- [ ] Tất cả pods Running
- [ ] Truy cập được app
- [ ] Test self-healing thành công
- [ ] Scale được pods

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **Pods:** Đơn vị nhỏ nhất trong K8s
2. ✅ **Deployments:** Quản lý replicas
3. ✅ **Services:** Load balancing & DNS
4. ✅ **PVC:** Persistent storage
5. ✅ **Self-healing:** Tự tạo pod mới khi crash

## 🚧 TIẾP THEO

Giai đoạn 10: **AWS EKS & Autoscaling** - Lên Cloud thật!
