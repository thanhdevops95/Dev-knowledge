# 🚨 Tình huống Thực chiến - Terraform/IaC

Đây là 5 tình huống thực tế mà DevOps Engineer thường gặp khi làm việc với Infrastructure as Code.

---

## Scenario 1: Terraform State bị corrupt/mất

### 📋 Bối cảnh

Ai đó chạy `terraform apply` giữa chừng thì Ctrl+C. State file bị **corrupt**.

> "terraform plan" báo lỗi không đọc được state!

### 🔍 Triệu chứng

```bash
terraform plan
# Error: Failed to load state: [error loading state file]
# Error: state file may be corrupt
```

Hoặc state file bị xóa:

```bash
terraform plan
# Terraform will create 50 resources
# (Nhưng resources đã tồn tại trên AWS!)
```

### 🕵️ Điều tra

```bash
# Kiểm tra state file
ls -la terraform.tfstate
# Hoặc trên S3
aws s3 ls s3://mybucket/terraform/state

# Xem state backup
ls terraform.tfstate.backup
```

### 💡 Giải pháp

**1. Restore từ backup:**

```bash
# Local backup
cp terraform.tfstate.backup terraform.tfstate

# S3 versioning
aws s3api list-object-versions --bucket mybucket --prefix terraform/state
aws s3api get-object --bucket mybucket --key terraform/state \
  --version-id "abc123" terraform.tfstate
```

**2. Import resources lại:**

```bash
# Nếu không có backup, import từng resource
terraform import aws_instance.web i-1234567890abcdef0
terraform import aws_s3_bucket.data my-bucket-name
# Lặp lại cho mỗi resource...
```

**3. Remote state với locking (prevent future issues):**

```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-company"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"  # Lock để prevent concurrent writes
    encrypt        = true
  }
}
```

**4. State backup automation:**

```bash
# Cron job backup state
#!/bin/bash
aws s3 cp s3://terraform-state/prod/terraform.tfstate \
  s3://terraform-backups/prod/$(date +%Y%m%d_%H%M%S).tfstate
```

### 🧠 Bài học

- **Remote state + locking là bắt buộc** - Không dùng local state cho production
- **S3 versioning** - Enable để có backup tự động
- **Đừng Ctrl+C giữa apply** - Để Terraform hoàn thành hoặc timeout
- **terraform import** - Cách cuối cùng để recover

---

## Scenario 2: "terraform plan" looks good, "apply" destroys production

### 📋 Bối cảnh

Run `terraform plan`, output looks fine. Run `terraform apply`... **DATABASE BỊ XÓA**.

> 3 năm data, mất trong 1 giây

### 🔍 Triệu chứng

```
terraform plan
# ~ aws_db_instance.prod will be updated in-place
#     name: "prod-db" -> "prod-database"

terraform apply
# aws_db_instance.prod: Destroying...
# WHAT?!
```

### 🕵️ Điều tra

```bash
# Terraform thấy: đổi tên = xóa + tạo mới
# Một số attributes force replacement:
# - Tên database
# - Engine version (một số trường hợp)
# - Availability zone
```

### 💡 Giải pháp

**1. ĐỌC KỸ plan output:**

```
# Xem kỹ các ký hiệu
+ create
- destroy
~ update in-place
-/+ destroy and recreate  ← NGUY HIỂM!
```

**2. lifecycle prevent_destroy:**

```hcl
resource "aws_db_instance" "prod" {
  # ...
  
  lifecycle {
    prevent_destroy = true  # Terraform sẽ error nếu cố xóa
  }
}
```

**3. Backup trước khi apply:**

```bash
# Script pre-apply
#!/bin/bash
echo "Creating RDS snapshot before apply..."
aws rds create-db-snapshot \
  --db-instance-identifier prod-db \
  --db-snapshot-identifier "pre-terraform-$(date +%Y%m%d_%H%M%S)"

terraform apply
```

**4. terraform plan -out:**

```bash
# Save plan để review
terraform plan -out=plan.tfplan

# Review kỹ
terraform show plan.tfplan

# Apply chính xác plan đã review
terraform apply plan.tfplan
```

**5. Approval workflow:**

```yaml
# CI/CD với approval
- name: Terraform Plan
  run: terraform plan -out=plan.tfplan

- name: Wait for approval
  uses: trstringer/manual-approval@v1
  with:
    approvers: infra-team

- name: Terraform Apply
  run: terraform apply plan.tfplan
```

### 🧠 Bài học

- **Plan ≠ thực sự an toàn** - Đọc kỹ destroy/recreate
- **prevent_destroy cho critical resources** - Database, S3 buckets
- **Backup trước apply** - Đặc biệt cho stateful resources
- **Approval workflow** - Human review cho production

---

## Scenario 3: Drift - Infrastructure khác với Terraform state

### 📋 Bối cảnh

Ai đó vào AWS Console edit security group **thủ công**. Terraform không biết.

> terraform plan: No changes. Infrastructure is up-to-date.
> Thực tế: Security group đã khác!

### 🔍 Triệu chứng

```bash
terraform plan
# No changes. Infrastructure is up-to-date.

# Nhưng trên AWS Console:
# Security group có rule mới mà Terraform không định nghĩa
```

### 🕵️ Điều tra

```bash
# Refresh state từ actual infrastructure
terraform refresh

terraform plan
# ~ aws_security_group.web will be updated
#     - ingress.rule[2] will be removed  ← Ai đã thêm rule này?
```

### 💡 Giải pháp

**1. Detect drift định kỳ:**

```bash
# Cron job detect drift
terraform plan -detailed-exitcode
# Exit code 2 = changes detected
```

**2. Import changes vào Terraform:**

```hcl
# Nếu rule manual là cần thiết, add vào code
resource "aws_security_group" "web" {
  # ...
  ingress {
    from_port   = 8080  # Rule mới
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
}
```

**3. Policy as Code - Prevent manual changes:**

```hcl
# AWS Service Control Policy
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": ["ec2:AuthorizeSecurityGroupIngress"],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": "arn:aws:iam::*:role/TerraformRole"
        }
      }
    }
  ]
}
```

**4. Drift detection tools:**

```bash
# Driftctl
driftctl scan

# Output:
# Found 3 resource(s)
# - 1 covered by IaC
# - 2 not covered by IaC  ← Manual resources!
```

### 🧠 Bài học

- **Manual changes = drift** - Terraform không biết
- **Detect drift định kỳ** - Trước khi apply
- **Lock down console access** - Hoặc ít nhất alert
- **Everything in code** - Kể cả "quick fixes"

---

## Scenario 4: Circular dependency - Terraform error

### 📋 Bối cảnh

Terraform plan báo:
> Error: Cycle detected in resource dependencies

Không hiểu dependency nào đang circular.

### 🔍 Triệu chứng

```bash
terraform plan
# Error: Cycle:
#   aws_security_group.app
#   aws_security_group.db
```

### 🕵️ Điều tra

```hcl
# app.tf
resource "aws_security_group" "app" {
  ingress {
    security_groups = [aws_security_group.db.id]  # Depends on db SG
  }
}

# db.tf
resource "aws_security_group" "db" {
  ingress {
    security_groups = [aws_security_group.app.id]  # Depends on app SG!
  }
}
# => Circular!
```

### 💡 Giải pháp

**1. Tách security group rules:**

```hcl
resource "aws_security_group" "app" {
  name = "app"
  # Chỉ định nghĩa SG, không có rules
}

resource "aws_security_group" "db" {
  name = "db"
}

# Rules riêng biệt
resource "aws_security_group_rule" "app_from_db" {
  security_group_id        = aws_security_group.app.id
  source_security_group_id = aws_security_group.db.id
  # ...
}

resource "aws_security_group_rule" "db_from_app" {
  security_group_id        = aws_security_group.db.id
  source_security_group_id = aws_security_group.app.id
  # ...
}
```

**2. depends_on explicit:**

```hcl
resource "aws_security_group_rule" "db_from_app" {
  # ...
  depends_on = [aws_security_group.app, aws_security_group.db]
}
```

**3. Graph để debug:**

```bash
terraform graph | dot -Tpng > graph.png
# Xem visual dependencies
```

### 🧠 Bài học

- **Inline rules gây circular** - Tách ra separate resources
- **terraform graph** - Visual debug dependencies
- **Design trước khi code** - Dependency diagram

---

## Scenario 5: Terraform quá chậm - 20+ phút mỗi plan

### 📋 Bối cảnh

Project có 500+ resources. Mỗi `terraform plan` mất **20 phút**.

> "Tôi không dám thay đổi gì vì chờ lâu quá"

### 🔍 Triệu chứng

```bash
time terraform plan
# Refreshing state...
# (20 minutes later)
# Plan: 0 to add, 1 to change, 0 to destroy.
```

### 🕵️ Điều tra

```bash
# Terraform phải call API cho mỗi resource để refresh state
# 500 resources x 2s/resource = 1000s = 16+ minutes
```

### 💡 Giải pháp

**1. Targeted plan:**

```bash
# Chỉ plan resources bạn đang sửa
terraform plan -target=module.app
terraform plan -target=aws_instance.web
```

**2. Split state by environment/component:**

```
infrastructure/
├── network/        # terraform state riêng
│   └── main.tf
├── database/       # terraform state riêng
│   └── main.tf
└── application/    # terraform state riêng
    └── main.tf
```

**3. Parallelism:**

```bash
terraform plan -parallelism=20  # Default là 10
```

**4. Skip refresh (cẩn thận!):**

```bash
# Nếu chắc chắn không có drift
terraform plan -refresh=false
```

**5. Terraform Cloud/Enterprise:**

```hcl
# Remote operations - chạy trên server mạnh
terraform {
  cloud {
    organization = "company"
    workspaces {
      name = "production"
    }
  }
}
```

### 🧠 Bài học

- **Monolith state = slow** - Split theo logical boundaries
- **Targeted operations** - Không cần plan tất cả
- **Remote execution** - Máy mạnh hơn laptop
- **Caching layer** - Terragrunt cache

---

## 📝 Terraform Best Practices Checklist

- [ ] Remote state với locking (S3 + DynamoDB)
- [ ] State versioning enabled
- [ ] prevent_destroy cho critical resources
- [ ] Plan output saved và reviewed
- [ ] Approval workflow cho production
- [ ] Drift detection scheduled
- [ ] State split theo component
- [ ] Secrets trong variables, không hardcode
