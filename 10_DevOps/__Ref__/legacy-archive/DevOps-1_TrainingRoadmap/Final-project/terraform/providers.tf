# terraform/providers.tf

# Khối terraform định nghĩa các provider cần thiết
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0" # Tương thích với phiên bản 4.x của AWS provider
    }
  }
}

# Cấu hình AWS provider
provider "aws" {
  region = "us-east-1" # Ví dụ: chọn region N. Virginia
}

/*
# GHI CHÚ QUAN TRỌNG VỀ STATE
# Trong một dự án thực tế, bạn KHÔNG BAO GIỜ được lưu file state trên local.
# Bạn phải cấu hình remote backend để lưu state một cách an toàn và cho phép làm việc nhóm.
# Dưới đây là ví dụ cấu hình backend S3 (đã được comment lại).

terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket-unique-name"
    key            = "final-project/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}
*/
