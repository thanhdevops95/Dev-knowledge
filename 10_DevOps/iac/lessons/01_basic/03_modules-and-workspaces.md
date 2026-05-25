# 🎓 Modules & Multi-env — DRY + Reusability

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [State & Backend](02_state-and-backend.md)

> 🎯 *Master **modules** (reusable code), **module sources** (local/git/Registry), **input/output**, **composition** patterns, **multi-env strategies** (workspaces vs separate dirs vs Terragrunt), **versioning** modules.*

## 🎯 Sau bài này bạn sẽ

- [ ] Write **module** (reusable block)
- [ ] Use **public modules** from Registry
- [ ] **Local** vs **remote** module sources
- [ ] **Composition** patterns
- [ ] **Multi-env**: workspaces vs separate dirs vs **Terragrunt**
- [ ] **Module versioning** + pinning
- [ ] **Module testing** với terratest

---

## 1️⃣ Module là gì?

**Module** = reusable Terraform code (collection of `.tf` files).

### Why?

Module solve 5 vấn đề chính trong infra management — DRY (không copy-paste), encapsulation (hide complexity), standardization (cùng building block), composition, sharing (Terraform Registry):

- 🔁 **DRY** — same VPC config across 3 envs.
- 📦 **Encapsulation** — hide complexity.
- 🎯 **Standardization** — team uses same building blocks.
- ✅ **Composition** — build complex from simple.
- 📚 **Sharing** — Terraform Registry has 1000s.

### Anatomy

Mỗi module là 1 folder với **4 file chuẩn** — main (resources), variables (inputs), outputs (returns), README. Call module với `module "name" { source = "..." }` từ root module:

```
modules/vpc/
├── main.tf           # Resources
├── variables.tf      # Inputs
├── outputs.tf        # Outputs
└── README.md          # Documentation
```

Caller (root module):

```hcl
# envs/production/main.tf
module "vpc" {
  source       = "../../modules/vpc"
  name         = "acmeshop-prod"
  cidr_block   = "10.0.0.0/16"
  azs          = ["us-east-1a", "us-east-1b"]
}

# Use outputs
resource "aws_instance" "web" {
  subnet_id = module.vpc.public_subnet_ids[0]
}
```

→ Module = function. Inputs (vars) → Outputs (returns).

---

## 2️⃣ Write a module — VPC example

### `modules/vpc/variables.tf`

File `variables.tf` định nghĩa **interface input** của module — name, type, default, validation. Caller pass values qua `module "vpc" { name = "..."  }`. Đây là "API contract" của module:

```hcl
variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR"
  type        = string
  default     = "10.0.0.0/16"
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDRs"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}
```

### `modules/vpc/main.tf`

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = merge(var.tags, { Name = "${var.name}-vpc" })
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.azs[count.index % length(var.azs)]
  map_public_ip_on_launch = true
  tags = merge(var.tags, { Name = "${var.name}-public-${count.index}" })
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = merge(var.tags, { Name = "${var.name}-igw" })
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = merge(var.tags, { Name = "${var.name}-rt-public" })
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
```

### `modules/vpc/outputs.tf`

```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "vpc_cidr_block" {
  value = aws_vpc.main.cidr_block
}
```

### Use it

```hcl
# envs/production/main.tf
module "vpc" {
  source = "../../modules/vpc"

  name = "acmeshop-prod"
  azs  = ["us-east-1a", "us-east-1b"]
  tags = {
    Environment = "production"
    Team        = "platform"
  }
}

resource "aws_security_group" "web" {
  vpc_id = module.vpc.vpc_id    # ← Use module output
  # ...
}
```

```bash
cd envs/production
terraform init       # Initialize modules
terraform apply
```

→ **DRY achieved**. Reuse `vpc/` module in dev/staging/prod with different vars.

---

## 3️⃣ Module sources

### Local (relative path)

```hcl
module "vpc" {
  source = "../../modules/vpc"
}
```

→ Same git repo. Most common.

### Terraform Registry (public)

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "acmeshop"
  cidr = "10.0.0.0/16"
  azs  = ["us-east-1a", "us-east-1b"]
  # ...
}
```

→ **terraform-aws-modules/vpc/aws** = community-maintained VPC module, 100M+ downloads. Mature.

### Git

```hcl
module "vpc" {
  source = "git::https://github.com/acmeshop/tf-modules.git//vpc?ref=v1.2.0"
}

# Or with SSH
source = "git@github.com:acmeshop/tf-modules.git//vpc?ref=v1.2.0"

# Pin to commit (immutable)
source = "git::https://github.com/acmeshop/tf-modules.git//vpc?ref=abc1234"
```

### Other sources

```hcl
# HTTP archive
source = "https://example.com/vpc-module.tar.gz"

# S3
source = "s3::https://s3-us-east-1.amazonaws.com/bucket/vpc.tar.gz"

# Subdirectory in git
source = "git::https://github.com/x/y.git//path/to/module"
```

→ **Recommended versioning**:
- **Registry**: `version = "~> 5.0"` (semver constraint).
- **Git**: `?ref=v1.2.0` (tag) or `?ref=<SHA>` (immutable).

---

## 4️⃣ Public modules — Terraform Registry

### Famous modules

| Module | Purpose |
|---|---|
| `terraform-aws-modules/vpc/aws` | AWS VPC |
| `terraform-aws-modules/eks/aws` | EKS cluster |
| `terraform-aws-modules/rds/aws` | RDS DB |
| `terraform-aws-modules/lambda/aws` | Lambda |
| `terraform-aws-modules/security-group/aws` | SG |
| `terraform-aws-modules/iam/aws` | IAM |

→ Search: registry.terraform.io. Read docs + examples.

### Example: EKS cluster in 30 lines

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "acmeshop-prod"
  cluster_version = "1.31"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 1
      max_size     = 10
      instance_types = ["t3.medium"]
    }
  }

  tags = local.tags
}
```

→ Without module: 500+ lines (cluster + IAM + node groups + add-ons + ...). With module: 30 lines.

### Pros / Cons community modules

| Pros | Cons |
|---|---|
| ✅ Battle-tested | ❌ "Black box" — debug harder |
| ✅ Save time | ❌ Versions drift; breaking changes |
| ✅ Best practices | ❌ Generic — may not fit exact need |
| ✅ Maintained | ❌ Depends on maintainer continued effort |

→ **2026 practice**: use community for **boilerplate** (VPC, EKS, IAM). Write own for **business-specific**.

---

## 5️⃣ Module composition

```hcl
# envs/production/main.tf
module "vpc" {
  source = "../../modules/vpc"
  # ...
}

module "database" {
  source = "../../modules/database"

  vpc_id     = module.vpc.vpc_id           # Pass output
  subnet_ids = module.vpc.private_subnet_ids
  db_name    = "acmeshop"
}

module "eks" {
  source = "../../modules/eks"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnet_ids
  db_endpoint = module.database.endpoint
}

module "app" {
  source = "../../modules/app"

  cluster_endpoint = module.eks.cluster_endpoint
  cluster_ca_cert  = module.eks.cluster_ca_certificate
  db_endpoint      = module.database.endpoint
}
```

→ Modules compose. Outputs flow into other modules.

### Module nesting

Modules can call other modules:

```
modules/app/
├── main.tf            # Calls modules/networking/ + modules/compute/
├── networking/         (nested module)
└── compute/            (nested module)
```

→ Deep nesting hurts readability. **Rule of thumb**: max 2 levels.

---

## 6️⃣ Multi-env strategies

### Strategy 1 — Workspaces

```bash
terraform workspace new dev
terraform workspace new staging
terraform workspace new production

terraform workspace select production
terraform apply
```

```hcl
locals {
  config = {
    dev        = { instance_type = "t3.small",  count = 1 }
    staging    = { instance_type = "t3.medium", count = 2 }
    production = { instance_type = "t3.large",  count = 5 }
  }
  current = local.config[terraform.workspace]
}

resource "aws_instance" "web" {
  count         = local.current.count
  instance_type = local.current.instance_type
}
```

**Pros**: simple, single codebase.
**Cons**: easy mistake (wrong workspace), shared `.tf` = small change affects all envs.

### Strategy 2 — Separate directories (recommended)

```
infra/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
└── envs/
    ├── dev/
    │   ├── main.tf
    │   ├── terraform.tfvars
    │   └── backend.tf
    ├── staging/
    │   ├── main.tf
    │   └── terraform.tfvars
    └── production/
        ├── main.tf
        └── terraform.tfvars
```

```hcl
# envs/production/main.tf
module "vpc" {
  source = "../../modules/vpc"
  name   = "acmeshop-prod"
  azs    = ["us-east-1a", "us-east-1b"]
}
```

**Pros**: explicit, no mistake. Each env state separate.
**Cons**: some boilerplate.

→ **2026 best practice**: separate dirs. Most teams.

### Strategy 3 — Terragrunt (DRY wrapper)

```hcl
# terragrunt.hcl in envs/production/
remote_state {
  backend = "s3"
  config = {
    bucket = "acmeshop-tf-state"
    key    = "envs/${path_relative_to_include()}/terraform.tfstate"
  }
}

inputs = {
  environment = "production"
}
```

```hcl
# envs/production/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules/vpc"
}

inputs = {
  name = "acmeshop-prod"
  azs  = ["us-east-1a", "us-east-1b"]
}
```

```bash
terragrunt apply
# Generate Terraform files, init, apply
```

→ Terragrunt:
- ✅ DRY backend config across envs.
- ✅ Auto state file naming per env.
- ✅ Dependencies between modules with order.
- ❌ Extra tool to learn.

→ **Use case**: large team, many envs. Small projects: separate dirs sufficient.

---

## 7️⃣ Module versioning + publish

### Semver for modules

```
v1.0.0 — Initial stable
v1.0.1 — Patch (bug fix, no API change)
v1.1.0 — Minor (new optional input, backward compat)
v2.0.0 — Major (breaking, e.g., required input added)
```

### Tag in git

```bash
git tag v1.0.0
git push origin v1.0.0

# Consumers:
module "x" { source = "git::...?ref=v1.0.0" }
```

### Publish to Terraform Registry

GitHub repo `terraform-<provider>-<name>` (e.g., `terraform-aws-myapp`) → publish to registry.terraform.io.

→ Public modules need GitHub OSS. Private: **Terraform Cloud private registry**.

### Module documentation

```bash
# Generate README from variables.tf + outputs.tf
brew install terraform-docs
terraform-docs markdown table modules/vpc > modules/vpc/README.md
```

→ Auto-generate. CI: ensure docs updated each PR.

---

## 8️⃣ Module testing

### Unit-style — `terraform plan`

```bash
# tests/vpc-defaults/main.tf
module "vpc" {
  source = "../../modules/vpc"
  name   = "test"
  azs    = ["us-east-1a"]
}
```

```bash
cd tests/vpc-defaults
terraform init
terraform plan -detailed-exitcode
# Exit 0 = no changes (idempotent)
# Exit 2 = first run
```

### Integration — Terratest

```go
// tests/vpc_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPC(t *testing.T) {
    options := &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "name": "test",
            "azs":  []string{"us-east-1a"},
        },
    }

    defer terraform.Destroy(t, options)

    terraform.InitAndApply(t, options)

    vpcId := terraform.Output(t, options, "vpc_id")
    assert.NotEmpty(t, vpcId)
}
```

```bash
cd tests
go test -v -timeout 30m
```

→ **Terratest** = Go-based integration testing. Apply real infra, assert, destroy.

### Tools

- `terratest` — most popular.
- `Kitchen-Terraform` — Ruby-based.
- `terraform test` (built-in since 1.6) — native YAML tests.

```hcl
# tests/vpc.tftest.hcl
variables {
  name = "test"
  azs  = ["us-east-1a"]
}

run "create_vpc" {
  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "CIDR should default to 10.0.0.0/16"
  }
}
```

```bash
terraform test
```

→ Built-in `terraform test` — newer, easier than Terratest for basics.

---

## 9️⃣ Structure của bạn

```
infra/
├── bootstrap/                    # One-time S3 + DynamoDB
├── modules/
│   ├── vpc/                       # Reusable VPC
│   ├── eks/                       # Reusable EKS
│   ├── rds/                       # Reusable RDS
│   └── app/                       # Reusable app deploy
├── envs/
│   ├── dev/
│   │   ├── backend.tf
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── backend.tf
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── production/
│       ├── backend.tf
│       ├── main.tf
│       └── terraform.tfvars
├── tests/
│   ├── vpc.tftest.hcl
│   └── eks.tftest.hcl
└── .github/workflows/terraform.yml
```

### `envs/production/main.tf`

```hcl
module "vpc" {
  source = "../../modules/vpc"

  name = "acmeshop-prod"
  azs  = ["us-east-1a", "us-east-1b", "us-east-1c"]
  tags = local.tags
}

module "eks" {
  source = "../../modules/eks"

  cluster_name = "acmeshop-prod"
  vpc_id       = module.vpc.vpc_id
  subnet_ids   = module.vpc.private_subnet_ids
  tags         = local.tags
}

module "rds" {
  source = "../../modules/rds"

  identifier = "acmeshop-prod-db"
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  tags       = local.tags
}

locals {
  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
    Project     = "Acmeshop"
  }
}
```

→ Each env = 100 lines main.tf calling modules. Modules = 200+ lines internal. **Composition + DRY achieved**.

---

## ⚠️ 5 pitfall hay vướng

1. **No version pinning module** → next year, module breaks unexpectedly. Always `version = "~> 5.0"` or `ref=v1.0.0`.
2. **Deep nested modules** (3+ levels) → hard debug. Max 2 levels.
3. **Workspaces for production envs** → mistake "wrong workspace" causes wrong deploy. Separate dirs.
4. **No module README** → consumers can't use. terraform-docs auto-generate.
5. **Reinvent VPC/IAM modules** → Reuse `terraform-aws-modules/*`. Battle-tested.

---

## ✅ Self-check

1. **Module** = gì? Anatomy?
2. **Workspaces** vs **separate directories** — chọn cái nào production?
3. **Terraform Registry** module — pros vs cons?
4. **Module versioning** — best practice?
5. **Terragrunt** thêm gì so với plain Terraform?

<details>
<summary>Gợi ý đáp án</summary>

1. **Module** = collection of `.tf` files (`main.tf` + `variables.tf` + `outputs.tf` + README). Like function: inputs (vars) → outputs (returns). Reusable across envs/projects. Anatomy: variables.tf (inputs), main.tf (resources), outputs.tf (returns to caller).

2. **Workspaces**: same code, state per workspace. Simple but easy "wrong workspace" mistake. **Separate dirs** (envs/{dev,staging,prod}/): explicit, each env own state + tfvars + backend. **2026 best practice**: separate dirs production. Workspaces: small projects, ephemeral envs (per-PR).

3. **Pros**: battle-tested by community, save time (EKS module = 30 lines vs 500), follow best practices, maintained. **Cons**: "black box" debug harder, version drift / breaking changes, generic doesn't fit edge cases, dependent on maintainer continued effort. Use community for boilerplate, write own for business-specific.

4. **Semver** (1.0.0, 1.0.1, 1.1.0, 2.0.0). Tag in git: `v1.0.0`. Consumer pin: `version = "~> 5.0"` (Registry) or `?ref=v1.0.0` (git). Patch updates auto, major bumps require deliberate. Match documentation per version.

5. **Terragrunt** adds: (a) **DRY backend config** across envs (1 file vs N). (b) **Auto state file naming** based on path. (c) **Dependencies** with order between modules. (d) Inherit configs from parent files. **Extra tool** to learn but valuable for large multi-env setup. Small projects: plain Terraform separate dirs sufficient.
</details>

---

## ⚡ Cheatsheet

### Module structure

```
modules/vpc/
├── main.tf
├── variables.tf
├── outputs.tf
└── README.md
```

### Sources

```hcl
source = "../../modules/vpc"                                 # Local
source = "terraform-aws-modules/vpc/aws"                     # Registry
source = "git::https://github.com/x/y.git//vpc?ref=v1.0.0"  # Git
```

### Multi-env

```
envs/dev/main.tf       module "vpc" { source = "../../modules/vpc" }
envs/staging/main.tf    ...
envs/production/main.tf ...
```

### Terragrunt

```hcl
# terragrunt.hcl
remote_state { backend = "s3" config = { ... } }
inputs = { environment = "prod" }
```

### Test

```bash
terraform-docs markdown modules/vpc > modules/vpc/README.md
terraform test                         # Built-in
go test ./...                            # Terratest
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Module** | Reusable Terraform code |
| **Root module** | Top-level directory invoked with `terraform apply` |
| **Child module** | Module called by root or another |
| **Source** | Where module code lives |
| **Terraform Registry** | Public module repository |
| **Composition** | Combine modules together |
| **Workspaces** | Named state instances |
| **Terragrunt** | DRY wrapper for Terraform |
| **terraform-docs** | Auto-generate module README |
| **Terratest** | Go-based integration test |
| **`terraform test`** | Built-in HCL test (1.6+) |
| **Semver** | Versioning scheme |

---

## 🔗 Links

### Trong cluster
- ← Trước: [State & Backend](02_state-and-backend.md)
- → Tiếp: [Best Practices & Alternatives](04_best-practices-and-alternatives.md)
- ↑ Cluster: [iac README](../../README.md)

### External
- 📖 [Module docs](https://developer.hashicorp.com/terraform/language/modules)
- 📖 [Terraform Registry](https://registry.terraform.io/)
- 📖 [terraform-aws-modules](https://github.com/terraform-aws-modules)
- 📖 [Terragrunt](https://terragrunt.gruntwork.io/)
- 📖 [Terratest](https://terratest.gruntwork.io/)
- 📖 [terraform-docs](https://terraform-docs.io/)

---

> 🎯 *Sau bài này modules + multi-env mastered. Bài cuối dạy **best practices + alternatives** — production wisdom.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Why module + Anatomy + variables.tf interface.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster iac basic lesson 4/5. Cover: module anatomy + write VPC module from scratch + workspaces + multi-env (dev/staging/prod) + Terraform Registry + module versioning + count/for_each loops.
