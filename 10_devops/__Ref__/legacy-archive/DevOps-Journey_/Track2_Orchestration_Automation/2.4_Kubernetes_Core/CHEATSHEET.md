# 📋 Kubernetes - Cheatsheet

> **Quick Reference for Kubernetes Commands**
>
> *Tra cứu nhanh các lệnh Kubernetes*

---

## 🔧 Basic Commands (Lệnh cơ bản)

```bash
# Cluster info (Thông tin cluster)
kubectl cluster-info
kubectl get nodes

# Get resources (Lấy resources)
kubectl get pods                    # List pods (Liệt kê pods)
kubectl get pods -A                 # All namespaces (Tất cả namespaces)
kubectl get services                # List services (Liệt kê services)
kubectl get deployments             # List deployments
kubectl get all                     # All resources (Tất cả resources)
```

---

## 📝 CRUD Operations (Thao tác CRUD)

```bash
# Create (Tạo)
kubectl apply -f deployment.yaml
kubectl create deployment nginx --image=nginx

# Read (Đọc)
kubectl describe pod pod-name
kubectl logs pod-name
kubectl logs -f pod-name            # Follow logs (Theo dõi logs)

# Update (Cập nhật)
kubectl set image deployment/app app=nginx:1.20
kubectl edit deployment app

# Delete (Xóa)
kubectl delete -f deployment.yaml
kubectl delete pod pod-name
```

---

## 🐚 Exec & Debug

```bash
kubectl exec -it pod-name -- sh     # Enter pod (Vào pod)
kubectl exec -it pod-name -- bash   # Bash shell
kubectl port-forward pod-name 8080:80  # Forward port
kubectl top pods                    # Resource usage (Tài nguyên)
kubectl top nodes
```

---

## 📄 Basic Manifests (Manifests cơ bản)

### Deployment

```yaml
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
        image: nginx:alpine
        ports:
        - containerPort: 80
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

---

## 🏷️ Labels & Selectors

```bash
kubectl get pods -l app=nginx       # Filter by label (Lọc theo label)
kubectl label pod pod-name env=prod # Add label (Thêm label)
kubectl get pods --show-labels      # Show labels (Hiện labels)
```

---

## 📊 Scaling (Mở rộng)

```bash
kubectl scale deployment nginx --replicas=5
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
