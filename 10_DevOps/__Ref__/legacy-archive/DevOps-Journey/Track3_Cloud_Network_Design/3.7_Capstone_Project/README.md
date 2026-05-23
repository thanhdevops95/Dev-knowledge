# 🏆 Module 3.7: Capstone Project

> **Production AWS Infrastructure**
>
> *Hạ tầng AWS Production*

---

## 🎯 Project Overview (Tổng quan dự án)

Deploy production-ready infrastructure on AWS with multi-AZ, auto scaling, and monitoring. This capstone project integrates all Track 3 knowledge.

*Deploy hạ tầng production-ready trên AWS với multi-AZ, auto scaling, và monitoring. Dự án capstone này tổng hợp tất cả kiến thức Track 3.*

---

## 📋 Requirements (Yêu cầu)

### Architecture (Kiến trúc)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AWS PRODUCTION INFRASTRUCTURE                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│                        ┌─────────────────┐                           │
│                        │   CloudFront    │ ← CDN for static assets   │
│                        │     (CDN)       │                           │
│                        └────────┬────────┘                           │
│                                 │                                     │
│                        ┌────────▼────────┐                           │
│                        │   Route 53      │ ← DNS                     │
│                        │     (DNS)       │                           │
│                        └────────┬────────┘                           │
│                                 │                                     │
│  ┌──────────────────────────────┴──────────────────────────────────┐ │
│  │                         VPC (10.0.0.0/16)                        │ │
│  │                                                                   │ │
│  │  ┌─────────────────┐              ┌─────────────────┐           │ │
│  │  │ Public Subnet   │              │ Public Subnet   │           │ │
│  │  │   (AZ-a)        │              │   (AZ-b)        │           │ │
│  │  │ ┌────┐ ┌────┐   │              │ ┌────┐ ┌────┐   │           │ │
│  │  │ │NAT │ │Bast│   │              │ │NAT │ │ALB │   │           │ │
│  │  │ └────┘ └────┘   │              │ └────┘ └────┘   │           │ │
│  │  └────────┬────────┘              └────────┬────────┘           │ │
│  │           │                                │                     │ │
│  │  ┌────────▼────────┐              ┌────────▼────────┐           │ │
│  │  │ Private Subnet  │              │ Private Subnet  │           │ │
│  │  │   (AZ-a)        │              │   (AZ-b)        │           │ │
│  │  │ ┌────────────┐  │              │ ┌────────────┐  │           │ │
│  │  │ │    EC2     │  │◄─── ASG ───► │ │    EC2     │  │           │ │
│  │  │ │ (Web App)  │  │              │ │ (Web App)  │  │           │ │
│  │  │ └────────────┘  │              │ └────────────┘  │           │ │
│  │  └────────┬────────┘              └────────┬────────┘           │ │
│  │           │                                │                     │ │
│  │  ┌────────▼────────────────────────────────▼────────┐           │ │
│  │  │              Database Subnet (Private)            │           │ │
│  │  │  ┌─────────────┐          ┌─────────────┐        │           │ │
│  │  │  │ RDS Primary │◄─ sync ─►│ RDS Standby │        │           │ │
│  │  │  │  (AZ-a)     │          │   (AZ-b)    │        │           │ │
│  │  │  └─────────────┘          └─────────────┘        │           │ │
│  │  │                                                   │           │ │
│  │  │  ┌─────────────┐                                 │           │ │
│  │  │  │ ElastiCache │ ← Redis for sessions/cache      │           │ │
│  │  │  │   (Redis)   │                                 │           │ │
│  │  │  └─────────────┘                                 │           │ │
│  │  └───────────────────────────────────────────────────┘           │ │
│  │                                                                   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    Monitoring & Logging                            │ │
│  │     CloudWatch    │    CloudWatch Logs    │    SNS Alerts         │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Component Details (Chi tiết thành phần)

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **VPC** | 10.0.0.0/16, 2 AZs | Public + Private subnets mỗi AZ |
| **ALB** | HTTPS, health checks | SSL certificate từ ACM |
| **ASG** | Min: 2, Max: 10 | Target tracking scaling |
| **RDS** | PostgreSQL, Multi-AZ | Automated backups 7 days |
| **ElastiCache** | Redis cluster | For session/cache |
| **S3** | Static assets | Versioning enabled |
| **CloudFront** | CDN | Origin là ALB + S3 |

---

### Infrastructure as Code

#### Terraform Example - VPC Module

```hcl
# modules/vpc/main.tf
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  # Database subnets
  database_subnets = ["10.0.201.0/24", "10.0.202.0/24"]
  create_database_subnet_group = true

  # NAT Gateway for private subnets
  enable_nat_gateway = true
  single_nat_gateway = false  # HA: 1 NAT per AZ

  # DNS
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = var.common_tags
}
```

#### Ansible Playbook - Web Server Setup

```yaml
# playbooks/webserver.yml
---
- name: Configure Web Servers
  hosts: webservers
  become: yes
  
  roles:
    - common
    - nginx
    - app_deploy
    
  tasks:
    - name: Install CloudWatch agent
      include_role:
        name: cloudwatch_agent
        
    - name: Configure log rotation
      template:
        src: logrotate.conf.j2
        dest: /etc/logrotate.d/webapp
```

---

## 📁 Project Structure (Cấu trúc dự án)

```
track3-capstone/
├── terraform/
│   ├── modules/
│   │   ├── vpc/
│   │   ├── alb/
│   │   ├── asg/
│   │   ├── rds/
│   │   └── elasticache/
│   ├── environments/
│   │   ├── staging/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── terraform.tfvars
│   │   └── production/
│   ├── backend.tf
│   └── versions.tf
│
├── ansible/
│   ├── inventory/
│   │   ├── staging.yml
│   │   └── production.yml
│   ├── playbooks/
│   │   ├── webserver.yml
│   │   └── database.yml
│   └── roles/
│
├── .gitlab-ci.yml          # CI/CD pipeline
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RUNBOOK.md
│   └── DR_PLAN.md
└── README.md
```

---

## ✅ Deliverables (Sản phẩm bàn giao)

- [ ] Terraform code
- [ ] Ansible playbooks
- [ ] Architecture diagram (Sơ đồ kiến trúc)
- [ ] DR plan (Kế hoạch DR)
- [ ] Cost estimation (Ước tính chi phí)
- [ ] Documentation (Tài liệu)

---

## 📊 Evaluation (Đánh giá)

| Criteria (Tiêu chí) | Weight (Trọng số) |
|---------------------|-------------------|
| Architecture (Kiến trúc) | 25% |
| IaC quality (Chất lượng IaC) | 25% |
| Security (Bảo mật) | 20% |
| Documentation (Tài liệu) | 15% |
| Monitoring (Giám sát) | 15% |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [3.6 System Design](../3.6_System_Design_Reliability/) | **3.7 Capstone** | [Track 4](../../Track4_DevSecOps/) |

---

**Good luck! 🚀**

*Chúc may mắn!*

</div>
