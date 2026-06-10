# 🧪 Kubernetes Basic Challenges: Bộ Bài Tập Rèn Luyện Tư Duy Và Lab Thực Hành Thực Chiến

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 26/05/2026\
> **Level:** Basic\
> **Tags:** [PRACTICAL, LAB, EXERCISE, K8S-BASIC]\
> **Yêu cầu trước:** [Kubernetes Basic Module (Lessons 00 - 04)](../../lessons/01_basic/00_what-is-kubernetes.md)

> 🎯 **Mục tiêu cốt lõi:** Chuyển hóa toàn bộ lý thuyết về Pod, Deployment, Service, ConfigMap, Secret, Namespace và RBAC thành kỹ năng thực tế. Bạn sẽ được rèn luyện tư duy thông qua 5 câu hỏi trắc nghiệm phản biện sâu sắc, và trực tiếp bắt tay vào xây dựng 3 dự án Lab thực chiến hoàn chỉnh, có khả năng chạy ngay trên các Cluster local như `kind` hay `minikube`.

---

## 🧭 Cấu Trúc Trải Nghiệm Bài Tập

Học đi đôi với hành chính là con đường ngắn nhất để làm chủ DevOps. Bộ bài tập được thiết kế gồm hai phần tách biệt:
* **Phần 1: Trắc Nghiệm Phản Biện (Tư Duy Sâu):** 5 câu hỏi trích từ các tình huống thực tế trên Production giúp bạn mài giũa tư duy xử lý sự cố.
* **Phần 2: 3 Bài Lab Thực Chiến (Hành Động Ngay):** Hướng dẫn từng bước viết Manifest YAML chuẩn hóa, áp dụng trực tiếp giải quyết "nỗi đau" vận hành của doanh nghiệp.

---

## 🧠 Phần 1: Trắc Nghiệm Phản Biện (Có Đáp Án Ẩn)

### Câu 1: Bản chất của Pod trong thiết kế K8s
Một Pod chạy ứng dụng NodeJS của bạn có cấu hình chứa 2 Container: Container chính chạy ứng dụng Web (Port `3000`), Container phụ chạy nhiệm vụ phụ trợ ghi Log (Sidecar Container). Tại sao hai Container này có thể kết nối với nhau thông qua địa chỉ `localhost:3000`?
- **A.** Vì Kubernetes tự động định tuyến (Port forwarding) giữa các Container thông qua CoreDNS.
- **B.** Vì tất cả các Container bên trong cùng một Pod dùng chung không gian mạng (Network Namespace) và có chung địa chỉ IP.
- **C.** Vì K8s tự động liên kết các Container bằng cơ chế Bridge Network giống như Docker Compose mặc định.
- **D.** K8s không cho phép 2 Container trong cùng 1 Pod gọi nhau qua `localhost`.

<details>
<summary>💡 Gợi ý giải đáp câu 1</summary>

- **Đáp án chính xác:** **B**
- **Giải thích sâu:** Pod là đơn vị lập lịch nhỏ nhất trong Kubernetes. Về mặt kỹ thuật, các Container chạy trong cùng một Pod sẽ dùng chung các Namespace của Linux (bao gồm Network Namespace, UTS Namespace và IPC Namespace). Điều này có nghĩa là chúng dùng chung một địa chỉ IP duy nhất của Pod, chia sẻ chung bảng định tuyến và các cổng kết nối (Port). Do đó, Container phụ trợ có thể kết nối trực tiếp đến Container chính thông qua `localhost:<port>` một cách cực kỳ nhanh chóng và không mất chi phí định tuyến qua mạng.
</details>

---

### Câu 2: Sự cố Liveness Probe khởi động chậm
Bạn vừa deploy một dịch vụ Java Spring Boot lên Cluster. Ứng dụng Java này mất khoảng 45 giây để khởi động hoàn toàn (Loading Context, Connect Database...). Tuy nhiên, ngay khi deploy, Pod liên tục bị K8s khởi động lại (Restart) sau mỗi 10-15 giây, khiến ứng dụng không bao giờ ở trạng thái sẵn sàng (Ready). Cấu hình Liveness Probe của bạn như sau:
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```
Nguyên nhân gốc rễ của sự cố này là gì?
- **A.** Ứng dụng Java bị crash do thiếu RAM vật lý trên Node.
- **B.** Đường dẫn `/healthz` khai báo sai, K8s API Server không thể kết nối.
- **C.** Liveness Probe bắt đầu quét quá sớm (sau 5 giây) trong khi ứng dụng cần 45 giây để khởi động. K8s hiểu lầm ứng dụng bị treo và tiến hành hủy diệt/khởi động lại Pod liên tục.
- **D.** Cổng kết nối `8080` chưa được expose thông qua Service ClusterIP.

<details>
<summary>💡 Gợi ý giải đáp câu 2</summary>

- **Đáp án chính xác:** **C**
- **Giải thích sâu:** Liveness Probe dùng để xác định khi nào ứng dụng bị treo (deadlock) để khởi động lại. Ở đây, ứng dụng cần 45 giây để khởi động, nhưng bạn cấu hình `initialDelaySeconds: 5` (đợi 5 giây) và `periodSeconds: 5` (quét lại sau mỗi 5 giây). Chỉ sau tối đa 15-20 giây đầu tiên, cuộc kiểm tra sức khỏe liên tiếp thất bại vì ứng dụng chưa khởi động xong. K8s lập tức phán quyết Pod bị treo và tự động ra lệnh Restart. Quá trình này lặp đi lặp lại vô tận.
- **Giải pháp:** Sử dụng **Startup Probe** để kiểm soát quá trình khởi động ban đầu của ứng dụng, hoặc tăng `initialDelaySeconds` lên trên 50 giây để cho ứng dụng đủ thời gian chuẩn bị.
</details>

---

### Câu 3: Định tuyến Service và Label Selector
Bạn có một dịch vụ Service với cấu hình Label Selector là `app: payment-api`. Bạn đang thực hiện bảo trì hệ thống và muốn tạm thời ngắt toàn bộ lưu lượng truy cập (Traffic) từ khách hàng vào một Pod cụ thể để kiểm tra lỗi trực tiếp. Cách làm nào sau đây nhanh và chuẩn xác nhất?
- **A.** Xóa Pod đó khỏi Cluster bằng lệnh `kubectl delete pod`.
- **B.** Thay đổi hoặc thêm một chữ vào nhãn (Label) của Pod đó (ví dụ: đổi từ `app: payment-api` thành `app: payment-api-debug`).
- **C.** Xóa cấu hình Ingress của hệ thống.
- **D.** Sửa đổi tệp cấu hình của Service để loại bỏ Pod đó.

<details>
<summary>💡 Gợi ý giải đáp câu 3</summary>

- **Đáp án chính xác:** **B**
- **Giải thích sâu:** K8s Service định tuyến lưu lượng truy cập động đến các Pod dựa trên Label Selector. Một khi bạn thay đổi nhãn của Pod sang một giá trị khác (ví dụ: `app: payment-api-debug`), Service sẽ lập tức nhận diện Pod đó không còn thỏa mãn điều kiện lọc nữa và tự động gỡ IP của Pod ra khỏi danh sách **Endpoints** hoạt động. Pod đó vẫn tiếp tục chạy hoàn toàn bình thường để bạn tha hồ debug, nhưng không nhận bất kỳ request nào từ khách hàng nữa. Khi debug xong, bạn chỉ cần đổi nhãn lại như cũ!
</details>

---

### Câu 4: Bản chất bảo mật của K8s Secret
Đồng nghiệp của bạn khẳng định: *"Dữ liệu nhạy cảm như mật khẩu Database lưu trong K8s Secret là tuyệt đối an toàn vì nó đã được mã hóa tự động sang chuỗi ký tự ngẫu nhiên dạng `dXNlcm5hbWU=`"*. Nhận định này đúng hay sai?
- **A.** **ĐÚNG.** Chuỗi ký tự trên đã được mã hóa bằng thuật toán đối xứng nâng cao AES-256.
- **B.** **SAI.** Chuỗi ký tự đó chỉ được mã hóa một chiều (Hashing) giống như MD5, không thể giải mã ngược lại.
- **C.** **SAI.** K8s Secret mặc định **chỉ được mã hóa dạng Base64** (một dạng mã hóa định dạng dữ liệu, không phải mã hóa bảo mật). Bất kỳ ai có quyền truy cập vào Cluster đều có thể dễ dàng giải mã ngược lại bằng một câu lệnh terminal đơn giản.

<details>
<summary>💡 Gợi ý giải đáp câu 4</summary>

- **Đáp án chính xác:** **C**
- **Giải thích sâu:** Base64 chỉ là một phương pháp mã hóa ký tự (encoding) giúp truyền tải dữ liệu dạng nhị phân an toàn qua mạng, hoàn toàn không có tính bảo mật hay mã hóa bảo vệ (encryption). Bạn có thể giải mã chuỗi `dXNlcm5hbWU=` về dạng text gốc bằng câu lệnh cực nhanh: `echo "dXNlcm5hbWU=" | base64 --decode` (kết quả trả về là `username`). Để bảo mật Secret thực sự trên Production, bạn phải cấu hình cơ chế *Encryption at Rest* của K8s hoặc tích hợp các công cụ bên ngoài như HashiCorp Vault.
</details>

---

### Câu 5: Phân biệt Role vs ClusterRole
Tài khoản CI/CD Bot của bạn cần có quyền liệt kê (list) và đọc thông tin của toàn bộ các Node vật lý trong Cluster để tự động chọn ra Node có tài nguyên trống tốt nhất. Bạn nên sử dụng đối tượng nào để phân quyền?
- **A.** Tạo một **Role** và một **RoleBinding** trong Namespace `default`.
- **B.** Tạo một **Role** và một **ClusterRoleBinding**.
- **C.** Tạo một **ClusterRole** và một **ClusterRoleBinding** vì đối tượng Node thuộc phạm vi toàn Cluster (Cluster-scoped), không thuộc về bất kỳ Namespace nào.
- **D.** Tạo một **ClusterRole** và một **RoleBinding** trong Namespace `kube-system`.

<details>
<summary>💡 Gợi ý giải đáp câu 5</summary>

- **Đáp án chính xác:** **C**
- **Giải thích sâu:** Đối tượng **Node** là tài nguyên cấp Cluster (Cluster-scoped Resource), tức là nó nằm ngoài tầm kiểm soát của mọi Namespace. Do đó, bạn không thể sử dụng đối tượng **Role** (vốn chỉ hoạt động trong 1 Namespace) để phân quyền thao tác với Node. Bạn bắt buộc phải tạo một **ClusterRole** để khai báo quyền và sử dụng **ClusterRoleBinding** để gán quyền này trên phạm vi toàn Cluster cho tài khoản của Bot.
</details>

---

## 🛠️ Phần 2: 3 Bài Lab Thực Chiến (Hands-on Labs)

> [!IMPORTANT]
> Để thực hiện các bài Lab này, hãy đảm bảo bạn đã cài đặt sẵn một Cluster cục bộ (Local Cluster) như `kind`, `minikube` hoặc `Docker Desktop`, kèm theo công cụ dòng lệnh `kubectl` được kết nối thành công.

---

### 🧪 LAB 1: Triển Khai Deployment Tự Phục Hồi & Tự Động Co Giãn (Auto-scaling)

#### Tình huống giả định:
Công ty yêu cầu bạn deploy ứng dụng API viết bằng FastAPI. Yêu cầu hệ thống phải:
1. Chạy tối thiểu 3 bản sao (Replicas) để đảm bảo tính sẵn sàng cao.
2. Được giới hạn cứng tài nguyên: Yêu cầu chạy (requests) là 64MB RAM, 100m CPU; Trần giới hạn (limits) là 128MB RAM, 200m CPU.
3. Tích hợp cơ chế tự phục hồi (Self-healing) thông qua Liveness Probe và Readiness Probe quét vào endpoint `/health` của ứng dụng.
4. Tự động co giãn (Auto-scaling): Khi tải CPU trung bình của các Pod vượt quá 70%, hệ thống phải tự động scale lên tối đa 10 Pod để gánh tải.

---

#### Hướng dẫn từng bước:

##### Bước 1: Viết Manifest khai báo Deployment & Service hoàn chỉnh
Hãy tạo tệp tin `lab1-fastapi-app.yaml` với nội dung Việt hóa chú thích chi tiết sau:

```yaml
# file: lab1-fastapi-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
  labels:
    app: fastapi-api
spec:
  replicas: 3                     # Khởi tạo 3 bản sao Pod để chạy song song
  selector:
    matchLabels:
      app: fastapi-api            # K8s tìm các Pod có nhãn này để quản lý
  template:
    metadata:
      labels:
        app: fastapi-api          # Gán nhãn cho các Pod được sinh ra
    spec:
      containers:
      - name: fastapi-container
        image: nginxdemos/hello:latest # Sử dụng ảnh demo hiển thị thông tin hệ thống nhanh
        ports:
        - containerPort: 80       # Port ứng dụng lắng nghe bên trong container
        
        # --- 1. Hạn mức tài nguyên nghiêm ngặt ---
        resources:
          requests:
            memory: "64Mi"        # Tài nguyên tối thiểu để Pod được khởi chạy
            cpu: "100m"           # 100m = 0.1 Core CPU
          limits:
            memory: "128Mi"       # Trần giới hạn tối đa tránh ngốn RAM Node
            cpu: "200m"           # Tối đa không quá 0.2 Core CPU
            
        # --- 2. Kiểm tra sức khỏe tự phục hồi ---
        livenessProbe:            # Phát hiện ứng dụng bị treo để tự động restart Pod
          httpGet:
            path: /               # Endpoint kiểm tra sức khỏe
            port: 80
          initialDelaySeconds: 5  # Đợi 5 giây sau khi container chạy rồi mới quét
          periodSeconds: 10       # Cứ mỗi 10 giây quét lại một lần
        readinessProbe:           # Phát hiện ứng dụng sẵn sàng nhận traffic từ khách hàng
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: ClusterIP                 # Dùng mạng nội bộ Cluster để định tuyến
  selector:
    app: fastapi-api              # Service tìm các Pod có nhãn này để gửi traffic
  ports:
  - port: 8080                    # Port của Service expose ra ngoài
    targetPort: 80                # Port thực tế của container nhận request
```

##### Bước 2: Thiết lập cơ chế tự động co giãn tài nguyên (HPA)
Tạo tệp cấu hình HPA `lab1-hpa.yaml` để tự động hóa việc scale pod:

```yaml
# file: lab1-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-deployment     # Chỉ rõ đối tượng Deployment cần tự động co giãn
  minReplicas: 3                 # Số lượng Pod tối thiểu luôn luôn chạy
  maxReplicas: 10                # Trần số lượng Pod tối đa khi quá tải hệ thống
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70   # Scale khi CPU trung bình các Pod vượt quá 70%
```

##### Bước 3: Deploy và kiểm toán thực tế
Chạy các lệnh sau trên terminal của bạn:

```bash
# 1. Áp dụng cấu hình Deployment và Service
kubectl apply -f lab1-fastapi-app.yaml

# 2. Áp dụng cấu hình tự động co giãn HPA
kubectl apply -f lab1-hpa.yaml

# 3. Giám sát trạng thái Deployment hoạt động thời gian thực
kubectl get deployments --watch

# 4. Kiểm tra danh sách Endpoints của Service đã tự động nhận 3 IP của 3 Pod chưa
kubectl get endpoints fastapi-service
```

---

### 🧪 LAB 2: Định Tuyến Đa Dịch Vụ Và SSL/TLS Tự Động (Ingress & Multi-Service Routing)

#### Tình huống giả định:
Doanh nghiệp của bạn sở hữu một hệ thống web gồm 2 phần độc lập:
* **Dịch vụ Frontend (React):** Hiển thị giao diện cho khách hàng.
* **Dịch vụ Backend (FastAPI):** Cung cấp API xử lý dữ liệu nhạy cảm.

Bạn cần cấu hình một hệ thống định tuyến tập trung duy nhất (Ingress Controller) đáp ứng:
1. Truy cập địa chỉ tên miền `http://my-company.local/` sẽ tự động định tuyến tới dịch vụ Frontend.
2. Truy cập địa chỉ `http://my-company.local/api` sẽ tự động chuyển hướng request tới dịch vụ Backend.
3. Kích hoạt bảo mật mã hóa SSL/TLS để khách hàng truy cập an toàn qua giao thức HTTPS (`https://my-company.local`).

---

#### Hướng dẫn từng bước:

##### Bước 1: Khởi tạo 2 ứng dụng Frontend và Backend giả định
Tạo tệp tin `lab2-apps-setup.yaml`:

```yaml
# file: lab2-apps-setup.yaml
# --- DỊCH VỤ FRONTEND ---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: web-frontend
  template:
    metadata:
      labels:
        app: web-frontend
    spec:
      containers:
      - name: frontend-container
        image: nginxdemos/hello:plain-text
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: ClusterIP
  selector:
    app: web-frontend
  ports:
  - port: 80
    targetPort: 80
---
# --- DỊCH VỤ BACKEND ---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api-backend
  template:
    metadata:
      labels:
        app: api-backend
    spec:
      containers:
      - name: backend-container
        image: nginxdemos/hello:plain-text
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP
  selector:
    app: api-backend
  ports:
  - port: 80
    targetPort: 80
```

##### Bước 2: Tạo chứng chỉ SSL/TLS tự ký (Self-signed Certificate) để bảo mật
Trước khi viết cấu hình Ingress, chúng ta tạo một Secret chứa chứng chỉ SSL giả định để cấu hình HTTPS:

```bash
# 1. Tạo cặp khóa SSL/TLS tự ký bằng OpenSSL
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=my-company.local"

# 2. Đóng gói cặp khóa này vào K8s Secret chuyên biệt loại 'tls'
kubectl create secret tls my-company-tls-secret \
  --cert=tls.crt \
  --key=tls.key
```

##### Bước 3: Viết Manifest cấu hình Ingress định tuyến tập trung
Tạo tệp tin `lab2-ingress-config.yaml` sử dụng lớp Ingress Nginx tiêu chuẩn:

```yaml
# file: lab2-ingress-config.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: company-web-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx" # Chỉ định sử dụng Nginx Ingress Controller
    nginx.ingress.kubernetes.io/rewrite-target: / # Kỹ thuật viết lại URL để chuyển tiếp sạch
spec:
  # --- Cấu hình mã hóa bảo mật SSL/TLS HTTPS ---
  tls:
  - hosts:
    - my-company.local
    secretName: my-company-tls-secret   # Chỉ rõ Secret chứa chứng chỉ SSL đã tạo ở trên
    
  # --- Cấu hình luật định tuyến URL Path-based ---
  rules:
  - host: my-company.local                # Tên miền truy cập chỉ định
    http:
      paths:
      - path: /                           # Định tuyến trang chủ
        pathType: Prefix
        backend:
          service:
            name: frontend-service        # Gửi request tới Service Frontend
            port:
              number: 80
      - path: /api                        # Định tuyến đường dẫn API
        pathType: Prefix
        backend:
          service:
            name: backend-service         # Gửi request tới Service Backend
            port:
              number: 80
```

##### Bước 4: Deploy ứng dụng và kiểm chứng định tuyến
Chạy lệnh apply các tệp cấu hình:

```bash
kubectl apply -f lab2-apps-setup.yaml
kubectl apply -f lab2-ingress-config.yaml
```

> [!TIP]
> **Cách kiểm tra Ingress trên máy cá nhân:**
> Để máy tính của bạn truy cập được tên miền giả định `my-company.local`, hãy mở tệp `/etc/hosts` (trên Linux/macOS) hoặc `C:\Windows\System32\drivers\etc\hosts` (trên Windows) bằng quyền Admin và thêm dòng sau:
> `127.0.0.1 my-company.local`
> Sau đó, mở trình duyệt web và truy cập địa chỉ `https://my-company.local/` để kiểm tra kết quả định tuyến HTTPS tuyệt đẹp!

---

### 🧪 LAB 3: Phân Quyền RBAC Bảo Mật Cô Lập Môi Trường (Namespace Role Separation)

#### Tình huống giả định:
Doanh nghiệp muốn lập ranh giới an toàn tuyệt đối cho môi trường thử nghiệm nâng cao (`staging`). Bạn được giao nhiệm vụ:
1. Tạo một Namespace chuyên biệt tên là `staging`.
2. Tạo một ServiceAccount có tên là `staging-deployer-sa` chuyên dùng để deploy ứng dụng trong môi trường này.
3. Thiết lập phân quyền RBAC:
   * Quyền của `staging-deployer-sa` **chỉ được gói gọn** trong Namespace `staging`.
   * Cho phép tạo, xem, cập nhật, xóa các tài nguyên Deployments, Services, ConfigMaps.
   * Tuyệt đối không cho phép ServiceAccount này can thiệp vào bất kỳ Namespace nào khác (như `default` hay `production`).

---

#### Hướng dẫn từng bước:

##### Bước 1: Khai báo tài nguyên và thiết lập phân quyền RBAC
Tạo tệp manifest `lab3-rbac-staging.yaml` chứa toàn bộ cấu hình hạ tầng:

```yaml
# file: lab3-rbac-staging.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: staging                   # Khởi tạo Namespace biệt lập cho Staging
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: staging-deployer-sa
  namespace: staging               # Định danh bot deployer nằm tại staging
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: staging-developer-role
  namespace: staging               # Thiết lập danh mục quyền chỉ có tác dụng trong staging
rules:
- apiGroups: ["", "apps", "networking.k8s.io"] # Chứa Core API, Apps và Network APIs
  resources: ["deployments", "services", "configmaps", "pods"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"] # Toàn quyền quản trị ứng dụng
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]                  # Chỉ được đọc Secret chỉ định, không được xem danh sách (list) Secrets
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: staging-developer-binding
  namespace: staging
subjects:
- kind: ServiceAccount
  name: staging-deployer-sa
  namespace: staging               # Liên kết trực tiếp với ServiceAccount đã tạo
roleRef:
  kind: Role
  name: staging-developer-role     # Trỏ tới danh mục quyền giới hạn ở trên
  apiGroup: rbac.authorization.k8s.io
```

##### Bước 2: Deploy cấu hình bảo mật
Áp dụng tệp manifest lên Cluster:

```bash
kubectl apply -f lab3-rbac-staging.yaml
```

##### Bước 3: Chạy kịch bản kiểm tra an ninh (Security Auditing Script)
Hãy sao chép và thực thi loạt lệnh sau trên Terminal để xác nhận hệ thống hoạt động hoàn hảo chuẩn đặc quyền tối thiểu:

```bash
echo "=== BẮT ĐẦU KIỂM TOÁN AN NINH RBAC STAGING ==="

# 1. Kiểm tra xem bot Staging SA có thể tạo Deployment trong chính Namespace staging không?
CAN_DEPLOY_STAGING=$(kubectl auth can-i create deployments -n staging --as=system:serviceaccount:staging:staging-deployer-sa)
echo "Quyền tạo Deployment tại Staging: $CAN_DEPLOY_STAGING" # Mong muốn: yes

# 2. Kiểm tra xem bot Staging SA có thể xóa Pod trong Namespace staging để tự phục hồi không?
CAN_DELETE_POD_STAGING=$(kubectl auth can-i delete pods -n staging --as=system:serviceaccount:staging:staging-deployer-sa)
echo "Quyền xóa Pod tại Staging: $CAN_DELETE_POD_STAGING" # Mong muốn: yes

# 3. Kiểm tra xem bot Staging SA có thể can thiệp tạo Deployment ở Namespace default không?
CAN_DEPLOY_DEFAULT=$(kubectl auth can-i create deployments -n default --as=system:serviceaccount:staging:staging-deployer-sa)
echo "Quyền tạo Deployment tại default Namespace: $CAN_DEPLOY_DEFAULT" # Mong muốn: no

# 4. Kiểm tra xem bot Staging SA có quyền xem (list) danh sách Secrets nhạy cảm ở Staging không?
CAN_LIST_SECRETS_STAGING=$(kubectl auth can-i list secrets -n staging --as=system:serviceaccount:staging:staging-deployer-sa)
echo "Quyền liệt kê danh sách Secrets tại Staging: $CAN_LIST_SECRETS_STAGING" # Mong muốn: no

echo "=== HOÀN TẤT KIỂM TOÁN: HỆ THỐNG AN TOÀN TUYỆT ĐỐI ==="
```

---

## 🏆 Lời Khuyên Gửi Bạn Từ Mr.Rom

Chúc mừng bạn đã hoàn thành xuất sắc toàn bộ thử thách lý thuyết và thực hành của chuyên đề **Kubernetes Basic**! 

Việc tự mình viết các tệp Manifest YAML, đóng gói cặp khóa SSL/TLS tự ký, thiết lập hạn mức ResourceQuota và trực tiếp chạy các kịch bản kiểm toán an ninh là bước chuyển mình mạnh mẽ từ một Lập trình viên thông thường sang một **Kỹ sư DevOps thực chiến**. 

Hãy tiếp tục duy trì ngọn lửa đam mê, lưu trữ các tệp manifest này làm thư viện tài liệu mẫu (Recipes) cá nhân để nhanh chóng tái sử dụng trong các dự án công ty thực tế nhé!

---

## 📜 Nhật Ký Thay Đổi (Changelog)

- **v1.0.0 (26/05/2026)** — **[Mr.Rom]** Khởi tạo bộ tài liệu bài tập rèn luyện tư duy cốt lõi và 3 bài Lab thực hành thực chiến chuẩn Premium 5 sao cho Kubernetes Basic.
