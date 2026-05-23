# Module 13: SECURITY (DevSecOps)

> **"Security không phải giai đoạn cuối - mà là phần của mọi giai đoạn"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu DevSecOps principles
- ✅ Secrets management
- ✅ Container security
- ✅ SAST và DAST
- ✅ Dependency scanning
- ✅ Security trong CI/CD
- ✅ OWASP Top 10
- ✅ Compliance basics

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| DevSecOps | DevSecOps | Security trong DevOps |
| Shift Left | Shift Left | Đưa security sớm hơn |
| SAST | Static Application Security Testing | Scan code tĩnh |
| DAST | Dynamic Application Security Testing | Scan app đang chạy |
| SCA | Software Composition Analysis | Scan dependencies |
| Secrets | Secrets | Thông tin nhạy cảm |
| Vault | HashiCorp Vault | Secrets management tool |
| CVE | Common Vulnerabilities and Exposures | Lỗ hổng công khai |
| CVSS | Common Vulnerability Scoring System | Điểm đánh giá lỗ hổng |
| OWASP | Open Web Application Security Project | Tổ chức bảo mật web |
| SQL Injection | SQL Injection | Tấn công SQL |
| XSS | Cross-Site Scripting | Tấn công script |
| CSRF | Cross-Site Request Forgery | Tấn công request |
| IAM | Identity and Access Management | Quản lý định danh |
| RBAC | Role-Based Access Control | Phân quyền theo role |
| mTLS | Mutual TLS | TLS 2 chiều |
| Zero Trust | Zero Trust | Không tin ai mặc định |
| Compliance | Compliance | Tuân thủ quy định |
| SOC2 | SOC 2 | Chuẩn bảo mật |
| GDPR | General Data Protection Regulation | Quy định bảo vệ dữ liệu EU |

---

## ✅ Checklist Labs

### Labs DevSecOps Concepts

- [ ] Lab 1: DevSecOps vs traditional security
- [ ] Lab 2: Shift Left principle
- [ ] Lab 3: Security gates trong pipeline
- [ ] Lab 4: OWASP Top 10 overview

### Labs Secrets Management

- [ ] Lab 5: Environment variables pitfalls
- [ ] Lab 6: .env files và .gitignore
- [ ] Lab 7: git-secrets setup
- [ ] Lab 8: gitleaks scanning
- [ ] Lab 9: HashiCorp Vault installation
- [ ] Lab 10: Vault secrets engine
- [ ] Lab 11: Vault dynamic secrets
- [ ] Lab 12: Vault với Kubernetes
- [ ] Lab 13: AWS Secrets Manager
- [ ] Lab 14: AWS Parameter Store
- [ ] Lab 15: Sealed Secrets cho K8s

### Labs Container Security

- [ ] Lab 16: Trivy image scanning
- [ ] Lab 17: Docker Scout
- [ ] Lab 18: Grype scanning
- [ ] Lab 19: Non-root containers
- [ ] Lab 20: Read-only root filesystem
- [ ] Lab 21: Security contexts trong K8s
- [ ] Lab 22: Pod Security Standards
- [ ] Lab 23: Network Policies
- [ ] Lab 24: Falco runtime security

### Labs SAST

- [ ] Lab 25: Bandit cho Python
- [ ] Lab 26: Semgrep basics
- [ ] Lab 27: SonarQube setup
- [ ] Lab 28: SonarQube analysis
- [ ] Lab 29: ESLint security rules
- [ ] Lab 30: SAST trong CI pipeline

### Labs Dependency Scanning (SCA)

- [ ] Lab 31: npm audit
- [ ] Lab 32: pip-audit
- [ ] Lab 33: Snyk CLI
- [ ] Lab 34: OWASP Dependency Check
- [ ] Lab 35: Dependabot setup
- [ ] Lab 36: Renovate bot

### Labs DAST

- [ ] Lab 37: OWASP ZAP basics
- [ ] Lab 38: ZAP automated scan
- [ ] Lab 39: Nikto web scanner
- [ ] Lab 40: DAST trong CI/CD

### Labs Infrastructure Security

- [ ] Lab 41: tfsec cho Terraform
- [ ] Lab 42: checkov
- [ ] Lab 43: Kyverno policies
- [ ] Lab 44: OPA/Gatekeeper
- [ ] Lab 45: AWS Config rules

### Labs Network Security

- [ ] Lab 46: TLS certificates
- [ ] Lab 47: mTLS concepts
- [ ] Lab 48: Service mesh security
- [ ] Lab 49: WAF basics

### Labs Security trong CI/CD

- [ ] Lab 50: Security pipeline design
- [ ] Lab 51: Pre-commit hooks security
- [ ] Lab 52: PR security checks
- [ ] Lab 53: Artifact signing
- [ ] Lab 54: Supply chain security
- [ ] Lab 55: SBOM generation

### Labs Counter App Security

- [ ] Lab 56: Security scan Counter App
- [ ] Lab 57: Fix vulnerabilities
- [ ] Lab 58: Secrets management cho Counter App
- [ ] Lab 59: Security trong Counter App CI

### Labs Compliance

- [ ] Lab 60: Compliance as Code concepts
- [ ] Lab 61: Policy as Code
- [ ] Lab 62: Audit logging
- [ ] Lab 63: AWS CloudTrail
- [ ] Lab 64: Security benchmarks (CIS)

---

## 🚨 Checklist Scenarios

### Scenarios về Secrets

- [ ] Scenario 1: Secret committed to Git
- [ ] Scenario 2: Secret exposed in logs
- [ ] Scenario 3: Secret in Docker image layers
- [ ] Scenario 4: Vault token expired
- [ ] Scenario 5: Secret rotation needed
- [ ] Scenario 6: Developer needs temporary secret access

### Scenarios về Vulnerabilities

- [ ] Scenario 7: Critical CVE in base image
- [ ] Scenario 8: Vulnerable dependency discovered
- [ ] Scenario 9: Zero-day vulnerability response
- [ ] Scenario 10: False positive in scan results
- [ ] Scenario 11: Legacy code with many vulnerabilities

### Scenarios về Container Security

- [ ] Scenario 12: Container running as root
- [ ] Scenario 13: Container escape attempt
- [ ] Scenario 14: Malicious image pulled
- [ ] Scenario 15: Resource exhaustion attack

### Scenarios về Network

- [ ] Scenario 16: Unauthorized API access
- [ ] Scenario 17: SQL injection detected
- [ ] Scenario 18: XSS attack in production
- [ ] Scenario 19: DDoS attack response
- [ ] Scenario 20: Man-in-the-middle concern

### Scenarios về Access Control

- [ ] Scenario 21: Excessive permissions
- [ ] Scenario 22: Orphaned service accounts
- [ ] Scenario 23: Admin access abuse
- [ ] Scenario 24: API key leaked

### Scenarios về Compliance

- [ ] Scenario 25: Audit failed
- [ ] Scenario 26: GDPR data request
- [ ] Scenario 27: Security incident reporting
- [ ] Scenario 28: Evidence collection for audit

---

## ⏱️ Thời lượng

**Ước tính:** 4-6 giờ

| Phần | Thời gian |
|------|-----------|
| DevSecOps concepts (Labs 1-4) | 0.5 giờ |
| Secrets management (Labs 5-15) | 1.5 giờ |
| Container security (Labs 16-24) | 1 giờ |
| SAST & SCA (Labs 25-36) | 1 giờ |
| DAST & Infrastructure (Labs 37-49) | 1 giờ |
| CI/CD Security & Compliance | 0.5 giờ |
| Counter App + Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [OWASP](https://owasp.org/)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [Trivy](https://trivy.dev/)
- [Snyk](https://snyk.io/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
