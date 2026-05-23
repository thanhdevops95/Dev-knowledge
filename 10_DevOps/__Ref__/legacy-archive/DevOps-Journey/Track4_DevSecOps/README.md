# 🔐 Track 4: DevSecOps

[![Duration](https://img.shields.io/badge/Duration-4--6%20weeks-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Advanced-red?style=flat-square)](.)
[![Prerequisites](https://img.shields.io/badge/Prerequisites-Track%201--3-green?style=flat-square)](../Track3_Cloud_Network_Design/)

> **Security-First DevOps** - Integrate security into every stage of CI/CD pipeline.
>
> *DevOps bảo mật - Tích hợp security vào mọi giai đoạn của CI/CD pipeline.*

---

## 🎯 Track Objectives (Mục Tiêu)

After completing Track 4, you will (Sau khi hoàn thành Track 4, bạn sẽ):

- ✅ Implement SAST - Static Application Security Testing (Triển khai SAST)
- ✅ Implement DAST - Dynamic Application Security Testing (Triển khai DAST)
- ✅ Container image scanning and vulnerability management (Quét container và quản lý lỗ hổng)
- ✅ Secrets management with HashiCorp Vault (Quản lý secrets với Vault)
- ✅ Infrastructure security hardening (Bảo mật hạ tầng)
- ✅ Compliance as Code (Tuân thủ dạng code)
- ✅ **Build Secure CI/CD Pipeline end-to-end** (Xây dựng pipeline bảo mật)

---

## 🤔 Why This Track? (Tại sao học Track này?)

You've built infrastructure and CI/CD. But if code has security vulnerabilities → **entire system gets hacked**.

*Bạn đã build được infrastructure và CI/CD. Nhưng nếu code có lỗ hổng bảo mật → **toàn bộ hệ thống bị hack**.*

| Market Reality (Thực tế thị trường) | Statistics (Số liệu) |
|------------------------------------|---------------------|
| Data breaches due to misconfigs | 21% (according to Verizon) *(21% theo Verizon)* |
| Time to detect breach | ~200 days (too late!) *(~200 ngày - quá muộn!)* |
| Cost of a breach | $4.45 million average *(4.45 triệu đô trung bình)* |
| Companies shifting left | 70% are adopting DevSecOps *(70% đang áp dụng DevSecOps)* |

**"Shift Left"** = Find security bugs IN the pipeline, BEFORE deploying, not AFTER being hacked.

*"Shift Left" = Tìm lỗi bảo mật TRONG pipeline, TRƯỚC khi deploy, không phải SAU khi bị hack.*

**Goal of this Track:** You will build a secure CI/CD pipeline with SAST, DAST, secret scanning, and policy as code.

*Điểm đến của Track này: Bạn sẽ build secure CI/CD pipeline với SAST, DAST, secret scanning, và policy as code.*

---

## 📋 Prerequisites (Điều kiện tiên quyết)

Before starting Track 4, you should complete (Trước khi bắt đầu Track 4, bạn cần hoàn thành):

- ✅ **Track 1, 2 & 3**
- ✅ Have experience with CI/CD pipelines (Có kinh nghiệm với CI/CD)
- ✅ Understand container security basics (Hiểu container security cơ bản)
- ✅ Familiar with cloud security concepts (Quen với cloud security)

---

## 📚 Module List (Danh Sách Modules)

| # | Module | Duration (Thời gian) | Description (Mô tả) |
|---|--------|----------------------|---------------------|
| 4.1 | [Security in Pipeline](./4.1_Security_in_Pipeline/) | 2 weeks | SAST, DAST, SCA, Container Scanning |
| 4.2 | [Infrastructure Security](./4.2_Infra_Security/) | 2 weeks | Secrets Management, Hardening, Compliance |
| 4.3 | [**Capstone Project**](./4.3_Capstone_Project/) | 1-2 weeks | 🎯 Secure CI/CD Pipeline |

---

## 🗓️ Suggested Schedule (Lịch Trình Đề Xuất)

### Week 1-2: Security in Pipeline

```
Week 1:
- Day 1-2: SAST with SonarQube
- Day 3-4: Dependency scanning (SCA)
- Day 5-7: Container image scanning with Trivy

Week 2:
- Day 1-3: DAST with OWASP ZAP
- Day 4-5: Secret scanning (GitLeaks, TruffleHog)
- Day 6-7: Integrating security gates in CI/CD
```

### Week 3-4: Infrastructure Security

```
Week 3:
- Day 1-3: Secrets management with Vault
- Day 4-5: Cloud security best practices
- Day 6-7: Network security & firewalls

Week 4:
- Day 1-3: Compliance as Code (OPA, Checkov)
- Day 4-5: Security monitoring & alerting
- Day 6-7: Incident response basics
```

### Week 5-6: Capstone Project

```
Week 5:
- Day 1-2: Architecture design
- Day 3-5: Implementation
- Day 6-7: Security testing

Week 6:
- Day 1-3: Remediation & hardening
- Day 4-5: Documentation
- Day 6-7: Review & presentation
```

---

## 🛠️ Tools Used (Công cụ sử dụng)

### Static Analysis (SAST)

| Tool | Purpose (Mục đích) | Documentation |
|------|-------------------|---------------|
| **SonarQube** | Code quality & security | [sonarqube.org](https://docs.sonarqube.org/) |
| **Semgrep** | Static analysis | [semgrep.dev](https://semgrep.dev/docs/) |
| **Bandit** | Python security | [bandit.readthedocs.io](https://bandit.readthedocs.io/) |

### Dynamic Analysis (DAST)

| Tool | Purpose (Mục đích) | Documentation |
|------|-------------------|---------------|
| **OWASP ZAP** | Web app security testing | [zaproxy.org](https://www.zaproxy.org/docs/) |
| **Nuclei** | Vulnerability scanning | [nuclei.projectdiscovery.io](https://nuclei.projectdiscovery.io/) |

### Container Security

| Tool | Purpose (Mục đích) | Documentation |
|------|-------------------|---------------|
| **Trivy** | Container scanning | [aquasecurity.github.io/trivy](https://aquasecurity.github.io/trivy/) |
| **Grype** | Vulnerability scanner | [github.com/anchore/grype](https://github.com/anchore/grype) |
| **Falco** | Runtime security | [falco.org](https://falco.org/docs/) |

### Secrets Management

| Tool | Purpose (Mục đích) | Documentation |
|------|-------------------|---------------|
| **HashiCorp Vault** | Secrets management | [vaultproject.io](https://www.vaultproject.io/docs) |
| **AWS Secrets Manager** | AWS secrets | [aws.amazon.com](https://docs.aws.amazon.com/secretsmanager/) |
| **GitLeaks** | Git secret scanning | [gitleaks.io](https://github.com/gitleaks/gitleaks) |

### Compliance & Policy

| Tool | Purpose (Mục đích) | Documentation |
|------|-------------------|---------------|
| **Checkov** | IaC scanning | [checkov.io](https://www.checkov.io/1.Welcome/Quick%20Start.html) |
| **OPA/Gatekeeper** | Policy as Code | [openpolicyagent.org](https://www.openpolicyagent.org/docs/) |
| **tfsec** | Terraform security | [tfsec.dev](https://aquasecurity.github.io/tfsec/) |

---

## 🔒 Security Concepts Covered

### OWASP Top 10

1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entities (XXE)
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting (XSS)
8. Insecure Deserialization
9. Using Components with Known Vulnerabilities
10. Insufficient Logging & Monitoring

### DevSecOps Practices (Thực hành DevSecOps)

- **Shift Left** - Security early in SDLC (Bảo mật sớm trong vòng đời phát triển)
- **Automation** - Automated security testing (Kiểm thử bảo mật tự động)
- **Continuous** - Security in every pipeline run (Bảo mật trong mọi lần chạy pipeline)
- **Collaboration** - Dev, Sec, Ops working together (Làm việc cùng nhau)

---

## 🎯 Capstone Project Preview

### **Secure CI/CD Pipeline Implementation**

You will build (Bạn sẽ xây dựng):

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Secure CI/CD Pipeline                            │
│                                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │  Code   │───▶│  Build  │───▶│  Test   │───▶│ Deploy  │         │
│  │  Commit │    │  Stage  │    │  Stage  │    │  Stage  │         │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘         │
│       │              │              │              │               │
│       ▼              ▼              ▼              ▼               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │ Secret  │    │  SAST   │    │  DAST   │    │ Runtime │         │
│  │ Scan    │    │ Scan    │    │ Scan    │    │ Security│         │
│  │(GitLeaks)│   │(SonarQube)│  │(OWASP ZAP)│  │(Falco)  │         │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘         │
│       │              │              │              │               │
│       ▼              ▼              ▼              ▼               │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │   SCA   │    │Container│    │ Policy  │    │ Monitor │         │
│  │  Scan   │    │ Scan    │    │ Check   │    │ & Alert │         │
│  │(Snyk)   │    │(Trivy)  │    │(OPA)    │    │(Grafana)│         │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘         │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                   HashiCorp Vault                             │ │
│  │              (Secrets Management Layer)                       │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │              Security Dashboard & Reporting                   │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Security Gates (Các cổng bảo mật)

- ⛔ **Pre-commit**: Secret scanning (Quét secrets)
- ⛔ **Build**: SAST, SCA, Container scan (Quét code, dependencies, container)
- ⛔ **Test**: DAST, Integration tests (Kiểm thử động)
- ⛔ **Deploy**: Policy compliance check (Kiểm tra tuân thủ)
- ⛔ **Runtime**: Continuous monitoring (Giám sát liên tục)

### Deliverables (Sản phẩm bàn giao)

- 🔄 Complete CI/CD pipeline with security gates (Pipeline hoàn chỉnh với security gates)
- 📊 Security dashboard with metrics (Dashboard bảo mật)
- 📝 Security policies documented (Tài liệu chính sách)
- 🔐 Vault integration for secrets (Tích hợp Vault)
- 📋 Compliance reports (Báo cáo tuân thủ)

👉 **[View Capstone Details →](./4.3_Capstone_Project/)** | **[Xem chi tiết →](./4.3_Capstone_Project/)**

---

## 📊 Evaluation (Đánh Giá)

### Track Completion Criteria (Tiêu chí hoàn thành Track)

- ✅ Complete all 2 modules (Hoàn thành tất cả 2 modules)
- ✅ Submit Capstone Project
- ✅ Pass security audit of pipeline (Qua kiểm tra bảo mật pipeline)
- ✅ Demo working security gates

---

## 📚 Certifications Related (Chứng chỉ liên quan)

After this Track, you can prepare for (Sau Track này, bạn có thể chuẩn bị cho):

| Certification | Provider | Level |
|--------------|----------|-------|
| **AWS Security Specialty** | AWS | Professional |
| **CKS** (Certified Kubernetes Security) | CNCF | Advanced |
| **CompTIA Security+** | CompTIA | Foundational |
| **OSCP** | Offensive Security | Advanced |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [Track 3: Cloud](../Track3_Cloud_Network_Design/) | **Track 4** | [Track 5: Career](../Track5_Career_Path/) |

---

## 📖 Getting Started (Bắt Đầu)

```bash
# Start with Module 4.1 (Bắt đầu với Module 4.1)
cd 4.1_Security_in_Pipeline
cat README.md
```

**📚 Start learning:** [4.1 Security in Pipeline →](./4.1_Security_in_Pipeline/)

---

<div align="center">

**🔐 Security is Everyone's Responsibility! 🔐**

*Bảo mật là trách nhiệm của tất cả mọi người!*

</div>
