# ☸️ Kubernetes — Container Orchestration

> `[ADVANCED]` — Quản lý containers ở quy mô lớn

---

## Kubernetes là gì?

**Kubernetes (K8s)** là hệ thống orchestration cho containers — tự động deploy, scale, và quản lý containerized applications.

**Khi nào cần K8s:**
- Nhiều containers cần quản lý (microservices)
- Cần auto-scaling theo tải
- Cần zero-downtime deployment
- High availability (self-healing)

**Khi nào KHÔNG cần K8s:**
- App nhỏ, 1-2 services → Docker Compose đủ
- Team nhỏ, ít DevOps experience

---

## Kiến trúc K8s

```
                     Kubernetes Cluster
┌──────────────────────────────────────────────────┐
│  Control Plane (Master)                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │API Server│ │Scheduler │ │Controller Manager│ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
│  ┌─────────────────────────────────────────────┐ │
│  │              etcd (State Store)             │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
         │              │              │
    ┌────▼────┐    ┌────▼────┐   ┌────▼────┐
    │  Node 1  │    │  Node 2  │   │  Node 3  │
    │ ┌──────┐ │    │ ┌──────┐ │   │ ┌──────┐ │
    │ │ Pod  │ │    │ │ Pod  │ │   │ │ Pod  │ │
    │ │ Pod  │ │    │ │ Pod  │ │   │ │ Pod  │ │
    │ └──────┘ │    │ └──────┘ │   │ └──────┘ │
    │ kubelet  │    │ kubelet  │   │ kubelet  │
    └──────────┘    └──────────┘   └──────────┘
```

---

## Các đối tượng cơ bản

### Pod — Đơn vị nhỏ nhất

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-api-pod
  labels:
    app: my-api
spec:
  containers:
    - name: api
      image: my-api:1.0.0
      ports:
        - containerPort: 8000
      env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
      resources:
        requests:
          memory: "128Mi"
          cpu: "250m"
        limits:
          memory: "256Mi"
          cpu: "500m"
      readinessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 10
      livenessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 15
        periodSeconds: 20
```

### Deployment — Quản lý Pods

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-api
  namespace: production
spec:
  replicas: 3                    # 3 pods running cùng lúc
  selector:
    matchLabels:
      app: my-api
  
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1               # Tối đa thêm 1 pod trong quá trình update
      maxUnavailable: 0         # Không pod nào được down trong update
  
  template:
    metadata:
      labels:
        app: my-api
        version: "1.0.0"
    spec:
      containers:
        - name: api
          image: my-registry/my-api:1.0.0
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: my-api-config
            - secretRef:
                name: my-api-secrets
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
      
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: my-api
```

### Service — Expose Pods

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-api-service
spec:
  selector:
    app: my-api          # Chọn pods có label này
  
  ports:
    - protocol: TCP
      port: 80           # Port của Service
      targetPort: 8000   # Port của container
  
  type: ClusterIP        # ClusterIP | NodePort | LoadBalancer

---
# LoadBalancer (tạo cloud LB)
apiVersion: v1
kind: Service
metadata:
  name: my-api-lb
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  selector:
    app: my-api
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

### Ingress — HTTP routing

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-api-service
                port:
                  number: 80
```

### ConfigMap & Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-api-config
data:
  APP_ENV: production
  LOG_LEVEL: info
  ALLOWED_ORIGINS: "https://myapp.com"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-api-secrets
type: Opaque
stringData:
  DATABASE_URL: postgresql://user:pass@db:5432/mydb
  JWT_SECRET: super-random-secret-value
  # Trong production: dùng External Secrets Operator
  # để sync từ AWS Secrets Manager, HashiCorp Vault...
```

### HPA — Auto Scaling

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-api
  
  minReplicas: 2
  maxReplicas: 10
  
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70   # Scale khi CPU > 70%
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

---

## kubectl — CLI cơ bản

```bash
# Context & Namespace
kubectl config get-contexts
kubectl config use-context my-cluster
kubectl config set-context --current --namespace=production

# Xem resources
kubectl get pods
kubectl get pods -n production -o wide        # Chi tiết hơn
kubectl get all                               # Tất cả resources
kubectl describe pod my-api-7d6b4c-xyz        # Chi tiết pod

# Apply config
kubectl apply -f deployment.yaml
kubectl apply -f ./k8s/                       # Apply cả thư mục
kubectl delete -f deployment.yaml

# Logs & Debug
kubectl logs my-api-7d6b4c-xyz               # Logs
kubectl logs my-api-7d6b4c-xyz -f            # Follow logs
kubectl logs -l app=my-api --tail=100        # Logs của tất cả pods

kubectl exec -it my-api-7d6b4c-xyz -- bash  # SSH vào pod

# Port forward (dev/debug)
kubectl port-forward pod/my-api-7d6b4c-xyz 8080:8000
kubectl port-forward svc/my-api-service 8080:80

# Scale
kubectl scale deployment my-api --replicas=5

# Rolling update
kubectl set image deployment/my-api api=my-registry/my-api:1.1.0
kubectl rollout status deployment/my-api
kubectl rollout undo deployment/my-api       # Rollback
kubectl rollout history deployment/my-api
```

---

## Helm — Package Manager cho K8s

```bash
# Cài chart từ Helm Hub
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-postgres bitnami/postgresql \
  --set auth.password=secret \
  --namespace database \
  --create-namespace

# Tạo Helm chart riêng
helm create my-app
helm install my-app ./my-app -f values.prod.yaml
helm upgrade my-app ./my-app -f values.prod.yaml
helm rollback my-app 1
helm list
```

---

## Monitoring với Prometheus + Grafana

```bash
# Cài Prometheus stack qua Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

---

## Bài tập thực hành

- [ ] Cài minikube hoặc kind để chạy K8s local
- [ ] Deploy app với Deployment + Service + Ingress
- [ ] Cấu hình HPA và test auto-scaling
- [ ] Deploy full stack với Helm charts

---

## Tài nguyên thêm

- [Kubernetes Docs](https://kubernetes.io/docs/) — Chính thức
- [Play with Kubernetes](https://labs.play-with-k8s.com/) — Labs online miễn phí
- [KillerCoda](https://killercoda.com/) — Interactive K8s scenarios
- [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) — Hiểu sâu từ cơ bản
