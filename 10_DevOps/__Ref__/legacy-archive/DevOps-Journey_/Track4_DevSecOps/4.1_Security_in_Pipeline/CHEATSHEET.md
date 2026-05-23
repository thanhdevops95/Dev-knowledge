# 📋 Security in Pipeline - Cheatsheet

> **Quick Reference for DevSecOps Tools**
>
> *Tra cứu nhanh công cụ DevSecOps*

---

## 🔍 SAST (Static Analysis - Phân tích tĩnh)

### SonarQube

```bash
# Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube

# Scan
sonar-scanner \
  -Dsonar.projectKey=myproject \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000
```

### Semgrep

```bash
# Install (Cài đặt)
pip install semgrep

# Scan
semgrep --config auto .
semgrep --config p/security-audit .
```

---

## 🐳 Container Scanning (Quét container)

### Trivy

```bash
# Image scan (Quét image)
trivy image nginx:latest
trivy image --severity HIGH,CRITICAL myapp:latest

# Filesystem scan (Quét filesystem)
trivy fs .

# IaC scan (Quét IaC)
trivy config .
```

### Docker Scout

```bash
docker scout cves nginx:latest
docker scout quickview nginx:latest
```

---

## 🔑 Secret Scanning (Quét secrets)

### Gitleaks

```bash
# Install
brew install gitleaks

# Scan repo (Quét repo)
gitleaks detect --source .
gitleaks detect --source . --report-format json --report-path report.json
```

---

## 🦊 GitLab CI Security Templates

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
```

---

## 📝 IaC Scanning (Quét IaC)

### Checkov

```bash
# Install
pip install checkov

# Scan Terraform
checkov -d terraform/
checkov -f main.tf
```

### tfsec

```bash
# Install
brew install tfsec

# Scan
tfsec .
tfsec . --format json
```

---

## 🔐 Dependency Scanning (Quét dependencies)

```bash
# npm
npm audit
npm audit fix

# pip
pip-audit
safety check

# Go
go list -json -m all | nancy sleuth
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
