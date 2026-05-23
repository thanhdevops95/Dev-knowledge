# 🔬 Labs: Security in Pipeline

---

## 🔬 Lab 1: Secret Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

```bash
# Run locally
gitleaks detect --source . --verbose

# Pre-commit hook
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

---

## 🔬 Lab 2: SAST - SonarQube

```yaml
# Docker Compose setup
version: '3.8'
services:
  sonarqube:
    image: sonarqube:community
    ports:
      - "9000:9000"
    volumes:
      - sonar-data:/opt/sonarqube/data
volumes:
  sonar-data:
```

```bash
# Scan project
sonar-scanner \
  -Dsonar.projectKey=myapp \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=admin \
  -Dsonar.password=admin
```

---

## 🔬 Lab 3: Dependency Scanning

```yaml
# GitHub Actions
- name: Snyk Scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high

# npm audit
- name: npm audit
  run: |
    npm audit --audit-level=high
    npm audit fix --force
```

```bash
# OWASP Dependency Check
dependency-check --project myapp --scan ./ --format HTML
```

---

## 🔬 Lab 4: Container Scanning

```yaml
# Trivy in CI
- name: Trivy vulnerability scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:${{ github.sha }}'
    format: 'table'
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
```

```bash
# Local scan
trivy image myapp:latest
trivy image --severity CRITICAL,HIGH myapp:latest

# Scan filesystem
trivy fs .

# Docker Scout
docker scout cves myapp:latest
```

---

## 🔬 Lab 5: Policy as Code (OPA)

```rego
# policy.rego
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Deployment"
    not input.request.object.spec.template.spec.securityContext.runAsNonRoot
    msg := "Deployments must run as non-root"
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged
    msg := sprintf("Container %v cannot be privileged", [container.name])
}
```

```bash
# Test policy
opa eval -i input.json -d policy.rego "data.kubernetes.admission.deny"

# Conftest for Dockerfile
conftest test Dockerfile
```

---

## ✅ Checklist

- [ ] Lab 1: Secret Scanning
- [ ] Lab 2: SAST
- [ ] Lab 3: Dependency Scanning
- [ ] Lab 4: Container Scanning
- [ ] Lab 5: Policy as Code

---

**[← Back to README](./README.md)**
