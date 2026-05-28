# Module 12: Infrastructure as Code (Terraform)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **IaC** | - | Infrastructure as Code - Viết code để tạo hạ tầng |
| **Terraform** | - | Tool IaC phổ biến nhất, hỗ trợ multi-cloud |
| **HCL** | - | HashiCorp Configuration Language - Ngôn ngữ của Terraform |
| **Provider** | - | Plugin kết nối Terraform với cloud (AWS, GCP, Azure) |
| **Resource** | - | Tài nguyên được quản lý (EC2, S3, VPC) |
| **State** | - | Trạng thái - File lưu thông tin resources đã tạo |
| **Plan** | - | Preview thay đổi trước khi áp dụng |
| **Apply** | - | Áp dụng thay đổi lên cloud |
| **Destroy** | - | Xóa tất cả resources |
| **Module** | - | Nhóm resources có thể tái sử dụng |
| **Variable** | - | Biến - Tham số hóa configuration |
| **Output** | - | Giá trị trả về sau khi apply |
| **Backend** | - | Nơi lưu state file (S3, Terraform Cloud) |

---

## 📖 Infrastructure as Code là gì? (Định nghĩa từ gốc)

### Trước hết: Infrastructure là gì?

**Infrastructure = Hạ tầng cho ứng dụng chạy**

Bao gồm tất cả các thành phần "dưới" ứng dụng:

- **Compute:** Servers (EC2), containers
- **Network:** VPC, subnets, security groups, load balancers
- **Storage:** S3 buckets, EBS volumes
- **Database:** RDS instances, DynamoDB tables
- **Security:** IAM roles, policies, certificates

### Cách truyền thống tạo Infrastructure (Manual/ClickOps)

Bạn vào AWS Console, click qua từng service để tạo:

```
1. Click "Create VPC" → Điền form → Create
2. Click "Create Subnet" → Điền form → Create
3. Click "Create Security Group" → Điền form → Create
4. Click "Create EC2" → Chọn options → Launch
5. ... lặp lại 50 lần cho production stack
```

**Vấn đề với ClickOps:**

| Vấn đề | Hậu quả |
|--------|---------|
| **Không reproducible** | `"Làm lại y hệt staging cho prod?"` - Không ai nhớ hết clicks |
| **Không trackable** | `"Ai đổi security group này?"` - Không biết |
| **Human error** | Click nhầm, typo, quên step → Production down |
| **Không automation** | Không thể tích hợp CI/CD |
| **Không review** | Không có Pull Request cho infrastructure changes |

### Infrastructure as Code giải quyết

> **Infrastructure as Code (IaC) = Định nghĩa infrastructure bằng code files**

Thay vì click, bạn viết file mô tả **"tôi muốn infrastructure như thế nào"**:

```hcl
# Thay vì click 50 lần, viết 1 file:
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t3.medium"
}
```

**Lợi ích của IaC:**

| Lợi ích | Giải thích |
|---------|------------|
| **Reproducible** | Chạy cùng code → cùng infrastructure (dev = staging = prod) |
| **Trackable** | Git history cho thấy ai đổi gì, khi nào |
| **Reviewable** | Pull Request cho infrastructure changes |
| **Automatable** | CI/CD có thể apply infrastructure |
| **Self-documenting** | Code là documentation |

### Terraform là gì trong bức tranh này?

> **Terraform = Tool IaC phổ biến nhất, hỗ trợ multi-cloud**

Có nhiều IaC tools:

- **Terraform** - Multi-cloud (AWS, Azure, GCP, etc.)
- **CloudFormation** - AWS only
- **Pulumi** - Dùng programming languages (Python, TypeScript)
- **Ansible** - Configuration management + IaC

**Tại sao học Terraform?**

- Multi-cloud: Một syntax cho tất cả
- Market share: Phổ biến nhất cho IaC
- Declarative: Dễ đọc, dễ hiểu
- Community: Nhiều modules có sẵn

---

## 🎬 Câu chuyện thực tế

Tuần 1: Click-click trong AWS Console để tạo production stack:

- VPC với subnets
- Security groups
- EC2 instances
- Load balancers
- RDS database

Tuần 2: Sếp yêu cầu tạo staging environment **y hệt production**.

**Với ClickOps:** `"Uhh... để em nhớ lại...*` - 2 ngày làm lại + sai sót

**Với Terraform:**

```bash
terraform workspace new staging
terraform apply
# Done trong 10 phút, đảm bảo giống 100%
```

---

## 📖 Terraform Basics

### Tại sao Terraform?

Trước khi có IaC, bạn phải click trong AWS Console để tạo resources. Vấn đề:

- **Không reproducible**: Không thể tạo lại chính xác
- **Không trackable**: Ai đổi gì, khi nào?
- **Không automatable**: Không thể tích hợp CI/CD

Terraform giải quyết tất cả bằng cách viết code:

| Đặc điểm | Giải thích |
|----------|------------|
| **Declarative** | Bạn mô tả "muốn gì", Terraform lo "làm thế nào" |
| **Multi-cloud** | Cùng một syntax cho AWS, GCP, Azure |
| **Version control** | Git track mọi thay đổi infrastructure |
| **Plan before apply** | Xem preview trước khi thực sự tạo resources |

### HCL Syntax

**HCL (HashiCorp Configuration Language)** là ngôn ngữ của Terraform. Syntax rất đơn giản và dễ đọc:

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "web-server"
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "my-unique-bucket-name"
}
```

**Giải thích từng phần:**

| Block | Ý nghĩa |
|-------|---------|
| `provider "aws"` | Kết nối với AWS, dùng region us-east-1 |
| `resource "aws_instance" "web"` | Tạo EC2 instance, đặt tên local là "web" |
| `ami = "..."` | Amazon Machine Image - OS template |
| `tags = { Name = "..." }` | Tag để dễ nhận biết trong Console |

> 💡 **Naming convention:** `resource "TYPE" "NAME"` - TYPE là loại resource của provider, NAME là tên bạn tự đặt để reference trong code.

---

## 🔧 Terraform Commands

**Workflow cơ bản:** `init` → `plan` → `apply`. Đây là 3 lệnh bạn sẽ dùng hàng ngày.

```bash
# 1. Initialize - Chạy 1 lần đầu khi clone project
terraform init
# Download providers (plugins) và setup state

# 2. Format - Tự động format code cho đẹp
terraform fmt

# 3. Validate - Kiểm tra syntax
terraform validate

# 4. Plan - XEM TRƯỚC thay đổi (quan trọng nhất!)
terraform plan
# Output sẽ show: + create, ~ modify, - destroy

# 5. Apply - Thực sự tạo/sửa resources
terraform apply
# Gõ "yes" để confirm

# 6. Destroy - Xóa TẤT CẢ resources (cẩn thận!)
terraform destroy
```

**Giải thích workflow:**

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
│  Code   │───▶│  Plan    │───▶│  Review  │───▶│  Apply    │
│  (.tf)  │    │          │    │  (human) │    │  (create) │
└─────────┘    └──────────┘    └──────────┘    └───────────┘
```

> ⚠️ **Best practice:** LUÔN chạy `plan` trước `apply`. Đọc kỹ output để tránh destroy nhầm resources.

---

## 📦 Variables và Outputs

**Tại sao cần Variables?** Để code có thể tái sử dụng cho nhiều environments (dev, staging, prod).

### Định nghĩa Variables

```hcl
# variables.tf - Khai báo variables
variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"  # Giá trị mặc định nếu không truyền vào
}

variable "environment" {
  description = "Environment name"
  type        = string      # Bắt buộc phải là string
  # Không có default = bắt buộc phải truyền giá trị
}
```

### Sử dụng Variables

```hcl
# main.tf - Dùng variables với prefix "var."
resource "aws_instance" "web" {
  instance_type = var.instance_type  # Tham chiếu variable
  
  tags = {
    Environment = var.environment
  }
}
```

### Outputs - Lấy giá trị sau khi apply

```hcl
# outputs.tf - Hiển thị/export giá trị quan trọng
output "instance_ip" {
  value = aws_instance.web.public_ip
  # Sau khi apply, sẽ in ra IP của EC2
}
```

### Truyền giá trị khi apply

```bash
# Cách 1: Command line
terraform apply -var="environment=production"

# Cách 2: File .tfvars (recommended cho nhiều variables)
terraform apply -var-file="production.tfvars"
```

**File production.tfvars:**

```hcl
environment   = "production"
instance_type = "t3.large"
```

> 💡 **Tip:** Tạo file `.tfvars` cho mỗi environment: `dev.tfvars`, `staging.tfvars`, `prod.tfvars`

---

## 📝 Tổng kết

✅ IaC concept  
✅ Terraform HCL syntax  
✅ init, plan, apply, destroy  
✅ Variables and outputs  

👉 **[LABS.md](LABS.md)** | **[SCENARIOS.md](SCENARIOS.md)**
