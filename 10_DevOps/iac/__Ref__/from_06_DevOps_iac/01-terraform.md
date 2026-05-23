# 🏗️ Infrastructure as Code — Terraform

> `[INTERMEDIATE → ADVANCED]` — Quản lý hạ tầng bằng code, không bằng click

---

## IaC là gì?

**Infrastructure as Code (IaC)** — Định nghĩa và quản lý hạ tầng (servers, databases, networks...) thông qua **code** thay vì giao diện đồ họa.

**Lợi ích:**
- **Reproducible** — Tạo lại hạ tầng giống hệt nhau mọi lúc
- **Version control** — Track thay đổi hạ tầng như track code
- **Automation** — CI/CD cho cả infrastructure
- **Documentation as code** — Code chính là tài liệu

**Công cụ phổ biến:**
| Tool | Approach | Provider |
|---|---|---|
| **Terraform** | Declarative | Multi-cloud (AWS/Azure/GCP/...) |
| **Pulumi** | Imperative (dùng code thật) | Multi-cloud |
| **AWS CDK** | Imperative | AWS only |
| **Ansible** | Procedural | Configuration management |

---

## Terraform Cơ bản

### Cài đặt

```bash
# macOS
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Kiểm tra
terraform version
```

### Cấu trúc project

```
infrastructure/
├── main.tf           # Resources chính
├── variables.tf      # Khai báo variables
├── outputs.tf        # Outputs
├── providers.tf      # Provider configuration
├── terraform.tfvars  # Giá trị của variables (không commit!)
├── .terraform/       # Cache, plugins (không commit!)
└── terraform.tfstate # State file (quan trọng, backup!)
```

---

## Cú pháp Terraform (HCL)

```hcl
# providers.tf
terraform {
  required_version = ">= 1.6"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state (khuyên dùng cho team)
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

provider "aws" {
  region = var.aws_region
}
```

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
    error_message = "Environment phải là dev, staging hoặc prod."
  }
}

variable "app_name" {
  type = string
}

variable "database_password" {
  type      = string
  sensitive = true  # Không hiện trong logs
}
```

```hcl
# main.tf — Ví dụ AWS
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.app_name
    ManagedBy   = "terraform"
  }
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(local.common_tags, {
    Name = "${var.app_name}-vpc"
  })
}

# Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name = "${var.app_name}-public-${count.index + 1}"
  })
}

# Security Group
resource "aws_security_group" "api" {
  name        = "${var.app_name}-api-sg"
  description = "Security group for API servers"
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

  tags = local.common_tags
}

# EC2 Instance
resource "aws_instance" "api" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small"
  subnet_id     = aws_subnet.public[0].id
  
  vpc_security_group_ids = [aws_security_group.api.id]
  key_name               = aws_key_pair.deployer.key_name

  user_data = base64encode(templatefile("${path.module}/scripts/init.sh", {
    app_name = var.app_name
  }))

  tags = merge(local.common_tags, {
    Name = "${var.app_name}-api"
  })
}

# RDS PostgreSQL
resource "aws_db_instance" "main" {
  identifier        = "${var.app_name}-db"
  engine            = "postgres"
  engine_version    = "16.1"
  instance_class    = "db.t3.micro"
  
  allocated_storage    = 20
  max_allocated_storage = 100  # Auto scaling

  db_name  = var.app_name
  username = "postgres"
  password = var.database_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  skip_final_snapshot     = var.environment != "prod"
  deletion_protection     = var.environment == "prod"

  tags = local.common_tags
}
```

```hcl
# outputs.tf
output "api_public_ip" {
  description = "Public IP của API server"
  value       = aws_instance.api.public_ip
}

output "database_endpoint" {
  description = "Database connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "vpc_id" {
  value = aws_vpc.main.id
}
```

---

## Lệnh Terraform

```bash
# Khởi tạo (tải providers)
terraform init

# Xem kế hoạch thay đổi (không apply)
terraform plan

# Plan với var file
terraform plan -var-file="prod.tfvars"

# Apply thay đổi
terraform apply

# Apply không cần confirm (CI/CD)
terraform apply -auto-approve

# Xem resources đang quản lý
terraform show
terraform state list

# Import resource đã tồn tại
terraform import aws_s3_bucket.my_bucket my-existing-bucket

# Xóa toàn bộ hạ tầng (⚠️ cẩn thận!)
terraform destroy

# Format code
terraform fmt

# Validate syntax
terraform validate
```

---

## Modules — Tái sử dụng code

```hcl
# modules/ec2-instance/main.tf
variable "name" { type = string }
variable "instance_type" { type = string; default = "t3.micro" }
variable "subnet_id" { type = string }

resource "aws_instance" "this" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  tags = { Name = var.name }
}

output "id" { value = aws_instance.this.id }
output "public_ip" { value = aws_instance.this.public_ip }
```

```hcl
# Dùng module
module "api_server" {
  source         = "./modules/ec2-instance"
  name           = "api-prod"
  instance_type  = "t3.small"
  subnet_id      = aws_subnet.public[0].id
}

module "worker_server" {
  source         = "./modules/ec2-instance"
  name           = "worker-prod"
  instance_type  = "t3.medium"
  subnet_id      = aws_subnet.private[0].id
}

# Dùng module từ Terraform Registry
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.5.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["ap-southeast-1a", "ap-southeast-1b"]
}
```

---

## Workspaces — Multiple environments

```bash
# Tạo workspace
terraform workspace new staging
terraform workspace new prod

# Chuyển workspace
terraform workspace select prod
terraform workspace list

# Dùng trong code
locals {
  env_configs = {
    dev     = { instance_type = "t3.micro",  db_class = "db.t3.micro" }
    staging = { instance_type = "t3.small",  db_class = "db.t3.small" }
    prod    = { instance_type = "t3.medium", db_class = "db.t3.medium" }
  }
  
  config = local.env_configs[terraform.workspace]
}

resource "aws_instance" "api" {
  instance_type = local.config.instance_type
}
```

---

## Ansible — Configuration Management

```yaml
# playbook.yml — Cài đặt và cấu hình server
---
- name: Setup API Server
  hosts: api_servers
  become: true  # sudo

  vars:
    app_user: appuser
    app_dir: /opt/my-app
    node_version: "20"

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install required packages
      apt:
        name:
          - curl
          - git
          - nginx
        state: present

    - name: Install Node.js
      shell: |
        curl -fsSL https://deb.nodesource.com/setup_{{ node_version }}.x | bash -
        apt-get install -y nodejs

    - name: Create app user
      user:
        name: "{{ app_user }}"
        create_home: yes
        shell: /bin/bash

    - name: Create app directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_user }}"

    - name: Configure Nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/my-app
      notify: Reload Nginx

    - name: Enable site
      file:
        src: /etc/nginx/sites-available/my-app
        dest: /etc/nginx/sites-enabled/my-app
        state: link

  handlers:
    - name: Reload Nginx
      service:
        name: nginx
        state: reloaded
```

```bash
# Chạy playbook
ansible-playbook -i inventory.yml playbook.yml
ansible-playbook -i inventory.yml playbook.yml --check  # Dry run
ansible-playbook -i inventory.yml playbook.yml --tags "nginx"
```

---

## Bài tập thực hành

- [ ] Provision VPC + EC2 + RDS trên AWS bằng Terraform
- [ ] Tạo module tái sử dụng cho web server
- [ ] Dùng Terraform workspace cho dev/staging/prod
- [ ] Viết Ansible playbook cài đặt và cấu hình Nginx + Node.js

---

## Tài nguyên thêm

- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry](https://registry.terraform.io/) — Modules sẵn có
- [Terragrunt](https://terragrunt.gruntwork.io/) — Wrapper giúp DRY Terraform
- [Ansible Docs](https://docs.ansible.com/)
