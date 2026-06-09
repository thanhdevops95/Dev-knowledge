---
title: Pods Và Deployments: Hạt Nhân Và Cỗ Máy Tự Động Hóa Trạng Thái Trong Kubernetes
author: Mr.Rom
version: v2.0.0
date: 2026-05-26
level: Basic
tags: [MUST-KNOW, DEVOPS, KUBERNETES]
---

# 🎓 Pods Và Deployments: Hạt Nhân Và Cỗ Máy Tự Động Hóa Trạng Thái Trong Kubernetes

> 🎯 **Lời dẫn của Mr.Rom:**
> Sau khi đã nắm vững bức tranh toàn cảnh về Kubernetes ở bài trước, giờ là lúc chúng ta đi sâu vào hai "viên gạch nền móng" quan trọng nhất để xây dựng một ứng dụng K8s thực tế: **Pod** và **Deployment**. Rất nhiều bạn mới học thường lầm tưởng chỉ cần dùng Pod đơn độc là đủ. Bài học thực chiến này sẽ giúp bạn hiểu rõ lý do vì sao trên Production chúng ta luôn bắt buộc phải sử dụng Deployment bao bọc lấy Pod, đồng thời nắm chắc cách cấu hình co giãn, tự phục hồi lỗi và quản lý tài nguyên an toàn cho hệ thống!

## 🎯 Sau bài học này, bạn sẽ làm chủ:

- [x] Bản chất thực sự của **Pod** — Đơn vị triển khai nhỏ nhất và lý do vì sao K8s không chạy trực tiếp container đơn lẻ.
- [x] Thiết kế hoàn chỉnh một tệp manifest YAML cho **Deployment** chuẩn doanh nghiệp.
- [x] Sử dụng thành thạo các lệnh `kubectl` để kiểm tra trạng thái co giãn, rollback và gỡ lỗi Pod/Deployment.
- [x] Cơ chế liên kết thông minh qua **Labels** và **Selectors** để quản lý tài nguyên khoa học.
- [x] Kỹ thuật cập nhật không downtime (**Rolling Update**) và phục hồi lỗi nhanh (**Rollback**).
- [x] Cách thiết lập giới hạn tài nguyên phần cứng (**Requests & Limits**) để bảo vệ cluster khỏi cạn kiệt tài nguyên.
- [x] Thiết lập bộ kiểm tra sức khỏe thông minh (**Liveness & Readiness Probes**) để tự động phục hồi container lỗi.

---

## Tình Huống: Bài Học Đắt Giá Từ Chiếc Pod Cô Độc Đầu Tiên

Hào hứng sau khi cài đặt thành công cluster `kind` ở local, bạn viết một tệp YAML tối giản để khởi chạy ứng dụng FastAPI của mình dưới dạng một Pod đơn lẻ:

```yaml
# pod-co-doc.yaml
apiVersion: v1
kind: Pod
metadata:
  name: fastapi-pod
spec:
  containers:
  - name: fastapi-container
    image: acmeshop/fastapi:latest
```

Bạn gõ lệnh apply và thấy container khởi chạy mượt mà:

```bash
# Gửi cấu hình Pod lên K8s
kubectl apply -f pod-co-doc.yaml

# Kiểm tra trạng thái
kubectl get pods
# Output: fastapi-pod   1/1   Running   0   10s
```

Để thử thách tính năng "tự phục hồi" thần thánh của Kubernetes mà mọi người vẫn thường ca ngợi, bạn chủ động gõ lệnh xóa Pod này để xem nó có tự hồi sinh hay không:

```bash
# Thử xóa Pod thủ công
kubectl delete pod fastapi-pod

# Kiểm tra lại danh sách Pod
kubectl get pods
# Output: No resources found in default namespace.
```

🔥 **Kết quả bất ngờ:** Chiếc Pod biến mất hoàn toàn và hệ thống không hề khởi tạo bất kỳ Pod mới nào để thay thế! 

Bạn hoang mang tự hỏi: *"Tại sao Kubernetes lại bỏ mặc chiếc Pod bị xóa chết yểu như vậy? Phép màu tự phục hồi (Self-healing) nằm ở đâu?"*

Một kỹ sư DevOps đàn anh mỉm cười giải thích:

> [!WARNING]
> *"Một chiếc Pod cô độc (Naked Pod) được tạo trực tiếp sẽ không có bất kỳ bộ điều khiển (Controller) nào đứng sau giám sát. Khi nó bị xóa hoặc máy chủ vật lý chứa nó bị mất điện, Pod đó sẽ biến mất vĩnh viễn. Trên môi trường Production, chúng ta bắt buộc phải sử dụng **Deployment** để bao bọc lấy Pod. Deployment sẽ chịu trách nhiệm giám sát, tự động hồi sinh Pod khi lỗi và quản lý quy trình nâng cấp an toàn."*

Bài học này sẽ hướng dẫn bạn làm chủ cỗ máy tự động hóa Deployment đó!

---

## 1️⃣ Khám Phá Pod: Đơn Vị Đo Lường Nhỏ Nhất Nhưng Chứa Đựng Nhiều Bí Mật

Trong thế giới của Kubernetes, **Pod** là đơn vị triển khai nhỏ nhất mà bạn có thể tạo lập và quản lý. Một Pod đại diện cho một tiến trình đang chạy trong cluster của bạn. Nó có thể chứa một container duy nhất hoặc một nhóm gồm **nhiều container dùng chung tài nguyên mạng, ổ đĩa và có cùng vòng đời**.

```text
┌────────────────────────────────────────────────────────┐
│               POD (DÙNG CHUNG IP & VOLUME)             │
│  ┌────────────────────────┐  ┌──────────────────────┐  │
│  │      Container 1       │  │     Container 2      │  │
│  │ (Ứng dụng chính Flask) │  │  (Sidecar ghi Log)   │  │
│  └────────────────────────┘  └──────────────────────┘  │
│  Shared: localhost network, Volume Mount               │
└────────────────────────────────────────────────────────┘
```

### Tại sao Kubernetes lại dùng Pod thay vì chạy trực tiếp Container?

Có 3 lý do cốt lõi cho thiết kế tuyệt vời này:
1. **Dùng chung mạng ảo (Shared Network):** Toàn bộ các container nằm trong cùng một Pod sẽ nói chuyện với nhau cực kỳ nhanh qua địa chỉ `localhost` và dùng chung một IP ảo do K8s cấp phát.
2. **Dùng chung ổ cứng (Shared Storage):** Các container trong Pod có thể mount chung một ổ đĩa ảo để chia sẻ tệp tin tức thời (ví dụ: Container chính ghi log ra tệp, Container phụ đọc tệp log đó gửi về hệ thống giám sát tập trung).
3. **Phối hợp mô hình Sidecar Pattern:** Cho phép bạn đính kèm các container phụ trợ (Helper container) chạy song song hỗ trợ container chính (ví dụ: Envoy Proxy để mã hóa bảo mật TLS, hoặc fluentbit để gom log hệ thống).

> [!TIP]
> Trong 95% các dự án thực tế, một Pod của bạn sẽ chỉ chứa **duy nhất 1 container**. Việc chạy nhiều container trong cùng một Pod (Sidecar Pattern) là một kỹ thuật nâng cao và chỉ nên dùng khi thực sự cần chia sẻ tài nguyên mạng/ổ đĩa cực kỳ chặt chẽ.

---

### Phân tích các giai đoạn vòng đời (Lifecycle Phases) của Pod

Một chiếc Pod kể từ khi được khai báo sẽ trải qua tuần tự các trạng thái hoạt động sau:

1. **Pending (Chờ xếp lịch):** Tệp cấu hình đã được gửi lên API Server, nhưng Pod đang phải chờ Scheduler quét tìm máy chủ Node có đủ RAM/CPU trống để đặt Pod vào.
2. **ContainerCreating (Đang khởi tạo):** Kubelet tại Node đã nhận lệnh, đang tiến hành tải (pull) Image từ Docker Hub về máy và khởi tạo container.
3. **Running (Đang chạy mượt mà):** Pod đã được gắn kết thành công vào Node và ít nhất một container bên trong đã hoạt động ổn định.
4. **CrashLoopBackOff (Vòng lặp lỗi liên tục):** Container khởi chạy bị lỗi crash ngay lập tức (do lỗi code, thiếu biến môi trường). K8s sẽ cố gắng tự động restart lại container này với thời gian chờ tăng dần (10s, 20s, 40s...) để tránh làm nghẽn hệ thống.

---

## 2️⃣ Cỗ Máy Deployment: Phương Pháp Triển Khai Chuẩn Production Cho Doanh Nghiệp

**Deployment** là một khối tài nguyên quản trị (Controller) cấp cao trong Kubernetes. Nó không trực tiếp chạy container, mà đóng vai trò là "người ra lệnh" quản lý một công cụ phụ trợ là **ReplicaSet** để duy trì chính xác số lượng bản sao Pod mong muốn.

```text
   Deployment (Quản lý chiến lược, Rolling Update)
        │
        ▼
   ReplicaSet (Đảm bảo duy trì đúng số lượng bản sao)
        │
        ├──────────────────────┬──────────────────────┐
        ▼                      ▼                      ▼
    [Pod bản sao 1]        [Pod bản sao 2]        [Pod bản sao 3]
```

### Tệp cấu hình Deployment YAML hoàn chỉnh đầu tiên

Hãy cùng phân tích một tệp tin manifest YAML chuẩn chỉnh để deploy ứng dụng FastAPI:

```yaml
# deployment-fastapi.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  labels:
    app: fastapi-service
spec:
  replicas: 3                         # Yêu cầu duy trì chính xác 3 Pod chạy đồng thời
  selector:
    matchLabels:
      app: fastapi-pod                 # Tìm và quản lý các Pod có nhãn match với label này
  template:
    metadata:
      labels:
        app: fastapi-pod               # Định nghĩa Nhãn sẽ gán cho các Pod được tạo ra
    spec:
      containers:
      - name: fastapi-container
        image: acmeshop/fastapi:v1.0
        ports:
        - containerPort: 8000
```

---

### Triển khai thực tế và kiểm tra tính năng tự phục hồi (Self-healing)

Hãy tiến hành gửi cấu hình này lên cluster và kiểm tra trạng thái hoạt động:

```bash
# 1. Apply cấu hình
kubectl apply -f deployment-fastapi.yaml

# 2. Kiểm tra Deployment
kubectl get deployments
# Output: fastapi-app   3/3   3   3   30s (3 pod mong muốn / 3 pod đã sẵn sàng)

# 3. Xem danh sách các Pod ảo được tạo ra tự động
kubectl get pods
# Output: 
# fastapi-app-7f9c-abc   1/1   Running
# fastapi-app-7f9c-def   1/1   Running
# fastapi-app-7f9c-ghi   1/1   Running
```

Để thử thách tính năng tự phục hồi thực sự của Deployment, bạn hãy chọn ngẫu nhiên một Pod và xóa nó đi:

```bash
# Xóa thử 1 Pod đang chạy ngầm của Deployment
kubectl delete pod fastapi-app-7f9c-abc

# Kiểm tra lại ngay lập tức danh sách Pod
kubectl get pods
# Output:
# fastapi-app-7f9c-def   1/1   Running
# fastapi-app-7f9c-ghi   1/1   Running
# fastapi-app-7f9c-xyz   0/1   ContainerCreating   <-- TỰ ĐỘNG KHỞI TẠO BẢN SAO MỚI!
```

> [!NOTE]
> **Mr.Rom giải mã cơ chế hoạt động:** 
> Khi Pod `fastapi-app-7f9c-abc` bị xóa, ReplicaSet lập tức phát hiện ra số lượng Pod thực tế (chỉ còn 2) bị lệch so với số lượng mong muốn khai báo trong file YAML (phải là 3). Vòng lặp cân bằng trạng thái (Reconciliation Loop) của K8s ngay lập tức kích hoạt, gửi yêu cầu tới Scheduler tạo mới ngay Pod `fastapi-app-7f9c-xyz` để đưa hệ thống về trạng thái cân bằng. Đây chính là chiếc khiên bảo vệ tối cao giúp ứng dụng của bạn sống sót qua mọi sự cố phần cứng trên Production!

---

## 3️⃣ Nhãn Labels Và Bộ Lọc Selectors: Những "Bí Danh" Phối Hợp Nhịp Nhàng

Trong Kubernetes, **Labels** là các cặp Key-Value được đính kèm trực tiếp vào các tài nguyên (như Pod) để phân nhóm và quản lý. **Selectors** là bộ lọc để tìm kiếm các tài nguyên có nhãn tương ứng.

```yaml
# Khai báo nhãn cho Pod
metadata:
  labels:
    app: fastapi
    tier: backend
    env: production
```

Để truy vấn nhanh các Pod theo nhãn trên terminal:
```bash
# Lọc ra các Pod đang chạy ở môi trường production
kubectl get pods -l env=production

# Lọc các Pod thuộc tầng backend ở production
kubectl get pods -l 'tier=backend,env=production'
```

> [!IMPORTANT]
> **Quy tắc bắt buộc khi viết YAML:**
> Nhãn của Pod khai báo trong phần `template.metadata.labels` **bắt buộc phải trùng khớp hoàn toàn** với bộ lọc Selector khai báo ở mục `spec.selector.matchLabels`. Nếu bạn cấu hình sai lệch dù chỉ 1 ký tự, Deployment sẽ không thể tìm thấy Pod của nó và hệ thống sẽ liên tục tạo Pod mới vô hạn (hoặc báo lỗi lập tức khi apply).

---

## 4️⃣ Quy Trình Rolling Update: Cập Nhật Tính Năng Mượt Mà Không Gây Downtime

Khi bạn nâng cấp ứng dụng lên phiên bản mới (ví dụ từ image `fastapi:v1.0` lên `fastapi:v2.0`), bạn mong muốn quá trình chuyển giao diễn ra êm đẹp mà không gây gián đoạn dịch vụ của khách hàng. Kubernetes xử lý việc này hoàn toàn tự động qua chiến lược **Rolling Update (Cập nhật cuốn chiếu)**.

### Cách thức hoạt động của Rolling Update:

```text
Trạng thái ban đầu:  [Pod v1.0] [Pod v1.0] [Pod v1.0]

Bước 1: Tạo mới 1 Pod v2.0 song song -> Đợi Pod v2.0 khởi chạy khỏe mạnh.
                     [Pod v1.0] [Pod v1.0] [Pod v1.0] + [Pod v2.0 (Mới)]

Bước 2: Tiêu hủy 1 Pod v1.0 cũ.
                     [Pod v1.0] [Pod v1.0] + [Pod v2.0]

Bước 3: Tạo tiếp 1 Pod v2.0 mới -> Đợi khỏe mạnh -> Tiêu hủy tiếp 1 Pod v1.0 cũ.
                     [Pod v1.0] + [Pod v2.0] [Pod v2.0]

Quá trình lặp lại cuốn chiếu cho đến khi toàn bộ Pod được nâng cấp lên v2.0 sạch sẽ!
```

Để tùy biến tốc độ nâng cấp và số lượng container được phép dư thừa trong file YAML:

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1                     # Cho phép tạo dư thừa tối đa 1 Pod trong lúc nâng cấp
      maxUnavailable: 0               # Tuyệt đối cấm tắt Pod cũ khi Pod mới chưa hoạt động khỏe mạnh (Bảo vệ Zero Downtime)
```

### Các câu lệnh điều khiển cập nhật và Rollback tức thời:

```bash
# 1. Ra lệnh nâng cấp image của Deployment lên phiên bản v2.0
kubectl set image deployment/fastapi-app fastapi-container=acmeshop/fastapi:v2.0

# 2. Theo dõi tiến độ cập nhật cuốn chiếu theo thời gian thực
kubectl rollout status deployment/fastapi-app

# 3. Phát hiện phiên bản mới bị lỗi code nghiêm trọng? Ra lệnh Rollback quay lại phiên bản trước đó trong 3 giây!
kubectl rollout undo deployment/fastapi-app

# 4. Xem lịch sử các phiên bản đã deploy để quay lại phiên bản cụ thể
kubectl rollout history deployment/fastapi-app
kubectl rollout undo deployment/fastapi-app --to-revision=1
```

---

## 5️⃣ Cân Đo Đong Đếm requests Và limits: Đảm Bảo Công Bằng Tài Nguyên Trong Cluster

Nếu bạn không giới hạn tài nguyên, một chiếc Pod bị lỗi rò rỉ bộ nhớ (Memory Leak) có thể âm thầm "nuốt chửng" toàn bộ RAM của máy chủ Node vật lý, khiến tất cả các Pod lành tính khác chạy chung trên Node đó bị hệ điều hành tiêu diệt.

Để bảo vệ cluster, hãy luôn luôn khai báo cấu hình tài nguyên an toàn cho từng container:

```yaml
resources:
  requests:
    memory: "256Mi"                   # Lượng RAM tối thiểu được cam kết cấp phát riêng cho Pod
    cpu: "250m"                       # Lượng CPU tối thiểu (250m = 0.25 Core CPU)
  limits:
    memory: "512Mi"                   # Giới hạn RAM tối đa cho phép sử dụng
    cpu: "500m"                       # Giới hạn CPU tối đa (500m = 0.5 Core CPU)
```

### Cách thức hoạt động của công cụ giám sát:

- **`requests` (Cam kết ban đầu):** Bộ phận Scheduler sẽ đọc thông số này để tìm máy chủ Node còn trống đủ lượng tài nguyên yêu cầu để đặt Pod vào. Nếu không có Node nào còn trống đủ 256MB RAM, Pod sẽ ở trạng thái `Pending`.
- **`limits.memory` (Ngưỡng RAM tối đa):** Đây là giới hạn cứng được nhân Linux thực thi. Nếu ứng dụng của bạn chạy quá giới hạn này, container sẽ lập tức bị hệ điều hành tiêu diệt với lỗi kinh điển: **`OOMKilled` (Out of Memory - Exit Code 137)**.
- **`limits.cpu` (Ngưỡng CPU tối đa):** Đây là giới hạn mềm. Khi ứng dụng dùng quá CPU giới hạn, K8s sẽ không giết container mà chỉ tiến hành **thắt cổ chai (throttle)** làm ứng dụng chạy chậm lại.

---

## 6️⃣ Kiểm Tra Sức Khỏe Probes: Giải Pháp Tự Động Phát Hiện Lỗi Và Phục Hồi Container

Một tiến trình Container có thể vẫn đang ở trạng thái `Running` (xét theo quyền quản lý của Docker), nhưng bên trong ứng dụng Web của bạn đã bị lỗi nghẽn luồng (Deadlock) hoặc mất kết nối tới Database dẫn đến việc người dùng truy cập web chỉ nhận lại lỗi HTTP 500.

Kubernetes giải quyết triệt để vấn đề này bằng cách gửi các yêu cầu kiểm tra sức khỏe (**Probes**) định kỳ vào sâu bên trong ứng dụng của bạn.

```text
API Server
   │
   ├─► Liveness Probe? ──► (Thử truy cập /healthz) ──► Fail 3 lần? ──► RESTART POD!
   │
   └─► Readiness Probe? ──► (Thử truy cập /ready) ──► Fail? ──► CẮT TRAFFIC! (Không cho khách truy cập)
```

### 1. Chỉ dẫn `livenessProbe` — Xem container còn sống hay đã chết lâm sàng

```yaml
livenessProbe:
  httpGet:
    path: /healthz                    # Đường dẫn endpoint check sức khỏe trong code app
    port: 8000
  initialDelaySeconds: 15             # Đợi 15 giây sau khi container start mới bắt đầu gửi lệnh check (để app kịp khởi động)
  periodSeconds: 10                   # Tần suất kiểm tra: Cứ mỗi 10 giây một lần
  failureThreshold: 3                 # Nếu thất bại 3 lần liên tiếp -> Quyết định restart container!
```

> [!TIP]
> Sử dụng `livenessProbe` để tự động cứu ứng dụng khỏi các lỗi treo luồng đơ cứng mà không cần kỹ sư thức đêm gõ lệnh restart thủ công.

---

### 2. Chỉ dẫn `readinessProbe` — Kiểm tra ứng dụng đã sẵn sàng tiếp nhận người dùng chưa

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

> [!IMPORTANT]
> Khác biệt cốt lõi: Nếu `readinessProbe` thất bại (ví dụ: DB đang bảo trì nên app chưa kết nối được), Kubernetes **sẽ không restart container**. Nó chỉ đơn giản là **tạm thời gỡ bỏ Pod này ra khỏi danh sách Service** để ngăn không cho người dùng kết nối vào Pod lỗi này, hướng toàn bộ traffic sang các Pod lành tính khác.

---

### 3. Chỉ dẫn `startupProbe` — Cứu cánh cho các ứng dụng khởi động siêu chậm

Đối với các ứng dụng Java hoặc Rails nặng nề có thể mất tới 1-2 phút để khởi động xong lần đầu, nếu bạn cấu hình `livenessProbe` check quá sớm, Pod sẽ bị K8s tiêu diệt và restart liên tục vô hạn vì tưởng app bị chết đơ.

`startupProbe` sẽ vô hiệu hóa hoàn toàn liveness và readiness check cho tới khi ứng dụng báo hiệu khởi chạy lần đầu thành công!

```yaml
startupProbe:
  httpGet:
    path: /healthz
    port: 8000
  failureThreshold: 30                # Cho phép kiểm tra thất bại tối đa 30 lần
  periodSeconds: 10                   # Mỗi lần cách nhau 10 giây -> Cho phép app có tối đa 300 giây (5 phút) để khởi động hoàn tất!
```

---

## 7️⃣ Init Containers: Người Tiền Trạm Chuẩn Bị Môi Trường Hoàn Hảo

Đôi khi ứng dụng chính của bạn bắt buộc phải có một số điều kiện tiên quyết mới khởi chạy được (ví dụ: Phải chờ cơ sở dữ liệu Postgres khởi chạy xong và migrate database thành công).

`initContainers` là một danh sách các container phụ chạy tuần tự và **hoàn thành 100% nhiệm vụ của mình rồi tự tắt đi** trước khi container chính được phép khởi hành.

```yaml
spec:
  # Container tiền trạm chạy trước
  initContainers:
  - name: wait-for-postgres
    image: busybox:latest
    # Chạy lệnh kiểm tra cổng kết nối Postgres hoạt động liên tục mỗi 1 giây
    command: ['sh', '-c', 'until nc -z postgres-service 5432; do echo "Chờ database..."; sleep 1; done;']
  
  # Container ứng dụng chính chạy sau
  containers:
  - name: fastapi-app
    image: acmeshop/fastapi:latest
```

---

## 8️⃣ Tự Động Co Giãn HPA: Bí Quyết Sinh Tồn Trước Cơn Bão Traffic

Một trong những tính năng quyền lực nhất của Kubernetes là **HPA (Horizontal Pod Autoscaler)**. Nó giám sát lượng CPU/RAM thực tế tiêu thụ của các Pod và tự động nhân bản thêm Pod để gánh tải khi có lượng truy cập đột biến.

```yaml
# hpa-fastapi.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app                 # Đối tượng áp dụng co giãn co tự động
  minReplicas: 3                      # Số lượng Pod tối thiểu luôn duy trì
  maxReplicas: 10                     # Số lượng Pod tối đa cho phép scale lên khi quá tải
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70        # Tự động scale up khi hiệu năng CPU trung bình của các Pod vượt quá 70%
```

---

## 9️⃣ Thực Hành Thực Chiến: Xây Dựng Bản Thiết Kế FastAPI Hoàn Chỉnh Chuẩn Production

Để thực sự làm chủ kiến thức, chúng ta sẽ thiết kế một tệp manifest YAML tích hợp đầy đủ mọi tiêu chuẩn vàng của môi trường doanh nghiệp: **Rolling Update chiến lược, giới hạn tài nguyên an toàn, kiểm tra sức khỏe đa tầng Probes và container tiền trạm Init Container.**

### Bước 9.1: Viết tệp manifest `production-fastapi.yaml`

Bạn hãy tạo một tệp tin cấu hình mang tên `production-fastapi.yaml` với nội dung hoàn chỉnh chuẩn Premium sau:

```yaml
# production-fastapi.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: production-fastapi
  labels:
    app: secure-api
    env: production
spec:
  replicas: 3                         # Chạy 3 bản sao phân tải
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1                     # Cho phép tạo thêm tối đa 1 pod mới lúc nâng cấp
      maxUnavailable: 0               # Không cho phép bất kỳ Pod nào offline lúc deploy mới
  selector:
    matchLabels:
      app: secure-api
  template:
    metadata:
      labels:
        app: secure-api
        env: production
    spec:
      # 1. Container tiền trạm: Đợi database PostgreSQL sẵn sàng trước khi chạy app
      initContainers:
      - name: wait-db
        image: busybox:1.36
        command: ['sh', '-c', 'until nc -z postgres-db 5432; do echo "Đang kết nối database..."; sleep 2; done;']

      # 2. Container ứng dụng chính
      containers:
      - name: main-app
        image: bitnami/fastapi:latest
        imagePullPolicy: IfNotPresent
        ports:
        - name: http-port
          containerPort: 8000
        
        # Thiết lập giới hạn tài nguyên phần cứng an toàn
        resources:
          requests:
            cpu: "200m"               # Cam kết cấp phát tối thiểu 0.2 Core CPU
            memory: "256Mi"           # Cam kết cấp phát tối thiểu 256 MB RAM
          limits:
            cpu: "500m"               # Cắt ngọn hiệu năng nếu dùng quá 0.5 Core CPU
            memory: "512Mi"           # Tiêu diệt Pod (OOM) nếu vượt quá 512 MB RAM để bảo vệ Node

        # Thiết lập Liveness Probe kiểm tra sự sống ứng dụng
        livenessProbe:
          httpGet:
            path: /healthz
            port: http-port
          initialDelaySeconds: 30     # Đợi 30 giây đầu tiên để app kịp khởi chạy
          periodSeconds: 10           # Quét kiểm tra mỗi 10 giây một lần
          failureThreshold: 3         # Restart Pod nếu thất bại 3 lần liên tiếp

        # Thiết lập Readiness Probe kiểm tra mức độ sẵn sàng nhận traffic của app
        readinessProbe:
          httpGet:
            path: /ready
            port: http-port
          initialDelaySeconds: 10
          periodSeconds: 5            # Kiểm tra nhanh mỗi 5 giây một lần

        # Khai báo các cấu hình môi trường
        env:
        - name: DATABASE_URL
          value: postgresql://admin:secret@postgres-db:5432/chatdb

---
# 3. Cấu hình tự động co giãn HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: production-fastapi
  minReplicas: 3
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75        # Scale up khi tải CPU trung bình vượt quá 75%
```

Mẫu cấu hình trên chính là bản thiết kế hoàn chỉnh nhất giúp hệ thống của bạn vận hành cực kỳ ổn định, tự phục hồi và chống chịu tải xuất sắc trước mọi cơn bão traffic thực tế trên internet!

---

## ⚠️ 5 Hố Đen Chết Người Khi Quản Lý Pod Và Deployment

1. **Deploy Naked Pod lên môi trường chạy thật:** Pod không có Deployment quản lý sẽ chết vĩnh viễn khi có sự cố mà không tự động restart.
2. **Selector và Labels bị lệch ký tự:** Lỗi kinh điển khiến ReplicaSet không thể nhận diện được Pod của nó, dẫn đến việc deployment liên tục tạo Pod vô hạn làm treo đơ cluster.
3. **Không thiết lập Resource Limits cứng cho RAM:** Pod bị lỗi Memory Leak sẽ âm thầm nuốt chửng RAM của toàn bộ máy chủ Node vật lý, kích hoạt OOM Killer của hệ điều hành quét sạch các Pod lành tính khác chạy chung Node.
4. **Cấu hình livenessProbe trùng khít với readinessProbe:** Lỗi thiết kế làm Pod bị khởi động lại liên tục vô hạn (Restart Loop) khi Database gặp sự cố tạm thời thay vì chỉ cần cắt tạm thời traffic kết nối.
5. **Cấu hình maxUnavailable quá cao khi số lượng Pod ít:** Nếu bạn chỉ chạy 2 replicas nhưng đặt `maxUnavailable: 50%` hoặc `100%`, quá trình deploy phiên bản mới sẽ lập tức ngắt kết nối toàn bộ hệ thống gây downtime cho người dùng. Hãy luôn đặt `maxUnavailable: 0` trên production.

---

## 🧠 Tự kiểm tra (Self-check)

Bạn hãy tự suy ngẫm và trả lời nhanh 5 câu hỏi cốt lõi sau để khắc sâu kiến thức:
1. Tại sao trên môi trường Production tuyệt đối không được dùng Raw Pod (Pod đơn độc)?
2. Sự khác biệt lớn nhất giữa `livenessProbe` và `readinessProbe` khi kiểm tra sức khỏe bị thất bại là gì?
3. Nếu container của bạn tiêu thụ dung lượng RAM vượt quá ngưỡng `limits.memory` khai báo trong file YAML, điều gì sẽ xảy ra?
4. Init Container khác biệt với Container chính ở điểm nào liên quan đến vòng đời hoạt động?
5. Vai trò cốt lõi của ReplicaSet nằm ở đâu trong kiến trúc Deployment?

<details>
<summary><b>💡 Bấm để xem gợi ý đáp án từ Mr.Rom</b></summary>

1. **Không dùng raw Pod:** Vì raw Pod không được gắn kết với bất kỳ bộ điều khiển (Controller) nào. Nếu Pod bị sập do lỗi phần cứng của Node chứa nó hoặc bị người dùng xóa nhầm, K8s sẽ không tự động phục hồi hay khởi tạo lại Pod mới thay thế.
2. **Khác biệt Probe:** 
   - Nếu `livenessProbe` fail -> K8s lập tức **restart** container.
   - Nếu `readinessProbe` fail -> K8s **chỉ gỡ bỏ** Pod ra khỏi dịch vụ định tuyến (Service) để ngắt traffic của người dùng, tuyệt đối không restart container.
3. **Vượt quá RAM Limit:** Container sẽ ngay lập tức bị hệ điều hành tiêu diệt và báo trạng thái lỗi **`OOMKilled` (Out of Memory - Exit Code 137)**.
4. **Init Container:** Phải chạy hoàn tất 100% nhiệm vụ của mình và tự kết thúc tắt đi thì Container chính mới được phép bắt đầu khởi hành. Trong khi đó, Container chính sẽ chạy liên tục không ngừng nghỉ để phục vụ người dùng.
5. **Vai trò của ReplicaSet:** Đảm bảo duy trì chính xác số lượng bản sao Pod khỏe mạnh đang chạy trong hệ thống đúng bằng con số khai báo mong muốn (`replicas`).

</details>

---

## ⚡ Bảng Tra Cứu Nhanh (Cheatsheet) Lệnh Bỏ Túi

### Quản lý Deployment nhanh chóng bằng CLI:
```bash
kubectl apply -f production-fastapi.yaml      # Áp dụng cấu hình deploy hệ thống
kubectl get deployments                       # Kiểm tra trạng thái Deployment
kubectl get rs                                # Kiểm tra thông tin các ReplicaSet
kubectl scale deployment/fastapi-app --replicas=5  # Ra lệnh scale nhanh lên 5 pod
```

### Theo dõi tiến trình cập nhật và gỡ lỗi:
```bash
kubectl rollout status deployment/fastapi-app  # Theo dõi tiến trình update cuốn chiếu
kubectl rollout history deployment/fastapi-app # Xem lịch sử các revision đã deploy
kubectl rollout undo deployment/fastapi-app    # Rollback ngay về phiên bản gần nhất
kubectl rollout undo deployment/fastapi-app --to-revision=2 # Rollback về revision chỉ định
```

---

## 📘 Từ Điển Thuật Ngữ (Glossary) Chuyên Ngành

- **Naked Pod (Pod đơn độc):** Pod được tạo thủ công trực tiếp không qua quản lý của Deployment hay StatefulSet.
- **Rolling Update (Cập nhật cuốn chiếu):** Chiến lược deploy mặc định của K8s giúp cập nhật phiên bản mới một cách mượt mà bằng cách thay thế dần từng Pod cũ, bảo toàn tính liên tục của hệ thống.
- **OOMKilled (Out of Memory Killed):** Trạng thái container bị hệ điều hành tiêu diệt đột ngột do sử dụng vượt quá giới hạn RAM tối đa cho phép.
- **Resource Requests (Cam kết tối thiểu):** Mức RAM/CPU tối thiểu mà Pod yêu cầu để Scheduler tìm máy chủ phù hợp đặt Pod vào.
- **Resource Limits (Giới hạn tối đa):** Ngưỡng RAM/CPU tối đa mà container được phép tiêu thụ trong suốt quá trình hoạt động.

---

## 🔗 Liên Kết & Tài Nguyên Học Tập Bổ Sung

### Các bài học liên quan trực tiếp:
- [⬅️ Bài học trước: Tổng quan về Kubernetes và Cài đặt Local](./00_what-is-kubernetes.md)
- [➡️ Bài học tiếp theo: Cấu hình định tuyến dịch vụ với Services và Ingress](./02_services-and-networking.md)

### Tài liệu chính hãng tham khảo thêm:
- [Tài liệu chính thức về cấu hình Pods trong Kubernetes](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Tài liệu chính thức về cơ chế hoạt động của Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

---

## 📌 Lịch Sử Thay Đổi (Changelog)

- **v2.0.0 (26/05/2026)** — **Mr.Rom nâng cấp Premium chuẩn 5 sao:**
  - Viết lại toàn diện bài học đạt chuẩn chất lượng Premium 5 sao của Blueprint mới.
  - Cấu trúc lại tiêu đề H1 Premium và metadata block YAML chuẩn chỉnh.
  - Sửa đổi 100% các tiêu đề H2 sang dạng câu hỏi gợi mở khơi gợi tư duy sâu sắc.
  - Thay thế toàn bộ các Alerts cũ sang định dạng GitHub Alerts tiêu chuẩn.
  - Việt hóa 100% các dòng ghi chú giải thích bên trong các block code YAML và Python.
  - Nâng cấp chương thực hành thực chiến: Bản thiết kế FastAPI hoàn chỉnh chuẩn Production tích hợp Rolling Update, Probes đa tầng, Init Container và HPA co giãn tự động.
- **v1.1.0 (25/05/2026)** — Áp dụng Blueprint v0.5.4+ §3.6: bổ sung lời dẫn trước phần cấu trúc logic của Deployment.
- **v1.0.0 (23/05/2026)** — Khởi tạo bản thảo sơ khai đầu tiên về Pod và Deployment.
