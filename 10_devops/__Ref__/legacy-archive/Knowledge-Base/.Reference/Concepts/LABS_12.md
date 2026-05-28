# Module 13: Security Labs

---

## 🔧 Lab 1: Scan for Secrets

```bash
# Install trufflehog
pip install trufflehog

# Scan repo
trufflehog git file://./

# Or use git-secrets
git secrets --install
git secrets --scan
```

---

## 🔧 Lab 2: Container Security

```bash
# Scan Docker image
docker scan myapp:latest

# Or use Trivy
trivy image myapp:latest
```

---

## 🔧 Lab 3: Dependency Audit

```bash
# Python
pip install pip-audit
pip-audit

# Node.js
npm audit
npm audit fix

# Go
go list -m all | nancy sleuth
```

---

## 🔧 Lab 4: HTTPS với Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
```

---

## 📋 Tổng kết

| Lab | Skill |
|-----|-------|
| 1 | Secret scanning |
| 2 | Container security |
| 3 | Dependency audit |
| 4 | HTTPS setup |

👉 **[SCENARIOS.md](SCENARIOS.md)**
