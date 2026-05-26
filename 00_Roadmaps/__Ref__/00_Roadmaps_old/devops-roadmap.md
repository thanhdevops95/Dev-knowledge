# 🔧 Lộ trình DevOps Engineer

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** `[BEGINNER → ADVANCED]`
> **Tags:** `[MUST-KNOW]` — Từ Docker đến Kubernetes trên Cloud
> **Prerequisite:** Đã nắm kiến thức nền tảng ([00-overview.md](./00-overview.md))

---

## Tại sao DevOps?

DevOps là cầu nối giữa **Development** và **Operations** — tự động hóa toàn bộ vòng đời phần mềm từ code đến production.

**Ví dụ thực tế:** Nếu phần mềm là sản phẩm, thì DevOps chính là **dây chuyền sản xuất tự động** trong nhà máy. Không có DevOps, mọi thứ đều thủ công, chậm và dễ sai sót.

| Không có DevOps | Có DevOps |
|---|---|
| Deploy bằng FTP / SSH thủ công | Tự động qua CI/CD pipeline |
| "Máy tôi chạy được mà!" | Docker đảm bảo môi trường nhất quán |
| Phát hiện lỗi khi user phản hồi | Monitoring cảnh báo trước khi user biết |
| Scale server bằng tay | Auto-scaling với Kubernetes |

---

## Sơ đồ lộ trình

```
Linux/Terminal ──→ Networking ──→ Git
                                   │
          ┌────────────────────────┘
          ▼
       Docker ──→ CI/CD ──→ Kubernetes
                                │
          ┌─────────────────────┘
          ▼
  IaC (Terraform) ──→ Cloud (AWS/Azure/GCP)
                              │
          ┌───────────────────┘
          ▼
    Monitoring ──→ SRE Practices
```

---

## Phase 1 — Linux & Terminal

> 🎯 Nền tảng bắt buộc — hầu hết server production đều chạy Linux

- [ ] Terminal navigation, pipes, redirects, file permissions
- [ ] Bash scripting: variables, loops, functions
- [ ] Process management, systemd, cron jobs
- [ ] SSH, user management, file system hierarchy
- 📄 [Terminal Basics](<../03-Terminal & OS/terminal/01-terminal-basics.md>)
- 📄 [Bash Scripting](<../03-Terminal & OS/terminal/02-bash-scripting-basics.md>)
- 📄 [Linux Essentials](<../03-Terminal & OS/linux/01-linux-essentials-basics.md>)
- 📄 [Linux Administration](../09-DevOps/linux/01-linux-basics.md)

---

## Phase 2 — Networking

- [ ] Mô hình OSI & TCP/IP — hiểu data đi từ A đến B như thế nào
- [ ] HTTP/HTTPS, DNS resolution, SSL/TLS handshake
- [ ] Firewall, Load Balancer, Reverse Proxy concepts
- 📄 [HTTP Fundamentals](../04-Networking/01-http-fundamentals.md)
- 📄 [OSI & TCP/IP](../04-Networking/03-osi-tcp-ip-fundamentals.md)
- 📄 [DNS](../04-Networking/05-dns-fundamentals.md)
- 📄 [TLS/SSL](../04-Networking/04-tls-ssl-fundamentals.md)

---

## Phase 3 — Version Control (Git)

- [ ] Git branching, merging, rebasing
- [ ] GitFlow vs Trunk-based development
- [ ] Pull requests, code review workflows
- 📄 [Git Basics](<../02-Version Control/git/01-git-basics.md>)
- 📄 [Git Workflows](<../02-Version Control/git/03-git-workflows-practices.md>)

---

## Phase 4 — Containers (Docker)

> 🐳 Kỹ năng quan trọng nhất của DevOps hiện đại

- [ ] Dockerfile, images, containers, volumes, networks
- [ ] Multi-stage builds, layer caching optimization
- [ ] Docker Compose cho multi-container apps
- [ ] Container security scanning
- 📄 [Docker Basics](../09-DevOps/docker/01-docker-basics.md)
- 📄 [Docker Advanced](../09-DevOps/docker/02-docker-advanced.md)
- 📄 [Docker Compose](../09-DevOps/docker/03-docker-compose-basics.md)

---

## Phase 5 — CI/CD

- [ ] Pipeline concepts: build → test → deploy
- [ ] GitHub Actions: workflows, jobs, secrets
- [ ] GitLab CI, Jenkins (nên biết thêm)
- [ ] ArgoCD & GitOps pattern
- [ ] Release strategies: Blue-Green, Canary, Rolling Update
- 📄 [CI/CD Basics](../09-DevOps/ci-cd/01-cicd-basics.md)
- 📄 [GitHub Actions](../09-DevOps/cicd/01-github-actions-basics.md)
- 📄 [ArgoCD & GitOps](../09-DevOps/cicd/04-argocd-gitops-basics.md)
- 📄 [Release Strategies](../09-DevOps/cicd/05-release-strategies-patterns.md)

---

## Phase 6 — Kubernetes

> ☸️ Container orchestration — quản lý hàng trăm containers

- [ ] Pods, Deployments, Services, ConfigMaps, Secrets
- [ ] Ingress controllers, Service mesh
- [ ] Helm charts cho package management
- [ ] RBAC, Pod Security Standards, Network Policies
- [ ] Persistent Volumes, StorageClass
- 📄 [Kubernetes Basics](../09-DevOps/kubernetes/01-kubernetes-basics.md)
- 📄 [Helm](../09-DevOps/kubernetes/02-helm-basics.md)
- 📄 [K8s Networking](../09-DevOps/kubernetes/03-k8s-networking-advanced.md)
- 📄 [K8s Security](../09-DevOps/kubernetes/04-k8s-security-advanced.md)
- 📄 [K8s Production](../09-DevOps/kubernetes/07-k8s-production-practices.md)

---

## Phase 7 — Infrastructure as Code (IaC)

- [ ] Terraform: HCL syntax, providers, state, modules
- [ ] Ansible: playbooks, roles, inventory management
- [ ] Pulumi hoặc AWS CDK (alternatives)
- [ ] Secret management: Vault, cloud-native solutions
- 📄 [Terraform Basics](../09-DevOps/iac/01-terraform-basics.md)
- 📄 [Ansible Basics](../09-DevOps/iac/02-ansible-basics.md)
- 📄 [Pulumi](../09-DevOps/iac/03-pulumi-basics.md)
- 📄 [Vault](../09-DevOps/secrets/01-vault-basics.md)

---

## Phase 8 — Cloud

> ☁️ Chọn 1 cloud provider học sâu, biết cơ bản 2 cái còn lại

- [ ] Core services: Compute, Storage, Networking, IAM
- [ ] Serverless: Lambda / Cloud Functions / Azure Functions
- [ ] Container services: ECS/EKS, AKS, GKE
- [ ] Cloud networking: VPC, Subnets, Security Groups
- 📄 [Cloud Overview](../10-Cloud/01-cloud-overview.md)
- 📄 [Cloud Services Compare](../10-Cloud/02-cloud-services-compare.md)
- 📄 [AWS Core](../10-Cloud/aws/01-aws-core-basics.md)
- 📄 [Azure Core](../10-Cloud/azure/01-azure-core-basics.md)
- 📄 [GCP Core](../10-Cloud/gcp/01-gcp-core-basics.md)

---

## Phase 9 — Monitoring & Observability

- [ ] Ba trụ cột: Logs, Metrics, Traces
- [ ] ELK Stack (Elasticsearch, Logstash, Kibana)
- [ ] Prometheus + Grafana dashboards
- [ ] Distributed tracing: OpenTelemetry, Jaeger
- 📄 [Observability Fundamentals](../09-DevOps/observability/01-observability-fundamentals.md)
- 📄 [ELK Stack](../09-DevOps/observability/02-elk-stack-basics.md)
- 📄 [Grafana & Prometheus](../09-DevOps/observability/03-grafana-prometheus-basics.md)
- 📄 [OpenTelemetry](../09-DevOps/observability/04-opentelemetry-basics.md)
- 📄 [Distributed Tracing](../09-DevOps/observability/06-distributed-tracing-fundamentals.md)

---

## Phase 10 — SRE Practices

- [ ] SLI, SLO, SLA và Error Budgets
- [ ] Incident management, on-call, postmortems
- [ ] Chaos engineering: kiểm tra khả năng chịu lỗi
- [ ] Capacity planning, High Availability patterns
- 📄 [SRE Practices](../09-DevOps/sre/01-sre-practices.md)
- 📄 [Incident Management](../09-DevOps/sre/02-incident-management-practices.md)
- 📄 [Chaos Engineering](../09-DevOps/sre/03-chaos-engineering-practices.md)
- 📄 [High Availability](../09-DevOps/sre/05-high-availability-fundamentals.md)

---

## 📦 Project thực hành

| Phase | Project | Độ khó |
|---|---|---|
| Docker | Containerize fullstack app (React + Node + PostgreSQL) | ⭐⭐ |
| CI/CD | GitHub Actions pipeline: lint → test → build → deploy staging | ⭐⭐ |
| K8s | Deploy 3 microservices lên K8s với Helm charts | ⭐⭐⭐ |
| IaC | Provision VPC + ECS cluster trên AWS bằng Terraform | ⭐⭐⭐ |
| Monitoring | Grafana + Prometheus + AlertManager cho production app | ⭐⭐⭐ |
| Tổng hợp | Full platform: Terraform → K8s → GitOps → Observability stack | ⭐⭐⭐⭐ |

---

## 📚 Tài nguyên

| Loại | Tên | Ghi chú |
|---|---|---|
| Roadmap | [roadmap.sh/devops](https://roadmap.sh/devops) | Interactive roadmap |
| Lab | [KodeKloud](https://kodekloud.com) | Hands-on labs cho Docker, K8s, Terraform |
| Sách | *The Phoenix Project* — Gene Kim | DevOps culture qua tiểu thuyết |
| Sách | *Site Reliability Engineering* — Google | [Đọc miễn phí online](https://sre.google/sre-book/table-of-contents/) |
| Cert | CKA (Certified Kubernetes Admin) | [cncf.io/certification/cka](https://www.cncf.io/certification/cka/) |
| Cert | AWS Solutions Architect Associate | [aws.amazon.com/certification](https://aws.amazon.com/certification/) |
| Lab | [Play with Docker](https://labs.play-with-docker.com) | Thực hành Docker miễn phí trên browser |
| Lab | [Katacoda / Killercoda](https://killercoda.com) | Interactive K8s scenarios |
