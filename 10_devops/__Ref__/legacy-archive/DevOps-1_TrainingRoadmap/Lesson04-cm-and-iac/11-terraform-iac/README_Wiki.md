# Bài 11: Terraform - Hạ tầng dưới dạng Mã (Infrastructure as Code)

## 🎯 Mục tiêu bài học

-   Hiểu rõ khái niệm Hạ tầng dưới dạng Mã (Infrastructure as Code - IaC) và lợi ích của nó.
-   Phân biệt được vai trò của Terraform (cung cấp hạ tầng) và Ansible (cấu hình hạ tầng).
-   Nắm vững chu trình làm việc cốt lõi của Terraform: `init`, `plan`, `apply`.
-   Viết được file cấu hình Terraform đơn giản để tạo một tài nguyên trên cloud (ví dụ: một máy chủ ảo EC2 trên AWS).
-   Hiểu được các khái niệm cơ bản: `Provider`, `Resource`, `Variable`, `Output`.

## 📖 Nội dung chính

1.  **Hạ tầng dưới dạng Mã (IaC) là gì?**
2.  **Giới thiệu Terraform:** Cung cấp (provisioning) hạ tầng một cách khai báo.
3.  **Terraform vs. Ansible:** Công cụ nào cho việc gì?
4.  **Chu trình làm việc của Terraform:** `init`, `plan`, `apply`, `destroy`.
5.  **Cú pháp HCL (HashiCorp Configuration Language):**
    -   `provider`: Nhà cung cấp đám mây (AWS, Azure, GCP,...).
    -   `resource`: Một thành phần hạ tầng (máy chủ, database, mạng,...).
    -   `variable`: Tham số hóa cấu hình.
    -   `output`: Trích xuất thông tin từ hạ tầng đã tạo.
6.  **Quản lý State:** File `terraform.tfstate`.
7.  **Thực hành:** Viết code Terraform để tạo một máy chủ AWS EC2.

## 🛠️ Công cụ & Lý thuyết

-   **Công cụ IaC:** <u>Terraform</u>, OpenTofu, Pulumi, AWS CloudFormation, Azure ARM Templates.
-   **Công cụ dòng lệnh:** `terraform`.
-   **Lý thuyết:** Infrastructure as Code (IaC), Declarative vs. Imperative, State Management.

---

# Nội dung chi tiết - Bài 11: Terraform - Hạ tầng dưới dạng Mã

Trong khi Ansible giúp chúng ta cấu hình những gì **bên trong** một máy chủ (phần mềm, file, dịch vụ), Terraform giúp chúng ta tạo ra **chính máy chủ đó**, cùng với toàn bộ hạ tầng xung quanh nó như mạng, database, load balancer... Đây chính là Hạ tầng dưới dạng Mã (Infrastructure as Code - IaC).

---

### 1. Hạ tầng dưới dạng Mã (IaC) là gì?

IaC là phương pháp quản lý và cung cấp hạ tầng máy tính thông qua các file cấu hình có thể đọc được bởi máy, thay vì cấu hình thủ công qua giao diện web hoặc các công cụ tương tác.

**Lợi ích:**
-   **Tái sử dụng và Nhất quán:** Bạn có thể dùng cùng một bộ code để tạo ra môi trường Development, Staging, và Production giống hệt nhau.
-   **Tự động hóa:** Tích hợp vào pipeline CI/CD để tự động tạo hạ tầng cho việc kiểm thử hoặc triển khai.
-   **Lưu vết và Kiểm soát phiên bản:** Toàn bộ hạ tầng của bạn được lưu trong Git. Bạn biết ai đã thay đổi gì, khi nào, và tại sao.
-   **Khả năng phục hồi sau thảm họa (Disaster Recovery):** Nếu cả một vùng (region) của nhà cung cấp đám mây gặp sự cố, bạn có thể nhanh chóng tái tạo lại toàn bộ hạ tầng ở một vùng khác từ code.

---

### 2. Giới thiệu Terraform

Terraform là một công cụ IaC mã nguồn mở được tạo bởi HashiCorp. Nó cho phép bạn định nghĩa hạ tầng của mình bằng một ngôn ngữ cấu hình khai báo (declarative) gọi là HCL (HashiCorp Configuration Language).

Bạn chỉ cần **mô tả hạ tầng bạn muốn**, và Terraform sẽ tự tìm cách để tạo, cập nhật hoặc xóa các tài nguyên trên các nhà cung cấp đám mây (AWS, GCP, Azure,...) để đạt được trạng thái đó.

---

### 3. Terraform vs. Ansible: Công cụ nào cho việc gì?

Đây là một điểm thường gây nhầm lẫn cho người mới bắt đầu.

| Tiêu chí       | Terraform                                     | Ansible                                               |
|---------------|-----------------------------------------------|-------------------------------------------------------|
| **Mục đích chính** | **Cung cấp hạ tầng (Provisioning)**           | **Quản lý cấu hình (Configuration Management)**       |
| **Phạm vi**     | Tạo máy chủ, VPC, database, load balancer... | Cài đặt phần mềm, quản lý file, user, service... **bên trong** máy chủ. |
| **Cách tiếp cận** | Khai báo (Declarative)                        | Thủ tục (Procedural) nhưng có tính Idempotent          |
| **Ví von**      | **Xây dựng ngôi nhà** và lắp đặt điện, nước.  | **Sắp xếp đồ đạc** và trang trí bên trong ngôi nhà. |

**Thực tế:** Terraform và Ansible thường được sử dụng **cùng nhau**. Terraform xây dựng hạ tầng, sau đó nó có thể gọi Ansible để cấu hình các máy chủ vừa được tạo.

---

### 4. Chu trình làm việc của Terraform

Terraform có một chu trình 3 bước rất rõ ràng:

1.  **`terraform init`**:
    -   Chạy một lần duy nhất cho mỗi dự án.
    -   Nó tải về các plugin cần thiết cho nhà cung cấp đám mây mà bạn định nghĩa (ví dụ: `aws` provider).
    -   Khởi tạo backend để lưu file state.

2.  **`terraform plan`**:
    -   Đây là bước "chạy thử". Terraform sẽ so sánh trạng thái hạ tầng mong muốn (trong code của bạn) với trạng thái hạ tầng thực tế (trên cloud).
    -   Nó sẽ tạo ra một kế hoạch (plan) chi tiết về những gì sẽ được tạo, thay đổi, hoặc xóa.
    -   **Đây là bước cực kỳ quan trọng để bạn kiểm tra lại trước khi thực hiện bất kỳ thay đổi nào.**

3.  **`terraform apply`**:
    -   Thực thi kế hoạch đã được tạo ra ở bước `plan`.
    -   Sau khi bạn xem xét kế hoạch và gõ `yes`, Terraform sẽ tiến hành gọi các API của nhà cung cấp đám mây để tạo/thay đổi hạ tầng.

-   **`terraform destroy`**: Xóa tất cả các tài nguyên hạ tầng được quản lý bởi Terraform. **Hãy cẩn thận với lệnh này!**

---

### 5. Cú pháp HCL

*Ví dụ: file `main.tf` để tạo một máy chủ AWS EC2*
```hcl
# 1. Khai báo nhà cung cấp
provider "aws" {
  region = "us-east-1"
}

# 2. Khai báo biến
variable "instance_type" {
  description = "Loại máy chủ EC2"
  type        = string
  default     = "t2.micro"
}

# 3. Định nghĩa một tài nguyên
resource "aws_instance" "my_server" {
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
  instance_type = var.instance_type      # Sử dụng giá trị từ biến

  tags = {
    Name = "MyTerraformServer"
  }
}

# 4. Định nghĩa một output
output "public_ip" {
  description = "Địa chỉ IP public của máy chủ"
  value       = aws_instance.my_server.public_ip
}
```

---

### 6. Quản lý State

Terraform cần một nơi để lưu trữ mapping giữa các tài nguyên trong code của bạn và các tài nguyên thực tế trên cloud. Nó làm điều này thông qua một file gọi là **Terraform state** (`terraform.tfstate`).

-   Đây là file quan trọng nhất trong một dự án Terraform. **Không bao giờ được chỉnh sửa file này bằng tay.**
-   Mặc định, file này được lưu trên máy local. Nhưng khi làm việc nhóm, bạn phải cấu hình **remote state** (lưu trên S3, Azure Blob Storage,...) để mọi người có thể chia sẻ và khóa (lock) file state khi có người đang chạy `apply`.

Trong bài học tiếp theo, sau khi đã tạo ra và cấu hình được hạ tầng, chúng ta sẽ tìm hiểu cách giám sát chúng để đảm bảo hệ thống luôn hoạt động ổn định.

---

## ✍️ Bài tập thực hành (Exercises)

Để hiểu được chu trình làm việc của Terraform mà không cần tài khoản cloud, chúng ta sẽ thực hành với `local` provider. Provider này cho phép Terraform quản lý các file trên chính máy tính của bạn.

**Yêu cầu:**
-   Cài đặt Terraform trên máy của bạn. Tham khảo [hướng dẫn cài đặt Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli).

**Bài 1: Viết mã Terraform đầu tiên**
1.  Tạo một thư mục mới cho bài thực hành, ví dụ `terraform-practice`.
2.  Bên trong thư mục đó, tạo một file mới tên là `main.tf`.
3.  Dán nội dung sau vào file `main.tf`. Đây là code để định nghĩa việc tạo ra một file text.
    ```hcl
    # Khối này khai báo rằng chúng ta cần provider "local"
    terraform {
      required_providers {
        local = {
          source  = "hashicorp/local"
          version = "2.2.3"
        }
      }
    }

    # Cấu hình cho provider "local" (ở đây không cần cấu hình gì thêm)
    provider "local" {}

    # Định nghĩa một tài nguyên: một file local
    resource "local_file" "devops_intro" {
      content  = "Hello, Terraform! This is my first resource."
      filename = "${path.module}/hello-iac.txt" # Tạo file trong thư mục hiện tại
    }
    ```

**Bài 2: Chu trình `init`, `plan`, `apply`**
1.  Mở terminal trong thư mục `terraform-practice`.
2.  Chạy lệnh `terraform init`. Quan sát Terraform tải về provider `hashicorp/local`. Một thư mục `.terraform` sẽ được tạo ra.
3.  Chạy `terraform plan`. Đọc kỹ "kế hoạch" mà Terraform đưa ra. Bạn sẽ thấy một mục `+ create` cho tài nguyên `local_file.devops_intro`.
4.  Chạy `terraform apply`. Terraform sẽ hiển thị lại kế hoạch và hỏi bạn xác nhận. Gõ `yes` và nhấn Enter.
5.  **Kiểm tra kết quả:** Một file mới tên là `hello-iac.txt` đã được tạo ra trong thư mục của bạn. Mở file đó ra xem nội dung. Bạn cũng sẽ thấy một file `terraform.tfstate` đã được tạo.

**Bài 3: Cập nhật Hạ tầng (dưới dạng mã)**
1.  Mở file `main.tf` và thay đổi giá trị của thuộc tính `content` thành một câu khác, ví dụ: `"Infrastructure as Code is awesome!"`.
2.  Lưu file lại và chạy `terraform plan`. Terraform sẽ phát hiện sự thay đổi và báo cho bạn biết nó sẽ cập nhật (`~ update in-place`) tài nguyên `local_file.devops_intro`.
3.  Chạy `terraform apply` và xác nhận.
4.  Kiểm tra lại nội dung file `hello-iac.txt`. Nội dung đã được cập nhật đúng như trong code của bạn.

**Bài 4: Dọn dẹp với `destroy`**
1.  Khi đã thực hành xong, hãy chạy lệnh `terraform destroy`.
2.  Terraform sẽ lên kế hoạch xóa (`- destroy`) tài nguyên đã tạo. Gõ `yes` để xác nhận.
3.  File `hello-iac.txt` sẽ bị xóa khỏi thư mục của bạn. Hạ tầng đã được dọn dẹp sạch sẽ.

---

Trong bài học tiếp theo, sau khi đã tạo ra và cấu hình được hạ tầng, chúng ta sẽ tìm hiểu cách giám sát chúng để đảm bảo hệ thống luôn hoạt động ổn định.

[Bài trước: Ansible - Quản lý Cấu hình](../10-ansible-config-management/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Giám sát với Prometheus & Grafana](../../Lesson05-monitoring-logging-alerting/12-prometheus-and-grafana/)