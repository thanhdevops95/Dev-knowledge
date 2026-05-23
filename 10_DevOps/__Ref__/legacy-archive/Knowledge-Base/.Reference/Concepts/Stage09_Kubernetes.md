# GIAI ĐOẠN 9: KUBERNETES - BẬC THẦY ĐIỀU PHỐI

## 📌 MỤC TIÊU GIAI ĐOẠN 9
Docker Compose rất tuyệt, nhưng nó chỉ chạy trên 1 máy. Khi bạn có 1000 containers chạy trên 50 server, bạn cần **Kubernetes**.
K8s giúp:
✅ **Self-healing:** App chết tự dựng lại.
✅ **Scaling:** App quá tải tự đẻ thêm.
✅ **Load Balancing:** Tự chia tải.

---

## 🛠️ PHẦN 1: VIẾT MANIFESTS (YAML)

Trong K8s, ta không dùng `docker-compose.yaml` mà dùng các object: **Deployment** (quản lý Pods) và **Service** (mở cổng mạng).

Tạo các file sau trong thư mục `k8s/`:

### 1. `k8s/mysql.yaml`
*(Database cần Persistent Volume để dữ liệu không mất)*
```yaml
apiVersion: v1
kind: PersistentVolumeClaim # Yêu cầu cấp ổ cứng
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: secret
        - name: MYSQL_DATABASE
          value: todo_db
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: db      # Tên DNS nội bộ (code Go sẽ gọi host: 'db')
spec:
  ports:
  - port: 3306
  selector:
    app: mysql
```

### 2. `k8s/backend.yaml` (Go Service)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 2           # Chạy luôn 2 bản sao (High Availability!)
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: your-docker-user/todo-go:latest # Thay bằng user DockerHub của bạn
        env:
        - name: DB_HOST
          value: db
        - name: DB_PASSWORD
          value: secret
---
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  ports:
  - port: 8081
  selector:
    app: backend
```

### 3. `k8s/gateway.yaml` (Python Service)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gateway
  template:
    metadata:
      labels:
        app: gateway
    spec:
      containers:
      - name: gateway
        image: your-docker-user/todo-python:latest
        env:
        - name: GO_HOST
          value: backend
---
apiVersion: v1
kind: Service
metadata:
  name: gateway
spec:
  ports:
  - port: 8080
  selector:
    app: gateway
```

### 4. `k8s/ingress.yaml` (Thay cho Nginx Container cũ)
Trong K8s, ta thường dùng **Ingress Controller** thay vì tự chạy Nginx container thủ công. Tuy nhiên để đơn giản ở bài này (Minikube), ta sẽ dùng `NodePort` hoặc `LoadBalancer` để expose Gateway/Web.

Nhưng chờ đã! Ta còn Frontend. Hãy tạo `k8s/frontend.yaml` chạy Nginx chứa code tĩnh.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
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
        # Cần mount code frontend vào đây hoặc build image frontend riêng.
        # Ở bài này ta giả sử build image frontend-nginx riêng.
        # Để đơn giản, ta dùng tạm image nginx gốc và chưa có mount code (sẽ trắng trang).
        # -> Giải pháp: Bạn nên Build Image cho Frontend ở Giai đoạn Dockerize.
        # (Ở đây ta tạm bỏ qua Frontend Deployment để tập trung vào API backend)
```
*Lưu ý: Để chạy trọn vẹn, bạn cần build image cho Frontend. Nhưng để test K8s Backend, ta tập trung vào API.*

---

## 🚀 PHẦN 2: TRIỂN KHAI (DEPLOY)

Trước khi deploy, hãy chắc chắn bạn đã sửa tên Image trong file YAML thành tên Docker Hub của bạn (nếu đã push lên Hub). Nếu chưa, bạn có thể build trực tiếp vào Minikube:
```bash
eval $(minikube docker-env)
# Rồi chạy lệnh docker build như bình thường -> Image sẽ chui thẳng vào Minikube
```

### Apply
```bash
kubectl apply -f k8s/
```
Lệnh này sẽ chạy tất cả file yaml trong thư mục.

### Kiểm tra
```bash
kubectl get pods
kubectl get services
```
Bạn sẽ thấy các Pods đang chuyển trạng thái từ `Pending` -> `ContainerCreating` -> `Running`.

---

## 🧪 PHẦN 3: CHAOS ENGINEERING (THỬ PHÁ HOẠI)

Đây là phần thú vị nhất của K8s.

1. Kiểm tra Backend có 2 Pods:
   ```bash
   kubectl get pods -l app=backend
   ```
   (Ví dụ: `backend-xyz-1` và `backend-xyz-2`)

2. **Xóa (Kill) một Pod:**
   ```bash
   kubectl delete pod backend-xyz-1
   ```

3. **Quan sát ngay lập tức:**
   ```bash
   kubectl get pods
   ```
   Bạn sẽ thấy Pod cũ biến mất (Terminating), nhưng **NGAY LẬP TỨC** một Pod mới (`backend-xyz-3`) được tạo ra để thay thế. K8s luôn đảm bảo `replicas: 2`.

---

## 📝 TỔNG KẾT
Bạn đã chạm tay vào công nghệ mạnh mẽ nhất của DevOps hiện đại.
- Không còn lo service chết (vì sẽ tự hồi sinh).
- Không còn lo cấu hình IP thủ công (vì có Service DNS).

👉 **Bước tiếp theo:** Chạy Local thì vui, nhưng chạy Production phải lên Cloud. Giai đoạn 10: **AWS EKS & Autoscaling**.
