# 🛡️ OWASP Top 10

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)

> 🎯 *OWASP Top 10 (2021 release) — 10 vulnerability phổ biến nhất web/app. Foundation cho mọi dev backend/full-stack/devops. 5 bài cover full A01-A10 + threat modeling + secure design + supply chain.*

---

## 🚀 Quick start

- [00_what-is-owasp-and-application-security](lessons/01_basic/00_what-is-owasp-and-application-security.md) — OWASP intro + STRIDE/DREAD + defense-in-depth
- [01_injection-and-access-control](lessons/01_basic/01_injection-and-access-control.md) — A01 + A03 (IDOR, SQLi, XSS, CSRF)
- [02_crypto-failures-and-secure-design](lessons/01_basic/02_crypto-failures-and-secure-design.md) — A02 + A04 (Argon2id, TLS, JWT, abuse case)
- [03_misconfig-vulnerable-components-supply-chain](lessons/01_basic/03_misconfig-vulnerable-components-supply-chain.md) — A05 + A06 + A08 (headers, deps, cosign, SLSA)
- [04_auth-failures-logging-and-ssrf](lessons/01_basic/04_auth-failures-logging-and-ssrf.md) — A07 + A09 + A10 (MFA, SIEM, SSRF)

---

## 📖 Lessons — Basic cluster (5 bài)

| # | Bài | OWASP coverage | Thời lượng |
|---|---|---|---|
| 00 | [OWASP + AppSec](lessons/01_basic/00_what-is-owasp-and-application-security.md) | Foundation + STRIDE/DREAD + defense-in-depth | ~18p |
| 01 | [Injection + Access Control](lessons/01_basic/01_injection-and-access-control.md) | A01 + A03 | ~22p |
| 02 | [Crypto + Secure Design](lessons/01_basic/02_crypto-failures-and-secure-design.md) | A02 + A04 | ~22p |
| 03 | [Misconfig + Components + Supply chain](lessons/01_basic/03_misconfig-vulnerable-components-supply-chain.md) | A05 + A06 + A08 | ~22p |
| 04 | [Auth + Logging + SSRF](lessons/01_basic/04_auth-failures-logging-and-ssrf.md) | A07 + A09 + A10 | ~22p |

→ **Tổng ~106 phút đọc + 10-15h hands-on**.

---

## 🔗 Liên kết

- ↑ [12_security README](../README.md)
- 🔐 [authentication](../authentication/) — deep A07
- 🐳 [Docker security](../../10_devops/docker/lessons/02_intermediate/02_image-security-supply-chain.md)
- 🔁 [CI/CD supply chain](../../10_devops/ci-cd/lessons/02_intermediate/02_supply-chain-security.md)
- 🌐 [HTTPS/TLS](../../05_networking/http-https/lessons/01_basic/04_https-tls.md)
- 🐍 [FastAPI auth](../../07_web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)

### Tài nguyên ngoài 2026
- 📖 [OWASP Top 10 2021](https://owasp.org/Top10/)
- 📖 [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- 📖 [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- 📖 [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. OWASP Top 10 (2021 release) full coverage A01-A10.
- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
