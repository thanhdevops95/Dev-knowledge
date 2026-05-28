# Hướng dẫn Kubernetes Basics

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Kubernetes (K8s) là nền tảng mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng container.

### Tại sao cần Kubernetes?

| Docker | Kubernetes |
|--------|------------|
| Chạy 1 container | Orchestrate nhiều containers |
| Manual scaling | Auto scaling |
| Restart thủ công | Self-healing |
| Single host | Multi-host cluster |

---

## 🔧**CÀI ĐẶT**

### Minikube (Local development)

```bash
# macOS
brew install minikube

# Windows (Chocolatey)
choco install minikube

# Khởi động cluster
minikube start

# Kiểm tra
minikube status
```

### kubectl (CLI tool)

```bash
# macOS
brew install kubectl

# Windows (Chocolatey)
choco install kubernetes-cli

# Kiểm tra
kubectl version --client
```

---

## 📦**KHÁI NIỆM CƠ BẢN**

| Khái niệm | Mô tả |
|-----------|-------|
| **Cluster** | Tập hợp các nodes |
| **Node** | Máy chủ (physical/virtual) |
| **Pod** | Đơn vị nhỏ nhất, chứa 1+ containers |
| **Deployment** | Quản lý replicas của pods |
| **Service** | Expose pods ra network |
| **Namespace** | Phân chia resources |
| **ConfigMap** | Lưu configuration |
| **Secret** | Lưu sensitive data |
| **Volume** | Lưu trữ dữ liệu |
| **Ingress** | HTTP routing |

---

## 🚀**PODS**

### Pod manifest

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  containers:
    - name: my-app
      image: nginx:latest
      ports:
        - containerPort: 80
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
        requests:
          memory: "64Mi"
          cpu: "250m"
```

### Lệnh kubectl cho Pods

```bash
# Tạo pod
kubectl apply -f pod.yaml

# Liệt kê pods
kubectl get pods
kubectl get pods -o wide

# Xem chi tiết
kubectl describe pod my-app

# Xem logs
kubectl logs my-app
kubectl logs -f my-app  # Follow

# Exec vào pod
kubectl exec -it my-app -- /bin/bash

# Xóa pod
kubectl delete pod my-app
kubectl delete -f pod.yaml
```

---

## 📊**DEPLOYMENTS**

### Deployment manifest

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: my-secret
                  key: database-url
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Lệnh kubectl cho Deployments

```bash
# Tạo/cập nhật deployment
kubectl apply -f deployment.yaml

# Liệt kê
kubectl get deployments
kubectl get deploy

# Scale
kubectl scale deployment my-app --replicas=5

# Update image
kubectl set image deployment/my-app my-app=my-app:2.0.0

# Rollback
kubectl rollout undo deployment/my-app
kubectl rollout history deployment/my-app

# Xem status
kubectl rollout status deployment/my-app
```

---

## 🌐**SERVICES**

### Service types

| Type | Mô tả |
|------|-------|
| **ClusterIP** | Internal IP (default) |
| **NodePort** | Expose qua port của node |
| **LoadBalancer** | Cloud load balancer |
| **ExternalName** | DNS alias |

### Service manifest

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
    - port: 80          # Service port
      targetPort: 8080  # Container port
```

### NodePort Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-nodeport
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080  # 30000-32767
```

### LoadBalancer Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-lb
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

```bash
# Lệnh
kubectl get services
kubectl get svc
kubectl describe svc my-app-service
```

---

## 🔐**CONFIGMAP & SECRETS**

### ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  APP_ENV: production
  LOG_LEVEL: info
  config.json: |
    {
      "key": "value"
    }
```

### Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  # Base64 encoded
  username: YWRtaW4=
  password: cGFzc3dvcmQxMjM=
```

```bash
# Tạo secret từ CLI
kubectl create secret generic my-secret \
  --from-literal=username=admin \
  --from-literal=password=password123
```

### Sử dụng trong Pod

```yaml
spec:
  containers:
    - name: my-app
      env:
        # Từ ConfigMap
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: my-config
              key: APP_ENV
        # Từ Secret
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: password
      # Mount ConfigMap là file
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: my-config
```

---

## 🌍**INGRESS**

### Ingress manifest

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-service
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

### TLS (HTTPS)

```yaml
spec:
  tls:
    - hosts:
        - myapp.example.com
      secretName: tls-secret
  rules:
    ...
```

---

## 📁**NAMESPACES**

```bash
# Liệt kê namespaces
kubectl get namespaces
kubectl get ns

# Tạo namespace
kubectl create namespace my-namespace

# Sử dụng namespace
kubectl get pods -n my-namespace
kubectl apply -f deployment.yaml -n my-namespace

# Set default namespace
kubectl config set-context --current --namespace=my-namespace
```

---

## 💾**PERSISTENT VOLUMES**

### PersistentVolumeClaim

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### Sử dụng trong Pod

```yaml
spec:
  containers:
    - name: my-app
      volumeMounts:
        - name: data
          mountPath: /app/data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: my-pvc
```

---

## 📊**KUBECTL COMMANDS**

### Xem resources

```bash
kubectl get all
kubectl get pods,svc,deploy

kubectl describe pod <name>
kubectl describe svc <name>

kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow
kubectl logs <pod-name> -c <container-name>  # Specific container
```

### Debug

```bash
# Exec vào pod
kubectl exec -it <pod-name> -- /bin/bash

# Port forward
kubectl port-forward pod/<pod-name> 8080:80
kubectl port-forward svc/<svc-name> 8080:80

# Xem events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Apply & Delete

```bash
# Apply folder
kubectl apply -f ./manifests/

# Delete
kubectl delete -f deployment.yaml
kubectl delete pod <name>
kubectl delete all --all -n my-namespace
```

---

## 🔄**HELM (Package Manager)**

### Cài đặt

```bash
# macOS
brew install helm

# Thêm repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Sử dụng

```bash
# Tìm charts
helm search repo nginx

# Install
helm install my-nginx bitnami/nginx

# List releases
helm list

# Upgrade
helm upgrade my-nginx bitnami/nginx

# Uninstall
helm uninstall my-nginx
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
