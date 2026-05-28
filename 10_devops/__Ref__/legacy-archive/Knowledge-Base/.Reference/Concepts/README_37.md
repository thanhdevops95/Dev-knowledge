# Dự án Tốt nghiệp: Quy trình CI/CD hoàn chỉnh cho Ứng dụng Web trên AWS EKS

Chào mừng bạn đến với dự án tốt nghiệp của Lộ trình học DevOps. Dự án này là sự kết hợp của tất cả các công cụ và khái niệm mà chúng ta đã học, nhằm mục đích xây dựng một quy trình tự động hóa CI/CD hoàn chỉnh để triển khai một ứng dụng web lên cụm Kubernetes trên AWS.

---

##  Kiến trúc tổng quan

Dự án này mô phỏng một quy trình DevOps hiện đại:

`Developer` -> `git push` -> `GitLab CI/CD` -> `Build & Push to Docker Hub` -> `Deploy to AWS EKS`

-   **Ứng dụng:** Một ứng dụng web đơn giản gồm Frontend (React) và Backend (Node.js).
-   **Containerization:** `Docker` được sử dụng để đóng gói frontend và backend thành các image độc lập. `Docker Compose` được dùng để chạy toàn bộ stack trên môi trường local.
-   **Infrastructure as Code (IaC):** `Terraform` được sử dụng để tự động tạo và quản lý toàn bộ hạ tầng trên AWS, bao gồm mạng (VPC) và cụm Kubernetes (EKS).
-   **CI/CD:** `GitLab CI` là công cụ điều phối chính. Nó tự động build các Docker image mới khi có code thay đổi và triển khai chúng lên cụm EKS.
-   **Container Orchestration:** `Kubernetes` (thông qua dịch vụ AWS EKS) chịu trách nhiệm chạy, mở rộng và quản lý các container ứng dụng của chúng ta.

---

## Cấu trúc thư mục dự án

```
.
├── app/                  # Chứa mã nguồn ứng dụng
│   ├── backend/          # Ứng dụng backend (Node.js)
│   │   ├── src/index.js
│   │   ├── package.json
│   │   └── Dockerfile
│   └── frontend/         # Ứng dụng frontend (React)
│       ├── src/App.js
│       ├── package.json
│       └── Dockerfile
├── kubernetes/           # Chứa các file manifest (.yaml) cho Kubernetes
│   ├── backend-deployment.yml
│   ├── backend-service.yml
│   ├── frontend-deployment.yml
│   ├── frontend-service.yml
│   └── secret.yml
├── terraform/            # Chứa code Terraform để tạo hạ tầng
│   ├── eks.tf
│   ├── providers.tf
│   └── vpc.tf
├── .gitlab-ci.yml        # File định nghĩa pipeline CI/CD trên GitLab
└── docker-compose.yml    # File để chạy toàn bộ ứng dụng trên môi trường local
```

---

## Hướng dẫn thực thi dự án (Conceptual Guide)

Đây là các bước bạn cần thực hiện trong một môi trường thực tế để triển khai dự án này.

### Bước 0: Điều kiện tiên quyết

1.  **Tài khoản:** Bạn cần có tài khoản tại AWS, GitLab, và Docker Hub.
2.  **Công cụ trên máy:** Cài đặt `git`, `docker`, `docker-compose`, `terraform`, và `kubectl` trên máy tính của bạn.
3.  **Cấu hình Credentials:** Cấu hình AWS credentials trên máy của bạn để Terraform có thể sử dụng.

### Bước 1: Kiểm tra trên môi trường Local

Mục tiêu của bước này là để đảm bảo ứng dụng và các Docker image được cấu hình đúng.
1.  Mở terminal tại thư mục gốc của dự án (`Final-project`).
2.  Chạy lệnh sau:
    ```bash
    docker-compose up --build
    ```
3.  Docker Compose sẽ build các image cho frontend, backend và khởi chạy chúng cùng với database Postgres.
4.  Mở trình duyệt và truy cập `http://localhost:3000`. Bạn sẽ thấy ứng dụng frontend chạy.

### Bước 2: Tạo hạ tầng với Terraform

Bây giờ, chúng ta sẽ tạo hạ tầng thực tế trên AWS.
1.  Di chuyển vào thư mục `terraform/`: `cd terraform`.
2.  Chạy `terraform init` để tải về các provider cần thiết.
3.  Chạy `terraform plan` để xem Terraform sẽ tạo ra những tài nguyên gì. Hãy xem kỹ kế hoạch này.
4.  Chạy `terraform apply` và xác nhận bằng cách gõ `yes`. Quá trình này sẽ mất khá nhiều thời gian (15-20 phút) vì nó đang tạo một cụm EKS hoàn chỉnh.
5.  Sau khi `apply` thành công, bạn cần cấu hình `kubectl` trên máy để có thể kết nối đến cụm EKS vừa tạo. Chạy lệnh theo hướng dẫn của AWS, ví dụ:
    ```bash
    aws eks --region us-east-1 update-kubeconfig --name final-project-cluster
    ```

### Bước 3: Cấu hình dự án GitLab và Biến CI/CD

1.  Tạo một dự án mới trên GitLab.
2.  Push toàn bộ mã nguồn trong thư mục `Final-project` này lên dự án GitLab đó.
3.  Trong dự án GitLab, đi đến **Settings > CI/CD > Variables**. Bạn cần tạo các biến sau để pipeline có thể hoạt động:
    -   `DOCKER_USER`: Tên tài khoản Docker Hub của bạn.
    -   `DOCKER_PASS`: Mật khẩu hoặc Access Token của Docker Hub. (Nên chọn "Masked").
    -   `AWS_ACCESS_KEY_ID`: Access key của tài khoản AWS.
    -   `AWS_SECRET_ACCESS_KEY`: Secret key của tài khoản AWS. (Nên chọn "Masked").
    -   `KUBE_CONFIG`:
        -   **Type:** `File`
        -   **Value:** Sao chép toàn bộ nội dung file `~/.kube/config` trên máy bạn (sau khi đã chạy lệnh `aws eks update-kubeconfig...` ở Bước 2) và dán vào đây.

### Bước 4: Kích hoạt Pipeline

1.  Bây giờ, hãy thử thay đổi một chút trong mã nguồn, ví dụ sửa lại một dòng chữ trong file `app/frontend/src/App.js`.
2.  Commit và `git push` thay đổi đó lên GitLab.
3.  Hành động này sẽ tự động kích hoạt pipeline mà chúng ta đã định nghĩa trong `.gitlab-ci.yml`.
4.  Vào mục **CI/CD > Pipelines** trong dự án GitLab để theo dõi pipeline chạy. Bạn sẽ thấy nó lần lượt đi qua các stage `build` và `deploy`.

### Bước 5: Kiểm tra ứng dụng

1.  Sau khi pipeline chạy thành công, `Service` `frontend-service` loại `LoadBalancer` sẽ được tạo trên EKS. Kubernetes sẽ yêu cầu AWS tạo ra một Elastic Load Balancer.
2.  Chạy lệnh sau để lấy địa chỉ của Load Balancer đó:
    ```bash
    kubectl get service frontend-service
    ```
3.  Trong cột `EXTERNAL-IP`, bạn sẽ thấy một địa chỉ URL dài. Sao chép địa chỉ đó và dán vào trình duyệt.
4.  Chúc mừng! Ứng dụng của bạn giờ đã chạy trên một cụm Kubernetes trên AWS, được triển khai hoàn toàn tự động.

### Bước 6: Dọn dẹp

**Đây là bước quan trọng nhất để tránh tốn tiền!**
1.  Vào thư mục `terraform/`.
2.  Chạy lệnh:
    ```bash
    terraform destroy
    ```
3.  Xác nhận bằng cách gõ `yes`. Terraform sẽ xóa toàn bộ các tài nguyên (EKS, VPC,...) đã tạo trên AWS.
4.  Bạn cũng có thể xóa các Docker image đã push lên Docker Hub và xóa dự án trên GitLab.

Dự án này là một minh chứng mạnh mẽ cho kỹ năng của bạn. Hãy tùy chỉnh, cải tiến nó và đưa vào portfolio của mình!