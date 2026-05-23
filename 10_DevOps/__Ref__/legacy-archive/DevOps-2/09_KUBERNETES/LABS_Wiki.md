# Module 09: Kubernetes Labs

---

## 🔧 Lab 1: Setup Minikube

```bash
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start

# Verify
kubectl cluster-info
kubectl get nodes
```

---

## 🔧 Lab 2: Deploy First App

```yaml
# nginx-deployment.yaml
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
          image: nginx:1.25
          ports:
            - containerPort: 80
```

```bash
kubectl apply -f nginx-deployment.yaml
kubectl get pods
kubectl get deployments
```

---

## 🔧 Lab 3: Expose Service

```yaml
# nginx-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - port: 80
  type: NodePort
```

```bash
kubectl apply -f nginx-service.yaml
minikube service nginx-service --url
```

---

## 🔧 Lab 4: Scaling

```bash
# Scale up
kubectl scale deployment nginx --replicas=5
kubectl get pods -w

# Scale down
kubectl scale deployment nginx --replicas=2
```

---

## 🔧 Lab 5: Rolling Update

```bash
# Update image
kubectl set image deployment/nginx nginx=nginx:1.26

# Watch rollout
kubectl rollout status deployment/nginx

# Rollback if needed
kubectl rollout undo deployment/nginx
```

---

## ✅ Tổng kết

| Lab | Skill |
|-----|-------|
| 1 | Minikube setup |
| 2 | Deployments |
| 3 | Services |
| 4 | Scaling |
| 5 | Rolling updates |

👉 **[SCENARIOS.md](SCENARIOS.md)**
