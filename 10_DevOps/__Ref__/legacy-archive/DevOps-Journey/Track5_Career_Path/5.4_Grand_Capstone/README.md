# 🏆 Module 5.4: Grand Capstone Project

> **Enterprise DevOps Platform**
>
> *Nền tảng DevOps Doanh nghiệp*

---

## 🎯 Project Overview (Tổng quan dự án)

Build a complete DevOps platform combining all knowledge from 5 tracks.

*Xây dựng nền tảng DevOps hoàn chỉnh tổng hợp tất cả kiến thức từ 5 tracks.*

---

## 📋 Requirements (Yêu cầu)

### Architecture (Kiến trúc)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Enterprise DevOps Platform                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                     GitLab (Primary)                         │    │
│  │  Repository │ CI/CD │ Registry │ Security Scanning          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                               │                                      │
│         ┌─────────────────────┼─────────────────────┐               │
│         ▼                     ▼                     ▼               │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐         │
│  │  Terraform  │      │   Ansible   │      │   ArgoCD    │         │
│  │   (IaC)     │      │  (Config)   │      │   (GitOps)  │         │
│  └─────────────┘      └─────────────┘      └─────────────┘         │
│         │                                           │               │
│         ▼                                           ▼               │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    AWS Infrastructure                        │    │
│  │                                                              │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │    │
│  │  │   VPC   │  │   EKS   │  │   RDS   │  │   S3    │        │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │    │
│  │                                                              │    │
│  │  ┌───────────────────────────────────────────────────────┐  │    │
│  │  │              Kubernetes Cluster (EKS)                 │  │    │
│  │  │                                                       │  │    │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │  │    │
│  │  │  │ Ingress │  │ Services│  │ Workloads│              │  │    │
│  │  │  └─────────┘  └─────────┘  └─────────┘              │  │    │
│  │  │                                                       │  │    │
│  │  │  ┌─────────────────────────────────────────────────┐│  │    │
│  │  │  │           Monitoring & Observability            ││  │    │
│  │  │  │  Prometheus │ Grafana │ Loki │ Alertmanager    ││  │    │
│  │  │  └─────────────────────────────────────────────────┘│  │    │
│  │  └───────────────────────────────────────────────────────┘  │    │
│  │                                                              │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Security Layer                            │    │
│  │  Vault (Secrets) │ OPA (Policy) │ Falco (Runtime)          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Components (Các thành phần)

#### 1. Infrastructure - Track 3 (Hạ tầng)

- [ ] Multi-AZ AWS infrastructure (Hạ tầng AWS nhiều AZ)
- [ ] Terraform modules for VPC, EKS, RDS (Modules Terraform)
- [ ] Network design with security groups (Thiết kế mạng với security groups)
- [ ] Cost-optimized resources (Tài nguyên tối ưu chi phí)

#### 2. Platform - Track 2 (Nền tảng)

- [ ] EKS Kubernetes cluster (Cluster Kubernetes EKS)
- [ ] Ingress controller (NGINX/ALB) (Ingress controller)
- [ ] Container registry (GitLab/ECR) (Registry container)
- [ ] Service mesh (optional - Istio) (Tùy chọn)

#### 3. CI/CD - Track 1 & 2

> Use **GitLab CI** as the primary CI/CD platform
> *Sử dụng **GitLab CI** làm nền tảng CI/CD chính*

- [ ] Multi-environment pipeline (Pipeline nhiều môi trường)
- [ ] GitOps deployment with ArgoCD (Deploy GitOps với ArgoCD)
- [ ] Automated testing (Kiểm thử tự động)
- [ ] Blue/Green or Canary deployments (Triển khai Blue/Green hoặc Canary)

**Example `.gitlab-ci.yml`:**

```yaml
stages:
  - validate
  - build
  - security
  - deploy-staging
  - deploy-production

include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

terraform-validate:
  stage: validate
  image: hashicorp/terraform:latest
  script:
    - cd terraform/
    - terraform init
    - terraform validate
    - terraform plan

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy-staging:
  stage: deploy-staging
  image: bitnami/kubectl
  script:
    - kubectl apply -k k8s/overlays/staging/
  environment:
    name: staging

deploy-production:
  stage: deploy-production
  image: bitnami/kubectl
  script:
    - kubectl apply -k k8s/overlays/production/
  environment:
    name: production
  when: manual
  only:
    - main
```

#### 4. Security - Track 4 (Bảo mật)

- [ ] Secrets management with Vault (Quản lý secrets với Vault)
- [ ] Security scanning in pipeline (Quét bảo mật trong pipeline)
- [ ] OPA policies for Kubernetes (Chính sách OPA cho Kubernetes)
- [ ] Compliance checks (Kiểm tra tuân thủ)

#### 5. Observability - Track 2 (Khả năng quan sát)

- [ ] Metrics with Prometheus (Metrics với Prometheus)
- [ ] Dashboards with Grafana (Dashboard với Grafana)
- [ ] Logs with Loki or ELK (Logs với Loki hoặc ELK)
- [ ] Alerting configured (Cảnh báo đã cấu hình)

---

## ✅ Deliverables (Sản phẩm bàn giao)

| Deliverable | Description |
|-------------|-------------|
| 📁 **Infrastructure Code** | Terraform modules, Ansible playbooks |
| ☸️ **Kubernetes Cluster** | Working EKS cluster with workloads |
| 🔄 **CI/CD Pipeline** | GitLab CI with security scanning |
| 🔐 **Security Controls** | Vault, OPA, scanning |
| 📊 **Monitoring Stack** | Prometheus, Grafana, Loki |
| 📝 **Documentation** | Architecture docs, runbooks |
| 🎤 **Presentation** | Slide deck for demo |

---

## 📁 Project Structure (Cấu trúc dự án)

```
grand-capstone/
├── terraform/
│   ├── modules/
│   │   ├── vpc/
│   │   ├── eks/
│   │   └── rds/
│   ├── environments/
│   │   ├── staging/
│   │   └── production/
│   └── main.tf
├── ansible/
│   ├── playbooks/
│   └── roles/
├── k8s/
│   ├── base/
│   │   ├── deployments/
│   │   ├── services/
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── staging/
│       └── production/
├── apps/
│   ├── frontend/
│   ├── api-gateway/
│   └── microservices/
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── alertmanager/
├── security/
│   ├── vault/
│   └── policies/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RUNBOOK.md
│   └── SECURITY.md
├── .gitlab-ci.yml
└── README.md
```

---

## 📊 Evaluation (Đánh giá)

| Criteria (Tiêu chí) | Weight (Trọng số) |
|---------------------|-------------------|
| Architecture design (Thiết kế kiến trúc) | 20% |
| Implementation quality (Chất lượng triển khai) | 25% |
| Security (Bảo mật) | 15% |
| Automation level (Mức độ tự động) | 15% |
| Documentation (Tài liệu) | 15% |
| Presentation (Thuyết trình) | 10% |

---

## 🎓 Completion (Hoàn thành)

Upon completing this project, you have demonstrated (Khi hoàn thành dự án này, bạn đã chứng minh):

- ✅ End-to-end DevOps skills (Kỹ năng DevOps toàn diện)
- ✅ Production-ready infrastructure design (Thiết kế hạ tầng production-ready)
- ✅ Security best practices implementation (Triển khai best practices bảo mật)
- ✅ Clear documentation and communication (Tài liệu và giao tiếp rõ ràng)
- ✅ Problem-solving and troubleshooting (Giải quyết vấn đề và khắc phục sự cố)

---

## 📖 Resources (Tài liệu tham khảo)

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [5.3 Portfolio](../5.3_Portfolio_Launch/) | **5.4 Grand Capstone** | [Home](../../README.md) |

---

**🎉 Congratulations! You are ready for a DevOps role! 🚀**

*Chúc mừng! Bạn đã sẵn sàng cho vị trí DevOps!*

</div>
