# 🧪 MODULE 04: LABS - Kubernetes & ArgoCD

## LAB 1: Thiết lập Kubernetes Local

```bash
# Install minikube
brew install minikube  # macOS
# hoặc Windows: choco install minikube

# Start cluster
minikube start

# Verify
kubectl get nodes
```

---

## LAB 2: Deploy App lên K8s

### Tạo k8s/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: counter
spec:
  replicas: 2
  selector:
    matchLabels:
      app: counter
  template:
    metadata:
      labels:
        app: counter
    spec:
      containers:
      - name: web
        image: counter-app:v1.0
        ports:
        - containerPort: 5000
        env:
        - name: REDIS_HOST
          value: redis-service
---
apiVersion: v1
kind: Service
metadata:
  name: counter-service
spec:
  selector:
    app: counter
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### Deploy

```bash
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods
kubectl get svc

# Access app
minikube service counter-service
```

---

## LAB 3: Cài đặt ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

---

## LAB 4: Cập nhật Tuần tự

### Update image version

```bash
# Edit deployment.yaml → image: counter-app:v2.0
kubectl apply -f k8s/deployment.yaml

# Watch rollout
kubectl rollout status deployment/counter

# Rollback if needed
kubectl rollout undo deployment/counter
```

✅ **Checklist**

- [ ] Minikube running
- [ ] App deployed to K8s
- [ ] ArgoCD installed
- [ ] Rolling update tested
