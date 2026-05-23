# Module 09: Kubernetes

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Kubernetes** | /kuːbərˈnetiːz/ | K8s - Nền tảng điều phối container |
| **Cluster** | - | Cụm - Tập hợp các nodes chạy K8s |
| **Node** | - | Máy chạy workloads (worker node) |
| **Control Plane** | - | Thành phần điều khiển cluster |
| **Pod** | - | Đơn vị nhỏ nhất, thường chứa 1 container |
| **Deployment** | - | Quản lý Pods: replicas, updates, rollbacks |
| **Service** | - | Expose Pods ra network, load balancing |
| **Namespace** | - | Không gian tên - Phân tách môi trường trong cluster |
| **ConfigMap** | - | Lưu trữ cấu hình non-sensitive |
| **Secret** | - | Lưu trữ dữ liệu nhạy cảm (mã hóa) |
| **Ingress** | - | Expose HTTP/HTTPS từ ngoài cluster |
| **kubectl** | - | CLI tool để tương tác với K8s |
| **Replica** | - | Bản sao của Pod |
| **Rolling Update** | - | Cập nhật từng pod một, không downtime |

---

## 🎬 Câu chuyện mở đầu

Docker giúp bạn đóng gói app. Nhưng khi cần:

- Chạy 100 containers
- Auto-restart khi crash
- Load balancing
- Rolling updates
- Scaling tự động

Bạn cần một **Container Orchestrator**. Và **Kubernetes** là tiêu chuẩn.

---

## 📖 Kubernetes là gì?

### Ẩn dụ: Nhạc trưởng dàn nhạc

```
┌─────────────────────────────────────────────────────────────┐
│                      KUBERNETES                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Bạn: "Tôi muốn 3 replicas của app"                         │
│            │                                                 │
│            ▼                                                 │
│   K8s: "OK, để tôi lo"                                       │
│            │                                                 │
│            ├── Tìm nodes có resources                        │
│            ├── Schedule containers                           │
│            ├── Setup networking                              │
│            ├── Monitor health                                │
│            └── Restart nếu crash                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Kiến trúc K8s

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL PLANE                             │
├─────────────────────────────────────────────────────────────┤
│  API Server │ Scheduler │ Controller Manager │ etcd         │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ kubectl / API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       WORKER NODES                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Node 1    │  │   Node 2    │  │   Node 3    │         │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │         │
│  │ │  Pod 1  │ │  │ │  Pod 3  │ │  │ │  Pod 5  │ │         │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │         │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │             │         │
│  │ │  Pod 2  │ │  │ │  Pod 4  │ │  │             │         │
│  │ └─────────┘ │  │ └─────────┘ │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Core Objects - Hiểu từ bản chất

Trước khi đi vào từng object, hãy hiểu **tầng nền tảng** trước:

### 🧱 Nền tảng: Process → Container → Pod

**Trong máy tính thông thường:**

Khi bạn chạy một chương trình (ví dụ: `python app.py`), hệ điều hành tạo ra một **process**. Process này:

- Có bộ nhớ riêng
- Có CPU time riêng
- Có thể đọc/ghi files
- Có thể mở network ports

**Vấn đề:** Process A trên máy bạn có thể khác Process A trên máy server (khác version Python, khác thư viện, khác config). Đây là nguồn gốc của "works on my machine".

**Container ra đời để giải quyết vấn đề này:**

**Container = Process + Môi trường đóng gói**

Container là một process (hoặc group processes) chạy trong môi trường **cô lập và đóng gói sẵn**:

- Có filesystem riêng (chứa sẵn code, thư viện, config)
- Có network riêng
- Không thấy các process khác trên cùng máy

```
Thông thường:                        Container:
┌─────────────────────┐              ┌─────────────────────┐
│    Máy vật lý       │              │    Máy vật lý       │
│                     │              │                     │
│  App A   App B      │              │  ┌─────┐ ┌─────┐   │
│    │       │        │              │  │App A│ │App B│   │
│    └───────┴────────│              │  │+libs│ │+libs│   │
│         │           │              │  │+conf│ │+conf│   │
│      OS chung       │              │  └──┬──┘ └──┬──┘   │
└─────────────────────┘              │     │       │      │
                                     │   Cô lập  Cô lập   │
App A, B dùng chung thư viện         └─────────────────────┘
→ Dễ conflict                        Mỗi container độc lập
```

**Bây giờ đến Pod:**

**Pod = Vỏ bọc của Kubernetes cho containers**

Kubernetes **không trực tiếp quản lý container**. Nó quản lý **Pod** - một đơn vị bao gồm:

- Một hoặc nhiều containers (thường là một)
- Shared network (các containers trong Pod dùng chung IP, có thể gọi nhau qua `localhost`)
- Shared storage volumes (các containers có thể đọc/ghi cùng files)

**Tại sao không quản lý container trực tiếp?**

Vì đôi khi bạn cần **nhiều processes hỗ trợ nhau** chạy cùng nhau:

| Ví dụ | Main container | Sidecar container |
|-------|----------------|-------------------|
| Logging | App | Log collector (gửi logs đi) |
| Security | App | Proxy (mã hóa traffic) |
| Sync | App | File syncer (sync data từ remote) |

Các containers này **phải chạy cùng máy**, **phải share network**, **phải cùng sống cùng chết**. → Pod là đơn vị logic cho việc này.

**Ẩn dụ để nhớ:**

```
Container = Một người             Pod = Một căn phòng
                                  
Người A làm việc riêng            Phòng chứa 1-2 người
                                  làm việc chung
                                  
                                  Chung điện, nước (network)
                                  Chung bàn ghế (storage)
                                  Phòng bị đóng = tất cả ra ngoài
```

**90% trường hợp:** Một Pod chứa một container. Nhưng bạn cần hiểu Pod để hiểu tại sao K8s thiết kế như vậy.

---

### Pod - Chi tiết

**Định nghĩa chính xác:**

> Pod là đơn vị triển khai nhỏ nhất trong Kubernetes. Nó là một nhóm gồm một hoặc nhiều containers, được schedule (đặt) trên cùng một node, chia sẻ network namespace và có thể chia sẻ storage volumes.

**Đặc điểm quan trọng:**

| Đặc điểm | Ý nghĩa thực tế |
|----------|-----------------|
| **IP duy nhất** | Mỗi Pod có một IP riêng trong cluster. Containers trong Pod dùng chung IP này. |
| **Ephemeral (tạm thời)** | Pod có thể bị xóa và tạo lại bất cứ lúc nào. **Không lưu data quan trọng trong Pod.** |
| **Không tự restart** | Nếu Pod chết, nó không tự sống lại. Cần Deployment để quản lý. |

**Khi nào cần hiểu Pod?**

- **Debug:** `kubectl describe pod my-app` để xem tại sao Pod không chạy
- **Logs:** `kubectl logs my-app` để xem output của container trong Pod
- **Exec:** `kubectl exec -it my-app -- bash` để vào trong container

**Ví dụ YAML:**

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
    - name: web
      image: nginx:1.25
      ports:
        - containerPort: 80
```

**Giải thích từng trường:**

| Trường | Ý nghĩa |
|--------|---------|
| `apiVersion: v1` | Version của K8s API cho loại object này. Pod dùng `v1`. |
| `kind: Pod` | Loại object bạn muốn tạo. |
| `metadata.name` | Tên duy nhất của Pod trong namespace. |
| `metadata.labels` | Nhãn dán - dùng để **phân loại và tìm kiếm** Pods. Service dùng labels để biết forward traffic đến Pods nào. |
| `spec.containers` | Danh sách containers chạy trong Pod. |
| `image: nginx:1.25` | Docker image. K8s sẽ pull image này và chạy container từ nó. |
| `containerPort: 80` | Port mà container lắng nghe. Đây là **thông tin khai báo**, K8s không tự động expose port này ra ngoài. |

---

### Deployment - "Người quản lý" Pods

**Vấn đề Pod có:**

1. Pod chết → không tự sống lại
2. Muốn chạy 3 bản sao Pod → phải tạo 3 file YAML
3. Muốn update image → phải xóa Pod cũ, tạo Pod mới thủ công

**Deployment giải quyết tất cả:**

> Deployment là object quản lý một nhóm Pods giống hệt nhau. Nó đảm bảo số lượng Pods mong muốn luôn chạy, tự động thay thế Pods chết, và hỗ trợ update/rollback.

**Ẩn dụ:**

```
Pod = Nhân viên                   Deployment = Quản lý nhân sự
                                  
Nhân viên nghỉ việc               "Tôi cần 3 nhân viên vị trí này"
→ Không ai thay                   → Tự động tuyển người mới thay
                                  
                                  "Đào tạo lại tất cả" (update)
                                  "Quay lại cách làm cũ" (rollback)
```

**So sánh trực tiếp:**

| Dùng Pod trực tiếp | Dùng Deployment |
|-------------------|-----------------|
| Pod chết = App chết, phải tạo lại thủ công | Pod chết → K8s tự động tạo Pod mới |
| Muốn 5 Pods = tạo 5 file YAML | `replicas: 5` trong một file |
| Update = delete + create thủ công | Đổi image → K8s tự rolling update |
| Rollback = nhớ config cũ, tạo lại | `kubectl rollout undo` |

**Thực tế:** Bạn **hầu như không bao giờ tạo Pod trực tiếp**. Luôn dùng Deployment.

**Ví dụ YAML:**

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
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.25
          ports:
            - containerPort: 80
          resources:
            limits:
              memory: "128Mi"
              cpu: "500m"
```

**Giải thích các trường quan trọng:**

| Trường | Ý nghĩa |
|--------|---------|
| `replicas: 3` | "Tôi muốn luôn có đúng 3 Pods chạy". Nếu 1 Pod chết, K8s tạo Pod mới. Nếu có 4 Pods, K8s xóa 1. |
| `selector.matchLabels` | Deployment quản lý những Pods nào? Những Pods có label `app: web`. |
| `template` | "Khuôn" để tạo Pods mới. Khi Pod chết, K8s dùng template này tạo Pod thay thế. |
| `template.metadata.labels` | Labels của Pods được tạo. **Phải match với selector.matchLabels**, nếu không Deployment không quản lý được Pods nó tạo ra! |
| `resources.limits.cpu: "500m"` | Giới hạn CPU tối đa. `1000m = 1 CPU core`, nên `500m = 0.5 core`. |
| `resources.limits.memory: "128Mi"` | Giới hạn RAM tối đa. `Mi = Mebibyte ≈ MB`. |

---

### Service - "Địa chỉ cố định" cho Pods

**Vấn đề:**

1. Pod có IP, nhưng IP **thay đổi** mỗi khi Pod restart
2. Có 3 Pods giống nhau, làm sao **chia đều traffic**?
3. App bên ngoài cluster muốn gọi app trong cluster, gọi đến đâu?

**Service giải quyết:**

> Service là object cung cấp một **địa chỉ cố định** (IP + DNS name) trỏ đến một nhóm Pods. Nó hoạt động như một load balancer nội bộ.

**Ẩn dụ:**

```
Pods = Nhân viên tổng đài          Service = Số hotline 1900xxxx
                                   
Nhân viên nghỉ/thay ca             Số hotline không đổi
→ Số điện thoại cá nhân đổi        → Khách gọi vẫn được phục vụ
                                   
                                   Cuộc gọi tự động chia cho
                                   nhân viên đang rảnh
```

**Cách Service tìm Pods:**

Service dùng **selector** để tìm Pods có labels phù hợp:

```yaml
Service selector:     Pods labels:
  app: web       ──→  app: web  ✓ (match)
                 ──→  app: api  ✗ (không match)
```

**Ví dụ YAML:**

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: web
  ports:
    - port: 80          # Port mà Service lắng nghe
      targetPort: 80    # Port mà container lắng nghe
  type: ClusterIP
```

**Giải thích:**

| Trường | Ý nghĩa |
|--------|---------|
| `selector.app: web` | Service này forward traffic đến Pods có label `app: web`. |
| `port: 80` | Clients gọi đến Service qua port 80. |
| `targetPort: 80` | Service forward đến container port 80. |
| `type: ClusterIP` | Loại Service (xem bảng dưới). |

**Các loại Service:**

| Type | Ai có thể truy cập? | Use case | Ví dụ |
|------|---------------------|----------|-------|
| `ClusterIP` | Chỉ bên trong cluster | Service gọi service khác | API gọi Database |
| `NodePort` | Bên ngoài qua `NodeIP:NodePort` | Testing, development | `http://192.168.1.10:30080` |
| `LoadBalancer` | Internet qua Cloud Load Balancer | Production public services | Website, public API |

**Sau khi tạo Service, bạn có thể:**

```bash
# Từ Pod khác trong cluster, gọi bằng DNS:
curl http://my-app-service        # Tự động resolve IP
curl http://my-app-service.default.svc.cluster.local  # Full DNS name
```

---

### ConfigMap & Secret - "Cấu hình bên ngoài code"

**Vấn đề thực tế:**

Bạn có một Docker image `myapp:1.0`. Muốn chạy trên 3 môi trường:

| Môi trường | Database URL | Log Level |
|------------|--------------|-----------|
| Development | `localhost:5432` | `debug` |
| Staging | `db-staging.internal:5432` | `info` |
| Production | `db-prod.internal:5432` | `warn` |

**Cách sai:** Tạo 3 images khác nhau (`myapp:1.0-dev`, `myapp:1.0-staging`, `myapp:1.0-prod`).

**Cách đúng:** Một image, **cấu hình tiêm từ bên ngoài** qua ConfigMap/Secret.

**ConfigMap vs Secret:**

| | ConfigMap | Secret |
|-|-----------|--------|
| **Chứa gì** | Config không nhạy cảm | Dữ liệu nhạy cảm |
| **Ví dụ** | Database host, log level, feature flags | Passwords, API keys, certificates |
| **Lưu trữ** | Plain text | Base64 encoded (không phải encrypted!) |

> ⚠️ **Lưu ý:** Secret chỉ encode base64, **không mã hóa**. Để bảo mật thực sự, cần dùng thêm tool như Sealed Secrets hoặc Vault.

**Ví dụ YAML:**

```yaml
# configmap.yaml - Cấu hình không nhạy cảm
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "db-prod.internal"
  DATABASE_PORT: "5432"
  LOG_LEVEL: "info"

---
# secret.yaml - Dữ liệu nhạy cảm
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:                     # stringData = tự động encode base64
  DATABASE_PASSWORD: "supersecret"
  API_KEY: "abc123xyz"
```

**Cách sử dụng trong Deployment:**

```yaml
# deployment.yaml (trích)
spec:
  containers:
    - name: web
      image: myapp:1.0
      envFrom:
        - configMapRef:
            name: app-config      # Tất cả keys trong ConfigMap → env vars
        - secretRef:
            name: app-secrets     # Tất cả keys trong Secret → env vars
```

Khi container chạy, nó sẽ có environment variables:

```
DATABASE_HOST=db-prod.internal
DATABASE_PORT=5432
LOG_LEVEL=info
DATABASE_PASSWORD=supersecret
API_KEY=abc123xyz
```

---

## 🔧 kubectl Commands

```bash
# Get resources
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get all

# Apply config
kubectl apply -f deployment.yaml

# Delete
kubectl delete -f deployment.yaml
kubectl delete pod my-pod

# Describe (debug)
kubectl describe pod my-pod

# Logs
kubectl logs my-pod
kubectl logs -f my-pod  # follow

# Exec
kubectl exec -it my-pod -- bash

# Scale
kubectl scale deployment my-app --replicas=5

# Rollout
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app
```

---

## 🚨 Lỗi thường gặp khi học Kubernetes

### 1. Pod ở trạng thái "CrashLoopBackOff"

**Triệu chứng:**

```bash
kubectl get pods
# NAME       READY   STATUS             RESTARTS   AGE
# my-app     0/1     CrashLoopBackOff   5          2m
```

**Nguyên nhân:** Container start rồi crash liên tục. K8s cố restart nhưng vẫn fail.

**Cách debug:**

```bash
# Xem logs của container
kubectl logs my-app
kubectl logs my-app --previous  # Logs trước khi crash

# Xem chi tiết events
kubectl describe pod my-app

# Nguyên nhân thường gặp:
# - Config sai (env vars, secrets không tồn tại)
# - Container command exit ngay
# - App crash do exception
```

---

### 2. Pod ở trạng thái "ImagePullBackOff"

**Triệu chứng:**

```bash
kubectl get pods
# NAME       READY   STATUS             RESTARTS   AGE
# my-app     0/1     ImagePullBackOff   0          1m
```

**Nguyên nhân:** K8s không pull được Docker image.

**Cách fix:**

```bash
# Kiểm tra image name có đúng không
kubectl describe pod my-app | grep "Image:"

# Nguyên nhân thường gặp:
# - Typo trong image name
# - Private registry cần imagePullSecrets
# - Image tag không tồn tại
```

---

### 3. Service không connect được đến Pods

**Triệu chứng:** Gọi Service nhưng không có response.

**Nguyên nhân:** Labels của Service selector không match với Pod labels.

**Cách debug:**

```bash
# Xem Service đang select labels nào
kubectl describe service my-service | grep Selector

# Xem Pods có labels đúng không
kubectl get pods --show-labels

# Xem endpoints của Service (danh sách Pod IPs)
kubectl get endpoints my-service
# Nếu ENDPOINTS trống = không có Pod nào match!
```

---

### 4. "0/3 nodes are available: insufficient memory"

**Triệu chứng:** Pod pending, không được schedule.

**Nguyên nhân:** Không đủ resources trên nodes.

**Cách fix:**

```bash
# Xem resource usage
kubectl top nodes
kubectl top pods

# Cách fix:
# - Giảm resource requests trong Deployment
# - Scale down các Pods khác
# - Thêm nodes vào cluster

# Ví dụ giảm resources:
resources:
  requests:
    memory: "64Mi"   # Giảm từ 128Mi
    cpu: "100m"       # Giảm từ 500m
```

---

### 5. Deployment update nhưng Pods không đổi

**Triệu chứng:** Edit Deployment nhưng không thấy Pods mới.

**Nguyên nhân:** Thường do chỉ đổi ConfigMap/Secret mà không đổi Pod spec.

**Cách fix:**

```bash
# Force rollout restart
kubectl rollout restart deployment/my-app

# Hoặc thêm annotation để trigger update
kubectl patch deployment my-app \
  -p '{"spec":{"template":{"metadata":{"annotations":{"date":"'$(date +%s)'"}}}}}'
```

---

## 📝 Tổng kết

Trong module này bạn đã học:

✅ Container → Pod → Deployment: Hệ thống phân cấp  
✅ Service: Địa chỉ cố định cho Pods  
✅ ConfigMap & Secret: Tách config khỏi code  
✅ kubectl: CLI để quản lý cluster  
✅ Debug: Cách xử lý lỗi thường gặp  

👉 **[LABS.md](LABS.md)** | **[SCENARIOS.md](SCENARIOS.md)**
