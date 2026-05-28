# ⚙️📦 A05 Misconfig + A06 Vulnerable Components + A08 Supply Chain Integrity

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 03/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** Bài [02_crypto-failures-and-secure-design](02_crypto-failures-and-secure-design.md) ✅

> 🎯 *Bài 03. 3 vuln liên quan: **A05 Misconfig** (server config sai, headers thiếu, debug bật trong prod), **A06 Vulnerable Components** (dep CVE chưa patch), **A08 Software/Data Integrity** (supply chain attack, unsigned package). Bài này dạy: security headers đầy đủ, CORS đúng, dependency scanning (Snyk/Dependabot/Trivy), SBOM, cosign + SLSA. Hands-on harden Acme Shop từ A → A+ trên Mozilla Observatory.*

## 🎯 Sau bài này bạn sẽ

- [ ] Setup **security headers** đầy đủ: CSP, HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy
- [ ] Configure **CORS** đúng (allowlist origin, không `*`)
- [ ] Disable **debug mode, default credentials, verbose errors** trong production
- [ ] Setup **dependency scanning**: Dependabot (GitHub) / Snyk / Trivy / OSV-Scanner
- [ ] Sinh + lưu trữ **SBOM** (Syft/CycloneDX/SPDX)
- [ ] Sign + verify image/artifact với **cosign** (Sigstore)
- [ ] Hiểu **SLSA framework** L1-L4 + áp dụng L2/L3
- [ ] Audit Acme Shop config + đẩy score Mozilla Observatory lên A+

---

## Tình huống — 3 vụ thật tuần qua

Pen-test report tiếp tục:

**A05 Misconfig**:
- `/api/docs` Swagger UI public — leak full API + admin endpoints.
- Django `DEBUG=True` trong prod — stack trace lộ DB password.
- S3 bucket public read — backup `users.csv` ai cũng download.

**A06 Components**:
- `lodash@4.17.4` (2017) — CVE prototype pollution.
- `log4j@2.14` — log4shell (chỉ Java component cũ).
- Docker image base `python:3.8` 2 năm chưa update.

**A08 Supply chain**:
- Image build push không sign → ai có thể push image giả vào registry.
- `package-lock.json` không pin → mỗi build dep version khác.

3 nhóm vấn đề khác nhau, cùng cluster. Bài này map fix.

---

## 1️⃣ A05 — Security Misconfiguration

🪞 **Ẩn dụ**: *Misconfig như **chìa khóa nhà cắm trong ổ ngoài cửa** — không phải khóa hỏng (broken design), mà do quên rút (config sai). Mọi default insecure, mỗi service mới mỗi quên check là 1 lỗ hổng.*

### Security headers thiết yếu

| Header | Mục đích | Giá trị recommend 2026 |
|---|---|---|
| **Strict-Transport-Security** | Force HTTPS | `max-age=31536000; includeSubDomains; preload` |
| **Content-Security-Policy** | Anti-XSS, anti-clickjacking | `default-src 'self'; script-src 'self' 'nonce-{n}'; frame-ancestors 'none'` |
| **X-Frame-Options** | Anti-clickjacking (legacy) | `DENY` |
| **X-Content-Type-Options** | Anti MIME-sniffing | `nosniff` |
| **Referrer-Policy** | Control Referer header | `strict-origin-when-cross-origin` |
| **Permissions-Policy** | Disable browser feature | `geolocation=(), camera=(), microphone=()` |
| **Cross-Origin-Opener-Policy** | Isolate window | `same-origin` |
| **Cross-Origin-Embedder-Policy** | Require CORP | `require-corp` |
| **Cross-Origin-Resource-Policy** | Cross-origin protection | `same-origin` |
| ~~X-XSS-Protection~~ | Legacy, deprecated 2024 | Omit (browser ignore) |

### FastAPI middleware

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    return response
```

### Nginx reverse proxy

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; frame-ancestors 'none'" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), camera=(), microphone=()" always;
```

→ Test: [securityheaders.com](https://securityheaders.com) → A+ target.

### CORS — Cross-Origin Resource Sharing

**Anti-pattern**: Allow `*`
```python
# ❌
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)
```

`allow_credentials=True` + `allow_origins=*` → browser block.

**Pattern**: Allowlist
```python
# ✅
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://acmeshop.vn", "https://admin.acmeshop.vn"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=600,
)
```

**Dynamic** (nhiều subdomain):
```python
ALLOWED_PATTERN = re.compile(r"^https://(\w+\.)?acmeshop\.vn$")

def origin_allowed(origin: str) -> bool:
    return bool(ALLOWED_PATTERN.match(origin))
```

### Debug mode + verbose errors

| Framework | Anti-pattern | Pattern |
|---|---|---|
| Django | `DEBUG = True` in prod | `DEBUG = False` + `ALLOWED_HOSTS` set |
| Flask | `app.run(debug=True)` | Production WSGI (gunicorn/uvicorn) |
| FastAPI | Default 422 verbose | Custom exception handler hide details |
| Rails | `config.consider_all_requests_local = true` | `false` in `production.rb` |
| Spring | `server.error.include-stacktrace=always` | `never` |

```python
# FastAPI — hide internal error
@app.exception_handler(Exception)
async def unhandled_exception(request, exc):
    log.exception(exc)  # log full to logger
    return JSONResponse({"error": "Internal server error"}, status_code=500)  # no detail to client
```

### Default credentials

Vendor default creds đã leak hết:
- MongoDB không password (pre-3.6 default).
- Postgres `postgres/postgres`.
- Jenkins `admin/admin`.
- Tomcat manager `tomcat/tomcat`.
- ElasticSearch không auth (pre-7.0).

**Fix**: Change immediately on first boot; automated via Terraform `random_password`.

### S3/GCS bucket misconfig

| Mistake | Fix |
|---|---|
| Public read all bucket | Block Public Access setting (AWS), Public Access Prevention (GCS) |
| `s3:GetObject` action `*` resource | Limit to specific prefix |
| Server access log disabled | Enable + ship to SIEM |
| Versioning + MFA delete off | Enable for critical bucket |
| Cross-region replication public | Verify replication bucket also private |

### Endpoint exposure

| Service | Don't expose | Tool to check |
|---|---|---|
| `/api/docs` (Swagger) | Public in prod | Restrict via IP allowlist or auth |
| `/metrics` (Prometheus) | Public | Auth or internal network only |
| `/health` `/ready` | OK public (no sensitive data) | — |
| `/admin/*` | Public | Network ACL + auth + MFA |
| `/debug/pprof` (Go) | Public | Disable in prod |
| `/.git/`, `/.env`, `/.aws/` | Webroot exposed | Nginx deny |

```nginx
location ~ /\.(git|env|aws|ssh) {
    deny all;
    return 404;
}
```

### Tools scan misconfig

| Tool | Scope |
|---|---|
| **Mozilla Observatory** | Web security headers |
| **securityheaders.com** | Headers grade |
| **SSL Labs** | TLS |
| **CIS Benchmark** | OS + cloud config baseline |
| **AWS Config / GCP Security Command Center / Azure Defender** | Cloud misconfig |
| **kube-bench** | K8s CIS |
| **Trivy config scan** | IaC + container |
| **Checkov, tfsec** | Terraform |

---

## 2️⃣ A06 — Vulnerable and Outdated Components

🪞 **Ẩn dụ**: *Dependencies như **bộ máy lái xe nhập từ nhiều nhà cung cấp** — mỗi nhà có thể recall (CVE). Không biết xe có recall = không biết phanh có hỏng hôm nay không.*

### Vấn đề scale

App modern có **hàng trăm transitive dep**:
- Node.js: 100 direct → 1000+ transitive.
- Python: 30 → 200.
- Go: 20 → 100.

Mỗi dep có thể CVE — tracking thủ công bất khả thi.

### Famous incidents

| CVE | Năm | Impact |
|---|---|---|
| **log4shell** (CVE-2021-44228) | 2021 | Java `log4j` — RCE simple `${jndi:ldap://...}` |
| **Spring4Shell** (CVE-2022-22965) | 2022 | Spring Framework RCE |
| **xz-utils backdoor** (CVE-2024-3094) | 2024 | Maintainer chèn backdoor — SSH exploit |
| **Polyfill.io supply chain** | 2024 | CDN bị mua + inject malicious script |

### Dependency scanning tools

| Tool | Type | Free? | Best for |
|---|---|---|---|
| **Dependabot** | GitHub native | ✅ | GitHub user |
| **Renovate** | Multi-platform | ✅ OSS | Flexible config |
| **Snyk** | Commercial | ✅ free tier | UI + remediation |
| **Trivy** | OSS scanner | ✅ | CI/Docker images |
| **Grype** | OSS (Anchore) | ✅ | Container |
| **OSV-Scanner** | Google OSS | ✅ | Multi-ecosystem |
| **GitHub Advisory Database** | DB | ✅ | Reference |
| **npm audit / pip-audit / cargo audit** | Native | ✅ | Quick local check |

### Dependabot setup

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
    groups:
      patches:
        update-types: ["patch"]
      minor:
        update-types: ["minor"]

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Trivy trong CI

```yaml
# .github/workflows/security.yml
- name: Trivy scan FS + image
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'  # Fail pipeline
    ignore-unfixed: true
```

### Vulnerability triage workflow

```
1. Scan output: 50 CVE → đừng panic
2. Filter HIGH/CRITICAL → 8 cần action
3. Check each:
   - Có patched version? → upgrade
   - Reachable in code path? → exploit feasible
   - Có mitigation khác? (WAF, network ACL)
4. Prioritize:
   - Critical + reachable + patched = fix immediate
   - Critical + not reachable = lower priority
5. Suppress with rationale:
   trivy --ignore-policy = file documented
6. Re-scan periodic
```

### Auto-upgrade strategy

| Strategy | Pros | Cons |
|---|---|---|
| Auto-merge patch (`x.y.Z`) | Velocity | Risk regression rare |
| Auto-merge minor (`x.Y.z`) | Velocity | Higher regression risk |
| Manual major (`X.y.z`) | Safe | Slow |
| **Recommend 2026**: auto patch + minor (with tests) + manual major

```yaml
# Renovate config
{
  "automerge": true,
  "automergeType": "pr",
  "packageRules": [
    {"updateTypes": ["patch", "minor"], "automerge": true},
    {"updateTypes": ["major"], "automerge": false}
  ]
}
```

### Out-of-date check

Beyond CVE:
- Library EOL (end-of-life) → no security patch even if no current CVE.
- Major version 2+ behind → eventual migration cost balloon.
- Maintainer unmaintained > 1 năm → risk.

Tool: **EOL.date**, **endoflife.date** — check support status.

---

## 3️⃣ A08 — Software and Data Integrity Failures

🪞 **Ẩn dụ**: *Supply chain integrity như **chuỗi giao bưu kiện** — kiện đến tay bạn có nguyên seal nhà cung cấp không? Có ai tráo giữa đường không? Cosign + SLSA = **seal vô hình chứng minh nguồn gốc**.*

### Vuln scenarios

| Scenario | Risk |
|---|---|
| Pull `node:latest` from Docker Hub không verify | Image có thể bị tampered tại registry |
| Install dep từ private npm registry | Repo bị xâm nhập → backdoor injected |
| CI pipeline build image, push without sign | Ai có push access → poison image |
| Auto-update từ untrusted source | Attacker takeover update channel |
| Deserialize untrusted data | RCE via pickled object (Python pickle, Java serialization) |

### SLSA framework (Supply-chain Levels for Software Artifacts)

| Level | Description |
|---|---|
| **L0** | No guarantees |
| **L1** | Build process documented + provenance |
| **L2** | Hosted build service (GitHub Actions) + signed provenance |
| **L3** | Hardened build platform + non-falsifiable provenance |
| **L4** | (deprecated 2023, merged with L3) — two-person review + hermetic build |

→ 2026 realistic target: **SLSA L3** for production critical.

### cosign (Sigstore) — Sign + verify image

```bash
# Generate keypair (or use keyless OIDC mode)
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key ghcr.io/acmeshop/api:v1.2.3

# Verify
cosign verify --key cosign.pub ghcr.io/acmeshop/api:v1.2.3
```

### Keyless signing với OIDC

```bash
# Sign sử dụng GitHub Actions OIDC (không cần key file)
cosign sign ghcr.io/acmeshop/api:v1.2.3 \
    --identity-token $(curl -s "${ACTIONS_ID_TOKEN_REQUEST_URL}&audience=sigstore" | jq -r .value)

# Verify with identity
cosign verify ghcr.io/acmeshop/api:v1.2.3 \
    --certificate-identity-regexp "https://github.com/acmeshop/api/.*" \
    --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

### SBOM (Software Bill of Materials)

SBOM = manifest **mọi component** trong artifact.

**Format**:
- **CycloneDX** (OWASP standard)
- **SPDX** (Linux Foundation)
- **SWID** (NIST)

```bash
# Syft generate SBOM
syft ghcr.io/acmeshop/api:v1.2.3 -o cyclonedx-json > sbom.json

# Attach to image với cosign
cosign attest --predicate sbom.json --type cyclonedx ghcr.io/acmeshop/api:v1.2.3

# Verify SBOM
cosign verify-attestation --type cyclonedx ghcr.io/acmeshop/api:v1.2.3
```

### Pin dependencies (reproducibility)

```python
# Python: requirements.txt with hash (pip-tools)
# pip-compile --generate-hashes requirements.in
fastapi==0.110.0 \
    --hash=sha256:abc123...
uvicorn==0.27.0 \
    --hash=sha256:def456...
```

```json
// Node.js: package-lock.json đã có hash sẵn
// Always commit package-lock.json
// Use npm ci (clean install) trong CI, không npm install
```

```yaml
# GitHub Actions: pin SHA, không tag
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

### Deserialize untrusted data

```python
# ❌ Anti-pattern
import pickle
data = pickle.loads(user_input)  # RCE risk

# ✅ Pattern: JSON
import json
data = json.loads(user_input)
```

```java
// ❌ Java native serialization vuln
ObjectInputStream ois = new ObjectInputStream(stream);
Object obj = ois.readObject();

// ✅ JSON, Protobuf, or strict allowlist class
```

### Auto-update channel security

| Pattern | Best practice |
|---|---|
| Application auto-update | Sign update bundle; verify before install |
| Plugin marketplace | Curated, scanned, signed |
| `curl | bash` install | Verify GPG signature first |

---

## 🛠️ Hands-on — Harden Acme Shop A → A+

### Mục tiêu

Mozilla Observatory grade hiện tại: **B-**. Target: **A+**.

### Bước 1 — Audit hiện trạng

```bash
# Test web headers
curl -I https://acmeshop.vn

# Or via online: https://observatory.mozilla.org/analyze/acmeshop.vn
```

Output: thiếu CSP, HSTS không preload, X-Frame-Options absent.

### Bước 2 — Add security headers

```python
# FastAPI middleware (xem section 1)
```

Deploy → re-scan → B+ → A.

### Bước 3 — CSP hardening

```python
import secrets

@app.middleware("http")
async def csp_nonce(request, call_next):
    nonce = secrets.token_urlsafe(16)
    request.state.csp_nonce = nonce
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        f"default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}'; "
        f"style-src 'self' 'unsafe-inline'; "
        f"img-src 'self' data: https://cdn.acmeshop.vn; "
        f"connect-src 'self' https://api.acmeshop.vn; "
        f"frame-ancestors 'none'; "
        f"form-action 'self'; "
        f"base-uri 'self'; "
        f"report-uri /csp-violation"
    )
    return response
```

Template inject nonce:
```html
<script nonce="{{ request.state.csp_nonce }}">
    // inline JS OK
</script>
```

### Bước 4 — HSTS preload

```python
# After verify domain + subdomain all HTTPS for 30+ days
response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
```

Submit https://hstspreload.org/ → 4-12 tuần để propagate vào browser.

### Bước 5 — Dependency scan setup

```yaml
# .github/dependabot.yml (xem section 2)
# .github/workflows/trivy.yml
name: Trivy
on:
  push:
  schedule:
    - cron: "0 6 * * 1"
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          severity: CRITICAL,HIGH
          exit-code: 1
          ignore-unfixed: true
```

### Bước 6 — cosign image sign

```yaml
# .github/workflows/build.yml
- name: Sign image
  env:
    COSIGN_EXPERIMENTAL: 1
  run: |
    cosign sign --yes ghcr.io/acmeshop/api:${{ github.sha }}

- name: Generate SBOM + attest
  run: |
    syft ghcr.io/acmeshop/api:${{ github.sha }} -o cyclonedx-json > sbom.json
    cosign attest --yes --predicate sbom.json --type cyclonedx ghcr.io/acmeshop/api:${{ github.sha }}
```

K8s policy verify (Kyverno):

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signature
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-cosign
      match:
        any:
          - resources:
              kinds: [Pod]
      verifyImages:
        - imageReferences:
            - "ghcr.io/acmeshop/*"
          attestors:
            - entries:
                - keyless:
                    issuer: "https://token.actions.githubusercontent.com"
                    subject: "https://github.com/acmeshop/api/.*"
```

### Bước 7 — Verify

Mozilla Observatory re-scan: **A+ (95/100)**.

securityheaders.com: **A+**.

SSL Labs: **A+**.

---

## ⚠️ Pitfalls

### 1. CSP `'unsafe-inline'` cho convenience

**Bẫy**: Dev thấy CSP block inline → thêm `'unsafe-inline'` → CSP vô nghĩa cho XSS.

**Fix**: Refactor inline → external file hoặc dùng nonce.

### 2. HSTS preload chưa ready

**Bẫy**: Submit preload list nhưng có subdomain còn HTTP → user bị break.

**Fix**: Verify mọi subdomain HTTPS 30+ ngày trước submit.

### 3. CORS `*` cho dev → quên revert

**Bẫy**: Local dev convenience → push prod.

**Fix**: ENV-based config; CI test reject `*` trong prod config.

### 4. Dependabot PR pile up

**Bẫy**: 50 PR pending → ignore → lose tracking.

**Fix**: Auto-merge patch/minor + group; weekly review major.

### 5. Trivy scan ignore unfixed

**Bẫy**: `--ignore-unfixed` → CVE chưa có patch → skip → forget.

**Fix**: Track unfixed CVE separately, có mitigation khác (WAF, isolation).

### 6. cosign sign nhưng không verify ở runtime

**Bẫy**: Sign image rồi để đó, K8s không enforce policy.

**Fix**: Kyverno/Gatekeeper/Sigstore Policy Controller.

### 7. SBOM không sign

**Bẫy**: SBOM ghi đúng nhưng bị tampered → false sense.

**Fix**: `cosign attest` để sign SBOM, verify khi consume.

### 8. `pickle.loads(untrusted)` 

**Bẫy**: Convenience deserialize user input.

**Fix**: JSON only; Pydantic schema validation.

---

## 🎯 Self-check

- [ ] 9 security headers + giá trị recommend 2026?
- [ ] CORS allowlist vs wildcard — code FastAPI?
- [ ] 5 default credentials phải đổi ngay khi setup service?
- [ ] Dependabot config + Trivy CI job?
- [ ] SLSA L1 → L3 — bước cần làm?
- [ ] cosign sign + verify image + SBOM attest?
- [ ] Pin dep với hash — Python + Node?
- [ ] Mozilla Observatory grade A+ cần gì?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Security headers** | HTTP response header tăng security |
| **HSTS** | HTTP Strict Transport Security |
| **CSP** | Content Security Policy |
| **CORS** | Cross-Origin Resource Sharing |
| **CIS Benchmark** | Center for Internet Security configuration baseline |
| **Dependabot** | GitHub automated dependency update |
| **Renovate** | Multi-platform alternative to Dependabot |
| **Trivy** | Aqua Security scanner — image, FS, IaC |
| **Snyk** | Commercial SCA + SAST |
| **OSV-Scanner** | Google open-source vuln scanner |
| **SBOM** | Software Bill of Materials |
| **CycloneDX** | SBOM format OWASP |
| **SPDX** | SBOM format Linux Foundation |
| **cosign** | Sigstore CLI to sign artifacts |
| **Sigstore** | Open-source signing infra (cosign, fulcio, rekor) |
| **SLSA** | Supply-chain Levels for Software Artifacts (L1-L4) |
| **Provenance** | Verifiable record of build (who, when, what) |
| **Attestation** | Signed statement về artifact (predicate type) |
| **Pin (dep)** | Lock to exact version (with hash) |
| **EOL** | End-of-Life — no more security patch |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [02_crypto-failures-and-secure-design](02_crypto-failures-and-secure-design.md)
- → Tiếp: [04_auth-failures-logging-and-ssrf](04_auth-failures-logging-and-ssrf.md) *(sắp viết)*
- ↑ Cluster OWASP: [OWASP README](../../README.md)

### Cross-reference
- 🐳 [Docker security](../../../../10_devops/docker/lessons/02_intermediate/02_image-security-supply-chain.md)
- 🔁 [CI/CD supply chain](../../../../10_devops/ci-cd/lessons/02_intermediate/02_supply-chain-security.md)
- 🔐 [Secrets management](../../../secrets-management/)
- ☁️ [Cloud security](../../../cloud-security/)
- 🐳 [Container security](../../../container-security/)

### Tài nguyên ngoài (2026)
- 📖 [OWASP A05](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
- 📖 [OWASP A06](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)
- 📖 [OWASP A08](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)
- 📖 [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- 📖 [Mozilla Observatory](https://observatory.mozilla.org/)
- 📖 [securityheaders.com](https://securityheaders.com/)
- 📖 [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- 📖 [SLSA framework](https://slsa.dev/)
- 📖 [Sigstore](https://www.sigstore.dev/)
- 📖 [CycloneDX](https://cyclonedx.org/)
- 📖 [Syft (Anchore)](https://github.com/anchore/syft)
- 📖 [Trivy](https://aquasecurity.github.io/trivy/)
- 📖 [endoflife.date](https://endoflife.date/) — software lifecycle
- 📖 [GitHub Advisory Database](https://github.com/advisories)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 03 OWASP basic. A05 Misconfig (9 security headers, CORS, debug, default creds, S3 misconfig) + A06 Components (Dependabot, Trivy, Snyk, OSV-Scanner, triage workflow) + A08 Integrity (SLSA L1-L3, cosign, SBOM CycloneDX, pin dep, deserialize) + hands-on harden Acme Shop A → A+ + 8 pitfalls.
