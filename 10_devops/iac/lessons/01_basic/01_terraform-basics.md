# 🎓 Terraform Basics — Providers, Resources, Variables

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [What is IaC](00_what-is-iac.md)

> 🎯 *Master Terraform/OpenTofu core: **HCL** syntax, **providers**, **resources**, **data sources**, **variables** + **outputs**, **locals**, **expressions**, **functions**, **dependencies**, **lifecycle**. Sau bài này provision real cloud infra.*

## 🎯 Sau bài này bạn sẽ

- [ ] Install Terraform/OpenTofu + first project
- [ ] **HCL** syntax (HashiCorp Configuration Language)
- [ ] **Providers** + version pinning
- [ ] **Resources** + **data sources**
- [ ] **Variables** (input) + **outputs** + **locals**
- [ ] **Expressions** + 50+ built-in functions
- [ ] **Dependencies** (implicit + explicit)
- [ ] **`lifecycle`** meta-arguments (prevent_destroy, etc.)
- [ ] **`count` + `for_each`** loops

---

## 1️⃣ Cài đặt

2 lựa chọn — Terraform (HashiCorp, license BSL từ 2023) hoặc OpenTofu (OSS fork). API compatible 100%, command interchangeable. 2026 community trend dùng OpenTofu cho production:

```bash
# Terraform (HashiCorp)
brew install terraform
terraform -version

# OpenTofu (recommended 2026, OSS fork)
brew install opentofu
tofu -version

# Drop-in compat — use `tofu` or `terraform` interchangeably
```

→ This lesson uses `terraform` but commands identical with `tofu`.

---

## 2️⃣ Project đầu tiên — Hello AWS

### Cấu trúc thư mục

Project Terraform tối thiểu gồm **3 file `.tf` cốt lõi** — main (resources), variables (input), outputs (output). Optional: `terraform.tfvars` (values, **gitignore vì chứa secrets**) và `.terraform/` (provider cache):

```
my-iac/
├── main.tf           # Resources
├── variables.tf      # Input vars
├── outputs.tf        # Output vars
├── terraform.tfvars  # Variable values (gitignore!)
└── .terraform/        # Provider plugins (gitignore!)
```

### `main.tf`

File chính chứa 3 thứ bắt buộc: `terraform {}` block (version + providers), `provider "aws" {}` (config), `resource` blocks (định nghĩa infra). Skeleton tối thiểu cho AWS:

```hcl
terraform {
  required_version = ">= 1.6"
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

resource "aws_s3_bucket" "logs" {
  bucket = "acmeshop-logs-2026"
}
```

### Luồng làm việc

Workflow Terraform chuẩn **5 lệnh** — init (download providers), fmt+validate (lint), plan (preview changes), apply (execute), destroy (tear down). Đây là loop bạn lặp daily:

```bash
# Initialize — download providers
terraform init

# Format + validate
terraform fmt
terraform validate

# Preview
terraform plan
# Output: + create aws_s3_bucket.logs

# Apply
terraform apply
# Confirm: yes
# Output: aws_s3_bucket.logs: Creating... Created

# Destroy
terraform destroy
```

→ **First infra provisioned in 5 commands**.

---

## 3️⃣ Cú pháp HCL

### Blocks

HCL (HashiCorp Configuration Language) dùng **block syntax** — type + labels + body trong `{}`. Quy ước: 0-2 labels tùy block type. Đây là building block của mọi `.tf` file:

```hcl
<block-type> "<label1>" "<label2>" {
  argument = value
  nested_block {
    arg2 = value
  }
}
```

| Block | Purpose |
|---|---|
| `terraform { }` | Terraform settings |
| `provider "x" { }` | Cloud provider config |
| `resource "type" "name" { }` | Create infra resource |
| `data "type" "name" { }` | Read existing data |
| `variable "name" { }` | Input variable |
| `output "name" { }` | Output value |
| `locals { }` | Local values |
| `module "name" { }` | Reusable module |

### Giá trị + kiểu dữ liệu

```hcl
# String
region = "us-east-1"
multiline = <<EOF
  multi
  line
EOF

# Number
count = 3
price = 0.05

# Boolean
enabled = true

# List
zones = ["us-east-1a", "us-east-1b"]

# Map (object)
tags = {
  Name = "web"
  Env  = "prod"
}

# Object — explicit types (rarely needed)
config = {
  size = "small"
  count = 3
  tags = ["a", "b"]
}
```

### Tham chiếu (references)

```hcl
# Reference other resource
resource "aws_instance" "web" {
  subnet_id = aws_subnet.public.id        # ← Reference subnet
}

# Reference variable
region = var.region

# Reference local
name = local.cluster_name

# Reference data source
ami_id = data.aws_ami.ubuntu.id

# Module output
db_endpoint = module.database.endpoint
```

### Chú thích (comments)

```hcl
# Single line
// Also single line
/*
  Multi-line
  comment
*/
```

---

## 4️⃣ Providers

**Provider** = plugin for specific cloud/service.

### Các provider chính

| Provider | Resources |
|---|---|
| `hashicorp/aws` | AWS — EC2, S3, RDS, ... |
| `hashicorp/google` | GCP |
| `hashicorp/azurerm` | Azure |
| `hashicorp/kubernetes` | K8s objects |
| `hashicorp/helm` | Helm charts |
| `cloudflare/cloudflare` | DNS, CDN |
| `digitalocean/digitalocean` | DO |
| `github/github` | GitHub repos, teams |
| `mongodb/mongodbatlas` | MongoDB Atlas |
| `pagerduty/pagerduty` | PagerDuty config |

→ 3000+ providers in Terraform Registry. Almost every SaaS has one.

### Ghim version (version pinning)

```hcl
terraform {
  required_version = ">= 1.6"             # Terraform CLI version

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"                   # ~> = pessimistic constraint
    }
  }
}
```

| Constraint | Meaning |
|---|---|
| `5.0` | Exactly 5.0 |
| `>= 5.0` | 5.0 or later |
| `>= 5.0, < 6.0` | 5.x.x range |
| `~> 5.0` | >= 5.0, < 6.0 (same major) |
| `~> 5.7` | >= 5.7, < 5.8 (same minor) |

→ Production: pin `~> 5.0` to allow patches but block major bumps.

### Cấu hình provider

```hcl
provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      ManagedBy   = "Terraform"
      Project     = "Acmeshop"
      Environment = var.environment
    }
  }
}

# Multiple regions
provider "aws" {
  alias  = "europe"
  region = "eu-west-1"
}

resource "aws_s3_bucket" "eu" {
  provider = aws.europe                   # Use alias
  bucket   = "acmeshop-eu"
}
```

### Xác thực (authentication)

```bash
# AWS — use any of:
# 1. Env vars
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# 2. AWS CLI profile
export AWS_PROFILE=acmeshop-prod

# 3. IAM role (EC2/CI) — auto

# 4. OIDC (GitHub Actions → AWS, no long-lived secrets)
```

→ **Never hardcode credentials in `.tf`**. Use env / profile / OIDC.

---

## 5️⃣ Resources — Khối dựng cốt lõi

```hcl
resource "<TYPE>" "<NAME>" {
  argument1 = value
  argument2 = value
}
```

### Ví dụ — EC2 instance

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  subnet_id     = aws_subnet.public.id

  tags = {
    Name = "web-server"
  }

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }
}
```

### Địa chỉ resource (resource address)

`<TYPE>.<NAME>` — used to reference + import + destroy specific.

```bash
terraform state list
# → aws_instance.web
# → aws_subnet.public

terraform destroy -target=aws_instance.web    # Destroy 1 resource
```

### Resource ID (định danh resource)

```hcl
output "instance_id" {
  value = aws_instance.web.id
}

# Reference attributes
subnet_cidr = aws_subnet.public.cidr_block
```

→ Provider docs list available attributes (id, arn, public_ip, etc).

---

## 6️⃣ Data sources — Đọc resource có sẵn

```hcl
# Find latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]              # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# Use in resource
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id    # ← Use data source
  instance_type = "t3.medium"
}
```

→ **Data sources** read state at apply time. Never modify external resources.

### Các data source hay dùng

```hcl
data "aws_availability_zones" "available" { state = "available" }
data "aws_vpc" "default" { default = true }
data "aws_caller_identity" "current" {}      # AWS account info
data "aws_region" "current" {}
```

---

## 7️⃣ Variables (input)

### Khai báo

```hcl
# variables.tf
variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 3
  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "Must be 1-10."
  }
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default = {
    ManagedBy = "Terraform"
  }
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "sensitive_value" {
  type      = string
  sensitive = true                            # Mask in logs
}

# Complex type
variable "subnets" {
  type = list(object({
    cidr = string
    az   = string
    name = string
  }))
}
```

### Gán giá trị

**1. CLI flag** (highest priority):
```bash
terraform apply -var="region=eu-west-1" -var="instance_count=5"
```

**2. tfvars file**:
```hcl
# terraform.tfvars (auto-loaded)
region         = "eu-west-1"
instance_count = 5
```

**3. Env vars**:
```bash
export TF_VAR_region=eu-west-1
export TF_VAR_instance_count=5
terraform apply
```

**4. Prompt** (interactive if no default).

### Best practice cho variables

- Sensitive in env vars or vault, NOT in committed tfvars.
- `terraform.tfvars` for dev defaults (gitignore if sensitive).
- `dev.tfvars`, `prod.tfvars` for envs.

```bash
terraform apply -var-file=prod.tfvars
```

---

## 8️⃣ Outputs

```hcl
# outputs.tf
output "instance_ip" {
  description = "Public IP of web instance"
  value       = aws_instance.web.public_ip
}

output "db_password" {
  value     = random_password.db.result
  sensitive = true                            # Mask in console
}

output "all_instance_ids" {
  value = aws_instance.web[*].id              # All from count/for_each
}
```

```bash
terraform apply
# Outputs:
# instance_ip = "203.0.113.5"

terraform output instance_ip
# 203.0.113.5

terraform output -json | jq '.instance_ip.value'
```

→ Outputs useful for:
- Show user (IP to SSH to).
- Pass between modules.
- CI pipeline consume.

---

## 9️⃣ Locals — Giá trị tạm

```hcl
locals {
  cluster_name = "acmeshop-${var.environment}"
  common_tags = {
    Project     = "Acmeshop"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_eks_cluster" "main" {
  name = local.cluster_name
  tags = local.common_tags
  # ...
}

resource "aws_s3_bucket" "logs" {
  bucket = "${local.cluster_name}-logs"
  tags   = local.common_tags
}
```

→ Like local variables in programming. DRY across resources.

---

## 1️⃣0️⃣ Expressions + Functions

### Toán tử (operators)

```hcl
sum = a + b
size = base * 2
greater = a > b
combined = "${prefix}-${suffix}"             # String interpolation
inline = a > 0 ? "positive" : "non-positive" # Ternary
```

### 50+ hàm dựng sẵn (built-in functions)

```hcl
length(var.list)                              # 3
upper("hello")                                 # "HELLO"
substr("acmeshop", 0, 4)                       # "acme"
format("instance-%d", count.index)             # "instance-0"
replace(string, "old", "new")
split(",", "a,b,c")                             # ["a","b","c"]
join("-", ["a","b"])                            # "a-b"
toset(["a","a","b"])                            # {"a","b"} — unique
contains(["a","b"], "a")                        # true
lookup(map, "key", "default")
merge({a=1}, {b=2})                             # {a=1, b=2}
keys({a=1, b=2})                                # ["a","b"]
values({a=1, b=2})                              # [1, 2]
file("config.json")                             # Read file
jsonencode({foo="bar"})                         # JSON string
jsondecode(json_string)
yamldecode(yaml_string)
base64encode("...")
base64decode("...")
md5("...")
sha256("...")
uuid()
timestamp()
formatdate("YYYY-MM-DD", timestamp())
cidrsubnet("10.0.0.0/16", 8, 0)                # 10.0.0.0/24
```

→ Full list: terraform.io/docs/language/functions/. 50+ functions cover most needs.

---

## 1️⃣1️⃣ Dependencies (phụ thuộc)

### Implicit — tự động

```hcl
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id              # ← Depends on aws_vpc.main
  cidr_block = "10.0.1.0/24"
}
```

→ Terraform parse references → build DAG → create VPC first, then subnet.

### Explicit — `depends_on` (khai báo tường minh)

```hcl
resource "aws_instance" "web" {
  # No direct reference, but need IAM role attached first
  depends_on = [aws_iam_role_policy_attachment.s3_access]
  # ...
}
```

→ Use when dependency not auto-detected (e.g., IAM eventual consistency).

### Trực quan hoá (visualize)

```bash
terraform graph | dot -Tpng > graph.png
```

→ DAG of resources. Helps understand order.

---

## 1️⃣2️⃣ `lifecycle` — Meta-arguments

```hcl
resource "aws_instance" "web" {
  # ...
  lifecycle {
    create_before_destroy = true             # Replace strategy
    prevent_destroy       = true              # Block accidental destroy
    ignore_changes = [
      ami,                                    # Don't reapply if AMI changes externally
      tags["LastSeen"],
    ]
    replace_triggered_by = [
      aws_security_group.web.id,              # Replace if SG changes
    ]
  }
}
```

| Argument | Purpose |
|---|---|
| `create_before_destroy` | Create new before destroy old (avoid downtime) |
| `prevent_destroy` | Error if destroy attempted (production DB protection) |
| `ignore_changes` | Skip diff for specific attributes |
| `replace_triggered_by` | Force replace if another resource changes |

---

## 1️⃣3️⃣ Count + for_each — Vòng lặp

### `count` — Theo số

```hcl
resource "aws_instance" "web" {
  count = 3                                  # 3 instances

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  tags = {
    Name = "web-${count.index}"               # web-0, web-1, web-2
  }
}

# Access
aws_instance.web[0].id
aws_instance.web[*].id          # All
length(aws_instance.web)
```

### `for_each` — Theo set hoặc map

```hcl
resource "aws_instance" "web" {
  for_each = toset(["app", "api", "worker"])

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  tags = {
    Name = each.key                            # app, api, worker
  }
}

# Or map for more control
locals {
  servers = {
    app    = { type = "t3.medium" }
    api    = { type = "t3.large" }
    worker = { type = "t3.small" }
  }
}

resource "aws_instance" "web" {
  for_each      = local.servers
  ami           = data.aws_ami.ubuntu.id
  instance_type = each.value.type
  tags          = { Name = each.key }
}

# Access
aws_instance.web["app"].id
aws_instance.web["api"].id
```

### `count` vs `for_each`

| Feature | `count` | `for_each` |
|---|---|---|
| Type | number | set/map |
| Address | `aws_x.web[0]` | `aws_x.web["key"]` |
| Reorder | Replaces all if list reorder | Stable by key |
| Conditional | `count = condition ? 1 : 0` | `for_each = condition ? toset(...) : []` |

→ **Default**: `for_each` (stable by key). `count` for: simple N copies, conditional create/skip.

---

## 1️⃣4️⃣ Resource có điều kiện (conditional resources)

```hcl
# Create only in production
resource "aws_db_instance" "prod_replica" {
  count = var.environment == "production" ? 1 : 0
  # ...
}

# for_each empty if not enabled
resource "aws_cloudwatch_alarm" "high_cpu" {
  for_each = var.enable_monitoring ? toset(["cpu", "mem"]) : []
  # ...
}
```

### Biểu thức điều kiện (conditional expression)

```hcl
instance_type = var.environment == "production" ? "t3.large" : "t3.small"
```

---

## 1️⃣5️⃣ Real Terraform đầu tiên của bạn — AWS VPC + EC2

```hcl
# main.tf
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.region
  default_tags { tags = local.tags }
}

locals {
  name = "acmeshop-${var.environment}"
  tags = {
    Project     = "Acmeshop"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "${local.name}-vpc" }
}

# Public subnet
resource "aws_subnet" "public" {
  for_each = toset(["a", "b"])

  vpc_id                  = aws_vpc.main.id
  availability_zone       = "${var.region}${each.key}"
  cidr_block              = each.key == "a" ? "10.0.1.0/24" : "10.0.2.0/24"
  map_public_ip_on_launch = true
  tags = { Name = "${local.name}-public-${each.key}" }
}

# Internet gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = { Name = "${local.name}-igw" }
}

# Route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = { Name = "${local.name}-rt-public" }
}

resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

# Security group
resource "aws_security_group" "web" {
  name   = "${local.name}-web"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
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

# AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# EC2 instances
resource "aws_instance" "web" {
  count = var.instance_count

  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public[count.index % 2 == 0 ? "a" : "b"].id
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
    #!/bin/bash
    docker run -d -p 80:80 nginx
  EOF

  tags = { Name = "${local.name}-web-${count.index}" }

  lifecycle {
    create_before_destroy = true
  }
}
```

```hcl
# variables.tf
variable "region" {
  type    = string
  default = "us-east-1"
}
variable "environment" {
  type    = string
  default = "production"
}
variable "instance_count" {
  type    = number
  default = 2
}
variable "instance_type" {
  type    = string
  default = "t3.medium"
}
```

```hcl
# outputs.tf
output "vpc_id"      { value = aws_vpc.main.id }
output "public_ips"  { value = aws_instance.web[*].public_ip }
output "subnet_ids"  { value = [for s in aws_subnet.public : s.id] }
```

### Chạy apply

```bash
terraform init
terraform plan -out=plan
# Review 15 resources to create

terraform apply plan
# Outputs: public_ips = ["54.234.1.5", "54.234.1.8"]

curl http://54.234.1.5/        # nginx default page
```

→ **VPC + 2 subnets + 2 EC2 + SG + IGW + routes** in 5 minutes IaC. Reproducible.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Hardcode credentials in .tf** → leak. Always env / profile / OIDC.
2. **Skip version pinning** → `terraform apply` next year = surprise breaking changes.
3. **Edit `.tfstate` manually** → corrupt. Use `terraform state` commands.
4. **No `lifecycle` cho prod DB** → accidental destroy = data lost. `prevent_destroy = true`.
5. **count + list reorder** → recreate all resources. Use `for_each` with map keys.

---

## 🧠 Tự kiểm tra (Self-check)

1. **terraform init** làm gì?
2. **Resource** vs **Data source**?
3. **`count`** vs **`for_each`** — chọn cái nào?
4. Cách reference output from other resource?
5. **Sensitive variable** + **sensitive output** — purpose?

<details>
<summary>Gợi ý đáp án</summary>

1. `terraform init`: (a) Download providers per `required_providers`. (b) Setup state backend (S3/local). (c) Initialize modules. Run first or after add new provider/module.

2. **Resource**: create/manage external resource (`aws_instance` creates EC2). Mutates infra. **Data source**: read existing data (`data "aws_ami" "ubuntu"` query latest AMI ID). No mutation. Both have address `<TYPE>.<NAME>` but resource modifies, data reads only.

3. **`count`**: numeric. Address `aws_x[0]`, `aws_x[1]`. Reorder list → recreate all (index-based). **`for_each`**: set/map. Address `aws_x["app"]`. Stable by key — add/remove items doesn't shift others. **Default 2026**: `for_each` (safer). `count` for: simple N copies, conditional 0-or-1.

4. Direct reference: `aws_subnet.public.id`. From `count`: `aws_instance.web[0].id` or `aws_instance.web[*].id` (all). From `for_each`: `aws_instance.web["app"].id`. From other module: `module.network.vpc_id`. From output: `terraform output instance_ip`.

5. **Sensitive variable**: input value masked in CLI prompt + plan output. Not stored cleartext. **Sensitive output**: value masked in console + plan output (still in state file though). Both prevent accidental leak in CI logs / screenshots. For real secrets: use Vault/Secrets Manager + data source fetch.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Luồng làm việc

```bash
terraform init       # Download providers
terraform fmt         # Format
terraform validate    # Syntax check
terraform plan        # Preview
terraform apply       # Execute
terraform destroy     # Tear down
terraform output      # Show outputs
terraform state list  # Show managed resources
```

### Resource block

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  tags          = { Name = "web" }

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
    ignore_changes        = [tags["LastSeen"]]
  }
}
```

### Variables

```hcl
variable "x" {
  type    = string
  default = "value"
}

# Use
var.x

# Set
terraform apply -var="x=value"
TF_VAR_x=value terraform apply
# or terraform.tfvars file
```

### Vòng lặp

```hcl
count = 3
each.key, each.value       # for_each

aws_instance.x[0]            # count addr
aws_instance.x["key"]        # for_each addr
aws_instance.x[*].id         # all (count)
[for k, v in map : v.id]     # for expression
```

### Hàm hữu ích

```
length, lookup, merge, contains
format, replace, join, split
file, jsonencode, base64encode
cidrsubnet, formatdate, timestamp
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **HCL** | HashiCorp Configuration Language |
| **Provider** | Plugin for specific cloud/service |
| **Resource** | Manages external resource |
| **Data source** | Reads existing data |
| **Variable** | Input parameter |
| **Output** | Exported value |
| **Local** | Computed local value |
| **Module** | Reusable Terraform code (next lesson) |
| **State** | Snapshot of managed resources |
| **`count` / `for_each`** | Loop meta-arguments |
| **`lifecycle`** | Resource behavior config |
| **`depends_on`** | Explicit dependency |
| **Expression** | Computation (math, string, conditional) |
| **Function** | Built-in helper (length, format, ...) |
| **Type** | string/number/bool/list/map/object |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [IaC là gì? — Infrastructure as Code overview](00_what-is-iac.md)
- ➡️ **Bài tiếp theo:** [State & Backend — Production essentials](02_state-and-backend.md)
- ↑ **Về cụm:** [iac README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [Terraform language docs](https://developer.hashicorp.com/terraform/language)
- 📖 [Terraform Registry](https://registry.terraform.io/) — providers + modules
- 📖 [HCL spec](https://github.com/hashicorp/hcl)
- 📖 [Built-in functions](https://developer.hashicorp.com/terraform/language/functions)
- 📖 [Terraform Best Practices](https://www.terraform-best-practices.com/)

---

> 🎯 *Sau bài này provision real cloud infra. Bài kế tiếp dạy **state + backend** — collaboration + production essentials.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster iac basic lesson 2/5. Cover: install Terraform/OpenTofu + folder structure + HCL blocks + resources + providers + variables + outputs + data sources + 5-command workflow + first AWS VPC.
- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước §1 Install, §2 Folder structure, main.tf, Workflow và §3 Blocks.
- **v1.1.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
