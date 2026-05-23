# Module 12: INFRASTRUCTURE AS CODE (IaC)

> **"IaC là robot xây dựng - viết 1 lần, tạo cả ngàn servers giống hệt nhau"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu IaC concepts và benefits
- ✅ Terraform từ cơ bản đến nâng cao
- ✅ Terraform modules
- ✅ Terraform state management
- ✅ Ansible basics
- ✅ Ansible playbooks và roles
- ✅ Packer cho image building

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| IaC | Infrastructure as Code | Hạ tầng dưới dạng code |
| Provider | Terraform Provider | Plugin kết nối cloud |
| Resource | Resource | Tài nguyên cần tạo |
| State | Terraform State | Trạng thái hiện tại |
| Plan | Terraform Plan | Xem trước changes |
| Apply | Terraform Apply | Thực thi changes |
| Destroy | Terraform Destroy | Xóa resources |
| Module | Terraform Module | Đơn vị tái sử dụng |
| Workspace | Terraform Workspace | Môi trường riêng biệt |
| Backend | State Backend | Nơi lưu state |
| Variable | Variable | Biến đầu vào |
| Output | Output | Giá trị đầu ra |
| Playbook | Ansible Playbook | File định nghĩa tasks |
| Role | Ansible Role | Tập hợp tasks tái sử dụng |
| Inventory | Ansible Inventory | Danh sách hosts |
| Task | Ansible Task | Một hành động |
| Handler | Ansible Handler | Task chạy khi notify |
| Template | Jinja2 Template | File template |

---

## ✅ Checklist Labs

### Labs Terraform Basics

- [ ] Lab 1: Install Terraform
- [ ] Lab 2: Terraform init, plan, apply
- [ ] Lab 3: Terraform destroy
- [ ] Lab 4: HCL syntax basics
- [ ] Lab 5: Provider configuration
- [ ] Lab 6: Resource basics
- [ ] Lab 7: terraform.tfvars

### Labs Terraform với AWS

- [ ] Lab 8: AWS provider setup
- [ ] Lab 9: Create VPC
- [ ] Lab 10: Create subnets
- [ ] Lab 11: Create security groups
- [ ] Lab 12: Create EC2 instance
- [ ] Lab 13: Create S3 bucket
- [ ] Lab 14: Create RDS instance
- [ ] Lab 15: Create EKS cluster

### Labs Terraform Variables & Outputs

- [ ] Lab 16: Input variables
- [ ] Lab 17: Variable types (string, list, map, object)
- [ ] Lab 18: Variable validation
- [ ] Lab 19: Sensitive variables
- [ ] Lab 20: Local values
- [ ] Lab 21: Output values
- [ ] Lab 22: Output với sensitive

### Labs Terraform State

- [ ] Lab 23: Local state
- [ ] Lab 24: Remote state (S3 backend)
- [ ] Lab 25: State locking (DynamoDB)
- [ ] Lab 26: terraform state commands
- [ ] Lab 27: State import
- [ ] Lab 28: terraform refresh

### Labs Terraform Modules

- [ ] Lab 29: Create custom module
- [ ] Lab 30: Module inputs và outputs
- [ ] Lab 31: Module sources (local, git, registry)
- [ ] Lab 32: Terraform Registry modules
- [ ] Lab 33: Module versioning
- [ ] Lab 34: Module composition

### Labs Terraform Advanced

- [ ] Lab 35: Terraform workspaces
- [ ] Lab 36: Count và for_each
- [ ] Lab 37: Dynamic blocks
- [ ] Lab 38: Conditional expressions
- [ ] Lab 39: Data sources
- [ ] Lab 40: Provisioners (local-exec, remote-exec)
- [ ] Lab 41: terraform fmt, validate
- [ ] Lab 42: terraform graph
- [ ] Lab 43: Terraform Cloud basics

### Labs Ansible Basics

- [ ] Lab 44: Install Ansible
- [ ] Lab 45: Ansible inventory
- [ ] Lab 46: Ad-hoc commands
- [ ] Lab 47: First playbook
- [ ] Lab 48: YAML syntax
- [ ] Lab 49: Ansible modules

### Labs Ansible Playbooks

- [ ] Lab 50: Multiple tasks
- [ ] Lab 51: Handlers
- [ ] Lab 52: Variables trong playbook
- [ ] Lab 53: Register và debug
- [ ] Lab 54: Conditionals (when)
- [ ] Lab 55: Loops (with_items, loop)
- [ ] Lab 56: Blocks và rescue
- [ ] Lab 57: Tags

### Labs Ansible Templates & Files

- [ ] Lab 58: Copy module
- [ ] Lab 59: Template module (Jinja2)
- [ ] Lab 60: File module
- [ ] Lab 61: Lineinfile module

### Labs Ansible Roles

- [ ] Lab 62: Role structure
- [ ] Lab 63: Create custom role
- [ ] Lab 64: Role defaults và vars
- [ ] Lab 65: Role handlers
- [ ] Lab 66: Ansible Galaxy
- [ ] Lab 67: Install roles từ Galaxy

### Labs Ansible Advanced

- [ ] Lab 68: Vault (encrypt secrets)
- [ ] Lab 69: Inventory plugins
- [ ] Lab 70: Dynamic inventory
- [ ] Lab 71: Ansible with Docker
- [ ] Lab 72: Ansible with Kubernetes

### Labs Packer

- [ ] Lab 73: Install Packer
- [ ] Lab 74: Packer template basics
- [ ] Lab 75: Build AMI với Packer
- [ ] Lab 76: Packer provisioners
- [ ] Lab 77: Packer với Ansible

### Labs Counter App IaC

- [ ] Lab 78: Terraform cho Counter App infrastructure
- [ ] Lab 79: Ansible để configure servers
- [ ] Lab 80: End-to-end IaC workflow

---

## 🚨 Checklist Scenarios

### Scenarios về Terraform State

- [ ] Scenario 1: State file corrupted
- [ ] Scenario 2: State lock stuck
- [ ] Scenario 3: Resource exists but not in state
- [ ] Scenario 4: Multiple people terraform apply conflict
- [ ] Scenario 5: State file accidentally deleted

### Scenarios về Terraform Apply

- [ ] Scenario 6: terraform apply fails halfway
- [ ] Scenario 7: Dependency cycle detected
- [ ] Scenario 8: Resource replacement unexpected
- [ ] Scenario 9: Provider authentication failed
- [ ] Scenario 10: Rate limit hit

### Scenarios về Terraform Modules

- [ ] Scenario 11: Module version mismatch
- [ ] Scenario 12: Module output not available
- [ ] Scenario 13: Module circular dependency

### Scenarios về Drift

- [ ] Scenario 14: Manual changes outside Terraform
- [ ] Scenario 15: Drift detection
- [ ] Scenario 16: Reconciling drift

### Scenarios về Ansible

- [ ] Scenario 17: SSH connection refused
- [ ] Scenario 18: Sudo password required
- [ ] Scenario 19: Module not found
- [ ] Scenario 20: Idempotency issue
- [ ] Scenario 21: Handler not triggered

### Scenarios về Playbooks

- [ ] Scenario 22: Variable undefined
- [ ] Scenario 23: Template rendering failed
- [ ] Scenario 24: Task failed but should continue
- [ ] Scenario 25: Vault password incorrect

### Scenarios về Production

- [ ] Scenario 26: Terraform destroy in production
- [ ] Scenario 27: Security group too permissive
- [ ] Scenario 28: Resource quota exceeded
- [ ] Scenario 29: Cost explosion from IaC
- [ ] Scenario 30: Secrets exposed in code

---

## ⏱️ Thời lượng

**Ước tính:** 8-10 giờ

| Phần | Thời gian |
|------|-----------|
| Terraform basics (Labs 1-15) | 2 giờ |
| Variables, State, Modules (Labs 16-34) | 2.5 giờ |
| Terraform advanced (Labs 35-43) | 1 giờ |
| Ansible basics (Labs 44-57) | 2 giờ |
| Ansible roles & advanced (Labs 58-72) | 1.5 giờ |
| Packer & Counter App | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Ansible Documentation](https://docs.ansible.com/)
- [Packer Documentation](https://www.packer.io/docs)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
