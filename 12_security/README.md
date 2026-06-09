# 🔒 12_security

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** 🟢 Active — 2/10 cluster có basic content (owasp-top-10 + authentication)

> 🎯 *Security knowledge: OWASP Top 10, Authentication (OAuth/JWT/MFA), Authorization (RBAC/ABAC), Cryptography, TLS/SSL, Pentesting, Cloud/Container security, Secrets management, Compliance (SOC2/PCI/HIPAA/GDPR). Cross-cuts mọi stack.*

---

## 🎯 Chủ đề này có gì

Application Security, Auth (OAuth/OIDC/JWT/MFA), Crypto (hash/encrypt), TLS, Pentesting, Cloud/Container security, Secrets mgmt, Compliance.

---

## 📂 Sub-clusters

| Cluster | Status | Basic | Intermediate |
|---|---|---|---|
| [owasp-top-10](owasp-top-10/) | ✅ Active | 5/5 ✅ | ⏳ |
| [authentication](authentication/) | ✅ Active | 5/5 ✅ | ⏳ |
| [authorization](authorization/) | 🟡 Skeleton | ⏳ | ⏳ |
| [cryptography](cryptography/) | 🟡 Skeleton | ⏳ | ⏳ |
| [tls-ssl](tls-ssl/) | 🟡 Skeleton | ⏳ | ⏳ |
| [pentesting-fundamentals](pentesting-fundamentals/) | 🟡 Skeleton | ⏳ | ⏳ |
| [cloud-security](cloud-security/) | 🟡 Skeleton | ⏳ | ⏳ |
| [container-security](container-security/) | 🟡 Skeleton | ⏳ | ⏳ |
| [secrets-management](secrets-management/) | 🟡 Skeleton | ⏳ | ⏳ |
| [compliance](compliance/) | 🟡 Skeleton | ⏳ | ⏳ |


---

## 🚀 Lộ trình đề xuất

| Bạn là... | Đi theo |
|---|---|
| 🟢 **Beginner dev** | [owasp-top-10/01_basic/](owasp-top-10/lessons/01_basic/) — foundation cross-stack |
| 🟡 **Backend dev đã làm app** | OWASP → authentication → authorization → cryptography |
| 🟠 **DevOps/Platform** | OWASP → secrets-management → container-security → cloud-security |
| 🔵 **Compliance/audit** | OWASP → compliance → pentesting fundamentals |
| 🧭 **Security Engineer career** | Tất cả 10 cluster (basic → intermediate) |

---

## 📖 Active cluster — owasp-top-10 basic (5 bài)

| # | Bài | OWASP coverage | Tag |
| --- | --- | --- | --- |
| 00 | [What is OWASP + AppSec](owasp-top-10/lessons/01_basic/00_what-is-owasp-and-application-security.md) | Foundation: STRIDE + DREAD + defense-in-depth | MUST-KNOW |
| 01 | [Injection + Access Control](owasp-top-10/lessons/01_basic/01_injection-and-access-control.md) | A01 + A03 | MUST-KNOW |
| 02 | [Crypto + Secure Design](owasp-top-10/lessons/01_basic/02_crypto-failures-and-secure-design.md) | A02 + A04 | MUST-KNOW |
| 03 | [Misconfig + Components + Supply chain](owasp-top-10/lessons/01_basic/03_misconfig-vulnerable-components-supply-chain.md) | A05 + A06 + A08 | MUST-KNOW |
| 04 | [Auth + Logging + SSRF](owasp-top-10/lessons/01_basic/04_auth-failures-logging-and-ssrf.md) | A07 + A09 + A10 | MUST-KNOW |

---

## 📖 Active cluster — authentication basic (5 bài)

| # | Bài | Tag |
| --- | --- | --- |
| 00 | [Authentication foundation](authentication/lessons/01_basic/00_what-is-authentication.md) | MUST-KNOW |
| 01 | [Password + MFA deep](authentication/lessons/01_basic/01_password-and-mfa.md) | MUST-KNOW |
| 02 | [OAuth 2.1 + OIDC](authentication/lessons/01_basic/02_oauth-and-oidc.md) | MUST-KNOW |
| 03 | [JWT + Sessions deep](authentication/lessons/01_basic/03_jwt-and-sessions-deep.md) | MUST-KNOW |
| 04 | [Federation + SSO + IdP](authentication/lessons/01_basic/04_federation-sso-and-idp.md) | MUST-KNOW |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- 🐳 [Docker security](../10_devops/docker/lessons/02_intermediate/02_image-security-supply-chain.md)
- 🔁 [CI/CD supply chain](../10_devops/ci-cd/lessons/02_intermediate/02_supply-chain-security.md)
- 🌐 [HTTPS/TLS](../05_networking/http-https/lessons/01_basic/04_https-tls.md)
- 🐍 [FastAPI auth](../07_web/backend/python-fastapi/)
- ☁️ [11_cloud](../11_cloud/)

### Tài nguyên ngoài 2026
- 📖 [OWASP Foundation](https://owasp.org/)
- 📖 [OWASP Top 10](https://owasp.org/Top10/)
- 📖 [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- 📖 [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Cluster **owasp-top-10 basic 5/5 hoàn chỉnh**. Cluster đầu tiên của 12_security branch. Foundation cross-stack security.
- **v1.1.0 (24/05/2026)** — Cluster **authentication basic 5/5 hoàn chỉnh**. 2/10 sub-clusters active.
