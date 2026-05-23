# Bài 9: Kubernetes (K8s) - Điều phối (Orchestration) Container

## 🎯 Mục tiêu bài học

-   Hiểu được tại sao cần một hệ thống điều phối (orchestration) như Kubernetes.
-   Nắm được kiến trúc tổng quan của một cụm Kubernetes (Control Plane và Worker Nodes).
-   Hiểu rõ vai trò của các đối tượng (Objects) cốt lõi: `Pod`, `Service`, `Deployment`, `ReplicaSet`.
-   Viết được các file manifest YAML đơn giản để định nghĩa các đối tượng trên.
-   Sử dụng công cụ `kubectl` để tương tác với cụm Kubernetes.

## 📖 Nội dung chính

1.  **Vấn đề của việc chạy container ở quy mô lớn:** Tại sao Docker một mình là không đủ?
2.  **Kubernetes là gì?** "Hệ điều hành cho đám mây".
3.  **Kiến trúc Kubernetes:**
    -   Control Plane (Master Node): "Bộ não" của cụm.
    -   Worker Node: "Cơ bắp" thực thi công việc.
4.  **Đối tượng Kubernetes (Kubernetes Objects):**
    -   `Pod`: Đơn vị triển khai nhỏ nhất, chứa một hoặc nhiều container.
    -   `ReplicaSet`: Đảm bảo một số lượng Pod copy luôn chạy.
    -   `Deployment`: Quản lý `ReplicaSet`, cho phép cập nhật ứng dụng (rolling update) và rollback.
    -   `Service`: Cung cấp một địa chỉ IP/DNS cố định để truy cập vào các Pod.
5.  **`kubectl`:** Công cụ dòng lệnh để "nói chuyện" với Kubernetes.
6.  **YAML Manifest:** Định nghĩa "trạng thái mong muốn".
7.  **Các khái niệm quan trọng khác:** Namespace, Probes, Resource Management.

## 🛠️ Công cụ & Lý thuyết

-   **Container Orchestration (Điều phối Container):** <u>Kubernetes</u>, Docker Swarm, Amazon ECS, HashiCorp Nomad.
-   **Local K8s Cluster (Cụm K8s tại local):** <u>Minikube</u>, kind, Docker Desktop.
-   **Công cụ dòng lệnh (Command-line tool):** <u>kubectl</u>.
-   **Lý thuyết:** Orchestration (Điều phối), Desired State (Trạng thái mong muốn), Declarative Configuration (Cấu hình khai báo), High Availability (Tính sẵn sàng cao).

---

# Nội dung chi tiết - Bài 9: Kubernetes (K8s) - Điều phối Container

Docker giúp chúng ta đóng gói và chạy ứng dụng trong các container một cách dễ dàng. Nhưng điều gì sẽ xảy ra khi ứng dụng của bạn phát triển và bạn cần chạy hàng trăm, thậm chí hàng ngàn container trên một cụm gồm nhiều máy chủ?

-   Làm thế nào để triển khai chúng?
-   Nếu một container hoặc một máy chủ bị chết, làm thế nào để tự động thay thế?
-   Làm thế nào để cân bằng tải giữa các container?
-   Làm thế nào để cập nhật ứng dụng lên phiên bản mới mà không gây gián đoạn dịch vụ?

Đây là lúc chúng ta cần một **Hệ thống Điều phối Container (Container Orchestration System)**, và Kubernetes chính là vị vua trong lĩnh vực này.

---

### 1. Kubernetes là gì?

**Kubernetes** (thường được viết tắt là **K8s** - do có 8 ký tự giữa 'K' và 's') là một nền tảng mã nguồn mở được phát triển bởi Google, dùng để **tự động hóa việc triển khai, mở rộng và quản lý các ứng dụng container hóa.**

> Hãy nghĩ về Kubernetes như một "hệ điều hành cho đám mây". Thay vì bạn phải quản lý từng máy chủ riêng lẻ, bạn chỉ cần "ra lệnh" cho Kubernetes, và nó sẽ tự tìm cách phân bổ tài nguyên, chạy container, và duy trì hệ thống của bạn ở "trạng thái mong muốn".

---

### 2. Kiến trúc Kubernetes

Một cụm (cluster) Kubernetes bao gồm hai loại máy chủ chính:

-   **Control Plane (trước đây gọi là Master Node):** Là "bộ não" của cụm. Nó đưa ra mọi quyết định, ví dụ như "chạy container này ở đâu?", "cần thêm bao nhiêu container?". Các thành phần chính của Control Plane bao gồm:
    -   **`kube-apiserver`**: Cổng giao tiếp (API) của cả cụm. Mọi lệnh (`kubectl`) đều đi qua đây.
    -   **`etcd`**: Một cơ sở dữ liệu key-value tin cậy, lưu trữ toàn bộ trạng thái của cụm (được coi là "nguồn chân lý duy nhất").
    -   **`kube-scheduler`**: Quyết định xem một Pod mới nên được chạy trên Worker Node nào dựa trên tài nguyên yêu cầu và các ràng buộc.
    -   **`kube-controller-manager`**: Chạy các bộ điều khiển (controllers) để đưa trạng thái hiện tại của cụm về trạng thái mong muốn.

-   **Worker Node:** Là các máy chủ "cơ bắp", nơi các container của bạn thực sự được chạy. Mỗi Worker Node có:
    -   **`kubelet`**: Agent của Kubernetes, giao tiếp với Control Plane và đảm bảo các container được chạy trong Pod đúng như yêu cầu.
    -   **`kube-proxy`**: Xử lý các vấn đề về mạng bên trong cụm, đảm bảo các Service có thể chuyển tiếp traffic đến đúng Pod.
    -   **Container Runtime:** Phần mềm chịu trách nhiệm chạy container (ví dụ: Docker, containerd).

---

### 3. Đối tượng Kubernetes (Kubernetes Objects)

Bạn không tương tác trực tiếp với container. Thay vào đó, bạn định nghĩa các **"Đối tượng" (Objects)** của Kubernetes bằng file YAML, và Kubernetes sẽ lo phần còn lại.

-   **`Pod`:**
    -   Là **đơn vị triển khai nhỏ nhất** trong Kubernetes.
    -   Một Pod đại diện cho một tiến trình đang chạy trong cụm của bạn.
    -   Một Pod chứa **một hoặc nhiều container** (ví dụ: một container ứng dụng chính và một container phụ để thu thập log). Các container trong cùng một Pod chia sẻ chung tài nguyên mạng và lưu trữ.

-   **`ReplicaSet`:**
    -   Nhiệm vụ của nó rất đơn giản: **đảm bảo rằng một số lượng bản sao (replicas) của một Pod luôn chạy.**
    -   Nếu một Pod bị chết, ReplicaSet sẽ ngay lập tức tạo ra một Pod mới để thay thế.
    -   Bạn thường không làm việc trực tiếp với ReplicaSet.

-   **`Deployment`:**
    -   Là đối tượng bạn sẽ làm việc thường xuyên nhất. Nó quản lý các ReplicaSet.
    -   `Deployment` cho phép bạn mô tả "trạng thái mong muốn" của ứng dụng, ví dụ: "Tôi muốn chạy 3 bản sao của ứng dụng A, phiên bản 1.2".
    -   **Tính năng quan trọng nhất:** Cung cấp cơ chế cập nhật ứng dụng một cách an toàn (`rolling update`) và khả năng quay lại phiên bản trước (`rollback`) nếu có lỗi.

-   **`Service`:**
    -   Pod rất "mong manh", chúng có thể bị xóa và tạo lại bất cứ lúc nào, và mỗi lần tạo lại chúng lại có một địa chỉ IP mới. Vậy làm thế nào để truy cập vào chúng một cách ổn định?
    -   `Service` giải quyết vấn đề này. Nó tạo ra một **điểm truy cập cố định** (một địa chỉ IP nội bộ và một tên DNS) cho một nhóm các Pod.
    -   Nó hoạt động như một bộ cân bằng tải (load balancer) nội bộ, phân phối traffic đến các Pod khỏe mạnh phía sau nó.

-   **`Namespace`:**
    -   Cung cấp một cách để **phân chia tài nguyên trong cụm** thành các không gian ảo, biệt lập.
    -   Giống như các thư mục trong một hệ thống file, bạn có thể dùng Namespace để tổ chức các ứng dụng theo từng dự án, môi trường (dev, staging, prod), hoặc đội nhóm.
    -   Mặc định, nếu bạn không chỉ định, các đối tượng sẽ được tạo trong namespace `default`.

---

### 4. `kubectl`: Giao tiếp với cụm

`kubectl` (viết tắt của Kubernetes Control) là công cụ dòng lệnh cho phép bạn "nói chuyện" với API server của Kubernetes.

-   `kubectl get pods`: Liệt kê tất cả các Pod trong namespace mặc định.
-   `kubectl get pods -n <tên-namespace>`: Liệt kê Pod trong một namespace cụ thể.
-   `kubectl get all`: Liệt kê tất cả các đối tượng phổ biến (Pod, Service, Deployment...).
-   `kubectl get deployments`: Liệt kê tất cả các Deployment.
-   `kubectl describe pod <pod-name>`: Xem thông tin chi tiết về một Pod.
-   `kubectl apply -f my-app.yaml`: Áp dụng (tạo hoặc cập nhật) các đối tượng được định nghĩa trong file YAML.
-   `kubectl delete -f my-app.yaml`: Xóa các đối tượng.
-   `kubectl logs <pod-name>`: Xem log của container trong Pod.
-   `kubectl exec -it <pod-name> -- /bin/sh`: Truy cập vào shell bên trong một container đang chạy.

---

### 5. YAML Manifest: Định nghĩa trạng thái mong muốn

Với Kubernetes, bạn định nghĩa mọi thứ bằng các file **YAML (YAML Ain't Markup Language)**. Đây là một cách thực hành **Infrastructure as Code (Hạ tầng dưới dạng mã)**.

*Ví dụ: một file `deployment.yaml` đơn giản:*
```yaml
apiVersion: apps/v1
kind: Deployment # Loại đối tượng là Deployment
metadata:
  name: my-nodejs-app-deployment
spec:
  replicas: 3 # Trạng thái mong muốn: có 3 bản sao
  selector:
    matchLabels:
      app: my-nodejs-app
  template: # Đây là template để tạo ra các Pod
    metadata:
      labels:
        app: my-nodejs-app
    spec:
      containers:
      - name: my-app-container # Tên của container
        image: your-username/my-nodejs-app:latest # Image đã build ở bài Docker
        ports:
        - containerPort: 8080 # Port mà ứng dụng của bạn lắng nghe bên trong container
```
Bạn chỉ cần khai báo "cái bạn muốn", và Kubernetes sẽ tự tìm cách để đạt được trạng thái đó. Đây được gọi là **cấu hình khai báo (declarative configuration)**.

## ✍️ Bài tập thực hành (Exercises)

Lý thuyết về Kubernetes có thể khá trừu tượng. Cách tốt nhất để hiểu nó là bắt tay vào làm. Loạt bài tập này sẽ hướng dẫn bạn triển khai ứng dụng đầu tiên lên một cụm K8s.

**Yêu cầu:**
-   Đã cài đặt `kubectl`.
-   Đã có một cụm Kubernetes tại local. Lựa chọn đơn giản nhất là **kích hoạt Kubernetes có sẵn trong Docker Desktop** (Settings -> Kubernetes -> Enable Kubernetes). Hoặc bạn có thể cài đặt [Minikube](https://minikube.sigs.k8s.io/docs/start/).
-   Sử dụng image `your-dockerhub-username/my-first-app:1.0` mà bạn đã push lên Docker Hub ở bài Docker.

**Bài 1: Viết Manifest cho Deployment**
1.  Tạo một thư mục mới cho bài thực hành này, ví dụ `k8s-practice`.
2.  Bên trong, tạo một file mới tên `deployment.yaml`.
3.  Dựa vào ví dụ trong bài học, hãy viết một `Deployment` để chạy ứng dụng của bạn.
    -   `kind`: `Deployment`
    -   `metadata`: đặt `name` là `my-app-deployment`.
    -   `spec.replicas`: `2` (chúng ta muốn chạy 2 bản sao của ứng dụng).
    -   `spec.selector.matchLabels`: đặt `app: my-app`.
    -   `spec.template.metadata.labels`: cũng đặt `app: my-app` (phải khớp với selector ở trên).
    -   `spec.template.spec.containers`:
        -   `name`: `my-app-container`
        -   `image`: `[TÀI KHOẢN DOCKER HUB CỦA BẠN]/my-first-app:1.0`
        -   `ports`: `containerPort` là `8080`.

**Bài 2: Triển khai ứng dụng với `kubectl`**
1.  Mở terminal trong thư mục `k8s-practice`.
2.  Áp dụng file manifest để ra lệnh cho Kubernetes tạo Deployment: `kubectl apply -f deployment.yaml`.
3.  Kiểm tra xem Deployment đã được tạo và sẵn sàng chưa: `kubectl get deployments`.
4.  Kiểm tra xem `ReplicaSet` đã được tạo tự động chưa: `kubectl get replicasets`.
5.  Quan trọng nhất, kiểm tra xem 2 Pod đã được tạo và đang chạy (Running) chưa: `kubectl get pods`.
6.  Xem log của một trong hai Pod để chắc chắn ứng dụng đã khởi động: `kubectl logs [tên-pod-của-bạn]`.

**Bài 3: Expose ứng dụng ra ngoài với `Service`**
1.  Hiện tại, ứng dụng đang chạy nhưng bị cô lập trong cụm. Ta cần tạo một `Service` để truy cập nó.
2.  Tạo một file mới `service.yaml`.
3.  Viết một `Service` loại `NodePort`.
    -   `kind`: `Service`
    -   `metadata`: đặt `name` là `my-app-service`.
    -   `spec.type`: `NodePort`.
    -   `spec.selector`: `app: my-app` (quan trọng: phải khớp với label của các Pod).
    -   `spec.ports`:
        -   `port`: `80` (Cổng nội bộ của Service).
        -   `targetPort`: `8080` (Cổng của container mà Service sẽ chuyển traffic tới).
4.  Áp dụng file này: `kubectl apply -f service.yaml`.
5.  Kiểm tra Service: `kubectl get services`. Tìm dòng `my-app-service`, bạn sẽ thấy một cổng được gán trong cột `PORT(S)`, ví dụ `80:31234/TCP`. Con số `31234` chính là `NodePort`.
6.  Mở trình duyệt và truy cập `http://localhost:[NodePort đó]`. Bạn sẽ thấy ứng dụng của mình!

**Bài 4: Trải nghiệm "Phép màu" của Kubernetes**
1.  **Tự phục hồi (Self-healing):**
    -   Lấy danh sách các Pod: `kubectl get pods -o wide` (`-o wide` để xem Pod đang nằm ở Node nào).
    -   Xóa một trong hai Pod: `kubectl delete pod [tên-pod-của-bạn]`.
    -   Ngay lập tức, chạy lại `kubectl get pods`. Bạn thấy điều gì? Kubernetes, thông qua ReplicaSet, đã phát hiện Pod bị thiếu và tự động tạo một Pod mới để thay thế, đảm bảo `replicas: 2` luôn đúng.
2.  **Mở rộng (Scaling):**
    -   Chỉnh sửa file `deployment.yaml`, thay đổi `replicas` từ `2` lên `4`.
    -   Áp dụng lại sự thay đổi: `kubectl apply -f deployment.yaml`.
    -   Kiểm tra lại số lượng Pod: `kubectl get pods`. Bạn sẽ thấy Kubernetes đang tự động tạo thêm 2 Pod mới.

---

Trong các bài học tiếp theo, chúng ta sẽ tìm hiểu cách tự động hóa việc cài đặt và cấu hình các máy chủ Worker Node bằng Ansible, và cách tạo ra cả một cụm Kubernetes bằng Terraform.

[Bài trước: Giới thiệu về Docker](../08-docker-introduction/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Ansible - Quản lý Cấu hình](../../Lesson04-cm-and-iac/10-ansible-config-management/)