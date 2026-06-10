# 🎓 IaC là gì? — Infrastructure as Code overview

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Docker](../../../docker/), [K8s](../../../kubernetes/)

> 🎯 *Bài INTRO. Hiểu **IaC** là gì, **declarative vs imperative**, **landscape 2026** (Terraform/OpenTofu/Pulumi/CDK/CloudFormation), **state management**, **why IaC** (reproducibility, version control, auto), **GitOps adjacent**.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **IaC** + history (CFEngine → Puppet → Chef → Terraform)
- [ ] **Declarative** vs **Imperative** approach
- [ ] **Mutable** vs **Immutable** infrastructure
- [ ] 6 tools landscape 2026
- [ ] **State** quan trọng (Terraform's killer feature)
- [ ] IaC vs **Config Management** (Ansible) vs **Container orchestration**
- [ ] **GitOps** + IaC integration

---

## 1️⃣ IaC là gì?

**Infrastructure as Code** = quản lý infra (servers, networks, DBs, K8s, ...) qua **code/config files**, version-controlled, automated provisioning.

### Click-ops vs IaC

**Click-ops** (manual):
- Click AWS Console: create EC2 instance, attach disk, security group, ...
- Click 50 times → 1 server.
- Production: 100+ resources × manual = error-prone, slow, irreproducible.

**IaC**:
```hcl
# terraform/main.tf
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  tags = { Name = "web-prod" }
}
```

```bash
terraform apply   # ← Create instance + dependencies
```

→ Code = source of truth. Re-apply = same result. Diff between envs = git diff.

---

## 2️⃣ Why IaC?

IaC giải quyết **8 vấn đề** quen thuộc của infra management — từ reproducibility đến onboarding. Quy mô càng lớn, benefit càng rõ. 2026 IaC không còn là tùy chọn:

| Benefit | Example |
|---|---|
| **Reproducibility** | Recreate prod env in 30 min |
| **Version control** | Git log = audit trail |
| **Code review** | PR review infra changes |
| **Drift detection** | `terraform plan` shows what differs from code |
| **Disaster recovery** | Apply IaC → infra back |
| **Multi-env consistency** | dev/staging/prod from same templates |
| **Cost tracking** | tag everything, audit cost |
| **Onboarding** | New dev `terraform apply` → working stack |

### Without IaC

Scenario điển hình **không** dùng IaC — click-ops manual qua AWS Console, mỗi env làm tay riêng. Sau vài tháng staging ≠ prod, debug khó vì không có source of truth:

```
Day 1: Nguyen Van A click-ops staging env
Day 30: Le Van B click-ops prod env
Day 60: Tran Van C debug "why staging different from prod?"
        → 200 differences. Pain.
```

### With IaC

Cùng nhu cầu nhưng dùng IaC — **1 module Terraform** apply nhiều lần với vars khác nhau. Staging và prod **identical structure**, chỉ khác vars (instance type, replicas, region):

```
1 module → apply staging (var.env=staging)
       → apply prod (var.env=prod)
       → identical structure, vars differ
```

→ **2026 reality**: team production-grade bắt buộc dùng IaC. Không còn là tùy chọn.

---

## 3️⃣ Declarative vs Imperative

### Declarative — Tell WHAT (Terraform, K8s)

Declarative IaC chỉ định **trạng thái mong muốn** (3 instances), tool tự figure out cách đạt (create/delete/update). **Idempotent** — apply 10 lần = vẫn 3 instance. Đây là default 2026:

```hcl
resource "aws_instance" "web" {
  count         = 3                       # ← Want 3 instances
  instance_type = "t3.medium"
}
```

→ Tool figures out HOW (create, delete, update). Idempotent.

### Imperative — Tell HOW (bash, AWS CLI)

Imperative IaC chỉ định **các bước cụ thể** — run 3 lần `aws ec2 run-instances`. Chạy lại = tạo thêm (không idempotent). Phù hợp one-off task, không phải infra management:

```bash
aws ec2 run-instances --count 1 --instance-type t3.medium
aws ec2 run-instances --count 1 --instance-type t3.medium
aws ec2 run-instances --count 1 --instance-type t3.medium
```

→ Run twice = 6 instances. Not idempotent.

| Aspect | Declarative | Imperative |
|---|---|---|
| Idempotent | ✅ | ❌ |
| State tracked | ✅ Auto | Manual |
| Easier diff | ✅ | ❌ |
| Drift detection | ✅ | ❌ |
| Tools | Terraform, K8s YAML, CloudFormation | Bash, Ansible (mostly), AWS CLI |

→ **2026 default**: declarative IaC. Imperative for one-off tasks.

---

## 4️⃣ Landscape 2026 — Tools

| Tool | Year | Type | Notes |
|---|---|---|---|
| **Terraform** | 2014 | Declarative, HCL | **De-facto standard** 2026 |
| **OpenTofu** | 2023 | Terraform fork (Linux Foundation) | Reaction to license change |
| **Pulumi** | 2018 | Declarative, multi-language (Python/TS/Go) | Real programming languages |
| **AWS CDK** | 2019 | Declarative, TS/Python → CloudFormation | AWS-only convenient |
| **CloudFormation** | 2011 | Declarative YAML/JSON | AWS-native, verbose |
| **CDK for Terraform** | 2020 | TS/Python → Terraform | Mix CDK syntax + TF backend |
| **Ansible** | 2012 | Procedural, agentless | Config management (different category) |
| **Chef / Puppet** | 2009/2005 | Procedural with agents | Legacy config management |

### Compare

| Tool | Pros | Cons | 2026 status |
|---|---|---|---|
| **Terraform** | Multi-cloud, huge module library, mature | License change worry | **#1** dominant |
| **OpenTofu** | OSS forever, drop-in TF replacement | Newer | Growing fast |
| **Pulumi** | Real programming language, loops/conditions | Smaller community | Growing |
| **CDK** | Familiar TS/Python | AWS only | Strong AWS shops |
| **CloudFormation** | Native AWS, no extra tool | YAML pain, AWS only | Legacy AWS |

### License drama 2023-2024

- HashiCorp changed Terraform from MPL (OSS) → BSL (source-available) Aug 2023.
- Community fork → **OpenTofu** (Linux Foundation, Sep 2023).
- **2026**: Most new projects choose **OpenTofu** (license freedom). Existing Terraform stable.
- Drop-in compatible — `tofu` command replaces `terraform`.

### Choose

| Use case | Pick |
|---|---|
| **Default 2026 new project** | **OpenTofu** (or Terraform if locked-in) |
| **Multi-cloud** | OpenTofu/Terraform |
| **AWS-only enterprise** | CDK (TypeScript familiar) |
| **Mixed (containers + infra)** | OpenTofu/Terraform |
| **Prefer programming language** | Pulumi |
| **Legacy AWS migration** | CloudFormation → migrate |

→ This cluster teaches **Terraform/OpenTofu** (cú pháp identical).

---

## 5️⃣ State — Terraform's killer feature

**Problem**: how does Terraform know what exists?

**Solution**: **state file** (`terraform.tfstate`) — JSON snapshot of managed resources.

```
terraform.tfstate
{
  "resources": [
    {
      "type": "aws_instance",
      "name": "web",
      "instances": [
        { "id": "i-0abc123", "private_ip": "10.0.0.5", ... }
      ]
    }
  ]
}
```

### Flow

```
1. Write .tf code (desired)
2. terraform plan
   - Read state (what currently exists)
   - Compare desired vs actual
   - Output: "+create X, -destroy Y, ~update Z"
3. terraform apply
   - Execute plan
   - Update state file
```

### State backend

Local state = `terraform.tfstate` file. **Production**: remote state.

| Backend | Use case |
|---|---|
| **S3 + DynamoDB** | AWS, locking via DynamoDB |
| **Azure Blob** | Azure |
| **GCS** | GCP |
| **Terraform Cloud** | HashiCorp managed, UI + collaboration |
| **Atlantis / Spacelift / env0** | Self-host + CI/CD integration |

```hcl
# Configure remote state
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

### State locking

Multi-engineer: 2 people `apply` same time → race condition. **DynamoDB lock**:

```
Nguyen Van A: terraform apply
  → acquire lock in DynamoDB
  → proceed
Le Van B: terraform apply (same time)
  → lock held → error "lock already exists"
  → retry after Nguyen Van A done
```

→ State locking prevents corruption. **Production essential**.

### Chi tiết — Bài 02

---

## 6️⃣ Mutable vs Immutable Infrastructure

### Mutable — Update in place

```
Day 1: Create EC2 with Ubuntu 22.04
Day 30: SSH + apt update + install Python
Day 60: Run scripts, modify config
Day 90: "Why server behaves weird?" — drift
```

→ Each server = unique snowflake. Hard reproduce. Configuration drift.

### Immutable — Replace, don't update

```
Day 1: Create EC2 from AMI v1.0
Day 30: New version → bake AMI v2.0 → replace EC2 (terminate old, create new)
Day 60: AMI v3.0 → replace
```

→ Every server fresh from baked image. **No drift**. Tools: **Packer** (HashiCorp) bake AMI, **Docker images** for K8s.

| Aspect | Mutable | Immutable |
|---|---|---|
| Update | In place | Replace |
| Drift | High | None |
| Rollback | Tricky | Easy (deploy old image) |
| Modern | ❌ | **2026 default** |

→ **Immutable infra** + IaC = perfect combo. Containers (Docker) naturally immutable.

---

## 7️⃣ IaC vs Config Management vs Orchestration

### IaC — Provision **infrastructure**

```
Terraform/OpenTofu/Pulumi
- Create VPC, EC2, RDS, ALB
- Cloud-level resources
```

### Config Management — Configure **existing servers**

```
Ansible/Chef/Puppet
- Install packages
- Configure files (/etc/nginx/...)
- Manage services (systemd start nginx)
- SSH into servers, apply playbook
```

### Container Orchestration — Schedule **containers**

```
Kubernetes/Nomad
- Schedule containers
- Auto-scale, self-heal
- Service discovery
```

### Mixed in real life

```
Terraform create:
  - VPC, subnets, security groups
  - EKS cluster (K8s)
  - RDS Postgres
  - ALB

K8s (declarative YAML) deploys apps inside EKS.

Ansible NOT needed for containers (Docker = immutable).
Ansible STILL useful for legacy VM-based apps.
```

→ **2026 stack**: Terraform + K8s + (no Ansible if all-container). Ansible for hybrid legacy.

---

## 8️⃣ Workflow — Daily IaC

### Local

```bash
# 1. Write code
vim main.tf

# 2. Format + validate
terraform fmt
terraform validate

# 3. Plan
terraform plan -out=plan.out
# Review: + create, - destroy, ~ update

# 4. Apply
terraform apply plan.out
# Confirm: yes

# 5. Commit
git add . && git commit -m "feat: add db cluster"
git push
```

### CI/CD

```yaml
# .github/workflows/terraform.yml
on:
  pull_request:
  push: { branches: [main] }

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: hashicorp/setup-terraform@v3
    - run: terraform init
    - run: terraform plan -out=plan.out
    - if: github.event_name == 'pull_request'
      run: terraform show -no-color plan.out > plan.txt
    - if: github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          const plan = fs.readFileSync('plan.txt', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `\`\`\`\n${plan}\n\`\`\``
          });

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
    - uses: actions/checkout@v4
    - uses: hashicorp/setup-terraform@v3
    - run: terraform init
    - run: terraform apply -auto-approve
```

→ PR: plan posted as comment. Reviewer approve → merge → apply prod.

### Tools

| Tool | Purpose |
|---|---|
| **terraform/tofu** | Core |
| **tflint** | Lint |
| **terraform-docs** | Auto-generate README |
| **checkov / tfsec** | Security scan |
| **Infracost** | Estimate cost from PR |
| **Atlantis** | PR-driven Terraform automation |
| **Terragrunt** | Multi-env DRY wrapper |

---

## 9️⃣ GitOps — IaC + Git auto-sync

**GitOps** = git repo = source of truth. **Operator** sync git → infra/K8s.

### IaC GitOps (Atlantis)

```
1. PR Terraform change
2. Atlantis bot comment plan
3. Reviewer approve
4. Merge to main
5. Atlantis auto-apply
6. State updated in S3
```

### K8s GitOps (ArgoCD)

```
1. PR K8s manifest change
2. Reviewer approve
3. Merge to main
4. ArgoCD sync (continuous)
5. K8s reconcile
```

→ **2026 trend**: GitOps everywhere. Pull-based (operator pull from git) vs push-based (CI push). Pull = ArgoCD/Flux preferred.

---

## 1️⃣0️⃣ Lộ trình học Terraform/OpenTofu

```
Week 1 — Basics
  ☐ Install + first resource (S3 bucket)
  ☐ Plan + apply + destroy workflow
  ☐ Variables + outputs

Week 2 — State + Backend
  ☐ Remote state (S3 + DynamoDB lock)
  ☐ Workspaces (env separation)
  ☐ terraform import existing resources

Week 3 — Modules + Patterns
  ☐ Write reusable modules
  ☐ Use Terraform Registry modules
  ☐ Composition patterns

Week 4 — Production
  ☐ CI/CD integration
  ☐ Security scanning (tfsec, checkov)
  ☐ Cost estimation (Infracost)
  ☐ Drift detection
```

→ Sau 4 tuần đủ deploy + manage production infra.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Click-ops + Terraform mix** → drift, IaC code wrong. **No click-ops** for resources Terraform manages.
2. **Commit `.tfstate` to git** → secrets exposed (DB passwords, keys). **Remote state** + `.gitignore`.
3. **No state locking** → 2 engineers `apply` concurrent corrupt state. **DynamoDB / GCS object lock**.
4. **Imperative inside IaC** (local-exec for create users) → not idempotent. Pure declarative resources.
5. **No drift detection** → manual changes break IaC sync. `terraform plan` daily + CI check.

---

## 🧠 Tự kiểm tra (Self-check)

1. **Click-ops** vs **IaC** — pros/cons mỗi cái?
2. **Declarative** vs **Imperative** — chọn cái nào cho IaC?
3. Tại sao **state** quan trọng?
4. **Terraform** vs **OpenTofu** — 2026 chọn?
5. **IaC** vs **Config management** vs **Orchestration** — phân biệt?

<details>
<summary>Gợi ý đáp án</summary>

1. **Click-ops**: easy single resource, no learning curve. But: irreproducible, no audit, drift, error-prone scale. **IaC**: learning curve + setup, but reproducible, version-control, code review, drift detection, multi-env consistency, disaster recovery. **2026**: IaC mandatory production.

2. **Declarative for IaC**. Tell WHAT (3 instances) → tool calculate HOW. Idempotent (apply 10× = apply 1×). State tracked. Easy diff and drift detection. Imperative for one-off ops scripts (bash, AWS CLI) — not for repeatable infra.

3. **State** = bridge between code (desired) and reality (actual). Without: tool blindly apply, can't detect "this already exists" → create duplicates. With state: plan = diff state vs code → minimal changes. Plus drift detection (state vs reality differs). **Killer feature** of Terraform.

4. **OpenTofu** for new projects 2026: OSS forever, drop-in TF compat, Linux Foundation. **Terraform** OK for existing locked-in but BSL license concern. Drop-in switch: `tofu` command. **Trend**: OpenTofu gaining majority new adoption.

5. **IaC (Terraform)** = provision infrastructure (VPC, EC2, RDS, K8s cluster). **Config management (Ansible)** = configure existing servers (install packages, files, services). **Orchestration (K8s)** = schedule containers. Modern stack: IaC create infra → K8s deploy containers → (Ansible legacy VMs if any).
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Terraform/OpenTofu workflow

```bash
terraform init                   # Setup
terraform fmt                     # Format
terraform validate                 # Syntax
terraform plan -out=plan.out      # Preview
terraform apply plan.out           # Execute
terraform destroy                  # Tear down
terraform show                     # Show state
terraform state list               # Resources tracked
terraform state mv X Y             # Refactor
terraform import RES ID            # Bring existing under management
```

### File structure

```
project/
├── main.tf           # Resources
├── variables.tf      # Input vars
├── outputs.tf        # Output vars
├── versions.tf       # Provider versions
├── terraform.tfvars  # Variable values (gitignore!)
└── README.md
```

### Tools 2026

```
OpenTofu     OSS Terraform fork (recommended)
Pulumi       Multi-language IaC
CDK          AWS TypeScript
Atlantis      PR-driven automation
tflint        Lint
tfsec         Security scan
Infracost     Cost estimation
Terragrunt   Multi-env DRY
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **IaC** | Infrastructure as Code |
| **Click-ops** | Manual cloud console operations |
| **Declarative** | Tell WHAT (Terraform) |
| **Imperative** | Tell HOW (Bash) |
| **State** | Snapshot of managed resources |
| **State backend** | Remote storage (S3, GCS) |
| **State locking** | Prevent concurrent apply |
| **Plan** | Preview changes |
| **Apply** | Execute changes |
| **Drift** | Real infra differs from code |
| **Mutable / Immutable** | Update in place vs replace |
| **Terraform / OpenTofu** | De-facto IaC tool |
| **Pulumi / CDK / CloudFormation** | Alternatives |
| **Atlantis** | PR-driven Terraform |
| **GitOps** | Git = source of truth, operator sync |
| **Module** | Reusable Terraform code |
| **Provider** | Cloud-specific resource definitions |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ➡️ **Bài tiếp theo:** [Terraform Basics — Providers, Resources, Variables](01_terraform-basics.md)
- ↑ **Về cụm:** [iac README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [Docker](../../../docker/) — immutable container images
- [Kubernetes](../../../kubernetes/) — K8s YAML = IaC for containers
- [CI/CD](../../../ci-cd/) — Terraform in pipeline

### 🌐 Tài nguyên tham khảo khác
- 📖 [Terraform docs](https://developer.hashicorp.com/terraform)
- 📖 [OpenTofu docs](https://opentofu.org/docs/)
- 📖 [Pulumi docs](https://www.pulumi.com/docs/)
- 📖 [AWS CDK docs](https://docs.aws.amazon.com/cdk/)
- 📖 [Terraform Up & Running — Yevgeniy Brikman](https://www.terraformupandrunning.com/) — bible
- 📖 [Infracost](https://www.infracost.io/)
- 📖 [Atlantis docs](https://www.runatlantis.io/)

---

> 🎯 *Sau bài này hiểu IaC landscape. Bài kế tiếp đi sâu **Terraform basics** — resources, providers, variables.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster iac basic lesson 1/5. Cover: IaC concept + 8 benefits + Without/With IaC + Declarative vs Imperative + tool landscape (Terraform/OpenTofu/Pulumi/CDK/Ansible/Crossplane).
- **v1.1.0 (25/05/2026)** — Bổ sung lead-in trước §2 Why IaC, ví dụ Without/With IaC và phần Declarative vs Imperative.
