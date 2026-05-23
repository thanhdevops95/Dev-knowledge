# main.tf
# File cấu hình Terraform để thực hành với 'local' provider.

# Khối `terraform` định nghĩa các yêu cầu về provider cho dự án.
terraform {
  required_providers {
    # Khai báo rằng chúng ta cần provider "local" của HashiCorp.
    local = {
      source  = "hashicorp/local"
      version = "2.2.3" # Ghim phiên bản provider để đảm bảo tính nhất quán.
    }
  }
}

# Khối `provider` dùng để cấu hình cho một provider cụ thể.
# Provider "local" không yêu cầu cấu hình gì thêm.
provider "local" {}

# Khối `resource` là phần quan trọng nhất, dùng để định nghĩa một tài nguyên hạ tầng.
# Cú pháp: resource "<loại_tài_nguyên>" "<tên_đại_diện>"
resource "local_file" "devops_intro" {
  # Các thuộc tính (arguments) của tài nguyên.
  
  # `content` định nghĩa nội dung của file sẽ được tạo.
  content  = "Hello, Terraform! This is my first resource."
  
  # `filename` định nghĩa đường dẫn và tên file sẽ được tạo.
  # `path.module` là một biến đặc biệt, trỏ đến thư mục chứa file .tf này.
  filename = "${path.module}/hello-iac.txt"
}
