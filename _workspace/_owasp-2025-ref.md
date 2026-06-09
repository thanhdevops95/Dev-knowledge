# OWASP Top 10:2025 — Reference (final release, 8th installment)

Nguồn: https://owasp.org/Top10/2025/

## Thứ tự chính thức 2025
1. **A01:2025 — Broken Access Control** (SSRF gộp vào đây)
2. **A02:2025 — Security Misconfiguration**
3. **A03:2025 — Software Supply Chain Failures** (MỚI — mở rộng từ "Vulnerable and Outdated Components" 2021)
4. **A04:2025 — Cryptographic Failures**
5. **A05:2025 — Injection**
6. **A06:2025 — Insecure Design**
7. **A07:2025 — Authentication Failures**
8. **A08:2025 — Software or Data Integrity Failures**
9. **A09:2025 — Security Logging & Alerting Failures**
10. **A10:2025 — Mishandling of Exceptional Conditions** (MỚI — xử lý lỗi/điều kiện ngoại lệ sai cách)

## Mapping 2021 → 2025
| 2021 | 2025 |
|---|---|
| A01 Broken Access Control | A01 (+ SSRF gộp vào) |
| A02 Cryptographic Failures | A04 |
| A03 Injection | A05 |
| A04 Insecure Design | A06 |
| A05 Security Misconfiguration | A02 |
| A06 Vulnerable & Outdated Components | A03 (mở rộng → Software Supply Chain Failures) |
| A07 Identification & Authentication Failures | A07 Authentication Failures |
| A08 Software & Data Integrity Failures | A08 |
| A09 Security Logging & Monitoring Failures | A09 (đổi "Monitoring"→"Alerting") |
| A10 SSRF | gộp vào A01 |
| (mới) | A10 Mishandling of Exceptional Conditions |
