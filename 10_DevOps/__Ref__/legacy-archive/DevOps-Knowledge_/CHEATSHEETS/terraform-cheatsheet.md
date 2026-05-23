# Terraform Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Terraform commands and syntax for quick reference -- Lệnh và cú pháp Terraform để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [CLI Commands](#cli-commands) -- Lệnh CLI
- [State Management](#state-management) -- Quản lý State
- [Workspaces](#workspaces) -- Workspaces
- [Configuration Syntax](#configuration-syntax) -- Cú pháp Cấu hình
- [Variables & Outputs](#variables--outputs) -- Variables và Outputs
- [Data Sources](#data-sources) -- Data Sources
- [Modules](#modules) -- Modules
- [Provisioners](#provisioners) -- Provisioners
- [Backend Configuration](#backend-configuration) -- Cấu hình Backend
- [Common Patterns](#common-patterns) -- Patterns Thường dùng

## <a id="cli-commands"></a> CLI Commands -- Lệnh CLI

```bash
# Initialize -- Khởi tạo
terraform init                          # Initialize working directory -- Khởi tạo thư mục làm việc
terraform init -upgrade                 # Upgrade providers -- Nâng cấp providers
terraform init -backend-config=backend.hcl  # With backend config -- Với cấu hình backend
terraform init -reconfigure            # Reconfigure backend -- Cấu hình lại backend

# Plan -- Lập kế hoạch
terraform plan                          # Show execution plan -- Hiển thị kế hoạch thực thi
terraform plan -out=plan.tfplan         # Save plan to file -- Lưu plan vào file
terraform plan -var="key=value"         # With variable -- Với biến
terraform plan -var-file=vars.tfvars    # With variable file -- Với file biến
terraform plan -target=resource.name    # Target specific resource -- Nhắm resource cụ thể
terraform plan -destroy                 # Plan for destruction -- Lập kế hoạch hủy

# Apply -- Áp dụng
terraform apply                         # Apply changes -- Áp dụng thay đổi
terraform apply plan.tfplan            # Apply saved plan -- Áp dụng plan đã lưu
terraform apply -auto-approve          # Skip approval prompt -- Bỏ qua xác nhận
terraform apply -var="key=value"       # With variable -- Với biến
terraform apply -target=resource.name   # Target specific resource -- Nhắm resource cụ thể

# Destroy -- Hủy
terraform destroy                       # Destroy all resources -- Hủy tất cả resources
terraform destroy -auto-approve         # Skip approval prompt -- Bỏ qua xác nhận
terraform destroy -target=resource.name # Destroy specific resource -- Hủy resource cụ thể

# Validate & Format -- Kiểm tra và Định dạng
terraform validate                      # Validate configuration -- Kiểm tra cấu hình
terraform fmt                           # Format configuration -- Định dạng cấu hình
terraform fmt -check                    # Check formatting -- Kiểm tra định dạng
terraform fmt -recursive                # Format recursively -- Định dạng đệ quy

# Show & Output -- Hiển thị và Output
terraform show                          # Show current state -- Hiển thị state hiện tại
terraform show plan.tfplan             # Show saved plan -- Hiển thị plan đã lưu
terraform output                        # Show outputs -- Hiển thị outputs
terraform output output_name           # Show specific output -- Hiển thị output cụ thể
terraform output -json                 # JSON format -- Định dạng JSON

# Providers -- Providers
terraform providers                     # List providers -- Liệt kê providers
terraform providers lock               # Lock provider versions -- Khóa phiên bản provider
terraform version                      # Show version -- Hiển thị phiên bản
```

## <a id="state-management"></a> State Management -- Quản lý State

```bash
# State list -- Liệt kê state
terraform state list                    # List all resources in state -- Liệt kê tất cả resources trong state
terraform state list 'aws_instance.*'   # Filter resources -- Lọc resources

# State show -- Hiển thị state
terraform state show resource.name      # Show resource details -- Hiển thị chi tiết resource

# State move -- Di chuyển state
terraform state mv old.name new.name    # Rename resource -- Đổi tên resource
terraform state mv -state-out=new.tfstate resource.name resource.name  # Move to different state -- Di chuyển sang state khác

# State remove -- Xóa khỏi state
terraform state rm resource.name        # Remove from state (not destroy) -- Xóa khỏi state (không hủy)

# State pull/push -- Pull/Push state
terraform state pull                    # Get current state -- Lấy state hiện tại
terraform state push state.tfstate      # Push state -- Push state

# State replace -- Thay thế state
terraform state replace-provider old new  # Replace provider -- Thay thế provider

# Import existing resources -- Import resources có sẵn
terraform import resource.name id       # Import resource -- Import resource
terraform import aws_instance.web i-1234567890abcdef0  # Example -- Ví dụ

# Refresh -- Làm mới
terraform refresh                       # Refresh state -- Làm mới state
terraform apply -refresh-only          # Refresh only (recommended) -- Chỉ làm mới (khuyến nghị)
```

## <a id="workspaces"></a> Workspaces

```bash
# List workspaces -- Liệt kê workspaces
terraform workspace list               # List all workspaces -- Liệt kê tất cả workspaces

# Create workspace -- Tạo workspace
terraform workspace new dev            # Create new workspace -- Tạo workspace mới

# Select workspace -- Chọn workspace
terraform workspace select dev         # Switch to workspace -- Chuyển sang workspace
terraform workspace show               # Show current workspace -- Hiển thị workspace hiện tại

# Delete workspace -- Xóa workspace
terraform workspace delete dev         # Delete workspace -- Xóa workspace

# Use in configuration -- Sử dụng trong cấu hình
# ${terraform.workspace} returns current workspace name
# -- ${terraform.workspace} trả về tên workspace hiện tại
```

## <a id="configuration-syntax"></a> Configuration Syntax -- Cú pháp Cấu hình

```hcl
# Provider configuration -- Cấu hình provider
provider "aws" {
  region  = "us-west-2"
  profile = "default"
}

# Resource definition -- Định nghĩa resource
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
    Environment = "Production"
  }
}

# Resource with count -- Resource với count
resource "aws_instance" "server" {
  count         = 3
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  tags = {
    Name = "Server-${count.index}"  # Index: 0, 1, 2
  }
}

# Resource with for_each -- Resource với for_each
resource "aws_instance" "server" {
  for_each      = toset(["web", "api", "db"])
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  tags = {
    Name = each.key  # "web", "api", "db"
  }
}

# Depends on -- Phụ thuộc
resource "aws_eip" "ip" {
  instance   = aws_instance.web.id
  depends_on = [aws_internet_gateway.gw]
}

# Lifecycle rules -- Quy tắc vòng đời
resource "aws_instance" "web" {
  # ... config ...

  lifecycle {
    create_before_destroy = true   # Create new before destroying old -- Tạo mới trước khi hủy cũ
    prevent_destroy       = true   # Prevent destruction -- Ngăn hủy
    ignore_changes        = [tags] # Ignore changes -- Bỏ qua thay đổi
  }
}
```

## <a id="variables--outputs"></a> Variables & Outputs -- Variables và Outputs

```hcl
# Variable definition (variables.tf) -- Định nghĩa biến
variable "instance_type" {
  description = "EC2 instance type"  # Mô tả
  type        = string
  default     = "t2.micro"
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 1
}

variable "enable_monitoring" {
  description = "Enable monitoring"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

variable "availability_zones" {
  description = "List of AZs"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}

variable "database_config" {
  description = "Database configuration"
  type = object({
    engine  = string
    version = string
    size    = number
  })
}

# Sensitive variable -- Biến nhạy cảm
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Variable validation -- Kiểm tra biến
variable "instance_type" {
  type = string
  validation {
    condition     = contains(["t2.micro", "t2.small"], var.instance_type)
    error_message = "Must be t2.micro or t2.small"
  }
}

# Using variables -- Sử dụng biến
resource "aws_instance" "web" {
  instance_type = var.instance_type
  count         = var.instance_count
}

# Output definition (outputs.tf) -- Định nghĩa output
output "instance_ip" {
  description = "Public IP of instance"
  value       = aws_instance.web.public_ip
}

output "instance_ids" {
  description = "List of instance IDs"
  value       = aws_instance.server[*].id  # Splat expression
}

output "db_password" {
  value     = var.db_password
  sensitive = true  # Hide in output -- Ẩn trong output
}
```

```bash
# Setting variables -- Đặt biến
# terraform.tfvars (auto-loaded) -- Tự động tải
instance_type = "t2.small"
instance_count = 3

# Command line -- Dòng lệnh
terraform apply -var="instance_type=t2.small"
terraform apply -var-file="prod.tfvars"

# Environment variables -- Biến môi trường
export TF_VAR_instance_type="t2.small"
```

## <a id="data-sources"></a> Data Sources

```hcl
# Data source - query existing resources -- Truy vấn resources có sẵn
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Using data source -- Sử dụng data source
resource "aws_instance" "web" {
  ami = data.aws_ami.ubuntu.id
}

# Other common data sources -- Các data source thường dùng
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "vpc/terraform.tfstate"
    region = "us-west-2"
  }
}
```

## <a id="modules"></a> Modules

```hcl
# Call a module -- Gọi module
module "vpc" {
  source  = "./modules/vpc"        # Local module -- Module local
  # source = "git::https://github.com/user/repo.git"  # Git module
  # source = "hashicorp/vpc/aws"   # Registry module

  vpc_cidr = "10.0.0.0/16"
  environment = "production"
}

# Module with version -- Module với phiên bản
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.0.0"
  # ... variables ...
}

# Access module outputs -- Truy cập outputs của module
resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnets[0]
}

# Module structure -- Cấu trúc module
# modules/vpc/
#   main.tf        # Main resources -- Resources chính
#   variables.tf   # Input variables -- Biến đầu vào
#   outputs.tf     # Output values -- Giá trị đầu ra
#   versions.tf    # Provider versions -- Phiên bản provider
```

```bash
# Module commands -- Lệnh module
terraform get                          # Download modules -- Tải modules
terraform get -update                  # Update modules -- Cập nhật modules
```

## <a id="provisioners"></a> Provisioners

```hcl
# Local-exec provisioner -- Provisioner local-exec
resource "aws_instance" "web" {
  # ...

  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> hosts.txt"
  }
}

# Remote-exec provisioner -- Provisioner remote-exec
resource "aws_instance" "web" {
  # ...

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}

# File provisioner -- Provisioner file
provisioner "file" {
  source      = "conf/app.conf"
  destination = "/etc/app.conf"
}

# On destroy -- Khi hủy
provisioner "local-exec" {
  when    = destroy
  command = "echo 'Destroying ${self.id}'"
}

# On failure -- Khi thất bại
provisioner "local-exec" {
  on_failure = continue  # or fail -- hoặc fail
  command    = "might_fail.sh"
}
```

## <a id="backend-configuration"></a> Backend Configuration -- Cấu hình Backend

```hcl
# S3 backend -- Backend S3
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Local backend (default) -- Backend local (mặc định)
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# Partial configuration -- Cấu hình một phần
terraform {
  backend "s3" {}
}
# Then run: terraform init -backend-config=backend.hcl
# -- Sau đó chạy: terraform init -backend-config=backend.hcl
```

```hcl
# backend.hcl
bucket         = "my-terraform-state"
key            = "prod/terraform.tfstate"
region         = "us-west-2"
encrypt        = true
dynamodb_table = "terraform-locks"
```

## <a id="common-patterns"></a> Common Patterns -- Patterns Thường dùng

```hcl
# Required providers -- Providers bắt buộc
terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Conditional resource -- Resource có điều kiện
resource "aws_eip" "optional" {
  count    = var.create_eip ? 1 : 0
  instance = aws_instance.web.id
}

# Dynamic blocks -- Blocks động
resource "aws_security_group" "web" {
  name = "web-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}

# Local values -- Giá trị local
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
  
  instance_name = "${var.project}-${var.environment}-web"
}

resource "aws_instance" "web" {
  tags = merge(local.common_tags, {
    Name = local.instance_name
  })
}

# Null resource for triggers -- Null resource cho triggers
resource "null_resource" "example" {
  triggers = {
    cluster_id = aws_eks_cluster.main.id
  }

  provisioner "local-exec" {
    command = "kubectl apply -f config.yaml"
  }
}

# Terraform functions -- Hàm Terraform
# String: format(), join(), split(), replace(), trim()
# Collection: concat(), flatten(), keys(), values(), length()
# Filesystem: file(), fileexists(), templatefile()
# Type: tolist(), toset(), tomap()
# Encoding: base64encode(), jsonencode(), yamlencode()
```

---
