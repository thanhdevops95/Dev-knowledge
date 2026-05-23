# ☸️ Module 2.4: Kubernetes Core

[![Duration](https://img.shields.io/badge/Duration-1--2%20weeks-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Container Orchestration** - Deploy and manage containers with Kubernetes.
>
> *Điều phối Container - Deploy và quản lý containers với Kubernetes.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand Kubernetes architecture (Hiểu kiến trúc Kubernetes)
- ✅ Deploy applications with kubectl (Deploy ứng dụng với kubectl)
- ✅ Work with Pods, Deployments, Services (Làm việc với Pods, Deployments, Services)
- ✅ Use ConfigMaps and Secrets (Sử dụng ConfigMaps và Secrets)
- ✅ Implement Persistent storage (Triển khai lưu trữ bền vững)
- ✅ Perform Rolling updates and rollbacks (Thực hiện cập nhật và hoàn tác)

---

## 📚 Content (Nội dung)

### 1. What is Kubernetes? (Kubernetes là gì?)

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> Your company runs 50 microservices in Docker containers. One day, a container crashes at 3 AM. Who restarts it? The server runs out of memory. Which container should be killed? Traffic spikes 10x during Black Friday. How to scale quickly?
>
> *Công ty bạn chạy 50 microservices trong Docker containers. Một ngày, container crash lúc 3 giờ sáng. Ai sẽ khởi động lại? Server hết memory. Container nào nên bị kill? Traffic tăng gấp 10 lần ngày Black Friday. Làm sao scale nhanh?*
>
> **Kubernetes solves ALL these problems automatically!**
>
> *Kubernetes giải quyết TẤT CẢ các vấn đề này một cách tự động!*

**Kubernetes** (K8s) is an open-source system for automating deployment, scaling, and management of containerized applications. It groups containers that make up an application into logical units for easy management and discovery.

*Kubernetes (K8s) là hệ thống mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng container hóa.*

#### 1.1 Docker Alone vs Docker + Kubernetes (Docker đơn lẻ vs Docker + K8s)

| Scenario | Docker Alone | Docker + Kubernetes |
|----------|--------------|---------------------|
| Container crashes at 3 AM *(Container crash lúc 3h sáng)* | ❌ Manual restart needed *(Cần restart thủ công)* | ✅ Auto-restart in seconds *(Tự động restart trong giây)* |
| Scale from 3 to 30 instances *(Scale từ 3 lên 30 instances)* | ❌ Run 27 more `docker run` commands *(Chạy thêm 27 lệnh)* | ✅ `kubectl scale --replicas=30` *(1 lệnh duy nhất)* |
| Deploy new version *(Deploy phiên bản mới)* | ❌ Stop old, start new (downtime) *(Dừng cũ, chạy mới - có downtime)* | ✅ Rolling update, zero downtime *(Cập nhật tuần tự, không downtime)* |
| Load balance traffic *(Cân bằng tải traffic)* | ❌ Need external tool (Nginx, HAProxy) *(Cần tool bên ngoài)* | ✅ Built-in Service load balancing *(Tích hợp sẵn)* |
| Server dies *(Server chết)* | ❌ All containers lost *(Mất hết containers)* | ✅ Reschedule to other nodes *(Chuyển sang nodes khác)* |

#### 1.2 Why K8s? - Key Features (Tại sao dùng K8s? - Các tính năng chính)

- **Service discovery & Load balancing**: Automatically exposes containers and distributes traffic *(Tự động expose containers và phân phối traffic)*
- **Self-healing**: Restarts failed containers, replaces and reschedules containers *(Tự khởi động lại, thay thế và lên lịch lại containers)*
- **Automated rollouts/rollbacks**: Controlled updates with rollback capability *(Cập nhật có kiểm soát với khả năng rollback)*
- **Secret and configuration management**: Store sensitive information securely *(Quản lý cấu hình và thông tin nhạy cảm an toàn)*
- **Horizontal scaling**: Scale up/down based on demand *(Mở rộng theo chiều ngang dựa trên nhu cầu)*

### 2. Architecture (Kiến trúc)

```
┌─────────────────────────────────────────┐
│              Control Plane               │
│  ┌─────────┐ ┌─────────┐ ┌───────────┐  │
│  │ API     │ │ etcd    │ │ Scheduler │  │
│  │ Server  │ │         │ │           │  │
│  └─────────┘ └─────────┘ └───────────┘  │
│  ┌─────────────────────────────────────┐│
│  │     Controller Manager              ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
            │
┌───────────┼───────────────────────────┐
│           │      Worker Nodes          │
│  ┌────────┴────────┐  ┌──────────────┐│
│  │     kubelet     │  │ kube-proxy   ││
│  └─────────────────┘  └──────────────┘│
│  ┌─────────────────────────────────────┐
│  │            Pods                     ││
│  └─────────────────────────────────────┘
└───────────────────────────────────────┘
```

**Architecture Components (Thành phần kiến trúc):**

- **Control Plane**: The brain of the cluster (Bộ não của cluster - quản lý tất cả).
  - **API Server**: Front-end for the Kubernetes control plane (Cổng giao tiếp chính).
  - **etcd**: Key-value store for all cluster data (Nơi lưu trữ dữ liệu của cluster).
  - **Scheduler**: Assigns pods to nodes (Phân phối pod vào các node).
  - **Controller Manager**: Runs controller processes (Quản lý các controller).
- **Worker Nodes**: Machines that run your applications (Máy chạy ứng dụng).
  - **kubelet**: Agent that runs on each node (Agent chạy trên mỗi node).
  - **kube-proxy**: Maintains network rules (Quản lý mạng).
  - **Pods**: The smallest deployable units (Đơn vị nhỏ nhất có thể deploy).

### 3. Basic Resources (Tài nguyên cơ bản)

```yaml
# Pod
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx:alpine
      ports:
        - containerPort: 80

---
# Deployment
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

---
# Service
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

### 4. kubectl Commands (Các lệnh kubectl)

These are the essential kubectl commands you'll use daily to interact with your Kubernetes cluster.

*Đây là các lệnh kubectl cần thiết bạn sẽ dùng hàng ngày để tương tác với Kubernetes cluster.*

```bash
# Cluster info (Thông tin cluster)
kubectl cluster-info
kubectl get nodes

# Pods
kubectl get pods
kubectl describe pod <name>
kubectl logs <pod>
kubectl exec -it <pod> -- sh

# Deployments
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=3
kubectl set image deployment/nginx nginx=nginx:1.20

# Services
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get services

# Apply manifests (Áp dụng manifests)
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
```

### 5. ConfigMaps & Secrets

ConfigMaps store non-sensitive configuration data, while Secrets store sensitive data like passwords.

*ConfigMaps lưu dữ liệu cấu hình không nhạy cảm, còn Secrets lưu dữ liệu nhạy cảm như mật khẩu.*

```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
  LOG_LEVEL: info

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQ=  # base64 encoded (mã hóa base64)
```

### 6. Persistent Volume (Volume bền vững)

Persistent Volumes allow data to survive pod restarts. Essential for databases.

*Persistent Volumes giúp dữ liệu tồn tại khi pod khởi động lại. Cần thiết cho databases.*

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

---
# Use in Pod (Sử dụng trong Pod)
spec:
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data-pvc
  containers:
    - name: app
      volumeMounts:
        - mountPath: /data
          name: data
```

---

### 7. Troubleshooting Pods (Xử lý sự cố Pods)

One of the most important skills for a DevOps engineer is debugging Kubernetes issues.

*Một trong những kỹ năng quan trọng nhất cho DevOps engineer là debug các vấn đề Kubernetes.*

#### 7.1 Common Pod States (Các trạng thái Pod phổ biến)

| Status | Meaning | Common Cause |
|--------|---------|-------------|
| `Pending` | Pod waiting to be scheduled *(Pod đang chờ được lên lịch)* | No node with enough resources *(Không có node đủ tài nguyên)* |
| `ContainerCreating` | Pulling image or mounting volumes *(Đang pull image hoặc mount volumes)* | Large image, slow network *(Image lớn, mạng chậm)* |
| `Running` | Pod is running *(Pod đang chạy)* | ✅ Normal state |
| `CrashLoopBackOff` | Container keeps crashing *(Container liên tục crash)* | App error, missing config *(Lỗi app, thiếu config)* |
| `ImagePullBackOff` | Cannot pull container image *(Không thể pull image)* | Wrong image name, no auth *(Sai tên image, không có auth)* |
| `Terminating` | Pod is being deleted *(Pod đang bị xóa)* | Stuck finalizers *(Finalizers bị kẹt)* |

#### 7.2 Debugging Commands (Các lệnh debug)

```bash
# Check pod status (Kiểm tra trạng thái pod)
kubectl get pods
kubectl get pods -o wide              # Show node, IP
kubectl get pods --all-namespaces     # All namespaces (Tất cả namespaces)

# Describe pod - shows events, errors (Xem chi tiết - hiển thị events, lỗi)
kubectl describe pod <pod-name>

# View logs (Xem logs)
kubectl logs <pod-name>
kubectl logs <pod-name> -f            # Follow mode
kubectl logs <pod-name> --previous    # Previous crashed container (Container đã crash trước)

# Execute into pod (Vào trong pod)
kubectl exec -it <pod-name> -- sh
kubectl exec -it <pod-name> -- /bin/bash

# Check events (Kiểm tra events)
kubectl get events --sort-by='.lastTimestamp'
```

#### 7.3 Common Issues and Solutions (Vấn đề thường gặp và cách giải quyết)

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| **CrashLoopBackOff** | `kubectl logs <pod> --previous` | Fix app error, check env vars *(Sửa lỗi app, kiểm tra biến môi trường)* |
| **ImagePullBackOff** | `kubectl describe pod <pod>` | Check image name, create imagePullSecret *(Kiểm tra tên image, tạo secret)* |
| **Pending** | `kubectl describe pod <pod>` | Add more nodes, reduce resource requests *(Thêm nodes, giảm resource requests)* |
| **OOMKilled** | `kubectl describe pod <pod>` | Increase memory limit *(Tăng memory limit)* |

---

### 8. Ingress - External Access (Truy cập từ bên ngoài)

Ingress exposes HTTP/HTTPS routes from outside the cluster to services within the cluster.

*Ingress expose các routes HTTP/HTTPS từ bên ngoài cluster vào các services bên trong.*

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

---

### 9. Horizontal Pod Autoscaler - HPA (Tự động mở rộng Pod)

HPA automatically scales the number of pods based on CPU/memory usage.

*HPA tự động scale số lượng pods dựa trên CPU/memory usage.*

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
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

```bash
# Create HPA via kubectl (Tạo HPA qua kubectl)
kubectl autoscale deployment my-app --min=2 --max=10 --cpu-percent=70

# Check HPA status (Kiểm tra trạng thái HPA)
kubectl get hpa
```

---

### 10. Best Practices (Thực hành tốt nhất)

| Practice | Description |
|----------|-------------|
| **Use namespaces** | Separate environments (dev, staging, prod) *(Tách biệt môi trường)* |
| **Set resource limits** | Prevent one pod from consuming all resources *(Ngăn pod chiếm hết tài nguyên)* |
| **Use liveness/readiness probes** | K8s knows when app is healthy *(K8s biết khi nào app khỏe mạnh)* |
| **Don't use latest tag** | Specify version for reproducibility *(Chỉ định version để tái tạo)* |
| **Use ConfigMaps/Secrets** | Don't hardcode config in images *(Không hardcode config trong images)* |
| **Implement RBAC** | Principle of least privilege *(Nguyên tắc quyền tối thiểu)* |

---

> ✅ **Checkpoint - Before continuing, make sure you can answer:**
> *(Trước khi tiếp tục, hãy chắc bạn có thể trả lời:)*
>
> - [ ] What's the difference between a Pod and a Deployment? *(Pod và Deployment khác nhau như thế nào?)*
> - [ ] How to debug a CrashLoopBackOff pod? *(Làm sao debug pod CrashLoopBackOff?)*
> - [ ] What does a Service do? *(Service làm gì?)*
> - [ ] When to use ConfigMap vs Secret? *(Khi nào dùng ConfigMap vs Secret?)*
>
> *If you can't answer, please re-read the sections above!*

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [2.3 Jenkins](../2.3_Jenkins/) | **2.4 Kubernetes Core** | [2.5 Monitoring](../2.5_Monitoring_Logging/) |

---

**Master container orchestration with Kubernetes! ☸️**

*Thành thạo điều phối container với Kubernetes!*

</div>
