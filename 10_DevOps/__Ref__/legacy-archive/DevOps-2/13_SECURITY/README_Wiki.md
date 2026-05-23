# Module 13: Security (DevSecOps)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **DevSecOps** | - | Security tích hợp vào DevOps từ đầu |
| **Shift Left** | - | Kiểm tra security sớm trong quy trình |
| **SAST** | - | Static Application Security Testing - Phân tích code tĩnh |
| **DAST** | - | Dynamic Application Security Testing - Test ứng dụng đang chạy |
| **Secrets Management** | - | Quản lý mật khẩu, API keys an toàn |
| **Vault** | - | HashiCorp Vault - Tool quản lý secrets |
| **CVE** | - | Common Vulnerabilities and Exposures - Lỗ hổng đã biết |
| **Vulnerability Scan** | - | Quét lỗ hổng trong code và dependencies |
| **RBAC** | - | Role-Based Access Control - Phân quyền theo vai trò |
| **Least Privilege** | - | Chỉ cấp quyền tối thiểu cần thiết |
| **Zero Trust** | - | Không tin tưởng, luôn xác minh |
| **Encryption** | - | Mã hóa dữ liệu |

---

## 📖 DevSecOps là gì? (Định nghĩa từ gốc)

### Trước hết: Security trong Development là gì?

**Security = Bảo vệ hệ thống khỏi bị truy cập/sử dụng trái phép**

Trong phần mềm, security bao gồm:

- **Authentication:** Ai đang access? (login)
- **Authorization:** Họ được phép làm gì? (permissions)
- **Data Protection:** Data có bị lộ không? (encryption)
- **Vulnerabilities:** Code có lỗ hổng không? (bugs có thể exploit)

### Cách làm truyền thống (Security as Afterthought)

```
Workflow cũ:
Dev viết code → Test → Build → Deploy → SECURITY REVIEW → Fix → Deploy lại

Vấn đề:
1. Phát hiện bug security SAU KHI code production
2. Fix tốn thời gian (phải qua lại nhiều team)
3. "Security team blocks everything" → Conflict giữa Dev và Security
4. Deadline pressure → "Ship first, fix later" → BUG LÊN PRODUCTION
```

### DevSecOps giải quyết

> **DevSecOps = Tích hợp Security vào mọi bước của DevOps pipeline**

Thay vì security review ở cuối, security **built-in từ đầu**:

```
DevSecOps workflow:
Code → SECURITY SCAN → Build → SECURITY TEST → Deploy

Mỗi bước đều có security check tự động:
- Commit secrets? → Block
- Vulnerable dependencies? → Alert
- SQL injection in code? → Fail build
```

**So sánh:**

| Traditional Security | DevSecOps |
|---------------------|-----------|
| Security team riêng, cuối process | Security integrated vào Dev team |
| Manual review | Automated scans |
| Phát hiện bug sau weeks | Phát hiện bug trong minutes |
| "Security blocks release" | "Security enables safe release" |
| Reactive (fix after breach) | Proactive (prevent breach) |

### Tại sao DevSecOps quan trọng với DevOps?

**Vì DevOps làm mọi thứ NHANH hơn:**

- Deploy 10x/ngày thay vì 1x/tháng
- → Bug có thể lên production 10x nhanh hơn
- → **Security cũng phải nhanh như DevOps**

**Không có DevSecOps:**

- DevOps deploy nhanh → Security review không kịp → Skip security → Breach

**Có DevSecOps:**

- Mỗi deploy đều đã qua automated security checks → Fast AND Secure

---

## 🎬 Câu chuyện thực tế

Bạn deploy xong, mọi thứ hoạt động... Sáng hôm sau:

> "Anh ơi, database bị hack, data user bị leak!"

Điều tra phát hiện: Developer commit database password vào Git 6 tháng trước. Hacker tìm thấy password trong Git history.

**Với DevSecOps:** Git pre-commit hook scan secrets → Block ngay khi commit → Password không bao giờ lên Git.

---

## 📖 DevSecOps Principles

**DevSecOps = Security + DevOps.** Thay vì để security review ở cuối (khi đã quá muộn để fix), ta tích hợp security từ đầu.

### Shift Left Security

**"Shift Left"** nghĩa là đưa security về phía bên trái của pipeline (sớm hơn trong quy trình).

```
Traditional (security ở cuối - quá muộn):
Code → Build → Test → ──────────────────→ Security Review → Deploy
                                               ↑
                                          (Phát hiện lỗi khi đã deploy!)

DevSecOps (security từ đầu - catch sớm):
Code → Security Scan → Build → Test (with security) → Deploy
           ↑
    (Phát hiện ngay khi code!)
```

**Lợi ích của Shift Left:**

| Metric | Traditional | DevSecOps |
|--------|-------------|-----------|
| Thời gian fix bug | Ngày/tuần | Phút/giờ |
| Chi phí fix | Cao (đã deploy) | Thấp (dev stage) |
| Ảnh hưởng user | Có | Không |

---

## 🔐 Security Practices

### 1. Secrets Management

**Vấn đề:** Hardcode passwords trong code = thảm họa bảo mật. Ai có access repo = có password.

**❌ Tuyệt đối KHÔNG làm:**

```python
# KHÔNG BAO GIỜ hardcode credentials - LỖI BẢO MẬT NGHIÊM TRỌNG
DATABASE_URL = "postgres://user:password123@db.example.com/app"
```

**✅ NÊN làm:**

```python
# Lấy từ environment variable - an toàn hơn
import os
DATABASE_URL = os.environ['DATABASE_URL']
```

**Các tools quản lý secrets:**

| Tool | Use case | Provider |
|------|----------|----------|
| **HashiCorp Vault** | Enterprise, multi-cloud | Self-hosted / HCP |
| **AWS Secrets Manager** | AWS workloads | AWS |
| **GitHub Secrets** | GitHub Actions | GitHub |
| **Azure Key Vault** | Azure workloads | Azure |

> 💡 **Best practice:** Rotate secrets định kỳ (30-90 ngày). Vault và cloud services hỗ trợ auto-rotation.

### 2. Container Security

**Ba nguyên tắc chính khi build container:**

```dockerfile
# 1. Dùng version cụ thể - KHÔNG dùng :latest
FROM node:18.17.0-alpine
# :latest có thể thay đổi, gây inconsistent và có thể có vulnerabilities

# 2. Chạy với non-root user
RUN adduser -D appuser
USER appuser
# Nếu container bị hack, attacker chỉ có quyền hạn chế

# 3. Scan images trước khi push
# docker scan myimage
# Hoặc: trivy image myimage
```

**Giải thích từng phần:**

| Practice | Lý do |
|----------|-------|
| `node:18.17.0-alpine` | Alpine = lightweight, ít attack surface. Version cố định = reproducible |
| `USER appuser` | Root trong container có thể escape ra host. Luôn chạy non-root |
| `docker scan` | Phát hiện CVEs trong base image và dependencies |

### 3. Dependency Scanning

**Vấn đề:** Thư viện bạn dùng có thể chứa vulnerabilities. Ví dụ: Log4j (2021) ảnh hưởng hàng triệu apps.

```bash
# Python - Kiểm tra security issues trong pip packages
pip-audit

# Node.js - Built-in npm security scanner
npm audit
npm audit fix  # Auto-fix nếu có patch

# Snyk - Multi-language, tích hợp CI/CD
snyk test
snyk monitor  # Continuous monitoring
```

> 💡 **Tip:** Chạy dependency scan trong CI pipeline. Fail build nếu có HIGH/CRITICAL vulnerabilities.

### 4. SAST (Static Analysis)

**SAST = Static Application Security Testing.** Phân tích source code để tìm security issues mà không cần chạy app.

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run SAST with CodeQL
        uses: github/codeql-action/analyze@v2
        # CodeQL tìm SQL injection, XSS, và nhiều patterns khác
```

**SAST phát hiện được:**

| Issue | Ví dụ |
|-------|-------|
| **SQL Injection** | `"SELECT * FROM users WHERE id = " + user_input` |
| **XSS** | `document.innerHTML = user_input` |
| **Hardcoded secrets** | `password = "admin123"` |
| **Path traversal** | `open("/data/" + user_input)` |

---

## 📋 Security Checklist

- [ ] No secrets in code
- [ ] Minimal container permissions
- [ ] Regular dependency updates
- [ ] Input validation
- [ ] HTTPS everywhere
- [ ] Least privilege access
- [ ] Audit logging

---

## 📝 Tổng kết

✅ Shift Left Security  
✅ Secrets management  
✅ Container security  
✅ Dependency scanning  

👉 **[LABS.md](LABS.md)** | **[SCENARIOS.md](SCENARIOS.md)**
