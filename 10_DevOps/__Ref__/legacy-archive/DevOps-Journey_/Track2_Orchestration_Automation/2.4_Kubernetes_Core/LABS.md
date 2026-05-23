# 🔬 Labs: Kubernetes Core

> **Hands-on Labs for Kubernetes**
>
> *Bài thực hành Kubernetes.*

---

## 🔬 Lab 1: Minikube Setup

```bash
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start

# Verify
kubectl get nodes
kubectl cluster-info
```

---

## 🔬 Lab 2: Deploy Application

```bash
# Create deployment
kubectl create deployment nginx --image=nginx:alpine

# Expose
kubectl expose deployment nginx --port=80 --type=NodePort

# Get URL
minikube service nginx --url

# Scale
kubectl scale deployment nginx --replicas=3
kubectl get pods
```

---

## 🔬 Lab 3: YAML Manifests

```yaml
# app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:alpine
          ports:
            - containerPort: 80
          resources:
            limits:
              memory: "128Mi"
              cpu: "250m"
---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
    - port: 80
  type: LoadBalancer
```

```bash
kubectl apply -f app.yaml
kubectl get all
```

---

## 🔬 Lab 4: ConfigMaps & Secrets

```yaml
# config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: debug
  API_URL: http://api:3000
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_PASSWORD: mysecret
---
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "env && sleep 3600"]
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secret
```

---

## 🔬 Lab 5: Rolling Update

```bash
# Update image
kubectl set image deployment/web web=nginx:1.21

# Watch rollout
kubectl rollout status deployment/web

# View history
kubectl rollout history deployment/web

# Rollback
kubectl rollout undo deployment/web
```

---

## ✅ Checklist

- [ ] Lab 1: Minikube Setup
- [ ] Lab 2: Deploy Application
- [ ] Lab 3: YAML Manifests
- [ ] Lab 4: ConfigMaps & Secrets
- [ ] Lab 5: Rolling Update

---

## ✅ General Verification (Kiểm chứng tổng quát)

Verify Kubernetes is working:

*(Xác nhận Kubernetes hoạt động:)*

```bash
# Check cluster status (Kiểm tra trạng thái cluster)
kubectl cluster-info
kubectl get nodes

# Check all resources (Kiểm tra tất cả resources)
kubectl get all

# Check deployments are running (Kiểm tra deployments chạy)
kubectl get deployments
kubectl get pods -o wide

# Test service connectivity (Kiểm tra kết nối service)
minikube service web --url
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Solution |
|-------|----------|
| `minikube start failed` | Check Docker/virtualization, try `minikube delete && minikube start` *(Xóa và thử lại)* |
| `ImagePullBackOff` | Check image name, registry auth *(Kiểm tra tên image và auth)* |
| `CrashLoopBackOff` | Check logs: `kubectl logs pod-name` *(Kiểm tra logs)* |
| `Pending pod` | Check resources: `kubectl describe pod` *(Kiểm tra resources)* |
| `Service unavailable` | Check selector matches, pod labels *(Kiểm tra selector và labels)* |
| `kubectl: command not found` | Install kubectl or use `minikube kubectl` *(Cài kubectl)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

```bash
# Delete lab resources (Xóa resources lab)
kubectl delete deployment nginx web 2>/dev/null
kubectl delete service nginx web 2>/dev/null
kubectl delete configmap app-config 2>/dev/null
kubectl delete secret app-secret 2>/dev/null
kubectl delete pod app 2>/dev/null

# Delete all in namespace (Xóa tất cả trong namespace)
kubectl delete all --all

# Stop minikube (Dừng minikube)
minikube stop

# Full cleanup (Dọn dẹp hoàn toàn)
minikube delete
```

---

**[← Back to README](./README.md)**

