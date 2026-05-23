# 🗺️ DevOps Roadmap - Lộ trình học tập

> **Hướng dẫn từng bước để trở thành DevOps Engineer**

---

## 📍 Tổng quan Roadmap

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEVOPS LEARNING PATH                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Month 1-2          Month 3-4          Month 5-6               │
│  ┌─────────┐        ┌─────────┐        ┌─────────┐             │
│  │ BASICS  │───────▶│ CORE    │───────▶│ ADVANCED│             │
│  │         │        │ DEVOPS  │        │         │             │
│  │ Linux   │        │ Docker  │        │ K8s     │             │
│  │ Network │        │ CI/CD   │        │ Cloud   │             │
│  │ Git     │        │         │        │ IaC     │             │
│  └─────────┘        └─────────┘        └─────────┘             │
│       │                  │                  │                   │
│       ▼                  ▼                  ▼                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              CONTINUOUS PRACTICE & PROJECTS              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Phase 1: Fundamentals (Month 1-2)

### Week 1-2: Linux

**Học gì:**

- [ ] Terminal commands (navigation, files, permissions)
- [ ] Text processing (grep, sed, awk)
- [ ] Process management
- [ ] Package management
- [ ] Systemd services

**Practice:**

- Setup Linux server (VM hoặc cloud)
- Cài đặt và cấu hình Nginx
- Troubleshoot common issues

**Module:** [01_LINUX](../01_LINUX/README.md)

---

### Week 3-4: Networking

**Học gì:**

- [ ] TCP/IP model
- [ ] DNS, HTTP/HTTPS
- [ ] Ports và protocols
- [ ] Firewall basics
- [ ] Load balancing concepts

**Practice:**

- Configure DNS records
- Setup SSL certificate
- Debug network issues

**Module:** [02_NETWORKING](../02_NETWORKING/README.md)

---

### Week 5-6: Scripting

**Học gì:**

- [ ] Bash scripting
- [ ] Python basics
- [ ] Automation scripts
- [ ] Cron jobs

**Practice:**

- Viết backup script
- Viết health check script
- Automate repetitive tasks

**Module:** [03_SCRIPTING](../03_SCRIPTING/README.md)

---

### Week 7-8: Git & Version Control

**Học gì:**

- [ ] Git basics (add, commit, push, pull)
- [ ] Branching strategies
- [ ] Merge conflicts
- [ ] GitHub/GitLab workflow

**Practice:**

- Tạo và quản lý repository
- Pull request workflow
- Resolve conflicts

**Module:** [04_GIT](../04_GIT/README.md)

---

## 🚀 Phase 2: Core DevOps (Month 3-4)

### Week 9-10: Web Servers & Databases

**Học gì:**

- [ ] Nginx configuration
- [ ] Reverse proxy, load balancing
- [ ] PostgreSQL/MySQL basics
- [ ] Redis caching

**Practice:**

- Deploy web app with Nginx
- Setup database with backup

**Modules:** [05_WEB_SERVERS](../05_WEB_SERVERS/README.md), [06_DATABASES](../06_DATABASES/README.md)

---

### Week 11-14: Docker

**Học gì:**

- [ ] Container concepts
- [ ] Dockerfile best practices
- [ ] Docker Compose
- [ ] Multi-stage builds
- [ ] Container networking

**Practice:**

- Dockerize multiple applications
- Create development environments
- Build production images

**Module:** [07_DOCKER](../07_DOCKER/README.md)

---

### Week 15-16: CI/CD

**Học gì:**

- [ ] CI/CD concepts
- [ ] GitHub Actions
- [ ] Pipeline design
- [ ] Testing in CI
- [ ] Artifact management

**Practice:**

- Setup CI pipeline cho project
- Automate testing
- Build và push Docker images

**Modules:** [08_CI](../08_CI/README.md), [10_CD](../10_CD/README.md)

---

## ⚡ Phase 3: Advanced (Month 5-6)

### Week 17-20: Kubernetes

**Học gì:**

- [ ] K8s architecture
- [ ] Pods, Deployments, Services
- [ ] ConfigMaps, Secrets
- [ ] Ingress, Storage
- [ ] Helm charts

**Practice:**

- Deploy app to K8s
- Setup Ingress với SSL
- Implement rolling updates

**Module:** [09_KUBERNETES](../09_KUBERNETES/README.md)

---

### Week 21-22: Cloud (AWS/GCP/Azure)

**Học gì:**

- [ ] Cloud concepts (IaaS, PaaS, SaaS)
- [ ] Compute (EC2, VMs)
- [ ] Storage (S3, Cloud Storage)
- [ ] Networking (VPC)
- [ ] Managed services

**Practice:**

- Deploy infrastructure on cloud
- Use managed Kubernetes (EKS/GKE/AKS)

**Module:** [11_CLOUD](../11_CLOUD/README.md)

---

### Week 23-24: Infrastructure as Code

**Học gì:**

- [ ] Terraform basics
- [ ] Modules và state management
- [ ] Ansible playbooks
- [ ] Configuration management

**Practice:**

- Provision cloud infra with Terraform
- Configure servers with Ansible

**Module:** [12_IAC](../12_IAC/README.md)

---

## 🎓 Phase 4: Specialization (Month 7+)

### Security (DevSecOps)

- [ ] Security scanning in CI
- [ ] Container security
- [ ] Secret management
- [ ] RBAC và policies

**Module:** [13_SECURITY](../13_SECURITY/README.md)

---

### Observability

- [ ] Prometheus & Grafana
- [ ] Logging (ELK/Loki)
- [ ] Distributed tracing
- [ ] Alerting

**Module:** [14_OBSERVABILITY](../14_OBSERVABILITY/README.md)

---

### SRE Practices

- [ ] SLI/SLO/SLA
- [ ] Error budgets
- [ ] Incident management
- [ ] Postmortems

**Module:** [15_SRE](../15_SRE/README.md)

---

## 📅 Weekly Schedule Template

```
Monday     - Learn theory (README.md)
Tuesday    - Practice labs (LABS.md)
Wednesday  - Continue labs
Thursday   - Troubleshooting practice (SCENARIOS.md)
Friday     - Mini project
Weekend    - Review & document learning
```

---

## 🏆 Milestones & Checkpoints

### Checkpoint 1: End of Month 2

- [ ] Comfortable with Linux terminal
- [ ] Understand networking basics
- [ ] Can write automation scripts
- [ ] Proficient with Git

### Checkpoint 2: End of Month 4

- [ ] Can Dockerize any application
- [ ] Understand CI/CD pipelines
- [ ] Setup complete dev environment
- [ ] Built 2-3 personal projects

### Checkpoint 3: End of Month 6

- [ ] Deploy apps to Kubernetes
- [ ] Work with cloud platforms
- [ ] Write Infrastructure as Code
- [ ] Complete Capstone Project

### Checkpoint 4: Month 7+

- [ ] Security integration
- [ ] Monitoring setup
- [ ] On-call ready
- [ ] Ready for interviews

---

## 💼 Portfolio Projects

### Beginner Project

**Personal Website với CI/CD**

- Source code on GitHub
- Dockerized application
- Automated deployment with GitHub Actions
- Hosted on cloud (AWS/GCP free tier)

### Intermediate Project

**Microservices Application**

- 2-3 services
- Docker Compose cho local dev
- Kubernetes manifests
- Monitoring với Prometheus/Grafana

### Advanced Project

**Complete DevOps Pipeline**

- Infrastructure as Code (Terraform)
- GitOps với ArgoCD
- Full observability stack
- Chaos engineering tests

---

## 📖 Recommended Resources

### Books

- "The Phoenix Project"
- "The DevOps Handbook"
- "Site Reliability Engineering" (Google)
- "Kubernetes Up & Running"

### Online

- Linux Academy / A Cloud Guru
- Kubernetes.io tutorials
- AWS/GCP/Azure free courses
- YouTube channels: TechWorld with Nana, NetworkChuck

### Certifications (Optional)

- AWS Solutions Architect
- CKA (Certified Kubernetes Administrator)
- Terraform Associate

---

## 🚦 How to Know You're Ready

### For Junior Position

- [ ] Deploy containerized app to cloud
- [ ] Write working CI/CD pipeline
- [ ] Debug common issues independently
- [ ] Understand basic networking

### For Mid Position

- [ ] Design and implement complete pipeline
- [ ] Work with Kubernetes in production
- [ ] Write Infrastructure as Code
- [ ] Handle on-call incidents

### For Senior Position

- [ ] Design scalable architectures
- [ ] Lead DevOps transformations
- [ ] Mentor junior engineers
- [ ] Make build vs buy decisions

---

**Good luck on your DevOps journey! 🚀**
