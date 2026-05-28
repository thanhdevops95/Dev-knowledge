# 🎓 Terragrunt — DRY Terraform cho multi-env multi-region

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** [00_intermediate-overview.md](00_intermediate-overview.md), Terraform modules + workspaces

> 🎯 *3 envs × 5 regions × 5 modules = 75 folder, 50K dòng duplicate. Terragrunt DRY: 1 module Terraform + 1 config per env (~10 dòng). Bài này dạy Terragrunt fundamentals + dependency graph + module versioning + run-all + advanced patterns.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Terragrunt** vs workspaces — khi nào dùng cái nào
- [ ] Setup repo structure **`live/` + `modules/`** pattern
- [ ] Dùng **`include`** + **`generate`** + **`inputs`** trong terragrunt.hcl
- [ ] Manage **remote state** với S3 + DynamoDB tự động generated
- [ ] **Dependencies** giữa modules (`dependency block`)
- [ ] **`run-all`** apply across multiple modules
- [ ] **Module versioning** với git tags
- [ ] Setup **multi-account AWS** với assume role

---

## Tình huống — Update VPC CIDR = sửa 15 file

Repo basic Terraform:
```
infra/
├── dev/
│   ├── us-east-1/vpc/
│   │   ├── main.tf      # 200 lines
│   │   ├── variables.tf
│   │   └── backend.tf   # S3 backend config — 20 lines, same in all 75 folders
│   ├── us-west-2/vpc/   # copy of us-east-1/vpc
│   ├── eu-west-1/vpc/   # copy
│   └── ...
├── staging/  # copy of dev
└── prod/     # copy of dev with different CIDR
```

→ Sửa VPC CIDR for prod: update `prod/us-east-1/vpc/variables.tf` + check 4 other regions + verify staging.

Workflow:
- Dev forget update `prod/us-west-2/vpc/` → drift.
- Code review nightmare: PR has 5+ duplicated files.

Sếp: *"Refactor to Terragrunt. 1 module, N config. Bài này dạy."*

---

## 1️⃣ Terragrunt concept

### What's Terragrunt?

**Terragrunt** = thin wrapper around Terraform, eliminates duplication:
- Module Terraform code in 1 place.
- Per-env config (`terragrunt.hcl`) minimal.
- Inherit + override pattern.
- Auto-generate `backend.tf`, `provider.tf` from config.

### vs workspaces

**Terraform workspaces** (basic):
- Same backend, different state file per workspace.
- `terraform workspace select prod`.
- Variables via `terraform.tfvars` files.
- Limit: still copy folder for multi-region (workspaces are within 1 directory).

**Terragrunt**:
- Different backend per env (separate state file).
- Multi-account, multi-region native.
- Dependency between modules.
- More flexible for complex layouts.

### Install

Terragrunt là Go binary standalone — cài 1 command. Wrap Terraform để add DRY layer (module versioning, dependency, multi-env config) — không thay Terraform mà tăng cường:

```bash
# macOS
brew install terragrunt

# Linux
wget https://github.com/gruntwork-io/terragrunt/releases/download/v0.55.0/terragrunt_linux_amd64
chmod +x terragrunt_linux_amd64
sudo mv terragrunt_linux_amd64 /usr/local/bin/terragrunt

terragrunt --version
```

🪞 **Ẩn dụ**: *Terraform module like **bản thiết kế nhà mẫu** (3 phòng ngủ, 2 phòng tắm, sân). Terragrunt config like **nhãn dán per căn nhà**: "Nhà số 1: dev env, us-east-1, kích thước nhỏ". 1 bản thiết kế + 75 nhãn vs 75 bản thiết kế.*

---

## 2️⃣ Repo structure pattern

### Standard layout

Repo Terragrunt chuẩn tách **2 folder**: `modules/` (Terraform reusable code, DRY) và `live/` (Terragrunt config per env/region/component). Pattern này scale từ 1 env đến hàng trăm:

```
infrastructure/
├── terragrunt.hcl              # root config
├── modules/                     # Terraform modules
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   ├── rds/
│   └── s3/
└── live/                        # per-env config
    ├── dev/
    │   ├── account.hcl          # account-level vars
    │   ├── us-east-1/
    │   │   ├── region.hcl       # region-level vars
    │   │   ├── vpc/
    │   │   │   └── terragrunt.hcl    # 10 lines
    │   │   ├── eks/
    │   │   │   └── terragrunt.hcl
    │   │   ├── rds/
    │   │   │   └── terragrunt.hcl
    │   │   └── s3/
    │   │       └── terragrunt.hcl
    │   ├── us-west-2/...
    │   └── eu-west-1/...
    ├── staging/...
    └── prod/...
```

→ **`modules/`**: Terraform code (DRY).  
**`live/`**: Terragrunt config per env.

### Workflow

Daily workflow đơn giản: `cd` vào env+region+component, gõ `terragrunt plan`/`apply`. Terragrunt tự download module, generate backend.tf + provider.tf, gọi Terraform underneath:

```bash
# Plan VPC dev us-east-1
cd live/dev/us-east-1/vpc
terragrunt plan

# Apply EKS prod us-east-1
cd live/prod/us-east-1/eks
terragrunt apply
```

→ Terragrunt downloads module, generates backend.tf, provider.tf, applies.

---

## 3️⃣ Root `terragrunt.hcl`

Common config inherited by all child Terragrunt:

```hcl
# infrastructure/terragrunt.hcl

# Generate backend.tf in each child (no duplicate)
remote_state {
  backend = "s3"
  
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  
  config = {
    bucket         = "acme-tfstate-${get_aws_account_id()}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "acme-tfstate-lock"
  }
}

# Generate provider.tf in each child
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.region
  
  default_tags {
    tags = {
      Environment = var.env
      ManagedBy   = "Terragrunt"
      Repository  = "acme/infrastructure"
    }
  }
  
  assume_role {
    role_arn = "arn:aws:iam::$${var.aws_account_id}:role/TerraformExecutionRole"
  }
}
EOF
}

# Common inputs all children inherit
inputs = {
  organization = "acme"
}
```

### Key features

6 feature chính của Terragrunt — chính là lý do dùng thay vì Terraform workspaces:

- **`generate`**: Terragrunt writes file (e.g., `backend.tf`) into child folder before running Terraform.
- **`path_relative_to_include()`**: returns relative path → unique state key per child.
- **`get_aws_account_id()`**: built-in functions.
- **`inputs`**: variables passed to module.

---

## 4️⃣ Account + Region levels

### `account.hcl` (per env account)

```hcl
# live/dev/account.hcl
locals {
  account_name = "dev"
  account_id   = "111111111111"
  env          = "dev"
}
```

```hcl
# live/prod/account.hcl
locals {
  account_name = "prod"
  account_id   = "222222222222"
  env          = "prod"
}
```

### `region.hcl` (per region)

```hcl
# live/dev/us-east-1/region.hcl
locals {
  aws_region = "us-east-1"
  vpc_cidr   = "10.0.0.0/16"
}
```

```hcl
# live/dev/us-west-2/region.hcl
locals {
  aws_region = "us-west-2"
  vpc_cidr   = "10.1.0.0/16"
}
```

→ Account + region vars cascade down via `include` blocks.

---

## 5️⃣ Child `terragrunt.hcl`

### Simple VPC module

```hcl
# live/dev/us-east-1/vpc/terragrunt.hcl

# Include root config (inherit backend, provider, common inputs)
include "root" {
  path = find_in_parent_folders()
}

# Reference local hcl files
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
}

# Terraform module source
terraform {
  source = "../../../../modules/vpc"
  # OR remote: source = "git::git@github.com:acme/infrastructure-modules.git//vpc?ref=v1.2.3"
}

# Inputs override / extend
inputs = {
  env             = local.account_vars.locals.env
  aws_account_id  = local.account_vars.locals.account_id
  region          = local.region_vars.locals.aws_region
  cidr_block      = local.region_vars.locals.vpc_cidr
  
  availability_zones = [
    "${local.region_vars.locals.aws_region}a",
    "${local.region_vars.locals.aws_region}b",
    "${local.region_vars.locals.aws_region}c",
  ]
  
  enable_nat_gateway = true
  single_nat_gateway = local.account_vars.locals.env == "dev"   # dev cheap, prod HA
}
```

→ **10 lines** per env-region. All inherit from root + account + region locals.

### Result

```bash
cd live/dev/us-east-1/vpc
terragrunt plan
```

Terragrunt:
1. Read this `terragrunt.hcl`.
2. Find root `terragrunt.hcl` (via `find_in_parent_folders`).
3. Inherit `remote_state`, `generate "provider"`, `inputs`.
4. Read `account.hcl` + `region.hcl` locals.
5. Generate `backend.tf` + `provider.tf` in current folder.
6. Run `terraform init` + `terraform plan`.

→ Clean apply. State file at `s3://acme-tfstate-...../live/dev/us-east-1/vpc/terraform.tfstate`.

---

## 6️⃣ Dependencies between modules

### Vấn đề

VPC must exist before EKS. EKS must exist before RDS.

Without Terragrunt: manual order. Forget order → apply fails.

### `dependency` block

```hcl
# live/dev/us-east-1/eks/terragrunt.hcl

include "root" {
  path = find_in_parent_folders()
}

dependency "vpc" {
  config_path = "../vpc"
  
  mock_outputs = {
    vpc_id     = "vpc-12345"
    subnet_ids = ["subnet-1", "subnet-2"]
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

terraform {
  source = "../../../../modules/eks"
}

inputs = {
  cluster_name = "acme-dev-us-east-1"
  vpc_id       = dependency.vpc.outputs.vpc_id
  subnet_ids   = dependency.vpc.outputs.private_subnet_ids
}
```

→ Terragrunt:
1. Check VPC state exists.
2. Read VPC outputs (`vpc_id`, `private_subnet_ids`).
3. Inject as input to EKS.
4. Apply EKS with VPC info.

**`mock_outputs`**: fake values for `plan` when VPC not yet applied (chicken-and-egg). Real apply needs VPC applied first.

### `terragrunt run-all`

Apply all modules in dependency order:

```bash
cd live/dev/us-east-1
terragrunt run-all apply
```

→ Terragrunt:
1. Scan all `terragrunt.hcl` in tree.
2. Build dependency graph.
3. Apply in topological order (VPC → EKS → RDS).
4. Parallel where possible (S3 + DynamoDB independent of VPC).

⚠️ `run-all` powerful but dangerous. Use carefully:
- `run-all destroy` = destroy everything.
- Lock collision possible.
- Use `--terragrunt-include-dir` / `--terragrunt-exclude-dir` to limit.

---

## 7️⃣ Module versioning

### Vấn đề

Module `modules/vpc/` in monorepo. Update breaks dev env without breaking prod.

→ Version modules.

### Pattern: external module repo

Separate repo `infrastructure-modules`:
```
infrastructure-modules/   (different repo)
├── vpc/
├── eks/
├── rds/
└── ...
```

Tag releases: `v1.2.0`, `v1.3.0`, etc.

### Reference in Terragrunt

```hcl
# live/dev/us-east-1/vpc/terragrunt.hcl
terraform {
  source = "git::git@github.com:acme/infrastructure-modules.git//vpc?ref=v1.2.0"
}

# live/prod/us-east-1/vpc/terragrunt.hcl
terraform {
  source = "git::git@github.com:acme/infrastructure-modules.git//vpc?ref=v1.0.0"
  # prod pinned older version
}
```

→ Update dev to `v1.3.0` first → test → promote prod to `v1.3.0` later.

### Tagging workflow

```bash
# In modules repo
git tag v1.3.0
git push origin v1.3.0

# In live infra
# Update terragrunt.hcl ref=v1.3.0
terragrunt plan   # downloads v1.3.0
terragrunt apply
```

---

## 8️⃣ Multi-account pattern

### Setup AssumeRole

3 AWS accounts:
- Root account (no resources).
- Dev account (111111111111).
- Prod account (222222222222).

Each child account has role `TerraformExecutionRole` trusting root.

Terragrunt provider config:
```hcl
generate "provider" {
  path = "provider.tf"
  contents = <<EOF
provider "aws" {
  region = var.region
  
  assume_role {
    role_arn = "arn:aws:iam::$${var.aws_account_id}:role/TerraformExecutionRole"
  }
}
EOF
}
```

→ Per-env `aws_account_id` in `account.hcl`. Terragrunt assume role of target account.

### Benefits

- **Blast radius isolation**: dev mistakes can't affect prod.
- **IAM separation**: dev access only via assume role.
- **Cost tracking**: per-account billing.
- **Compliance**: prod account has stricter SCPs.

### Cross-account dependency

Sometimes prod EKS needs dev VPC peering. Terragrunt `dependency` works cross-account if state in shared bucket.

```hcl
dependency "dev_vpc" {
  config_path = "../../../dev/us-east-1/vpc"
  # State bucket might be different — root config handles
}
```

---

## 9️⃣ Hands-on: Refactor 75-folder repo to Terragrunt

### Before

```
infra/dev/us-east-1/vpc/main.tf        (200 lines)
infra/dev/us-west-2/vpc/main.tf        (copy)
infra/dev/eu-west-1/vpc/main.tf        (copy)
infra/staging/us-east-1/vpc/main.tf    (copy)
infra/prod/us-east-1/vpc/main.tf       (copy)
...  (75 folders, ~15K lines)
```

### After: Terragrunt structure

```
infrastructure/
├── terragrunt.hcl                       (50 lines, root config)
├── modules/
│   └── vpc/main.tf                       (200 lines, ONE copy)
└── live/
    ├── dev/
    │   ├── account.hcl                   (5 lines)
    │   ├── us-east-1/
    │   │   ├── region.hcl                (4 lines)
    │   │   └── vpc/terragrunt.hcl        (15 lines)
    │   ├── us-west-2/
    │   │   ├── region.hcl
    │   │   └── vpc/terragrunt.hcl
    │   └── eu-west-1/...
    ├── staging/...
    └── prod/...
```

**Code reduction**: 15K lines → 200 lines module + 15 × 15 = 225 lines config = **~400 lines total**. **97% reduction**.

### Migration workflow

1. **Audit existing**: list all current Terraform configs, identify common code.
2. **Extract module**: copy `dev/us-east-1/vpc/main.tf` → `modules/vpc/main.tf`. Parameterize via variables.
3. **Create live structure**: `live/dev/us-east-1/vpc/terragrunt.hcl` referencing module + dev/us-east-1 vars.
4. **Test 1 env**: `terragrunt plan` should show no changes (state same).
5. **Migrate state if needed**: if state path changes, use `terragrunt state mv`.
6. **Repeat per env**.
7. **Delete old folders**.

### Promotion workflow

Dev updates module to `v1.3.0`:
```bash
cd live/dev/us-east-1/vpc
# Update ref=v1.3.0 in terragrunt.hcl
terragrunt plan
terragrunt apply
```

If OK, promote staging:
```bash
cd live/staging/us-east-1/vpc
# Update ref=v1.3.0
terragrunt plan
terragrunt apply
```

Repeat regions + envs.

`run-all` for batch:
```bash
cd live/dev   # dev only
terragrunt run-all plan
```

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: `run-all destroy` accident

```bash
cd live/prod
terragrunt run-all destroy   # destroys ALL prod resources!
```

→ Cluster gone in 5 minutes.

→ **Fix**:
- **Always `--terragrunt-non-interactive` removed** — require confirmation.
- **RBAC**: `terraform destroy` permission only for specific roles.
- **State backup**: S3 versioning + DynamoDB enable.
- **No prod `run-all`** — apply individual modules only.

### ❌ Pitfall: Mock outputs different from real

```hcl
mock_outputs = {
  vpc_id = "vpc-12345"
  subnet_ids = []                    # ← empty!
}
```

→ `terragrunt plan` works, `apply` fails because EKS needs ≥2 subnets.

→ **Fix**: Mock outputs realistic. Test apply periodically.

### ❌ Pitfall: Circular dependency

```
A depends on B
B depends on C
C depends on A    ← cycle!
```

→ `run-all apply` infinite loop / error.

→ **Fix**: Refactor to break cycle. Often C → split into C1 (no A dep) + C2 (uses A).

### ❌ Pitfall: Manual `backend.tf` in module folder

```
modules/vpc/
├── main.tf
└── backend.tf      ← DON'T! Terragrunt generates this
```

→ Conflicts with Terragrunt `generate "backend"`.

→ **Fix**: Module folder has NO `backend.tf` or `provider.tf`. Terragrunt generates per env.

### ❌ Pitfall: Hardcoded account_id in modules

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"   # ← env-specific should be variable!
}
```

→ Module not reusable across envs.

→ **Fix**: Make module parameterized. `variable "cidr_block" {}`.

### ❌ Pitfall: Lock duration set too long

```hcl
remote_state {
  config = {
    dynamodb_table = "tflocks"
    # No lock TTL!
  }
}
```

→ Crashed apply leaves lock forever. Manual unlock needed.

→ **Fix**: 
- Terragrunt timeout: `--terragrunt-fetch-dependency-output-from-state` shorter timeout.
- Manual unlock: `terragrunt force-unlock <lock-id>`.
- Atlantis (next lesson) handles automatically.

### ❌ Pitfall: Module monorepo + git ref pointing branch

```hcl
source = "git::...//vpc?ref=main"   # ← main moves!
```

→ Same `terragrunt.hcl`, different apply over time. Reproducibility broken.

→ **Fix**: Always pin to **tag** or **commit SHA**:
```hcl
source = "git::...//vpc?ref=v1.2.0"          # tag
source = "git::...//vpc?ref=abc123def4567890" # SHA
```

### ✅ Best practice: Use `dependency` over `data` source

```hcl
# ❌ Use data source to read state
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = { bucket = "...", key = "..." }
}

# ✅ Use Terragrunt dependency
dependency "vpc" {
  config_path = "../vpc"
}
```

→ Dependency block: Terragrunt manages ordering, fail if VPC not applied yet (cleaner error).

### ✅ Best practice: Lock terragrunt version

```hcl
# .terragrunt-version
0.55.0
```

→ Tools like `tgenv` (Terragrunt env manager) install correct version per repo.

→ Team consistency.

### ✅ Best practice: Pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terragrunt_validate
      - id: terragrunt_fmt
      - id: terraform_tflint
      - id: terraform_tfsec
```

→ Auto-format + validate + security scan before commit.

---

## 🧠 Self-check

**Q1.** Terragrunt vs Terraform workspaces — chọn khi nào?

<details>
<summary>💡 Đáp án</summary>

**Workspaces** (basic Terraform):
- Same backend, different state per workspace.
- Same directory, switch via `terraform workspace`.
- Variables via `<workspace>.tfvars`.
- 1 provider config.

**Best for**:
- Simple multi-env (dev/staging/prod), same AWS account.
- Same region (or region as variable).
- Small team, < 5 modules.

**Terragrunt**:
- Different backend per env (state isolation).
- Different folders per env-region.
- Different account/region configs.
- Dependency management between modules.

**Best for**:
- Multi-account (env in separate AWS accounts).
- Multi-region with different config.
- 10+ modules with dependencies.
- Module versioning across envs (dev v1.3, prod v1.0).

**Decision**:
- **1 account, 1 region, < 5 modules**: workspaces.
- **Multi-account OR multi-region OR > 10 modules**: Terragrunt.

Hybrid: Terraform Cloud workspaces (different from `terraform workspace`) overlap with Terragrunt features.

Migration: workspaces → Terragrunt is straightforward (state copy + refactor structure).
</details>

**Q2.** Why generate `backend.tf` instead of putting in module?

<details>
<summary>💡 Đáp án</summary>

**Without Terragrunt** (backend in module):
```
modules/vpc/
├── main.tf
└── backend.tf      # bucket = "...", key = "vpc/terraform.tfstate"
```

→ Same backend for ALL envs! All envs share state. Conflict + dangerous.

**Workaround**: parameterize backend? Doesn't work — Terraform backend can't use variables.

```hcl
# DOES NOT WORK
backend "s3" {
  bucket = "${var.env}-tfstate"   # ERROR
}
```

→ Backend config can't use variables (chicken-and-egg: need backend before init, vars come after).

**Workaround**: backend partial config + `-backend-config` flag:
```bash
terraform init -backend-config="bucket=acme-dev-tfstate"
```

→ Works but manual + verbose.

**Terragrunt solution**:
- `generate "backend"` writes `backend.tf` in **current child folder** before `terraform init`.
- Content from root `terragrunt.hcl` with interpolated values (path, env).
- Per-env unique state automatically.

```hcl
remote_state {
  backend = "s3"
  generate = {
    path = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = "acme-tfstate-${get_aws_account_id()}"
    key = "${path_relative_to_include()}/terraform.tfstate"
    # ...
  }
}
```

→ Each child folder gets correct backend, no manual config.

**Key insight**: Terragrunt sits OUTSIDE Terraform. Generates files Terraform reads. Avoid Terraform backend variable limitation.
</details>

**Q3.** Dependency `mock_outputs` — vì sao cần?

<details>
<summary>💡 Đáp án</summary>

**Scenario**: brand new env (dev), no resources exist yet. Want to plan EKS.

EKS Terragrunt has `dependency "vpc"`. VPC not applied yet → state empty → `dependency.vpc.outputs.vpc_id` = undefined → plan fails.

**Mock outputs** solve:
```hcl
dependency "vpc" {
  config_path = "../vpc"
  
  mock_outputs = {
    vpc_id = "vpc-mock"
    private_subnet_ids = ["subnet-mock-1", "subnet-mock-2"]
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}
```

→ Plan can render templates with mock values. Apply requires real (mock_outputs not used for apply).

**Workflow**:
1. `terragrunt plan` EKS → uses mock_outputs → shows what EKS WILL create.
2. Realize need VPC first.
3. `terragrunt apply` VPC → real outputs available.
4. `terragrunt apply` EKS → uses real VPC outputs.

**`mock_outputs_allowed_terraform_commands`** restricts mock use to safe commands (plan, validate). Apply/destroy must use real outputs.

**Best practice**:
- Mock outputs **realistic** (real-looking IDs, valid CIDR, etc.).
- Mock outputs match types (list vs scalar).
- Test full apply periodically to ensure mocks don't drift from reality.

→ Mock outputs = developer convenience for planning across not-yet-applied modules.
</details>

**Q4.** `run-all` parallel limits — gì cần biết?

<details>
<summary>💡 Đáp án</summary>

**`terragrunt run-all apply`** behavior:
- Scans all `terragrunt.hcl` recursively.
- Builds dependency graph.
- Applies in **topological order** (dependencies first).
- **Parallelizes independent modules** at same level.

**Default parallelism**: all independent modules at once.

**Issues**:

1. **AWS API rate limits**: 100+ modules applied in parallel → API throttling.

```bash
# Limit parallelism
terragrunt run-all apply --terragrunt-parallelism 5
```

2. **Lock collision**: 2 modules same DynamoDB lock → wait.

3. **Resource limits**: each Terraform process = ~100MB RAM. 50 modules = 5GB. CI runner OOM.

4. **Network**: 50 parallel `terraform init` downloads providers concurrently.

**Solutions**:
- `--terragrunt-parallelism N` — cap concurrency.
- Group apply by stage (prod-vpc → all → prod-eks → all → prod-apps).
- Atlantis (next lesson) queue apply intelligently.

**Production pattern**: Atlantis runs `terragrunt plan/apply` per module, not `run-all`. Avoids cascade risk.

**`run-all` good for**:
- Local development (apply all in dev quickly).
- Disaster recovery (rebuild from scratch in DR region).
- New env bootstrap.

**`run-all` bad for**:
- Production apply (use Atlantis with explicit PR).
- Destroy operations (use module-by-module).

→ `run-all` is power tool. Use intentionally.
</details>

**Q5.** Module versioning via Git tag — how rollback?

<details>
<summary>💡 Đáp án</summary>

**Scenario**: dev applied module v1.3.0, broke something. Need rollback to v1.2.0.

**Step 1**: Update terragrunt.hcl:
```hcl
source = "git::...//vpc?ref=v1.2.0"
```

**Step 2**: 
```bash
cd live/dev/us-east-1/vpc
terragrunt plan
```

Terragrunt:
- Downloads v1.2.0 of module.
- Reads current state (was applied with v1.3.0).
- Diff: shows changes to revert from v1.3.0 → v1.2.0.

**Step 3**:
```bash
terragrunt apply
```

Applies reverse changes.

**Caveats**:

1. **Destructive operations possible**: v1.3.0 added column to RDS, v1.2.0 doesn't have → `terraform plan` shows column drop. **Loss of data**.

   Fix: Add `lifecycle { prevent_destroy = true }` on critical resources.

2. **Resource recreation**: some changes (e.g., subnet CIDR) require destroy + recreate. Downtime.

   Fix: `lifecycle { create_before_destroy = true }` where possible.

3. **State migration**: v1.3.0 added new output. v1.2.0 doesn't. `terragrunt apply` removes output → other dependent modules break.

   Fix: Phased rollback. Update dependent modules first.

**Best practice**:
- **Test in dev first** before promoting tag to prod.
- **Tag every release** for easy rollback.
- **Document breaking changes** in module CHANGELOG.
- **Major version bump** for breaking changes (SemVer).

**Disaster recovery**:
- S3 versioning on state bucket = restore previous state file if needed.
- Combined with git revert of terragrunt.hcl = full rollback path.

→ Module versioning + state versioning = safety net for prod IaC changes.
</details>

---

## ⚡ Cheatsheet

```bash
# === Terragrunt basics ===
terragrunt --version
terragrunt init
terragrunt plan
terragrunt apply
terragrunt destroy
terragrunt show
terragrunt output

# === Run-all ===
terragrunt run-all plan
terragrunt run-all apply
terragrunt run-all apply --terragrunt-parallelism 5
terragrunt run-all apply --terragrunt-include-dir live/dev
terragrunt run-all apply --terragrunt-exclude-dir live/prod

# === State commands ===
terragrunt state list
terragrunt state show <resource>
terragrunt state mv <source> <dest>
terragrunt state rm <resource>
terragrunt force-unlock <lock-id>

# === Inspect dependency graph ===
terragrunt graph-dependencies
# Output: DAG of all modules
```

```hcl
# === terragrunt.hcl template ===
include "root" {
  path = find_in_parent_folders()
}

locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
}

dependency "vpc" {
  config_path = "../vpc"
  mock_outputs = { vpc_id = "vpc-mock" }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

terraform {
  source = "git::git@github.com:acme/infra-modules.git//eks?ref=v1.3.0"
}

inputs = {
  cluster_name = "${local.account_vars.locals.env}-eks"
  vpc_id       = dependency.vpc.outputs.vpc_id
  subnet_ids   = dependency.vpc.outputs.private_subnet_ids
}
```

```bash
# === Built-in functions ===
get_aws_account_id()
get_terraform_command()
get_terraform_commands_that_need_locking()
get_env("ENV_VAR", "default")
path_relative_to_include()
path_relative_from_include()
find_in_parent_folders("filename.hcl")
read_terragrunt_config("file.hcl")
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Terragrunt** | Wrapper around Terraform for DRY config |
| **Terraform module** | Reusable Terraform code (variables + resources + outputs) |
| **`live/` folder** | Per-env Terragrunt config |
| **`modules/` folder** | Reusable Terraform module code |
| **`terragrunt.hcl`** | Per-folder Terragrunt config file |
| **`include` block** | Inherit parent terragrunt.hcl config |
| **`generate` block** | Auto-write file (backend.tf/provider.tf) before Terraform |
| **`dependency` block** | Reference outputs of another module |
| **`mock_outputs`** | Fake values for plan when dependency not applied yet |
| **`run-all`** | Apply across multiple modules in dependency order |
| **Topological order** | Order respecting dependencies (DAG) |
| **`source`** | Reference Terraform module location (local/git/registry) |
| **Module versioning** | Pin module to specific tag/SHA |
| **Cross-account** | Multi-AWS-account setup with assume role |
| **DRY** | Don't Repeat Yourself principle |
| **`find_in_parent_folders()`** | Built-in: walk up tree to find file |
| **`path_relative_to_include()`** | Path from root config to current |
| **driftctl** | OSS drift detection tool (next lesson) |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_intermediate-overview.md](00_intermediate-overview.md)
- → Tiếp: [02_atlantis-gitops-for-iac.md](02_atlantis-gitops-for-iac.md) *(sắp viết)*
- ↑ Cluster: [IaC README](../../README.md)

### Cross-reference
- 🏗️ [Basic Modules & Workspaces](../01_basic/03_modules-and-workspaces.md)
- ☸️ [K8s Helm sub-charts](../../../kubernetes/lessons/02_intermediate/01_helm-package-manager.md) — same DRY concept

### Tài nguyên ngoài
- 📖 [Terragrunt docs](https://terragrunt.gruntwork.io/)
- 📖 [Gruntwork Terragrunt Examples](https://github.com/gruntwork-io/terragrunt-infrastructure-live-example)
- 📖 [Terragrunt Best Practices](https://terragrunt.gruntwork.io/docs/getting-started/best-practices/)
- 📖 [terragrunt-atlantis-config](https://github.com/transcend-io/terragrunt-atlantis-config) — bridge tool
- 📖 [pre-commit-terraform](https://github.com/antonbabenko/pre-commit-terraform)

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Install + Standard layout + Workflow + Key features.

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Lesson 01 intermediate. Terragrunt vs workspaces + `live/` + `modules/` structure + root + account + region + child terragrunt.hcl + generate backend/provider + dependency block + run-all + module versioning + multi-account assume role + migration workflow. 7 pitfall + 3 best practice + 5 self-check + cheatsheet.
