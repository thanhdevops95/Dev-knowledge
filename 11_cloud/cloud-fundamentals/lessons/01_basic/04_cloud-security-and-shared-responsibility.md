# 🎓 Cloud Security & Shared Responsibility Model

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [03_storage-and-databases.md](03_storage-and-databases.md), basic IAM concepts

> 🎯 *Bài cuối cluster cloud-fundamentals. Cloud secure hơn on-prem? **Có**, nếu cấu hình đúng. **Shared Responsibility Model**: vendor lo security **OF** cloud, bạn lo security **IN** cloud. Bài này dạy: IAM, encryption, network security, compliance frameworks, common misconfigs gây breach.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Shared Responsibility Model**: vendor vs you
- [ ] **IAM** fundamentals: users, roles, policies, MFA
- [ ] **Least privilege** + **temporary credentials** patterns
- [ ] **Encryption**: at-rest, in-transit, KMS, BYOK
- [ ] **Network security**: SG, NACL, WAF, DDoS protection
- [ ] **Secrets management**: never in code
- [ ] **Compliance frameworks**: SOC2, ISO 27001, HIPAA, PCI, GDPR
- [ ] **Common breaches** + how to prevent

---

## Tình huống — Startup S3 bucket public, customer data leaked

Sáng thứ Hai, startup nhận email:
- *"We discovered your S3 bucket `acme-data` is publicly readable. Customer PII (names, emails, addresses) of 100K users accessible to anyone with URL."*
- Email từ security researcher.
- Bucket public 6 months.
- Verified: anyone could `aws s3 ls s3://acme-data/` and download.

Causes:
- Dev set `Public Read` cho testing, forgot revert.
- No alert system.
- No periodic security audit.

Damages:
- GDPR fine: up to 4% of annual revenue.
- Customer notifications (legal requirement).
- Trust loss, customer churn.
- Engineering 2 weeks on remediation.

→ **90% cloud breaches = misconfiguration**, not cloud vendor fault. Bài này dạy prevent.

---

## 1️⃣ Shared Responsibility Model

### Concept

**Cloud security = shared responsibility** between vendor and customer.

```
┌─────────────────────────────────────────┐
│         YOUR responsibility             │
│  (Security IN the cloud)                 │
│                                          │
│  - Data (encryption, classification)     │
│  - IAM users, policies, MFA              │
│  - Network config (SG, NACL)             │
│  - App security (OWASP top 10)           │
│  - OS patching (IaaS only)               │
│  - Encryption keys (BYOK)                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       VENDOR responsibility             │
│  (Security OF the cloud)                 │
│                                          │
│  - Datacenter physical security          │
│  - Network infrastructure                │
│  - Hypervisor                            │
│  - Host OS (PaaS, SaaS)                  │
│  - Hardware                              │
└─────────────────────────────────────────┘
```

### Per service model

**IaaS (EC2)**:
- Vendor: hardware, hypervisor, datacenter, network.
- You: OS patching, app, data, IAM, SG.

**PaaS (Elastic Beanstalk, RDS)**:
- Vendor: + OS, runtime, DB engine.
- You: app code, data, IAM, network rules.

**SaaS (Workspaces, Chime)**:
- Vendor: + application.
- You: data (what you upload), IAM users, SSO.

### Why this matters

Shared Responsibility Model không phải khái niệm trừu tượng — nó **quyết định ai chịu hậu quả** khi có breach. AWS bảo mật datacenter, mã hoá disk vật lý, nhưng nếu bạn để S3 bucket public hoặc IAM key trên GitHub, đó là lỗi của bạn — vendor không bồi thường, audit ghi bạn vi phạm:

- **Don't assume vendor secures everything**.
- **Don't blame vendor for your misconfig**.
- Audit + compliance: you must demonstrate IN-cloud security.

→ AWS Shared Responsibility Model is industry standard. GCP/Azure similar.

🪞 **Ẩn dụ**: *Cloud như **căn hộ chung cư cao cấp**. Chủ tòa nhà (cloud vendor) lo: an ninh sảnh, camera lối đi chung, cứu hỏa, kết cấu tòa. Bạn lo: khóa cửa căn hộ, két sắt, danh tánh khách thăm.*

---

## 2️⃣ IAM — Identity and Access Management

### Core concepts

**User**: human identity. Login + password + MFA.
**Group**: collection of users.
**Role**: identity assumed by services (EC2, Lambda) or users (cross-account).
**Policy**: JSON document defining permissions.

### Policy example

IAM policy là **JSON statement** — mỗi statement có Effect (Allow/Deny), Action (`s3:GetObject`), Resource (ARN cụ thể), và optional Condition (chỉ áp dụng khi điều kiện đúng). Ví dụ dưới đây: cho phép read+write 1 bucket cụ thể, đồng thời **deny mọi S3 request không qua HTTPS** (defence-in-depth):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": "*",
      "Condition": {
        "Bool": { "aws:SecureTransport": "false" }
      }
    }
  ]
}
```

→ Allow S3 get/put on `my-bucket`. Deny S3 over HTTP (only HTTPS).

### Principle: Least privilege

**Anti-pattern**:
```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```
→ AdministratorAccess. ⚠️ NEVER for daily use.

**Correct**:
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::my-app/data/*"
}
```
→ Only what's needed. Specific resource.

### MFA — Multi-Factor Authentication

**Required for**:
- Root account (always).
- IAM users with console access.
- IAM users with high-privilege.

**Methods**:
- TOTP (Google Authenticator, Authy).
- Hardware key (YubiKey, AWS U2F).
- SMS (least secure, avoid if possible).

**Enforce via policy**:
```json
{
  "Condition": {
    "Bool": { "aws:MultiFactorAuthPresent": "false" }
  },
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*"
}
```
→ Deny everything if MFA not present.

### Service roles (no static credentials)

**Anti-pattern**: 
```
EC2 instance has AWS access key in environment variable.
Key leaked → AWS account compromised.
```

**Correct**: **IAM role for EC2** (or IRSA for K8s):
```
EC2 assumes IAM role.
AWS provides temporary credentials (1-hour TTL).
Auto-rotated.
Never in environment.
```

```hcl
resource "aws_iam_role" "app" {
  name = "app-role"
  assume_role_policy = jsonencode({
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "app" {
  name = "app-profile"
  role = aws_iam_role.app.name
}

resource "aws_instance" "app" {
  ami = "ami-xxx"
  iam_instance_profile = aws_iam_instance_profile.app.name
  # No access keys needed!
}
```

→ Inside EC2, AWS SDK auto-gets credentials from instance metadata. No keys in code.

### IRSA — IAM Roles for Service Accounts (EKS)

K8s pod → IAM role mapping:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/app-role
```

→ Pod uses ServiceAccount, AWS SDK auto-assumes IAM role.

### Permission boundaries

Limit max permissions even with `*`:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "StringNotEquals": {
        "aws:RequestedRegion": ["us-east-1", "us-west-2"]
      }
    }
  }]
}
```
→ Even admin can only act in us-east-1, us-west-2. Useful for sandboxes.

### IAM common patterns

1. **Separate human + machine accounts**:
   - Humans: IAM user, MFA enforced.
   - Machines: IAM role, no console access.

2. **Use AWS SSO** (IAM Identity Center):
   - Central identity (Google Workspace, Okta, AD).
   - Single sign-on across AWS accounts.
   - Temporary credentials.

3. **Cross-account access**:
   - Account A has role.
   - Account B's user assumes role.
   - Centralized vs distributed control.

---

## 3️⃣ Encryption — At-rest + In-transit

### At-rest encryption

**What**: data encrypted on disk.
**Why**: physical media theft, disk reuse, snapshot leak.

**AWS services**:
- **S3**: SSE-S3 (default 2026), SSE-KMS, SSE-C.
- **EBS**: encryption at rest with KMS.
- **RDS**: encryption at rest (snapshots too).
- **DynamoDB**: encrypted by default.

**Key management**:
- **AWS managed**: keys owned by AWS, free.
- **Customer managed (KMS)**: you control, audit log, $1/key/month.
- **BYOK** (Bring Your Own Key): import key material.
- **External (Cloud HSM)**: keys in dedicated hardware.

### In-transit encryption

**What**: data encrypted over network.
**Why**: man-in-the-middle, eavesdropping.

**Standards 2026**:
- **TLS 1.3** (minimum 1.2).
- **HTTPS** for web traffic.
- **mTLS** for service-to-service (microservices).
- **VPN** for site-to-site.

**Enforce**:
- ALB/CloudFront: HTTPS only, redirect HTTP → HTTPS.
- S3 bucket policy: deny non-HTTPS.
- RDS: require SSL.

### KMS — Key Management Service

**KMS** = managed encryption key service.

```bash
# Create CMK (Customer Master Key)
aws kms create-key --description "App encryption key"

# Encrypt data
aws kms encrypt --key-id alias/app-key --plaintext "secret data"

# Decrypt
aws kms decrypt --ciphertext-blob ...
```

**Use cases**:
- S3 SSE-KMS encryption.
- EBS encryption.
- Secrets Manager.
- Encrypt small data directly.

**Envelope encryption** (for large data):
1. KMS generate data key.
2. Encrypt data with data key (locally).
3. Encrypt data key with KMS.
4. Store: encrypted data + encrypted data key.

→ Efficient for large data (don't send to KMS).

### Encryption everywhere

Production deploy 2026 phải mã hoá **end-to-end** — không có chỗ nào data đi qua dạng plaintext. Diagram dưới đây minh hoạ: TLS từ browser đến CloudFront, tiếp TLS đến ALB, tiếp TLS đến EC2, tiếp TLS đến RDS, và EBS disk được KMS mã hoá at-rest. Mỗi hop một lớp:

```
User browser ──TLS──→ CloudFront ──TLS──→ ALB ──TLS──→ EC2
                                                       ↓
                                                  TLS to RDS
                                                       ↓
                                                  KMS-encrypted EBS
```

→ Encrypted end-to-end.

---

## 4️⃣ Network security

### Defense in depth

Layered:

1. **Edge** (CloudFront + WAF): block bots, geographic.
2. **Network** (SG, NACL): restrict ports + IPs.
3. **Host** (OS firewall): additional rules.
4. **App** (auth + input validation).
5. **Data** (encryption).

→ One layer fails, others still protect.

### Security Group + NACL

(Detailed bài 02.)

- **SG**: stateful, allow only, per-resource.
- **NACL**: stateless, allow + deny, per-subnet.

### Web Application Firewall (WAF)

**WAF** = filter HTTP traffic by rules.

**Block**:
- SQL injection.
- XSS.
- Command injection.
- Bot patterns.
- Geographic (block countries).

**AWS WAF**:
- Attach to CloudFront, ALB, API Gateway.
- Rules: managed (AWS, OWASP) or custom.
- Rate limiting per IP.

**Alternatives**:
- **Cloudflare WAF**: included in plan.
- **AWS Shield**: DDoS protection (Advanced $3000/month).

### DDoS protection

**Layer 3/4 DDoS** (network flood): cloud vendors auto-mitigate at infra level.

**Layer 7 DDoS** (application flood): need WAF + rate limiting.

**Tools**:
- AWS Shield Standard (free, basic).
- AWS Shield Advanced ($3000/month, premium).
- Cloudflare Pro+ (DDoS unmetered).

### Bastion / Jump host

**Old pattern**: bastion EC2 in public subnet, SSH to private EC2.
**Modern 2026**: **AWS Systems Manager Session Manager** — no bastion needed, no SSH port.

```bash
aws ssm start-session --target i-abc123
# Direct shell, IAM auth, no SSH key, audit log
```

→ Eliminate SSH attack surface.

---

## 5️⃣ Secrets management

### Anti-patterns

❌ Secrets in code:
```python
DATABASE_PASSWORD = "supersecret123"   # Will leak in Git
```

❌ Secrets in environment variables in code:
```dockerfile
ENV DATABASE_PASSWORD=secret    # in image layer history
```

❌ Secrets in CI logs:
```yaml
- run: echo $DATABASE_PASSWORD    # leaked to logs
```

### Solutions

**AWS Secrets Manager**:
- Store secrets encrypted by KMS.
- Auto-rotation built-in (RDS, Redshift).
- Audit log via CloudTrail.

```python
import boto3
secrets = boto3.client('secretsmanager')
db_password = secrets.get_secret_value(SecretId='prod/db/password')['SecretString']
```

**AWS Parameter Store**:
- Cheaper alternative (free for Standard).
- Hierarchical paths.

**Vault** (HashiCorp):
- Multi-cloud.
- Dynamic credentials.
- (Detailed CI/CD intermediate bài 03.)

**External Secrets Operator** (K8s):
- Sync external store → K8s Secrets.

### Pre-commit secret scanning

Block secrets in commits:
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.20.0
  hooks:
    - id: gitleaks
```

→ Detect AWS keys, GitHub tokens, Stripe keys before commit.

### GitHub secret scanning

GitHub auto-scans public repos for known secret patterns. If detected:
- Notify owner.
- Some partners (AWS, Stripe) auto-revoke leaked keys.

→ Free safety net for OSS.

---

## 6️⃣ Compliance frameworks

### Common frameworks

Compliance không phải "1 chuẩn cho mọi loại". Mỗi framework phục vụ 1 domain riêng — SaaS B2B cần SOC 2, healthcare cần HIPAA, payment cần PCI DSS, EU user cần GDPR. Đa số startup khi scale gặp đồng thời 3-4 framework. Bảng dưới giúp scope đúng audit cần làm:

| Framework | Domain | Required for |
|---|---|---|
| **SOC 2** | Trust services criteria | SaaS B2B (sales requirement) |
| **ISO 27001** | Info security management | International enterprise |
| **HIPAA** | Healthcare data privacy (US) | Healthcare apps |
| **PCI DSS** | Credit card data | Payment processing |
| **GDPR** | EU privacy regulation | EU users |
| **CCPA** | California consumer privacy | California users |
| **FedRAMP** | US Federal Gov data | Selling to US Government |
| **HITRUST** | Healthcare cross-framework | Healthcare with multiple frameworks |
| **PIPEDA** | Canada privacy | Canada users |

### Compliance as differentiator

Compliance không chỉ là "tránh phạt" — nó là **chiến lược kinh doanh**. Enterprise B2B sẽ yêu cầu SOC 2 trước khi ký hợp đồng; healthcare cần HIPAA BAA mới dùng được data PHI; thẻ tín dụng phải qua PCI DSS. Đầu tư audit = unlock market — không có compliance = mất deal:

- **B2B SaaS** sales: SOC 2 mandatory ($5K+/year audit).
- **Healthcare**: HIPAA BAA (Business Associate Agreement).
- **Payment**: PCI level depends on transaction volume.
- **EU users**: GDPR compliance.

→ Compliance enables markets.

### Cloud vendors compliance

AWS/GCP/Azure: pre-certified for most frameworks:
- SOC 2 ✓
- ISO 27001 ✓
- HIPAA (with BAA) ✓
- PCI DSS Level 1 ✓
- FedRAMP High (GovCloud) ✓

→ Cloud provides infrastructure compliance. **You** must implement compliance for your application.

### SOC 2 example checklist (high-level)

- **Access control**: IAM with MFA, least privilege.
- **Encryption**: at-rest + in-transit.
- **Logging**: all admin actions logged (CloudTrail).
- **Monitoring**: alerts for security events.
- **Incident response**: documented process.
- **Background checks**: employees with prod access.
- **Vendor management**: 3rd party security reviews.
- **Change management**: PR-based deploys.
- **Backup + DR**: tested quarterly.
- **Code review**: required for all changes.

→ SOC 2 audit annually. Tooling: **Vanta**, **Drata**, **SecureFrame** automate evidence collection.

### GDPR compliance basics

(Detailed bài 01.)

- Data residency (EU data in EU region).
- Right to access + delete user data.
- Data Processing Agreement.
- DPO (Data Protection Officer) if processing certain data.
- Breach notification 72 hours.

---

## 7️⃣ Common cloud breaches + Prevention

### Breach 1: Public S3 bucket

**Scenario**: Dev sets bucket public for testing. Forgets.

**Prevention**:
1. **Block Public Access** at account level:
   ```bash
   aws s3control put-public-access-block --account-id <ID> \
     --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
   ```
2. **AWS Config** rule detect public buckets.
3. **Monthly audit** with Macie or AWS Trusted Advisor.

### Breach 2: Leaked AWS access key in Git

**Scenario**: Dev commits `aws_access_key_id` to public GitHub. Bots scan, find, mine bitcoin.

**Prevention**:
1. **Pre-commit hook**: gitleaks.
2. **GitHub secret scanning**: alerts.
3. **No static keys**: use IAM roles + SSO.
4. **MFA + Conditional access**: deny without MFA.
5. **Billing alerts**: detect anomaly.

### Breach 3: Weak DB password

**Scenario**: Postgres `admin/password`. Bots brute force.

**Prevention**:
1. **Strong passwords**: 24+ chars random.
2. **Secrets Manager**: rotate automatically.
3. **DB in private subnet**: no internet exposure.
4. **IAM database auth** (RDS Postgres): no password, IAM token.

### Breach 4: SSRF in app → cloud credentials

**Scenario**: App has SSRF vulnerability. Attacker fetches `http://169.254.169.254/` (EC2 metadata) → AWS credentials.

**Prevention**:
1. **IMDSv2**: requires session token (mitigates SSRF).
2. **App input validation**: prevent SSRF.
3. **WAF rules**: block metadata IPs in outbound.

### Breach 5: Compromised CI/CD pipeline

**Scenario**: GitHub Actions deploy key leaked. Attacker pushes malicious code.

**Prevention**:
1. **OIDC instead of long-lived keys**: GitHub Actions → AWS via OIDC token.
2. **Branch protection**: require review.
3. **Signed commits**: GPG/Sigstore.
4. **Code signing**: cosign for images.

### Breach 6: Insider threat

**Scenario**: Disgruntled employee deletes data on departure.

**Prevention**:
1. **Audit logging**: all actions in CloudTrail.
2. **Least privilege**: revoke unnecessary access.
3. **Break-glass procedures**: emergency only.
4. **Backup**: immutable retention.
5. **Offboarding checklist**: revoke access on departure.

---

## 8️⃣ Tools 2026 — Cloud security ops

### AWS native

| Tool | Use case |
|---|---|
| **IAM Access Analyzer** | Detect over-permissive policies |
| **AWS Config** | Compliance rules, configuration drift |
| **CloudTrail** | API audit log |
| **GuardDuty** | Threat detection (ML-based) |
| **Security Hub** | Aggregate findings |
| **Macie** | S3 PII detection |
| **Inspector** | EC2/Lambda vulnerability scan |
| **Detective** | Forensic investigation |
| **CloudFormation Guard** | IaC compliance check |

### Third-party

| Tool | Use case |
|---|---|
| **Wiz** | Cloud security posture management (CSPM) |
| **Lacework** | Workload + posture |
| **Snyk** | Code + IaC scanning |
| **Checkov** | IaC scanning (Terraform) |
| **tfsec** | Terraform security scan |
| **Prowler** | AWS audit |
| **ScoutSuite** | Multi-cloud audit |
| **Vanta / Drata / SecureFrame** | Compliance automation |

### Recommended baseline 2026

For startup:
- IAM Access Analyzer (free).
- GuardDuty (~$30/month for small account).
- Config (rule cost).
- Macie (audit S3 quarterly).
- tfsec in CI.
- gitleaks pre-commit.

For enterprise:
- + Security Hub (aggregator).
- + Wiz / Lacework (CSPM).
- + Vanta (compliance auto).

---

## 9️⃣ Hands-on: Secure baseline for new AWS account

### Step 1: Lock root account

1. Root account MFA hardware key.
2. Never use root for daily ops.
3. Store root credentials in offline safe.

### Step 2: Block public S3 access

```bash
aws s3control put-public-access-block --account-id $(aws sts get-caller-identity --query Account --output text) \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

### Step 3: Enable CloudTrail

```bash
aws cloudtrail create-trail \
  --name acme-trail \
  --s3-bucket-name acme-cloudtrail-logs \
  --is-multi-region-trail \
  --include-global-service-events
```

→ All API calls logged.

### Step 4: Enable GuardDuty

```bash
aws guardduty create-detector --enable
```

→ ML-based threat detection.

### Step 5: IAM Access Analyzer

```bash
aws accessanalyzer create-analyzer \
  --analyzer-name acme-analyzer \
  --type ACCOUNT
```

→ Find unintended cross-account access.

### Step 6: Config rules baseline

```bash
# Enable Config recorder
aws configservice put-configuration-recorder --configuration-recorder name=default,roleARN=arn:aws:iam::ROLE

# Subscribe to AWS managed rules
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "s3-bucket-public-read-prohibited",
  "Source": { "Owner": "AWS", "SourceIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED" }
}'
```

→ Auto-detect non-compliant resources.

### Step 7: Set up alerting

```yaml
# CloudWatch alarms
- Billing alert if > $500/month
- GuardDuty critical findings → SNS → Slack
- CloudTrail root user activity → alert
- Failed login spike → alert
```

### Step 8: Backup policy

- **AWS Backup**: automated, cross-region.
- Daily snapshots, retain 30 days.
- Test restore quarterly.

### Step 9: Network defaults

- Default VPC: delete (unused).
- Custom VPC: per-AZ subnets, NAT, SG layered.
- Block port 22, 3389 to 0.0.0.0/0.
- Use Session Manager for shell.

### Step 10: Compliance baseline

- Enable encryption-at-rest default (S3, EBS, RDS).
- Force HTTPS via bucket policy.
- Document security controls.
- Schedule quarterly internal audit.

→ This is **Day 1** baseline. Build on this.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Root account daily use

→ Root account = master key. Any compromise = total account loss.

→ **Fix**: 
- Hardware MFA on root.
- Don't use root daily.
- Create IAM admin user for ops.

### ❌ Pitfall: Long-lived access keys

→ Key in laptop → laptop stolen → key valid forever.

→ **Fix**:
- IAM roles + IAM Identity Center (SSO).
- Temporary credentials (1-12 hours).
- Auto-rotate where possible.

### ❌ Pitfall: SG `0.0.0.0/0` to internal services

→ DB exposed to internet.

→ **Fix**:
- DB SG: only allow from app SG.
- Audit SG quarterly.
- Use Inspector / Prowler.

### ❌ Pitfall: No CloudTrail

→ No audit trail. Incident investigation impossible.

→ **Fix**: CloudTrail multi-region, default Day 1.

### ❌ Pitfall: Public S3 bucket "for serving images"

→ Often misconfigured wider than intended.

→ **Fix**: CloudFront in front. Bucket private. Signed URLs or OAI.

### ❌ Pitfall: Compliance "next year"

→ Customer demands SOC 2. Scramble 6 months.

→ **Fix**: Build with compliance from Day 1. Vanta / Drata automate.

### ❌ Pitfall: No incident response plan

→ Breach happens. Confused, slow response, wider impact.

→ **Fix**:
- Documented IR plan.
- Runbook for common scenarios.
- Quarterly tabletop exercise.

### ✅ Best practice: IAM identity center for SSO

Centralized identity via Okta / Google Workspace / AD:
- One account, access many.
- Group-based permissions.
- Auto-revoke on offboarding.

### ✅ Best practice: Defense in depth

```
WAF (edge) → ALB SG (network) → EC2 SG (instance) → app auth (logic) → DB SG + encrypt (data)
```

One layer fails, others still protect.

### ✅ Best practice: Encryption everywhere

- S3: SSE-KMS default.
- EBS: encryption at rest.
- RDS: encryption at rest.
- TLS in-transit everywhere.
- Secrets in Secrets Manager.

### ✅ Best practice: Audit + alert

- Daily: cost anomaly, security findings.
- Weekly: SG audit, IAM review.
- Monthly: compliance check, dependency vulnerabilities.
- Quarterly: penetration test, DR drill, postmortem review.

---

## 🧠 Self-check

**Q1.** Shared responsibility model — vendor cụ thể lo gì với EC2?

<details>
<summary>💡 Đáp án</summary>

**AWS responsibility (Security OF the cloud)**:

1. **Physical security**:
   - Datacenter access controls.
   - Surveillance.
   - Fire suppression.

2. **Infrastructure**:
   - Network hardware (switches, routers).
   - Storage hardware.
   - Power, cooling.

3. **Hypervisor**:
   - Hardware virtualization layer.
   - Isolation between tenants.
   - Hypervisor security patches.

4. **Host OS** (for managed services):
   - Bare metal management.
   - Not your concern.

5. **AWS service security**:
   - EC2 service availability.
   - VPC routing.
   - S3 durability.

**Your responsibility (Security IN the cloud)** for EC2:

1. **Guest OS**:
   - Patch Ubuntu/RHEL/Windows.
   - Configure firewall, antivirus.

2. **Identity + Access**:
   - IAM users, roles, policies.
   - MFA.
   - Key management (SSH keys, certificates).

3. **Network config**:
   - Security Groups rules.
   - NACL.
   - VPC routing decisions.

4. **Application security**:
   - Code vulnerabilities (OWASP top 10).
   - Dependency management.
   - Input validation.

5. **Data**:
   - Encryption at-rest (KMS).
   - Encryption in-transit (TLS).
   - Backup + retention.
   - Classification (PII, PHI, PCI).

6. **Compliance**:
   - SOC 2 controls in your app.
   - HIPAA application-level.

**Gray area**:

- **Patches for managed services** (RDS, ElastiCache): AWS does, but you set maintenance window.
- **Lambda runtime**: AWS patches, but you select runtime version.

→ Roughly: **higher up the stack = more on you**.

**Service-specific shifts**:
- IaaS (EC2): more on you.
- PaaS (RDS): more on AWS.
- SaaS (Workspaces): mostly AWS.

**Common misunderstanding**:
- "AWS secures my data" — NO. AWS provides tools (encryption). You configure.
- "My app is secure because it's in AWS" — NO. Your app code is your responsibility.

→ Shared responsibility is a **partnership**, not delegation.
</details>

**Q2.** IAM least privilege — practical workflow?

<details>
<summary>💡 Đáp án</summary>

**Concept**: grant minimum permissions needed, nothing more.

**Anti-pattern**: `AdministratorAccess` policy attached to all roles. Easy but dangerous.

**Practical workflow**:

**Step 1: Start restrictive, expand on demand**:
- New service: deny all by default.
- Empty policy initially.
- Add permission when app errors with `AccessDenied`.

**Step 2: Use AWS managed policies as starting point**:
- `AmazonS3ReadOnlyAccess`.
- `AmazonEC2ContainerRegistryReadOnly`.
- Customize → custom policy.

**Step 3: Specific resource ARNs**:
```json
"Resource": "arn:aws:s3:::my-bucket/*"
```
Not:
```json
"Resource": "*"
```

**Step 4: Conditional permissions**:
```json
"Condition": {
  "StringEquals": { "aws:RequestedRegion": "us-east-1" },
  "DateGreaterThan": { "aws:CurrentTime": "2026-01-01T00:00:00Z" }
}
```

**Step 5: IAM Access Analyzer review**:
- Detect: "this role has unused permissions for 30 days".
- Trim to actual usage.

**Step 6: Permissions boundary** for delegation:
- Devs can create roles, but with max permissions defined by boundary.

**Tools**:

- **IAM Access Advisor**: shows last accessed services per role. Trim unused.
- **iamlive**: log AWS API calls during test, generate minimal policy.
- **policy_sentry**: generate least-privilege policies from CRUD patterns.
- **AWS IAM Access Analyzer**: ongoing analysis.

**Common policies to AVOID**:
- `AdministratorAccess` for daily use.
- `PowerUserAccess` (almost as bad).
- `*` action or resource without conditions.

**Audit cadence**:
- Quarterly: review all roles, remove unused.
- Monthly: check IAM Access Analyzer findings.
- Daily: alert on new role with broad permissions.

**Reality**:
- Day 1: easier to start broad, narrow over time.
- Year 2: tight policies essential.
- Year 3+: automated boundary + just-in-time access.

→ Least privilege is **culture + tooling**, not single config.
</details>

**Q3.** KMS Customer Managed Key vs AWS Managed Key — tradeoffs?

<details>
<summary>💡 Đáp án</summary>

**AWS Managed Key** (default):
- Owned by AWS.
- Free.
- No control over rotation, deletion.
- Auto-rotated by AWS.
- Cannot be deleted by you.

**Customer Managed Key (CMK)** ($1/month + API calls):
- You own.
- Define key policy (who can use).
- Manual or auto-annual rotation.
- Can delete (with 7-30 day window).
- Audit log of all uses (CloudTrail).

**Use Customer Managed Key when**:

1. **Compliance requires control**:
   - HIPAA, FedRAMP, PCI: often require customer-managed.
   - SOC 2 Trust Services Criteria: customer key control.

2. **Cross-account access**:
   - Share key with another AWS account.
   - Allow Account A's KMS to decrypt Account B's data.

3. **Granular access control**:
   - Different keys per service / per data classification.
   - Revoke key access surgically.

4. **Audit specific key usage**:
   - CloudTrail logs every encrypt/decrypt with key ID.
   - Detect anomalous use.

5. **Key rotation policy**:
   - Manual rotation triggered by event (compliance, suspected breach).
   - Vs AWS managed = annual automatic.

6. **BYOK** (Bring Your Own Key):
   - Import key material from on-prem HSM.
   - Maintain control over key generation.

**Use AWS Managed Key when**:

1. **Default encryption, low complexity**:
   - SSE-S3, EBS encryption defaults.
   - No specific compliance need.

2. **Cost-sensitive at scale**:
   - 1000+ keys × $1 = $1000/month.
   - AWS managed = free.

3. **No need for fine-grained access**:
   - All apps can encrypt/decrypt.
   - No segmentation requirements.

**Real-world recommendation**:

- **Day 1 small startup**: AWS managed (cheap, simple).
- **Day 1 with PII / sensitive**: Customer managed for sensitive resources only.
- **SOC 2 / HIPAA**: Customer managed for everything in compliance scope.

**Hybrid**:
- Customer managed for: PII, PHI, secrets, encryption keys for backups.
- AWS managed for: logs, non-sensitive temporary data.

**Cost example** (medium app):
- 10 customer managed keys = $10/month.
- 100K API calls (encrypt/decrypt) = $0.03/10K = $0.30.
- **Total**: ~$11/month for compliance-grade key management.

→ Cheap insurance for compliance + control. Use Customer Managed for anything PII+.

**Anti-pattern**: 1 key for everything. Lose key access = data unrecoverable. Compartmentalize.
</details>

**Q4.** Top 3 cloud security misconfigs causing breaches?

<details>
<summary>💡 Đáp án</summary>

Based on industry reports (Verizon DBIR, Trend Micro, Wiz):

**1. Publicly accessible storage** (S3, GCS, Azure Blob):

- Bucket policies set `"Principal": "*"`.
- Public ACL enabled.
- Object-level permissions misconfigured.
- **Examples**: Capital One (S3 + SSRF), Uber, Verizon, Pentagon.

**Prevention**:
- AWS Block Public Access (account + bucket).
- AWS Config rule.
- CSPM tools (Wiz, Lacework).
- Mandatory tagging + alerts.

**2. Exposed credentials in code/config**:

- AWS keys committed to GitHub.
- Database passwords in environment files in Docker images.
- Secrets in CI logs.
- **Examples**: Uber 2022 (AWS keys in Slack), many small startups.

**Prevention**:
- Pre-commit hooks (gitleaks).
- GitHub secret scanning.
- Secrets Manager / Vault.
- IAM roles instead of static keys.
- Rotation + alerts.

**3. Over-permissive IAM**:

- `*:*` on `*` resource.
- Long-lived access keys.
- Roles assumable by too-wide principals.
- Cross-account trust without conditions.
- **Examples**: SolarWinds, Capital One.

**Prevention**:
- Least privilege from start.
- IAM Access Analyzer.
- Permission boundaries.
- IAM Identity Center / SSO.
- Just-in-time access.
- Quarterly IAM audit.

**Honorable mentions**:

**4. Unencrypted data at rest**:
- EBS without encryption.
- RDS snapshot without encryption.
- Backups in clear text.

**5. No MFA on root**:
- Root account = master access.
- No MFA = single password = total compromise.

**6. Open security groups**:
- SSH 22 / RDP 3389 to `0.0.0.0/0`.
- DB ports exposed.
- Default VPC default SG.

**7. Outdated software**:
- EC2 unpatched.
- Container images with CVEs.
- Lambda runtime EOL.

**8. No logging / monitoring**:
- CloudTrail not enabled.
- No CloudWatch alarms.
- Incident detected only by external researcher.

**9. Insider threat / poor offboarding**:
- Ex-employee retains access.
- No access review on departure.

**10. Insecure CI/CD**:
- GitHub Actions with admin keys.
- No code review.
- Unsigned containers.

**Mitigation framework**:

1. **Day 1 baseline**: enable defaults (block public, encrypt, log, MFA).
2. **Continuous monitoring**: GuardDuty, Security Hub, CSPM.
3. **IaC + scanning**: Checkov, tfsec catch in PR.
4. **Compliance automation**: Vanta / Drata.
5. **Quarterly audit**: external pentest annually.

→ **80% of breaches are preventable** with baseline configurations + monitoring.

→ The top 3 = focus first. Get these right = prevent most breaches.
</details>

**Q5.** SOC 2 audit prep — practical timeline?

<details>
<summary>💡 Đáp án</summary>

**SOC 2 = Service Organization Control 2**, audit by CPA firm. Two types:
- **Type I**: point-in-time. "Controls exist."
- **Type II**: 6-12 months observation. "Controls work consistently."

→ Type II is the gold standard.

**Timeline**:

**Month 0**: Decide to pursue SOC 2 (typically driven by enterprise sales requirement).

**Month 0-1**: Choose scope:
- Trust Services Criteria: Security (mandatory), Availability, Confidentiality, Privacy, Processing Integrity.
- Most start: Security only.

**Month 1-3**: Gap assessment:
- Hire consultant or use automated platform (Vanta, Drata, SecureFrame).
- Map current controls vs SOC 2 requirements.
- Identify gaps.

**Month 3-6**: Implement controls:
- IAM with MFA + IAM Identity Center.
- Encryption (KMS).
- Logging (CloudTrail, audit logs).
- Monitoring + alerting (CloudWatch, GuardDuty).
- Access reviews (quarterly).
- Vendor management.
- Background checks (for prod access).
- Incident response plan + tabletop exercise.
- Change management (PR-based).
- Backup + DR testing.

**Month 6**: Initial audit (Type I):
- Auditor reviews documentation + evidence.
- Type I report: "as of June 1, 2026, controls exist."

**Month 6-12**: Observation period (Type II):
- Continue evidence collection.
- Auditor periodically samples.
- Maintain controls operationally.

**Month 12**: Type II report:
- "From June 1, 2026 to June 1, 2027, controls operated effectively."
- Annual renewal.

**Cost**:
- **Audit**: $15K-$60K depending on size + firm.
- **Vanta/Drata**: $7K-$30K/year subscription.
- **Engineering time**: 2-3 person-months upfront, 0.5/month ongoing.
- **Total Year 1**: $30K-$100K.
- **Year 2+**: $20K-$70K/year.

**Acceleration with platforms**:
- Vanta/Drata pre-built integrations:
  - AWS: auto-collect IAM, CloudTrail, Config.
  - GitHub: code review evidence.
  - Slack: incident response.
  - Notion: policy documents.
- Automated evidence collection.
- Reduce from 6+ months to 3 months prep.

**Common pitfalls**:

1. **Underestimate scope**: starting too broad.
2. **Tool-only approach**: tooling without process.
3. **Last-minute scramble**: 1 month before audit, panic.
4. **No ownership**: nobody owns compliance program.
5. **One-time effort**: SOC 2 is ongoing, not single project.

**Recommended sequence**:

1. **Engineering baseline first** (3 months):
   - IAM, encryption, logging, monitoring.
2. **Documentation second** (1 month):
   - Policies, procedures.
3. **Vanta/Drata onboarding** (1 month):
   - Connect tools, auto-collect.
4. **Gap remediation** (1-2 months):
   - Address findings.
5. **Type I audit** (1 month).
6. **Type II observation** (6 months).

**Total**: ~12 months from start to Type II report.

→ SOC 2 is achievable for startups. Plan for it as soon as enterprise sales mentioned.

**ROI**:
- Without SOC 2: enterprise customers reject. Lose deals.
- With SOC 2: door open to enterprise sales. Average enterprise contract = $50K-$500K/year.
- **Payback**: usually first 1-2 deals.

→ Treat SOC 2 as sales enabler + good security hygiene byproduct.
</details>

---

## ⚡ Cheatsheet

```bash
# === IAM ===
aws iam list-users
aws iam create-policy --policy-name MyPolicy --policy-document file://policy.json
aws iam attach-user-policy --user-name alice --policy-arn arn:aws:iam::...:policy/MyPolicy
aws iam create-access-key --user-name alice    # avoid! Use SSO

# === KMS ===
aws kms create-key --description "App key"
aws kms encrypt --key-id alias/my-key --plaintext "secret"
aws kms decrypt --ciphertext-blob fileb://encrypted.bin

# === S3 security ===
aws s3api put-public-access-block --bucket mybucket --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket mybucket --server-side-encryption-configuration ...

# === CloudTrail ===
aws cloudtrail create-trail --name myTrail --s3-bucket-name myBucket --is-multi-region-trail
aws cloudtrail start-logging --name myTrail

# === GuardDuty ===
aws guardduty create-detector --enable
aws guardduty list-findings --detector-id $DETECTOR_ID

# === Config ===
aws configservice describe-config-rules
aws configservice get-compliance-summary-by-config-rule

# === Secrets Manager ===
aws secretsmanager create-secret --name prod/db --secret-string '{"username":"admin","password":"..."}'
aws secretsmanager get-secret-value --secret-id prod/db
```

```json
// === IAM policy templates ===

// Least privilege S3 access:
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/users/${aws:userid}/*"
}

// Deny without MFA:
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "Bool": { "aws:MultiFactorAuthPresent": "false" }
  }
}

// Region restriction:
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": { "aws:RequestedRegion": ["us-east-1", "us-west-2"] }
  }
}
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Shared Responsibility Model** | Vendor + customer responsibility split |
| **IAM** | Identity and Access Management |
| **User** | Human identity in IAM |
| **Role** | Identity assumed by services/users temporarily |
| **Policy** | JSON document defining permissions |
| **Least privilege** | Grant minimum permissions necessary |
| **MFA** | Multi-Factor Authentication |
| **TOTP** | Time-based One-Time Password (Google Authenticator) |
| **Hardware key** | Physical 2FA device (YubiKey) |
| **Service role** | IAM role assumed by AWS service (EC2, Lambda) |
| **IRSA** | IAM Roles for Service Accounts (K8s) |
| **IAM Identity Center** | AWS SSO with central identity |
| **Permission boundary** | Max permissions limit on principal |
| **KMS** | Key Management Service |
| **CMK** | Customer Master Key |
| **Envelope encryption** | Encrypt data key with KMS, data with data key |
| **BYOK** | Bring Your Own Key |
| **CloudHSM** | Dedicated HSM hardware |
| **WAF** | Web Application Firewall |
| **DDoS** | Distributed Denial of Service |
| **SOC 2** | Service Organization Control 2 audit |
| **ISO 27001** | International security standard |
| **HIPAA** | US healthcare data privacy |
| **PCI DSS** | Payment card data security |
| **GDPR** | EU privacy regulation |
| **CloudTrail** | AWS API audit log |
| **GuardDuty** | AWS ML threat detection |
| **Config** | AWS resource configuration audit |
| **Macie** | AWS S3 PII detection |
| **Security Hub** | Aggregator for findings |
| **CSPM** | Cloud Security Posture Management (Wiz, Lacework) |
| **Session Manager** | SSH-less access via AWS IAM |
| **SSO** | Single Sign-On |
| **OIDC** | OpenID Connect (federated identity) |
| **Vanta/Drata/SecureFrame** | Compliance automation platforms |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [03_storage-and-databases.md](03_storage-and-databases.md)
- ↑ Cluster: [Cloud Fundamentals README](../../README.md)
- 🎯 Hoàn thành cluster cloud-fundamentals basic 5/5!

### Cross-reference
- 🔁 [CI/CD intermediate Supply chain](../../../../10_devops/ci-cd/lessons/02_intermediate/02_supply-chain-security.md) — image signing + verify
- 🔁 [CI/CD intermediate Secret mgmt](../../../../10_devops/ci-cd/lessons/02_intermediate/03_secret-management.md) — Vault + ESO
- ☸️ [K8s basic RBAC](../../../../10_devops/kubernetes/lessons/01_basic/04_namespaces-and-rbac.md) — K8s IAM
- 🏗️ [IaC basic best practices](../../../../10_devops/iac/lessons/01_basic/04_best-practices-and-alternatives.md) — IaC scan

### Tài nguyên ngoài (2026)
- 📖 [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- 📖 [AWS IAM docs](https://docs.aws.amazon.com/IAM/)
- 📖 [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- 📖 [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- 📖 [GCP Security best practices](https://cloud.google.com/security/best-practices)
- 📖 [Azure Security baseline](https://learn.microsoft.com/en-us/security/benchmark/azure/)
- 📖 [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- 📖 [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- 📖 [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- 📖 [Verizon Data Breach Investigations Report](https://www.verizon.com/business/resources/reports/dbir/)
- 📖 [Vanta](https://www.vanta.com/) / [Drata](https://drata.com/) / [SecureFrame](https://secureframe.com/) — compliance automation

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Why this matters + Policy example + Encryption everywhere + Common frameworks + Compliance as differentiator.
- **v1.0.0 (24/05/2026)** — Bài 04 — cuối cluster cloud-fundamentals basic. Shared Responsibility Model + IAM deep (users/roles/policies/MFA/SSO/IRSA) + encryption (KMS, BYOK, at-rest, in-transit) + network security (WAF, DDoS, defense in depth) + secrets management + compliance frameworks (SOC2/ISO27001/HIPAA/PCI/GDPR) + top 6 cloud breaches + tools 2026 + hands-on secure baseline. 7 pitfall + 4 best practice + 5 self-check + cheatsheet.
