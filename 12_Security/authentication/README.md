# 🔐 Authentication

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)

> 🎯 *Authentication deep cluster — extension của OWASP A07. 5 bài cover foundation → password/MFA → OAuth/OIDC → JWT/Session → Federation/SSO. Sau cluster: design + implement production-ready auth từ MVP đến enterprise.*

---

## 🚀 Quick start

- [00_what-is-authentication](lessons/01_basic/00_what-is-authentication.md)
- [01_password-and-mfa](lessons/01_basic/01_password-and-mfa.md)
- [02_oauth-and-oidc](lessons/01_basic/02_oauth-and-oidc.md)
- [03_jwt-and-sessions-deep](lessons/01_basic/03_jwt-and-sessions-deep.md)
- [04_federation-sso-and-idp](lessons/01_basic/04_federation-sso-and-idp.md)

---

## 📖 Lessons — Basic cluster (5 bài)

| # | Bài | Trọng tâm | Thời lượng |
|---|---|---|---|
| 00 | [Auth foundation](lessons/01_basic/00_what-is-authentication.md) | AuthN vs AuthZ + 3 factors + session vs token + lifecycle + threat model | ~18p |
| 01 | [Password + MFA deep](lessons/01_basic/01_password-and-mfa.md) | Argon2id + breach check + TOTP + WebAuthn/Passkey + backup codes | ~22p |
| 02 | [OAuth 2.1 + OIDC](lessons/01_basic/02_oauth-and-oidc.md) | 5 flows + PKCE + ID token + Google/Apple + account linking | ~22p |
| 03 | [JWT + Sessions deep](lessons/01_basic/03_jwt-and-sessions-deep.md) | JWT/JWS/JWE + signing algorithms + refresh rotation + revocation | ~22p |
| 04 | [Federation + SSO + IdP](lessons/01_basic/04_federation-sso-and-idp.md) | SAML + Keycloak + SCIM + JIT + break-glass + 500-employee architecture | ~22p |

→ **Tổng ~106 phút đọc + 15-20h hands-on**.

---

## 🔗 Liên kết

- ↑ [12_Security README](../README.md)
- 🛡️ [owasp-top-10](../owasp-top-10/) — overview level
- 🌐 [HTTPS/TLS](../../05_Networking/http-https/lessons/01_basic/04_https-tls.md)
- 🐍 [FastAPI auth](../../07_Web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)

### Tài nguyên ngoài 2026
- 📖 [OAuth 2.1 draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1)
- 📖 [OIDC Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- 📖 [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- 📖 [Keycloak docs](https://www.keycloak.org/docs/latest/)
- 📖 [Passkeys Developer](https://developers.google.com/identity/passkeys)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. Deep dive OWASP A07 với 4 chuyên đề (Password/MFA, OAuth/OIDC, JWT/Session, Federation/SSO).
- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
