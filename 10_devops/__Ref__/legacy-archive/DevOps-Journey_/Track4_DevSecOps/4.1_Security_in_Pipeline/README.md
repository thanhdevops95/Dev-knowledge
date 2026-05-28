# 🔐 Module 4.1: Security in Pipeline

[![Duration](https://img.shields.io/badge/Duration-2%20weeks-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Shift-Left Security** - Integrate security into CI/CD pipeline.
>
> *Bảo mật Shift-Left - Tích hợp bảo mật vào CI/CD pipeline.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Implement SAST - Static Application Security Testing (Triển khai SAST)
- ✅ Use DAST - Dynamic Application Security Testing (Sử dụng DAST)
- ✅ Perform SCA - Software Composition Analysis (Thực hiện SCA)
- ✅ Configure secret scanning (Cấu hình quét secrets)
- ✅ Secure containers (Bảo mật container)
- ✅ Apply Policy as Code (Áp dụng Policy as Code)

---

## 📋 Prerequisites (Điều kiện tiên quyết)

- Complete Track 1-3 (Hoàn thành Track 1-3)
- Familiar with GitLab CI or GitHub Actions (Quen với GitLab CI hoặc GitHub Actions)
- Docker experience (Kinh nghiệm Docker)

---

## 📚 Content (Nội dung)

### 1. What is DevSecOps and Shift-Left Security? (DevSecOps và Shift-Left Security là gì?)

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> Your team releases a new feature to production. 2 weeks later, a security researcher finds a critical SQL injection vulnerability and posts it on Twitter. Your company is on the news. Customers lose trust. The fix takes 2 hours, but the reputation damage takes months to recover.
>
> *Team của bạn release tính năng mới lên production. 2 tuần sau, một security researcher tìm thấy lỗ hổng SQL injection nghiêm trọng và đăng lên Twitter. Công ty bạn lên báo. Khách hàng mất niềm tin. Việc sửa lỗi mất 2 tiếng, nhưng phục hồi uy tín mất hàng tháng.*
>
> **With DevSecOps, that SQL injection would have been caught by SAST scanner BEFORE it reached production!**
>
> *Với DevSecOps, lỗ hổng SQL injection đó đã bị SAST scanner bắt TRƯỚC KHI đến production!*

#### The Traditional Problem (Vấn đề truyền thống)

Traditionally, security was checked at the **end** of development, before release. This led to:

*Trước đây, bảo mật thường được kiểm tra **ở cuối** quá trình phát triển, trước khi release. Điều này dẫn đến:*

```ini
┌─────────────────────────────────────────────────────────────────┐
│   MÔ HÌNH TRUYỀN THỐNG (Traditional Model)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Dev → Dev → Dev → Dev → QA → SECURITY → Release               │
│                                    ↑                             │
│                              Phát hiện lỗi ở đây                 │
│                              = TỐN KÉM để sửa! 💸                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

- 💸 **Chi phí cao**: Sửa lỗi ở production đắt gấp 100 lần so với sửa ở development
- ⏰ **Delay release**: Phải quay lại sửa code, re-test
- 😡 **Developers bực mình**: Lỗi phát hiện muộn, context đã mất

#### Solution: Shift-Left Security (Giải pháp: Shift-Left Security)

**Shift-Left** means moving security checks to the **left** (earlier) in the pipeline.

*Shift-Left có nghĩa là di chuyển security checks sang **bên trái** (sớm hơn) trong pipeline.*

```ini
┌─────────────────────────────────────────────────────────────────┐
│   MÔ HÌNH SHIFT-LEFT (Shift-Left Model)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Dev → SECURITY → Build → SECURITY → Deploy → SECURITY         │
│          ↑                    ↑                  ↑               │
│       SAST, Lint         Container Scan      DAST               │
│       (Chi phí thấp)     (Nhanh, tự động)    (Runtime)          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

#### Types of Security Testing (Các loại Security Testing)

| Type (Loại) | When (Thời điểm) | Tools (Công cụ) | Detects (Phát hiện) |
|-------------|------------------|-----------------|---------------------|
| **SAST** (Static) | Code commit | SonarQube, CodeQL | SQL Injection, XSS in code *(Trong code)* |
| **SCA** (Composition) | Build | Snyk, npm audit | Vulnerabilities in dependencies *(Trong dependencies)* |
| **Container Scan** | Build image | Trivy, Docker Scout | CVE in base image *(Trong base image)* |
| **Secret Scan** | Commit | Gitleaks, TruffleHog | API keys, passwords in code *(Trong code)* |
| **DAST** (Dynamic) | Staging | OWASP ZAP, Nuclei | Vulnerabilities when app runs *(Khi app chạy)* |

---

### 2. SAST - Static Application Security Testing

#### What is SAST? (SAST là gì?)

**SAST** analyzes source code to find security flaws **without running the application**. It's like having a security expert automatically review your code.

*SAST phân tích source code để tìm lỗi bảo mật **mà không cần chạy ứng dụng**. Nó giống như có một security expert review code của bạn tự động.*

#### GitLab CI - SAST (Chính)

GitLab provides built-in SAST, just include the template:

*GitLab cung cấp SAST sẵn có, chỉ cần include template:*

```yaml
# .gitlab-ci.yml
include:
  - template: Security/SAST.gitlab-ci.yml

sast:
  stage: test

```

#### SonarQube - Advanced SAST (SAST nâng cao)

SonarQube provides deeper analysis with a visual dashboard:

*SonarQube cung cấp phân tích sâu hơn với dashboard trực quan:*

```yaml
sonarqube:
  stage: test
  image: sonarsource/sonar-scanner-cli
  script:
    - sonar-scanner
        -Dsonar.projectKey=myproject
        -Dsonar.sources=.
        -Dsonar.host.url=$SONAR_HOST_URL
        -Dsonar.login=$SONAR_TOKEN

```

**Lưu ý:**

- `SONAR_HOST_URL` và `SONAR_TOKEN` nên lưu trong GitLab CI/CD Variables (masked)
- SonarQube server cần được setup riêng (self-hosted hoặc SonarCloud)

#### GitHub Actions - SAST (Alternative - Thay thế)

```yaml
# .github/workflows/sast.yml
- name: CodeQL Analysis
  uses: github/codeql-action/analyze@v2

# SonarQube
- name: SonarQube Scan
  uses: sonarsource/sonarqube-scan-action@master

```

---

### 2. Dependency Scanning (Quét dependencies)

#### GitLab CI - Dependency Scanning

```yaml
# .gitlab-ci.yml
include:
  - template: Security/Dependency-Scanning.gitlab-ci.yml

dependency_scanning:
  stage: test

```

#### CLI Tools (Công cụ CLI)

```bash
# npm audit (Kiểm tra npm)
npm audit
npm audit --json > npm-audit.json

# Snyk
snyk test
snyk monitor

# OWASP Dependency Check
dependency-check --project myapp --scan ./

```

---

### 3. Secret Scanning (Quét secrets)

Secret scanning detects hardcoded passwords, API keys, and tokens in your code before they're exposed.

*Secret scanning phát hiện passwords, API keys, tokens hardcode trong code trước khi chúng bị lộ.*

#### GitLab CI - Secret Detection

GitLab has built-in secret detection. Just include the template:

*GitLab có sẵn secret detection. Chỉ cần include template:*

```yaml
# .gitlab-ci.yml
include:
  - template: Security/Secret-Detection.gitlab-ci.yml

secret_detection:
  stage: test

```

#### Gitleaks

Gitleaks is a popular open-source tool for scanning secrets. Works with any Git repository.

*Gitleaks là tool mã nguồn mở phổ biến để quét secrets. Hoạt động với bất kỳ Git repository nào.*

```yaml
# GitLab CI
gitleaks:
  stage: test
  image: zricethezav/gitleaks
  script:
    - gitleaks detect --source . --verbose
  allow_failure: false

# GitHub Actions
- name: Scan for secrets (Quét secrets)
  uses: gitleaks/gitleaks-action@v2

```

#### TruffleHog

TruffleHog scans Git history for secrets, catching secrets that were committed and later removed.

*TruffleHog quét lịch sử Git tìm secrets, bắt cả secrets đã commit rồi xóa sau.*

```bash
# Scan git history (Quét lịch sử git)
trufflehog git https://gitlab.com/user/repo
trufflehog git https://github.com/user/repo

```

---

### 4. Container Scanning (Quét container)

Container scanning finds vulnerabilities in your Docker images before deployment.

*Container scanning tìm lỗ hổng trong Docker images trước khi deploy.*

#### GitLab CI - Container Scanning

```yaml
# .gitlab-ci.yml
include:
  - template: Security/Container-Scanning.gitlab-ci.yml

container_scanning:
  stage: test
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

```

#### Trivy

```yaml
# GitLab CI
trivy-scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  allow_failure: false

# Command line
trivy image myapp:latest
trivy image --severity CRITICAL myapp:latest

```

#### Docker Scout

```bash
# Built-in Docker scanning
docker scout cves myapp:latest
docker scout quickview myapp:latest

```

---

### 5. DAST - Dynamic Testing (Kiểm thử động)

#### OWASP ZAP

```yaml
# GitLab CI
dast:
  stage: test
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t https://staging.example.com -r zap-report.html
  artifacts:
    paths:
      - zap-report.html

```

#### Nuclei

```bash
# Vulnerability scanning
nuclei -u https://example.com -t cves/
nuclei -u https://example.com -severity critical,high

```

---

### 6. Policy as Code (OPA/Gatekeeper)

```rego
# policy.rego
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.spec.securityContext.runAsNonRoot
    msg := "Pods must run as non-root"
}

deny[msg] {
    input.request.kind.kind == "Deployment"
    not input.request.object.spec.template.spec.containers[_].securityContext.readOnlyRootFilesystem
    msg := "Containers must use read-only filesystem"
}

```

#### Terraform Security (IaC Scanning)

```yaml
# GitLab CI - Checkov
checkov:
  stage: test
  image: bridgecrew/checkov
  script:
    - checkov -d . --output cli --output junitxml > checkov-report.xml
  artifacts:
    reports:
      junit: checkov-report.xml

# tfsec
tfsec:
  stage: test
  image: aquasec/tfsec
  script:
    - tfsec . --format junit > tfsec-report.xml

```

---

## 🔄 Complete Security Pipeline Example (Ví dụ Pipeline bảo mật hoàn chỉnh)

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security
  - build
  - deploy

include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml

# Custom security jobs
gitleaks:
  stage: security
  image: zricethezav/gitleaks
  script:
    - gitleaks detect --source . --verbose

trivy:
  stage: security
  image: aquasec/trivy
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  needs:
    - build

checkov:
  stage: security
  image: bridgecrew/checkov
  script:
    - checkov -d terraform/ --output cli
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

```

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

## 📖 Resources (Tài liệu tham khảo)

- [GitLab Security Scanning](https://docs.gitlab.com/ee/user/application_security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Checkov Documentation](https://www.checkov.io/)

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [Track 3 Capstone](../../Track3_Cloud_Network_Design/3.7_Capstone_Project/) | **4.1 Security Pipeline** | [4.2 Infra Security](../4.2_Infra_Security/) |

---

**Secure your pipeline! 🔐**

*Bảo mật pipeline của bạn!*

</div>
