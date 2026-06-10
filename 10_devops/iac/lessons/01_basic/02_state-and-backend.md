# 🎓 State & Backend — Production essentials

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Terraform Basics](01_terraform-basics.md)

> 🎯 *Deep state: **state file** format + secrets, **remote backends** (S3+DynamoDB / GCS / Azure), **state locking**, **`terraform state` commands** (mv/rm/import/list), **drift detection**, **state recovery**, **workspaces** intro.*

## 🎯 Sau bài này bạn sẽ

- [ ] Setup **remote backend** (S3 + DynamoDB)
- [ ] Master `terraform state` subcommands
- [ ] **Import** existing resources
- [ ] **Drift detection** workflow
- [ ] Handle **state corruption** recovery
- [ ] **Workspaces** for env separation (intro)
- [ ] Secret hygiene + encryption

---

## 1️⃣ State file — Inside

State file là **JSON snapshot** Terraform maintain để track resource đã tạo. Mỗi `apply` update file này. Chứa **mọi metadata** — bao gồm secrets (password, private key). Vì vậy state phải treat như secret:

```json
{
  "version": 4,
  "terraform_version": "1.6.5",
  "serial": 42,
  "lineage": "uuid",
  "outputs": {
    "vpc_id": { "value": "vpc-0abc123", "type": "string" }
  },
  "resources": [
    {
      "type": "aws_vpc",
      "name": "main",
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": [
        {
          "schema_version": 1,
          "attributes": {
            "id": "vpc-0abc123",
            "cidr_block": "10.0.0.0/16",
            "default_security_group_id": "sg-xyz",
            "tags": { "Name": "acmeshop-vpc" }
          }
        }
      ]
    }
  ]
}
```

→ JSON snapshot of all managed resources. Updated on every apply.

### Secrets in state

⚠️ State contains **everything** — including:
- Database passwords (if generated).
- Private keys.
- API tokens.
- IP addresses (sometimes sensitive).

→ **Implication**: state file is a **secret**. Treat accordingly.

### Local state — Dangerous

Default Terraform lưu state ở local file `terraform.tfstate` — 3 vấn đề lớn: commit Git → leak secrets, lose laptop → mất control, single point of failure (không collab được):

```
$ ls
main.tf  terraform.tfstate  terraform.tfstate.backup

$ cat terraform.tfstate
{... database password in cleartext ...}
```

→ ❌ Commit to git → leak. ❌ Lose laptop → can't manage infra. ❌ Single point of failure.

→ **Production: ALWAYS remote backend**.

---

## 2️⃣ Remote backend — S3 + DynamoDB

### Setup (bootstrap)

Bootstrap nghĩa là **tạo trước backend infra** (S3 bucket + DynamoDB table) bằng IaC riêng — chicken-and-egg problem giải bằng 1 lần manual hoặc bootstrap module riêng. S3 lưu state, DynamoDB lock concurrent applies:

```hcl
# bootstrap/main.tf — Run ONCE to create backend infra
resource "aws_s3_bucket" "tf_state" {
  bucket = "acmeshop-tf-state"
}

resource "aws_s3_bucket_versioning" "tf_state" {
  bucket = aws_s3_bucket.tf_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tf_state" {
  bucket = aws_s3_bucket.tf_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "tf_state" {
  bucket                  = aws_s3_bucket.tf_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "tf_locks" {
  name         = "tf-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

→ Apply once with **local state** to create the bucket + table. Then migrate.

### Configure backend in main project

```hcl
# main project — main.tf
terraform {
  backend "s3" {
    bucket         = "acmeshop-tf-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```

```bash
terraform init
# Initializing backend...
# Do you want to copy local state to S3? yes
```

→ State now in S3, locked via DynamoDB. Local file deleted (optional).

### Other backends

```hcl
# GCS
terraform {
  backend "gcs" {
    bucket = "acmeshop-tf-state"
    prefix = "production"
  }
}

# Azure
terraform {
  backend "azurerm" {
    storage_account_name = "acmeshoptfstate"
    container_name       = "tfstate"
    key                  = "prod.tfstate"
  }
}

# HTTP (custom)
terraform {
  backend "http" { address = "https://my-backend/" }
}

# Terraform Cloud
terraform {
  cloud {
    organization = "acmeshop"
    workspaces { name = "production" }
  }
}
```

→ Terraform Cloud / Spacelift / Atlantis / env0 = managed backends with UI + collaboration.

---

## 3️⃣ State locking — How it works

```
Nguyen Van A: terraform apply
  1. Acquire lock in DynamoDB (insert row LockID=xxx)
  2. Read state from S3
  3. Apply changes
  4. Write new state to S3
  5. Release lock

Le Van B: terraform apply (concurrent)
  1. Try acquire lock → row exists → error "lock held"
  2. Retry after Nguyen Van A done
```

### Lock errors

```
$ terraform apply
Error: Error acquiring the state lock
Lock Info:
  ID:        abc-123
  Path:      acmeshop-tf-state/production/terraform.tfstate
  Operation: OperationTypeApply
  Who:       nguyenvana@laptop
  Version:   1.6.5
  Created:   2026-05-23 14:32:01.234567 +0000 UTC
```

→ Wait for Nguyen Van A. If Nguyen Van A's process killed (didn't release):

```bash
# Force unlock (cẩn thận!)
terraform force-unlock <LOCK_ID>
```

→ Only use if **sure** other process not running. Force unlock during real apply = corrupt.

---

## 4️⃣ `terraform state` subcommands

### List

```bash
terraform state list
# aws_vpc.main
# aws_subnet.public["a"]
# aws_subnet.public["b"]
# aws_instance.web[0]
# aws_instance.web[1]
```

### Show

```bash
terraform state show aws_vpc.main
# Detailed attributes of resource
```

### Move (rename in code)

```bash
# Renamed in code: aws_vpc.main → aws_vpc.production
terraform state mv aws_vpc.main aws_vpc.production
# No re-create; just rename in state.

# Move into module
terraform state mv aws_vpc.main module.network.aws_vpc.main
```

→ **Critical**: renaming in code without `state mv` → Terraform destroy + recreate (downtime!). State mv preserves resource.

### Remove (from state, not from cloud)

```bash
terraform state rm aws_instance.web[0]
# Stops managing this resource (still exists in AWS).
```

→ Use case: stop managing legacy resource via Terraform but keep alive.

### Pull / Push (download/upload state)

```bash
terraform state pull > state-backup.json    # Download for backup
terraform state push state-backup.json       # Upload (DANGEROUS)
```

→ Backup before destructive operations.

### Refresh

```bash
terraform refresh
# Update state file to match actual infra (no apply changes to code-desired)
```

→ Detect external changes. Modern: `terraform apply -refresh-only`.

---

## 5️⃣ Import — Bring existing under management

Scenario: existing AWS resources (created click-ops) → bring into Terraform.

### Method 1 — `terraform import` (legacy)

```bash
# Write resource block (without attributes)
resource "aws_instance" "legacy" {
  # Will fill after import
}

# Import
terraform import aws_instance.legacy i-0abc123def456

# terraform plan → show diff
# Edit .tf to match attributes
# Iterate until plan = no changes
```

### Method 2 — `import` block (modern, Terraform 1.5+)

```hcl
# imports.tf
import {
  to = aws_instance.legacy
  id = "i-0abc123def456"
}

resource "aws_instance" "legacy" {
  # Define expected state
  ami           = "ami-..."
  instance_type = "t3.medium"
  # ...
}
```

```bash
terraform plan -generate-config-out=generated.tf
# Auto-generate resource block from current state
# Review + clean up
terraform apply
```

→ Better workflow — config gen via plan.

### When to import?

- Migrate from click-ops to IaC.
- Acquire company's infra.
- Modules require new resource address (state mv usually better).

---

## 6️⃣ Drift detection

**Drift** = actual infra differs from code (someone manually changed).

### Detect

```bash
terraform plan
# If drift exists → plan shows changes
# Example:
# ~ aws_instance.web[0]
#   ~ instance_type: "t3.medium" -> "t3.large"
#     (changed manually in console)
```

→ Plan = "what Terraform would do to align reality to code".

### Choices

1. **Revert** — `terraform apply` → reverts manual change.
2. **Adopt** — edit code to match new reality → re-apply.
3. **Investigate** — who/why changed? Improve process.

### CI drift detection

```yaml
# .github/workflows/drift-check.yml
on:
  schedule:
  - cron: '0 9 * * *'                       # Daily 9 AM

jobs:
  drift:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: hashicorp/setup-terraform@v3
    - run: terraform init
    - run: |
        terraform plan -detailed-exitcode
        # Exit 0: no changes
        # Exit 2: changes detected
    - if: failure()
      run: |
        ./notify-slack.sh "Drift detected in production!"
```

→ Daily check production matches code. Alert if not.

---

## 7️⃣ State corruption recovery

### Scenario 1 — Corrupted state file

```bash
# Restore from S3 versioning
aws s3api list-object-versions --bucket acmeshop-tf-state --prefix production/
# Find good version

aws s3api copy-object \
  --bucket acmeshop-tf-state \
  --copy-source 'acmeshop-tf-state/production/terraform.tfstate?versionId=xxx' \
  --key production/terraform.tfstate
```

→ S3 versioning saves life. **Always enable**.

### Scenario 2 — Deleted resource externally

```bash
terraform plan
# Shows "+ create" for resource that exists in state but not in cloud

# Option A: re-create (if OK)
terraform apply

# Option B: just remove from state (keep code, but accept gone)
terraform state rm aws_instance.legacy
```

### Scenario 3 — Force unlock + state stale

```bash
# Pull current state
terraform state pull > state.json

# Manual edit if needed (CAREFUL!)
# Push back
terraform state push state.json
```

→ Last resort. Backup before.

### Best practice

- ✅ **S3 versioning** enabled (recover any version).
- ✅ **Daily state backup** to separate bucket.
- ✅ **Tag state files** by date.
- ✅ **Test recovery** quarterly.

---

## 8️⃣ Workspaces — Lightweight env separation

```bash
terraform workspace list
# * default

terraform workspace new dev
terraform workspace new staging
terraform workspace new production

terraform workspace select production
terraform apply
```

### Each workspace = separate state

```
S3 bucket: acmeshop-tf-state
└── env:/
    ├── default/production/terraform.tfstate
    ├── dev/production/terraform.tfstate
    ├── staging/production/terraform.tfstate
    └── production/production/terraform.tfstate
```

→ Same code, different state per workspace.

### Use in code

```hcl
locals {
  name = "acmeshop-${terraform.workspace}"
}

resource "aws_instance" "web" {
  count = terraform.workspace == "production" ? 5 : 1
  # ...
}
```

### Workspaces vs directories

| Approach | Pros | Cons |
|---|---|---|
| **Workspaces** | Same code, easy switch | Easy mistake (wrong workspace) |
| **Separate dirs** (`environments/dev/`, `environments/prod/`) | Explicit, no mistake | Some code duplication |
| **Terragrunt** | DRY + explicit | Extra tool |

→ **2026 best practice**: separate directories (explicit). Workspaces for: small projects, ephemeral envs.

→ Workspaces detail + modules ở [bài 03](03_modules-and-workspaces.md).

---

## 9️⃣ Production setup của bạn

### Bootstrap (one-time)

```bash
cd bootstrap/
terraform init                              # Local state for bootstrap
terraform apply                              # Create S3 + DynamoDB
```

### Main project — Backend

```hcl
terraform {
  backend "s3" {
    bucket         = "acmeshop-tf-state"
    key            = "envs/production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```

### Directory structure

```
infra/
├── bootstrap/             # One-time S3+DynamoDB
├── modules/
│   ├── network/
│   ├── eks/
│   └── rds/
├── envs/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
└── README.md
```

### Daily workflow

```bash
cd envs/production
terraform init
terraform plan -out=plan
terraform apply plan
```

### CI/CD

```yaml
# Plan on PR, apply on merge main
jobs:
  plan:
    if: github.event_name == 'pull_request'
    - terraform plan
    - post plan as PR comment

  apply:
    if: github.ref == 'refs/heads/main'
    needs: plan
    environment: production    # Approval required
    - terraform apply
```

→ State managed centrally, locked, encrypted, recoverable.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Local state in production** → laptop dies = lose ability to manage. **Remote backend mandatory**.
2. **Commit `.tfstate` to git** → secrets leak forever. **`.gitignore` + remote backend**.
3. **No state locking** → 2 engineers apply concurrent = corrupt. DynamoDB/GCS lock.
4. **Force unlock during real apply** → corrupt state. Wait + verify other process.
5. **Rename resource without `terraform state mv`** → destroy + recreate (downtime). Always `state mv`.

---

## 🧠 Tự kiểm tra (Self-check)

1. Sao **local state** không OK production?
2. **S3 + DynamoDB** backend — vai trò mỗi cái?
3. **`terraform state mv`** vs editing code directly — khác sao?
4. **`terraform import`** — workflow?
5. **Drift detection** — daily CI sao?

<details>
<summary>Gợi ý đáp án</summary>

1. (a) Laptop = single point of failure. (b) No collaboration (only 1 person has state). (c) Secrets in state at risk leak. (d) No locking → concurrent apply corrupt. (e) No backup/version history. **Remote backend mandatory** production.

2. **S3**: store state file. Versioning enabled = recover any version. Encryption at rest. **DynamoDB**: state locking via item with `LockID`. Insert = lock acquired, delete = released. Prevent concurrent apply corruption.

3. **`state mv`**: rename in state file ONLY. Resource preserved in cloud. **Edit code only**: Terraform sees old name missing → destroy. New name → create. Result: **downtime + data loss** (if DB). Always `state mv` for rename.

4. (a) Write empty resource block. (b) `terraform import aws_x.name <ID>` (or `import` block + `-generate-config-out`). (c) `terraform plan` → diff. (d) Edit code to match. (e) Iterate until plan = no changes. Used for: migrate click-ops → IaC, acquire infra.

5. CI cron daily: `terraform plan -detailed-exitcode`. Exit 2 = drift detected. Alert Slack/PagerDuty. Investigate: was change auth? Revert (apply code) or adopt (update code). Daily check ensures code = reality production.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Backend S3 + DynamoDB

```hcl
terraform {
  backend "s3" {
    bucket         = "acmeshop-tf-state"
    key            = "envs/production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```

### State commands

```bash
terraform state list                              # All resources
terraform state show aws_x.name                    # Details
terraform state mv aws_x.old aws_x.new             # Rename
terraform state rm aws_x.name                      # Untrack
terraform state pull > backup.json                 # Backup
terraform import aws_x.name <id>                   # Bring under management
terraform force-unlock <lock_id>                   # Emergency
terraform apply -refresh-only                       # Sync state with reality
```

### Workspaces

```bash
terraform workspace new prod
terraform workspace select prod
terraform workspace list
```

### Best practices

```
[ ] Remote backend (S3 + DynamoDB)
[ ] S3 versioning enabled
[ ] State encryption
[ ] DynamoDB lock
[ ] CI drift detection daily
[ ] Backup state quarterly test recovery
[ ] No commit .tfstate
[ ] No edit state file manually
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **State file** | JSON snapshot of resources |
| **Backend** | Where state stored (S3, GCS, local) |
| **State locking** | Prevent concurrent apply |
| **DynamoDB lock** | AWS state lock implementation |
| **Drift** | Actual differs from code |
| **`terraform state mv`** | Rename in state |
| **`terraform import`** | Bring existing under management |
| **`force-unlock`** | Emergency unlock |
| **Workspace** | Named state instance |
| **Refresh** | Sync state with reality (no apply changes) |
| **Versioning** | S3 keeps old state versions |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Terraform Basics — Providers, Resources, Variables](01_terraform-basics.md)
- ➡️ **Bài tiếp theo:** [Modules & Multi-env — DRY + Reusability](03_modules-and-workspaces.md)
- ↑ **Về cụm:** [iac README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [Terraform State docs](https://developer.hashicorp.com/terraform/language/state)
- 📖 [Backend types](https://developer.hashicorp.com/terraform/language/settings/backends/configuration)
- 📖 [Terraform Cloud](https://www.hashicorp.com/products/terraform)
- 📖 [Spacelift](https://spacelift.io/) — managed Terraform alternative

---

> 🎯 *Sau bài này state production-grade. Bài kế tiếp dạy **modules + workspaces** — DRY + multi-env.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster iac basic lesson 3/5. Cover: state file structure + secrets in state + local vs remote + S3 + DynamoDB backend setup + state operations (import/mv/rm) + state encryption.
- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước §1 State file inside, Local state dangerous và §2 Setup bootstrap.
