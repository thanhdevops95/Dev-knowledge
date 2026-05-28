# 🏆 Module 4.3: DevSecOps Capstone Project

> **Secure CI/CD Pipeline**
>
> *Pipeline CI/CD an toàn*

---

## 🎯 Project Overview (Tổng quan dự án)

Build a complete secure CI/CD pipeline with all security controls integrated.

*Xây dựng pipeline CI/CD an toàn hoàn chỉnh với tất cả security controls được tích hợp.*

---

## 📋 Requirements (Yêu cầu)

### Pipeline Architecture (Kiến trúc Pipeline)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Secure CI/CD Pipeline                            │
│                                                                     │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐ │
│  │  Source   │───▶│   Build   │───▶│   Test    │───▶│  Deploy   │ │
│  └───────────┘    └───────────┘    └───────────┘    └───────────┘ │
│       │                │                │                │         │
│       ▼                ▼                ▼                ▼         │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐   │
│  │ Secret  │      │  SAST   │      │  DAST   │      │ Policy  │   │
│  │ Scan    │      │  + SCA  │      │  Scan   │      │ Check   │   │
│  │(GitLeaks)│     │(Sonar)  │      │(ZAP)    │      │(OPA)    │   │
│  └─────────┘      └─────────┘      └─────────┘      └─────────┘   │
│       │                │                │                │         │
│       │           ┌─────────┐           │                │         │
│       │           │Container│           │                │         │
│       │           │ Scan    │           │                │         │
│       │           │(Trivy)  │           │                │         │
│       │           └─────────┘           │                │         │
│       │                │                │                │         │
│       └────────────────┼────────────────┼────────────────┘         │
│                        ▼                                            │
│              ┌─────────────────────┐                               │
│              │  Security Dashboard │                               │
│              │  (Grafana/DefectDojo)│                              │
│              └─────────────────────┘                               │
│                        │                                            │
│              ┌─────────▼─────────┐                                 │
│              │   HashiCorp Vault  │                                 │
│              │   (Secrets Mgmt)   │                                 │
│              └───────────────────┘                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Pipeline Stages (Các giai đoạn Pipeline)

| Stage | Tool | Description (Mô tả) |
|-------|------|---------------------|
| **1. Source** | Gitleaks | Secret scanning - *Quét secrets* |
| **2. Build** | SonarQube, npm audit | SAST + Dependency scan - *Quét mã nguồn, dependencies* |
| **3. Container** | Trivy | Image scanning - *Quét image* |
| **4. Test** | OWASP ZAP | DAST - *Kiểm thử động* |
| **5. Deploy** | OPA, Checkov | Policy checks - *Kiểm tra chính sách* |
| **6. Runtime** | Falco | Runtime monitoring - *Giám sát runtime* |

---

### GitLab CI Example (Ví dụ GitLab CI)

```yaml
# .gitlab-ci.yml
stages:
  - secrets
  - build
  - security
  - test
  - deploy

include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

# Custom Gitleaks scan
gitleaks:
  stage: secrets
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --verbose --report-format json --report-path gitleaks-report.json
  artifacts:
    paths:
      - gitleaks-report.json
    when: always

# Custom SonarQube
sonarqube:
  stage: build
  image: sonarsource/sonar-scanner-cli
  script:
    - sonar-scanner
        -Dsonar.projectKey=$CI_PROJECT_NAME
        -Dsonar.sources=.
        -Dsonar.host.url=$SONAR_HOST_URL
        -Dsonar.login=$SONAR_TOKEN
  allow_failure: true

# Container scanning with Trivy
trivy:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  allow_failure: false
  needs:
    - build

# DAST with OWASP ZAP
dast:
  stage: test
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t $STAGING_URL -r zap-report.html
  artifacts:
    paths:
      - zap-report.html
    when: always
  needs:
    - deploy-staging

# IaC scanning with Checkov
checkov:
  stage: security
  image: bridgecrew/checkov
  script:
    - checkov -d terraform/ --output cli --output junitxml > checkov-report.xml
  artifacts:
    reports:
      junit: checkov-report.xml

# Deploy to staging
deploy-staging:
  stage: deploy
  script:
    - kubectl apply -k k8s/staging/
  environment:
    name: staging
    url: $STAGING_URL

# Deploy to production (manual)
deploy-production:
  stage: deploy
  script:
    - kubectl apply -k k8s/production/
  environment:
    name: production
  when: manual
  only:
    - main
```

---

### Security Controls Checklist (Kiểm soát bảo mật)

- [ ] No secrets in code (Không có secrets trong code)
- [ ] All dependencies scanned (Tất cả dependencies đã quét)
- [ ] Container runs as non-root (Container chạy không phải root)
- [ ] Read-only root filesystem (Filesystem root chỉ đọc)
- [ ] Network policies applied (Đã áp dụng network policies)
- [ ] RBAC configured (Đã cấu hình RBAC)
- [ ] Audit logging enabled (Đã bật ghi nhật ký kiểm toán)
- [ ] Alerting configured (Đã cấu hình cảnh báo)
- [ ] Secrets managed by Vault (Secrets được Vault quản lý)

---

### Tools (Công cụ)

| Category | Tool | Purpose |
|----------|------|---------|
| **CI/CD** | GitLab CI / Jenkins | Pipeline automation |
| **SAST** | SonarQube, Semgrep | Static code analysis |
| **SCA** | npm audit, Snyk | Dependency scanning |
| **Container** | Trivy, Docker Scout | Image vulnerability scanning |
| **DAST** | OWASP ZAP, Nuclei | Dynamic testing |
| **Secrets** | HashiCorp Vault | Secrets management |
| **Policy** | OPA, Checkov | Policy as Code |
| **Runtime** | Falco | Runtime security |
| **Dashboard** | Grafana, DefectDojo | Security metrics |

---

## ✅ Deliverables (Sản phẩm bàn giao)

- [ ] Complete CI/CD pipeline with security gates (Pipeline hoàn chỉnh với security gates)
- [ ] All security scans passing (Tất cả quét bảo mật pass)
- [ ] Security dashboard with metrics (Dashboard bảo mật với metrics)
- [ ] Security documentation (Tài liệu bảo mật)
- [ ] Incident response plan (Kế hoạch xử lý sự cố)

---

## 📊 Evaluation (Đánh giá)

| Criteria (Tiêu chí) | Weight (Trọng số) |
|---------------------|-------------------|
| Pipeline implementation (Triển khai pipeline) | 30% |
| Security controls (Kiểm soát bảo mật) | 30% |
| Automation level (Mức độ tự động hóa) | 20% |
| Documentation (Tài liệu) | 20% |

---

## 📁 Project Structure (Cấu trúc dự án)

```
devsecops-capstone/
├── .gitlab-ci.yml              # GitLab CI pipeline
├── app/
│   ├── Dockerfile
│   └── src/
├── terraform/
│   └── main.tf
├── k8s/
│   ├── base/
│   ├── staging/
│   └── production/
├── security/
│   ├── policies/               # OPA policies
│   ├── vault-config/           # Vault configuration
│   └── alerts/                 # Alert rules
├── docs/
│   ├── SECURITY.md
│   └── INCIDENT_RESPONSE.md
└── README.md
```

---

## 📖 Resources (Tài liệu tham khảo)

- [GitLab Security Scanning](https://docs.gitlab.com/ee/user/application_security/)
- [OWASP DevSecOps Maturity Model](https://owasp.org/www-project-devsecops-maturity-model/)
- [HashiCorp Vault](https://www.vaultproject.io/docs)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [4.2 Infra Security](../4.2_Infra_Security/) | **4.3 Capstone** | [Track 5](../../Track5_Career_Path/) |

---

**Build secure pipelines! 🔐**

*Xây dựng pipeline an toàn!*

</div>
