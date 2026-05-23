# 🏗️ Terraform nâng cao — Modules, State & Production

> `[INTERMEDIATE → ADVANCED]` — Infrastructure as Code cho production

---

## 1. Modules — Code tái sử dụng

```
Cấu trúc project:
terraform/
├── main.tf              ← Root module
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── rds/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── prod.tfvars
```

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(var.common_tags, {
    Name = "${var.project}-${var.environment}-vpc"
  })
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.azs[count.index]

  map_public_ip_on_launch = true

  tags = merge(var.common_tags, {
    Name = "${var.project}-${var.environment}-public-${count.index + 1}"
    Type = "public"
  })
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.azs[count.index]

  tags = merge(var.common_tags, {
    Name = "${var.project}-${var.environment}-private-${count.index + 1}"
    Type = "private"
  })
}

# modules/vpc/variables.tf
variable "cidr_block" { type = string }
variable "public_subnets" { type = list(string) }
variable "private_subnets" { type = list(string) }
variable "azs" { type = list(string) }
variable "project" { type = string }
variable "environment" { type = string }
variable "common_tags" { type = map(string) default = {} }

# modules/vpc/outputs.tf
output "vpc_id" { value = aws_vpc.main.id }
output "public_subnet_ids" { value = aws_subnet.public[*].id }
output "private_subnet_ids" { value = aws_subnet.private[*].id }

# Root main.tf — Sử dụng module
module "vpc" {
  source = "./modules/vpc"

  cidr_block      = "10.0.0.0/16"
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.10.0/24", "10.0.11.0/24"]
  azs             = ["ap-southeast-1a", "ap-southeast-1b"]
  project         = var.project
  environment     = var.environment
  common_tags     = local.common_tags
}

module "rds" {
  source = "./modules/rds"

  vpc_id     = module.vpc.vpc_id          # Output từ module vpc!
  subnet_ids = module.vpc.private_subnet_ids
  # ...
}
```

---

## 2. State Management — Remote Backend

```hcl
# backend.tf — Lưu state trên S3 (team collaboration)
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "prod/infrastructure.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "terraform-locks"    # State locking!
    encrypt        = true
  }
}

# Tạo S3 + DynamoDB cho backend (bootstrap 1 lần)
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mycompany-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"    # Giữ history state → rollback nếu cần
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

### State Commands

```bash
# Xem state hiện tại
terraform state list
terraform state show aws_instance.web

# Import resource có sẵn vào Terraform quản lý
terraform import aws_instance.web i-1234567890

# Move resource (refactor)
terraform state mv aws_instance.old module.compute.aws_instance.new

# Remove resource khỏi state (Terraform không quản lý nữa)
terraform state rm aws_instance.temp
```

---

## 3. Workspaces — Multi-environment

```bash
# Mỗi workspace = 1 state file riêng biệt
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

terraform workspace select prod
terraform workspace list
```

```hcl
# Dùng workspace trong code
locals {
  environment = terraform.workspace

  instance_type = {
    dev     = "t3.micro"
    staging = "t3.small"
    prod    = "t3.medium"
  }

  instance_count = {
    dev     = 1
    staging = 2
    prod    = 3
  }
}

resource "aws_instance" "web" {
  count         = local.instance_count[local.environment]
  instance_type = local.instance_type[local.environment]
  ami           = var.ami_id

  tags = {
    Name        = "web-${local.environment}-${count.index + 1}"
    Environment = local.environment
  }
}
```

---

## 4. Advanced Patterns

### for_each vs count

```hcl
# count: dùng cho list đơn giản
resource "aws_subnet" "public" {
  count      = 3
  cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index)
}

# for_each: dùng cho map (stable, không bị reorder!)
resource "aws_iam_user" "developers" {
  for_each = toset(["an", "binh", "cuong"])
  name     = each.value
}
# aws_iam_user.developers["an"]
# aws_iam_user.developers["binh"]
# → Xóa "binh" không ảnh hưởng "cuong" (khác count!)
```

### Dynamic blocks

```hcl
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = module.vpc.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
}

variable "ingress_rules" {
  default = [
    { port = 80,  cidr_blocks = ["0.0.0.0/0"], description = "HTTP" },
    { port = 443, cidr_blocks = ["0.0.0.0/0"], description = "HTTPS" },
    { port = 22,  cidr_blocks = ["10.0.0.0/8"], description = "SSH internal" },
  ]
}
```

### Lifecycle rules

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = "t3.medium"

  lifecycle {
    create_before_destroy = true   # Tạo mới trước khi xóa cũ
    prevent_destroy       = true   # Chặn terraform destroy
    ignore_changes        = [tags]  # Không track changes cho tags
  }
}
```

---

## 5. CI/CD cho Terraform

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  pull_request:
    paths: ['terraform/**']
  push:
    branches: [main]
    paths: ['terraform/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Init
        run: terraform init
        working-directory: terraform

      - name: Validate
        run: terraform validate
        working-directory: terraform

      - name: Plan
        run: terraform plan -out=tfplan
        working-directory: terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            // Post plan output as PR comment

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production    # Requires approval!
    steps:
      - name: Apply
        run: terraform apply -auto-approve tfplan
```

---

## Các lỗi thường gặp

```
❌ Sai: terraform apply trên local cho production
✅ Đúng: CI/CD pipeline + approval gates

❌ Sai: Hardcode secrets trong .tf files
✅ Đúng: Dùng variables + tfvars (gitignored) hoặc Vault

❌ Sai: 1 state file chứa MỌI resources
✅ Đúng: Tách state theo component (vpc, eks, rds) → giảm blast radius
```

---

## Bài tập thực hành

- [ ] Module: VPC + Subnets + Security Groups tái sử dụng
- [ ] Remote backend: S3 + DynamoDB state locking
- [ ] Multi-env: dev/staging/prod với workspaces hoặc tfvars
- [ ] CI/CD: GitHub Actions plan on PR, apply on merge

---

## Tài nguyên thêm

- [Terraform Docs](https://developer.hashicorp.com/terraform/docs) — Official
- [Terraform Best Practices](https://www.terraform-best-practices.com/) — Community
- [Terraform Registry](https://registry.terraform.io/) — Modules & Providers
