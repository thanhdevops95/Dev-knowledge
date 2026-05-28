# 🏗️ Module 3.5: Terraform IaC

[![Duration](https://img.shields.io/badge/Duration-2%20weeks-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Infrastructure as Code** - Manage infrastructure with Terraform.
>
> *Infrastructure as Code - Quản lý hạ tầng với Terraform.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand Terraform workflow (Hiểu quy trình Terraform)
- ✅ Master HCL syntax (Thành thạo cú pháp HCL)
- ✅ Work with Providers and resources (Làm việc với Providers và resources)
- ✅ Manage Terraform state (Quản lý state)
- ✅ Create reusable modules (Tạo modules tái sử dụng)
- ✅ Use workspaces for environments (Sử dụng workspaces cho các môi trường)
- ✅ Integrate Terraform with CI/CD (Tích hợp Terraform với CI/CD)

---

## 📋 Prerequisites (Điều kiện tiên quyết)

- Complete Module 3.1-3.4 (Hoàn thành Module 3.1-3.4)
- AWS account with Free Tier (Tài khoản AWS với Free Tier)
- Familiar with AWS services (Quen với các dịch vụ AWS)

---

## 📚 Content (Nội dung)

### 1. What is Terraform? (Terraform là gì?)

**Terraform** is an Infrastructure as Code (IaC) tool that allows you to build, change, and version infrastructure safely and efficiently.

*Terraform là công cụ Infrastructure as Code (IaC) cho phép bạn xây dựng, thay đổi và quản lý phiên bản hạ tầng một cách an toàn và hiệu quả.*

#### Why Terraform? (Tại sao Terraform?)

**Problem:** Creating infrastructure manually (clicking console) cannot be tracked, rolled back, or verified.

*Tạo infrastructure bằng tay (click console) không thể tracking, không thể rollback, dễ sai.*

| Manual (Click Console) | Terraform (IaC) |
|------------------------|-----------------|
| ❌ Không có version history | ✅ Git versioning |
| ❌ Mỗi người làm một kiểu | ✅ Consistent, reproducible |
| ❌ Không biết đã thay đổi gì | ✅ `terraform plan` xem trước thay đổi |
| ❌ Rollback = làm lại từ đầu | ✅ `terraform apply` phiên bản cũ |
| ❌ Không thể review | ✅ Code review như application code |

#### Terraform Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    TERRAFORM WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. WRITE          2. PLAN           3. APPLY              │
│   ┌─────────┐      ┌─────────┐       ┌─────────┐           │
│   │  .tf    │ ───► │terraform│ ───── │terraform│ ───►      │
│   │  files  │      │  plan   │       │  apply  │           │
│   └─────────┘      └─────────┘       └─────────┘           │
│                         │                   │               │
│                         ▼                   ▼               │
│                    Preview             Create/Update        │
│                    changes             resources            │
│                                             │               │
│                                             ▼               │
│                                      ┌─────────────┐       │
│                                      │   State     │       │
│                                      │   (.tfstate)│       │
│                                      └─────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key concepts (Khái niệm chính):**

- **Infrastructure as Code**: Define infrastructure in config files (Định nghĩa hạ tầng bằng code).
- **Execution Plans**: Preview changes before applying (Xem trước thay đổi trước khi áp dụng).
- **Resource Graph**: Builds dependency graph (Xây dựng đồ thị phụ thuộc).
- **State**: Terraform lưu trạng thái thực tế của infrastructure để so sánh với code.

### 2. Basic Structure (Cấu trúc cơ bản)

A typical Terraform project has these main blocks. Here's a complete example:

*Một project Terraform điển hình có các blocks chính sau. Dưới đây là ví dụ đầy đủ:*

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Remote state (recommended for teams)
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
  
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = "t3.micro"
  
  tags = {
    Name = "web-server"
  }
}
```

---

### 3. Variables (Biến)

```hcl
# variables.tf
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "ami_id" {
  description = "AMI ID for EC2 instance"
  type        = string
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 1
}
```

```hcl
# terraform.tfvars
region      = "us-west-2"
environment = "prod"
ami_id      = "ami-xxx"
```

---

### 4. Outputs (Đầu ra)

```hcl
# outputs.tf
output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.web.id
}

output "instance_ip" {
  description = "EC2 public IP"
  value       = aws_instance.web.public_ip
}

output "instance_dns" {
  description = "EC2 public DNS"
  value       = aws_instance.web.public_dns
}
```

---

### 5. Commands (Các lệnh)

```bash
# Initialize (Khởi tạo)
terraform init

# Format code (Định dạng code)
terraform fmt

# Validate configuration (Xác thực cấu hình)
terraform validate

# Preview changes (Xem trước thay đổi)
terraform plan
terraform plan -out=tfplan    # Save plan

# Apply changes (Áp dụng thay đổi)
terraform apply
terraform apply tfplan        # Apply saved plan
terraform apply -auto-approve # Skip confirmation (use with caution!)

# Destroy infrastructure (Hủy hạ tầng)
terraform destroy

# State management (Quản lý state)
terraform state list          # List resources
terraform state show <resource>
terraform state rm <resource> # Remove from state
```

---

### 6. Modules

#### Using Public Modules (Sử dụng modules công khai)

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
}
```

#### Creating Your Own Module (Tạo module của riêng bạn)

```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── ec2/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

```hcl
# modules/ec2/main.tf
resource "aws_instance" "this" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  
  tags = var.tags
}

# Usage in root module
module "web_server" {
  source = "./modules/ec2"
  
  ami_id        = "ami-xxx"
  instance_type = "t3.micro"
  subnet_id     = module.vpc.private_subnets[0]
  tags          = { Name = "web-server" }
}
```

---

### 7. Terraform with GitLab CI (Terraform với GitLab CI)

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - apply

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform

before_script:
  - cd ${TF_ROOT}
  - terraform init

validate:
  stage: validate
  image: hashicorp/terraform:latest
  script:
    - terraform fmt -check
    - terraform validate

plan:
  stage: plan
  image: hashicorp/terraform:latest
  script:
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - ${TF_ROOT}/tfplan

apply:
  stage: apply
  image: hashicorp/terraform:latest
  script:
    - terraform apply -auto-approve tfplan
  dependencies:
    - plan
  when: manual
  only:
    - main
```

---

### 8. Best Practices (Best Practices)

| Practice | Description (Mô tả) |
|----------|---------------------|
| **Remote State** | Store state in S3/GCS, not locally (Lưu state trên S3/GCS, không lưu local) |
| **State Locking** | Use DynamoDB for state locking (Dùng DynamoDB để khóa state) |
| **Modules** | Create reusable modules (Tạo modules tái sử dụng) |
| **Workspaces** | Separate environments via workspaces (Phân tách môi trường qua workspaces) |
| **Variables** | Never hardcode values (Không hardcode giá trị) |
| **Outputs** | Export useful values (Xuất các giá trị hữu ích) |
| **Formatting** | Run `terraform fmt` before commit (Chạy lệnh fmt trước khi commit) |
| **Validation** | Run in CI pipeline (Chạy validate trong CI pipeline) |

---

## 📖 Resources (Tài liệu tham khảo)

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Terraform Associate Certification](https://www.hashicorp.com/certification/terraform-associate)

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [3.4 Ansible](../3.4_Config_Management_Ansible/) | **3.5 Terraform** | [3.6 System Design](../3.6_System_Design_Reliability/) |

---

**Master Infrastructure as Code! 🏗️**

*Thành thạo Infrastructure as Code!*

</div>
