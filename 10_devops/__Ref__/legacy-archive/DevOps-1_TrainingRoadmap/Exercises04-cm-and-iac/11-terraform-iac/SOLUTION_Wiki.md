# Lời giải và Hướng dẫn - Bài 11: Terraform

Chào mừng bạn đến với bài thực hành về Terraform. Tôi đã chuẩn bị một file cấu hình (`main.tf`) sử dụng `local provider`. Provider này cho phép chúng ta thực hành chu trình làm việc của Terraform một cách an toàn bằng cách tạo và quản lý các file trên chính máy tính của bạn, không cần đến bất kỳ tài khoản cloud nào.

**Yêu cầu:** Máy tính của bạn phải được cài đặt Terraform.

Hãy mở terminal, di chuyển vào thư mục của bài tập này (`workspare/.../11-terraform-iac`) và làm theo các bước dưới đây.

---

### Bài 1: Viết mã Terraform đầu tiên

**Mục tiêu:** Hiểu cấu trúc của một file cấu hình Terraform cơ bản.

Bước này đã được tôi thực hiện sẵn bằng cách tạo ra file `main.tf`. Hãy cùng phân tích nó:

```hcl
# main.tf
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.2.3"
    }
  }
}

provider "local" {}

resource "local_file" "devops_intro" {
  content  = "Hello, Terraform! This is my first resource."
  filename = "${path.module}/hello-iac.txt"
}
```

-   **`terraform { ... }`**: Khối này khai báo các yêu cầu của dự án. Ở đây, chúng ta yêu cầu Terraform phải có `provider` tên là `local` của `hashicorp`.
-   **`provider "local" {}`**: Cấu hình cho provider `local`. Provider này rất đơn giản nên không cần cấu hình gì thêm.
-   **`resource "local_file" "devops_intro" { ... }`**: Đây là phần chính, định nghĩa một "tài nguyên".
    -   `local_file`: Loại tài nguyên (tạo một file local).
    -   `devops_intro`: Tên định danh cho tài nguyên này trong code Terraform.
    -   `content` và `filename`: Là các thuộc tính của tài nguyên, định nghĩa nội dung và tên của file sẽ được tạo.

---

### Bài 2: Chu trình `init`, `plan`, `apply`

**Mục tiêu:** Thực hành chu trình 3 bước cốt lõi của Terraform.

**1. `terraform init`**
Chạy lệnh này để khởi tạo dự án. Terraform sẽ đọc khối `terraform` trong file `main.tf` và tải về plugin cho `local` provider.

```bash
terraform init
```
-   **Kết quả mong đợi:** Bạn sẽ thấy thông báo Terraform đã tải xong provider và một thư mục `.terraform` được tạo ra.

**2. `terraform plan`**
Lệnh này sẽ tạo một "kế hoạch" hành động. Nó sẽ so sánh code của bạn với trạng thái hiện tại (chưa có gì) và cho bạn biết nó sẽ làm gì.

```bash
terraform plan
```
-   **Kết quả mong đợi:** Terraform sẽ in ra một kế hoạch, trong đó phần quan trọng nhất là:
    ```
    + create

    Terraform will perform the following actions:

      # local_file.devops_intro will be created
    + resource "local_file" "devops_intro" {
        + content              = "Hello, Terraform! This is my first resource."
        + file_permission      = "0777"
        + filename             = "./hello-iac.txt"
        + id                   = (known after apply)
      }

    Plan: 1 to add, 0 to change, 0 to destroy.
    ```
    -   Dấu `+` màu xanh lá cây có nghĩa là tài nguyên này sẽ được **tạo mới**.

**3. `terraform apply`**
Lệnh này sẽ thực thi kế hoạch đã tạo ở trên.

```bash
terraform apply
```
-   **Thực hiện:** Terraform sẽ hiển thị lại kế hoạch và hỏi bạn xác nhận. Gõ `yes` và nhấn Enter.
-   **Kiểm tra kết quả:**
    -   Một file mới tên là `hello-iac.txt` sẽ xuất hiện trong thư mục của bạn.
    -   Một file mới tên là `terraform.tfstate` cũng được tạo. Đây là file state cực kỳ quan trọng, giúp Terraform theo dõi trạng thái hạ tầng mà nó quản lý.

---

### Bài 3: Cập nhật Hạ tầng

**Mục tiêu:** Xem cách Terraform xử lý khi mã IaC thay đổi.

1.  **Thay đổi code:** Mở file `main.tf` và sửa dòng `content`:
    ```hcl
    content  = "Infrastructure as Code is awesome!"
    ```
2.  **Chạy `terraform plan`:**
    ```bash
    terraform plan
    ```
    -   **Kết quả mong đợi:** Lần này, Terraform sẽ phát hiện sự khác biệt giữa code và file state.
        ```
        ~ update in-place

        Terraform will perform the following actions:

        # local_file.devops_intro will be updated in-place
        ~ resource "local_file" "devops_intro" {
            ~ content              = "Hello, Terraform! This is my first resource." -> "Infrastructure as Code is awesome!"
            id                   = "./hello-iac.txt"
            # (other attributes unchanged)
        }

        Plan: 0 to add, 1 to change, 0 to destroy.
        ```
    -   Dấu `~` màu vàng có nghĩa là tài nguyên này sẽ được **cập nhật**.
3.  **Chạy `terraform apply`:**
    Chạy `terraform apply` và xác nhận với `yes`.
4.  **Kiểm tra kết quả:** Mở file `hello-iac.txt`, bạn sẽ thấy nội dung của nó đã được cập nhật.

---

### Bài 4: Dọn dẹp với `destroy`

**Mục tiêu:** Học cách xóa toàn bộ hạ tầng được quản lý bởi Terraform một cách an toàn.

1.  **Chạy `terraform destroy`:**
    ```bash
    terraform destroy
    ```
-   **Kết quả mong đợi:** Terraform sẽ lên kế hoạch xóa bỏ tài nguyên.
    ```
    - destroy

    Terraform will perform the following actions:

    # local_file.devops_intro will be destroyed
    - resource "local_file" "devops_intro" {
        - content              = "Infrastructure as Code is awesome!" -> null
        # ...
    }

    Plan: 0 to add, 0 to change, 1 to destroy.
    ```
    -   Dấu `-` màu đỏ có nghĩa là tài nguyên sẽ bị **xóa**.
2.  **Xác nhận:** Gõ `yes` và nhấn Enter.
3.  **Kiểm tra kết quả:** File `hello-iac.txt` sẽ biến mất khỏi thư mục của bạn.

Chúc mừng! Bạn đã hoàn thành chu trình làm việc IaC cơ bản với Terraform. Quy trình này áp dụng cho mọi tài nguyên, từ một file local đơn giản cho đến một hệ thống cloud phức tạp.