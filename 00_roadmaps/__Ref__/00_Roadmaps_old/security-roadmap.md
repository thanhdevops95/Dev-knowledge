# 🔐 Lộ trình Security Engineer

> `[BEGINNER → ADVANCED]` — Xem trước [Tổng quan Lộ trình](./00-overview.md)

---

## Tại sao Security?

Mỗi năm, các vụ data breach gây thiệt hại hàng tỷ đô. Security Engineer giống như "hệ miễn dịch" của hệ thống — bạn không chỉ xây tường lửa, mà phải **nghĩ như kẻ tấn công** để phòng thủ trước. Từ startup đến enterprise, mọi công ty đều cần security.

An ninh mạng không chỉ là "hack". Nó bao gồm thiết kế hệ thống an toàn, mã hóa dữ liệu, kiểm soát truy cập, tuân thủ pháp lý, và xây dựng văn hóa bảo mật trong tổ chức. Đây là lĩnh vực thiếu nhân lực nghiêm trọng trên toàn cầu.

---

## Sơ đồ lộ trình

```
Networking Basics
    │
    ▼
Web Security (OWASP Top 10)
    │
    ├──► Authentication (JWT, OAuth, SAML)
    │
    ├──► Cryptography (Hashing, Encryption, TLS)
    │
    ├──► Authorization (RBAC, ABAC, Policies)
    │
    ▼
Penetration Testing
    │
    ▼
DevSecOps (SAST/DAST, Supply Chain)
    │
    ▼
Compliance (GDPR, SOC2, PCI-DSS)
```

---

## Giai đoạn 1 — Networking cơ bản

- [ ] TCP/IP, DNS, HTTP/HTTPS → [../04-Networking/](../04-Networking/)
- [ ] Firewalls, Proxies, VPN
- [ ] Wireshark — phân tích network traffic
- [ ] Linux command line & permissions

---

## Giai đoạn 2 — Web Security

- [ ] OWASP Top 10 → [../12-Security/01-web-security-fundamentals.md](../12-Security/01-web-security-fundamentals.md)
- [ ] XSS (Cross-Site Scripting)
- [ ] SQL Injection
- [ ] CSRF, SSRF, Broken Access Control
- [ ] Security Headers (CSP, HSTS, X-Frame-Options)

---

## Giai đoạn 3 — Authentication

- [ ] Authentication fundamentals → [../12-Security/02-authentication-fundamentals.md](../12-Security/02-authentication-fundamentals.md)
- [ ] Password hashing (bcrypt, Argon2)
- [ ] JWT, Session-based auth
- [ ] OAuth 2.0, OpenID Connect, SAML
- [ ] Multi-Factor Authentication (MFA)

---

## Giai đoạn 4 — Cryptography

- [ ] Symmetric vs Asymmetric encryption → [../12-Security/encryption/](../12-Security/encryption/)
- [ ] TLS/SSL handshake
- [ ] Digital Signatures, Certificates (PKI)
- [ ] Hashing algorithms (SHA-256, bcrypt)

---

## Giai đoạn 5 — Authorization

- [ ] RBAC, ABAC, ReBAC → [../12-Security/authorization/](../12-Security/authorization/)
- [ ] OAuth scopes & permissions
- [ ] Policy engines (OPA, Casbin)
- [ ] Principle of Least Privilege

---

## Giai đoạn 6 — Penetration Testing

- [ ] Pentest basics → [../12-Security/pentest/01-pentest-basics.md](../12-Security/pentest/01-pentest-basics.md)
- [ ] Reconnaissance, Scanning, Exploitation
- [ ] Burp Suite, OWASP ZAP
- [ ] Kali Linux toolchain
- [ ] Bug Bounty methodology

---

## Giai đoạn 7 — DevSecOps

- [ ] SAST (Static Analysis) → [../12-Security/devsecops/](../12-Security/devsecops/)
- [ ] DAST (Dynamic Analysis)
- [ ] Dependency scanning (Snyk, Dependabot)
- [ ] Container security (Trivy, Docker Scout)
- [ ] Supply chain security (SBOM, Sigstore)

---

## Giai đoạn 8 — Compliance & Governance

- [ ] GDPR, CCPA — Data privacy → [../12-Security/compliance/](../12-Security/compliance/)
- [ ] SOC 2 Type II
- [ ] PCI-DSS (payment security)
- [ ] Security incident response plan

---

## 📦 Project thực hành

| Giai đoạn | Project |
|---|---|
| Sau Web Security | Tìm và fix OWASP Top 10 trên DVWA / Juice Shop |
| Sau Auth | Xây hệ thống auth hoàn chỉnh (JWT + OAuth + MFA) |
| Sau Pentest | Hoàn thành 10+ challenges trên HackTheBox / TryHackMe |
| Sau DevSecOps | CI pipeline với SAST + dependency scan + container scan |
| Nâng cao | Security audit report cho 1 ứng dụng thực tế |

---

## 📚 Tài nguyên

- [OWASP](https://owasp.org/) — Tài nguyên bảo mật web #1 thế giới
- [HackTheBox](https://www.hackthebox.com/) — Lab thực hành pentest
- [TryHackMe](https://tryhackme.com/) — Học security qua hands-on rooms
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) — Học web security miễn phí
- [CyberDefenders](https://cyberdefenders.org/) — Blue team challenges
