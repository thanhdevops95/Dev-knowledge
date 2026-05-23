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

**Kubernetes** (K8s) is an open-source system for automating deployment, scaling, and management of containerized applications. It groups containers that make up an application into logical units for easy management and discovery.

*Kubernetes (K8s) là hệ thống mã nguồn mở để tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng container hóa.*

**Why K8s? (Tại sao dùng K8s?)**

- **Service discovery & Load balancing**: Automatically exposes containers (Tự động định tuyến traffic).
- **Self-healing**: Restarts failed containers (Tự khởi động lại container bị lỗi).
- **Automated rollouts/rollbacks**: Controlled updates (Cập nhật có kiểm soát).

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
