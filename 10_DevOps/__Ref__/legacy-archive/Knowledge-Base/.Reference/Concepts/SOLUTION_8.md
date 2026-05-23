# Lời giải và Giải thích - Bài 9: Kubernetes (K8s)

Chào mừng bạn đến với bài học về Kubernetes. Vì đây là một bài giới thiệu lý thuyết, "lời giải" ở đây sẽ là một bộ các file cấu hình YAML mẫu và một bản giải thích chi tiết để biến các khái niệm trừu tượng thành những ví dụ cụ thể.

Chúng ta sẽ sử dụng lại Docker image `my-first-app` đã tạo ở bài học trước.

---

### Tổng quan: `Deployment` và `Service` liên kết với nhau như thế nào?

Trong Kubernetes, chúng ta không chạy container một cách trực tiếp. Thay vào đó, chúng ta dùng các đối tượng để quản lý chúng:

1.  **`Deployment`**: Nhiệm vụ của nó là **chạy và duy trì** ứng dụng của bạn. Bạn yêu cầu nó: "Hãy chạy 3 bản sao của ứng dụng `my-first-app`", và `Deployment` sẽ tạo ra 3 `Pod`, mỗi `Pod` chứa một container chạy image `my-first-app`. Nếu một `Pod` bị lỗi, `Deployment` sẽ tự động tạo ra cái mới.
2.  **`Service`**: Các `Pod` có thể bị xóa và tạo lại, dẫn đến địa chỉ IP của chúng liên tục thay đổi. Nhiệm vụ của `Service` là tạo ra một **điểm truy cập mạng cố định và ổn định** cho các `Pod` này. Nó tìm các `Pod` phù hợp dựa trên `labels` (nhãn) và hoạt động như một bộ cân bằng tải (load balancer) nội bộ, phân phối traffic đến chúng.

Mối liên kết giữa `Deployment` và `Service` được thực hiện thông qua `labels` và `selectors`.

---

### Giải thích chi tiết `deployment.yaml`

File này khai báo "trạng thái mong muốn" cho ứng dụng của bạn.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment # 1. Loại đối tượng: Deployment
metadata:
  name: my-app-deployment # 2. Tên của Deployment này
spec:
  replicas: 3 # 3. Trạng thái mong muốn: Luôn có 3 bản sao (Pod) của ứng dụng chạy
  selector:
    matchLabels:
      app: my-app # 4. Cách Deployment tìm các Pod mà nó quản lý
  template: # 5. "Bản thiết kế" để tạo ra các Pod
    metadata:
      labels:
        app: my-app # 6. Gán nhãn cho mỗi Pod được tạo ra. Phải khớp với `selector` ở trên.
    spec:
      containers:
      - name: my-app-container
        image: my-first-app:latest # 7. Docker image sẽ được sử dụng
        ports:
        - containerPort: 8080 # 8. Cổng mà ứng dụng bên trong container đang lắng nghe
```

1.  **`kind: Deployment`**: Khai báo rằng chúng ta muốn tạo một đối tượng `Deployment`.
2.  **`metadata.name`**: Đặt tên cho `Deployment` là `my-app-deployment`.
3.  **`spec.replicas: 3`**: Yêu cầu Kubernetes đảm bảo rằng luôn có 3 `Pod` chạy ứng dụng này.
4.  **`spec.selector`**: Định nghĩa cách `Deployment` tìm và quản lý các `Pod`. Ở đây, nó sẽ tìm tất cả các `Pod` có nhãn (`label`) là `app: my-app`.
5.  **`spec.template`**: Là phần khuôn mẫu để tạo ra các `Pod`. Mọi `Pod` do `Deployment` này tạo ra sẽ có cấu hình y hệt như phần `template` này.
6.  **`template.metadata.labels`**: Gán nhãn `app: my-app` cho mỗi `Pod`. **Đây là điểm kết nối cực kỳ quan trọng**, vì nó khớp với `selector` ở mục (4).
7.  **`template.spec.containers.image`**: Chỉ định rằng container bên trong `Pod` sẽ chạy image `my-first-app:latest` (image chúng ta đã build ở bài Docker).
8.  **`template.spec.containers.ports.containerPort`**: Thông báo rằng ứng dụng bên trong container đang lắng nghe trên cổng `8080`.

---

### Giải thích chi tiết `service.yaml`

File này tạo ra một "cửa ngõ" để thế giới bên ngoài có thể truy cập vào các `Pod` đang chạy.

```yaml
# service.yaml
apiVersion: v1
kind: Service # 1. Loại đối tượng: Service
metadata:
  name: my-app-service # 2. Tên của Service này
spec:
  type: NodePort # 3. Loại Service.
  selector:
    app: my-app # 4. Tìm các Pod có nhãn `app: my-app` để gửi traffic đến.
  ports:
    - protocol: TCP
      port: 80 # 5. Cổng của chính Service này (bên trong cluster).
      targetPort: 8080 # 6. Cổng mà container đang lắng nghe.
```

1.  **`kind: Service`**: Khai báo rằng chúng ta muốn tạo một đối tượng `Service`.
2.  **`metadata.name`**: Đặt tên cho `Service` là `my-app-service`.
3.  **`spec.type: NodePort`**: Đây là một cách để "xuất bản" `Service` ra bên ngoài cụm K8s. Nó sẽ mở một cổng tĩnh trên mỗi Worker Node. Bất kỳ traffic nào đến cổng này trên Node sẽ được chuyển tiếp đến `Service`.
4.  **`spec.selector`**: **Đây là điểm kết nối thứ hai**. `Service` này sẽ tìm kiếm tất cả các `Pod` trong cụm có nhãn `app: my-app` và tự động gửi traffic đến chúng. Đây chính là cách `Service` biết được `Pod` nào thuộc về `Deployment` của chúng ta.
5.  **`ports.port: 80`**: Cổng mà `Service` này "lắng nghe" ở bên trong cụm.
6.  **`ports.targetPort: 8080`**: Cổng đích trên các `Pod` mà traffic sẽ được chuyển tiếp đến. Giá trị này phải khớp với `containerPort` trong `deployment.yaml`.

**Luồng traffic:** `Bên ngoài -> <IP của Node>:<NodePort> -> Service (cổng 80) -> Pod (cổng 8080)`

---

### Làm thế nào để sử dụng các file này?

Để chạy các file này, bạn cần có một cụm Kubernetes đang hoạt động (ví dụ: `minikube`, `kind`, hoặc `Docker Desktop`).

1.  **Chạy lệnh `apply`:**
    Lệnh này sẽ gửi định nghĩa của bạn đến Kubernetes API Server. Kubernetes sẽ đọc và bắt đầu tạo các đối tượng.
    ```bash
    # Chạy lệnh trong thư mục chứa 2 file yaml
    kubectl apply -f deployment.yaml -f service.yaml
    ```
2.  **Kiểm tra trạng thái:**
    ```bash
    # Kiểm tra xem Deployment đã được tạo chưa
    kubectl get deployments

    # Kiểm tra xem 3 Pod đã được tạo và đang chạy chưa (có thể mất một lúc)
    kubectl get pods

    # Kiểm tra xem Service đã được tạo và có NodePort chưa
    kubectl get services
    ```
3.  **Truy cập ứng dụng:**
    Nếu bạn dùng Minikube, cách dễ nhất là chạy lệnh:
    ```bash
    minikube service my-app-service
    ```
    Minikube sẽ tự động mở trình duyệt và trỏ đến đúng địa chỉ IP và cổng của ứng dụng.

Chúc mừng bạn đã có cái nhìn tổng quan về cách triển khai một ứng dụng trên Kubernetes!