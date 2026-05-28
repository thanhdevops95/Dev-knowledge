# ☸️ Kubernetes cơ bản — Điều phối container

> `[INTERMEDIATE → ADVANCED]` ⭐ `[MUST-KNOW]` — Quản lý container ở quy mô lớn

---

## Tại sao cần Kubernetes?

Docker chạy tốt trên **1 máy**. Nhưng production cần:
- Chạy trên **nhiều máy** (cluster)
- **Tự khởi động lại** khi container crash
- **Scale** lên-xuống theo traffic
- **Rolling update** không downtime
- **Load balancing** tự động

**Kubernetes (K8s)** giải quyết tất cả.

---

## 1. Kiến trúc K8s

```
┌─────────────────── Kubernetes Cluster ──────────────────┐
│                                                          │
│  ┌─── Control Plane (Master) ────────────────────────┐  │
│  │  ┌──────────┐ ┌──────────┐ ┌────────────────────┐│  │
│  │  │ API      │ │ etcd     │ │ Controller Manager ││  │
│  │  │ Server   │ │ (DB)     │ │ + Scheduler        ││  │
│  │  └──────────┘ └──────────┘ └────────────────────┘│  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
│            kubelet + kube-proxy                          │
│                          │                               │
│  ┌─── Worker Node 1 ────┴──── Worker Node 2 ────────┐  │
│  │  ┌──────┐ ┌──────┐      ┌──────┐ ┌──────┐       │  │
│  │  │Pod A │ │Pod B │      │Pod C │ │Pod D │       │  │
│  │  │┌────┐│ │┌────┐│      │┌────┐│ │┌────┐│       │  │
│  │  ││ 🐳 ││ ││ 🐳 ││      ││ 🐳 ││ ││ 🐳 ││       │  │
│  │  │└────┘│ │└────┘│      │└────┘│ │└────┘│       │  │
│  │  └──────┘ └──────┘      └──────┘ └──────┘       │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Thành phần chính:**
- **API Server**: Cổng vào duy nhất — kubectl giao tiếp qua đây
- **etcd**: Database lưu trạng thái cluster
- **Scheduler**: Quyết định Pod chạy trên Node nào
- **Controller Manager**: Đảm bảo trạng thái thực = trạng thái mong muốn
- **kubelet**: Agent trên mỗi Node, quản lý Pods
- **kube-proxy**: Networking, load balancing

---

## 2. Các khái niệm cốt lõi

### Pod — Đơn vị nhỏ nhất

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: web
spec:
  containers:
    - name: app
      image: myapp:1.0
      ports:
        - containerPort: 3000
      resources:
        requests:
          cpu: "100m"      # 0.1 CPU
          memory: "128Mi"
        limits:
          cpu: "500m"      # Max 0.5 CPU
          memory: "256Mi"
```

### Deployment — Quản lý Pods

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3                    # Chạy 3 bản copy
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: app
          image: myapp:2.0
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
          readinessProbe:        # Kiểm tra app sẵn sàng
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:         # Kiểm tra app còn sống
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
  strategy:
    type: RollingUpdate          # Update từng pod
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0          # Không downtime!
```

### Service — Expose Pods ra bên ngoài

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web                     # Tìm Pods có label app=web
  type: ClusterIP                # Chỉ trong cluster
  ports:
    - port: 80                   # Port của Service
      targetPort: 3000           # Port của container
---
# LoadBalancer — expose ra internet
apiVersion: v1
kind: Service
metadata:
  name: web-public
spec:
  selector:
    app: web
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 3000
```

```
Bên ngoài ──► Service (Load Balancer) ──┬──► Pod 1
              (web-service:80)          ├──► Pod 2
                                        └──► Pod 3
Service tự load balance giữa các Pods!
```

### ConfigMap & Secret

```yaml
# ConfigMap — cấu hình KHÔNG nhạy cảm
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"

---
# Secret — dữ liệu nhạy cảm (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAZGI6NTQzMi9teWRi  # base64
```

---

## 3. kubectl — Lệnh cơ bản

```bash
# Xem resources
kubectl get pods                   # Liệt kê pods
kubectl get pods -o wide           # Chi tiết (IP, Node)
kubectl get deployments
kubectl get services
kubectl get all                    # Tất cả resources

# Tạo/cập nhật
kubectl apply -f deployment.yaml   # Tạo hoặc update
kubectl delete -f deployment.yaml  # Xóa

# Debug
kubectl describe pod my-pod        # Chi tiết về pod
kubectl logs my-pod                # Xem logs
kubectl logs my-pod -f             # Follow logs
kubectl exec -it my-pod -- sh     # Vào shell container

# Scale
kubectl scale deployment web-app --replicas=5

# Rolling update
kubectl set image deployment/web-app app=myapp:3.0
kubectl rollout status deployment/web-app
kubectl rollout undo deployment/web-app    # Rollback!
```

---

## 4. Ingress — Routing HTTP

```yaml
# Ingress — reverse proxy cho cluster
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - myapp.com
      secretName: tls-secret
  rules:
    - host: myapp.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

---

## 5. HPA — Auto Scaling

```yaml
# Tự động scale dựa trên CPU/Memory
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70   # Scale khi CPU > 70%
```

---

## K8s vs Docker Compose

| | Docker Compose | Kubernetes |
|---|---|---|
| **Dùng cho** | Dev, small projects | Production, scale lớn |
| **Máy** | 1 máy | Multi-node cluster |
| **Self-healing** | Restart only | Reschedule, replace |
| **Scaling** | Manual | Auto (HPA) |
| **Rolling update** | ❌ | ✅ Zero-downtime |
| **Service discovery** | Docker DNS | K8s DNS + Services |
| **Learning curve** | Thấp | Cao |

---

## Các lỗi thường gặp

```
❌ Sai: Không set resource limits → 1 pod "ăn" hết RAM
✅ Đúng: LUÔN set requests và limits cho CPU/Memory

❌ Sai: Dùng :latest tag → không kiểm soát version
✅ Đúng: Pin version cụ thể: myapp:2.0.1

❌ Sai: Lưu secrets trong ConfigMap
✅ Đúng: Dùng Secrets (hoặc external secret manager)

❌ Sai: Không có health checks → K8s không biết pod lỗi
✅ Đúng: Luôn có readinessProbe + livenessProbe
```

---

## Bài tập thực hành

- [ ] Deploy ứng dụng lên minikube (local K8s): Deployment + Service
- [ ] Thêm ConfigMap, Secret cho database URL
- [ ] Implement rolling update: deploy version mới, rollback nếu lỗi
- [ ] Setup HPA: scale từ 2→5 pods khi CPU > 70%

---

## Tài nguyên thêm

- [Kubernetes Official Tutorial](https://kubernetes.io/docs/tutorials/) — Hands-on
- [Learn Kubernetes Basics (Interactive)](https://kubernetes.io/docs/tutorials/kubernetes-basics/) — Trong browser
- [KillerCoda](https://killercoda.com/playgrounds/scenario/kubernetes) — Playground miễn phí
