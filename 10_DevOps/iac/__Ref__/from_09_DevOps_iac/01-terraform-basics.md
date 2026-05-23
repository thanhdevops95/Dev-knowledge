# 🏗️ Terraform cơ bản — Infrastructure as Code

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Quản lý hạ tầng cloud bằng code

---

## Tại sao Terraform?

```
❌ Thủ công (Console):
  Click AWS Console → Tạo VPC → Tạo EC2 → Tạo RDS → Cấu hình SG...
  Ai làm? Ai biết cấu hình gì? Rollback thế nào?

✅ Terraform (IaC):
  Viết code mô tả infra → terraform apply → Tạo TẤT CẢ tự động
  Version control (Git) → Review → Reproducible → Destroy khi không dùng
```

---

## 1. Workflow

```
Write → Plan → Apply → Destroy

1. Write:     Viết .tf files mô tả infrastructure
2. Init:      terraform init (tải provider plugins)
3. Plan:      terraform plan (preview thay đổi)
4. Apply:     terraform apply (tạo/sửa resources)
5. Destroy:   terraform destroy (xóa tất cả)
```

```
┌──────────────┐
│  .tf files   │ ──► terraform plan ──► Review changes
│ (desired     │                          │
│  state)      │                     terraform apply
└──────────────┘                          │
                                          ▼
┌──────────────┐                   ┌──────────────┐
│ terraform    │ ◄──── sync ─────► │ Real Cloud   │
│ .tfstate     │                   │ Infrastructure│
│ (current     │                   │ (AWS/Azure/   │
│  state)      │                   │  GCP)         │
└──────────────┘                   └──────────────┘
```

---

## 2. Cấu trúc cơ bản

```hcl
# main.tf

# Provider — cloud nào?
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state (team collaboration)
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.project}-vpc"
    Environment = var.environment
  }
}

# Subnet
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.project}-public-${count.index + 1}"
  }
}

# Security Group
resource "aws_security_group" "web" {
  name_prefix = "${var.project}-web-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = var.key_name

  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx
    EOF

  tags = {
    Name = "${var.project}-web"
  }
}
```

---

## 3. Variables & Outputs

```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "db_password" {
  type      = string
  sensitive = true    # Không hiện trong logs
}

# outputs.tf
output "web_public_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of web server"
}

output "vpc_id" {
  value = aws_vpc.main.id
}
```

```bash
# Cách truyền variables
terraform apply -var="environment=prod" -var="db_password=secret"

# Hoặc file terraform.tfvars
# terraform.tfvars (KHÔNG commit file này nếu có secrets!)
environment   = "prod"
instance_type = "t3.medium"
db_password   = "super-secret"
```

---

## 4. Modules — Tái sử dụng

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags       = { Name = "${var.name}-vpc" }
}
# ... subnets, internet gateway, route tables

# modules/vpc/variables.tf
variable "name" { type = string }
variable "cidr_block" { type = string }

# modules/vpc/outputs.tf
output "vpc_id" { value = aws_vpc.this.id }
output "subnet_ids" { value = aws_subnet.public[*].id }

# ─── Sử dụng module ───
# main.tf
module "vpc" {
  source     = "./modules/vpc"
  name       = "production"
  cidr_block = "10.0.0.0/16"
}

module "vpc_staging" {
  source     = "./modules/vpc"
  name       = "staging"
  cidr_block = "10.1.0.0/16"
}

# Dùng output của module
resource "aws_instance" "web" {
  subnet_id = module.vpc.subnet_ids[0]
}
```

---

## 5. State Management

```
terraform.tfstate = "nguồn sự thật" về infrastructure hiện tại

Local state:
  terraform.tfstate → Local file → 1 người dùng

Remote state (production): ⭐
  S3 + DynamoDB (locking) → Team cùng dùng → Không conflict

terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/terraform.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "tf-locks"      # State locking
    encrypt        = true
  }
}
```

```bash
# Lệnh state
terraform state list                    # Liệt kê resources
terraform state show aws_instance.web   # Chi tiết 1 resource
terraform state rm aws_instance.old     # Xóa khỏi state (không xóa thật)
terraform import aws_instance.web i-0123456   # Import resource có sẵn
```

---

## 6. Lệnh Terraform

```bash
terraform init             # Tải providers, khởi tạo backend
terraform plan             # Preview thay đổi (+ tạo, ~ sửa, - xóa)
terraform apply            # Áp dụng thay đổi
terraform apply -auto-approve  # Không hỏi xác nhận
terraform destroy          # Xóa TẤT CẢ resources
terraform fmt              # Format code
terraform validate         # Kiểm tra syntax
terraform output           # Xem outputs
terraform graph            # Tạo dependency graph
```

---

## 7. Project Structure

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── vpc/
│   ├── ec2/
│   ├── rds/
│   └── s3/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
└── .gitignore          # *.tfstate, *.tfvars (secrets)
```

---

## Terraform vs CloudFormation vs Pulumi

| | Terraform | CloudFormation | Pulumi |
|---|---|---|---|
| **Language** | HCL | JSON/YAML | Python/TS/Go |
| **Cloud** | Multi-cloud ⭐ | AWS only | Multi-cloud |
| **State** | File-based | AWS-managed | Pulumi Cloud |
| **Maturity** | Rất cao | Rất cao | Đang phát triển |
| **Learning** | Trung bình | Trung bình | Thấp (ngôn ngữ quen) |

---

## Các lỗi thường gặp

```
❌ Sai: Commit terraform.tfstate vào Git → lộ secrets
✅ Đúng: Remote state (S3) + .gitignore có *.tfstate

❌ Sai: terraform apply không plan trước
✅ Đúng: LUÔN terraform plan trước → review → apply

❌ Sai: Sửa resource thủ công trên Console → state drift
✅ Đúng: MỌI thay đổi qua Terraform code
```

---

## Bài tập thực hành

- [ ] Tạo VPC + EC2 + Security Group trên AWS Free Tier
- [ ] Dùng modules: tách VPC module, EC2 module riêng
- [ ] Setup remote state trên S3 + DynamoDB locking
- [ ] Tạo 2 environments (dev, prod) dùng cùng modules

---

## Tài nguyên thêm

- [Terraform Docs](https://developer.hashicorp.com/terraform/docs) — Official
- [Terraform Registry](https://registry.terraform.io/) — Modules & Providers
- [Learn Terraform (HashiCorp)](https://developer.hashicorp.com/terraform/tutorials) — Free tutorials
