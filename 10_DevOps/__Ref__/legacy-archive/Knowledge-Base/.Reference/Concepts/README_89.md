# 📘 MODULE 04: CD - Continuous Deployment with Kubernetes

## 🤔 Tại sao cần CD và K8s?

### Ẩn dụ: Bến cảng container

**Kubernetes** giống như **bến cảng container**:

- Containers (Docker) = Các container hàng hóa
- Kubernetes = Hệ thống điều phối, sắp xếp containers
- Tự động: Xếp container, phân phối, thay thế container hỏng

**CD** = Tự động cập nhật phiên bản mới:

- Code mới → Build → Test → Deploy tự động
- Không cần ssh vào server, copy file thủ công

---

## 🏗️ Kubernetes Architecture

```mermaid
graph TB
    A[Developer] -->|git push| B[GitHub]
    B -->|webhook| C[CI builds image]
    C -->|push| D[Docker Registry]
    D -->|pull| E[Kubernetes Cluster]
    
    subgraph Kubernetes
        E --> F[Pod 1<br/>App]
        E --> G[Pod 2<br/>App]
        E --> H[Pod 3<br/>Redis]
        I[Service<br/>Load Balancer] --> F
        I --> G
    end
    
    J[Users] --> I
```

---

## 📦 K8s Core Concepts

### 1. Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: counter-pod
spec:
  containers:
  - name: web
    image: counter-app:v1.0
    ports:
    - containerPort: 5000
```

### 2. Deployment (Manages Pods)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: counter-deployment
spec:
  replicas: 3  # 3 pods
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
```

### 3. Service (Load Balancer)

```yaml
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

---

## 🔄 GitOps with ArgoCD

**GitOps** = Git is the source of truth

```mermaid
graph LR
    A[Developer] -->|1. Update YAML| B[Git Repo]
    B -->|2. ArgoCD detects change| C[ArgoCD]
    C -->|3. Sync| D[Kubernetes Cluster]
    D -->|4. Status| C
    C -->|5. Alert if diff| A
```

**Benefits:**

- Declarative config
- Version control for infrastructure
- Easy rollback (git revert)

---

## 💡 Key Takeaways

1. **K8s = Container orchestrator** - Tự động quản lý lifecycle
2. **Deployment > Pod** - Deployment manages replicas
3. **Service = Internal load balancer** - Distribute traffic
4. **GitOps** - Git làm single source of truth

⏭️ Next: **LABS.md**
