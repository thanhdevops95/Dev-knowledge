# Bài 15: Dự án Tốt nghiệp - Triển khai ứng dụng Web hoàn chỉnh

## 🎯 Mục tiêu bài học

-   Vận dụng và kết hợp tất cả các công cụ và kiến thức đã học trong suốt lộ trình.
-   Trải nghiệm một quy trình DevOps hoàn chỉnh từ đầu đến cuối trong một kịch bản gần với thực tế.
-   Xây dựng một portfolio (sản phẩm mẫu) ấn tượng để thể hiện kỹ năng với nhà tuyển dụng.

## 📖 Nội dung chính

Dự án sẽ bao gồm việc triển khai một ứng dụng web đơn giản (ví dụ: một ứng dụng "Todo list" với frontend React và backend Node.js) lên AWS, sử dụng một quy trình tự động hóa hoàn toàn.

**Các bước thực hiện:**

1.  **Phân tích ứng dụng:** Chuẩn bị một ứng dụng web đơn giản có thể container hóa.
2.  **Container hóa:** Viết `Dockerfile` cho frontend và backend, và một file `docker-compose.yml` để chạy chúng trên môi trường local.
3.  **Hạ tầng dưới dạng Mã (IaC):**
    -   Viết code **Terraform** để tạo ra các tài nguyên hạ tầng cần thiết trên AWS:
        -   Một **VPC** với các public và private subnets.
        -   Một cụm **Kubernetes (EKS - Elastic Kubernetes Service)**.
        -   Một cơ sở dữ liệu **RDS (PostgreSQL)**.
4.  **Quản lý Cấu hình:** Viết **Ansible Playbook** (tùy chọn) để cấu hình các worker node nếu cần.
5.  **CI/CD Pipeline:**
    -   Sử dụng **GitLab CI** để tạo một pipeline hoàn chỉnh.
    -   **Stage Build:** Build các Docker image cho frontend và backend, sau đó đẩy (push) chúng lên một container registry (ví dụ: Docker Hub hoặc AWS ECR).
    -   **Stage Test:** Chạy các unit test.
    -   **Stage Deploy:** Sử dụng `kubectl` để áp dụng các file manifest Kubernetes (Deployment, Service) lên cụm EKS, triển khai phiên bản mới của ứng dụng.
6.  **Giám sát và Ghi log:**
    -   Triển khai **Prometheus** và **Grafana** lên cụm Kubernetes để giám sát tài nguyên của cụm và của ứng dụng.
    -   Triển khai **Fluentd** để thu thập log của các container và đẩy về **Elasticsearch**, sau đó dùng **Kibana** để xem log.

## 🏆 Kết quả mong đợi

-   Một kho chứa Git hoàn chỉnh chứa mã nguồn ứng dụng, Dockerfile, code Terraform, và file `.gitlab-ci.yml`.
-   Một pipeline CI/CD hoạt động trên GitLab, tự động triển khai ứng dụng lên Kubernetes mỗi khi có commit mới.
-   Một ứng dụng web chạy trên AWS EKS.
-   Các dashboard trên Grafana và Kibana để giám sát và xem log của ứng dụng.

---

# Nội dung chi tiết - Bài 15: Dự án Tốt nghiệp

Chúc mừng bạn đã đi đến bài học cuối cùng trong phần kỹ thuật! Đây là lúc để tổng hợp tất cả những mảnh ghép kiến thức mà chúng ta đã thu thập trong suốt hành trình thành một bức tranh hoàn chỉnh. Dự án này sẽ là một bài thực hành tổng hợp, mô phỏng một quy trình DevOps thực tế từ đầu đến cuối.

---

### Kịch bản dự án

Chúng ta sẽ triển khai một ứng dụng web "Todo List" đơn giản. Ứng dụng này bao gồm:
-   **Frontend:** Một ứng dụng React.js giao tiếp với backend qua API.
-   **Backend:** Một API server viết bằng Node.js/Express, lưu trữ dữ liệu trong một database PostgreSQL.

**Mục tiêu:** Triển khai ứng dụng này lên cụm Kubernetes (EKS) trên AWS một cách hoàn toàn tự động thông qua pipeline CI/CD trên GitLab.

---

### Bước 1: Chuẩn bị và Container hóa ứng dụng

1.  **Chuẩn bị mã nguồn:** Lấy mã nguồn của một ứng dụng Todo List có sẵn hoặc tự viết một ứng dụng đơn giản. Đảm bảo frontend và backend nằm trong các thư mục riêng.
2.  **Viết Dockerfile cho Backend:**
    -   Bắt đầu từ `FROM node:16-alpine`.
    -   Sao chép `package.json` và chạy `npm install`.
    -   Sao chép toàn bộ mã nguồn còn lại.
    -   `EXPOSE` cổng mà API server lắng nghe.
    -   Dùng `CMD` để khởi động server.
3.  **Viết Dockerfile cho Frontend:**
    -   Sử dụng multi-stage build.
    -   **Stage 1 (Build):** Dùng `node:16-alpine`, sao chép code, chạy `npm install` và `npm run build` để tạo ra các file tĩnh.
    -   **Stage 2 (Serve):** Dùng `nginx:alpine`, sao chép các file tĩnh đã build từ stage 1 vào thư mục phục vụ web của Nginx.
4.  **Viết `docker-compose.yml`:**
    -   Định nghĩa 3 services: `frontend`, `backend`, và `postgres`.
    -   Cấu hình network để các service có thể giao tiếp với nhau.
    -   Mục tiêu là có thể chạy toàn bộ ứng dụng trên máy local chỉ bằng lệnh `docker-compose up`.

---

### Bước 2: Tạo Hạ tầng bằng Terraform

Viết một bộ code Terraform để tự động tạo ra các tài nguyên sau trên AWS:
1.  **VPC:** Tạo một VPC mới với các public và private subnets trên nhiều Availability Zones để đảm bảo tính sẵn sàng cao.
2.  **EKS Cluster (Elastic Kubernetes Service):**
    -   Tạo Control Plane của EKS.
    -   Tạo một nhóm các Worker Node (EC2 instances) sẽ tham gia vào cụm.
3.  **RDS Instance (Relational Database Service):**
    -   Tạo một database PostgreSQL. Đặt nó trong private subnet để không thể truy cập trực tiếp từ Internet.
    -   Cấu hình Security Group để chỉ cho phép các Worker Node của EKS kết nối đến database.
4.  **Outputs:** Xuất ra các thông tin quan trọng như endpoint của cụm EKS, tên database...

---

### Bước 3: Định nghĩa ứng dụng trên Kubernetes

Viết các file manifest YAML để triển khai ứng dụng lên cụm EKS:
1.  **`secret.yml`:** Tạo một Secret để lưu trữ thông tin kết nối database (username, password, host).
2.  **`backend-deployment.yml`:**
    -   Tạo một `Deployment` cho backend.
    -   Chỉ định Docker image của backend (sẽ được build bởi CI/CD).
    -   Gắn các thông tin từ `Secret` vào container dưới dạng biến môi trường.
3.  **`backend-service.yml`:** Tạo một `Service` (ClusterIP) để các Pod frontend có thể giao tiếp với backend bên trong cụm.
4.  **`frontend-deployment.yml`:** Tạo một `Deployment` cho frontend.
5.  **`frontend-service.yml`:** Tạo một `Service` (LoadBalancer). Dịch vụ này sẽ yêu cầu AWS tự động tạo ra một Elastic Load Balancer để "phơi" ứng dụng frontend ra Internet.

---

### Bước 4: Xây dựng Pipeline CI/CD trên GitLab

Tạo file `.gitlab-ci.yml` với các stage sau:
1.  **`build`:**
    -   Đăng nhập vào Docker Hub (hoặc AWS ECR).
    -   Build Docker image cho backend, tag nó với commit SHA.
    -   Push image backend lên registry.
    -   Build và push image frontend tương tự.
2.  **`test`:**
    -   Chạy các unit test cho backend và frontend.
3.  **`deploy`:**
    -   Cấu hình `kubectl` để kết nối đến cụm EKS đã tạo bởi Terraform.
    -   Sử dụng lệnh `sed` hoặc `envsubst` để thay thế tag của image trong file `backend-deployment.yml` và `frontend-deployment.yml` bằng commit SHA mới nhất.
    -   Chạy `kubectl apply -f .` để triển khai phiên bản mới của ứng dụng.

---

### Bước 5 (Nâng cao): Giám sát và Ghi log

1.  **Cài đặt Prometheus và Grafana:** Sử dụng Helm (một trình quản lý gói cho Kubernetes) để dễ dàng triển khai Prometheus và Grafana lên cụm. Import các dashboard có sẵn để giám sát tài nguyên cụm và các Pod.
2.  **Cài đặt EFK:** Triển khai Elasticsearch, Fluentd (dưới dạng DaemonSet để chạy trên mọi node), và Kibana để thu thập, lưu trữ và phân tích log của ứng dụng.

## 📋 Kế hoạch thực hiện dự án (Project Checklist)

Dự án này rất lớn. Hãy chia nhỏ nó thành các giai đoạn và các nhiệm vụ cụ thể để dễ quản lý và thực hiện. Đây là một checklist gợi ý.

---

### Giai đoạn 1: Chuẩn bị & Container hóa (Môi trường Local)
*Mục tiêu: Đảm bảo ứng dụng có thể chạy được dưới dạng container trên máy của bạn.*

-   [ ] **Chuẩn bị mã nguồn:** Chuẩn bị sẵn code cho ứng dụng frontend (React) và backend (Node.js).
-   [ ] **Viết `Dockerfile` cho Backend:**
    -   Tạo một file `Dockerfile` trong thư mục backend.
    -   Sử dụng image `node:16-alpine` hoặc tương đương.
    -   Tối ưu hóa build-cache bằng cách copy `package.json` và chạy `npm install` trước, sau đó mới copy phần code còn lại.
-   [ ] **Viết `Dockerfile` cho Frontend:**
    -   Tạo một file `Dockerfile` trong thư mục frontend.
    -   Áp dụng kỹ thuật "multi-stage build".
    -   *Stage 1:* Dùng image `node` để build ứng dụng React, tạo ra các file tĩnh trong thư mục `build`.
    -   *Stage 2:* Dùng image `nginx:alpine` và copy kết quả từ thư mục `build` của stage 1 vào.
-   [ ] **Tạo `docker-compose.yml`:**
    -   Viết một file `docker-compose.yml` ở thư mục gốc.
    -   Định nghĩa 3 services: `frontend`, `backend`, và `postgres` (dùng image `postgres:13`).
    -   Cấu hình biến môi trường và network để các service có thể giao tiếp với nhau.
-   [ ] **Xác minh:**
    -   Chạy `docker-compose up --build`.
    -   Truy cập ứng dụng trên trình duyệt và xác nhận mọi chức năng (thêm, xóa, sửa todo) hoạt động bình thường trên môi trường local.

---

### Giai đoạn 2: Hạ tầng dưới dạng Mã (Terraform)
*Mục tiêu: Viết code để tự động tạo ra môi trường hạ tầng trên AWS.*

-   [ ] **Cấu hình Terraform:**
    -   Tạo thư mục `terraform`.
    -   Định nghĩa AWS provider và cấu hình backend để lưu state file trên S3 (khuyến khích).
-   [ ] **Mạng (VPC):**
    -   Viết code để tạo một VPC mới.
    -   Tạo các public subnets và private subnets trên ít nhất 2 Availability Zones.
    -   Tạo Internet Gateway, Route Tables.
-   [ ] **Cơ sở dữ liệu (RDS):**
    -   Viết code để tạo một RDS instance (PostgreSQL).
    -   Đặt RDS vào trong các private subnets.
    -   Tạo một Security Group cho RDS, chỉ cho phép traffic trên cổng 5432 từ bên trong VPC.
-   [ ] **Kubernetes (EKS):**
    -   Viết code để tạo một EKS control plane.
    -   Tạo một Node Group (các máy chủ EC2 làm worker node) và đặt chúng vào public subnets.
    -   Cấu hình IAM Roles cần thiết cho EKS.
-   [ ] **Xác minh:**
    -   Chạy `terraform init`, `terraform plan`, và `terraform apply`.
    -   Kiểm tra trên AWS Management Console để thấy các tài nguyên (VPC, EKS, RDS) đã được tạo.

---

### Giai đoạn 3: Định nghĩa ứng dụng trên Kubernetes
*Mục tiêu: Viết các file manifest để Kubernetes hiểu cách chạy ứng dụng của bạn.*

-   [ ] **Cấu hình `kubectl`:** Cấu hình `kubectl` trên máy của bạn để có thể kết nối đến cụm EKS vừa tạo.
-   [ ] **Secrets:** Tạo file `secret.yml` để lưu trữ các thông tin nhạy cảm như username, password của database.
-   [ ] **Backend:** Tạo `backend-deployment.yml` và `backend-service.yml` (loại `ClusterIP`). Deployment này sẽ sử dụng các biến môi trường từ Secret.
-   [ ] **Frontend:** Tạo `frontend-deployment.yml` và `frontend-service.yml` (loại `LoadBalancer`).
-   [ ] **Xác minh (Tùy chọn):** Thử `kubectl apply -f .` để triển khai ứng dụng lên EKS bằng tay. Truy cập vào địa chỉ của LoadBalancer để kiểm tra xem ứng dụng có hoạt động không.

---

### Giai đoạn 4: Tự động hóa với CI/CD (GitLab CI)
*Mục tiêu: Tạo một pipeline tự động build và triển khai ứng dụng mỗi khi có code mới.*

-   [ ] **Cấu hình GitLab:**
    -   Lưu các credentials (AWS Access Key, Secret Key,...) dưới dạng biến CI/CD trong phần Settings của dự án GitLab.
    -   Lưu nội dung file `kubeconfig` để kết nối đến EKS dưới dạng biến `file`.
-   [ ] **Viết `.gitlab-ci.yml`:**
    -   **Stage `build`:**
        -   Đăng nhập vào registry (Docker Hub hoặc AWS ECR).
        -   Build image cho backend, tag với `$CI_COMMIT_SHORT_SHA`.
        -   Push image backend lên registry.
        -   Làm tương tự cho frontend.
    -   **Stage `deploy`:**
        -   Sử dụng image có chứa `kubectl` và `envsubst`.
        -   Dùng `envsubst` để thay thế các biến (ví dụ: image tag) trong file `.yml` của Kubernetes bằng các biến môi trường của GitLab CI.
        -   Chạy `kubectl apply` với các file manifest đã được cập nhật.
-   [ ] **Xác minh:**
    -   Tạo một commit mới và push lên GitLab.
    -   Theo dõi pipeline chạy.
    -   Sau khi pipeline thành công, kiểm tra lại ứng dụng trên trình duyệt để thấy thay đổi đã được cập nhật.

Dự án này sẽ là một bằng chứng xác thực nhất cho kỹ năng DevOps của bạn. Hãy đưa nó lên GitHub và đính kèm vào CV của mình!

[Bài trước: Nhập môn AWS](../../Lesson06-cloud-platforms/14-aws-core-services/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Tổng kết và Định hướng nghề nghiệp](../16-career-orientation/)