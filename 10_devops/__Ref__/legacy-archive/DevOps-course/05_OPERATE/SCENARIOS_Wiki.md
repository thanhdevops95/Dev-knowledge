# 🚨 MODULE 05: SCENARIOS - IaC & Cloud Operations

## Scenario 1: Terraform State Bị Corrupt

### 🚨 Bối cảnh

```bash
terraform plan
# Error: state file is corrupted
```

### 🕵️ Điều tra

State file lưu local, bị xóa hoặc corrupt do crash.

### 💡 Giải pháp

**1. Use remote state (S3):**

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "counter-app/terraform.tfstate"
    region = "us-east-1"
  }
}
```

**2. Enable state locking (DynamoDB):**

```hcl
terraform {
  backend "s3" {
    ...
    dynamodb_table = "terraform-locks"
  }
}
```

**3. Restore from backup:**

```bash
cp terraform.tfstate.backup terraform.tfstate
```

### 🧠 Bài học

- Never store state locally in production
- Use remote backends (S3, Terraform Cloud)
- Enable state locking
- Automated backups

---

## Scenario 2: Manual Changes Conflict với IaC

### 🚨 Bối cảnh

Developer vào AWS Console, manually thay đổi security group. Sau đó chạy `terraform  plan` → Shows drift.

### 🕵️ Điều tra

```bash
terraform plan
# ~ security_group: "sg-old" → "sg-new"
```

### 💡 Giải pháp

**Option 1: Import manual changes**

```bash
terraform import aws_security_group.web sg-12345
terraform refresh
```

**Option 2: Revert manual changes**

```bash
terraform apply  # Overwrite manual changes
```

**Prevention: Use IAM policies**

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestTag/ManagedBy": "Terraform"
    }
  }
}
```

### 🧠 Bài học

- Avoid manual changes
- Use tags: `ManagedBy: Terraform`
- IAM policies prevent manual edits
- Drift detection tools

---

## Scenario 3: Ansible Playbook Failed Midway

### 🚨 Bối cảnh

Playbook cài 10 tasks, fail ở task 5 → Servers ở trạng thái inconsistent.

### 🕵️ Điều tra

```bash
ansible-playbook playbook.yml
# TASK [Install Docker] **** FAILED
```

### 💡 Giải pháp

**1. Idempotent tasks (best practice):**

```yaml
- name: Install Docker
  apt:
    name: docker.io
    state: present  # ← Idempotent: safe to rerun
```

**2. Use `--start-at-task`:**

```bash
ansible-playbook playbook.yml --start-at-task="Install Docker"
```

**3. Rollback playbook:**

```yaml
- name: Uninstall if failed
  apt:
    name: docker.io
    state: absent
  when: install_docker_failed
```

### 🧠 Bài học

- Write idempotent tasks
- Test playbooks on staging first
- Use `--check` mode (dry run)
- Have rollback playbooks

---

## Scenario 4: Cloud Bill Skyrocket ($1K → $10K)

### 🚨 Bối cảnh

AWS bill tháng trước: $1000  
AWS bill tháng này: $10,000  
CFO gọi họp gấp!

### 🕵️ Điều tra

```bash
# Check AWS Cost Explorer
# Top costs: EC2 instances running 24/7

aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]'
# 50 instances running!
```

**Nguyên nhân:** Developer test auto-scaling, quên tắt.

### 💡 Giải pháp

**1. Immediate: Stop unused instances**

```bash
aws ec2 stop-instances --instance-ids $(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`running`].InstanceId' --output text)
```

**2. Set budgets & alerts:**

```hcl
resource "aws_budgets_budget" "cost_alert" {
  budget_type = "COST"
  limit_amount = "1000"
  time_unit = "MONTHLY"
  
  notification {
    notification_type = "ACTUAL"
    comparison_operator = "GREATER_THAN"
    threshold = 80
    subscriber_email_addresses = ["devops@company.com"]
  }
}
```

**3. Auto-shutdown schedules:**

```bash
# Lambda function to stop instances after 6pm
# Tag instances: AutoShutdown=true
```

**4. Use spot instances:**

```hcl
resource "aws_instance" "web" {
  instance_market_options {
    market_type = "spot"  # 70% cheaper
  }
}
```

### 🧠 Bài học

- Always set budget alerts
- Tag resources with owner/project
- Auto-shutdown non-prod environments
- Use spot/reserved instances
- Regular cost audits

---

## Scenario 5: Accidental `terraform destroy` Production

### 🚨 Bối cảnh

Junior dev nhầm workspace, chạy:

```bash
terraform destroy -auto-approve
```

→ Xóa toàn bộ production infrastructure!

### 🕵️ Điều tra

```bash
terraform show
# No resources
```

### 💡 Giải pháp

**1. Restore from state backup:**

```bash
# S3 versioning enabled
aws s3api list-object-versions --bucket terraform-state --prefix prod/
aws s3api get-object --bucket terraform-state --key prod/terraform.tfstate --version-id <version> terraform.tfstate

terraform apply
```

**2. Prevention: Workspace protection**

```hcl
# main.tf
locals {
  workspace = terraform.workspace
}

# Prevent destroy on prod
lifecycle {
  prevent_destroy = true
}

# Require confirmation
resource "null_resource" "confirm_destroy" {
  count = terraform.workspace == "prod" ? 1 : 0
  
  provisioner "local-exec" {
    command = "echo 'WARNING: Destroying production!'; read -p 'Type DESTROY to confirm: ' confirm; [ $confirm != 'DESTROY' ] && exit 1"
  }
}
```

**3. Use Terraform Cloud:**

- Requires 2-person approval for production destroys
- Audit logs
- Access control

**4. Backup strategy:**

- Daily snapshots (EBS, RDS)
- S3 versioning for state files
- Disaster recovery drills

### 🧠 Bài học

- **NEVER use `-auto-approve` in production**
- Separate workspaces (dev, staging, prod)
- Enable versioning on state backends
- Require manual confirmation for destroys
- Regular backups & DR drills
- Terraform Cloud for access control

---

## 🎯 Tổng kết Module 05

| Scenario | Vấn đề | Giải pháp |
|----------|--------|-----------|
| 1 | State corrupt | Remote backend + Locking |
| 2 | Manual changes | IAM policies + Import |
| 3 | Playbook failed | Idempotent + Rollback |
| 4 | Cost overrun | Budgets + Auto-shutdown |
| 5 | Accidental destroy | Prevent_destroy + Backups |

✅ **Next:** Module 06 - MONITOR!
