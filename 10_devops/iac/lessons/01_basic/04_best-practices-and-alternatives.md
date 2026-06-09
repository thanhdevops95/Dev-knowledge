# 🎓 IaC Best Practices & Alternatives

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [Modules & Multi-env](03_modules-and-workspaces.md)

> 🎯 *Production best practices: **security scanning** (tfsec, checkov), **cost estimation** (Infracost), **policy as code** (OPA, Sentinel), **drift detection** automation, **CI/CD integration**, **secrets management**. Plus **alternatives** to Terraform: Pulumi, CDK, Crossplane.*

## 🎯 Sau bài này bạn sẽ

- [ ] **Security scanning** (tfsec, checkov, Snyk)
- [ ] **Cost estimation** với Infracost
- [ ] **Policy as code** (OPA + Sentinel)
- [ ] **Drift detection** CI/CD
- [ ] **Secrets management** integration (Vault, AWS SM)
- [ ] **CI/CD pattern** đầy đủ
- [ ] **Pulumi / CDK / Crossplane** comparison
- [ ] Common **anti-patterns** to avoid

---

## 1️⃣ Security scanning — tfsec, checkov

Tools scan `.tf` files for security issues.

### tfsec (Aqua, OSS)

`tfsec` là tool security scan đầu tiên đáng dùng — fast, 100+ rules, CWE-tagged. Cài 1 lệnh + chạy 1 lệnh. Phù hợp pre-commit hook hoặc CI gate:

```bash
brew install tfsec
tfsec .

# Output:
# Result #1 CRITICAL S3 bucket does not encrypt data with KMS.
#   tf-modules/s3/main.tf:5
#   bucket "logs" {
#     bucket = "acmeshop-logs"
#   }
```

→ 100+ rules. CWE-tagged. Fast.

### Checkov (Bridgecrew/Palo Alto)

`checkov` cover rộng hơn tfsec — 1000+ check across Terraform + CloudFormation + K8s + Dockerfile + helm. Slow hơn nhưng comprehensive. Dùng combo tfsec (fast feedback) + checkov (CI):

```bash
pip install checkov
checkov -d .

# Or specific framework
checkov --framework terraform -d .
```

→ 1000+ checks. Covers Terraform + CloudFormation + K8s + Dockerfile. Comprehensive.

### Snyk IaC

```bash
snyk iac test
```

→ Commercial, integrate Snyk platform.

### CI integration

Integrate scan vào CI/CD pipeline với GitHub Actions — `tfsec-action` output SARIF format, upload vào GitHub Security tab. Block merge nếu có CRITICAL finding:

```yaml
# .github/workflows/security.yml
jobs:
  iac-security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/tfsec-action@v1
      with:
        soft_fail: false                   # Fail PR on findings
        format: sarif
    - uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: tfsec-results.sarif
```

→ PR scanned. Findings show in Security tab. Block merge if critical.

### Common findings

8 lỗi security phổ biến nhất tfsec/checkov catch — đặc biệt S3 public, RDS no encryption, security group 0.0.0.0/0. Đây là baseline mọi infra production phải pass:

```
- S3 bucket public access
- RDS no encryption
- Security group 0.0.0.0/0 ingress (too open)
- No backup retention
- IAM policy too broad
- KMS key rotation disabled
- Logs not enabled
- HTTP instead of HTTPS
```

→ Catch before production.

---

## 2️⃣ Cost estimation — Infracost

Estimate AWS/GCP/Azure cost from Terraform plan.

### Install

```bash
brew install infracost
infracost auth login
```

### Run

```bash
terraform plan -out=plan.out
terraform show -json plan.out > plan.json
infracost breakdown --path plan.json

# Output:
# Project: acmeshop/production
# Name                          Monthly Qty  Unit       Monthly Cost
# aws_instance.web              730          hours      $30
# aws_rds_cluster.main           730          hours       $180
# aws_eks_cluster.main           730          hours       $73
# OVERALL TOTAL (USD)                                    $283
```

### CI integration

```yaml
- uses: infracost/actions/setup@v3
  with:
    api-key: ${{ secrets.INFRACOST_API_KEY }}

- run: |
    infracost breakdown --path . \
      --format json --out-file /tmp/infracost.json

- run: |
    infracost comment github --path /tmp/infracost.json \
      --repo $GITHUB_REPOSITORY \
      --github-token ${{ secrets.GITHUB_TOKEN }} \
      --pull-request ${{ github.event.pull_request.number }}
```

→ PR comment shows cost diff:

```
Old: $283/mo
New: $312/mo (+$29/mo)
   + aws_rds_cluster.replica  +$29
```

→ Catch budget surprises before merge.

---

## 3️⃣ Policy as Code — OPA, Sentinel

**Policy as Code** = automate compliance rules (e.g., "no public S3 buckets allowed").

### OPA (Open Policy Agent) + Conftest

```rego
# policy/no-public-s3.rego
package main

deny[msg] {
  input.resource.aws_s3_bucket[name].acl == "public-read"
  msg := sprintf("S3 bucket %v cannot be public", [name])
}

deny[msg] {
  input.resource.aws_security_group[name].ingress[_].cidr_blocks[_] == "0.0.0.0/0"
  input.resource.aws_security_group[name].ingress[_].from_port < 1024
  msg := sprintf("SG %v: well-known port open to 0.0.0.0/0", [name])
}
```

```bash
terraform plan -out=plan
terraform show -json plan | conftest test --policy policy/
```

→ Conftest evaluate Rego policies on plan. Block apply if violation.

### HashiCorp Sentinel (Terraform Cloud paid)

```hcl
# sentinel.hcl
import "tfplan/v2" as tfplan

required_tags = ["Environment", "Owner", "Project"]

main = rule {
  all tfplan.resource_changes as _, rc {
    rc.change.actions contains "create" implies
    all required_tags as t {
      rc.change.after.tags[t] is not null
    }
  }
}
```

→ Built-in TFC. Cloud paid feature.

### Policy patterns

```
Network:
- No SG with 0.0.0.0/0 on ports <1024
- No public-read S3 buckets
- No public IPs on private subnets

Resource tags:
- Required tags: Project, Environment, Owner

Cost:
- Max instance type t3.large (no x.4xlarge in dev)
- Required reserved instance for production-grade

Compliance:
- Encryption at rest mandatory
- Backup retention >= 7 days
- Logs enabled

K8s:
- Required resource limits
- No privileged containers
- No hostNetwork
```

→ Policies = guardrails. Devs free to deploy within policy.

---

## 4️⃣ Drift detection automation

```yaml
# .github/workflows/drift.yml
on:
  schedule:
  - cron: '0 9 * * *'                       # Daily 9 AM
  workflow_dispatch:

jobs:
  drift-check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [dev, staging, production]
    steps:
    - uses: actions/checkout@v4
    - uses: hashicorp/setup-terraform@v3

    - working-directory: envs/${{ matrix.env }}
      run: |
        terraform init
        terraform plan -detailed-exitcode
      # Exit 2 = changes detected (drift)

    - if: failure() && steps.plan.outputs.exitcode == '2'
      run: |
        ./scripts/slack-notify.sh \
          "🚨 Drift detected in ${{ matrix.env }}"
```

→ Daily check 3 envs. Alert Slack if reality diverges from code.

### Investigate drift

```bash
terraform plan
# Shows specific resources with diff

terraform plan -detailed-exitcode -no-color > plan.txt
# Save for analysis

# Investigate:
# - Cloud audit logs (who changed)
# - Slack #engineering (declared change?)
# - Code archeology (recent merges)

# Resolve:
# - Revert manual change → apply
# - Adopt manual change → update code
```

→ Drift detection = continuous compliance. Production health check.

---

## 5️⃣ Secrets management — Vault, AWS SM

### Anti-pattern — Secrets in tfvars

```hcl
# ❌ terraform.tfvars
db_password = "supersecret123"
```

→ Commit git = leak. Use external secrets store.

### Vault integration

```hcl
# Provider
provider "vault" { address = "https://vault.acmeshop.vn" }

# Read secret
data "vault_generic_secret" "db" {
  path = "secret/data/db/production"
}

# Use
resource "aws_db_instance" "main" {
  password = data.vault_generic_secret.db.data["password"]
  # ...
}
```

→ Secret fetched at apply time. Not in `.tf`. State still has it (encrypt state!).

### AWS Secrets Manager

```hcl
data "aws_secretsmanager_secret_version" "db" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  password = jsondecode(data.aws_secretsmanager_secret_version.db.secret_string).password
}
```

### Random + manage in Terraform

```hcl
resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_db_instance" "main" {
  password = random_password.db.result
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id     = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({ password = random_password.db.result })
}

# Store in Secrets Manager for app to read
```

→ Terraform generate + store. App fetch from Secrets Manager (not from Terraform state).

### Marking sensitive

```hcl
variable "api_key" {
  type      = string
  sensitive = true
}

output "db_password" {
  value     = random_password.db.result
  sensitive = true
}
```

→ Masked in console/CI logs. **Still in state file** — protect state.

---

## 6️⃣ CI/CD pattern — Production-grade

```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths: ['envs/**', 'modules/**']
  push:
    branches: [main]
    paths: ['envs/**', 'modules/**']

permissions:
  contents: read
  pull-requests: write
  id-token: write                            # OIDC AWS

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: hashicorp/setup-terraform@v3
    - run: terraform fmt -check -recursive
    - uses: terraform-linters/setup-tflint@v4
    - run: tflint --recursive

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/tfsec-action@v1
    - uses: bridgecrewio/checkov-action@v12
      with:
        framework: terraform

  plan:
    needs: [lint, security]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [dev, staging, production]
    steps:
    - uses: actions/checkout@v4
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE }}
        aws-region: us-east-1
    - uses: hashicorp/setup-terraform@v3

    - working-directory: envs/${{ matrix.env }}
      run: |
        terraform init
        terraform plan -out=plan.out -no-color > plan.txt

    - uses: infracost/actions/setup@v3
      with:
        api-key: ${{ secrets.INFRACOST_API_KEY }}
    - run: |
        infracost breakdown \
          --path envs/${{ matrix.env }} \
          --format github-comment \
          --out-file infracost-comment.md

    - if: github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          const plan = fs.readFileSync('envs/${{ matrix.env }}/plan.txt', 'utf8');
          const cost = fs.readFileSync('infracost-comment.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## Terraform Plan: ${{ matrix.env }}\n\`\`\`\n${plan}\n\`\`\`\n\n${cost}`
          });

  apply:
    needs: plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [dev, staging, production]
    environment:
      name: ${{ matrix.env }}                # Production needs approval
    steps:
    - uses: actions/checkout@v4
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.AWS_ROLE }}

    - working-directory: envs/${{ matrix.env }}
      run: |
        terraform init
        terraform apply -auto-approve

    - if: failure()
      run: ./scripts/slack-notify.sh "Terraform apply failed for ${{ matrix.env }}"
```

→ Production-grade: lint + security + cost + plan + manual approve + apply.

---

## 7️⃣ Pulumi — Alternative #1

**Pulumi** (2018) = IaC in **real programming languages** (Python, TypeScript, Go, C#).

### Python example

```python
# __main__.py
import pulumi
import pulumi_aws as aws

vpc = aws.ec2.Vpc("main",
    cidr_block="10.0.0.0/16",
    tags={"Name": "acmeshop"}
)

for i, cidr in enumerate(["10.0.1.0/24", "10.0.2.0/24"]):
    subnet = aws.ec2.Subnet(f"public-{i}",
        vpc_id=vpc.id,
        cidr_block=cidr
    )

pulumi.export("vpc_id", vpc.id)
```

```bash
pulumi up        # = terraform apply
```

### Vs Terraform

| Aspect | Pulumi | Terraform |
|---|---|---|
| Language | TS/Python/Go/C# real programming | HCL DSL |
| Loops/conditions | Native (if, for) | `count`, `for_each` (limited) |
| Type safety | ✅ TypeScript strict | Partial |
| Ecosystem | Smaller | **Much larger** |
| State | Cloud-managed (free) | DIY (S3+DynamoDB) |
| Multi-language modules | ✅ Mix | ❌ HCL only |
| Adoption | Growing | **Dominant** |

→ **Choose Pulumi** if: team strong TS/Python, complex loops, need OOP abstractions.
→ **Choose Terraform** if: ecosystem matters, team mixed background, simple infra.

---

## 8️⃣ AWS CDK — Alternative #2

**CDK** = AWS official, TypeScript/Python → CloudFormation.

```typescript
// app.ts
import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'AcmeshopStack');

const vpc = new ec2.Vpc(stack, 'VPC', {
  maxAzs: 2,
  natGateways: 1,
});

app.synth();
```

```bash
cdk deploy
```

### Vs Terraform

| Aspect | CDK | Terraform |
|---|---|---|
| Cloud | AWS only | Multi-cloud |
| Backend | CloudFormation | Provider-direct |
| Constructs (modules) | Rich AWS L3 | Generic |
| Language | TS/Python | HCL |
| Adoption AWS | Growing fast | Dominant |

→ **Choose CDK** if: AWS-only, TypeScript team familiar.
→ Limited beyond AWS — vendor lock-in.

### CDK for Terraform (CDKTF)

→ Pulumi-like syntax but Terraform backend. Best of both? Niche adoption.

---

## 9️⃣ Crossplane — K8s-native IaC

**Crossplane** = K8s controller for cloud provisioning. Define cloud resources as K8s CRDs.

```yaml
apiVersion: ec2.aws.upbound.io/v1beta1
kind: VPC
metadata:
  name: main
spec:
  forProvider:
    cidrBlock: 10.0.0.0/16
    region: us-east-1
```

```bash
kubectl apply -f vpc.yaml
# Crossplane controller provision AWS VPC
```

### Vs Terraform

| Aspect | Crossplane | Terraform |
|---|---|---|
| Workflow | Continuous reconcile (K8s style) | Apply on demand |
| State | K8s etcd | Separate backend |
| Self-healing | ✅ (drift auto-fixed) | Manual `apply` |
| Adoption | Growing | Dominant |
| Best for | K8s-centric platforms | Everything |

→ **Choose Crossplane** if: K8s-native platform, want continuous reconcile (GitOps).
→ **Choose Terraform** if: simple infra, traditional workflow.

→ **2026 trend**: Platform Engineering teams adopt Crossplane for "infrastructure as APIs".

---

## 1️⃣0️⃣ Anti-patterns to avoid

### 1. Click-ops mix with IaC

```
Click console → create thing
Terraform manage same thing
→ Drift, conflict, confusion
```

→ **Rule**: Terraform owns resource exclusively. No manual changes.

### 2. Mega monorepo (1 state file all resources)

```
1 state file: VPC + EKS + RDS + Lambda + ALB + Route53
→ Apply takes 30 min
→ Lock blocks all team
→ One bad resource = lock
```

→ **Rule**: split state by "blast radius". Per-env + per-domain (network/compute/data).

### 3. Hardcode environment vars

```hcl
# ❌
provider "aws" { region = "us-east-1" }       # Stuck

# ✅
provider "aws" { region = var.region }
```

### 4. No automated tests

```
Apply → break production → "oops"
```

→ Tests + plan in PR review.

### 5. Big bang apply

```
20 PRs accumulated → 1 huge apply
→ Hard rollback if break
```

→ Apply each PR after merge. Small batches.

### 6. Ignore output of `terraform plan`

```
20 lines changes → assume "OK, looks like usual"
→ Apply → break
```

→ **Read every line plan**. If unsure, ask.

### 7. No tagging strategy

```
$10K AWS bill, no tags
→ Who owns? Which env? Can delete?
```

→ Tag ALL resources: `Owner`, `Environment`, `Project`, `ManagedBy=Terraform`.

---

## 1️⃣1️⃣ Production setup của bạn — Summary

```
Codebase:
  infra/
  ├── modules/ (reusable)
  ├── envs/dev|staging|production/ (callers)
  ├── tests/
  └── .github/workflows/

State:
  S3 (versioning + encrypt) + DynamoDB lock
  Separate state per env
  Daily backup to separate bucket

CI/CD:
  PR: lint + tfsec + checkov + plan + Infracost
  PR comment: plan + cost diff
  Merge main: apply dev → staging
  Production: manual approval

Security:
  OIDC GitHub Actions → AWS (no long-lived keys)
  Secrets from Vault + AWS Secrets Manager
  tfsec + checkov mandatory pass
  Policy as code (OPA) for compliance

Operations:
  Daily drift check 3 envs
  Quarterly disaster recovery drill
  Module versioning + changelog
  Onboarding doc: clone repo, terraform init, plan
```

→ Production-grade IaC. Setup 2 weeks, leverage years.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Skip security scanning** → CVE in production. tfsec + checkov mandatory.
2. **Mega monorepo state** → slow apply, lock blocks team. Split by domain.
3. **Click-ops mix** → drift forever. Terraform owns or doesn't manage.
4. **Hardcode secrets** → leak. Vault/Secrets Manager.
5. **No drift detection** → silently diverge. Daily CI check.

---

## 🧠 Tự kiểm tra (Self-check)

1. **tfsec** vs **checkov** — chọn cái nào?
2. **Infracost** giải quyết vấn đề gì?
3. **Policy as Code** (OPA) — use case?
4. **Pulumi** vs **Terraform** — chọn 2026?
5. 5 anti-patterns common?

<details>
<summary>Gợi ý đáp án</summary>

1. Both. **tfsec**: focused Terraform, fast, 100+ rules. **Checkov**: broader (TF + CFN + K8s + Dockerfile), 1000+ rules. Many teams use both. CI integration easy. 2026 standard: at least 1 of them mandatory PR check.

2. **Cost surprise** before deploy. `terraform plan` shows resources but no $$ impact. **Infracost** parse plan → estimate monthly cost → PR comment shows diff (+$50/mo for new RDS). Catch budget breaches before merge. Engineers think about cost.

3. (a) **Compliance automate** — "no public S3, all resources tagged, encryption mandatory". (b) **Cost guardrails** — "no instance > t3.large in dev". (c) **Security baselines** — "no SG 0.0.0.0/0 on <1024 ports". OPA + Conftest evaluate Rego policies on plan. Block apply if violation. Devs free within policy.

4. Most teams 2026: **Terraform/OpenTofu** (ecosystem, hiring, mature). **Pulumi** if: strong TS/Python team, complex loops/OOP needed, want type safety. Hybrid: CDKTF (Pulumi-style syntax + Terraform backend). Not a clear winner — context-dependent.

5. (a) **Click-ops mix** — drift. (b) **Mega monorepo state** — slow + lock blocks. (c) **Hardcode vars** — inflexible. (d) **No tests + automated checks** — bugs in prod. (e) **Big bang apply** — hard rollback. (f) **No tagging** — cost mystery. (g) **Skim plan output** — surprise destroy. (h) **Secrets in code** — leak.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Production checklist

```
[ ] Remote backend (S3 + DynamoDB lock + versioning + encrypt)
[ ] Separate state per env + per domain
[ ] CI: lint + tfsec/checkov + plan + Infracost
[ ] PR: plan posted, cost diff posted
[ ] OIDC auth (no long-lived AWS keys)
[ ] Secrets from Vault/Secrets Manager
[ ] Policy as code (OPA)
[ ] Daily drift detection
[ ] Quarterly DR drill
[ ] Module versioning
[ ] Tag all resources (Owner/Env/Project)
[ ] terraform fmt + tflint passed
[ ] Module README auto-gen (terraform-docs)
```

### Tools

```
Security:   tfsec, checkov, snyk-iac
Cost:       Infracost
Policy:     OPA/Conftest, Sentinel
Lint:       terraform fmt, tflint
Docs:       terraform-docs
Test:       terraform test, Terratest
Multi-env:   Terragrunt, separate dirs
Automation: Atlantis, Spacelift, env0
```

### Alternatives

```
Pulumi      TS/Python/Go/C#, real lang
AWS CDK     TS/Python → CFN, AWS only
CDKTF       TS/Python → Terraform
Crossplane   K8s-native IaC
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **tfsec / Checkov / Snyk** | IaC security scanners |
| **Infracost** | Cost estimation |
| **Policy as Code** | Compliance rules in code |
| **OPA / Conftest** | OSS policy engine |
| **Sentinel** | HashiCorp policy framework |
| **Drift detection** | Find code-vs-reality diff |
| **Pulumi** | Real-language IaC alternative |
| **AWS CDK** | AWS-only TS/Python → CFN |
| **CDKTF** | CDK syntax + Terraform backend |
| **Crossplane** | K8s-native IaC |
| **Atlantis** | PR-driven Terraform automation |
| **Spacelift / env0** | Managed Terraform platforms |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Modules & Multi-env — DRY + Reusability](03_modules-and-workspaces.md)
- ↑ **Về cụm:** [iac README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [CI/CD pipeline patterns](../../../ci-cd/lessons/01_basic/03_pipeline-patterns.md) — security scanning patterns
- [K8s + RBAC](../../../kubernetes/lessons/01_basic/04_namespaces-and-rbac.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [Terraform Best Practices](https://www.terraform-best-practices.com/)
- 📖 [tfsec](https://aquasecurity.github.io/tfsec/)
- 📖 [Checkov](https://www.checkov.io/)
- 📖 [Infracost](https://www.infracost.io/)
- 📖 [Pulumi vs Terraform](https://www.pulumi.com/docs/concepts/vs/terraform/)
- 📖 [Crossplane docs](https://www.crossplane.io/)
- 📖 [Awesome Terraform](https://github.com/shuaibiyy/awesome-terraform)

---

> 🎯 *Cluster IaC basic 5/5 hoàn thành. DevOps sprint 4 cluster (K8s + CI/CD + Observability + IaC) đóng đủ. Bạn vận hành DevOps stack production-grade end-to-end.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster iac basic lesson 5/5. Cover: security scan (tfsec/checkov/snyk) + cost (Infracost) + policy (OPA/Sentinel) + alternatives (Pulumi/CDK/Crossplane decision matrix) + tagging strategy + naming convention.
- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước tfsec, Checkov, CI integration và Common findings.
