# 📋 Terraform - Cheatsheet

> **Quick Reference for Terraform**
>
> *Tra cứu nhanh Terraform*

---

## 🔧 Basic Commands (Lệnh cơ bản)

```bash
terraform init              # Initialize (Khởi tạo)
terraform fmt               # Format code (Định dạng)
terraform validate          # Validate syntax (Xác thực)
terraform plan              # Preview changes (Xem trước)
terraform apply             # Apply changes (Áp dụng)
terraform apply -auto-approve  # Apply without confirm
terraform destroy           # Destroy all (Xóa tất cả)
```

---

## 📊 State Commands (Lệnh state)

```bash
terraform state list        # List resources (Liệt kê)
terraform state show aws_instance.web
terraform state mv old_name new_name
terraform state rm resource_name
terraform state pull        # Download state
terraform import aws_instance.web i-xxx  # Import existing
```

---

## 📝 Basic Syntax

```hcl
# Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Resource
resource "aws_instance" "web" {
  ami           = "ami-xxx"
  instance_type = "t3.micro"
  
  tags = {
    Name = "web-server"
  }
}

# Variable
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# Output
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

---

## 🧩 Common Patterns (Patterns phổ biến)

```hcl
# Data source (Lấy dữ liệu)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/*"]
  }
}

# Local values
locals {
  common_tags = {
    Environment = var.environment
    Project     = "myapp"
  }
}

# Count (Số lượng)
resource "aws_instance" "server" {
  count         = 3
  instance_type = "t3.micro"
  ami           = data.aws_ami.ubuntu.id
}

# For_each
resource "aws_subnet" "this" {
  for_each          = var.subnets
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az
}
```

---

## 🔄 GitLab CI Integration (Tích hợp GitLab CI)

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - apply

terraform-validate:
  stage: validate
  image: hashicorp/terraform
  script:
    - terraform init
    - terraform validate

terraform-plan:
  stage: plan
  image: hashicorp/terraform
  script:
    - terraform init
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - tfplan
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
